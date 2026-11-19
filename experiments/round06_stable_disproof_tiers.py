"""Exhaust a bounded Magnus path by successively tightening exact corridors."""

import argparse
from collections import Counter
from functools import lru_cache
from itertools import product
import json
import sys

from round01_magnus_distance import (
    ONE as SET_ONE,
    evaluate as set_evaluate,
    generator as set_generator,
    inverse as set_inverse,
    multiply as set_multiply,
)
from round01_stable_disproof_search import AK3, MagnusQuotient, ONE
from round06_magnus_corridor import balls, corridor, encode


class SupportQuotient(MagnusQuotient):
    """Keep only monomials involving at most two marked letters."""

    def __init__(self, rank, degree):
        total = sum(rank ** length for length in range(degree + 1))
        bits = bytearray((total + 7) // 8)
        index = 0
        for length in range(degree + 1):
            for term in product(range(rank), repeat=length):
                if len(set(term)) <= 2:
                    bits[index // 8] |= 1 << (index % 8)
                index += 1
        self.support_mask = int.from_bytes(bits, "little")
        super().__init__(rank, degree)

    def multiply_uncached(self, lhs, rhs):
        return super().multiply_uncached(lhs, rhs) & self.support_mask


def endpoints(group, padding, ordered):
    auxiliary = group.generators[2:] or (ONE,) * padding
    start = (*map(group.evaluate, AK3), *auxiliary)
    target = (*group.generators[:2], *auxiliary)
    if ordered:
        return start, target
    return tuple(sorted(start)), tuple(sorted(target))


def projection(high, low):
    mask = (1 << (low.offset[-1] + low.width[-1])) - 1
    mask = getattr(low, "support_mask", mask)
    mapping = tuple(
        (1 << (high.offset[degree] + encode(word, high.rank)),
         1 << (low.offset[degree] + encode(word, low.rank)))
        for degree in range(low.degree + 1)
        for word in product(range(low.rank), repeat=degree)
    )

    @lru_cache(maxsize=100_000)
    def row(value):
        if high.rank == low.rank:
            return value & mask
        return sum(target_bit for source_bit, target_bit in mapping if value & source_bit)

    def state(rows):
        return tuple(map(row, rows))

    return state


def half_layers(graph, start, allowed, project, unordered, screen=None):
    states = [{start}]
    menu = tuple(instruction_labels(len(start), graph.rank, not unordered)) if screen else ()
    for layer in allowed[1:]:
        following = set()

        @lru_cache(maxsize=100_000)
        def compatible(projected):
            return tuple(move for move in menu if tuple(sorted(apply(screen, projected, move))) in layer)

        for parent in states[-1]:
            projected = project(parent)
            if tuple(sorted(projected)) in layer:
                following.add(parent)
            if screen:
                for move in compatible(projected):
                    child = apply(graph, parent, move)
                    following.add(tuple(sorted(child)) if unordered else child)
            else:
                following.update(
                    child for child in graph.neighbors(parent, unordered) if tuple(sorted(project(child))) in layer
                )
        states.append(following)
    return states


def trim(graph, layers, midpoint):
    trimmed = [midpoint]
    for layer in reversed(layers[:-1]):
        active = set()
        for state in trimmed[-1]:
            if state in layer:
                active.add(state)
            active.update(neighbor for neighbor in graph.neighbors(state, True) if neighbor in layer)
        trimmed.append(active)
    return trimmed[::-1]


def trace(graph, layers, finish, unordered):
    steps = [finish]
    for layer in reversed(layers[:-1]):
        if steps[-1] not in layer:
            steps.append(min(state for state in graph.neighbors(steps[-1], unordered) if state in layer))
    return steps[::-1]


def instruction_labels(row_count, rank, ordered):
    for i in range(row_count):
        yield ("invert", i)
        for j in range(row_count):
            if i != j:
                for sign in (1, -1):
                    yield ("multiply", i, j, sign)
            if ordered and i < j:
                yield ("swap", i, j)
        for j in range(rank):
            for sign in (1, -1):
                yield ("conjugate", i, j, sign)


def apply(graph, rows, move):
    kind, i, *operands = move
    row = rows[i]
    if kind == "invert":
        result = graph.inverse(row)
    elif kind == "multiply":
        j, sign = operands
        donor = rows[j] if sign == 1 else graph.inverse(rows[j])
        result = graph.multiply(row, donor)
    elif kind == "swap":
        (j,) = operands
        return rows[:i] + (rows[j],) + rows[i + 1:j] + (row,) + rows[j + 1:]
    else:
        j, sign = operands
        if j >= graph.rank:
            return rows
        pair = graph.signed_generators[j]
        a, b = pair if sign == 1 else pair[::-1]
        result = graph.multiply(graph.multiply(a, row), b)
    return rows[:i] + (result,) + rows[i + 1:]


def ledger(graph, start, states, ordered):
    moves = []
    current = start
    for state in states[1:]:
        for instruction in instruction_labels(len(current), graph.rank, ordered):
            next_rows = apply(graph, current, instruction)
            if (next_rows if ordered else tuple(sorted(next_rows))) == state:
                moves.append(instruction)
                current = next_rows
                break
        else:
            raise AssertionError("cannot replay a reconstructed edge")
    return moves


def independent_replay(degree, padding, moves, erased=False):
    rank = 2 if erased else padding + 2
    generators = tuple(set_generator(i) for i in range(rank))
    auxiliary = (SET_ONE,) * padding if erased else generators[2:]
    rows = [*(set_evaluate(word, degree) for word in AK3), *auxiliary]
    for kind, i, *operands in moves:
        if kind == "invert":
            rows[i] = set_inverse(rows[i], degree)
        elif kind == "swap":
            (j,) = operands
            assert i != j
            rows[i], rows[j] = rows[j], rows[i]
        elif kind == "multiply":
            j, sign = operands
            assert i != j and sign in (-1, 1)
            donor = rows[j] if sign == 1 else set_inverse(rows[j], degree)
            rows[i] = set_multiply(rows[i], donor, degree)
        elif kind == "conjugate":
            j, sign = operands
            assert sign in (-1, 1)
            letter = generators[j]
            if sign == -1:
                letter = set_inverse(letter, degree)
            rows[i] = set_multiply(set_multiply(letter, rows[i], degree), set_inverse(letter, degree), degree)
        else:
            raise AssertionError(kind)
    basis = (*generators[:2], *auxiliary)
    slots = list(range(len(basis)))
    labels = []
    for row in rows:
        index = next(i for i in slots if basis[i] == row)
        slots.remove(index)
        labels.append(index)
    return labels


def search(padding, degrees, radii, ordered=False, retracted=False,
           progress=False, support_two=False, screen_instructions=False):
    low = MagnusQuotient(2, degrees[0])
    low_ends = endpoints(low, padding, False)
    depths = []
    ball_layers = []
    for start, radius in zip(low_ends, radii):
        d = balls(low, start, radius)
        depths.append(d)
        counts = Counter(d.values())
        ball_layers.append([counts[i] for i in range(radius + 1)])
        if progress:
            print(f"degree {low.degree} radius {radius}: {len(d)} ball states", file=sys.stderr, flush=True)
    midpoint = set(depths[0]).intersection(depths[1])
    allowed = [corridor(low, d, r, midpoint) for d, r in zip(depths, radii)]
    del depths, d
    statistics = [{
        "degree": low.degree,
        "rank": low.rank,
        "ball_layers": ball_layers,
        "midpoint_count": len(midpoint),
        "corridor_layers": [list(map(len, side)) for side in allowed],
    }]
    moves = None
    endpoint_order = None
    remaining = [(degree, 2, False) for degree in degrees[1:-1]]
    if support_two:
        remaining.append((degrees[-1], padding + 2, True))
    remaining.append((degrees[-1], 2 if retracted else padding + 2, False))
    for tier, (degree, rank, limited_support) in enumerate(remaining):
        if not midpoint:
            break
        final = tier == len(remaining) - 1
        high = (SupportQuotient if limited_support else MagnusQuotient)(rank, degree)
        use_order = final and ordered
        ends = endpoints(high, padding, use_order)
        project = projection(high, low)
        assert tuple(tuple(sorted(project(end))) for end in ends) == low_ends
        halves = [
            half_layers(high, end, side, project, not use_order, low if screen_instructions else None)
            for end, side in zip(ends, allowed)
        ]
        midpoint = halves[0][-1].intersection(halves[1][-1])
        stage = {
            "degree": degree,
            "rank": high.rank,
            "lift_layers": [list(map(len, side)) for side in halves],
            "midpoint_count": len(midpoint),
        }
        if limited_support:
            stage["monomial_support_cap"] = 2
        statistics.append(stage)
        if progress:
            print(f"degree {degree} rank {high.rank}: {len(midpoint)} surviving midpoints", file=sys.stderr, flush=True)
        if final and midpoint:
            finish = min(midpoint)
            left, right = (trace(high, side, finish, not use_order) for side in halves)
            path = left + right[-2::-1]
            moves = ledger(high, endpoints(high, padding, True)[0], path, use_order)
            endpoint_order = independent_replay(degree, padding, moves, erased=retracted)
            assert len(moves) <= sum(radii)
            if ordered:
                assert endpoint_order == list(range(2 + padding))
        if not final:
            allowed = [trim(high, side, midpoint) for side in halves]
            stage["corridor_layers"] = [list(map(len, side)) for side in allowed]
            low, low_ends = high, ends
        del halves
    return {
        "padding": padding,
        "degrees": degrees,
        "radii": radii,
        "ordered": ordered,
        "retracted": retracted,
        "stages": statistics,
        "path_exists": bool(midpoint),
        "certificate": moves,
        "endpoint_basis_order": endpoint_order,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("padding", type=int)
    parser.add_argument("left_radius", type=int)
    parser.add_argument("right_radius", type=int)
    parser.add_argument("degrees", type=int, nargs="+")
    parser.add_argument("--ordered", action="store_true")
    parser.add_argument("--retracted", action="store_true")
    parser.add_argument("--support-two", action="store_true")
    parser.add_argument("--screen-instructions", action="store_true")
    parser.add_argument("--progress", action="store_true")
    a = parser.parse_args()
    if min(a.padding, a.left_radius, a.right_radius) < 0 or len(a.degrees) < 2 or a.degrees[0] < 1:
        parser.error("provide nonnegative counts and at least two positive degrees")
    if any(x >= y for x, y in zip(a.degrees, a.degrees[1:])):
        parser.error("degrees must increase strictly")
    if a.support_two and (a.padding == 0 or a.retracted):
        parser.error("--support-two requires positive padding and a full-rank final tier")
    print(json.dumps(search(a.padding, a.degrees, [a.left_radius, a.right_radius],
                            a.ordered, a.retracted, a.progress, a.support_two,
                            a.screen_instructions), indent=2))


if __name__ == "__main__":
    main()
