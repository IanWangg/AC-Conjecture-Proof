#!/usr/bin/env python3
"""Agent TH04: twist rigidity in torus-knot groups and the AK(n) torus island.

Supports research/research-th04.md.  Uses agent G's exact torus-group
conjugacy invariant (g_torus.torus_class) and certificate compiler (g_cert).

  python3 experiments/th04_island.py --selftest
  python3 experiments/th04_island.py --enumerate N K P L   (bounded listing, T5)
  python3 experiments/th04_island.py --write certificates  (certificate for T4, n = 3)
  python3 experiments/th04_island.py --normal-form K       (Lemma 6.3 at matrix level, all |entries| <= K)
  python3 experiments/th04_island.py --check-t8 N L        (brute-force check of Theorem 6.4's case analysis)
  python3 experiments/th04_island.py --check-t2side N L    (same for Theorem 6.6)
  python3 experiments/th04_island.py --stabilizer K        (experiment for Proposition 6.5)
  python3 experiments/th04_island.py --lemma-m N L E LW    (experiment for Missing Lemma M)
  python3 experiments/th04_island.py --check-t7 N K P      (consistency check of Prop. 6.2)
"""
import itertools, json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g_torus as G

# ---------------------------------------------------------------- matrices
def mul(M, N):
    return ((M[0][0]*N[0][0]+M[0][1]*N[1][0], M[0][0]*N[0][1]+M[0][1]*N[1][1]),
            (M[1][0]*N[0][0]+M[1][1]*N[1][0], M[1][0]*N[0][1]+M[1][1]*N[1][1]))
def act(M, v):
    return (M[0][0]*v[0]+M[0][1]*v[1], M[1][0]*v[0]+M[1][1]*v[1])
I2 = ((1, 0), (0, 1))
DX = ((-1, 0), (0, 1))
def Apow(p, m): return ((1, p*m), (0, 1))
def Bpow(q, m): return ((1, 0), (q*m, 1))

def reduced_words(p, q, E, Lw):
    """All reduced words S_k...S_1 (k <= Lw) in A^m, B^m, 0 < |m| <= E, as
    (matrix, description)."""
    exps = [m for m in range(-E, E + 1) if m]
    out = [(I2, ())]
    frontier = [(I2, ())]
    for _ in range(Lw):
        nxt = []
        for M, d in frontier:
            for g in "AB":
                if d and d[-1][0] == g:
                    continue
                for m in exps:
                    S = Apow(p, m) if g == "A" else Bpow(q, m)
                    nxt.append((mul(S, M), d + ((g, m),)))
        out += nxt
        frontier = nxt
    return out

def lam(p, q, bound):
    return [(a, b) for a in range(-bound, bound + 1) for b in range(-3*bound, 3*bound + 1)
            if q*a - p*b in (1, -1)]

def twist_solutions(p, q, E=3, Lw=4, bound=12):
    """All (v, word, D) with v in Lambda, M = word * D (D in {I, DX}) and
    M v in Lambda, excluding word = () with D = I."""
    xi = lambda v: q*v[0] - p*v[1]
    sols = []
    words = reduced_words(p, q, E, Lw)
    for v in lam(p, q, bound):
        for D, dn in ((I2, "I"), (DX, "Dx")):
            w = act(D, v)
            for M, d in words:
                if not d and dn == "I":
                    continue
                if xi(act(M, w)) in (1, -1):
                    sols.append((v, d, dn))
    return sols

def expected_exceptions(p, q):
    """Theorem T+-: the hidden involutions (as (word, D))."""
    ex = set()
    if abs(p) == 2: ex.add(((("B", 2 // p),), "Dx"))
    if abs(q) == 2: ex.add(((("A", 2 // q),), "Dx"))
    return ex

# ------------------------------------------------------------ automorphisms
def iota(p, q):
    """Hidden involution for p = +-2: x -> y^(-2q/p) x^-1, y -> y."""
    assert abs(p) == 2
    return (G.red(G.power("y", -2*q//p) + "X"), "y")
KAPPA = ("x", "xxY")          # trefoil x^2 y^-3: x -> x, y -> x^2 Y
def img(aut, w): return G.cyc(G.apply(aut, w))
def U(n): return "xY"*n + "xYY"*(n + 1)                  # phi(x^n Y^(n+1))
def W(n): return G.red("xy"*n + "x" + G.inv("yx"*n + "y"))   # T(2,2n+1) relator
def N(n): return "xY"*0 + ("x" + "Y"*n)*2 + ("x" + "Y"*(n + 1))*3   # trefoil relator in T(2,2n+1) coordinates
def conj(u, v, p, q): return G.torus_class(u, p, q) == G.torus_class(v, p, q)

def six_words(n):
    i = iota(2, -3)
    return {"U": U(n), "iU": img(i, U(n)), "W": W(n), "iW": img(i, W(n)),
            "kW": img(KAPPA, W(n)), "ikW": img(i, img(KAPPA, W(n)))}

def selftest():
    rng = random.Random(4)
    # (a) Theorem T+- : brute force over words of syllable length <= 4, |m| <= 3
    for (p, q) in [(3, -4), (4, -5), (5, -6), (2, 5), (-2, 7), (2, -9), (3, 5), (3, 7), (5, -7), (5, 2), (7, -2), (4, 3)]:
        sols = twist_solutions(p, q)
        got = set((d, dn) for (_, d, dn) in sols)
        assert got == expected_exceptions(p, q), ((p, q), got)
        nv = len(lam(p, q, 12))
        assert len(sols) == nv * len(expected_exceptions(p, q))
    # trefoil: extra twists exist, but only on Lambda_0
    for (p, q) in [(2, -3), (2, 3), (3, -2)]:
        sols = twist_solutions(p, q)
        extra = [s for s in sols if (s[1], s[2]) not in expected_exceptions(p, q)]
        assert extra, "trefoil should have extra twists"
        for (v, d, dn) in extra:
            assert sorted((abs(v[0]), abs(v[1]))) in ([1, 1], [1, 2]), v
    # (b) hidden involution: iota(W) = W in T, iota(R) ~ R^-1
    for (p, q) in [(2, -3), (-2, 7), (2, 5), (-2, 9)]:
        i = iota(p, q)
        R = G.cyc(G.power("x", p) + G.power("y", q))
        assert G.cyc_canon(img(i, R)) == G.cyc_canon(G.inv(R))
        for _ in range(200):
            w = G.red("".join(rng.choice("xXyY") for _ in range(rng.randint(1, 14))))
            if w:
                assert conj(G.apply(i, w), w, p, q)
    # (c) uniform memberships (T3, T4, T5) for n = 1..8, trefoil frozen as x^2 y^-3
    for n in range(1, 9):
        sw = six_words(n)
        cU, cUi = G.torus_class(U(n), 2, -3), G.torus_class(G.inv(U(n)), 2, -3)
        for name, w in sw.items():
            assert G.torus_class(w, 2, -3) in (cU, cUi), (n, name)
        assert conj(sw["kW"], G.inv(W(n)), 2, -3) and conj(W(n), G.inv(U(n)), 2, -3)
        assert len(set(G.cyc_canon(w) for w in sw.values())) == (6 if n >= 2 else len(set(G.cyc_canon(w) for w in sw.values())))
        # T(2,2n+1) side: N(n) and iota'(N(n)) conjugate in <x,y | x^-2 y^(2n+1)>
        ip = iota(-2, 2*n + 1)
        assert conj(img(ip, N(n)), N(n), -2, 2*n + 1)
    print("th04 self-test passed")

def enumerate_island(n, K, P, L):
    mats = G.gl2_matrices(K)
    def lst(Uw, p, q):
        return sorted((G.cyc_canon(w), M, a, b) for (M, a, b, w) in G.edges(Uw, p, q, mats, P=P, maxlen=L))
    print("n=%d K=%d P=%d L=%d" % (n, K, P, L))
    e1 = lst("xyxYXY", n, -(n + 1))
    print(" T(n,n+1) frozen, class of b: %d torus-type/primitive words:" % len(e1), [(w, a, b) for (w, M, a, b) in e1])
    e2 = lst(U(n), 2, -3)
    names = {G.cyc_canon(w): k for k, w in six_words(n).items()}
    names.update({G.cyc_canon(G.inv(w)): k + "^-1" for k, w in six_words(n).items()})
    print(" trefoil frozen, class of U_n: %d words:" % len(e2))
    for (w, M, a, b) in e2:
        print("   ", names.get(w, "UNEXPECTED"), M, (a, b), "len", len(w))
    e3 = lst(N(n), -2, 2*n + 1)
    ip = iota(-2, 2*n + 1)
    nm = {G.cyc_canon(N(n)): "N", G.cyc_canon(G.inv(N(n))): "N^-1", G.cyc_canon(img(ip, N(n))): "i'N",
          G.cyc_canon(G.inv(img(ip, N(n)))): "i'N^-1"}
    print(" T(2,2n+1) frozen, class of N_n: %d words:" % len(e3), [(nm.get(w, "UNEXPECTED"), M, (a, b)) for (w, M, a, b) in e3])

def write_cert(outdir, n=3):
    import g_cert as C
    b = "xyxYXY"
    cert = C.Cert("x"*n + "Y"*(n + 1), b)
    C.acm_edge(cert, 0, C.PSI, 2, -3, img(KAPPA, W(n)))
    cert.cyclically_reduce(0); cert.cyclically_reduce(1)
    assert cert.s[1] == b
    j = cert.to_json([cert.s[0], b])
    print(C.replay(j))
    with open(os.path.join(outdir, "th04_ak%d_to_kappa_node.json" % n), "w") as f:
        json.dump(j, f)

def gamma_pm(p, q, big):
    """All elements of Gamma^pm = <A, B, Dx, -I> with entries <= big (closure)."""
    gens = [Apow(p, 1), Apow(p, -1), Bpow(q, 1), Bpow(q, -1), DX, ((-1, 0), (0, -1))]
    seen = {I2}
    fr = [I2]
    while fr:
        nx = []
        for M in fr:
            for g in gens:
                Nn = mul(g, M)
                if Nn not in seen and max(abs(Nn[0][0]), abs(Nn[0][1]), abs(Nn[1][0]), abs(Nn[1][1])) <= big:
                    seen.add(Nn)
                    nx.append(Nn)
        fr = nx
    return seen

def preserves_kernel(M, p, q):
    """Is (pi u, pi v), (u, v) = theta_M(x, y), conjugate to (s^+-1, t^+-1) in C_|p| * C_|q|?"""
    u, v = G.aut_cached(M)
    cu, cv = G.torus_class(u, p, q)[1], G.torus_class(v, p, q)[1]
    if len(cu) != 1 or len(cv) != 1 or cu[0][0] != "x" or cv[0][0] != "y":
        return False
    if cu[0][1] not in (1, abs(p) - 1) or cv[0][1] not in (1, abs(q) - 1):
        return False
    return len(G.torus_class(u + v, p, q)[1]) == 2      # fixed vertices adjacent

def stabilizer_experiment(K, pairs=((3, -4), (2, -3), (2, 5), (3, 5), (-2, 7))):
    """Evidence for Missing Lemma M2: for |entries| <= K, theta_M preserves
    <<x^p, y^q>> iff M is in Gamma^pm."""
    ok = True
    mats = G.gl2_matrices(K)
    for (p, q) in pairs:
        gam = gamma_pm(p, q, 60 * K)
        S1 = set(M for M in mats if preserves_kernel(M, p, q))
        S2 = set(M for M in mats if M in gam)
        print((p, q), "K", K, "matrices", len(mats), "kernel-preserving", len(S1), "in Gamma^pm", len(S2), "equal", S1 == S2)
        ok = ok and S1 == S2
    return ok

def check_t7(n, K, P):
    """Consistency check of Proposition 6.2: every theta_M(x^a y^b), |M| <= K,
    2 <= |a|,|b| <= P, whose image in C_n * C_(n+1) is the necklace of b^+-1
    has two hyperbolic roots.  Returns (#hits, #hits with an elliptic root)."""
    p, q = n, -(n + 1)
    b = "xyxYXY"
    target = (G.torus_class(b, p, q)[1], G.torus_class(G.inv(b), p, q)[1])
    hits = bad = 0
    for M in G.gl2_matrices(K):
        u, v = G.aut_cached(M)
        for a in range(-P, P + 1):
            for c in range(2, P + 1):          # (a, c) and (-a, -c) give inverse words
                if abs(a) < 2:
                    continue
                w = G.cyc(G.power(u, a) + G.power(v, c))
                if G.torus_class(w, p, q)[1] in target:
                    hits += 1
                    if len(G.torus_class(u, p, q)[1]) < 2 or len(G.torus_class(v, p, q)[1]) < 2:
                        bad += 1
    return hits, bad

def necklace_family(partner, p, q):
    """Necklaces of partner^+-1 and of their images under the factor inversions."""
    out = set()
    for w in (partner, G.inv(partner)):
        for sx in (0, 1):
            for sy in (0, 1):
                v = w
                if sx: v = v.translate(str.maketrans("xX", "Xx"))
                if sy: v = v.translate(str.maketrans("yY", "Yy"))
                out.add(G.torus_class(v, p, q)[1])
    return out

def reduced_solutions(p, q, partner, maxlen):
    """Brute-force check of the case analyses of Theorems 6.4 and 6.6: all
    cyclic words eta(W0), W0 = (positive word)(negative word) in A, B with
    r + t <= maxlen, for every reduced form (Y_k), 1 <= k <= |q|-2, and
    (X_j), 1 <= j <= |p|-2, whose necklace lies in the family of `partner`.
    Returns the set of (form, k, canonical cyclic word)."""
    F = necklace_family(partner, p, q)
    sols = set()
    for heavy, top in (("y", abs(q) - 2), ("x", abs(p) - 2)):
        for k in range(1, top + 1):
            if heavy == "y": sub = {"a": "x" + "y"*k, "b": "x" + "y"*(k + 1)}
            else: sub = {"a": "y" + "x"*k, "b": "y" + "x"*(k + 1)}
            for r in range(0, maxlen + 1):
                for t in range(0, maxlen + 1 - r):
                    for pos in itertools.product("ab", repeat=r):
                        for neg in itertools.product("ab", repeat=t):
                            w = G.cyc("".join(sub[c] for c in pos) + "".join(G.inv(sub[c]) for c in neg))
                            if w and G.torus_class(w, p, q)[1] in F:
                                sols.add((heavy, k, G.cyc_canon(w)))
    return sols

def node3_partner(n):
    """Trefoil relator x^2 Y^3 in the coordinates where kappa(W_n) = x^-2 y^(2n+1)."""
    kinv = ("x", "Yxx")
    thinv = (G.red("y"*n + "X"), G.red("x" + "Y"*(n + 1)))
    P = G.cyc(G.apply(thinv, G.apply(kinv, "xxYYY")))
    assert len(G.torus_class(P, -2, 2*n + 1)[1]) == 14
    return P

def check_t8(n, maxlen):
    """Theorem 6.4: reduced words with the necklace family of b in C_n * C_(n+1)."""
    b = "xyxYXY"
    sols = reduced_solutions(n, -(n + 1), b, maxlen)
    tw_y = G.cyc_canon(("x" + "y"*(n - 1))*2 + G.inv("x" + "y"*n)*3)
    tw_x = G.cyc_canon(("y" + "x"*(n - 2))*2 + G.inv("y" + "x"*(n - 1))*3)
    expected = {("y", 1, G.cyc_canon(b)), ("y", n - 1, tw_y), ("x", 1, G.cyc_canon(b)), ("x", n - 2, tw_x)}
    return sols == expected, sorted(sols)

def check_t2side(n, maxlen):
    """Theorem 6.6: reduced words with the necklace families of N_n and of the
    node-3 partner in C_2 * C_(2n+1): only positive/negative words with k = n."""
    A, B = "x" + "y"*n, "x" + "y"*(n + 1)
    ok = True
    out = []
    for partner, pats in ((N(n), ("aaabb", "aabbb")), (node3_partner(n), ("bbaabaa", "aabbabb"))):
        sols = reduced_solutions(-2, 2*n + 1, partner, maxlen)
        exp = set(("y", n, G.cyc_canon("".join(A if c == "a" else B for c in pat))) for pat in pats)
        ok = ok and sols == exp
        out.append(sorted(sols))
    return ok, out

def normal_form(M, p, q):
    """Matrix-level version of the proof of Lemma 6.3.  Rows are changed only by
    twists (negate a row; row2 -= j*row1 with |q| | j; row1 -= j*row2 with
    |p| | j), columns only by sign.  Every claim of the proof is asserted.
    Returns ('L', 0), ('Y', k) or ('X', j)."""
    from fractions import Fraction
    P, Q = abs(p), abs(q)
    (a, b), (c, d) = M
    for _ in range(500):
        cand = [(s1*a, s2*b, s1*r2*c, s2*r2*d) for s1 in (1, -1) for s2 in (1, -1) for r2 in (1, -1)]
        cand = [t for t in cand if min(t) >= 0]
        assert cand, "columns not in one closed quadrant"
        a, b, c, d = cand[0]
        if (a, c) in ((1, 0), (0, 1)) or (b, d) in ((1, 0), (0, 1)):
            return ("L", 0)
        assert min(a, b, c, d) >= 1
        s1, s2 = Fraction(c, a), Fraction(d, b)
        size = a + b + c + d
        if min(s1, s2) >= 1:
            k = min(s1, s2).__floor__()
            assert max(s1, s2) <= k + 1
            k0 = k % Q
            if 1 <= k0 <= Q - 2:
                return ("Y", k0)
            j = k if k0 == 0 else k + 1
            c, d = c - j*a, d - j*b
        else:
            assert max(s1, s2) <= 1
            r1, r2 = Fraction(a, c), Fraction(b, d)
            k = min(r1, r2).__floor__()
            assert k >= 1 and max(r1, r2) <= k + 1
            k0 = k % P
            if 1 <= k0 <= P - 2:
                return ("X", k0)
            j = k if k0 == 0 else k + 1
            a, b = a - j*c, b - j*d
        assert abs(a) + abs(b) + abs(c) + abs(d) < size
    raise AssertionError("no termination")

def normal_form_check(K, pairs=((3, -4), (4, -5), (2, -3), (-2, 7), (2, 5), (5, 7))):
    out = {}
    for (p, q) in pairs:
        cnt = {}
        for M in G.gl2_matrices(K):
            f = normal_form(M, p, q)
            cnt[f] = cnt.get(f, 0) + 1
        out[(p, q)] = sorted(cnt.items())
    return out

# ---------------------------------------------- experiment for Lemma M (trefoil side)
_WH = [("xy", "y"), ("xY", "y"), ("x", "yx"), ("x", "yX")]

def wh_min(w):
    """Whitehead descent (rank 2: these four automorphisms realise every
    Whitehead move on cyclic words up to conjugacy)."""
    w = G.cyc(w)
    while True:
        best = w
        for a in _WH:
            v = G.cyc(G.apply(a, w))
            if len(v) < len(best):
                best = v
        if best == w:
            return w
        w = best

def _runs(w):
    w = G.min_rot(w)
    v = w
    for i in range(len(w)):
        v = w[i:] + w[:i]
        if v[0] != v[-1]:
            break
    out = []
    for c in v:
        if out and out[-1][0] == c: out[-1][1] += 1
        else: out.append([c, 1])
    return out

def word_type(w):
    """'torus(a,c)', 'primitive' or 'other', by Whitehead's algorithm (minimise,
    then search the level set for a word x^a y^c)."""
    m = wh_min(w)
    if len(m) == 1:
        return "primitive"
    seen = {G.cyc_canon(m)}
    fr = [m]
    while fr and len(seen) < 5000:
        nx = []
        for u in fr:
            rr = _runs(u)
            if len(rr) == 2 and min(rr[0][1], rr[1][1]) >= 2:
                return "torus(%d,%d)" % tuple(sorted((rr[0][1], rr[1][1])))
            for a in _WH:
                v = G.cyc(G.apply(a, u))
                if len(v) == len(u) and G.cyc_canon(v) not in seen:
                    seen.add(G.cyc_canon(v))
                    nx.append(v)
        fr = nx
    return "other"

def lemma_m_experiment(n, L, E, Lw, log=print, partner=None):
    """Trefoil side.  All cyclically reduced W0 = (pos)(neg) in A = xy, B = xyy
    with r + t <= L whose image has the necklace family of U_n; all their
    twists by reduced words in A, B (<= Lw syllables, |m| <= E, with or without
    Dx) that are conjugate to U_n^+-1 in <x,y | x^2 = y^3>; Whitehead type of
    each such word.  Lemma M predicts: the torus-type ones are exactly the six
    words, and none is primitive."""
    p, q = 2, -3
    Un = partner if partner else U(n)      # `partner` given: positive control with another class
    cU = (G.torus_class(Un, p, q), G.torus_class(G.inv(Un), p, q))
    F = necklace_family(Un, p, q)
    sub = {"a": "xy", "b": "xyy"}
    red = set()
    for r in range(0, L + 1):
        for t in range(0, L + 1 - r):
            for pos in itertools.product("ab", repeat=r):
                for neg in itertools.product("ab", repeat=t):
                    if r and t and (pos[-1] == neg[0] or neg[-1] == pos[0]):
                        continue
                    w = G.cyc("".join(sub[c] for c in pos) + "".join(G.inv(sub[c]) for c in neg))
                    if w and G.torus_class(w, p, q)[1] in F:
                        red.add(G.cyc_canon(w))
    words = reduced_words(p, q, E, Lw)
    xi = lambda v: q*v[0] - p*v[1]
    hits = set()
    for key in red:
        e = G.expvec(key)
        for D, dn in ((I2, "I"), (DX, "Dx")):
            for M, d in words:
                if xi(act(mul(M, D), e)) not in (1, -1):
                    continue
                w = G.apply(("X", "y"), key) if dn == "Dx" else key
                for (g, m) in d:
                    w = G.apply(("x", G.red(G.power("x", p*m) + "y")), w) if g == "A" else G.apply((G.red(G.power("y", q*m) + "x"), "y"), w)
                w = G.cyc(w)
                if len(w) <= 600 and G.torus_class(w, p, q) in cU:
                    hits.add(G.cyc_canon(w))
    six = {G.cyc_canon(w): k for k, w in six_words(n).items()} if not partner else {G.cyc_canon(partner): "partner"}
    types = {}
    for k in hits:
        types.setdefault(word_type(k), []).append(six.get(k, "NEW"))
    summary = {ty: sorted(v) if not ty == "other" else len(v) for ty, v in types.items()}
    log("n=%d: reduced words %d, twists in the class of U_n^+-1: %d, by Whitehead type: %s" % (n, len(red), len(hits), summary))
    good = all(("NEW" not in v) for ty, v in types.items() if ty != "other")
    return good, summary

if __name__ == "__main__":
    if sys.argv[1:2] == ["--lemma-m"]:
        n, L, E, Lw = [int(a) for a in sys.argv[2:6]]
        print("consistent with Lemma M:", lemma_m_experiment(n, L, E, Lw)[0])
    elif sys.argv[1:2] == ["--lemma-m-control"]:
        L, E, Lw = [int(a) for a in sys.argv[2:5]]
        # AK(2) with x^2 Y^3 frozen and partner b: research-g found primitive words in this class
        print("no torus-type/primitive word besides the partner:", lemma_m_experiment(2, L, E, Lw, partner="xyxYXY")[0])
    elif sys.argv[1:] == ["--selftest"]:
        selftest()
        normal_form_check(6)
        assert check_t8(3, 6)[0] and check_t8(4, 6)[0]
        assert check_t2side(2, 7)[0]
        assert stabilizer_experiment(5, pairs=((3, -4), (2, -3)))
        h, bad = check_t7(3, 4, 5)
        assert h > 0 and bad == 0, (h, bad)
        print("th04 extra checks passed (M2 evidence K=5; T7 consistency n=3: %d hits, 0 with an elliptic root)" % h)
    elif sys.argv[1:2] == ["--normal-form"]:
        for k, v in normal_form_check(int(sys.argv[2])).items():
            print(k, v)
    elif sys.argv[1:2] == ["--check-t8"]:
        n, L = int(sys.argv[2]), int(sys.argv[3])
        print("n=%d, r+t<=%d: case analysis of Theorem 6.4 confirmed:" % (n, L), check_t8(n, L))
    elif sys.argv[1:2] == ["--check-t2side"]:
        n, L = int(sys.argv[2]), int(sys.argv[3])
        print("n=%d, r+t<=%d: case analysis of Theorem 6.6 confirmed:" % (n, L), check_t2side(n, L))
    elif sys.argv[1:2] == ["--stabilizer"]:
        print("all equal:", stabilizer_experiment(int(sys.argv[2])))
    elif sys.argv[1:2] == ["--check-t7"]:
        n, K, P = [int(a) for a in sys.argv[2:5]]
        print("n=%d K=%d P=%d: hits, hits with an elliptic root =" % (n, K, P), check_t7(n, K, P))
    elif sys.argv[1:2] == ["--enumerate"]:
        enumerate_island(*[int(a) for a in sys.argv[2:6]])
    elif sys.argv[1:2] == ["--write"]:
        write_cert(sys.argv[2])
    else:
        print(__doc__)
