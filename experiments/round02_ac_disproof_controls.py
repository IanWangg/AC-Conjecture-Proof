"""Check the lobe-pair premise, the long bridge guards, and two AK(2) controls."""

import argparse
from collections import deque
from itertools import combinations, product
import json
from pathlib import Path
import random

from primitive_map_pairs import ALPHABETS, LETTERS, decide, fold, follow, inverse, reduce, verify_absence
from round01_ac_disproof_barbells import character_record, rotations, source_graph, sources
from v_vertex_identification import spanning, word_voltage


POWER = "xxxYYYY"
BRAID = "xyxYXY"
FAMILY_POWER = "YYYYxxx"


def signed_graphs_acyclic(graph):
    """Check signed double-free transition graphs by topological sorting."""
    for alphabet in ALPHABETS:
        labels = [LETTERS.index(letter) for letter in alphabet]
        states = {
            (v, label)
            for v in range(len(graph) // 4)
            for label in labels
            if graph[4 * v + label] >= 0
        }
        for forbidden in labels:
            indegree = dict.fromkeys(states, 0)
            arrows = {}
            for v, label in states:
                end = graph[4 * v + label]
                arcs = [
                    (end, other)
                    for other in labels
                    if (end, other) in states and (label, other) != (forbidden, forbidden)
                ]
                arrows[v, label] = arcs
                for target in arcs:
                    indegree[target] += 1
            frontier = deque(key for key in states if indegree[key] == 0)
            visited = 0
            while frontier:
                at = frontier.popleft()
                visited += 1
                for target in arrows[at]:
                    indegree[target] -= 1
                    if indegree[target] == 0:
                        frontier.append(target)
            if visited != len(states):
                return False
    return True


def lobe_rotations():
    tests = []
    for left, right in ((POWER, POWER), (POWER, BRAID), (BRAID, BRAID)):
        exact_states = 0
        graph_count = 0
        for a, b in product(rotations(left), rotations(right)):
            certificate = decide(fold((a, b)), save_certificate=True)
            assert certificate["status"] == "ABSENT"
            exact_states += verify_absence(certificate)["closed_map_pair_states_checked"]
            graph_count += 1
        tests.append(
            {"lobes": [left, right], "rotation_pairs": graph_count, "map_pair_states": exact_states}
        )
    return tests


def maximum_y_run(graph):
    vertices = len(graph) // 4
    lengths = []
    for start in range(vertices):
        length = 0
        while follow(graph, start, "y" * (length + 1)) >= 0:
            length += 1
            assert length < vertices, "pure y cycle"
        lengths.append(length)
    return max(lengths)


def guarded_bridge():
    # The proof uses the local neighbourhoods, not extrapolation from samples.
    # Subwords of length at most seven that use a lobe edge stay near one end.
    m = 18
    bridge = "x" + "y" * m
    _, graph = source_graph(FAMILY_POWER, BRAID, bridge)
    signed = [word for lobe in (POWER, BRAID) for a in rotations(lobe) for word in (a, inverse(a))]
    readings = {}
    for word in signed + [bridge]:
        hits = [v for v in range(len(graph) // 4) if follow(graph, v, word) >= 0]
        assert len(hits) == 1
        readings[word] = hits[0]
    largest_rotation_run = max(
        maximum_y_run(fold((p, b)))
        for p, b in product(rotations(POWER), rotations(BRAID))
    )
    assert largest_rotation_run < m
    return {
        "power": FAMILY_POWER,
        "braid": BRAID,
        "local_example_bridge": bridge,
        "unique_reading_starts": readings,
        "maximum_y_run_in_earlier_rotation_cores": largest_rotation_run,
        "maximum_y_run_bound_in_bridge_cap5_cores": 16,
    }


def rebased_join(basis, paths, a, b):
    # This independently constructs the same subgroup from four based
    # words, using the batch bouquet fold rather than the native join.
    rebased = [
        reduce(inverse(paths[v]) + word + paths[v])
        for v in (a, b)
        for word in basis
    ]
    return fold(rebased)


def audit_joins(basis, graph, expect_primitive=False):
    paths, *_ = spanning(graph)
    checked = dag_exclusions = finite_states = 0
    positive = []
    for a, b in combinations(sorted(paths), 2):
        joined = rebased_join(basis, paths, a, b)
        if signed_graphs_acyclic(joined):
            dag_exclusions += 1
        decision = decide(joined, save_certificate=True)
        if decision["status"] == "PRIMITIVE":
            assert expect_primitive
            positive.append({"vertices": [a, b], "witness": decision["witness"]})
        else:
            assert decision["status"] == "ABSENT"
            finite_states += verify_absence(decision)["closed_map_pair_states_checked"]
        checked += 1
    return {
        "checked_joins": checked,
        "dag_exclusions": dag_exclusions,
        "closed_map_states": finite_states,
        "primitive_joins": positive,
    }


def controls():
    literal = ("xxYYY", BRAID)
    result = audit_joins(literal, fold(literal), expect_primitive=True)
    assert len(result["primitive_joins"]) == 3
    p, b, bridge = "xYYYx", "yxYXYx", "y"
    basis, graph = source_graph(p, b, bridge)
    barbell = audit_joins(basis, graph)
    assert barbell["checked_joins"] == 55
    paths, *_ = spanning(graph)
    quotient = character_record(basis, graph, paths, 0, 3)
    primitive = "xYxYYxYY"
    a, bword = "x", "Y"
    for move in "RLRL":
        if move == "R":
            a += bword
        else:
            bword = a + bword
    assert bword == primitive
    assert follow(quotient["graph"], 2, primitive) == 2
    assert word_voltage(quotient["graph"], quotient["edge_voltages"], primitive, 2) == 0
    barbell["larger_kernel_witness"] = {
        "identified_vertices": [0, 3], "loop_vertex": 2, "primitive": primitive,
        "positive_basis_program": "RLRL", "extra_generator": quotient["extra_generator"],
        "voltage": 0,
    }
    return {"literal_AK2": result, "disjoint_AK2_barbell": barbell}


def sample_reference():
    rng = random.Random(20261119)
    report = {}
    for length in range(1, 9):
        checked = 0
        for _ in range(5):
            bridge = rng.choice(LETTERS)
            for _ in range(length - 1):
                bridge += rng.choice([letter for letter in LETTERS if letter != inverse(bridge[-1])])
            p, b = rng.choice(list(sources(3, bridge)))
            basis, graph = source_graph(p, b, bridge)
            paths, *_ = spanning(graph)
            for a, z in combinations(sorted(paths), 2):
                assert signed_graphs_acyclic(rebased_join(basis, paths, a, z))
                checked += 1
        report[str(length)] = {"sample_sources": 5, "checked_joins": checked}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("native_summary", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    native = json.loads(args.native_summary.read_text())
    assert set(native) == {str(i) for i in range(1, 9)}
    for key, row in native.items():
        length = int(key)
        n = 12 + length
        assert row["sources"] == 42 * 3 ** (length - 1)
        assert row["vertex_pairs"] == row["sources"] * n * (n - 1) // 2
        assert row["DAG_exclusions"] == row["vertex_pairs"]
        assert row["DAG_unresolved"] == 0
        assert row["join_ranks"] == {"4": row["vertex_pairs"]}
    result = {
        "ordinary_AC_goal_solved": False,
        "native_by_bridge_length": native,
        "native_total_sources": sum(row["sources"] for row in native.values()),
        "native_total_joins": sum(row["vertex_pairs"] for row in native.values()),
        "independent_four_word_folds": sample_reference(),
        "exact_lobe_rotation_tests": lobe_rotations(),
        "arbitrary_length_family": guarded_bridge(),
        "controls": controls(),
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
