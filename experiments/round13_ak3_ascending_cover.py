"""Exact odd-character Fox screens in the first energy-20 ascending HNN quotient."""

import json
import sys
from functools import lru_cache
from hashlib import sha256
from itertools import product
from pathlib import Path

from elementary_verify import inverse
from free_waypoint_search import canonical
from round10_ac_proof_blocks import marked_group
from round12_ak3_reciprocal_charts import reverse_index
from round12_ak3_torus_chart import DONOR as SOURCE
from round12_ak3_torus_chart import RECEIVER as FIXED
from round13_ak3_sign_cover import span

NAMES = "abc"
PHI = ("b", "c", "Caac")
IDENTITY = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


def factors(word):
    output = []
    height = 0
    for c in word:
        if c == "x":
            height -= 1
        elif c == "X":
            height += 1
        elif c == "y":
            height += 2
            output.append((height, 1))
        else:
            output.append((height, -1))
            height -= 2
    return output, height


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def add(a, b, p):
    return tuple((x + y) % p for x, y in zip(a, b))


def matrix_times(a, b, p):
    columns = tuple(zip(*b))
    return [[dot(row, col) % p for col in columns] for row in a]


def vector_times(a, v, p):
    return [dot(row, v) % p for row in a]


@lru_cache(None)
def vector_at(index, k):
    steps, i = divmod(index, 3)
    return tuple(pow(2, steps, k) if j == i else 0 for j in range(3))


def exponents(seq, k):
    v = (0, 0, 0)
    for index, sgn in seq:
        v = add(v, [sgn * x for x in vector_at(index, k)], k)
    return v


def fox(word, character, k, p, powers):
    vector = [0, 0, 0]
    weight = 0
    for c in word:
        i = NAMES.index(c.lower())
        if c.isupper():
            weight -= character[i]
            vector[i] -= powers[weight % k]
        else:
            vector[i] += powers[weight % k]
            weight += character[i]
    return [x % p for x in vector]


def orbit_records(k):
    pending = set(product(range(k), repeat=3))
    orbit_list = []
    while pending:
        root = min(pending)
        at = root
        cycle = []
        while at in pending:
            pending.remove(at)
            cycle.append(at)
            a, b, c = at
            at = (b, c, 2 * a % k)
        assert at == root
        orbit_list.append(cycle)
    return orbit_list


def matrix_inverse(matrix, p):
    columns = []
    for unit in IDENTITY:
        sol, null = span(matrix, unit, p)
        assert not null
        columns.append(sol)
    return list(zip(*columns))


def derivatives(orbit, k, p, powers, lo, hi):
    jac = [list(zip(*(fox(w, c, k, p, powers) for w in PHI))) for c in orbit]
    inverse_jac = [matrix_inverse(m, p) for m in jac]
    size = len(orbit)
    vectors = {0: [[1, 0, 0]] * size}
    for h in range(1, hi + 1):
        old = vectors[h - 1]
        vectors[h] = [vector_times(jac[i], old[(i + 1) % size], p) for i in range(size)]
    for h in range(-1, lo - 1, -1):
        old = vectors[h + 1]
        vectors[h] = [
            vector_times(inverse_jac[(i - 1) % size], old[(i - 1) % size], p)
            for i in range(size)
        ]
    return jac, vectors


def derivative_values(word, orbit, k, p, powers, vectors):
    prefix = (0, 0, 0)
    values = [[0, 0, 0] for c in orbit]
    for h, sgn in word:
        v = vector_at(h, k)
        if sgn < 0:
            prefix = add(prefix, [-a for a in v], k)
        for i, c in enumerate(orbit):
            coefficient = sgn * powers[dot(c, prefix) % k]
            values[i] = [
                (a + coefficient * b) % p for a, b in zip(values[i], vectors[h][i])
            ]
        if sgn > 0:
            prefix = add(prefix, v, k)
    return values


def normalize(word):
    seq, h = factors(word)
    if h == -1:
        seq, h = factors(inverse(word))
    assert h == 1
    return seq


def screened(keywords, k, p, root):
    assert all(a % 2 for a in (k, p))
    powers = [pow(root, i, p) for i in range(k)]
    assert len(set(powers)) == k and pow(root, k, p) == 1
    src = normalize(SOURCE)
    donor, h = factors(FIXED)
    assert h == 0 and exponents(donor, k) == (0, 0, 0)
    lo = min(h for f in (src, donor, *keywords.values()) for h, s in f)
    hi = max(h for f in (src, donor, *keywords.values()) for h, s in f)
    u = exponents(src, k)
    conjugators = {}
    for word, seq in keywords.items():
        a, b, c = add(u, [-a for a in exponents(seq, k)], k)
        ga = -(a + 2 * (b + c)) % k
        gb = (ga + b) % k
        gc = (gb + c) % k
        assert ((ga - 2 * gc) % k, (gb - ga) % k, (gc - gb) % k) == (a, b, c)
        conjugators[word] = (ga, gb, gc)
    hits = keywords.copy()
    orbit_counts = []
    for orbit in orbit_records(k):
        Jacobian, vecs = derivatives(orbit, k, p, powers, lo, hi)
        donor_values = derivative_values(donor, orbit, k, p, powers, vecs)
        assert not any(c for v in donor_values for c in v)
        trans = []
        for c, matrix in zip(orbit, Jacobian):
            scale = powers[dot(c, u) % k]
            trans.append([[scale * a % p for a in row] for row in matrix])
        M = IDENTITY
        for t in trans:
            M = matrix_times(M, t, p)
        left = list(zip(*[[a - b for a, b in zip(r, s)] for r, s in zip(IDENTITY, M)]))
        _, dual = span(left, [0, 0, 0], p)
        if not dual:
            continue
        source = derivative_values(src, orbit, k, p, powers, vecs)
        functionals = []
        for probe in dual:
            rows = []
            for t in trans:
                rows.append(probe)
                probe = [dot(probe, c) % p for c in zip(*t)]
            assert probe == rows[0]
            expected = sum(dot(row, v) for row, v in zip(rows, source)) % p
            functionals.append((rows, expected))
        before = len(hits)
        for word, seq in list(hits.items()):
            target = derivative_values(seq, orbit, k, p, powers, vecs)
            g = conjugators[word]
            scaled = [
                [powers[dot(c, g) % k] * a % p for a in v]
                for c, v in zip(orbit, target)
            ]
            if any(
                sum(dot(row, v) for row, v in zip(rows, scaled)) % p != expected
                for rows, expected in functionals
            ):
                del hits[word]
        if len(hits) != before:
            orbit_counts.append([orbit[0], len(orbit), len(dual), before, len(hits)])
    return hits, orbit_counts


def driver(archive):
    reverse, _ = reverse_index(Path(archive), 56)
    image, id_, _, _, cycle = marked_group(
        "symmetric", 8, (1, 3, 4, 5, 6, 7, 8, 2), (2, 1, 4, 6, 8, 7, 5, 3)
    )
    assert image(FIXED) == id_
    matched = cycle(image(SOURCE))
    tall = [w for w in sorted(reverse) if abs(factors(w)[1]) == 1]
    sources = {w: normalize(w) for w in tall if cycle(image(w)) == matched}
    counts = [len(reverse), len(tall), len(sources)]
    details = []
    controls = {
        inverse(g) + SOURCE + g: normalize(inverse(g) + SOURCE + g)
        for g in ("xxy", "x", "xyyX")
    }
    for k, p, root in ((3, 7, 2), (5, 11, 3), (7, 29, 16)):
        control_result, _ = screened(controls, k, p, root)
        assert control_result == controls
        filtered, counts_at_orbit = screened(sources, k, p, root)
        details.append([k, p, root, len(sources), len(filtered), counts_at_orbit])
        sources = filtered
        if len(sources) <= 1:
            break
    assert list(sources) == [canonical(SOURCE)]
    companions = sorted(reverse[canonical(SOURCE)])
    reference = (
        Path(__file__).resolve().parents[1] / "results/round12_ak3_torus_chart.json"
    )
    torus = json.loads(reference.read_text())
    archive_digest = sha256(Path(archive).read_bytes()).hexdigest()
    assert torus["reverse_tsv_sha256"] == archive_digest
    assert torus["fixed_donor"] == SOURCE and torus["receiver"] == FIXED
    allowed = sorted(row["donor_cyclic_key"] for row in torus["exact_conjugacy_hits"])
    assert len(allowed) == 7 and len(companions) == 97
    assert not set(allowed).intersection(companions)
    return {
        "archive_tsv_sha256": archive_digest,
        "prefilter": counts,
        "details": details,
        "positive_conjugacy_controls": list(controls),
        "remaining": list(sources),
        "remaining_word_is_source_class": True,
        "archive_companions": companions,
        "compatible_receivers_in_other_quotient": allowed,
        "reciprocal_connections": 0,
    }


if __name__ == "__main__":
    print(json.dumps(driver(sys.argv[1]), indent=2))
