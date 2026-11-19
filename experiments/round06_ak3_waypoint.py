"""Lift the bounded AK(3) route to the exact marked stable waypoint."""

import argparse
import json
from pathlib import Path

from elementary_verify import replay
from free_waypoint_search import canonical, cyclic, normalize
from round03_ak3_escape_replay import START, compile_route
from round05_ak3_lift_orbit_path import lift
from round05_ak3_orbit_audit import MAPS
from stallings_search import apply

TARGET = ("XXyxYxyXYxyXYxY", "XXyyxYY")


def marked_waypoint(orbit_route, seed_route):
    core, orbit_result = lift(orbit_route)
    marking, = (m for m in MAPS if tuple(canonical(word.translate(m)) for word in core["target"]) == TARGET)
    marked_seed = tuple(word.translate(marking) for word in START)
    assert tuple(sorted(map(canonical, marked_seed))) == tuple(seed_route["route"][-1])
    seed_length = max(sum(map(len, state)) for state in seed_route["route"])
    seed, seed_result = compile_route({**seed_route, "cyclic_cap": seed_length})
    state = tuple(seed["target"])
    moves = seed["moves"].copy()
    for slot, word in enumerate(marked_seed):
        state, extra = normalize(state, slot, word)
        moves.extend(extra)
    assert state == marked_seed
    marked_start_step = len(moves)

    for plain in core["moves"]:
        step = plain.copy()
        if step["op"] == "conjugate":
            step["g"] = step["g"].translate(marking)
        state = apply(state, step)
        moves.append(step)
    assert state == tuple(w.translate(marking) for w in core["target"])
    for slot, word in enumerate(TARGET):
        state, extra = normalize(state, slot, word)
        moves.extend(extra)
    assert state == TARGET
    certificate = {"format": "ordinary-ac-elementary-v1", "start": list(START),
                   "target": list(TARGET), "moves": moves}
    result = replay(certificate)
    state = START
    energies = [sum(len(cyclic(w)) for w in state)]
    for step in moves:
        state = apply(state, step)
        energies.append(sum(len(cyclic(w)) for w in state))
    assert max(energies) == orbit_route["cyclic_cap"] == 29
    return certificate, {
        **result, "cyclic_peak": max(energies),
        "seed_strict_moves_before_alignment": seed_result["moves"],
        "seed_peak_cyclic_length": seed_result["cyclic_peak"],
        "seed_alignment_complete_step": marked_start_step,
        "orbit_route_strict_moves": orbit_result["moves"],
        "transported_marking": "xXyY".translate(marking),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("orbit_route", "seed_route", "certificate"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    certificate, result = marked_waypoint(
        json.loads(args.orbit_route.read_text()), json.loads(args.seed_route.read_text()),
    )
    args.certificate.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
