"""Enumerate the bounded automorphism orbit of the BS(1,2) relator."""

import argparse
import json
from collections import deque
from io import BytesIO
from pathlib import Path
from struct import pack

from elementary_verify import replay
from free_waypoint_search import cyclic
from round05_ak3_orbit_audit import MAPS, rotations, word_key
from round06_stable_proof_strict_escape import StrictPath
from round08_ak3_acm_replay import compile_move
from stallings_search import inverse, reduce

RELATOR = "xxyXY"


def signed_class(word):
    word = cyclic(word)
    return min(word_key(word.translate(change)) for change in MAPS)


def shears(word):
    for recipient, other in (("x", "y"), ("y", "x")):
        for donor in (other, other.upper()):
            for replacement in (recipient + donor, donor + recipient):
                substitution = {
                    recipient: replacement,
                    recipient.upper(): inverse(replacement),
                }
                yield reduce("".join(substitution.get(letter, letter) for letter in word))


def atlas(limit):
    pending = deque([signed_class(RELATOR)])
    reached = set(pending)
    while pending:
        for neighbour in shears(pending.popleft()):
            key = signed_class(neighbour)
            if len(key) <= limit and key not in reached:
                reached.add(key)
                pending.append(key)
    return sorted(reached, key=lambda word: (len(word), word))


def packed_cyclic(word):
    encoded = lambda row: int("1" + "".join(f'{"xXyY".index(c):02b}' for c in row), 2)
    return min(map(encoded, (*rotations(word), *rotations(inverse(word)))))


def control(ledger, fixture):
    source = (RELATOR, "yyxYX")
    prefix, _ = compile_move(source, 1, "y", 1)
    path = StrictPath(source, BytesIO())
    path.extend(prefix["moves"])
    path.change_occurrences(0, "y", "", 1)
    moves = [json.loads(entry) for entry in path.sink.getvalue().splitlines()[1:]]
    certificate = {**prefix, "moves": moves, "target": path.rows}
    assert path.rows == ["x", "y"] and replay(certificate)["moves"] == 26
    ledger.write_text(json.dumps(certificate, separators=(",", ":")) + "\n")
    pair = sorted(map(packed_cyclic, source))
    # A binary format fixture exercises lookup on the verified nonprimitive starting tuple.
    fixture.write_bytes(pack("=4Q", *pair, *pair))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--control", type=Path, nargs=2, metavar=("LEDGER", "FIXTURE"))
    args = parser.parse_args()
    words = atlas(31)
    args.output.write_text("".join(word + "\n" for word in words))
    if args.control:
        control(*args.control)


if __name__ == "__main__":
    main()
