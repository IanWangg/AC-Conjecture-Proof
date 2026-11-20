"""Independently count four-product cases and replay the spherical controls."""

import argparse
from functools import lru_cache
from io import BytesIO
from itertools import product
import json
from pathlib import Path

from elementary_verify import inverse, replay
from euclidean_primitive_audit import primitive_cyclic_word
from free_waypoint_search import cyclic
from round06_stable_proof_strict_escape import StrictPath
from round08_ak3_acm_search import cyclic_peak
from round19_ak3_three_products_replay import spherical_factors


FIXTURES = {
    "AAB": (("XyxYxYY", "yXYxy"), (1, 1, -1, 1), ("y", "Xy", "Yx", "")),
    "ABA": (("YxyxY", "yXYXyx"), (1, 1, -1, 1), ("", "XY", "xy", "xY")),
    "ABB": (("yxYxy", "yXyxYx"), (-1, -1, -1, 1), ("Y", "x", "yX", "x")),
}


def census(word):
    return tuple(word.count(letter) for letter in "xXyY")


def exponents(word):
    x, X, y, Y = census(word)
    return x-X, y-Y


def receivers(mode, first):
    return tuple(first if letter == "A" else 1-first for letter in mode + mode[-1])


def signed_expansion(mode, first, signs):
    rows = ["x", "y"]
    indices = receivers(mode, first)
    for index, sign in zip(indices, signs):
        donor = rows[1-index]
        rows[index] += donor if sign > 0 else inverse(donor)
    return rows[indices[-1]]


@lru_cache(None)
def expected_cases(mode):
    return [{census(signed_expansion(mode, first, bounds))
             for bounds in product((-1, 1), repeat=4)} for first in (0, 1)]


def verify_receipt(receipt, source):
    mode = receipt["mode"]
    assert tuple(tuple(row["source"]) for row in receipt["rows"]) == tuple(source)
    counts = {"rows": len(source), "sign_histories": 0, "equations": 0, "witnesses": 0}
    for row in receipt["rows"]:
        assert row["sign_histories"] == 32
        expected = expected_cases(mode)
        assert row["equations"] == sum(map(len, expected))
        seen = set()
        for hit in row["hits"]:
            first, signs = hit["first_receiver"], hit["signs"]
            counts_key = census(signed_expansion(mode, first, signs))
            assert tuple(hit["multiplicities"]) == counts_key and counts_key in expected[first]
            assert (first, counts_key) not in seen
            seen.add((first, counts_key))
            a, b = row["source"]
            alphabet = {"x": a, "X": inverse(a), "y": b, "Y": inverse(b)}
            boundary = hit["boundary"]
            assert boundary[:-1] == [alphabet[letter] for letter in signed_expansion(mode, first, signs)]
            primitive = inverse(boundary[-1])
            assert primitive_cyclic_word(primitive) and tuple(hit["slope"]) == exponents(primitive)
            spherical_factors(boundary, hit["equation"])
        counts["sign_histories"] += row["sign_histories"]
        counts["equations"] += row["equations"]
        counts["witnesses"] += len(seen)
    return counts


def strict_control(mode):
    source, signs, conjugators = FIXTURES[mode]
    assert all(not primitive_cyclic_word(cyclic(word)) for word in source)
    sink = BytesIO()
    path = StrictPath(source, sink)
    for index, sign, transport in zip(receivers(mode, 0), signs, conjugators):
        path.factor(index, 1-index, sign, transport)
    assert path.rows == ["x", "y"] and path.counts["multiply"] == 4
    proof = {"format": "ordinary-ac-elementary-v1", "start": list(source), "target": path.rows,
             "moves": [json.loads(line) for line in sink.getvalue().splitlines()[1:]]}
    return proof, dict(replay(proof), cyclic_peak=cyclic_peak(proof), products=4)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-controls", type=Path)
    parser.add_argument("--check-controls", type=Path)
    parser.add_argument("--receipt", type=Path, action="append", default=[])
    parser.add_argument("--source", type=Path)
    args = parser.parse_args()
    if args.write_controls:
        args.write_controls.mkdir(parents=True, exist_ok=True)
        for mode, (source, _, _) in FIXTURES.items():
            (args.write_controls / f"{mode}.tsv").write_text("\t".join(source) + "\n")
    controls, production = {}, {}
    if args.check_controls:
        for mode, (source, _, _) in FIXTURES.items():
            receipt = json.loads((args.check_controls / f"{mode}-control.json").read_bytes())
            counts = verify_receipt(receipt, (source,))
            assert receipt["mode"] == mode and counts["witnesses"] > 0
            proof, checked = strict_control(mode)
            controls[mode] = {"native_spheres": counts, "strict_control": proof, "replay": checked}
    if args.receipt:
        with args.source.open() as reader:
            source = [tuple(row.split()) for row in reader]
        for path in args.receipt:
            receipt = json.loads(path.read_bytes())
            production[receipt["mode"]] = verify_receipt(receipt, source)
    if controls or production:
        report = {"controls": controls, "production": production} if controls and production else controls or production
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
