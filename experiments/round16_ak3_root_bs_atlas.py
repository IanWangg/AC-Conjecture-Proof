"""Enumerate marked root-adjoined Baumslag–Solitar relators through width 31."""

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


def relator(k, n):
    return "x" * k + "y" * n + "X" * k + "Y" * (n + 1)


def generate(destination):
    seen = set()
    moves = transformations()
    with destination.open("w") as output:
        for k in range(2, 15):
            for n in range(1, 16 - k):
                for word, (x, y) in sorted(atlas(relator(k, n), 31, moves).items()):
                    assert word not in seen
                    seen.add(word)
                    output.write(f"{word}\t{k}\t{n}\t{x}\t{y}\n")


def fixture_pair(donor, primitive):
    return donor, cyclic(primitive + "x" + donor + "X")


def save_seed(pair, path):
    words = sorted(map(packed_cyclic, pair))
    path.write_bytes(pack("=4Q", *words, *words))


def control(ledger, vertex_seed, mixed_seed):
    donor = relator(2, 2)
    source = fixture_pair(donor, "x")
    assert all(not primitive_cyclic_word(word) for word in source)
    proof, _ = compile_move(source, 1, "x", 3)
    path = StrictPath(source, BytesIO())
    path.extend(proof["moves"])
    path.change_occurrences(0, "x", "", 1)
    assert path.rows == ["Y", "x"]
    path.extend([
        {"op": "multiply", "i": 0, "j": 1},
        {"op": "invert", "i": 0},
        {"op": "multiply", "i": 1, "j": 0},
        {"op": "invert", "i": 0},
        {"op": "conjugate", "i": 0, "g": "y"},
        {"op": "multiply", "i": 0, "j": 1},
    ])
    proof["moves"] = [json.loads(row) for row in path.sink.getvalue().splitlines()[1:]]
    proof["target"] = path.rows
    assert path.rows == ["x", "y"]
    replay(proof)
    ledger.write_text(json.dumps(proof, separators=(",", ":")) + "\n")
    save_seed(source, vertex_seed)
    save_seed(fixture_pair(donor, "xy"), mixed_seed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--control", type=Path, nargs=3, metavar=("LEDGER", "VERTEX", "MIXED"))
    args = parser.parse_args()
    generate(args.output)
    if args.control:
        control(*args.control)


if __name__ == "__main__":
    main()
