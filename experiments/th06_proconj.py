#!/usr/bin/env python3
"""TH06: constructive check of the universal 8-move scheme (research-th06.md, Theorem 1).

Standard library only.  Elements of N_c = F/gamma_{c+1} are handled through their
truncated Magnus series in Z<X,Y>/(degree > c) (Magnus: this is faithful on N_c);
every element is built from mu(x)=1+X, mu(y)=1+Y by group operations only, so it
is the image of an honest element of F.

  python3 experiments/th06_proconj.py --selftest
  python3 experiments/th06_proconj.py --solve AK3 --class 5 [--out cert.json]
  python3 experiments/th06_proconj.py --verify certificates/th06_ak3_8move_class6.json
"""
import json, random, sys
from collections import deque

PRES = {"AK1": ("xYY", "xyxYXY"), "AK2": ("xxYYY", "xyxYXY"),
        "AK3": ("xxxYYYY", "xyxYXY"), "AK4": ("xxxxYYYYY", "xyxYXY"),
        "MS3": ("XyyyxYYYY", "XYxxY"), "P3": ("xyxYYXy", "xxxYXyy")}

class Alg:
    """Z<X,Y> truncated at degree c (optionally mod a prime); monomial = tuple of 0/1."""
    def __init__(self, c, mod=None):
        self.c, self.mod = c, mod
        self.one = {(): 1}
    def clean(self, A):
        if self.mod:
            A = {m: v % self.mod for m, v in A.items()}
        return {m: v for m, v in A.items() if v}
    def add(self, A, B, s=1):
        out = dict(A)
        for m, v in B.items():
            out[m] = out.get(m, 0) + s * v
        return self.clean(out)
    def mul(self, A, B):
        c, out = self.c, {}
        for m1, a in A.items():
            r = c - len(m1)
            for m2, b in B.items():
                if len(m2) <= r:
                    m = m1 + m2
                    out[m] = out.get(m, 0) + a * b
        return self.clean(out)
    def inv(self, A):                       # A = 1 + n, n nilpotent
        n = self.add(A, self.one, -1)
        out, term = dict(self.one), dict(self.one)
        for _ in range(self.c):
            term = self.mul(term, {m: -v for m, v in n.items()})
            out = self.add(out, term)
        return out
    def pw(self, A, k):
        if k < 0:
            A, k = self.inv(A), -k
        out = dict(self.one)
        while k:
            if k & 1:
                out = self.mul(out, A)
            A = self.mul(A, A)
            k >>= 1
        return out
    def conj(self, A, G):
        return self.mul(self.mul(self.inv(G), A), G)
    def comm(self, A, B):
        return self.mul(self.mul(self.inv(A), self.inv(B)), self.mul(A, B))
    def word(self, w):
        g = {"x": {(): 1, (0,): 1}, "y": {(): 1, (1,): 1}}
        gi = {k: self.inv(v) for k, v in g.items()}
        out = dict(self.one)
        for ch in w:
            out = self.mul(out, g[ch] if ch in g else gi[ch.lower()])
        return out
    def part(self, A, d):
        return {m: v for m, v in A.items() if len(m) == d}

def lyndon(m):
    """Lyndon words of length m over 0<1 (as tuples), in lexicographic order."""
    out = []
    for n in range(2 ** m):
        w = tuple((n >> (m - 1 - i)) & 1 for i in range(m))
        if all(w < w[i:] for i in range(1, m)):
            out.append(w)
    return out

def std_fact(w):
    for i in range(1, len(w)):              # longest proper Lyndon suffix
        v = w[i:]
        if all(v < v[j:] for j in range(1, len(v))):
            return w[:i], v

def gcomm(alg, w, cache):
    """group commutator C(w) (Magnus series) for the standard bracketing of Lyndon w."""
    key = (alg.c, alg.mod, w)
    if key not in cache:
        if len(w) == 1:
            cache[key] = alg.word("xy"[w[0]])
        else:
            u, v = std_fact(w)
            cache[key] = alg.comm(gcomm(alg, u, cache), gcomm(alg, v, cache))
    return cache[key]

def wname(w):
    return "".join("xy"[i] for i in w)

def solve_int(cols, v):
    """integers z with sum_j z[j]*cols[j] = v (vectors = dicts); None if unsolvable over Z."""
    n = len(cols)
    work = [(dict(cj), [1 if i == j else 0 for i in range(n)]) for j, cj in enumerate(cols)]
    rows = sorted(set(k for cj in cols for k in cj) | set(v))
    v, z = dict(v), [0] * n
    for r in rows:
        while True:
            nz = [t for t in work if t[0].get(r, 0)]
            if len(nz) <= 1:
                break
            a = min(nz, key=lambda t: abs(t[0][r]))
            for b in nz:
                if b is a:
                    continue
                f = b[0][r] // a[0][r]
                for k, val in a[0].items():
                    b[0][k] = b[0].get(k, 0) - f * val
                for i in range(n):
                    b[1][i] -= f * a[1][i]
        nz = [t for t in work if t[0].get(r, 0)]
        vr = v.get(r, 0)
        if not nz:
            if vr:
                return None
            continue
        piv = nz[0]
        work = [t for t in work if t is not piv]
        if vr % piv[0][r]:
            return None
        f = vr // piv[0][r]
        for k, val in piv[0].items():
            v[k] = v.get(k, 0) - f * val
        for i in range(n):
            z[i] += f * piv[1][i]
    return z if not any(v.values()) else None

def lift(alg, coeffs, cache):
    """prod_w C(w)^{e_w}, in the order of the dict."""
    out = dict(alg.one)
    for w, e in coeffs:
        out = alg.mul(out, alg.pw(gcomm(alg, tuple(w), cache), e))
    return out

def two_conj(alg, p, q, T, cache):
    """Lemma 1.1: find g, g' with (p^g q)^{g'} q^-1 = T, for T = p mod gamma_2."""
    g, gp, rec_g, rec_gp = dict(alg.one), dict(alg.one), [], []
    lin = lambda A: {m: v for m, v in A.items() if len(m) == 1}
    pb, qb = lin(p), lin(q)
    for m in range(1, alg.c):
        R = alg.mul(alg.conj(alg.mul(alg.conj(p, g), q), gp), alg.inv(q))
        delta = alg.add(alg.mul(alg.inv(T), R), alg.one, -1)
        assert all(len(k) >= m + 1 for k in delta), "error not in gamma_{m+1}"
        D = alg.part(delta, m + 1)
        if not D:
            continue
        L = lyndon(m)
        low = Alg(m + 1)
        basis = [low.part(low.add(gcomm(low, w, cache), low.one, -1), m) for w in L]
        br = lambda a, B: low.add(low.mul(a, B), low.mul(B, a), -1)
        cols = [br(pb, B) for B in basis] + [br(qb, B) for B in basis]
        z = solve_int(cols, {k: -v for k, v in D.items()})
        assert z is not None, "linear step unsolvable (contradicts (*))"
        alpha, beta = z[:len(L)], z[len(L):]
        ch = [(w, a - b) for w, a, b in zip(L, alpha, beta) if a - b]
        chp = [(w, b) for w, b in zip(L, beta) if b]
        g, gp = alg.mul(g, lift(alg, ch, cache)), alg.mul(gp, lift(alg, chp, cache))
        rec_g += [[wname(w), e] for w, e in ch]
        rec_gp += [[wname(w), e] for w, e in chp]
    R = alg.mul(alg.conj(alg.mul(alg.conj(p, g), q), gp), alg.inv(q))
    assert R == T, "two-conjugation lemma failed"
    return rec_g, rec_gp

# ------------------------------------------------------------------ free words, Nielsen part
def red(w):
    out = []
    for ch in w:
        if out and out[-1] == ch.swapcase():
            out.pop()
        else:
            out.append(ch)
    return "".join(out)

def winv(w):
    return w[::-1].swapcase()

def nielsen(i, U):
    a, b = U
    return [(winv(a), b), (a, winv(b)), (b, a), (red(a + b), b), (red(a + winv(b)), b),
            (a, red(b + a)), (a, red(b + winv(a)))][i]

def expo(w):
    return (w.count("x") - w.count("X"), w.count("y") - w.count("Y"))

def nielsen_path(U):
    """shortest sequence of the 7 Nielsen instructions taking the exponent matrix to I."""
    def step(i, M):
        a, b = M
        neg = lambda v: (-v[0], -v[1])
        add = lambda v, w, s: (v[0] + s * w[0], v[1] + s * w[1])
        return [(neg(a), b), (a, neg(b)), (b, a), (add(a, b, 1), b), (add(a, b, -1), b),
                (a, add(b, a, 1)), (a, add(b, a, -1))][i]
    start, goal = (expo(U[0]), expo(U[1])), ((1, 0), (0, 1))
    seen, dq = {start: []}, deque([start])
    while dq:
        M = dq.popleft()
        if M == goal:
            return seen[M]
        for i in range(7):
            N = step(i, M)
            if N not in seen and max(abs(t) for r in N for t in r) < 50:
                seen[N] = seen[M] + [i]
                dq.append(N)

def cword(w):
    """free word of the group commutator C(w), w a Lyndon word given as a string in x,y."""
    if len(w) == 1:
        return w
    u, v = std_fact(tuple("xy".index(ch) for ch in w))
    a, b = cword(wname(u)), cword(wname(v))
    return red(winv(a) + winv(b) + a + b)

def solve(name_or_pair, c):
    U = PRES.get(name_or_pair, name_or_pair) if isinstance(name_or_pair, str) else name_or_pair
    seq = nielsen_path(U)
    V = tuple(U)
    for i in seq:
        V = nielsen(i, V)
    assert (expo(V[0]), expo(V[1])) == ((1, 0), (0, 1))
    alg, cache = Alg(c), {}
    A, B, x, y = alg.word(V[0]), alg.word(V[1]), alg.word("x"), alg.word("y")
    g1, g2 = two_conj(alg, x, y, A, cache)          # (x^g1 y)^g2 y^-1 = A
    g3, g4 = two_conj(alg, y, A, B, cache)          # (y^g3 A)^g4 A^-1 = B
    return {"format": "th06-8move-nilpotent-v1", "class": c, "presentation": list(U),
            "nielsen": seq, "normalized": list(V), "conjugators": [g1, g2, g3, g4],
            "note": "QUOTIENT-ONLY (mod gamma_{class+1}); NOT an AC trivialization in F. "
                    "g_i = product of C(w)^e in list order, C(w) = group commutator of the "
                    "standard bracketing of the Lyndon word w; scheme of research-th06 Thm 1."}

def verify(cert):
    c, U, V = cert["class"], tuple(cert["presentation"]), tuple(cert["normalized"])
    W = U
    for i in cert["nielsen"]:
        W = nielsen(i, W)
    assert W == V, "Nielsen part does not reproduce the normalized pair"
    alg = Alg(c)
    gs, lens = [], []
    for rec in cert["conjugators"]:
        g, n = dict(alg.one), 0
        for w, e in rec:
            cw = cword(w)                            # explicit free word, independent of gcomm
            g = alg.mul(g, alg.pw(alg.word(cw), e))
            n += abs(e) * len(cw)
        gs.append(g)
        lens.append(n)
    u0, u1 = alg.word("x"), alg.word("y")
    u0 = alg.conj(u0, gs[0]); u0 = alg.mul(u0, u1)
    u0 = alg.conj(u0, gs[1]); u0 = alg.mul(u0, alg.inv(u1))
    u1 = alg.conj(u1, gs[2]); u1 = alg.mul(u1, u0)
    u1 = alg.conj(u1, gs[3]); u1 = alg.mul(u1, alg.inv(u0))
    assert u0 == alg.word(V[0]) and u1 == alg.word(V[1]), "8-move scheme does not reach the pair"
    return lens

def exhaustive_p3_mod2():
    """independent of the solver: in P_3^(2) (order 128) Lemma 1.1 holds for all data."""
    alg = Alg(3, mod=2)
    key = lambda A: frozenset(A)
    x, y = alg.word("x"), alg.word("y")
    elems, dq = {key(alg.one): alg.one}, deque([alg.one])
    while dq:
        g = dq.popleft()
        for s in (x, y):
            h = alg.mul(g, s)
            if key(h) not in elems:
                elems[key(h)] = h
                dq.append(h)
    G = list(elems.values())
    der = {key(alg.one): alg.one}                    # derived subgroup = closure of commutators
    comms = {key(alg.comm(g, h)): alg.comm(g, h) for g in G for h in G}
    dq = deque([alg.one])
    while dq:
        g = dq.popleft()
        for s in comms.values():
            h = alg.mul(g, s)
            if key(h) not in der:
                der[key(h)] = h
                dq.append(h)
    yi, total = alg.inv(y), 0
    for e0 in der.values():                          # stage 2 for every first coordinate x*e0
        q = alg.mul(x, e0)
        qi = alg.inv(q)
        cls = {key(alg.conj(y, g)): alg.conj(y, g) for g in G}
        got = set()
        for a in cls.values():
            w = alg.mul(a, q)
            for g in G:
                got.add(key(alg.mul(alg.conj(w, g), qi)))
        assert got == {key(alg.mul(y, e)) for e in der.values()}
        total += len(got)
    cls = {key(alg.conj(x, g)): alg.conj(x, g) for g in G}
    got = {key(alg.mul(alg.conj(alg.mul(a, y), g), yi)) for a in cls.values() for g in G}
    assert got == {key(alg.mul(x, e)) for e in der.values()}
    return len(G), len(der)

def witt_margin(cmax=60):
    """Witt ranks r_c, Hirsch lengths n_c; Proposition 6 needs 3 r_c - n_c - 1 >= 1 for c >= 5."""
    def mob(n):
        r, p = 1, 2
        while p * p <= n:
            if n % p == 0:
                n //= p
                if n % p == 0:
                    return 0
                r = -r
            p += 1
        return -r if n > 1 else r
    out, n = [], 0
    for c in range(1, cmax + 1):
        r = sum(mob(d) * 2 ** (c // d) for d in range(1, c + 1) if c % d == 0) // c
        n += r
        out.append((c, r, n, 3 * r - n - 1))
    return out

def selftest():
    W = witt_margin()
    assert [w[1] for w in W[:8]] == [2, 1, 2, 3, 6, 9, 18, 30]
    assert all(w[3] >= 1 for w in W if w[0] >= 5)
    print("selftest: Witt ranks; 3r_c - n_c - 1 =", [w[3] for w in W[4:11]], "for c = 5..11, >= 1 for 5 <= c <= 60")
    for m in range(1, 7):                            # leading terms of C(w) are Lie brackets
        alg, cache = Alg(m), {}
        L = lyndon(m)
        assert len(L) == [2, 1, 2, 3, 6, 9][m - 1]
        for w in L:
            d = alg.add(gcomm(alg, w, cache), alg.one, -1)
            assert d and all(len(k) == m for k in d)
            assert alg.word(cword(wname(w))) == gcomm(alg, w, cache)
    n, d = exhaustive_p3_mod2()
    print(f"selftest: P_3^(2): |P|={n} |[P,P]|={d}: two-conjugation lemma exhaustive OK")
    rnd = random.Random(6)
    for trial in range(12):                          # random pairs (x e0, y e1), e_i in [F,F]
        c = rnd.choice([3, 4, 5])
        rw = lambda: "".join(rnd.choice("xyXY") for _ in range(rnd.randint(1, 5)))
        cm = lambda: (lambda a, b: winv(a) + winv(b) + a + b)(rw(), rw())
        U = (red("x" + cm() + cm()), red("y" + cm() + cm()))
        verify(solve(U, c))
    print("selftest: 12 random pairs (x e0, y e1), classes 3-5: solved and verified")
    for name in ("AK1", "AK2", "AK3", "AK4", "MS3", "P3"):
        for c in (2, 3, 4):
            verify(solve(name, c))
    print("selftest: AK1 AK2 AK3 AK4 MS3 P3, classes 2-4: solved and verified")
    print("selftest passed")

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        selftest()
    elif "--solve" in a:
        cert = solve(a[a.index("--solve") + 1], int(a[a.index("--class") + 1]))
        lens = verify(cert)
        print(json.dumps({"presentation": cert["presentation"], "class": cert["class"],
                          "nielsen_moves": len(cert["nielsen"]),
                          "max_abs_exponent": max([abs(e) for g in cert["conjugators"] for _, e in g] + [0]),
                          "conjugator_word_length_bounds": lens}))
        if "--out" in a:
            json.dump(cert, open(a[a.index("--out") + 1], "w"))
    elif "--verify" in a:
        for f in a[a.index("--verify") + 1:]:
            cert = json.load(open(f))
            print(f, "OK: class", cert["class"], "conjugator word-length bounds", verify(cert))
    else:
        print(__doc__)
