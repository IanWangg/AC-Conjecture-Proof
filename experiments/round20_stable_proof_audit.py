"""Verify the donor-free cap-37 graph with literal stack-reduced moves."""

import argparse
import hashlib
import json
from pathlib import Path

from round03_stable_proof_pivot import neighbors
from round09_stable_proof_lift_excursion import signed_rows
from round12_stable_proof_corridor import native_nodes, pivot_count, rank_three_key


def audit(roots, catalogue, earlier):
    short = {point[0] for point in signed_rows(("xxyXYY",) * 3)}
    seeds = {tuple(line.split()) for line in roots.read_text().splitlines()}
    assert len(seeds) == 528
    old = {rows for _, pivots, rows in native_nodes(earlier)
           if not pivots and set(rows).isdisjoint(short)}
    assert seeds == old

    listed = {rows for _, pivots, rows in native_nodes(catalogue) if not pivots}
    assert len(listed) == 1728
    reached = set(seeds)
    pending = sorted(seeds)
    candidates = 0
    for source in pending:
        assert set(source).isdisjoint(short) and not pivot_count(source)
        energy = sum(map(len, source))
        assert energy + min(map(len, source)) + 2 > 37
        assert max(37 - energy + len(word) for word in source) <= 21
        nearby, terms = neighbors(source, 37)
        candidates += terms
        for chart in nearby:
            if not set(chart).isdisjoint(short):
                continue
            key = rank_three_key(chart)
            if key not in reached:
                reached.add(key)
                pending.append(key)
    assert reached == listed
    canonical = "".join("\t".join(row) + "\n" for row in sorted(reached)).encode()
    return {"roots":len(seeds), "closed_states":len(reached), "stack_candidates":candidates,
            "primitive_rows":0, "catalogue_sha256":hashlib.sha256(canonical).hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", type=Path)
    parser.add_argument("catalogue_prefix", type=Path)
    parser.add_argument("earlier_prefix", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.roots, args.catalogue_prefix, args.earlier_prefix), indent=2))
