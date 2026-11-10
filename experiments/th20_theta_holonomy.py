#!/usr/bin/env python3
"""TH20 referee check (independent of coord/fig8_check.py and of TH11's code).
(1) theta = (x->X, y->yx): free-group identities for c, x^s y, k_n.
(2) exact holonomy invariant tau(u t) = tr(rho(u)T)^2/det T of the figure-eight subgroup
    H = <a,b,t | t a T = B a, t b T = A b b>, computed in Z[w]/(w^2+w+1) with integer
    arithmetic (matrices scaled by a common denominator), plus a mod-p cross-check.
Usage: python3 experiments/th20_theta_holonomy.py [N=14] [S=40]
"""
import sys
from fractions import Fraction as F

def red(w):
    o = []
    for ch in w:
        if o and o[-1] == ch.swapcase(): o.pop()
        else: o.append(ch)
    return "".join(o)
def inv(w): return w.swapcase()[::-1]
def cyc(w):
    w = red(w)
    while len(w) > 1 and w[0] == w[-1].swapcase(): w = w[1:-1]
    return w
def conj(u, v):
    u, v = cyc(u), cyc(v)
    return len(u) == len(v) and u in v + v
TH = {"x": "X", "X": "x", "y": "yx", "Y": "XY"}
def theta(w): return red("".join(TH[ch] for ch in w))
c = "xyxYYXy"
assert conj(theta(c), inv(c)) and not conj(theta(c), c)
for s in range(-8, 9):
    xs = ("x" * s if s >= 0 else "X" * -s) + "y"
    t = 1 - s
    assert conj(theta(xs), ("x" * t if t >= 0 else "X" * -t) + "y")
for n in range(1, 12):
    assert theta("x" * n + "YXyy") == "X" * (n + 1) + "Yxyxyx"
print("theta: c -> conj of c^-1; x^s y -> conj of x^(1-s) y; k_n -> X^(n+1) Yxyxyx  [free identities OK]")

# ---- Q(w) as pairs of Fractions (own implementation)
class Q:
    def __init__(s, p=0, q=0): s.p, s.q = F(p), F(q)
    def __add__(s, o): return Q(s.p + o.p, s.q + o.q)
    def __sub__(s, o): return Q(s.p - o.p, s.q - o.q)
    def __mul__(s, o): return Q(s.p*o.p - s.q*o.q, s.p*o.q + s.q*o.p - s.q*o.q)
    def inv(s):
        n = s.p*s.p - s.p*s.q + s.q*s.q
        return Q((s.p - s.q)/n, -s.q/n)
    def key(s): return (s.p, s.q)
ONE, ZERO = Q(1), Q(0)
def mm(A, B): return [[A[i][0]*B[0][j] + A[i][1]*B[1][j] for j in range(2)] for i in range(2)]
def det(A): return A[0][0]*A[1][1] - A[0][1]*A[1][0]
def minv(A):
    d = det(A).inv(); m = Q(-1)
    return [[A[1][1]*d, m*A[0][1]*d], [m*A[1][0]*d, A[0][0]*d]]
def mpow(A, n):
    if n < 0: A, n = minv(A), -n
    R = [[ONE, ZERO], [ZERO, ONE]]
    for _ in range(n): R = mm(R, A)
    return R
def same(A, B): return all(A[i][j].key() == B[i][j].key() for i in range(2) for j in range(2))
x, y, z = Q(1, -1), Q(2, 1), Q(2, 1)             # fixed point of the trace map (derived in the note)
zi = z.inv()
A = [[(x*z - y)*zi, x*zi*zi], [x, y*zi]]
B = [[(y*z - x)*zi, Q(-1)*y*zi*zi], [Q(-1)*y, x*zi]]
assert det(A).key() == (1, 0) and det(B).key() == (1, 0)
A1, B1 = mm(minv(B), A), mm(minv(A), mm(B, B))
# intertwiner T with T M = M' T: T = sum over a spanning set  M'_i X M_i^-1 is not finite; instead use
# the closed form T = A1*N + N*A^-1 ... we simply search X in {E11,E12,E21,E22} for
# T = X + A1 X A^-1 + B1 X B^-1 + (A1B1) X (AB)^-1 projected by iterating the averaging map.
def lin_solve():
    # unknown T = [[t0,t1],[t2,t3]]; rows of T A - A1 T = 0 and T B - B1 T = 0
    rows = []
    for M, M1 in ((A, A1), (B, B1)):
        for i in range(2):
            for j in range(2):
                r = [ZERO]*4
                for k in range(2):
                    r[2*i + k] = r[2*i + k] + M[k][j]
                    r[2*k + j] = r[2*k + j] - M1[i][k]
                rows.append(r)
    piv, rk = [], 0
    for col in range(4):
        p = next((i for i in range(rk, 8) if rows[i][col].key() != (0, 0)), None)
        if p is None: continue
        rows[rk], rows[p] = rows[p], rows[rk]
        iv = rows[rk][col].inv(); rows[rk] = [e*iv for e in rows[rk]]
        for i in range(8):
            if i != rk and rows[i][col].key() != (0, 0):
                f = rows[i][col]; rows[i] = [a - f*b for a, b in zip(rows[i], rows[rk])]
        piv.append(col); rk += 1
    free = [c_ for c_ in range(4) if c_ not in piv]
    assert len(free) == 1
    v = [ZERO]*4; v[free[0]] = ONE
    for i, col in enumerate(piv): v[col] = Q(-1)*rows[i][free[0]]
    return [[v[0], v[1]], [v[2], v[3]]]
T = lin_solve()
assert same(mm(T, A), mm(A1, T)) and same(mm(T, B), mm(B1, T)) and det(T).key() != (0, 0)
dTi = det(T).inv()
def tau(M):
    m = mm(M, T); t = m[0][0] + m[1][1]
    return (t*t*dTi).key()
def W(*pairs):
    R = [[ONE, ZERO], [ZERO, ONE]]
    for l, e in pairs: R = mm(R, mpow(A if l == "a" else B, e))
    return R
N = int(sys.argv[1]) if len(sys.argv) > 1 else 14
S = int(sys.argv[2]) if len(sys.argv) > 2 else 40
BiA = mm(minv(B), A)
cand = {}
for s in range(-S, S + 1):
    cand.setdefault(tau(W(("a", s), ("b", s))), set()).add(s)          # (x^s y)^2 = (a^s b^s, 2)
    cand.setdefault(tau(mm(mpow(B, s), mpow(BiA, s))), set()).add(s)   # y (x^s y)^2 Y
hits = []
for n in range(1, N + 1):
    k2 = tau(W(("a", n), ("b", -1), ("a", -1), ("b", n), ("a", -1)))   # k_n^2 = (a^n B A b^n A, 2)
    hits += [(n, s) for s in sorted(cand.get(k2, ()))]
    th = tau(W(("a", -n), ("b", 1), ("a", 1), ("b", -n), ("a", 2)))
    # theta(k_n)^2 = (v phi(v), 2), v = a^-n b a b, phi(v) = b^-n (Ba) b (Ba) = b^-(n+1) a a
    hits += [("theta", n, s) for s in sorted(cand.get(th, ()))]
print("trace coincidences (n,s), n<=%d, |s|<=%d:" % (N, S), hits)
