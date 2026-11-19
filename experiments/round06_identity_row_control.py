"""Replay an augmented F2 path with a spare identity row."""

import json

from round02_braid_kernel_lift import collect, power
from stallings_search import inverse, reduce

MARKS = frozenset("xXyY")
START = ("xxxYYYY", "xyxYXY", "")


def replay(moves):
    rows = list(START)
    for move in moves:
        recipient = move["i"]
        assert 0 <= recipient < len(rows)
        if move["op"] == "conjugate":
            letter = move["g"]
            assert letter in MARKS
            rows[recipient] = reduce(letter + rows[recipient] + inverse(letter))
        elif move["op"] == "multiply":
            donor, sign = move["j"], move["sign"]
            assert 0 <= donor < len(rows) and donor != recipient and sign in (-1, 1)
            rows[recipient] = reduce(rows[recipient] + (rows[donor] if sign == 1 else inverse(rows[donor])))
        else:
            raise ValueError(move)
    return rows


def conjugated_product(recipient, donor, conjugator, sign):
    return (
        [{"op": "conjugate", "i": donor, "g": c} for c in reversed(conjugator)]
        + [{"op": "multiply", "i": recipient, "j": donor, "sign": sign}]
        + [{"op": "conjugate", "i": donor, "g": c} for c in reversed(inverse(conjugator))]
    )


def main():
    # y = p^-1 (x p x^-1) ((xy) p^-1 (xy)^-1) b (y b y^-1) (y^2 b y^-2)
    # for p = x^3 y^-4 and b = xyx/(yxy).
    moves = []
    for donor, conjugator, sign in [(0, "", -1), (0, "x", 1), (0, "xy", -1),
                                   (1, "", 1), (1, "y", 1), (1, "yy", 1)]:
        moves.extend(conjugated_product(2, donor, conjugator, sign))
    assert replay(moves) == [START[0], START[1], "y"]
    identity_filled_at = len(moves)

    for index, projected in enumerate(("xxx", "x")):
        error = reduce(inverse(START[index]) + projected)
        for exponent, letter in collect(error, "x"):
            moves.extend(conjugated_product(index, 2, power("x", exponent), 1 if letter == "y" else -1))
    assert replay(moves) == ["xxx", "x", "y"]
    moves.extend([{"op": "multiply", "i": 0, "j": 1, "sign": -1}] * 3)
    target = replay(moves)
    assert sorted(target) == ["", "x", "y"]
    print(json.dumps({
        "start": START,
        "target": target,
        "free_ambient_rank": 2,
        "spare_identity_rows": 1,
        "first_basis_letter_reached_at": identity_filled_at,
        "instruction_count": len(moves),
        "moves": moves,
    }, indent=2))


if __name__ == "__main__":
    main()
