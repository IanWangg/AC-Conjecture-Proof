#!/usr/bin/env python3
"""th02_acm.py (agent TH02): exact frozen-relator (ACM) search for T(2,n)-type
partners, with unbounded conjugators.

A T(2,n)-type cyclic word is W(M,t) = theta_M(x Y^t x y^(t+1)), n = 2t+1, with
theta_M an automorphism of matrix M in GL2(Z) (columns = images of x, y).
For a frozen relator r = W(M0,t0) (so F/<<r>> is the torus-knot group
<u,v | u^2 v^n0>) and a partner s, W(M,t) is conjugate to s^{+-1} in F/<<r>>
iff the necklace/central-exponent invariants agree (research-g Lemma 1).  Then
(r, s) ~AC (r, W(M,t)) by one ACM move and the hidden reflection of W(M,t)
lies in the stabilizer of the class (Theorem TH02.1).

Usage: python3 experiments/th02_acm.py --self-test
       python3 experiments/th02_acm.py --explore [K J T DEPTH]
"""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from th02_hidden import red, inv, pw, subst, compose, matrix, mmul
from th02_scan import hidden_reflection, cycred, closure, D6, minv


def aut_from_matrix(M):
    (a, b), (c, d) = M
    assert a * d - b * c in (1, -1)
    steps = []
    while a != 0 and b != 0:
        if abs(a) >= abs(b):
            k = a // b if abs(a - (a // b) * b) < abs(b) else a // b + 1
            a, c = a - k * b, c - k * d
            steps.append({"x": red("x" + pw("y", k)), "y": "y"})
        else:
            k = b // a if abs(b - (b // a) * a) < abs(a) else b // a + 1
            b, d = b - k * a, d - k * c
            steps.append({"x": "x", "y": red("y" + pw("x", k))})
    if b == 0:
        th = {"x": red(pw("x", a) + pw("y", c)), "y": pw("y", d)}
    else:
        th = {"x": pw("y", c), "y": red(pw("x", b) + pw("y", d))}
    for g in reversed(steps):
        th = compose(th, g)
    assert matrix(th) == M, (matrix(th), M)
    return th


def aut_inverse(th):
    Mi = minv(matrix(th))
    cand = aut_from_matrix(Mi)                      # inverse up to an inner automorphism
    c = compose(cand, th)                           # = conjugation by some g
    # find g with c(x) = g x g^-1, c(y) = g y g^-1 and correct it
    from th02_hidden import conjugator
    g = conjugator("x", c["x"])
    for extra in range(-40, 41):
        h = red(g + pw("x", extra))
        if red(h + "y" + inv(h)) == c["y"]:
            out = {"x": red(inv(h) + cand["x"] + h), "y": red(inv(h) + cand["y"] + h)}
            assert compose(out, th) == {"x": "x", "y": "y"} and compose(th, out) == {"x": "x", "y": "y"}
            return out
    raise ValueError("inverse not found")


def torus_inv(word, p, q):
    """complete conjugacy invariant in <x,y | x^p y^q>: (necklace, central exponent)."""
    syl = []; c = 0
    for ch in red(word):
        t = ch.lower(); e = 1 if ch.islower() else -1
        if syl and syl[-1][0] == t:
            syl[-1][1] += e
        else:
            syl.append([t, e])
    def norm(s):
        nonlocal c
        t, e = s
        if t == "x":
            e0 = e % abs(p); c += (e - e0) // p
        else:
            e0 = e % abs(q); c -= (e - e0) // q
        return [t, e0]
    changed = True
    while changed:
        changed = False
        syl = [norm(s) for s in syl]
        out = []
        for s in syl:
            if s[1] == 0:
                changed = True; continue
            if out and out[-1][0] == s[0]:
                out[-1][1] += s[1]; changed = True
            else:
                out.append(s)
        syl = out
        if len(syl) >= 2 and syl[0][0] == syl[-1][0]:
            syl[0][1] += syl[-1][1]; syl.pop(); changed = True
    neck = [tuple(s) for s in syl]
    best = min(tuple(neck[k:] + neck[:k]) for k in range(max(1, len(neck))))
    return best, c


class Frozen:
    """frozen relator r = theta0(x Y^t0 x y^(t0+1)) -- group <u,v | u^2 v^n0>."""
    def __init__(self, M0, t0):
        self.M0, self.t0, self.n0 = M0, t0, 2 * t0 + 1
        self.th = aut_from_matrix(M0); self.thi = aut_inverse(self.th)
        self.word = cycred(subst("x" + "Y" * t0 + "x" + "y" * (t0 + 1), self.th))
        self.rho = (2 * M0[0][0] + M0[0][1], 2 * M0[1][0] + M0[1][1])

    def cls(self, w):
        # in (u,v) coordinates r = u v^-t u v^(t+1) ~ (u v^-t)^2 v^n: use basis (u v^-t, v)
        t = subst(w, self.thi)
        t = subst(t, {"x": "x" + "y" * self.t0, "y": "y"})      # u = u' v^t
        return torus_inv(t, 2, self.n0)


def tword(M, t):
    return cycred(subst("x" + "Y" * t + "x" + "y" * (t + 1), aut_from_matrix(M)))


def partners(fr, s, rho_s, K, J, T):
    """all T(2,n)-type words W(M,t) in the box that are conjugate to s^{+-1} mod <<fr.word>>."""
    want = {fr.cls(s), fr.cls(inv(s))}
    det = lambda a, b: a[0] * b[1] - a[1] * b[0]
    out = []
    for sg in (1, -1):
        for k in range(-K, K + 1):
            rho = (sg * rho_s[0] + k * fr.rho[0], sg * rho_s[1] + k * fr.rho[1])
            # primitive v with det(v, rho) = +-2 and v = rho mod 2: v = v0 + 2 j rho
            # v0 = 2*(a0,b0) + rho with det((a0,b0), rho) = 1 (extended Euclid)
            def egcd(m, n):
                if n == 0:
                    return (m, 1, 0)
                g, s1, t1 = egcd(n, m % n)
                return (g, t1, s1 - (m // n) * t1)
            g, s1, t1 = egcd(rho[1], rho[0])          # s1*rho[1] + t1*rho[0] = g = +-1
            if g not in (1, -1):
                continue
            a0, b0 = g * s1, -g * t1                   # a0*rho[1] - b0*rho[0] = 1
            v0 = (2 * a0 + rho[0], 2 * b0 + rho[1])
            assert det(v0, rho) == 2
            for j in range(-J, J + 1):
                v = (v0[0] + 2 * j * rho[0], v0[1] + 2 * j * rho[1])
                u = ((rho[0] - v[0]) // 2, (rho[1] - v[1]) // 2)
                M = ((u[0], v[0]), (u[1], v[1]))
                if det(u, v) not in (1, -1):
                    continue
                for t in range(1, T + 1):
                    w = tword(M, t)
                    if fr.cls(w) in want:
                        out.append((M, t, w))
    return out


def canon(w):
    w = cycred(w)
    return min(u[k:] + u[:k] for u in (w, inv(w)) for k in range(len(w)))


RMIN = ((-1, 0), (-1, 1))


def refl(M):
    return mmul(M, mmul(RMIN, minv(M)))


def explore(start, K, J, T, depth, group=None, verbose=True):
    """BFS over double-T(2,.) states: start = ((M1,t1),(M2,t2))."""
    key = lambda st: tuple(sorted(canon(tword(M, t)) for M, t in st))
    seen = {key(start): start}; frontier = [start]; refls = {}
    for d in range(depth + 1):
        nxt = []
        for st in frontier:
            for i in (0, 1):
                (M0, t0), (M1, t1) = st[i], st[1 - i]
                refls.setdefault(refl(M0), (tword(M0, t0), 2 * t0 + 1))
                if d == depth:
                    continue
                fr = Frozen(M0, t0)
                s = tword(M1, t1)
                rho_s = (2 * M1[0][0] + M1[0][1], 2 * M1[1][0] + M1[1][1])
                for (M, t, w) in partners(fr, s, rho_s, K, J, T):
                    new = ((M0, t0), (M, t))
                    k = key(new)
                    if k not in seen:
                        seen[k] = new; nxt.append(new)
                        if verbose:
                            print("depth %d: frozen %s, new partner %s (n=%d) reflection %s"
                                  % (d + 1, fr.word, w, 2 * t + 1, refl(M)))
        frontier = nxt
    G = closure(list(refls))
    if verbose:
        print("states %d, distinct hidden reflections %d, generated group order %s"
              % (len(seen), len(refls), len(G) if len(G) <= 2000 else "> 2000 (infinite)"))
        for R, (w, n) in refls.items():
            print("  ", R, "n=%d" % n, w, ("in group" if group is None or R in group else "NOT IN GROUP"))
    return seen, refls


MA = ((1, 1), (1, 0)); I2 = ((1, 0), (0, 1))


def self_test():
    import random
    rnd = random.Random(7)
    # aut_from_matrix / inverse
    for _ in range(200):
        M = I2
        for _ in range(rnd.randint(0, 8)):
            M = mmul(M, rnd.choice([((1, 0), (1, 1)), ((1, 1), (0, 1)), ((0, 1), (1, 0)), ((-1, 0), (0, 1))]))
        th = aut_from_matrix(M); aut_inverse(th)
    # torus_inv: invariance under conjugation and insertion of conjugates of the relator
    for _ in range(300):
        p, q = rnd.choice([(2, 5), (5, 2), (2, 3), (3, 4), (2, -7), (-3, 5)])
        R = pw("x", p) + pw("y", q)
        w = "".join(rnd.choice("xyXY") for _ in range(rnd.randint(1, 12)))
        g = "".join(rnd.choice("xyXY") for _ in range(rnd.randint(0, 6)))
        h = "".join(rnd.choice("xyXY") for _ in range(rnd.randint(0, 6)))
        k = rnd.randint(0, len(w))
        w2 = g + w[:k] + h + rnd.choice([R, inv(R)]) + inv(h) + w[k:] + inv(g)
        assert torus_inv(w, p, q) == torus_inv(w2, p, q)
        assert torus_inv(w, p, q) != torus_inv(w + pw("x", p), p, q)       # central twist changes the class
    # the words of C4
    assert canon(tword(MA, 2)) == canon("xxxxyXy") and canon(tword(I2, 2)) == canon("xyyyxYY")
    assert refl(MA) == ((1, -3), (0, -1)) and refl(I2) == ((-1, 0), (-1, 1))
    for _ in range(100):
        M = I2
        for _ in range(rnd.randint(0, 6)):
            M = mmul(M, rnd.choice([((1, 0), (1, 1)), ((1, 1), (0, 1)), ((0, 1), (1, 0)), ((-1, 0), (0, 1))]))
        t = rnd.randint(1, 5)
        assert hidden_reflection(tword(M, t)) == (refl(M), 2 * t + 1)
    # frozen A = x^4 y X y: x^8 y^5 ~ xY^2xy^3 (Lemma 3), and not ~ x^7 y^5 etc.
    fr = Frozen(MA, 2)
    assert fr.cls("xxxxxxxxyyyyy") == fr.cls("xYYxyyy")
    assert fr.cls("xxxxxxxyyyyy") != fr.cls("xYYxyyy")
    assert fr.cls(subst("xyyyxYY", {"x": "x", "y": "xYXXXX"})) == fr.cls("xyyyxYY")   # beta_A acts trivially
    fw = Frozen(I2, 2)
    assert fw.cls(subst("xxxxyXy", {"x": "yyXYYY", "y": "y"})) == fw.cls("xxxxyXy")   # beta_w acts trivially
    print("th02_acm self-test OK")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    elif "--explore" in sys.argv:
        a = [int(v) for v in sys.argv[2:]] + [3, 3, 4, 2][len(sys.argv) - 2:]
        explore(((MA, 2), (I2, 2)), a[0], a[1], a[2], a[3], group=D6)
    else:
        print(__doc__)
