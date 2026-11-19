"""Free-word and finite quotient controls for marked Andrews–Curtis projections."""

from itertools import combinations
import json

from elementary_verify import replay
from round02_ac_proof_controls import conjugate, invert, multiply, triangular_frames
from stallings_search import inverse, reduce


def substitute(word, images):
    signed = dict(images)
    signed.update({letter.upper(): inverse(image) for letter, image in images.items()})
    return reduce("".join(signed.get(letter, letter) for letter in word))


def replay_between(start, target, moves):
    return replay({
        "format": "ordinary-ac-elementary-v1",
        "start": start,
        "target": target,
        "moves": moves,
    })


def permutation_product(left, right):
    return tuple(left[i - 1] for i in right)


def permutation_inverse(image):
    return tuple(image.index(i) + 1 for i in range(1, len(image) + 1))


def permutation_evaluation(word, images):
    signed = dict(images)
    signed.update({letter.upper(): permutation_inverse(image) for letter, image in images.items()})
    value = tuple(range(1, 6))
    for letter in word:
        value = permutation_product(value, signed[letter])
    return value


def nonfree_common_block():
    commutator = "zxZX"
    common = reduce("tt" + commutator + "T" + inverse(commutator))
    left = [common, "z", "X", "yzxz"]
    right = [common, reduce(left[1] + left[2]), *left[2:]]
    assert triangular_frames(left, "zt") == triangular_frames(right, "zt") == []
    projections = []
    for words, images in ((left, {"z": "", "t": ""}), (right, {"z": "x", "t": ""})):
        evaluated = [substitute(word, images) for word in words]
        assert evaluated[:2] == ["", ""]
        projections.append(evaluated[2:])
    assert projections == [["X", "yx"], ["X", "yxxx"]]
    projected_moves = [invert(0), multiply(1, 0), multiply(1, 0), invert(0)]
    projected = replay_between(*projections, projected_moves)

    images = {"z": (2, 1, 3, 4, 5), "x": (4, 5, 3, 1, 2),
              "t": (2, 3, 1, 4, 5), "y": (1, 2, 3, 4, 5)}
    identity = (1, 2, 3, 4, 5)
    assert permutation_evaluation(common, images) == identity
    assert permutation_evaluation("t", images) != identity
    assert permutation_evaluation(commutator + "t" + inverse(commutator), images) == (
        permutation_evaluation("tt", images)
    )
    return {
        "padded_edge_from": left,
        "padded_edge_to": right,
        "marked_projections": projections,
        "projected_moves": projected_moves,
        "projected_replay": projected,
        "common_block_nonfree_witness_S5": images,
    }


def invert_nielsen(start, steps):
    pair = list(start)
    for i in reversed(steps):
        pair[i] = reduce(pair[i] + inverse(pair[1 - i]))
    return pair


def auxiliary_unimodular_slots(words):
    exponents = [(w.count("z") - w.count("Z"), w.count("t") - w.count("T")) for w in words]
    return [
        [i, j] for i, j in combinations(range(len(words)), 2)
        if abs(exponents[i][0] * exponents[j][1] - exponents[i][1] * exponents[j][0]) == 1
    ]


def strict_path(start):
    rows = list(start)
    moves = []

    def do(m):
        moves.append(m)
        i = m["i"]
        if m["op"] == "multiply":
            rows[i] = reduce(rows[i] + rows[m["j"]])
        elif m["op"] == "invert":
            rows[i] = inverse(rows[i])
        else:
            rows[i] = reduce(m["g"] + rows[i] + inverse(m["g"]))

    def swap():
        previous = list(rows)
        do(multiply(0, 1))
        do(invert(0))
        do(multiply(1, 0))
        do(invert(0))
        donor = rows[1]
        do(multiply(0, 1))
        for letter in reversed(donor):
            do(conjugate(0, letter))
        do(invert(1))
        assert rows == previous[::-1]

    swap()
    do(invert(0))
    for i in (0, 1, 0, 1):
        do(multiply(i, 1 - i))
    assert rows == ["Yx", "X"]
    do(multiply(0, 1))
    do(invert(0))
    do(invert(1))
    swap()
    assert rows == ["x", "y"]
    return moves


def nontriangular_edge():
    steps = (0, 1, 0, 1)
    basis = ["z", "t"]
    for i in steps:
        basis[i] = reduce(basis[i] + basis[1 - i])
    u, v = basis
    left = ["z", "t", "Z" + v + "x", u + v + "y", "w"]
    right = [reduce(left[0] + left[2]), *left[1:]]
    assert auxiliary_unimodular_slots(left) == [[0, 1]]
    assert auxiliary_unimodular_slots(right) == [[0, 3]]
    assert triangular_frames(right, "zt") == []
    left_projection = [substitute(row, {"z": "", "t": ""}) for row in left[2:]]
    solutions = dict(zip("zt", invert_nielsen(["Yx", "X"], steps)))
    evaluated = [substitute(row, solutions) for row in right]
    assert evaluated[0] == evaluated[3] == ""
    right_projection = [evaluated[i] for i in (1, 2, 4)]
    assert left_projection == ["x", "y", "w"] and right_projection[-1] == "w"
    moves = strict_path(right_projection[:2])
    return {
        "padded_edge_from": left,
        "padded_edge_to": right,
        "exact_frame_slots": [[0, 1], [0, 3]],
        "right_triangular_frames": [],
        "marked_projections": [left_projection, right_projection],
        "right_to_left_moves_with_w_fixed": moves,
        "right_to_left_replay": replay_between(right_projection[:2], left_projection[:2], moves),
    }


if __name__ == "__main__":
    print(json.dumps({
        "nonfree_common_block": nonfree_common_block(),
        "nontriangular_exact_frame_edge": nontriangular_edge(),
    }, indent=2))
