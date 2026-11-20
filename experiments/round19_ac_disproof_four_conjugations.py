"""Exact four-conjugation restrictions for the literal rank-two AK(3) pair."""

from collections import Counter
from functools import lru_cache
from itertools import combinations, product
import json

from euclidean_primitive_audit import primitive_cyclic_word
from primitive_map_pairs import LETTERS, decide, fold, follow, inverse, reduce, verify_absence
from round05_ac_disproof_third_phase_audit import graph_basis
from round06_stable_disproof_conjugations import START, envelope
from round11_three_conjugations import ROSE, completing_conjugate
from round17_ac_disproof_three_phases import check_character, conjugated_copies
from stallings_search import cyclic
from u_verify_voltage_phase import fold_word_arcs
from v_vertex_identification import fold_identification, spanning


SOURCE = fold(START)
EXPECTED = ("xyxy", "xyxY", "xyXy", "xyXY", "yxyx", "yxyX", "yxYx", "yxYX")


@lru_cache(None)
def source_envelope(letters):
    return envelope(letters)


@lru_cache(None)
def subgroup_basis(graph):
    words = tuple(graph_basis(graph))
    assert fold(words) == graph
    return words


@lru_cache(None)
def primitive_test(graph):
    result = decide(graph, 0, save_certificate=True)
    if result["status"] == "ABSENT":
        return False, verify_absence(result)
    assert result["status"] == "PRIMITIVE"
    return True, result["witness"]


@lru_cache(None)
def complete(core, relative):
    assert core != ROSE
    return completing_conjugate(core, relative)


@lru_cache(None)
def free_block(core, first, second):
    return fold(conjugated_copies(subgroup_basis(core), (first, second)))


def homogeneous_fibre(letter, last):
    words = conjugated_copies(START, (letter, letter * 2))
    base = fold((*words, last))
    assert tuple(fold_word_arcs((*words, last))) == base
    kernel = check_character(base, words, last)
    weights = [0] * len(base)
    for (vertex, label, _), (index, sign) in spanning(base)[2].items():
        weights[4 * vertex + label] = sign * kernel["character"][index]

    fibre = {(0, 0): ("", 0)}
    vertices = [(0, 0)]
    edge_count = 0
    for a, b in vertices:
        path, height = fibre[a, b]
        for label, symbol in enumerate(LETTERS):
            edge = 4 * b + label
            target = SOURCE[4 * a + label], base[edge]
            if min(target) < 0:
                continue
            edge_count += 1
            value = height + weights[edge]
            if target in fibre:
                assert fibre[target][1] == value
            else:
                fibre[target] = (path + symbol, value)
                vertices.append(target)
    assert len(fibre) == 12 and edge_count == 22
    assert len({(b, height) for (_, b), (_, height) in fibre.items()}) == len(fibre)

    merges = []
    for (a, b), (c, d) in combinations(fibre, 2):
        if a != c:
            continue
        word = reduce(fibre[a, b][0] + inverse(fibre[c, d][0]))
        assert follow(SOURCE, 0, word) == 0
        enlarged = fold((*words, word, last))
        assert enlarged == fold_identification(base, b, d)[0]
        merges.append({"vertices": ((a, b), (c, d)), "representative": word,
                       "core": enlarged, **check_character(enlarged, (*words, word), last)})
    assert len(merges) == 2

    explored = 0
    for source_start, base_start in fibre:
        for alphabet in ("xy", "xY", "Xy", "XY"):
            letters = tuple(LETTERS.index(symbol) for symbol in alphabet)
            for forbidden in letters:
                states = {(source_start, -1)}
                queue = [(source_start, -1)]
                for start, previous in queue:
                    if previous != -1:
                        assert all(start != a or base[4 * b + (previous ^ 1)] >= 0
                                   for a, b in fibre)
                    for label in letters:
                        target = SOURCE[4 * start + label]
                        if target < 0 or label == previous == forbidden:
                            continue
                        if previous == -1 and base[4 * base_start + label] >= 0:
                            continue
                        state = target, label
                        if state not in states:
                            states.add(state)
                            queue.append(state)
                explored += len(states) - 1
    return {"prefix": letter * 2, "third_letter": last, "base": base,
            "base_certificate": kernel, "fibre": [(a, b, path, value)
                for (a, b), (path, value) in fibre.items()],
            "fibre_edges": edge_count // 2, "gapless_merges": merges,
            "signed_double_free_gap_states": explored, "accepted_signed_double_free_gaps": 0}


def basis_witness(prefix_core, last):
    forward = complete(prefix_core, last)["completing_word"]
    reverse = complete(prefix_core, inverse(last))["completing_word"]
    assert forward is not None and reverse is not None
    stationary = reduce(last + reverse + inverse(last))
    moving = reduce(inverse(last) + forward + last)
    assert all(follow(prefix_core, 0, row) == 0 for row in (stationary, moving))
    assert fold((stationary, forward)) == ROSE
    assert all(primitive_cyclic_word(cyclic(row)) for row in (stationary, moving))
    return {"prefix_pair": (stationary, moving), "conjugated_pair": (stationary, forward)}


def four_letter_cases(excluded_prefixes):
    rows = []
    totals = Counter()
    for letters in product(LETTERS, repeat=4):
        sequence = "".join(letters)
        whole = source_envelope(sequence)
        prefix = source_envelope(sequence[:3])
        final_has_primitive, final_test = primitive_test(whole)
        row = {"sequence": sequence, "whole_vertices": len(whole) // 4,
               "prefix_vertices": len(prefix) // 4}
        if not final_has_primitive:
            status = "whole_primitive_free"
            row["closed_map_pair_states"] = final_test["closed_map_pair_states_checked"]
        elif whole != ROSE:
            status = "whole_proper"
            row["primitive"] = final_test["based_primitive_word"]
        elif prefix == ROSE:
            status = "prefix_rose"
            row["prefix_graph"] = ROSE
        else:
            forward = complete(prefix, letters[-1])
            reverse = complete(prefix, inverse(letters[-1]))
            status = "last_forward_absent" if forward["completing_word"] is None else (
                "last_reverse_absent" if reverse["completing_word"] is None else "both_last_tests")
            row["forward"] = forward
            row["reverse"] = reverse

        row["coarse_status"] = status
        totals[status] += 1
        if status in ("prefix_rose", "both_last_tests"):
            has_primitive, primitive = primitive_test(prefix)
            if not has_primitive:
                row["ordinary_status"] = "prefix_primitive_free"
                row["prefix_closed_map_pair_states"] = primitive["closed_map_pair_states_checked"]
            elif sequence[:3] in excluded_prefixes:
                row["ordinary_status"] = "prefix_fibre_exclusion"
            else:
                row["ordinary_status"] = "unresolved"
                row["relaxed_last_basis"] = basis_witness(prefix, letters[-1])
            totals[row["ordinary_status"]] += 1
        rows.append(row)
    assert totals == {"whole_primitive_free": 138, "whole_proper": 26, "prefix_rose": 16,
                      "last_forward_absent": 17, "last_reverse_absent": 13, "both_last_tests": 46,
                      "prefix_primitive_free": 38, "prefix_fibre_exclusion": 16, "unresolved": 8}
    return totals, rows


@lru_cache(None)
def possible_last_block(core, relative):
    if core == ROSE:
        return True
    if not primitive_test(core)[0] or free_block(core, "", relative) != ROSE:
        return False
    return all(complete(core, direction)["completing_word"] is not None
               for direction in (relative, inverse(relative)))


def gap_masks(sequence):
    results = {}
    for marks in product((0, 1), repeat=3):
        blocks = [sequence[0]]
        for mark, letter in zip(marks, sequence[1:]):
            if mark:
                blocks.append(letter)
            else:
                blocks[-1] += letter
        possible = 0
        for receivers in product((0, 1), repeat=4):
            used = 0
            core = SOURCE
            for i, block in enumerate(blocks):
                transporters = ["", ""]
                for letter, receiver in zip(block, receivers[used:used+len(block)]):
                    transporters[receiver] = reduce(letter + transporters[receiver])
                used += len(block)
                if sum(map(len, transporters)) < len(block):
                    break
                if i == len(blocks) - 1:
                    relative = reduce(inverse(transporters[0]) + transporters[1])
                    possible += possible_last_block(core, relative)
                else:
                    core = free_block(core, *transporters)
        results["".join(map(str, marks))] = possible
    assert results == {f"{mask:03b}": 16 if mask == 7 else 0 for mask in range(8)}
    return results


def main():
    fibres = [homogeneous_fibre("x", "Y"), homogeneous_fibre("y", "X")]
    excluded_prefixes = {"xxy", "xxY", "yyx", "yyX"}
    counts, rows = four_letter_cases(excluded_prefixes)
    remaining = tuple(row["sequence"] for row in rows if row.get("ordinary_status") == "unresolved")
    assert remaining == EXPECTED
    gaps = {sequence: gap_masks(sequence) for sequence in remaining}
    print(json.dumps({"source": START, "homogeneous_prefix_fibres": fibres,
                      "all_schedule_counts": counts, "four_letter_cases": rows,
                      "remaining_schedules": remaining, "allowed_gap_masks": gaps,
                      "minimum_intervening_products": (1, 1, 2)}, indent=2))


if __name__ == "__main__":
    main()
