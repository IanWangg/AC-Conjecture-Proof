#!/usr/bin/env python3
"""Research agent TH13 (round 5): the two-parameter Akbulut-Kirby family

    AK(k;p) = ( x^p y^-(p+1) ,  W_k ),   W_k = (xy)^k x ((yx)^k y)^-1,

and its dual D(k;p) = ( (y^k x)^p y^k ((x y^k)^p x)^-1 , x^2 y^-(2k+1) ).
Standard library only; imports G's exact torus-group tools read-only.

  python3 experiments/th13_family.py --selftest      (about 1 minute)
  python3 experiments/th13_family.py --write certificates
  python3 experiments/th13_family.py --mirror certificates   (needs the two d_certify outputs, see the note)
  python3 experiments/th13_family.py --islands       (bounded experiment, ~40 s)
  python3 experiments/th13_family.py --exits         (exact brute force, ~2.5 min)
"""
import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g_torus as T  # noqa: E402
import g_cert as C  # noqa: E402
from g_torus import red, inv, cyc, apply, torus_class  # noqa: E402

IDENT = ("x", "y")


def W(k):
    """Wirtinger/Artin relator of T(2,2k+1): (xy)^k x Y (XY)^k."""
    return red("xy" * k + "x" + inv("yx" * k + "y"))


def pw(p):
    return "x" * p + "Y" * (p + 1)


def qw(p):
    return "y" * p + "X" * (p + 1)


def AK(k, p):
    return (pw(p), W(k))


def psi(k):
    """psi_k: x -> x(xy)^k, y -> xy; psi_k(x^2 y^-(2k+1)) is a rotation of W_k."""
    return ("x" + "xy" * k, "xy")


def phi(k):
    """phi_k = psi_k^-1: x -> x y^-k, y -> y^k x^-1 y."""
    return ("x" + "Y" * k, "y" * k + "Xy")


def V(k, p):
    """Artin relator of length 2p+1 in (x, y^k): (y^k x)^p y^k ((x y^k)^p x)^-1."""
    c = "y" * k
    return red((c + "x") * p + c + inv(("x" + c) * p + "x"))


def dual(k, p):
    return (V(k, p), "xx" + "Y" * (2 * k + 1))


def artin(i, j, m):
    """(x^i y^j)^m x^i ((y^j x^i)^m y^j)^-1 for integers i, j."""
    a = T.power("x", i)
    b = T.power("y", j)
    return red((a + b) * m + a + inv((b + a) * m + b))


def to_ints(w):
    return tuple({"x": 1, "X": -1, "y": 2, "Y": -2}[c] for c in w)


def is_trivial(r1, r2):
    import f_descent
    return f_descent.is_trivial_group(to_ints(r1), to_ints(r2))


def orb(w):
    w = cyc(w)
    out = set()
    for u in (w, inv(w)):
        for r in range(len(u)):
            out.add(u[r:] + u[:r])
    return out


def cyc_reduced_words(L):
    """All cyclically reduced words of length exactly L."""
    letters = "xXyY"
    bad = {"x": "X", "X": "x", "y": "Y", "Y": "y"}
    out = []

    def rec(w):
        if len(w) == L:
            if bad[w[0]] != w[-1]:
                out.append(w)
            return
        for c in letters:
            if bad[w[-1]] != c:
                rec(w + c)
    for c in letters:
        rec(c)
    return out


def classes_pm(u, p, q):
    return {torus_class(u, p, q), torus_class(inv(u), p, q)}


def power_side(k, p, L):
    """Words of length L conjugate to p_p^{+-1} in F/<<W_k>> (exact, via phi_k)."""
    f = phi(k)
    tgt = classes_pm(apply(f, pw(p)), 2, -(2 * k + 1))
    return [u for u in cyc_reduced_words(L) if torus_class(apply(f, u), 2, -(2 * k + 1)) in tgt]


def braid_side(k, p, L, swapped=False):
    """Words of length L conjugate to W_k^{+-1} in <x^p=y^(p+1)> (or <y^p=x^(p+1)>)."""
    sw = ("y", "x")
    Wk = apply(sw, W(k)) if swapped else W(k)
    tgt = classes_pm(Wk, p, -(p + 1))
    out = []
    for u in cyc_reduced_words(L):
        v = apply(sw, u) if swapped else u
        if torus_class(v, p, -(p + 1)) in tgt:
            out.append(u)
    return out


# ------------------------------------------------------------ certificates

def cert_duality(k, p):
    """AK(k;p) -> (red psi_k(V_{k,p}), W_k): one W_k-frozen ACM move (Theorem 2)."""
    cert = C.Cert(pw(p), W(k))
    C.acm_edge(cert, 0, psi(k), 2, -(2 * k + 1), V(k, p))
    assert cert.s[0] == red(apply(psi(k), V(k, p)))
    cert.cyclically_reduce(1)
    cert.rotate_to(1, W(k))
    return cert.to_json(list(cert.s))


def cert_ak22():
    """AK(2;2) = (xxYYY, W_2) -> (x, y) by two torus-frozen ACM moves and a
    primitive finish: W_2 -> phi_1(x^2 Y^3)^-1 (Theorem G1 read backwards, xxYYY
    frozen), then xxYYY = phi_1(b) -> phi_1(yXyXyXy) with phi_1(x^2 Y^3) frozen
    (G's AK(2) move, transported), then the primitive relator is used."""
    f = ("xY", "yyX")          # G's phi; phi(xyxYXY) = xxYYY
    cert = C.Cert("xxYYY", W(2))
    C.acm_edge(cert, 1, IDENT, 2, -3, inv(apply(f, "xxYYY")))
    C.acm_edge(cert, 0, f, 2, -3, "yXyXyXy")
    C.finish_primitive(cert, 0, f)
    assert cert.s == ["x", "y"]
    return cert.to_json(["x", "y"])


def cert_p1(k):
    """AK(k;1) = (xYY, W_k) -> (x, y): the first relator is primitive."""
    cert = C.Cert("xYY", W(k))
    C.finish_primitive(cert, 0, IDENT)
    assert cert.s == ["x", "y"]
    return cert.to_json(["x", "y"])


def _apply_moves(cert, moves):
    for mv in moves:
        if mv["op"] == "invert":
            cert.invert(mv["i"])
        elif mv["op"] == "multiply":
            cert.multiply(mv["i"])
        else:
            cert.conj_letter(mv["i"], mv["g"])


def cert_ak3_to_ak32(certdir):
    """AK(3) -> AK(3;2) = (xxYYY, W_3) exactly.  G's phi = (xY, yyX) = t1 o t2 with
    t1 = (x -> xY), t2 = (y -> yX); D's certificates realise t1, t2 on AK(3) (Lemma
    D6): AK(3) -> t1(AK(3)) -> t1(t2(AK(3))) = phi(AK(3)) = (phi(p_3), xxYYY); then
    one xxYYY-frozen ACM move phi(p_3) -> W_3 (Theorem 2 / G1) and a swap."""
    t1 = ("xY", "y")
    c1 = json.load(open(os.path.join(certdir, "d_ak3_aut_x_xY.json")))
    c2 = json.load(open(os.path.join(certdir, "d_ak3_aut_y_yX.json")))
    c2t = C.transport_certificate(c2, t1)
    cert = C.Cert("xxxYYYY", "xyxYXY")
    _apply_moves(cert, c1["moves"])
    assert cert.s == [red(w) for w in c2t["start"]]
    _apply_moves(cert, c2t["moves"])
    f = ("xY", "yyX")
    assert cert.s == [red(apply(f, "xxxYYYY")), "xxYYY"], cert.s
    C.acm_edge(cert, 0, IDENT, 2, -3, W(3))
    assert cert.s == [W(3), "xxYYY"]
    C.swap(cert)
    assert cert.s == ["xxYYY", W(3)]
    return cert.to_json(["xxYYY", W(3)])


def cert_sigma(k, p):
    """AK(k;p) -> sigma(AK(k;p)) = (y^p X^(p+1), W_k^-1) exactly, sigma = (x <-> y):
    one W_k-frozen ACM move p_p -> q_p = Delta p_p Delta^-1, then W_k is inverted."""
    cert = C.Cert(pw(p), W(k))
    C.acm_edge(cert, 0, psi(k), 2, -(2 * k + 1), red(apply(phi(k), qw(p))))
    assert cert.s[0] == qw(p)
    cert.cyclically_reduce(1)
    cert.rotate_to(1, W(k))
    cert.invert(1)
    tgt = [apply(("y", "x"), pw(p)), apply(("y", "x"), W(k))]
    assert cert.s == tgt, (cert.s, tgt)
    return cert.to_json(tgt)


def cert_mirror_23(certdir):
    """AK(2;3) -> its mirror image (x -> X) = (XXXYYYY, XyXyXYxYxY) exactly, composed
    from the two generator certificates R(t1): P -> t1(P), t1 = (x -> xy), and
    R(sg): P -> sg(P), sg = (x <-> y) (both compiled by d_certify.py from engine
    paths), using R(a o b) = R(a) + a(R(b)) and R(a^-1) = a^-1(reverse R(a))
    (Lemma 6.1):  iota_x = Inn(X) o mu o sg,  mu = t2^-1 t1 t2^-1,  t2 = sg t1 sg."""
    P = ["xxxYYYY", "xyxyxYXYXY"]

    def comp(a, b):
        return (red(apply(a, b[0])), red(apply(a, b[1])))

    def img(th):
        return [red(apply(th, w)) for w in P]

    def prod(Ra, a, Rb):
        return C.concat_certificates(Ra, C.transport_certificate(Rb, a))

    t1, sg, t2i = ("xy", "y"), ("y", "x"), ("x", "yX")
    R1 = json.load(open(os.path.join(certdir, "th13_ak_2_3_aut_x_xy.json")))
    Rs = json.load(open(os.path.join(certdir, "th13_ak_2_3_aut_swap_short.json")))
    assert R1["target"] == img(t1) and Rs["target"] == img(sg)
    st1 = comp(sg, t1)
    Rt2 = prod(prod(Rs, sg, R1), st1, Rs)
    assert comp(st1, sg) == ("x", "yx") and comp(t2i, ("x", "yx")) == ("x", "y")
    Rt2i = C.transport_certificate(C.reverse_certificate(Rt2), t2i)
    a = comp(t2i, t1)
    mu = comp(a, t2i)
    Rmu = prod(prod(Rt2i, t2i, R1), a, Rt2i)
    ms = comp(mu, sg)
    assert ms == ("X", "xyX")
    Rms = prod(Rmu, mu, Rs)
    cert = C.Cert(*P)
    _apply_moves(cert, Rms["moves"])
    assert cert.s == img(ms)
    cert.conj_letter(0, "X")
    cert.conj_letter(1, "X")
    tgt = img(("X", "y"))
    assert cert.s == tgt == ["XXXYYYY", "XyXyXYxYxY"]
    cj = cert.to_json(tgt)
    cj["note"] = "AK(2;3) -> mirror image exactly; research-th13.md section 6; th13_family.py --mirror"
    path = os.path.join(certdir, "th13_ak_2_3_mirror.json")
    with open(path, "w") as fh:
        json.dump(cj, fh, separators=(",", ":"))
    print("th13_ak_2_3_mirror.json moves", len(cj["moves"]), "bytes", os.path.getsize(path))


def write(outdir):
    jobs = [("th13_dual_k2_p2.json", cert_duality(2, 2)),
            ("th13_dual_k2_p3.json", cert_duality(2, 3)),
            ("th13_dual_k3_p3.json", cert_duality(3, 3)),
            ("th13_ak_2_2_trivialization.json", cert_ak22()),
            ("th13_ak_2_1_trivialization.json", cert_p1(2)),
            ("th13_ak_3_1_trivialization.json", cert_p1(3)),
            ("th13_ak3_to_ak_3_2.json", cert_ak3_to_ak32(outdir)),
            ("th13_ak_2_3_aut_swap.json", cert_sigma(2, 3)),
            ("th13_ak_2_4_aut_swap.json", cert_sigma(2, 4))]
    for name, cj in jobs:
        cj["note"] = "research-th13.md; generated by experiments/th13_family.py --write"
        path = os.path.join(outdir, name)
        with open(path, "w") as fh:
            json.dump(cj, fh, separators=(",", ":"))
        print(name, "moves", len(cj["moves"]), "bytes", os.path.getsize(path))


# ------------------------------------------------------------ self-test

def selftest():
    # 1. automorphisms and the frozen relator
    for k in range(1, 9):
        assert red(apply(phi(k), psi(k)[0])) == "x" and red(apply(phi(k), psi(k)[1])) == "y"
        assert red(apply(psi(k), phi(k)[0])) == "x" and red(apply(psi(k), phi(k)[1])) == "y"
        R = "xx" + "Y" * (2 * k + 1)
        assert cyc(apply(psi(k), R)) in orb(W(k))
        assert cyc(apply(phi(k), W(k))) in orb(R)
    # 1b. Corollary 3(a): V_{1,k} = W_k^-1;  remark of section 8: (x -> xY)(W_k) = x^(k+1) Y X^k Y
    for k in range(1, 9):
        assert V(1, k) == inv(W(k))
        assert red(apply(("xY", "y"), W(k))) == "x" * (k + 1) + "Y" + "X" * k + "Y"
        # Delta_k = (xy)^k x conjugates p_p to q_p modulo W_k (Lemma P)
        for p in range(1, 6):
            assert torus_class(apply(phi(k), pw(p)), 2, -(2 * k + 1)) == torus_class(apply(phi(k), qw(p)), 2, -(2 * k + 1))
    # 2. Theorem 2: phi_k(p_p) ~ V_{k,p} in <x^2 = y^(2k+1)>, necklace (k+1)^p k^(p+1)
    for k in range(1, 9):
        for p in range(1, 9):
            cu = torus_class(apply(phi(k), pw(p)), 2, -(2 * k + 1))
            assert cu == torus_class(V(k, p), 2, -(2 * k + 1))
            assert cu[0] == -(2 * p + 1) and len(cu[1]) == 4 * p + 2
            ts = sorted(e for g, e in cu[1] if g == "y")
            assert ts == [k] * (p + 1) + [k + 1] * p
            # image of W_k in C_p * C_(p+1): 4k+2 syllables (p >= 2)
            if p >= 2:
                assert len(torus_class(W(k), p, -(p + 1))[1]) == 4 * k + 2
            # length of the dual relator
            assert len(C.cyc(V(k, p))) == (2 * p + 1) * (k + 1)
    # 3. group triviality (coset enumeration) for small parameters
    for k in range(1, 5):
        for p in range(1, 6):
            assert is_trivial(*AK(k, p)) and is_trivial(*dual(k, p))
    for (a, b, i, j) in [(3, 5, 2, 3), (5, 7, 3, 4), (4, 7, -1, -2), (5, 3, 2, 1)]:
        assert abs(b * i - a * j) == 1
        for m in (1, 2, 3):
            assert is_trivial("x" * a + "Y" * b, artin(i, j, m))
    assert not is_trivial("xxx" + "Y" * 5, artin(1, 1, 1))
    # 4. Theorem 1(b): F(a,b;i,j;m) relators are equal elements for (i,j)+l(a,b)
    for (a, b, i, j) in [(3, 4, 1, 1), (2, 5, 1, 2), (3, 5, 2, 3)]:
        for m in (1, 2):
            c0 = torus_class(artin(i, j, m), a, -b)
            for l in (-2, -1, 1, 2):
                assert torus_class(artin(i + l * a, j + l * b, m), a, -b) == c0
            assert torus_class(inv(artin(-i, -j, m)), a, -b) == c0
    # 5. plateau part of Lemmas P and B, brute force (Theorem 4(a))
    for (k, p) in [(1, 3), (2, 3), (3, 3), (2, 4)]:
        for L in range(1, 2 * p + 3):
            got = set(power_side(k, p, L))
            want = (orb(pw(p)) | orb(qw(p))) if L == 2 * p + 1 else set()
            assert got == want, (k, p, L, len(got))
    for (k, p) in [(1, 3), (2, 3), (1, 4), (2, 4)]:
        for sw in (False, True):
            for L in range(1, 4 * k + 4):
                got = set(braid_side(k, p, L, sw))
                want = orb(W(k)) if L == 4 * k + 2 else set()
                assert got == want, (k, p, L, sw, len(got))
    # 6. Proposition 5: primitive words one ACM move away (exact, Lemma G4)
    for k in range(1, 7):
        for p in range(2, 8):
            h1 = T.primitive_complete(apply(phi(k), pw(p)), 2, -(2 * k + 1))
            h2 = T.primitive_complete(W(k), p, -(p + 1))
            assert bool(h1 or h2) == ((k, p) == (1, 2)), (k, p, h1, h2)
    # 7. first exits (Lemma P, Lemma B): exact minimal off-plateau lengths
    assert [len(power_side(2, 2, L)) for L in range(6, 12)] == [0, 0, 0, 0, 0, 264]
    assert [len(braid_side(1, 4, L)) for L in range(7, 11)] == [0, 0, 0, 40]
    assert len(power_side(1, 3, 9)) == 432 and len(braid_side(1, 3, 8)) == 32
    # 8. commutator necklaces (Lemma 7): [s,t^k] vs [s,t] in C_2 * C_(2k+1)
    for k in range(1, 9):
        c1 = classes_pm("xyXY", 2, -(2 * k + 1))
        c2 = classes_pm("x" + "y" * k + "X" + "Y" * k, 2, -(2 * k + 1))
        n1 = {x[1] for x in c1}
        n2 = {x[1] for x in c2}
        assert (n1 == n2) == (k == 1)
    print("th13_family self-test passed")


def islands(K=12, P=20, L=120):
    """Bounded torus-graph islands (G's bfs, exact primitive-neighbour test)."""
    for (k, p) in [(2, 2), (3, 2), (1, 3), (2, 3), (2, 4), (3, 3), (2, 5), (3, 4), (4, 3)]:
        st = T.start_node(pw(p), W(k), K=max(K, 10), P=max(P, 16))
        nodes, _, winners = T.bfs(st, K=K, P=P, maxlen=L, depth=6, max_nodes=3000,
                                  log=lambda s: None, complete=True)
        types = sorted(((nd[0], nd[1]), (nd[4], nd[5])) for nd in nodes.values())
        print("AK(%d;%d): %d Aut-orbits, %d winners, torus types %s" % (k, p, len(nodes), len(winners), types), flush=True)


def exits():
    """Exact first off-plateau lengths by brute force (about 2.5 minutes)."""
    for (k, p, Lmax) in [(1, 3, 9), (2, 2, 11), (2, 3, 12), (3, 2, 11), (3, 3, 12)]:
        res = [(L, len(power_side(k, p, L))) for L in range(2 * p + 2, Lmax + 1)]
        print("power side", (k, p), "Lemma P bound", 2 * p + 1 + min(4 * k - 2, 2 * k + 2), res, flush=True)
    for (k, p, Lmax) in [(1, 3, 8), (1, 4, 10), (1, 5, 12), (2, 3, 12), (2, 4, 12)]:
        res = [(L, len(braid_side(k, p, L)), len(braid_side(k, p, L, True))) for L in range(4 * k + 3, Lmax + 1)]
        print("braid side", (k, p), "Lemma B bound", 4 * k + 2 * p - 2, res, flush=True)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    elif "--write" in sys.argv:
        write(sys.argv[sys.argv.index("--write") + 1])
    elif "--mirror" in sys.argv:
        cert_mirror_23(sys.argv[sys.argv.index("--mirror") + 1])
    elif "--islands" in sys.argv:
        islands()
    elif "--exits" in sys.argv:
        exits()
    else:
        print(__doc__)
