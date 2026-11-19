"""Certify local guards and lobe-pair primitive exclusions for the energy-15 escape."""

from collections import Counter
from functools import lru_cache
from itertools import product
import json
import random

from primitive_map_pairs import LETTERS, decide, fold, follow, inverse, verify_absence
from round01_ac_disproof_barbells import reduced_words, rotations, source_graph
from round02_ac_disproof_controls import audit_joins
from round03_ac_disproof_bridges import count_readings, endpoint_graph, signed_rotations


LEFT, RIGHT = "XXYxYxy", "XYXyxYYY"
WINDOW = max(len(LEFT), len(RIGHT))
FORBIDDEN = signed_rotations(LEFT) | signed_rotations(RIGHT)


def admissible(lobe, outward):
    return outward != lobe[0] and outward != inverse(lobe[-1])


def guard(lobe, tail):
    graph = endpoint_graph(lobe, tail)
    expected = signed_rotations(lobe)
    return all(count_readings(graph, word) == (word in expected) for word in FORBIDDEN)


def measure(lobe):
    guarded_tails = Counter()
    endpoint_counts = Counter()
    for r in rotations(lobe):
        for c in LETTERS:
            endpoint_counts[c] += admissible(r, c)
    totals = {mode: [0, 0] for mode in ("all", "positive", "negative")}
    for tail in reduced_words(WINDOW):
        for r in rotations(lobe):
            if not admissible(r, tail[0]):
                continue
            accepted = guard(r, tail)
            guarded_tails[tail] += accepted
            for mode, alphabet in (("all", LETTERS), ("positive", "xy"), ("negative", "XY")):
                if all(c in alphabet for c in tail):
                    totals[mode][0] += 1
                    totals[mode][1] += accepted
    return guarded_tails, endpoint_counts, totals


@lru_cache(maxsize=None)
def next_suffixes(suffix):
    return tuple(
        (suffix + c)[-WINDOW:]
        for c in LETTERS
        if c != inverse(suffix[-1]) and not any((suffix + c).endswith(f) for f in FORBIDDEN)
    )


def count_language(left, right, endpoints_left, endpoints_right, stops):
    # Count literal legal placements. Each left or right weight counts
    # endpoint rotations, rather than just reduced bridge labels.
    prefixes = left.copy()
    direction = endpoints_left.copy()
    counts = {}
    for length in range(1, max(stops) + 1):
        if length in stops:
            good = sum(count * right[inverse(s)] for s, count in prefixes.items())
            total = sum(count * endpoints_right[inverse(c)] for c, count in direction.items())
            counts[length] = {"admissible": total, "guarded": good}
        if length >= WINDOW:
            next_prefixes = Counter()
            for suffix, count in prefixes.items():
                if count:
                    for next_suffix in next_suffixes(suffix):
                        next_prefixes[next_suffix] += count
            prefixes = next_prefixes
        direction = Counter({
            c: sum(direction.values()) - direction[inverse(c)] for c in LETTERS
        })
    return counts


def check_lobe_pairs():
    totals = []
    for p, b in ((LEFT, LEFT), (LEFT, RIGHT), (RIGHT, RIGHT)):
        states = checked = 0
        for r, s in product(rotations(p), rotations(b)):
            cert = decide(fold((r, s)), save_certificate=True)
            assert cert["status"] == "ABSENT", (r, s, cert)
            states += verify_absence(cert)["closed_map_pair_states_checked"]
            checked += 1
        totals.append({"lobes": [p, b], "rotation_pairs": checked, "map_pair_states": states})
    return totals


def controls():
    rng = random.Random(261504)
    checked = passed = join_count = 0
    for length in (8, 9, 15, 24, 32):
        for _ in range(24):
            q = rng.choice(LETTERS)
            while len(q) < length:
                q += rng.choice([c for c in LETTERS if c != inverse(q[-1])])
            p = rng.choice([r for r in rotations(LEFT) if admissible(r, q[0])])
            b = rng.choice([r for r in rotations(RIGHT) if admissible(r, inverse(q[-1]))])
            predicted = (
                not any(f in q for f in FORBIDDEN)
                and guard(p, q[:WINDOW])
                and guard(b, inverse(q[-WINDOW:]))
            )
            basis, graph = source_graph(p, b, q)
            measured = all(
                sum(follow(graph, v, w) >= 0 for v in range(len(graph) // 4)) == 1
                for w in FORBIDDEN
            )
            assert measured == predicted
            if measured and checked % 29 == 0:
                result = audit_joins(basis, graph)
                join_count += result["checked_joins"]
            checked += 1
            passed += measured
    assert 0 < passed < checked
    return {"full_folds": checked, "guard_passes": passed, "replayed_two_copy_joins": join_count}


def main():
    left, endpoints_left, left_totals = measure(LEFT)
    right, endpoints_right, right_totals = measure(RIGHT)
    print(json.dumps({
        "lobes": [LEFT, RIGHT],
        "guard_window": WINDOW,
        "forbidden_signed_rotations": len(FORBIDDEN),
        "endpoint_guards": {LEFT: left_totals, RIGHT: right_totals},
        "regular_language_counts": count_language(
            left, right, endpoints_left, endpoints_right, (8, 9, 10, 12, 16, 20, 30, 50)
        ),
        "lobe_pairs": check_lobe_pairs(),
        "independent_controls": controls(),
    }, indent=2))


if __name__ == "__main__":
    main()
