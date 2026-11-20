#!/usr/bin/env python3
"""Replay the complete sign test for a two-letter cyclic shift core."""

import json
from collections import Counter
from itertools import combinations, permutations, product

from round14_ac_proof_wirtinger_degree4 import Magnus


# Count only affected letters. For the lower singleton the affected letter is a.
AFFECTED_SIGNS = {
    "upper": ((1, -1, -1), (1, 1, -1)),  # P and Q^{-1} with affected letter b
    "lower": ((-1, 1), (-1, -1, 1, 1)),  # P^{-1} and Q with affected letter a
}


def input_patterns(coordinate):
    """Yield balanced input signs and gap vectors that pass the class-two test."""
    for positive in combinations(range(4), 2):
        signs = tuple(1 if index in positive else -1 for index in range(4))
        for plus, minus in permutations(range(5), 2):
            gaps = tuple((index == plus) - (index == minus) for index in range(5))
            if any(not gaps[i] and signs[i - 1] != signs[i] for i in range(1, 4)):
                yield signs, gaps, "unreduced_input"
                continue
            area = sum(gap * sum(signs[i:]) for i, gap in enumerate(gaps))
            yield signs, gaps, "" if area == coordinate else "class_two_mismatch"


def shift_signs(core_signs, input_signs, gaps):
    result = []
    inverse_signs = tuple(-sign for sign in reversed(core_signs))
    if gaps[0]:
        result.append(gaps[0])
    for sign, gap in zip(input_signs, gaps[1:]):
        result.extend(core_signs if sign == 1 else inverse_signs)
        if gap:
            result.append(gap)
    return tuple(result)


def conjugator_residues():
    """Restrict the remaining shift family by the class-four condition mod 3."""
    group = Magnus(3)
    a, b = group.generators
    hall_commutator = group.commutator(a, b)
    conditions = {
        ("upper", -1): (2, lambda r: 1),
        ("upper", 1): (1, lambda r: r * r + 2 * r + 1),
        ("lower", -1): (2, lambda r: r + 1),
        ("lower", 1): (1, lambda r: 2 * r * r + 2 * r + 2),
    }
    result = {}
    for (side, epsilon), (multiplier, polynomial) in conditions.items():
        trace = 3 + epsilon
        c, d = (a, b) if side == "upper" else (b, a)
        base_exponents = (-2, trace) if side == "upper" else (trace, -2)
        base_inverse = group.inverse(group.evaluate_powers((a, b), base_exponents))
        residue_commutator = group.commutator(c, d)
        admissible = []
        for first_power in range(3):
            admissible_for_power = []
            for conjugator_coordinate in range(3):
                j = group.power(residue_commutator, conjugator_coordinate)
                w = group.combine(
                    group.power(d, first_power),
                    j,
                    group.power(c, -2),
                    group.inverse(j),
                    group.power(d, trace - first_power),
                )
                remainder = group.combine(base_inverse, w)
                r = remainder.get((0, 1), 0)
                remainder = group.combine(group.power(hall_commutator, -r), remainder)
                s = -remainder.get((0, 0, 1), 0)
                t = remainder.get((0, 1, 1), 0)
                if (s + multiplier * t - polynomial(r)) % 3 == 0:
                    admissible_for_power.append(conjugator_coordinate)
            assert len(admissible_for_power) == 1
            admissible.extend(admissible_for_power)
        assert epsilon != 1 or 0 not in admissible
        result[f"{side}, epsilon {epsilon}"] = admissible
    return result


def run():
    counts = {}
    surviving_input_patterns = {}
    for determinant in (0, 2):
        patterns = tuple(input_patterns(determinant - 1))
        surviving_input_patterns[determinant] = [
            dict(input_signs=signs, gaps=gaps) for signs, gaps, rejection in patterns if not rejection
        ]
        for side, (left, right) in AFFECTED_SIGNS.items():
            counter = Counter()
            counts[f"{side}, determinant {determinant}"] = counter
            for core_signs in product((-1, 1), repeat=2):
                for signs, gaps, rejection in patterns:
                    counter["cases"] += 1
                    if rejection:
                        counter[rejection] += 1
                    elif shift_signs(core_signs, signs, gaps) != left + signs + right:
                        counter["affected_sign_mismatch"] += 1
                    else:
                        counter["survivors"] += 1
            assert not counter["survivors"]
    totals = Counter()
    for counter in counts.values():
        totals.update(counter)
    return dict(
        counts=counts,
        totals=totals,
        surviving_input_patterns=surviving_input_patterns,
        admissible_conjugator_coordinates_mod_3_by_first_power=conjugator_residues(),
    )


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
