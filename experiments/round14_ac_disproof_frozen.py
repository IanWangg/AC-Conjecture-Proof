"""Replay all-length frozen primitive exclusions for E24 and four E23 projections."""

import json
from functools import cache
from math import lcm

from elementary_verify import inverse
from primitive_map_pairs import fold
from round10_ac_proof_blocks import det, marked_group, vectors
from round11_ac_disproof_wirtinger import ROSE
from round13_ac_disproof_external import PAIR, ROOT
from round14_ak3_sheared_fox import (
    abel,
    affine_system,
    dot,
    flow,
    inconsistency,
    orbits,
    rewrite,
    solve,
    substitute,
)
from stallings_search import reduce


CYCLE9 = (2, 3, 4, 5, 6, 7, 8, 9, 1)
E24_MARKINGS = (
    (
        (CYCLE9, (1, 4, 6, 2, 3, 8, 9, 7, 5)),
        (CYCLE9, (2, 4, 6, 7, 9, 1, 8, 5, 3)),
    ),
    (((1, 3, 2, 5, 6, 4), (2, 4, 5, 3, 1, 6)),),
)

SHORT_BASES = (
    (("Yxxxxxxx", "Yxxxxxx"), ("Yxxxxxx", "Yxxxxxxx")),
    (("XY", "xyxyx"), ("xxyxy", "YX")),
    (("Yx", "YYx"), ("YYx", "Yx")),
    (("xyy", "xyyy"), ("xyyy", "xyy")),
)

SHORT_MARKINGS = {
    (0, 0): (((1, 2, 4, 5, 6, 7, 8, 9, 3), (3, 5, 1, 2, 7, 8, 9, 6, 4)),),
    (1, 0): (
        ((1, 3, 4, 2, 6, 7, 5), (2, 1, 3, 5, 4, 6, 7)),
        ((2, 3, 4, 1, 6, 7, 8, 5), (2, 4, 5, 3, 8, 7, 1, 6)),
    ),
    (1, 1): (((2, 3, 4, 5, 6, 7, 8, 1), (2, 3, 7, 6, 1, 8, 4, 5)),),
    (2, 0): ((CYCLE9, (1, 3, 5, 9, 6, 8, 7, 2, 4)),),
    (2, 1): (
        ((2, 3, 4, 5, 1), (1, 2, 5, 3, 4)),
        ((2, 1, 4, 5, 6, 3), (1, 3, 4, 2, 5, 6)),
    ),
    (3, 0): (
        ((1, 3, 4, 5, 6, 7, 8, 2), (2, 3, 1, 7, 5, 6, 8, 4)),
        ((1, 2, 4, 5, 6, 7, 8, 9, 3), (3, 5, 7, 8, 1, 9, 4, 6, 2)),
    ),
    (3, 1): (
        ((1, 2, 4, 5, 3), (2, 3, 1, 4, 5)),
        ((1, 2, 3, 5, 6, 4), (2, 4, 5, 1, 6, 3)),
    ),
}


def validate_family(fixed, source, transverse, axial):
    assert fold((transverse, axial)) == ROSE
    assert abs(det(vectors(fixed), vectors(source))) == 1
    assert vectors(transverse) == vectors(source)
    assert vectors(axial) in (vectors(fixed), tuple(-x for x in vectors(fixed)))


def permutation_residues(fixed, source, transverse, axial, markings):
    records = []
    for x, y in markings:
        image, identity, multiply, invert, cycle_type = marked_group(
            "symmetric", len(x), x, y
        )
        assert image(fixed) == identity
        want = cycle_type(image(source))
        assert want == cycle_type(invert(image(source)))
        start, increment = image(transverse), image(axial)
        power, shapes = identity, []
        while True:
            element = multiply(start, power)
            shape = cycle_type(element)
            assert shape == cycle_type(invert(element))
            shapes.append(shape)
            power = multiply(power, increment)
            if power == identity:
                break
        records.append(
            {
                "x": x,
                "y": y,
                "source_cycle_type": want,
                "period": len(shapes),
                "tail_cycle_types": shapes,
                "allowed_residues": [
                    i for i, shape in enumerate(shapes) if shape == want
                ],
            }
        )
    period = lcm(*(row["period"] for row in records))
    survivors = [
        i
        for i in range(period)
        if all(i % row["period"] in row["allowed_residues"] for row in records)
    ]
    return {"markings": records, "combined_period": period, "survivors": survivors}


def rank_seven_fox(fixed, source, transverse, axial):
    names = "abcdefg"
    images = ("b", "c", "d", "e", "f", "g", "AcDf")
    backward = ("bCeG", "a", "b", "c", "d", "e", "f")
    for first, second in ((images, backward), (backward, images)):
        assert tuple(substitute(word, names, first) for word in second) == tuple(names)

    def mark(word):
        return reduce(
            "".join(
                {"x": "x", "X": "X", "y": "yxxxxxxx", "Y": "XXXXXXXY"}[c] for c in word
            )
        )

    @cache
    def generator(index):
        if index < -3:
            return substitute(generator(index + 1), names, backward)
        if index > 3:
            return substitute(generator(index - 1), names, images)
        return names[index + 3]

    def expand(word):
        terms, height = rewrite(mark(word))
        expanded = reduce(
            "".join(
                generator(at) if sign > 0 else inverse(generator(at))
                for at, sign in terms
            )
        )
        return expanded, height

    def normalized(word):
        if rewrite(mark(word))[1] < 0:
            word = inverse(word)
        expanded, height = expand(word)
        assert height == 1
        return expanded

    donor_factors = rewrite(mark(fixed))
    assert donor_factors == ([(2, 1), (4, -1), (-3, -1), (-1, 1), (0, -1)], 0)
    assert expand(fixed) == ("", 0)
    kernel_source = normalized(source)
    columns = [abel(image, names) for image in images]
    equation = [
        [int(i == j) - col[i] for j, col in enumerate(columns)]
        for i in range(len(names))
    ]
    for i in range(len(names)):
        solve(equation, [int(i == j) for j in range(len(names))])

    roots, prime = (1, 2, 4, 3), 5
    period = len(roots) * prime
    powers, height = expand(axial * period)
    assert height == 0 and not any(value % len(roots) for value in abel(powers, names))
    all_orbits = list(orbits(columns, len(roots)))
    assert sum(map(len, all_orbits)) == len(roots) ** len(names)
    assert all(
        not any(value % prime for value in flow(powers, names, chi, roots))
        for orbit in all_orbits
        for chi in orbit
    )
    check_word = "abCd"
    check_g = abel(check_word, names)
    check_target = reduce(
        inverse(check_word) + kernel_source + substitute(check_word, names, images)
    )
    source_vector = abel(kernel_source, names)
    assert (
        solve(
            equation, [a - b for a, b in zip(source_vector, abel(check_target, names))]
        )
        == check_g
    )
    for orbit in all_orbits:
        system = affine_system(
            names, images, kernel_source, check_target, check_g, orbit, roots, prime
        )
        check_flow = flow(check_word, names, orbit[0], roots)
        assert all((dot(row[:-1], check_flow) - row[-1]) % prime == 0 for row in system)

    witnesses = {}
    for n in range(period):
        word = normalized(transverse + axial * n)
        vector = solve(
            equation, [a - b for a, b in zip(source_vector, abel(word, names))]
        )
        for orbit in all_orbits:
            system = affine_system(
                names, images, kernel_source, word, vector, orbit, roots, prime
            )
            contradiction = inconsistency(system, prime)
            if contradiction is None:
                continue
            dual, incompatible = contradiction
            assert tuple(dot(dual, col) % prime for col in zip(*system)) == incompatible
            assert incompatible[:-1] == (0,) * len(names) and incompatible[-1] != 0
            witnesses[n] = {
                "initial_character": orbit[0],
                "orbit_length": len(orbit),
                "augmented_matrix": system,
                "dual_row": dual,
                "nonzero_residue": incompatible[-1],
            }
            break
    assert len(witnesses) == period
    return {
        "basis": names,
        "monodromy": images,
        "inverse_monodromy": backward,
        "donor_schreier_factors": donor_factors,
        "roots": roots,
        "prime": prime,
        "period": period,
        "character_orbits": len(all_orbits),
        "genuine_conjugacy_control": check_word,
        "residue_contradictions": witnesses,
    }


def check_direction(pair, slot, family, markings=None):
    source, fixed = pair[1 - slot], pair[slot]
    validate_family(fixed, source, *family)
    if markings:
        proof = permutation_residues(fixed, source, *family, markings)
        assert not proof["survivors"]
    else:
        proof = rank_seven_fox(fixed, source, *family)
    return {"pair": pair, "fixed_slot": slot, "primitive_basis": family, "proof": proof}


def main():
    short = json.loads(
        (ROOT / "results/round13_stable_proof_whitehead.json").read_text()
    )
    pairs = short["coverage32"]["shortest_absent"][:4]
    assert all(sum(map(len, pair)) == 23 for pair in pairs)
    control = permutation_residues("x", "y", "y", "x", [((1, 2, 3), (2, 3, 1))])
    assert control["survivors"] == [0]
    return {
        "external_e24": [
            check_direction(PAIR, j, family, E24_MARKINGS[j])
            for j, family in enumerate((("y", "xyy"), ("XYY", "y")))
        ],
        "short_e23": [
            check_direction(pair, j, SHORT_BASES[i][j], SHORT_MARKINGS.get((i, j)))
            for i, pair in enumerate(pairs)
            for j in range(2)
        ],
        "known_positive_control": control,
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
