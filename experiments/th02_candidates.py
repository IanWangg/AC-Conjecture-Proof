#!/usr/bin/env python3
"""th02_candidates.py (agent TH02): tests for NON-hidden stabilizer elements.

Lemma 0 of research-th02: if phi fixes the cyclic word r up to inversion, then
phi(r,s) ~AC (r,s) as soon as phi(s) ~ s^{+-1} in F/<<r>>.  For relators that
are not of torus type no conjugacy algorithm is available here, so this file
offers (i) necessary conditions through finite quotients (cycle types in S_n,
traces in SL2(p), and "is h.phi conjugate to h"), and (ii) a bounded
bidirectional search for an explicit r-frozen chain of cyclic products.
A surviving candidate is NOT a proof; a separating quotient IS a proof that
Lemma 0 does not apply at that state.

Usage: python3 experiments/th02_candidates.py --self-test
       python3 experiments/th02_candidates.py sn   R S S2 N
       python3 experiments/th02_candidates.py sl2  R S S2 P
       python3 experiments/th02_candidates.py inner R N      (phi = x -> X)
       python3 experiments/th02_candidates.py bfs  R A B CAP SECONDS
       python3 experiments/th02_candidates.py r1   L          (Collins equation for the open candidate)
"""
import sys, itertools, time, heapq
sys.dont_write_bytecode = True
SW = str.maketrans("xyXY", "XYxy")


def red(w):
    out = []
    for c in w:
        if out and out[-1] == c.swapcase():
            out.pop()
        else:
            out.append(c)
    return "".join(out)


def cycred(w):
    w = red(w)
    while len(w) >= 2 and w[0] == w[-1].swapcase():
        w = w[1:-1]
    return w


def inv(w):
    return w.translate(SW)[::-1]


def canon(w):
    return min(u[k:] + u[:k] for u in (w, inv(w)) for k in range(len(w)))


# ---------------- S_n
def _ctype(p):
    n = len(p); seen = [False] * n; out = []
    for i in range(n):
        if not seen[i]:
            k = 0; j = i
            while not seen[j]:
                seen[j] = True; j = p[j]; k += 1
            out.append(k)
    return tuple(sorted(out))


def _pinv(p):
    return tuple(sorted(range(len(p)), key=lambda i: p[i]))


def _pev(word, tab, n):
    cur = tuple(range(n))
    for ch in word:
        t = tab[ch]; cur = tuple(t[i] for i in cur)
    return cur


def sn_homs(r, n):
    perms = list(itertools.permutations(range(n))); idp = tuple(range(n)); reps = {}
    for p in perms:
        reps.setdefault(_ctype(p), p)
    for px in reps.values():
        for py in perms:
            tab = {"x": px, "y": py, "X": _pinv(px), "Y": _pinv(py)}
            if _pev(r, tab, n) == idp:
                yield tab


def sn_test(r, s, s2, n):
    """(homs with x up to conjugacy, homs separating s from s2 by cycle type)"""
    homs = sep = 0
    for tab in sn_homs(r, n):
        homs += 1
        sep += _ctype(_pev(s, tab, n)) != _ctype(_pev(s2, tab, n))
    return homs, sep


def inner_test(r, n):
    """nontrivial homs h and how many have h.eps_x conjugate to h (necessary for eps_x inner)."""
    perms = list(itertools.permutations(range(n))); homs = good = 0
    mul = lambda a, b: tuple(b[i] for i in a)
    for tab in sn_homs(r, n):
        px, py = tab["x"], tab["y"]
        if px == tuple(range(n)):
            continue
        homs += 1
        good += any(mul(mul(_pinv(g), px), g) == tab["X"] and mul(mul(_pinv(g), py), g) == py for g in perms)
    return homs, good


# ---------------- SL2(p)
def sl2_test(r, s, s2, p):
    G = [(a, b, c, d) for a in range(p) for b in range(p) for c in range(p) for d in range(p) if (a * d - b * c) % p == 1]
    mul = lambda A, B: ((A[0] * B[0] + A[1] * B[2]) % p, (A[0] * B[1] + A[1] * B[3]) % p,
                        (A[2] * B[0] + A[3] * B[2]) % p, (A[2] * B[1] + A[3] * B[3]) % p)
    minv = lambda A: (A[3], (-A[1]) % p, (-A[2]) % p, A[0])
    def ev(word, tab):
        cur = (1, 0, 0, 1)
        for ch in word:
            cur = mul(cur, tab[ch])
        return cur
    seen = set(); reps = []
    for g in G:
        if g not in seen:
            reps.append(g)
            for h in G:
                seen.add(mul(mul(h, g), minv(h)))
    homs = nonab = sep = 0
    for X in reps:
        for Y in G:
            tab = {"x": X, "y": Y, "X": minv(X), "Y": minv(Y)}
            if ev(r, tab) == (1, 0, 0, 1):
                homs += 1; nonab += mul(X, Y) != mul(Y, X)
                A, B = ev(s, tab), ev(s2, tab)
                sep += (A[0] + A[3]) % p != (B[0] + B[3]) % p
    return homs, nonab, sep


# ---------------- bounded r-frozen search
def frozen_search(r, a, b, cap, seconds, maxstates=600000):
    """bidirectional best-first search: is canon(b) reachable from canon(a) by cyclic products with
    rotations of r^{+-1} (at least one cancelled letter), all words of length <= cap?
    Returns (found, chain or None, states_a, states_b, exhausted)."""
    rots = [u[k:] + u[:k] for u in (r, inv(r)) for k in range(len(r))]
    by_first = {}
    for R in rots:
        by_first.setdefault(R[0], []).append(R)
    t0 = time.time()
    side = [{canon(a): None}, {canon(b): None}]
    heaps = [[(len(a), canon(a))], [(len(b), canon(b))]]
    if canon(a) == canon(b):
        return True, [canon(a)], 1, 1, False
    while (heaps[0] or heaps[1]) and time.time() - t0 < seconds and len(side[0]) + len(side[1]) < maxstates:
        k = 0 if (heaps[0] and (not heaps[1] or len(side[0]) <= len(side[1]))) else 1
        _, w = heapq.heappop(heaps[k])
        for u in (w, inv(w)):
            for i in range(len(u)):
                v = u[i:] + u[:i]
                for R in by_first.get(v[-1].swapcase(), ()):
                    new = cycred(v + R)
                    if not new or len(new) > cap:
                        continue
                    c = canon(new)
                    if c not in side[k]:
                        side[k][c] = w
                        if c in side[1 - k]:
                            chain = [[c], [c]]
                            for j in (0, 1):
                                while side[j][chain[j][-1]] is not None:
                                    chain[j].append(side[j][chain[j][-1]])
                            return True, chain[0][::-1] + chain[1][1:], len(side[0]), len(side[1]), False
                        heapq.heappush(heaps[k], (len(c), c))
    return False, None, len(side[0]), len(side[1]), not (heaps[0] and heaps[1])


def collins_r2_check():
    """Proposition 10 of research-th02: with a = x, b = yxY, d = ab, t = y the relator
    r2 = xxyxYXyXYXyxY is a^2 b A B A b, i.e. ada = dad, and F/<<r2>> = HNN(B3; t a T = A d).
    p = xyXYYXyXY = (a B) T (A B) freely, eps_x(p) = (A b) T (a b) freely, so p ~ T h, eps_x(p) ~ T h'
    with h = A D a a D a, h' = d A A d.  Collins: conjugate iff h' = b^k h a^-k; abelianizing B3
    forces k = 0; h != h' because their images in SL2(Z) differ."""
    sub = lambda w, m: red("".join(m[c] for c in w))
    m = {"a": "x", "A": "X", "b": "yxY", "B": "yXY", "t": "y", "T": "Y"}
    assert sub("aabABAb", m) == "xxyxYXyXYXyxY"
    assert sub("aBTAB", m) == "xyXYYXyXY" and sub("AbTab", m) == "XyxYYxyxY"
    mm = lambda P, Q: tuple(tuple(sum(P[i][k] * Q[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    A, D, Ai, Di = ((1, 1), (0, 1)), ((1, 0), (-1, 1)), ((1, -1), (0, 1)), ((1, 0), (1, 1))
    assert mm(mm(A, D), A) == mm(mm(D, A), D)                       # braid relation in SL2(Z)
    def ev(w):
        out = ((1, 0), (0, 1))
        for c in w:
            out = mm(out, {"a": A, "d": D, "A": Ai, "D": Di}[c])
        return out
    # b = A d ; a B = a D a ; A B a B = A D a a D a = h ; a b A b = d A A d = h'
    h, h2 = ev("ADaaDa"), ev("dAAd")
    assert h == ((-1, -2), (4, 7)) and h2 == ((3, -2), (-4, 3)) and h != h2
    assert sum(1 if c.islower() else -1 for c in "ADaaDa") == 0 == sum(1 if c.islower() else -1 for c in "dAAd")
    # second partner p'' = xxYxyXYXyy = a a T a (t A T) A t t = a a T a B A t t ~ t (b b a B A); b b a B A = h^-1 in B3
    assert sub("aaTatATAtt", m) == "xxYxyXYXyy" and sub("aaTaBAtt", m) == "xxYxyXYXyy"
    assert mm(ev("AdAdaD"), h) == ((1, 0), (0, 1))
    return True


def collins_r1_search(L, seed=11, sizes=(7, 7, 8, 8, 9)):
    """The open candidate eps_x(s_w) ~ s_w in F/<<R1>>, R1 = xxxyXYYXXyyXY.  With x_i = y^i x y^-i:
    F/<<R1>> = HNN(H; t x0 T = x1, t x1 T = x2), H = <x0,x1,x2 | x1^3 = x2 x0^2 x2>, s_w ~ t x2 x0 and
    eps_x(s_w) ~ t X2 X0.  Collins: conjugate iff  Z(x0,x1) X2 X0 Z(x1,x2)^-1 = x2 x0  in H for a word
    Z(p,q); abelianizing H forces exponent sums (-6, +6), so |Z| >= 12 and |Z| is even.  This function
    tests EVERY reduced word Z of length L with these exponent sums in random finite quotients of H
    (a failing quotient excludes Z rigorously) and returns (number tested, survivors)."""
    import random
    rnd = random.Random(seed)
    mul = lambda a, b: tuple(b[i] for i in a)
    def power(q, k):
        r = tuple(range(len(q)))
        for _ in range(k):
            r = mul(r, q)
        return r
    def order(q):
        k, r, e = 1, q, tuple(range(len(q)))
        while r != e:
            r = mul(r, q); k += 1
        return k
    homs = []
    for n in sizes:
        while True:
            x0 = tuple(rnd.sample(range(n), n)); x1 = tuple(rnd.sample(range(n), n))
            c = mul(power(x1, 3), power(x0, 2)); o = order(c)
            if o % 2:
                x2 = mul(power(c, (o + 1) // 2), _pinv(power(x0, 2)))
                assert mul(mul(x2, power(x0, 2)), x2) == power(x1, 3)      # a homomorphism of H
                homs.append((x0, x1, x2)); break
    def ok(z):
        for x0, x1, x2 in homs:
            a = _pev(z, {"p": x0, "q": x1, "P": _pinv(x0), "Q": _pinv(x1)}, len(x0))
            b = _pev(z, {"p": x1, "q": x2, "P": _pinv(x1), "Q": _pinv(x2)}, len(x0))
            if mul(mul(mul(a, _pinv(x2)), _pinv(x0)), _pinv(b)) != mul(x2, x0):
                return False
        return True
    tested = 0; surv = []
    def gen(k, cnt, word):
        nonlocal tested
        if k == 0:
            tested += 1
            if ok(word):
                surv.append(word)
            return
        for i, ch in enumerate("pPqQ"):
            if cnt[i] and not (word and word[-1] == ch.swapcase()):
                c2 = list(cnt); c2[i] -= 1
                gen(k - 1, c2, word + ch)
    e = (L - 12) // 2
    for ep in range(e + 1):
        gen(L, [ep, 6 + ep, 6 + e - ep, e - ep], "")
    return tested, surv


R1 = "xxxyXYYXXyyXY"          # relator of the state (R1, xyyyxYY) of Fwd(C4, 20); eps_x(R1) ~ R1^-1
SW_ = "xyyyxYY"               # second relator of C4


def self_test():
    eps_x = str.maketrans("xX", "Xx")
    # control 1: hidden reflection beta_A of A = x^4 y X y acts trivially: no quotient separates
    A = "xxxxyXy"; s = "xyyyxYY"
    bs = red("".join({"x": "x", "X": "X", "y": "xYXXXX", "Y": "xxxxyX"}[c] for c in s))
    assert sn_test(A, s, bs, 5)[1] == 0 and sl2_test(A, s, bs, 5)[2] == 0
    # control 2: a wrong partner IS separated (x^8y^5 vs x^7y^5 modulo A)
    assert sn_test(A, "x" * 8 + "y" * 5, "x" * 7 + "y" * 5, 5)[1] > 0
    # control 3: Lemma 3 found by the frozen search; a false statement is not
    assert frozen_search(A, "x" * 8 + "y" * 5, "xYYxyyy", 20, 20)[0]
    f = frozen_search(A, "x" * 7 + "y" * 5, "xYYxyyy", 16, 20)
    assert not f[0] and f[4]
    # control 4: transvection y -> yx on a relator in <x, yxY> is separated in S_6 (not realized by Lemma 0)
    r2 = "xxyxYXyXYXyxY"; p2 = "xyXYYXyXY"
    p2t = cycred("".join({"x": "x", "X": "X", "y": "yx", "Y": "XY"}[c] for c in p2))
    assert sn_test(r2, p2, p2t, 6)[1] > 0
    # the open candidate: eps_x on (R1, s_w): eps_x(R1) ~ R1^-1, and no quotient below separates
    assert canon(R1.translate(eps_x)) == canon(R1)
    assert sn_test(R1, SW_, SW_.translate(eps_x), 6) == (792, 0)
    assert sl2_test(R1, SW_, SW_.translate(eps_x), 7) == (348, 12, 0)
    assert inner_test(R1, 6) == (72, 72)
    collins_r2_check()
    assert collins_r1_search(12) == (924, []) and collins_r1_search(14) == (11088, [])
    print("th02_candidates self-test OK")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--self-test"]:
        self_test()
    elif a[:1] == ["sn"]:
        print("S_%s: homs %d, separating %d" % ((a[4],) + sn_test(a[1], a[2], a[3], int(a[4]))))
    elif a[:1] == ["sl2"]:
        print("SL2(%s): homs %d, nonabelian %d, trace-separating %d" % ((a[4],) + sl2_test(a[1], a[2], a[3], int(a[4]))))
    elif a[:1] == ["inner"]:
        print("S_%s: nontrivial homs %d, with h.eps_x conjugate to h: %d" % ((a[2],) + inner_test(a[1], int(a[2]))))
    elif a[:1] == ["r1"]:
        print("length %s: tested %d words Z, survivors %s" % ((a[1],) + collins_r1_search(int(a[1]))))
    elif a[:1] == ["bfs"]:
        f = frozen_search(a[1], a[2], a[3], int(a[4]), float(a[5]))
        print("found" if f[0] else "not found", f[1], "states", f[2], f[3], "exhausted" if f[4] else "not exhausted")
    else:
        print(__doc__)
