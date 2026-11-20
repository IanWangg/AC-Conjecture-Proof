"""Verify indexed donor words and an explicit outer-compatible Dehn obstruction."""

import json
from itertools import product
from random import Random

from elementary_verify import inverse, replay, reduce
from round11_ac_proof_wirtinger_lifts import A, B, C, donor_product


def schreier(word):
    height = 0
    factors = []
    for letter in word:
        if letter in "xX":
            height += 1 if letter == "x" else -1
            continue
        sign = 1 if letter == "y" else -1
        if factors and factors[-1] == (height, -sign):
            factors.pop()
        else:
            factors.append((height, sign))
    return tuple(factors), height


def inverse_indexed(word):
    return tuple((index, -sign) for index, sign in reversed(word))


def cyclic_indexed(word):
    lo, hi = 0, len(word)
    while hi - lo > 1:
        index, sign = word[hi - 1]
        if word[lo] != (index, -sign):
            break
        lo, hi = lo + 1, hi - 1
    return word[lo:hi]


def rotations(word):
    return [word[i:] + word[:i] for i in range(len(word))]


def cancellation_and_extremes(word):
    assert cyclic_indexed(word) == word and len(word) > 6
    n = len(word)
    cyclic_reads = sorted(set(rotations(word) + rotations(inverse_indexed(word))))
    assert len(cyclic_reads) == 2 * n
    longest_piece = 0
    for first, second in zip(cyclic_reads, cyclic_reads[1:]):
        overlap = next(i for i, (a, b) in enumerate(zip(first, second)) if a != b)
        longest_piece = max(longest_piece, overlap)
    min_index, max_index = min(i for i, _ in word), max(i for i, _ in word)
    changes = []
    window = n // 2 + 1
    for segment in cyclic_reads:
        markers = [i for i, _ in segment[:window] if i in (min_index, max_index)]
        changes.append(sum(a != b for a, b in zip(markers, markers[1:])))
    return {
        "width": max_index - min_index,
        "length": n,
        "longest_piece": longest_piece,
        "half_window_length": window,
        "min_extreme_transitions": min(changes),
        "windows_checked": len(cyclic_reads),
    }


def indexed_to_ambient(index, sign):
    stable = "x" * index if index >= 0 else "X" * (-index)
    return stable + ("y" if sign == 1 else "Y") + inverse(stable)


def lift_example(seed):
    rng = Random(seed)
    factors = [
        tuple(
            reduce(
                "".join(
                    indexed_to_ambient(rng.randrange(-2, 1), rng.choice((-1, 1)))
                    for _ in range(20)
                )
            )
            for _ in range(2)
        )
        for _ in range(5)
    ]
    products = {B: [], C: []}
    middle = A
    for left, right in factors:
        u = reduce(left + B + inverse(left))
        v = reduce(right + C + inverse(right))
        middle = reduce(middle + u + v + inverse(u) + inverse(v))
        products[B].extend([(1, left), (-1, reduce(v + left))])
        products[C].extend([(1, reduce(u + right)), (-1, right)])
    indexed, height = schreier(middle)
    assert height == 0
    indexed = cyclic_indexed(indexed)
    stats = cancellation_and_extremes(indexed)
    if (
        6 * stats["longest_piece"] >= stats["length"]
        or stats["min_extreme_transitions"] < 3
    ):
        return None
    replays = {}
    for donor, sequence in products.items():
        certificate = {
            "format": "ordinary-ac-elementary-v1",
            "start": [A, donor],
            "target": [middle, donor],
            "moves": [
                move for sign, word in sequence for move in donor_product(sign, word)
            ],
        }
        replays[donor] = replay(certificate)
    return {
        "seed": seed,
        "conjugating_words": factors,
        "middle": middle,
        "schreier_relator": indexed,
        "dehn_parameters": stats,
        "outer_replays": replays,
    }


def degree_three_residues():
    prime = 5
    identity = {(): 1}
    a = {(): 1, (0,): 1}
    b = {(): 1, (1,): 1}

    def multiply(left, right):
        result = {}
        for u, c in left.items():
            for v, d in right.items():
                if len(u) + len(v) <= 3:
                    monomial = u + v
                    result[monomial] = (result.get(monomial, 0) + c * d) % prime
        return {monomial: value for monomial, value in result.items() if value}

    def power(value, exponent):
        result = identity
        for _ in range(exponent % prime):
            result = multiply(result, value)
        return result

    def marking(x, y):
        return {"x": x, "y": y, "X": power(x, -1), "Y": power(y, -1)}

    def evaluate(word, marks):
        value = identity
        for letter in word:
            value = multiply(value, marks[letter])
        return value

    p, q = "XyxYY", "XXyxxYY"
    commutator = "xyXY"
    triple_a = commutator + "x" + inverse(commutator) + "X"
    triple_b = commutator + "y" + inverse(commutator) + "Y"
    ordinary_marks = marking(a, b)
    ordinary_p, ordinary_q = [evaluate(word, ordinary_marks) for word in (p, q)]
    solutions = {}
    for side in ("upper", "lower"):
        rows = []
        for residue in range(prime):
            correction = commutator * residue
            if side == "upper":
                changed = marking(b, evaluate("XXyy" + correction, ordinary_marks))
            else:
                changed = marking(evaluate("xxYY" + correction, ordinary_marks), a)
            changed_p, changed_q = [evaluate(word, changed) for word in (p, q)]
            passing = []
            for i, j, k in product(range(prime), repeat=3):
                word = commutator * i + triple_a * j + triple_b * k
                g = evaluate(word, ordinary_marks)
                shifted_g = evaluate(word, changed)
                if side == "upper":
                    left, right = multiply(shifted_g, changed_q), multiply(changed_p, g)
                else:
                    left, right = (
                        multiply(g, ordinary_q),
                        multiply(ordinary_p, shifted_g),
                    )
                if left == right:
                    passing.append((i, j, k))
            rows.append(passing)
        assert [len(row) for row in rows] == [0, 5, 0, 0, 0]
        solutions[side] = rows
    return {
        "prime": prime,
        "commutator_coordinates_per_case": 125,
        "solutions": solutions,
    }


def main():
    p, height_p = schreier(B)
    q, height_q = schreier(C)
    assert height_p == height_q == -1
    assert p == ((-2, -1), (-1, 1), (-2, 1), (-1, -1), (-1, -1))
    assert q == ((-2, -1), (-2, -1), (-1, 1), (-2, 1), (-2, 1), (-1, -1), (-1, -1))
    assert reduce("XyxYY" + inverse("XXyxxYY")) == reduce("X" + "yXYx" + "x")
    example = lift_example(0)
    assert example is not None
    print(
        json.dumps(
            {
                "donor_coefficients": [p, q],
                "explicit_example": example,
                "width_two_determinant_two": degree_three_residues(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
