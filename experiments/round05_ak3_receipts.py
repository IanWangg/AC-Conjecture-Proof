"""Combine the cap searches, controls and primitive audits into one receipt."""

import argparse
from hashlib import sha256
import json
from pathlib import Path


def file_hash(path):
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def receipts(work, cap26, cap27, reverse56, certificate, certificate28):
    def read(name):
        return json.loads((work / name).read_text())

    diff = read("diff/catalogue.json")
    escape = read("escape.json")
    replay = read("escape-replay.json")
    escape_orbit_control = read("escape27.orbit-control.json")
    replay_orbit_control = read("escape27.control-replay.json")
    rotational = read("two-copy.json")
    disjoint = read("disjoint-counts.json")
    basis27 = read("basis-matches56.json")
    basis28 = read("c28.basis-matches56.json")
    generation = read("c28.orbit.json")
    closure = read("c28.verify.json")
    primitive = read("c28.primitive.json")
    expanded = read("c28.expanded.json")
    diff28 = read("diff28/catalogue.json")
    escape28 = read("escape28.orbit.json")
    replay28 = read("escape28.replay.json")
    projection28 = read("stable-projection28.json")
    assert diff["minimum_escape_energy"] == 16
    assert diff["all_escapes"]["16"] == 8 == escape["target_count"]
    assert escape["minimum_macro_distance"] == sum(escape["disjoint_ball_radii"]) + 1
    assert escape["minimum_macro_distance"] == escape_orbit_control["minimum_macro_distance"]
    assert replay["cyclic_peak"] == 27 == escape["cyclic_cap"]
    assert sorted(replay["endpoint"]) == escape["route"][-1]
    assert rotational["positive"] == rotational["incomplete"] == 0
    assert len(disjoint["lengths"]) == 8
    assert all(item["positive"] == item["incomplete"] == 0 for item in disjoint["lengths"].values())
    assert basis27["status"] == basis28["status"] == "NO_SUBGROUP_JOIN"
    assert closure["status"] == "CLOSED_AND_CONNECTED"
    assert not primitive["primitive_coordinates"] and generation["primitive_coordinate_orbits"] == 0
    assert primitive["rows"] == closure["signed_permutation_orbits"] == generation["signed_permutation_orbits"]
    assert generation["rotation_product_candidates"] == closure["rotation_product_candidates"]
    assert generation["admitted_neighbors"] == closure["admitted_neighbors"]
    assert expanded["expanded_rows"] == basis28["forward_pairs"]
    assert diff28["all_escapes"] == {"16": 8}
    assert escape28["minimum_macro_distance"] == sum(escape28["disjoint_ball_radii"]) + 1
    assert replay28["cyclic_peak"] == 28 and not projection28["present"]
    return {
        "status": "CHECKED_BOUNDED_SEARCHES",
        "ordinary_AC_goal_solved": False,
        "minimum_required_cyclic_peak": 29,
        "input_sha256": {"cap26_tsv": file_hash(cap26), "cap27_tsv": file_hash(cap27),
                         "reverse56_tsv": file_hash(reverse56)},
        "cap27_reverse_basis_index": basis27,
        "cap28_reverse_basis_index": basis28,
        "cap27_escape_catalogue": diff,
        "cap27_shortest_escape": {
            **escape,
            "certificate_sha256": file_hash(certificate),
            "strict_moves": replay["moves"],
            "raw_peak": replay["peak_total_length"],
            "cyclic_peak": replay["cyclic_peak"],
            "endpoint": replay["endpoint"],
            "orbit_partition": read("lowest.partition.json"),
        },
        "cap27_shortest_escape_orbit_control": {
            key: escape_orbit_control[key] for key in ("minimum_macro_distance", "disjoint_ball_radii", "products_checked")
        } | {"strict_moves": replay_orbit_control["moves"], "cyclic_peak": replay_orbit_control["cyclic_peak"]},
        "cap27_escape_intersecting_axis_first_phase": rotational,
        "cap27_escape_disjoint_axis_first_phase": disjoint,
        "cap28_short_escape_catalogue_through_energy_16": diff28,
        "cap28_shortest_escape": {
            **escape28,
            "certificate_sha256": file_hash(certificate28),
            "strict_moves": replay28["moves"],
            "raw_peak": replay28["peak_total_length"],
            "cyclic_peak": replay28["cyclic_peak"],
            "endpoint": replay28["endpoint"],
            "orbit_partition": read("lowest28.partition.json"),
        },
        "cap28_stable_proof_projection_membership": projection28,
        "cap28_signed_orbit_generation": generation,
        "cap28_signed_orbit_verification": closure,
        "cap28_signed_orbit_primitive_audit": primitive,
        "cap28_literal_expansion": {**expanded, "tsv_sha256": file_hash(work / "c28.expanded.tsv")},
        "cap22_literal_orbit_control": read("c22.compare.json"),
        "cap22_seed_image_control": read("c22.seed.json"),
        "cap22_closure_control": read("c22.verify.json"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("work", "cap26", "cap27", "reverse56", "certificate", "certificate28"):
        parser.add_argument(arg, type=Path)
    args = parser.parse_args()
    print(json.dumps(receipts(args.work, args.cap26, args.cap27, args.reverse56,
                              args.certificate, args.certificate28), indent=2))


if __name__ == "__main__":
    main()
