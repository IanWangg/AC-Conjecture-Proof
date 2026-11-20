"""Fast Fox character-cover filter for the second energy-20 donor."""

import json
import sys
from functools import lru_cache
from pathlib import Path

from elementary_verify import inverse
from round10_ac_proof_blocks import marked_group
from round12_ak3_reciprocal_charts import reverse_index
from stallings_search import reduce

DONOR = "xxyyxYYYxxY"
SOURCE = "xxxxyXXYY"
NAMES = "abcdefghij"
N = len(NAMES)
SIZE = 1 << N
SIGNS = tuple((-1) ** sum((i >> bit) & 1 for bit in range(N)) for i in range(SIZE))
IMAGES = tuple(NAMES[1:]) + ("igdbADFI",)
BACKWARD = ("CEHJhfca",) + tuple(NAMES[:-1])
IDENTITY = tuple(tuple(int(i == j) for j in range(N)) for i in range(N))
X = "UpU"
Y = "U" + X + X
MARKING = {"x": X, "X": inverse(X), "y": Y, "Y": inverse(Y)}


def substitute(word, images=IMAGES):
    return reduce(
        "".join(
            images[NAMES.index(c.lower())]
            if c.islower()
            else inverse(images[NAMES.index(c.lower())])
            for c in word
        )
    )


def exponent_bits(word):
    bits = 0
    for c in word:
        bits ^= 1 << NAMES.index(c.lower())
    return bits


def apply_binary(columns, x):
    result = 0
    for i, col in enumerate(columns):
        if (x >> i) & 1:
            result ^= col
    return result


def sign(left, right):
    return SIGNS[left & right]


def character_step(columns, x):
    return sum((1 << i) for i, col in enumerate(columns) if sign(col, x) < 0)


def schreier(word):
    height = 0
    factors = []
    for c in reduce("".join(MARKING[c] for c in word)):
        if c in "uU":
            height += 1 if c == "u" else -1
        else:
            factors.append((height, 1 if c == "p" else -1))
    return factors, height


def fox(word, character):
    prefix = 0
    vector = [0] * N
    for c in word:
        i = NAMES.index(c.lower())
        if c.isupper():
            prefix ^= 1 << i
            vector[i] -= sign(prefix, character)
        else:
            vector[i] += sign(prefix, character)
            prefix ^= 1 << i
    return vector


COLUMNS = tuple(map(exponent_bits, IMAGES))
INV_COLUMNS = tuple(map(exponent_bits, BACKWARD))


@lru_cache(None)
def parity_at(index):
    if index == -2:
        return 1 << (N - 1)
    if index > -2:
        return apply_binary(COLUMNS, parity_at(index - 1))
    return apply_binary(INV_COLUMNS, parity_at(index + 1))


def parity_of(factors):
    bits = 0
    for i, _ in factors:
        bits ^= parity_at(i)
    return bits


def span(matrix, rhs, modulus):
    rows = [[x % modulus for x in row] + [v % modulus] for row, v in zip(matrix, rhs)]
    pivots = []
    for column in range(len(matrix[0])):
        rank = len(pivots)
        pivot = next((j for j in range(rank, len(rows)) if rows[j][column]), None)
        if pivot is None:
            continue
        pivots.append(column)
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse_pivot = pow(rows[rank][column], -1, modulus)
        rows[rank] = [v * inverse_pivot % modulus for v in rows[rank]]
        for j in range(len(rows)):
            if j != rank and rows[j][column]:
                rows[j] = [
                    (a - rows[j][column] * b) % modulus
                    for a, b in zip(rows[j], rows[rank])
                ]
    assert all(any(row[:-1]) or not row[-1] for row in rows[len(pivots) :])
    particular = [0] * len(matrix[0])
    for j, i in enumerate(pivots):
        particular[i] = rows[j][-1]
    null = []
    for j in range(len(matrix[0])):
        if j not in pivots:
            vector = [0] * len(matrix[0])
            vector[j] = 1
            for k, i in enumerate(pivots):
                vector[i] = -rows[k][j] % modulus
            null.append(vector)
    return particular, null


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def character_orbits():
    pending = set(range(SIZE))
    groups = []
    while pending:
        first = min(pending)
        orbit, c = [], first
        while c in pending:
            pending.remove(c)
            orbit.append(c)
            c = character_step(COLUMNS, c)
        assert c == first
        groups.append(tuple(orbit))
    return groups


def right_product(row, last_column, scalar, p):
    return [scalar * x % p for x in row[1:]] + [scalar * dot(row, last_column) % p]


def orbit_transports(orbit, p, source_parity):
    return [(fox(IMAGES[-1], char), sign(char, source_parity)) for char in orbit]


def obstructions(orbit, p, source_parity):
    transports = orbit_transports(orbit, p, source_parity)
    matrix = IDENTITY
    for column, scalar in transports:
        matrix = [right_product(row, column, scalar, p) for row in matrix]
    # Left null vectors of I - K_0 ... K_(period-1).
    transposed = list(
        zip(
            *[[a - b for a, b in zip(row, mrow)] for row, mrow in zip(IDENTITY, matrix)]
        )
    )
    _, null = span(transposed, [0] * N, p)
    return transports, null


def shifted_vectors(orbit, lower, upper, p):
    period = len(orbit)
    unit = [0] * (N - 1) + [1]
    flows = {-2: [unit] * period}
    forward_columns = [fox(IMAGES[-1], c) for c in orbit]
    backward_columns = [fox(BACKWARD[0], c) for c in orbit]
    for h in range(-1, upper + 1):
        previous = flows[h - 1]
        next_vectors = []
        for i, col in enumerate(forward_columns):
            v = previous[(i + 1) % period]
            shifted = [0] + v[:-1]
            next_vectors.append([(x + v[-1] * y) % p for x, y in zip(shifted, col)])
        flows[h] = next_vectors
    for h in range(-3, lower - 1, -1):
        previous = flows[h + 1]
        next_vectors = []
        for i, col in enumerate(backward_columns):
            v = previous[(i - 1) % period]
            shifted = v[1:] + [0]
            next_vectors.append([(x + v[0] * y) % p for x, y in zip(shifted, col)])
        flows[h] = next_vectors
    return flows


def hadamard(values, p):
    width = 1
    while width < len(values):
        for block in range(0, len(values), 2 * width):
            for i in range(block, block + width):
                a, b = values[i], values[i + width]
                values[i], values[i + width] = (a + b) % p, (a - b) % p
        width *= 2
    return values


def coefficient_tables(orbit, transports, dual, flows, p):
    rows = []
    for column, scalar in transports:
        rows.append(dual)
        dual = right_product(dual, column, scalar, p)
    assert dual == rows[0]
    tables = {}
    for h, vectors in flows.items():
        expanded = [0] * SIZE
        for i, char in enumerate(orbit):
            expanded[char] = dot(rows[i], vectors[i]) % p
        tables[h] = hadamard(expanded, p)
    return tables


def traverse(factors, parity, weight, p):
    value = 0
    for h, s in factors:
        if s > 0:
            value += weight[h][parity]
            parity ^= parity_at(h)
        else:
            parity ^= parity_at(h)
            value -= weight[h][parity]
    return value % p


def archive_screen(archive):
    keys, _ = reverse_index(archive, 56)
    u, height = schreier(SOURCE)
    assert height == 1
    n_previous = len(keys)
    context = {}
    for k in sorted(keys):
        factors, height = schreier(k)
        if height == -1:
            factors = [(h, -s) for h, s in reversed(factors)]
            factors = [(h + 1, s) for h, s in factors]
        if abs(height) == 1:
            context[k] = factors
    total_height_one = len(context)
    image, _, _, _, _ = marked_group("SL2", 11, (0, 10, 1, 1), (0, 2, 5, 4))
    assert image(DONOR) == (10, 0, 0, 10)

    def squared_trace(word):
        a, _, _, d = image(word)
        return (a + d) ** 2 % 11

    target = squared_trace(SOURCE)
    context = {k: f for k, f in context.items() if squared_trace(k) == target}
    after_psl = len(context)
    lower = min(h for f in (u, *context.values()) for h, _ in f)
    upper = max(h for f in (u, *context.values()) for h, _ in f)
    u_parity = parity_of(u)
    inverse_I_minus_M = {g ^ apply_binary(COLUMNS, g): g for g in range(SIZE)}
    assert len(inverse_I_minus_M) == SIZE
    orbit_data = character_orbits()[1:]
    details = []
    for p, index in [(3, 0), (3, 2), (11, 1)]:
        orbit = orbit_data[index]
        trans, dual_basis = obstructions(orbit, p, u_parity)
        flows = shifted_vectors(orbit, lower, upper, p)
        before = len(context)
        for dual in dual_basis:
            weights = coefficient_tables(orbit, trans, dual, flows, p)
            expected = traverse(u, 0, weights, p)
            context = {
                word: f
                for word, f in context.items()
                if traverse(f, inverse_I_minus_M[u_parity ^ parity_of(f)], weights, p)
                == expected
            }
        details.append([p, orbit[0], len(orbit), len(dual_basis), before, len(context)])
    return {
        "all_keys": n_previous,
        "height_one": total_height_one,
        "trace_gate": after_psl,
        "details": details,
        "remaining": list(context),
    }


if __name__ == "__main__":
    print(json.dumps(archive_screen(Path(sys.argv[1])), indent=2))
