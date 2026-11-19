"""Replay the four-lobe chain census and verify a bridge outside every three-lobe core."""

import argparse
from collections import Counter
from itertools import product
import json
from pathlib import Path
import random

from primitive_map_pairs import LETTERS, fold, follow, inverse, reduce
from round02_ac_disproof_controls import audit_joins
from round03_ac_disproof_bridges import BRAID, FORBIDDEN, POWER, chain_words, rotations

EXAMPLE = ((POWER, "XXXyyyy", "XXyyyyX", BRAID), "Xyy")


def free_directions(lobe):
    return set(LETTERS) - {lobe[0], inverse(lobe[-1])}


def four_chains():
    for power, braid, first, second in product(
        rotations(POWER), rotations(BRAID), sorted(FORBIDDEN), sorted(FORBIDDEN)
    ):
        for c in sorted(free_directions(power) & {inverse(a) for a in free_directions(first)}):
            d, = free_directions(first) - {inverse(c)}
            if inverse(d) not in free_directions(second):
                continue
            e, = free_directions(second) - {inverse(d)}
            if inverse(e) in free_directions(braid):
                yield (power, first, second, braid), c + d + e


def basis(lobes, connectors):
    return [
        connectors[:i] + loop + inverse(connectors[:i]) for i, loop in enumerate(lobes)
    ]


def older_graphs():
    return [
        fold(basis((power, middle, braid), c + d))
        for power, braid, middle, c, d in chain_words()
    ]


def starts_reading(graphs, word):
    return sum(
        follow(graph, v, word) >= 0 for graph in graphs for v in range(len(graph) // 4)
    )


def endpoint_paths(graph, terminal, first, last, limit):
    paths = [(word, vertex) for word in sorted(first) if (vertex := follow(graph, 0, word)) >= 0]
    for length in range(1, limit + 1):
        yield length, [
            word for word, vertex in paths if vertex == terminal and inverse(word[-1]) in last
        ]
        paths = [
            (word + label, graph[4 * vertex + i])
            for word, vertex in paths
            for i, label in enumerate(LETTERS)
            if label != inverse(word[-1]) and graph[4 * vertex + i] >= 0
        ]


def short_escape_control(words, graph):
    (p, r, s, b), connectors = EXAMPLE
    c, d, e = connectors
    q0 = c + r + d + s + e
    assert reduce(q0) == q0 and r in FORBIDDEN and r in q0
    terminal = follow(graph, 0, connectors)
    assert follow(graph, 0, q0) == terminal
    exact = words[1] + words[2] + words[3] + inverse(words[2]) + inverse(words[1])
    assert reduce(exact) == q0 + b + inverse(q0)

    old = older_graphs()
    assert len(old) == 552
    assert starts_reading(old, q0) == starts_reading(old, inverse(q0)) == 0
    lengths = {}
    for length, paths in endpoint_paths(
        graph, terminal, free_directions(p), free_directions(b), len(q0)
    ):
        if paths:
            readings = {word: starts_reading(old, word) for word in paths}
            lengths[str(length)] = readings
            if length < len(q0):
                assert all(readings.values())

    # Each retained sample follows a longer path with q0 as an exact prefix.
    words_at_depth_four = set()
    for choices in product((r, inverse(r)), repeat=4):
        q = q0 + b + inverse(e)
        q += "".join(s + inverse(d) + choice + d for choice in choices)
        q += s + e
        assert reduce(q) == q and q[0] in free_directions(p)
        assert inverse(q[-1]) in free_directions(b) and q.startswith(q0)
        assert follow(graph, 0, q) == terminal
        assert follow(graph, 0, q + b + inverse(q)) == 0
        words_at_depth_four.add(q)
    assert len(words_at_depth_four) == 16
    return {
        "lobes": [p, r, s, b],
        "connectors": connectors,
        "overgroup_basis": words,
        "bridge": q0,
        "bridge_length": len(q0),
        "older_three_lobe_cores": len(old),
        "older_start_vertices_checked": sum(len(g) // 4 for g in old),
        "older_reading_starts_by_length_in_this_chain": lengths,
        "minimum_escape_length_in_this_chain": len(q0),
        "equal_length_extended_sample_count": len(words_at_depth_four),
        "extended_sample_bridge_length": len(next(iter(words_at_depth_four))),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("native_json", type=Path)
    parser.add_argument("exceptions", type=Path)
    args = parser.parse_args()
    native = json.loads(args.native_json.read_text())
    assert args.exceptions.stat().st_size == 0
    choices = list(four_chains())
    vertex_counts = Counter(sum(map(len, lobes)) for lobes, _ in choices)
    expected_joins = sum(count * size * (size - 1) // 2 for size, count in vertex_counts.items())
    assert len(choices) == native["certified_sources"] == native["native_joins"]["sources"] == 7200
    assert expected_joins == native["native_joins"]["vertex_pairs"]
    assert expected_joins == native["native_joins"]["DAG_exclusions"]
    assert native["source_vertex_counts"] == {str(k): v for k, v in vertex_counts.items()}
    assert native["primitive_positive"] == native["incomplete"] == 0

    assert EXAMPLE in choices
    sampled = [EXAMPLE, *random.Random(20261119).sample(choices, 8)]
    controls = []
    for lobes, connectors in sampled:
        generators = basis(lobes, connectors)
        graph = fold(generators)
        assert len(graph) // 4 == sum(map(len, lobes))
        control = audit_joins(generators, graph)
        assert control["checked_joins"] == control["dag_exclusions"]
        controls.append(control)

    old_ak2 = ("xxYYY", BRAID)
    positive = audit_joins(old_ak2, fold(old_ak2), expect_primitive=True)
    assert len(positive["primitive_joins"]) == 3
    result = {
        "native": native,
        "independent_bouquet_audit": {
            "sampled_chains": len(sampled),
            "rebased_joins": sum(c["checked_joins"] for c in controls),
            "closed_map_pair_states_checked": sum(c["closed_map_states"] for c in controls),
            "explicit_chain": controls[0],
        },
        "escape_control": short_escape_control(basis(*EXAMPLE), fold(basis(*EXAMPLE))),
        "literal_AK2_positive_control": positive,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
