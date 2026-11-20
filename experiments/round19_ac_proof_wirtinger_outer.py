#!/usr/bin/env python3
"""Replay outer twisted-conjugacy obstructions in the free-by-cyclic donor quotient."""

import json
from collections import defaultdict
from itertools import product
from math import factorial, gcd

from round10_ac_proof_blocks import A, C


GENS = "uvw"
IDENTITY = {(): 1}


def inverse_word(word):
    return word[::-1].swapcase()


def free_reduce(word):
    stack = []
    for letter in word:
        if stack and stack[-1] == letter.swapcase():
            stack.pop()
        else:
            stack.append(letter)
    return "".join(stack)


def height_rewrite(word):
    index = 0
    letters = []
    for letter in word:
        if letter == "x":
            index += 1
        elif letter == "X":
            index -= 1
        elif letter == "y":
            index -= 1
            letters.append((index, 1))
        else:
            letters.append((index, -1))
            index += 1
    return letters, index


def setup():
    relation, height = height_rewrite(C)
    assert height == 0
    assert relation == [(-2, -1), (-1, -1), (0, 1), (-2, 1), (-3, 1), (-2, -1), (-1, -1)]
    t0 = "wvwvUV"
    basis = {-3: "u", -2: "v", -1: "w", 0: t0}

    def kernel_word(letters):
        return free_reduce("".join(basis[index] if sign == 1 else inverse_word(basis[index])
                                   for index, sign in letters))

    assert kernel_word(relation) == ""
    a_quotient, a_height = height_rewrite(A)
    assert a_height == 1
    a0 = free_reduce(kernel_word(a_quotient) + "w")
    shift = ["v", "w", t0]
    psi = [free_reduce("W" + word + "w") for word in shift]
    expected_exponents = [(0, 1, 0), (0, 0, 1), (-1, 1, 2)]
    assert [tuple(word.count(g) - word.count(g.upper()) for g in GENS) for word in psi] == expected_exponents
    return psi, a0


def plus(left, right, multiple=1, prime=None):
    result = dict(left)
    for word, coefficient in right.items():
        result[word] = result.get(word, 0) + multiple * coefficient
    if prime is not None:
        result = {word: coefficient % prime for word, coefficient in result.items()}
    return {word: coefficient for word, coefficient in result.items() if coefficient}


def scale(poly, scalar):
    return {word: coefficient * scalar for word, coefficient in poly.items() if coefficient * scalar}


def times(left, right, degree, prime=None):
    result = defaultdict(int)
    for x, a in left.items():
        for y, b in right.items():
            if len(x) + len(y) <= degree:
                result[x + y] += a * b
    return plus({}, result, prime=prime)


def expand_word(word, degree, prime=None):
    result = IDENTITY
    for letter in word:
        generator = GENS.index(letter.lower())
        if letter.islower():
            series = {(): 1, (generator,): 1}
        else:
            series = {(generator,) * n: (-1)**n for n in range(degree + 1)}
        result = times(result, series, degree, prime)
    return result


def substitute_basis(psi, degree, prime=None):
    images = [plus(expand_word(word, degree, prime), IDENTITY, -1, prime) for word in psi]
    expansions = {(): IDENTITY}
    for n in range(1, degree + 1):
        for word in product(range(3), repeat=n):
            expansions[word] = times(expansions[word[:-1]], images[word[-1]], degree, prime)
    return expansions


def homogeneous(poly, degree):
    return {word: coefficient for word, coefficient in poly.items() if len(word) == degree}


def substitution(poly, expansions):
    result = defaultdict(int)
    for term, coefficient in poly.items():
        for word, value in expansions[term].items():
            result[word] += coefficient * value
    return {word: coefficient for word, coefficient in result.items() if coefficient}


def symmetric_power(degree):
    """Apply U->V, V->W, W->-U+V+2W to commutative degree-d monomials."""
    weights = [(i, j, degree - i - j) for i in range(degree + 1) for j in range(degree + 1 - i)]
    indexes = {weight: index for index, weight in enumerate(weights)}
    matrix = [[0] * len(weights) for _ in weights]
    for column, (i, j, k) in enumerate(weights):
        for a in range(k + 1):
            for b in range(k + 1 - a):
                c = k - a - b
                coefficient = ((-1) ** a) * (2**c) * factorial(k) // (factorial(a) * factorial(b) * factorial(c))
                matrix[indexes[a, i + b, j + c]][column] = coefficient
    return matrix


def characteristic(matrix):
    size = len(matrix)
    traces = [size]
    matrix_power = matrix
    for exponent in range(1, size + 1):
        traces.append(sum(matrix_power[i][i] for i in range(size)))
        if exponent < size:
            columns = list(zip(*matrix))
            matrix_power = [[sum(a * b for a, b in zip(row, col)) for col in columns] for row in matrix_power]
    coefficients = [1]
    for k in range(1, size + 1):
        total = -sum(coefficients[k - i] * traces[i] for i in range(1, k + 1))
        assert total % k == 0
        coefficients.append(total // k)
    return coefficients


def divide_x_minus_one(coefficients):
    quotient = [coefficients[0]]
    for coefficient in coefficients[1:-1]:
        quotient.append(coefficient + quotient[-1])
    return quotient, coefficients[-1] + quotient[-1]


def apply_operator(coefficients, poly, linear):
    result = {}
    for coefficient in coefficients:
        result = plus(substitution(result, linear), poly, coefficient)
    return result


def uniform_outer_obstruction(psi, a0):
    depth = 6
    expansions = substitute_basis(psi, depth)
    linear = {word: homogeneous(series, len(word)) for word, series in expansions.items()}
    a = expand_word(a0, depth)
    k = IDENTITY
    denominator = 1
    records = []
    for degree in range(1, depth + 1):
        residual = homogeneous(plus(times(a, substitution(k, expansions), depth), k, -1), degree)
        char = characteristic(symmetric_power(degree))
        quotient, value = divide_x_minus_one(char)
        record = {"degree": degree, "symmetric_characteristic_at_1": value}
        records.append(record)
        if degree < depth:
            assert value
            correction = apply_operator(quotient, residual, linear)
            assert plus(correction, substitution(correction, linear), -1) == scale(residual, value)
            k = plus(scale(k, value), correction)
            denominator *= value
        else:
            assert not value
            while sum(quotient) == 0:
                quotient, remainder = divide_x_minus_one(quotient)
                assert not remainder
            witness = apply_operator(quotient, residual, linear)
            assert witness and substitution(witness, linear) == witness
            common_divisor = gcd(*witness.values())
            first = min(witness)
            record.update({"projector_characteristic_quotient": quotient, "witness_support": len(witness),
                           "witness_coefficient_gcd": common_divisor,
                           "example_coefficient": [list(first), witness[first]]})
    return {"denominator": denominator, "stages": records,
            "excluded_prime_divisors_threshold": depth + 1,
            "exception_integer": abs(denominator * common_divisor)}


def field_obstruction(psi, a0, prime, depth):
    a = expand_word(a0, depth, prime)
    expansions = substitute_basis(psi, depth, prime)
    words = [word for word in expansions if word]
    indexes = {word: i for i, word in enumerate(words)}
    pivots = {}

    def eliminate(vector):
        while vector:
            leading = min(vector)
            if leading not in pivots:
                break
            coefficient = vector[leading]
            for i, value in pivots[leading].items():
                remainder = (vector.get(i, 0) - coefficient * value) % prime
                if remainder:
                    vector[i] = remainder
                elif i in vector:
                    del vector[i]
        return vector

    for word in words:
        column = plus({word: 1}, times(a, expansions[word], depth, prime), -1, prime)
        column = eliminate({indexes[term]: coefficient for term, coefficient in column.items()})
        if column:
            leading = min(column)
            inverse = pow(column[leading], -1, prime)
            pivots[leading] = {i: coefficient * inverse % prime for i, coefficient in column.items()}
    residual = eliminate({indexes[word]: coefficient for word, coefficient in a.items() if word})
    assert residual
    first = min(residual)
    exponent_bound = prime
    while exponent_bound <= depth:
        exponent_bound *= prime
    return {"prime": prime, "depth": depth, "excluded_divisor": exponent_bound,
            "rank": len(pivots), "variables": len(words),
            "first_nonzero_remainder": [list(words[first]), residual[first]]}


def run():
    psi, a0 = setup()
    uniform = uniform_outer_obstruction(psi, a0)
    assert uniform["exception_integer"] == 2**14 * 7**7 * 13**10 * 71**2
    uniform["exception_integer_factors"] = {2: 14, 7: 7, 13: 10, 71: 2}
    fields = [field_obstruction(psi, a0, prime, depth)
              for prime, depth in ((2, 3), (7, 6), (13, 4), (71, 6))]
    return {"kernel_shift_by_b_inverse": psi, "A_kernel_factor": a0,
            "uniform_outer_obstruction": uniform, "finite_field_obstructions": fields,
            "necessary_positive_absolute_exponents": [1, 2, 3, 5, 6, 10, 15, 30]}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
