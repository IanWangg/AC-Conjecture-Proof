#!/usr/bin/env python3
"""TH01: exact replay of the AC path (omega,t) -> (z*omega,t) of research-th01 Theorem 4.2
in G = <SL(2,3), t | [t,z]=1> = SL(2,3) *_{<z>} (<z> x Z), z = -1.

Standard library only.  K = SL(2,3) = 24 unit Hurwitz quaternions, stored with doubled
integer coordinates (a,b,c,d) ~ (a+bi+cj+dk)/2.  Elements of G are kept in the amalgam
normal form  k0 t^n1 k1 ... t^nr kr  with k1..kr in a fixed transversal of {+-1} in K,
interior ki not central, ni != 0 (unique by the normal form theorem for amalgams).
AC moves: invert, multiply coordinate a by coordinate b^{+-1}, conjugate one coordinate
by a generator i, w(=omega), t or its inverse.   Usage: --selftest | --replay
"""
import itertools, random, sys

def qmul(p, q):
    a, b, c, d = p; e, f, g, h = q
    r = (a*e-b*f-c*g-d*h, a*f+b*e+c*h-d*g, a*g-b*h+c*e+d*f, a*h+b*g-c*f+d*e)
    assert all(x % 2 == 0 for x in r)
    return tuple(x // 2 for x in r)
def qinv(p): return (p[0], -p[1], -p[2], -p[3])
def qneg(p): return tuple(-x for x in p)
ONE, Z = (2, 0, 0, 0), (-2, 0, 0, 0)
I, J, KK, W = (0, 2, 0, 0), (0, 0, 2, 0), (0, 0, 0, 2), (-1, 1, 1, 1)
def closure(gens):
    S, frontier = {ONE}, [ONE]
    while frontier:
        nxt = []
        for x in frontier:
            for g in gens:
                y = qmul(x, g)
                if y not in S: S.add(y); nxt.append(y)
        frontier = nxt
    return S
K = closure([I, W])
def rep(k): return max(k, qneg(k))          # transversal of {+-1}

def norm(seq):
    """seq = [k0, n1, k1, ..., nr, kr] -> normal form tuple."""
    out = [seq[0]]
    for a in range(1, len(seq), 2):
        n, k = seq[a], seq[a+1]
        if n == 0: out[-1] = qmul(out[-1], k); continue
        out += [n, k]
        while len(out) >= 5 and out[-3] in (ONE, Z):     # central interior letter: merge t-powers
            s, n2, k2 = out[-3], out[-2], out[-1]
            del out[-3:]
            m = out[-1] + n2
            del out[-1]
            if m == 0: out[-1] = qmul(qmul(out[-1], s), k2)
            else: out += [m, qmul(s, k2)]
    for a in range(len(out)-1, 1, -2):                   # push signs to the left
        if rep(out[a]) != out[a]:
            out[a] = qneg(out[a]); out[a-2] = qneg(out[a-2])
    return tuple(out)
def gmul(x, y): return norm(list(x[:-1]) + [qmul(x[-1], y[0])] + list(y[1:]))
def ginv(x):
    ks = [qinv(k) for k in x[::2]][::-1]; ns = [-n for n in x[1::2]][::-1]
    return norm([v for pair in itertools.zip_longest(ks, ns) for v in pair if v is not None])
def gk(k): return (k,)
T = (ONE, 1, ONE)
def prod(*xs):
    r = gk(ONE)
    for x in xs: r = gmul(r, x)
    return r
def conj(x, g): return prod(ginv(g), x, g)               # x^g = g^-1 x g
def comm(a, b): return prod(ginv(a), ginv(b), a, b)
GENS = {"i": gk(I), "w": gk(W), "t": T}
GENS.update({k.upper(): ginv(v) for k, v in list(GENS.items())})
def word(s): return prod(*[GENS[c] for c in s])

def kword(target):
    """a word in i,w (and inverses) for an element of K, by BFS."""
    seen, frontier = {ONE: ""}, [ONE]
    while target not in seen:
        nxt = []
        for x in frontier:
            for c in "iwIW":
                y = qmul(x, GENS[c][0])
                if y not in seen: seen[y] = seen[x] + c; nxt.append(y)
        frontier = nxt
    return seen[target]
def gword(x):
    """a word in the six generator letters for an element of G in normal form."""
    s = kword(x[0])
    for a in range(1, len(x), 2):
        s += ("t" if x[a] > 0 else "T") * abs(x[a]) + kword(x[a+1])
    return s
def as_conj_product(target, a):
    """target in K as a list of (eps, h): target = prod (a^eps)^h, h in K (BFS in K)."""
    steps = [(e, h, qmul(qmul(qinv(h), a if e > 0 else qinv(a)), h)) for e in (1, -1) for h in sorted(K)]
    seen, frontier = {ONE: []}, [ONE]
    while target not in seen:
        nxt = []
        for x in frontier:
            for e, h, c in steps:
                y = qmul(x, c)
                if y not in seen: seen[y] = seen[x] + [(e, gk(h))]; nxt.append(y)
        if not nxt: raise ValueError("not in normal closure")
        frontier = nxt
    return seen[target]

class Pair:
    """a pair of G with a log of elementary AC moves."""
    def __init__(self, u, v): self.c, self.log = [u, v], []
    def inv(self, a): self.c[a] = ginv(self.c[a]); self.log.append(("invert", a))
    def mul(self, a, b): self.c[a] = gmul(self.c[a], self.c[b]); self.log.append(("multiply", a, b))
    def cj(self, a, letters):
        for ch in letters: self.c[a] = conj(self.c[a], GENS[ch]); self.log.append(("conjugate", a, ch))
    def mult_by_conj(self, a, eps, g):
        """coordinate a  <-  coordinate a * (other^eps)^g   (composite move (M))."""
        b, s = 1 - a, gword(g)
        self.cj(b, s)
        if eps < 0: self.inv(b)
        self.mul(a, b)
        if eps < 0: self.inv(b)
        self.cj(b, s.swapcase()[::-1])

def replay(verbose=True):
    w, i, j, t, z = gk(W), gk(I), gk(J), T, gk(Z)
    P = Pair(w, t)
    # step 1: omega -> p = omega * t^-1 * t^i
    P.mult_by_conj(0, -1, gk(ONE)); P.mult_by_conj(0, 1, i)
    p = prod(w, comm(t, i)); assert P.c == [p, t]
    # step 2: t -> t j^-1, with j^-1 written as a product of conjugates of p^{+-1}:
    #   i*omega = prod_{m=0..3} gam^m (i p i^-1) gam^-m,  gam = t^-1 i t   (Lemma 2.3, n = 4)
    gam = conj(i, t); iw = gmul(i, w)
    gms = [ginv(prod(*([gam] * m + [i]))) for m in range(4)]       # p^{g_m} = gam^m i p i^-1 gam^-m
    assert prod(*[conj(p, g) for g in gms]) == iw
    for eps, h in as_conj_product(qinv(J), iw[0]):
        for g in (gms if eps > 0 else gms[::-1]):
            P.mult_by_conj(1, eps, gmul(g, h))
    tp = gmul(t, ginv(j)); assert P.c == [p, tp]
    # step 3: p -> p*w = z*omega,  w = (t'^-1)^{A^-1} (t')^{(AB)^-1},  A = i^-1 j^-1, AB = i^-1 j^-1 i
    A = prod(ginv(i), ginv(j)); AB = gmul(A, i)
    P.mult_by_conj(0, -1, ginv(A)); P.mult_by_conj(0, 1, ginv(AB))
    assert P.c == [gmul(z, w), tp]
    # step 4: t j^-1 -> t, with j a product of conjugates of (z*omega)^{+-1} in K
    for eps, h in as_conj_product(J, qmul(Z, W)): P.mult_by_conj(1, eps, h)
    ok = P.c == [gmul(z, w), t]
    if verbose:
        n = {k: sum(1 for m in P.log if m[0] == k) for k in ("invert", "multiply", "conjugate")}
        print("start (omega, t); end == (z*omega, t):", ok, "| elementary moves:", len(P.log), n)
    return ok, P.log

def selftest():
    rnd = random.Random(1)
    assert len(K) == 24 and Z in K and comm(gk(J), gk(I)) == gk(Z)
    Q8 = closure([I, J]); assert len(Q8) == 8
    for a in K:                                   # normal closures in K: outside Q8 -> all of K
        ncl = closure([qmul(qmul(qinv(h), a), h) for h in K])
        assert len(ncl) == (24 if a not in Q8 else 8 if a not in (ONE, Z) else 2 if a == Z else 1)
    def rand():
        return norm([rnd.choice(sorted(K))] + [v for _ in range(rnd.randint(0, 4))
                    for v in (rnd.choice([-2, -1, 1, 2]), rnd.choice(sorted(K)))])
    for _ in range(3000):
        a, b, c = rand(), rand(), rand()
        assert gmul(gmul(a, b), c) == gmul(a, gmul(b, c)) and gmul(a, ginv(a)) == gk(ONE)
        assert gmul(a, gk(Z)) == gmul(gk(Z), a) and word(gword(a)) == a
    assert comm(T, gk(Z)) == gk(ONE) and comm(T, gk(I)) != gk(ONE) and gk(Z) != gk(ONE)
    w, i, t = gk(W), gk(I), T                      # Lemma 2.3: c u = (c p c^-1)(t^-1 c t)
    p = prod(w, comm(t, i)); assert gmul(i, w) == prod(i, p, ginv(i), ginv(t), i, t)
    iw = qmul(I, W); assert qmul(qmul(iw, iw), iw) == ONE and iw not in Q8
    assert qmul(Z, W) not in Q8 and gmul(gk(Z), w) != w
    ok, log = replay(verbose=False); assert ok
    # the logged elementary moves alone reproduce the endpoint
    c = [w, t]
    for m in log:
        if m[0] == "invert": c[m[1]] = ginv(c[m[1]])
        elif m[0] == "multiply": c[m[1]] = gmul(c[m[1]], c[m[2]])
        else: c[m[1]] = conj(c[m[1]], GENS[m[2]])
    assert c == [gmul(gk(Z), w), t]
    identities_s4(rnd)
    print("selftest passed: |K|=24, normal form checks (3000 random triples), Lemma 2.3 identity, replay of", len(log),
          "moves, S4 identities for Lemma 3.4 / Theorem 3.5(b)")

def identities_s4(rnd):
    """the two algebraic identities behind Lemma 3.4 and Theorem 3.5(b), tested in S4 with N = V4."""
    def pm(a, b): return tuple(a[b[i]] for i in range(4))          # (a*b)(i) = a(b(i))
    def pi(a):
        r = [0] * 4
        for i, x in enumerate(a): r[x] = i
        return tuple(r)
    def cm(a, b): return pm(pm(pi(a), pi(b)), pm(a, b))
    S4 = list(itertools.permutations(range(4)))
    V4 = [(0, 1, 2, 3), (1, 0, 3, 2), (2, 3, 0, 1), (3, 2, 1, 0)]
    for _ in range(2000):
        g, h, s_, t_ = (rnd.choice(S4) for _ in range(4))
        m, nu0, nu1, n = (rnd.choice(V4) for _ in range(4))
        gh = pm(pm(pi(h), g), h); gnh = pm(pm(pi(h), pm(g, nu0)), h)
        assert cm(m, gnh) == cm(m, gh)                              # Lemma 3.4
        lhs = pm(pm(pm(t_, nu1), pm(pm(s_, nu0), n)), pi(pm(s_, nu0)))
        assert lhs == pm(pm(t_, nu1), pm(pm(s_, n), pi(s_)))        # Theorem 3.5(b), last step
    return True

if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    elif "--replay" in sys.argv: sys.exit(0 if replay()[0] else 1)
    else: print(__doc__)
