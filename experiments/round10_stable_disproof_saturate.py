"""Saturate the saved degree-nine padded corridor using unpadded ledgers."""

import json
from functools import cache
from pathlib import Path

from round01_magnus_distance import evaluate, generator, inverse, multiply, neighbors
from round01_stable_disproof_search import AK3
from round06_stable_disproof_tiers import independent_replay

ROOT = Path(__file__).resolve().parents[1]
DEGREE = 9
RADIUS = 17
LETTERS = "xXyY"
START = tuple(evaluate(word, DEGREE) for word in AK3)
GOAL = tuple(generator(i) for i in range(2))


def read_result(name):
    return json.loads((ROOT / "results" / name).read_text())


@cache
def polynomial_key(poly):
    return tuple(sorted(poly))


def orbit(rows):
    return tuple(sorted(rows, key=polynomial_key))


def step(rows, move):
    op, i = move["op"], move.get("i")
    if op == "swap":
        return rows[::-1]
    if op == "invert":
        image = inverse(rows[i], DEGREE)
    elif op == "multiply":
        donor = rows[move["j"]]
        if move["sign"] == -1:
            donor = inverse(donor, DEGREE)
        image = multiply(rows[i], donor, DEGREE)
    elif op == "conjugate":
        index = LETTERS.index(move["g"])
        a = generator(index // 2)
        if index % 2:
            a = inverse(a, DEGREE)
        image = multiply(multiply(a, rows[i], DEGREE), inverse(a, DEGREE), DEGREE)
    else:
        raise ValueError(op)
    return rows[:i] + (image,) + rows[i + 1 :]


@cache
def adjacent(rows):
    return {orbit(candidate) for candidate in neighbors(rows, DEGREE, False, len(rows))}


def initial_layers():
    layers = [{orbit(START)}, *(set() for _ in range(RADIUS))]
    for filename in ("round07_magnus_d9_witness.json", "round07_magnus_d9_ordered_witness.json"):
        witness = read_result(filename)
        assert witness["degree"] == DEGREE and len(witness["moves"]) == RADIUS
        rows = START
        for tick, move in enumerate(witness["moves"], 1):
            rows = step(rows, move)
            layers[tick].add(orbit(rows))
        assert orbit(rows) == orbit(GOAL)
    return layers


def widths(layers):
    return list(map(len, layers))


def short_bridges(layers, length):
    """Insert all penultimate states of fixed-length bridges between witnessed layers."""
    while True:
        before = widths(layers)
        for i in range(len(layers) - length):
            forward = layers[i]
            for _ in range(length - 1):
                forward = set().union(*map(adjacent, forward))
            backward = set().union(*map(adjacent, layers[i + length]))
            layers[i + length - 1].update(forward.intersection(backward))
        if widths(layers) == before:
            return


def saturation():
    layers = initial_layers()
    profiles = [widths(layers)]
    for length in (2, 3):
        short_bridges(layers, length)
        profiles.append(widths(layers))
    return layers, profiles


def corridor_data():
    receipts = read_result("round10_stable_disproof_corridors.json")
    ordinary = receipts["ordinary_degree10_budget19"]
    padded = receipts["one_spare_free_middle_budget17"]
    assert (ordinary["degree"], ordinary["spare_rows"], ordinary["ordered"], ordinary["radii"]) == (10, 0, False, [9, 10])
    assert not ordinary["path_within_budget"] and ordinary["tiers"][-1]["midpoints"] == 0
    assert (padded["degree"], padded["spare_rows"], padded["ordered"], padded["radii"]) == (9, 1, False, [8, 9])
    assert not padded["path_within_budget"] and padded["free_tier"]["midpoints"] == 0
    layer = padded["tiers"][-1]
    assert layer["degree"] == DEGREE
    left, right = layer["widths"]
    assert len(left) == 9 and len(right) == 10 and left[-1] == right[-1] == layer["midpoints"]
    return left + right[-2::-1]


def main():
    expected = corridor_data()
    _, profiles = saturation()
    assert profiles[-1] == expected
    native = read_result("round10_stable_disproof_corridors.json")["independent_unpadded_degree_nine_budget17"]
    assert (native["degree"], native["spare_rows"], native["ordered"], native["radii"]) == (DEGREE, 0, False, [8, 9])
    assert native["path_within_budget"] and len(native["moves"]) == RADIUS
    left, right = native["tiers"][-1]["widths"]
    assert expected == left + right[-2::-1]
    end_order = independent_replay(DEGREE, 0, native["moves"], erased=True)
    print(json.dumps({
        "degree": DEGREE,
        "middle_budget": RADIUS,
        "full_padded_corridor_widths": expected,
        "unpadded_widths_seed_ledgers": profiles[0],
        "unpadded_widths_after_two_step_bridges": profiles[1],
        "unpadded_widths_after_three_step_bridges": profiles[2],
        "positive_widths_verified_by_monomial_sets": True,
        "every_padded_corridor_vertex_contains_the_identity": True,
        "native_unpadded_width_comparison": True,
        "native_unpadded_witness_rows_after_independent_replay": end_order,
    }, indent=2))


if __name__ == "__main__":
    main()
