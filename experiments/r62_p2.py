#!/usr/bin/env python3
"""Agent R6-2: the frontier holdout P2 = (XyyxYYY, XXXYxxY) in O's coordinates of G_c.
TH18 T10: P2 ~AC (r4, w0), r4 = XyyyyxYYYYY (BS(4,5) relator), w0 = xxyyXY = alpha(c),
alpha = (x -> xy, y -> Y) an involution of F2.  alpha(r4, w0) = (alpha(r4), c), and
alpha(r4) has degree 1 in G_c = <x,y | c>, c = xyxYYXy.  Decide alpha(r4) ~ x^s y in G_c
with TH03's exact invariants I (holonomy), eps (mod-2 mirror), L4 (degree-4 trace).
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/r62_p2.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import th03_uniform as t
import th03_two as q2
import o_gc as G

def red(w): return t.red(w)
def inv(w): return t.inv(w)
def aut(img, w):
    return red("".join(img[ch] if ch.islower() else inv(img[ch.lower()]) for ch in w))
ALPHA = {'x': 'xy', 'y': 'Y'}
C = 'xyxYYXy'; R4 = 'XyyyyxYYYYY'; W0 = 'xxyyXY'

def main():
    assert aut(ALPHA, aut(ALPHA, 'x')) == 'x' and aut(ALPHA, aut(ALPHA, 'y')) == 'y'   # involution
    assert aut(ALPHA, C) == W0, aut(ALPHA, C)
    w = aut(ALPHA, R4)
    u, k = t.nf(w)
    print("alpha(r4) =", w, " nf =", (u, k), " o_gc.nf agrees:", G.nf(w))
    if k == -1:
        u, k = t.nf(inv(w)); print("use inverse: nf =", (u, k))
    assert k == 1
    Iu = t.I(u); e = q2.eps(u)
    print("I(u) =", Iu, " eps(u) =", e)
    hits = [s for s in range(-80, 81) if t.sigma(s) == Iu]
    print("s in [-80,80] with sigma(s) = I(u):", hits)
    print("sigma(-10..11):", [t.sigma(s) for s in range(-10, 12)])
    for s in hits:
        print("  s =", s, " eps(a^s) =", q2.eps('a' * s if s >= 0 else 'A' * (-s)))
    G4, L4 = q2.l4_setup()
    print("L4(u) =", L4(u), " L4(a^s), s in hits:", [(s, L4('a' * s if s >= 0 else 'A' * (-s))) for s in hits])
    return u, hits

if __name__ == "__main__":
    main()
