"""Count four-letter middle bridges and verify the complete lobe-reading guard."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import random

from elementary_verify import replay
from free_waypoint_search import conj_ops, cyclic
from primitive_map_pairs import decide, fold, follow, inverse, reduce, verify_absence
from round02_ac_disproof_controls import rebased_join, signed_graphs_acyclic
from round03_ac_disproof_bridges import endpoint_graph, signed_rotations
from round06_ac_disproof_basis_controls import AK3, rotations
from round07_ac_disproof_long_bridges_audit import check_counts, phase, readable_prefix
from stallings_search import apply, nielsen_move
from v_vertex_identification import spanning


ALPHABET = "xXyY"
CANCELLATIONS = {letter + inverse(letter) for letter in ALPHABET}


def reads_at_attachment(circle, word):
    at = 0
    for letter in word:
        at = circle[at].get(letter)
        if at is None:
            return False
    return True


def outward_forbidden(lobe, circle, markers):
    blocked = {lobe[0], inverse(lobe[-1])}
    return blocked | {
        marker[cut:]
        for marker in markers for cut in range(1, len(marker))
        if reads_at_attachment(circle, inverse(marker[:cut]))
    }


class BridgeGuard:
    def __init__(self, left, right):
        left_circle, right_circle = (endpoint_graph(w, "") for w in (left, right))
        left_markers, right_markers = map(signed_rotations, (left, right))
        assert check_counts(left_circle, left_markers, right_markers)
        assert check_counts(right_circle, right_markers, left_markers)
        self.markers = left_markers | right_markers
        self.prefixes = outward_forbidden(left, left_circle, self.markers)
        self.suffixes = {inverse(w) for w in outward_forbidden(right, right_circle, self.markers)}
        self.crossings = {
            marker[first:last]
            for marker in self.markers
            for first in range(1, len(marker) - 1)
            if reads_at_attachment(left_circle, inverse(marker[:first]))
            for last in range(first + 1, len(marker))
            if reads_at_attachment(right_circle, marker[last:])
        }

    def failures(self, bridge):
        prefix = any(bridge.startswith(w) for w in self.prefixes)
        suffix = any(bridge.endswith(w) for w in self.suffixes)
        internal = any(w in bridge for w in self.markers)
        return [name for name, fails in (
            ("folded_endpoint_or_one_lobe", prefix or suffix),
            ("interior", internal),
            ("both_lobes", bridge in self.crossings),
        ) if fails]

    def accepts(self, bridge):
        return bool(bridge) and reduce(bridge) == bridge and not self.failures(bridge)


class SuffixMachine:
    def __init__(self, forbidden, terminal_forbidden=()):
        prefixes = {""}
        for word in forbidden:
            prefixes.update(word[:i] for i in range(1, len(word)))
        for word in terminal_forbidden:
            prefixes.update(word[:i] for i in range(1, len(word) + 1))
        states = sorted(prefixes, key=lambda word: (len(word), word))
        state_id = {word: i for i, word in enumerate(states)}
        self.edges = []
        self.terminal = []
        for word in states:
            outgoing = []
            for letter in ALPHABET:
                new = word + letter
                suffixes = [new[i:] for i in range(len(new) + 1)]
                if any(suffix in forbidden for suffix in suffixes):
                    continue
                target = next(state_id[suffix] for suffix in suffixes if suffix in state_id)
                outgoing.append((letter, target))
            self.edges.append(outgoing)
            self.terminal.append(not any(word.endswith(end) for end in terminal_forbidden))

    def advance(self, state, word):
        for letter in word:
            state = dict(self.edges[state]).get(letter)
            if state is None:
                return None
        return state

    def step(self, counts, alphabet=ALPHABET):
        result = [0] * len(counts)
        for source, count in enumerate(counts):
            if count:
                for letter, target in self.edges[source]:
                    if letter in alphabet:
                        result[target] += count
        return result

    def returns(self, state, length, alphabet=ALPHABET):
        counts = [0] * len(self.edges)
        counts[state] = 1
        for _ in range(length):
            counts = self.step(counts, alphabet)
        return counts[state]


def exact_counts(guard, requested_lengths):
    machine = SuffixMachine(guard.markers | CANCELLATIONS, guard.suffixes)
    left_prefixes = {w[:i] for w in guard.prefixes for i in range(len(w))}
    crossed_at_length = Counter()
    for bridge in guard.crossings:
        if guard.failures(bridge) == ["both_lobes"] and reduce(bridge) == bridge:
            crossed_at_length[len(bridge)] += 1
    running = {(0, ""): 1}
    result = {}
    for length in range(1, max(requested_lengths) + 1):
        next_running = Counter()
        for (at, prefix), count in running.items():
            for letter, target in machine.edges[at]:
                extended = None if prefix is None else prefix + letter
                if extended in guard.prefixes:
                    continue
                retained = extended if extended in left_prefixes else None
                next_running[target, retained] += count
        running = next_running
        if length in requested_lengths:
            result[length] = sum(
                count for (at, _), count in running.items() if machine.terminal[at]
            ) - crossed_at_length[length]
    return result


def return_family(record, block_length):
    left, bridge, right = record["example"]
    length = record["guard_length"]
    assert length == max(map(len, (left, right)))
    c, d = record["example_alphabet"]
    entrance, exit_word = c * length, d * length
    assert bridge == entrance + exit_word
    guard = BridgeGuard(left, right)
    assert guard.accepts(bridge)
    machine = SuffixMachine(guard.markers | CANCELLATIONS)
    start = machine.advance(0, entrance)
    assert start is not None and machine.advance(start, exit_word) is not None
    count = machine.returns(start, block_length)
    assert count > 2 ** block_length
    all_signs = all_sign_returns(machine, start, block_length)
    assert all_signs > 2 ** block_length
    return {
        "lobes": record["example"][::2], "entrance": entrance, "exit": exit_word,
        "states": len(machine.edges), "block_length": block_length, "return_labels": count,
        "all_sign_return_labels": all_signs,
    }, machine, start


def all_sign_returns(machine, start, block_length):
    count = 0
    for size in range(len(ALPHABET) + 1):
        for alphabet in combinations(ALPHABET, size):
            count += (-1) ** (len(ALPHABET) - size) * machine.returns(start, block_length, alphabet)
    return count


def all_sign_example(machine, start, block_length):
    paths = {(start, 0): ""}
    for _ in range(block_length):
        paths = {
            (target, seen | (1 << ALPHABET.index(letter))): word + letter
            for (at, seen), word in paths.items() for letter, target in machine.edges[at]
        }
    return paths[start, (1 << len(ALPHABET)) - 1]


def side_is_folded(left, right, bridge):
    def allows(lobe, letter):
        return letter not in (lobe[0], inverse(lobe[-1]))

    return allows(left, bridge[0]) and allows(right, inverse(bridge[-1]))


def full_fold_readings(left, right, bridge, guard):
    basis = (left, bridge + right + inverse(bridge))
    graph = fold(basis)
    vertices = len(graph) // 4
    assert vertices == len(left) + len(right) + len(bridge) - 1
    readings = {marker: sum(follow(graph, v, marker) >= 0 for v in range(vertices))
                for marker in guard.markers}
    return basis, graph, readings


def short_controls(left, right, max_length):
    guard = BridgeGuard(left, right)
    counts = Counter()
    testing = [""]
    for length in range(1, max_length + 1):
        testing = [prefix + letter for prefix in testing for letter in ALPHABET
                   if not prefix or prefix[-1] != inverse(letter)]
        for bridge in testing:
            if not side_is_folded(left, right, bridge):
                continue
            _, _, readings = full_fold_readings(left, right, bridge, guard)
            assert guard.accepts(bridge) == all(count == 1 for count in readings.values())
            counts["entire_barbells"] += 1
            counts[length] += guard.accepts(bridge)
    accepted = dict(sorted((n, counts[n]) for n in range(1, max_length + 1)))
    assert accepted == exact_counts(guard, tuple(accepted))
    return {"lobes": [left, right], "direct_fold_comparisons": counts["entire_barbells"],
            "counts_by_length": accepted}


def both_lobes_control(class_words):
    for left, right in product(*(rotations(w) for w in class_words)):
        guard = BridgeGuard(left, right)
        for bridge in sorted(guard.crossings, key=lambda word: (len(word), word)):
            if guard.failures(bridge) != ["both_lobes"]:
                continue
            assert reduce(bridge) == bridge and side_is_folded(left, right, bridge)
            _, _, readings = full_fold_readings(left, right, bridge, guard)
            repeated = {w: readings[w] for w in sorted(readings) if readings[w] > 1}
            assert repeated
            return {"lobes": [left, right], "bridge": bridge, "repeated_markers": repeated}
    raise AssertionError("no independent two-lobe guard counterexample")


def circle_vertices(graph, root, lobe):
    vertices = set()
    at = root
    for letter in lobe:
        vertices.add(at)
        at = follow(graph, at, letter)
    assert at == root and len(vertices) == len(lobe)
    return vertices


def reads_inside(graph, start, bridge, vertices):
    at = start
    for letter in bridge:
        at = follow(graph, at, letter)
        if at not in vertices:
            return False
    return True


def exceptional_bridges(left, right):
    guard = BridgeGuard(left, right)
    candidates = {
        marker[:length] for marker in guard.markers for length in range(1, len(marker))
    }
    accepted, checked, exact_states = [], 0, 0
    for bridge in sorted(candidates, key=lambda word: (len(word), word)):
        if not guard.accepts(bridge):
            continue
        accepted.append(bridge)
        basis, graph, readings = full_fold_readings(left, right, bridge, guard)
        assert set(readings.values()) == {1}
        paths, *_ = spanning(graph)
        right_root = follow(graph, 0, bridge)
        circles = (circle_vertices(graph, 0, left), circle_vertices(graph, right_root, right))
        starts = sorted(v for circle in circles for v in circle if reads_inside(graph, v, bridge, circle))
        assert starts and 0 not in starts
        for start in starts:
            joined = rebased_join(basis, paths, 0, start)
            checked += 1
            if signed_graphs_acyclic(joined):
                continue
            decision = decide(joined, save_certificate=True)
            assert decision["status"] == "ABSENT"
            exact_states += verify_absence(decision)["closed_map_pair_states_checked"]
    return {"lobes": [left, right], "bare_circle_subwords": len(candidates),
            "guarded_exceptions": accepted, "bare_circle_alignment_joins_checked": checked,
            "exact_map_pair_states": exact_states}


def euclidean_word(a, b):
    if a == 0:
        return "y"
    if b == 0:
        return "x"
    if a == b:
        return "xy"
    if a > b:
        return euclidean_word(a - b, b).replace("y", "xy")
    return euclidean_word(a, b - a).replace("x", "xy")


def positive_additions(columns):
    v, w = columns
    last_to_first = []
    while sum(v) + sum(w) > 2:
        if v[0] >= w[0] and v[1] >= w[1]:
            v = v[0] - w[0], v[1] - w[1]
            last_to_first.append(0)
        else:
            assert w[0] >= v[0] and w[1] >= v[1]
            w = w[0] - v[0], w[1] - v[1]
            last_to_first.append(1)
    return last_to_first[::-1]


def nesting_control(left, right, bridge, mass_bound):
    words_checked = 0
    slopes = [(a, b) for a in range(mass_bound) for b in range(mass_bound - a) if a or b]
    for v, w in combinations(slopes, 2):
        determinant = v[0] * w[1] - v[1] * w[0]
        if sum(v) + sum(w) > mass_bound or abs(determinant) != 1:
            continue
        if determinant < 0:
            v, w = w, v
        choices = positive_additions((v, w))
        if not choices:
            continue
        first_retained = 1 - choices[0]
        last_retained = 1 - choices[-1]
        for a, b in product((left, inverse(left)), (right, inverse(right))):
            generators = (a, bridge + b + inverse(bridge))
            rooted = list(generators if first_retained == 0 else (inverse(bridge) + a + bridge, b))
            for changed in choices:
                rooted[changed] = rooted[1 - changed] + rooted[changed]
            values = dict(zip("xy", generators))
            expected = [cyclic("".join(values[c] for c in euclidean_word(*slope))) for slope in (v, w)]
            assert all(actual == cyclic(actual) for actual in rooted)
            assert all(actual in rotations(word) for actual, word in zip(rooted, expected))
            assert rooted[1 - last_retained].startswith(rooted[last_retained])
            words_checked += 1
    return {"mass_bound": mass_bound, "positive_unimodular_pairs_and_orientations": words_checked}


def nested_replay(entry):
    base = entry["strict_entry_ledger"]
    state = tuple(base["target"])
    moves = []
    changed_rows = (1, 0, 1)
    for changed in changed_rows:
        state, steps = nielsen_move(state, changed, left=True, negative=False)
        moves.extend(steps)
    assert all(cyclic(word) == word for word in state)
    assert state[1].startswith(state[0])
    ledger = dict(base, target=list(state), moves=base["moves"] + moves)
    return {"slopes": [[2, 1], [3, 2]], "basis_mass": 8, "changed_rows": changed_rows,
            "strict_entry_ledger": ledger, "replayed": replay(ledger),
            "retained_word_length": len(state[0]), "longer_word_length": len(state[1])}


def replay_control(record, family, block, rng):
    left, right = family["lobes"]
    bridge = family["entrance"] + block * 2 + family["exit"]
    assert set(bridge) == set(ALPHABET)
    guard = BridgeGuard(left, right)
    assert guard.accepts(bridge)
    basis, graph, readings = full_fold_readings(left, right, bridge, guard)
    assert set(readings.values()) == {1}
    first, before, first_mass = phase(AK3, record["first_placement"], 4)
    second, between, second_mass = phase(first, (left, right), 3)
    donor = second.index(right)
    moves = conj_ops(donor, bridge)
    target = second
    for move in moves:
        target = apply(target, move)
    assert target[donor] == basis[1] and target[1 - donor] == basis[0]
    ledger = {"format": "ordinary-ac-elementary-v1", "start": list(AK3),
              "target": list(target), "moves": before + between + moves}
    report = replay(ledger)
    original = fold(first)
    endpoints = [[v for v in range(len(original) // 4) if follow(original, v, lobe) == v]
                 for lobe in (left, right)]
    assert all(len(end) == 1 for end in endpoints)
    prefix = readable_prefix(original, endpoints[0][0], bridge)
    suffix = readable_prefix(original, endpoints[1][0], inverse(bridge))
    assert prefix == suffix == 0
    paths, *_ = spanning(graph)
    exact_states = 0
    sample = rng.sample(list(combinations(range(len(graph) // 4), 2)), 40)
    for i, j in sample:
        joined = rebased_join(basis, paths, i, j)
        decision = decide(joined, save_certificate=True)
        assert decision["status"] == "ABSENT"
        exact_states += verify_absence(decision)["closed_map_pair_states_checked"]
    return {
        "lobes": [left, right], "bridge": bridge, "block": block, "basis_masses": [first_mass, second_mass],
        "first_placed_pair": first, "readable_prefix": prefix, "readable_suffix": suffix,
        "unread_gap": len(bridge) - prefix - suffix, "strict_entry_ledger": ledger, "replayed": report,
        "independent_final_join_audits": len(sample), "independent_map_pair_states": exact_states,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalogue", type=Path)
    args = parser.parse_args()
    records = [json.loads(line) for line in args.catalogue.read_text().splitlines()]
    block_length = 16
    families = [return_family(record, block_length)[0] for record in records]
    weakest = min(families, key=lambda family: family["return_labels"])
    weakest_all_signs = min(families, key=lambda family: family["all_sign_return_labels"])
    chosen = records[0]
    family, machine, start = return_family(chosen, block_length)
    block = all_sign_example(machine, start, block_length)
    long_block_length = 128
    long_all_signs = all_sign_returns(machine, start, long_block_length)
    assert long_all_signs * 1000 ** long_block_length > 2883 ** long_block_length
    limits = (1, 8, 16, 25, 32, 50, 74, 100)
    baseline = ("XXXyyyy", "XYXyxy")
    mixed_entry = replay_control(chosen, family, block, random.Random(3908))
    result = {
        "catalogue_sha256": sha256(args.catalogue.read_bytes()).hexdigest(),
        "certified_marked_families": len(families),
        "families_sha256": sha256(json.dumps(families, sort_keys=True).encode()).hexdigest(),
        "weakest_marked_family": weakest,
        "weakest_all_sign_family": weakest_all_signs,
        "explicit_marked_family": family,
        "explicit_long_return_labels": {"block_length": long_block_length, "all_sign_labels": long_all_signs},
        "explicit_counts_by_bridge_length": exact_counts(BridgeGuard(*family["lobes"]), limits),
        "short_exact_guards": [short_controls(*baseline, 8), short_controls(*family["lobes"], 7)],
        "both_lobes_negative_control": both_lobes_control(baseline),
        "finite_separating_cut_exceptions": [exceptional_bridges(*basis) for basis in (baseline, family["lobes"])],
        "mixed_sign_replay": mixed_entry,
        "nesting_finite_check": nesting_control(*family["lobes"], mixed_entry["bridge"], 20),
        "nested_both_rows_changed": nested_replay(mixed_entry),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
