"""Screen two-row blocks in the chart-free part of a partial cap-23 catalogue."""

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from euclidean_primitive_audit import primitive_cyclic_word
from round03_stable_proof_pivot import canonical, det, rotations, tails
from round04_chart_screen import chart_projections
from round04_stable_proof_blocks import cyclic_cover_obstruction
from round05_stable_proof_chartless import chart_count, primitive
from round05_stable_proof_projections import geometry_screen, rank_two_orbit
from round06_stable_proof_cap23_charts import compact_row


def expose(pair):
    for recipient, donor in (pair, pair[::-1]):
        for a, b, (bridge, opposite) in product(rotations(recipient), rotations(donor), tails(1)):
            new = canonical(a + bridge + b + opposite)
            for eliminated, pivot, (projection,) in chart_projections((new, donor)):
                if pivot == new:
                    return dict(recipient=a, donor=b, bridge=bridge, new_pivot=pivot,
                                eliminated=eliminated, projected_row=projection,
                                projected_row_primitive=bool(primitive_cyclic_word(projection)))
    return None


def run(path, compact_cap29):
    input_hash = sha256()
    blocks = {}
    total = chartless = chartless_nonprimitive = 0
    with path.open("rb") as stream:
        for raw in stream:
            input_hash.update(raw)
            total += 1
            rows = tuple(raw.decode("ascii").split())
            if chart_count(rows):
                continue
            chartless += 1
            if any(primitive(word) for word in rows):
                continue
            assert abs(det(rows)) == 1
            chartless_nonprimitive += 1
            for pair in combinations(rows, 2):
                blocks.setdefault(pair, rows)
    remaining = []
    for pair, source in sorted(blocks.items()):
        obstructed, weights, omit, determinant = cyclic_cover_obstruction(pair)
        if not obstructed:
            remaining.append(dict(pair=pair, source=source, weights=weights, omitted_column=omit,
                                  determinant=determinant, exposure=expose(pair)))
    two_letter = {}
    for row in remaining:
        if row["exposure"] is None and all("z" not in word.lower() for word in row["pair"]):
            pair = min(rank_two_orbit(row["pair"]))
            two_letter.setdefault(pair, {"source_block": row["pair"]})
    expected = {compact_row(pair) for pair in two_letter}
    with compact_cap29.open("rb") as catalogue:
        matched = {line for line in catalogue if line in expected}
    return dict(input_sha256=input_hash.hexdigest(), input_states=total, chartless_states=chartless,
                nonprimitive_row_states=chartless_nonprimitive, unordered_two_row_blocks=len(blocks),
                cyclic_cover_obstructions=len(blocks) - len(remaining),
                remaining_blocks=remaining, two_letter_signed_orbits=len(two_letter),
                two_letter_orbits_in_cap29=len(matched), two_letter_geometry=geometry_screen(two_letter, None))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("partial_states", type=Path)
    parser.add_argument("compact_cap29", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.partial_states, args.compact_cap29), indent=2))
