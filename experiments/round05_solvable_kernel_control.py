"""Check the one-row solvable-kernel correction in A5 times BS(1,2)."""

import json
from fractions import Fraction

from elementary_verify import inverse, reduce, replay
from round03_frozen_donors import cycle_type
from round04_chart_lifts import ONE, X, Y, marked_value
from round04_finite_corrections import commutator, operations


def solvable_value(word):
    exponent, translation = 0, Fraction(0)
    for letter in word:
        if letter in "xX":
            exponent += 1 if letter == "x" else -1
        else:
            translation += (1 if letter == "y" else -1) * Fraction(2) ** exponent
    return exponent, translation


def main():
    c = commutator("x", "y")
    d = reduce(c * 3)
    cp = commutator("x", inverse(d))
    start = [reduce("x" + c), reduce("y" + d)]
    marks = {"x": X, "y": Y}
    assert marked_value(c, marks) != ONE
    assert marked_value(d, marks) == ONE
    assert solvable_value(d) == (0, 3)
    assert solvable_value(cp) == (0, -3)

    # c^(-1)c' = (yd) (c'^(-1)x) (yd)^(-1) (c'^(-1)x)^(-1).
    g = reduce(inverse(cp) + "x")
    assert reduce(inverse(c) + cp) == reduce(start[1] + g + inverse(start[1]) + inverse(g))
    first = [{"op": "multiply", "i": 0, "j": 1}]
    first += [{"op": "conjugate", "i": 1, "g": letter} for letter in reversed(g)]
    first += [
        {"op": "invert", "i": 1},
        {"op": "multiply", "i": 0, "j": 1},
        {"op": "invert", "i": 1},
    ]
    first += [{"op": "conjugate", "i": 1, "g": letter} for letter in reversed(inverse(g))]
    changed_first = reduce("x" + cp)

    # The first donor has exponent one in BS(1,2), so [d,xc'] has
    # translation -3 and trivial permutation. Use y to remove c' then.
    second = operations(1, d)
    changed_second = reduce(start[1] + commutator(d, changed_first))
    ch = commutator("x", changed_second)
    final_first = reduce(changed_first + ch * 3)
    third = operations(0, "x") * 3

    def inspect(word):
        a, q = solvable_value(word)
        return {"permutation": marked_value(word, marks), "exponent": a, "translation": str(q)}

    assert inspect(changed_second) == inspect("y")
    assert inspect(final_first) == inspect("x")
    checked = replay({
        "format": "ordinary-ac-elementary-v1",
        "start": start,
        "target": [final_first, changed_second],
        "moves": first + second + third,
    })
    print(json.dumps({
        "solvable_kernel": "additive Z[1/2] in A5 times BS(1,2)",
        "quotient": "A5 times Z",
        "first_error_permutation_cycle_type": cycle_type(marked_value(c, marks)),
        "second_error_infinite_kernel_translation": str(solvable_value(d)[1]),
        "substitution_images": list(map(inspect, [changed_first, start[1]])),
        "final_images": list(map(inspect, checked["endpoint"])),
        "strict_moves_by_stage": list(map(len, [first, second, third])),
        "strict_moves": checked["moves"],
    }, indent=2))


if __name__ == "__main__":
    main()
