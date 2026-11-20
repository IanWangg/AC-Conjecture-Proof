"""Compute the forced integral Fox flows of the remaining archive candidates."""

import json
import sys
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from pathlib import Path

from elementary_verify import inverse
from free_waypoint_search import canonical
from round12_ak3_reciprocal_charts import reverse_index
from round13_ak3_sign_cover import (
    BACKWARD,
    DONOR,
    IDENTITY,
    IMAGES,
    NAMES,
    SIZE,
    SOURCE,
    N,
    archive_screen,
    character_orbits,
    dot,
    fox,
    parity_at,
    parity_of,
    schreier,
    sign,
)
from stallings_search import reduce


def abelian(word):
    return tuple(word.count(c) - word.count(c.upper()) for c in NAMES)


Z_COLUMNS = tuple(map(abelian, IMAGES))
Z_INVERSE_COLUMNS = tuple(map(abelian, BACKWARD))


@lru_cache(None)
def exponent_at(index):
    unit = tuple(int(i == N - 1) for i in range(N))
    if index == -2:
        return unit
    columns = Z_COLUMNS if index > -2 else Z_INVERSE_COLUMNS
    incoming = exponent_at(index - 1 if index > -2 else index + 1)
    return tuple(dot(row, incoming) for row in zip(*columns))


def exponents(factors):
    return tuple(sum(k * exponent_at(h)[i] for h, k in factors) for i in range(N))


def normalized_factors(word):
    factors, height = schreier(word)
    assert abs(height) == 1
    if height == -1:
        return [(h + 1, -s) for h, s in reversed(factors)]
    return factors


def linear_solution(matrix, right):
    rows = [list(map(Fraction, (*m, r))) for m, r in zip(matrix, right)]
    for j in range(N):
        pivot = next(i for i in range(j, len(rows)) if rows[i][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scalar = rows[j][j]
        rows[j] = [a / scalar for a in rows[j]]
        for i, r in enumerate(rows):
            if i != j and r[j]:
                rows[i] = [a - r[j] * b for a, b in zip(r, rows[j])]
    assert all(not any(r) for r in rows[N:])
    return tuple(r[-1] for r in rows[:N])


def int_flow_tables(orbit, lower, upper):
    flows = {-2: [[0] * (N - 1) + [1]] * len(orbit)}
    period = len(orbit)
    forward_columns = [fox(IMAGES[-1], c) for c in orbit]
    backward_columns = [fox(BACKWARD[0], c) for c in orbit]
    for step, start, end, columns in (
        (1, -1, upper + 1, forward_columns),
        (-1, -3, lower - 1, backward_columns),
    ):
        for h in range(start, end, step):
            old = flows[h - step]
            nxt = []
            for i, col in enumerate(columns):
                v = old[(i + step) % period]
                if step == 1:
                    shifted, coefficient = [0] + v[:-1], v[-1]
                else:
                    shifted, coefficient = v[1:] + [0], v[0]
                nxt.append([x + coefficient * y for x, y in zip(shifted, col)])
            flows[h] = nxt
    return flows


def flow_from_factors(factors, orbit, tables):
    prefix = 0
    result = [[0] * N for _ in orbit]
    for h, k in factors:
        if k < 0:
            prefix ^= parity_at(h)
        for i, char in enumerate(orbit):
            coeff = k * sign(prefix, char)
            result[i] = [x + coeff * y for x, y in zip(result[i], tables[h][i])]
        if k > 0:
            prefix ^= parity_at(h)
    return result


def times(vector, col, scalar):
    return [scalar * x for x in vector[1:]] + [scalar * dot(vector, col)]


def apply_to_vector(vector, col, scalar):
    shifted = [0] + list(vector[:-1])
    return [scalar * (x + vector[-1] * y) for x, y in zip(shifted, col)]


def eval_orbit(u, v, orbit, tables, g):
    u_flow = flow_from_factors(u, orbit, tables)
    v_flow = flow_from_factors(v, orbit, tables)
    g_parity = sum((n % 2) << i for i, n in enumerate(g))
    u_parity = parity_of(u)
    const = [
        [x - sign(c, g_parity) * y for x, y in zip(a, b)]
        for c, a, b in zip(orbit, u_flow, v_flow)
    ]
    transports = [(fox(IMAGES[-1], c), sign(c, u_parity)) for c in orbit]
    closure = IDENTITY
    for col, scalar in transports:
        closure = [times(row, col, scalar) for row in closure]
    difference = [
        [a - b for a, b in zip(row, mrow)] for row, mrow in zip(IDENTITY, closure)
    ]
    zero = [0] * N
    for (col, scalar), b in zip(reversed(transports), reversed(const)):
        zero = [x + y for x, y in zip(b, apply_to_vector(zero, col, scalar))]
    chi = orbit[0]
    difference.append([sign(chi, 1 << i) - 1 for i in range(N)])
    zero.append(sign(chi, g_parity) - 1)
    initial = linear_solution(difference, zero)
    if any(x.denominator != 1 for x in initial):
        return None, tuple(map(str, initial))
    assigned = []
    current = list(map(int, initial))
    for (col, scalar), b in zip(reversed(transports), reversed(const)):
        current = [x + y for x, y in zip(b, apply_to_vector(current, col, scalar))]
        assigned.append(current)
    assert current == list(initial)
    return list(reversed(assigned)), None


def integer_hadamard(values):
    stride = 1
    while stride < len(values):
        for block in range(0, len(values), 2 * stride):
            for i in range(block, block + stride):
                a, b = values[i], values[i + stride]
                values[i], values[i + stride] = a + b, a - b
        stride *= 2
    return values


def classify(archive_words):
    u = normalized_factors(SOURCE)
    u_exp = exponents(u)
    linear = [
        [a - b for a, b in zip(row, col)] for row, col in zip(IDENTITY, zip(*Z_COLUMNS))
    ]
    u_ambient = "xxY"
    p_ambient = u_ambient + "xxxY"
    test_conjugators = (
        p_ambient,
        u_ambient + p_ambient + inverse(u_ambient),
        p_ambient + u_ambient + inverse(p_ambient) + inverse(u_ambient),
    )
    inputs = {word: normalized_factors(word) for word in archive_words}
    controls = {reduce(inverse(g) + SOURCE + g): g for g in test_conjugators}
    inputs.update({word: normalized_factors(word) for word in controls})
    lower = min(h for f in (u, *inputs.values()) for h, _ in f)
    upper = max(h for f in (u, *inputs.values()) for h, _ in f)
    orbits = character_orbits()[1:]
    tables = [int_flow_tables(orbit, lower, upper) for orbit in orbits]
    coverage = {}
    for word, v in inputs.items():
        rhs = [a - b for a, b in zip(u_exp, exponents(v))]
        g = linear_solution(linear, rhs)
        assert all(x.denominator == 1 for x in g)
        g = tuple(map(int, g))
        if word in controls:
            expected, h = schreier(controls[word])
            assert h == 0 and g == exponents(expected)
        evaluations = [None] * SIZE
        evaluations[0] = g
        for orbit, shifted in zip(orbits, tables):
            seen, failure = eval_orbit(u, v, orbit, shifted, g)
            if failure:
                coverage[word] = {
                    "status": "sign_eval_nonintegral",
                    "start_character": orbit[0],
                    "conjugator_abelianization": g,
                    "failed_values": failure,
                }
                break
            for c, values in zip(orbit, seen):
                evaluations[c] = values
        else:
            for coordinate, values in enumerate(zip(*evaluations)):
                nodes = integer_hadamard(list(values))
                bad = next((s for s, val in enumerate(nodes) if val % SIZE), None)
                if bad is not None:
                    coverage[word] = {
                        "status": "cover_nonintegral",
                        "basis_index": coordinate,
                        "parity_vertex": bad,
                        "scaled_value": nodes[bad],
                    }
                    break
            else:
                coverage[word] = {"status": "integral"}
        if word in controls:
            assert coverage[word]["status"] == "integral"
    return {
        "branches": coverage,
        "counts": dict(
            Counter(v["status"] for w, v in coverage.items() if w not in controls)
        ),
        "known_conjugate_controls": controls,
    }


def full_archive_test(archive):
    prefilter = archive_screen(archive)
    exact = classify(prefilter["remaining"])
    candidates = [
        word
        for word in prefilter["remaining"]
        if exact["branches"][word]["status"] == "integral"
    ]
    assert candidates == [canonical(SOURCE)]
    reverse, _ = reverse_index(archive, 56)
    companions = sorted(reverse[candidates[0]])
    r12_report = (
        Path(__file__).resolve().parents[1]
        / "results/round12_ac_proof_amalgam_archive.json"
    )
    former = json.loads(r12_report.read_text())
    assert former["fixed_donor"] == SOURCE and former["receiver"] == DONOR
    archive_digest = sha256(archive.read_bytes()).hexdigest()
    assert archive_digest == former["reverse_tsv_sha256"]
    allowed = sorted(row["reverse_donor"] for row in former["exact_conjugacy_hits"])
    assert len(companions) == 18 and not set(companions).intersection(allowed)
    return {
        "archive_tsv_sha256": archive_digest,
        "modular_prefilter": prefilter,
        "integer_cover": exact,
        "remaining_cyclic_word": candidates[0],
        "remaining_word_is_source_class": True,
        "archive_companions": companions,
        "compatible_receivers_in_other_quotient": allowed,
        "reciprocal_connections": 0,
    }


if __name__ == "__main__":
    print(json.dumps(full_archive_test(Path(sys.argv[1])), indent=2))
