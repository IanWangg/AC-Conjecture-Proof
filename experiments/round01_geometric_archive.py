"""Whitehead-minimize rank-two cyclic pairs and apply planar-link parity."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from elementary_verify import reduce as free_reduce
from planar_link_parity import decide
from round01_ak3_archive import cyclic_word, pair_key
from thickening_rotations import link
from verify_link_parity import verify_certificate


def image(pair, letter, replacement):
    inverse = replacement[::-1].swapcase()
    letters = {letter: replacement, letter.upper(): inverse}
    return tuple(
        cyclic_word(free_reduce("".join(letters.get(c, c) for c in word)))
        for word in pair
    )


def length(pair):
    return sum(map(len, pair))


def minimal_pair(pair):
    while True:
        candidates = [
            image(pair, letter, substitution)
            for letter, donor in (("x", "y"), ("y", "x"))
            for signed in (donor, donor.upper())
            for substitution in (letter + signed, signed + letter)
        ]
        best = min(candidates, key=length)
        if length(best) >= length(pair):
            return pair_key(pair)
        pair = best


def exponent_vector(word):
    return word.count("x") - word.count("X"), word.count("y") - word.count("Y")


def check_whitehead_cuts(pair):
    incident, _, edges = link(pair)
    for vertex in range(4):
        for cut in range(16):
            sides = tuple(bool(cut & (1 << i)) for i in range(4))
            if sides[vertex] and not sides[vertex ^ 1]:
                crossing = sum(sides[a] != sides[b] for a, b in edges)
                assert crossing >= len(incident[vertex])


def screen(path):
    data = path.read_bytes()
    sources = [tuple(line.split()) for line in data.decode("ascii").splitlines()]
    reduced = {}
    shortenings = 0
    for pair in sources:
        first, second = pair
        a, b = exponent_vector(first)
        c, d = exponent_vector(second)
        assert abs(a * d - b * c) == 1
        reduced_pair = minimal_pair(pair)
        shortenings += length(reduced_pair) < length(pair)
        reduced.setdefault(reduced_pair, pair)
    counts = Counter()
    remaining = []
    for pair, source in reduced.items():
        check_whitehead_cuts(pair)
        certificate = decide(pair)
        status = certificate["status"]
        if status == "PARITY_OBSTRUCTION":
            verify_certificate(certificate)
        else:
            remaining.append({"minimal_pair": pair, "source": source, "status": status})
        counts[status] += 1
    return {
        "input_sha256": hashlib.sha256(data).hexdigest(),
        "source_pairs": len(sources),
        "strict_whitehead_shortenings": shortenings,
        "distinct_whitehead_minimal_keys": len(reduced),
        "classification": dict(sorted(counts.items())),
        "remaining": remaining,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalogue", type=Path)
    args = parser.parse_args()
    print(json.dumps(screen(args.catalogue), indent=2))
