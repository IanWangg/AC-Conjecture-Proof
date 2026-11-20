"""Audit the compact width-eight template filter and its last-equality tests."""

from collections import Counter
from functools import cache
import json
import sys

from round01_stable_disproof_search import MagnusQuotient, ONE
from round10_stable_disproof_neighborhood import pack
from round10_stable_disproof_saturate import corridor_data, saturation, widths
from round11_stable_disproof_symbolic4 import inverse, ordinary, pair_ball
from round12_stable_disproof_symbolic6 import cyclic_relation, degree_three_evaluations, rewrites


def degree_two_audit():
    group = MagnusQuotient(3, 2)
    elements = frontier = {ONE}
    while frontier:
        frontier = {group.multiply(a, x) for a in frontier for x in group.generators} - elements
        elements = elements | frontier

    def project(value):
        linear = (value >> group.offset[1]) & 7
        quadratics = (value >> (group.offset[2] + 6)) & 7
        return linear | (quadratics << 3)

    def product(a, b):
        return a ^ b ^ ((b & 3) << 3 if a & 4 else 0) ^ (32 if a & b & 4 else 0)

    compact = {value: project(value) for value in elements}
    for a, linear_a in compact.items():
        assert product(linear_a, project(group.inverse(a))) == 0
        for b, linear_b in compact.items():
            assert product(linear_a, linear_b) == compact[group.multiply(a, b)]
    return {"full_group_elements": len(elements), "compact_group_elements": len(set(compact.values())),
            "verified_products": len(elements) ** 2}


def read_templates(stream):
    result = {"symbolic_forward_layers": []}
    pending = []
    for line in stream:
        name, *items = line.split()
        if name == "R":
            result["compact_reverse_layers"] = list(map(int, items))
        elif name == "L":
            alpha, beta, *widths = map(int, items)
            result["symbolic_forward_layers"].append({"old_linear_parts": [alpha, beta], "widths_through_depth_five": widths[:6],
                                                      "sixth_step_edges": widths[6], "distinct_terminal_templates_so_far": widths[7]})
        elif name == "C":
            reached, literal, equality, exponent, residual = map(int, items)
            result.update({"formal_radius_seven_pairs": reached, "literal_replacement": literal, "last_equality_replacement": equality,
                           "exponent_obstruction_modulo_sixteen": exponent, "remaining_after_exponents": residual})
        elif name == "T":
            removed, donor, a, b = items
            pending.append((removed, donor, (a, b)))
        else:
            raise ValueError(f"unexpected record {name}")
    assert len(pending) == result["remaining_after_exponents"]
    assert len(result["symbolic_forward_layers"]) == 3
    assert sum(result[key] for key in ("literal_replacement", "last_equality_replacement", "exponent_obstruction_modulo_sixteen",
                                       "remaining_after_exponents")) == result["symbolic_forward_layers"][-1]["distinct_terminal_templates_so_far"]
    return result, pending


def covered_by_the_last_equality(pending):
    radius = pair_ball(6)
    _, _, solutions = degree_three_evaluations()

    @cache
    def within_radius_seven(pair):
        return pair in radius or any(tuple(sorted(neighbor)) in radius for neighbor in ordinary(pair))

    counts = Counter()
    residual = []
    for removed, donor, pair in pending:
        equality = cyclic_relation(removed + inverse(donor))
        if not solutions(equality):
            counts["degree_three_obstruction"] += 1
        elif any(within_radius_seven(tuple(sorted((a, b)))) for a in rewrites(pair[0], equality)
                 for b in rewrites(pair[1], equality)):
            counts["two_last_equality_rewrites_per_row"] += 1
        else:
            residual.append({"removed": removed, "signed_donor": donor, "remaining_pair": pair, "last_equality": equality})
    return {"counts": counts, "unresolved_templates": residual}


def strict_saving_windows():
    low = MagnusQuotient(2, 9)
    geodesics, _ = saturation()
    assert widths(geodesics) == corridor_data()
    idle = [{tuple(sorted((ONE, pack(a), pack(b)))) for a, b in layer} for layer in geodesics]

    @cache
    def active_neighbors(state):
        return {child for child in low.neighbors(state, True) if ONE not in child}

    def half(layer):
        for _ in range(4):
            layer = {child for state in layer for child in active_neighbors(state)}
        return layer

    records = []
    for t in range(len(idle) - 7):
        left = half(idle[t])
        right = half(idle[t + 7])
        count = len(left & right)
        assert count == 0
        records.append({"entry_tick": t, "exit_geodesic_tick": t + 7, "half_widths": [len(left), len(right)], "midpoints": count})
    return records


if __name__ == "__main__":
    first_comparison, pending = read_templates(sys.stdin)
    print(json.dumps({"arithmetic_audit": degree_two_audit(), "first_comparison": first_comparison,
                      "last_equality_tests": covered_by_the_last_equality(pending),
                      "strict_saving_geodesic_windows": strict_saving_windows()}, indent=2, sort_keys=True))
