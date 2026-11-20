"""Compare all energy-23 frontier chart projections with marked ordinary archives."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import zip_longest
import json
from pathlib import Path

from round05_stable_proof_projections import each_available_chart
from round06_stable_proof_cap23_charts import compact_row
from round07_stable_proof_automorphic_charts import signed_key


def scan(triples, parents, cap30, trivial):
    with trivial.open() as source:
        reverse = {signed_key(tuple(line.split())) for line in source}
    counts = Counter()
    projected = {}
    with triples.open() as states, parents.open() as predecessors:
        for raw, previous in zip_longest(states, predecessors):
            assert raw is not None and previous is not None
            rows, parent = tuple(raw.split()), tuple(previous.split())
            assert len(rows) == len(parent) == 3
            counts["states"] += 1
            for pair, chart in each_available_chart(rows):
                counts[chart["chart"] + "_charts"] += 1
                projected.setdefault(signed_key(pair), dict(rows=rows, parent_orbit_representative=parent,
                                                           pair=pair, **chart))
    target = {compact_row(pair): pair for pair in projected}
    assert len(target) == len(projected)
    with cap30.open("rb") as source:
        ordinary = {target[line] for line in source if line in target}
    missed = sorted(projected.keys() - ordinary, key=lambda pair: (sum(map(len, pair)), pair))
    trivial_hits = sorted(reverse & projected.keys())
    return {
        "states": counts["states"], "literal_charts": counts["literal_charts"],
        "intrinsic_charts": counts["intrinsic_charts"], "signed_projections": len(projected),
        "literal_c30": len(ordinary), "reverse_archive_signed_orbits": len(reverse),
        "reverse_archive_hits": [projected[pair] for pair in trivial_hits],
        "shortest_outside_c30": [projected[pair] for pair in missed[:10]],
        "triple_catalogue_sha256": sha256(triples.read_bytes()).hexdigest(),
        "parent_catalogue_sha256": sha256(parents.read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("triples", type=Path)
    parser.add_argument("parents", type=Path)
    parser.add_argument("compact_c30", type=Path)
    parser.add_argument("literal_trivial_archive", type=Path)
    args = parser.parse_args()
    print(json.dumps(scan(args.triples, args.parents, args.compact_c30, args.literal_trivial_archive), indent=2))
