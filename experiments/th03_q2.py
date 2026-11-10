#!/usr/bin/env python3
"""Agent TH03: the k_n-frozen primitive exit Q2(n) via twisted traces on a truncated Magnus algebra.

G_{k_n} = <x,y | x^n YXyy> = F(t_0..t_{n-1}) x|_psi <x>,  t = y x^(n-1), t_i = x^i t x^-i,
psi(t_i) = t_{i+1} (i < n-1), psi(t_{n-1}) = t_{n-1} t_0.  Elements (u,k) = u x^k.
c = xyxYYXy = (t_1 T_2 T_1, 1) for n >= 3; the primitive candidates are x t^j = (t_1^j, 1).
A linear functional l on A = Q<X_0..X_{n-1}>/(degree > D) with l(a m) = l(m Psi(a)) for all a, m
("twisted trace"; Psi(X_i) = Magnus(psi(t_i)) - 1) gives the twisted-conjugacy invariant
u -> l(Magnus(u)) of the class of (u,1), where Magnus(t_i) = 1 + X_i.

    python3 experiments/th03_q2.py --selftest
"""
import itertools
import random
import sys
from fractions import Fraction as Fr

def red(w):                                   # words: tuples of nonzero ints, +-(i+1) = t_i^{+-1}
    out = []
    for g in w:
        if out and out[-1] == -g: out.pop()
        else: out.append(g)
    return tuple(out)
def inv(w): return tuple(-g for g in reversed(w))

class GK:
    def __init__(self, n, D):
        self.n, self.D = n, D
        self.mons = [m for d in range(D + 1) for m in itertools.product(range(n), repeat=d)]
        self.idx = {m: i for i, m in enumerate(self.mons)}
        self.PsiX = [self.magnus(self.psi((i + 1,))) for i in range(n)]
        for P in self.PsiX: P[()] = P.get((), 0) - 1          # Psi(X_i) = Magnus(psi(t_i)) - 1
        self.traces = self._traces()
    # ---- the automorphism psi and its inverse on words
    def psi(self, w):
        n, out = self.n, []
        for g in w:
            i = abs(g) - 1
            img = (i + 2,) if i < n - 1 else (n, 1)
            out.extend(img if g > 0 else inv(img))
        return red(out)
    def psi_inv(self, w):
        n, out = self.n, []
        for g in w:
            i = abs(g) - 1
            img = (i,) if i >= 1 else (-(n - 1), n)           # psi^-1(t_0) = T_{n-2} t_{n-1}
            out.extend(img if g > 0 else inv(img))
        return red(out)
    def nf(self, w):
        """Normal form (u,k) of an (x,y)-word, y = t x^(1-n)."""
        n = self.n
        w = "".join({'x': 'x', 'X': 'X', 'y': 't' + 'X' * (n - 1), 'Y': 'x' * (n - 1) + 'T'}[ch] for ch in w)
        u, k = (), 0
        for ch in w:
            if ch == 'x': k += 1
            elif ch == 'X': k -= 1
            else:
                g = (1,) if ch == 't' else (-1,)
                for _ in range(abs(k)): g = self.psi(g) if k > 0 else self.psi_inv(g)
                u = red(u + g)
        return u, k
    # ---- truncated algebra
    def mul(self, P, Q):
        R = {}
        for m1, c1 in P.items():
            for m2, c2 in Q.items():
                if len(m1) + len(m2) <= self.D:
                    m = m1 + m2; R[m] = R.get(m, 0) + c1 * c2
        return {m: c for m, c in R.items() if c}
    def magnus(self, w):
        P = {(): 1}
        for g in w:
            i = abs(g) - 1
            if g > 0: L = {(): 1, (i,): 1}
            else: L = {(i,) * d: (-1) ** d for d in range(self.D + 1)}
            P = self.mul(P, L)
        return P
    def Psi(self, P):                          # algebra endomorphism induced by psi
        R = {}
        for m, c in P.items():
            T = {(): c}
            for i in m: T = self.mul(T, self.PsiX[i])
            for mm, cc in T.items(): R[mm] = R.get(mm, 0) + cc
        return {m: c for m, c in R.items() if c}
    def _traces(self):
        """Basis of {l : l(X_i m - m Psi(X_i)) = 0 for all i, monomials m} (exact, over Q)."""
        rows = []
        for i in range(self.n):
            for m in self.mons:
                if len(m) >= self.D: continue
                r = dict(self.mul({(i,): 1}, {m: 1}))
                for mm, cc in self.mul({m: 1}, self.PsiX[i]).items(): r[mm] = r.get(mm, 0) - cc
                v = [Fr(0)] * len(self.mons)
                for mm, cc in r.items(): v[self.idx[mm]] = Fr(cc)
                rows.append(v)
        N = len(self.mons); piv = []; r0 = 0
        for c in range(N):
            pr = next((r for r in range(r0, len(rows)) if rows[r][c] != 0), None)
            if pr is None: continue
            rows[r0], rows[pr] = rows[pr], rows[r0]
            f = rows[r0][c]; rows[r0] = [e / f for e in rows[r0]]
            for r in range(len(rows)):
                if r != r0 and rows[r][c] != 0:
                    f = rows[r][c]; rows[r] = [e - f * g for e, g in zip(rows[r], rows[r0])]
            piv.append(c); r0 += 1
        free = [c for c in range(N) if c not in piv]
        basis = []
        for fc in free:
            l = [Fr(0)] * N; l[fc] = Fr(1)
            for i, c in enumerate(piv): l[c] = -rows[i][fc]
            basis.append(l)
        return basis
    def ev(self, l, P): return sum(l[self.idx[m]] * c for m, c in P.items())
    def Inv(self, u): P = self.magnus(u); return tuple(self.ev(l, P) for l in self.traces)
    def power_poly(self, i):
        """Inv(t_i^j) = sum_k C(j,k) * coef[k]  (generalized binomials; valid for all j in Z)."""
        return [tuple(l[self.idx[(i,) * k]] for l in self.traces) for k in range(self.D + 1)]

def binom(j, k):
    r = Fr(1)
    for i in range(k): r = r * (j - i) / (i + 1)
    return r

# ------------------------------------------------------------------ the question Q2(n)
C_WORD = 'xyxYYXy'

def relations(G):
    """All vectors X_i m - m Psi(X_i) (as dicts), i < n, m a monomial of degree < D."""
    out = []
    for i in range(G.n):
        for m in G.mons:
            if len(m) >= G.D: continue
            r = dict(G.mul({(i,): 1}, {m: 1}))
            for mm, cc in G.mul({m: 1}, G.PsiX[i]).items(): r[mm] = r.get(mm, 0) - cc
            out.append({m_: c_ for m_, c_ in r.items() if c_})
    return out

def integer_roots(poly):
    """Integer roots of sum_k poly[k] * C(j,k) (rational coefficients, not identically 0)."""
    D = len(poly) - 1
    # convert to the monomial basis exactly: C(j,k) = prod_{i<k} (j-i)/(i+1)
    mono = [Fr(0)] * (D + 1)
    for k, a in enumerate(poly):
        term = [Fr(1)]
        for i in range(k):
            new = [Fr(0)] * (len(term) + 1)
            for d, t in enumerate(term):
                new[d + 1] += t / (i + 1); new[d] -= t * i / (i + 1)
            term = new
        for d, t in enumerate(term): mono[d] += a * t
    den = 1
    for t in mono: den = den * t.denominator // __import__('math').gcd(den, t.denominator)
    ints = [int(t * den) for t in mono]
    roots = set()
    while ints and ints[0] == 0: roots.add(0); ints = ints[1:]
    if len(ints) > 1:
        a0 = abs(ints[0])
        for d in range(1, a0 + 1):
            if a0 % d == 0:
                for j in (d, -d):
                    if sum(cf * j ** e for e, cf in enumerate(ints)) == 0: roots.add(j)
    return sorted(r for r in roots if sum(binom(r, k) * a for k, a in enumerate(poly)) == 0)

def q2_rational(n, D):
    """(Inv(c), coefficient table, sorted list of all j in Z with Inv(t_1^j) = Inv(c))."""
    G = GK(n, D)
    cu, k = G.nf(C_WORD); assert k == 1
    ic = G.Inv(cu); co = G.power_poly(1)
    cand = None
    for r in range(len(G.traces)):
        poly = [co[k_][r] for k_ in range(D + 1)]; poly[0] -= ic[r]
        if any(poly):
            rts = set(integer_roots(poly))
            cand = rts if cand is None else cand & rts
    assert cand is not None, "no informative twisted trace"
    return G, ic, co, sorted(cand)

def q2_mod2(n, D):
    """F_2-valued twisted traces (bitset elimination).  Returns (#traces, allowed j mod 8)."""
    assert D < 8
    G = GK.__new__(GK); G.n, G.D = n, D
    G.mons = [m for d in range(D + 1) for m in itertools.product(range(n), repeat=d)]
    G.idx = {m: i for i, m in enumerate(G.mons)}
    G.PsiX = [G.magnus(G.psi((i + 1,))) for i in range(n)]
    for P in G.PsiX: P[()] = P.get((), 0) - 1
    N = len(G.mons)
    rows = []
    for r in relations(G):
        b = 0
        for m, c in r.items():
            if c % 2: b |= 1 << G.idx[m]
        if b: rows.append(b)
    piv = {}                                   # pivot column -> reduced row
    for b in rows:
        while b:
            c = b.bit_length() - 1
            if c in piv: b ^= piv[c]
            else: piv[c] = b; break
    # traces: l with <l, row> = 0 for all rows; back-substitution from low to high pivots
    free = [c for c in range(N) if c not in piv]
    basis = []
    for fc in free:
        l = 1 << fc
        for c in sorted(piv):                  # row = bit c + lower bits; solve l_c
            if bin(piv[c] & l & ~(1 << c)).count("1") % 2: l |= 1 << c
        assert all(bin(b & l).count("1") % 2 == 0 for b in rows)
        basis.append(l)
    def ev(l, P): return sum(c for m, c in P.items() if (l >> G.idx[m]) & 1) % 2
    cu, _ = G.nf(C_WORD); ic = tuple(ev(l, G.magnus(cu)) for l in basis)
    allowed = [j for j in range(8) if tuple(ev(l, G.magnus((2,) * j)) for l in basis) == ic]
    return len(basis), allowed

L3 = {'00': 1, '01': 1, '02': 1, '10': 1, '11': 1, '12': 1, '21': 1, '22': 1, '002': 1, '010': -1, '012': -1,
      '020': -2, '021': 1, '022': 1, '100': 1, '101': -1, '102': 1, '110': 1, '120': -1, '121': -1, '200': 1,
      '201': -2, '202': -1, '210': 2, '211': 1, '212': -1, '221': 1}   # the twisted trace l of Theorem T11 (n = 3)

def selftest():
    rnd = random.Random(11)
    for n in range(2, 8):                      # structure of G_{k_n}
        G = GK(n, 1)
        assert G.nf('x' * n + 'YXyy') == ((), 0)
        for _ in range(50):
            w = red(tuple(rnd.choice([1, -1]) * rnd.randint(1, n) for _ in range(8)))
            assert G.psi(G.psi_inv(w)) == w == G.psi_inv(G.psi(w))
        if n >= 3:
            assert G.nf(C_WORD) == ((2, -3, -2), 1)
        for j in range(1, 4):
            assert G.nf('x' + ('y' + 'x' * (n - 1)) * j) == ((2,) * j, 1)
    G, ic, co, sols = q2_rational(3, 3)
    assert len(G.mons) == 40 and len(G.traces) == 3
    l = [Fr(L3.get("".join(map(str, m)), 0)) for m in G.mons]
    assert all(G.ev(l, r) == 0 for r in relations(G)) and len(relations(G)) == 39   # l is a twisted trace
    cu, _ = G.nf(C_WORD)
    assert G.ev(l, G.magnus(cu)) == -2
    for j in range(-40, 41):
        u = (2,) * j if j >= 0 else (-2,) * (-j)
        assert G.ev(l, G.magnus(u)) == binom(j, 2) >= 0
    for _ in range(200):                       # invariance; and conjugates of c computed through nf
        u = red(tuple(rnd.choice([1, -1]) * rnd.randint(1, 3) for _ in range(rnd.randint(0, 8))))
        v = red(tuple(rnd.choice([1, -1]) * rnd.randint(1, 3) for _ in range(rnd.randint(1, 6))))
        assert G.Inv(red(v + u + inv(G.psi(v)))) == G.Inv(u) == G.Inv(G.psi(u))
    for _ in range(60):
        g = "".join(rnd.choice('xXyY') for _ in range(rnd.randint(1, 8)))
        u, k = G.nf(g + C_WORD + g.swapcase()[::-1]); assert k == 1 and G.Inv(u) == ic
    assert sols == []
    nt4, allowed4 = q2_mod2(4, 4); assert nt4 == 7 and allowed4 == []
    G5, ic5, co5, sols5 = q2_rational(5, 3); assert len(G5.traces) == 4 and sols5 == []
    return ic, co, ic5, co5

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        ic, co, ic5, co5 = selftest()
        print("th03_q2 self-test passed")
        print("n=3: l(c) = -2, l(x t^j) = C(j,2) >= 0  => Q2(3) has no solution j")
        print("n=3 full invariant: Inv(c) =", [str(a) for a in ic], " Inv(t_1^j) coefficients of C(j,k):", [[str(a) for a in c] for c in co])
        print("n=4: 7 twisted traces mod 2 in degree <= 4, no residue j mod 8 allowed => Q2(4) has no solution")
        print("n=5: Inv(c) =", [str(a) for a in ic5], " coefficients:", [[str(a) for a in c] for c in co5], "=> no integer j")
    else:
        print(__doc__)
