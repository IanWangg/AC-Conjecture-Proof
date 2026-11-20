"""Test both ambient and shared-pivot ordinary ancestry of cap-24 projections."""

import argparse
from collections import Counter
import json
from pathlib import Path

from round04_chart_screen import chart_projections
from round05_stable_proof_chartless import whitehead_image
from round05_stable_proof_projections import each_available_chart
from round06_stable_proof_cap23_charts import compact_row
from round07_stable_proof_automorphic_charts import explore, projected_sources, signed_key

ROOT = Path(__file__).resolve().parents[1]


def known_previous_and_child(old, new, cap29):
    nodes_old, classes_old, outside_old = explore(old, 29)
    nodes_new, classes_new, outside_new = explore(new, 29)
    old_signatures = {compact_row(pair): root for pair, root in nodes_old.items()}
    new_signatures = {compact_row(pair): root for pair, root in nodes_new.items()}
    roots_old, roots_new = set(), set()
    with cap29.open("rb") as stream:
        for row in stream:
            if row in old_signatures:
                roots_old.add(old_signatures[row])
            if row in new_signatures:
                roots_new.add(new_signatures[row])
    proven_old = {pair for root in roots_old for pair, _ in classes_old[root]["inputs"]}
    proven_new = {pair for root in roots_new for pair, _ in classes_new[root]["inputs"]}
    previous = json.loads((ROOT / "results/round07_stable_proof_ambient_projections.json").read_text())
    for orbit in previous["minimal_missing_orbits"]:
        proven_old.add(signed_key(orbit["restated_source"]["projected_pair"]))
    assert len(proven_old) == 310
    return proven_old, proven_new, {
        "old_known_ordinary_sources": len(proven_old), "new_sources_with_minimum_above_cap29": len(outside_new),
        "searched_new_ambient_orbits": len(classes_new), "searched_new_signed_states": len(nodes_new),
        "new_ambient_orbits_with_c29_anchor": len(roots_new),
        "new_projected_pairs_with_c29_ambient_anchor": len(proven_new),
    }


def old_pair_in_same_chart(parent, chosen):
    old_pivot = chosen.get("original_pivot", chosen["pivot"])
    if old_pivot not in parent:
        return None
    if "whitehead_descent" in chosen:
        for move in chosen["whitehead_descent"]:
            parent = whitehead_image(parent, move["multiplier"], move["cut"])
    (pair,) = [pair for e, p, pair in chart_projections(parent)
               if (e, p) == (chosen["eliminated"], chosen["pivot"])]
    return signed_key(pair)


def scan(old_partial, new_neighbors, cap29):
    old, _, _ = projected_sources(old_partial)
    child_pairs = {}
    occurrences = []
    with new_neighbors.open() as source:
        for line in source:
            full = tuple(line.split())
            child, parent = full[:3], full[3:]
            for pair, selection in each_available_chart(child):
                key = signed_key(pair)
                item = dict(rank_three_rows=child, predecessor=parent, projected_pair=pair, **selection)
                child_pairs.setdefault(key, item)
                occurrences.append((key, item))
    proven_old, proven_new, report = known_previous_and_child(old, child_pairs, cap29)
    same_pivot_proofs = {}
    for key, item in occurrences:
        prior_pair = old_pair_in_same_chart(item["predecessor"], item)
        if prior_pair in proven_old:
            same_pivot_proofs.setdefault(key, dict(prior_pair=prior_pair, **item))
    done = proven_new | same_pivot_proofs.keys()
    uncovered = sorted(child_pairs.keys() - done, key=lambda pair: (sum(map(len,pair)),pair))
    independently_anchored_outside = sorted(same_pivot_proofs.keys() - proven_new,
                                            key=lambda pair:(sum(map(len,pair)),pair))
    return {**report, "child_signed_projections": len(child_pairs), "known_by_retained_pivot": len(same_pivot_proofs),
            "known_by_retained_pivot_without_c29_ambient_anchor": len(independently_anchored_outside),
            "ordinary_ancestry_established_total": len(done),
            "uncovered_by_either_test": len(uncovered),
            "uncovered_energy_histogram": dict(sorted(Counter(sum(map(len,p)) for p in uncovered).items())),
            "shortest_retained_pivot_only_examples": [same_pivot_proofs[p] for p in independently_anchored_outside[:6]],
            "shortest_uncovered_examples": [child_pairs[p] for p in uncovered[:10]]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old_cap23", type=Path)
    parser.add_argument("new_cap24", type=Path)
    parser.add_argument("compact_cap29", type=Path)
    args = parser.parse_args()
    print(json.dumps(scan(args.old_cap23, args.new_cap24, args.compact_cap29), indent=2))
