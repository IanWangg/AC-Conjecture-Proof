"""Lift a signed cap-22 excursion to actual relator products."""

import argparse
from itertools import permutations, product
import json
from pathlib import Path

from round03_stable_proof_pivot import canonical, neighbors
from round04_chart_screen import chart_projections
from round04_stable_proof_paths import compile_rank_three, replay
from round07_stable_proof_automorphic_charts import signed_key

LETTERS = "xyz"
TARGET = ("XXXYY", "XYXZy", "XzyZZ")
TARGET_PIVOT = "XzyZZ"
TARGET_LETTER = "y"
TARGET_PAIR = ("XXXYYXYXy", "XYYXyXYYxyy")


def actions():
    for permutation in permutations(LETTERS):
        for signs in product((False, True), repeat=3):
            image = "".join(c.upper() if sign else c for c, sign in zip(permutation, signs))
            yield str.maketrans(LETTERS + LETTERS.upper(), image + image.swapcase())


ACTIONS = tuple(actions())


def signed_rows(rows):
    return {tuple(sorted(canonical(row.translate(action)) for row in rows)) for action in ACTIONS}


def lift(orbit_path):
    current = {orbit_path[0]: None}
    ancestors = []
    for representative in orbit_path[1:]:
        targets = signed_rows(representative)
        parents = {}
        for source in sorted(current):
            successors, _ = neighbors(source, 22)
            for endpoint in successors & targets:
                parents.setdefault(endpoint, source)
        assert parents, (representative, list(current)[:2])
        ancestors.append(parents)
        current = parents
    endpoint = TARGET if TARGET in current else min(current)
    path = [endpoint]
    for parents in reversed(ancestors):
        path.append(parents[path[-1]])
    assert path[-1] == orbit_path[0]
    return path[::-1]


def verify_chart(endpoint):
    for action in ACTIONS:
        words = tuple(sorted(canonical(w.translate(action)) for w in TARGET))
        if words != tuple(sorted(endpoint)):
            continue
        marked = canonical(TARGET_PIVOT.translate(action))
        eliminated = TARGET_LETTER.translate(action).lower()
        for letter, pivot, pair in chart_projections(endpoint):
            if (letter, pivot) == (eliminated, marked):
                assert signed_key(pair) == signed_key(TARGET_PAIR)
                return dict(pivot_slot=endpoint.index(pivot), eliminated=eliminated,
                            pivot=pivot, projected_pair=pair, requested_pair=TARGET_PAIR)
    raise ValueError("target chart has no lifted marking")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rank_two_prefix", type=Path)
    parser.add_argument("rank_three_orbits", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    rank_two = json.loads(args.rank_two_prefix.read_text())
    orbit_path = [tuple(line.split()) for line in args.rank_three_orbits.open()]
    assert rank_two["cyclic_cap"] == 21 and orbit_path[-1] in signed_rows(TARGET)
    literal = lift(orbit_path)
    certificate = compile_rank_three(rank_two, literal)
    proof = replay(certificate)
    args.certificate.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps(dict(prefix_replay=proof, first_exit_seed=literal[0],
                          excursion_products=len(literal)-1, strict_signed_chart=verify_chart(proof["target"])),
                     indent=2))
