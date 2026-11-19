"""Verify the two compiled corrections for AK(3) modulo gamma_3 of the braid kernel."""

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from braid_relation_module import IDENTITY, LETTERS, product
from elementary_verify import inverse, reduce, replay

SOURCE = Path(__file__).resolve().parents[1] / "certificates/optimized_first_order_strict.json"


def schreier_degree_two(word):
    """Read a closed path in an actual Schreier basis and expand to degree two."""
    vertex = IDENTITY
    seen = {vertex}
    tree_edges = set()
    path = []
    for letter in word:
        successor = product(vertex, LETTERS[letter])
        sign = 1 if letter.islower() else -1
        edge = (vertex if sign == 1 else successor, letter.lower())
        path.append((edge, sign))
        if successor not in seen:
            seen.add(successor)
            tree_edges.add(edge)
        vertex = successor
    assert vertex == IDENTITY

    # The first-arrival edges form a genuine tree, extendible to any
    # spanning tree of the full braid Cayley graph.
    linear = {}
    quadratic = defaultdict(int)
    basis_edges = set()
    schreier_letters = 0
    for edge, sign in path:
        if edge in tree_edges:
            continue
        basis_edges.add(edge)
        schreier_letters += 1
        for j, coefficient in linear.items():
            quadratic[j, edge] += coefficient * sign
        if sign == -1:
            quadratic[edge, edge] += 1
        updated = linear.get(edge, 0) + sign
        if updated:
            linear[edge] = updated
        else:
            linear.pop(edge, None)
    return {
        "free_word_length": len(word),
        "braid_vertices": len(seen),
        "schreier_letters": schreier_letters,
        "schreier_basis_edges": len(basis_edges),
        "degree_one_support": len(linear),
        "degree_two_support": sum(coefficient != 0 for coefficient in quadratic.values()),
    }


def power(letter, exponent):
    return letter * exponent if exponent >= 0 else inverse(letter) * -exponent


def collect(word, target):
    """Write word as conjugates of the other symbol by powers of target."""
    exponent = 0
    factors = []
    for letter in word:
        if letter.lower() == target:
            exponent += 1 if letter.islower() else -1
        else:
            factors.append((exponent, letter))
    assert exponent == 0
    reconstructed = "".join(
        power(target, exponent) + letter + power(target, -exponent)
        for exponent, letter in factors
    )
    assert reduce(reconstructed) == word
    return factors


def substitute(word, current):
    images = dict(zip("xy", current))
    images.update({letter.upper(): inverse(image) for letter, image in list(images.items())})
    return reduce("".join(images[letter] for letter in word))


def compile_correction(current, slot):
    target = "xy"[slot]
    error = reduce(inverse(current[slot]) + target)
    factors = collect(error, target)
    before = schreier_degree_two(error)
    assert before["degree_one_support"] == 0
    assert before["degree_two_support"] > 0
    corrected = reduce(current[slot] + substitute(error, current))
    residual = reduce(inverse(corrected) + target)
    after = schreier_degree_two(residual)
    assert after["degree_one_support"] == after["degree_two_support"] == 0
    return {
        "target": target,
        "donor_factors": len(factors),
        "total_conjugator_power": sum(abs(exponent) for exponent, _ in factors),
        "strict_word_moves_from_this_stage": sum(
            1 + 2 * abs(exponent) * len(current[slot]) + 2 * letter.isupper()
            for exponent, letter in factors
        ),
        "before": before,
        "after": after,
    }


def main():
    data = SOURCE.read_bytes()
    prefix = replay(json.loads(data))
    u, v = prefix["endpoint"]
    first = compile_correction((u, v), 0)
    # In this quotient the first corrected row is x. The second calculation
    # uses that equality and does not claim the displayed free words are x,y.
    second = compile_correction(("x", v), 1)
    print(json.dumps({
        "prefix_sha256": hashlib.sha256(data).hexdigest(),
        "prefix_moves": prefix["moves"],
        "verified_ambient_quotient": "F/gamma_3(N), N the braid normal closure",
        "corrections": [first, second],
    }, indent=2))


if __name__ == "__main__":
    main()
