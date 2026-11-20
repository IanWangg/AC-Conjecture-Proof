"""Find and replay sharp cap-32 entries from the marked energy-17 waypoint."""

import argparse
from collections import Counter
import json
from pathlib import Path

from euclidean_primitive_audit import primitive_cyclic_word
from round10_ak3_frontier_audit import parent_records, strict_route


def energy(pair):
    return sum(map(len, pair))


def bounded_keys(path, limit):
    previous = 0
    with path.open("rb") as stream:
        for row in stream:
            size = len(row) - 2
            assert size >= previous
            previous = size
            if size > limit:
                break
            yield row


def witness_route(parent, endpoint, anchor):
    route = [endpoint]
    while route[-1] != anchor:
        route.append(parent[route[-1]])
    return route[::-1]


def audit(prefix, catalogue, entry, destination, bound):
    entry = json.loads(entry.read_text())
    anchor = tuple(entry["target"])
    assert energy(anchor) == 17
    new_path = Path(str(prefix) + ".outside.tsv")
    low = set(bounded_keys(new_path, bound))
    old = set()
    lower_rows_screened = 0
    for key in bounded_keys(catalogue, bound):
        lower_rows_screened += 1
        if key in low:
            old.add(key)
    absent = {tuple(row.decode().split()) for row in low - old}
    assert absent
    assert all(not any(primitive_cyclic_word(word) for word in pair) for pair in absent)
    ledger = dict(parent_records(Path(str(prefix) + ".outside.parents.bin")))
    shortest = min(map(energy, absent))
    routes = [witness_route(ledger, target, anchor) for target in absent if energy(target) == shortest]
    route = min(routes, key=lambda candidate: (len(candidate), candidate))
    anchored = {"cyclic_cap": 32, "lower_anchor": anchor, "orbit_route": route}
    certificate, summary = strict_route(anchored, entry)
    assert energy(summary["endpoint"]) == shortest
    destination.write_text(json.dumps(certificate, separators=(",", ":")) + "\n")
    return {"cap31_membership_bound": bound, "cap31_rows_compared": lower_rows_screened,
            "reached_rows_through_bound": len(low), "present_in_cap31": len(old),
            "absent_from_cap31_by_energy": dict(sorted(Counter(energy(pair) for pair in absent).items())),
            "absent_from_cap31_at_energy_at_most_31": sorted(pair for pair in absent if energy(pair) <= 31),
            "minimal_energy_reached_outside_cap31": shortest,
            "primitive_coordinates_among_candidates_outside_cap31": 0,
            "chosen_anchor_route": anchored, "strict_replay": summary,
            "entry_moves": len(entry["moves"]), "suffix_moves": summary["moves"] - len(entry["moves"])}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("prefix", "catalogue", "entry", "destination"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--bound", type=int, default=32)
    args = parser.parse_args()
    print(json.dumps(audit(**vars(args)), indent=2))
