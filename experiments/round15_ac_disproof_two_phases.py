"""Check two independent-conjugation phases for the external energy-24 pair."""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from elementary_verify import replay
from euclidean_primitive_audit import primitive_cyclic_word
from primitive_map_pairs import LETTERS, fold, follow, inverse, reduce
from round10_ac_disproof_outsider_quotient import graph_rank
from round11_ac_disproof_wirtinger import ROSE, verify_single_voltage
from round13_ac_disproof_external import PAIR, kernel_basis
from stallings_search import cyclic
from u_verify_voltage_phase import fold_relation, voltage_word
from v_vertex_identification import fold_identification, spanning
from v_voltage_cycle_review import components, potential, review


ROOT = Path(__file__).resolve().parents[1]


def signed_pattern_edges(graph, weights, alphabet, forbidden):
    states = [
        (vertex, ''.join(history))
        for vertex in range(len(graph) // 4)
        for history in product(alphabet, repeat=2)
        if ''.join(history) not in forbidden
    ]
    indices = {state: index for index, state in enumerate(states)}
    edges = []
    for index, (vertex, prior) in enumerate(states):
        for letter in alphabet:
            edge = 4 * vertex + LETTERS.index(letter)
            window = prior + letter
            if graph[edge] >= 0 and all(pattern not in window for pattern in forbidden):
                target = indices[graph[edge], window[-2:]]
                edges.append((index, target, weights[edge]))
    return tuple(range(len(states))), edges


def verify_refinement(graph, weights, alphabet, forbidden):
    states, edges = signed_pattern_edges(graph, weights, alphabet, forbidden)
    reach = {state: {state} for state in states}
    for start, end, _ in edges:
        reach[start].add(end)
    for middle in states:
        for start in states:
            if middle in reach[start]:
                reach[start].update(reach[middle])
    groups = {frozenset(end for end in reach[start] if start in reach[end]) for start in states}
    by_group = []
    for group in components(states, edges):
        group_set = frozenset(group)
        assert group_set in groups
        groups.remove(group_set)
        inside = [(a, b, w) for a, b, w in edges if a in group_set and b in group_set]
        if not inside:
            continue
        values = potential(group, inside, 1)
        sign = 1
        if values is None:
            values = potential(group, inside, -1)
            sign = -1
        assert values is not None
        saved = dict(zip(group, values))
        for start, end, value in inside:
            assert saved[end] - saved[start] <= len(group) * sign * value - 1
        by_group.append([group, sign, values, len(inside)])
    assert not groups
    return {"alphabet": alphabet, "forbidden": forbidden, "components": by_group,
            "inequalities": sum(row[-1] for row in by_group)}


def check_kernel(graph, generators, added):
    _, chords, arcs, coordinates = spanning(graph)
    rows = [coordinates(word) for word in generators]
    character, = kernel_basis(rows)
    assert len(character) == len(chords) == len(generators) + 1
    new_voltage = sum(a * b for a, b in zip(character, coordinates(added)))
    assert new_voltage in (-1, 1)
    weights = [0] * len(graph)
    for (vertex, letter, _), (index, sign) in arcs.items():
        weights[4 * vertex + letter] = sign * character[index] * new_voltage
    assert all(voltage_word(graph, weights, word) == 0 for word in generators)
    assert voltage_word(graph, weights, added) == 1
    for edge, end in enumerate(graph):
        if end >= 0:
            vertex, letter = divmod(edge, 4)
            assert weights[edge] == -weights[4 * end + (letter ^ 1)]

    broad = review(graph, weights)["checks"]
    inequalities = 0
    refined = []
    for test in broad:
        if test["status"] == "PASS":
            inequalities += verify_single_voltage(graph, weights, test)
            continue
        letters = [LETTERS[index] for index in test["alphabet"]]
        isolated = letters[test["forbidden_double"]]
        other = letters[1 - test["forbidden_double"]]
        for pattern in (isolated + other + isolated, other * 3):
            refined.append(verify_refinement(graph, weights, ''.join(letters),
                                             (isolated * 2, pattern)))
    return {"character": [value * new_voltage for value in character],
            "broad_inequalities": inequalities, "refined": refined,
            "broad_tests": broad}


def both_copies(word):
    return (*PAIR, *(reduce(word + row + inverse(word)) for row in PAIR))


def census():
    source = fold(PAIR)
    source_paths = spanning(source)[0]
    first_cases = {}
    for first, second in combinations(range(len(source_paths)), 2):
        t = reduce(source_paths[first] + inverse(source_paths[second]))
        n = fold((*PAIR, t))
        assert n == fold_identification(source, first, second)[0]
        assert graph_rank(n) == 3
        j = fold(both_copies(t))
        assert graph_rank(j) == 4
        first_cases.setdefault((n, j), []).append((first, second, t))

    records = []
    totals = Counter()
    checksum = sha256()
    refinements = {}
    for (n, j), representatives in first_cases.items():
        t = representatives[0][2]
        generators = both_copies(t)
        paths = spanning(j)[0]
        image = []
        for v in paths:
            image.append(follow(n, 0, paths[v]))
            assert image[-1] >= 0
        counts = Counter()
        for a, b in combinations(range(len(paths)), 2):
            second = reduce(paths[a] + inverse(paths[b]))
            cumulative = tuple(fold_relation(n, (image[a], image[b]))[0])
            assert cumulative == fold_identification(n, image[a], image[b])[0]
            counts["second_identifications"] += 1
            if cumulative != ROSE:
                counts["proper_cumulative_subgroup"] += 1
                checksum.update(repr((t, a, b, cumulative)).encode())
                continue

            counts["ambient_cumulative_subgroup"] += 1
            graph, _ = fold_identification(j, a, b)
            assert tuple(fold_relation(j, (a, b))[0]) == graph
            assert graph == fold((*generators, second))
            assert graph_rank(graph) == 5
            receipt = check_kernel(graph, generators, second)
            counts["broad_inequalities"] += receipt["broad_inequalities"]
            if receipt["refined"]:
                counts["requires_gap_refinement"] += 1
                counts["refined_inequalities"] += sum(
                    pattern["inequalities"] for pattern in receipt["refined"])
                refinements.setdefault(graph, {
                    "first_relative_word": t, "second_relative_word": second,
                    "folded_graph": graph, "character": receipt["character"],
                    "refinements": receipt["refined"],
                })
            checksum.update(repr((t, a, b, graph, receipt)).encode())
        totals.update(counts)
        records.append({"first_representatives": representatives,
                        "two_copy_vertices": len(j) // 4, **dict(counts)})
    assert len(first_cases) == 68
    assert totals["ambient_cumulative_subgroup"] == 9267
    assert totals["requires_gap_refinement"] == 70
    assert len(refinements) == 2
    return {"source": PAIR, "first_representative_count": sum(map(len, first_cases.values())),
            "distinct_first_graph_pairs": len(first_cases), **dict(totals),
            "first_graph_pairs": records, "exceptional_graphs": list(refinements.values()),
            "case_digest": checksum.hexdigest()}


def ak2_control():
    prefix = json.loads((ROOT / "certificates/t_v_ak2_candidate_prefix.json").read_text())
    full = json.loads((ROOT / "certificates/t_v_ak2_hidden_full.json").read_text())
    prelude = prefix["moves"][:6]
    phase = prefix["moves"][6:]
    waypoint = full["primitive_waypoint"]
    suffix = full["moves"][len(prefix["moves"]):full["waypoint_prefix_moves"]]
    assert all(move["op"] != "conjugate" for move in (*prelude, *suffix))
    assert all(move["op"] == "conjugate" for move in phase)
    assert full["moves"][:len(prefix["moves"])] == prefix["moves"]
    receipt = replay({**prefix, "target": waypoint, "moves": (*prelude, *phase, *suffix)})
    coordinate = full["primitive_coordinate"]
    assert primitive_cyclic_word(cyclic(waypoint[coordinate]))
    return {"original_start": prefix["start"], "prelude_moves": len(prelude),
            "single_conjugation_phase_moves": len(phase), "suffix_moves": len(suffix),
            "primitive_coordinate": coordinate, "primitive_cyclic_word": cyclic(waypoint[coordinate]),
            "waypoint_replay": receipt, "basis_replay": replay(full)}


if __name__ == "__main__":
    print(json.dumps({"two_phase_census": census(), "AK2_positive_control": ak2_control()},
                     indent=2))
