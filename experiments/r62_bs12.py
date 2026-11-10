#!/usr/bin/env python3
"""Agent R6-2: BS(1,2) exit test at the node (c, alpha(r4)) of P2's class (c fixed).
The automorphic images of the BS(1,2) relator yxYXX of G_c-degree +-1 are, up to conjugacy,
z = x^e p x^-e p^-2 with p = (x^k y)^d, e, d = +-1, k in Z (bases containing p are
(p, p^j x^{+-1} p^l)).  An exit needs z^{+-1} ~ alpha(r4) in G_c; compare I (and L4, eps)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import th03_uniform as t, th03_two as q2
red, inv = t.red, t.inv
TARGET = 'aababaabaab'                           # nf of alpha(r4), I = 44, L4 = 9, eps = 1
def zword(k, e, d):
    p = ('x' * k if k >= 0 else 'X' * (-k)) + 'y'
    if d < 0: p = inv(p)
    xe = 'x' if e > 0 else 'X'
    return red(xe + p + inv(xe) + inv(p) + inv(p))
if __name__ == "__main__":
    G4, L4 = q2.l4_setup()
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    hits, rows = [], []
    for k in range(-K, K + 1):
        for e in (1, -1):
            for d in (1, -1):
                z = zword(k, e, d); u, deg = t.nf(z)
                if deg == -1: u, deg = t.nf(inv(z))
                assert deg == 1
                Iz = t.I(u); rows.append((k, e, d, Iz))
                if Iz == 44: hits.append((k, e, d, z, u, L4(u), q2.eps(u)))
    print("I-values for |k|<=3:", [r for r in rows if abs(r[0]) <= 3])
    print("min I over |k| in [4..%d]:" % K, min(r[3] for r in rows if abs(r[0]) >= 4))
    print("candidates with I = 44:", hits)
