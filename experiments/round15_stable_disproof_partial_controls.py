"""Differentially check top-coordinate refinements against published and full controls."""

import argparse
import json
from pathlib import Path
import subprocess

from round06_stable_disproof_tiers import independent_replay


def compare(executable):
    root = Path(__file__).resolve().parents[1]
    known = json.loads((root / "results/round08_magnus_native_corridor_controls.json").read_text())
    census = json.loads((root / "results/round15_stable_disproof_d6_kernel.json").read_text())
    coordinates = [row["degree_six_coordinate"] for row in census["central_basis"]]
    masks = [sum(1 << coordinate for coordinate in coordinates[:length]) for length in range(1, len(coordinates))]

    def run(degree, radii, *options):
        args = [executable, str(degree), *map(str, radii), "--ledger", *options]
        receipt = subprocess.run(args, text=True, capture_output=True, check=True)
        result = json.loads(receipt.stdout)
        if result["path_within_budget"]:
            order = independent_replay(degree, 0, result["moves"], erased=True)
            assert sorted(order) == [0, 1]
            if result["ordered"]:
                assert order == [0, 1]
            result["independent_replay_order"] = order
        return result

    controls = []
    for degree, radii, ordered in ((6, (5, 6), False), (6, (6, 6), False), (6, (6, 6), True), (7, (7, 7), False)):
        options = ("--first-arrivals", "--ordered") if ordered else ("--first-arrivals",)
        full = run(degree, radii, *options)
        partial = run(degree, radii, *options, "--partial-degree-six")
        assert full["path_within_budget"] == partial["path_within_budget"]
        assert full["tiers"] == [tier for tier in partial["tiers"] if "top_mask" not in tier]
        assert masks == [tier["top_mask"] for tier in partial["tiers"] if "top_mask" in tier]
        if degree == 6 and not ordered:
            previous = next(row for row in known if row["radii"] == list(radii) and not row["ordered"])
            assert previous["tiers"] == full["tiers"]
        controls.append({"full": full, "partial": partial})

    layered = run(6, (6, 6), "--partial-degree-six")
    assert layered["tiers"] == controls[1]["partial"]["tiers"]
    return {"controls": controls, "layered_degree_six_positive": layered}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corridor", help="path to the rebuilt native corridor executable")
    args = parser.parse_args()
    print(json.dumps(compare(args.corridor), indent=2, sort_keys=True))
