"""Enumerate every same-rank overgroup via audited Stallings quotients."""

from collections import Counter
from itertools import combinations
import json

from primitive_map_pairs import base_path, decide, fold, inverse, reduce
from u_verify_voltage_phase import fold_relation
from v_vertex_identification import fold_identification

AK3 = ("xxxYYYY", "xyxYXY")
ENERGY17 = ("xxyXYXy", "xxYXYxYYXY")
ROSE = fold(("x", "y"))


def rank(graph):
    return sum(endpoint >= 0 for endpoint in graph) // 2 - len(graph) // 4 + 1


def census(rows):
    [a, b], [c, d] = [[word.count(letter) - word.count(letter.upper()) for letter in "xy"] for word in rows]
    assert abs(a * d - b * c) == 1
    initial = fold(rows)
    assert rank(initial) == 2
    graphs = [initial]
    seen = {initial}
    steps = 0
    for graph in graphs:
        for first, second in combinations(range(len(graph) // 4), 2):
            quotient, projection = fold_identification(graph, first, second)
            independent, independent_projection = fold_relation(graph, (first, second))
            assert quotient == tuple(independent) and projection == independent_projection
            steps += 1
            if quotient not in seen:
                seen.add(quotient)
                graphs.append(quotient)
    status = []
    for graph in graphs:
        if rank(graph) != 2:
            continue
        checked = decide(graph)
        assert checked["status"] in ("PRIMITIVE", "ABSENT")
        status.append({"vertices": len(graph) // 4, "initial_subgroup": graph == initial,
                       "ambient_rose": graph == ROSE, "primitive_detector": checked})
    immediate_generators = []
    paths = [base_path(initial, vertex) for vertex in range(len(initial) // 4)]
    for first, second in combinations(range(len(paths)), 2):
        quotient, _ = fold_identification(initial, first, second)
        if quotient == ROSE:
            representative = reduce(paths[first] + inverse(paths[second]))
            assert fold((*rows, representative)) == ROSE
            immediate_generators.append({"vertices": [first, second], "representative": representative})
    return {"rows": rows, "core_vertices": len(initial) // 4, "all_principal_quotients": len(graphs),
            "quotients_by_rank": dict(sorted(Counter(map(rank, graphs)).items())),
            "independently_matched_pair_identifications": steps, "rank_two_overgroups": status,
            "vertex_pairs_giving_ambient_rose": immediate_generators}, seen


def substituted(word, images):
    marked = dict(zip("xy", images))
    marked.update({letter.upper(): inverse(image) for letter, image in tuple(marked.items())})
    return reduce("".join(marked[letter] for letter in word))


def main():
    ak3, _ = census(AK3)
    assert len(ak3["rank_two_overgroups"]) == 2
    assert ak3["rank_two_overgroups"][0]["primitive_detector"]["status"] == "ABSENT"
    energy17, _ = census(ENERGY17)
    outer = ("xxyX", "y")
    inner = ("x", "yyxY")
    composition = tuple(substituted(row, outer) for row in inner)
    control, control_graphs = census(composition)
    middle = fold(outer)
    assert middle in control_graphs and rank(middle) == 2
    assert middle not in (fold(composition), ROSE)
    assert decide(middle)["status"] == "PRIMITIVE"
    print(json.dumps({"AK3": ak3, "new_energy17": energy17,
                      "factorization_control": {"outer_map": outer, "inner_map": inner,
                                                "middle_core": middle, "census": control}}, indent=2))


if __name__ == "__main__":
    main()
