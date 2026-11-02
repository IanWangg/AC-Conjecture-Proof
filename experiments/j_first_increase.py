#!/usr/bin/env python3
"""Agent J (round 3): finite checks for Theorem J1 of research/research-j.md.

Setting (research-a): quotient-conjugacy (ACM) moves on AK(3) = (p, b) with
    p = x^3 Y^4,  q = y^3 X^4,  b = x y x Y X Y   (X = x^-1, Y = y^-1).
Research-a proves that every non-increasing ACM path stays on the plateau
(Orb(p) u Orb(q)) x Orb(b), so the first increasing move lands at total cyclic
length >= 14.  Theorem J1 sharpens this to >= 15 by two facts:

  (I)  No cyclically reduced word of length 8 is conjugate to p^{+-1} in
       B = <x,y | xyx = yxy>: its image in B/Z(B) = C_2 * C_3 has cyclic
       syllable length 16 (no orientation change) or <= 12, never 14.
  (II) No cyclically reduced word of length 7 is conjugate to b^{+-1} in
       G = <x,y | x^3 = y^4> (or in G' = <x,y | y^3 = x^4>): conjugacy in
       these torus-knot groups is equivalent to conjugacy in the quotient
       C_3 * C_4 (resp. C_4 * C_3) PLUS equality of the abelianization
       exponent (Lemma J0), and the quotient-conjugate candidates of length 7
       all have the wrong abelianization.

This script enumerates all cyclically reduced words of the relevant lengths
and verifies (I) and (II) exactly, and reports the length-9 and length-8
counts (the first states at total length 15 and 16).  Standard library only.
"""
from itertools import chain
import json

ALPHABET = (1, -1, 2, -2)  # x, X, y, Y
P3 = (1, 1, 1, -2, -2, -2, -2)
Q3 = (2, 2, 2, -1, -1, -1, -1)
BRAID = (1, 2, 1, -2, -1, -2)
# images in C_2 * C_3 = <S | S^2> * <T | T^3>, factor 0 = S, factor 1 = T:
# x -> T^2 S, X -> S T, y -> S T^2, Y -> T S   (research-a, Lemma 1)
BRAID_IMAGE = {1: ((1, 2), (0, 1)), -1: ((0, 1), (1, 1)),
               2: ((0, 1), (1, 2)), -2: ((1, 1), (0, 1))}


def inverse(word):
    return tuple(-a for a in reversed(word))


def rotations(word):
    return {word[k:] + word[:k] for k in range(len(word))}


def orbit(word):
    return rotations(word) | rotations(inverse(word))


def reduce_syllables(syl, orders):
    out = []
    for f, p in syl:
        p %= orders[f]
        if p == 0:
            continue
        if out and out[-1][0] == f:
            p = (out.pop()[1] + p) % orders[f]
            if p:
                out.append((f, p))
        else:
            out.append((f, p))
    return tuple(out)


def cyclic_signature(syl, orders):
    w = reduce_syllables(syl, orders)
    while len(w) > 1 and w[0][0] == w[-1][0]:
        w = reduce_syllables(w[1:] + w[:1], orders)
    return min(rotations(w)) if w else ()


def sig_C2C3(word):
    return cyclic_signature(chain.from_iterable(BRAID_IMAGE[a] for a in word), (2, 3))


def sig_CpCq(word, orders):
    return cyclic_signature(((abs(a) - 1, 1 if a > 0 else -1) for a in word), orders)


def exps(word):
    return sum(1 for a in word if a == 1) - sum(1 for a in word if a == -1), \
        sum(1 for a in word if a == 2) - sum(1 for a in word if a == -2)


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


def power_side(length):
    """Words of the given length whose image is conjugate to p^{+-1} in C_2*C_3,
    and the subset with the right abelianization in B (x,y -> t; p -> t^-1)."""
    targets = {sig_C2C3(P3): -1, sig_C2C3(inverse(P3)): 1}
    quot, exact = [], []
    for w in cyclically_reduced_words(length):
        s = sig_C2C3(w)
        if s in targets:
            quot.append(w)
            ex, ey = exps(w)
            if ex + ey == targets[s]:
                exact.append(w)
    return quot, exact


def braid_side(length, swapped):
    """Words of the given length conjugate to b^{+-1} in C_3*C_4 (orders (3,4),
    frozen p) or C_4*C_3 (orders (4,3), frozen q), and the subset with the right
    abelianization in the torus-knot group."""
    orders = (4, 3) if swapped else (3, 4)
    ax, ay = (3, 4) if swapped else (4, 3)   # x -> t^ax, y -> t^ay kills the frozen relator
    bx, by = exps(BRAID)
    ab_b = ax * bx + ay * by
    assert ab_b in (1, -1), ab_b
    targets = {sig_CpCq(BRAID, orders): ab_b, sig_CpCq(inverse(BRAID), orders): -ab_b}
    quot, exact = [], []
    for w in cyclically_reduced_words(length):
        s = sig_CpCq(w, orders)
        if s in targets:
            quot.append(w)
            ex, ey = exps(w)
            if ax * ex + ay * ey == targets[s]:
                exact.append(w)
    return quot, exact


def wstr(word):
    return "".join({1: "x", -1: "X", 2: "y", -2: "Y"}[a] for a in word)


def main():
    out = {"scope": "finite checks of Theorem J1 (first increasing ACM move from the "
                    "AK(3) plateau lands at total cyclic length >= 15); not an AC solution"}
    # sanity: the braid relator dies in C_2*C_3 and the torus relators die in C_3*C_4
    assert sig_C2C3(BRAID) == ()
    assert sig_CpCq(P3, (3, 4)) == () and sig_CpCq(Q3, (4, 3)) == ()
    # (I) power relator updated, braid relator frozen
    res = {}
    for L in (7, 8, 9):
        quot, exact = power_side(L)
        res[L] = {"quotient_conjugate_candidates": len(quot),
                  "with_correct_abelianization": len(exact)}
        if L == 7:
            assert set(quot) == orbit(P3) | orbit(Q3)
            assert set(exact) == orbit(P3) | orbit(Q3)
        if L == 8:
            assert not quot, [wstr(w) for w in quot]
    # which of the length-9 B-conjugates lie in Orb(P3) * Orb(b) shifted? just report
    res[9]["examples"] = [wstr(w) for w in power_side(9)[1][:6]]
    out["power_relator_updated_braid_frozen"] = res
    # (II) braid relator updated, power relator frozen
    res2 = {}
    for swapped in (False, True):
        r = {}
        for L in (6, 7, 8):
            quot, exact = braid_side(L, swapped)
            r[L] = {"quotient_conjugate_candidates": len(quot),
                    "with_correct_abelianization": len(exact)}
            if L == 6:
                assert set(quot) == orbit(BRAID) and set(exact) == orbit(BRAID)
            if L == 7:
                r[L]["quotient_candidates_examples"] = [wstr(w) for w in quot[:4]]
                assert not exact, [wstr(w) for w in exact]
        res2["frozen " + ("q=yyyXXXX" if swapped else "p=xxxYYYY")] = r
    out["braid_relator_updated_power_frozen"] = res2
    out["theorem_J1_finite_part_verified"] = True
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
