"""Compile the donor-free rank-three chart and destabilize its isolated letter."""

import argparse
import json
from pathlib import Path

from round03_stable_proof_pivot import canonical
from round04_stable_proof_paths import edge, replay
from round06_stable_proof_strict_escape import StrictPath
from round09_stable_proof_lift_excursion import signed_rows
from round15_stable_proof_splice import align, statistics


def lift_route(start, route):
    states = {tuple(map(canonical, start)): []}
    assert tuple(sorted(next(iter(states)))) in signed_rows(route[0])
    for orbit in route[1:]:
        images = sorted(signed_rows(orbit))
        next_states = {}
        for state, prefix in states.items():
            for target in images:
                if len(set(state) & set(target)) < 2:
                    continue
                local_cap = max(sum(map(len, state)), sum(map(len, target)))
                try:
                    endpoint, steps = edge(state, target, local_cap, "xXyYzZ")
                except ValueError:
                    continue
                candidate = prefix + steps
                if endpoint not in next_states or len(candidate) < len(next_states[endpoint]):
                    next_states[endpoint] = candidate
        assert next_states
        states = next_states
    isolated = [
        (len(moves), rows, moves)
        for rows, moves in states.items()
        if "Z" in rows and sum("z" in word.lower() for word in rows) == 1
    ]
    assert isolated
    _, rows, moves = min(isolated, key=lambda entry: entry[:2])
    return rows, moves


def compile_release(ordinary, released, route, output):
    replay(released)
    goal, moves = lift_route(tuple(released["target"]), route)
    short = {entry[0] for entry in signed_rows(("xxyXYY",) * 3)}
    with output.open("wb") as sink:
        path = StrictPath(ordinary["start"], sink)
        path.extend(ordinary["moves"])
        path.add({"op": "stabilize", "generator": "z"})
        assert path.rows == released["start"]
        path.extend(released["moves"])
        old_count = path.total
        assert set(map(canonical, path.rows)).isdisjoint(short)
        for slot, word in enumerate(path.rows):
            align(path, slot, canonical(word))
        for move in moves:
            path.add(move)
            assert set(map(canonical, path.rows)).isdisjoint(short)
        assert tuple(path.rows) == goal
        slot = goal.index("Z")
        align(path, slot, "z")
        path.add({"op": "destabilize", "generator": "z", "i": slot})
        path.record((json.dumps({"target": path.rows}, separators=(",", ":")) + "\n").encode())
        return statistics(path) | {"tail_products": len(route) - 1,
                                   "tail_instructions_including_deletion": path.total - old_count}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ordinary", type=Path)
    parser.add_argument("release", type=Path)
    parser.add_argument("orbit_route", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    route = [tuple(line.split()) for line in args.orbit_route.read_text().splitlines()]
    result = compile_release(json.loads(args.ordinary.read_text()), json.loads(args.release.read_text()),
                             route, args.output)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
