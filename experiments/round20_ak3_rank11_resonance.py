"""Test the rank-eleven twisted-conjugacy equation in resonant degree three."""

import json
from functools import cache
from itertools import product
from math import comb

from round19_ak3_minima_fibres import indexed_pair, reverse_mark
from round19_ak3_minimum_class_two import solve_letter

DONOR = "xxxYxxYXYXY"
RECEIVER = "xxyXYY"
PRIMES = (821, 9377)


def update(out, key, value, p):
    new = (out.get(key, 0) + value) % p
    if new:
        out[key] = new
    else:
        out.pop(key, None)


def add_scaled(out, values, scale, p):
    for key, value in values.items():
        update(out, key, scale * value, p)


def multiply(left, right, p, degree=3):
    result = {}
    for a, x in left.items():
        for b, y in right.items():
            if len(a) + len(b) <= degree:
                update(result, a + b, x * y, p)
    return result


def inverse(series, p):
    delta = series.copy()
    update(delta, (), -1, p)
    term, answer = {(): 1}, {(): 1}
    for j in range(1, 4):
        term = multiply(term, delta, p)
        add_scaled(answer, term, (-1) ** j, p)
    assert multiply(series, answer, p) == {(): 1}
    return answer


def substitute(series, images, p, degree=3):
    result = {}
    for word, coefficient in series.items():
        term = {(): coefficient}
        for index in word:
            term = multiply(term, images[index], p, degree)
        add_scaled(result, term, 1, p)
    return result


class Block:
    def __init__(self, linear, degree, p):
        self.rank, self.degree, self.p = len(linear), degree, p
        self.pivots = {}
        self.columns = {}
        self.boundary = []
        assert all(linear[i] == {(i + 1,): 1} for i in range(self.rank - 1))
        for word in product(range(self.rank), repeat=degree):
            if max(word) < self.rank - 1:
                # An internal column is exactly e_word - e_(word+1).
                continue
            self.boundary.append(word)
            column = {word: 1}
            add_scaled(column, substitute({word: 1}, linear, p, degree), -1, p)
            self.columns[word] = column
            vector = self.project(column)
            combined = {word: 1}
            while vector:
                row = min(vector)
                coeff = vector[row]
                if row not in self.pivots:
                    scale = pow(coeff, -1, p)
                    self.pivots[row] = (
                        {k: v * scale % p for k, v in vector.items()},
                        {k: v * scale % p for k, v in combined.items()},
                    )
                    break
                previous, previous_combined = self.pivots[row]
                add_scaled(vector, previous, -coeff, p)
                add_scaled(combined, previous_combined, -coeff, p)

    def project(self, target):
        result = {}
        for word, coefficient in target.items():
            low = min(word)
            update(result, tuple(i - low for i in word), coefficient, self.p)
        return result

    def remainder(self, target):
        remaining, formal = self.project(target), {}
        for row, (vector, basis) in sorted(self.pivots.items()):
            coefficient = remaining.get(row, 0)
            if coefficient:
                add_scaled(remaining, vector, -coefficient, self.p)
                add_scaled(formal, basis, coefficient, self.p)
        return remaining, formal

    def particular(self, target):
        remainder, border = self.remainder(target)
        assert not remainder
        terms = target.copy()
        for key, coefficient in border.items():
            add_scaled(terms, self.columns[key], -coefficient, self.p)
        assert not self.project(terms)
        # Lift along each chain of diagonal index shifts.
        result = border.copy()
        for word in product(range(self.rank), repeat=self.degree):
            if max(word) == self.rank - 1:
                continue
            amount = terms.get(word, 0)
            if amount:
                update(result, word, amount, self.p)
                update(terms, word, -amount, self.p)
                update(terms, tuple(i + 1 for i in word), amount, self.p)
        assert not terms
        return result

    def dual(self, coordinate):
        assert coordinate not in self.pivots
        functional = {coordinate: 1}
        for row, (vector, _) in reversed(sorted(self.pivots.items())):
            value = -sum(coefficient * functional.get(k, 0) for k, coefficient in vector.items())
            update(functional, row, value, self.p)
        for operator in self.columns.values():
            assert sum(coefficient * functional.get(row, 0)
                       for row, coefficient in self.project(operator).items()) % self.p == 0
        return functional


def test(p):
    chart, _ = reverse_mark(DONOR)
    relator, row = indexed_pair(DONOR, RECEIVER, chart)
    low = min(i for i, _ in relator)
    high = max(i for i, _ in relator)
    assert (low, high) == (0, 11)
    upper = solve_letter(relator, high)
    lower = solve_letter(relator, low)

    @cache
    def indexed(i):
        if low <= i < high:
            return {(): 1, (i,): 1}
        base, delta = (upper, i - high) if i >= high else (lower, i - low)
        return evaluate((j + delta, eps) for j, eps in base)

    def evaluate(word):
        value = {(): 1}
        for i, sign in word:
            image = indexed(i)
            value = multiply(value, image if sign > 0 else inverse(image, p), p)
        return value

    assert evaluate(relator) == evaluate((i + 1, eps) for i, eps in relator) == {(): 1}
    images = []
    for i in range(low, high):
        image = indexed(i + 1).copy()
        update(image, (), -1, p)
        images.append(image)
    linear = [{k: v for k, v in image.items() if len(k) == 1} for image in images]
    blocks = [Block(linear, d, p) for d in range(1, 4)]
    assert all(len(block.pivots) == len(block.boundary) for block in blocks[:2])
    source = evaluate(row)
    residuals, samples = [], []
    for k in range(4):
        target = {((0,) * j): comb(k, j) % p for j in range(k + 1)}
        g = {(): 1}
        for d, block in enumerate(blocks, 1):
            difference = multiply(target, substitute(g, images, p, d), p, d)
            add_scaled(difference, multiply(g, source, p, d), -1, p)
            assert all(len(word) == d for word in difference)
            if d < 3:
                g.update(block.particular(difference))
            else:
                reduced = block.remainder(difference)[0]
                residuals.append(reduced)
                samples.append(g)

    coordinates = sorted({word for sample in residuals for word in sample})
    polynomials = {}
    for word in coordinates:
        values = [value.get(word, 0) for value in residuals]
        differences = []
        while values:
            differences.append(values[0])
            values = [(b - a) % p for a, b in zip(values, values[1:])]
        polynomials[word] = differences
    survivors = [
        k
        for k in range(p)
        if all(
            sum(coefficient * comb(k, j) for j, coefficient in enumerate(poly)) % p == 0
            for poly in polynomials.values()
        )
    ]
    # Retain one independently checkable left dual that by itself excludes
    # every residue, when such a coordinate is available.
    witness_coordinate = next(
        (word for word, poly in polynomials.items()
         if all(sum(c * comb(k, j) for j, c in enumerate(poly)) % p for k in range(p))),
        None,
    )
    witness = None
    if witness_coordinate is not None:
        witness = {
            "coordinate": witness_coordinate,
            "lower_conjugator_samples": [sorted(sample.items()) for sample in samples],
            "degree_three_dual": sorted(blocks[2].dual(witness_coordinate).items()),
        }
    return {
        "prime": p,
        "period": p,
        "graded_diagonal_quotient_sizes": [len(block.boundary) for block in blocks],
        "graded_cokernel_dimensions": [len(block.boundary) - len(block.pivots) for block in blocks],
        "residual_newton_coefficients": [
            [word, values] for word, values in sorted(polynomials.items())
        ],
        "surviving_count": len(survivors),
        "surviving_residues": survivors,
        "single_coordinate_witness": witness,
    }


if __name__ == "__main__":
    print(json.dumps([test(p) for p in PRIMES], indent=2))
