"""Filter a bounded Magnus search through lower-degree midpoint paths."""

import argparse
from collections import Counter
from functools import lru_cache
from itertools import product
import json
import sys

from round01_stable_disproof_search import AK3, MagnusQuotient, ONE
from round05_stable_disproof_retractions import endpoints


def balls(group, start, radius):
    depths = {start: 0}
    frontier = {start}
    for i in range(1, radius + 1):
        frontier = {
            neighbor for state in frontier for neighbor in group.neighbors(state, True)
            if neighbor not in depths
        }
        depths.update(dict.fromkeys(frontier, i))
    return depths


def corridor(group, depths, radius, middle):
    layers = [middle]
    for depth in reversed(range(radius)):
        active = set()
        for state in layers[-1]:
            if depths[state] <= depth:
                active.add(state)
            active.update(
                neighbor for neighbor in group.neighbors(state, True)
                if depths.get(neighbor, radius + 1) <= depth
            )
        layers.append(active)
    return layers[::-1]


def encode(digits, base):
    value = 0
    for digit in digits:
        value = value * base + digit
    return value


def solve(padding, high_degree, low_degree, left_radius, right_radius, verbose=False):
    low = MagnusQuotient(2, low_degree)
    high = MagnusQuotient(padding + 2, high_degree)
    low_start, low_goal = endpoints(map(low.evaluate, AK3), low.generators, ONE, padding)
    high_start = tuple(sorted(tuple(map(high.evaluate, AK3)) + high.generators[2:]))
    high_goal = tuple(sorted(high.generators))
    mapping = tuple(
        (1 << (high.offset[degree] + encode(word, high.rank)),
         1 << (low.offset[degree] + encode(word, low.rank)))
        for degree in range(low_degree + 1) for word in product(range(2), repeat=degree)
    )
    low_mask = (1 << (low.offset[-1] + low.width[-1])) - 1

    @lru_cache(maxsize=100_000)
    def project_polynomial(value):
        if high.rank == low.rank:
            return value & low_mask
        return sum(low_bit for high_bit, low_bit in mapping if value & high_bit)

    def project(state):
        return tuple(sorted(map(project_polynomial, state)))

    assert project(high_start) == low_start and project(high_goal) == low_goal
    radii = [left_radius, right_radius]
    low_depths = []
    low_widths = []
    for start, radius in zip((low_start, low_goal), radii):
        depths = balls(low, start, radius)
        low_depths.append(depths)
        histogram = Counter(depths.values())
        width = [histogram.get(i, 0) for i in range(radius + 1)]
        low_widths.append(width)
        if verbose:
            print(f"Lower ball at radius {radius} has {len(depths)} states.", file=sys.stderr, flush=True)
    middle = set(low_depths[0]).intersection(low_depths[1])
    allowed = [corridor(low, depths, radius, middle) for depths, radius in zip(low_depths, radii)]
    del low_depths, depths

    def lift(start, layers):
        current = {start}
        widths = [1]
        for layer in layers[1:]:
            following = set()
            for state in current:
                if project(state) in layer:
                    following.add(state)
                following.update(
                    neighbor for neighbor in high.neighbors(state, True) if project(neighbor) in layer
                )
            widths.append(len(following))
            current = following
        return current, widths

    forward, forward_widths = lift(high_start, allowed[0])
    backward, backward_widths = lift(high_goal, allowed[1])
    return {
        "extra_rows": padding,
        "high_degree": high_degree,
        "low_degree": low_degree,
        "radii": radii,
        "low_ball_layers": low_widths,
        "low_midpoint_intersection": len(middle),
        "low_corridor_widths": [[len(layer) for layer in side] for side in allowed],
        "lifted_widths": [forward_widths, backward_widths],
        "high_midpoint_intersection": len(forward.intersection(backward)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("padding", "high_degree", "low_degree", "left_radius", "right_radius"):
        parser.add_argument(name, type=int)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.padding < 0 or not 1 <= args.low_degree <= args.high_degree or min(args.left_radius, args.right_radius) < 0:
        parser.error("require nonnegative padding and radii, and 1 <= low_degree <= high_degree")
    print(json.dumps(solve(**vars(args)), indent=2))


if __name__ == "__main__":
    main()
