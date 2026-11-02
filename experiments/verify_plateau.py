#!/usr/bin/env python3
"""Exact sanity checks for the frozen-relator and nonincreasing-plateau lemmas.

No external dependencies. This checks finite instances, not the AC conjecture.
The all-n conclusions follow from the proof in research-a.md.
"""

from itertools import chain
import json

ALPHABET = (1, -1, 2, -2)  # x, x^-1, y, y^-1
BRAID = (1, 2, 1, -2, -1, -2)
BRAID_IMAGE = {
    1: ((1, 2), (0, 1)),
    -1: ((0, 1), (1, 1)),
    2: ((0, 1), (1, 2)),
    -2: ((1, 1), (0, 1)),
}


def inverse(word):
    return tuple(-a for a in reversed(word))


def rotations(word):
    return {word[k:] + word[:k] for k in range(len(word))}


def signed_rotations(word):
    return rotations(word) | rotations(inverse(word))


def reduce_syllables(syllables, orders):
    """Normal form in C_orders[0] * C_orders[1]."""
    out = []
    for factor, power in syllables:
        power %= orders[factor]
        if power == 0:
            continue
        if out and out[-1][0] == factor:
            power = (out.pop()[1] + power) % orders[factor]
            if power:
                out.append((factor, power))
        else:
            out.append((factor, power))
    return tuple(out)


def cyclic_signature(syllables, orders):
    """Canonical cyclic syllable necklace (a necessary conjugacy invariant)."""
    word = reduce_syllables(syllables, orders)
    while len(word) > 1 and word[0][0] == word[-1][0]:
        word = reduce_syllables(word[1:] + word[:1], orders)
    return min(rotations(word)) if word else ()


def braid_signature(word):
    return cyclic_signature(chain.from_iterable(BRAID_IMAGE[a] for a in word), (2, 3))


def power_signature(word, orders):
    return cyclic_signature(((abs(a) - 1, 1 if a > 0 else -1) for a in word), orders)


def cyclically_reduced_words(length):
    def extend(prefix):
        if len(prefix) == length:
            if prefix[-1] != -prefix[0]:
                yield prefix
            return
        for a in ALPHABET:
            if not prefix or a != -prefix[-1]:
                yield from extend(prefix + (a,))
    yield from extend(())


def check_power_equality(n):
    p = (1,) * n + (-2,) * (n + 1)
    swapped = (2,) * n + (-1,) * (n + 1)
    targets = {braid_signature(p), braid_signature(inverse(p))}
    expected = signed_rotations(p) | signed_rotations(swapped)
    found = set()
    tested = 0
    for length in range(1, len(p) + 1):
        for word in cyclically_reduced_words(length):
            tested += 1
            if braid_signature(word) in targets:
                found.add(word)
    assert found == expected, (n, found - expected, expected - found)
    return {"n": n, "tested_words": tested, "minimal_length": len(p),
            "equality_representatives": len(found), "classification_verified": True}


def check_braid_equality(n, swapped=False):
    orders = (n + 1, n) if swapped else (n, n + 1)
    targets = {power_signature(BRAID, orders), power_signature(inverse(BRAID), orders)}
    expected = signed_rotations(BRAID)
    found = set()
    tested = 0
    for length in range(1, 7):
        for word in cyclically_reduced_words(length):
            tested += 1
            if power_signature(word, orders) in targets:
                found.add(word)
    assert not any(len(word) < 6 for word in found)
    if n >= 3:
        assert found == expected, (n, swapped, found - expected, expected - found)
    return {"n": n, "swapped_power": swapped, "tested_words": tested,
            "minimal_length": 6, "quotient_equality_candidates": len(found),
            "only_braid_rotations": found == expected}


def main():
    assert braid_signature(BRAID) == ()
    # This verifies the formula behind the uniform proof in additional instances.
    for n in range(1, 101):
        p = (1,) * n + (-2,) * (n + 1)
        assert len(braid_signature(p)) == 4 * n + 2
    result = {
        "scope": "finite checks supporting the all-n proof; not an AC solution",
        "power_equality": [check_power_equality(n) for n in (2, 3, 4)],
        "braid_equality": [check_braid_equality(n, swapped)
                            for n in (2, 3, 4) for swapped in (False, True)],
        "formula_checks_n_1_through_100": True,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
