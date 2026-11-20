#!/usr/bin/env python3
"""Replay the free-word and polynomial obstructions in the overlap branch."""

import json

from elementary_verify import inverse, reduce


P = "XyxYY"
Q = "XXyxxYY"


def multiply(left, right):
    coefficients = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            coefficients[i + j] += a * b
    return coefficients


def cubic_controls():
    # Coefficients are in increasing order of powers of t.
    cases = {
        1: ([1, -1, 1], [-1, 1, 1], 3, [1, -1, 0, 1], 1),
        -1: ([1, 1, -1], [1, -1, 1], 1, [1, 0, -1, 1], -1),
    }
    controls = {}
    for sign, (first, second, subtract_at, cubic, multiplier) in cases.items():
        coefficients = multiply(first, second)
        coefficients[subtract_at] -= 1
        assert coefficients == multiply([-multiplier, multiplier], cubic)
        assert all(sum(coeff * root**i for i, coeff in enumerate(cubic)) for root in (-1, 1))
        controls[sign] = {"coefficients": coefficients, "cubic_factor": cubic}
    return controls


def conjugacy_controls():
    controls = {}
    for sign, (first, last) in {1: (Q, P), -1: (P, Q)}.items():
        target = reduce("Y" + first + "x" + inverse(last))
        assert len(target) == 14 and target[0] != target[-1].swapcase()
        rotations = []
        midpoint = len(target) // 2
        for offset in range(len(target)):
            rotation = target[offset:] + target[:offset]
            if rotation[0] == "Y" and rotation[midpoint] == "x":
                first_half = rotation[1:midpoint]
                inverse_second_half = inverse(rotation[midpoint + 1 :])
                assert first_half != inverse_second_half
                rotations.append({"rotation": rotation, "first_half": first_half,
                                  "inverse_second_half": inverse_second_half})
        assert len(rotations) == (2 if sign == 1 else 1)
        controls[sign] = {"cyclic_target": target, "eligible_rotations": rotations}
    return controls


if __name__ == "__main__":
    print(json.dumps({"polynomial_identities": cubic_controls(),
                      "simple_lift_exclusions": conjugacy_controls()}, indent=2, sort_keys=True))
