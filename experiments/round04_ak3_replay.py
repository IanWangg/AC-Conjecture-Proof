"""Build Round 04 fixtures and consolidate its independently replayed receipts."""

import argparse
from hashlib import sha256
import json
from pathlib import Path

from elementary_verify import replay
from round01_ak3_archive import pair_key
from round04_ak3_outward import barbell_control

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text())


def prepare(work):
    work.mkdir(parents=True, exist_ok=True)
    route = read(ROOT / "results/round03_cyclic26_energy15_path.json")["route"]
    anchors = (ROOT / "results/round03_cyclic26_energy15.tsv").read_text().splitlines()
    rows = sorted(set(anchors) | {"\t".join(p) for p in route})
    assert len(rows) == 38
    (work / "forward.tsv").write_text("".join(row + "\n" for row in rows))
    cases = {
        "barbell": ("xyxyXY", "y"), "rose": ("xxy", "xy"), "reverse-control": ("x", "y"),
        "theta-forward": ("XXY", "XXYXyxxY"), "theta-reverse": ("XXXY", "XXY"),
    }
    for name, pair in cases.items():
        (work / f"{name}.tsv").write_text("\t".join(pair_key(pair)) + "\n")


def combine(work, cap26, reverse32, reverse56):
    check = {}
    for shape in ("barbell", "rose", "theta"):
        result = read(work / f"{shape}.json")
        assert result["status"] == "JOIN" and result["topology"] == shape
        check[shape] = result
    check["theta_round01_reference"] = read(work / "theta-reference.json")["status"]
    assert check["theta_round01_reference"] == "BOTH_INTERSECT"
    check["barbell_strict_certificate"] = replay(barbell_control())

    outward = read(work / "outward/outward.json")
    outward["known_trivial_basis_comparison"] = read(work / "outward/basis-matches.json")
    outward["literal_two_copy_screen"] = read(work / "outward/two-copy.json")
    assert outward["known_trivial_basis_comparison"]["status"] == "NO_SUBGROUP_JOIN"
    assert outward["literal_two_copy_screen"]["positive"] == outward["literal_two_copy_screen"]["incomplete"] == 0
    disjoint = {}
    for filename in ("disjoint-counts.json", "disjoint8-counts.json"):
        record = read(work / filename)
        assert (record["left"], record["right"]) == ("XXYxYxy", "XYXyxYYY")
        for size, row in record["lengths"].items():
            assert size not in disjoint
            vertices = 14 + int(size)
            assert row["joins"] == row["distinct_cores"] * vertices * (vertices - 1) // 2
            assert row["positive"] == row["incomplete"] == 0
            assert row["dag_absent"] + row["exact_absent"] == row["joins"] + row["distinct_cores"]
            disjoint[size] = row
    assert set(disjoint) == {str(n) for n in range(1, 9)}

    shapes32 = read(work / "basis-matches.json")
    shapes56 = read(work / "basis-matches56.json")
    assert shapes32["status"] == shapes56["status"] == "NO_SUBGROUP_JOIN"
    assert shapes32["forward_pairs"] == shapes56["forward_pairs"] == 10_340_996

    fiber = read(work / "reverse-fiber.json")
    bridges = read(work / "reverse-bridges.json")
    edges = fiber["sources"]
    bars = bridges["sources"]
    assert fiber["target_rows"] == bridges["targets"] == 9257
    assert len(edges) == len(bars) == 38
    assert all(f["source"] == b["source"] for f, b in zip(edges, bars))
    assert all(f["source_has_primitive_absence"] and not f["inconclusive_lattice"]
               and f["rank_two_products"] == f["full_ambient_targets"]
               and not f["two_valid_cyclic_components"] for f in edges)
    assert all(not b["nonmalnormal"] and not b["rank_at_least_two"]
               and not b["intrinsic_lobe_exceptions"] for b in bars)
    return {
        "input_sha256": {name: sha256(path.read_bytes()).hexdigest() for name, path in (
            ("cap26", cap26), ("reverse32", reverse32), ("reverse56", reverse56),
            ("fixed_forward_route_and_escapes", work / "forward.tsv"),
        )},
        "intrinsic_basis_index": {"reverse32": shapes32, "reverse56": shapes56, "controls": check},
        "fixed_forward_core_comparison": {
            "forward_cores": len(edges), "reverse_pairs": fiber["target_rows"],
            "reverse_rotated_core_comparisons": sum(f["compared"] for f in edges),
            "full_ambient_rank_two_cases": sum(f["full_ambient_targets"] for f in edges),
            "multilift_bridge_placements": sum(b["map_placements"] for b in bars),
            "join_found": False,
        },
        "energy15_first_disjoint_bridge_scan": disjoint,
        "energy15_first_disjoint_guarded_language": read(work / "language.json"),
        "outward_search": outward,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path)
    parser.add_argument("--measure", nargs=3, type=Path, metavar=("CAP26", "REVERSE32", "REVERSE56"))
    args = parser.parse_args()
    if args.measure:
        print(json.dumps(combine(args.work, *args.measure), indent=2))
    else:
        prepare(args.work)


if __name__ == "__main__":
    main()
