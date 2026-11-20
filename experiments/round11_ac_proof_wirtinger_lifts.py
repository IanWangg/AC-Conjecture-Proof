"""Check Schreier identities, permutation residues, and strict outer lifts."""

import json

from elementary_verify import inverse, reduce, replay
from round10_ac_proof_blocks import A, B, C, marked_group, vectors


MARKINGS = {
    "round11_degree5": ((1, 2, 4, 5, 3), (3, 4, 2, 5, 1)),
    "round11_degree7": ((1, 2, 4, 3, 6, 7, 5), (5, 6, 2, 4, 3, 1, 7)),
    "rigid_middle_degree8": ((1, 3, 4, 5, 6, 7, 8, 2), (2, 6, 8, 4, 3, 7, 5, 1)),
    "dihedral_order14": ((1, 7, 6, 5, 4, 3, 2), (2, 3, 4, 5, 6, 7, 1)),
}


def commutator(a, b):
    return reduce(a + b + inverse(a) + inverse(b))


def signed_power(g, exponent):
    return g * exponent if exponent >= 0 else inverse(g) * -exponent


def schreier(word):
    height = 0
    factors = []
    for letter in word:
        if letter.lower() == "x":
            height += 1 if letter == "x" else -1
        else:
            factors.append((height, letter))
    rebuilt = "".join(signed_power("x", k) + letter + signed_power("x", -k)
                      for k, letter in factors) + signed_power("x", height)
    assert reduce(rebuilt) == reduce(word)
    return {"schreier_factors": factors, "trailing_x_power": height}


def exact_identities():
    assert tuple(map(vectors, (A, B, C))) == ((0, -1), (-1, -1), (-1, -1))
    comm = commutator("xYX", "Y")
    base_change = "yyXY"
    assert reduce(inverse(B) + C) == reduce(base_change + comm + inverse(base_change))
    normal_form = schreier(B)
    assert normal_form["schreier_factors"] == [(-2, "Y"), (-1, "y"), (-2, "y"),
                                                (-1, "Y"), (-1, "Y")]
    assert normal_form["trailing_x_power"] == -1
    return {"rows": [A, B, C], "exponent_vectors": tuple(map(vectors, (A, B, C))),
            "B_inverse_C_conjugator": base_change, "B_inverse_C_cyclic_core": comm,
            "B_schreier_normal_form": normal_form}


def residue_separator():
    x, y = MARKINGS["rigid_middle_degree8"]
    image, identity, multiply, invert, cycle_type = marked_group("symmetric", 8, x, y)
    assert image(B) == identity
    source = image(A)
    assert cycle_type(source) == cycle_type(invert(source)) == (4, 4)
    step, tail = image("yxYX"), image("xYX")
    power = identity
    residues = []
    while True:
        candidate = multiply(power, tail)
        invariant = cycle_type(candidate)
        assert invariant == cycle_type(invert(candidate))
        assert invariant != cycle_type(source)
        residues.append({"p": len(residues), "image": candidate, "cycle_type": invariant})
        power = multiply(power, step)
        if power == identity:
            break
    assert len(residues) == 6
    return {"marking": {"x": x, "y": y}, "B_image": image(B), "A_image": source,
            "A_cycle_type": cycle_type(source), "step_word": "yxYX",
            "step_image": step, "period": len(residues), "tail_word": "xYX",
            "tail_image": tail, "residues": residues}


def donor_product(sign, conjugator):
    conjugations = [{"op": "conjugate", "i": 1, "g": g}
                    for g in reversed(conjugator)]
    invert = [{"op": "invert", "i": 1}] if sign == -1 else []
    undo = [{"op": "conjugate", "i": 1, "g": g}
            for g in reversed(inverse(conjugator))]
    return invert + conjugations + [{"op": "multiply", "i": 0, "j": 1}] + undo + invert


def outer_replays():
    g = "Y"
    conjugated_c = reduce(g + C + inverse(g))
    correction = commutator(B, conjugated_c)
    middle = reduce(A + correction)
    routes = []
    for donor, products in ((B, [(1, ""), (-1, conjugated_c)]),
                            (C, [(1, reduce(B + g)), (-1, g)])):
        certificate = {"format": "ordinary-ac-elementary-v1",
                       "start": [A, donor], "target": [middle, donor],
                       "moves": [move for sign, word in products
                                 for move in donor_product(sign, word)]}
        receipt = replay(certificate)
        assert receipt["endpoint"] == [middle, donor]
        routes.append({"donor": donor, "signed_conjugate_products": products, **receipt})
    return middle, {"commutator_conjugator": g, "correction": correction,
                    "word": middle, "outer_replays": routes}


def group_generated(generators, identity, multiply):
    found = {identity}
    pending = [identity]
    for current in pending:
        for generator in generators:
            product = multiply(current, generator)
            if product not in found:
                found.add(product)
                pending.append(product)
    return found


def normal_subgroup(value, marking, identity, multiply, invert):
    conjugates = {value}
    pending = [value]
    for current in pending:
        for generator in marking:
            conjugate = multiply(multiply(generator, current), invert(generator))
            if conjugate not in conjugates:
                conjugates.add(conjugate)
                pending.append(conjugate)
    generators = []
    subgroup = {identity}
    for conjugate in pending:
        if conjugate not in subgroup:
            generators.append(conjugate)
            subgroup = group_generated(generators, identity, multiply)
    return subgroup


def finite_lift_checks(middle):
    output = {}
    for name, (x, y) in MARKINGS.items():
        image, identity, multiply, invert, cycle_type = marked_group("symmetric", len(x), x, y)
        subgroup = normal_subgroup(image(middle), (x, y), identity, multiply, invert)
        assert y in subgroup
        assert multiply(image(B), invert(image(C))) in subgroup
        quotient_order = len(group_generated((x, y), identity, multiply)) // len(subgroup)
        output[name] = {"marking": {"x": x, "y": y},
                        "A_cycle_type": cycle_type(image(A)),
                        "middle_cycle_type": cycle_type(image(middle)),
                        "y_in_normal_closure": True, "normal_closure_order": len(subgroup),
                        "quotient_order": quotient_order}
    return output


def main():
    middle, outer = outer_replays()
    print(json.dumps({"exact_identities": exact_identities(),
                      "rigid_middle_separator": residue_separator(),
                      "finite_lift_example": {**outer, "checks": finite_lift_checks(middle)}},
                     indent=2))


if __name__ == "__main__":
    main()
