"""Check a one-outlier rank-three lift with an infinite abelian kernel."""

import json

from free_waypoint_search import conj_ops, cyclic
from round04_chart_lifts import ONE, X, Y, marked_value
from round04_finite_corrections import commutator
from round04_stable_proof_paths import replay
from round05_solvable_kernel_control import solvable_value
from stallings_search import apply, inverse, reduce


def value(word):
    retained = word.replace("z", "").replace("Z", "")
    return marked_value(retained, {"x": X, "y": Y}), solvable_value(retained), word.count("z") - word.count("Z")


def printable(word):
    permutation, (exponent, translation), center = value(word)
    return {"permutation": permutation, "exponent": exponent, "translation": str(translation), "z": center}


def main():
    v = reduce(commutator("x", "y") * 6 + "Y" * 5)
    assert value(v) == (ONE, (0, 1), 0)
    first = reduce("x" + v)
    second = reduce("y" + inverse(v))
    outlier = commutator(first, second)
    assert value(outlier)[0] != ONE
    assert value(outlier)[1:] == ((0, 0), 0)
    start = (first, second, reduce("z" + outlier))
    rows = start
    moves = []
    cyclic_peak = sum(len(cyclic(row)) for row in rows)

    def execute(instructions):
        nonlocal rows, cyclic_peak
        for instruction in instructions:
            rows = apply(rows, instruction)
            moves.append(instruction)
            cyclic_peak = max(cyclic_peak, sum(len(cyclic(row)) for row in rows))

    def product(recipient, donor, negative=False):
        invert = {"op": "invert", "i": donor}
        multiply = {"op": "multiply", "i": recipient, "j": donor}
        execute([invert, multiply, invert] if negative else [multiply])

    # The outlier is removed by the two fixed donors. Then the frozen
    # projected donors are both trivial in BS(1,2), but a conjugation fixes x.
    for donor, negative in ((1, False), (0, False), (1, True), (0, True)):
        product(2, donor, negative)
    assert rows[2] == "z"
    outlier_fixed_at = len(moves)
    assert value(rows[1])[1] == (0, 0)
    assert value(rows[2])[1] == (0, 0)
    assert value(rows[0])[1] == (1, 2) != value("x")[1]
    execute(conj_ops(0, reduce(v + v)))
    assert value(rows[0]) == value("x")
    first_fixed_at = len(moves)

    # [v^(-1), x] has translation +1. The donor is restored literally.
    current_first = rows[0]
    execute(conj_ops(0, inverse(v)))
    product(1, 0)
    execute(conj_ops(0, v))
    product(1, 0, negative=True)
    assert rows[0] == current_first
    assert tuple(map(value, rows)) == tuple(map(value, "xyz"))

    certificate = {
        "format": "rank-three-ac-elementary-v1",
        "start": start,
        "target": rows,
        "moves": moves,
        "maximum_cyclic_length": cyclic_peak,
    }
    checked = replay(certificate)
    print(json.dumps({
        "ambient_group": "A5 times BS(1,2) times Z",
        "abelian_kernel": "dyadic translation group",
        "initial_tuple_images": list(map(printable, start)),
        "outlier_fixed_at": outlier_fixed_at,
        "first_row_fixed_at": first_fixed_at,
        "final_tuple_images": list(map(printable, checked["target"])),
        "strict_moves": checked["moves"],
        "free_endpoint_lengths": list(map(len, checked["target"])),
    }, indent=2))


if __name__ == "__main__":
    main()
