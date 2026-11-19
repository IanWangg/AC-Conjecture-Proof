"""Assemble the independent cut receipts and the completed rank-two erasures."""
import argparse
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path)
    parser.add_argument("--include-one-padding", action="store_true")
    args = parser.parse_args()
    work = args.work
    native = [read(work / f"incidence-{k}.json") for k in range(1, 5)]
    independent = read(work / "incidence-independent.json")
    assert len(native) == len(independent)
    for first, second in zip(native, independent):
        assert first["padding"] == second["padding"]
        assert first["crossing_budget"] == second["left_radius"] + second["right_radius"]
        assert first["parity_matches_all_target_orders"] == second["parity_matches_all_target_orders"]
        assert first["all_cuts_at_least_three"] == second["all_cuts_at_least_three"] == 0
    cubic = read(work / "incidence-cubic.json")
    assert cubic["padding"] == 5
    assert cubic["crossing_budget"] == 9
    assert len(cubic["results"]) == 2
    assert all(r["parity_matches"] == 0 for r in cubic["results"])

    degrees = [(5, 4, 9), (6, 3, 11), (7, 2, 13)]
    if args.include_one_padding:
        degrees.append((8, 1, 15))
    erasures = []
    for degree, k, radius in degrees:
        result = read(work / f"d{degree}-k{k}-L{radius}.json")
        assert (result["degree"], result["spare_rows"], result["limit"]) == (degree, k, radius)
        assert sum(result["radii"]) == radius and not result["ordered"]
        erasures.append(result)
    result = {
        "tight_product_budget": native,
        "all_target_orders_audit": independent,
        "five_padding_cubic_audit": cubic,
        "degree_nine_bounded_padding_erasures": erasures,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
