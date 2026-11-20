"""Check the normal-closure obstruction for every proper small-rank overgroup."""

import json
from itertools import combinations
from math import gcd

from primitive_map_pairs import LETTERS, fold, inverse, reduce
from round09_rank_two_overgroups import AK3, ENERGY17, ROSE, census, rank
from round10_one_outside_kernel import build, read_old
from u_verify_voltage_phase import verify_cycles, voltage_word
from v_vertex_identification import cross, fold_identification, spanning
from v_voltage_cycle_review import review
from verify_vertex_voltage import verify


def extra_character(graph, rows):
    paths, chords, arcs, coordinates = spanning(graph)
    row_coordinates = [coordinates(word) for word in rows]
    character = cross(*row_coordinates)
    divisor = gcd(*character)
    assert divisor
    character = [value // divisor for value in character]
    weights = [0] * len(graph)
    for (source, label, _), (chord, orientation) in arcs.items():
        weights[4 * source + label] = orientation * character[chord]
    for source in range(len(graph) // 4):
        for label, target in enumerate(graph[4 * source:4 * source + 4]):
            if target >= 0:
                assert weights[4 * source + label] == -weights[4 * target + (label ^ 1)]
    assert all(voltage_word(graph, weights, word) == 0 for word in rows)
    basis = [reduce(paths[a] + LETTERS[label] + inverse(paths[b])) for a, label, b in chords]
    assert fold(basis) == graph
    assert [voltage_word(graph, weights, word) for word in basis] == character
    certificate = review(graph, weights)
    inequalities, components = verify_cycles({"graph": graph, "edge_voltages": weights}, certificate)
    return {"graph": graph, "basis": basis, "row_coordinates": row_coordinates,
            "character": character, "edge_voltages": weights, "inequalities": inequalities,
            "cyclic_components": components, "certificate": certificate}


def analyze(rows, identifications, potentials):
    audit = verify(identifications, potentials)
    stats, graphs = census(rows)
    original = fold(rows)
    rank_two = {graph for graph in graphs if rank(graph) == 2}
    assert rank_two == {original, ROSE}
    assert stats["rank_two_overgroups"][0]["primitive_detector"]["status"] == "ABSENT"
    one_fold = {tuple(item["graph"]) for item in identifications["records"]}
    direct = {fold_identification(original, a, b)[0] for a, b in combinations(range(len(original) // 4), 2)}
    assert one_fold == direct and all(rank(graph) == 3 for graph in one_fold)
    rank_three = {graph for graph in graphs if rank(graph) == 3}
    assert one_fold <= rank_three
    return {"rows": rows, "principal_quotients_by_rank": stats["quotients_by_rank"],
            "independent_vertex_pair_checks": stats["independently_matched_pair_identifications"],
            "rank_three_single_identification_audit": audit,
            "rank_three_single_identification_distinct_cores": len(one_fold),
            "rank_three_additional_cores": [extra_character(graph, rows)
                                            for graph in sorted(rank_three - one_fold)]}


def main():
    ak3 = analyze(AK3, read_old("v_vertex_identification_results.json"),
                  read_old("v_voltage_cycle_results.json"))
    new = build(ENERGY17)
    e17 = analyze(ENERGY17, new["identifications"], new["potentials"])
    assert len(ak3["rank_three_additional_cores"]) == 1
    assert not e17["rank_three_additional_cores"]
    print(json.dumps({"AK3": ak3, "energy17": e17}, indent=2))


if __name__ == "__main__":
    main()
