"""Collect and cross-check the recorded round-six search outputs."""

import argparse
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def collect(work, prior):
    def load(name):
        return read(work / f"{name}.json")

    cap28 = load("c28.reverse56-control")
    literal28 = read(prior)["cap28_reverse_basis_index"]
    representation_fields = {"forward_pairs", "forward_distinct_words"}
    assert all(value == literal28[key] for key, value in cap28.items()
               if key not in representation_fields)
    cap29 = load("c29.reverse56")
    outward = load("outward32")
    primitives = load("outward32.primitive")
    outward_join = load("outward32.reverse56")
    outside_count = sum(layer["novel_orbits"] for layer in outward["layers"])
    assert outside_count == primitives["rows"] == outward_join["forward_pairs"]
    assert cap29["status"] == outward_join["status"] == "NO_SUBGROUP_JOIN"
    assert primitives["primitive_coordinates"] == outward["primitive_route"] == []
    intersecting = load("escape-short.two-copy")
    assert intersecting["positive"] == intersecting["incomplete"] == 0
    assert intersecting["DAG_absent"] + intersecting["exact_absent"] == (
        intersecting["own_tests"] + intersecting["distinct_vertex_joins"]
    )
    disjoint = load("energy17.disjoint")
    assert set(disjoint["lengths"]) == set("12345678")
    for row in disjoint["lengths"].values():
        assert row["positive"] == row["incomplete"] == row["exact_absent"] == 0
        assert row["dag_absent"] == row["distinct_cores"] + row["joins"]
    return {
        "ordinary_ak3_trivialization_found": False,
        "marked_waypoint": {
            "exact_minimum_cyclic_peak": 29,
            "orbit_route": load("stable-projection29.route"),
            "literal_route": load("waypoint.literal.route"),
            "relabeled_seed_route": load("seed-gamma.route"),
            "marked_low_raw_replay": load("marked-replay"),
            "literal_route_replay": load("waypoint.literal.replay"),
        },
        "cap28_compact_control": cap28,
        "cap29_reverse_join": cap29,
        "cap29_new_low_energy_orbits": load("low-escapes"),
        "cap29_energy17_route": load("energy17.orbit-route"),
        "cap29_energy17_replay": load("energy17.replay"),
        "cap29_escape_intersecting_axes_two_phase": intersecting,
        "cap29_energy17_disjoint_axes_two_phase": disjoint,
        "outward_cap32_search": outward,
        "outward_cap32_primitive_audit": primitives,
        "outward_cap32_reverse_join": outward_join,
        "outward_cap32_energy23_entry_route": load("outward32.entry"),
        "outward_cap32_energy23_strict_replay": load("outward32.replay"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path)
    parser.add_argument("round_five_receipt", type=Path)
    args = parser.parse_args()
    print(json.dumps(collect(args.work, args.round_five_receipt), indent=2))


if __name__ == "__main__":
    main()
