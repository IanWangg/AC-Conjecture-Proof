"""Separate residual sheared contacts by Fox flow in free-by-cyclic quotients."""

import argparse
import json
from fractions import Fraction
from functools import cache
from hashlib import sha256
from itertools import product
from pathlib import Path

from elementary_verify import inverse
from round13_ak3_primitive_third import changed_basis, image
from stallings_search import reduce

MARKINGS = {
    "XXXXXXXXyxxxxxYXXYYxxxy": [(1, True), (1, True)],
    "XXXXXyxxYxYXYxxy": [(1, True)],
}


def rewrite(word):
    level = 0
    output = []
    for letter in word:
        if letter.lower() == "x":
            level += 1 if letter == "x" else -1
        else:
            entry = (level, 1 if letter == "y" else -1)
            if output and output[-1] == (entry[0], -entry[1]):
                output.pop()
            else:
                output.append(entry)
    return output, level


def substitute(word, names, images):
    marks = dict(zip(names + names.upper(), (*images, *map(inverse, images))))
    return reduce("".join(marks[c] for c in word))


def normal_form(donor, source, targets):
    def mark(word):
        for slot, negate in MARKINGS[donor]:
            word = image(word, changed_basis(slot, False, negate))
        return word

    indices, height = rewrite(mark(donor))
    assert height == 0
    low = min(i for i, _ in indices)
    high = max(i for i, _ in indices)
    names = "abcdefghijklmnopqrstuvwxyz"[: high - low]
    assert len(names) == high - low
    upper = [(j, sign) for j, (i, sign) in enumerate(indices) if i == high]
    assert len(upper) == 1
    cut, sign = upper[0]
    remainder = indices[cut + 1 :] + indices[:cut]
    upper_image = reduce(
        "".join(
            names[i - low] if s > 0 else names[i - low].upper() for i, s in remainder
        )
    )
    if sign > 0:
        upper_image = inverse(upper_image)
    images = (*names[1:], upper_image)
    lower = [
        (j, 1 if c.islower() else -1)
        for j, c in enumerate(upper_image)
        if c.lower() == "a"
    ]
    assert len(lower) == 1
    cut, sign = lower[0]
    shift = str.maketrans(
        names[1:] + names[1:].upper(), names[:-1] + names[:-1].upper()
    )
    down = (
        inverse(upper_image[:cut].translate(shift))
        + names[-1]
        + inverse(upper_image[cut + 1 :].translate(shift))
    )
    backward = (down if sign > 0 else inverse(down), *names[:-1])
    assert tuple(substitute(word, names, images) for word in backward) == tuple(names)
    assert tuple(substitute(word, names, backward) for word in images) == tuple(names)

    @cache
    def indexed(i):
        if i >= high:
            return substitute(indexed(i - 1), names, images)
        if i < low:
            return substitute(indexed(i + 1), names, backward)
        return names[i - low]

    def expand(terms):
        return reduce(
            "".join(
                indexed(i) if sign > 0 else inverse(indexed(i)) for i, sign in terms
            )
        )

    def normalized(word):
        word = mark(word)
        terms, height = rewrite(word)
        if height < 0:
            terms, height = rewrite(inverse(word))
        assert height == 1
        return expand(terms)

    assert expand(indices) == ""
    return (
        names,
        images,
        normalized(source),
        {word: normalized(word) for word in targets},
        indices,
    )


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def abel(word, names):
    return tuple(word.count(c) - word.count(c.upper()) for c in names)


def solve(matrix, target):
    rows = [list(map(Fraction, (*row, y))) for row, y in zip(matrix, target)]
    for j in range(len(rows)):
        pivot = next(i for i in range(j, len(rows)) if rows[i][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [x / scale for x in rows[j]]
        for i, row in enumerate(rows):
            if i != j and row[j]:
                rows[i] = [x - row[j] * y for x, y in zip(row, rows[j])]
    answer = [row[-1] for row in rows]
    assert all(x.denominator == 1 for x in answer)
    return tuple(map(int, answer))


def flow(word, names, character, roots):
    total = [0] * len(names)
    at = 0
    for c in word:
        i = names.index(c.lower())
        if c.isupper():
            at -= character[i]
            total[i] -= roots[at % len(roots)]
        else:
            total[i] += roots[at % len(roots)]
            at += character[i]
    return total


def orbits(columns, order):
    remaining = set(product(range(order), repeat=len(columns)))
    while remaining:
        current = first = min(remaining)
        orbit = []
        while current in remaining:
            orbit.append(current)
            remaining.remove(current)
            current = tuple(dot(col, current) % order for col in columns)
        assert current == first
        yield orbit


def inconsistency(matrix, p):
    n = len(matrix)
    rows = [row[:] + [int(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    variables = len(matrix[0]) - 1
    offset = 0
    for j in range(variables):
        pivot = next((i for i in range(offset, n) if rows[i][j] % p), None)
        if pivot is None:
            continue
        rows[offset], rows[pivot] = rows[pivot], rows[offset]
        at = rows[offset]
        at[:] = [x * pow(at[j], -1, p) % p for x in at]
        for i in range(offset + 1, n):
            factor = rows[i][j]
            if factor:
                rows[i] = [(x - factor * y) % p for x, y in zip(rows[i], at)]
        offset += 1
    for row in rows[offset:]:
        if not any(row[:variables]) and row[variables]:
            dual = row[variables + 1 :]
            value = tuple(dot(dual, col) % p for col in zip(*matrix))
            assert value == tuple(row[: variables + 1])
            return dual, value
    return None


def affine_system(names, images, source, target, g, orbit, roots, p):
    identity = [[int(i == j) for j in names] for i in names]
    transport, const = identity, [0] * len(names)
    modulo = len(roots)
    av = abel(source, names)
    for chi in reversed(orbit):
        u, v = (flow(word, names, chi, roots) for word in (source, target))
        scale = roots[dot(chi, av) % modulo]
        mark = roots[dot(chi, g) % modulo]
        local = [
            tuple(scale * x for x in row)
            for row in zip(*(flow(word, names, chi, roots) for word in images))
        ]
        const = [(x - mark * y + dot(row, const)) % p for x, y, row in zip(u, v, local)]
        transport = [[dot(row, col) % p for col in zip(*transport)] for row in local]
    chi = orbit[0]
    matrix = [
        [(a - b) % p for a, b in zip(row, end)] + [y]
        for row, end, y in zip(identity, transport, const)
    ]
    matrix.append(
        [(roots[c] - 1) % p for c in chi] + [(roots[dot(chi, g) % modulo] - 1) % p]
    )
    return matrix


def separate(donor, source, targets):
    names, images, u, candidates, indices = normal_form(donor, source, targets)
    columns = [abel(word, names) for word in images]
    linear = [
        [int(i == j) - column[i] for j, column in enumerate(columns)]
        for i in range(len(names))
    ]
    wanted = abel(u, names)
    g_values = {
        target: solve(linear, [a - b for a, b in zip(wanted, abel(word, names))])
        for target, word in candidates.items()
    }
    witnesses = {}
    prime, roots = 3, (1, 2)
    control_word = "abCd"
    control_target = reduce(
        inverse(control_word) + u + substitute(control_word, names, images)
    )
    control_g = abel(control_word, names)
    assert (
        solve(linear, [a - b for a, b in zip(wanted, abel(control_target, names))])
        == control_g
    )
    for orbit in orbits(columns, len(roots)):
        control_matrix = affine_system(
            names, images, u, control_target, control_g, orbit, roots, prime
        )
        control_values = flow(control_word, names, orbit[0], roots)
        assert all(
            (dot(row[:-1], control_values) - row[-1]) % prime == 0
            for row in control_matrix
        )
        for target in sorted(candidates.keys() - witnesses.keys()):
            g = g_values[target]
            matrix = affine_system(
                names, images, u, candidates[target], g, orbit, roots, prime
            )
            contradiction = inconsistency(matrix, prime)
            if contradiction is not None:
                dual, value = contradiction
                witnesses[target] = {
                    "modulus": prime,
                    "root": roots[1],
                    "order": len(roots),
                    "character": orbit[0],
                    "orbit_length": len(orbit),
                    "conjugator_abelianization": g,
                    "system": matrix,
                    "dual": dual,
                    "dual_product": value,
                }
        if len(witnesses) == len(targets):
            break
    return {
        "frozen_donor": donor,
        "source_row": source,
        "schreier_donor": indices,
        "kernel_generators": names,
        "shift_images": images,
        "kernel_source": u,
        "kernel_targets": candidates,
        "known_conjugate_control": control_target,
        "witnesses": witnesses,
        "unresolved": sorted(candidates.keys() - witnesses.keys()),
    }


def run(path):
    content = path.read_bytes()
    records = [
        separate(trial["frozen_donor"], trial["source_row"], trial["unresolved"])
        for trial in json.loads(content)["records"]
        if trial["unresolved"]
    ]
    return {
        "permutation_receipt_sha256": sha256(content).hexdigest(),
        "exactly_excluded": sum(len(record["witnesses"]) for record in records),
        "records": records,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("permutation_receipt", type=Path)
    print(json.dumps(run(parser.parse_args().permutation_receipt), indent=2))
