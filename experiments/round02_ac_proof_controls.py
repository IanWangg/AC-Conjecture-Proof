"""Exact controls for multi-auxiliary Andrews–Curtis projection."""

import json
from itertools import combinations

from elementary_verify import replay
from stallings_search import inverse, reduce


def cyclic(word):
    word = reduce(word)
    lo, hi = 0, len(word)
    while hi - lo > 1 and word[lo] == word[hi - 1].swapcase():
        lo += 1
        hi -= 1
    return word[lo:hi]


def auxiliary_letters(word, auxiliary):
    return [letter.lower() for letter in cyclic(word) if letter.lower() in auxiliary]


def triangular_frames(words, auxiliary):
    def orders(remaining, used):
        if not remaining:
            yield ()
        for slot, word in enumerate(words):
            support = auxiliary_letters(word, remaining)
            if slot in used or len(support) != 1:
                continue
            generator = support[0]
            for tail in orders(remaining - {generator}, used | {slot}):
                yield ((slot, generator),) + tail

    return sorted({tuple(sorted(order)) for order in orders(set(auxiliary), set())})


def eliminate(words, slot, generator):
    pivot = cyclic(words[slot])
    copies = [i for i, letter in enumerate(pivot) if letter.lower() == generator]
    assert len(copies) == 1
    pos = copies[0]
    pivot = pivot[pos:] + pivot[:pos]
    value = inverse(pivot[1:]) if pivot[0].islower() else pivot[1:]
    assert all(letter.lower() != generator for letter in value)
    substitution = {generator: value, generator.upper(): inverse(value)}
    return tuple(
        None if i == slot or word is None
        else reduce("".join(substitution.get(letter, letter) for letter in word))
        for i, word in enumerate(words)
    )


def project(words, order):
    for slot, generator in order:
        words = eliminate(words, slot, generator)
    return [word for word in words if word is not None]


def replay_to_basis(start, moves):
    return replay({
        "format": "ordinary-ac-elementary-v1",
        "start": start,
        "target": ["x", "y"],
        "moves": moves,
    })


def multiply(i, j):
    return {"op": "multiply", "i": i, "j": j}


def invert(i):
    return {"op": "invert", "i": i}


def conjugate(i, g):
    return {"op": "conjugate", "i": i, "g": g}


def pivot_switch_control():
    r, q, u, v = words = ("z", "ZtztZT", "zztx", "ztty")
    r_prime = reduce(r + q)
    assert r_prime == "tztZT"
    assert reduce(r_prime + inverse(q)) == r
    after = (r_prime, q, u, v)
    first_frame = ((0, "z"), (2, "t"))
    second_frame = ((0, "t"), (3, "z"))
    assert triangular_frames(words, "zt") == [first_frame]
    assert triangular_frames(after, "zt") == [second_frame]
    left = project(words, first_frame)
    right = project(after, second_frame)
    assert left == ["X", "XXy"] and right == ["y", "YYx"]
    common = (r, r_prime, u, v)
    assert project(common, ((0, "z"), (1, "t"))) == ["x", "y"]
    left_moves = [invert(0)] + [multiply(1, 0), conjugate(1, "x")] * 2
    right_moves = [multiply(1, 0), conjugate(1, "y")] * 2 + [
        multiply(0, 1), invert(0), multiply(1, 0), invert(0), multiply(0, 1),
        conjugate(0, "Y"), invert(1),
    ]
    return {
        "edge_from": words, "edge_to": after, "middle_tuple": common,
        "triangular_frames": [first_frame, second_frame],
        "left_projection": left, "left_replay": replay_to_basis(left, left_moves),
        "right_projection": right, "right_replay": replay_to_basis(right, right_moves),
    }


def relative_frame_control():
    u, v = "z", "t"
    nielsen_steps = (0, 1, 0, 1)
    basis = [u, v]
    for i in nielsen_steps:
        basis[i] = reduce(basis[i] + basis[1-i])
    u, v = basis
    words = ("z", "t", u + "x", v + "y")
    exponents = [tuple(w.count(g) - w.count(g.upper()) for g in "zt") for w in words]
    determinants = []
    for i, j in combinations(range(4), 2):
        a, b = exponents[i]
        c, d = exponents[j]
        determinants.append(([i, j], a*d-b*c))
    assert [slots for slots, det in determinants if abs(det) == 1] == [[0, 1], [2, 3]]
    assert [slots for slots in triangular_frames(words, "zt")] == [((0, "z"), (1, "t"))]
    solutions = ["X", "Y"]
    for i in reversed(nielsen_steps):
        solutions[i] = reduce(solutions[i] + inverse(solutions[1-i]))
    table = dict(zip("zt", solutions))
    assert reduce("".join(table[c] for c in u) + "x") == ""
    assert reduce("".join(table[c] for c in v) + "y") == ""
    return {"tuple": words, "determinants": determinants, "second_projection": solutions}


def dynamic_elimination_control():
    words = ("z", "zX", "tzTZty", "y")
    first_branch = eliminate(words, 0, "z")
    second_branch = eliminate(words, 1, "z")
    assert triangular_frames(words, "zt") == []
    assert first_branch == (None, "X", "ty", "y")
    assert project(words, ((0, "z"), (2, "t"))) == ["X", "y"]
    assert second_branch == ("x", None, "txTXty", "y")
    assert [auxiliary_letters(w, "t") for w in second_branch if w is not None] == [
        [], ["t", "t", "t"], []
    ]
    return {"tuple": words, "successful_first_elimination": first_branch,
            "stalled_first_elimination": second_branch}


if __name__ == "__main__":
    print(json.dumps({
        "pivot_switch": pivot_switch_control(),
        "disconnected_relative_frames": relative_frame_control(),
        "dynamic_elimination": dynamic_elimination_control(),
    }, indent=2))
