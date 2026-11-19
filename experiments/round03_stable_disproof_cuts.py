"""Replay a same-marking excursion and enumerate degree-one crossing patterns."""

import json
from fractions import Fraction
from itertools import permutations

from round02_stable_disproof_search import inverse, reduce_word


def exponent(word):
    return tuple(word.count(letter) - word.count(letter.upper()) for letter in "xyz")


def replay(start, moves):
    rows = list(start)
    yield tuple(rows)
    for operation, receiver, donor, sign in moves:
        if operation == "multiply":
            assert receiver != donor and sign in (1, -1)
            word = rows[donor] if sign == 1 else inverse(rows[donor])
            rows[receiver] = reduce_word(rows[receiver] + word)
        elif operation == "conjugate":
            assert donor in "xyzXYZ"
            rows[receiver] = reduce_word(donor + rows[receiver] + inverse(donor))
        else:
            assert operation == "invert"
            rows[receiver] = inverse(rows[receiver])
        yield tuple(rows)


def conjugations(row, word):
    return [("conjugate", row, letter, 1) for letter in reversed(word)]


def affine_mul(lhs, rhs):
    return lhs[0] * rhs[0], lhs[0] * rhs[1] + lhs[1]


def affine_inv(pair):
    return 1 / pair[0], -pair[1] / pair[0]


def control():
    w = "xyXYY"
    start = (w, "x", "z")
    moves = [
        ("multiply", 2, 0, 1),
        ("multiply", 0, 1, 1),
        ("multiply", 0, 1, -1),
        ("multiply", 1, 2, 1),
        ("multiply", 2, 0, -1),
        *conjugations(2, inverse(w)),
        ("multiply", 1, 2, -1),
        *conjugations(2, w),
    ]
    states = list(replay(start, moves))
    assert states[5] == (w, "xz" + w, "z")
    assert states[-1] == (w, "x" + w, "z")
    assert all(exponent(word) not in (exponent(w), exponent(inverse(w))) for word in states[2][:2])
    removal = str.maketrans("", "", "zZ")
    before = tuple(reduce_word(word.translate(removal)) for word in states[0][:2])
    after = tuple(reduce_word(word.translate(removal)) for word in states[4][:2])
    assert before == (w, "x") and after == (w, "x" + w)
    splice = [("multiply", 1, 0, 1)]
    assert tuple(replay(before, splice))[-1] == after
    cleanup = [
        ("multiply", 1, 0, -1),
        ("multiply", 0, 1, -1),
        *conjugations(0, "X"),
        *conjugations(1, "yy"),
        ("multiply", 0, 1, 1),
        *conjugations(1, "YY"),
        ("invert", 0, None, 1),
    ]
    endpoint = list(replay(states[-1], cleanup))[-1]
    assert endpoint == ("y", "x", "z")
    crossed = [m for m in moves if m[0] == "multiply" and ((m[1] == 2) != (m[2] == 2))]
    directions = ["in" if m[1] == 2 else "out" for m in crossed]
    assert directions == ["in", "out", "in", "out"]
    x = (Fraction(2), Fraction(0))
    y = (Fraction(1), Fraction(1))
    images = {"x": x, "y": y, "X": affine_inv(x), "Y": affine_inv(y)}
    value = (Fraction(1), Fraction(0))
    for letter in w:
        value = affine_mul(value, images[letter])
    assert value == (1, 0) and affine_mul(x, y) != affine_mul(y, x)
    return {
        "start": start,
        "crossing_order": directions,
        "state_with_no_retained_conjugate_of_donor": states[2],
        "projected_before_capture": before,
        "projected_before_erasure": after,
        "excursion_moves": len(moves),
        "projected_splice_moves": len(splice),
        "excursion_endpoint": states[-1],
        "moves_to_unordered_basis": len(moves) + len(cleanup),
        "endpoint": endpoint,
    }


def crossing(first, second):
    # A rank-one shear on a plane over F2 is determined by its
    # one-dimensional functional kernel and a nonzero vector in the donor.
    for kernel_generator in first - {0}:
        for donor in second - {0}:
            yield frozenset(
                vector if vector in (0, kernel_generator) else vector ^ donor
                for vector in first
            )


def linear_patterns():
    u, v = frozenset((0, 1, 2, 3)), frozenset((0, 4, 8, 12))
    axes = {1, 2, 4, 8}
    result = {}
    for pattern in sorted(set(permutations("AABB"))):
        states = {(u, v)}
        for side in pattern:
            if side == "A":
                states = {(new_a, b) for a, b in states for new_a in crossing(a, b)}
            else:
                states = {(a, new_b) for a, b in states for new_b in crossing(b, a)}
        transfers = sorted({
            len(a & v & axes) for a, b in states if len(a & axes) == len(b & axes) == 2
        })
        result["".join(pattern)] = {"span_states": len(states), "coordinate_transfers": transfers}
    assert result["AABB"]["coordinate_transfers"] == result["BBAA"]["coordinate_transfers"] == [0]
    assert all(d["coordinate_transfers"] == [0, 1] for p, d in result.items()
               if p not in {"AABB", "BBAA"})
    return result


if __name__ == "__main__":
    print(json.dumps({"metabelian_donor_control": control(), "degree_one_two_by_two": linear_patterns()}, indent=2))
