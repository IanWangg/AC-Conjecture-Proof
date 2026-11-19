"""Replay two-incoming OIIO cuts with a transferred marked generator."""

import json
from fractions import Fraction

from round02_stable_disproof_search import inverse, reduce_word
from round03_stable_disproof_cuts import affine_inv, affine_mul, conjugations, replay


def values(word, images):
    return reduce_word("".join(
        images[c] if c.islower() else inverse(images[c.lower()])
        for c in word
    ))


def control(conjugator):
    start = ("y", "x", "z")
    moves = [
        ("multiply", 0, 2, -1),
        *conjugations(0, "Z"),
        *conjugations(1, conjugator),
        ("multiply", 0, 1, 1),
        ("multiply", 2, 0, 1),
        ("multiply", 2, 1, -1),
        ("multiply", 0, 1, -1),
        *conjugations(1, inverse(conjugator)),
        ("multiply", 0, 2, -1),
        ("invert", 0, None, 1),
    ]
    states = list(replay(start, moves))
    assert states[-1] == ("z", "x", "y")
    crossing_indices = [
        i for i, (op, receiver, donor, _) in enumerate(moves)
        if op == "multiply" and ((receiver == 2) != (donor == 2))
    ]
    directions = ["in" if moves[i][1] == 2 else "out" for i in crossing_indices]
    assert directions == ["out", "in", "in", "out"]
    first, second = crossing_indices[1:3]
    before = states[first]
    middle = states[first + 1]
    after = states[second + 1]
    receipt = {
        "start": start,
        "moves": len(moves),
        "crossing_order": directions,
        "before_first_incoming": before,
        "middle": middle,
        "after_second_incoming": after,
        "endpoint": states[-1],
    }
    return receipt, before, middle, after


def free_middle():
    receipt, before, middle, after = control("")
    old = {"x": "x", "y": "y", "z": ""}
    middle_early = {"x": "x", "y": "X", "z": "xy"}
    middle_late = {"x": "x", "y": "X", "z": "y"}
    new = {"x": "x", "y": "", "z": "y"}
    assert middle[2] == "yx"
    assert [values(w, middle_late) for w in ("x", "y")] == ["x", "X"]
    for chosen, charts in (
        (("x", "yz"), (old, middle_early)),
        (("x", "z"), (middle_late, new)),
    ):
        for chart in charts:
            assert tuple(values(w, chart) for w in chosen) == ("x", "y")
    assert values(middle[2], middle_early) == values(middle[2], middle_late) == ""
    early = tuple(values(w, old) for w in before[:2])
    capture = tuple(values(w, middle_early) for w in middle[:2])
    erasure = tuple(values(w, middle_late) for w in middle[:2])
    late = tuple(values(w, new) for w in after[:2])
    first_splice = [("invert", 0, None, 1), *conjugations(0, "x")]
    second_splice = [("multiply", 0, 1, 1)]
    assert list(replay(early, first_splice))[-1] == capture
    assert tuple(values(w, {"x": "x", "y": "Xy"}) for w in capture) == erasure
    assert list(replay(erasure, second_splice))[-1] == late
    receipt.update({
        "early_common_basis_words": ("x", "yz"),
        "late_common_basis_words": ("x", "z"),
        "projected_early_pair": early,
        "projected_middle_early_marking": capture,
        "projected_middle_late_marking": erasure,
        "projected_late_pair": late,
        "strict_splice_moves": [len(first_splice), len(second_splice)],
    })
    return receipt


def nonfree_middle():
    receipt, before, middle, after = control("xy")
    assert middle[2] == "yxyxYX"
    identity = (Fraction(1), Fraction(0))
    x, u = (Fraction(2), Fraction(0)), (Fraction(1), Fraction(1))
    known = {"x": x, "y": affine_mul(u, affine_inv(x)), "z": identity}

    def evaluate(word):
        image = identity
        for c in word:
            letter = known[c.lower()]
            image = affine_mul(image, letter if c.islower() else affine_inv(letter))
        return image

    assert evaluate(middle[2]) == identity
    assert evaluate("yx") == u != identity
    assert evaluate("xyxX") == affine_mul(u, u)
    small_chart = {"x": "x", "y": "", "z": ""}
    assert values(before[0], small_chart) == values(after[1], small_chart) == "x"
    receipt.update({
        "nonfree_relation": "x u x^-1 = u^2, u = yx",
        "affine_image_of_u": list(map(int, u)),
        "incoming_donors_after_killing_y_and_z": ["x", "x"],
    })
    return receipt


if __name__ == "__main__":
    print(json.dumps({"free_middle": free_middle(), "nonfree_middle": nonfree_middle()}, indent=2))
