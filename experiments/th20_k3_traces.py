#!/usr/bin/env python3
"""TH20: own twisted traces for G_{k3} = <x,y | xxxYXyy> = F(t0,t1,t2) x|_psi <x> (t0 = y x^2, t_i = x^i t0 x^-i,
psi: t0->t1, t1->t2, t2->t2 t0), used to check TH16 Theorem H(b) (q1 frozen side of Q).  Linear functionals l on
A = Q<X0,X1,X2>/(deg > D) with l(X_i m) = l(m Psi(X_i)) are twisted-conjugacy invariants of (u,1)."""
import sys, itertools
from fractions import Fraction as F
sys.dont_write_bytecode = True
from th20_lib import red, inv, cyc, conj, aut
D = 3
PSI = {0: [((1,), 1)], 1: [((2,), 1)], 2: [((2,), 1), ((0,), 1), ((2, 0), 1)]}   # Psi(X_i) as list of (monomial, coeff)
MON = [m for d in range(D + 1) for m in itertools.product(range(3), repeat=d)]
IDX = {m: i for i, m in enumerate(MON)}
def mul(p, q):
    r = {}
    for a, x in p.items():
        for b, y in q.items():
            if len(a) + len(b) <= D: r[a + b] = r.get(a + b, 0) + x * y
    return {m: v for m, v in r.items() if v}
def gen(i, s): return {(): 1, (i,): 1} if s > 0 else {(i,) * d: (-1) ** d for d in range(D + 1)}
def psi_t(i, s):        # psi(t_i)^s as a word over (index, sign)
    w = {0: [(1, 1)], 1: [(2, 1)], 2: [(2, 1), (0, 1)]}[i]
    return w if s > 0 else [(j, -e) for j, e in reversed(w)]
def psi_word(u, k):     # psi^k(u), k >= 0, u list of (i, sign)
    for _ in range(k): u = [y for (i, s) in u for y in psi_t(i, s)]
    return u
def psiinv_word(u):     # psi^-1: t0 -> t1^-1 t2, t1 -> t0, t2 -> t1
    img = {0: [(1, -1), (2, 1)], 1: [(0, 1)], 2: [(1, 1)]}
    out = []
    for i, s in u: out += img[i] if s > 0 else [(j, -e) for j, e in reversed(img[i])]
    return out
def nf(word):           # element = u x^k ; y = t0 x^-2, Y = x^2 t0^-1
    u, k = [], 0
    for ch in word:
        if ch == "x": k += 1
        elif ch == "X": k -= 1
        else:
            s = 1 if ch == "y" else -1
            kk = k if s > 0 else k + 2
            v = [(0, s)]
            if kk >= 0: v = psi_word(v, kk)
            else:
                for _ in range(-kk): v = psiinv_word(v)
            u += v; k += -2 if s > 0 else 2
    out = []
    for g in u:
        if out and out[-1] == (g[0], -g[1]): out.pop()
        else: out.append(g)
    return out, k
assert nf("xxxYXyy") == ([], 0)
def magnus(u):
    r = {(): 1}
    for i, s in u: r = mul(r, gen(i, s))
    return r
# solve for twisted traces
rows = []
for i in range(3):
    for m in MON:
        lhs = {(i,) + m: 1} if len(m) < D else {}
        rhs = mul({m: 1}, {mm: c for mm, c in PSI[i]})
        row = [F(0)] * len(MON)
        for mm, c in lhs.items(): row[IDX[mm]] += c
        for mm, c in rhs.items(): row[IDX[mm]] -= c
        rows.append(row)
piv = []; R = [r[:] for r in rows]; rk = 0
for col in range(len(MON)):
    p = next((r for r in range(rk, len(R)) if R[r][col] != 0), None)
    if p is None: continue
    R[rk], R[p] = R[p], R[rk]; R[rk] = [v / R[rk][col] for v in R[rk]]
    for r in range(len(R)):
        if r != rk and R[r][col] != 0: R[r] = [a - R[r][col] * b for a, b in zip(R[r], R[rk])]
    piv.append(col); rk += 1
free = [c for c in range(len(MON)) if c not in piv]
basis = []
for f in free:
    v = [F(0)] * len(MON); v[f] = F(1)
    for r, col in enumerate(piv): v[col] = -R[r][f]
    basis.append(v)
def invariant(word):
    u, k = nf(word)
    if k == -1: u, k = nf(inv(word))
    assert k == 1, (word, k)
    M = magnus(u)
    return tuple(sum(v[IDX[m]] * c for m, c in M.items()) for v in basis)
import random
rnd = random.Random(3)
c = "xyxYYXy"; base = invariant(c)
for _ in range(300):    # invariance under conjugation and insertion of conjugates of k3
    g = red("".join(rnd.choice("xXyY") for _ in range(rnd.randint(0, 6)))); j = rnd.randint(0, len(c))
    h = red("".join(rnd.choice("xXyY") for _ in range(rnd.randint(0, 4))))
    w = red(g + c[:j] + h + rnd.choice(["xxxYXyy", "YYxyXXX"]) + inv(h) + c[j:] + inv(g))
    assert invariant(w) == base
print("twisted traces (D=3): space of dimension %d; invariance on 300 random conjugates/relator insertions of c: OK" % len(basis))
TH = {"x": "X", "y": "y"}; q1 = "xxyXYY"; tq1 = aut(TH, q1)
assert invariant(tq1) == base, "theta(q1) and c differ"
def words(L):
    def rec(p):
        if len(p) == L:
            if p[0] != p[-1].swapcase(): yield p
            return
        for ch in "xXyY":
            if not p or p[-1] != ch.swapcase(): yield from rec(p + ch)
    yield from rec("")
left = []
for L in range(1, 6):
    for w in words(L):
        tw = aut(TH, w); d = sum({"x": 1, "X": -1, "y": -2, "Y": 2}[ch] for ch in tw)
        if abs(d) == 1 and invariant(tw) == base: left.append(w)
print("words W of length <= 5 (degree +-1 in G_{q2}) with theta(W) not separated from theta(q1)^{+-1}:", left)
