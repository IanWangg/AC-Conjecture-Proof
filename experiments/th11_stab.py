#!/usr/bin/env python3
"""TH11: exact stabilizer in Out(F2) = GL2(Z) of a cyclic word (up to inversion), by Whitehead
peak reduction: if w is of minimal length in its Aut-orbit, every automorphism carrying the cyclic
word w to a cyclic word of the same length is a product of Whitehead automorphisms through cyclic
words of that same length (Whitehead 1936; Higgins-Lyndon 1974; recalled).  Modulo inner
automorphisms the Whitehead automorphisms of F(x,y) are the 8 signed permutations and
y->yx, y->yX, x->xy, x->xY.  We do a BFS over pairs (cyclic word, matrix).
Matrix convention: columns = exponent vectors of the images of x, y.
Usage: python3 experiments/th11_stab.py --selftest
"""
import sys

def red(w):
    out = []
    for ch in w:
        if out and out[-1] == ch.swapcase(): out.pop()
        else: out.append(ch)
    return "".join(out)
def inv(w): return w.swapcase()[::-1]
def cyc(w):
    w = red(w)
    while len(w) >= 2 and w[0] == w[-1].swapcase(): w = w[1:-1]
    return w
def canon(w):
    w = cyc(w)
    return min(w[i:] + w[:i] for i in range(len(w))) if w else w
def apply(img, w):
    return "".join(img[ch] if ch.islower() else inv(img[ch.lower()]) for ch in w)
def mat(img):
    def ev(u): return (u.count("x") - u.count("X"), u.count("y") - u.count("Y"))
    (a, c), (b, d) = ev(img["x"]), ev(img["y"])
    return ((a, b), (c, d))
def mmul(M, N):
    return tuple(tuple(sum(M[i][k] * N[k][j] for k in range(2)) for j in range(2)) for i in range(2))

GENS = []
for px, py in (("x", "y"), ("y", "x")):
    for sx in (1, -1):
        for sy in (1, -1):
            GENS.append({"x": px if sx > 0 else px.upper(), "y": py if sy > 0 else py.upper()})
GENS += [{"x": "x", "y": "yx"}, {"x": "x", "y": "yX"}, {"x": "xy", "y": "y"}, {"x": "xY", "y": "y"}]
I2 = ((1, 0), (0, 1))

def minimize(w):
    """greedy Whitehead reduction: (minimal cyclic word w', matrix N) with w' = theta_N(w)."""
    u, N = canon(w), I2
    while True:
        for g in GENS:
            v = canon(apply(g, u))
            if len(v) < len(u):
                u, N = v, mmul(mat(g), N); break
        else:
            return u, N
def minv(M):
    (a, b), (c, d) = M; e = a * d - b * c
    assert e in (1, -1)
    return ((d * e, -b * e), (-c * e, a * e))

def stabilizer(w, cap=200000):
    """returns (set of matrices M with theta_M(w) ~ w, set with theta_M(w) ~ w^-1, #minimal words)."""
    w0, N = minimize(w); L = len(w0); Ni = minv(N)
    seen = {(w0, I2)}; todo = [(w0, I2)]
    while todo:
        u, M = todo.pop()
        for g in GENS:
            v = canon(apply(g, u))
            assert len(v) >= L, "minimal word was not minimal"
            if len(v) == L:
                st = (v, mmul(mat(g), M))
                if st not in seen:
                    seen.add(st); todo.append(st)
                    assert len(seen) < cap, "stabilizer looks infinite"
    back = lambda M: mmul(Ni, mmul(M, N))
    plus = {back(M) for (u, M) in seen if u == w0}
    minus = {back(M) for (u, M) in seen if u == canon(inv(w0))}
    return plus, minus, len({u for u, _ in seen})

def show(name, w):
    p, m, k = stabilizer(w)
    print(f"{name:8s} {w:22s} Stab(w) = {sorted(p)}  to w^-1: {sorted(m)}  minimal words in orbit: {k}")
    return p, m

def selftest():
    c, b = "xyxYYXy", "xyxYXY"
    th0 = ((-1, 1), (0, 1)); sw = ((0, 1), (1, 0)); mI = ((-1, 0), (0, -1)); msw = ((0, -1), (-1, 0))
    p, m = show("c", c); assert p == {I2} and m == {th0}
    p, m = show("b", b); assert p == {I2, msw} and m == {mI, sw}
    show("p_2", "xxYYY")
    for n in range(3, 13):
        w = "x" * n + "Y" * (n + 1)
        p, m, k = stabilizer(w)
        assert p == {I2} and m == {mI} and k == 8, n
        for g in GENS[8:]:          # all four type-II maps strictly lengthen p_n (n >= 3)
            assert len(canon(apply(g, w))) > len(w)
    print("p_n = x^n Y^(n+1), n = 3..12: Stab(p_n) = {I}, to p_n^-1: {-I}, 8 minimal words")
    for n in range(2, 7):
        show(f"k_{n}", "x" * n + "YXyy")
    assert cyc(apply({"x": "X", "y": "yx"}, c)) in [inv(c)[i:] + inv(c)[:i] for i in range(7)]
    print("th11_stab self-test passed")

if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    else:
        for w in sys.argv[1:]: show("word", w)
