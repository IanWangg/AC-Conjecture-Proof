"""Combine closure and primitive checks for exact finite cyclic components."""

import argparse
from hashlib import sha256
import json
from pathlib import Path


def read_summary(folder, cap, kind):
    data = json.loads((folder / f"c{cap}_{kind}.json").read_text())
    data.pop("seconds", None)
    return data


def summarize(folder, cap):
    build = read_summary(folder, cap, "build")
    closure = read_summary(folder, cap, "verify")
    primitive = read_summary(folder, cap, "prim")
    catalogue = (folder / f"c{cap}.json").read_bytes()
    digest = sha256(catalogue).hexdigest()
    tsv_digest = sha256((folder / f"c{cap}.tsv").read_bytes()).hexdigest()
    if any(row["status"] != "PASS" for row in (build, closure, primitive)):
        raise ValueError(f"cap-{cap} has an unfinished stage")
    if (build["cyclic_cap"] != cap or closure["cyclic_cap"] != cap
            or not build["full_bridge_menu"]
            or not closure["closed_under_full_geometric_neighbor_menu"]
            or not closure["all_states_reachable_from_original_AK3"]
            or not closure["independent_free_reduction_and_Booth_canonicalizer"]):
        raise ValueError(f"cap-{cap} is missing closure checks")
    matches = (
        ("states", "canonical_states"),
        ("rotation_product_candidates", "all_menu_candidates_checked"),
        ("admitted_neighbors", "admitted_neighbor_checks"),
        ("minimum_cyclic_sum", "minimum_cyclic_sum"),
        ("minimum_cyclic_coordinate", "minimum_cyclic_coordinate"),
        ("minimum_disjoint_axes_neighbor_sum", "minimum_disjoint_axes_neighbor_sum"),
        ("histogram", "state_histogram"),
    )
    for built_field, audited_field in matches:
        if build[built_field] != closure[audited_field]:
            raise ValueError(f"cap-{cap}: generator and audit differ on {built_field}")
    if (primitive["catalogue_sha256"] != digest or primitive["states"] != build["states"]
            or closure["minimum_cyclic_coordinate"] <= 1 or primitive["primitive_coordinates"]):
        raise ValueError(f"cap-{cap} does not certify primitive-coordinate absence")
    return {
        "catalogue_sha256": digest,
        "catalogue_tsv_sha256": tsv_digest,
        "closure_and_connectedness": closure,
        "primitive_coordinate_audit": primitive,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment_folder", type=Path)
    parser.add_argument("caps", type=int, nargs="+")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    records = {cap: summarize(args.experiment_folder, cap) for cap in args.caps}
    result = {"ordinary_AC_goal_solved": False,
              "minimum_cyclic_peak_before_a_primitive_coordinate": max(args.caps) + 1,
              "cyclic_components": records}
    args.output.write_text(json.dumps(result, indent=2) + "\n")
