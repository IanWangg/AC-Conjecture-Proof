#!/usr/bin/env python3
"""TH11: nilpotent Reidemeister invariants (kappa, J) of degree-1 conjugacy classes of
G_c = F(a,b) x|_phi Z  (phi(a)=b, phi(b)=b^-1 a), and the symmetry theta0 = (x->X, y->yx).

(u,1) ~ (u',1) in G_c  iff  u' = v u phi(v)^-1 for some v in F(a,b)   (research-o, 2.2).
We compute the complete invariant of the phi-twisted class of u in F/gamma_5 F:
   kappa(u) in Z/2   (level gamma_2/gamma_3),   J(u) in Z   (level gamma_4/gamma_5),
exactly, in the truncated Magnus algebra Z<X,Y>/(degree>=5)  (a -> 1+X, b -> 1+Y).
Usage:  python3 experiments/th11_nil.py --selftest
"""
import random, sys
from itertools import product

D = 4                                    # truncation degree (work modulo degree >= 5)
MONO = [m for d in range(D + 1) for m in product((0, 1), repeat=d)]

def mul(p, q):
    r = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            if len(m1) + len(m2) <= D:
                m = m1 + m2
                r[m] = r.get(m, 0) + c1 * c2
    return {m: c for m, c in r.items() if c}

ONE = {(): 1}
def gen(i, sign):                        # 1+X_i or its inverse 1 - X_i + X_i^2 - ...
    if sign > 0:
        return {(): 1, (i,): 1}
    return {(i,) * d: (-1) ** d for d in range(D + 1)}
LET = {"a": gen(0, 1), "A": gen(0, -1), "b": gen(1, 1), "B": gen(1, -1)}

def red(w):
    out = []
    for ch in w:
        if out and out[-1] == ch.swapcase(): out.pop()
        else: out.append(ch)
    return "".join(out)
def inv(w): return w.swapcase()[::-1]
PHI = {"a": "b", "b": "Ba"}
def endo(img, u):
    return red("".join(img[ch] if ch.islower() else inv(img[ch.lower()]) for ch in u))
def phi(u): return endo(PHI, u)
def power(w, n): return w * n if n >= 0 else inv(w) * (-n)
def mu(u):
    r = ONE
    for ch in u: r = mul(r, LET[ch])
    return r
def tw(v, u): return red(v + u + inv(phi(v)))        # v u phi(v)^-1

def comm(p, q): return red(p + q + inv(p) + inv(q))
Z = comm("a", "b")                       # z = [a,b] = abAB
ZA, ZB = comm(Z, "a"), comm(Z, "b")      # basis of gamma_3/gamma_4
L4 = [comm(ZA, "a"), comm(ZA, "b"), comm(ZB, "b")]   # basis of gamma_4/gamma_5

def part(p, d): return {m: c for m, c in p.items() if len(m) == d}
def sub(p, q):
    r = dict(p)
    for m, c in q.items(): r[m] = r.get(m, 0) - c
    return {m: c for m, c in r.items() if c}

L4VEC = [part(mu(w), 4) for w in L4]     # leading (degree 4) Lie polynomials
PIV = [(0, 0, 0, 1), (0, 0, 1, 1), (0, 1, 1, 1)]     # monomials XXXY, XXYY, XYYY
def l4coords(poly):
    """coordinates of a degree-4 Lie polynomial in the basis L4VEC (exact, checked)."""
    M = [[L4VEC[j].get(m, 0) for j in range(3)] for m in PIV]
    assert M[0][1] == M[0][2] == M[1][2] == 0 and abs(M[0][0]) == abs(M[1][1]) == abs(M[2][2]) == 1
    c = [0, 0, 0]
    c[0] = poly.get(PIV[0], 0) * M[0][0]
    c[1] = (poly.get(PIV[1], 0) - M[1][0] * c[0]) * M[1][1]
    c[2] = (poly.get(PIV[2], 0) - M[2][0] * c[0] - M[2][1] * c[1]) * M[2][2]
    chk = {}
    for j in range(3):
        for m, v in L4VEC[j].items(): chk[m] = chk.get(m, 0) + c[j] * v
    assert {m: v for m, v in chk.items() if v} == poly, "not a Lie polynomial of degree 4"
    return c

PHI4 = [l4coords(part(mu(phi(w)), 4)) for w in L4]   # columns: phi on gamma_4/gamma_5
ELL = None
def _ell():
    """primitive integer row vector l with l*(I - PHI4) = 0."""
    global ELL
    M = [[(1 if i == j else 0) - PHI4[j][i] for j in range(3)] for i in range(3)]  # M[i][j]
    best = None
    for l in product(range(-3, 4), repeat=3):
        if any(l) and all(sum(l[i] * M[i][j] for i in range(3)) == 0 for j in range(3)):
            if best is None or sum(map(abs, l)) < sum(map(abs, best)): best = l
    assert best is not None
    ELL = best if [x for x in best if x][0] > 0 else tuple(-x for x in best)
    return M
MAT4 = _ell()

def invariant(u):
    """(kappa, J) of the phi-twisted class of u; also returns the conjugator v with
    v u phi(v)^-1 = z^kappa * w4 (mod gamma_5), w4 in gamma_4."""
    u = red(u); m1 = mu(u)
    i, j = m1.get((0,), 0), m1.get((1,), 0)
    v1 = power("a", -2 * i - j) + power("b", -i - j)          # (1-A) v = -ab(u)
    u1 = tw(v1, u); m = mu(u1)
    assert not part(m, 1)
    k = m.get((0, 1), 0); kap = k % 2
    v2 = power(Z, -(k // 2)); u2 = tw(v2, u1); m = mu(u2)
    zk = mu(power(Z, kap))
    assert part(m, 2) == part(zk, 2)
    d3 = sub(part(m, 3), part(zk, 3))
    al, be = -d3.get((0, 0, 1), 0), d3.get((0, 1, 1), 0)      # d3 = al[[X,Y],X]+be[[X,Y],Y]
    v3 = power(ZA, -be) + power(ZB, -al + be)
    u3 = tw(v3, u2); m = mu(u3)
    assert part(m, 3) == part(zk, 3), "degree-3 part not killed"
    c = l4coords(sub(part(m, 4), part(zk, 4)))
    return kap, sum(ELL[t] * c[t] for t in range(3)), red(v3 + v2 + v1)

def KJ(u):
    k, J, _ = invariant(u); return k, J
def killer(n): return power("a", n) + "BA"                    # k_n = (a^n B A, 1)
def theta(u):                                                 # theta0_*: (u,1) -> (iota(u) b, 1)
    return red(endo({"a": "A", "b": "B"}, u) + "b")

# ---- fast version: everything inside the truncated Magnus algebra (faithful on F/gamma_5)
def ser_inv(p):
    q = sub(ONE, p); r = ONE; t = ONE                 # 1/(1-q) = 1+q+q^2+...
    for _ in range(D):
        t = mul(t, q); r = sub(r, {m: -c for m, c in t.items()})
    return r
def ser_pow(p, n):
    if n < 0: p, n = ser_inv(p), -n
    r = ONE
    while n:
        if n & 1: r = mul(r, p)
        p = mul(p, p); n >>= 1
    return r
_SUB = [sub(mu(PHI["a"]), ONE), sub(mu(PHI["b"]), ONE)]     # images of X, Y under phi
def ser_phi(p):
    r = {}
    for m, c in p.items():
        t = {(): c}
        for i in m: t = mul(t, _SUB[i])
        for mm, cc in t.items(): r[mm] = r.get(mm, 0) + cc
    return {m: c for m, c in r.items() if c}
def tw_ser(v, u): return mul(mul(v, u), ser_inv(ser_phi(v)))
_MA, _MB, _MZ, _MZA, _MZB = mu("a"), mu("b"), mu(Z), mu(ZA), mu(ZB)
def KJ_ser(m):
    """(kappa, J) from the Magnus series m = mu(u)."""
    i, j = m.get((0,), 0), m.get((1,), 0)
    m = tw_ser(mul(ser_pow(_MA, -2 * i - j), ser_pow(_MB, -i - j)), m)
    assert not part(m, 1)
    k = m.get((0, 1), 0); kap = k % 2
    m = tw_ser(ser_pow(_MZ, -(k // 2)), m)
    zk = ser_pow(_MZ, kap)
    assert part(m, 2) == part(zk, 2)
    d3 = sub(part(m, 3), part(zk, 3))
    al, be = -d3.get((0, 0, 1), 0), d3.get((0, 1, 1), 0)
    m = tw_ser(mul(ser_pow(_MZA, -be), ser_pow(_MZB, -al + be)), m)
    assert part(m, 3) == part(zk, 3)
    c = l4coords(sub(part(m, 4), part(zk, 4)))
    return kap, sum(ELL[t] * c[t] for t in range(3))
def ser_killer(n): return mul(ser_pow(_MA, n), mu("BA"))
def ser_theta(m):                                    # mu(iota(u) b) from mu(u)
    r = {}
    inv_gen = [sub(mu("A"), ONE), sub(mu("B"), ONE)]
    for mm, c in m.items():
        t = {(): c}
        for i in mm: t = mul(t, inv_gen[i])
        for q, cc in t.items(): r[q] = r.get(q, 0) + cc
    return mul({q: c for q, c in r.items() if c}, _MB)

def selftest():
    rnd = random.Random(11)
    assert [sum(ELL[i] * MAT4[i][j] for i in range(3)) for j in range(3)] == [0, 0, 0]
    for _ in range(300):
        u = red("".join(rnd.choice("aAbB") for _ in range(rnd.randint(0, 14))))
        v = red("".join(rnd.choice("aAbB") for _ in range(rnd.randint(1, 8))))
        assert KJ(u) == KJ(tw(v, u)) == KJ(phi(u)), (u, v)
        k, J = KJ(u); k2, J2 = KJ(theta(u))
        assert k2 == 1 - k, "theta0 must flip kappa"
        assert KJ_ser(mu(u)) == (k, J) and KJ_ser(ser_theta(mu(u))) == (k2, J2)
        assert ser_phi(mu(u)) == mu(phi(u))
    print("PHI4 (columns) =", PHI4, " ELL =", ELL)
    print("th11_nil self-test passed: (kappa,J) invariant on 300 random twisted conjugations; theta0 flips kappa")

if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    else:
        for u in sys.argv[1:]: print(u, KJ(u))
