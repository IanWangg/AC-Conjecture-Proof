#!/usr/bin/env python3
"""Agent J (round 3): finite checks for Theorem J1 of research/research-j.md.

Setting (research-a): quotient-conjugacy (ACM) moves on AK(n) = (p_n, b) with
    p_n = x^n Y^(n+1),  q_n = y^n X^(n+1),  b = x y x Y X Y   (X = x^-1, Y = y^-1).
Research-a proves that every non-increasing ACM path stays on the plateau
(Orb(p_n) u Orb(q_n)) x Orb(b), so the first increasing move lands at total
cyclic length >= 2n+8.  Theorem J1 sharpens this to >= 2n+9 (15 for AK(3)):

  (I)  No cyclically reduced word of length 2n+2 is conjugate to p_n^{+-1} in
       B = <x,y | xyx = yxy>: its image in B/Z(B) = C_2 * C_3 has cyclic
       syllable length 2(2n+2) (no orientation change) or <= 4n, never 4n+2.
  (II) No cyclically reduced word of length 7 is conjugate to b^{+-1} in
       G = <x,y | x^n = y^(n+1)> (or in G' = <x,y | y^n = x^(n+1)>).  For n >= 4
       already the quotient C_n * C_(n+1) excludes it; for n = 3 one needs
       Lemma J0: conjugacy in these torus-knot groups is equivalent to conjugacy
       in the quotient C_n * C_(n+1) PLUS equality of the abelianization
       exponent, and the 42 quotient-conjugate candidates of length 7 all have
       the wrong abelianization.

This script enumerates all cyclically reduced words of the relevant lengths
and verifies (I) and (II) exactly for n = 3 and n = 4, and reports the counts
one length higher (the first off-plateau states).  Standard library only.
Run: python3 experiments/j_first_increase.py        (about 1 s)
"""
from itertools import chain
import json

ALPHABET = (1, -1, 2, -2)  # x, X, y, Y
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
    return (sum(1 for a in word if a == 1) - sum(1 for a in word if a == -1),
            sum(1 for a in word if a == 2) - sum(1 for a in word if a == -2))


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


def power_side(n, length):
    """Words of the given length whose C_2*C_3 image is conjugate to that of
    p_n^{+-1}, and the subset with the right abelianization in B (x,y -> t)."""
    p = (1,) * n + (-2,) * (n + 1)
    targets = {sig_C2C3(p): -1, sig_C2C3(inverse(p)): 1}
    quot, exact = [], []
    for w in cyclically_reduced_words(length):
        s = sig_C2C3(w)
        if s in targets:
            quot.append(w)
            ex, ey = exps(w)
            if ex + ey == targets[s]:
                exact.append(w)
    return quot, exact


def braid_side(n, length, swapped):
    """Words of the given length conjugate to b^{+-1} in C_n*C_(n+1) (frozen p_n)
    or C_(n+1)*C_n (frozen q_n), and the subset with the right abelianization in
    the torus-knot group (Lemma J0)."""
    orders = (n + 1, n) if swapped else (n, n + 1)
    ax, ay = (n, n + 1) if swapped else (n + 1, n)   # x -> t^ax, y -> t^ay kills the frozen relator
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


def check_n(n):
    p = (1,) * n + (-2,) * (n + 1)
    q = (2,) * n + (-1,) * (n + 1)
    assert sig_C2C3(BRAID) == ()
    assert sig_CpCq(p, (n, n + 1)) == () and sig_CpCq(q, (n + 1, n)) == ()
    res = {}
    for L in (2 * n + 1, 2 * n + 2, 2 * n + 3):
        quot, exact = power_side(n, L)
        res[L] = {"quotient_conjugate_candidates": len(quot),
                  "with_correct_abelianization": len(exact)}
        if L == 2 * n + 1:
            assert set(quot) == orbit(p) | orbit(q) == set(exact)
        if L == 2 * n + 2:
            assert not quot, [wstr(w) for w in quot]
    res2 = {}
    for swapped in (False, True):
        r = {}
        for L in (6, 7, 8):
            quot, exact = braid_side(n, L, swapped)
            r[L] = {"quotient_conjugate_candidates": len(quot),
                    "with_correct_abelianization": len(exact)}
            if L == 6:
                assert set(quot) == orbit(BRAID) == set(exact)
            if L == 7:
                r[L]["quotient_candidates_examples"] = [wstr(w) for w in quot[:3]]
                assert not exact, [wstr(w) for w in exact]
        res2["frozen " + ("q_n" if swapped else "p_n")] = r
    return {"n": n, "power_relator_updated_braid_frozen": res,
            "braid_relator_updated_power_frozen": res2,
            "first_exit_total_cyclic_length_at_least": 2 * n + 9}


def main():
    out = {"scope": "finite checks of Theorem J1 (first increasing ACM move from the "
                    "AK(n) plateau lands at total cyclic length >= 2n+9, n = 3, 4); "
                    "not an AC solution",
           "checks": [check_n(3), check_n(4)],
           "theorem_J1_finite_part_verified": True}
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
