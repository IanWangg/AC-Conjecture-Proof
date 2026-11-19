"""Replay two chartless excursions with a retained one-row donor block."""

import json
from pathlib import Path

from free_waypoint_search import normalize
from round02_ac_proof_controls import conjugate, invert, multiply
from round03_ac_proof_controls import replay_between, substitute
from round03_stable_proof_pivot import canonical
from round04_stable_proof_paths import replay as replay_rank_three
from round05_ac_proof_charts import add_conjugate, ak3_descent, conjugations, make_chart
from round05_stable_proof_chartless import minima
from stallings_search import apply, inverse, reduce

ROOT = Path(__file__).resolve().parents[1]
PREFIX = ROOT / "certificates/round05_stable_proof_chartless22.json"
BRAID = "xyxYXY"
POWER = "xxxYYYY"


def advance(rows, moves):
    for move in moves:
        rows = apply(rows, move)
    return rows


def inspect_gap(start, moves, pivot_before, pivot_after):
    """Check all interior cyclic classes for absence of a primitive relator."""
    rows = tuple(start)
    states = [tuple(map(canonical, rows))]
    for move in moves:
        rows = apply(rows, move)
        states.append(tuple(map(canonical, rows)))
    summaries = {
        state: tuple(len(minima((word,))[0][0]) for word in state)
        for state in states
    }
    first = 1 + max(i for i, words in enumerate(states[:-1]) if 1 in summaries[words])
    assert first > 0 and first < len(moves)
    assert summaries[states[first - 1]][pivot_before] == 1
    assert summaries[states[-1]][pivot_after] == 1
    assert all(1 not in summaries[state] for state in states[first:-1])
    return dict(
        first_chartless_step=first,
        last_chartless_step=len(moves) - 1,
        chartless_cyclic_tuples=[
            {"tuple": state, "individual_whitehead_minima": summaries[state]}
            for state in dict.fromkeys(states[first:-1])
        ],
    )


def imported_control():
    start = ("z", BRAID, POWER)
    rows = start
    moves, outgoing = [], []

    def run(ops):
        nonlocal rows
        rows = advance(rows, ops)
        moves.extend(ops)

    def out(expected_donor, factor_check):
        assert rows[expected_donor] == factor_check
        outgoing.append({"step": len(moves) + 1, "slot": expected_donor,
                         "word": rows[expected_donor]})
        run([multiply(2, expected_donor)])

    # The block slots are 0 and 1. P is already a product of conjugates
    # of their initial rows, so both listed outgoing donors lie in K.
    h = "xz"
    v = reduce(h + BRAID + inverse(h))
    p = reduce("z" + v)
    run(conjugations(1, h))
    run([multiply(0, 1)])
    assert rows == (p, v, POWER)
    out(0, p)
    u = rows[2]
    run([multiply(0, 2)])
    imported = rows[0]
    assert imported == reduce(p + u)
    out(1, v)
    new_outside = rows[2]
    run([invert(2), multiply(0, 2), invert(2)])
    assert rows[0] == reduce(p + u + inverse(v) + inverse(u))
    run(conjugations(1, u))
    run([multiply(0, 1)])
    run(conjugations(1, inverse(u)))
    assert rows[0] == p

    # Move the outsider inside the gap in a way that is nontrivial in Q.
    run([conjugate(2, "y")])
    assert rows[2] == reduce("y" + new_outside + "Y")

    # Make p0*q without returning to the initial pivot en route.
    run(conjugations(1, inverse(h)))
    run([multiply(0, 1)])
    run(conjugations(1, reduce(inverse(BRAID) + h)))
    run([invert(1), multiply(0, 1), invert(1)])
    return_step = len(moves) - 1
    run(conjugations(1, reduce(inverse(h) + BRAID)))
    assert rows[:2] == (reduce("z" + BRAID), BRAID)

    # A permutation image records the genuine change to the block quotient.
    # In S_3 let x and y be adjacent transpositions and z be the identity.
    mark = {"x": (1, 0, 2), "y": (0, 2, 1), "z": (0, 1, 2)}

    def image(word):
        result = mark["z"]
        for letter in word:
            factor = mark[letter.lower()]
            result = tuple(result[i] for i in factor)
        return result

    assert image("z") == image(BRAID) == mark["z"]
    assert image(imported) == mark["x"] and image(imported) != mark["z"]
    assert image(rows[2]) != image(POWER)
    assert all(image(item["word"]) == mark["z"] for item in outgoing)

    end_words = rows
    left = (BRAID, POWER)
    projection = make_chart(end_words[0], "z", {"x": "x", "y": "y"})
    right = tuple(substitute(word, projection) for word in end_words[1:])
    h_new = substitute(h, projection)
    ordinary = add_conjugate(1, 0, "", True)
    ordinary += 2 * add_conjugate(1, 0, h_new, False)
    ordinary.append(conjugate(1, "y"))
    padded = {"format": "rank-three-ac-elementary-v1", "start": start,
              "target": end_words, "maximum_cyclic_length": 65, "moves": moves}
    gap = inspect_gap(start, moves[:return_step], 0, 0)
    return {
        "rank_three_replay": replay_rank_three(padded),
        "rank_three_moves": moves,
        "gap": gap,
        "block": [0, 1],
        "outgoing_donors_in_fixed_normal_closure": outgoing,
        "intermediate_imported_pivot": imported,
        "its_nonidentity_permutation": image(imported),
        "outside_permutations": [image(POWER), image(end_words[2])],
        "exit_chart": projection,
        "ordinary_from": left,
        "ordinary_moves": ordinary,
        "ordinary_replay": replay_between(list(left), list(right), ordinary),
    }


def rotated_product(rows, receiver, donor, receiver_word, donor_word):
    rows, moves = normalize(rows, receiver, receiver_word)
    rows, operations = normalize(rows, donor, donor_word)
    moves.extend(operations)
    operation = multiply(receiver, donor)
    rows = apply(rows, operation)
    moves.append(operation)
    for slot in (receiver, donor):
        rows, operations = normalize(rows, slot)
        moves.extend(operations)
    return rows, moves


def existing_witness():
    original = json.loads(PREFIX.read_text())
    start = tuple(original["start"])
    entry = advance(start, original["moves"][:248])
    middle = tuple(original["target"])
    assert advance(entry, original["moves"][248:]) == middle
    rows, outgoing = rotated_product(middle, 2, 0, "YYZZYXX", "zzzyxYXyy")
    end, reentry = rotated_product(rows, 1, 0, "XYxYXy", "YxyXYZZZY")
    assert end == ("XYZZZYYxy", "XYYZZZY", "XXzzzyxYXZZY")
    gap_moves = original["moves"][248:] + outgoing + reentry
    gap = inspect_gap(entry, gap_moves[:next(
        i for i, move in enumerate(gap_moves) if move == multiply(1, 0)
    ) + 1], 0, 1)
    full = {**original, "target": end, "maximum_cyclic_length": 28,
            "moves": original["moves"] + outgoing + reentry}
    full["macro_boundaries"] += [len(original["moves"]) + len(outgoing), len(full["moves"])]

    # Use the round-five ordinary path up to the old pivot in slot 0.
    # Inversion of that pivot at step 248 leaves its quotient unchanged.
    projected = ak3_descent()["ordinary_certificate"]
    chart = make_chart(entry[0], "x", {"y": "y", "z": "x"})
    assert chart == make_chart(end[1], "x", {"y": "y", "z": "x"})
    left = tuple(substitute(entry[i], chart) for i in (2, 1))
    assert list(left) == projected["target"]
    right = tuple(substitute(end[i], chart) for i in (2, 0))
    ordinary = left
    ledger = []
    padded_rows = entry
    outgoing_word = None
    for move in gap_moves:
        if move["i"] == 2:
            if move["op"] == "conjugate":
                ops = conjugations(0, substitute(move["g"], chart))
            elif move["op"] == "invert":
                ops = [invert(0)]
            else:
                assert move["j"] == 0 and outgoing_word is None
                outgoing_word = substitute(padded_rows[0], chart)
                _, change = normalize(ordinary, 1, outgoing_word)
                back = [conjugate(1, move["g"].swapcase()) if move["op"] == "conjugate"
                        else invert(1) for move in reversed(change)]
                ops = change + [multiply(0, 1)] + back
            ledger.extend(ops)
            ordinary = advance(ordinary, ops)
        padded_rows = apply(padded_rows, move)
        assert ordinary[0] == substitute(padded_rows[2], chart)
        assert ordinary[1] == left[1]
    _, align = normalize(ordinary, 1, right[1])
    ledger.extend(align)
    assert advance(ordinary, align) == right
    return {
        "source_certificate": PREFIX.name,
        "rank_three_replay": replay_rank_three(full),
        "rank_three_continuation": outgoing + reentry,
        "gap_start_rank_three_step": 248,
        "gap": gap,
        "pivot_slots": [0, 1],
        "shared_chart": chart,
        "outgoing_projected_word": outgoing_word,
        "ordinary_from": left,
        "ordinary_gap_moves": ledger,
        "ordinary_gap_replay": replay_between(list(left), list(right), ledger),
        "ordinary_full_replay": replay_between(projected["start"], list(right), projected["moves"] + ledger),
    }


if __name__ == "__main__":
    print(json.dumps({"imports_with_safe_outgoing": imported_control(),
                      "ak3_primitive_slot_transfer": existing_witness()}, indent=2))
