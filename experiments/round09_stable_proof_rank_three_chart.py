"""Compile an intrinsic chart into strict AC moves with maximum rank three."""

import argparse
from functools import cache
from io import BytesIO
import json
from pathlib import Path

from free_waypoint_search import conj_ops, normalize
from round03_stable_proof_pivot import canonical
from round04_stable_proof_paths import replay
from round05_stable_proof_chartless import minima
from round06_stable_proof_strict_escape import StrictPath, initial_proofs, letters_as_factors
from stallings_search import inverse, reduce

LETTERS = "xyz"
START = ("xxxYYYY", "xyxYXY", "z")
IDENTITY = tuple(LETTERS)


def apply_marking(word, marking):
    images = dict(zip(LETTERS + LETTERS.upper(), marking + tuple(map(inverse, marking))))
    return reduce("".join(images[letter] for letter in word))


def shear(recipient, donor, left=False):
    replacement = donor + recipient if left else recipient + donor
    return tuple(replacement if letter == recipient else letter for letter in LETTERS)


def compose(first, second):
    return tuple(apply_marking(word, first) for word in second)


INVERT_Z = ("x", "y", "Z")


def swap_with_z(letter):
    steps = (
        shear(letter, "z", True),
        shear("z", letter.upper(), True),
        shear(letter, "z"),
        INVERT_Z,
    )
    check = IDENTITY
    for step in steps:
        check = compose(check, step)
    assert check == tuple(letter if g == "z" else "z" if g == letter else g for g in LETTERS)
    return steps


def expand_shear(recipient, donor, left, use_commutator):
    if "z" in (recipient, donor.lower()):
        return [shear(recipient, donor, left)]
    if use_commutator:
        return [shear("z", donor, not left), shear(recipient, "z", left),
                shear("z", inverse(donor), not left), shear(recipient, "Z", left)]
    substitute = "Z" if donor.isupper() else "z"
    swap = swap_with_z(donor.lower())
    return [*swap, shear(recipient, substitute, left), *swap]


def whitehead_factors(move, use_commutator):
    multiplier, side = move["multiplier"], move["cut"]
    factors = []
    marking = IDENTITY
    for letter in LETTERS:
        if letter == multiplier.lower():
            continue
        if letter in side:
            factors.extend(expand_shear(letter, multiplier, True, use_commutator))
            marking = compose(marking, shear(letter, multiplier, True))
        if letter.upper() in side:
            factors.extend(expand_shear(letter, inverse(multiplier), False, use_commutator))
            marking = compose(marking, shear(letter, inverse(multiplier)))
    composed = IDENTITY
    for factor in factors:
        composed = compose(composed, factor)
    assert composed == marking
    return factors


def renaming_to_delete(eliminated):
    if eliminated == "x":
        return [*swap_with_z("x"), *swap_with_z("y")]
    if eliminated == "y":
        return list(swap_with_z("y"))
    return []


def literal_shears(word, eliminated, use_commutator):
    assert word.lower().count(eliminated) == 1
    position = word.lower().index(eliminated)
    tail = word[position + 1:] + word[:position]
    left = word[position].isupper()
    factors = []
    for donor in tail[::-1] if left else inverse(tail):
        factors.extend(expand_shear(eliminated, donor, left, use_commutator))
    return factors


@cache
def basic_ledger(marking):
    """Compile one interaction with the initially isolated spare generator."""
    with BytesIO() as sink:
        path = StrictPath(START[:2], sink)
        path.add({"op": "stabilize", "generator": "z"})
        if marking == INVERT_Z:
            path.add({"op": "invert", "i": 2})
        elif marking[2] != "z":
            x, y, changed_z = marking
            assert (x, y) == ("x", "y") and len(changed_z) == 2
            old_letter = changed_z.replace("z", "")
            correction = reduce("Z" + changed_z)
            factors = letters_as_factors(old_letter, initial_proofs(path.rows))
            if changed_z[0] != "z":
                factors = [(i, sign, reduce("Z" + word)) for i, sign, word in factors]
            path.append_normal_product(2, correction, factors)
        else:
            (letter,) = [g for g, value in zip(LETTERS, marking) if g != value]
            index = LETTERS.index(letter)
            substitution = {letter: marking[index], letter.upper(): inverse(marking[index])}
            for i, word in enumerate(START[:2]):
                expression = list(word)
                for j in range(len(word) - 1, -1, -1):
                    if word[j] not in substitution:
                        continue
                    replacement = substitution[word[j]]
                    correction = reduce(inverse(word[j]) + replacement)
                    core = correction.lower().index("z")
                    sign = 1 if correction[core] == "z" else -1
                    h = correction[:core]
                    assert correction[core + 1:] == inverse(h)
                    suffix = reduce("".join(expression[j + 1:]))
                    path.factor(i, 2, sign, reduce(inverse(suffix) + h))
                    expression[j] = replacement
                    assert path.rows[i] == reduce("".join(expression))
        assert path.rows == [apply_marking(word, marking) for word in START]
        return tuple(json.loads(line) for line in sink.getvalue().splitlines()[2:])


def transport(path, moves, marking):
    for move in moves:
        if move["op"] == "conjugate":
            path.extend(conj_ops(move["i"], apply_marking(move["g"], marking)))
        else:
            assert move["op"] in {"multiply", "invert"}
            path.add(move)


def compile_chart(prefix, pivot_slot, sink, literal=None, use_commutator=True):
    assert tuple(prefix["start"]) == START
    original = replay(prefix)["target"]
    assert pivot_slot in range(len(START))
    source_pivot = original[pivot_slot]
    if literal is None:
        (minimum,), descent, _, _, _ = minima((source_pivot,))
        if len(minimum) != 1:
            raise ValueError("specified relator is not primitive")
        eliminated = minimum.lower()
        factors = renaming_to_delete(eliminated)
        for step in reversed(descent):
            factors.extend(whitehead_factors(step, use_commutator))
    else:
        eliminated = literal
        descent = []
        rename_factors = renaming_to_delete(eliminated)
        rename = IDENTITY
        for factor in rename_factors:
            rename = compose(rename, factor)
        renamed_pivot = apply_marking(source_pivot, rename)
        factors = literal_shears(renamed_pivot, "z", use_commutator) + rename_factors

    path = StrictPath(START[:2], sink)
    path.add({"op": "stabilize", "generator": "z"})
    marking = IDENTITY
    for basic in factors:
        transport(path, basic_ledger(basic), marking)
        marking = compose(marking, basic)
        assert path.rows == [apply_marking(word, marking) for word in START]
    marking_end = path.total
    transport(path, prefix["moves"], marking)
    assert path.rows == [apply_marking(word, marking) for word in original]
    prefix_end = path.total
    transformed = path.rows.copy()

    _, normalization = normalize(tuple(path.rows), pivot_slot, "z")
    path.extend(normalization)
    for i, row in enumerate(transformed):
        if i == pivot_slot:
            continue
        while "z" in row.lower():
            position = row.lower().index("z")
            letter = row[position]
            suffix = row[position + 1:]
            path.factor(i, pivot_slot, 1 if letter == "Z" else -1, inverse(suffix))
            row = reduce(row[:position] + suffix)
            assert row == path.rows[i]
    path.add({"op": "destabilize", "generator": "z", "i": pivot_slot})
    for i in range(2):
        _, normalization = normalize(tuple(path.rows), i)
        path.extend(normalization)
    expected = [canonical(reduce(w.replace("z", "").replace("Z", "")))
                for i, w in enumerate(transformed) if i != pivot_slot]
    assert path.rows == expected
    path.record((json.dumps({"target": path.rows}, separators=(",", ":")) + "\n").encode("ascii"))
    return {
        "moves": path.total, "move_counts": dict(path.counts), "rank_peak": path.peak_rank,
        "raw_peak": path.raw_peak, "cyclic_peak": path.cyclic_peak,
        "initial_marking_moves": marking_end, "end_transported_prefix": prefix_end,
        "prefix_moves": len(prefix["moves"]), "pivot_slot": pivot_slot, "descent": descent,
        "literal_source_letter": literal,
        "old_generator_shear_factors": "commutator" if use_commutator else "swaps",
        "basic_marking_factors": len(factors), "marking": dict(zip(LETTERS, marking)),
        "transformed_rank_three_words": transformed, "final_words": path.rows,
        "strict_ledger_sha256": path.digest.hexdigest(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rank_three_prefix", type=Path)
    parser.add_argument("pivot_slot", type=int)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--literal", choices=LETTERS)
    parser.add_argument("--use-swaps-for-shears", action="store_true")
    args = parser.parse_args()
    prefix = json.loads(args.rank_three_prefix.read_text())
    with args.ledger.open("wb") as sink:
        receipt = compile_chart(prefix, args.pivot_slot, sink, args.literal, not args.use_swaps_for_shears)
    print(json.dumps(receipt, indent=2))
