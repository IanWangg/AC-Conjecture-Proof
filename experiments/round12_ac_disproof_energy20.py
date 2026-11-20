"""Audit both energy-20 fringes and locate exact relative-conjugator cuts."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, groupby, product
import json

from elementary_verify import replay
from free_waypoint_search import conj_ops
from primitive_map_pairs import LETTERS, decide, fold, follow, inverse, verify_absence
from round10_ac_disproof_outsider_quotient import (
    ALPHABETS,
    CHORDS,
    chord_words,
    exact_cycle,
    graph_rank,
    principal_quotients,
    quotient_weights,
    ranked_outsiders,
    reduce,
    spanning,
    weight_of_loop,
)
from round11_ac_disproof_wirtinger import ROSE, checked_certificate, verify_single_voltage
from stallings_search import apply
from u_verify_voltage_phase import automaton, fold_relation, fold_word_arcs, voltage_word
from v_vertex_identification import fold_identification
from v_voltage_cycle_review import review


SECOND_ENERGY20 = ("xxxxyXXYY", "xxyyxYYYxxY")
AFFINE_EXCEPTION = (1, -1, 1, 2, 2, 0, -1, 0, 3, 1, 0, -1,
                    4, 2, -1, -1, 5, 3, -1, 5, -1, 4, 4, -1)
VOLTAGE_EXCEPTION = (1, 1, 1, 2, 0, 0, 2, 0, 2, 2, 0, 1)
VOLTAGE_CHARACTERS = ((-1, 0, 0, 1), (-2, -2, -2, 1), (-1, -2, -2, 0))
TESTS = tuple(product(ALPHABETS, (0, 1)))


def chord_data(graph, base):
    paths, chords, arcs, _ = spanning(graph)
    words = [reduce(paths[a] + LETTERS[c] + inverse(paths[b])) for a, c, b in chords]
    marking, _ = chord_words(graph, [*base, *words[2:]])
    return words, marking[:2], arcs


def affine_multiply(first, second):
    k, c = first
    exponent, translation = second
    return k + exponent, c + Fraction(2) ** k * translation


def affine_image(chord_word):
    values = {
        "a": (1, 0), "A": (-1, 0),
        "b": (0, 1), "B": (0, -1),
        "c": (0, 1), "C": (0, -1),
    }
    result = (0, Fraction(0))
    for letter in chord_word:
        result = affine_multiply(result, values[letter])
    return result


def affine_exclusion(graph, base):
    basis, marked, arcs = chord_data(graph, base)
    assert marked == ("bC", "bbaBA")
    assert all(affine_image(word) == (0, 0) for word in marked)
    chord_labels = [""] * len(graph)
    for (a, c, _), (chord, sign) in arcs.items():
        label = CHORDS[chord]
        chord_labels[4 * a + c] = label if sign == 1 else label.upper()
    tests = []
    for alphabet, blocked in TESTS:
        signs = tuple(map(LETTERS.index, alphabet))
        cycles = []
        for states, edges in automaton(graph, [0] * len(graph), signs, blocked):
            successor = {a: b for a, b, _ in edges}
            assert len(edges) == len(states) and successor.keys() == states
            at = start = min(states)
            visited = []
            ambient = []
            weights = []
            while at not in visited:
                visited.append(at)
                vertex, next_letter = divmod(at, 2)
                label = signs[next_letter]
                ambient.append(LETTERS[label])
                weights.append(chord_labels[4 * vertex + label])
                at = successor[at]
            assert at == start and set(visited) == states
            word = "".join(ambient)
            assert follow(graph, start // 2, word) == start // 2
            k, translation = affine_image("".join(weights))
            assert k or translation
            cycles.append({"states": visited, "ambient_cycle": word, "chord_word": "".join(weights),
                           "dyadic_scale_exponent": k, "dyadic_translation": str(translation)})
        tests.append({"alphabet": alphabet, "blocked": alphabet[blocked], "cycles": cycles})
    return {"graph": graph, "chord_basis": basis, "source_in_chords": marked, "tests": tests}


def voltage_exclusion(graph, base):
    basis, marked, arcs = chord_data(graph, base)
    checks = {}
    for character in VOLTAGE_CHARACTERS:
        weights = [0] * len(graph)
        for (a, label, _), (i, sign) in arcs.items():
            weights[4 * a + label] = sign * character[i]
        assert all(voltage_word(graph, weights, word) == 0 for word in base)
        for check in review(graph, weights)["checks"]:
            key = (*check["alphabet"], check["forbidden_double"])
            if check["status"] == "PASS" and key not in checks:
                count = verify_single_voltage(graph, weights, check)
                checks[key] = {"character": character, "inequalities_checked": count, **check}
    assert len(checks) == len(TESTS)
    return {"graph": graph, "chord_basis": basis, "source_in_chords": marked,
            "tests": [checks[key] for key in sorted(checks)]}


def audit_fringe(base, exceptional):
    source = fold(base)
    assert fold_word_arcs(base) == list(source)
    original_absence = verify_absence(decide(source, save_certificate=True))
    table = principal_quotients(base)
    assert {g for g in table if graph_rank(g) == 2} == {source, ROSE}
    first_identifications = {}
    for a, b in combinations(range(len(source) // 4), 2):
        child, _ = fold_relation(source, (a, b))
        assert tuple(child) == fold_identification(source, a, b)[0]
        first_identifications[a, b] = len(child) // 4, graph_rank(child)
    assert all(rank == 3 for _, rank in first_identifications.values())
    outsiders = ranked_outsiders(base, table)
    assert set(table) - {ROSE} - outsiders.keys() == exceptional.keys()
    ranks = Counter()
    digest = sha256()
    for graph, outside in sorted(outsiders.items()):
        if graph == source:
            continue
        rows = [*base, *outside]
        rank = graph_rank(graph)
        assert len(rows) == rank and fold(rows) == graph
        weights, _ = quotient_weights(graph, rows)
        assert [weight_of_loop(graph, weights, word, 0) for word in rows] == ["", "", *CHORDS[2:rank]]
        assert all(exact_cycle(graph, weights, alphabet, blocked) is None for alphabet, blocked in TESTS)
        ranks[rank] += 1
        digest.update(json.dumps([graph, outside, weights], separators=(",", ":")).encode() + b"\n")
    return {"pair": base, "source_vertices": len(source) // 4,
            "source_map_pair_absence": original_absence, "principal_quotients": len(table),
            "principal_quotients_by_rank": dict(sorted(Counter(map(graph_rank, table)).items())),
            "free_quotient_exclusions_by_rank": dict(sorted(ranks.items())),
            "free_quotient_exclusions": sum(ranks.values()), "free_quotient_case_sha256": digest.hexdigest(),
            "first_vertex_identifications_rank_three": len(first_identifications),
            "minimum_new_words_to_generate_ambient_with_pair": 2,
            "exceptional": {name: check(graph, base) for graph, (name, check) in exceptional.items()}}


def inverse_moves(moves):
    result = []
    for move in reversed(moves):
        if move["op"] == "conjugate":
            result.append({**move, "g": inverse(move["g"])})
        elif move["op"] == "multiply":
            invert = {"op": "invert", "i": move["j"]}
            result.extend((invert, move, invert))
        else:
            result.append(move)
    return result


def common_conjugate(pair, gauge):
    return tuple(reduce(gauge + row + inverse(gauge)) for row in pair)


def rose_splits(graph, word):
    hits = []
    for split in range(len(word) + 1):
        a = follow(graph, 0, word[:split])
        b = follow(graph, 0, inverse(word[split:]))
        if min(a, b) >= 0 and a != b and fold_identification(graph, a, b)[0] == ROSE:
            hits.append({"prefix": word[:split], "suffix": word[split:], "vertices": [a, b]})
    return hits


def relative_cut(start, moves, pivot, offset=0):
    original = normalized = tuple(start)
    gauge = ""
    support = list(start)
    proper = fold(support)
    strict = []
    growth = []
    other = 1 - pivot
    for products, group in groupby(enumerate(moves, offset + 1), lambda item: item[1]["op"] == "multiply"):
        block = list(group)
        conjugators = ["", ""]
        signs = [1, 1]
        for _, move in block:
            original = apply(original, move)
            i = move["i"]
            if move["op"] == "conjugate":
                conjugators[i] = reduce(move["g"] + conjugators[i])
            if move["op"] == "invert":
                signs[i] *= -1
        if products:
            block_moves = [move for _, move in block]
        else:
            old_gauge = gauge
            gauge = reduce(gauge + inverse(conjugators[pivot]))
            relative = reduce(gauge + conjugators[other] + inverse(old_gauge))
            block_moves = [{"op": "invert", "i": i} for i, sign in enumerate(signs) if sign == -1]
            block_moves += conj_ops(other, relative)
            support.append(relative)
        strict.extend(block_moves)
        for move in block_moves:
            normalized = apply(normalized, move)
        assert common_conjugate(original, gauge) == normalized
        if products:
            assert all(follow(proper, 0, row) == 0 for row in normalized)
            continue
        enlarged = fold(support)
        assert all(follow(enlarged, 0, row) == 0 for row in normalized)
        if enlarged == proper:
            continue
        assert fold_word_arcs(support) == list(enlarged)
        growth.append({"instruction_interval": [block[0][0], block[-1][0]],
                       "conjugators_in_input_block": conjugators, "relative_conjugator": relative,
                       "vertices": len(enlarged) // 4, "rank": graph_rank(enlarged),
                       "cumulative_graph": enlarged, "normalized_endpoint": normalized})
        if enlarged == ROSE:
            splits = rose_splits(proper, relative)
            assert splits
            certificate = {"format": "ordinary-ac-elementary-v1", "start": list(start),
                           "target": list(normalized), "moves": strict}
            return {"growth": growth, "last_proper_graph": proper, "rose_fold_splits": splits,
                    "strict_gauged_prefix_replay": replay(certificate), "strict_gauged_prefix": certificate}
        proper = enlarged
    raise AssertionError("relative conjugators did not reach the rose")


def both_pivots(start, moves, offset=0):
    proofs = [relative_cut(start, moves, pivot, offset) for pivot in (0, 1)]
    assert [g["cumulative_graph"] for g in proofs[0]["growth"]] == [
        g["cumulative_graph"] for g in proofs[1]["growth"]]
    assert [g["instruction_interval"] for g in proofs[0]["growth"]] == [
        g["instruction_interval"] for g in proofs[1]["growth"]]
    return proofs


def run():
    entry, entry_replay = checked_certificate("round11_ak3_cap32_minimum.json")
    ak2, ak2_replay = checked_certificate("n_ak2_cyclic13.json")
    energy20 = tuple(entry["target"])
    reversed_entry = inverse_moves(entry["moves"])
    reverse_replay = replay({**entry, "start": entry["target"], "target": entry["start"], "moves": reversed_entry})
    adjacent = tuple(ak2["start"])
    for move in ak2["moves"][:2]:
        adjacent = apply(adjacent, move)
    assert adjacent == ("yyXXy", "xyxYXY")
    cases = {
        AFFINE_EXCEPTION: ("six_vertex_affine", affine_exclusion),
        VOLTAGE_EXCEPTION: ("index_three_voltage", voltage_exclusion),
    }
    first = audit_fringe(energy20, cases)
    second = audit_fringe(SECOND_ENERGY20, {})
    assert first["free_quotient_exclusions"] == 10474 and second["free_quotient_exclusions"] == 7368
    return {"energy20_first_fringe": first, "energy20_second_fringe": second,
            "strict_energy20_entry": entry_replay, "strict_energy20_reverse_replay": reverse_replay,
            "strict_ak2_full": ak2_replay,
            "relative_rose_cuts": {
                "from_ak3": both_pivots(entry["start"], entry["moves"]),
                "from_energy20": both_pivots(energy20, reversed_entry),
                "from_ak2_exclusion_side": both_pivots(adjacent, ak2["moves"][2:], 2),
            }}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
