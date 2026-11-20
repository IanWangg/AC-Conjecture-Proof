"""Exclude isolated short activated intervals in the degree-nine retraction."""

from collections import Counter
from functools import cache
from itertools import permutations
import json

from round01_stable_disproof_search import AK3, MagnusQuotient, ONE
from round06_stable_disproof_tiers import apply, instruction_labels
from round10_stable_disproof_neighborhood import pack
from round10_stable_disproof_saturate import corridor_data, saturation, widths
from round11_stable_disproof_symbolic4 import candidates, exponent_difference, inverse, pair_ball, parity, reduce
from round12_stable_disproof_symbolic6 import cyclic_relation, degree_three_evaluations, rewrites, substitute_removed


def project(state):
    return tuple(value for value, _ in state)


def search():
    low = MagnusQuotient(2, 9)
    menu = tuple(instruction_labels(3, 2, False))
    geodesics, _ = saturation()
    assert widths(geodesics) == corridor_data()
    idle_layers = [
        {tuple(sorted(((pack(a), 0), (pack(b), 0), (ONE, 1)))) for a, b in layer}
        for layer in geodesics
    ]

    @cache
    def active_neighbors(state):
        low_values, marks = zip(*state)
        children = set()
        for move in menu:
            moved = apply(low, low_values, move)
            if ONE in moved or tuple(sorted(moved)) == low_values:
                continue
            moved_marks = marks
            if move[0] == "multiply":
                _, i, j, _ = move
                moved_marks = marks[:i] + (marks[i] ^ marks[j],) + marks[i + 1:]
            children.add(tuple(sorted(zip(moved, moved_marks))))
        return children

    def active_layer(states, distance):
        for _ in range(distance):
            states = {child for state in states for child in active_neighbors(state)}
        return states

    records = []
    for span in (2, 3, 4, 5, 6):
        left_depth = span // 2
        right_depth = span - left_depth
        windows = []
        for t in range(len(idle_layers) - span + 1):
            left = active_layer(idle_layers[t], left_depth)
            right = active_layer(idle_layers[t + span - 1], right_depth)
            low_meeting = {project(state) for state in left} & {project(state) for state in right}
            windows.append({"entry_tick": t, "exit_geodesic_tick": t + span - 1,
                            "marked_half_widths": [len(left), len(right)],
                            "degree_nine_midpoints": len(low_meeting),
                            "marked_midpoints": len(left & right)})
        assert all(window["marked_midpoints"] == 0 for window in windows)
        records.append({"excursion_instructions": span, "half_depths": [left_depth, right_depth],
                        "windows_with_degree_nine_midpoints": sum(w["degree_nine_midpoints"] > 0 for w in windows),
                        "windows": windows})
    assert [record["windows_with_degree_nine_midpoints"] for record in records[:2]] == [9, 6]
    return {"rank_two_projection_degree": 9, "z_coefficient_modulus": 2, "middle_budget": 18,
            "compressed_budget": 17, "geodesic_layer_widths": widths(geodesics), "active_windows": records}


@cache
def marked_formal_children(rows, mask):
    children = set()
    for i, receiver in enumerate(rows):
        options = {(inverse(receiver), mask)}
        for letter in "xXyY":
            options.add((reduce(letter + receiver + inverse(letter)), mask))
        for j, donor in enumerate(rows):
            if i != j:
                changed = mask ^ (1 << i) if mask & (1 << j) else mask
                options.update((reduce(receiver + word), changed) for word in (donor, inverse(donor)))
        children.update((rows[:i] + (image,) + rows[i + 1:], changed)
                        for image, changed in options if image and image != receiver)
    return children


def templates(span):
    layer = {(("a", "b", copy), 4) for copy in "aA"}
    for _ in range(span - 2):
        layer = {child for state in layer for child in marked_formal_children(*state)}
    terminal = set()
    for rows, mask in layer:
        if mask not in (1, 2, 4):
            continue
        i = mask.bit_length() - 1
        removed = rows[i]
        remaining = tuple(sorted(rows[:i] + rows[i + 1:]))
        for j, donor in enumerate(rows):
            if i != j and parity(donor) == parity(removed):
                terminal.add((removed, donor, remaining))
                terminal.add((removed, inverse(donor), remaining))
    return len(layer), terminal


def classify(span, radius, cases, solutions):
    counts = Counter()
    residual = []
    for removed, donor, pair in sorted(cases):
        if pair in radius:
            counts["literal_replacement"] += 1
            continue
        if substitute_removed(removed, donor, pair) in radius:
            counts["restated_last_equality"] += 1
            continue
        if any(value % 16 for value in exponent_difference(removed, donor)):
            counts["abelianization_modulo_sixteen"] += 1
            continue
        relation = cyclic_relation(removed + inverse(donor))
        if not solutions(relation):
            counts["degree_three_obstruction"] += 1
            continue
        if any(tuple(sorted((a, b))) in radius for a in rewrites(pair[0], relation)
               for b in rewrites(pair[1], relation)):
            counts["two_rewrites_per_row"] += 1
        else:
            residual.append({"removed": removed, "signed_donor": donor,
                             "remaining_pair": pair, "last_equality_class": relation})
    assert sum(counts.values()) + len(residual) == len(cases)
    return {"excursion_instructions": span, "formal_rank_two_radius": span - 1,
            "formal_rank_two_ball": len(radius), "terminal_templates": len(cases),
            "counts": counts, "unresolved_templates": residual}


def symbolic_savings():
    _, _, solutions = degree_three_evaluations()
    unmarked = []
    isolated = []
    for span in (4, 5, 6):
        radius = pair_ball(span - 1)
        unmarked.append(classify(span, radius, set(candidates(span)), solutions))
        marked_width, cases = templates(span)
        record = classify(span, radius, cases, solutions)
        assert not record["unresolved_templates"]
        record["last_marked_layer_width"] = marked_width
        isolated.append(record)
    assert [len(row["unresolved_templates"]) for row in unmarked] == [0, 0, 136]
    return {"unrestricted_interval_templates": unmarked, "isolated_interval_templates": isolated}


def three_six_instruction_intervals(cases):
    group = MagnusQuotient(2, 9)

    @cache
    def idle_successors(pair):
        neighbors = set()
        for a, b in permutations(pair):
            letters = dict(zip("abxy", (a, b, *group.generators)))
            letters.update({c.upper(): group.inverse(value) for c, value in tuple(letters.items())})

            @cache
            def evaluate(word):
                value = ONE
                for letter in word:
                    value = group.multiply(value, letters[letter])
                return value

            for case in cases:
                if evaluate(case["removed"]) == evaluate(case["signed_donor"]):
                    neighbors.add(tuple(sorted(map(evaluate, case["remaining_pair"]))))
        return neighbors

    endpoints = [tuple(sorted(map(group.evaluate, AK3))), tuple(sorted(group.generators))]
    one_interval = [idle_successors(endpoint) for endpoint in endpoints]
    two_intervals = [{successor for pair in pairs for successor in idle_successors(pair)} for pairs in one_interval]
    midpoints = [len(one_interval[0] & two_intervals[1]), len(two_intervals[0] & one_interval[1])]
    assert midpoints == [0, 0]
    return {"residual_templates": len(cases), "one_interval_widths": list(map(len, one_interval)),
            "two_interval_widths": list(map(len, two_intervals)), "midpoints": midpoints}


if __name__ == "__main__":
    symbolic = symbolic_savings()
    residual = symbolic["unrestricted_interval_templates"][-1]["unresolved_templates"]
    print(json.dumps({"geodesic_search": search(), **symbolic,
                      "three_six_instruction_intervals": three_six_instruction_intervals(residual)}, indent=2))
