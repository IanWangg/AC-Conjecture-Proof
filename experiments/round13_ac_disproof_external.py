"""Classify the proper principal images of the new rank-three projection."""

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import lcm
from pathlib import Path
import subprocess

from primitive_map_pairs import LETTERS, decide, fold, verify_absence
from round10_ac_proof_blocks import marked_group
from round10_ac_disproof_outsider_quotient import (
    ALPHABETS,
    CHORDS,
    audit_controls,
    exact_cycle,
    graph_rank,
    principal_quotients,
    quotient_weights,
    ranked_outsiders,
    weight_of_loop,
)
from round11_ac_disproof_wirtinger import ROSE, verify_single_voltage
from round12_ac_disproof_energy20 import chord_data
from u_verify_voltage_phase import fold_relation, fold_word_arcs, voltage_word
from v_vertex_identification import fold_identification
from v_voltage_cycle_review import review


PAIR = ("XXYxYXXYxxy", "XXYXYxxyXyxxy")
TESTS = tuple(product(ALPHABETS, (0, 1)))
ROOT = Path(__file__).resolve().parents[1]


def exponent_vector(word, names):
    return [word.count(c) - word.count(c.upper()) for c in names]


def kernel_basis(rows):
    """A rational nullspace basis scaled to integer characters."""
    rows = [list(map(Fraction, row)) for row in rows]
    width = len(rows[0])
    pivots = []
    for column in range(width):
        rank = len(pivots)
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        divisor = rows[rank][column]
        rows[rank] = [entry / divisor for entry in rows[rank]]
        for i in range(len(rows)):
            if i != rank:
                multiple = rows[i][column]
                rows[i] = [x - multiple * y for x, y in zip(rows[i], rows[rank])]
        pivots.append(column)
    for j in range(width):
        if j in pivots:
            continue
        vector = [0] * width
        vector[j] = 1
        for i, pivot in enumerate(pivots):
            vector[pivot] = -rows[i][j]
        factor = lcm(*(Fraction(x).denominator for x in vector))
        yield tuple(int(x * factor) for x in vector)


def check_voltage(graph, pair, bound=4):
    basis, marked, arcs = chord_data(graph, pair)
    rank = len(basis)
    exponent_rows = [exponent_vector(w, CHORDS[:rank]) for w in marked]
    characters = tuple(kernel_basis(exponent_rows))
    supplied = {}
    combinations_ = sorted(product(range(-bound, bound + 1), repeat=len(characters)),
                           key=lambda v: (sum(map(abs, v)), v))
    for coefficients in combinations_:
        if not any(coefficients):
            continue
        character = tuple(sum(a * b for a, b in zip(coefficients, column))
                          for column in zip(*characters))
        weights = [0] * len(graph)
        for (vertex, label, _), (i, sign) in arcs.items():
            weights[4 * vertex + label] = sign * character[i]
        assert all(voltage_word(graph, weights, word) == 0 for word in pair)
        for check in review(graph, weights)["checks"]:
            key = (*check["alphabet"], check["forbidden_double"])
            if check["status"] == "PASS" and key not in supplied:
                count = verify_single_voltage(graph, weights, check)
                supplied[key] = {"character": character, "inequalities_checked": count, **check}
        if len(supplied) == len(TESTS):
            break
    return {"graph": graph, "chord_basis": basis, "source_in_chords": marked,
            "integer_character_basis": characters, "excluded_languages": len(supplied),
            "tests": [supplied[key] for key in sorted(supplied)]}


def first_ranks(graph):
    ranks = Counter()
    for a, b in combinations(range(len(graph) // 4), 2):
        folded, _ = fold_relation(graph, (a, b))
        assert tuple(folded) == fold_identification(graph, a, b)[0]
        ranks[graph_rank(folded)] += 1
    return dict(sorted(ranks.items()))


def native_images(executable, graph, *flags):
    request = " ".join(map(str, (len(graph) // 4, *graph))) + "\n"
    output = subprocess.check_output([executable, *flags], input=request, text=True)
    rows = [tuple(map(int, line.split())) for line in output.splitlines()]
    assert len(set(rows)) == len(rows)
    return set(rows), sha256(output.encode()).hexdigest()


def short_projection_checks():
    result = ROOT / "results/round13_stable_proof_whitehead.json"
    pairs = json.loads(result.read_text())["coverage32"]["shortest_absent"][:4]
    checks = []
    for pair in pairs:
        assert sum(map(len, pair)) == 23
        graph = fold(pair)
        assert fold_word_arcs(pair) == list(graph)
        ranks = first_ranks(graph)
        assert set(ranks) == {3}
        checks.append({"pair": pair, "first_identifications_by_rank": ranks,
                       "source_map_pair_absence": verify_absence(
                           decide(graph, save_certificate=True))})
    return checks


def frozen_receiver_check():
    x = (1, 3, 2, 5, 6, 4)
    y = (2, 4, 5, 3, 1, 6)
    image, identity, multiply, inverse, cycle_type = marked_group("symmetric", 6, x, y)
    receiver, frozen = PAIR
    assert image(frozen) == identity
    assert exponent_vector(frozen, "xy") == [0, 1]
    shape = cycle_type(image(receiver))
    assert cycle_type(inverse(image(receiver))) == shape
    values = []
    power = identity
    while True:
        candidate = multiply(x, power)
        candidate_shape = cycle_type(candidate)
        assert cycle_type(inverse(candidate)) == candidate_shape != shape
        values.append(candidate_shape)
        power = multiply(power, y)
        if power == identity:
            break
    return {"receiver": receiver, "fixed_donor": frozen, "x": x, "y": y,
            "receiver_cycle_type": shape, "power_period": len(values),
            "primitive_residue_cycle_types": values}


def main(executable, strict_verifier):
    original = fold(PAIR)
    assert fold_word_arcs(PAIR) == list(original)
    (a, b), (c, d) = [exponent_vector(word, "xy") for word in PAIR]
    assert abs(a * d - b * c) == 1
    source_check = verify_absence(decide(original, save_certificate=True))
    first_identifications = first_ranks(original)
    assert set(first_identifications) == {3}
    principal = principal_quotients(PAIR)
    ranks = Counter(map(graph_rank, principal))
    same_rank = sorted(graph for graph in principal if graph_rank(graph) == 2)
    assert set(same_rank) == {original, ROSE}
    outside_words = ranked_outsiders(PAIR, principal)
    compiled_full, compiled_digest = native_images(executable, original)
    compiled_ranked, compiled_ranked_digest = native_images(
        executable, original, "--rank-increasing")
    assert compiled_full == set(principal)
    assert compiled_ranked == set(outside_words)
    remaining = sorted(set(principal) - outside_words.keys() - {ROSE})
    exceptional = [check_voltage(graph, PAIR) for graph in remaining]
    digest = sha256()
    free_excluded = Counter()
    free_hits = []
    for graph, outsiders in sorted(outside_words.items()):
        if graph == original:
            continue
        marked = [*PAIR, *outsiders]
        rank = graph_rank(graph)
        assert fold(marked) == graph and len(marked) == rank
        weights, _ = quotient_weights(graph, marked)
        assert [weight_of_loop(graph, weights, word, 0) for word in marked] == [
            "", "", *CHORDS[2:rank]
        ]
        hits = [hit for alphabet, blocked in TESTS
                if (hit := exact_cycle(graph, weights, alphabet, blocked))]
        if hits:
            free_hits.append({"graph": graph, "outsiders": outsiders, "hits": hits})
        else:
            free_excluded[rank] += 1
        digest.update(json.dumps([graph, outsiders, weights, hits], separators=(",", ":")).encode()
                      + b"\n")
    certificate = ROOT / "certificates/round13_stable_proof_external_projection.jsonl"
    strict = json.loads(subprocess.check_output([strict_verifier, certificate], text=True))
    assert tuple(strict["final_words"]) == PAIR and strict["rank_peak"] == 3
    return {
        "pair": PAIR,
        "row_exponent_determinant": a * d - b * c,
        "strict_stable_replay": strict,
        "strict_stable_ledger_sha256": sha256(certificate.read_bytes()).hexdigest(),
        "source_vertices": len(original) // 4,
        "source_map_pair_absence": source_check,
        "first_identifications_by_rank": first_identifications,
        "principal_quotients_by_rank": dict(sorted(ranks.items())),
        "rank_two_principal_images": same_rank,
        "principal_quotients": len(principal),
        "independent_principal_enumeration": {
            "all_images": len(compiled_full), "all_images_sha256": compiled_digest,
            "rank_increasing_images": len(compiled_ranked),
            "rank_increasing_images_sha256": compiled_ranked_digest,
        },
        "free_quotient_exclusions_by_rank": dict(sorted(free_excluded.items())),
        "free_quotient_case_sha256": digest.hexdigest(),
        "free_quotient_neutral_cases": free_hits,
        "exceptional": exceptional,
        "all_proper_images_excluded": (
            not free_hits and all(r["excluded_languages"] == len(TESTS) for r in exceptional)
        ),
        "ak2_positive_control": audit_controls(),
        "short_generated_projection_checks": short_projection_checks(),
        "fixed_second_row_primitive_exclusion": frozen_receiver_check(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("principal_executable", type=Path)
    parser.add_argument("strict_verifier", type=Path)
    args = parser.parse_args()
    print(json.dumps(main(args.principal_executable.resolve(), args.strict_verifier.resolve()), indent=2))
