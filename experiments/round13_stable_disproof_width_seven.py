"""Test all isolated seven-instruction excursions in the degree-nine retraction."""

from collections import Counter, defaultdict
from functools import cache
from itertools import permutations
import json

from round01_stable_disproof_search import MagnusQuotient, ONE
from round06_stable_disproof_tiers import apply, instruction_labels
from round10_stable_disproof_neighborhood import pack
from round10_stable_disproof_saturate import corridor_data, saturation, widths
from round11_stable_disproof_symbolic4 import candidates, exponent_difference, inverse, pair_ball, reduce
from round12_stable_disproof_short_savings import marked_formal_children
from round12_stable_disproof_symbolic6 import cyclic_relation, degree_three_evaluations, rewrites, substitute_removed


def strict_comparison():
    radius = pair_ball(6)
    _, _, solutions = degree_three_evaluations()
    counts = Counter()
    pending = set()
    for removed, donor, pair in candidates(7):
        if pair in radius:
            counts["literal_replacement_occurrences"] += 1
        elif substitute_removed(removed, donor, pair) in radius:
            counts["last_equality_replacement_occurrences"] += 1
        elif any(value % 16 for value in exponent_difference(removed, donor)):
            counts["exponent_obstruction_occurrences"] += 1
        else:
            counts["other_template_occurrences"] += 1
            pending.add((removed, donor, pair))

    unique_counts = Counter()
    residual = set()
    for removed, donor, pair in sorted(pending):
        equality = cyclic_relation(removed + inverse(donor))
        if not solutions(equality):
            unique_counts["degree_three_obstruction"] += 1
        elif any(tuple(sorted((a, b))) in radius for a in rewrites(pair[0], equality)
                 for b in rewrites(pair[1], equality)):
            unique_counts["last_equality_rewrites"] += 1
        else:
            residual.add((removed, donor, pair))
    assert len(residual) == 5730
    return residual, {"formal_radius_six_pairs": len(radius), "template_occurrences": counts,
                      "distinct_remaining_templates": len(pending), "covered_remaining_templates": unique_counts,
                      "residual_templates": len(residual)}


def geodesic_windows():
    low = MagnusQuotient(2, 9)
    geodesics, _ = saturation()
    assert widths(geodesics) == corridor_data()
    idle = [{tuple(sorted((ONE, pack(a), pack(b)))) for a, b in layer} for layer in geodesics]

    @cache
    def active_neighbors(state):
        return {child for child in low.neighbors(state, True) if ONE not in child}

    def at_distance(layer, distance):
        for _ in range(distance):
            layer = {child for state in layer for child in active_neighbors(state)}
        return layer

    records = []
    for tick in range(len(idle) - 6):
        left = at_distance(idle[tick], 3)
        right = at_distance(idle[tick + 6], 4)
        count = len(left & right)
        assert count == 0
        records.append({"entry_tick": tick, "exit_geodesic_tick": tick + 6,
                        "degree_nine_half_widths": [len(left), len(right)], "midpoints": count})
    return records


def marked_targets(residual):
    targets = defaultdict(set)
    for removed, donor, pair in residual:
        for order in permutations(range(3)):
            recipient = order.index(0)
            values = (removed, *pair)
            rows = tuple(values[index] for index in order)
            state = rows, 1 << recipient
            for j, word in enumerate(rows):
                if j == recipient:
                    continue
                if word == donor:
                    targets[state].add(("multiply", recipient, j, -1))
                if word == inverse(donor):
                    targets[state].add(("multiply", recipient, j, 1))
    return targets


def formal_step(state, move):
    rows, mask = state
    op, i, *operands = move
    word = rows[i]
    if op == "multiply":
        j, sign = operands
        donor = rows[j] if sign == 1 else inverse(rows[j])
        image = reduce(word + donor)
        mask ^= ((mask >> j) & 1) << i
    elif op == "invert":
        image = inverse(word)
    else:
        j, sign = operands
        letter = "xy"[j] if sign == 1 else "XY"[j]
        image = reduce(letter + word + inverse(letter))
    if not image or image == word:
        return None
    return rows[:i] + (image,) + rows[i + 1:], mask


def terminal_template(state, move):
    rows, _ = state
    _, i, j, sign = move
    donor = rows[j] if sign == -1 else inverse(rows[j])
    return rows[i], donor, tuple(sorted(rows[:i] + rows[i + 1:]))


def degree_two_lift(residual):
    targets = marked_targets(residual)
    target_states = set(targets)
    forward = [{(("a", "b", copy), 4) for copy in "aA"}]
    for _ in range(4):
        forward.append({child for state in forward[-1] for child in marked_formal_children(*state)})

    allowed = [set() for _ in range(6)]
    for state in forward[4]:
        hits = marked_formal_children(*state) & target_states
        if hits:
            allowed[4].add(state)
            allowed[5].update(hits)
    for tick in range(3, -1, -1):
        allowed[tick] = {state for state in forward[tick] if marked_formal_children(*state) & allowed[tick + 1]}
    marked_case_count = len({terminal_template(state, move) for state in allowed[5] for move in targets[state]})
    assert marked_case_count == 1440

    menu = tuple(instruction_labels(3, 2, False))
    edges = [{state: [(child, move) for move in menu
                     if (child := formal_step(state, move)) in allowed[tick + 1]] for state in allowed[tick]}
             for tick in range(5)]
    high = MagnusQuotient(3, 2)
    z = high.generators[2]
    mixed_mask = sum(1 << (high.offset[2] + 3 * i + j) for i in range(3) for j in range(3) if 2 in (i, j))
    markings = {1: (1,), 2: (2,), 3: (1, 2)}
    checks = []
    survivors = set()
    for alpha, beta in permutations(markings, 2):
        a = high.evaluate(markings[alpha])
        b = high.evaluate(markings[beta])
        layer = {(state, (a, b, high.multiply(z, a if state[0][2] == "a" else high.inverse(a))))
                 for state in allowed[0]}
        layer_widths = [len(layer)]
        for transitions in edges:
            layer = {(child, apply(high, values, move)) for state, values in layer for child, move in transitions[state]}
            layer_widths.append(len(layer))
        admitted = {terminal_template(state, move) for state, values in layer for move in targets[state]
                    if all(value & mixed_mask == 0 for value in apply(high, values, move))}
        checks.append({"old_linear_parts": [alpha, beta], "lifted_layer_widths": layer_widths,
                       "surviving_templates": len(admitted)})
        survivors.update(admitted)
    assert survivors == expected_square_templates()
    return {"marked_symbolic_layer_widths": widths(allowed), "terminals_restoring_linear_marking": marked_case_count,
            "quadratic_lift_checks": checks, "surviving_square_templates": sorted(survivors)}


def expected_square_templates():
    cases = set()
    for conjugator in "xXyY":
        positive = conjugator + "aaa" + inverse(conjugator)
        negative = inverse(positive)
        first = tuple(sorted(("aa" + negative + "aa", "b")))
        second = tuple(sorted(("aaaa" + negative, "b")))
        cases.add((negative + "aa", "AA" + positive + "AA", first))
        cases.add((positive + "AA", "aaaa" + negative, second))
    return cases


if __name__ == "__main__":
    residual, strict = strict_comparison()
    quadratic = degree_two_lift(residual)
    geodesic = geodesic_windows()
    print(json.dumps({"strict_comparison": strict, "marked_and_quadratic_checks": quadratic,
                      "strict_saving_geodesic_windows": geodesic}, indent=2, sort_keys=True))
