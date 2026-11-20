"""Replay the corrected published AK(3) connection and test a frozen repair."""

import argparse
from collections import Counter
from io import BytesIO
from itertools import product
import json
from pathlib import Path

from elementary_verify import replay as replay_pair
from euclidean_primitive_audit import primitive_cyclic_word
from free_waypoint_search import conj_ops, normalize
from round03_frozen_donors import cycle_type, perm_inv, perm_mul
from round03_stable_proof_pivot import canonical, cyclic, exponent
from round04_chart_screen import chart_projections
from round04_stable_proof_blocks import cyclic_cover_obstruction
from round04_stable_proof_paths import edge, replay as replay_triple
from round05_stable_proof_chartless import minima, whitehead_image
from round06_stable_proof_strict_escape import StrictPath
from round08_ac_proof_two_donors import reverse_moves
from round09_stable_proof_rank_three_chart import (
    IDENTITY, START, apply_marking, basic_ledger, compose, shear, transport,
)
from stallings_search import apply, inverse, reduce


# Shehper et al., arXiv:2408.15332v2, Appendices B and F.
MACROS = (
    9, 7, 4, 8, 11, 5, 11, 9, 3, 10, 12, 7, 7, 9, 11, 5, 3, 5,
    4, 3, 12, 5, 7, 7, 1, 9, 11, 8, 3, 5, 10, 2, 6, 12, 9, 7,
    5, 11, 10, 3, 8, 11, 9, 2, 10, 12, 5, 7, 9, 11, 1, 9, 8,
)
MULTIPLICATIONS = {1: (1, 0, 1), 2: (0, 1, -1), 3: (1, 0, -1), 4: (0, 1, 1)}
CONJUGATIONS = {5: (1, "X"), 6: (0, "Y"), 7: (1, "Y"), 8: (0, "x"),
                9: (1, "x"), 10: (0, "y"), 11: (1, "y"), 12: (0, "X")}
PUBLISHED_PAIR = ["XYxYXyxYYxyXy", "YXyyXYxyxYYx"]
DEFINITIONS = dict(zip("abcdefghijklmn", (
    "jnJ", "Jaj", "Aba", "Fcf", "ldL", "Geg", "Dfd", "agA", "Khk",
    "niN", "Bjb", "Aka", "elE", "amA",
)))
# In the numbered Wirtinger diagram, x5, x7 and x12 are x, y and z.
FAMILY_MARK = str.maketrans("eglEGL", "xyzXYZ")
S5 = ((5, 4, 2, 1, 3), (2, 3, 4, 5, 1), (2, 4, 1, 5, 3))
MERIDIAN_S5 = ((5, 2, 3, 1, 4), (1, 2, 5, 3, 4), (1, 5, 2, 4, 3))
MERIDIAN_S6 = ((6, 5, 4, 3, 1, 2), (2, 1, 4, 5, 6, 3), (5, 4, 1, 2, 6, 3))
MERIDIAN_MATRICES = {
    "XXy": (5, (0, 4, 1, 1), (0, 1, 4, 1)),
    "XXYxyxY": (11, (0, 10, 1, 2), (0, 7, 3, 2)),
    "XXYXyxyXYxyxYXyXYxy": (11, (0, 10, 1, 2), (0, 7, 3, 2)),
}


def commutator(a, b):
    return reduce(a + b + inverse(a) + inverse(b))


def three_row_source():
    c = commutator("Y", "X")
    return [reduce("Xz" + commutator(c, "z")),
            reduce("Yx" + commutator(c, "Z") + commutator("Z", "x")), "Xyz"]


def invert(i):
    return dict(op="invert", i=i)


def factor(recipient, donor, sign, conjugator):
    edit = [invert(donor)] if sign == -1 else []
    edit.extend(conj_ops(donor, conjugator))
    edit.append(dict(op="multiply", i=recipient, j=donor))
    edit.extend(conj_ops(donor, inverse(conjugator)))
    if sign == -1:
        edit.append(invert(donor))
    return edit


def history_pair_certificate():
    moves = []
    for instruction in MACROS:
        if instruction in MULTIPLICATIONS:
            i, j, sign = MULTIPLICATIONS[instruction]
            moves.extend(factor(i, j, sign, ""))
        else:
            i, g = CONJUGATIONS[instruction]
            moves.extend(conj_ops(i, g))
    proof = dict(format="ordinary-ac-elementary-v1", start=PUBLISHED_PAIR,
                 target=list(START[:2]), moves=moves)
    return proof


def literal_clearing(start, letter, donor):
    assert start[donor] == letter
    rows = tuple(start)
    moves = []
    for i in range(len(rows)):
        if i == donor:
            continue
        while letter in rows[i].lower():
            row = rows[i]
            where = row.lower().index(letter)
            sign = -1 if row[where] == letter else 1
            suffix = row[where + 1:]
            for move in factor(i, donor, sign, inverse(suffix)):
                rows = apply(rows, move)
                moves.append(move)
            assert rows[i] == reduce(row[:where] + suffix)
    return rows, moves


def history_rank_three(pair_proof):
    final = three_row_source()
    chart = ("x", "y", "Yxz")
    transformed = [apply_marking(row, chart) for row in final]
    projected, clear = literal_clearing(transformed, "z", 2)
    lifted = list(reverse_moves(pair_proof["moves"]))
    active = (*pair_proof["start"], "z")
    for i in range(2):
        active, ops = normalize(active, i, projected[i])
        lifted.extend(ops)
    assert active == projected
    lifted.extend(reverse_moves(clear))
    with BytesIO() as sink:
        path = StrictPath(START[:2], sink)
        path.add(dict(op="stabilize", generator="z"))
        undo = IDENTITY
        for change in (shear("z", "y", True), shear("z", "X", True)):
            transport(path, basic_ledger(change), undo)
            undo = compose(undo, change)
        assert compose(undo, chart) == IDENTITY
        transport(path, lifted, undo)
        assert path.rows == final
        moves = [json.loads(line) for line in sink.getvalue().splitlines()[2:]]
        certificate = dict(format="rank-three-ac-elementary-v1", start=START,
                           target=final, maximum_cyclic_length=path.cyclic_peak, moves=moves)
    return certificate


def substitute(word, letter, image):
    back = inverse(image)
    return reduce("".join(image if c == letter else back if c == letter.upper() else c for c in word))


def eliminate(donors, key, letter, observed):
    word = cyclic(donors[key])
    assert word.lower().count(letter) == 1
    if letter in word:
        word = inverse(word)
    position = word.index(letter.upper())
    image = word[position + 1:] + word[:position]
    residual = {j: substitute(row, letter, image) for j, row in donors.items() if j != key}
    tracked = [substitute(row, letter, image) for row in observed]
    return residual, tracked, dict(relator=key, generator=letter, image=image)


def explicit_wrong_elimination():
    donors = {g: g.upper() + row for g, row in DEFINITIONS.items() if g != "l"}
    donors["w"] = "Egl"
    donors["b"] = substitute(donors["b"], "a", DEFINITIONS["a"])
    assert donors["b"] == "Bn"
    trace = []
    for letter, key in zip("nkimhdcfjba", "bkimhdcfjna"):
        if letter == "k":
            assert donors["j"] == "JbiB"
            donors["k"] = substitute(donors["k"], "j", "biB")
            assert donors["k"] == "Ki"
        donors, _, step = eliminate(donors, key, letter, ())
        trace.append(step)
    marked = tuple(row.translate(FAMILY_MARK) for row in donors.values())
    assert sorted(map(canonical, marked)) == sorted(map(canonical, three_row_source()))
    return dict(eliminations=trace, rank_three_rows=marked)


def permutation_evaluator(marks):
    images = dict(zip("xyzXYZ", (*marks, *map(perm_inv, marks))))

    def evaluate(word):
        value = tuple(range(1, len(marks[0]) + 1))
        for c in word:
            value = perm_mul(value, images[c])
        return value

    return evaluate


def frozen_repair():
    donors = {g: g.upper() + row for g, row in DEFINITIONS.items() if g not in "lm"}
    donors["w"] = "Egl"
    observed = ["MelE", "MdlD"]
    trace = []
    for key, letter in (("w", "e"), ("c", "c"), ("h", "h"), ("i", "i"), ("b", "b"),
                        ("f", "f"), ("n", "m"), ("k", "k"), ("a", "n"), ("e", "d"), ("j", "g")):
        donors, observed, step = eliminate(donors, key, letter, observed)
        trace.append(step)
    rename = str.maketrans("ajlAJL", "xyzXYZ")
    fixed = tuple(row.translate(rename) for row in donors.values())
    observed = tuple(row.translate(rename) for row in observed)
    evaluate = permutation_evaluator(S5)
    assert all(evaluate(row) == (1, 2, 3, 4, 5) for row in fixed)
    outputs = list(map(evaluate, observed))
    cycles = list(map(cycle_type, outputs))
    assert cycles == [(5,), (1, 1, 3)]
    fox, weights, omit, polynomial = cyclic_cover_obstruction(fixed)
    assert fox
    minima_fixed, descent, *_ = minima(fixed)
    projected = []
    for row in observed:
        marked = (*fixed, row)
        for step in descent:
            marked = whitehead_image(marked, step["multiplier"], step["cut"])
        assert marked[:2] == minima_fixed and marked[0] == "X"
        (pair,) = [pair for e, pivot, pair in chart_projections(marked) if (e, pivot) == ("x", "X")]
        projected.append(pair)
    return dict(eliminations=trace, fixed_rows=fixed, wrong_and_corrected_row=observed,
                generator_images_s5=dict(zip("xyz", S5)), target_images_s5=outputs, target_cycle_types=cycles,
                fox_weights=weights, fox_omitted_column=omit, fox_determinant=polynomial,
                fixed_joint_minimum=minima_fixed, fixed_whitehead_descent=descent,
                wrong_and_corrected_rank_two_pairs=projected)


def matrix_witness(relator, source, target):
    p, *marks = MERIDIAN_MATRICES[target]
    identity = (1, 0, 0, 1)

    def multiply(a, b):
        return tuple(value % p for value in (a[0]*b[0] + a[1]*b[2], a[0]*b[1] + a[1]*b[3],
                                               a[2]*b[0] + a[3]*b[2], a[2]*b[1] + a[3]*b[3]))

    inverted = [(d, -b % p, -c % p, a) for a, b, c, d in marks]
    assert all(multiply(a, b) == identity for a, b in zip(marks, inverted))
    images = dict(zip("xyXY", (*marks, *inverted)))

    def evaluate(word):
        result = identity
        for c in word:
            result = multiply(result, images[c])
        return result

    assert evaluate(relator) == identity
    old, new = map(evaluate, (source, target))
    traces = (old[0]+old[3]) % p, (new[0]+new[3]) % p
    assert traces[0] != traces[1]
    return dict(prime=p, marking=dict(zip("xy", marks)), source_trace=traces[0], target_trace=traces[1])


def frozen_extra_relator():
    a, b, old = three_row_source()
    assert [exponent(a), exponent(b)] == [[-1, 0, 1], [1, -1, 0]]
    evaluate = permutation_evaluator(MERIDIAN_S5)
    assert all(evaluate(row) == (1, 2, 3, 4, 5) for row in (a, b))
    source_cycle = cycle_type(evaluate(old))
    assert source_cycle == (5,) and all(cycle_type(evaluate(g)) == (1, 1, 3) for g in "xyz")
    counts = Counter()
    seen = set()
    hits = {}
    for length in (1, 3, 5, 7):
        for letters in product("xXyYzZ", repeat=length):
            if not any(letters.count(g)+letters.count(g.upper()) == 1 for g in "xyz"):
                continue
            if abs(sum(1 if c.islower() else -1 for c in letters)) != 1:
                continue
            word = "".join(letters)
            if cyclic(word) != word:
                continue
            word = canonical(word)
            if word in seen:
                continue
            seen.add(word)
            counts["literal_unit_height_cyclic_words"] += 1
            if cycle_type(evaluate(word)) != source_cycle:
                continue
            counts["passing_initial_cycle_type"] += 1
            for eliminated, pivot, pair in chart_projections((a, b, word)):
                if pivot == word and any(map(primitive_cyclic_word, pair)):
                    hits.setdefault(word, []).append(dict(eliminated=eliminated, pair=pair))
    (unit,), moves, *_ = minima((b,))
    assert unit == "Y"
    names = str.maketrans("xzXZ", "xyXY")

    def quotient(word):
        for move in moves:
            (word,) = whitehead_image((word,), move["multiplier"], move["cut"])
        return canonical(word.replace("y", "").replace("Y", "").translate(names))

    fixed, removed, baseline = map(quotient, (a, b, old))
    assert not removed
    second_evaluation = permutation_evaluator(MERIDIAN_S6)
    assert all(second_evaluation(row) == (1, 2, 3, 4, 5, 6) for row in (a, b))
    assert cycle_type(second_evaluation(old)) == (1, 1, 2, 2)
    assert all(cycle_type(second_evaluation(word)) == (1, 5) for word in hits)
    return dict(generator_images_s5=dict(zip("xyz", MERIDIAN_S5)), extra_relator_image_s5=evaluate(old),
                generator_images_s6=dict(zip("xyz", MERIDIAN_S6)), extra_relator_image_s6=second_evaluation(old),
                **counts, second_fixed_row_whitehead_descent=moves, surviving_fixed_relator=fixed,
                baseline_extra_relator=baseline,
                candidates=[dict(word=word, literal_charts=charts, projected_word=quotient(word),
                                 image_s6=second_evaluation(word),
                                 separating_witness=matrix_witness(fixed, baseline, quotient(word)))
                            for word, charts in sorted(hits.items())])


def wrong_pair_certificate(route, wrong_pair):
    cap = route["cyclic_cap"]
    rows = START[:2]
    moves = []
    for i in range(2):
        rows, steps = normalize(rows, i, canonical(rows[i]))
        moves.extend(steps)
    assert tuple(sorted(rows)) == tuple(route["route"][0])
    for point in route["route"][1:]:
        rows, steps = edge(rows, tuple(point), cap, "xXyY")
        moves.extend(steps)
    assert tuple(sorted(rows)) == wrong_pair
    return dict(format="ordinary-ac-elementary-v1", start=list(START[:2]),
                target=list(rows), moves=moves)


def correct_pair_certificate(correct_pair):
    rows = correct_pair
    moves = factor(0, 1, -1, "")
    for move in moves:
        rows = apply(rows, move)
    rows, steps = normalize(rows, 0, "x")
    moves.extend(steps)
    rows, steps = literal_clearing(rows, "x", 0)
    moves.extend(steps)
    rows, steps = normalize(rows, 1, "y")
    moves.extend(steps)
    assert rows == ("x", "y")
    return dict(format="ordinary-ac-elementary-v1", start=list(correct_pair),
                target=list(rows), moves=moves)


def cyclic_peak(proof):
    rows = tuple(proof["start"])
    peak = sum(len(cyclic(row)) for row in rows)
    for move in proof["moves"]:
        rows = apply(rows, move)
        peak = max(peak, sum(len(cyclic(row)) for row in rows))
    return peak


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rank_two_certificate", type=Path)
    parser.add_argument("rank_three_certificate", type=Path)
    parser.add_argument("wrong_pair_route", type=Path)
    parser.add_argument("wrong_pair_certificate", type=Path)
    parser.add_argument("correct_pair_certificate", type=Path)
    args = parser.parse_args()
    pair = history_pair_certificate()
    triple = history_rank_three(pair)
    rank_two = replay_pair(pair)
    rank_three = replay_triple(triple)
    reconstruction = explicit_wrong_elimination()
    repair = frozen_repair()
    wrong, correct = repair["wrong_and_corrected_rank_two_pairs"]
    wrong_proof = wrong_pair_certificate(json.loads(args.wrong_pair_route.read_text()), wrong)
    correct_proof = correct_pair_certificate(correct)
    repair["wrong_pair_ordinary_replay"] = dict(**replay_pair(wrong_proof), cyclic_peak=cyclic_peak(wrong_proof))
    repair["correct_pair_ordinary_replay"] = dict(**replay_pair(correct_proof), cyclic_peak=cyclic_peak(correct_proof))
    args.rank_two_certificate.write_text(json.dumps(pair, indent=2) + "\n")
    args.rank_three_certificate.write_text(json.dumps(triple, indent=2) + "\n")
    args.wrong_pair_certificate.write_text(json.dumps(wrong_proof, indent=2) + "\n")
    args.correct_pair_certificate.write_text(json.dumps(correct_proof, indent=2) + "\n")
    print(json.dumps(dict(published_macros=len(MACROS), rank_two_replay=rank_two, rank_three_replay=rank_three,
                          wrong_elimination_reconstruction=reconstruction, frozen_repair=repair,
                          frozen_extra_relator=frozen_extra_relator()), indent=2))
