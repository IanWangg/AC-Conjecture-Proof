"""Test primitive replacement slopes in finite class-two fibre quotients."""

from fractions import Fraction
from functools import lru_cache
from itertools import combinations
import json

from round15_ak3_torus_atlas import apply

SOURCE = ("xxyXYY", "xxxxYxYxYXY")
MARKINGS = (("xy", "y"), ("xYYYY", "YxYYYY"))
INVERSE_MARKINGS = (("xY", "y"), ("xxYxYxYxY", "xY"))


def indexed_word(word):
    height = 0
    letters = []
    for symbol in word:
        if symbol.lower() == "y":
            height += 1 if symbol == "y" else -1
        else:
            letters.append((height, 1 if symbol == "x" else -1))
    return tuple(letters), height


def inverse(word):
    return tuple((index, -sign) for index, sign in reversed(word))


def solve_letter(relator, target):
    indices = [i for i, (index, _) in enumerate(relator) if index == target]
    assert len(indices) == 1
    at = indices[0]
    remainder = inverse(relator[at+1:] + relator[:at])
    return remainder if relator[at][1] == 1 else inverse(remainder)


def abelian_images(relator, low, high):
    upper = solve_letter(relator, high)
    rank = high - low
    matrix = [[0] * rank for _ in range(rank)]
    for i in range(rank-1):
        matrix[i+1][i] = 1
    for index, sign in upper:
        matrix[index-low][-1] += sign
    return matrix


def inverse_integer(matrix):
    rank = len(matrix)
    rows = [[Fraction(x) for x in row] + [Fraction(i == j) for j in range(rank)]
            for i, row in enumerate(matrix)]
    for col in range(rank):
        pivot = next(i for i in range(col, rank) if rows[i][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        divisor = rows[col][col]
        rows[col] = [x/divisor for x in rows[col]]
        for i in range(rank):
            if i != col and (factor := rows[i][col]):
                rows[i] = [a-factor*b for a,b in zip(rows[i],rows[col])]
    assert all(x.denominator == 1 for row in rows for x in row)
    return [[int(x) for x in row[rank:]] for row in rows]


def product(matrix, vector):
    return tuple(sum(a*b for a,b in zip(row, vector)) for row in matrix)


class ClassTwo:
    def __init__(self, rank, prime):
        self.rank = rank
        self.central = prime
        self.linear = 2*prime if prime == 2 else prime
        self.pairs = tuple(combinations(range(rank), 2))
        self.identity = (0,)*rank, (0,)*len(self.pairs)

    def generator(self, index):
        return tuple(int(i == index) for i in range(self.rank)), self.identity[1]

    def multiply(self, left, right):
        v, z = left
        w, h = right
        return (
            tuple((a+b) % self.linear for a,b in zip(v,w)),
            tuple((a+b-v[j]*w[i]) % self.central for a,b,(i,j) in zip(z,h,self.pairs)),
        )

    def power(self, element, exponent):
        v, z = element
        pairs = exponent * (exponent-1) // 2
        return (
            tuple(exponent*a % self.linear for a in v),
            tuple((exponent*a-pairs*v[j]*v[i]) % self.central for a,(i,j) in zip(z,self.pairs)),
        )

    def transform(self, element, images, wedge):
        v, z = element
        result = self.identity
        for image, exponent in zip(images, v):
            result = self.multiply(result, self.power(image, exponent))
        return self.multiply(result, (self.identity[0], product(wedge, z)))


def central_system(matrix, targets, prime):
    rows = [[x % prime for x in base] + [t[i] % prime for t in targets]
            for i, base in enumerate(matrix)]
    width = len(matrix)
    top = 0
    for col in range(width):
        pivot = next((i for i in range(top, width) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[top], rows[pivot] = rows[pivot], rows[top]
        factor = pow(rows[top][col], -1, prime)
        rows[top] = [x*factor % prime for x in rows[top]]
        for i in range(top+1, width):
            if factor := rows[i][col]:
                rows[i] = [(a-factor*b) % prime for a,b in zip(rows[i],rows[top])]
        top += 1
    return top, [k for k in range(len(targets)) if all(row[width+k] == 0 for row in rows[top:])]


def finite_test(relator, receiver, prime):
    low = min(index for index, _ in relator)
    high = max(index for index, _ in relator)
    rank = high - low
    upper = solve_letter(relator, high)
    lower = solve_letter(relator, low)
    group = ClassTwo(rank, prime)
    matrix = abelian_images(relator, low, high)
    difference = [[int(i == j)-matrix[i][j] for j in range(rank)] for i in range(rank)]
    inverse_difference = inverse_integer(difference)
    wedge = [[matrix[i][k]*matrix[j][l] - matrix[j][k]*matrix[i][l]
              for k,l in group.pairs] for i,j in group.pairs]
    central_difference = [[int(i == j)-wedge[i][j] for j in range(len(wedge))]
                          for i in range(len(wedge))]

    @lru_cache(None)
    def letter(index):
        if low <= index < high:
            return group.generator(index-low)
        template, delta = (upper, index-high) if index >= high else (lower, index-low)
        return evaluate((j+delta, sign) for j, sign in template)

    def evaluate(word):
        result = group.identity
        for index, sign in word:
            result = group.multiply(result, group.power(letter(index), sign))
        return result

    assert evaluate(relator) == group.identity
    images = [letter(i+1) for i in range(low,high)]
    target = letter(0)
    relative = evaluate(receiver)
    residuals = []
    for k in range(group.linear):
        candidate = group.power(target, k)
        desired = tuple(a-b for a,b in zip(candidate[0],relative[0]))
        v = tuple(a % group.linear for a in product(inverse_difference, desired))
        g = v, group.identity[1]
        twisted = group.multiply(group.multiply(g,relative),
                                 group.power(group.transform(g,images,wedge),-1))
        assert twisted[0] == candidate[0]
        residuals.append(tuple(a-b for a,b in zip(candidate[1],twisted[1])))
    central_rank, survivors = central_system(central_difference, residuals, prime)
    return {"prime": prime, "slope_period": group.linear, "central_dimension": len(wedge),
            "linear_system_rank": central_rank, "surviving_residues": survivors}


def main():
    reports = []
    for index, (chart, back) in enumerate(zip(MARKINGS, INVERSE_MARKINGS)):
        assert tuple(apply(w, back) for w in chart) == ("x", "y")
        assert tuple(apply(w, chart) for w in back) == ("x", "y")
        donor, receiver = SOURCE[index], SOURCE[1-index]
        relator, donor_height = indexed_word(apply(donor,chart))
        row, receiver_height = indexed_word(apply(receiver,chart))
        assert donor_height == 0 and receiver_height == 1
        probes = [finite_test(relator,row,prime) for prime in (2,3,5,7,11,13,17,19)]
        reports.append({"donor": donor, "receiver": receiver,
                        "marking_to_kernel_and_height": chart,
                        "inverse_marking": back,
                        "indexed_donor": relator, "indexed_receiver": row,
                        "finite_class_two_tests": probes})
    print(json.dumps(reports,indent=2))


if __name__ == "__main__":
    main()
