"""Check spherical diagrams of rank-three states without primitive relators."""

import argparse
from collections import Counter
from itertools import combinations
import json
from multiprocessing import Pool
from pathlib import Path

from round03_stable_proof_pivot import det
from round05_stable_proof_chartless import minima
from round05_stable_proof_geometry import full_signed_key, planar_orders

VERTICES = "XYZxyz"
EDGE_BITS = {edge: 1 << i for i, edge in enumerate(combinations(VERTICES, 2))}


def mask_of(edges):
    return sum(EDGE_BITS[tuple(sorted(edge))] for edge in edges)


def forbidden_masks():
    masks = set()
    for selected in combinations(VERTICES, 3):
        complement = set(VERTICES) - set(selected)
        masks.add(mask_of((a, b) for a in selected for b in complement))
    for middle in VERTICES:
        clique = tuple(combinations(VERTICES.replace(middle, ""), 2))
        masks.add(mask_of(clique))
        for edge in clique:
            masks.add(mask_of([pair for pair in clique if pair != edge] +
                              [(edge[0], middle), (edge[1], middle)]))
    return tuple(sorted(masks))


NONPLANAR_MASKS = forbidden_masks()


def minimal_planar_key(rows):
    assert abs(det(rows)) == 1
    minimized, _, edges, _, _ = minima(rows)
    abstract = mask_of(edges)
    if any(abstract & forbidden == forbidden for forbidden in NONPLANAR_MASKS):
        return None, rows
    return full_signed_key(minimized), rows


def spherical_test(job):
    key, source = job
    proof = planar_orders(key)
    return proof["checked_rotations"], dict(minimum=key, source=source, **proof) if proof["planar"] else None


def search(catalogue, workers):
    totals = Counter()
    planar = {}
    with catalogue.open() as data, Pool(workers) as pool:
        rows = (tuple(line.split()) for line in data)
        for key, source in pool.imap_unordered(minimal_planar_key, rows, chunksize=48):
            totals["states"] += 1
            if key is None:
                totals["abstract_nonplanar"] += 1
                continue
            totals["abstract_planar"] += 1
            if key not in planar or source < planar[key]:
                planar[key] = source
        spherical = []
        rotations = 0
        for count, witness in pool.imap_unordered(spherical_test, sorted(planar.items()), chunksize=16):
            rotations += count
            if witness is not None:
                spherical.append(witness)
    return dict(**totals, abstract_planar_minimal_signed_diagrams=len(planar),
                paired_rotations=rotations, spherical=sorted(spherical, key=lambda item: item["minimum"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chartless_rank_three_states", type=Path)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    print(json.dumps(search(args.chartless_rank_three_states, args.workers), indent=2))
