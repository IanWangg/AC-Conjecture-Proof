"""Check the padded corridor controls and exact length-nineteen erasures."""

import argparse
import json
from pathlib import Path

from round06_stable_disproof_tiers import independent_replay


def load(path):
    return json.loads(path.read_text())


def verify_ledger(record):
    moves = record["moves"]
    assert record["path_within_budget"] and len(moves) <= sum(record["radii"])
    endpoint = independent_replay(record["degree"], record["spare_rows"], moves, erased=True)
    if record["ordered"]:
        assert endpoint == list(range(record["spare_rows"] + 2))
    return {"length": len(moves), "target_slots": endpoint, "independent_monomial_replay": True}


def equivalent_corridors(left, right):
    fields = ("degree", "spare_rows", "ordered", "radii", "path_within_budget", "tiers")
    assert {key: left[key] for key in fields} == {key: right[key] for key in fields}
    assert sorted(left["midpoint_hex"]) == sorted(right["midpoint_hex"])
    assert left.get("free_tier") == right.get("free_tier")
    assert sorted(left.get("midpoint_words", [])) == sorted(right.get("midpoint_words", []))


def summarize(directory):
    modes = ("padded-control6-L12", "first-padded-control6-L12", "padded-control6-L12-ordered",
             "padded-free-control6-L12", "first-padded-free-control6-L12",
             "padded-control7-L14", "first-padded-control7-L14", "screen-control6-L12")
    controls = {mode: load(directory / f"{mode}.json") for mode in modes}
    for mode in ("padded-control6-L12", "padded-free-control6-L12", "padded-control7-L14"):
        equivalent_corridors(controls[mode], controls[f"first-{mode}"])
    finite_positive = (
        "padded-control6-L12", "first-padded-control6-L12", "screen-control6-L12",
        "padded-control7-L14", "first-padded-control7-L14",
    )
    replays = {mode: verify_ledger(controls[mode]) for mode in finite_positive}
    assert not controls["padded-control6-L12-ordered"]["path_within_budget"]
    assert not controls["padded-free-control6-L12"]["path_within_budget"]
    assert controls["padded-free-control6-L12"]["free_tier"]["midpoints"] == 0

    signed = [json.loads(line) for line in (directory / "signed-k3.jsonl").read_text().splitlines()]
    assert [record["products"] for record in signed] == [6, 7, 8]
    assert all(record["padding"] == 3 and record["matching_state_pairs"] == 0 for record in signed)

    erasures = []
    for degree, padding, budget in ((8, 2, 15), (7, 3, 13), (7, 4, 11)):
        record = load(directory / f"d{degree}-k{padding}-L{budget}-native.json")
        assert (record["degree"], record["spare_rows"], record["limit"]) == (degree, padding, budget)
        assert record["distance"] is None and not record["ordered"] and record["final_boundary_candidates"] > 0
        erasures.append(record)
    one_spare = load(directory / "d9-k1-L16-corridor.json")
    assert (one_spare["degree"], one_spare["spare_rows"], one_spare["radii"]) == (9, 1, [8, 8])
    assert not one_spare["ordered"] and not one_spare["path_within_budget"]
    assert [tier["midpoints"] for tier in one_spare["tiers"]] == [232448, 4060216, 250833, 3930, 132, 2, 0]
    return {
        "stable_budget": 19,
        "rank_two_magnus_erasures": erasures,
        "one_spare_degree_nine_middle_budget_sixteen": one_spare,
        "signed_integral_abelianization": signed,
        "corridor_controls": controls,
        "independent_replays": replays,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(summarize(args.directory), indent=2))


if __name__ == "__main__":
    main()
