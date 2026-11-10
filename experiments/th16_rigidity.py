#!/usr/bin/env python3
"""TH16: piece structure (small cancellation), exact conjugacy minima in BS(3,4)
(Collins slides) and in torus-type one-relator quotients (weighted syllables).
Standard library only.  Usage: python3 experiments/th16_rigidity.py --selftest | --all
Words: x,y and X,Y (inverse).  All lengths are cyclic lengths."""
import sys, itertools
from fractions import Fraction

INV = str.maketrans("xXyY", "XxYy")
def inv(w): return w.translate(INV)[::-1]
def red(w):
    o = []
    for c in w:
        if o and o[-1] == c.swapcase(): o.pop()
        else: o.append(c)
    return "".join(o)
def cyc(w):
    w = red(w)
    while len(w) > 1 and w[0] == w[-1].swapcase(): w = w[1:-1]
    return w
def rots(w): return [w[i:] + w[:i] for i in range(len(w))]
def orb(w):
    w = cyc(w); return set(rots(w)) | set(rots(inv(w)))
def cyc_words(L):
    """all cyclically reduced words of length L"""
    def rec(p):
        if len(p) == L:
            if L < 2 or p[0] != p[-1].swapcase(): yield p
            return
        for c in "xXyY":
            if not p or p[-1] != c.swapcase(): yield from rec(p + c)
    yield from rec("")

# ---------- pieces ----------
def max_piece(rel_list):
    """max length of a piece of the symmetrized closure of rel_list
    (relators cyclically reduced, not proper powers, pairwise non-conjugate up to inversion)"""
    R = set()
    for r in rel_list: R |= orb(r)
    R = sorted(R); best = 0
    for i, a in enumerate(R):
        for b in R[i+1:]:
            k = 0
            while k < min(len(a), len(b)) and a[k] == b[k]: k += 1
            best = max(best, k)
    return best
def min_pieces_cover(r):
    """least number of pieces whose product is a cyclic conjugate of r (C(p) holds iff this is >= p)"""
    r = cyc(r); L = len(r); R = sorted(orb(r))
    def is_piece(u):
        return sum(1 for a in R if a.startswith(u)) >= 2
    best = None
    for start in range(L):
        w = r[start:] + r[:start]
        # shortest path cover of w by pieces (linear DP)
        INF = 10**9; d = [INF] * (L + 1); d[0] = 0
        for i in range(L):
            if d[i] == INF: continue
            for j in range(i + 1, L + 1):
                if is_piece(w[i:j]): d[j] = min(d[j], d[i] + 1)
                else: break
        if d[L] < INF: best = d[L] if best is None else min(best, d[L])
    return best
def whitehead_triangle(r):
    """True iff the star graph of cyc(r) on {x,X,y,Y} has a triangle (then T(4) fails)"""
    r = cyc(r); E = set()
    for i in range(len(r)):
        u, v = r[i], r[(i + 1) % len(r)]
        E.add(frozenset((u.swapcase(), v)))
    V = "xXyY"
    return any(frozenset((a, b)) in E and frozenset((b, c)) in E and frozenset((a, c)) in E
               for a, b, c in itertools.combinations(V, 3))

# ---------- free products C_m * C_n and torus-type quotients (Lemma J0 of research-j) ----------
def fp_reduce(syl, orders):
    """syl: list of (factor, exponent); reduce in the free product of cyclic groups of given orders"""
    o = []
    for f, e in syl:
        e %= orders[f]
        if e == 0: continue
        if o and o[-1][0] == f:
            e2 = (o[-1][1] + e) % orders[f]; o.pop()
            if e2: o.append((f, e2))
        else: o.append((f, e))
    return o
def fp_necklace(syl, orders):
    """canonical cyclically reduced necklace (tuple), computed by brute force and safely"""
    s = fp_reduce(syl, orders)
    while len(s) > 1 and s[0][0] == s[-1][0]:
        f = s[0][0]; e = (s[0][1] + s[-1][1]) % orders[f]
        s = s[1:-1]
        if e: s = [(f, e)] + s
        s = fp_reduce(s, orders)
    if not s: return ()
    return min(tuple(s[i:] + s[:i]) for i in range(len(s)))
class TorusQuotient:
    """G = <x,y | r> with G/Z = C_m * C_n; img maps each of x,y to a syllable list; ab = (ab(x), ab(y)).
    By Lemma J0: w ~ w' in G iff necklaces agree and ab agree."""
    def __init__(self, orders, img, ab):
        self.orders = orders; self.ab = ab
        self.img = dict(img)
        for g in "xy":
            self.img[g.upper()] = [(f, -e) for f, e in reversed(self.img[g])]
    def cls(self, w):
        syl = [p for c in w for p in self.img[c]]
        a = sum((1 if c.islower() else -1) * self.ab["xy".index(c.lower())] for c in w)
        return (fp_necklace(syl, self.orders), a)
    def conj_pm(self, w, s):
        c = self.cls(w); return c == self.cls(s) or c == self.cls(inv(s))
    def short_conjugates(self, s, maxlen):
        """dict length -> sorted list of cyclically reduced words w, |w| = length, w ~ s^{+-1} in G"""
        t = {self.cls(s), self.cls(inv(s))}
        return {L: sorted(w for w in cyc_words(L) if self.cls(w) in t) for L in range(1, maxlen + 1)}

# ---------- BS(P,Q) = <x,y | X y^P x = y^Q>: Britton reduction and Collins slides ----------
class BS:
    """stable letter x; pinches X y^(P j) x -> y^(Q j), x y^(Q j) X -> y^(P j).
    slide at x^e between y^a (left) and y^b (right):  e=+1: a-=P k, b+=Q k ;  e=-1: a-=Q k, b+=P k."""
    def __init__(self, P, Q): self.P, self.Q = P, Q
    def parse(self, w):
        """cyclic word -> (eps list, a list) with w = x^e1 y^a1 ... x^en y^an (cyclic); n=0 -> ([], [a])"""
        w = cyc(w)
        if not any(c in "xX" for c in w):
            return [], [sum(1 if c == "y" else -1 for c in w)]
        i = next(j for j, c in enumerate(w) if c in "xX"); w = w[i:] + w[:i]
        eps, a = [], []
        for c in w:
            if c in "xX": eps.append(1 if c == "x" else -1); a.append(0)
            else: a[-1] += 1 if c == "y" else -1
        return eps, a
    def britton(self, w):
        """cyclically Britton-reduced (eps, a)"""
        eps, a = self.parse(w); P, Q = self.P, self.Q
        changed = True
        while changed and len(eps) >= 2:
            changed = False; n = len(eps)
            for i in range(n):
                j = (i + 1) % n
                if eps[i] == -1 and eps[j] == 1 and a[i] % P == 0: new = a[i] // P * Q
                elif eps[i] == 1 and eps[j] == -1 and a[i] % Q == 0: new = a[i] // Q * P
                else: continue
                if n == 2:
                    return [], [a[j] + new]
                h = (i - 1) % n; tot = a[h] + new + a[j]
                keep = [t for t in range(n) if t not in (i, j)]
                a2 = {t: a[t] for t in keep}; a2[h] = tot
                eps = [eps[t] for t in keep]; a = [a2[t] for t in keep]
                changed = True; break
        return eps, a
    def word(self, eps, a):
        return "".join(("x" if e == 1 else "X") + ("y" * k if k > 0 else "Y" * (-k)) for e, k in zip(eps, a))
    def solve(self, eps, d):
        """integer k with d_i = in_i k_i - out_{i+1} k_{i+1}, or None (exact rational elimination)"""
        n = len(eps); P, Q = self.P, self.Q
        inn = [Q if e == 1 else P for e in eps]; out = [P if e == 1 else Q for e in eps]
        M = [[Fraction(0)] * n + [Fraction(d[i])] for i in range(n)]
        for i in range(n):
            M[i][i] += inn[i]; M[i][(i + 1) % n] -= out[(i + 1) % n]
        r = 0; piv = []
        for c in range(n):
            p = next((i for i in range(r, n) if M[i][c] != 0), None)
            if p is None: continue
            M[r], M[p] = M[p], M[r]; pv = M[r][c]; M[r] = [v / pv for v in M[r]]
            for i in range(n):
                if i != r and M[i][c] != 0:
                    f = M[i][c]; M[i] = [v - f * u for v, u in zip(M[i], M[r])]
            piv.append(c); r += 1
        if r < n: raise ValueError("singular slide matrix (x-exponent sum 0)")
        k = [M[i][n] for i in range(n)]
        return [int(v) for v in k] if all(v.denominator == 1 for v in k) else None
    def min_conjugates(self, w, slack=0):
        """(minimal length, set of all cyclically reduced words of length <= minlen+slack conjugate to w),
        for Britton length n >= 1 and nonzero x-exponent sum.  Exact, via Collins' lemma."""
        eps, a = self.britton(w); n = len(eps)
        if n == 0: raise ValueError("elliptic")
        L0 = sum(abs(v) for v in a) + slack
        found = {}
        def ball(i, rem):
            if i == n: yield []; return
            for v in range(-rem, rem + 1):
                for rest in ball(i + 1, rem - abs(v)): yield [v] + rest
        for sh in range(n):
            if eps[sh:] + eps[:sh] != eps: continue      # alignment of the sign pattern
            a_rot = a[sh:] + a[:sh]
            for t in ball(0, L0):
                if self.solve(eps, [t[i] - a_rot[i] for i in range(n)]) is not None:
                    ww = self.word(eps, t)
                    if cyc(ww) == ww: found[ww] = len(ww)
        mn = min(found.values())
        out = set()
        for ww, l in found.items():
            if l <= mn + slack: out |= set(rots(ww))
        return mn, out

AKB = TorusQuotient({"S": 2, "T": 3}, {"x": [("T", 2), ("S", 1)], "y": [("S", 1), ("T", 2)]}, (1, 1))   # F/<<xyxYXY>>
MW  = TorusQuotient({"a": 3, "t": 2}, {"x": [("a", 1)], "y": [("t", 1), ("a", 2)]}, (2, 1))             # F/<<XYxxY>>
def torus_xy(n, m):   # F/<<x^n Y^m>> -> C_n * C_m, ab x->m, y->n
    return TorusQuotient({"a": n, "b": m}, {"x": [("a", 1)], "y": [("b", 1)]}, (m, n))

# ---------- finite-quotient sieve (necessary conditions for conjugacy in F/<<r>>) ----------
def perm_mul(p, q): return tuple(p[i] for i in q)          # (p*q)(i) = p(q(i))
def perm_inv(p):
    r = [0] * len(p)
    for i, v in enumerate(p): r[v] = i
    return tuple(r)
def cycle_type(p):
    seen = [False] * len(p); ct = []
    for i in range(len(p)):
        if not seen[i]:
            l = 0; j = i
            while not seen[j]: seen[j] = True; j = p[j]; l += 1
            ct.append(l)
    return tuple(sorted(ct))
def class_reps(n):
    """one permutation per cycle type of S_n"""
    reps = {}
    def parts(n, m):
        if n == 0: yield []; return
        for k in range(min(n, m), 0, -1):
            for r in parts(n - k, k): yield [k] + r
    out = []
    for lam in parts(n, n):
        p = list(range(n)); pos = 0
        for k in lam:
            for i in range(k): p[pos + i] = pos + (i + 1) % k
            pos += k
        out.append(tuple(p))
    return out
def ev(w, gx, gy, gX, gY, e):
    m = {"x": gx, "y": gy, "X": gX, "Y": gY}; p = e
    for c in w: p = perm_mul(p, m[c])
    return p
def homs(r, n):
    """all homomorphisms F/<<r>> -> S_n up to conjugacy of the image of x (x runs over class reps)"""
    e = tuple(range(n)); out = []
    for gx in class_reps(n):
        gX = perm_inv(gx)
        for gy in itertools.permutations(range(n)):
            gY = perm_inv(gy)
            if ev(r, gx, gy, gX, gY, e) == e: out.append((gx, gy, gX, gY))
    return out
def sieve(r, s, maxlen, degrees=(4, 5, 6, 7), ab=None):
    """cyclically reduced words w, |w| <= maxlen, not excluded from being conjugate to s^{+-1} in F/<<r>>:
    same cycle types as s under every hom to S_n (n in degrees) and, if ab=(cx,cy) is given, ab(w) = +-ab(s).
    Returns dict length -> list.  A word NOT returned is PROVED non-conjugate to s^{+-1}."""
    def abv(w): return sum((1 if c.islower() else -1) * ab["xy".index(c.lower())] for c in w)
    cand = {L: [w for w in cyc_words(L) if ab is None or abs(abv(w)) == abs(abv(s))] for L in range(1, maxlen + 1)}
    for n in degrees:
        e = tuple(range(n))
        for h in homs(r, n):
            ts = cycle_type(ev(s, *h, e))
            for L in cand: cand[L] = [w for w in cand[L] if cycle_type(ev(w, *h, e)) == ts]
    return cand
MW2 = TorusQuotient({"a": 3, "s": 2}, {"x": [("a", 1)], "y": [("s", 1), ("a", 1)]}, (2, -1))            # F/<<YXXYx>>

# ---------- named words ----------
B_ = "xyxYXY"; P3_ = "xxxYYYY"; C_ = "xyxYYXy"; K3_ = "xxxYXyy"; Q1_ = "xxyXYY"; Q2_ = "xxxYYXy"
W1_ = "XYxxY"; W2_ = "YXXYx"
def ms(n): return "X" + "y" * n + "x" + "Y" * (n + 1)          # x^-1 y^n x y^-(n+1)
def msp(n): return "X" + "y" * (n + 1) + "x" + "Y" * n          # x^-1 y^(n+1) x y^-n
D34 = ("YXYxx YXXYx YXYxyx YYxyXX YXyXYx YYxxyX YXYXYx YXYxYx YYxyXyX YYYXXyx YYXyxyX YYxyXYX YYxyxyX YYYXyxx "
       "YYxyXyx YYxYxyX YYxYXYx YYXYxYX YYYXyXyx YYYXyxyX YYxYXyyx YYYXYXyx YYYXYYxx YYYXXYYx YYYXyxYx YYxYYxyX "
       "YYXyyxYX YYYXyxyx YYYxyXyx YYXYYxyX YYYXYxYX YYYYxYXX YYYYxxYX YYYxYXYx").split()

def c16_possible(L):
    """is there a cyclically reduced non-power word of length L in F2 with all pieces < L/6 ?  (brute force)"""
    for w in cyc_words(L):
        if len(orb(w)) == 2 * L and 6 * max_piece([w]) < L: return w
    return None

def selftest():
    import random
    rnd = random.Random(16)
    # (1) pieces: hand-checked values
    assert max_piece([C_]) == 2 and min_pieces_cover(C_) == 4
    assert max_piece(["xyXY"]) == 1 and min_pieces_cover("xyXY") == 4 and not whitehead_triangle("xyXY")
    assert max_piece([P3_]) == 3          # y^3 inside y^4
    # (2) Proposition 1 by brute force for 3 <= L <= 10: no C'(1/6) relator
    for L in range(3, 11): assert c16_possible(L) is None, L
    # (3) torus quotients reproduce research-a / research-j counts for AK(3)
    d = AKB.short_conjugates(P3_, 9); assert [len(d[L]) for L in (7, 8, 9)] == [28, 0, 432]
    assert set(d[7]) == orb(P3_) | orb("yyyXXXX")
    d = torus_xy(3, 4).short_conjugates(B_, 8); assert [len(d[L]) for L in (6, 7, 8)] == [12, 0, 32]
    # (4) class functions are invariant under conjugation and insertion of relator conjugates
    def rw(k): return red("".join(rnd.choice("xXyY") for _ in range(k)))
    for T, r in ((AKB, B_), (MW, W1_), (MW2, W2_), (torus_xy(3, 4), P3_)):
        assert T.cls(r) == ((), 0)
        for _ in range(300):
            w, g, h = rw(8), rw(5), rw(4)
            w2 = red(g + w[:3] + h + rnd.choice([r, inv(r)]) + inv(h) + w[3:] + inv(g))
            assert T.cls(cyc(w)) == T.cls(cyc(w2))
    # (5) BS slides: invariance of the minimal set under conjugation / relator insertion (odd x-exponent words)
    for P, Q in ((3, 4), (4, 3)):
        bs = BS(P, Q); r = "X" + "y" * P + "x" + "Y" * Q
        assert bs.britton(r) == ([], [0])
        done = 0
        while done < 40:
            w = cyc(rw(6))
            if sum((c == "x") - (c == "X") for c in w) not in (1, -1): continue
            if len(bs.britton(w)[0]) < 3: continue
            g, h = rw(3), rw(2)
            w2 = cyc(red(g + w[:2] + h + rnd.choice([r, inv(r)]) + inv(h) + w[2:] + inv(g)))
            if len(bs.britton(w2)[0]) != len(bs.britton(w)[0]): raise AssertionError((w, w2))
            assert bs.min_conjugates(w) == bs.min_conjugates(w2), (w, w2)
            done += 1
    # (6) sieve soundness on a known case
    r = sieve(P3_, B_, 7, degrees=(4, 5), ab=(4, 3)); assert orb(B_) <= set(r[6])
    print("th16_rigidity self-test passed")

# ---------- PSL(2,p) sieve (necessary conditions for conjugacy in F/<<r>>) ----------
def sl2(p):
    out = []
    for a in range(p):
        for b in range(p):
            for c in range(p):
                if a:
                    d = (1 + b * c) * pow(a, p - 2, p) % p; out.append((a, b, c, d))
                elif (b * c) % p == p - 1:
                    out.extend((0, b, c, d) for d in range(p))
    return out
def mm(A, B, p):
    return ((A[0]*B[0] + A[1]*B[2]) % p, (A[0]*B[1] + A[1]*B[3]) % p,
            (A[2]*B[0] + A[3]*B[2]) % p, (A[2]*B[1] + A[3]*B[3]) % p)
def minv(A, p): return (A[3], (-A[1]) % p, (-A[2]) % p, A[0])
def mev(w, g, p):
    M = (1, 0, 0, 1)
    for ch in w: M = mm(M, g[ch], p)
    return M
def psl_homs(r, p):
    """lifts F -> SL(2,p) of all homs F/<<r>> -> PSL(2,p), x up to GL(2,p)-conjugacy.  Returns (g, sign)."""
    I, J = (1, 0, 0, 1), (p - 1, 0, 0, p - 1)
    xs = [I, J] + [(0, p - 1, 1, t) for t in range(p)]
    out = []; G = sl2(p)
    for gx in xs:
        gX = minv(gx, p)
        for gy in G:
            g = {"x": gx, "X": gX, "y": gy, "Y": minv(gy, p)}
            v = mev(r, g, p)
            if v == I: out.append((g, 1))
            elif v == J: out.append((g, -1))
    return out
def psl_inv(w, g, sign, p):
    M = mev(w, g, p); t = (M[0] + M[3]) % p
    scalar = M[1] == 0 and M[2] == 0 and M[0] == M[3]
    return (t if sign == 1 else t * t % p, scalar)
def psl_sieve(r, s, maxlen, primes, ab, cand=None, stats=None):
    """words w (cyclically reduced, |w| <= maxlen, ab(w) = +-ab(s)) NOT separated from s^{+-1} by any
    hom F/<<r>> -> PSL(2,p), p in primes.  A word not returned is PROVED non-conjugate to s^{+-1} in F/<<r>>."""
    def abv(w): return sum((1 if c.islower() else -1) * ab["xy".index(c.lower())] for c in w)
    if cand is None:
        cand = [w for L in range(1, maxlen + 1) for w in cyc_words(L) if abs(abv(w)) == abs(abv(s))]
    for p in primes:
        hs = psl_homs(r, p)
        for g, sign in hs:
            ts = psl_inv(s, g, sign, p)
            cand = [w for w in cand if psl_inv(w, g, sign, p) == ts]
        if stats is not None: stats.append((p, len(hs), len(cand)))
    return cand

def piece_table():
    rows = [("b", B_), ("p_3", P3_), ("c", C_), ("k_3", K3_), ("q_1", Q1_), ("q_2", Q2_), ("m_3", ms(3)),
            ("w_1", W1_), ("w_2", W2_)]
    print("relator  word        len  maxpiece  ratio   min#pieces  star-graph triangle")
    for nm, r in rows:
        print("%-8s %-11s %3d  %5d    %.3f  %6s      %s" % (nm, r, len(r), max_piece([r]), max_piece([r]) / len(r),
              min_pieces_cover(r), whitehead_triangle(r)))
    print("pairs (joint symmetrized set): max piece")
    for nm, (r, s) in (("AK(3)", (P3_, B_)), ("P_3", (C_, K3_)), ("Q", (Q1_, Q2_)), ("MS(3,w1)", (ms(3), W1_)),
                       ("MS(3,w2)", (ms(3), W2_))):
        print("  %-9s %d  (shorter relator length %d)" % (nm, max_piece([r, s]), min(len(r), len(s))))

def uniform_checks(nmax=8):
    """Theorems A, B, D of research-th16 for n = 3..nmax, by exact computation"""
    def yy(k): return "y" * k if k > 0 else "Y" * (-k)
    for n in range(3, nmax + 1):
        for T in (MW, MW2):          # Theorem B, the (2, 2n+1) case: all two-x-letter words of length 2n+3
            good = set()
            for e1 in "xX":
                for e2 in "xX":
                    for k1 in range(-(2 * n + 1), 2 * n + 2):
                        for sg in (1, -1):
                            w = e1 + yy(k1) + e2 + yy(sg * (2 * n + 1 - abs(k1)))
                            if cyc(w) == w and len(w) == 2 * n + 3 and T.conj_pm(w, ms(n)): good |= set(rots(w))
            assert good == orb(ms(n)) | orb(msp(n)), n
        for w in (W1_, W2_):         # Theorem A
            for P, Q in ((n, n + 1), (n + 1, n)):
                mn, S = BS(P, Q).min_conjugates(w); assert mn == 5 and S == set(rots(w)), (n, w)
        assert B_ in BS(n, n + 1).min_conjugates(W1_, slack=1)[1]                 # exit (m_n, b)
        assert AKB.cls(ms(n)) == AKB.cls("x" * n + "Y" * (n + 1))                 # Proposition D
    return True

def report_ms():
    m = ms(3); bs = BS(3, 4); classes = {}
    assert orb("YYYYXyyyx") == orb(m)
    for v in D34:
        mn, S = bs.min_conjugates(v); key = min(S | {inv(u) for u in S}); classes.setdefault(key, []).append(v)
        assert mn == 5
    print("34 benchmark partners (research-d 4.3): minimal BS(3,4)-conjugate length 5 for all;",
          len(classes), "classes up to inversion")
    for key, vs in classes.items():
        tag = "w1" if key in orb(W1_) else "w2" if key in orb(W2_) else "?"
        print("  class of", tag, "(canonical", key + "):", len(vs), "partners; of length 5:", [v for v in vs if len(v) == 5])
    for T, w, nm in ((MW, W1_, "w1"), (MW2, W2_, "w2")):
        for n in (3, 4):
            d = T.short_conjugates(ms(n), 2 * n + 4)
            print("  m_%d in G_%s: conjugates by length" % (n, nm), {L: len(v) for L, v in d.items() if v},
                  "| equality set == Orb(m) u Orb(m'):", set(d[2 * n + 3]) == orb(ms(n)) | orb(msp(n)))
        mn, S = bs.min_conjugates(w, slack=1)
        print("  %s in BS(3,4): min %d, #words of length 5: %d, of length 6: %d" % (nm, mn,
              len({u for u in S | {inv(u) for u in S} if len(u) == 5}), len({u for u in S | {inv(u) for u in S} if len(u) == 6})))

def report_sieve(primes=(5, 7, 11, 13), degrees=(5, 6, 7, 8)):
    """cheap necessary-condition sieves for P_3 and Q (research-th16 section 5); inconclusive by design"""
    jobs = (("P_3, c frozen, k_3 moved", C_, K3_, 6, (0, 1)), ("P_3, k_3 frozen, c moved", K3_, C_, 6, (1, -2)),
            ("Q, q_1 frozen, q_2 moved", Q1_, Q2_, 6, (1, 1)), ("Q, q_2 frozen, q_1 moved", Q2_, Q1_, 5, (1, 2)))
    for name, r, s, L, ab in jobs:
        cand = psl_sieve(r, s, L, primes, ab)
        for n in degrees:
            e = tuple(range(n))
            for h in homs(r, n):
                if perm_mul(h[0], h[1]) == perm_mul(h[1], h[0]): continue
                ts = cycle_type(ev(s, *h, e))
                cand = [w for w in cand if cycle_type(ev(w, *h, e)) == ts]
        by = {}
        for w in cand: by[len(w)] = by.get(len(w), 0) + 1
        print("%s: unseparated shorter words: %d, by length %s; shortest: %s" % (name, len(cand), by, sorted(cand, key=len)[:6]), flush=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a or not a:
        selftest(); assert uniform_checks(8); print("uniform checks n = 3..8 passed (Theorems A, B, D)")
    if "--pieces" in a or "--all" in a: piece_table()
    if "--ms" in a or "--all" in a: report_ms()
    if "--sieve" in a: report_sieve()
