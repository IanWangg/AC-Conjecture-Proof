"""Build a strict ordinary path to the second stable waypoint via y -> yx."""

import argparse
import json
from pathlib import Path

from elementary_verify import inverse, reduce, replay
from free_waypoint_search import canonical, conj_ops, cyclic, normalize
from round03_ak3_escape_replay import START, compile_route
from stallings_search import apply, nielsen_move

E = ("XXYxyyXYxY", "XYYxYXyXYxYXy")
TARGET = ("XXXYxyxyXYY", "XYXYYXyXYYXy")
IMAGES = {"x": "x", "X": "X", "y": "yx", "Y": "XY"}


def phi(word):
    return reduce("".join(IMAGES[letter] for letter in word))


def normalize_pair(state, target):
    moves = []
    if tuple(map(canonical, state)) != tuple(map(canonical, target)):
        assert tuple(map(canonical, reversed(state))) == tuple(map(canonical, target))
        # (a,b) -> (ab,b) -> (ab,a^-1) -> (b,a^-1) -> (b,a).
        for i, left, negative in ((0, False, False), (1, False, True), (0, True, False)):
            state, instructions = nielsen_move(state, i, left=left, negative=negative)
            moves.extend(instructions)
        step = {"op": "invert", "i": 1}
        state = apply(state, step)
        moves.append(step)
    for i, word in enumerate(target):
        state, instructions = normalize(state, i, word)
        moves.extend(instructions)
    assert state == target
    return moves


def compile_at_route_peak(path):
    route = json.loads(path.read_text())
    peak = max(sum(map(len, row)) for row in route["route"])
    return compile_route({**route, "cyclic_cap": peak})


def transport(anchor_route, preimage_route, destination):
    anchor, anchor_result = compile_at_route_peak(anchor_route)
    preimage, preimage_result = compile_at_route_peak(preimage_route)
    assert tuple(sorted(map(canonical, preimage["target"]))) == E
    seed = tuple(map(phi, START))
    moves = anchor["moves"] + normalize_pair(tuple(anchor["target"]), seed)
    seed_step = len(moves)
    for move in preimage["moves"]:
        if move["op"] == "conjugate":
            moves.extend(conj_ops(move["i"], phi(move["g"])))
        else:
            moves.append(move)
    image_step = len(moves)
    mapped_endpoint = tuple(map(phi, preimage["target"]))
    moves.extend(normalize_pair(mapped_endpoint, TARGET))
    certificate = {"format": "ordinary-ac-elementary-v1", "start": list(START),
                   "target": list(TARGET), "moves": moves}
    verified = replay(certificate)
    state = START
    cyclic_peak = sum(map(len, state))
    for count, move in enumerate(moves, 1):
        state = apply(state, move)
        cyclic_peak = max(cyclic_peak, sum(len(cyclic(word)) for word in state))
        if count == seed_step:
            assert state == seed
        if count == image_step:
            assert state == mapped_endpoint
    destination.write_text(json.dumps(certificate, indent=2) + "\n")
    return {
        **verified, "cyclic_peak": cyclic_peak,
        "seed_peak": anchor_result["cyclic_peak"], "seed_alignment_step": seed_step,
        "preimage_peak": preimage_result["cyclic_peak"], "preimage_strict_moves": preimage_result["moves"],
        "transported_move_count": image_step - seed_step,
        "preimage": E, "ambient_automorphism": {letter: IMAGES[letter] for letter in "xy"},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("anchor_route", "preimage_route", "destination"):
        parser.add_argument(name, type=Path)
    print(json.dumps(transport(**vars(parser.parse_args())), indent=2))
