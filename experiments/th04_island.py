#!/usr/bin/env python3
"""Agent TH04: twist rigidity in torus-knot groups and the AK(n) torus island.

Supports research/research-th04.md.  Uses agent G's exact torus-group
conjugacy invariant (g_torus.torus_class) and certificate compiler (g_cert).

  python3 experiments/th04_island.py --selftest
  python3 experiments/th04_island.py --enumerate N K P L   (bounded listing, T5)
  python3 experiments/th04_island.py --write certificates  (certificate for T4, n = 3)
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

if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif sys.argv[1:2] == ["--enumerate"]:
        enumerate_island(*[int(a) for a in sys.argv[2:6]])
    elif sys.argv[1:2] == ["--write"]:
        write_cert(sys.argv[2])
    else:
        print(__doc__)
