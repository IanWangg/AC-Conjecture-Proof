"""Cross-check the two-block midpoint language by explicit occupation schedules."""

from collections import Counter
from itertools import product
import json


def explicit_language():
    widths = {}
    for first in range(5, 10):
        for second in range(5, 15 - first):
            spare = 14 - first - second
            for extra in product(range(spare + 1), repeat=5):
                if sum(extra) != spare:
                    continue
                idle_before, lead, bridge, trail, idle_after = extra
                word = ((2,) * (1 + idle_before) + (3,) * (1 + lead) + (4,) * (first - 1)
                        + (3,) * (1 + bridge) + (4,) * (second - 1)
                        + (3,) * (1 + trail) + (2,) * (1 + idle_after))
                assert len(word) == 17 and word not in widths
                widths[word] = first, second
    return widths


def half_language():
    moves = {
        "idle": ("idle", "before"),
        "before": ("before", "first0"),
        "first0": ("first1",),
        "first1": ("first2",),
        "first2": ("first3",),
        "first3": ("first3", "between"),
        "between": ("between", "second0"),
        "second0": ("second1",),
        "second1": ("second2",),
        "second2": ("second3",),
        "second3": ("second3",),
    }
    states = tuple(moves)
    heights = dict(zip(states, (2, 3, 4, 4, 4, 4, 3, 4, 4, 4, 4)))
    remaining = dict(zip(states, (12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2)))
    records = {((2,), "idle")}
    for t in range(1, 9):
        records = {(word + (heights[child],), child) for word, stage in records
                   for child in moves[stage] if remaining[child] <= 16 - t}
    return records


def search():
    requested = explicit_language()
    half = half_language()
    matches = {
        ("between", "between"),
        ("first2", "second1"),
        ("first3", "second0"),
        ("first3", "second1"),
    }
    valid = matches | {(end, start) for start, end in matches}
    implicit = {left + right[-2::-1] for (left, a), (right, b) in product(half, repeat=2) if (a, b) in valid}
    assert implicit == requested.keys()
    counts = Counter(requested.values())
    return {
        "exact_occupation_words": len(implicit),
        "half_occupation_words": len(half),
        "width_pair_counts": [[*pair, count] for pair, count in sorted(counts.items())],
        "midpoint_occupations": dict(Counter(h[8] for h in implicit)),
    }


if __name__ == "__main__":
    print(json.dumps(search(), indent=2, sort_keys=True))
