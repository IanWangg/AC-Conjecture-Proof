"""Replay unbounded frozen-row and short alternating-block obstructions."""

from itertools import permutations, product
import json
from math import gcd
from pathlib import Path

from round03_frozen_donors import cycle_type, evaluate, perm_inv, perm_mul
from stallings_search import apply

ROOT = Path(__file__).resolve().parents[1]
A = "XXYYxyyyxYY"
B = "XXYxyXyxYY"
C = "XXYYxyXyyxYY"


def vectors(word):
    return tuple(word.count(g) - word.count(g.upper()) for g in "xy")


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


def add(u, v, sign):
    return tuple(x + sign * y for x, y in zip(u, v))


def sl2(p):
    identity = (1, 0, 0, 1)

    def mul(a, b):
        return tuple(value % p for value in (
            a[0]*b[0] + a[1]*b[2], a[0]*b[1] + a[1]*b[3],
            a[2]*b[0] + a[3]*b[2], a[2]*b[1] + a[3]*b[3],
        ))

    def inv(a):
        assert (a[0]*a[3] - a[1]*a[2]) % p == 1
        return (a[3], -a[1] % p, -a[2] % p, a[0])

    return identity, mul, inv, lambda a: (a[0] + a[3]) % p


def symmetric(n):
    return tuple(range(1, n + 1)), perm_mul, perm_inv, cycle_type


def marked_group(kind, parameter, x, y):
    identity, mul, inv, invariant = (sl2 if kind == "SL2" else symmetric)(parameter)
    for marking in (x, y):
        if kind == "symmetric":
            assert tuple(sorted(marking)) == identity
        assert mul(marking, inv(marking)) == identity

    def image(word):
        return evaluate(word, (x, y), identity, mul, inv)

    return image, identity, mul, inv, invariant


def witness(donors, source, target, x, y):
    image, identity, _, inv, invariant = marked_group("symmetric", len(x), x, y)
    assert all(image(donor) == identity for donor in donors)
    old, new = image(source), image(target)
    assert invariant(old) == invariant(inv(old))
    assert invariant(new) == invariant(inv(new))
    assert invariant(old) != invariant(new)
    return {"donors_killed": donors, "source": source, "target": target,
            "degree": len(x), "marking": {"x": x, "y": y},
            "source_cycle_type": invariant(old), "target_cycle_type": invariant(new)}


def one_block_families():
    configurations = (
        (A, B, "X", "y", "SL2", 7, (0, 1, 6, 3), (0, 1, 6, 6)),
        (B, A, "x", "xy", "symmetric", 8, (1, 3, 2, 5, 4, 7, 8, 6), (6, 1, 4, 8, 3, 5, 7, 2)),
    )
    reports = []
    for donor, source, transverse, axial, kind, parameter, x, y in configurations:
        assert abs(det(vectors(transverse), vectors(axial))) == 1
        assert abs(det(vectors(transverse), vectors(donor))) == 1
        assert det(vectors(axial), vectors(donor)) == 0
        assert abs(det(vectors(source), vectors(donor))) == 1
        image, identity, mul, inv, invariant = marked_group(kind, parameter, x, y)
        assert image(donor) == identity
        old, u, v = map(image, (source, transverse, axial))
        assert invariant(inv(old)) == invariant(old)
        residues = []
        power = identity
        while True:
            value = mul(u, power)
            assert invariant(inv(value)) == invariant(value)
            residues.append(invariant(value))
            power = mul(power, v)
            if power == identity:
                break
        assert invariant(old) not in residues
        reports.append({"donor": donor, "source": source,
                        "primitive_family": [transverse, axial],
                        "group": kind, "group_parameter": parameter,
                        "marking": {"x": x, "y": y}, "source_invariant": invariant(old),
                        "power_period": len(residues), "primitive_residue_invariants": residues})
    return reports


# Assignments refer to literal rows of each saved rank-two certificate.
def e20_endpoints(name):
    record = json.loads((ROOT / "certificates" / f"round09_ac_proof_e20_{name}_splice.json").read_text())
    return tuple(record["start"]), tuple(record["target"])


P4 = ((1, 3, 4, 2), (2, 3, 4, 1))
P7 = ((1, 3, 4, 5, 6, 7, 2), (2, 4, 7, 1, 5, 3, 6))
TEMPLATES = {
    "wirtinger": {
        (0, (0, 1)): (1, ((1, 2, 4, 5, 3), (3, 4, 2, 5, 1))),
        (1, (0, 1)): (0, ((1, 2, 4, 5, 3), (3, 4, 2, 5, 1))),
    },
    "e20_vertex": {
        (0, (0, 1)): (1, P4),
        (0, (1, 0)): (1, P7),
        (1, (1, 0)): (0, ((2, 3, 4, 5, 1), (1, 3, 5, 4, 2))),
    },
    "e20_product": {(1, (0, 1)): (0, P4)},
}


def two_blocks(name, start, target):
    reports = []
    assert all(abs(det(*map(vectors, pair))) == 1 for pair in (start, target))
    for first, assignment in product(range(2), permutations(range(2))):
        second = 1 - first
        end = tuple(target[k] for k in assignment)
        blocks = ((start[second], start[first], end[first]), (end[first], start[second], end[second]))
        determinants = [[abs(det(vectors(d), vectors(a))), abs(det(vectors(d), vectors(b)))]
                        for d, a, b in blocks]
        report = {"receiving_order": [first, second], "target_assignment": assignment,
                  "abelian_quotient_absolute_determinants": determinants}
        if all(m == n for m, n in determinants):
            blocked, marking = TEMPLATES[name][first, assignment]
            report["first_decisive_quotient_check"] = blocked
            donor, a, b = blocks[blocked]
            report["separator"] = witness((donor,), a, b, *marking)
        else:
            assert (first, assignment) not in TEMPLATES[name]
        reports.append(report)
    return reports


def in_lattice(v, b, d):
    index = abs(det(b, d))
    if index:
        return det(v, d) % index == 0 and det(b, v) % index == 0
    # The two fixed rows have primitive exponent vectors.
    assert gcd(*b) == gcd(*d) == 1
    return det(b, v) == 0


def three_blocks(name, start, target):
    reports = []
    for outer, assignment in product(range(2), permutations(range(2))):
        inner = 1 - outer
        a, b = start[outer], start[inner]
        c, d = target[assignment[outer]], target[assignment[inner]]
        signs = [s for s in (1, -1) if in_lattice(add(vectors(a), vectors(c), -s), vectors(b), vectors(d))]
        report = {"receiving_order": [outer, inner, outer], "target_assignment": assignment,
                  "outer_quotient_abelian_index": abs(det(vectors(b), vectors(d))),
                  "permitted_relative_signs_in_abelianization": signs}
        if not signs:
            report["status"] = "excluded_in_abelianized_common_quotient"
        elif (name, outer, assignment) == ("e20_product", 1, (0, 1)):
            report["separator"] = witness((b, d), a, c, *P4)
            report["status"] = "excluded_in_finite_common_quotient"
        elif (name, outer, assignment) == ("wirtinger", 1, (0, 1)):
            assert b == d == A
            report["separator"] = witness((b,), a, c, *TEMPLATES[name][(1, (0, 1))][1])
            report["status"] = "excluded_in_finite_common_quotient"
        else:
            report["status"] = "unresolved"
        reports.append(report)
    return reports


def positive_control(start):
    # Three shears with coefficient two, without conjugations or inversions.
    moves = [{"op": "multiply", "i": i, "j": 1-i} for i in (0, 0, 1, 1, 0, 0)]
    state = start
    for move in moves:
        state = apply(state, move)
    coefficients = []
    for row in state:
        v = vectors(row)
        a, b = map(vectors, start)
        coefficients.append([det(v, b) // det(a, b), det(a, v) // det(a, b)])
    assert coefficients == [[5, 12], [2, 5]]
    return {"start": start, "endpoint": state, "endpoint_coefficients_in_starting_rows": coefficients,
            "moves": moves, "minimum_receiving_blocks": 3}


def main():
    endpoints = {"wirtinger": ((A, B), (A, C))}
    endpoints.update({f"e20_{name}": e20_endpoints(name) for name in ("vertex", "product")})
    comparisons = {name: {"start": start, "target": target,
                          "two_blocks": two_blocks(name, start, target),
                          "three_blocks": three_blocks(name, start, target)}
                   for name, (start, target) in endpoints.items()}
    print(json.dumps({"wirtinger_unbounded_primitive_exclusions": one_block_families(),
                      "marked_endpoint_comparisons": comparisons,
                      "three_block_positive_control": positive_control(endpoints["e20_vertex"][0])}, indent=2))


if __name__ == "__main__":
    main()
