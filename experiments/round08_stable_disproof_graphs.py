"""List the marked three-edge-connected graphs at the tight crossing budget."""

import argparse
from itertools import combinations, permutations
import json
from pathlib import Path


def edge_options(vertices):
    pairs = tuple(combinations(range(vertices), 2))
    return {edge: 1 << i for i, edge in enumerate(pairs)}


def labeled_graphs(degrees, high, edges):
    vertices = len(degrees)
    remaining = list(degrees)

    def visit(node, mask, repeated):
        if node == vertices:
            yield mask, repeated
            return
        options = [j for j in range(node + 1, vertices) if remaining[j]]
        twice = [j for j in options if high in (node, j) and remaining[j] >= 2]
        for double in [None, *twice] if not repeated else [None]:
            rest = [j for j in options if j != double]
            singles = remaining[node] - (2 if double is not None else 0)
            if singles < 0:
                continue
            for chosen in combinations(rest, singles):
                new_mask = mask
                for vertex in chosen:
                    remaining[vertex] -= 1
                    new_mask |= edges[node, vertex]
                new_repeat = repeated
                if double is not None:
                    remaining[double] -= 2
                    new_repeat = edges[node, double]
                    new_mask |= new_repeat
                yield from visit(node + 1, new_mask, new_repeat)
                if double is not None:
                    remaining[double] += 2
                for vertex in chosen:
                    remaining[vertex] += 1

    yield from visit(0, 0, 0)


def marked_orbit(high, graph, vertices, edges):
    mask, repeated = graph
    flexible = [i for i in range(vertices) if i not in (0, high)]
    pairs = [pair for pair, bit in edges.items() if mask & bit]
    double = next((pair for pair, bit in edges.items() if repeated == bit), None)
    labeling = list(range(vertices))
    orbit = set()

    def image(pair):
        i, j = pair
        return edges[tuple(sorted((labeling[i], labeling[j])))]

    for perm in permutations(flexible):
        for i, j in zip(flexible, perm):
            labeling[i] = j
        orbit.add((sum(image(pair) for pair in pairs), image(double) if double else 0))
    return orbit


def marked_graphs(vertices, high):
    edges = edge_options(vertices)
    # Taking complements covers exactly the cuts whose chosen side omits vertex 0.
    cuts = tuple(sum(bit for (i, j), bit in edges.items() if (subset >> i ^ subset >> j) & 1)
                 for subset in range(2, 1 << vertices, 2))
    degrees = tuple(4 if i == high else 3 for i in range(vertices))
    viable = {
        (mask, double) for mask, double in labeled_graphs(degrees, high, edges)
        if all(bin(mask & cut).count("1") + bool(double & cut) >= 3 for cut in cuts)
    }
    labeled_count = len(viable)
    representatives = []
    while viable:
        mask, double = min(viable)
        orbit = marked_orbit(high, (mask, double), vertices, edges)
        assert orbit <= viable
        viable.difference_update(orbit)
        pairs = [pair for pair, bit in edges.items() if mask & bit]
        pairs.extend(pair for pair, bit in edges.items() if double & bit)
        representatives.append(pairs)
    return {
        "padding": vertices - 1,
        "degree_four_vertex": high,
        "labeled_graphs": labeled_count,
        "representatives": representatives,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    groups = [marked_graphs(vertices, high) for vertices, high in
              ((6, None), (7, 0), (7, 1), (8, None))]
    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / "graphs.json").open("w") as output:
        json.dump(groups, output, indent=2)
    with (args.output / "graphs.txt").open("w") as output:
        for group in groups:
            for graph in group["representatives"]:
                print(len(graph), *(vertex for pair in graph for vertex in pair), file=output)


if __name__ == "__main__":
    main()
