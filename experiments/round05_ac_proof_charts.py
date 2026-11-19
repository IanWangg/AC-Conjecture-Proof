"""Exact controls for ordinary AC projection through changing one-row charts."""

from collections import Counter
from itertools import permutations
import json
from pathlib import Path

from euclidean_primitive_audit import primitive_cyclic_word
from round02_ac_proof_controls import conjugate, invert, multiply
from round02_braid_kernel_lift import collect, power
from round03_ac_proof_controls import replay_between, substitute
from round04_chart_lifts import ONE, commutator, image_size, marked_value
from round03_frozen_donors import cycle_type
from round04_stable_proof_paths import replay as replay_rank_three
from stallings_search import apply, cyclic, inverse, reduce


ROOT = Path(__file__).resolve().parents[1]
WITNESS = ROOT / "certificates/round04_stable_proof_pivotless22.json"


def pivot_choices(rows):
    return [(i, a) for i, word in enumerate(map(cyclic, rows)) for a in "xyz"
            if word.count(a) + word.count(a.upper()) == 1]


def make_chart(word, axis, complement):
    pivot = cyclic(word)
    if axis not in pivot:
        pivot = inverse(pivot)
    assert pivot.count(axis) == 1 and axis.upper() not in pivot
    index = pivot.index(axis)
    solution = inverse(pivot[index + 1:] + pivot[:index])
    chart = {**complement, axis: substitute(solution, complement)}
    assert substitute(word, chart) == ""
    return chart


def conjugations(slot, word):
    return [conjugate(slot, a) for a in reversed(word)]


def add_inverse_powers(slot, donor, exponent):
    return [invert(donor), *[multiply(slot, donor) for _ in range(exponent)], invert(donor)]


def add_conjugate(slot, donor, word, negative):
    orientation = [invert(donor)] if negative else []
    return [*conjugations(donor, word), *orientation, multiply(slot, donor),
            *orientation, *conjugations(donor, inverse(word))]


def edge(first_image, second_image, retained):
    p = "z" + inverse(first_image)
    q = "x" + inverse(second_image)
    donor = reduce(inverse(p) + q)
    r = reduce(retained + p * 2 + q * 2)
    before = (p, donor, r)
    after = (q, donor, r)
    assert apply(before, multiply(0, 1)) == after
    assert pivot_choices(before) == [(0, "z")]
    assert pivot_choices(after) == [(0, "x")]
    return before, after


def project(rows, chart, slots=(1, 2)):
    return [substitute(rows[i], chart) for i in slots]


def positive_control():
    before, after = edge("xx", "zzyy", "yx")
    left = make_chart(before[0], "z", {"x": "x", "y": "y"})
    right = make_chart(after[0], "x", {"y": "y", "z": "XYY"})
    native_right = make_chart(after[0], "x", {"y": "y", "z": "x"})
    for chart in (left, right):
        assert project(("Xz", "y"), chart, (0, 1)) == ["x", "y"]
    assert project(("Xz", "y"), native_right, (0, 1)) == ["YYX", "y"]
    assert right == {"x": "XYYX", "y": "y", "z": "XYY"}
    start, target = project(before, left), project(after, right)
    assert all(not primitive_cyclic_word(cyclic(w)) for w in start + target)
    moves = [*add_inverse_powers(1, 0, 2), *conjugations(0, "XXX"),
             multiply(1, 0), *conjugations(0, "XYY"), *add_inverse_powers(1, 0, 2)]
    return {
        "edge_from": before, "edge_to": after, "common_lift": ["Xz", "y"],
        "left_chart": left, "right_chart": right, "projected_from": start,
        "projected_to": target, "moves": moves, "replay": replay_between(start, target, moves),
    }


def a5_spectra(words):
    even = [p for p in permutations(ONE)
            if sum(a > b for i, a in enumerate(p) for b in p[i + 1:]) % 2 == 0]
    generating = [(a, b) for a in even for b in even if image_size((a, b)) == 60]
    counts = []
    for word in words:
        spectrum = Counter()
        for a, b in generating:
            if marked_value(word, {"x": a, "y": b}) == ONE:
                spectrum[cycle_type(commutator(a, b))] += 1
        counts.append(spectrum)
    return len(generating), counts


def clear_with_y(start, changed_pivot):
    donor = start[0]
    power_moves = [multiply(1, 0), multiply(1, 0)] if changed_pivot else add_inverse_powers(1, 0, 2)
    assert replay_between(start, [donor, "y"], power_moves)["endpoint"] == [donor, "y"]
    target = "X" if changed_pivot else "x"
    moves = list(power_moves)
    for exponent, letter in collect(reduce(inverse(donor) + target), "x"):
        moves += add_conjugate(0, 1, power("x", exponent), letter.isupper())
    if changed_pivot:
        moves.append(invert(0))
    return moves


def negative_control():
    before, after = edge("x" + "y" * 31 + "X", "yyzz", "y")
    left = make_chart(before[0], "z", {"x": "x", "y": "y"})
    right = make_chart(after[0], "x", {"y": "y", "z": "x"})
    projections = project(before, left), project(after, right)
    assert all(not primitive_cyclic_word(cyclic(w)) for pair in projections for w in pair)
    count, spectra = a5_spectra([first for first, _ in projections])
    assert count == 2280 and spectra == [{(1, 1, 3): 120}, {(5,): 120}]
    ledgers = [clear_with_y(pair, i == 1) for i, pair in enumerate(projections)]
    return {
        "edge_from": before, "edge_to": after, "charts": [left, right],
        "projections": projections, "all_projected_rows_nonprimitive": True,
        "a5_generating_ordered_pairs": count,
        "commutator_cycle_types_killing_each_donor": [
            [{"cycle_type": cycle, "count": multiplicity} for cycle, multiplicity in sorted(spectrum.items())]
            for spectrum in spectra
        ],
        "ordinary_paths_to_basis": [
            {"moves": moves, "replay": replay_between(pair, ["x", "y"], moves)}
            for pair, moves in zip(projections, ledgers)
        ],
    }


def correct_changed_x(word):
    """Replace x by x*donor^-1, preserving the second row's donor slot."""
    moves = []
    for i, a in enumerate(word):
        if a.lower() == "x":
            # Right multiplication by inverse(suffix)*old_letter^-1*new_letter*suffix.
            conjugator = inverse(word[i + 1:])
            if a == "X":
                conjugator = reduce(conjugator + "x")
            moves += add_conjugate(1, 0, conjugator, a == "x")
    return moves


def ak3_descent():
    certificate = json.loads(WITNESS.read_bytes())
    padded_receipt = replay_rank_three(certificate)
    rows = tuple(certificate["start"])
    pivot, axis, complement = 2, "z", {"x": "x", "y": "y"}
    slots = [0, 1]
    chart = make_chart(rows[pivot], axis, complement)
    start = project(rows, chart, slots)
    ordinary = tuple(start)
    ledger, events = [], []
    for step, move in enumerate(certificate["moves"], 1):
        rows = apply(rows, move)
        receiver = move["i"]
        emitted = []
        if step == 218:
            # The changed row is a z pivot and an x pivot. The old z row
            # takes its donor slot in the projection, with inverted value.
            assert move == multiply(0, 2)
            pivot, slots = 0, [2, 1]
            new_z_chart = make_chart(rows[pivot], "z", complement)
            axis, complement = "x", {"y": "y", "z": new_z_chart["z"]}
            chart = make_chart(rows[pivot], axis, complement)
            assert chart == new_z_chart
            emitted = [invert(0)]
        elif step == 235:
            assert move == multiply(0, 2)
            target_chart = make_chart(rows[pivot], axis, complement)
            target_donor = substitute(rows[2], target_chart)
            assert target_donor == reduce("X" + inverse(ordinary[0]) + "x")
            assert chart["x"] == "x" and target_chart["x"] == reduce("x" + inverse(target_donor))
            assert set(rows[1]) <= set("xXyY")
            chart = target_chart
            emitted = [invert(0), conjugate(0, "X"), *correct_changed_x(rows[1])]
        elif receiver == pivot:
            chart = make_chart(rows[pivot], axis, complement)
        elif move["op"] == "conjugate":
            emitted = conjugations(slots.index(receiver), substitute(move["g"], chart))
        elif move["op"] == "invert":
            emitted = [invert(slots.index(receiver))]
        elif move["j"] != pivot:
            emitted = [multiply(slots.index(receiver), slots.index(move["j"]))]
        for operation in emitted:
            ordinary = apply(ordinary, operation)
        ledger.extend(emitted)
        assert substitute(rows[pivot], chart) == ""
        assert list(ordinary) == project(rows, chart, slots)
        if step in (218, 235):
            events.append({"rank_three_step": step, "padded_rows": rows, "chart": chart,
                           "ordinary_rows": ordinary, "compiled_moves": len(emitted)})
    transported = list(ordinary)
    native_chart = make_chart(rows[pivot], axis, {"y": "y", "z": "x"})
    target = project(rows, native_chart, slots)
    cleanup = [operation for slot in range(2) for operation in conjugations(slot, "YY")]
    projected_replay = replay_between(transported, target, cleanup)
    ledger.extend(cleanup)
    return {
        "padded_receipt": padded_receipt, "chart_events": events,
        "transported_marking_for_surviving_y_z": [chart["y"], chart["z"]],
        "transported_projection": transported, "terminal_marking_moves": projected_replay["moves"],
        "ordinary_certificate": {"format": "ordinary-ac-elementary-v1", "start": start,
                                 "target": target, "moves": ledger},
        "ordinary_replay": replay_between(start, target, ledger),
    }


def main():
    print(json.dumps({"compatible_forced_switch": positive_control(),
                      "incompatible_forced_switch": negative_control(),
                      "ak3_witness_descent": ak3_descent()}, indent=2))


if __name__ == "__main__":
    main()
