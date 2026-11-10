#!/usr/bin/env python3
"""TH20 brute-force check of TH13's Lemma P (power side) and Lemma B (braid side), own code.
Lemma P: cyclically reduced u ~ p_p^{+-1} in B_k = F/<<W_k>>  =>  u in Orb(p_p) u Orb(q_p) or |u| >= 2p+1+min(4k-2,2k+2).
Lemma B (p >= 3): u ~ W_k^{+-1} in <x^p=y^(p+1)> or <y^p=x^(p+1)>  =>  u in Orb(W_k) or |u| >= 4k+2+2(p-2).
Usage: th20_th13_plateau.py k p [Lmax]  (enumerates all cyclically reduced words up to the claimed bound)"""
import sys
sys.dont_write_bytecode = True
from th20_lib import red, inv, cyc, aut, torus_inv
k, p = int(sys.argv[1]), int(sys.argv[2]); LMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 99
W = red("xy" * k + "x" + inv("yx" * k + "y")); pw = "x" * p + "Y" * (p + 1); qw = "y" * p + "X" * (p + 1)
phi = {"x": "x" + "Y" * k, "y": "y" * k + "Xy"}
SW = {"x": "y", "y": "x"}
def orb(w):
    w = cyc(w); return {u[i:] + u[:i] for u in (w, inv(w)) for i in range(len(u))}
def words(L):
    def rec(pre, ex, ey):
        if len(pre) == L:
            if pre[0] != pre[-1].swapcase(): yield pre, ex, ey
            return
        for c in "xXyY":
            if pre and pre[-1] == c.swapcase(): continue
            yield from rec(pre + c, ex + (c == "x") - (c == "X"), ey + (c == "y") - (c == "Y"))
    yield from rec("", 0, 0)
# power side
tgt = {torus_inv(aut(phi, pw), 2, -(2 * k + 1)), torus_inv(aut(phi, inv(pw)), 2, -(2 * k + 1))}
bound = 2 * p + 1 + min(4 * k - 2, 2 * k + 2); plateau = orb(pw) | orb(qw)
for L in range(1, min(bound, LMAX) + 1):
    hits = [u for u, ex, ey in words(L) if abs(ex + ey) == 1 and torus_inv(aut(phi, u), 2, -(2 * k + 1)) in tgt]
    off = [u for u in hits if u not in plateau]
    print("power side k=%d p=%d L=%2d: %5d words conjugate to p_p^+-1 in B_k, %5d off the plateau%s" % (k, p, L, len(hits), len(off), "  (claimed bound)" if L == bound else ""), flush=True)
    assert (L < bound and not off and (set(hits) == plateau if L == 2 * p + 1 else not hits)) or L == bound
# braid side
if p >= 3:
    bound = 4 * k + 2 + 2 * (p - 2)
    for swapped in (False, True):
        Wk = aut(SW, W) if swapped else W
        tgt = {torus_inv(Wk, p, -(p + 1)), torus_inv(inv(Wk), p, -(p + 1))}
        for L in range(1, min(bound, LMAX) + 1):
            hits = []
            for u, ex, ey in words(L):
                a, b = (ey, ex) if swapped else (ex, ey)
                if abs((p + 1) * a + p * b) != 1: continue
                if torus_inv(aut(SW, u) if swapped else u, p, -(p + 1)) in tgt: hits.append(u)
            off = [u for u in hits if u not in orb(W)]
            print("braid side k=%d p=%d %s L=%2d: %5d words, %5d off Orb(W_k)%s" % (k, p, "G_p'" if swapped else "G_p ", L, len(hits), len(off), "  (claimed bound)" if L == bound else ""), flush=True)
            assert (L < bound and not off and (set(hits) == orb(W) if L == 4 * k + 2 else not hits)) or L == bound
print("done")
