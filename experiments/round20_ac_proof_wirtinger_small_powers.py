#!/usr/bin/env python3
"""Replay restrictions on small powers in the free-by-cyclic C quotient."""

import json
from functools import cache
from itertools import combinations, product

from round19_ac_proof_wirtinger_outer import (
    GENS,
    IDENTITY,
    apply_operator,
    characteristic,
    divide_x_minus_one,
    expand_word,
    free_reduce,
    homogeneous,
    inverse_word,
    plus,
    setup,
    substitute_basis,
    substitution,
    symmetric_power,
    times,
)


DEPTH = 6


def reduce_columns(source, pivots, prime, complete=False):
    vector = dict(source)
    remainder = {}
    while vector:
        first = min(vector)
        coefficient = vector[first]
        if first not in pivots:
            if not complete:
                break
            remainder[first] = vector.pop(first)
            continue
        for i, value in pivots[first].items():
            updated = (vector.get(i, 0) - coefficient * value) % prime
            if updated:
                vector[i] = updated
            elif i in vector:
                del vector[i]
    return vector | remainder


def span(columns, prime):
    pivots = {}
    for column in columns:
        vector = reduce_columns(column, pivots, prime)
        if vector:
            first = min(vector)
            inv = pow(vector[first], -1, prime)
            pivots[first] = {i: value * inv % prime for i, value in vector.items()}
    return pivots


def module_quotient(psi, a0, prime):
    a = expand_word(a0, DEPTH, prime)
    expansions = substitute_basis(psi, DEPTH, prime)
    words = tuple(word for word in expansions if word)
    indexes = {word: i for i, word in enumerate(words)}

    def indexed(poly):
        return {indexes[word]: value % prime for word, value in poly.items() if word and value % prime}

    columns = (indexed(plus({word: 1}, times(a, expansions[word], DEPTH, prime), -1, prime))
               for word in words)
    pivots = span(columns, prime)

    @cache
    def monomial_remainder(word):
        return reduce_columns({indexes[word]: 1}, pivots, prime, complete=True)

    def remainder(poly):
        value = {}
        for word, coefficient in poly.items():
            if word and coefficient % prime:
                value = plus(value, monomial_remainder(word), coefficient, prime)
        return value

    assert len(words) == 1092 and len(pivots) == 1002
    assert remainder(a)
    return a, expansions, remainder


def commutator(left, right):
    return free_reduce(left + right + inverse_word(left) + inverse_word(right))


def positive_word(coordinates):
    return "".join(letter * count for letter, count in zip(GENS, coordinates))


def fifth_power_test(psi, a0):
    prime = 5
    a, _, remainder = module_quotient(psi, a0, prime)
    required = remainder(a)
    lie_two = [{(i, j): 1, (j, i): prime - 1} for i, j in combinations(range(3), 2)]
    tested = 0
    survivors = []
    for coordinates in product(range(prime), repeat=3):
        first = {(i,): value for i, value in enumerate(coordinates) if value}
        powers = [IDENTITY]
        for _ in range(prime):
            powers.append(times(powers[-1], first, DEPTH, prime))

        def correction(second):
            result = {}
            for i in range(prime):
                partial = times(powers[i], second, DEPTH, prime)
                result = plus(result, times(partial, powers[prime - 1 - i], DEPTH, prime), prime=prime)
            return result

        base_second = homogeneous(expand_word(positive_word(coordinates), 2, prime), 2)
        base = remainder(plus(powers[prime], correction(base_second), prime=prime))
        pivots = span((remainder(correction(term)) for term in lie_two), prime)
        for multiplier in range(1, prime):
            residual = plus(required, base, -multiplier, prime)
            tested += 1
            if not reduce_columns(residual, pivots, prime):
                survivors.append((coordinates, multiplier))
    assert tested == 500 and not survivors
    return {"prime": prime, "tested": tested, "survivors": survivors}


def third_power_test(psi, a0):
    prime = 3
    a, expansions, remainder = module_quotient(psi, a0, prime)
    linear = {word: homogeneous(image, len(word)) for word, image in expansions.items()}
    coordinates = (2, 1, 1)

    def multiply(left, right, depth=DEPTH):
        return times(left, right, depth, prime)

    def add(left, right, multiple=1):
        return plus(left, right, multiple, prime)

    def inverse_homogeneous_operator(degree, poly):
        characteristic_poly = characteristic(symmetric_power(degree))
        quotient, value = divide_x_minus_one(characteristic_poly)
        result = add({}, apply_operator(quotient, poly, linear), pow(value, -1, prime))
        assert add(result, substitution(result, linear), -1) == poly
        return result

    def cube_variation(low, change):
        squared = multiply(low, low)
        return add(add(multiply(change, squared), multiply(multiply(low, change), low)),
                   multiply(squared, change))

    second_k = inverse_homogeneous_operator(2, homogeneous(a, 2))
    baseline = homogeneous(multiply(a, substitution(add(IDENTITY, second_k), expansions)), 3)
    required = remainder(a)
    prefix = [letter * power for letter, power in zip(GENS, coordinates)]
    first_v = homogeneous(expand_word("".join(prefix), 1, prime), 1)
    first_cube = multiply(multiply(first_v, first_v), first_v)
    first_sixth = multiply(first_cube, first_cube)
    third_k = {multiplier: inverse_homogeneous_operator(3, add(baseline, first_cube, -multiplier))
               for multiplier in (1, 2)}

    comm_two = [commutator(left, right) for left, right in combinations(GENS, 2)]
    comm_three = [commutator(word, letter) for word in comm_two for letter in GENS]
    comm_four = [commutator(word, letter) for word in comm_three for letter in GENS]
    appended = [add(expand_word(word, 4, prime), IDENTITY, -1) for word in comm_three + comm_four]
    survivors = {1: [], 2: []}
    rejected = {1: [], 2: []}
    for seconds in product(range(prime), repeat=3):
        suffix = "".join(word * power for word, power in zip(comm_two, seconds))
        base_v = expand_word("".join(prefix) + suffix, 4, prime)
        nil = add(base_v, IDENTITY, -1)
        low = add(first_v, homogeneous(nil, 2))
        cube = multiply(multiply(nil, nil), nil)
        corrections = [multiply(base_v, part, 4) for part in appended]
        for i, letter in enumerate(GENS):
            shifted = list(prefix)
            shifted[i] += letter * prime
            extra_cube = expand_word("".join(shifted) + suffix, 4, prime)
            corrections.append(add(extra_cube, base_v, -1))
        assert all(all(len(term) in (3, 4) for term in change) for change in corrections)
        pivots = span((remainder(cube_variation(low, change)) for change in corrections), prime)
        for multiplier in (1, 2):
            power = add({}, cube, multiplier)
            if multiplier == 2:
                power = add(power, first_sixth)
            degree_three = homogeneous(power, 3)
            cross_two = multiply(second_k, add(degree_three, homogeneous(power, 4)))
            cross_three = multiply(third_k[multiplier], degree_three)
            correction = add(add(power, cross_two), cross_three)
            residual = add(required, remainder(correction), -1)
            sets = rejected if reduce_columns(residual, pivots, prime) else survivors
            sets[multiplier].append(seconds)
    assert [len(survivors[i]) for i in (1, 2)] == [21, 21]
    return {"prime": prime, "normalized_first_degree": coordinates,
            "remaining_counts_by_alpha_over_3": {i: len(value) for i, value in survivors.items()},
            "rejected_second_degree_commutator_coordinates_by_alpha_over_3": rejected}


def run():
    psi, a0 = setup()
    return {"fifth_power_obstruction": fifth_power_test(psi, a0),
            "third_power_conditions": third_power_test(psi, a0),
            "necessary_positive_absolute_exponents": [1, 2, 3, 6]}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
