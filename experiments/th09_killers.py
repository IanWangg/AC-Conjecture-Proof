#!/usr/bin/env python3
"""TH09 (round 5): killers of one-relator groups.

Standard library only; imports g_torus / f_descent / elementary_verify read-only.

  python3 experiments/th09_killers.py --selftest          # all checks (about 1 min)
  python3 experiments/th09_killers.py --write certificates # MS(1,w) certificates
  python3 experiments/th09_killers.py --census 9           # killers of the trefoil group

Part 1  BS(1,2) = <x,y | x^-1 y x = y^2>: normal forms, and a compiler that turns
        "every element of x-degree -1 is conjugate to x^-1" into strict elementary
        AC moves (format ordinary-ac-elementary-v1).
Part 2  BS(1,2)-type words (Aut(F2)-images of XyxYY): the one-parameter families
        that kill the braid/trefoil group and the T(n,n+1) group, with the closed
        necklace formulas of research-th09 Prop. 5 and 6 checked by machine.
Part 3  Census of killers of the trefoil group by syllable necklace.
"""
import json
import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g_torus as G  # noqa: E402

R_BS = "XyxYY"  # x^-1 y x y^-2

# ----------------------------------------------------------------- Part 1


def bs_nf(w):
    """Normal form of w in BS(1,2) = Z[1/2] x| Z: returns (a, k), a in Z[1/2],
    k = x-degree; y -> (1,0), x -> (0,1); x^-1 y x = y^2, i.e. x acts on
    Z[1/2] by a -> a/2 (x a x^-1 = a/2)."""
    a, k = Fraction(0), 0
    for c in w:
        if c == "x":
            k += 1
        elif c == "X":
            k -= 1
        else:  # y^{+-1} sits at "height" k: x^k y x^-k = y^(2^-k)
            a += Fraction(1 if c == "y" else -1) * Fraction(2) ** (-k)
    return a, k


class Cert:
    """State (r0, r1) with recorded strict elementary moves."""

    def __init__(self, r0, r1):
        self.s = [G.red(r0), G.red(r1)]
        self.start = list(self.s)
        self.moves = []

    def conj(self, i, g):
        self.s[i] = G.red(g + self.s[i] + g.swapcase())
        self.moves.append({"op": "conjugate", "i": i, "g": g})

    def conj_word(self, i, h):  # r_i <- h r_i h^-1
        for g in reversed(h):
            self.conj(i, g)

    def inv(self, i):
        self.s[i] = G.inv(self.s[i])
        self.moves.append({"op": "invert", "i": i})

    def mul(self, i, j):
        self.s[i] = G.red(self.s[i] + self.s[j])
        self.moves.append({"op": "multiply", "i": i, "j": j})

    def mul_conj(self, i, j, h, e):
        """r_i <- r_i * (h r_j^e h^-1), r_j restored afterwards."""
        h = G.red(h)
        self.conj_word(j, h)
        if e < 0:
            self.inv(j)
        self.mul(i, j)
        if e < 0:
            self.inv(j)
        self.conj_word(j, G.inv(h))

    def json(self, target, description):
        assert self.s == list(target), (self.s, target)
        return {"format": "ordinary-ac-elementary-v1", "start": self.start,
                "target": list(target), "moves": self.moves, "description": description}


# rewriting rules alpha -> beta with alpha^-1 beta = h0 R^e h0^-1 (checked in selftest)
RULES = {"yx": ("xyy", "YY", -1), "Yx": ("xYY", "", 1),
         "Xy": ("yyX", "Yx", -1), "XY": ("YYX", "x", 1)}


def rule_step(C, i, j, pos):
    """Apply the rule at s[pos:pos+2] of relator i (frozen relator j = R_BS)."""
    s = C.s[i]
    al = s[pos:pos + 2]
    be, h0, e = RULES[al]
    A, B = s[:pos], s[pos + 2:]
    C.mul_conj(i, j, G.inv(B) + h0, e)
    assert C.s[i] == G.red(A + be + B), (C.s[i], A, be, B)


def bs_push(C, i, j, limit=20000):
    """Rewrite relator i to the form x^a y^b X^c using the rules (frozen j)."""
    for _ in range(limit):
        s = C.s[i]
        pos = next((p for p in range(len(s) - 1) if s[p:p + 2] in RULES), None)
        if pos is None:
            return
        rule_step(C, i, j, pos)
    raise RuntimeError("rewriting limit")


def bs12_trivialize(s, limit=20000):
    """Certificate (XyxYY, s) -> (x, y) for any s of x-degree +-1 (Theorem 1)."""
    C = Cert(R_BS, s)
    assert C.s[0] == R_BS
    if bs_nf(C.s[1])[1] == 1:
        C.inv(1)
    assert bs_nf(C.s[1])[1] == -1, "s must have x-exponent sum +-1"
    bs_push(C, 1, 0, limit)                       # s = x^a y^b X^(a+1)
    while C.s[1].startswith("x"):                 # conjugate to y^b X
        C.conj(1, "X")
    b = C.s[1].count("y") - C.s[1].count("Y")
    assert C.s[1] == G.red(G.power("y", b) + "X")
    for _ in range(abs(b)):                       # y^b (y^b X) y^-b, then push
        C.conj(1, "y" if b > 0 else "Y")
    bs_push(C, 1, 0, limit)
    assert C.s[1] == "X", C.s[1]
    # (XyxYY, X) -> (y, x) -> (x, y)
    C.inv(1); C.conj(0, "x"); C.mul(0, 1)         # r = yxYY
    C.conj(0, "Y"); C.inv(1); C.conj(0, "X"); C.mul(0, 1)   # r = Y
    C.inv(0); C.inv(1)
    assert C.s == ["y", "x"]
    C.mul(0, 1); C.inv(1); C.mul(1, 0); C.conj(1, "x"); C.inv(1)
    C.conj(0, "Y"); C.mul(0, 1); C.inv(1)
    return C.json(["x", "y"], "TH09 Theorem 1: (XyxYY, s) is AC-trivial; s is rewritten "
                  "to x^-1 inside BS(1,2) by explicit conjugates of the frozen relator")


# ----------------------------------------------------------------- Part 2

PHI = ("xY", "yyX")      # phi(xyxYXY) = xxYYY (research-g); AK coords -> trefoil coords


def bs_word(P, Q, d=1):
    """cyc(P^-d Q P^d Q^-2): the BS(1,2)-type word of the basis (P^d, Q)."""
    Pd = P if d > 0 else G.inv(P)
    return G.cyc(G.inv(Pd) + Q + Pd + G.inv(Q) + G.inv(Q))


def matrix_class(m, k, d):
    """Class of theta(XyxYY) for some theta with [theta(y)] = (m,k), det = d."""
    g, u, v = _egcd(k, -m)
    a, c = u * g * d, v * g * d
    assert a * k - c * m == d
    th = G.aut_from_matrix(((a, m), (c, k)))
    assert G.expvec(th[0]) == (a, c) and G.expvec(th[1]) == (m, k)
    return G.min_rot(G.cyc(G.apply(th, R_BS)))


def _egcd(a, b):
    if b == 0:
        return (abs(a), (1 if a >= 0 else -1), 0)
    g, u, v = _egcd(b, a % b)
    return (g, v, u - (a // b) * v)


def braid_family(j):
    """Explicit cyclic words v_j^+, v_j^- in AK coordinates (Prop. 5)."""
    if j >= 0:
        return "yxYX" + "yX" * j + "X", "YxyXX" + "yX" * j
    i = -j
    return "yxYY" + "xY" * (i - 1) + "X", "YxyXY" + "xY" * (i - 1)


def neck23(w_ak):
    """t-exponent necklace in C2*C3 of an AK-coordinate word (frozen b)."""
    z, nk = G.torus_class(G.apply(PHI, w_ak), 2, -3)
    return "".join(str(e) for g, e in nk if g == "y")


def canon_neck(s):
    """Necklace up to rotation, reversal and complement 1<->2."""
    comp = s.translate(str.maketrans("12", "21"))
    cands = []
    for t in (s, s[::-1], comp, comp[::-1]):
        cands += [t[i:] + t[:i] for i in range(len(t))]
    return min(cands)


def rot_min(s):
    return min(s[i:] + s[:i] for i in range(len(s)))


def alpha(j):
    return "112" + "21" * j


def beta(j):
    return "112" if j == 0 else "111" + "21" * (j - 1) + "22"


def check_braid_side(J=40):
    for j in range(-J, J + 1):
        P, Q = "xY", G.red(G.power("xY", j) + "x")
        vp, vm = braid_family(j)
        assert G.min_rot(vp) == G.min_rot(bs_word(P, Q, 1)), j
        assert G.min_rot(vm) == G.min_rot(bs_word(P, Q, -1)), j
        m, k = G.expvec(Q)
        assert (m, k) == (j + 1, -j)
        assert {G.min_rot(vp), G.min_rot(vm)} == {matrix_class(m, k, 1), matrix_class(m, k, -1)}, j
        assert len(vp) == len(vm) == len(G.cyc(Q)) + 4
        if j >= 0:
            exp = (alpha(j), beta(j))
        else:
            exp = (beta(-j - 1), alpha(-j - 1))
        assert rot_min(neck23(vp)) == rot_min(exp[0]), (j, neck23(vp), exp)
        assert rot_min(neck23(vm)) == rot_min(exp[1]), (j, neck23(vm), exp)
        # primitive killers themselves: necklace (21)^j 2 up to symmetry
        jj = j if j >= 0 else -j - 1
        assert canon_neck(neck23(Q)) == canon_neck("21" * jj + "2"), j
    # AK(n) partners: necklace 1^(n+1) 2^n up to symmetry; BS-type only for n <= 2
    bs = {canon_neck(alpha(j)) for j in range(J)} | {canon_neck(beta(j)) for j in range(J)}
    hits = []
    for n in range(1, J // 2):
        nk = neck23("x" * n + "Y" * (n + 1))
        assert canon_neck(nk) == canon_neck("1" * (n + 1) + "2" * n)
        if canon_neck(nk) in bs:
            hits.append(n)
    assert hits == [1, 2], hits
    return hits


def torus_family(n, j):
    """Explicit v_j^+, v_j^- for the frozen relator x^n Y^(n+1) (Prop. 6)."""
    u = "xY" * n + "Y"
    vp = G.cyc("yxYX" + G.power(u, -j) + "yX")
    vm = G.cyc("x" + "yX" * (n + 1) + G.power(u, 1 - j) + "yyXY")
    return vp, vm


def check_torus_side(nmax=9, J=12):
    out = {}
    for n in range(2, nmax + 1):
        p, q = n, -(n + 1)
        tb = {G.torus_class("xyxYXY", p, q), G.torus_class("YXYxyx"[::-1].swapcase(), p, q),
              G.torus_class(G.inv("xyxYXY"), p, q)}
        hit = []
        for j in range(-J, J + 1):
            m, k = 1 + j * n, -1 - j * (n + 1)
            vp, vm = torus_family(n, j)
            assert {G.min_rot(vp), G.min_rot(vm)} == {matrix_class(m, k, 1), matrix_class(m, k, -1)}, (n, j)
            for v in (vp, vm):
                L = G.syllables(v, p, q)
                assert L == (2 * n * j + 6 if j >= 0 else 2 * n * (-j) + 2), (n, j, L)
                if G.torus_class(v, p, q) in tb:
                    hit.append(j)
        out[n] = sorted(set(hit))
    assert out[2] and all(not out[n] for n in out if n >= 3), out
    return out


# ----------------------------------------------------------------- Part 3

def necklace_word(nk):
    """A word s in x,y with t-exponent necklace nk in C2*C3 (frozen xxYYY,
    z = x^2 = y^3) and abelianization +-1 (x -> 3, y -> 2); None if impossible."""
    k, S = len(nk), sum(int(c) for c in nk)
    base = 3 * k + 2 * S
    js = [(e - base) // 6 for e in (1, -1) if (e - base) % 6 == 0]
    if not js:
        return None
    j = js[0]                       # central exponent to distribute
    syl = []
    for c in nk:
        syl.append("x")
        syl.append("y" * int(c))
    for idx in range(len(syl)):     # y^2 = Y z, x = X z
        if j < 0 and syl[idx] == "yy":
            syl[idx] = "Y"; j += 1
    for idx in range(len(syl)):
        if j < 0 and syl[idx] == "x":
            syl[idx] = "X"; j += 1
    w = "".join(syl) + G.power("xx", j)
    a, b = G.expvec(w)
    assert abs(3 * a + 2 * b) == 1
    got = "".join(str(e) for g, e in G.torus_class(w, 2, -3)[1] if g == "y")
    assert rot_min(got) == rot_min(nk), (got, nk)
    return G.cyc(w)


def census(kmax=9, limit=400000):
    import f_descent as FD
    import f_thicken as FT
    rows = []
    for k in range(1, kmax + 1, 2):
        seen = set()
        for bits in range(2 ** k):
            nk = "".join("2" if bits >> i & 1 else "1" for i in range(k))
            c = canon_neck(nk)
            if c in seen:
                continue
            seen.add(c)
            w = necklace_word(c)
            if w is None:
                continue
            triv = FD.is_trivial_group(FT.parse("xxYYY"), FT.parse(w), limit)
            j = (k - 1) // 2
            tags = []
            if c == canon_neck("21" * j + "2"):
                tags.append("primitive")
            if k >= 3 and c in (canon_neck(alpha(j - 1)), canon_neck(beta(j - 1))):
                tags.append("BS(1,2)-type")
            if k >= 3 and c == canon_neck("1" * (j + 1) + "2" * j):
                tags.append("AK(%d)" % j)
            rows.append((k, c, w, triv, tags))
    return rows


def print_census(kmax):
    for k, c, w, triv, tags in census(kmax):
        st = {True: "killer", False: "not a killer", None: "undecided (coset limit)"}[triv]
        if triv:
            st += "; " + (", ".join(tags) if tags else "NO KNOWN EXIT")
        print("k=%d necklace %-13s s=%-28s %s" % (k, c, w, st))


def selftest():
    import elementary_verify as V
    for al, (be, h0, e) in RULES.items():       # rule identities in F2
        rel = R_BS if e > 0 else G.inv(R_BS)
        assert G.red(G.inv(al) + be) == G.red(h0 + rel + G.inv(h0)), al
    assert bs_nf(R_BS) == (0, 0)
    import random
    rng = random.Random(9)
    n = 0
    while n < 40:                               # Theorem 1 on random killers
        s = G.red("".join(rng.choice("xXyY") for _ in range(rng.randint(1, 9))))
        if abs(bs_nf(s)[1]) != 1:
            continue
        out = V.replay(json.loads(json.dumps(bs12_trivialize(s))))
        assert out["endpoint"] == ["x", "y"]
        n += 1
    hits = check_braid_side(40)
    tor = check_torus_side(9, 12)
    rows = census(7)
    kill = [(c, tags) for k, c, w, triv, tags in rows if triv]
    print("th09 self-test passed: 40 random BS(1,2) certificates replayed; "
          "braid-side BS exits for n in %s only (n < 20); torus-side hits %s; "
          "killers with k <= 7: %s" % (hits, tor, kill))


MS1_EXAMPLES = ["XyxyX", "XYxyyX", "XyXYxxYxYXX", "XXyxyyxYX", "XyyXYYxxyXYxX", "XYYxyXyx" + "X"]

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    elif "--census" in sys.argv:
        print_census(int(sys.argv[sys.argv.index("--census") + 1]))
    elif "--write" in sys.argv:
        d = sys.argv[sys.argv.index("--write") + 1]
        for n, s in enumerate(MS1_EXAMPLES, 1):
            c = bs12_trivialize(s)
            path = os.path.join(d, "th09_ms1_%d.json" % n)
            with open(path, "w") as f:
                json.dump(c, f)
            print(path, c["start"], len(c["moves"]))
