"""Verify finite witnesses against completing either single frozen-donor phase."""

import hashlib
import json
from pathlib import Path

from elementary_verify import replay

SOURCE = Path(__file__).resolve().parents[1] / "certificates/optimized_first_order_strict.json"
MODULUS = 11


def evaluate(word, marks, identity, mul, inv):
    images = dict(zip("xy", marks))
    images.update({"X": inv(marks[0]), "Y": inv(marks[1])})
    result = identity
    for letter in word:
        result = mul(result, images[letter])
    return result


def matrix_mul(a, b):
    return tuple(entry % MODULUS for entry in (
        a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3],
        a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
    ))


def matrix_inv(m):
    assert (m[0] * m[3] - m[1] * m[2]) % MODULUS == 1
    return m[3], -m[1] % MODULUS, -m[2] % MODULUS, m[0]


def matrix_trace(m):
    return (m[0] + m[3]) % MODULUS


def perm_mul(a, b):
    return tuple(a[i - 1] for i in b)


def perm_inv(a):
    return tuple(a.index(i) + 1 for i in range(1, len(a) + 1))


def cycle_type(p):
    unseen = set(range(1, len(p) + 1))
    lengths = []
    while unseen:
        start = at = min(unseen)
        length = 0
        while True:
            unseen.remove(at)
            length += 1
            at = p[at - 1]
            if at == start:
                break
        lengths.append(length)
    return tuple(sorted(lengths))


def census(rows, receiver, marks, identity, mul, inv, invariant, name):
    donor = 1 - receiver
    assert mul(*marks) != mul(*reversed(marks))
    images = tuple(evaluate(row, marks, identity, mul, inv) for row in rows)
    assert images[donor] == identity
    actual = invariant(images[receiver])
    assert invariant(inv(images[receiver])) == actual
    allowed = []
    power = identity
    while True:
        allowed.append(invariant(mul(marks[receiver], power)))
        power = mul(power, marks[donor])
        if power == identity:
            break
    assert actual not in allowed
    return {
        "group": name,
        "receiver": "UV"[receiver],
        "donor": "UV"[donor],
        "generator_images": dict(zip("xy", marks)),
        "endpoint_images": dict(zip("UV", images)),
        "receiver_invariant": actual,
        "candidate_invariants_in_donor_generator_power_order": allowed,
    }


def main():
    original = SOURCE.read_bytes()
    prefix = replay(json.loads(original))
    rows = prefix["endpoint"]
    assert [
        (w.count("x") - w.count("X"), w.count("y") - w.count("Y")) for w in rows
    ] == [(1, 0), (0, 1)]
    matrix = census(
        rows, 0, ((0, 1, 10, 5), (0, 2, 5, 1)), (1, 0, 0, 1),
        matrix_mul, matrix_inv, matrix_trace, "SL(2,11)",
    )
    permutation = census(
        rows, 1, ((1, 2, 4, 5, 3), (3, 4, 2, 5, 1)), (1, 2, 3, 4, 5),
        perm_mul, perm_inv, cycle_type, "S5",
    )
    print(json.dumps({
        "prefix_sha256": hashlib.sha256(original).hexdigest(),
        "prefix_moves": prefix["moves"],
        "free_endpoint_lengths": list(map(len, rows)),
        "witnesses": [matrix, permutation],
    }, indent=2))


if __name__ == "__main__":
    main()
