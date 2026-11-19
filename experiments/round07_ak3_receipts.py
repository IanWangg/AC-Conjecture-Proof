"""Assemble checked receipts from the cap-30 and waypoint searches."""

import argparse
import json
from pathlib import Path


def read(directory, name):
    return json.loads((directory / f"{name}.json").read_text())


def check_closure(generated, checked):
    assert checked["status"] == "CLOSED_AND_CONNECTED"
    for key in ("cyclic_cap", "signed_permutation_orbits", "rotation_product_candidates",
                "admitted_neighbors"):
        assert checked[key] == generated[key]


def summarize(directory):
    cap22 = read(directory, "c22.orbit")
    checked22 = read(directory, "c22.verify")
    check_closure(cap22, checked22)
    assert cap22["signed_permutation_orbits"] == 32363

    cap30 = read(directory, "c30.orbit")
    primitive30 = read(directory, "c30.primitive")
    reverse30 = read(directory, "c30.reverse56")
    assert (cap30["signed_permutation_orbits"] == primitive30["rows"]
            == reverse30["forward_pairs"] == 73876424)
    assert cap30["w23_found"]
    assert cap30["primitive_coordinate_orbits"] == 0 and not primitive30["primitive_coordinates"]
    assert reverse30["status"] == "NO_SUBGROUP_JOIN"
    closure = directory / "c30.verify.json"
    checked30 = read(directory, "c30.verify") if closure.exists() and closure.stat().st_size else None
    if checked30 is not None:
        check_closure(cap30, checked30)

    bridge = read(directory, "waypoint30")
    bridge_route = read(directory, "waypoint30.bridge.route")
    prefix_route = read(directory, "waypoint30.prefix.route")
    marked = read(directory, "waypoint30.marked.replay")
    assert bridge["hit_cap29"] and not bridge["hit_primitive"]
    assert bridge["completed_radius"] + 1 == bridge_route["macro_distance"] == 17
    assert prefix_route["minimum_macro_distance"] == marked["products_to_bridge"] == 26
    assert marked["cyclic_peak"] == 30 and marked["moves"] == 956
    assert marked["endpoint"] == ["XXXYxyxyXYY", "XYXYYXyXYYXy"]

    component = read(directory, "waypoint29")
    component_verified = read(directory, "waypoint29.verify")
    component_replay = read(directory, "waypoint29.chamber18.replay")
    assert component["closed_component"] and not component["hit_cap29"]
    assert component_verified["status"] == "CLOSED_AND_CONNECTED"
    assert component_verified["signed_permutation_orbits"] == component["states_discovered"] == 3745
    assert component_verified["rotation_product_candidates"] == component["product_candidates"]
    assert component_verified["admitted_neighbors"] == component["admitted_products"]
    assert component["minimum_discovered_energy"] == sum(map(len, component_replay["endpoint"])) == 18
    assert component_replay["cyclic_peak"] == 30 and component_replay["moves"] == 846
    component_reverse = read(directory, "waypoint29.reverse56")
    assert component_reverse["status"] == "NO_SUBGROUP_JOIN"
    component_primitive = read(directory, "waypoint29.primitive")
    assert component_primitive["rows"] == 3745 and not component_primitive["primitive_coordinates"]

    low = read(directory, "c30.low22")
    low_geometry = read(directory, "c30.low22.geometry")
    low_join = read(directory, "c30.low22.two-copy")
    assert low["new_orbits_by_energy"] == {"18": 1, "19": 2, "20": 10, "21": 37, "22": 45}
    assert low_join["positive"] == low_join["incomplete"] == 0
    assert not low_geometry["remaining"] and low_geometry["source_pairs"] == 95
    component_geometry = read(directory, "waypoint29.geometry")
    assert not component_geometry["remaining"] and component_geometry["source_pairs"] == 3745
    frozen = read(directory, "chamber18.frozen36")
    assert len(frozen) == 2 and all(case["primitive_recipients"] == 0 for case in frozen)
    return {
        "ordinary_AC_goal_solved": False,
        "cap22_wide_control": {"generator": cap22, "independent_checker": checked22},
        "cap30_generator": cap30,
        "cap30_independent_closure": checked30,
        "cap30_independent_primitive_screen": primitive30,
        "cap30_reverse56": reverse30,
        "minimum_cyclic_peak_before_primitive": 31 if checked30 else 30,
        "w23_minimum_cyclic_entry_peak": 30,
        "w23_bridge_search": bridge,
        "w23_bridge_route": bridge_route,
        "w23_cap29_prefix": prefix_route,
        "w23_strict_replay": marked,
        "w23_cap29_component": {
            "generator": component,
            "independent_checker": component_verified,
            "primitive_screen": component_primitive,
            "reverse56": component_reverse,
            "geometry": component_geometry,
            "lowest_energy_route": read(directory, "waypoint29.lowest.route"),
        },
        "energy18_entry_strict_replay": {
            key: value for key, value in component_replay.items() if key != "macro_boundary_receipts"
        },
        "energy18_frozen_cap36": frozen,
        "cap30_new_through_energy22": low,
        "cap30_new_low_geometry": low_geometry,
        "cap30_new_low_two_copy": low_join,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(summarize(args.directory), indent=2))


if __name__ == "__main__":
    main()
