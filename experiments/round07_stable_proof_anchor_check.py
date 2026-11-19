"""Check ordinary component anchors for every primitive row of the cap-23 endpoint."""

import argparse
import json
from pathlib import Path

from round01_geometric_archive import image
from round03_stable_proof_pivot import canonical
from round04_chart_screen import chart_projections
from round06_stable_proof_cap23_charts import compact_row

ROOT = Path(__file__).resolve().parents[1]


def check(cap27, cap29):
    previous = json.loads((ROOT / "results/round06_stable_proof_cap23_escape.json").read_text())
    stages = [previous["rank_three_replay"]["target"], *(stage["rows"] for stage in previous["whitehead_stages"])]
    anchors = []
    for slot, stage, selected in ((0, 4, "z"), (1, 0, "y"), (2, 1, "z")):
        rows = stages[stage]
        pivot = rows[slot]
        (pair,) = [candidate for letter, word, candidate in chart_projections(rows)
                   if word == pivot and letter == selected]
        anchors.append(dict(slot=slot, whitehead_stage=stage, pivot=pivot, deleted=selected, pair=pair))
    signatures = {compact_row(row["pair"]) for row in anchors}
    with cap29.open("rb") as input_file:
        found = {raw for raw in input_file if raw in signatures}
    assert found == signatures
    e23 = anchors[0]["pair"]
    raw = ("\t".join(e23) + "\n").encode("ascii")
    with cap27.open("rb") as input_file:
        assert any(line == raw for line in input_file)
    substituted = sorted(map(canonical, image(e23, "y", "yx")))
    assert substituted == previous["rank_two_projection"]
    assert sorted(map(canonical, image(substituted, "y", "yX"))) == list(e23)
    return dict(primitive_slot_anchors=anchors, all_in_cyclic_cap29=True, first_in_cap27=True,
                induced_rank_two_automorphism={"x": "x", "y": "yx"}, induced_image=substituted)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cap27_literal", type=Path)
    parser.add_argument("cap29_compact", type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.cap27_literal, args.cap29_compact), indent=2))
