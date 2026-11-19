"""Finite endpoint guards for the uniform two-copy proof on long bridges."""

from collections import Counter
from functools import lru_cache
from itertools import product
import argparse
import json
from pathlib import Path
import random

from primitive_map_pairs import LETTERS, fold, follow, inverse, reduce
from round01_ac_disproof_barbells import reduced_words, rotations, source_graph, sources
from round02_ac_disproof_controls import audit_joins, lobe_rotations

POWER = "xxxYYYY"
BRAID = "xyxYXY"
WINDOW = max(len(POWER), len(BRAID))


def signed_rotations(word):
    return set(rotations(word) + rotations(inverse(word)))


FORBIDDEN = signed_rotations(POWER) | signed_rotations(BRAID)


def endpoint_graph(lobe, tail):
    """A folded lobe circle with a path attached at its marked vertex."""
    graph = [{} for _ in range(len(lobe) + len(tail))]

    def put(start, end, letter):
        backward = inverse(letter)
        assert letter not in graph[start] and backward not in graph[end]
        graph[start][letter] = end
        graph[end][backward] = start

    for start, letter in enumerate(lobe):
        put(start, (start + 1) % len(lobe), letter)
    start = 0
    for end, letter in enumerate(tail, len(lobe)):
        put(start, end, letter)
        start = end
    return graph


def count_readings(graph, word):
    count = 0
    for start in range(len(graph)):
        vertex = start
        for letter in word:
            vertex = graph[vertex].get(letter)
            if vertex is None:
                break
        else:
            count += 1
    return count


def check_endpoints(lobe_word, tails):
    report = {}
    good = Counter()
    for lobe in rotations(lobe_word):
        expected = signed_rotations(lobe)
        counts = {name: [0, 0] for name in ("any", "positive", "negative")}
        for tail in tails:
            if tail[0] in (lobe[0], inverse(lobe[-1])):
                continue
            graph = endpoint_graph(lobe, tail)
            accepts = all(
                count_readings(graph, word) == int(word in expected)
                for word in sorted(FORBIDDEN)
            )
            if accepts:
                good[tail] += 1
            counts["any"][0] += 1
            counts["any"][1] += accepts
            for name, alphabet in (("positive", "xy"), ("negative", "XY")):
                if set(tail).issubset(alphabet):
                    counts[name][0] += 1
                    counts[name][1] += accepts
        report[lobe] = {
            name: {"admissible": tested, "guarded": accepted}
            for name, (tested, accepted) in counts.items()
        }
        for name in ("positive", "negative"):
            assert counts[name][0] == counts[name][1]
    return report, good


@lru_cache(maxsize=None)
def successors(suffix):
    choices = []
    for letter in LETTERS:
        if letter == inverse(suffix[-1]):
            continue
        candidate = suffix + letter
        if not any(candidate.endswith(forbidden) for forbidden in FORBIDDEN):
            choices.append(candidate[-WINDOW:])
    return tuple(choices)


def count_guarded_bridges(left, right, limits):
    counts = left.copy()
    report = {}
    for length in range(WINDOW, max(limits) + 1):
        if length in limits:
            accepted = sum(count * right[inverse(suffix)] for suffix, count in counts.items())
            admissible = 42 * 3 ** (length - 1)
            assert 0 < accepted < admissible
            report[str(length)] = {
                "all_admissible_literal_sources": admissible,
                "guarded_literal_sources": accepted,
            }
        following = Counter()
        for suffix, count in counts.items():
            for next_suffix in successors(suffix):
                following[next_suffix] += count
        counts = following
    return report


def control(power, braid, q):
    basis, graph = source_graph(power, braid, q)
    size = len(graph) // 4
    for word in FORBIDDEN:
        assert sum(follow(graph, vertex, word) >= 0 for vertex in range(size)) == 1
    return {
        "power": power,
        "braid": braid,
        "bridge": q,
        "bridge_reading_starts": [
            vertex for vertex in range(size) if follow(graph, vertex, q) >= 0
        ],
        "direct_two_copy_audit": audit_joins(basis, graph),
    }


def audit_guards():
    """Compare endpoint classification with readings on independent full folds."""
    rng = random.Random(20261119)
    tested = accepted = 0
    for length in (7, 8, 9, 15, 25, 45):
        for _ in range(40):
            bridge = rng.choice(LETTERS)
            for _ in range(length - 1):
                bridge += rng.choice([c for c in LETTERS if c != inverse(bridge[-1])])
            p, b = rng.choice(list(sources(3, bridge)))
            flags = []
            for lobe, tail in ((p, bridge[:WINDOW]), (b, inverse(bridge[-WINDOW:]))):
                graph = endpoint_graph(lobe, tail)
                expected = signed_rotations(lobe)
                flags.append(all(count_readings(graph, w) == int(w in expected) for w in FORBIDDEN))
            predicted = all(flags) and not any(word in bridge for word in FORBIDDEN)
            _, graph = source_graph(p, b, bridge)
            measured = all(
                sum(follow(graph, vertex, w) >= 0 for vertex in range(len(graph) // 4)) == 1
                for w in FORBIDDEN
            )
            assert predicted == measured
            tested += 1
            accepted += measured
    return {"source_folds": tested, "passes": accepted, "failures": tested - accepted}


def chain_words():
    for p, b, r, c, d in product(rotations(POWER), rotations(BRAID), sorted(FORBIDDEN), LETTERS, LETTERS):
        if c in (p[0], inverse(p[-1])) or inverse(d) in (b[0], inverse(b[-1])):
            continue
        if len({r[0], inverse(r[-1]), inverse(c), d}) == 4:
            yield p, b, r, c, d


def audit_chains(native):
    choices = list(chain_words())
    expected_pairs = sum(
        (len(p) + len(b) + len(r)) * (len(p) + len(b) + len(r) - 1) // 2
        for p, b, r, _, _ in choices
    )
    assert native["sources"] == len(choices) == 552
    assert native["vertex_pairs"] == native["DAG_exclusions"] == expected_pairs
    assert native["DAG_unresolved"] == 0
    assert sum(native["join_ranks"].values()) == expected_pairs

    explicit = (POWER, BRAID, "YXYxyx", "X", "y")
    cases = [explicit, *random.Random(20261119).sample(choices, 8)]
    sample_checks = []
    for p, b, r, c, d in cases:
        words = [p, c + r + inverse(c), c + d + b + inverse(c + d)]
        graph = fold(words)
        assert len(graph) // 4 == len(p) + len(b) + len(r)
        sample_checks.append(audit_joins(words, graph))
    p, b, r, c, d = explicit
    q = c + r * 3 + d
    _, graph = source_graph(p, b, q)
    q_readings = sum(follow(graph, v, r) >= 0 for v in range(len(graph) // 4))
    assert r in q and q_readings >= 3
    h = c + r + inverse(c)
    g = c + d + b + inverse(c + d)
    assert reduce(h * 3 + g + inverse(h) * 3) == q + b + inverse(q)
    return {
        "native_counts": native,
        "independent_sampled_chains": len(cases),
        "independent_sampled_joins": sum(row["checked_joins"] for row in sample_checks),
        "independent_map_states": sum(row["closed_map_states"] for row in sample_checks),
        "repeated_lobe_control": {
            "power": p,
            "braid": b,
            "middle": r,
            "overgroup_basis": [p, h, g],
            "bridge": q,
            "middle_word_readings_in_source": q_readings,
            "overgroup_audit": sample_checks[0],
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("native_chain_counts", type=Path)
    args = parser.parse_args()
    tails = tuple(reduced_words(WINDOW))
    power, left = check_endpoints(POWER, tails)
    braid, right = check_endpoints(BRAID, tails)
    limits = (7, 8, 9, 10, 12, 16, 20, 25, 30, 40, 50)
    repeated = control("YYYYxxx", BRAID, "x" * 18)
    mixed = control("YYYYxxx", BRAID, "x" + "y" * 7 + "xYXyx" + "y" * 7)
    assert len(repeated["bridge_reading_starts"]) == 5
    assert set(mixed["bridge"]) == set(LETTERS)
    result = {
        "endpoint_window": WINDOW,
        "signed_lobe_rotations": len(FORBIDDEN),
        "all_length_regular_language": count_guarded_bridges(left, right, limits),
        "endpoint_guard_counts": {"power": power, "braid": braid},
        "same_sign_endpoint_totals": {
            lobe: {
                sign: sum(counts[sign]["admissible"] for counts in report.values())
                for sign in ("positive", "negative")
            }
            for lobe, report in (("power", power), ("braid", braid))
        },
        "replayed_lobe_pair_certificates": lobe_rotations(),
        "independent_full_fold_guard_check": audit_guards(),
        "multiple_full_readings_control": repeated,
        "mixed_sign_control": mixed,
        "chain_families": audit_chains(json.loads(args.native_chain_counts.read_text())),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
