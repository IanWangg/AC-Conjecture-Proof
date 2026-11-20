"""Independently enumerate the degree-three width-eight positive control."""

from functools import cache
import json
import sys

from round01_stable_disproof_search import AK3, MagnusQuotient, ONE


def check(native):
    graph = MagnusQuotient(2, 3)

    @cache
    def neighbors(state):
        result = {2: set(), 3: set(), 4: set()}
        for child in graph.neighbors(state, unordered=True):
            result[4 - child.count(ONE)].add(child)
        return result

    def path(start, occupations):
        layer = {start}
        for size in occupations:
            layer = {child for state in layer for child in neighbors(state)[size]}
        return layer

    start = tuple(sorted((ONE, ONE, *map(graph.evaluate, AK3))))
    finish = tuple(sorted((ONE, ONE, *graph.generators)))
    # The zero-idle (8,8) schedule has a long block with either three
    # or four four-active internal steps. An extra three-active step
    # can be before or after a block with three such steps.
    long_patterns = (
        (3, 3, 4, 4, 4, 4, 3, 2),
        (3, 4, 4, 4, 4, 3, 3, 2),
        (3, 4, 4, 4, 4, 4, 3, 2),
    )
    plain = tuple(path(endpoint, (3,) * 7 + (2,)) for endpoint in (start, finish))
    long = tuple(set.union(*(path(endpoint, pattern) for pattern in long_patterns))
                 for endpoint in (start, finish))
    boundary_matches = [len(plain[0] & long[1]), len(long[0] & plain[1]), len(long[0] & long[1])]
    assert native["degree"] == 3 and native["widths"] == [8, 8] and native["idle"] == [0, 0, 0]
    assert list(map(len, long)) == native["four_active_boundaries"]
    assert list(map(bool, boundary_matches)) == list(map(bool, native["hits"]))
    assert all(boundary_matches)
    return {
        "degree": 3,
        "widths": [8, 8],
        "occupations": long_patterns,
        "three_active_boundaries": list(map(len, plain)),
        "four_active_boundaries": list(map(len, long)),
        "boundary_matches": boundary_matches,
        "native_hits": native["hits"],
    }


if __name__ == "__main__":
    print(json.dumps(check(json.load(sys.stdin)), indent=2, sort_keys=True))
