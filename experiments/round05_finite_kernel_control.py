"""Replay the noncentral and central stages of the finite-kernel lifting proof."""

import json

from elementary_verify import inverse, reduce, replay
from round04_finite_corrections import commutator, operations

ONE = (0, 0, 0, 0)
MARKS = {"x": (1, 0, 0, 0), "y": (0, 1, 0, 1)}


def multiply(left, right):
    a, b, c, v = left
    d, e, f, w = right
    return a + d, b + e, (c + f + a * e) % 3, (v + pow(2, a % 4, 5) * w) % 5


def value(word):
    marks = {**MARKS, "X": (-1, 0, 0, 0), "Y": (0, -1, 0, 4)}
    result = ONE
    for letter in word:
        result = multiply(result, marks[letter])
    return result


def main():
    shared = commutator("x", "y")
    central = reduce(shared * 10)
    noncentral = reduce(shared * 6)
    assert value(central) == (0, 0, 1, 0)
    assert value(noncentral) == (0, 0, 0, 1)
    start = [reduce(central * 2 + noncentral * 2 + "x"), reduce(central + "y" + inverse(noncentral))]
    assert list(map(value, start)) == [(1, 0, 2, 2), (0, 1, 1, 0)]
    assert value(commutator(*start)) == (0, 0, 1, 0)
    assert value(commutator(noncentral, start[0])) == (0, 0, 0, 4)

    words = start.copy()
    moves, stages = [], []

    def record(stage, expected):
        images = list(map(value, words))
        assert images == expected
        stages.append({"stage": stage, "moves": len(moves), "tuple_images": images})

    def twist(recipient, conjugator):
        moves.extend(operations(recipient, conjugator))
        words[recipient] = reduce(words[recipient] + commutator(conjugator, words[1 - recipient]))

    # The only active row modulo the central kernel is row zero. Give row one
    # the same action on the noncentral kernel, fix row zero, and undo the mix.
    moves.append({"op": "multiply", "i": 1, "j": 0})
    words[1] = reduce(words[1] + words[0])
    twist(0, noncentral)
    moves.extend([{"op": "invert", "i": 0}, {"op": "multiply", "i": 1, "j": 0}, {"op": "invert", "i": 0}])
    words[1] = reduce(words[1] + inverse(words[0]))
    twist(1, noncentral)
    record("noncentral kernel corrected modulo the central kernel", [(1, 0, 2, 0), (0, 1, 1, 1)])

    # These commutators belong to the central kernel, since the indicated
    # powers kill the noncentral contribution.
    twist(0, "xxxx")
    twist(1, "y" * 10)
    record("central kernel corrected", list(MARKS.values()))
    checked = replay({"format": "ordinary-ac-elementary-v1", "start": start, "target": words, "moves": moves})
    print(json.dumps({
        "infinite_group": "Z^2 with a central C3 coordinate and a C5 coordinate acted on by multiplication by 2^a",
        "finite_kernel_order": 15,
        "initial_images": list(map(value, start)),
        "stages": stages,
        "strict_moves": checked["moves"],
        "free_endpoint_lengths": list(map(len, checked["endpoint"])),
    }, indent=2))


if __name__ == "__main__":
    main()
