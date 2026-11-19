"""Check all-tail joins, archive catalogue overlap and map certificates."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile

from elementary_verify import replay
from primitive_map_pairs import fold
from rotation_fold_controls import unbased
from round01_ak3_archive import certificate, pair_key
from u_verify_native import verify_absence


def native_controls(binary):
    # <x, (yx)y(yx)^-1> has disjoint axes. The basis obtained by multiplying
    # its first word by the second has an intersecting-axes representation.
    moves = [("conjugate", 1, "XY"), ("multiply", 0, 1, "right")]
    actual_disjoint = certificate(("x", "y"), moves[:1])
    actual_mixed = certificate(("x", "y"), moves)
    disjoint_key = pair_key(actual_disjoint["target"])
    mixed_key = pair_key(actual_mixed["target"])
    canonical_graph = unbased(fold(actual_disjoint["target"]))
    if canonical_graph != unbased(fold(actual_mixed["target"])):
        raise ValueError("independent folding found different control subgroups")
    examples = [
        (mixed_key, disjoint_key, "FORWARD_INTERSECT_REVERSE_BARBELL"),
        (disjoint_key, mixed_key, "FORWARD_BARBELL_REVERSE_INTERSECT"),
        (pair_key(("xy", "y")), disjoint_key, "BOTH_INTERSECT"),
        (mixed_key, mixed_key, "EQUAL_CYCLIC_PAIR"),
        (pair_key(("xxxYYYY", "xyxYXY")), disjoint_key, "COMPLETE_NO_ALL_TAIL_SUBGROUP_MATCH"),
    ]
    reports = {}
    with tempfile.TemporaryDirectory(prefix="round01-ak3-all-tail-") as temp:
        path = Path(temp)
        first, second, result = (path / name for name in ("a.tsv", "b.tsv", "match.json"))
        for left, right, expected in examples:
            first.write_text("\t".join(left) + "\n")
            second.write_text("\t".join(right) + "\n")
            subprocess.run([str(binary.resolve()), str(first), str(second), str(result)], check=True)
            row = json.loads(result.read_text())
            if row["status"] != expected:
                raise ValueError(f"join control expected {expected}, got {row}")
            if "BARBELL" in expected and tuple(row["canonical_unbased_graph"]) != canonical_graph:
                raise ValueError("native barbell witness disagrees with independent fold")
            reports[expected] = row
    return {"positive_and_negative_controls": reports,
            "strict_disjoint_basis_change": replay(actual_disjoint),
            "strict_intersecting_basis_change": replay(actual_mixed)}


def catalogue_overlap(folder):
    archive_rows = (folder / "forward.tsv").read_bytes().splitlines()
    sources = json.loads((folder / "forward.sources.json").read_text())
    if len(archive_rows) != len(sources):
        raise ValueError("forward catalogue and provenance disagree")
    archive = dict(zip(archive_rows, sources))
    c22 = set((folder / "c22.tsv").read_bytes().splitlines())
    inside = {row for row in archive if len(row) - 1 <= 22}
    return {"archive_pairs_with_cyclic_energy_at_most_22": len(inside),
            "previous_c22_members": len(inside & c22),
            "outside_previous_c22_with_cyclic_energy_at_most_22": len(inside - c22),
            "outside_previous_c22_short_pairs": [
                {"canonical_pair": row.decode().split("\t"), "source": archive[row]}
                for row in sorted(inside - c22)
            ],
            "archive_pairs_with_cyclic_energy_23_to_32": len(archive) - len(inside)}


def collect(folder, binary):
    def read(name):
        return json.loads((folder / name).read_text())

    dag = read("dag_summary.json")
    dag.pop("seconds", None)
    map_bytes = (folder / "map_results.jsonl").read_bytes()
    maps = [json.loads(line) for line in map_bytes.splitlines()]
    if dag["status"] != "COMPLETE" or len(maps) != dag["inconclusive_graphs"]:
        raise ValueError("primitive audit incomplete")
    map_states = sum(verify_absence(row) for row in maps)
    return {
        "ordinary_AC_goal_solved": False,
        "external_path_replay": read("archive.json"),
        "c22_overlap": catalogue_overlap(folder),
        "archive_all_tail_primitive_scan": {
            **dag,
            "closed_map_certificates_checked": len(maps),
            "closed_map_pair_states_checked": map_states,
            "closed_map_certificates_sha256": sha256(map_bytes).hexdigest(),
        },
        "exact_one_phase_join_controls": native_controls(binary),
        "new_archive_waypoints_vs_known_trivial_archive": read("all_tails.json"),
        "known_trivial_archive_vs_certified_AK3_cap22": read("c22_all_tails.json"),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment_folder", type=Path)
    parser.add_argument("match_binary", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(collect(args.experiment_folder, args.match_binary),
                                      indent=2) + "\n")
