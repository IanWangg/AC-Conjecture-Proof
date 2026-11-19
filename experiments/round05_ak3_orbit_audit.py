"""Independently compare signed-ambient orbit catalogues and replay escape receipts."""

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path

from elementary_verify import inverse
from euclidean_primitive_audit import primitive_cyclic_word


MAPS = tuple(
    str.maketrans("xXyY", first + first.swapcase() + second + second.swapcase())
    for first_slot, second_slot in (("xX", "yY"), ("yY", "xX"))
    for first in first_slot
    for second in second_slot
)


def rotations(word):
    doubled = word + word
    return (doubled[start:start + len(word)] for start in range(len(word)))


def word_key(word):
    return min(min(rotations(word)), min(rotations(inverse(word))))


@lru_cache(maxsize=100_000)
def word_orbit(word):
    return tuple(word_key(word.translate(transformation)) for transformation in MAPS)


def pair_orbit(a, b):
    return min(tuple(sorted(pair)) for pair in zip(word_orbit(a), word_orbit(b)))


def load(path, reps_only=False):
    counts = Counter()
    rows = 0
    with path.open() as source:
        for row in source:
            pair = tuple(row.rstrip("\n").split("\t"))
            assert len(pair) == 2 and all(pair)
            key = pair_orbit(*pair)
            if reps_only:
                assert key not in counts, (path, pair, key)
            counts[key] += 1
            rows += 1
    return counts, rows


def compare(full, compact):
    expanded, full_count = load(full)
    quotient, compact_count = load(compact, reps_only=True)
    assert expanded.keys() == quotient.keys()
    assert all(value in (1, 2, 4, 8) for value in expanded.values())
    return {
        "status": "SAME_ORBITS",
        "full_rows": full_count,
        "quotient_rows": compact_count,
        "full_multiplicities": dict(sorted(Counter(expanded.values()).items())),
    }


def seed_images(path):
    seed = ("xxxYYYY", "xyxYXY")
    orbit = {tuple(sorted(pair)) for pair in zip(*(word_orbit(word) for word in seed))}
    missing = set(orbit)
    with path.open() as source:
        for row in source:
            missing.discard(tuple(row.rstrip("\n").split("\t")))
    assert not missing, sorted(missing)
    return {"all_seed_images_present": True, "signed_cyclic_seed_images": sorted(orbit)}


def compact_membership(path, a, b):
    encode = str.maketrans("xXyY", "0123")
    decode = str.maketrans("0123", "xXyY")

    def encoded_word(word):
        forward = word.translate(encode)
        backward = inverse(word).translate(encode)
        return min(min(rotations(forward)), min(rotations(backward)))

    candidates = []
    for transformation in MAPS:
        pair = tuple(encoded_word(word.translate(transformation)) for word in (a, b))
        candidates.append(tuple(sorted(pair, key=lambda item: (len(item), item))))
    compact = tuple(word.translate(decode) for word in min(candidates))
    target = ("\t".join(compact) + "\n").encode("ascii")
    with path.open("rb") as source:
        found = any(row == target for row in source)
    return {"literal_input": [a, b], "compact_key": compact, "present": found}


def audit_primitives(path):
    digest = sha256()
    rows = candidates = 0
    primitive_coordinates = []
    with path.open("rb") as source:
        for line in source:
            digest.update(line)
            rows += 1
            for word in line.rstrip(b"\n").split(b"\t"):
                if (b"x" in word and b"X" in word) or (b"y" in word and b"Y" in word):
                    continue
                candidates += 1
                if primitive_cyclic_word(word.decode("ascii")):
                    primitive_coordinates.append(word.decode("ascii"))
    return {"rows": rows, "single_sign_candidates": candidates, "primitive_coordinates": primitive_coordinates,
            "tsv_sha256": digest.hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    compare_parser = subparsers.add_parser("compare")
    compare_parser.add_argument("full", type=Path)
    compare_parser.add_argument("compact", type=Path)
    partition = subparsers.add_parser("partition")
    partition.add_argument("catalogue", type=Path)
    primitive_parser = subparsers.add_parser("primitive")
    primitive_parser.add_argument("catalogue", type=Path)
    seed_parser = subparsers.add_parser("seed")
    seed_parser.add_argument("catalogue", type=Path)
    member_parser = subparsers.add_parser("contains")
    member_parser.add_argument("catalogue", type=Path)
    member_parser.add_argument("first")
    member_parser.add_argument("second")
    args = parser.parse_args()
    if args.command == "compare":
        result = compare(args.full, args.compact)
    elif args.command == "primitive":
        result = audit_primitives(args.catalogue)
    elif args.command == "seed":
        result = seed_images(args.catalogue)
    elif args.command == "contains":
        result = compact_membership(args.catalogue, args.first, args.second)
    else:
        counts, rows = load(args.catalogue)
        result = {"rows": rows, "signed_permutation_orbits": len(counts),
                  "multiplicities": dict(sorted(Counter(counts.values()).items())),
                  "sha256": sha256(args.catalogue.read_bytes()).hexdigest()}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
