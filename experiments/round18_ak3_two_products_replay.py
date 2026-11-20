"""Compile a four-boundary meeting into two strict ordinary products."""

import argparse
from io import BytesIO
import json
from pathlib import Path

from elementary_verify import inverse, reduce, replay
from euclidean_primitive_audit import primitive_cyclic_word
from free_waypoint_search import cyclic
from round06_stable_proof_strict_escape import StrictPath
from round07_automorphism_transport import normalize_pair
from round08_ak3_acm_search import cyclic_peak
from round13_ak3_primitive_third import primitive_to_basis


def conjugate(word, by):
    return reduce(by + word + inverse(by))


def strip(word):
    original = word = reduce(word)
    cut = 0
    while len(word) > 1 and word[0] == word[-1].swapcase():
        cut += 1
        word = word[1:-1]
    return original[:cut], word


def conjugator(source, target):
    """Return a word g satisfying g source g^-1 = target."""
    left, a = strip(source)
    right, b = strip(target)
    assert len(a) == len(b)
    if not a:
        return ""
    cut = (a + a).find(b)
    assert 0 <= cut < len(a)
    answer = reduce(right + inverse(a[:cut]) + inverse(left))
    assert conjugate(source, answer) == reduce(target)
    return answer


def rows(split):
    first, second, bridge = split
    return first, conjugate(second, bridge)


def control_source():
    donor = "xxxyyXXYY"
    receiver = cyclic("y" + conjugate(inverse(donor), "x") + conjugate(inverse(donor), "y"))
    assert not any(map(primitive_cyclic_word, (receiver, donor)))
    return receiver, donor


def compile_hit(hit):
    source = tuple(hit["source"])
    donor = hit["donor_index"]
    receiver = 1 - donor
    primitive = hit["primitive"]
    assert primitive_cyclic_word(primitive)
    initial_signs = {0: (1, -1), 2: (1, 1), -2: (-1, -1)}[hit["axial_coefficient"]]
    expected = (
        source[receiver],
        source[donor] if initial_signs[0] > 0 else inverse(source[donor]),
        source[donor] if initial_signs[1] > 0 else inverse(source[donor]),
        inverse(primitive),
    )
    left, right = rows(hit["left"]), rows(hit["right"])
    shift = conjugator("".join(right), inverse("".join(left)))
    factors = list(zip(hit["order"], (*left, *(conjugate(w, shift) for w in right))))
    assert sorted(i for i, _ in factors) == list(range(4))
    assert not reduce("".join(w for _, w in factors))
    for i, word in factors:
        conjugator(expected[i], word)

    # Adjacent Hurwitz swaps change the order while preserving the product.
    for i in range(len(factors)):
        j = next(j for j in range(i, len(factors)) if factors[j][0] == i)
        while j > i:
            (a, u), (b, v) = factors[j-1:j+1]
            factors[j-1:j+1] = [(b, v), (a, conjugate(u, inverse(v)))]
            j -= 1
    shift = conjugator(factors[0][1], source[receiver])
    factors = [conjugate(w, shift) for _, w in factors]
    assert factors[0] == source[receiver] and not reduce("".join(factors))
    path = StrictPath(source, BytesIO())
    for at, sign in enumerate(initial_signs, start=1):
        g = conjugator(expected[at], factors[at])
        path.factor(receiver, donor, sign, g)
    assert path.rows[receiver] == inverse(factors[3]) and path.rows[donor] == source[donor]
    oriented = (primitive, source[donor])
    path.extend(normalize_pair(tuple(path.rows), oriented))
    path.extend(primitive_to_basis(oriented))
    proof = {
        "format": "ordinary-ac-elementary-v1",
        "start": source, "target": path.rows,
        "moves": [json.loads(row) for row in path.sink.getvalue().splitlines()[1:]],
    }
    checked = {**replay({**proof, "start": list(source)}), "cyclic_peak": cyclic_peak(proof)}
    return proof, checked


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", nargs="?", type=Path)
    parser.add_argument("ledger", nargs="?", type=Path)
    parser.add_argument("--write-control", type=Path)
    args = parser.parse_args()
    if args.write_control:
        args.write_control.write_text("\t".join(control_source()) + "\n")
    else:
        hit = json.loads(args.receipt.read_bytes())["hit"]
        proof, checked = compile_hit(hit)
        args.ledger.write_text(json.dumps(proof, separators=(",", ":")) + "\n")
        print(json.dumps(checked))
