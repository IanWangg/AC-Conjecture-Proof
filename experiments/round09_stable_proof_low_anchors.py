"""Compare projections of one exact low-energy layer with ordinary cap catalogues."""

import argparse
from collections import Counter
import json
from pathlib import Path

from round05_stable_proof_projections import each_available_chart
from round06_stable_proof_cap23_charts import compact_row
from round07_stable_proof_automorphic_charts import explore, signed_key


def scan(rank_three_rows, cap29, cap30, limit):
    projected = {}
    with rank_three_rows.open() as source:
        for line in source:
            rows = tuple(line.split()[:3])
            for pair, choice in each_available_chart(rows):
                projected.setdefault(signed_key(pair), dict(source=rows, projected=pair, **choice))
    states, classes, outside = explore(projected, limit)
    wanted = {compact_row(pair): root for pair, root in states.items()}
    anchors = {}
    for cap, name in ((29, cap29), (30, cap30)):
        with name.open("rb") as file:
            anchors[cap] = {wanted[line] for line in file if line in wanted}
    unanchored = [
        point for root, orbit in classes.items() if root not in anchors[30]
        for point, _ in orbit["inputs"]
    ]
    unanchored.sort(key=lambda pair: (sum(map(len, pair)), pair))
    return dict(
        signed_projections=len(projected), whitehead_sublevel=limit,
        minimum_energy_above_sublevel=len(outside), ambient_classes=len(classes), ambient_states=len(states),
        anchored_classes={cap: len(roots) for cap, roots in anchors.items()},
        anchored_sources={cap: sum(len(classes[key]["inputs"]) for key in roots)
                          for cap, roots in anchors.items()},
        unanchored_source_energies=dict(sorted(Counter(sum(map(len, p)) for p in unanchored).items())),
        shortest_unanchored_sources=[projected[pair] for pair in unanchored[:18]],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("low_energy_rank_three_rows", type=Path)
    parser.add_argument("compact_cap29", type=Path)
    parser.add_argument("compact_cap30", type=Path)
    parser.add_argument("--whitehead-sublevel", type=int, default=30)
    args = parser.parse_args()
    print(json.dumps(scan(args.low_energy_rank_three_rows, args.compact_cap29, args.compact_cap30,
                          args.whitehead_sublevel), indent=2))
