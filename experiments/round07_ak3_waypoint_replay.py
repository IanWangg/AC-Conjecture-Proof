"""Replay the cap-30 ordinary path to the exact marked energy-23 pair."""

import argparse
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from elementary_verify import replay
from free_waypoint_search import canonical, cyclic, normalize
from round03_ak3_escape_replay import START, compile_path
from round05_ak3_lift_orbit_path import literal_route
from round05_ak3_orbit_audit import MAPS
from stallings_search import apply

TARGET = ("XXXYxyxyXYY", "XYXYYXyXYYXy")
SWAP = (
    {"op": "multiply", "i": 0, "j": 1},
    {"op": "invert", "i": 0},
    {"op": "multiply", "i": 1, "j": 0},
    {"op": "invert", "i": 1},
    {"op": "multiply", "i": 0, "j": 1},
    {"op": "invert", "i": 0},
)


def marked_pair(state):
    return tuple(map(canonical, state))


def translate(state, marking):
    return tuple(word.translate(marking) for word in state)


def entry_to_marking(marked_seed, path_search):
    target = tuple(sorted(marked_pair(marked_seed)))
    start = tuple(sorted(marked_pair(START)))
    if target == start:
        return compile_path([start], 22)[0]
    with TemporaryDirectory() as scratch:
        root = Path(scratch)
        target_file = root / "target.tsv"
        route_file = root / "route.json"
        target_file.write_text("\t".join(target) + "\n")
        subprocess.run([str(path_search), "22", str(target_file), str(route_file)],
                       check=True, capture_output=True)
        route = json.loads(route_file.read_text())
    return compile_path(list(map(tuple, route["route"])), 22)[0]


def marked_certificate(core, path_search, cap):
    target = marked_pair(TARGET)
    for marking in MAPS:
        achieved = marked_pair(translate(core["target"], marking))
        if achieved in (target, target[::-1]):
            break
    else:
        raise ValueError("orbit path does not end at W23")
    reversed_slots = achieved != target
    marked_seed = translate(START, marking)
    seed = entry_to_marking(marked_seed, path_search)
    state = tuple(seed["target"])
    moves = seed["moves"].copy()
    wanted = marked_seed[::-1] if reversed_slots else marked_seed
    if marked_pair(state) != marked_pair(wanted):
        for move in SWAP:
            state = apply(state, move)
            moves.append(move)
    for i, row in enumerate(wanted):
        state, extra = normalize(state, i, row)
        moves.extend(extra)
    assert state == wanted
    seed_prefix = len(moves)
    for move in core["moves"]:
        step = move.copy()
        if step["op"] == "conjugate":
            step["g"] = step["g"].translate(marking)
        if reversed_slots:
            step["i"] = 1 - step["i"]
            if "j" in step:
                step["j"] = 1 - step["j"]
        state = apply(state, step)
        moves.append(step)
    for i, row in enumerate(TARGET):
        state, extra = normalize(state, i, row)
        moves.extend(extra)
    assert state == TARGET
    certificate = {"format": "ordinary-ac-elementary-v1", "start": list(START),
                   "target": list(TARGET), "moves": moves}
    summary = replay(certificate)
    peak = sum(map(len, START))
    state = START
    for step in moves:
        state = apply(state, step)
        peak = max(peak, sum(len(cyclic(word)) for word in state))
    assert peak == cap
    summary.update(cyclic_peak=peak, seed_prefix_moves=seed_prefix,
                   transported_core_moves=len(core["moves"]),
                   ambient_signed_marking="xXyY".translate(marking),
                   swapped_slot_instructions=reversed_slots)
    return certificate, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("prefix", "bridge", "literal_path_binary", "certificate"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--continue-route", type=Path)
    args = parser.parse_args()
    prefix = json.loads(args.prefix.read_text())
    bridge = json.loads(args.bridge.read_text())
    assert prefix["orbit_route"][-1] == bridge["orbit_route"][0]
    cap = bridge["cyclic_cap"]
    route = prefix["orbit_route"] + bridge["orbit_route"][1:]
    if args.continue_route:
        continuation = json.loads(args.continue_route.read_text())
        assert route[-1] == continuation["orbit_route"][0]
        route.extend(continuation["orbit_route"][1:])
        cert, summary = compile_path(literal_route(route, cap), cap)
        summary["continuation_products"] = continuation["macro_distance"]
    else:
        core, _ = compile_path(literal_route(route, cap), cap)
        cert, summary = marked_certificate(core, args.literal_path_binary, cap)
    summary["products_to_bridge"] = len(prefix["orbit_route"]) - 1
    summary["products_from_bridge_to_w23"] = bridge["macro_distance"]
    args.certificate.write_text(json.dumps(cert, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
