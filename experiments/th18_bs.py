#!/usr/bin/env python3
"""TH18: exact conjugacy classes (unbounded conjugators) of elements with
non-zero x-exponent sum in  G_n = BS(n,n+1) = <x,y | X y^n x = y^(n+1)>,
and a compiler from frozen-relator rewriting paths to ordinary AC moves.

Theory (research/research-th18.md, Theorem T2): a cyclically reduced element
is  U_d(a) = x^d1 y^a1 ... x^dl y^al ; two such are conjugate iff, after a
cyclic shift, the sign vectors agree and a - a' lies in the lattice L_d
spanned by  q_i e_i - p_i e_{i-1}  ((p,q) = (n,n+1) if d_i=+1, (n+1,n) else).

Run:  python3 experiments/th18_bs.py --selftest
"""
import random
import sys
from fractions import Fraction


def inv(w):
    return w.swapcase()[::-1]


def red(w):
    out = []
    for ch in w:
        if out and out[-1] == ch.swapcase():
            out.pop()
        else:
            out.append(ch)
    return "".join(out)


def parse(w):
    """w = y^c[0] x^d[0] y^c[1] ... x^d[r-1] y^c[r]."""
    c, d = [0], []
    for ch in w:
        if ch == "y":
            c[-1] += 1
        elif ch == "Y":
            c[-1] -= 1
        else:
            d.append(1 if ch == "x" else -1)
            c.append(0)
    return c, d


def yp(k):
    return "y" * k if k >= 0 else "Y" * -k


def unparse(c, d):
    return yp(c[0]) + "".join(("x" if e == 1 else "X") + yp(c[i + 1]) for i, e in enumerate(d))


def rel(n):
    return "X" + "y" * n + "x" + "Y" * (n + 1)


class Tr:
    """A word tracked in syllable form.  self.path lists freely reduced words;
    consecutive ones differ by ONE letter conjugation or ONE application of
    the relator r_n (i.e. U^-1 V is a free conjugate of r_n^{+-1})."""

    def __init__(self, w, n):
        self.n = n
        self.c, self.d = parse(red(w))
        self.path = [red(w)]

    def word(self):
        return red(unparse(self.c, self.d))

    def rec(self):
        w = self.word()
        if w != self.path[-1]:
            self.path.append(w)

    def pq(self, i):
        return (self.n, self.n + 1) if self.d[i] == 1 else (self.n + 1, self.n)

    def move(self, i, k):
        """k times  y^p x^d -> x^d y^q  at stable letter i (k<0: backwards)."""
        p, q = self.pq(i)
        e = 1 if k > 0 else -1
        for _ in range(abs(k)):
            self.c[i] -= e * p
            self.c[i + 1] += e * q
            self.rec()

    def conj_y(self, k):
        """w -> y^k w y^-k by |k| letter conjugations."""
        e = 1 if k > 0 else -1
        for _ in range(abs(k)):
            self.c[0] += e
            self.c[-1] -= e
            self.rec()

    def conj_x(self, e):
        """w -> x^e w x^-e (one letter conjugation)."""
        self.c = [0] + self.c + [0]
        self.d = [e] + self.d + [-e]
        self.cancel()
        self.rec()

    def cancel(self):
        i = 0
        while i < len(self.d) - 1:
            if self.d[i] == -self.d[i + 1] and self.c[i + 1] == 0:
                self.c[i:i + 3] = [self.c[i] + self.c[i + 2]]
                del self.d[i:i + 2]
                i = max(i - 1, 0)
            else:
                i += 1

    def britton(self):
        while True:
            self.cancel()
            for i in range(len(self.d) - 1):
                if self.d[i] == -self.d[i + 1] and self.c[i + 1] % self.pq(i + 1)[0] == 0:
                    self.move(i + 1, self.c[i + 1] // self.pq(i + 1)[0])
                    break
            else:
                return

    def cyc(self):
        """Cyclically reduce: afterwards c[0] = 0 and the word is U_d(a), a = c[1:]."""
        while True:
            self.britton()
            if not self.d:
                return self
            if self.c[0]:
                self.conj_y(-self.c[0])
            if len(self.d) >= 2 and self.d[-1] == -self.d[0] and self.c[-1] % self.pq(0)[0] == 0:
                k = self.c[-1] // self.pq(0)[0]
                self.conj_y(k * self.pq(0)[0])
                self.move(0, k)
                self.conj_x(-self.d[0])
                continue
            return self

    def rot(self):
        """Move the first syllable x^d0 y^c1 to the end (letter conjugations)."""
        c1 = self.c[1]
        self.conj_x(-self.d[0])
        self.conj_y(-c1)


def lattice(n, d):
    rows = []
    for i in range(len(d)):
        p, q = (n, n + 1) if d[i] == 1 else (n + 1, n)
        v = [0] * len(d)
        v[i] += q
        v[i - 1] -= p
        rows.append(v)
    return rows


def hnf(rows):
    M = [r[:] for r in rows]
    H = []
    for col in range(len(rows[0])):
        while True:
            nz = sorted((r for r in M if r[col]), key=lambda r: abs(r[col]))
            if len(nz) <= 1:
                break
            for r in nz[1:]:
                f = r[col] // nz[0][col]
                for j in range(len(r)):
                    r[j] -= f * nz[0][j]
        if nz:
            M = [r for r in M if r is not nz[0]]
            H.append((col, nz[0] if nz[0][col] > 0 else [-t for t in nz[0]]))
    return H


def reduce_mod(a, H):
    a = list(a)
    for col, p in H:
        f = a[col] // p[col]
        for j in range(len(a)):
            a[j] -= f * p[j]
    return tuple(a)


def xexp(w):
    return w.count("x") - w.count("X")


def cls(w, n):
    """Complete conjugacy invariant of w in BS(n,n+1) (requires xexp(w) != 0):
    (t-length, canonical sign vector, canonical exponent vector mod L_d)."""
    assert xexp(w) != 0
    t = Tr(w, n).cyc()
    d, a, best = t.d, t.c[1:], None
    for j in range(len(d)):
        dj = tuple(d[j:] + d[:j])
        cand = (dj, reduce_mod(a[j:] + a[:j], hnf(lattice(n, list(dj)))))
        if best is None or cand < best:
            best = cand
    return (len(d),) + best


def tlen(w, n):
    return len(Tr(w, n).cyc().d)


def label3(w, n):
    """For t-length 3: (sign, b) with w^sign in C_b, b in Z/n(n+1) (Theorem T4)."""
    s = 1 if xexp(w) > 0 else -1
    t = Tr(w if s == 1 else inv(w), n).cyc()
    assert len(t.d) == 3
    while t.d != [1, 1, -1]:
        t.rot()
    for b in range(n * (n + 1)):
        if (b - t.c[2]) % (n + 1) == 0 and (b + t.c[3]) % n == 0:
            return s, b


def solve(n, d, delta):
    """Integers k with sum_i k_i * lattice(n,d)[i] = delta, or None."""
    l = len(d)
    pq = [(n, n + 1) if e == 1 else (n + 1, n) for e in d]
    al, be = [Fraction(1)], [Fraction(0)]
    for j in range(l):                      # k_{j+1} = (k_j q_j - delta_j) / p_{j+1}
        p_next = pq[(j + 1) % l][0]
        al.append(al[j] * pq[j][1] / p_next)
        be.append((be[j] * pq[j][1] - delta[j]) / p_next)
    if al[l] == 1:
        return None                         # x-exponent sum 0: not handled
    t = be[l] / (1 - al[l])
    k = [al[j] * t + be[j] for j in range(l)]
    return [int(v) for v in k] if all(v.denominator == 1 for v in k) else None


def bs_path(w, w2, n):
    """Words w = W_0, ..., W_m = w2, each step one letter conjugation or one
    application of r_n; raises ValueError if w, w2 are not conjugate in G_n."""
    t1, t2 = Tr(w, n).cyc(), Tr(w2, n).cyc()
    l = len(t1.d)
    if l != len(t2.d):
        raise ValueError("not conjugate (t-length)")
    for _ in range(l):
        k = None
        if t2.d == t1.d:
            k = solve(n, t1.d, [u - v for u, v in zip(t2.c[1:], t1.c[1:])])
        if k is not None:
            break
        t2.rot()
    else:
        raise ValueError("not conjugate")
    for i in range(1, l):
        t2.move(i, -k[i])
    t2.conj_y(-k[0] * t2.pq(0)[0])
    t2.move(0, -k[0])
    assert t2.word() == t1.word()
    return t1.path + t2.path[::-1][1:]


def conj_form(D, f):
    """(g, e) with D = g f^e g^-1 in the free group, or None."""
    def cyc_split(u):
        u, i = red(u), 0
        while len(u) - 2 * i >= 2 and u[i] == u[len(u) - 1 - i].swapcase():
            i += 1
        return u[:i], u[i:len(u) - i]
    h, D0 = cyc_split(D)
    u, f0 = cyc_split(f)
    for e, R in ((1, f0), (-1, inv(f0))):
        if len(R) == len(D0):
            for k in range(len(R)):
                if R[k:] + R[:k] == D0:     # D0 = p^-1 R p, p = R[:k]
                    return red(h + inv(R[:k]) + inv(u)), e
    return None


def compile_path(words, state, mi, moves):
    """Replay a path of the moving relator state[mi] (other relator frozen)
    as strict elementary moves appended to `moves`; state is updated."""
    fi = 1 - mi
    assert red(words[0]) == state[mi]
    for V in words[1:]:
        U = state[mi]
        if V == U:
            continue
        for g in "xXyY":
            if red(g + U + inv(g)) == V:
                moves.append({"op": "conjugate", "i": mi, "g": g})
                break
        else:
            cf = conj_form(inv(U) + V, state[fi])
            if cf is None:
                raise ValueError("not a single relator application: %s -> %s" % (U, V))
            g, e = cf
            moves.extend({"op": "conjugate", "i": fi, "g": ch} for ch in reversed(g))
            if e == -1:
                moves.append({"op": "invert", "i": fi})
            moves.append({"op": "multiply", "i": mi, "j": fi})
            if e == -1:
                moves.append({"op": "invert", "i": fi})
            moves.extend({"op": "conjugate", "i": fi, "g": ch.swapcase()} for ch in g)
        state[mi] = V


def rewrite_path(w, lhs, rhs, cap=100000):
    """Leftmost string rewriting lhs -> rhs with free reduction."""
    path = [red(w)]
    for _ in range(cap):
        j = path[-1].find(lhs)
        if j < 0:
            return path
        path.append(red(path[-1][:j] + rhs + path[-1][j + len(lhs):]))
    raise RuntimeError("rewriting did not terminate")


def finish(state, pi, moves):
    """state[pi] is primitive with a single y-letter: go to exactly (x, y) (Lemma D3)."""
    wi = 1 - pi
    p = state[pi]
    path = [p]
    while len(p) >= 2 and p[0] == p[-1].swapcase():
        p = red(p[-1] + p + p[0])
        path.append(p)
    assert p.count("y") + p.count("Y") == 1
    while p[0] not in "yY":
        p = red(p[1:] + p[0])
        path.append(p)
    compile_path(path, state, pi, moves)
    k = xexp(p)
    assert len(set(p[1:])) <= 1
    same, other = ("X" if k > 0 else "x") * abs(k), ("x" if k > 0 else "X") * abs(k)
    w = state[wi]
    path = [w]
    while "y" in w or "Y" in w:
        j = min(i for i, ch in enumerate(w) if ch in "yY")
        w = red(w[:j] + (same if w[j] == p[0] else other) + w[j + 1:])
        path.append(w)
    assert w in ("x", "X"), "presentation is not of the trivial group"
    compile_path(path, state, wi, moves)
    compile_path([p[:i] for i in range(len(p), 0, -1)], state, pi, moves)
    for i in (0, 1):
        if state[i] in ("X", "Y"):
            moves.append({"op": "invert", "i": i})
            state[i] = inv(state[i])
    if state == ["y", "x"]:                 # interchange, Lemma D1(a)
        moves.extend([{"op": "multiply", "i": 0, "j": 1}, {"op": "invert", "i": 1},
                      {"op": "multiply", "i": 1, "j": 0}, {"op": "conjugate", "i": 1, "g": "x"},
                      {"op": "invert", "i": 1}, {"op": "multiply", "i": 0, "j": 1},
                      {"op": "conjugate", "i": 0, "g": "Y"}, {"op": "invert", "i": 1}])
        state[:] = ["x", "y"]
    assert state == ["x", "y"]


def normalize(state, moves):
    """From a state {x^+-1, y^+-1} in either order to exactly (x, y)."""
    for i in (0, 1):
        if state[i] in ("X", "Y"):
            moves.append({"op": "invert", "i": i})
            state[i] = inv(state[i])
    if state == ["y", "x"]:                 # interchange, Lemma D1(a)
        moves.extend([{"op": "multiply", "i": 0, "j": 1}, {"op": "invert", "i": 1},
                      {"op": "multiply", "i": 1, "j": 0}, {"op": "conjugate", "i": 1, "g": "x"},
                      {"op": "invert", "i": 1}, {"op": "multiply", "i": 0, "j": 1},
                      {"op": "conjugate", "i": 0, "g": "Y"}, {"op": "invert", "i": 1}])
        state[:] = ["x", "y"]
    assert state == ["x", "y"]


def div_path(n, b):
    """Theorem T6: from r_n to a primitive word; every step is a letter
    conjugation or ONE application of w_b = x^2 y^b X y^-b (b | n or b | n+1)."""
    r, B = rel(n), abs(b)
    if n % B == 0:
        return rewrite_path(r, "y" * B + "x", "xx" + "y" * B) if b > 0 else \
            rewrite_path(r, "X" + "y" * B, "y" * B + "XX")
    assert (n + 1) % B == 0
    r2 = red("x" + r + "X")
    return [r] + (rewrite_path(r2, "x" + "Y" * B, "Y" * B + "xx") if b > 0 else
                  rewrite_path(r2, "Y" * B + "X", "XX" + "Y" * B))


def _cert(start, moves, text):
    return {"format": "ordinary-ac-elementary-v1", "start": start, "target": ["x", "y"],
            "moves": moves, "description": text}


def cert_divisor(n, w):
    """MS(n,w) -> (x,y) for w in a divisor class C_b^{+-1} (Theorem T6)."""
    state, moves = [rel(n), red(w)], []
    start = state[:]
    if xexp(state[1]) < 0:
        moves.append({"op": "invert", "i": 1})
        state[1] = inv(state[1])
    bb = label3(state[1], n)[1]
    cands = [c for c in (bb, bb - n * (n + 1)) if n % abs(c) == 0 or (n + 1) % abs(c) == 0]
    if not cands:
        raise ValueError("not a divisor class")
    b = cands[0]
    compile_path(bs_path(state[1], "xx" + yp(b) + "X" + yp(-b), n), state, 1, moves)
    compile_path(div_path(n, b), state, 0, moves)
    finish(state, 0, moves)
    return _cert(start, moves, "TH18 Theorem T6: MS(%d,w), w in C_%d, two ACM moves + D3" % (n, b))


def cert_len1(n, w):
    """MS(n,w) -> (x,y) for w of t-length 1 (Theorem T3)."""
    state, moves = [rel(n), red(w)], []
    start = state[:]
    if xexp(state[1]) < 0:
        moves.append({"op": "invert", "i": 1})
        state[1] = inv(state[1])
    compile_path(bs_path(state[1], "x", n), state, 1, moves)
    compile_path([rel(n), rel(n)[1:], "Y"], state, 0, moves)
    normalize(state, moves)
    return _cert(start, moves, "TH18 Theorem T3: MS(%d,w), t-length 1, one ACM move + D3" % n)


def selftest():
    sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
    import elementary_verify as EV
    import g_bs
    rng = random.Random(18)
    rw = lambda a, b: red("".join(rng.choice("xXyY") for _ in range(rng.randint(a, b))))
    npath = 0
    for n in (2, 3, 4):
        R = rel(n)
        for it in range(400):
            w = rw(1, 14)
            if xexp(w) == 0:
                continue
            g, h, j = rw(0, 8), rw(0, 4), rng.randint(0, len(w))
            w2 = red(g + w[:j] + h + rng.choice((R, inv(R))) + inv(h) + w[j:] + inv(g))
            assert cls(w, n) == cls(w2, n), (n, w, w2)
            if it % 8 == 0:
                state, moves = [R, w], []
                compile_path(bs_path(w, w2, n), state, 1, moves)
                EV.replay({"format": "ordinary-ac-elementary-v1", "start": [R, w],
                           "target": [R, w2], "moves": moves})
                npath += 1
    pos = 0
    for n in (2, 3):
        for _ in range(1500):
            u, v = rw(1, 7), rw(1, 7)
            if abs(xexp(u)) != 1 or abs(xexp(v)) != 1:
                continue
            mine = cls(u, n) in (cls(v, n), cls(inv(v), n))
            theirs = g_bs.conjugate(u, v, n, n + 1, window=40) is not None
            assert mine or not theirs, (n, u, v)        # G's positives are exact
            assert theirs or not mine, (n, u, v)        # short words: window 40 suffices
            pos += mine
    words, frontier = [], [""]
    for _ in range(7):
        frontier = [w + ch for w in frontier for ch in "xXyY" if not w or w[-1] != ch.swapcase()]
        words += [w for w in frontier if xexp(w) == 1]
    for n in (2, 3, 4):
        lab = {}
        for w in words:
            c = cls(w, n)
            if c[0] == 3:
                lab.setdefault(label3(w, n)[1], set()).add(c)
        assert len(lab) == n * (n - 1) and all(len(s) == 1 for s in lab.values()), (n, lab)
        assert len({next(iter(s)) for s in lab.values()}) == n * (n - 1)
        assert all(b % n and b % (n + 1) for b in lab)
        assert label3("XYxxY", n)[1] == (2 * n + 1) % (n * (n + 1))
        assert all(cls("x" + yp(k), n) == cls("x", n) for k in range(-9, 10))
    ncert = 0
    for n in range(2, 9):
        for b in range(-n - 1, n + 2):
            if b and (n % abs(b) == 0 or (n + 1) % abs(b) == 0) and b % n and b % (n + 1):
                EV.replay(cert_divisor(n, "xx" + yp(b) + "X" + yp(-b)))
                ncert += 1
    EV.replay(cert_divisor(2, "XYxxY"))
    EV.replay(cert_len1(3, "XyyyxxxyyyyXy"))
    print("th18_bs self-test passed: invariance (3 x 400 trials), %d compiled paths replayed, "
          "%d conjugate pairs cross-checked against g_bs, class counts n(n-1) for n=2,3,4, "
          "%d divisor-class certificates replayed" % (npath, pos, ncert))


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        print(__doc__)
