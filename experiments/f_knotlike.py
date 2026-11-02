#!/usr/bin/env python3
"""One-relator (knot-group) obstruction to thickenability, by Fox calculus.

Research agent F, 2026-11-02.  Standard library only.

Proposition F2 (research-f.md, Section 3): if the 2-complex of a balanced
presentation (r1, r2) of the trivial group embeds in a 3-manifold, then for
each i the one-relator group <x,y | r_i> is the fundamental group of a compact
orientable 3-manifold N_i with torus boundary and H_1(N_i) = Z, so its
Alexander polynomial is symmetric: Delta(t) = +-t^k Delta(t^-1).

This module computes Delta for <x,y | r> when the exponent-sum vector of r is
primitive, and tests symmetry.  An asymmetric Delta for either relator proves
non-thickenability; it says nothing about AC-triviality.

`python3 experiments/f_knotlike.py --selftest` checks known values and
cross-checks the obstruction against the exact algorithm of f_thicken.py.
"""
import math
import random
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import f_thicken as T  # noqa: E402


def exponent_sums(r):
    return (sum(1 if a == 1 else -1 if a == -1 else 0 for a in r),
            sum(1 if a == 2 else -1 if a == -2 else 0 for a in r))


def _poly_from_terms(terms):
    """terms: dict exponent -> coeff (Laurent).  Return (shift, list coeffs)."""
    terms = {e: c for e, c in terms.items() if c}
    if not terms:
        return None
    lo, hi = min(terms), max(terms)
    return lo, [terms.get(e, 0) for e in range(lo, hi + 1)]


def _divide_exact(num, den):
    """Exact division of integer polynomials (lists, low degree first)."""
    num = num[:]
    out = [0] * (len(num) - len(den) + 1)
    if len(out) <= 0:
        raise ArithmeticError("degree too small")
    for i in range(len(out) - 1, -1, -1):
        c = num[i + len(den) - 1]
        if c % den[-1]:
            raise ArithmeticError("not divisible")
        q = c // den[-1]
        out[i] = q
        for j, d in enumerate(den):
            num[i + j] -= q * d
    if any(num):
        raise ArithmeticError("nonzero remainder")
    return out


def alexander(r):
    """Alexander polynomial (coefficient list, normalized: low-degree first,
    nonzero constant term, positive leading... up to units) of <x,y|r>."""
    a, b = exponent_sums(r)
    if math.gcd(a, b) != 1:
        raise ValueError("exponent-sum vector of r must be primitive")
    p, q = -b, a        # phi(x) = t^p, phi(y) = t^q, with a p + b q = 0
    # Fox derivative w.r.t. the generator whose image exponent is nonzero
    # paired with division by (t^{other}-1)/(t-1).
    def fox(gen):
        terms = {}
        e = 0
        for c in r:
            g, s = abs(c), (1 if c > 0 else -1)
            val = p if g == 1 else q
            if g == gen:
                if s > 0:
                    terms[e] = terms.get(e, 0) + 1
                else:
                    terms[e - val] = terms.get(e - val, 0) - 1
            e += s * val
        return _poly_from_terms(terms)
    if p != 0:
        D = fox(2)       # D_y = -Delta * (t^p - 1)/(t - 1)
        k = abs(p)
    else:
        D = fox(1)       # D_x =  Delta * (t^q - 1)/(t - 1)
        k = abs(q)
    if D is None:
        return [0]
    _, coeffs = D
    den = [1] * k        # 1 + t + ... + t^{k-1}
    delta = _divide_exact(coeffs, den)
    while delta and delta[0] == 0:
        delta = delta[1:]
    while delta and delta[-1] == 0:
        delta = delta[:-1]
    if delta and delta[-1] < 0:
        delta = [-c for c in delta]
    return delta


def symmetric(delta):
    return delta == delta[::-1] or delta == [-c for c in delta[::-1]]


def knotlike_obstructed(r1, r2):
    """True if some relator has an asymmetric Alexander polynomial (proves
    the complex is not thickenable, by Proposition F2)."""
    for r in (r1, r2):
        a, b = exponent_sums(r)
        if math.gcd(a, b) != 1:
            return True   # then H_1(<x,y|r>) is not Z: also obstructed
        if not symmetric(alexander(r)):
            return True
    return False


def selftest(seed=7, trials=3000):
    P = T.parse
    # trefoil (braid relator) and T(3,4) torus knot: t^2-t+1, t^6-t^5+t^3-t+1
    assert alexander(P("xyxYXY")) == [1, -1, 1], alexander(P("xyxYXY"))
    assert alexander(P("xxxYYYY")) == [1, -1, 0, 1, 0, -1, 1], alexander(P("xxxYYYY"))
    # BS(n,n+1): n - (n+1)t up to units, asymmetric
    for n in range(1, 8):
        r = (-1,) + (2,) * n + (1,) + (-2,) * (n + 1)
        d = alexander(r)
        assert sorted(map(abs, d)) == [n, n + 1] and not symmetric(d), (n, d)
    # cross-check against the exact thickenability algorithm
    rng = random.Random(seed)
    checked = obstructed = thick = 0
    for _ in range(trials):
        r1 = T.random_cr_word(rng.randint(1, 9), rng)
        r2 = T.random_cr_word(rng.randint(1, 9), rng)
        a1, b1 = exponent_sums(r1)
        a2, b2 = exponent_sums(r2)
        if abs(a1 * b2 - a2 * b1) != 1:
            continue
        obs = knotlike_obstructed(r1, r2)
        th = T.thickenable_fast(r1, r2)
        assert not (obs and th), ("obstruction contradicts exact test", T.fmt(r1), T.fmt(r2))
        checked += 1
        obstructed += obs
        thick += th
    print(f"self-test passed: {checked} unimodular random pairs, {obstructed} "
          f"Alexander-obstructed, {thick} thickenable, 0 contradictions")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
    else:
        for w in sys.argv[1:]:
            d = alexander(T.parse(w))
            print(w, d, "symmetric" if symmetric(d) else "ASYMMETRIC")


# ------------------------------------------------ torus-knot meridian test

def _apply(phi, w):
    out = []
    for a in w:
        img = phi[abs(a)]
        out += list(img) if a > 0 else list(T.inverse(img))
    return T.free_reduce(out)


_NIELSEN = [{1: (1, 2), 2: (2,)}, {1: (1, -2), 2: (2,)}, {1: (2, 1), 2: (2,)},
            {1: (-2, 1), 2: (2,)}, {1: (1,), 2: (2, 1)}, {1: (1,), 2: (2, -1)},
            {1: (1,), 2: (1, 2)}, {1: (1,), 2: (-1, 2)}, {1: (2,), 2: (1,)}]


def torus_form(r, depth=6):
    """Search automorphisms phi (products of <= depth Nielsen generators) with
    phi(r) cyclically equal to x^p y^q, |p|,|q| >= 2.  Returns (phi, p, q)."""
    start = {1: (1,), 2: (2,)}
    frontier = [start]
    seen = {(start[1], start[2])}
    for _ in range(depth + 1):
        nxt = []
        for phi in frontier:
            w = T.cyc_reduce(_apply(phi, r))
            for k in range(len(w)):
                u = w[k:] + w[:k]
                gs = [abs(a) for a in u]
                if len(set(gs)) == 2:
                    # x^p y^q blocks?
                    i = 0
                    while i < len(u) and u[i] == u[0]:
                        i += 1
                    if all(c == u[i] for c in u[i:]) and abs(u[0]) == 1:
                        p = i * (1 if u[0] > 0 else -1)
                        q = (len(u) - i) * (1 if u[i] > 0 else -1)
                        if abs(p) >= 2 and abs(q) >= 2:
                            return phi, p, q
            for g in _NIELSEN:
                new = {1: _apply(phi, g[1]), 2: _apply(phi, g[2])}
                key = (new[1], new[2])
                if key not in seen and len(new[1]) + len(new[2]) <= 12:
                    seen.add(key)
                    nxt.append(new)
        frontier = nxt
    return None


def syllable_length_in_free_product(w, p, q):
    """Cyclic syllable length of w in C_|p| * C_|q| (x -> first factor)."""
    orders = {1: abs(p), 2: abs(q)}
    syl = []
    for a in w:
        g, s = abs(a), (1 if a > 0 else -1)
        if syl and syl[-1][0] == g:
            e = (syl[-1][1] + s) % orders[g]
            syl.pop()
            if e:
                syl.append((g, e))
        else:
            syl.append((g, s % orders[g]))
        # merge possible new adjacency after pop
        while len(syl) >= 2 and syl[-1][0] == syl[-2][0]:
            g2, e2 = syl.pop()
            g1, e1 = syl.pop()
            e = (e1 + e2) % orders[g1]
            if e:
                syl.append((g1, e))
    while len(syl) >= 2 and syl[0][0] == syl[-1][0]:
        g, e1 = syl.pop(0)
        _, e2 = syl.pop()
        e = (e1 + e2) % orders[g]
        if e:
            syl.append((g, e))
    return len(syl)


def meridian_test(r_knot, r_other, depth=6):
    """If <x,y|r_knot> is a torus-knot group T(p,q) via a found automorphism,
    return the cyclic syllable length of the other relator's image in
    C_p * C_q (a meridian has syllable length 2)."""
    found = torus_form(r_knot, depth)
    if not found:
        return None
    phi, p, q = found
    w = T.cyc_reduce(_apply(phi, r_other))
    return {"p": p, "q": q, "other_image": T.fmt(w),
            "syllable_length": syllable_length_in_free_product(w, p, q)}
