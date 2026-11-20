#!/usr/bin/env python3
"""Exclude the finite Round 16 shift family by exact quotient tests."""

import json
from functools import cache
from itertools import product
from pathlib import Path

from round14_ac_proof_wirtinger_degree4 import Magnus
from round16_ac_proof_wirtinger_finite import stems


RESULTS = Path(__file__).resolve().parents[1] / "results"
TORUS_PRIMES = {
    2: (11, 29, 31, 61, 67),
    4: (19, 29, 31, 37, 43, 47, 61, 71, 83, 103),
}


def stem_coordinates(stem):
    """Compute exp_d(J) and the degree-two cd coefficient of J in (c,d)."""
    c_height = 0
    d_height = 0
    area = 0
    for c_power, d_power in stem:
        c_height += c_power
        d_height += d_power
        area += c_height * d_power
    return d_height, area


@cache
def hall_coordinates(side, trace, prime, first_power, conjugator_area):
    group = Magnus(prime)
    a, b = group.generators
    c, d = (a, b) if side == "upper" else (b, a)
    commutator = group.commutator(c, d)
    j = group.power(commutator, conjugator_area)
    w = group.combine(
        group.power(d, first_power),
        j,
        group.power(c, -2),
        group.inverse(j),
        group.power(d, trace - first_power),
    )
    base = (-2, trace) if side == "upper" else (trace, -2)
    leading = group.evaluate_powers((a, b), base)
    remainder = group.combine(group.inverse(leading), w)
    basis = group.commutators(a, b)[:3]
    r = remainder.get((0, 1), 0)
    higher = group.combine(group.power(basis[0], -r), remainder)
    s = -higher.get((0, 0, 1), 0) % prime
    t = higher.get((0, 1, 1), 0)
    reconstructed = group.evaluate_powers(basis, (r, s, t))
    assert all(not any(group.difference(remainder, reconstructed, n)) for n in range(1, 4))
    return r, s, t


def nilpotent_passes(side, trace, stem, first_power, conditions):
    d_height, area = stem_coordinates(stem)
    for prime, records in conditions:
        r, s, t = hall_coordinates(side, trace, prime, (first_power + d_height) % prime, area % prime)
        if records is None:
            if r != 1:
                return False
        else:
            s_multiplier, t_multiplier, required = records[r]["condition_for_s_t"]
            if (s_multiplier * s + t_multiplier * t - required) % prime:
                return False
    return True


@cache
def field_cycles(trace, prime):
    """List cycles of (C,D) -> (D,C^-2 D^trace) on the finite torus."""
    values = range(1, prime)
    def next_point(point):
        c, d = point
        return d, (pow(c, -2, prime) * pow(d, trace, prime)) % prime

    unseen = set(product(values, repeat=2))
    cycles = []
    while unseen:
        point = unseen.pop()
        path = [point]
        path_positions = {point: 0}
        while True:
            point = next_point(point)
            if point in path_positions:
                cycle = path[path_positions[point] :]
                first = cycle.index(min(cycle))
                cycles.append(tuple(cycle[first:] + cycle[:first]))
                break
            if point not in unseen:
                break
            unseen.remove(point)
            path_positions[point] = len(path)
            path.append(point)
    cycles.sort()
    for cycle in cycles:
        assert all(next_point(point) == cycle[(i + 1) % len(cycle)] for i, point in enumerate(cycle))
    return tuple(cycles)


def derivative_terms(stem):
    c_height = 0
    d_height = 0
    for c_power, d_power in stem:
        c_height += c_power
        yield c_height, min(d_height, d_height + d_power), d_power
        d_height += d_power


def cycle_witness(side, trace, stem, first_power, prime, cycles, powers):
    c_power = -2 if side == "upper" else 1
    d_power = first_power + (trace - 2 if side == "upper" else 2 - 2 * trace)
    terms = tuple(derivative_terms(stem))
    for cycle in cycles:
        coefficient_product = 1
        prefix_sum = 0
        for c, d in cycle:
            h = 1 + (d - 1) * sum(sign * powers[c][i] * powers[d][j] for i, j, sign in terms)
            g = powers[c][c_power] * (1 + c) * powers[d][d_power] * h
            prefix_sum = (prefix_sum + coefficient_product) % prime
            coefficient_product = coefficient_product * g % prime
            if not coefficient_product:
                break
        if coefficient_product == 1 and prefix_sum:
            return {"cycle_start": cycle[0], "cycle_length": len(cycle), "prefix_sum": prefix_sum}
    return None


def run():
    round14 = json.loads((RESULTS / "round14_ac_proof_wirtinger_degree4.json").read_text())
    cases = {}
    for trace, side in product((2, 4), ("upper", "lower")):
        conditions = [(5, None)] if trace == 2 else []
        conditions.extend(
            (row["modulus"], row["records"])
            for row in round14["degree_four_residues"]
            if row["trace"] == trace and row["singleton"] == side
        )
        assert len(conditions) == (3 if trace == 2 else 2)
        initial = list(product(stems(trace), range(-5, trace + 6)))
        survivors = [candidate for candidate in initial if nilpotent_passes(side, trace, *candidate, conditions)]
        phases = [{"initial_count": len(initial), "remaining_after_nilpotent_tests": len(survivors)}]
        for prime in TORUS_PRIMES[trace]:
            cycles = field_cycles(trace, prime)
            powers = {
                value: {exponent: pow(value, exponent, prime) for exponent in range(-30, 31)}
                for value in range(1, prime)
            }
            previous = survivors
            survivors = []
            excluded = []
            for stem, first_power in previous:
                witness = cycle_witness(side, trace, stem, first_power, prime, cycles, powers)
                if witness is None:
                    survivors.append((stem, first_power))
                else:
                    excluded.append({"stem": stem, "first_power": first_power, **witness})
            phase = {"prime": prime, "cycles": len(cycles), "remaining": len(survivors)}
            if not survivors:
                phase["final_exclusions"] = excluded
            phases.append(phase)
        assert not survivors
        cases[f"{side}, trace {trace}"] = phases
    return {"cases": cases, "survivors": 0}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
