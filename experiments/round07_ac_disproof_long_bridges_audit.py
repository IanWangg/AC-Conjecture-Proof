"""Reconstruct actual bases and independently check long middle-bridge examples."""

import argparse
from itertools import combinations, permutations, product
from hashlib import sha256
import json
from pathlib import Path
import random

from elementary_verify import replay
from free_waypoint_search import canonical, conj_ops, cyclic, normalize
from primitive_map_pairs import decide, fold, follow, inverse, reduce, verify_absence
from round02_ac_disproof_controls import rebased_join, signed_graphs_acyclic
from round03_ac_disproof_bridges import count_readings, endpoint_graph, signed_rotations
from round06_ac_disproof_basis_controls import AK3, direct_marked_bases, direct_placements, rotations
from stallings_search import apply, nielsen_move
from v_vertex_identification import spanning

ALPHABET = "xXyY"


def lobe_classes(words):
    return tuple(sorted(map(canonical, words)))


def check_counts(circle, own, other):
    return all(count_readings(circle, word) == 1 for word in own) and not any(
        count_readings(circle, word) for word in other
    )


def permitted(lobe, direction):
    return direction not in (lobe[0], inverse(lobe[-1]))


def read_prefixes(words, lobe, alphabet):
    """Use outward paths into the tail, rather than inverse-path prefix tests."""
    circle = endpoint_graph(lobe, "")
    possible_prefixes = set()
    for word in words:
        for start in range(len(lobe)):
            at = start
            for position, letter in enumerate(word):
                if at == 0 and position > 0 and permitted(lobe, letter):
                    suffix = word[position:]
                    if set(suffix) <= set(alphabet):
                        possible_prefixes.add(suffix)
                at = circle[at].get(letter)
                if at is None:
                    break
    return possible_prefixes


def audit_template(record):
    lobes = tuple(record["lobes"])
    patterns = [signed_rotations(lobe) for lobe in lobes]
    all_patterns = patterns[0] | patterns[1]
    rotations_by_lobe = [rotations(lobe) for lobe in lobes]
    length = max(map(len, lobes))
    assert length == record["guard_length"]
    ends = [
        {
            letter: sum(permitted(rotation, letter) and check_counts(
                endpoint_graph(rotation, letter * length), patterns[i], patterns[1 - i]
            ) for rotation in choices)
            for letter in ALPHABET
        }
        for i, choices in enumerate(rotations_by_lobe)
    ]
    constant = sum(ends[0][c] * ends[1][inverse(c)] for c in ALPHABET
                   if not any(set(w) == {c} for w in all_patterns))
    exponential, alphabets = 0, []
    for a, b in product(ALPHABET, repeat=2):
        if a.lower() == b.lower() or any(set(w) <= {a, b} for w in all_patterns):
            continue
        count = ends[0][a] * ends[1][inverse(b)]
        exponential += count
        if count:
            alphabets.append(a + b)
    unrestricted = 0
    for a, b in product("xX", "yY"):
        if any(set(w) <= {a, b} for w in all_patterns):
            continue
        count = 1
        for choices, letters in zip(rotations_by_lobe, ((a, b), (inverse(a), inverse(b)))):
            count *= sum(
                any(permitted(rotation, letter) for letter in letters)
                and not read_prefixes(all_patterns, rotation, letters)
                for rotation in choices
            )
        unrestricted += count
    assert constant == record["constant_families"]
    assert exponential == record["exponential_families"]
    assert unrestricted == record["unrestricted_alphabet_families"]
    assert set(alphabets) == set(record["accepted_end_letters"])

    left, right = rotations_by_lobe
    pairs = [(a, b) for choices in (left, right) for i, a in enumerate(choices) for b in choices[i:]]
    pairs.extend(product(left, right))
    assert all(signed_graphs_acyclic(fold(pair)) for pair in pairs)
    return len(pairs)


def audit_scope(summary, catalogue, rng):
    first_mass, second_mass, gap = (summary[k] for k in (
        "first_basis_mass", "second_basis_mass", "first_bridge_cap"
    ))
    first = set(direct_placements(AK3, first_mass, gap))
    classes = {
        lobe_classes(words)
        for placed in first
        for words in direct_marked_bases(placed, second_mass)
    }
    assert len(first) == summary["first_marked_pairs"]
    assert len(classes) == summary["distinct_second_lobe_pairs"]
    bare = {
        (a, b) for a, b in classes
        if check_counts(endpoint_graph(a, ""), signed_rotations(a), signed_rotations(b))
        and check_counts(endpoint_graph(b, ""), signed_rotations(b), signed_rotations(a))
    }
    assert len(bare) == summary["bare_lobes_unique"] == summary["rotation_certified_pairs"]
    data = [json.loads(line) for line in catalogue.read_text().splitlines()]
    assert {tuple(row["lobes"]) for row in data} == bare
    for key in ("constant_families", "exponential_families", "unrestricted_alphabet_families"):
        assert sum(row[key] for row in data) == summary[key]
    assert summary["rotation_positive_checks"] == summary["rotation_incomplete_checks"] == 0
    assert not summary["rotation_exact_exclusions"]
    assert sum(
        (len(a) + len(b)) * (len(a) + len(b) + 1) // 2 for a, b in bare
    ) == summary["rotation_DAG_exclusions"]
    sample = rng.sample(data, min(len(data), 10))
    return {
        "independent_first_markings": len(first),
        "independent_second_lobe_pairs": len(classes),
        "independent_bare_unique_pairs": len(bare),
        "sampled_exact_endpoint_template_audits": len(sample),
        "sampled_independent_rotation_pair_DAG_checks": sum(map(audit_template, sample)),
        "catalogue_sha256": sha256(catalogue.read_bytes()).hexdigest(),
    }


def basis_paths(rows, bound):
    yield rows, [], 2
    for i, negative in product(range(2), (False, True)):
        state, ledger = rows, []
        for k in range(1, bound - 1):
            state, part = nielsen_move(state, i, left=False, negative=negative)
            ledger += part
            yield state, list(ledger), k + 2


def align(rows, slots):
    moves = []
    for i, wanted in slots.items():
        core = cyclic(wanted)
        state, part = normalize(rows, i, core)
        # The chosen example has cyclically reduced first and second lobes.
        assert core == wanted
        rows = state
        moves += part
    return rows, moves


def phase(rows, target, bound):
    for state, steps, mass in basis_paths(rows, bound):
        for placement in permutations(target):
            if tuple(map(canonical, state)) == tuple(map(canonical, placement)):
                marked, rest = align(state, dict(enumerate(placement)))
                return marked, steps + rest, mass
    raise AssertionError("the requested actual simultaneous basis was not generated")


def readable_prefix(graph, position, word):
    for i, letter in enumerate(word):
        step = graph[4 * position + ALPHABET.index(letter)]
        if step < 0:
            return i
        position = step
    return len(word)


def example_scope(record, rng):
    left, start_bridge, right = record["example"]
    c, d = record["example_alphabet"]
    length = record["guard_length"]
    assert start_bridge == c * length + d * length and c + d == "xy"
    middle = "xyxxyy" * 4
    q = c * length + middle + d * length
    first, steps, mass_one = phase(AK3, record["first_placement"], 4)
    second, following, mass_two = phase(first, (left, right), 3)
    assert mass_one > 2 and mass_two > 2
    donor = second.index(right)
    tail = conj_ops(donor, q)
    state = second
    for move in tail:
        state = apply(state, move)
    ledger = {"format": "ordinary-ac-elementary-v1", "start": list(AK3), "target": list(state),
              "moves": steps + following + tail}
    replayed = replay(ledger)
    assert state[donor] == q + right + inverse(q)

    original = fold(first)
    candidates = [
        [v for v in range(len(original) // 4) if follow(original, v, lobe) == v]
        for lobe in (left, right)
    ]
    assert all(len(vertices) == 1 for vertices in candidates)
    a, b = (vertices[0] for vertices in candidates)
    prefix = readable_prefix(original, a, q)
    suffix = readable_prefix(original, b, inverse(q))
    assert len(q) - prefix - suffix > 4
    patterns = signed_rotations(left) | signed_rotations(right)
    refolded_joins = exact_states = 0
    for inner in ("", c * 3, d * 7, middle):
        bridge = c * length + inner + d * length
        basis = (left, bridge + right + inverse(bridge))
        graph = fold(basis)
        n = len(graph) // 4
        assert n == len(left) + len(right) + len(bridge) - 1
        assert all(sum(follow(graph, v, word) >= 0 for v in range(n)) == 1 for word in patterns)
        paths, *_ = spanning(graph)
        for i, j in rng.sample(list(combinations(range(n), 2)), 20):
            join = rebased_join(basis, paths, i, j)
            assert signed_graphs_acyclic(join)
            decision = decide(join, save_certificate=True)
            assert decision["status"] == "ABSENT"
            exact_states += verify_absence(decision)["closed_map_pair_states_checked"]
            refolded_joins += 1
    return {
        "first_placed_pair": first, "basis_masses": [mass_one, mass_two],
        "second_placed_lobes": [left, right], "bridge": q,
        "first_core_vertices": len(original) // 4, "lobe_loop_vertices": [a, b],
        "bridge_readable_prefix": prefix, "bridge_readable_suffix": suffix,
        "bridge_unread_gap": len(q) - prefix - suffix,
        "strict_entry_ledger": ledger, "replayed": replayed,
        "sampled_full_barbell_folds": 4, "sampled_independent_final_joins": refolded_joins,
        "sampled_exact_partial_map_states": exact_states,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    rng = random.Random(3907)
    summaries = []
    for name in ("220", "330", "231", "331", "430", "340"):
        summary = json.loads((args.work / f"{name}.json").read_text())
        catalogue = args.work / f"{name}.jsonl"
        summaries.append({"native": summary, "independent": audit_scope(summary, catalogue, rng)})
    example = json.loads((args.work / "430.jsonl").read_text().splitlines()[0])
    print(json.dumps({"unbounded_middle_bridge_scopes": summaries,
                      "nontrivial_strict_example": example_scope(example, rng)}, indent=2))


if __name__ == "__main__":
    main()
