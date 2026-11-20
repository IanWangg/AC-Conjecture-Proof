"""Pack and replay the exact obstructions to a fourth receiving block."""

import argparse
import json
import re
from collections import Counter, defaultdict
from fractions import Fraction
from functools import cache, lru_cache
from hashlib import sha256
from pathlib import Path

from elementary_verify import reduce
from free_waypoint_search import canonical
from round10_ac_proof_blocks import marked_group
from round13_ak3_primitive_third import changed_basis, image
from round14_ak3_sheared_fox import MARKINGS, separate

AMALGAM_DONOR = "XXYxxYxxYxxyXXy"


def mark(word):
    shear = changed_basis(1, False, False)
    return image(image(word, shear), shear)


def lifted_factor(word):
    (odd,) = (m for m in re.finditer("[xX]+", word) if len(m[0]) % 2)
    odd_letter = odd[0][0]
    remainder = reduce(word[odd.start() + 1 :] + word[: odd.start()])
    factor = []
    for run in re.findall("[xX]+|[yY]+", remainder):
        if run[0] in "xX":
            assert len(run) % 2 == 0
            factor.append(("t" if run[0] == "x" else "T") * (len(run) // 2))
        else:
            factor.append(run.translate(str.maketrans("yY", "aA")))
    return odd_letter, "".join(factor)


def affine(word):
    translation, height = Fraction(), 0
    for letter in word:
        if letter in "tT":
            height += 1 if letter == "t" else -1
        elif letter in "aA":
            translation += (1 if letter == "a" else -1) * Fraction(3, 2) ** height
        else:
            raise ValueError(letter)
    return translation, height


def valuation(rational, prime):
    numerator, denominator = rational.numerator, rational.denominator
    assert numerator
    net = 0
    while numerator % prime == 0:
        numerator //= prime
        net += 1
    while denominator % prime == 0:
        denominator //= prime
        net -= 1
    return net


def amalgam_separation(donor, source, target):
    relator = canonical(mark(donor))
    assert relator == "XXYYYxxyy"
    assert affine("TAAAtaa") == (0, 0)
    a, first = lifted_factor(mark(source))
    b, second = lifted_factor(mark(target))
    first_translation, first_height = affine(first)
    second_translation, second_height = affine(second)
    if not first_translation or not second_translation:
        return None
    first_signature = sum(valuation(first_translation, p) for p in (2, 3))
    second_signature = sum(valuation(second_translation, p) for p in (2, 3))
    if first_signature == second_signature:
        return None
    return {
        "donor": donor,
        "source": source,
        "target": target,
        "marked_relator": relator,
        "odd_cyclic_factors": [a, b],
        "affine_words": [first, second],
        "translations": list(map(str, (first_translation, second_translation))),
        "scaling_heights": [first_height, second_height],
        "sum_of_valuations": [first_signature, second_signature],
    }


def pack(raw, permutations):
    source = raw.read_bytes()
    receipt = json.loads(source)
    perm_bytes = permutations.read_bytes()
    perm = json.loads(perm_bytes)
    assert perm["contacts_sha256"] == sha256(source).hexdigest()
    by_donor = defaultdict(set)
    for e, s, choices in receipt.pop("fourth_queries"):
        by_donor[s].update((f, e) for f in choices)
    groups = []
    for s, pairs in sorted(by_donor.items()):
        left, right = (sorted({row[i] for row in pairs}) for i in (0, 1))
        assert pairs == {(f, e) for f in left for e in right if f != e}
        groups.append([s, left, right])
    assert "last_contacts" not in receipt
    receipt["last_contacts"] = groups
    receipt["raw_search_sha256"] = sha256(source).hexdigest()
    receipt["raw_separator_sha256"] = sha256(perm_bytes).hexdigest()
    marks = {
        (tuple(w["x"]), tuple(w["y"]))
        for row in perm["records"]
        for w in row["witnesses"].values()
    }
    receipt["permutation_markings"] = [list(map(list, row)) for row in sorted(marks)]
    result = audit(receipt)
    assert result["permutation_excluded"] >= perm["exactly_excluded"]
    receipt["fourth_exact_obstructions"] = result
    return receipt


def audit(receipt):
    closed, residual = Counter(), defaultdict(set)
    markings = []
    for x, y in receipt["permutation_markings"]:
        assert len(x) == len(y) <= 10
        map_word, identity, _, inverse, classify = marked_group(
            "symmetric", len(x), tuple(x), tuple(y)
        )
        evaluate = lru_cache(maxsize=None)(map_word)

        @cache
        def cycle_type(word, evaluate=evaluate, inverse=inverse, classify=classify):
            element = evaluate(word)
            shape = classify(element)
            assert shape == classify(inverse(element))
            return shape

        markings.append((len(x), evaluate, identity, cycle_type))

    contacts = 0
    for s, left, right in receipt["last_contacts"]:
        candidates = sorted(
            (degree, i)
            for i, (degree, evaluate, identity, _) in enumerate(markings)
            if evaluate(s) == identity
        )
        for f in left:
            for e in right:
                if f == e:
                    continue
                contacts += 1
                for degree, i in candidates:
                    shape = markings[i][-1]
                    if shape(f) != shape(e):
                        closed[degree] += 1
                        break
                else:
                    residual[s, f].add(e)
    assert contacts == receipt["fourth"]["word_checks"]
    fox, amalgam, unresolved = [], [], []
    for (s, f), targets in sorted(residual.items()):
        if s in MARKINGS:
            result = separate(s, f, sorted(targets))
            fox.append(result)
            unresolved.extend([f, s, e] for e in result["unresolved"])
        elif s == AMALGAM_DONOR:
            for e in sorted(targets):
                proof = amalgam_separation(s, f, e)
                if proof is None:
                    unresolved.append([f, s, e])
                else:
                    amalgam.append(proof)
        else:
            unresolved.extend([f, s, e] for e in sorted(targets))
    return {
        "contacts": contacts,
        "permutation_excluded": sum(closed.values()),
        "permutation_witness_degrees": dict(sorted(closed.items())),
        "fox_excluded": sum(len(row["witnesses"]) for row in fox),
        "fox_records": fox,
        "affine_amalgam_excluded": len(amalgam),
        "affine_amalgam_records": amalgam,
        "unresolved": unresolved,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contact_receipt", type=Path)
    parser.add_argument("--permutations", type=Path)
    options = parser.parse_args()
    if options.permutations is not None:
        result = pack(options.contact_receipt, options.permutations)
    else:
        stored = json.loads(options.contact_receipt.read_bytes())
        result = audit(stored)
        assert json.loads(json.dumps(result)) == stored["fourth_exact_obstructions"]
    print(json.dumps(result, separators=(",", ":")))
