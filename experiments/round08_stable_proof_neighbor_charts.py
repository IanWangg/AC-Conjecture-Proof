"""Test actual cap-24 chart neighbors for primitive and geometric completions."""

import argparse
from collections import Counter
from functools import cache
from hashlib import sha256
import json
from pathlib import Path

from euclidean_primitive_audit import primitive_cyclic_word
from round05_stable_proof_chartless import minima
from round05_stable_proof_geometry import full_signed_key, planar_orders
from round05_stable_proof_projections import each_available_chart, geometry_screen
from round06_stable_proof_cap23_charts import compact_row
from round07_stable_proof_automorphic_charts import signed_key


primitive = cache(primitive_cyclic_word)


def primitive_scan(input_file):
    counts = Counter()
    hits = {}
    digest = sha256()
    with input_file.open("rb") as stream:
        for raw in stream:
            digest.update(raw)
            rows = tuple(raw.decode("ascii").split())
            child, parent = rows[:3], rows[3:]
            counts["neighbor_states"] += 1
            choices = 0
            for pair, chart in each_available_chart(child):
                choices += 1
                counts[chart["chart"] + "_charts"] += 1
                if any(primitive(word) for word in pair):
                    hits.setdefault(signed_key(pair), dict(rank_three_rows=child, predecessor=parent,
                                                            projected_pair=pair, **chart))
            counts["states_without_primitive_row"] += choices == 0
    return dict(input_sha256=digest.hexdigest(), counts=dict(counts),
                primitive_projections=[hits[key] for key in sorted(hits)])


def screen(input_file, cap29, basis_index_tsv=None):
    rank_two_sources = {}
    joint_rank_three = {}
    counts = Counter()
    digest = sha256()
    with input_file.open("rb") as stream:
        for raw in stream:
            digest.update(raw)
            rows = tuple(raw.decode("ascii").split())
            assert len(rows) == 6
            child, parent = rows[:3], rows[3:]
            counts["neighbor_states"] += 1
            charts = list(each_available_chart(child))
            if not charts:
                counts["states_without_primitive_row"] += 1
                jointly_minimized = full_signed_key(minima(child)[0])
                joint_rank_three.setdefault(jointly_minimized, (child, parent))
                continue
            for pair, chart in charts:
                counts[chart["chart"] + "_charts"] += 1
                key = signed_key(pair)
                rank_two_sources.setdefault(key, dict(rank_three_rows=child, predecessor=parent,
                                                      projected_pair=pair, **chart))

    rank_three_geometry = []
    systems = 0
    for minimum, (child, parent) in sorted(joint_rank_three.items()):
        attempt = planar_orders(minimum)
        systems += attempt["checked_rotations"]
        if attempt["planar"]:
            rank_three_geometry.append(dict(rows=child, predecessor=parent, minimum=minimum, **attempt))

    signatures = {compact_row(pair): pair for pair in rank_two_sources}
    assert len(signatures) == len(rank_two_sources)
    with cap29.open("rb") as source:
        covered = {signatures[line] for line in source if line in signatures}
    return dict(
        input_sha256=digest.hexdigest(), counts=dict(counts),
        distinct_projection_classes=len(rank_two_sources), projection_classes_in_cap29=len(covered),
        primitive_projections=[rank_two_sources[pair] for pair in sorted(rank_two_sources)
                               if any(primitive(word) for word in pair)],
        rank_two_geometry=geometry_screen(rank_two_sources, basis_index_tsv),
        jointly_minimized_rank_three_diagrams=len(joint_rank_three),
        rank_three_paired_rotation_systems=systems,
        spherical_rank_three_diagrams=rank_three_geometry,
        lowest_outside_cap29=[rank_two_sources[pair] for pair in
                             sorted(rank_two_sources.keys()-covered, key=lambda pair:(sum(map(len,pair)),pair))[:8]],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("neighbors_with_parent", type=Path)
    parser.add_argument("compact_cap29", type=Path)
    parser.add_argument("--basis-index-tsv", type=Path)
    parser.add_argument("--primitive-only", action="store_true")
    args = parser.parse_args()
    if args.primitive_only:
        result = primitive_scan(args.neighbors_with_parent)
    else:
        result = screen(args.neighbors_with_parent, args.compact_cap29, args.basis_index_tsv)
    print(json.dumps(result, indent=2))
