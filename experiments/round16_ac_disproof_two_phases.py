"""Replay the arbitrary two-phase obstruction for additional marked pairs."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from elementary_verify import replay
from euclidean_primitive_audit import primitive_cyclic_word
from primitive_map_pairs import LETTERS, decide, fold, follow, inverse, reduce, verify_absence
from round10_ac_disproof_outsider_quotient import (
    ALPHABETS, exact_cycle, graph_rank, quotient_weights, weight_of_loop,
)
from round11_ac_disproof_wirtinger import ROSE
from round13_ac_disproof_external import check_voltage, first_ranks
from round15_ac_disproof_two_phases import check_kernel
from stallings_search import cyclic
from u_verify_voltage_phase import fold_relation, fold_word_arcs
from v_vertex_identification import fold_identification, spanning


ROOT = Path(__file__).resolve().parents[1]
AK3 = ("xxxYYYY", "xyxYXY")


def copies(pair, word):
    return (*pair, *(reduce(word + row + inverse(word)) for row in pair))


def rows_of_rank_three(pair, source):
    paths = spanning(source)[0]
    rows = {}
    for a, b in combinations(range(len(paths)), 2):
        outside = reduce(paths[a] + inverse(paths[b]))
        graph = fold_identification(source, a, b)[0]
        assert graph_rank(graph) == 3
        assert fold((*pair, outside)) == graph
        rows.setdefault(graph, (*pair, outside))
    return rows


def proper_exclusion(graph, pair, marking):
    if marking:
        weights, _ = quotient_weights(graph, marking)
        assert all(weight_of_loop(graph, weights, row, 0) == "" for row in pair)
        loops = [
            loop for alphabet in ALPHABETS for blocked in (0, 1)
            if (loop := exact_cycle(graph, weights, alphabet, blocked)) is not None
        ]
        if not loops:
            return {"method": "free_quotient", "marking": marking}
    voltage = check_voltage(graph, pair)
    if voltage["excluded_languages"] == 8:
        return {"method": "integer_characters", "voltage": voltage}
    return {"method": "unresolved", "graph": graph, "marking": marking,
            "excluded_languages": voltage["excluded_languages"]}


def census(pair):
    source = fold(pair)
    assert list(source) == fold_word_arcs(pair)
    assert graph_rank(source) == 2
    absence = verify_absence(decide(source, save_certificate=True))
    first_rank = first_ranks(source)
    assert set(first_rank) == {3}
    rank_three = rows_of_rank_three(pair, source)
    source_paths = spanning(source)[0]
    first_cases = {}
    for a, b in combinations(range(len(source_paths)), 2):
        t = reduce(source_paths[a] + inverse(source_paths[b]))
        n = fold((*pair, t))
        j = fold(copies(pair, t))
        assert graph_rank(n) == 3 and graph_rank(j) == 4
        first_cases.setdefault((n, j), []).append((a, b, t))

    proper = {graph: proper_exclusion(graph, pair, rows)
              for graph, rows in rank_three.items()}
    totals = Counter()
    records = []
    failures = []
    checksum = sha256()
    for (n, j), representatives in first_cases.items():
        t = representatives[0][2]
        generators = copies(pair, t)
        paths = spanning(j)[0]
        image = [follow(n, 0, paths[v]) for v in range(len(paths))]
        assert min(image) >= 0
        counts = Counter()
        for a, b in combinations(range(len(paths)), 2):
            s = reduce(paths[a] + inverse(paths[b]))
            cumulative = fold_identification(n, image[a], image[b])[0]
            assert tuple(fold_relation(n, (image[a], image[b]))[0]) == cumulative
            counts["second_identifications"] += 1
            if cumulative != ROSE:
                rank = graph_rank(cumulative)
                counts[f"proper_cumulative_rank_{rank}"] += 1
                if cumulative not in proper:
                    assert fold((*pair, t, s)) == cumulative
                    assert rank in (3, 4)
                    marking = (*pair, t, s) if rank == 4 else None
                    proper[cumulative] = proper_exclusion(cumulative, pair, marking)
                checksum.update(repr((t, a, b, cumulative)).encode())
                continue

            counts["ambient_cumulative_subgroup"] += 1
            graph, _ = fold_identification(j, a, b)
            assert tuple(fold_relation(j, (a, b))[0]) == graph
            assert graph == fold((*generators, s))
            try:
                assert graph_rank(graph) == 5
                receipt = check_kernel(graph, generators, s)
            except AssertionError:
                failures.append({"first": t, "second": s, "graph": graph, "rank": graph_rank(graph)})
                continue
            counts["broad_inequalities"] += receipt["broad_inequalities"]
            if receipt["refined"]:
                counts["requires_gap_refinement"] += 1
                counts["refined_inequalities"] += sum(
                    pattern["inequalities"] for pattern in receipt["refined"])
            checksum.update(repr((t, a, b, graph, receipt)).encode())
        totals.update(counts)
        records.append({"first_representatives": representatives,
                        "two_copy_vertices": len(j) // 4, **dict(counts)})

    proper_counts = Counter(receipt["method"] for receipt in proper.values())
    for graph, receipt in sorted(proper.items()):
        checksum.update(repr((graph, receipt)).encode())
    return {"source": pair, "source_absence": absence, "first_identifications": first_rank,
            "distinct_first_graph_pairs": len(first_cases), **dict(totals),
            "proper_subgroups_by_method": dict(proper_counts),
            "proper_exceptions": [r for r in proper.values() if r["method"] != "free_quotient"],
            "ambient_cumulative_failures": failures, "first_graph_pairs": records,
            "case_digest": checksum.hexdigest()}


def control():
    certificate = json.loads((ROOT / "certificates/round16_ac_disproof_ak2_two_phase.json").read_text())
    assert [step["op"] for step in certificate["moves"]] == [
        "conjugate", "multiply", "conjugate", "conjugate", "conjugate", "multiply",
    ]
    checked = replay(certificate)
    assert primitive_cyclic_word(cyclic(checked["endpoint"][0]))
    pair = tuple(certificate["start"])
    first, second = "X", "Y"
    assert fold((*pair, first, second)) == fold((*copies(pair, first), second)) == ROSE
    return {"start": pair, "strict_replay": checked, "first_phase": 1, "second_phase": 3,
            "primitive_cyclic_word": cyclic(checked["endpoint"][0]),
            "separate_envelope_escape": {"first": first, "second": second, "rank": 2}}


def external_pairs():
    path = ROOT / "results/round13_stable_proof_whitehead.json"
    pairs = json.loads(path.read_text())["coverage32"]["shortest_absent"][:4]
    assert all(sum(map(len, pair)) == 23 for pair in pairs)
    return tuple(map(tuple, pairs))


def main():
    parser = argparse.ArgumentParser()
    sources = parser.add_mutually_exclusive_group()
    sources.add_argument("--projection", type=int, choices=range(1, 5))
    sources.add_argument("--all-projections", action="store_true")
    args = parser.parse_args()
    if args.projection:
        print(json.dumps(census(external_pairs()[args.projection - 1]), indent=2))
        return
    if args.all_projections:
        projections = [census(pair) for pair in external_pairs()]
        assert [case["ambient_cumulative_subgroup"] for case in projections] == [
            8297, 8300, 6790, 4852,
        ]
        assert all(not case["ambient_cumulative_failures"] for case in projections)
        assert all("unresolved" not in case["proper_subgroups_by_method"] for case in projections)
        print(json.dumps(projections, indent=2))
        return
    original = census(AK3)
    assert original["ambient_cumulative_subgroup"] == 1608
    assert not original["ambient_cumulative_failures"]
    assert "unresolved" not in original["proper_subgroups_by_method"]
    print(json.dumps({"literal_AK3": original, "AK2_positive_control": control()}, indent=2))


if __name__ == "__main__":
    main()
