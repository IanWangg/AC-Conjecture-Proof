"""Verify two frozen-donor obstructions at the marked cap-29 waypoint."""

from itertools import product
import json
from math import lcm
from pathlib import Path

from elementary_verify import replay
from round03_frozen_donors import evaluate

PATH = Path(__file__).resolve().parents[1] / "certificates/round06_ak3_marked_waypoint29.json"
MODULUS = 7
ZERO = (0, 0, 0)
A, B, C = (1, 0, 0), (0, 1, 0), (0, 0, 1)
W = (3, 6, 0)


def matrix_product(a, b):
    return tuple(entry % MODULUS for entry in (
        a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3],
        a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
    ))


def matrix_inverse(a):
    assert (a[0] * a[3] - a[1] * a[2]) % MODULUS == 1
    return a[3], -a[1] % MODULUS, -a[2] % MODULUS, a[0]


def traces(rows):
    marks = (0, 6, 1, 6), (0, 1, 6, 4)
    identity = (1, 0, 0, 1)
    x, y = marks
    assert matrix_product(x, y) != matrix_product(y, x)

    def trace(a):
        return (a[0] + a[3]) % MODULUS

    receiver, donor = [evaluate(row, marks, identity, matrix_product, matrix_inverse) for row in rows]
    assert donor == identity
    allowed = []
    power = identity
    while True:
        allowed.append(trace(matrix_product(y, power)))
        power = matrix_product(power, x)
        if power == identity:
            break
    assert trace(receiver) == trace(matrix_inverse(receiver)) and trace(receiver) not in allowed
    return {
        "marking": marks, "endpoint_images": [receiver, donor],
        "receiver_trace": trace(receiver), "candidate_traces": allowed,
    }


def heisenberg_product(g, h):
    a, b, c = g
    d, e, f = h
    return (a + d) % MODULUS, (b + e) % MODULUS, (c + f - b * d) % MODULUS


def power(g, n):
    a, b, c = g
    return a * n % MODULUS, b * n % MODULUS, (c * n - a * b * n * (n - 1) // 2) % MODULUS


def phi(g):
    a, b, c = g
    return heisenberg_product(heisenberg_product(power(W, a), power(A, b)), power(C, c))


def cycling(h):
    values = [h]
    while phi(values[-1]) != h:
        values.append(phi(values[-1]))
    return values


def heisenberg_witness(rows):
    group = list(product(range(MODULUS), repeat=3))
    assert len({phi(g) for g in group}) == len(group)
    from_a, from_b = cycling(A), cycling(B)
    return_period = lcm(len(from_a), len(from_b))
    actions = {h: cycling(h) for h in group}
    assert all(return_period % len(cycle) == 0 for cycle in actions.values())

    def action(h, k):
        return actions[h][k % len(actions[h])]

    def multiply(left, right):
        k, u = left
        l, v = right
        return (k + l) % return_period, heisenberg_product(action(u, -l), v)

    def inverse(state):
        k, u = state
        return -k % return_period, action(power(u, -1), k)

    identity = (0, ZERO)
    marks = (-1 % return_period, ZERO), (0, A)
    assert multiply(*marks) != multiply(*reversed(marks))
    donor, receiver = [evaluate(row, marks, identity, multiply, inverse) for row in rows]
    assert donor == identity and receiver == (1, (4, 5, 6))
    candidates = [(1, power(A, j)) for j in range(MODULUS)]
    conjugators = list(product(range(return_period), group))
    for candidate in candidates:
        orbit = {multiply(multiply(h, candidate), inverse(h)) for h in conjugators}
        assert receiver not in orbit
    differences = []
    for j in range(MODULUS):
        g = ((j - 2) % MODULUS, -j % MODULUS, 0)
        twist = heisenberg_product(heisenberg_product(g, power(A, j)), power(phi(g), -1))
        difference = (twist[2] - receiver[1][2]) % MODULUS
        assert twist[:2] == receiver[1][:2]
        assert difference == ((j * j + 3 * j + 8) * pow(2, -1, MODULUS)) % MODULUS != 0
        differences.append(difference)
    return {
        "marking": marks, "endpoint_images": [donor, receiver],
        "action_order": return_period, "finite_group_order": len(conjugators),
        "candidate_central_differences": differences,
    }


def main():
    checked = replay(json.loads(PATH.read_text()))
    rows = checked["endpoint"]
    assert [[w.count(g) - w.count(g.upper()) for g in "xy"] for w in rows] == [[0, -1], [-1, 0]]
    print(json.dumps({
        "strict_prefix_moves": checked["moves"], "free_endpoint": rows,
        "short_donor_SL2_F7": traces(rows), "long_donor_heisenberg_semidirect": heisenberg_witness(rows),
    }, indent=2))


if __name__ == "__main__":
    main()
