"""TH19 independent check of TH03 Prop. T12 (Q2(4), Q2(5)) and Prop. T13 (integer twisted trace L4 on G_c).
Own code: truncated free algebra, the linear system (TT) l(X_i m) = l(m Psi(X_i)), its full solution space over Q or F_2."""
import itertools, sys
from fractions import Fraction as Fr
class Alg:
    def __init__(s, r, D): s.r, s.D = r, D; s.mons = [m for d in range(D+1) for m in itertools.product(range(r), repeat=d)]; s.idx = {m: i for i, m in enumerate(s.mons)}
    def mul(s, A, B):
        out = {}
        for m1, a in A.items():
            for m2, b in B.items():
                if len(m1) + len(m2) <= s.D: out[m1+m2] = out.get(m1+m2, 0) + a*b
        return {m: v for m, v in out.items() if v}
    def gen(s, i, e):
        if e == 1: return {(): 1, (i,): 1}
        return {tuple([i]*k): (-1)**k for k in range(s.D+1)}
    def M(s, word):
        R = {(): 1}
        for (i, e) in word: R = s.mul(R, s.gen(i, e))
        return R
def tt_rows(al, PsiX):
    rows = []
    for m in al.mons:
        if len(m) == al.D: continue
        for i in range(al.r):
            row = {al.idx[(i,)+m]: 1}
            for m2, v in al.mul({m: 1}, PsiX[i]).items(): row[al.idx[m2]] = row.get(al.idx[m2], 0) - v
            rows.append({k: v for k, v in row.items() if v})
    return rows
def nullspace(rows, n, mod=None):
    """basis of {l : row.l = 0 for all rows}, over Q (mod None) or F_p"""
    piv = {}                               # pivot column -> row (dict col->coef), reduced
    for row in rows:
        row = {k: (v % mod if mod else Fr(v)) for k, v in row.items()}; row = {k: v for k, v in row.items() if v}
        while row:
            c = min(row)
            if c in piv:
                f = row[c]; pr = piv[c]
                for k, v in pr.items():
                    nv = row.get(k, 0) - f*v
                    if mod: nv %= mod
                    if nv: row[k] = nv
                    else: row.pop(k, None)
            else:
                iv = pow(row[c], -1, mod) if mod else 1/row[c]
                piv[c] = {k: (v*iv % mod if mod else v*iv) for k, v in row.items()}; break
    free = [c for c in range(n) if c not in piv]; basis = []
    for f in free:                         # back-substitution: l[f] = 1, other free = 0
        l = {f: 1}
        for c in sorted(piv, reverse=True):
            s = sum(v * l.get(k, 0) for k, v in piv[c].items() if k != c)
            if mod: s %= mod
            if s: l[c] = (-s) % mod if mod else -s
        basis.append(l)
    return basis
def ev(al, l, A): return sum(v * l.get(al.idx[m], 0) for m, v in A.items())
# ---------------- (A) G_c, rank 2 (a=0, b=1), D = 4, Psi(X_a) = X_b, Psi(X_b) = (1+X_b)^-1 (1+X_a) - 1
al = Alg(2, 4)
Pb = al.mul(al.gen(1, -1), al.gen(0, 1)); Pb[()] = Pb.get((), 0) - 1; Pb = {m: v for m, v in Pb.items() if v}
rows = tt_rows(al, {0: {(1,): 1}, 1: Pb}); ns = nullspace(rows, len(al.mons))
code = lambda s: tuple("ab".index(ch) for ch in s)
L4 = {}
for s_, v in [("ba", 1), ("aaa", 1), ("aab", 1), ("abb", 1), ("bbb", 1), ("aba", -1), ("bab", -1), ("baa", 2), ("bba", 3),
              ("aaaa", 1), ("aaab", 1), ("aabb", 1), ("abbb", 1), ("bbbb", 1), ("aaba", -1), ("abab", -1), ("baba", -1), ("babb", -1),
              ("abaa", -2), ("baab", -2), ("bbaa", 2), ("bbba", 2)]: L4[al.idx[code(s_)]] = v
viol = sum(1 for row in rows if sum(v * L4.get(k, 0) for k, v in row.items()) != 0)
kn = [ev(al, L4, al.M([(0, 1)]*n + [(1, -1), (0, -1)])) for n in range(1, 10)]
xs = all(ev(al, L4, al.M([(0, 1 if s > 0 else -1)]*abs(s))) == (s+1)*s*(s-1)*(s-2)//24 for s in range(-30, 31))
print(f"(A) G_c, D=4: {len(rows)} (TT) equations, solution space dim {len(ns)}; L4 violates {viol}; L4(k_n), n=1..9: {kn}; L4(x^s y) = C(s+1,4) for |s|<=30: {xs}")
# ---------------- (B),(C) G_{k_n}: rank n, psi: t_i -> t_{i+1}, t_{n-1} -> t_{n-1} t_0 ; c -> (t1 t2^-1 t1^-1, 1), x t^j -> (t1^j, 1)
def setup(n, D):
    al = Alg(n, D); PsiX = {i: {(i+1,): 1} for i in range(n-1)}; PsiX[n-1] = {(n-1,): 1, (0,): 1, (n-1, 0): 1}
    return al, tt_rows(al, PsiX)
al, rows = setup(3, 3); ns = nullspace(rows, len(al.mons))
print(f"(B0) n=3, D=3 over Q: solution space dim {len(ns)} (TH03: 3)")
al, rows = setup(4, 4); ns = nullspace(rows, len(al.mons), mod=2)
cM = al.M([(1, 1), (2, -1), (1, -1)])
allowed = [j for j in range(8) if all((ev(al, l, al.M([(1, 1)]*j)) - ev(al, l, cM)) % 2 == 0 for l in ns)]
print(f"(B) n=4, D=4 over F_2: {len(al.mons)} monomials, solution space dim {len(ns)} (TH03: 7); residues j mod 8 on which all traces agree for t1^j and c: {allowed}")
al, rows = setup(5, 3); ns = nullspace(rows, len(al.mons))
cM = al.M([(1, 1), (2, -1), (1, -1)])
# is there a twisted trace vanishing on 1, X1, X1X1, X1X1X1 (hence on all M(t1^j)) and nonzero on M(c)?  Solve in the nullspace.
keys = [al.idx[()], al.idx[(1,)], al.idx[(1, 1)], al.idx[(1, 1, 1)]]
import copy
vecs = [[l.get(k, 0) for k in keys] + [ev(al, l, cM)] for l in ns]      # each basis trace: its 4 "power" coordinates and its value on c
# nullspace of the 4 power coordinates within span(ns): brute elimination over Q on the small matrix
rowsm = [list(map(Fr, v)) for v in vecs]; r = 0
for col in range(4):
    p = next((i for i in range(r, len(rowsm)) if rowsm[i][col] != 0), None)
    if p is None: continue
    rowsm[r], rowsm[p] = rowsm[p], rowsm[r]
    for i in range(len(rowsm)):
        if i != r and rowsm[i][col] != 0:
            f = rowsm[i][col] / rowsm[r][col]; rowsm[i] = [a - f*b for a, b in zip(rowsm[i], rowsm[r])]
    r += 1
killing = [row[4] for row in rowsm[r:]]
print(f"(C) n=5, D=3 over Q: solution space dim {len(ns)} (TH03: 4); traces vanishing on all M(t1^j): {len(rowsm)-r}, their values on c: {killing}")
