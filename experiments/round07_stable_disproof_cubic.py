"""Test the tight five-padding budget using the two possible cubic graphs."""

from itertools import combinations
import json

from round07_stable_disproof_incidence_audit import midpoint_key


def schedules(graph, radius, start):
    rank = 7  # The contracted original vertex stands for two rows.
    stride = sum(1 << (rank * i) for i in range(rank))
    menus = []
    for i, j in graph:
        left = (0, 1) if i == 0 else (i + 1,)
        right = (0, 1) if j == 0 else (j + 1,)
        moves = []
        for a in left:
            for b in right:
                moves.extend(((a, b), (b, a)))
        menus.append(moves)

    def visit(matrix, used, depth):
        if depth == radius:
            yield (used, midpoint_key(matrix, rank))
        else:
            for i, menu in enumerate(menus):
                bit = 1 << i
                if not used & bit:
                    for receiver, donor in menu:
                        image = matrix ^ (((matrix >> donor) & stride) << receiver)
                        yield from visit(image, used | bit, depth + 1)

    yield from visit(start, 0, 0)


def check(name, omitted):
    graph = [e for e in combinations(range(6), 2) if e not in omitted]
    assert len(graph) == 9
    assert all(sum(i in e for e in graph) == 3 for i in range(6))
    assert all(
        sum(bool(subset >> i & 1) != bool(subset >> j & 1) for i, j in graph) >= 3
        for subset in range(1, (1 << 6) - 1)
    )
    unit = sum(1 << (8 * i) for i in range(7))
    whole = (1 << len(graph)) - 1
    before = {}
    left_size = right_size = hits = 0
    for key in schedules(graph, 4, unit ^ 2):
        before[key] = before.get(key, 0) + 1
        left_size += 1
    for used, columns in schedules(graph, 5, unit):
        hits += before.get((whole ^ used, columns), 0)
        right_size += 1
    return {"graph": name, "edges": graph, "prefixes": left_size,
            "inverse_suffixes": right_size, "parity_matches": hits}


def main():
    hexagon = {tuple(sorted((i, (i + 1) % 6))) for i in range(6)}
    triangles = set(combinations((0, 1, 2), 2)) | set(combinations((3, 4, 5), 2))
    results = [check("triangular_prism", hexagon), check("K_3_3", triangles)]
    print(json.dumps({"padding": 5, "crossing_budget": 9, "results": results}, indent=2))


if __name__ == "__main__":
    main()
