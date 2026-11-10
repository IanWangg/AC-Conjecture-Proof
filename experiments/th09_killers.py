#!/usr/bin/env python3
"""TH09 (round 5): killers of one-relator groups.

Standard library only; imports g_torus / f_descent / elementary_verify read-only.

  python3 experiments/th09_killers.py --selftest          # all checks (about 1 min)
  python3 experiments/th09_killers.py --write certificates # MS(1,w) certificates
  python3 experiments/th09_killers.py --census 9           # killers of the trefoil group
  python3 experiments/th09_killers.py --exchange 12 9 160  # exchange graph (bounded)
  python3 experiments/th09_killers.py --forward 20         # AK(3) forward set, BS(1,2) test
  python3 experiments/th09_killers.py --gsieve             # Theorem 6, full sieve (about 80 s)
  python3 experiments/th09_killers.py --identify           # necklaces of AK(n), C3, C6, X7, BS7, R249

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


class _Ops:
    def conj_word(self, i, h):  # r_i <- h r_i h^-1
        for g in reversed(h):
            self.conj(i, g)

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


class ViewState(_Ops):
    """The same primitives in theta-coordinates on top of a g_cert.View."""

    def __init__(self, view):
        self.v = view

    @property
    def s(self):
        return self.v.U

    def conj(self, i, g):
        self.v.conj_word(i, g)

    def inv(self, i):
        self.v.invert(i)

    def mul(self, i, j):
        assert j == 1 - i
        self.v.multiply(i)


class Cert(_Ops):
    """State (r0, r1) with recorded strict elementary moves."""

    def __init__(self, r0, r1):
        self.s = [G.red(r0), G.red(r1)]
        self.start = list(self.s)
        self.moves = []

    def conj(self, i, g):
        self.s[i] = G.red(g + self.s[i] + g.swapcase())
        self.moves.append({"op": "conjugate", "i": i, "g": g})

    def inv(self, i):
        self.s[i] = G.inv(self.s[i])
        self.moves.append({"op": "invert", "i": i})

    def mul(self, i, j):
        self.s[i] = G.red(self.s[i] + self.s[j])
        self.moves.append({"op": "multiply", "i": i, "j": j})

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


MAXLEN = [10 ** 6]


def bs_push(C, i, j, limit=20000):
    """Rewrite relator i to the form x^a y^b X^c using the rules (frozen j)."""
    for _ in range(limit):
        s = C.s[i]
        if len(s) > MAXLEN[0]:
            raise RuntimeError("length guard")
        pos = next((p for p in range(len(s) - 1) if s[p:p + 2] in RULES), None)
        if pos is None:
            return
        rule_step(C, i, j, pos)
    raise RuntimeError("rewriting limit")


def bs12_trivialize(s, limit=20000):
    """Certificate (XyxYY, s) -> (x, y) for any s of x-degree +-1 (Theorem 1)."""
    C = Cert(R_BS, s)
    _bs12_core(C, limit)
    return C.json(["x", "y"], "TH09 Theorem 1: (XyxYY, s) is AC-trivial; s is rewritten "
                  "to x^-1 inside BS(1,2) by explicit conjugates of the frozen relator")


def _bs12_core(C, limit=20000):
    """C.s[0] == XyxYY exactly, C.s[1] of x-degree +-1; ends with C.s == [x, y]."""
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
    assert list(C.s) == ["y", "x"]
    C.mul(0, 1); C.inv(1); C.mul(1, 0); C.conj(1, "x"); C.inv(1)
    C.conj(0, "Y"); C.mul(0, 1); C.inv(1)
    assert list(C.s) == ["x", "y"]


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
            u = "xY" * n + "Y"                 # the form of v_j^- printed in the note
            assert G.min_rot(G.cyc("Yx" + "yX" * (n + 1) + G.power(u, -j) + "xY" * (n - 1))) == G.min_rot(vm)
            assert G.min_rot(vp) == G.min_rot(bs_word(u, G.red("xY" + G.power(u, j)), 1))
            assert G.min_rot(vm) == G.min_rot(bs_word(u, G.red("xY" + G.power(u, j)), -1))
            assert {G.min_rot(vp), G.min_rot(vm)} == {matrix_class(m, k, 1), matrix_class(m, k, -1)}, (n, j)
            for v in (vp, vm):
                L = G.syllables(v, p, q)
                assert L == (2 * n * j + 6 if j >= 0 else 2 * n * (-j) + 2), (n, j, L)
                if G.torus_class(v, p, q) in tb:
                    hit.append(j)
        out[n] = sorted(set(hit))
    assert out[2] and all(not out[n] for n in out if n >= 3), out
    return out


def check_gieseking(ns=range(1, 9), p=13):
    """Theorem 6: traces (up to sign, mod 13) of rho(v^2), rho(y v^2 Y) for the
    BS(1,2)-type killers v_j^+- of G_c against those of k_n, with O's witness
    hom rho: H -> PSL(2,13) (H = even-degree subgroup of G_c, t = y^2)."""
    import o_gc as O

    def mm(A, B):
        return (((A[0][0] * B[0][0] + A[0][1] * B[1][0]) % p, (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % p),
                ((A[1][0] * B[0][0] + A[1][1] * B[1][0]) % p, (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % p))

    def mi(A):
        return ((A[1][1], -A[0][1] % p), (-A[1][0] % p, A[0][0]))

    def neg(A):
        return tuple(tuple((-e) % p for e in r) for r in A)

    RA, RB, RT = ((0, 2), (6, 8)), ((1, 11), (6, 2)), ((0, 1), (12, 5))
    M = {"a": RA, "A": mi(RA), "b": RB, "B": mi(RB)}
    I2 = ((1, 0), (0, 1))

    def ev(u):
        R = I2
        for ch in u:
            R = mm(R, M[ch])
        return R

    for X in (RA, RB, RT):
        assert (X[0][0] * X[1][1] - X[0][1] * X[1][0]) % p == 1
    for lhs, rhs in ((mm(mm(RT, RA), mi(RT)), ev("Ba")), (mm(mm(RT, RB), mi(RT)), ev("Abb"))):
        assert lhs in (rhs, neg(rhs))          # t a T = b^-1 a, t b T = a^-1 b^2
    for X in (RA, RB):                          # order 7 in PSL(2,13)
        Y = I2
        for _ in range(7):
            Y = mm(Y, X)
        assert Y in (I2, neg(I2))
    assert O.nf("xyxYYXy") == ("", 0)

    def traces(w):
        out = set()
        for g in (w + w, "y" + w + w + "Y"):
            u, k = O.nf(g)
            assert k % 2 == 0
            R = ev(u)
            T = RT if k > 0 else mi(RT)
            for _ in range(abs(k) // 2):
                R = mm(R, T)
            tr = (R[0][0] + R[1][1]) % p
            out.add(min(tr, (-tr) % p))
        return out

    def fam(j):
        Xj = G.power("X", j)
        return "yxY" + Xj + "YX", "xyXY" + Xj + "Y"

    for j in range(-6, 7):                      # the words are v(x^+-1, x^j y)
        Q = G.red(G.power("x", j) + "y")
        vp, vm = fam(j)
        assert G.min_rot(G.cyc(vp)) == G.min_rot(bs_word("x", Q, 1))
        assert G.min_rot(G.cyc(vm)) == G.min_rot(bs_word("x", Q, -1))
    cand = [(traces(fam(j)[0]), traces(fam(j)[1])) for j in range(7)]
    for j in range(-21, 22):
        assert (traces(fam(j)[0]), traces(fam(j)[1])) == cand[j % 7]
    allc = set().union(*[a | b for a, b in cand])
    res = {n: sorted(traces(O.killer(n))) for n in ns}
    excluded = [n for n in ns if not (set(res[n]) & allc)]
    return cand, res, excluded


def gieseking_sieve(ns=range(1, 9), primes=(7, 13)):
    """Theorem 6, full sieve: all homs H -> PSL(2,p) (o_sieve.homs_H) with
    non-abelian fibre image; residues j mod the period for which the trace of
    rho(k_n^2) is among those of rho(v^2), rho(y v^2 Y), v = v_j^+ (sign 0) or
    v_j^- (sign 1); CRT intersection (o_sieve.combine).  Returns
    {n: (survivors for +, survivors for -)}; both empty = exclusion."""
    import o_sieve as S
    import o_gc as O

    def fam(j):
        Xj = G.power("X", j)
        return "yxY" + Xj + "YX", "xyXY" + Xj + "Y"

    def hword(w):
        u, k = O.nf(w)
        assert k % 2 == 0
        return u + ("t" if k > 0 else "T") * (abs(k) // 2)

    allc = []
    for p in primes:
        cons = {(n, sg): {} for n in ns for sg in (0, 1)}
        for (A, B, T) in S.homs_H(p):
            if S.is_pm_I(S.mmul(S.mmul(A, B, p), S.mmul(S.minv(A, p), S.minv(B, p), p), p), p):
                continue
            o = S.lcm(S.psl_order(A, p), S.psl_order(B, p), S.psl_order(S.mmul(S.minv(B, p), A, p), p))
            cand = [[None] * o, [None] * o]
            for j in range(o):
                for sg, v in enumerate(fam(j)):
                    cand[sg][j] = {S.tr(S.evab(hword(v + v), A, B, T, p), p),
                                   S.tr(S.evab(hword("y" + v + v + "Y"), A, B, T, p), p)}
            for n in ns:
                t = S.tr(S.evab(S.sq_word(n), A, B, T, p), p)
                for sg in (0, 1):
                    arr = cons[(n, sg)].setdefault(o, bytearray(b"\x01") * o)
                    for j in range(o):
                        if t not in cand[sg][j]:
                            arr[j] = 0
        allc.append(cons)
    out = {}
    for n in ns:
        out[n] = tuple(S.combine([c[(n, sg)] for c in allc]) for sg in (0, 1))
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


# ------------------------------------------------- exchange exit (Lemma 2.2(ii))

def exchange_neighbours(w, K=6, maxlen=90):
    """Necklaces N' such that some trefoil-type word v (|matrix| <= K, length <=
    maxlen) is conjugate to w^{+-1} in <x,y | xxYYY> and xxYYY has necklace N'
    in G_v.  Bounded enumeration (g_torus.edges)."""
    import g_cert as GC
    nb = set()
    for (M2, a, b, v) in G.edges(w, 2, -3, G.gl2_matrices(K), P=3, maxlen=maxlen):
        if {abs(a), abs(b)} != {2, 3}:
            continue
        U1 = G.cyc(G.apply(GC.exact_inverse(G.aut_cached(M2)), "xxYYY"))
        g3 = "y" if abs(b) == 3 else "x"
        nb.add(canon_neck("".join(str(e) for g, e in G.torus_class(U1, a, b)[1] if g == g3)))
    return sorted(nb, key=lambda t: (len(t), t))


def two_step_certificate(r0, r1, K=6, P=14, maxlen=70):
    """(r0, r1) with r1 of torus type.  Move r0 (r1 frozen) to a torus-type word
    v such that r1 is conjugate in G_v to a primitive word; move r1 to it (v
    frozen); finish.  Returns a strict certificate (r0, r1) -> (x, y) or None."""
    import g_cert as GC
    cert = GC.Cert(r0, r1)
    M, p, q = G.torus_type(r1)
    theta = G.aut_cached(M)
    U0 = G.cyc(G.apply(GC.exact_inverse(theta), r0))
    for (M2, a, b, v) in G.edges(U0, p, q, G.gl2_matrices(K), P=P, maxlen=maxlen):
        if abs(a) < 2 or abs(b) < 2:
            continue
        th2 = GC.compose(theta, G.aut_cached(M2))
        U1 = G.cyc(G.apply(GC.exact_inverse(th2), r1))
        prims = G.primitive_complete(U1, a, b)
        if not prims:
            continue
        GC.acm_edge(cert, 0, theta, p, q, v)
        mid = list(cert.s)
        GC.acm_edge(cert, 1, th2, a, b, prims[0][-1])
        GC.finish_primitive(cert, 1, th2)
        return {"format": "ordinary-ac-elementary-v1", "start": [G.red(r0), G.red(r1)],
                "target": ["x", "y"], "moves": cert.moves,
                "description": "TH09 exchange exit: relator 0 moved (relator 1 frozen) to the torus-type "
                               "word %s of type (%d,%d); then relator 1 moved to a primitive word "
                               "(%s in adapted coordinates); primitive finish" % (mid[0], a, b, prims[0][-1])}
    return None


def bs_trial_cost(sprime, limit=250, maxlen=120):
    """Number of moves of Theorem 1's compiler on (XyxYY, sprime), or None."""
    MAXLEN[0] = maxlen
    try:
        C = Cert(R_BS, sprime)
        _bs12_core(C, limit)
        return len(C.moves)
    except (RuntimeError, AssertionError):
        return None
    finally:
        MAXLEN[0] = 10 ** 6


def bs_exit_certificate(r0, r1, mmax=6, swap_first=False):
    """(r0, r1) with r1 of torus type x^p y^q (up to Aut).  If r0 is conjugate
    modulo r1 to a BS(1,2)-type word v = P^-1 Q P Q^-2, move r0 to v (r1 frozen),
    apply Theorem 1 in the coordinates (P, Q), Nielsen-finish.  Among the
    BS(1,2)-type words found (|m| <= mmax) and the complements P Q^i (|i| <= 3)
    the cheapest one (trial run of the Theorem 1 compiler) is used.  Returns a
    strict certificate to (x, y) or None.  With swap_first the certificate
    starts at (r1, r0) and begins with the AC swap."""
    import g_cert as GC
    if swap_first:
        cert = GC.Cert(r1, r0)
        GC.swap(cert)
    else:
        cert = GC.Cert(r0, r1)
    start = list(cert.start)
    M, p, q = G.torus_type(r1)
    theta = G.aut_cached(M)
    R = G.red(G.power("x", p) + G.power("y", q))
    U0 = G.cyc(G.apply(GC.exact_inverse(theta), r0))
    tc = {G.torus_class(U0, p, q), G.torus_class(G.inv(U0), p, q)}
    best = None
    for m in range(-mmax, mmax + 1):
        for k in range(-8 * mmax, 8 * mmax + 1):
            if math.gcd(m, k) != 1 or abs(q * m - p * k) != 1:
                continue
            for d in (1, -1):
                g, u, v = _egcd(k, -m)
                th0 = G.aut_from_matrix(((u * g * d, m), (v * g * d, k)))
                if G.torus_class(G.cyc(G.apply(th0, R_BS)), p, q) not in tc:
                    continue
                for i in range(-3, 4):
                    th = (G.red(th0[0] + G.power(th0[1], i)), th0[1])
                    for Rv in (R, G.inv(R)):
                        cost = bs_trial_cost(G.apply(GC.exact_inverse(th), Rv))
                        if cost is not None and (best is None or cost < best[0]):
                            best = (cost, th)
    if best is None:
        return None
    th = best[1]
    w = G.cyc(G.apply(th, R_BS))
    GC.acm_edge(cert, 0, theta, p, q, w)
    mid = list(cert.s)
    eta = GC.compose(theta, th)
    view = GC.View(cert, eta, GC.exact_inverse(eta))
    h, eps = GC.conj_rep(view.U[0], R_BS)
    if eps < 0:
        view.invert(0)
        h, eps = GC.conj_rep(view.U[0], R_BS)
    view.conj_word(0, G.inv(h))
    assert view.U[0] == R_BS
    _bs12_core(ViewState(view))
    view.check()
    GC.nielsen_finish(cert)
    return {"format": "ordinary-ac-elementary-v1", "start": start, "target": ["x", "y"],
            "moves": cert.moves,
            "description": "TH09 BS(1,2) exit: relator 0 moved (relator 1 frozen) to the BS(1,2)-type "
                           "word %s = P^-1 Q P Q^-2 with (P, Q) = %s; then Theorem 1 in the "
                           "coordinates (P, Q); Nielsen finish" % (mid[0], eta)}


def transport_certificate(r0, r1, base_cert):
    """(r0, r1) with r1 trefoil-type (torus type in general); base_cert a strict
    certificate (a, b) -> (x, y) with b of the same torus type.  If r0 and a lie
    in the same killer class up to the symmetries of Corollary 8.1, i.e. if for
    some alpha in Aut(F) alpha(b) ~ r1^{+-1} and alpha(a) ~ r0^{+-1} modulo r1,
    return a strict certificate (r0, r1) -> (x, y): one generalized move
    r0 -> alpha(a) (r1 frozen), the base certificate transported by alpha
    (Lemma D2), Nielsen finish.  Otherwise None."""
    import g_cert as GC
    a, b = base_cert["start"]
    MR, pR, qR = G.torus_type(r1)
    MB, pB, qB = G.torus_type(b)
    thR, thB = G.aut_cached(MR), G.aut_cached(MB)
    thBi = GC.exact_inverse(thB)
    RR = G.red(G.power("x", pR) + G.power("y", qR))
    RB = G.red(G.power("x", pB) + G.power("y", qB))
    U0 = G.cyc(G.apply(GC.exact_inverse(thR), r0))
    tc = {G.torus_class(U0, pR, qR), G.torus_class(G.inv(U0), pR, qR)}
    for sw in (False, True):
        for sx in ("x", "X"):
            for sy in ("y", "Y"):
                sig = (sy, sx) if sw else (sx, sy)
                if G.cyc_canon(G.apply(sig, RB)) != G.cyc_canon(RR):
                    continue
                tw = G.apply(sig, G.apply(thBi, a))
                if G.torus_class(tw, pR, qR) not in tc:
                    continue
                alpha = GC.compose(thR, GC.compose(sig, thBi))
                cert = GC.Cert(r0, r1)
                GC.acm_edge(cert, 0, thR, pR, qR, tw)
                assert cert.s[0] == G.apply(alpha, a)
                T1 = G.apply(alpha, b)
                h, eps = GC.conj_rep(cert.s[1], T1)
                if eps < 0:
                    cert.invert(1)
                    h, eps = GC.conj_rep(cert.s[1], T1)
                cert.conj_word(1, G.inv(h))
                assert cert.s == [G.apply(alpha, a), T1]
                img = {"x": alpha[0], "X": G.inv(alpha[0]), "y": alpha[1], "Y": G.inv(alpha[1])}
                st = [a, b]                       # shadow state in base coordinates
                for mv in base_cert["moves"]:
                    i = mv["i"]
                    if mv["op"] == "invert":
                        cert.invert(i); st[i] = G.inv(st[i])
                    elif mv["op"] == "multiply":
                        cert.multiply(i); st[i] = G.red(st[i] + st[1 - i])
                    else:
                        cert.conj_word(i, img[mv["g"]])
                        st[i] = G.red(mv["g"] + st[i] + mv["g"].swapcase())
                    assert cert.s[i] == G.apply(alpha, st[i])
                assert st == ["x", "y"]
                GC.nielsen_finish(cert)
                return {"format": "ordinary-ac-elementary-v1", "start": [G.red(r0), G.red(r1)],
                        "target": ["x", "y"], "moves": cert.moves,
                        "description": "TH09: one generalized move to alpha(%s, %s), alpha = %s, then the "
                                       "transported base certificate and a Nielsen finish" % (a, b, alpha)}
    return None


def frozen_path_certificate(a, s1, s2, maxlen=16, depth=3):
    """Strict certificate (a, s1) -> (a, s2) by at most `depth` cyclic products
    of the second relator with rotations of a^{+-1} (breadth-first), or None."""
    import g_cert as GC

    def rots(w):
        return [w[i:] + w[:i] for i in range(len(w))]

    par = {G.cyc_canon(s1): None}
    front = [G.cyc(s1)]
    for _ in range(depth):
        nxt = []
        for w in front:
            for u in rots(w) + rots(G.inv(w)):
                for v in rots(a) + rots(G.inv(a)):
                    c = G.cyc(u + v)
                    k = G.cyc_canon(c)
                    if c and len(c) <= maxlen and k not in par:
                        par[k] = (w, u, v, c)
                        nxt.append(c)
        front = nxt
        if G.cyc_canon(s2) in par:
            break
    if G.cyc_canon(s2) not in par:
        return None
    steps, k = [], G.cyc_canon(s2)
    while par[k] is not None:
        steps.append(par[k])
        k = G.cyc_canon(par[k][0])
    cert = GC.Cert(a, s1)

    def set_to(i, target):          # relator i -> exactly `target` (a rotation of it or its inverse)
        if G.min_rot(cert.s[i]) != G.min_rot(target):
            cert.invert(i)
        cert.rotate_to(i, target)

    for (w, u, v, c) in reversed(steps):
        set_to(1, u)
        set_to(0, v)
        cert.multiply(1)
        cert.cyclically_reduce(1)
        assert cert.s[1] == c
    set_to(0, a)
    set_to(1, s2)
    return {"format": "ordinary-ac-elementary-v1", "start": [a, s1], "target": [a, s2],
            "moves": cert.moves,
            "description": "TH09: %d cyclic products with the first relator frozen" % len(steps)}


def forward_bs_scan(cap, tlim=250.0, start=("xxxYYYY", "xyxYXY")):
    """Breadth-first forward set of `start` under cyclic products (u, v) ->
    (cyc(rot(u) rot(v^{+-1})), v) with total length <= cap; every relator met
    is tested for primitivity and for BS(1,2)-type (Corollary 1.2)."""
    import time
    import d_whitehead as W
    BS = W.aut_canon((R_BS,))
    st0 = tuple(sorted(W.canon_word(w) for w in start))
    seen, front, rels, hits, t0, done = {st0}, [st0], {}, [], time.time(), True
    while front and done:
        nxt = []
        for st in front:
            if time.time() - t0 > tlim:
                done = False
                break
            for i in (0, 1):
                u, v = st[i], st[1 - i]
                vi = G.inv(v)
                for V in [v[k:] + v[:k] for k in range(len(v))] + [vi[k:] + vi[:k] for k in range(len(v))]:
                    for k in range(len(u)):
                        c = G.cyc(u[k:] + u[:k] + V)
                        if not c or len(c) + len(v) > cap:
                            continue
                        cw = W.canon_word(c)
                        ns = tuple(sorted((cw, v)))
                        if ns in seen:
                            continue
                        seen.add(ns)
                        nxt.append(ns)
                        if cw not in rels:
                            L, cf = W.aut_canon((cw,))
                            rels[cw] = "primitive" if L == 1 else ("BS(1,2)-type" if (L, cf) == BS else "")
                        if rels[cw]:
                            hits.append((rels[cw], ns))
        front = nxt
    return {"cap": cap, "complete": done, "states": len(seen), "relators": len(rels), "hits": hits[:5]}


def partner_necklaces(pair):
    """[(i, necklace)]: relator i of the pair is trefoil-type and the other
    relator has this necklace (up to rotation/reversal/complement) in its group."""
    import g_cert as GC
    import d_whitehead as W
    tref = W.aut_canon(("xxYYY",))
    out = []
    for i in (0, 1):
        r, s = pair[i], pair[1 - i]
        if W.aut_canon((r,)) != tref:
            continue
        M, p, q = G.torus_type(r)
        U = G.cyc(G.apply(GC.exact_inverse(G.aut_cached(M)), s))
        g3 = "y" if abs(q) == 3 else "x"
        out.append((i, canon_neck("".join(str(e) for g, e in G.torus_class(U, p, q)[1] if g == g3))))
    return out


KNOWN = {"AK(2)": ("xxYYY", "xyxYXY"), "AK(3)": ("xxxYYYY", "xyxYXY"), "AK(4)": ("xxxxYYYYY", "xyxYXY"),
         "C3": ("xxyXy", "xyyyyyxYY"), "C6": ("xxyxxYY", "xyXYYXy"), "C4": ("xxxxyXy", "xyyyxYY")}


X7 = ("XXXYXXYxxy", "XYYXy")     # killer class 1121122 of the trefoil group
BS7 = ("XXXXYXYxxy", "XYYXy")    # killer class 1112122 (BS(1,2)-type)
R249 = ("xxyXXYY", "xyXyxyyyy")  # row of the third-party residual list, label R249; class 1112122
R249_SEED = "xxxyyXyXy"          # (xxyXXYY, xxxyyXyXy) is the list's seed for R249


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
    cand, res, excl = check_gieseking()
    assert excl == [3, 4], excl
    rows = census(7)
    kill = [(c, tags) for k, c, w, triv, tags in rows if triv]
    assert [c for c, _ in kill] == ["1", "112", "11122", "11212", "1111112", "1111222",
                                    "1112122", "1121122", "1121212"], kill
    print("th09 self-test passed: 40 random BS(1,2) certificates replayed; "
          "braid-side BS exits for n in %s only (n < 20); torus-side hits (n: j) %s; "
          "Gieseking side: candidate traces %s, k_n traces %s, excluded n = %s; "
          "killers with k <= 7: %s" % (hits, tor, cand, res, excl, kill))


MS1_EXAMPLES = ["XyxyX", "XYxyyX", "XyXYxxYxYXX", "XXyxyyxYX", "XyyXYYxxyXYxX", "XYYxyXyx" + "X"]

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    elif "--census" in sys.argv:
        print_census(int(sys.argv[sys.argv.index("--census") + 1]))
    elif "--identify" in sys.argv:
        for name, pair in list(KNOWN.items()) + [("X7", X7), ("BS7", BS7), ("R249", R249)]:
            print(name, pair, partner_necklaces(pair))
    elif "--gsieve" in sys.argv:
        for n, (plus, minus) in gieseking_sieve().items():
            print("n=%d modulus %d survivors +: %s  -: %s  %s" % (n, plus[0], plus[1][:6], minus[1][:6],
                  "EXCLUDED" if not plus[1] and not minus[1] else ""))
    elif "--forward" in sys.argv:
        print(forward_bs_scan(int(sys.argv[sys.argv.index("--forward") + 1])))
    elif "--exchange" in sys.argv:
        i = sys.argv.index("--exchange")
        K, kmax, ml = int(sys.argv[i + 1]), int(sys.argv[i + 2]), int(sys.argv[i + 3])
        for k, c, w, triv, tags in census(kmax):
            if triv:
                print(k, c, tags, "trefoil-exchange neighbours:", exchange_neighbours(w, K, ml), flush=True)
    elif "--write" in sys.argv:
        d = sys.argv[sys.argv.index("--write") + 1]
        c = two_step_certificate(*X7)
        with open(os.path.join(d, "th09_x7_trivialization.json"), "w") as f:
            json.dump(c, f)
        print("th09_x7_trivialization.json", c["start"], len(c["moves"]))
        c = two_step_certificate(necklace_word("112121122"), "xxYYY", K=12, P=3, maxlen=160)
        with open(os.path.join(d, "th09_k9_112121122_trivialization.json"), "w") as f:
            json.dump(c, f)
        print("th09_k9_112121122_trivialization.json", c["start"], len(c["moves"]))
        bs7 = bs_exit_certificate(*BS7)
        ak2 = bs_exit_certificate("xxYYY", "xyxYXY")
        r249 = transport_certificate(R249[0], R249[1], bs7)
        seed = frozen_path_certificate(R249[0], R249_SEED, R249[1])
        for name, c in (("th09_bs7_bs_exit", bs7), ("th09_ak2_bs_exit", ak2),
                        ("th09_r249_trivialization", r249), ("th09_r249_seed_to_member", seed)):
            with open(os.path.join(d, name + ".json"), "w") as f:
                json.dump(c, f)
            print(name + ".json", c["start"], len(c["moves"]))
        for n, s in enumerate(MS1_EXAMPLES, 1):
            c = bs12_trivialize(s)
            path = os.path.join(d, "th09_ms1_%d.json" % n)
            with open(path, "w") as f:
                json.dump(c, f)
            print(path, c["start"], len(c["moves"]))
