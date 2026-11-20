"""Replay unbounded primitive slopes at the five energy-20 minima."""

import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from pathlib import Path

from euclidean_primitive_audit import positive
from primitive_map_pairs import fold
from round05_ak3_orbit_audit import rotations
from round10_ac_proof_blocks import vectors
from round11_ac_disproof_wirtinger import ROSE
from round14_ac_disproof_frozen import permutation_residues, validate_family

MINIMA = (
    ("xxxyxYxYY", "xyxYYxyyXYY"),
    ("xxxyxYxYY", "xyxYYYxyyXY"),
    ("xxxyyXXYY", "xyxYYxyyXYY"),
    ("xxxyyXXYY", "xyXYYxyyxYY"),
    ("xxyxYxxyy", "xyyxYYXyyxY"),
)


def euclidean(vector):
    x, y = vector
    alphabet = ("X" if x < 0 else "x") + ("Y" if y < 0 else "y")
    return positive(abs(x), abs(y)).translate(str.maketrans("xy", alphabet))


def slope_basis(fixed, source):
    words = [euclidean(vectors(w)) for w in (source, fixed)]
    for transverse, axial in product(*map(rotations, words)):
        if fold((transverse, axial)) == ROSE:
            validate_family(fixed, source, transverse, axial)
            return transverse, axial
    raise RuntimeError(f"no paired primitive basis for {fixed}, {source}")


def scan(executable, fixed, source, maximum):
    a, b = slope_basis(fixed, source)
    rows = subprocess.check_output(
        [str(executable), fixed, source, a, b, str(maximum)], text=True
    ).splitlines()
    markings = []
    for line in rows:
        x, y, count = line.split("\t")
        markings.append(tuple(tuple(map(int, row.split(","))) for row in (x, y)))
        check = permutation_residues(fixed, source, a, b, markings)
        assert 2520 % check["combined_period"] == 0
        assert len(check["survivors"]) * (2520 // check["combined_period"]) == int(count)
    return {"donor": fixed, "receiver": source, "basis": [a, b],
            **permutation_residues(fixed, source, a, b, markings)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("finder", type=Path)
    parser.add_argument("--degree", type=int, default=9)
    args = parser.parse_args()
    pairs = [p for pair in MINIMA for p in (pair, pair[::-1])]
    controls = [("xxyyy", "xxxyyyy"), ("XXYXYxxyXyxxy", "XXYxYXXYxxy")]
    with ThreadPoolExecutor(max_workers=5) as pool:
        outcomes = list(pool.map(
            lambda pair: scan(args.finder, *pair, args.degree), pairs + controls
        ))
    positive, excluded = outcomes[-2:]
    assert positive["survivors"]
    assert not excluded["survivors"]
    print(json.dumps(
        {"degree_cap": args.degree, "pairs": MINIMA,
         "directions": outcomes[:-2],
         "excluded": sum(not row["survivors"] for row in outcomes[:-2]),
         "positive_control": positive, "negative_control": excluded},
        indent=2,
    ))


if __name__ == "__main__":
    main()
