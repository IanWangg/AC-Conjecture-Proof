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
