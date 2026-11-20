"""Exact fourth-degree obstructions to the determinant-two Wirtinger repair."""

import json
from itertools import product

from elementary_verify import inverse, reduce


class Magnus:
    def __init__(self, modulus):
        self.modulus = modulus
        self.identity = {(): 1}
        self.generators = ({(): 1, (0,): 1}, {(): 1, (1,): 1})

    def multiply(self, left, right):
        coefficients = {}
        for first, a in left.items():
            for second, b in right.items():
                if len(first) + len(second) <= 4:
                    monomial = first + second
                    coefficients[monomial] = (
                        coefficients.get(monomial, 0) + a * b
                    ) % self.modulus
        return {key: value for key, value in coefficients.items() if value}

    def combine(self, *factors):
        value = self.identity
        for factor in factors:
            value = self.multiply(value, factor)
        return value

    def inverse(self, value):
        assert value[()] == 1
        reduced = {term: coefficient for term, coefficient in value.items() if term}
        power = self.identity
        result = self.identity.copy()
        for degree in range(1, 5):
            power = self.multiply(power, reduced)
            for term, coefficient in power.items():
                result[term] = (
                    result.get(term, 0) + (-1) ** degree * coefficient
                ) % self.modulus
        return {key: value for key, value in result.items() if value}

    def power(self, value, exponent):
        if exponent < 0:
            return self.power(self.inverse(value), -exponent)
        return self.combine(*([value] * exponent))

    def commutator(self, left, right):
        return self.combine(left, right, self.inverse(left), self.inverse(right))

    def commutators(self, a, b):
        c = self.commutator(a, b)
        e = self.commutator(c, a)
        f = self.commutator(c, b)
        return (
            c,
            e,
            f,
            self.commutator(e, a),
            self.commutator(e, b),
            self.commutator(f, b),
        )

    def donor_coefficients(self, a, b):
        p = self.combine(self.inverse(a), b, a, self.power(b, -2))
        q = self.combine(self.power(a, -2), b, self.power(a, 2), self.power(b, -2))
        return p, q

    def evaluate_powers(self, basis, exponents):
        return self.combine(*(self.power(word, k) for word, k in zip(basis, exponents)))

    def difference(self, left, right, degree):
        return [
            (left.get(word, 0) - right.get(word, 0)) % self.modulus
            for word in product(range(2), repeat=degree)
        ]


def reduce_columns(rows, columns, prime):
    """Eliminate specified coefficient columns, keeping other columns untouched."""
    rows = [[entry % prime for entry in row] for row in rows]
    pivots = {}
    for column in columns:
        pivot_row = len(pivots)
        index = next((i for i in range(pivot_row, len(rows)) if rows[i][column]), None)
        if index is None:
            continue
        rows[pivot_row], rows[index] = rows[index], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [entry * inverse % prime for entry in rows[pivot_row]]
        for i, row in enumerate(rows):
            if i != pivot_row and row[column]:
                rows[i] = [
                    (a - row[column] * b) % prime for a, b in zip(row, rows[pivot_row])
                ]
        pivots[column] = pivot_row
    return rows, pivots


def affine_system(evaluate, variables, prime):
    origin = evaluate((0,) * variables)
    columns = [
        evaluate(tuple(int(j == i) for j in range(variables))) for i in range(variables)
    ]
    return [
        [(entry - origin[i]) % prime for entry in entries] + [-origin[i] % prime]
        for i, entries in enumerate(zip(*columns))
    ]


def obstruction(singleton, sign, prime):
    group = Magnus(prime)
    a, b = group.generators
    basis = group.commutators(a, b)
    p, q = group.donor_coefficients(a, b)
    p_minus_q = group.combine(p, group.inverse(q))[(0, 1)]
    commutator_exponent = (2 if singleton == "upper" else -1) * p_minus_q
    trace = 3 + sign
    first_powers = (-2, trace) if singleton == "upper" else (trace, -2)
    leading_word = group.evaluate_powers((a, b), first_powers)

    def difference(r, st, g_coordinates, degree):
        monodromy = group.combine(
            leading_word, group.evaluate_powers(basis[:3], (r, *st))
        )
        images = (b, monodromy) if singleton == "upper" else (monodromy, a)
        shifted_basis = group.commutators(*images)
        g = group.evaluate_powers(basis, g_coordinates)
        shifted_g = group.evaluate_powers(shifted_basis, g_coordinates)
        if singleton == "upper":
            shifted_p, shifted_q = group.donor_coefficients(*images)
            left = group.combine(group.inverse(shifted_p), shifted_g, shifted_q)
            right = g
        else:
            left = group.combine(group.inverse(p), g, q)
            right = shifted_g
        return group.difference(left, right, degree)

    records = []
    i = commutator_exponent % prime
    for r in range(prime):
        lower = affine_system(
            lambda jk, r=r: difference(r, (0, 0), (i, *jk), 3), 2, prime
        )
        lower, pivots = reduce_columns(lower, range(2), prime)
        assert len(pivots) == 2 and not any(any(row) for row in lower[2:])
        j, k = (lower[pivots[index]][-1] for index in range(2))
        higher = affine_system(
            lambda inputs, r=r, j=j, k=k: difference(
                r, inputs[:2], (i, j, k, *inputs[2:]), 4
            ),
            5,
            prime,
        )
        higher, pivots = reduce_columns(higher, range(2, 5), prime)
        assert all(not any(row[2:5]) for row in higher[len(pivots) :])
        projected = [[row[0], row[1], row[-1]] for row in higher[len(pivots) :]]
        conditions, pivots = reduce_columns(projected, range(2), prime)
        assert len(pivots) == 1 and not any(any(row) for row in conditions[1:])
        assert sum(conditions[0][:2]) > 0
        records.append({"r": r, "condition_for_s_t": conditions[0]})
    rows = [entry["condition_for_s_t"] for entry in records]
    a = rows[0][2]
    c = (rows[2][2] - 2 * rows[1][2] + a) * pow(2, -1, prime) % prime
    b = (rows[1][2] - c - a) % prime
    assert rows == [
        [1, rows[0][1], (c * r * r + b * r + a) % prime] for r in range(prime)
    ]
    return {
        "singleton": singleton,
        "sign": sign,
        "modulus": prime,
        "trace": trace,
        "t_coefficient": rows[0][1],
        "right_hand_polynomial_descending": [c, b, a],
        "records": records,
    }


def cyclic_core(word):
    word = reduce(word)
    while len(word) > 1 and word[0] == inverse(word[-1]):
        word = word[1:-1]
    return word


def end_powers(word, letter):
    left = 0
    while left < len(word) and word[left].lower() == letter:
        left += 1
    right = len(word)
    while right > left and word[right - 1].lower() == letter:
        right -= 1
    assert left < right
    before, after = word[:left], word[right:]
    exponent = lambda section: section.count(letter) - section.count(letter.upper())
    return exponent(before), exponent(after)


def sparse_middle_obstruction():
    # Here the free generators a,b are encoded by x,y respectively.
    p, q = "XyxYY", "XXyxxYY"
    records = []
    for upper, determinant in product((True, False), (0, 2)):
        wanted = (determinant - 1) if upper else (1 - determinant)
        power_letter = "x" if upper else "y"
        for a, b in product("xX", "yY"):
            if (1 if a.islower() == b.islower() else -1) != wanted:
                continue
            fixed = a + b + inverse(a) + inverse(b)
            if upper:
                target = reduce(
                    inverse(q) + inverse(a.replace("x", "y").replace("X", "Y")) + p
                )
            else:
                target = reduce(q + b.replace("y", "x").replace("Y", "X") + inverse(p))
            u_left, u_right = end_powers(fixed, power_letter)
            v_left, v_right = end_powers(target, power_letter)
            exceptions = sorted({-u_left - v_right, u_right + v_left})
            cores = []
            for exponent in exceptions:
                stem = (power_letter if exponent >= 0 else power_letter.upper()) * abs(
                    exponent
                )
                core = cyclic_core(stem + fixed + inverse(stem) + target)
                assert len(core) > 1
                cores.append([exponent, core])
            records.append(
                {
                    "singleton": "upper" if upper else "lower",
                    "determinant": determinant,
                    "commutator": fixed,
                    "fixed_right_word": target,
                    "power_letter": power_letter,
                    "seam_zero_cases": cores,
                }
            )
    assert len(records) == 8
    return records


def main():
    all_cases = []
    for side, sign in product(("upper", "lower"), (-1, 1)):
        for prime in (3, 17 if sign < 0 else 7):
            all_cases.append(obstruction(side, sign, prime))
    print(
        json.dumps(
            {
                "degree_four_residues": all_cases,
                "two_occurrence_middle_exclusion": sparse_middle_obstruction(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
