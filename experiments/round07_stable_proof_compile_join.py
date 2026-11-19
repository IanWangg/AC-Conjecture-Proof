"""Lift each cap-31 join from the signed orbit graph to the fixed marking."""

import argparse
import json
from pathlib import Path

from elementary_verify import replay as replay_strict
from free_waypoint_search import canonical, cyclic, inverse, normalize, variants, words_upto
from round03_ak3_escape_replay import START, compile_path
from round04_stable_proof_paths import edge
from round05_ak3_lift_orbit_path import images
from round07_stable_proof_local_audit import MARKED, STARTS
from stallings_search import apply


def lift_from(start, orbit_path, cap):
    state = tuple(sorted(map(canonical, start)))
    assert state in images(orbit_path[0])
    lifted = [state]
    for goal in orbit_path[1:]:
        wanted = images(goal)
        possibilities = set()
        for a, b in (state, state[::-1]):
            if all(b not in pair for pair in wanted):
                continue
            bound = max(0, (cap - len(a) - 2 * len(b)) // 2)
            for u in variants(a):
                for v in variants(b):
                    for q in words_upto(bound):
                        candidate = tuple(sorted((canonical(u + q + v + inverse(q)), b)))
                        if candidate in wanted:
                            possibilities.add(candidate)
        assert possibilities, (state, goal)
        state = min(possibilities)
        lifted.append(state)
    return lifted


def prepare(work, case):
    local_route = ("cap31_anchored", "minimum28_c31", "minimum29_c31", "marked0_c37")[case]
    anchor_route = ("anchor26", "anchor28", "anchor29", "anchor_marked0")[case]
    peak = (31, 31, 31, 37)[case]
    with (work / (local_route + ".route.tsv")).open() as f:
        there = lift_from((*STARTS, MARKED)[case], [tuple(line.split()) for line in f], peak)
    root_to_anchor = json.loads((work / (anchor_route + ".orbit.json")).read_text())["orbit_route"]
    back = lift_from(there[-1], root_to_anchor[::-1], 29)
    assert back[-1] in images(START)
    return dict(literal_route_back_to_signed_AK3=back, literal_route_to_anchor=there,
                signed_AK3=back[-1], cyclic_cap=peak)


def finish(pieces, route_to_signed_root):
    assert tuple(route_to_signed_root[-1]) == tuple(pieces["signed_AK3"])
    route = route_to_signed_root + pieces["literal_route_back_to_signed_AK3"][-2::-1]
    route += pieces["literal_route_to_anchor"][-2::-1]
    cap = pieces["cyclic_cap"]
    compiler = compile_path if cap <= 31 else compile_local_caps
    certificate, replay = compiler([tuple(row) for row in route], cap)
    assert replay["cyclic_peak"] == cap and sorted(map(canonical, certificate["target"])) == route[-1]
    return certificate, replay


def compile_local_caps(route, cap):
    state = START
    moves = []
    for i in range(2):
        state, steps = normalize(state, i, canonical(state[i]))
        moves.extend(steps)
    assert tuple(sorted(state)) == route[0]
    for source, destination in zip(route, route[1:]):
        local_cap = max(sum(map(len, source)), sum(map(len, destination)))
        assert local_cap <= cap
        state, local = edge(state, destination, local_cap, "xXyY")
        moves.extend(local)
    certificate = dict(format="ordinary-ac-elementary-v1", start=list(START), target=list(state), moves=moves)
    replay = replay_strict(certificate)
    state = START
    energies = [sum(map(len, START))]
    for move in moves:
        state = apply(state, move)
        energies.append(sum(len(cyclic(row)) for row in state))
    replay["cyclic_peak"] = max(energies)
    return certificate, replay


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "finish"))
    parser.add_argument("work", type=Path)
    parser.add_argument("case", type=int)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    segments = args.work / f"literal_segments{args.case}.json"
    if args.mode == "prepare":
        pieces = prepare(args.work, args.case)
        segments.write_text(json.dumps(pieces, indent=2) + "\n")
        print(*pieces["signed_AK3"], sep="\t")
    else:
        assert args.certificate is not None
        pieces = json.loads(segments.read_text())
        prefix = json.loads((args.work / f"signed_root{args.case}.json").read_text())["route"]
        cert, replay = finish(pieces, prefix)
        args.certificate.write_text(json.dumps(cert, indent=2) + "\n")
        print(json.dumps(replay, indent=2))
