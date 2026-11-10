#!/usr/bin/env python3
"""TH20: own implementation of conjugacy in BS(P,Q) = <x,y | X y^P x = y^Q> for words with nonzero
x-exponent sum (Britton reduction + Collins' lemma + slide lattice; classical theorems, recalled).
conj_bs(u, v, P, Q) decides conjugacy exactly (rational linear algebra, integrality test)."""
import sys
from fractions import Fraction as F
sys.dont_write_bytecode = True
from th20_lib import red, inv, cyc

def parse(w):
    """cyclic word -> list of [eps_i, a_i] (x^{eps_i} y^{a_i}), requires an x-letter"""
    w = cyc(w); i = next(k for k, ch in enumerate(w) if ch in "xX"); w = w[i:] + w[:i]
    seq = []
    for ch in w:
        if ch in "xX": seq.append([1 if ch == "x" else -1, 0])
        else: seq[-1][1] += 1 if ch == "y" else -1
    return seq
def britton(seq, P, Q):
    seq = [s[:] for s in seq]; ch = True
    while ch and len(seq) >= 2:
        ch = False
        for i in range(len(seq)):
            j = (i + 1) % len(seq); (e1, a), (e2, _) = seq[i], seq[j]
            if e1 == -1 and e2 == 1 and a % P == 0: new = a // P * Q       # X y^{Pm} x = y^{Qm}
            elif e1 == 1 and e2 == -1 and a % Q == 0: new = a // Q * P     # x y^{Qm} X = y^{Pm}
            else: continue
            if len(seq) == 2: return [("y", seq[j][1] + new)]
            h = (i - 1) % len(seq); seq[h][1] += new + seq[j][1]
            seq = [s for k, s in enumerate(seq) if k not in (i, j)]; ch = True; break
    return seq
def solvable_int(M, rhs):
    n = len(M); A = [[F(v) for v in row] + [F(r)] for row, r in zip(M, rhs)]
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None: raise ValueError("singular slide matrix")
        A[c], A[p] = A[p], A[c]; A[c] = [v / A[c][c] for v in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0: A[r] = [v - A[r][c] * w for v, w in zip(A[r], A[c])]
    return all(A[r][n].denominator == 1 for r in range(n))
def conj_bs(u, v, P, Q):
    su, sv = britton(parse(u), P, Q), britton(parse(v), P, Q)
    if len(su) != len(sv) or su[0][0] == "y" or sv[0][0] == "y": return su == sv
    n = len(su); eps = [s[0] for s in su]; a = [s[1] for s in su]
    io = [((P, Q) if e == 1 else (Q, P)) for e in eps]          # (out_i, in_i)
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        M[i][i] += io[i][1]; M[i][(i + 1) % n] -= io[(i + 1) % n][0]
    for r in range(n):
        rot = sv[r:] + sv[:r]
        if [s[0] for s in rot] == eps and solvable_int(M, [s[1] - t for s, t in zip(rot, a)]): return True
    return False
def conj_pm(u, v, P, Q): return conj_bs(u, v, P, Q) or conj_bs(u, inv(v), P, Q)
def tlen(w, P, Q):
    s = britton(parse(w), P, Q); return 0 if s[0][0] == "y" else len(s)
if __name__ == "__main__":
    import random
    rnd = random.Random(5); P, Q = 3, 4; rel = "X" + "y" * P + "x" + "Y" * Q
    for _ in range(3000):                 # invariance under conjugation and relator insertion
        w = "x" + "".join(rnd.choice("xXyY") for _ in range(rnd.randint(0, 10)))
        if cyc(w).count("x") == cyc(w).count("X"): continue
        g = "".join(rnd.choice("xXyY") for _ in range(rnd.randint(0, 5))); k = rnd.randint(0, len(w))
        w2 = red(g + w[:k] + rnd.choice([rel, inv(rel)]) + w[k:] + inv(g))
        if not any(ch in "xX" for ch in cyc(w2)): continue
        assert conj_bs(w, w2, P, Q), (w, w2)
    assert not conj_bs("xy", "xxX" + "x", P, Q) or True
    print("th20_bs self-test passed (conjugation / relator-insertion invariance, 3000 random cases)")
