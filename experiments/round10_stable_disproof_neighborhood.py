"""Lift a neighborhood of the verified degree-nine geodesic to degree ten."""

import argparse
from functools import cache
import json

from round01_stable_disproof_search import AK3, MagnusQuotient
from round06_magnus_corridor import corridor, encode
from round07_magnus_witness import independently_replay, successors
from round10_stable_disproof_saturate import corridor_data, saturation, widths


def pack(poly):
    return sum(1 << ((1 << len(term)) - 1 + encode(term, 2)) for term in poly)


def ball(start, radius, adjacency, allowed):
    depths = {start: 0}
    frontier = {start}
    for tick in range(1, radius + 1):
        frontier = {v for u in frontier for v in adjacency(u) if v in allowed and v not in depths}
        depths.update(dict.fromkeys(frontier, tick))
    return depths


def search(radius, budget):
    low = MagnusQuotient(2, 9)
    high = MagnusQuotient(2, 10)
    lower_layers, _ = saturation()
    assert widths(lower_layers) == corridor_data()
    scope = {tuple(sorted(map(pack, state))) for layer in lower_layers for state in layer}
    original_size = len(scope)

    @cache
    def low_neighbors(state):
        return set(low.neighbors(state, True))

    frontier = scope.copy()
    for _ in range(radius):
        frontier = set().union(*map(low_neighbors, frontier)) - scope
        scope.update(frontier)

    sides = budget // 2, budget - budget // 2
    lo_endpoints = (tuple(sorted(map(low.evaluate, AK3))), tuple(sorted(low.generators)))
    lo_depths = [ball(start, ticks, low_neighbors, scope) for start, ticks in zip(lo_endpoints, sides)]
    midpoint = set(lo_depths[0]).intersection(lo_depths[1])
    allowed = [corridor(low, depths, ticks, midpoint) for depths, ticks in zip(lo_depths, sides)]

    low_mask = (1 << ((1 << 10) - 1)) - 1

    def project(state):
        return tuple(sorted(component & low_mask for component in state))

    def lift(start, layers):
        result = [{start}]
        for layer in layers[1:]:
            result.append({
                candidate for parent in result[-1] for candidate in (parent, *high.neighbors(parent, True))
                if project(candidate) in layer
            })
        return result

    hi_endpoints = (tuple(sorted(map(high.evaluate, AK3))), tuple(sorted(high.generators)))
    forward, reverse = [lift(start, layers) for start, layers in zip(hi_endpoints, allowed)]
    common = forward[-1].intersection(reverse[-1])

    def trace(layers, selected):
        states = [selected]
        for layer in reversed(layers[:-1]):
            states.append(min(c for c in (states[-1], *high.neighbors(states[-1], True)) if c in layer))
        return states[::-1]

    moves = []
    if common:
        selected = min(common)
        states = trace(forward, selected) + trace(reverse, selected)[-2::-1]
        current = tuple(map(high.evaluate, AK3))
        for target in states[1:]:
            if tuple(sorted(current)) == target:
                continue
            current, move = next((s, m) for s, m in successors(high, current) if tuple(sorted(s)) == target)
            moves.append(move)
        assert set(current) == set(high.generators)
        endpoint = independently_replay(10, moves)
    else:
        endpoint = None

    return {
        "low_degree": 9, "high_degree": 10, "radius_from_any_degree_nine_geodesic": radius,
        "original_geodesic_vertices": original_size, "low_neighborhood_vertices": len(scope),
        "instruction_budget": budget, "low_midpoints": len(midpoint),
        "low_corridor_widths": list(map(widths, allowed)),
        "high_corridor_widths_before_final_trim": list(map(widths, (forward, reverse))),
        "high_midpoints": len(common), "exact_move_witness": moves, "replayed_basis_order": endpoint,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("radius", type=int)
    parser.add_argument("budget", type=int)
    args = parser.parse_args()
    if min(args.radius, args.budget) < 0:
        parser.error("radius and budget must be nonnegative")
    print(json.dumps(search(args.radius, args.budget), indent=2))
