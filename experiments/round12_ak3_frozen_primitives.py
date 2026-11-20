"""Replay the word and finite-group calculations for the new energy-20 charts."""

import json

from elementary_verify import inverse, reduce
from round03_frozen_donors import cycle_type, perm_inv, perm_mul
from round10_ac_proof_blocks import marked_group, vectors
from round12_ak3_torus_chart import DONOR, RECEIVER, primitive_obstruction
from stallings_search import graph


SECOND_DONOR, SECOND_RECEIVER = "xxxxyXXYY", "xxyyxYYYxxY"


def exponent(word, weights):
    return sum(a * b for a, b in zip(vectors(word), weights))


def first_pair_reverse_direction():
    x = (1, 3, 4, 5, 6, 7, 8, 2)
    y = (2, 1, 4, 6, 8, 7, 5, 3)
    image, identity, _, _, _ = marked_group("symmetric", 8, x, y)
    assert image(RECEIVER) == identity
    source = image(DONOR)
    actual = cycle_type(source)
    assert cycle_type(perm_inv(source)) == actual
    records = []
    for initial, period in (("xxyxy", "xxy"), ("x", "xxy")):
        assert graph((initial, period))[1] == 1
        translation = image(period)
        power = identity
        types = []
        while True:
            candidate = perm_mul(image(initial), power)
            shape = cycle_type(candidate)
            assert cycle_type(perm_inv(candidate)) == shape and shape != actual
            types.append(shape)
            power = perm_mul(power, translation)
            if power == identity:
                break
        records.append({"initial": initial, "period": period, "period_order": len(types), "cycle_types": types})
    exceptional = cycle_type(image("xy"))
    assert exceptional != actual
    return {"donor": RECEIVER, "receiver": DONOR, "marking": {"x": x, "y": y},
            "receiver_cycle_type": actual, "primitive_tail_residues": records, "exception_xy_cycle_type": exceptional}


def substitute(word, x, y):
    images = {"x": x, "y": y, "X": inverse(x), "Y": inverse(y)}
    return reduce("".join(images[c] for c in word))


def second_pair_amalgam():
    # Write a and b as x^2 and y in the original marking.
    assert substitute("xxyXYY", "xx", "y") == SECOND_DONOR
    # Here x denotes u and y denotes b in the substitutions.
    assert substitute("xxyXYY", "xy", "y") == "xyxyXYY"
    h = substitute("YYYxYxyy", "xx", "y")
    assert reduce("xxyy" + "x" + h + inverse("xxyy")) == SECOND_RECEIVER
    assert h == reduce("YYY" + "xxY" * 2 + "yyy")
    assert exponent(SECOND_RECEIVER, (1, 2)) == 1
    for u in ("x", "xY"):
        assert graph((u, "xxY"))[1] == 1
    # On F(u0,u1) use x=u0 and y=u1. Verify inverse monodromy.
    for letter in "xy":
        assert substitute(substitute(letter, "y", "xy"), "yX", "x") == letter
        assert substitute(substitute(letter, "yX", "x"), "y", "xy") == letter
    shifted = "x"
    for _ in range(3):
        shifted = substitute(shifted, "yX", "x")
    defect = inverse("xyxy")
    assert reduce(defect + "xx" + inverse(defect)) != "xx"
    return {"donor": SECOND_DONOR, "receiver": SECOND_RECEIVER, "amalgam_coefficient": h,
            "forward_monodromy": {"u0": "u1", "u1": "u0 u1"},
            "inverse_monodromy": {"u0": "u1 u0^-1", "u1": "u0"},
            "u_minus3_in_kernel_basis": shifted, "conjugation_defect_in_kernel_basis": defect,
            "defect_conjugate_of_u0_squared": reduce(defect + "xx" + inverse(defect))}


if __name__ == "__main__":
    print(json.dumps({"first_pair_torus": primitive_obstruction(),
                      "first_pair_reverse_direction": first_pair_reverse_direction(),
                      "second_pair_amalgam": second_pair_amalgam()}, indent=2))
