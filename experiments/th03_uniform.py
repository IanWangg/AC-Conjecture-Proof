#!/usr/bin/env python3
"""Agent TH03 (round 5): exact length-spectrum invariant on G_c = F(a,b) x|_phi Z.

G_c = <x,y | xyxYYXy>, a = x, b = yxY, phi(a) = b, phi(b) = B a  (research-o, O1).
rho: F(a,b) -> SL(2, Z[w]) (w = primitive cube root of unity),
    A = [[1,1],[w,1+w]],  B = [[1-w,w],[1+w,0]],  Y = [[w^2,0],[w^2,w]],
with  Y conj(A) Y^-1 = B  and  Y conj(B) Y^-1 = B^-1 A  (exact).  Hence
rho(phi(u)) = Y conj(rho(u)) Y^-1 and, for a degree-1 element (u,1),
    I(u) = tr( N conj(N) ),  N = rho(u) Y,
is an INTEGER depending only on the phi-twisted conjugacy class of u, i.e. only
on the conjugacy class of (u,1) in G_c.   sigma(s) = I(a^s)  [x^s y],
tau(n) = I(a^n B A)  [k_n = x^n YXyy].   Part B: a second exact invariant at a
rational point of the character curve of H = F(a,b) x| <y^2> (separates n=4,5).

    python3 experiments/th03_uniform.py --selftest
    python3 experiments/th03_uniform.py --table 12
"""
import random
import sys
from fractions import Fraction as Fr

# ------------------------------------------------------------------ Z[w]
def zadd(p, q): return (p[0] + q[0], p[1] + q[1])
def zneg(p): return (-p[0], -p[1])
def zmul(p, q):                       # (a+bw)(c+dw), w^2 = -1-w
    a, b = p; c, d = q
    return (a * c - b * d, a * d + b * c - b * d)
def zconj(p): return (p[0] - p[1], -p[1])      # w -> w^2 = -1-w
Z0, Z1, ZW, ZW2 = (0, 0), (1, 0), (0, 1), (-1, -1)

class Ring:                            # 2x2 matrices over a commutative ring
    def __init__(self, add, mul, neg, zero, one):
        self.add, self.mul, self.neg, self.zero, self.one = add, mul, neg, zero, one
        self.I = ((one, zero), (zero, one))
    def mm(self, M, N):
        a, m = self.add, self.mul
        return tuple(tuple(a(m(M[i][0], N[0][j]), m(M[i][1], N[1][j])) for j in range(2)) for i in range(2))
    def det(self, M): return self.add(self.mul(M[0][0], M[1][1]), self.neg(self.mul(M[0][1], M[1][0])))
    def tr(self, M): return self.add(M[0][0], M[1][1])
    def adj(self, M): return ((M[1][1], self.neg(M[0][1])), (self.neg(M[1][0]), M[0][0]))
    def power(self, M, n):
        if n < 0: M, n = self.adj(M), -n
        R = self.I
        for _ in range(n): R = self.mm(R, M)
        return R
    def word(self, gens, u):           # gens: {'a': A, 'b': B}; capitals = inverses (det 1)
        R = self.I
        for ch in u:
            G = gens[ch.lower()]
            R = self.mm(R, G if ch.islower() else self.adj(G))
        return R

RW = Ring(zadd, zmul, zneg, Z0, Z1)
A = ((Z1, Z1), (ZW, (1, 1)))
B = (((1, -1), ZW), ((1, 1), Z0))
Y = ((ZW2, Z0), (ZW2, ZW))
GW = {'a': A, 'b': B}
def mconj(M): return tuple(tuple(zconj(e) for e in r) for r in M)

def I_of_matrix(M):
    N = RW.mm(M, Y)
    t = RW.tr(RW.mm(N, mconj(N)))
    assert t[1] == 0                   # real element of Z[w] = rational integer
    return t[0]
def I(u): return I_of_matrix(RW.word(GW, u))
def sigma(s): return I_of_matrix(RW.power(A, s))
def tau(n): return I_of_matrix(RW.mm(RW.power(A, n), RW.word(GW, 'BA')))

# ------------------------------------------------------------------ F(a,b), phi
def red(w):
    out = []
    for ch in w:
        if out and out[-1] == ch.swapcase(): out.pop()
        else: out.append(ch)
    return "".join(out)
def inv(w): return w.swapcase()[::-1]
PHI = {'a': 'b', 'b': 'Ba'}
def phi(u): return red("".join(PHI[ch] if ch.islower() else inv(PHI[ch.lower()]) for ch in u))
def nf(w):                             # normal form (u,k) of an (x,y)-word, as in o_gc.nf
    u, k = "", 0
    for ch in w:
        if ch in "xX":
            g = 'a' if ch == 'x' else 'A'
            for _ in range(abs(k)):
                g = phi(g) if k > 0 else red("".join({'a': 'ab', 'b': 'a', 'A': 'BA', 'B': 'A'}[c] for c in g))
            u = red(u + g)
        else:
            k += 1 if ch == 'y' else -1
    return u, k

# ------------------------------------------------------------------ Part B: rational point
RQ = Ring(lambda p, q: p + q, lambda p, q: p * q, lambda p: -p, Fr(0), Fr(1))
def rational_point(p):
    """Character (x, v, v), v = p + 1/p, x = v/(v-1): fixed by phi^2.  Returns A, B, T over Q
    with T A = (B^-1 A) T and T B = (A^-1 B^2) T (T solved exactly, then verified)."""
    p = Fr(p); v = p + 1 / p; x = v / (v - 1)
    Aq = ((x, Fr(-1)), (Fr(1), Fr(0)))
    Bq = ((p, Fr(0)), (x * p - v, 1 / p))
    P1 = RQ.mm(RQ.adj(Bq), Aq); P2 = RQ.mm(RQ.adj(Aq), RQ.mm(Bq, Bq))
    rows = []                          # linear equations in T = (t0,t1,t2,t3) = [[t0,t1],[t2,t3]]
    for G, P in ((Aq, P1), (Bq, P2)):
        for i in range(2):
            for j in range(2):
                r = [Fr(0)] * 4        # (T G)_{ij} - (P T)_{ij}
                for k in range(2):
                    r[2 * i + k] += G[k][j]
                    r[2 * k + j] -= P[i][k]
                rows.append(r)
    piv, r0 = [], 0                    # Gaussian elimination, nullspace
    for c in range(4):
        pr = next((r for r in range(r0, len(rows)) if rows[r][c] != 0), None)
        if pr is None: continue
        rows[r0], rows[pr] = rows[pr], rows[r0]
        rows[r0] = [e / rows[r0][c] for e in rows[r0]]
        for r in range(len(rows)):
            if r != r0 and rows[r][c] != 0:
                f = rows[r][c]; rows[r] = [e - f * g for e, g in zip(rows[r], rows[r0])]
        piv.append(c); r0 += 1
    free = [c for c in range(4) if c not in piv]
    assert len(free) == 1, "intertwiner space must be a line"
    t = [Fr(0)] * 4; t[free[0]] = Fr(1)
    for i, c in enumerate(piv): t[c] = -rows[i][free[0]]
    T = ((t[0], t[1]), (t[2], t[3]))
    assert RQ.det(T) != 0 and RQ.mm(T, Aq) == RQ.mm(P1, T) and RQ.mm(T, Bq) == RQ.mm(P2, T)
    return Aq, Bq, T
def J(pt, u):
    """tr(rho(u phi(u)) T)^2 / det T: invariant of the G_c-class of the degree-1 element (u,1)."""
    Aq, Bq, T = pt
    M = RQ.mm(RQ.word({'a': Aq, 'b': Bq}, red(u + phi(u))), T)
    return RQ.tr(M) ** 2 / RQ.det(T)

REC = (3, -1, 3, -1)                   # u(n+4) = 3u(n+3) - u(n+2) + 3u(n+1) - u(n)
def rec_ok(f, lo, hi):
    return all(f(n + 4) == 3 * f(n + 3) - f(n + 2) + 3 * f(n + 1) - f(n) for n in range(lo, hi))

def growth_base(f, m):
    """Hypothesis of Lemma T3 at m: f(m) > 0 and f(m+i+1) >= 2 f(m+i), i = 0,1,2."""
    return f(m) > 0 and all(f(m + i + 1) >= 2 * f(m + i) for i in range(3))

def selftest(N=200):
    rnd = random.Random(3)
    w3 = zmul(ZW, zmul(ZW, ZW)); assert w3 == Z1 and zadd(zadd(Z1, ZW), ZW2) == Z0
    # 1. the representation
    assert RW.det(A) == Z1 and RW.det(B) == Z1 and RW.det(Y) == Z1
    assert RW.tr(A) == (2, 1) and RW.tr(B) == (1, -1) and RW.tr(RW.mm(A, B)) == (1, -1)
    assert RW.mm(Y, mconj(A)) == RW.mm(B, Y)                       # Y conj(A) = B Y
    assert RW.mm(Y, mconj(B)) == RW.mm(RW.mm(RW.adj(B), A), Y)     # Y conj(B) = B^-1 A Y
    T = RW.mm(Y, mconj(Y))
    assert T == ((Z1, Z0), ((0, -1), Z1))                          # T = [[1,0],[-w,1]]
    assert RW.mm(T, A) == RW.mm(RW.mm(RW.adj(B), A), T)            # t a t^-1 = B a
    assert RW.mm(T, B) == RW.mm(RW.mm(RW.adj(A), RW.mm(B, B)), T)  # t b t^-1 = A b b
    assert red(phi(phi('a'))) == 'Ba' and red(phi(phi('b'))) == 'Abb'
    comm = RW.word(GW, 'abAB'); assert RW.tr(comm) == (-2, 0)      # parabolic commutator
    # 2. rho(phi(u)) Y = Y conj(rho(u)); invariance of I under twisted conjugation
    for _ in range(300):
        u = red("".join(rnd.choice('aAbB') for _ in range(rnd.randint(0, 14))))
        v = red("".join(rnd.choice('aAbB') for _ in range(rnd.randint(1, 10))))
        assert RW.mm(RW.word(GW, phi(u)), Y) == RW.mm(Y, mconj(RW.word(GW, u)))
        assert I(red(v + u + inv(phi(v)))) == I(u) == I(phi(u))
    # 3. normal forms of k_n and x^s y (cross-check with research-o's o_gc.nf when importable)
    for n in range(1, 9):
        assert nf('x' * n + 'YXyy') == ('a' * n + 'BA', 1)
        assert nf('x' * n + 'y') == ('a' * n, 1) and nf('X' * n + 'y') == ('A' * n, 1)
    try:
        sys.dont_write_bytecode = True
        sys.path.insert(0, __file__.rsplit('/', 1)[0])
        import o_gc
        for _ in range(300):
            w = "".join(rnd.choice('xXyY') for _ in range(rnd.randint(0, 16)))
            assert o_gc.nf(o_gc.red(w)) == nf(w)
        ogc = "cross-checked against o_gc.nf"
    except ImportError:
        ogc = "o_gc not importable (skipped)"
    # 4. tables, recurrence, symmetry
    S = {s: sigma(s) for s in range(-N - 2, N + 6)}
    Tt = {n: tau(n) for n in range(-N - 2, N + 6)}
    sg, ta = S.__getitem__, Tt.__getitem__
    assert [sg(s) for s in range(-1, 3)] == [2, 2, 2, 2] and [ta(n) for n in range(0, 4)] == [2, 8, 8, 20]
    assert rec_ok(sg, -N - 2, N) and rec_ok(ta, -N - 2, N)
    assert all(sg(s) == sg(1 - s) for s in range(-N, N))
    assert [sg(s) for s in range(3, 9)] == [8, 26, 74, 218, 650, 1928]
    assert [ta(n) for n in range(3, 9)] == [20, 74, 218, 632, 1880, 5588]
    # 5. Lemma T3 bases and Theorem T4 on a long window
    e = lambda n: sg(n + 1) - ta(n); d = lambda n: ta(n) - sg(n); dt = lambda n: ta(n + 1) - ta(n)
    assert growth_base(e, 6) and growth_base(d, 3) and growth_base(dt, 2)
    assert all(sg(n) < ta(n) < sg(n + 1) for n in range(6, N))
    assert all(sg(s) < sg(s + 1) for s in range(2, N)) and all(ta(n) < ta(n + 1) for n in range(2, N))
    vals = {sg(s): s for s in range(1, N + 2)}
    sols = [(n, vals[ta(n)]) for n in range(1, N) if ta(n) in vals]
    assert sols == [(1, 3), (2, 3), (4, 5), (5, 6)], sols
    # 6. controls: genuine conjugacies of research-o must have equal invariants
    assert I(nf('xy')[0]) == I(nf('xxy')[0]) and I(nf('y')[0]) == I(nf('Xy')[0])
    assert I('aBA') == I('aaBA') == I('AA') == 8
    assert I(red('ab' + 'aBA' + inv(phi('ab')))) == 8
    # 7. Part B: a rational point of the character curve of H separates n = 4, 5
    out = {}
    for p in (2, 3):
        pt = rational_point(p)
        Jk = {n: J(pt, 'a' * n + 'BA') for n in range(1, 9)}
        Js = {s: J(pt, ('a' * s if s >= 0 else 'A' * (-s))) for s in range(-9, 11)}
        assert Jk[1] == Jk[2] == Js[-2] == Js[3]                 # control (true conjugacy)
        assert all(Js[s] == Js[1 - s] for s in range(-8, 10))     # alpha-symmetry
        assert Js[0] == Js[-1] and Js[1] == Js[2]                 # control (true conjugacies)
        for u, v in (('ab', 'aBA'), ('Ba', 'aaBA'), ('abbA', 'aaa')):   # invariance
            assert J(pt, red(u + v + inv(phi(u)))) == J(pt, v) == J(pt, phi(v))
        assert Jk[4] != Js[5] and Jk[4] != Js[-4] and Jk[5] != Js[6] and Jk[5] != Js[-5]
        out[p] = (Jk[4], Js[5], Jk[5], Js[6])
    return ogc, out

def main():
    if "--table" in sys.argv:
        N = int(sys.argv[sys.argv.index("--table") + 1])
        print("s, sigma(s):", [(s, sigma(s)) for s in range(-N, N + 1)])
        print("n, tau(n):  ", [(n, tau(n)) for n in range(-N, N + 1)])
        return
    if "--selftest" in sys.argv:
        ogc, out = selftest()
        print("th03_uniform self-test passed (%s)" % ogc)
        print("solutions of tau(n) = sigma(s), 1 <= n < 200, s >= 1: (1,3),(2,3),(4,5),(5,6); sigma(s) = sigma(1-s)")
        for p, (j4, s5, j5, s6) in out.items():
            print("rational point p=%d: J(k_4)=%s != J(x^5y)=%s ; J(k_5)=%s != J(x^6y)=%s" % (p, j4, s5, j5, s6))
        return
    print(__doc__)

if __name__ == "__main__":
    main()
