"""Test cyclic quotients of two-row blocks after the cap-24 expansion."""

import argparse
from functools import cache
from itertools import combinations
import json
from math import gcd
from pathlib import Path

from round03_frozen_donors import evaluate, perm_inv, perm_mul
from round03_stable_proof_pivot import canonical, det, exponent
from round04_stable_proof_blocks import cyclic_cover_obstruction
from round05_stable_proof_chartless import chart_count, primitive
from round06_stable_proof_cap23_blocks import expose
from stallings_search import inverse


HNN_MARKINGS = {
    ("XXXYYxy", "XYxzXZy"): ((1, 3, 2), (2, 3, 1)),
    ("XXXYZXzxY", "XXyxYY"): ((1, 3, 4, 2), (2, 3, 1, 4)),
    ("XXXYxyy", "XYxzXZy"): ((1, 3, 2), (2, 3, 1)),
    ("XYYYZXzXy", "XYxYXy"): ((1, 3, 2), (2, 1, 3)),
}


@cache
def has_primitive(rows):
    return any(primitive(word) for word in rows)


def hnn_witness(pair):
    marks = HNN_MARKINGS[pair]
    base, extension = sorted(pair, key=lambda word: word.lower().count("z"))
    assert "z" not in base.lower() and extension.count("z") == extension.count("Z") == 1
    start = extension.index("z")
    rotation = extension[start:] + extension[:start]
    conjugated_word, other_tail = rotation[1:].split("Z")
    associated_words = conjugated_word, inverse(other_tail)
    x, y, _ = exponent(base)
    assert gcd(x, y) == 1
    weights = y, -x
    heights = [sum(a * b for a, b in zip(weights, exponent(word))) for word in associated_words]
    assert sum(height == 0 for height in heights) == 1
    identity = tuple(range(1, len(marks[0]) + 1))
    assert evaluate(base, marks, identity, perm_mul, perm_inv) == identity
    zero_word = associated_words[heights.index(0)]
    image = evaluate(zero_word, marks, identity, perm_mul, perm_inv)
    assert image != identity
    return dict(base_relator=base, rotated_extension_relator=rotation, associated_words=associated_words,
                base_abelian_weights=weights, associated_heights=heights, zero_height_word=zero_word,
                generator_images=dict(zip("xy", marks)), zero_height_image=image)


def scan(input_file):
    blocks = {}
    rows_screened = 0
    for line in input_file.open():
        child = tuple(line.split()[:3])
        if chart_count(child) or has_primitive(child):
            continue
        assert abs(det(child)) == 1
        rows_screened += 1
        for pair in combinations(child, 2):
            blocks.setdefault(pair, child)
    survivors = []
    for pair, source in sorted(blocks.items()):
        obstructed, weights, omit, determinant = cyclic_cover_obstruction(pair)
        if not obstructed:
            survivors.append(dict(pair=pair, source=source, weights=weights, omitted_column=omit,
                                  determinant=determinant, exposure=expose(pair)))
    pivot_exclusions = 0
    hnn_exclusions = 0
    for item in survivors:
        if item["exposure"] is not None:
            assert not item["exposure"]["projected_row_primitive"]
            pivot_exclusions += 1
            continue
        item["hnn_witness"] = hnn_witness(item["pair"])
        hnn_exclusions += 1
    return dict(three_row_states_without_primitive=rows_screened, distinct_two_row_blocks=len(blocks),
                fox_exclusions=len(blocks)-len(survivors), blocks_surviving_fox=survivors,
                pivot_exclusions=pivot_exclusions, hnn_exclusions=hnn_exclusions,
                total_noncyclic_blocks=len(blocks))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("neighbor_states", type=Path)
    args = parser.parse_args()
    print(json.dumps(scan(args.neighbor_states), indent=2))
