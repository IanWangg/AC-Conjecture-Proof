"""Build marked torus-relator orbit tables and a strict ordinary control."""

import argparse
import json
from collections import deque
from io import BytesIO
from math import gcd
from pathlib import Path
from struct import pack

from elementary_verify import replay
from euclidean_primitive_audit import positive, primitive_cyclic_word
from free_waypoint_search import cyclic
from round05_ak3_orbit_audit import rotations
from round06_stable_proof_strict_escape import StrictPath
from round08_ak3_acm_replay import compile_move
from round14_ak3_bs_atlas import packed_cyclic
from stallings_search import graph, inverse, reduce

ALPHABET = "xXyY"
ORDER = str.maketrans(ALPHABET, "0123")
PAIRS = tuple(
    (p, q) for p in range(2, 16) for q in range(p + 1, 32 - p) if gcd(p, q) == 1
)


def key(word):
    word = cyclic(word)
    return min(
        (*rotations(word), *rotations(inverse(word))), key=lambda w: w.translate(ORDER)
    )


def apply(word, images):
    by_letter = dict(zip("xyXY", (*images, *map(inverse, images))))
    return reduce("".join(by_letter[c] for c in word))


def transformations():
    moves = [
        (("X", "y"), ("X", "y")),
        (("x", "Y"), ("x", "Y")),
        (("y", "x"), ("y", "x")),
    ]
    for i in range(2):
        major, minor = "xy"[i], "yx"[i]
        for tail in (minor, minor.upper()):
            for prefix in (False, True):
                value = tail + major if prefix else major + tail
                inv = inverse(tail) + major if prefix else major + inverse(tail)
                a = list("xy")
                b = list("xy")
                a[i], b[i] = value, inv
                moves.append((tuple(a), tuple(b)))
    assert all(tuple(apply(w, a) for w in b) == tuple("xy") for a, b in moves)
    return moves


def farey(p, q):
    b = next(x for x in range(1, q) if (1 + p * x) % q == 0)
    a = (1 + p * b) // q
    assert 0 < a < p and q * a - p * b == 1 and 0 < b < q
    u, w = positive(a, b), positive(p - a, q - b)
    for first in rotations(u):
        for second in rotations(w):
            if not all(part[0] == "x" and part[-1] == "y" for part in (first, second)):
                continue
            if graph((first, second))[1] == 1:
                return first, second, first + second
    raise AssertionError((p, q, u, w))


def atlas(root, cap, moves):
    start = key(root)
    assert all(len(key(apply(start, forward))) >= len(start) for forward, _ in moves)
    inverse_marks = {start: ("x", "y")}
    pending = deque([start])
    while pending:
        current = pending.popleft()
        original = inverse_marks[current]
        for forward, back in moves:
            word = key(apply(current, forward))
            if len(word) > cap or word in inverse_marks:
                continue
            mark = tuple(apply(w, original) for w in back)
            assert key(apply(word, mark)) == start
            inverse_marks[word] = mark
            pending.append(word)
    return inverse_marks


def generate(output):
    moves = transformations()
    counts = {}
    indexed = set()
    with output.open("w") as stream:
        for p, q in PAIRS:
            assert gcd(p, q) == 1 and p < q
            u, w, v = farey(p, q)
            words = atlas("x" * p + "y" * q, 31, moves)
            for word, (x, y) in sorted(
                words.items(), key=lambda item: (len(item[0]), item[0])
            ):
                assert word not in indexed
                indexed.add(word)
                stream.write("\t".join(map(str, (word, p, q, x, y, u, w, v))) + "\n")
            counts[p, q] = (len(words), u, w, v)
    return counts


def positive_control(ledger, fixture):
    donor = "xxyyy"
    receiver = cyclic("xyx" + donor + "X")
    source = donor, receiver
    assert all(not primitive_cyclic_word(row) for row in source)
    prefix, _ = compile_move(source, 1, "xy", 3)
    path = StrictPath(source, BytesIO())
    path.extend(prefix["moves"])
    path.change_occurrences(0, "y", "X", 1)
    assert path.rows == ["X", "xy"]
    path.add({"op": "invert", "i": 0})
    path.change_occurrences(1, "x", "", 0)
    assert path.rows == ["x", "y"]
    moves = [json.loads(row) for row in path.sink.getvalue().splitlines()[1:]]
    proof = {**prefix, "moves": moves, "target": path.rows}
    assert replay(proof)["moves"] == 109
    ledger.write_text(json.dumps(proof, separators=(",", ":")) + "\n")
    a, b = sorted(map(packed_cyclic, source))
    fixture.write_bytes(pack("=4Q", a, b, a, b))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--control", type=Path, nargs=2, metavar=("LEDGER", "FIXTURE"))
    args = parser.parse_args()
    generate(args.output)
    if args.control:
        positive_control(*args.control)


if __name__ == "__main__":
    main()
