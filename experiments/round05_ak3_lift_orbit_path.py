"""Lift each quotient edge in the original marked free basis and replay strictly."""

import argparse
import json
from pathlib import Path

from free_waypoint_search import canonical, inverse, variants, words_upto
from round03_ak3_escape_replay import START, compile_route
from round05_ak3_orbit_audit import word_orbit


def images(pair):
    return {tuple(sorted(item)) for item in zip(*(word_orbit(word) for word in pair))}


def lift(record):
    route = [tuple(sorted(map(canonical, START)))]
    cap = record["cyclic_cap"]
    assert route[0] in images(record["orbit_route"][0])
    for orbit_target in record["orbit_route"][1:]:
        target_images = images(orbit_target)
        candidates = set()
        state = route[-1]
        for a, b in (state, state[::-1]):
            if all(b not in target for target in target_images):
                continue
            bound = max(0, (cap - len(a) - 2 * len(b)) // 2)
            for u in variants(a):
                for v in variants(b):
                    for q in words_upto(bound):
                        product = canonical(u + q + v + inverse(q))
                        target = tuple(sorted((product, b)))
                        if target in target_images:
                            candidates.add(target)
        assert candidates, (state, orbit_target)
        route.append(min(candidates))
    return compile_route({**record, "route": route})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("orbit_route", "certificate", "replay"):
        parser.add_argument(arg, type=Path)
    args = parser.parse_args()
    certificate, replay = lift(json.loads(args.orbit_route.read_text()))
    args.certificate.write_text(json.dumps(certificate, indent=2) + "\n")
    args.replay.write_text(json.dumps(replay, indent=2) + "\n")


if __name__ == "__main__":
    main()
