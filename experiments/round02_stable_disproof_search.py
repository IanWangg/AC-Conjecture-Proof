"""Reproduce the degree-six searches and the one-incoming chart-switch control."""

import argparse
from concurrent.futures import ProcessPoolExecutor
import json

from round01_stable_disproof_search import ak3_bounded_test


def inverse(word):
    return word.swapcase()[::-1]


def reduce_word(word):
    stack = []
    for letter in word:
        if stack and stack[-1] == letter.swapcase():
            stack.pop()
        else:
            stack.append(letter)
    return "".join(stack)


def chart_control(power):
    """The spent auxiliary row changes its generator from z to x."""
    rows = ["x", "x" * power + "y", "z"]
    moves = []

    def multiply(receiver, donor, sign=1):
        word = rows[donor] if sign == 1 else inverse(rows[donor])
        rows[receiver] = reduce_word(rows[receiver] + word)
        moves.append(("multiply", receiver, donor, sign))

    def conjugate(row, word):
        for letter in reversed(word):
            rows[row] = reduce_word(letter + rows[row] + inverse(letter))
            moves.append(("conjugate", row, letter))

    def invert(row):
        rows[row] = inverse(rows[row])
        moves.append(("invert", row))

    multiply(0, 2, -1)
    conjugate(0, "Z")
    assert rows[0] == "Zx"
    for i in range(power):
        # Replace one x by z modulo the retained donor Zx, restoring it.
        conjugator = "Y" + "X" * (power - i - 1)
        conjugate(0, conjugator)
        multiply(1, 0, -1)
        conjugate(0, inverse(conjugator))
    assert rows == ["Zx", "z" * power + "y", "z"]
    before = tuple(reduce_word(word.translate(str.maketrans("", "", "zZ"))) for word in rows[:2])
    multiply(2, 0)
    assert rows[2] == "x"
    after = tuple(reduce_word(word.translate(str.maketrans("zZ", "xX", "xX"))) for word in rows[:2])
    assert before == ("x", "y")
    assert after == ("X", "x" * power + "y")
    multiply(0, 2, -1)
    invert(0)
    for _ in range(power):
        multiply(1, 0, -1)
        conjugate(1, "Z")
    assert rows == ["z", "y", "x"]

    crossings = [m for m in moves if m[0] == "multiply" and ((m[1] == 2) != (m[2] == 2))]
    assert [m[1] == 2 for m in crossings] == [False, True, False]
    return {
        "power": power,
        "full_path_moves": len(moves),
        "cut_crossing_directions": ["out", "in", "out"],
        "chart_switch_projection_before": before,
        "chart_switch_projection_after_reindexing": after,
        "switch_move_lower_bound_from_exponent_growth": (power - 1).bit_length(),
        "full_path_endpoint": rows,
    }


def search(config):
    return ak3_bounded_test(*config)


def measurements(workers):
    configs = [
        (6, 0, 12, True),
        (6, 0, 13, False),
        (6, 1, 10, True),
        (6, 2, 8, True),
        (6, 3, 6, True),
        (7, 0, 13, True),
        (8, 0, 13, True),
    ]
    if workers == 1:
        runs = list(map(search, configs))
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            runs = list(pool.map(search, configs))
    assert [run["distance"] for run in runs] == [12, 13, None, None, None, None, None]
    assert all(run["last_radius"] == run["limit"] for run in runs)
    return {
        "degree_six_stable": {"unordered": 12, "ordered": 13},
        "degree_seven_and_higher_stable_lower_bound": 13,
        "runs": runs,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--controls-only", action="store_true")
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers must be positive")
    controls = [chart_control(power) for power in (1, 4, 32)]
    result = {"three_crossing_controls": controls}
    if not args.controls_only:
        result.update(measurements(args.workers))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
