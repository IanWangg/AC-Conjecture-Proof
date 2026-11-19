"""Extend a checked cap-29 orbit route by a prescribed outward product path."""

import argparse
import json
from pathlib import Path

from elementary_verify import replay
from free_waypoint_search import canonical, cyclic, expand_edge, inverse, variants, words_upto
from round05_ak3_lift_orbit_path import images, lift
from stallings_search import apply


def continue_route(entry, continuation):
    certificate, _ = lift(entry)
    state = tuple(certificate["target"])
    route = continuation["minimum_energy_route"]
    cap = continuation["cap"]
    assert tuple(sorted(state)) in images(route[0])
    continuation_steps = []
    for expected in route[1:]:
        targets = images(expected)
        candidates = []
        for slot, receiver in enumerate(state):
            donor = state[1 - slot]
            bound = max(0, (cap - len(receiver) - 2 * len(donor)) // 2)
            for a in variants(receiver):
                for b in variants(donor):
                    for tail in words_upto(bound):
                        product = canonical(a + tail + b + inverse(tail))
                        if tuple(sorted((product, donor))) not in targets:
                            continue
                        nxt, moves = expand_edge(state, (slot, a, b, tail))
                        assert tuple(sorted(nxt)) in targets
                        candidates.append((len(moves), slot, a, b, tail, nxt, moves))
        assert candidates, (state, expected)
        *_, state, moves = min(candidates)
        certificate["moves"].extend(moves)
        continuation_steps.append(len(certificate["moves"]))
    certificate["target"] = list(state)
    result = replay(certificate)
    state = tuple(certificate["start"])
    cyclic_peak = sum(len(cyclic(word)) for word in state)
    for move in certificate["moves"]:
        state = apply(state, move)
        cyclic_peak = max(cyclic_peak, sum(len(cyclic(word)) for word in state))
    assert cyclic_peak <= cap
    return certificate, {**result, "cyclic_peak": cyclic_peak,
                         "continuation_step_indices": continuation_steps}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("entry", "continuation", "certificate"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    certificate, result = continue_route(
        json.loads(args.entry.read_text()), json.loads(args.continuation.read_text()),
    )
    args.certificate.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
