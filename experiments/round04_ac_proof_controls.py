"""Exact mismatch controls for marked Andrews–Curtis projection."""

from itertools import combinations, permutations
import json

from round02_ac_proof_controls import conjugate, cyclic, invert, multiply
from round03_ac_proof_controls import replay_between, substitute
from stallings_search import inverse, reduce


def exponent(word, generator):
    return word.count(generator) - word.count(generator.upper())


def determinant(rows):
    total = 0
    for cols in permutations(range(len(rows))):
        inversions = sum(a > b for a, b in combinations(cols, 2))
        term = (-1) ** inversions
        for i, j in enumerate(cols):
            term *= rows[i][j]
        total += term
    return total


def admissible_minors(words, auxiliaries):
    vectors = [tuple(exponent(word, a) for a in auxiliaries) for word in words]
    return [
        list(slots) for slots in combinations(range(len(words)), len(auxiliaries))
        if abs(determinant([vectors[i] for i in slots])) == 1
    ]


def project(words, slots, chart):
    evaluated = [substitute(word, chart) for word in words]
    assert all(not evaluated[i] for i in slots)
    return [word for i, word in enumerate(evaluated) if i not in slots]


def two_auxiliary():
    receiver = "zztZTzzt"
    donor = reduce(inverse(receiver) + "z")
    product = reduce(receiver + donor)
    assert product == "z"
    left = [receiver, donor, "tX", "ytt"]
    right = [product, *left[1:]]
    assert admissible_minors(left, "zt") == [[0, 1]]
    assert admissible_minors(right, "zt") == [[0, 1], [0, 2]]
    assert tuple(exponent(receiver, a) for a in "zt") == (3, 1)
    assert len(cyclic(receiver)) == 8
    assert substitute(receiver, {"z": ""}) == "t"
    projected_left = project(left, [0, 1], {"z": "", "t": ""})
    projected_right = project(right, [0, 2], {"z": "", "t": "x"})
    assert (projected_left, projected_right) == (["X", "y"], ["X", "yxx"])
    moves = [invert(0), multiply(1, 0), multiply(1, 0), invert(0)]
    return {
        "edge_from": left,
        "edge_to": right,
        "chosen_slots": [[0, 1], [0, 2]],
        "projections": [projected_left, projected_right],
        "projected_moves": moves,
        "projected_replay": replay_between(projected_left, projected_right, moves),
    }


def check_whitehead_minimum(words, alphabet, automorphisms):
    words = [cyclic(word) for word in words]
    for images in automorphisms:
        previous = sum(map(len, words))
        words = [cyclic(substitute(word, images)) for word in words]
        assert sum(map(len, words)) < previous
    signed = "".join(a + a.upper() for a in alphabet)
    corners = [
        (a, b.swapcase()) for word in words
        for a, b in zip(word, word[1:] + word[:1])
    ]
    certificates = {}
    for generator in alphabet:
        degree = sum(generator in edge for edge in corners)
        free_vertices = [v for v in signed if v.lower() != generator]
        minimum = len(corners)
        for mask in range(1 << len(free_vertices)):
            side = {generator} | {v for i, v in enumerate(free_vertices) if mask >> i & 1}
            crossing = sum((u in side) != (v in side) for u, v in corners)
            minimum = min(minimum, crossing)
        assert minimum == degree
        certificates[generator] = [degree, minimum]
    return {"minimal_words": words, "degree_and_minimum_cut": certificates}


def three_auxiliary():
    bridge = "tuz"
    receiver, donor = "z", reduce(bridge + "t" + inverse(bridge))
    product = reduce(receiver + donor)

    # In the relative basis (product, z, bridge), take the inverses A,B of its
    # last two entries and perform B1=B A, beta=A B1^2, gamma=B1 beta.
    first, second = "Z", inverse(bridge)
    second1 = second + first
    beta = first + second1 * 2
    gamma = second1 + beta
    left = [receiver, donor, "u", reduce(product * 2 + beta + "x"),
            reduce(product * 5 + gamma + "y")]
    right = [product, *left[1:]]
    middle = [receiver, product, *left[2:]]
    assert admissible_minors(left, "ztu") == [[0, 1, 2]]
    assert admissible_minors(right, "ztu") == [[0, 1, 2], [0, 3, 4]]
    assert admissible_minors(middle, "ztu") == [[0, 1, 2], [1, 3, 4]]

    transported_at_right = check_whitehead_minimum(
        ["x", "y", product, donor, "u"], "xyztu",
        [{"t": "Ztz", "u": "Zu"}, {"u": "Tu"}],
    )
    transported_at_middle = check_whitehead_minimum(
        ["x", "y", receiver, product, "u"], "xyztu",
        [{"t": "Zt"}, {"u": "Tu"}],
    )
    for record in (transported_at_right, transported_at_middle):
        assert sum(map(len, record["minimal_words"])) == 10

    quotient_by_product = {"t": "WZw", "u": "WzwwZ"}
    assert substitute(bridge, quotient_by_product) == "w"
    assert substitute(product, quotient_by_product) == ""
    quotient_residual_frame = [substitute(row, quotient_by_product) for row in (receiver, "u")]
    assert quotient_residual_frame == ["z", "WzwwZ"]
    assert tuple(exponent(cyclic(quotient_residual_frame[1]), a) for a in "zw") == (0, 1)
    assert len(cyclic(quotient_residual_frame[1])) == 5

    second1_image = "Yx"
    first_image = reduce("X" + inverse(second1_image) * 2)
    second_image = reduce(second1_image + inverse(first_image))
    z = inverse(first_image)
    w = inverse(second_image)
    t = reduce(inverse(w) + inverse(z) + w)
    u = reduce(inverse(t) + w + inverse(z))
    left_projection = project(left, [0, 1, 2], dict.fromkeys("ztu", ""))
    chart = {"z": z, "t": t, "u": u}
    right_projection = project(right, [0, 3, 4], chart)
    assert left_projection == ["x", "y"]
    assert right_projection == [first_image, u]
    assert u == reduce(second_image + inverse(first_image) + w * 2 + first_image)

    power = reduce(second_image * 2)
    moves = [invert(0), multiply(1, 0), invert(0)]
    moves += [conjugate(0, c) for c in reversed(power)]
    moves += [multiply(1, 0)]
    moves += [conjugate(0, c) for c in reversed(inverse(power))]
    moves += [
        invert(1), multiply(1, 0), multiply(0, 1), multiply(0, 1), multiply(1, 0),
        invert(0), invert(1),
    ]
    return {
        "edge_from": left,
        "edge_to": right,
        "middle_tuple": middle,
        "chosen_slots": [[0, 1, 2], [0, 3, 4]],
        "transported_at_right": transported_at_right,
        "transported_at_middle": transported_at_middle,
        "old_residual_frame_after_killing_product": quotient_residual_frame,
        "right_chart": chart,
        "projections": [left_projection, right_projection],
        "right_to_left_moves": moves,
        "projected_replay": replay_between(right_projection, left_projection, moves),
    }


if __name__ == "__main__":
    print(json.dumps({"two_auxiliary": two_auxiliary(), "three_auxiliary": three_auxiliary()}, indent=2))
