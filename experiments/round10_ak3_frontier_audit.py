"""Check complete small frontier catalogues and replay their saved anchored routes."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
from random import Random
from struct import Struct

from elementary_verify import replay
from free_waypoint_search import canonical, normalize
from round04_stable_proof_paths import edge
from round07_stable_proof_compile_join import lift_from
from round08_ak3_acm_search import cyclic_peak


WORD_LETTERS = "xXyY"
PARENT_RECORD = Struct("=QQQQ")


def packed_word(code):
    digits = []
    while code > 1:
        digits.append(WORD_LETTERS[code & 3])
        code >>= 2
    assert code == 1 and digits
    return "".join(reversed(digits))


def parse_words(path):
    return {tuple(line.split()) for line in path.read_text().splitlines()}


def parent_records(path):
    for a, b, c, d in PARENT_RECORD.iter_unpack(path.read_bytes()):
        yield (packed_word(a), packed_word(b)), (packed_word(c), packed_word(d))


def strict_route(record, entry=None):
    cap = record["cyclic_cap"]
    start = tuple(entry["target"] if entry else record["lower_anchor"])
    state = start
    moves = []
    for i in range(2):
        state, instructions = normalize(state, i, canonical(state[i]))
        moves.extend(instructions)
    rows = lift_from(state, record["orbit_route"], cap)
    for target in rows[1:]:
        state, instructions = edge(state, target, cap, "xXyY")
        moves.extend(instructions)
    certificate = {"format": "ordinary-ac-elementary-v1", "start": list(start),
                   "target": list(state), "moves": moves}
    if entry:
        assert tuple(entry["target"]) == start
        certificate["start"] = entry["start"]
        certificate["moves"] = entry["moves"] + moves
    verified = replay(certificate)
    verified["cyclic_peak"] = cyclic_peak(certificate)
    assert verified["cyclic_peak"] == cap
    return certificate, verified


def audit(lower, full, prefix, split):
    old = parse_words(lower)
    full_component = parse_words(full)
    new_path = Path(str(prefix) + ".outside.tsv")
    new = parse_words(new_path)
    assert old <= full_component and not old & new and full_component - old == new
    if split:
        assert new_path.read_bytes() == Path(str(split) + ".outside.tsv").read_bytes()
    seed = json.loads(Path(str(prefix) + ".boundary.json").read_text())
    walk = json.loads(Path(str(prefix) + ".outside.json").read_text())
    assert seed["source_reached_eof"] and seed["start_offset"] == 0
    assert seed["source_rows_scanned"] == len(old) and walk["lower_orbits"] == len(old)
    assert walk["outside_orbits"] == len(new) and walk["closure_reached_from_listed_seeds"]
    cap = seed["cyclic_cap"]
    seeds = set()
    boundary_path = Path(str(prefix) + ".boundary.bin")
    for child, parent in parent_records(boundary_path):
        assert parent in old and child in new and sum(map(len, child)) == cap
        seeds.add(child)
    assert len(seeds) == walk["unique_seed_orbits"]
    assert boundary_path.stat().st_size == PARENT_RECORD.size * seed["boundary_records"]
    discovered = set()
    records = list(parent_records(Path(str(prefix) + ".outside.parents.bin")))
    for child, parent in records:
        assert child in new and child not in discovered and (parent in old or parent in discovered)
        discovered.add(child)
    assert discovered == new
    chosen = Random(130 + cap).sample(records, 24)
    for child, parent in chosen:
        edge_cap = max(sum(map(len, child)), sum(map(len, parent)))
        strict_route({"cyclic_cap": edge_cap, "lower_anchor": parent, "orbit_route": [parent, child]})
    route = json.loads(Path(str(prefix) + ".minimum.route.json").read_text())
    assert tuple(route["lower_anchor"]) in old and all(tuple(pair) in new for pair in route["orbit_route"][1:])
    _, replayed = strict_route(route)
    return {"exact_set_comparison": "PASS", "split_resume_comparison": bool(split),
            "full_orbits": len(full_component), "new_orbits": len(new),
            "outside_catalogue_sha256": sha256(new_path.read_bytes()).hexdigest(),
            "parent_records_structurally_verified": len(records), "sample_parent_edges_strictly_replayed": len(chosen),
            "seed": seed, "expansion": walk, "minimum_energy_anchored_route": route,
            "minimum_energy_anchored_route_replay": replayed}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("lower", "full", "prefix"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--split", type=Path)
    options = parser.parse_args()
    print(json.dumps(audit(**vars(options)), indent=2))
