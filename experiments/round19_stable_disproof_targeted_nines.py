"""Independently lift the saved degree-six (9,9) cut survivors to degree seven."""

import argparse
from functools import lru_cache
import json
from pathlib import Path

from round01_stable_disproof_search import AK3, MagnusQuotient


class OneCoordinateDegreeSeven(MagnusQuotient):
    def __init__(self, coordinate):
        self.retained = ((1 << 127) - 1) | (1 << (127 + coordinate))
        super().__init__(2, 7)

    def multiply_uncached(self, left, right):
        return super().multiply_uncached(left, right) & self.retained


def slides(move, spare, donor):
    kind, receiver, operand = move
    other = 3 - spare - donor
    return (receiver == other and (kind != "multiply" or operand != spare)) or (receiver == donor and kind == "invert")


def moves(graph, state):
    inverse = tuple(graph.inverse(value) for value, _ in state)
    for i, (value, mark) in enumerate(state):
        before, after = state[:i], state[i + 1:]
        yield ("invert", i, -1), before + ((inverse[i], mark),) + after
        for positive, negative in graph.signed_generators:
            for prefix, suffix in ((positive, negative), (negative, positive)):
                changed = graph.multiply(graph.multiply(prefix, value), suffix)
                yield ("conjugate", i, -1), before + ((changed, mark),) + after
        for j, (donor, donor_mark) in enumerate(state):
            if j != i:
                for factor in (donor, inverse[j]):
                    changed = graph.multiply(value, factor)
                    yield ("multiply", i, j), before + ((changed, mark ^ donor_mark),) + after


def neighbors(graph):
    @lru_cache(maxsize=24000)
    def adjacent(state):
        return {tuple(sorted(child)) for _, child in moves(graph, state)}
    return adjacent


def births(graph, pair):
    for i, (value, mark) in enumerate(pair):
        for copy in (value, graph.inverse(value)):
            yield i, pair + ((copy, mark ^ 1),)


def depth_two(graph, pair):
    return {tuple(sorted(child)) for donor, state in births(graph, pair)
            for move, child in moves(graph, state) if not slides(move, 2, donor)}


def expand(graph, adjacent, pair):
    first = {tuple(sorted(state)) for _, state in births(graph, pair)}
    second = depth_two(graph, pair)
    third = {child for state in second for child in adjacent(state)}
    fourth = {child for state in third for child in adjacent(state)}
    return [set(), first, second, third, fourth]


def allowed_layers(graph, adjacent, front, target):
    rear = expand(graph, adjacent, target)
    cut = set()
    rear_four = set()
    for state in rear[4]:
        meeting = adjacent(state) & front[4]
        if meeting:
            cut.update(meeting)
            rear_four.add(state)
    if not cut:
        return {}

    forward_three = {child for state in cut for child in adjacent(state) if child in front[3]}
    forward_two = {child for state in forward_three for child in adjacent(state) if child in front[2]}
    rear_three = {child for state in rear_four for child in adjacent(state) if child in rear[3]}
    rear_two = {child for state in rear_three for child in adjacent(state) if child in rear[2]}
    return {2: forward_two, 3: forward_three, 4: cut, 5: rear_four, 6: rear_three, 7: rear_two, 8: rear[1]}


def high_lift(graph, adjacent, start, target, layers):
    if not layers:
        return [], set()
    mask = (1 << 127) - 1

    def project(state):
        return tuple(sorted((value & mask, mark) for value, mark in state))

    layer = {state for state in depth_two(graph, start) if project(state) in layers[2]}
    widths = [len(layer)]
    for tick in range(3, 8):
        layer = {child for state in layer for child in adjacent(state) if project(child) in layers[tick]}
        widths.append(len(layer))

    result = set()
    for state in layer:
        for move, child in moves(graph, state):
            if project(child) not in layers[8]:
                continue
            for i, (value, mark) in enumerate(child):
                for j, (donor, donor_mark) in enumerate(child):
                    if i == j or mark == donor_mark or slides(move, i, j):
                        continue
                    if value == donor or value == graph.inverse(donor):
                        pair = tuple(sorted(child[:i] + child[i + 1:]))
                        if project(pair) == target:
                            result.add(pair)
    return widths, result


def search(receipt, coordinate=None):
    low = MagnusQuotient(2, 6)
    high = MagnusQuotient(2, 7) if coordinate is None else OneCoordinateDegreeSeven(coordinate)
    low_edges, high_edges = neighbors(low), neighbors(high)

    def endpoints(graph):
        return tuple(sorted((graph.evaluate(word), 0) for word in AK3)), tuple(sorted((value, 0) for value in graph.generators))

    lower, upper = endpoints(low), endpoints(high)
    prefixes = [expand(low, low_edges, endpoint) for endpoint in lower]
    coordinates = receipt["pruned_degree_six"]["meeting_coordinates"]
    records = []
    for pair in coordinates:
        target = tuple(sorted((int(value, 16), mark) for value, mark in pair))
        stages = [allowed_layers(low, low_edges, prefix, target) for prefix in prefixes]
        lifts = [high_lift(high, high_edges, start, target, allowed) for start, allowed in zip(upper, stages)]
        meetings = len(lifts[0][1] & lifts[1][1])
        assert meetings == 0
        records.append({"degree_six_marked_pair": pair,
                        "degree_six_path_widths": [[len(s) for s in stage.values()] for stage in stages],
                        "degree_seven_prefix_widths": [row[0] for row in lifts],
                        "degree_seven_return_widths": [len(row[1]) for row in lifts],
                        "degree_seven_return_coordinates": [
                            [[(f"{value:064x}", mark) for value, mark in pair] for pair in sorted(row[1])]
                            for row in lifts],
                        "degree_seven_meetings": meetings})
    result = {"degree_six_cut_survivors": len(coordinates), "prefix_depths_at_streamed_cut": [4, 5], "lifts": records}
    if coordinate is not None:
        result["sole_degree_seven_coordinate"] = coordinate
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--top-coordinate", type=int, choices=range(128))
    args = parser.parse_args()
    print(json.dumps(search(json.loads(args.receipt.read_text()), args.top_coordinate), indent=2, sort_keys=True))
