#!/usr/bin/env python3
"""TH20 independent checks for TH12.
(1) identities (I_x), (I_y): x, y as products of conjugates over AK(n) with counts (3,n+1), (3,n), n <= 30.
(2) c_r = 1 impossible: trace of r in SL2(Z) under x -> L, y -> [[1,0],[-1,1]] is n^2+n+2 != 2.
(3) Theorem 3, exhaustive: all d*t_1..t_mu (t_i in {L,R}^{+-1}, d in {+-I,+-S}) equal to Sigma = [[-1,n+1],[-1,n]]
    with mu <= n+1 have count matrix |d||t_1|..|t_mu| = [[1,n+1],[1,n]] (first column (1,1) < 3);  n <= 6.
(4) Lemma 4.1 permutation model: r trivial, s fixes [1,n-3], letters shift by sigma inside [1,n]; 4 <= n <= 40."""
import sys, itertools
sys.dont_write_bytecode = True
from th20_lib import red, inv
def cj(g, u): return red(g + u + inv(g))
for n in range(1, 31):
    r, s, D = "x" * n + "Y" * (n + 1), "xyxYXY", "xyx"
    w = ""
    for i in range(n + 1): w = red(w + cj(red(inv(D) + "y" * i), s))
    for g, e in ((inv(D), -1), ("XY", 1), ("X", -1)): w = red(w + cj(g, r if e > 0 else inv(r)))
    v = inv(r)
    for i in range(n): v = red(v + cj("y" * i, s))
    v = red(v + cj(red("y" * n + "x" + "Y" * n), inv(r))); v = red(v + cj(red("y" * n + "x" + "Y" * (n + 1)), r))
    assert w == "x" and v == "y", n
print("(1) identities OK, n = 1..30")
mm = lambda A, B: tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
ab = lambda A: tuple(tuple(abs(e) for e in r) for r in A)
I2 = ((1, 0), (0, 1)); L = ((1, 1), (0, 1)); R = ((1, 0), (1, 1)); Li = ((1, -1), (0, 1)); Ri = ((1, 0), (-1, 1)); S = ((0, 1), (-1, 0))
def mpow(A, n):
    M = I2
    for _ in range(n): M = mm(M, A)
    return M
for n in range(1, 40):
    y = ((1, 0), (-1, 1)); yi = ((1, 0), (1, 1))
    assert mm(mm(L, y), L) == mm(mm(y, L), y)
    M = mm(mpow(L, n), mpow(yi, n + 1)); assert M[0][0] + M[1][1] == n * n + n + 2
print("(2) trace(r) = n^2+n+2 in SL2(Z), braid relation holds")
neg = lambda A: tuple(tuple(-e for e in r) for r in A)
for n in range(1, 7):
    Sig = ((-1, n + 1), (-1, n)); found = {}
    for mu in range(0, n + 2):
        for word in itertools.product((L, R, Li, Ri), repeat=mu):
            P, C = I2, I2
            for t in word: P = mm(P, t); C = mm(C, ab(t))
            for d in (I2, neg(I2), S, neg(S)):
                if mm(d, P) == Sig: found.setdefault(mu, set()).add(mm(ab(d), C))
    assert set(found) == {n + 1} and found[n + 1] == {((1, n + 1), (1, n))}, (n, found)
print("(3) n <= 6: mu <= n+1 forces mu = n+1 and count matrix [[1,n+1],[1,n]]  (so mu >= n+2 by c_r >= 3)")
for n in range(4, 41):
    px = {i: i + 1 for i in range(1, n)}; px[n] = 1; px[0] = 0
    py = {i: i + 1 for i in range(0, n)}; py[n] = 0
    act = {"x": px, "y": py, "X": {v: k for k, v in px.items()}, "Y": {v: k for k, v in py.items()}}
    def ap(p, w):
        for ch in w: p = act[ch][p]
        return p
    r, s = "x" * n + "Y" * (n + 1), "xyxYXY"
    assert all(ap(p, r) == p for p in range(n + 1))
    assert all(ap(p, s) == p for p in range(1, n - 2))
    for p in range(1, n + 1):
        for h, d in (("x", 1), ("y", 1), ("X", -1), ("Y", -1)):
            if 1 <= p + d <= n: assert act[h][p] == p + d
print("(4) permutation model OK, n = 4..40")
# (5) Propositions 8-9 (added in the 04:45 version): identities over P_n = (c, k_n), a = x, b = yxY
def w(*parts): return red("".join(parts))
def pwr(u, e): return red(u * e) if e >= 0 else red(inv(u) * (-e))
for n in range(2, 31):
    a, b, c, k = "x", "yxY", "xyxYYXy", "x" * n + "YXyy"
    assert w(inv(c), a, b, pwr(a, -n), k) == "y"                                             # (P1)
    u = w(a, b, pwr(a, 1 - n))
    s = w(a, b, a, inv(b), inv(a), inv(b))
    assert s == w(u, k, inv(u), u, inv(a), inv(k), a, inv(u), c, b, inv(c), inv(b))            # (P2)
    g = w(pwr(b, n), inv(a))
    assert w(pwr(a, n), pwr(b, -n - 1)) == w(k, "y", inv(k), "Y", g, inv(c), inv(g))           # (P3)
    C = w("y", c, "Y"); g1 = w(a, b, pwr(a, -2)); g2 = w(a, b, inv(a))
    Psi = w(a, b, pwr(a, -2), b)
    assert Psi == w(g1, C, inv(g1), g2, C, inv(g2), inv(C), "y", s, "Y")                       # Prop. 9 (2)
    h = w(a, inv(b), inv(a))
    assert b == w(inv(a), s, a, h, Psi, inv(h))                                                # Prop. 9 (3)
print("(5) TH12 Prop. 8 (P1)-(P3) and Prop. 9 identities hold as free identities, n = 2..30; x = Y b y has 4 + 7 = 11 factors (4 on k, 7 on c)")
