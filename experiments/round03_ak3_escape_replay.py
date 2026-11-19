"""Compile and exactly replay each edge of the shortest cap-25 escape route."""

import argparse
import json
from pathlib import Path

from elementary_verify import replay
from free_waypoint_search import (
    canonical, cyclic, expand_edge, inverse, normalize, variants, words_upto,
)
from stallings_search import apply


START = ("xxxYYYY", "xyxYXY")


def compile_route(record):
    route = [tuple(row) for row in record["route"]]
    cap = record["cyclic_cap"]
    assert len(route) == record["minimum_macro_distance"] + 1
    assert 1 + sum(record["disjoint_ball_radii"]) == record["minimum_macro_distance"]
    certificate, summary = compile_path(route, cap)
    assert summary["cyclic_peak"] == cap
    return certificate, summary


def compile_path(route, cap):
    assert all(sum(map(len, state)) <= cap for state in route)
    state = START
    ledger = []
    for i in (0, 1):
        state, moves = normalize(state, i, canonical(state[i]))
        ledger.extend(moves)
    assert tuple(sorted(state)) == route[0]
    receipts = [{"strict_step": len(ledger), "state": list(state)}]
    for expected in route[1:]:
        candidates = []
        for i in (0, 1):
            j = 1 - i
            if state[j] not in expected:
                continue
            bound = max(0, (cap - len(state[i]) - 2 * len(state[j])) // 2)
            for u in variants(state[i]):
                for v in variants(state[j]):
                    for q in words_upto(bound):
                        product = canonical(u + q + v + inverse(q))
                        if tuple(sorted((product, state[j]))) != expected:
                            continue
                        result, moves = expand_edge(state, (i, u, v, q))
                        assert tuple(sorted(result)) == expected
                        candidates.append((len(moves), u, v, q, result, moves))
        assert candidates, (state, expected)
        _, _, _, _, state, moves = min(candidates, key=lambda c: c[:4])
        ledger.extend(moves)
        receipts.append({"strict_step": len(ledger), "state": list(state)})
    certificate = {
        "format": "ordinary-ac-elementary-v1",
        "start": list(START),
        "target": list(state),
        "moves": ledger,
    }
    summary = replay(certificate)
    state = START
    energies = [sum(len(cyclic(word)) for word in state)]
    for move in ledger:
        state = apply(state, move)
        energies.append(sum(len(cyclic(word)) for word in state))
    summary["cyclic_peak"] = max(energies)
    summary["macro_boundary_receipts"] = receipts
    assert summary["cyclic_peak"] <= cap
    return certificate, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("route", type=Path)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    cert, summary = compile_route(json.loads(args.route.read_text()))
    args.certificate.write_text(json.dumps(cert, indent=2) + "\n")
    args.output.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
