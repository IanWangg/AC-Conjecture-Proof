#!/usr/bin/env python3
"""Enumerate the finite width-two singleton shift family of Round 16."""

import json
from itertools import groupby, product

from elementary_verify import inverse

P = "XyxYY"
Q = "XXyxxYY"
SWAP = str.maketrans("xXyY", "yYxX")
WINGS = {
    "upper": (P, inverse(Q)),
    "lower": (inverse(P).translate(SWAP), Q.translate(SWAP)),
}


def run_lengths(word, letter):
    return [len(tuple(run)) for symbol, run in groupby(word) if symbol.lower() == letter]


def stems(trace):
    yield ()
    exponents = tuple(i for i in range(-trace - 7, trace + 8) if i)
    for run_count in (1, 2):
        for c_powers in product(exponents, repeat=run_count):
            if sum(abs(power) != trace for power in c_powers) > 1:
                continue
            for d_powers in product((-1, 1), repeat=run_count):
                yield tuple(zip(c_powers, d_powers))


def run():
    receipts = {}
    for trace in (2, 4):
        by_length = [0, 0, 0]
        for stem in stems(trace):
            by_length[len(stem)] += 1
        p_range = [-5, trace + 5]
        receipts[trace] = {
            "stems_by_number_of_c_runs": by_length,
            "first_end_power_interval": p_range,
            "shift_words_per_orientation": sum(by_length) * (p_range[1] - p_range[0] + 1),
        }
    wings = {}
    for case, (left, right) in WINGS.items():
        left_counts = run_lengths(left, "y")
        right_counts = run_lengths(right, "y")
        assert left[0].lower() == right[-1].lower() == "x"
        assert left[-1].lower() == right[0].lower() == "y"
        assert len(left_counts) == len(right_counts) == 2
        assert sum(left_counts) + sum(right_counts) == 6
        assert sum(n - 1 for n in left_counts + right_counts) == 2
        assert sum(n != 2 for z in (left, right) for n in run_lengths(z, "x")) == 2
        assert sum(n != 4 for z in (left, right) for n in run_lengths(z, "x")) == 4
        wings[case] = {"left_affected_runs": left_counts, "right_affected_runs": right_counts}
    total = 2 * sum(row["shift_words_per_orientation"] for row in receipts.values())
    return {"fixed_wings": wings, "trace_controls": receipts, "total_shift_words": total}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
