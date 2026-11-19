"""Synchronize the two finite witnesses while preserving the braid relation-module image."""

import argparse
import hashlib
import json
from pathlib import Path

from elementary_verify import inverse, reduce, replay
from round03_frozen_donors import evaluate, matrix_inv, matrix_mul, perm_inv, perm_mul

MATRIX_ONE = (1, 0, 0, 1)
PERMUTATION_ONE = (1, 2, 3, 4, 5)
ONE = (MATRIX_ONE, PERMUTATION_ONE)
MARKS = (
    ((0, 1, 10, 5), (1, 2, 4, 5, 3)),
    ((0, 2, 5, 1), (3, 4, 2, 5, 1)),
)
MULTIPLY = (matrix_mul, perm_mul)
INVERT = (matrix_inv, perm_inv)
BRAID = "xyxYXY"
SOURCE = Path(__file__).resolve().parents[1] / "certificates/optimized_first_order_strict.json"


def product(a, b):
    return matrix_mul(a[0], b[0]), perm_mul(a[1], b[1])


def value(word):
    return tuple(
        evaluate(
            word, tuple(mark[factor] for mark in MARKS), ONE[factor],
            MULTIPLY[factor], INVERT[factor],
        )
        for factor in range(2)
    )


def commutator(a, b):
    return reduce(a + b + inverse(a) + inverse(b))


def lift_generators():
    # These three words are explicit elements of [N,N].
    return [
        commutator(BRAID, reduce(letter + BRAID + inverse(letter)))
        for letter in ("x", "y", "X")
    ]


def lifts(generators):
    """Find one word for each element in the finite image of the lift words."""
    signed = generators + [inverse(g) for g in generators]
    actions = [(value(word), word) for word in signed]
    seen = {ONE: ""}
    queue = [ONE]
    for state in queue:
        for action, word in actions:
            successor = product(state, action)
            if successor not in seen:
                seen[successor] = reduce(seen[state] + word)
                queue.append(successor)
    return seen


def check_commutator_classes(table, component):
    """Every noncentral donor generates the factor by commutator updates."""
    group = {image[component] for image in table}
    remaining = set(group)
    identity = ONE[component]
    mul, inv = MULTIPLY[component], INVERT[component]
    classes = central = 0
    while remaining:
        donor = min(remaining)
        orbit = {mul(mul(g, donor), inv(g)) for g in group}
        remaining.difference_update(orbit)
        classes += 1
        if len(orbit) == 1:
            central += 1
            continue
        actions = {mul(conjugate, inv(donor)) for conjugate in orbit}
        seen, queue = {identity}, [identity]
        for state in queue:
            for action in actions:
                successor = mul(state, action)
                if successor not in seen:
                    seen.add(successor)
                    queue.append(successor)
            if len(seen) == len(group):
                break
        assert seen == group
    return {"factor_order": len(group), "conjugacy_classes": classes, "central_classes": central}


def correction_factors(table, component, donor, difference):
    """Factor a desired correction using commutators with the donor."""
    identity = ONE[component]
    mul, inv = MULTIPLY[component], INVERT[component]
    actions = {}
    for image, g in table.items():
        if image[1 - component] != ONE[1 - component]:
            continue
        conjugator = image[component]
        action = mul(mul(mul(conjugator, donor), inv(conjugator)), inv(donor))
        if action not in actions or len(g) < len(actions[action]):
            actions[action] = g
    queue = [identity]
    seen = {identity: (None, None)}
    for current in queue:
        if current == difference:
            break
        for action, g in actions.items():
            successor = mul(current, action)
            if successor not in seen:
                seen[successor] = current, g
                queue.append(successor)
    assert difference in seen
    factors = []
    while difference != identity:
        difference, g = seen[difference]
        factors.append(g)
    return list(reversed(factors))


def operations(recipient, conjugator):
    donor = 1 - recipient
    return (
        [{"op": "conjugate", "i": donor, "g": c} for c in reversed(conjugator)]
        + [{"op": "multiply", "i": recipient, "j": donor}]
        + [{"op": "conjugate", "i": donor, "g": c} for c in reversed(inverse(conjugator))]
        + [
            {"op": "invert", "i": donor},
            {"op": "multiply", "i": recipient, "j": donor},
            {"op": "invert", "i": donor},
        ]
    )


def apply_corrections(words, table):
    images = [value(word) for word in words]
    moves, receipts = [], []
    # Give V a noncentral matrix component first. Then fix U before V in A5.
    for recipient, component in ((1, 0), (0, 0), (0, 1), (1, 1)):
        mul, inv = MULTIPLY[component], INVERT[component]
        donor = 1 - recipient
        goal = MARKS[recipient][component]
        difference = mul(inv(images[recipient][component]), goal)
        factors = correction_factors(table, component, images[donor][component], difference)
        start = len(moves)
        for g in factors:
            words[recipient] = reduce(words[recipient] + commutator(g, words[donor]))
            moves.extend(operations(recipient, g))
        new_image = value(words[recipient])
        assert new_image[component] == goal
        assert new_image[1 - component] == images[recipient][1 - component]
        images[recipient] = new_image
        receipts.append({
            "recipient": recipient,
            "component": component,
            "conjugators_in_braid_derived_subgroup": factors,
            "strict_moves": len(moves) - start,
            "free_endpoint_lengths": list(map(len, words)),
        })
    assert tuple(images) == MARKS
    return moves, receipts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    data = SOURCE.read_bytes()
    prefix = json.loads(data)
    initial = replay(prefix)
    generators = lift_generators()
    table = lifts(generators)
    assert len(table) == 1320 * 60
    factor_audits = [check_commutator_classes(table, factor) for factor in range(2)]
    words = initial["endpoint"].copy()
    extra, receipts = apply_corrections(words, table)
    certificate = {
        "format": "ordinary-ac-elementary-v1",
        "start": prefix["start"],
        "target": words,
        "moves": prefix["moves"] + extra,
    }
    final = replay(certificate)
    args.certificate.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps({
        "prefix_sha256": hashlib.sha256(data).hexdigest(),
        "image_of_braid_derived_subgroup_size": len(table),
        "braid_derived_subgroup_lift_generators": generators,
        "finite_factor_commutator_audits": factor_audits,
        "phases": receipts,
        "strict_moves": final["moves"],
        "raw_peak": final["peak_total_length"],
        "free_endpoint_lengths": list(map(len, words)),
        "both_finite_images_match_marked_basis": True,
        "braid_relation_module_image_matches_marked_basis": True,
    }, indent=2))


if __name__ == "__main__":
    main()
