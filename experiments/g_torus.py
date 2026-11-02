#!/usr/bin/env python3
"""Agent G: the torus-knot-pair ACM graph.

Words are strings over x, X=x^-1, y, Y=y^-1.

Background (research/research-g.md, Section 2).
  * A cyclic word is of *torus type* (p,q) if it is the cyclic reduction of
    theta(x^p y^q) for some theta in Aut(F_2).  Since Out(F_2) = GL(2,Z)
    (Nielsen), these words are exactly cyc(theta_M(x^p y^q)), M in GL(2,Z),
    where theta_M is any automorphism with abelianisation M.
  * In G = <x,y | x^p y^q> (|p|,|q| >= 2) the element z = x^p = y^-q is
    central and G/<z> = C_|p| * C_|q|.  Conjugacy in G is decided exactly by
    (z-exponent, cyclic syllable necklace) of a cyclically reduced normal form
    (`torus_class`).  This decides the quotient-conjugacy (ACM) move
        u -> u'   allowed iff  u' ~ u^{+-1} in <x,y | v>
    for a frozen torus-type relator v, with NO bound on conjugators.
  * `edges(U, p, q, ...)` enumerates every torus-type (or primitive) word u'
    with |entries of M| <= K, exponents <= P, length <= maxlen, which is
    conjugate to U^{+-1} in <x,y | x^p y^q>.

Run `python3 experiments/g_torus.py --selftest`.
"""
import itertools
import math
import random
import sys

# ------------------------------------------------------------------ words


def red(w):
    out = []
    for c in w:
        if out and out[-1] == c.swapcase():
            out.pop()
        else:
            out.append(c)
    return "".join(out)


def inv(w):
    return w.swapcase()[::-1]


def cyc(w):
    w = red(w)
    i, j = 0, len(w)
    while j - i >= 2 and w[i] == w[j - 1].swapcase():
        i += 1
        j -= 1
    return w[i:j]


def power(w, k):
    if k >= 0:
        return red(w * k)
    return red(inv(w) * (-k))


def min_rot(w):
    if not w:
        return w
    return min(w[i:] + w[:i] for i in range(len(w)))


def cyc_canon(w):
    """Canonical representative of the cyclic word w up to rotation and inversion."""
    w = cyc(w)
    return min(min_rot(w), min_rot(inv(w)))


def expvec(w):
    return (w.count("x") - w.count("X"), w.count("y") - w.count("Y"))


def apply(aut, w):
    """aut = (image of x, image of y)."""
    wx, wy = aut
    img = {"x": wx, "X": inv(wx), "y": wy, "Y": inv(wy)}
    return red("".join(img[c] for c in w))


# ------------------------------------------------- GL(2,Z) -> Aut(F_2)


def mat_mul(A, B):
    return ((A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]),
            (A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]))


def det(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def mat_inv(M):
    d = det(M)
    assert d in (1, -1)
    return ((M[1][1] * d, -M[0][1] * d), (-M[1][0] * d, M[0][0] * d))


def aut_from_matrix(M):
    """An automorphism (wx, wy) of F_2 whose abelianisation has columns
    expvec(wx) = (M00, M10), expvec(wy) = (M01, M11)."""
    assert det(M) in (1, -1)
    ops = []  # column operations reducing M to I
    A = [list(M[0]), list(M[1])]

    def colop(i, j, k):  # col_i += k col_j
        for r in range(2):
            A[r][i] += k * A[r][j]
        ops.append(("add", i, j, k))

    def swap():
        for r in range(2):
            A[r][0], A[r][1] = A[r][1], A[r][0]
        ops.append(("swap",))

    def neg(i):
        for r in range(2):
            A[r][i] = -A[r][i]
        ops.append(("neg", i))

    while A[0][0] != 0 and A[0][1] != 0:
        if abs(A[0][0]) >= abs(A[0][1]):
            k = -(A[0][0] // A[0][1]) if A[0][0] * A[0][1] > 0 else (abs(A[0][0]) // abs(A[0][1]))
            # choose k so that |A00 + k A01| < |A01|
            k = -int(A[0][0] / A[0][1])
            colop(0, 1, k)
        else:
            k = -int(A[0][1] / A[0][0])
            colop(1, 0, k)
    if A[0][0] == 0:
        swap()
    if A[0][0] < 0:
        neg(0)
    assert A[0][0] == 1 and A[0][1] == 0
    if A[1][1] < 0:
        neg(1)
    assert A[1][1] == 1
    if A[1][0] != 0:
        colop(0, 1, -A[1][0])
    assert A == [[1, 0], [0, 1]], A
    # M * E1...Ek = I  =>  apply inverses in reverse order to (x, y)
    w = ["x", "y"]
    for op in reversed(ops):
        if op[0] == "add":
            _, i, j, k = op
            w[i] = red(w[i] + power(w[j], -k))
        elif op[0] == "swap":
            w[0], w[1] = w[1], w[0]
        else:
            w[op[1]] = inv(w[op[1]])
    assert expvec(w[0]) == (M[0][0], M[1][0]) and expvec(w[1]) == (M[0][1], M[1][1]), (M, w)
    return (w[0], w[1])


def gl2_matrices(K):
    """All M in GL(2,Z) with max |entry| <= K."""
    out = []
    for a in range(-K, K + 1):
        for c in range(-K, K + 1):
            if math.gcd(a, c) != 1:
                continue
            for b in range(-K, K + 1):
                for d in range(-K, K + 1):
                    if a * d - b * c in (1, -1):
                        out.append(((a, b), (c, d)))
    return out


# ------------------------------------------- normal forms in torus groups


def torus_class(w, p, q):
    """Conjugacy invariant of w in G = <x,y | x^p y^q>, |p|,|q| >= 2.
    z := x^p is central, y^q = z^-1.  Returns (zexp, necklace) where necklace
    is the minimal rotation of the cyclic syllable sequence ((gen, e), ...),
    0 < e < order.  Complete invariant (normal form theorem for C_|p|*C_|q|
    and centrality of z)."""
    P, Q = abs(p), abs(q)
    zf = {"x": (1 if p > 0 else -1), "y": (-1 if q > 0 else 1)}  # x^P = z^zf[x], y^Q = z^zf[y]
    order = {"x": P, "y": Q}
    z = 0
    st = []
    w = red(w)
    i = 0
    n = len(w)
    while i < n:
        g = w[i].lower()
        e = 0
        while i < n and w[i].lower() == g:
            e += 1 if w[i] == g else -1
            i += 1
        if st and st[-1][0] == g:
            e += st.pop()[1]
        k, r = divmod(e, order[g])
        z += k * zf[g]
        if r:
            st.append((g, r))
        else:
            # vanished: neighbours (other factor) may now be adjacent to the next run;
            # handled when the next run (other generator) arrives.
            pass
        # merge if the top two are the same generator (possible after a vanish)
        while len(st) >= 2 and st[-1][0] == st[-2][0]:
            g2, e2 = st.pop()
            g1, e1 = st.pop()
            k, r = divmod(e1 + e2, order[g1])
            z += k * zf[g1]
            if r:
                st.append((g1, r))
    # cyclic reduction (conjugation does not change the central exponent)
    dq = st
    while len(dq) >= 2 and dq[0][0] == dq[-1][0]:
        g, e1 = dq.pop(0)
        _, e2 = dq.pop()
        k, r = divmod(e1 + e2, order[g])
        z += k * zf[g]
        if r:
            dq.append((g, r))
    t = tuple(dq)
    if len(t) <= 1:
        return (z, t)
    rots = [t[i:] + t[:i] for i in range(len(t))]
    return (z, min(rots))


def syllables(w, p, q):
    return len(torus_class(w, p, q)[1])


def ab_value(w, p, q):
    """Image of w in H_1(<x,y | x^p y^q>) = Z, x -> q, y -> -p."""
    a, b = expvec(w)
    return q * a - p * b


# ---------------------------------------------- torus-type recognition

_AUT_CACHE = {}


def aut_cached(M):
    a = _AUT_CACHE.get(M)
    if a is None:
        a = _AUT_CACHE[M] = aut_from_matrix(M)
    return a


def torus_word(M, p, q):
    wx, wy = aut_cached(M)
    return cyc(power(wx, p) + power(wy, q))


def edges(U, p, q, mats, P=12, maxlen=80, allow_primitive=True):
    """All (M, p', q', word) with word = cyc(theta_M(x^p' y^q')) torus type
    (|p'|,|q'| >= 2) or primitive, |p'|,|q'| <= P, len <= maxlen, and word
    conjugate to U or U^-1 in <x,y | x^p y^q>."""
    cU = torus_class(U, p, q)
    cUi = torus_class(inv(U), p, q)
    abU = ab_value(U, p, q)
    hits = {}
    for M in mats:
        abx = q * M[0][0] - p * M[1][0]
        aby = q * M[0][1] - p * M[1][1]
        for p2 in range(-P, P + 1):
            if p2 == 0:
                continue
            for target in (abU, -abU):
                num = target - p2 * abx
                if aby == 0:
                    if num != 0:
                        continue
                    q2s = [s for s in range(-P, P + 1) if s != 0]
                else:
                    if num % aby:
                        continue
                    q2s = [num // aby]
                for q2 in q2s:
                    if q2 == 0 or abs(q2) > P or math.gcd(p2, q2) != 1:
                        continue
                    prim = abs(p2) == 1 or abs(q2) == 1
                    if prim and not allow_primitive:
                        continue
                    w = torus_word(M, p2, q2)
                    if len(w) > maxlen or not w:
                        continue
                    c = torus_class(w, p, q)
                    if c == cU or c == cUi:
                        key = cyc_canon(w)
                        if key not in hits or len(hits[key][3]) > len(w):
                            hits[key] = (M, p2, q2, w)
    return list(hits.values())


def partner_defect(M, p2, q2, V):
    """Normalise by theta_M^-1: returns (V', syllable length of V' in C_p2*C_q2)."""
    Vn = cyc(apply(aut_cached(mat_inv(M)), V))
    if abs(p2) < 2 or abs(q2) < 2:
        return Vn, None
    return Vn, syllables(Vn, p2, q2)


# --------------------------------------------------------------- selftest


def _brute_conj_check(rng, trials=300):
    """torus_class agrees with conjugation and with relator insertion."""
    for _ in range(trials):
        p = rng.choice([2, 3, 4, 5, -2, -3, -5])
        q = rng.choice([2, 3, 4, 7, -3, -4, -5])
        if math.gcd(p, q) != 1:
            continue
        rel = power("x", p) + power("y", q)
        w = "".join(rng.choice("xXyY") for _ in range(rng.randint(1, 14)))
        c0 = torus_class(w, p, q)
        g = "".join(rng.choice("xXyY") for _ in range(rng.randint(0, 6)))
        assert torus_class(g + w + inv(g), p, q) == c0
        # insert a rotation of rel^{+-1} at a random place
        r = rel if rng.random() < 0.5 else inv(rel)
        k = rng.randrange(len(r))
        r = r[k:] + r[:k]
        h = "".join(rng.choice("xXyY") for _ in range(rng.randint(0, 4)))
        j = rng.randrange(len(w) + 1)
        w2 = w[:j] + h + r + inv(h) + w[j:]
        assert torus_class(w2, p, q) == c0, (w, w2, p, q)
    return True


def _finite_rep_check(rng, trials=200):
    """Independent check of non-conjugacy: map <x,y|x^p y^q> to a permutation
    group by brute-force search over small symmetric groups; if classes are
    equal, cycle types must agree."""
    import itertools as it
    n = 5
    perms = list(it.permutations(range(n)))

    def mul(a, b):  # a then b
        return tuple(b[a[i]] for i in range(n))

    def pw(a, k):
        r = tuple(range(n))
        if k < 0:
            ai = [0] * n
            for i, v in enumerate(a):
                ai[v] = i
            a = tuple(ai)
            k = -k
        for _ in range(k):
            r = mul(r, a)
        return r

    def ev(w, X, Y):
        r = tuple(range(n))
        m = {"x": X, "X": pw(X, -1), "y": Y, "Y": pw(Y, -1)}
        for c in w:
            r = mul(r, m[c])
        return r

    def ctype(a):
        seen = [False] * n
        t = []
        for i in range(n):
            if not seen[i]:
                L = 0
                j = i
                while not seen[j]:
                    seen[j] = True
                    j = a[j]
                    L += 1
                t.append(L)
        return tuple(sorted(t))

    p, q = 2, -3
    reps = []
    for X in perms:
        for Y in perms:
            if mul(pw(X, p), pw(Y, q)) == tuple(range(n)):
                reps.append((X, Y))
    rng.shuffle(reps)
    reps = reps[:60]
    bad = 0
    for _ in range(trials):
        a = "".join(rng.choice("xXyY") for _ in range(rng.randint(1, 10)))
        b = "".join(rng.choice("xXyY") for _ in range(rng.randint(1, 10)))
        if torus_class(a, p, q) == torus_class(b, p, q):
            for X, Y in reps:
                if ctype(ev(a, X, Y)) != ctype(ev(b, X, Y)):
                    bad += 1
                    break
    assert bad == 0
    return True


def selftest():
    rng = random.Random(2026)
    # aut_from_matrix produces bases with the right abelianisation
    mats = gl2_matrices(6)
    for M in mats:
        wx, wy = aut_from_matrix(M)
    # basis check by Nielsen reduction (Whitehead-free: reduce total length greedily)
    def is_basis(a, b):
        for _ in range(500):
            if sorted([cyc_canon(a), cyc_canon(b)]) in (["X", "Y"], ["X", "y"], ["x", "Y"], ["x", "y"]) \
                    and len(a) == 1 and len(b) == 1:
                return True
            best = None
            for na, nb in ((red(a + b), b), (red(a + inv(b)), b), (red(b + a), b), (red(inv(b) + a), b),
                           (a, red(b + a)), (a, red(b + inv(a))), (a, red(a + b)), (a, red(inv(a) + b))):
                if best is None or len(na) + len(nb) < len(best[0]) + len(best[1]):
                    best = (na, nb)
            if len(best[0]) + len(best[1]) >= len(a) + len(b):
                return len(a) + len(b) == 2 and {a.lower(), b.lower()} == {"x", "y"}
            a, b = best
        return False
    for M in rng.sample(mats, 200):
        assert is_basis(*aut_from_matrix(M)), M
    _brute_conj_check(rng)
    _finite_rep_check(rng)
    # the braid relator is torus type (2,-3): psi(x^2 y^-3) = xyxYXY, psi: x->xyx, y->yx
    assert cyc(apply(("xyx", "yx"), "xxYYY")) == "xyxYXY"
    assert cyc(apply(("xY", "yyX"), "xyxYXY")) == "xxYYY"
    # meridian defect of AK(3) relators (research-f: 6 and 14)
    assert syllables("xyxYXY", 3, -4) == 6
    assert syllables(cyc(apply(("xY", "yyX"), "xxxYYYY")), 2, -3) == 14
    print("g_torus self-test passed: %d matrices, conjugacy invariants checked" % len(mats))


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()


# ------------------------------------------------------------- torus BFS

def _wh():
    import importlib.util, os
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("d_whitehead", os.path.join(here, "d_whitehead.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def node_info(p, q, W, MW, p2, q2):
    """Defects of a normalised node: frozen x^p y^q, other W = cyc(theta_MW(x^p2 y^q2))."""
    R = cyc(power("x", p) + power("y", q))
    d1 = syllables(W, p, q)
    Vn = cyc(apply(aut_cached(mat_inv(MW)), R))
    d2 = syllables(Vn, p2, q2) if abs(p2) >= 2 and abs(q2) >= 2 else None
    prim = abs(p2) == 1 or abs(q2) == 1
    return d1, d2, prim, Vn


def bfs(start, K=8, P=12, maxlen=60, depth=4, max_nodes=20000, log=print):
    """start = (p, q, W, MW, p2, q2).  Returns (nodes, parent, winners)."""
    WH = _wh()
    mats = gl2_matrices(K)
    R0 = cyc(power("x", start[0]) + power("y", start[1]))
    key0 = WH.aut_canon((R0, start[2]))
    nodes = {key0: start}
    parent = {key0: None}
    frontier = [key0]
    winners = []
    for lev in range(1, depth + 1):
        nxt = []
        hist = {}
        for key in frontier:
            p, q, W, MW, p2, q2 = nodes[key]
            R = cyc(power("x", p) + power("y", q))
            d1, d2, prim, Vn = node_info(p, q, W, MW, p2, q2)
            cand = []
            for (M, a, b, w) in edges(W, p, q, mats, P=P, maxlen=maxlen):
                cand.append((p, q, w, M, a, b))
            if abs(p2) >= 2 and abs(q2) >= 2:
                for (M, a, b, w) in edges(Vn, p2, q2, mats, P=P, maxlen=maxlen):
                    cand.append((p2, q2, w, M, a, b))
            for c in cand:
                Rc = cyc(power("x", c[0]) + power("y", c[1]))
                k = WH.aut_canon((Rc, c[2]))
                if k in nodes:
                    continue
                nodes[k] = c
                parent[k] = key
                e1, e2, pr, _ = node_info(*c)
                dm = min([d for d in (e1, e2) if d is not None] + [99])
                hist[dm] = hist.get(dm, 0) + 1
                if pr or e1 == 2 or e2 == 2:
                    winners.append(k)
                nxt.append(k)
                if len(nodes) >= max_nodes:
                    break
            if len(nodes) >= max_nodes:
                break
        log("level %d: new %d, total %d, min-defect histogram %s, winners %d"
            % (lev, len(nxt), len(nodes), sorted(hist.items()), len(winners)))
        frontier = nxt
        if winners or not frontier or len(nodes) >= max_nodes:
            break
    return nodes, parent, winners


# ------------------------------------------- primitive classes (Christoffel)

def christoffel(m, n):
    """The primitive cyclic word with exponent vector (m, n), gcd(m,n) = 1
    (lower Christoffel word, letters inverted according to signs).  By
    Osborne-Zieschang / Nielsen, primitive conjugacy classes of F_2 are in
    bijection with primitive vectors (inverse class <-> -vector)."""
    a, b = abs(m), abs(n)
    assert math.gcd(a, b) == 1
    L = a + b
    out = []
    for i in range(1, L + 1):
        out.append("y" if (i * b) // L != ((i - 1) * b) // L else "x")
    w = "".join(out)
    if m < 0:
        w = w.replace("x", "X")
    if n < 0:
        w = w.replace("y", "Y")
    return w


def primitive_hits(U, p, q, Lmax):
    """All primitive cyclic words of length <= Lmax conjugate to U^{+-1} in
    <x,y | x^p y^q>, by exhaustive enumeration of primitive vectors subject
    to the abelianisation constraint q*m - p*n = +-ab(U)."""
    cU = torus_class(U, p, q)
    cUi = torus_class(inv(U), p, q)
    abU = ab_value(U, p, q)
    hits = []
    g = math.gcd(p, q)
    for m in range(-Lmax, Lmax + 1):
        for t in (abU, -abU):
            # q*m - p*n = t  ->  n = (q*m - t)/p
            num = q * m - t
            if num % p:
                continue
            n = num // p
            if abs(m) + abs(n) > Lmax or (m == 0 and n == 0) or math.gcd(m, n) != 1:
                continue
            w = christoffel(m, n)
            c = torus_class(w, p, q)
            if c == cU or c == cUi:
                hits.append((m, n, w))
    return hits
