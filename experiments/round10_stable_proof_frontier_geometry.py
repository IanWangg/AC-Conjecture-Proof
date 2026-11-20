"""Test geometric quotients of the charted cap-23 frontier."""

import argparse
import json
from pathlib import Path

from round05_stable_proof_projections import each_available_chart, geometry_screen
from round07_stable_proof_automorphic_charts import signed_key


def scan(catalogue, basis_index_tsv):
    projections = {}
    with catalogue.open() as states:
        for line in states:
            rows = tuple(line.split())
            assert len(rows) == 3
            for pair, chart in each_available_chart(rows):
                projections.setdefault(signed_key(pair), {"rows": rows, "projected_pair": pair, **chart})
    return {"signed_projections": len(projections), **geometry_screen(projections, basis_index_tsv)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalogue", type=Path)
    parser.add_argument("--basis-index-tsv", type=Path)
    args = parser.parse_args()
    print(json.dumps(scan(args.catalogue, args.basis_index_tsv), indent=2))
