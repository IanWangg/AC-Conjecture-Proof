#!/usr/bin/env python3
"""th02_scan.py (agent TH02): find relators of type T(2,n) (Aut(F2)-images of
x^2 y^n, n odd >= 3) in a list of states and compute their hidden reflections.

By Theorem TH02.1 the hidden reflection of ANY such relator of ANY state that
is AC-equivalent to U (without automorphism) lies in the stabilizer S^(U).
Recognition: reduce the single cyclic word by the four type-II Whitehead maps
x->xy, x->xY, y->yx, y->yX (tracking the exponent matrix); the minimal words of
the orbit of x^2 y^n (n >= 3) are exactly the cyclic words with two equal-sign
occurrences of one generator, e^ y^i e^ y^k with i*k <= 0, |i-k| = n.

Usage: python3 experiments/th02_scan.py --self-test
       python3 experiments/th02_scan.py DUMP [--d6]     (lines: w1 w2 ...)
Output: every distinct reflection matrix (rows), its -1 eigenvector (the
abelianization of the relator), n, count, and one example state.
"""
import sys
sys.dont_write_bytecode = True
INV = {"x": "X", "X": "x", "y": "Y", "Y": "y"}
MAPS = [({"x": "xy", "X": "YX"}, ((1, 0), (1, 1))), ({"x": "xY", "X": "yX"}, ((1, 0), (-1, 1))),
        ({"y": "yx", "Y": "XY"}, ((1, 1), (0, 1))), ({"y": "yX", "Y": "xY"}, ((1, -1), (0, 1)))]


def cycred(w):
    out = []
    for c in w:
        if out and out[-1] == INV[c]:
            out.pop()
        else:
            out.append(c)
    w = "".join(out)
    while len(w) >= 2 and w[0] == INV[w[-1]]:
        w = w[1:-1]
    return w


def mmul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def minv(A):
    d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return ((A[1][1] * d, -A[0][1] * d), (-A[1][0] * d, A[0][0] * d))


def reduce_word(w):
    """greedy Whitehead reduction of one cyclic word; returns (min word, M) with
    ab(min) = M ab(w)."""
    w = cycred(w); M = ((1, 0), (0, 1))
    improved = True
    while improved:
        improved = False
        for m, mat in MAPS:
            q = cycred("".join(m.get(c, c) for c in w))
            if len(q) < len(w):
                w, M, improved = q, mmul(mat, M), True
                break
    return w, M


def visible(w):
    """if the cyclic word w is e y^i e y^k (e = x^+-1) or the same with x,y
    exchanged, return (R, n) with R the hidden reflection in these coordinates."""
    for a, b in (("x", "y"), ("y", "x")):
        na, nA = w.count(a), w.count(a.upper())
        if (na, nA) in ((2, 0), (0, 2)) and len(w) > 2:
            e = 1 if na == 2 else -1
            c = a if na == 2 else a.upper()
            k0 = w.index(c); v = w[k0:] + w[:k0]
            k1 = v.index(c, 1)
            ex = lambda s: s.count(b) - s.count(b.upper())
            s1, s2 = v[1:k1], v[k1 + 1:]
            if len(s1) != abs(ex(s1)) or len(s2) != abs(ex(s2)):
                continue
            i, k = ex(s1), ex(s2)
            n = abs(k - i)
            R = ((-1, 0), (-e * (i + k), 1)) if a == "x" else ((1, -e * (i + k)), (0, -1))
            return R, n
    return None


def hidden_reflection(w):
    """(matrix of the hidden reflection of the cyclic word w, n) or None."""
    m, M = reduce_word(w)
    v = visible(m)
    if v is None or v[1] < 3 or v[1] % 2 == 0:
        return None
    return mmul(minv(M), mmul(v[0], M)), v[1]


def closure(gens, limit=2000):
    I = ((1, 0), (0, 1)); seen = {I}; todo = [I]
    while todo and len(seen) <= limit:
        g = todo.pop()
        for h in gens:
            k = mmul(g, h)
            if k not in seen:
                seen.add(k); todo.append(k)
    return seen


D6 = closure([((1, -3), (0, -1)), ((-1, 0), (-1, 1))])     # <beta_A, beta_w> for C4


def _signed_perms():
    out = []
    for swap in (False, True):
        for sx in (1, -1):
            for sy in (1, -1):
                a, b = ("y", "x") if swap else ("x", "y")
                ia = a if sx == 1 else a.upper(); ib = b if sy == 1 else b.upper()
                m = {"x": ia, "X": ia.swapcase(), "y": ib, "Y": ib.swapcase()}
                cx = (0, sx) if swap else (sx, 0); cy = (sy, 0) if swap else (0, sy)
                out.append((m, ((cx[0], cy[0]), (cx[1], cy[1]))))
    return out


def stab_order(w, limit=20000):
    """order of the stabilizer in GL2(Z) of the cyclic word w up to inversion, by BFS through the
    level set of its Whitehead-minimal form (peak reduction); None if more than `limit` states."""
    inv = lambda u: "".join(INV[c] for c in reversed(u))
    canon = lambda u: min(t[k:] + t[:k] for t in (u, inv(u)) for k in range(len(u)))
    w0 = canon(reduce_word(w)[0]); L = len(w0); I = ((1, 0), (0, 1))   # stabilizers of w and its minimal form are conjugate
    moves = MAPS + _signed_perms()
    seen = {(w0, I)}; todo = [(w0, I)]
    while todo:
        c, M = todo.pop()
        for m, mat in moves:
            q = cycred("".join(m.get(ch, ch) for ch in c))
            assert len(q) >= L, "word was not minimal"
            if len(q) == L:
                st = (canon(q), mmul(mat, M))
                if st not in seen:
                    seen.add(st); todo.append(st)
                    if len(seen) > limit:
                        return None
    return len({M for c, M in seen if c == w0})


def self_test():
    import random
    rnd = random.Random(5)
    assert len(D6) == 12
    for p, q, order in ((3, 4, 2), (3, 5, 2), (4, 5, 2), (3, 7, 2), (5, 7, 2), (5, 8, 2),
                        (2, 3, 4), (2, 5, 4), (2, 7, 4), (2, 9, 4)):
        assert stab_order("x" * p + "y" * q) == order, (p, q, stab_order("x" * p + "y" * q))
    assert stab_order("xyxYXY") == 4 and stab_order("xxxxyXy") == 4 and stab_order("xYYxyyy") == 4
    assert stab_order("x") is None                      # primitive: infinite stabilizer
    assert hidden_reflection("xxxxyXy") == (((1, -3), (0, -1)), 5)
    assert hidden_reflection("xyyyxYY") == (((-1, 0), (-1, 1)), 5)
    assert hidden_reflection("xxyXy") == (((1, -1), (0, -1)), 3)
    assert hidden_reflection("xyxYXY") == (((0, 1), (1, 0)), 3)      # braid relator: the swap
    for bad in ("xxxyyyy", "xxxxxxxxyyyyy", "xxyy", "xy", "xxxYXyy", "xyxyxYY", "xxxYYYY"):
        assert hidden_reflection(bad) is None, bad
    gens = [({"x": "xy", "X": "YX"}, ((1, 0), (1, 1))), ({"y": "yx", "Y": "XY"}, ((1, 1), (0, 1))),
            ({"x": "X", "X": "x"}, ((-1, 0), (0, 1))), ({"x": "y", "y": "x", "X": "Y", "Y": "X"}, ((0, 1), (1, 0)))]
    for _ in range(400):
        n = rnd.choice([3, 5, 7, 9, 11])
        w = "xx" + "y" * n; R = ((-1, 0), (-n, 1)); M = ((1, 0), (0, 1))
        for _ in range(rnd.randint(0, 7)):
            m, mat = rnd.choice(gens)
            w = cycred("".join(m.get(c, c) for c in w)); M = mmul(mat, M)
        got = hidden_reflection(w)
        assert got == (mmul(M, mmul(R, minv(M))), n), (w, got)
    print("th02_scan self-test OK (400 planted T(2,n) words, 7 negative controls, braid relator = swap)")


def scan(path, d6):
    found = {}; states = 0; with_t2 = 0; cache = {}
    for line in open(path):
        p = line.split()
        if len(p) < 2:
            continue
        states += 1; hit = False
        for w in p[:2]:
            if w not in cache:
                cache[w] = hidden_reflection(w)
            h = cache[w]
            if h:
                hit = True
                rec = found.setdefault(h[0], [h[1], 0, p[0] + " " + p[1]])
                rec[1] += 1
        with_t2 += hit
    print("states %d (distinct relator words %d), states with a T(2,n)-type relator %d, distinct reflections %d"
          % (states, len(cache), with_t2, len(found)))
    for R, (n, cnt, ex) in sorted(found.items(), key=lambda t: -t[1][1]):
        tag = ("in D6" if R in D6 else "NOT in D6") if d6 else ""
        print(R, "n=%d" % n, "count=%d" % cnt, tag, "e.g.", ex)
    G = closure(list(found))
    print("group generated by the reflections found: order", len(G) if len(G) <= 2000 else "> 2000 (infinite)")
    full, word = generates_gl2(list(found))
    print("contains swap, x->X, x->xy (i.e. equals GL2(Z)):", full)
    if full:
        for name, w in word.items():
            print("  %s = product of reflections %s" % (name, w))
    return found


NIELSEN = {"swap": ((0, 1), (1, 0)), "invx": ((-1, 0), (0, 1)), "x_xy": ((1, 0), (1, 1))}


def generates_gl2(gens, bound=40, limit=400000):
    """bounded BFS (entries <= bound): does <gens> contain the three Nielsen matrices?
    Returns (True, words) with explicit words in the generators, or (False, {})."""
    I = ((1, 0), (0, 1)); seen = {I: ()}; todo = [I]; want = dict(NIELSEN); got = {}
    while todo and len(seen) < limit and len(got) < len(want):
        nxt = []
        for g in todo:
            for h in gens:
                k = mmul(g, h)
                if k in seen or max(abs(e) for r in k for e in r) > bound:
                    continue
                seen[k] = seen[g] + (h,)
                nxt.append(k)
                for name, m in want.items():
                    if k == m and name not in got:
                        got[name] = seen[k]
        todo = nxt
    return len(got) == len(want), got


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    elif len(sys.argv) > 1:
        scan(sys.argv[1], "--d6" in sys.argv)
    else:
        print(__doc__)
