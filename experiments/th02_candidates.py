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
    elif a[:1] == ["bfs"]:
        f = frozen_search(a[1], a[2], a[3], int(a[4]), float(a[5]))
        print("found" if f[0] else "not found", f[1], "states", f[2], f[3], "exhausted" if f[4] else "not exhausted")
    else:
        print(__doc__)
