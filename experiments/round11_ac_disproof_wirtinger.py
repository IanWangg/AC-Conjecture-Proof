"""Replay proper-overgroup primitive exclusion and adjacent AK(2) controls."""

from collections import Counter
import hashlib
from itertools import product
import json
from pathlib import Path

from elementary_verify import replay
from euclidean_primitive_audit import primitive_cyclic_word
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
    substitute,
    weight_of_loop,
)
from u_verify_voltage_phase import automaton, voltage_word
from v_voltage_cycle_review import review


ROOT = Path(__file__).resolve().parents[1]
ROSE = fold(("x", "y"))
EXCEPTION_CHARACTERS = {
    (1, 1, 2, 2, 0, 0, 1, 1, 2, 2, 0, 0): ((-1, 0, 0, 1), (0, -3, 2, 1)),
    (1, 2, 1, 1, 2, 0, 0, 0, 0, 1, 2, 2): ((-1, -1, 2, 0), (-1, 2, 0, -2)),
}


def checked_certificate(filename):
    path = "certificates/" + filename
    certificate = json.loads((ROOT / path).read_text())
    return certificate, {"path": path, **replay(certificate)}


def signed_images(names, words):
    return dict(zip(names + names.upper(), (*words, *(inverse(w) for w in words))))


def kernel_witness(graph, rows, hit, marking_inverse):
    """Express a genuine cyclic primitive as a product of relator conjugates."""
    word, vertex = hit["word"], hit["vertex"]
    assert primitive_cyclic_word(word)
    assert follow(graph, vertex, word) == vertex
    paths, *_ = spanning(graph)
    based = reduce(paths[vertex] + word + inverse(paths[vertex]))
    chord_expression = chord_words(graph, [*rows[:-1], based])[0][-1]
    expression = substitute(chord_expression, marking_inverse)
    images = signed_images(CHORDS[:len(rows)], rows)
    assert substitute(expression, images) == based

    prefix = ""
    factored = []
    ambient_product = ""
    for letter in expression:
        if letter not in "aAbB":
            prefix = reduce(prefix + letter)
            continue
        conjugator = substitute(prefix, images)
        assert follow(graph, 0, conjugator) == 0
        factored.append({"row": "ab".index(letter.lower()), "sign": -1 if letter.isupper() else 1,
                         "conjugator": conjugator})
        ambient_product = reduce(ambient_product + conjugator + images[letter] + inverse(conjugator))
    assert prefix == ""
    assert ambient_product == based
    return {**hit, "base_path": paths[vertex], "based_primitive": based,
            "marked_basis_expression": expression, "normal_product": factored}


def verify_single_voltage(graph, weights, check):
    alphabet, blocked = tuple(check["alphabet"]), check["forbidden_double"]
    expected = automaton(graph, weights, alphabet, blocked)
    supplied = {frozenset(c["states"]): c for c in check["cyclic_components"]}
    assert len(supplied) == len(check["cyclic_components"])
    assert set(supplied) == {group for group, _ in expected}
    inequalities = 0
    for group, arcs in expected:
        component = supplied[group]
        sign = component["strict_cycle_voltage_sign"]
        assert sign in (-1, 1)
        assert len(component["states"]) == len(component["potential"]) == len(group)
        potentials = dict(zip(component["states"], component["potential"]))
        assert all(type(p) is int for p in potentials.values())
        for start, end, value in arcs:
            assert potentials[end] - potentials[start] <= len(group) * sign * value - 1
            inequalities += 1
    return inequalities


def exceptional_voltage(graph, base):
    assert graph_rank(graph) == 4 and len(graph) == 12 and min(graph) >= 0
    paths, chord_edges, arcs, _ = spanning(graph)
    chord_basis = [reduce(paths[a] + LETTERS[label] + inverse(paths[b]))
                   for a, label, b in chord_edges]
    coefficients = EXCEPTION_CHARACTERS[graph]
    required = {(x, y, blocked) for x, y, blocked in product((0, 1), (2, 3), (0, 1))}
    verified = {}
    combinations = sorted(product(range(-3, 4), repeat=2), key=lambda p: (sum(map(abs, p)), p))
    for first, second in combinations:
        if not (first or second):
            continue
        character = [first * a + second * b for a, b in zip(*coefficients)]
        weights = [0] * len(graph)
        for (a, label, _), (i, sign) in arcs.items():
            weights[4 * a + label] = sign * character[i]
        assert all(weights[4 * a + label] == -weights[4 * b + (label ^ 1)]
                   for a in range(len(graph) // 4) for label in range(4)
                   for b in [graph[4 * a + label]])
        assert all(voltage_word(graph, weights, word) == 0 for word in base)
        for check in review(graph, weights)["checks"]:
            case = (*check["alphabet"], check["forbidden_double"])
            if check["status"] == "PASS" and case not in verified:
                verified[case] = {
                    "chord_character": character,
                    "edge_voltages": weights,
                    "inequalities_verified": verify_single_voltage(graph, weights, check),
                    **check,
                }
        if verified.keys() == required:
            break
    assert verified.keys() == required
    marked, _ = chord_words(graph, [*base, *chord_basis[2:]])
    return {"chord_basis": chord_basis, "marked_rows_in_chord_basis": marked[:2],
            "checks": [verified[k] for k in sorted(verified)]}


def audit_fringe(base, exceptions=False):
    graph = fold(base)
    fringe = principal_quotients(base)
    assert {g for g in fringe if graph_rank(g) == 2} == {graph, ROSE}
    outsiders = ranked_outsiders(base, fringe)
    assert set(fringe) - {ROSE} - outsiders.keys() == (EXCEPTION_CHARACTERS.keys() if exceptions else set())
    cases = []
    for child in sorted(fringe, key=lambda g: (graph_rank(g), g)):
        rank = graph_rank(child)
        if child == ROSE:
            continue
        case = {"graph": child, "rank": rank}
        if child == graph:
            result = decide(graph, save_certificate=True)
            if result["status"] == "ABSENT":
                cases.append({**case, "status": "source_excluded", "absence": verify_absence(result)})
                continue
        if child not in outsiders:
            cases.append({**case, "status": "voltage_excluded", "voltage": exceptional_voltage(child, base)})
            continue
        added = outsiders[child]
        rows = [*base, *added]
        assert len(rows) == rank and fold(rows) == child
        weights, expressions = quotient_weights(child, rows)
        assert [weight_of_loop(child, weights, word, 0) for word in rows] == ["", "", *CHORDS[2:rank]]
        hits = [hit for alphabet, blocked in product(ALPHABETS, (0, 1))
                if (hit := exact_cycle(child, weights, alphabet, blocked))]
        primitive = next((hit for hit in hits if primitive_cyclic_word(hit["word"])), None)
        status = "free_excluded" if not hits else "primitive" if primitive else "neutral_unresolved"
        cases.append({**case, "status": status, "outsiders": added,
                      "inverse_marking": [expressions[c] for c in CHORDS[:rank]],
                      "witness": kernel_witness(child, rows, primitive, expressions) if primitive else None,
                      "neutral_cyclic_paths": hits})
    return cases


def summarize(base, cases):
    return {
        "pair": base,
        "source_vertices": len(fold(base)) // 4,
        "rank_histogram_including_ambient_rose": dict(sorted(Counter([2, *(c["rank"] for c in cases)]).items())),
        "proper_cases_by_rank_and_status": {
            rank: dict(sorted(Counter(c["status"] for c in cases if c["rank"] == rank).items()))
            for rank in sorted({c["rank"] for c in cases})
        },
        "case_sha256": hashlib.sha256(json.dumps(cases, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "source": next(c for c in cases if c["rank"] == 2),
        "exceptional_covers": [c for c in cases if c["status"] == "voltage_excluded"],
        "example_primitive_in_strict_proper_overgroup": next(
            (c for c in cases if c["rank"] > 2 and c["status"] == "primitive"), None),
    }


def run():
    wrong, wrong_entry = checked_certificate("round10_stable_proof_wirtinger_wrong.json")
    corrected, corrected_exit = checked_certificate("round10_stable_proof_wirtinger_correct.json")
    ak2, ak2_exit = checked_certificate("n_ak2_cyclic13.json")
    assert ak2["moves"][:2] == [{"op": "invert", "i": 0}, {"op": "conjugate", "i": 0, "g": "Y"}]
    ak2_base = ak2["start"]
    adjacent = [reduce("Y" + inverse(ak2_base[0]) + "y"), ak2_base[1]]
    suffix = replay(dict(ak2, start=adjacent, moves=ak2["moves"][2:]))
    assert wrong_entry["moves"] == 105 and corrected_exit["moves"] == 73 and suffix["moves"] == 44
    inputs = {"wrong_wirtinger": wrong["target"], "corrected_wirtinger": corrected["start"],
              "ak2_initial": ak2_base, "ak2_after_two_moves": adjacent}
    fringes = {name: audit_fringe(base, exceptions=name == "wrong_wirtinger") for name, base in inputs.items()}
    for name in ("wrong_wirtinger", "ak2_after_two_moves"):
        assert all(c["status"].endswith("_excluded") for c in fringes[name])
    assert all(c["status"] == "primitive" for c in fringes["corrected_wirtinger"])
    result = {name: summarize(base, fringes[name]) for name, base in inputs.items()}
    corrected_first, corrected_second = corrected["start"]
    assert reduce(inverse(corrected_first) + corrected_second) == "yyXYYxyyxYY"
    assert result["corrected_wirtinger"]["source"]["witness"]["based_primitive"] == "yyXYYxyyxYY"

    positive = result["ak2_initial"]["example_primitive_in_strict_proper_overgroup"]
    primitive = positive["witness"]["based_primitive"]
    outside, = positive["outsiders"]
    assert (outside, primitive) == ("xYX", "yyXyyXyX")
    strict_moves = [{"op": "invert", "i": 0}, {"op": "multiply", "i": 1, "j": 0},
                    *({"op": "conjugate", "i": 1, "g": g} for g in reversed(outside)),
                    {"op": "multiply", "i": 0, "j": 1}]
    right = reduce(outside + ak2_base[1] + inverse(ak2_base[0]) + inverse(outside))
    primitive_replay = replay(dict(ak2, target=[primitive, right], moves=strict_moves))
    initial_plus_y = fold([*ak2_base, "Y"])
    assert initial_plus_y == fold([*adjacent, "y"]) != ROSE
    assert fold([*adjacent, "y", outside]) == ROSE
    return {
        "ordinary_AC_goal_solved": False, "fringes": result,
        "ordinary_replays": {"wrong_wirtinger_entry": wrong_entry, "corrected_wirtinger_exit": corrected_exit,
                             "ak2_full_exit": ak2_exit, "ak2_after_two_moves_exit": suffix,
                             "ak2_primitive_exposure": {**primitive_replay, "elementary_moves": strict_moves}},
        "ak2_barrier_transition": {
            "last_move": ak2["moves"][1],
            "proper_common_overgroup": initial_plus_y,
            "primitive_exposure_macro_conjugator": outside,
            "from_exclusion_side_with_both_conjugators": ROSE,
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
