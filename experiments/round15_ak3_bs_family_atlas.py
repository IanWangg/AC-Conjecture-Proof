"""Enumerate standard BS(n,n+1) markings and replay a strict ordinary control."""

import argparse
import json
from io import BytesIO
from pathlib import Path
from struct import pack

from elementary_verify import replay
from euclidean_primitive_audit import primitive_cyclic_word
from free_waypoint_search import cyclic
from round06_stable_proof_strict_escape import StrictPath
from round08_ak3_acm_replay import compile_move
from round14_ak3_bs_atlas import packed_cyclic
from round15_ak3_torus_atlas import atlas, transformations


def relator(n):
    return "x" * (n + 1) + "y" + "X" * n + "Y"


def generate(destination):
    seen = set()
    moves = transformations()
    with destination.open("w") as output:
        for n in range(2, 15):
            seed = "y" + "x" * n + "Y" + "X" * (n + 1)
            for word, (x, y) in sorted(atlas(seed, 31, moves).items()):
                assert word not in seen
                seen.add(word)
                output.write(f"{word}\t{n}\t{x}\t{y}\n")


def control(ledger, fixture):
    donor = relator(2)
    source = donor, cyclic("yx" + donor + "X")
    assert all(not primitive_cyclic_word(word) for word in source)
    proof, _ = compile_move(source, 1, "y", 3)
    path = StrictPath(source, BytesIO())
    path.extend(proof["moves"])
    path.change_occurrences(0, "y", "", 1)
    assert path.rows == ["x", "y"]
    proof["moves"] = [json.loads(row) for row in path.sink.getvalue().splitlines()[1:]]
    proof["target"] = path.rows
    replay(proof)
    ledger.write_text(json.dumps(proof, separators=(",", ":")) + "\n")
    pair = sorted(map(packed_cyclic, source))
    fixture.write_bytes(pack("=4Q", *pair, *pair))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--control", type=Path, nargs=2, metavar=("LEDGER", "FIXTURE"))
    args = parser.parse_args()
    generate(args.output)
    if args.control:
        control(*args.control)


if __name__ == "__main__":
    main()
