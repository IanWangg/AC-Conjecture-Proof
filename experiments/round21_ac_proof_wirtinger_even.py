#!/usr/bin/env python3
"""Check the two even exponent residues in the C deletion quotient."""

from itertools import combinations, product
import json

from round19_ac_proof_wirtinger_outer import (
    GENS, IDENTITY, expand_word, homogeneous, inverse_word, plus, setup,
    substitute_basis, substitution,
)
from round20_ac_proof_wirtinger_small_powers import commutator


DEPTH = 6


def add(left, right):
    return plus(left, right, prime=2)


def multiply(left, right, depth=DEPTH):
    right_by_degree = [[] for _ in range(depth + 1)]
    for word, coefficient in right.items():
        if len(word) <= depth and coefficient % 2:
            right_by_degree[len(word)].append(word)
    terms = set()
    for left_word, coefficient in left.items():
        if not coefficient % 2:
            continue
        for degree in range(depth - len(left_word) + 1):
            for right_word in right_by_degree[degree]:
                word = left_word + right_word
                if word in terms:
                    terms.remove(word)
                else:
                    terms.add(word)
    return dict.fromkeys(terms, 1)


def expand(word, depth=DEPTH):
    return expand_word(word, depth, 2)


def reduce_bits(vector, pivots):
    while vector:
        pivot = vector.bit_length() - 1
        if pivot not in pivots:
            break
        vector ^= pivots[pivot]
    return vector


def insert(vector, pivots):
    reduced = reduce_bits(vector, pivots)
    if reduced:
        pivots[reduced.bit_length() - 1] = reduced
    return bool(reduced)


def solve_unique(columns, target):
    pivots = {}
    for i, vector in enumerate(columns):
        coordinates = 1 << i
        while vector and vector.bit_length() - 1 in pivots:
            reduced, implied = pivots[vector.bit_length() - 1]
            vector ^= reduced
            coordinates ^= implied
        assert vector
        pivots[vector.bit_length() - 1] = vector, coordinates
    answer = 0
    while target:
        vector, coordinates = pivots[target.bit_length() - 1]
        target ^= vector
        answer ^= coordinates
    return answer


def brackets(words):
    return tuple(dict.fromkeys(commutator(word, letter) for word in words for letter in GENS))


def all_choices(base, parts):
    directions = [base]
    for part in parts:
        directions = [row for partial in directions for row in (partial, add(partial, part))]
    return directions


def describe_survivors(survivors):
    if not survivors:
        return {"count": 0}
    masks = []
    for mask in range(1, 256):
        bits = {bin(mask & coordinate).count("1") % 2 for coordinate in survivors}
        if len(bits) == 1:
            masks.append((mask, bits.pop()))
    assert len(masks) == 1 and len(survivors) == 128
    mask, parity = masks[0]
    return {"count": len(survivors), "weight_three_bitmask": mask, "parity": parity}


class Catalogue:
    def __init__(self, shift):
        self.shifts = substitute_basis(shift, DEPTH, 2)
        self.by_degree = [tuple(word for word in self.shifts if len(word) == degree)
                          for degree in range(DEPTH + 1)]
        # The leading bit is assigned to the lowest remaining degree.
        self.index = {word: i for i, word in enumerate(reversed(self.shifts))}
        self.degree_two = [self.bits(add({word: 1}, homogeneous(self.shifts[word], 2)))
                           for word in self.by_degree[2]]
        self.weight_two = [commutator(left, right) for left, right in combinations(GENS, 2)]
        weight_three = brackets(self.weight_two)
        self.weight_three = []
        self.weight_three_words = []
        independent = {}
        for word in weight_three:
            term = homogeneous(expand(word, 3), 3)
            if insert(self.bits(term), independent):
                self.weight_three.append(add(expand(word, 5), IDENTITY))
                self.weight_three_words.append(word)
        assert len(self.weight_three) == 8
        weight_four = brackets(weight_three)
        weight_five = brackets(weight_four)
        high_words = [word * 2 for word in self.weight_two] + list(weight_four + weight_five)
        prefix = expand("Uvw", 1)
        self.high_terms = [multiply(prefix, add(expand(word, 5), IDENTITY), 5)
                           for word in high_words]
        assert all(all(len(word) in (4, 5) for word in term) for term in self.high_terms)

    def bits(self, poly):
        return sum(1 << self.index[word] for word, coefficient in poly.items() if coefficient % 2)

    def test_configuration(self, target, shifted_target, parity_two, alpha_residue):
        word = "Uvw" + "".join(word * exponent for word, exponent in zip(self.weight_two, parity_two))
        base = expand(word, 5)
        low = add(homogeneous(base, 1), homogeneous(base, 2))
        square = multiply(low, low)
        degree_two_residual = self.bits(add(homogeneous(target, 2), homogeneous(square, 2)))
        degree_two_coefficients = solve_unique(self.degree_two, degree_two_residual)
        second = {word: 1 for i, word in enumerate(self.by_degree[2]) if degree_two_coefficients >> i & 1}
        small_k = add(IDENTITY, second)
        left_target = multiply(target, substitution(small_k, self.shifts))
        through_three = add(IDENTITY, add(homogeneous(square, 2), homogeneous(square, 3)))

        pivots = {}
        for degree in range(3, DEPTH + 1):
            for monomial in self.by_degree[degree]:
                column = add(shifted_target[monomial], multiply({monomial: 1}, through_three))
                insert(self.bits(column), pivots)
        k_rank = len(pivots)
        for delta in self.high_terms:
            change = add(multiply(low, delta), multiply(delta, low))
            insert(self.bits(multiply(small_k, change)), pivots)

        survivors = []
        initial = add(base, IDENTITY)
        third_choices = [multiply(base, delta, 5) for delta in self.weight_three]
        for coordinate, nil in enumerate(all_choices(initial, third_choices)):
            power_two = multiply(nil, nil)
            power = add(IDENTITY, power_two)
            if alpha_residue == 6:
                power_four = multiply(power_two, power_two)
                power = add(power, add(power_four, multiply(power_four, power_two)))
            residual = self.bits(add(left_target, multiply(small_k, power)))
            if not reduce_bits(residual, pivots):
                survivors.append(coordinate)
        return {"weight_two": parity_two, "conjugator_column_rank": k_rank,
                "joint_column_rank": len(pivots), "surviving_weight_three": survivors}

    def shifted_target(self, target):
        assert not homogeneous(target, 1)
        return {word: multiply(target, value) for word, value in self.shifts.items()}


def run():
    shift, outer_word = setup()
    catalogue = Catalogue(shift)
    cases = {}
    target = expand(outer_word)
    shifted_target = catalogue.shifted_target(target)
    for alpha_residue in (2, 6):
        rows = [catalogue.test_configuration(target, shifted_target, parity, alpha_residue)
                for parity in product(range(2), repeat=3)]
        assert [row["weight_two"] for row in rows if row["surviving_weight_three"]] == [(1, 0, 1), (1, 1, 1)]
        for row in rows:
            row["weight_three_condition"] = describe_survivors(row.pop("surviving_weight_three"))
        cases[alpha_residue] = rows

    # Construct a nonzero conjugator and a relator with an actual high correction.
    parity = (1, 0, 1)
    correction = commutator(catalogue.weight_two[0], catalogue.weight_two[-1])
    v = "Uvw" + catalogue.weight_two[0] + catalogue.weight_two[2] + correction
    k = catalogue.weight_two[1]
    shifted_k = "".join(shift[GENS.index(letter)] if letter.islower()
                        else inverse_word(shift[GENS.index(letter.lower())]) for letter in k)
    control_word = k + v * 6 + inverse_word(shifted_k)
    control = expand(control_word)
    positive = catalogue.test_configuration(control, catalogue.shifted_target(control), parity, 6)
    assert 0 in positive["surviving_weight_three"]
    positive["weight_three_condition"] = describe_survivors(positive.pop("surviving_weight_three"))
    return {"characteristic": 2, "depth": DEPTH, "normalized_weight_one": [-1, 1, 1],
            "class_three_cases_tested": 2 * 8 * 256, "remaining_absolute_exponents": [1, 2, 3, 6],
            "weight_three_words": catalogue.weight_three_words,
            "exponent_residue_rows": cases,
            "positive_control": {"v": v, "conjugator": k, "exponent": 6, "scan": positive}}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
