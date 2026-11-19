"""Check for paired spherical Whitehead diagrams of rank-three tuples."""

import argparse
from collections import defaultdict
from itertools import permutations, product
import json
from math import factorial, prod
from pathlib import Path

from round03_stable_proof_pivot import canonical, det
from round05_stable_proof_chartless import LETTERS, TARGET, chart_count, minima, primitive


def rank_three_link(rows):
    darts = [[] for _ in LETTERS]
    endpoints = []
    paired = {}
    for word in rows:
        offset = len(endpoints)
        for i, a in enumerate(word):
            b = word[(i + 1) % len(word)]
            first, second = LETTERS.index(a.swapcase()), LETTERS.index(b)
            assert first != second
            endpoints.append((first, second))
            dart = 2 * (offset + i)
            darts[first].append(dart)
            darts[second].append(dart + 1)
            before = 2 * (offset + (i - 1) % len(word)) + 1
            paired[dart] = before
            paired[before] = dart
    return darts, endpoints, paired


def components(neighbors, present):
    remaining = set(present)
    count = 0
    while remaining:
        count += 1
        todo = [remaining.pop()]
        while todo:
            reached = neighbors[todo.pop()] & remaining
            remaining -= reached
            todo.extend(reached)
    return count


def rotate_to_minimum(row):
    if not row:
        return row
    slot = row.index(min(row))
    return row[slot:] + row[:slot]


def planar_orders(rows):
    darts, endpoints, paired = rank_three_link(rows)
    edges = len(endpoints)
    neighbors = [set() for _ in LETTERS]
    bundles = defaultdict(list)
    for edge, (u, v) in enumerate(endpoints):
        neighbors[u].add(v)
        neighbors[v].add(u)
        bundles[tuple(sorted((u, v)))].append(edge)
    present = {v for v, row in enumerate(darts) if row}
    component_count = components(neighbors, present)
    target_faces = 2 * component_count - len(present) + edges
    parallel = {edge: frozenset(labels) for edge, labels in bundles.items() if len(labels) > 1}
    contiguous = {
        edge: labels for edge, labels in parallel.items()
        if components(neighbors, present.difference(edge)) <= 1
    }

    def dart_groups(v):
        groups = []
        rest = set(darts[v])
        for edge, labels in contiguous.items():
            if v in edge:
                group = sorted(d for d in rest if d // 2 in labels)
                assert len(group) == len(labels)
                rest.difference_update(group)
                groups.append(tuple(group))
        groups.extend((d,) for d in sorted(rest))
        return sorted(groups)

    def group_count(groups):
        if len(groups) <= 1:
            return factorial(max(len(groups[0]) - 1, 0)) if groups else 1
        return factorial(len(groups) - 1) * prod(factorial(len(group)) for group in groups)

    def group_orders(groups):
        if not groups:
            yield ()
        elif len(groups) == 1:
            start, *rest = groups[0]
            for tail in permutations(rest):
                yield (start, *tail)
        else:
            for arranged in product(*(permutations(g) for g in groups)):
                for tail in permutations(arranged[1:]):
                    order = tuple(d for g in (arranged[0], *tail) for d in g)
                    yield rotate_to_minimum(order)

    def valid_contiguity(v, order):
        for edge, labels in contiguous.items():
            if v not in edge:
                continue
            membership = [d // 2 in labels for d in order]
            if sum(a != b for a, b in zip(membership, membership[1:] + membership[:1])) > 2:
                return False
        return True

    def bundle_orders(v, order):
        return {
            edge: rotate_to_minimum(tuple(d // 2 for d in order if d // 2 in labels))
            for edge, labels in parallel.items()
            if v in edge and len(labels) >= 3
        }

    def compatible(first, second):
        return all(rotate_to_minimum(first[k][::-1]) == second[k] for k in first.keys() & second.keys())

    def local_orders(letter):
        groups = {v: dart_groups(v) for v in (letter, letter ^ 1)}
        a = min(groups, key=lambda v: (group_count(groups[v]), v))
        b = a ^ 1
        for first in group_orders(groups[a]):
            second = tuple(paired[d] for d in first[::-1])
            if not valid_contiguity(b, second):
                continue
            left, right = bundle_orders(a, first), bundle_orders(b, second)
            if compatible(left, right):
                merged = left | right
                yield {a: first, b: second}, merged

    factors = [list(local_orders(v)) for v in (0, 2, 4)]
    factors.sort(key=len)
    checked = 0
    for first, left in factors[0]:
        for second, middle in factors[1]:
            if not compatible(left, middle):
                continue
            merged = left | middle
            for third, right in factors[2]:
                if not compatible(merged, right):
                    continue
                checked += 1
                combined = first | second | third
                sigma = [0] * (2 * edges)
                for order in combined.values():
                    for here, there in zip(order, order[1:] + order[:1]):
                        sigma[here] = there
                unseen = set(range(2 * edges))
                faces = 0
                while unseen:
                    faces += 1
                    d = unseen.pop()
                    d = sigma[d ^ 1]
                    while d in unseen:
                        unseen.remove(d)
                        d = sigma[d ^ 1]
                if faces == target_faces:
                    return dict(planar=True, checked_rotations=checked,
                                local_order_counts=list(map(len, factors)),
                                spherical_orders=[combined[v] for v in range(6)])
    return dict(planar=False, checked_rotations=checked, local_order_counts=list(map(len, factors)))


def full_signed_key(rows):
    images = []
    for names in permutations("xyz"):
        for inverted in product((False, True), repeat=3):
            basis = [a.upper() if inv else a for a, inv in zip(names, inverted)]
            marking = str.maketrans(LETTERS, "".join(a + a.swapcase() for a in basis))
            images.append(tuple(sorted(canonical(w.translate(marking)) for w in rows)))
    return min(images)


def scan(path):
    states = {}
    for line in path.open():
        rows = tuple(line.split())
        if chart_count(rows) == 0 and not any(primitive(w) for w in rows):
            assert abs(det(rows)) == 1
            minimized = minima(rows)[0]
            states.setdefault(full_signed_key(minimized), rows)
    results = [(rows, planar_orders(rows)) for rows in sorted(states)]
    return dict(
        checked_minimal_diagrams=len(results),
        spherical_diagrams=[dict(rows=rows, source=states[rows], **r) for rows, r in results if r["planar"]],
        maximum_local_order_count=max(n for _, r in results for n in r["local_order_counts"]),
        checked_rotations=sum(r["checked_rotations"] for _, r in results),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scan", type=Path)
    args = parser.parse_args()
    controls = {
        "basis": ("x", "y", "z"),
        "nonprimitive_rank_two_geometric_block_with_z": ("xxYYY", "xxxYYYY", "z"),
        "cap_22_boundary": TARGET,
    }
    output = {key: planar_orders(rows) for key, rows in controls.items()}
    assert output["basis"]["planar"] and output["nonprimitive_rank_two_geometric_block_with_z"]["planar"]
    if args.scan:
        output["scan"] = scan(args.scan)
    print(json.dumps(output, indent=2))
