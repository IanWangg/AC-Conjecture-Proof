"""Independently verify the compact characteristic-9377 exclusion certificate."""

import argparse
from collections import defaultdict
from itertools import product
import json
from math import comb, isqrt
from pathlib import Path

from round15_ak3_torus_atlas import apply

P = 9377
NAMES = range(11)
UPPER = ((10, 1), (5, 1), (1, 1), (0, -1), (4, -1), (7, -1))
ROW = ((1, -1), (5, -1), (4, 1), (1, 1))
RELATOR = ((1, -1), (5, -1), (10, -1), (11, 1), (7, 1), (4, 1), (0, 1))


def index_letters(word):
    height, result = 0, []
    for letter in word:
        if letter in "yY":
            height += 1 if letter == "y" else -1
        else:
            sign = 1 if letter == "x" else -1
            if result and result[-1] == (height, -sign):
                result.pop()
            else:
                result.append((height, sign))
    return tuple(result), height


def quotient(values):
    return {k: v % P for k, v in values.items() if v % P}


def mult(first, second, degree):
    result = defaultdict(int)
    for left, x in first.items():
        for right, y in second.items():
            if len(left) + len(right) <= degree:
                result[left + right] += x * y
    return quotient(result)


def program(word, degree):
    accum = {(): 1}
    for index, sign in word:
        factor = {(): 1, (index,): sign}
        if sign < 0:
            factor.update({(index,) * k: (-1) ** k for k in range(2, degree + 1)})
        accum = mult(accum, factor, degree)
    return accum


def image(word, images, degree):
    current = {(): 1}
    for letter in word:
        current = mult(current, images[letter], degree)
    return current


def direct_rank(images, degree):
    pivots = {}
    for word in product(NAMES, repeat=degree):
        raw = {k: -c for k, c in image(word, images, degree).items()}
        raw[word] = raw.get(word, 0) + 1
        vector = quotient(raw)
        while vector:
            root = max(vector)
            if root not in pivots:
                inverse = pow(vector[root], -1, P)
                pivots[root] = {k: v * inverse % P for k, v in vector.items()}
                break
            scale = vector[root]
            for key, c in pivots[root].items():
                vector[key] = (vector.get(key, 0) - scale*c) % P
                if not vector[key]:
                    del vector[key]
    return len(pivots)


def verify(path):
    assert all(P % n for n in range(2, isqrt(P) + 1))
    found = next(row for row in json.loads(path.read_bytes()) if row["prime"] == P)
    control = found["single_coordinate_witness"]
    marking = "yXyyy", "Xyyy"
    original = "xYxYxYY", "xY"
    assert tuple(apply(w, marking) for w in original) == tuple("xy")
    assert tuple(apply(w, original) for w in marking) == tuple("xy")
    assert index_letters(apply("xxxYxxYXYXY", marking)) == (RELATOR, 0)
    assert index_letters(apply("xxyXYY", marking)) == (ROW, 1)
    relator = tuple(term for step in RELATOR for term in (UPPER if step == (11, 1) else (step,)))
    assert program(relator, 3) == {(): 1}

    changed = program(UPPER, 3)
    del changed[()]
    images = [{(j + 1,): 1} for j in range(10)] + [changed]
    linear = [{k: v for k, v in poly.items() if len(k) == 1} for poly in images]
    ranks = [direct_rank(linear, d) for d in (1, 2)]
    assert ranks == [11, 121]
    compressed = {tuple(word): value for word, value in control["degree_three_dual"]}

    def dual(word):
        minimum = min(word)
        return compressed.get(tuple(i - minimum for i in word), 0)

    for triple in product(NAMES, repeat=3):
        assert (dual(triple) - sum(dual(key) * v for key, v in image(triple, linear, 3).items())) % P == 0

    receiver = program(ROW, 3)
    sample_values = []
    for k, entries in enumerate(control["lower_conjugator_samples"]):
        g = {tuple(word): value for word, value in entries}
        assert g[()] == 1 and all(len(word) <= 2 for word in g)
        shifted = defaultdict(int)
        for word, coefficient in g.items():
            for label, v in image(word, images, 3).items():
                shifted[label] += coefficient * v
        target = {((0,) * j): comb(k, j) for j in range(min(k, 3) + 1)}
        difference = defaultdict(int, mult(target, quotient(shifted), 3))
        for word, coefficient in mult(g, receiver, 3).items():
            difference[word] -= coefficient
        difference = quotient(difference)
        assert all(len(word) == 3 for word in difference)
        sample_values.append(sum(dual(word) * value for word, value in difference.items()) % P)
    (polynomial,) = [coefficients for coordinate, coefficients in found["residual_newton_coefficients"]
                     if coordinate == control["coordinate"]]
    assert sample_values == [
        sum(coefficient * comb(k, j) for j, coefficient in enumerate(polynomial)) % P
        for k in range(4)
    ]
    assert all(sum(c * comb(k, j) for j, c in enumerate(polynomial)) % P for k in range(P))
    return {
        "prime": P, "full_lower_ranks": ranks, "annihilated_cubic_columns": 11**3,
        "sample_values": sample_values, "residues_checked": P, "surviving_residues": [],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    print(json.dumps(verify(parser.parse_args().receipt), indent=2))
