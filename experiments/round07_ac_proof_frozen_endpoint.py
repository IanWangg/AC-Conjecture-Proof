"""Verify a chartless excursion with nonzero outgoing changes that cancel in Q."""

import json

from round02_ac_proof_controls import conjugate, invert, multiply
from round03_ac_proof_controls import permutation_inverse, permutation_product, replay_between, substitute
from round04_stable_proof_paths import replay as replay_rank_three
from round05_ac_proof_charts import add_conjugate, conjugations
from round06_ac_proof_excursions import advance, inspect_gap
from stallings_search import inverse, reduce


BRAID = "xyxYXY"
POWER = "xxxYYYY"


def evaluate(word, marking):
    result = (1, 2, 3)
    for letter in word:
        value = marking[letter.lower()]
        result = permutation_product(result, permutation_inverse(value) if letter.isupper() else value)
    return result


def opposite_product(recipient, donor):
    return [invert(donor), multiply(recipient, donor), invert(donor)]


def main():
    start = ("z", BRAID, POWER)
    state = start
    ledger = []

    def emit(moves):
        nonlocal state
        ledger.extend(moves)
        state = advance(state, moves)

    def outgoing(donor, negative=False):
        value = inverse(state[donor]) if negative else state[donor]
        initial = state[2]
        moves = opposite_product(2, donor) if negative else [multiply(2, donor)]
        product_step = len(ledger) + (2 if negative else 1)
        emit(moves)
        return {"strict_product_step": product_step, "word": value,
                "outside_before": initial, "outside_after": state[2]}

    h = "xz"
    emit(conjugations(1, h))
    v = state[1]
    emit([multiply(0, 1)])
    p = state[0]
    assert p == reduce("z" + v)
    events = [outgoing(0)]
    u = state[2]
    emit([multiply(0, 2)])
    e = state[0]
    assert e == reduce(p + u)

    events.append(outgoing(0))
    events.append(outgoing(1))
    events.append(outgoing(0, negative=True))
    w = reduce(e + v + inverse(e))
    assert state[2] == reduce(u + w)

    emit(opposite_product(0, 2))
    assert state[0] == reduce(p + u + inverse(w) + inverse(u))
    emit(add_conjugate(0, 1, reduce(u + e), False))
    assert state[0] == p
    emit([conjugate(2, "y")])
    emit(opposite_product(0, 1))
    unlock = len(ledger) - 1
    emit(conjugations(1, inverse(h)))
    assert state[:2] == ("z", BRAID)

    gap = inspect_gap(start, ledger[:unlock], 0, 0)
    identity = (1, 2, 3)
    marked = {"x": (2, 1, 3), "y": (1, 3, 2), "z": identity}
    assert evaluate("z", marked) == evaluate(BRAID, marked) == identity
    for event in events:
        for key, word in event.copy().items():
            if isinstance(word, str):
                event[key + "_S3"] = evaluate(word, marked)
    positive, negative = events[1], events[3]
    assert positive["word_S3"] == negative["word_S3"] != identity
    assert positive["outside_before_S3"] != positive["outside_after_S3"]
    assert negative["outside_before_S3"] != negative["outside_after_S3"]
    assert gap["first_chartless_step"] <= positive["strict_product_step"] < negative["strict_product_step"] <= gap["last_chartless_step"]

    # The two nonzero images cancel already in Q: p, v and w vanish there.
    exterior = state[2]
    beta = {"z": ""}
    target = [BRAID, substitute(exterior, beta)]
    e_bar = substitute(e, beta)
    ordinary = add_conjugate(1, 0, "x", False)
    ordinary += add_conjugate(1, 0, reduce(e_bar + "x"), False)
    ordinary.append(conjugate(1, "y"))
    padded = {"format": "rank-three-ac-elementary-v1", "start": start, "target": state,
              "maximum_cyclic_length": 200, "moves": ledger}
    return {
        "rank_three_replay": replay_rank_three(padded),
        "rank_three_moves": ledger,
        "block_slots": [0, 1],
        "common_quotient_relators": ["z", BRAID],
        "quotient_witness_marking_S3": marked,
        "chartless_gap": gap,
        "outgoing_events": events,
        "ordinary_splice_moves": ordinary,
        "ordinary_splice_replay": replay_between([BRAID, POWER], target, ordinary),
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
