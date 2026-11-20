"""Replay spherical contractions and compile an exact fixed-donor hit."""

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
from round18_ak3_two_products_replay import conjugate, conjugator, rows


def permute_factors(indices, factors):
    terms = list(zip(indices, factors))
    assert sorted(indices) == list(range(len(factors)))
    for i in range(len(terms)):
        j = next(j for j in range(i, len(terms)) if terms[j][0] == i)
        while j > i:
            (a, left), (b, right) = terms[j-1:j+1]
            terms[j-1:j+1] = [(b, right), (a, conjugate(left, inverse(right)))]
            j -= 1
    return [word for _, word in terms]


def spherical_factors(words, tree):
    kind = tree["kind"]
    if kind == "contract":
        i, j = tree["i"], tree["j"]
        indices = [at for at in range(len(words)) if at not in (i, j)]
        rest = [words[at] for at in indices]
        a, b = rows(tree["merge"])
        coefficient = tree["coefficient"]
        child = spherical_factors(rest + ([coefficient] if coefficient else []), tree["child"])
        if coefficient:
            shift = conjugator(a + b, child.pop())
            a, b = (conjugate(w, shift) for w in (a, b))
        else:
            assert not reduce(a + b)
        result = permute_factors(indices + [i, j], child + [a, b])
    elif kind == "quadruple":
        left, right = rows(tree["left"]), rows(tree["right"])
        shift = conjugator("".join(right), inverse("".join(left)))
        result = permute_factors(tree["order"], [*left, *(conjugate(w, shift) for w in right)])
    elif kind == "triple":
        a, b = rows(tree["split"])
        result = [a, b, reduce(inverse(a + b))]
    elif kind == "pair":
        result = [words[0], inverse(words[0])]
    elif kind == "empty":
        result = []
    else:
        raise ValueError(kind)
    assert len(result) == len(words) and not reduce("".join(result))
    for expected, actual in zip(words, result):
        conjugator(expected, actual)
    return result


def control_source():
    donor = "xxxyyXXYY"
    receiver = cyclic("y" + "".join(conjugate(inverse(donor), g) for g in ("x", "y", "xy")))
    assert not any(map(primitive_cyclic_word, (receiver, donor)))
    return receiver, donor


def compile_hit(hit):
    assert hit["first_sign"] == 0
    primitive = hit["primitive"]
    assert primitive_cyclic_word(primitive)
    source = hit["source"]
    r, d = hit["working_pair"]
    receiver = source.index(r)
    donor = 1 - receiver
    assert source[donor] == d
    basis = hit["boundary"]
    assert basis[0] == r and basis[-1] == inverse(primitive) and len(basis) == 5
    factors = spherical_factors(basis, hit["equation"])
    shift = conjugator(factors[0], r)
    factors = [conjugate(word, shift) for word in factors]
    path = StrictPath(source, BytesIO())
    for term, factor in zip(basis[1:-1], factors[1:-1]):
        assert term in (d, inverse(d))
        path.factor(receiver, donor, 1 if term == d else -1, conjugator(term, factor))
    assert path.rows[receiver] == inverse(factors[-1]) and path.rows[donor] == d
    primitive_steps = path.total
    oriented = (primitive, d)
    path.extend(normalize_pair(tuple(path.rows), oriented))
    path.extend(primitive_to_basis(oriented))
    proof = {
        "format": "ordinary-ac-elementary-v1",
        "start": source, "target": path.rows,
        "moves": [json.loads(line) for line in path.sink.getvalue().splitlines()[1:]],
    }
    return proof, {
        **replay(proof), "cyclic_peak": cyclic_peak(proof),
        "primitive_exposed_at": primitive_steps,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", nargs="?", type=Path)
    parser.add_argument("ledger", nargs="?", type=Path)
    parser.add_argument("--write-control", type=Path)
    args = parser.parse_args()
    if args.write_control:
        args.write_control.write_text("\t".join(control_source()) + "\n")
    else:
        receipt = json.loads(args.receipt.read_bytes())
        for hit in receipt["hits"]:
            spherical_factors(hit["boundary"], hit["equation"])
        if args.ledger:
            assert len(receipt["hits"]) == 1 and receipt["mode"] == "fixed"
            proof, checked = compile_hit(receipt["hits"][0])
            args.ledger.write_text(json.dumps(proof, separators=(",", ":")) + "\n")
            print(json.dumps(checked))
        else:
            print(json.dumps({"spherical_witnesses_replayed": len(receipt["hits"])}))
