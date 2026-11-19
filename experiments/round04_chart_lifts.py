"""Check a balanced trivial tuple with two free charts and no common lifted basis."""

import json

from elementary_verify import inverse, replay
from round02_braid_kernel_lift import collect, power
from round03_frozen_donors import cycle_type, perm_inv, perm_mul
from stallings_search import reduce

ONE = (1, 2, 3, 4, 5)
X = (2, 3, 1, 4, 5)
Y = (2, 3, 4, 5, 1)
A = "xyX"
B = "yyzz"
P = "z" + inverse(A)
Q = "x" + inverse(B)


def marked_value(word, marks):
    values = dict(marks)
    values.update({c.upper(): perm_inv(p) for c, p in marks.items()})
    value = ONE
    for letter in word:
        value = perm_mul(value, values[letter])
    return value


def image_size(marks):
    reached = {ONE}
    queue = [ONE]
    for state in queue:
        for mark in marks:
            value = perm_mul(state, mark)
            if value not in reached:
                reached.add(value)
                queue.append(value)
    return len(reached)


def commutator(a, b):
    return perm_mul(perm_mul(perm_mul(a, b), perm_inv(a)), perm_inv(b))


def substitute(word, letter, replacement):
    mapping = {letter: replacement, letter.upper(): inverse(replacement)}
    return reduce("".join(mapping.get(c, c) for c in word))


def complete_projection(row):
    moves = []
    for exponent, letter in collect(reduce(inverse(row) + "x"), "x"):
        conjugator = power("x", exponent)
        moves.extend({"op": "conjugate", "i": 1, "g": c} for c in reversed(conjugator))
        if letter.isupper():
            moves.append({"op": "invert", "i": 1})
        moves.append({"op": "multiply", "i": 0, "j": 1})
        if letter.isupper():
            moves.append({"op": "invert", "i": 1})
        moves.extend({"op": "conjugate", "i": 1, "g": c} for c in reversed(inverse(conjugator)))
    cert = {
        "format": "ordinary-ac-elementary-v1",
        "start": [row, "y"],
        "target": ["x", "y"],
        "moves": moves,
    }
    return {"start": cert["start"], **replay(cert)}


def main():
    z = marked_value(A, {"x": X, "y": Y})
    marks = {"x": X, "y": Y, "z": z}
    assert marked_value(P, marks) == marked_value(Q, marks) == ONE
    assert image_size((X, Y)) == image_size((z, Y)) == 60
    first = cycle_type(commutator(X, Y))
    second = cycle_type(commutator(z, Y))
    assert first != second
    assert substitute(P, "y", "") == "z"
    assert substitute(substitute(Q, "y", ""), "z", "") == "x"
    old = substitute(Q, "z", A)
    new = substitute(P, "x", B).translate(str.maketrans("zZ", "xX"))
    print(json.dumps({
        "rank_three_tuple": [P, Q, "y"],
        "finite_marked_permutations": marks,
        "chart_commutator_cycle_types": {"eliminate_z": first, "eliminate_x": second},
        "projected_ordinary_controls": [complete_projection(old), complete_projection(new)],
    }, indent=2))


if __name__ == "__main__":
    main()
