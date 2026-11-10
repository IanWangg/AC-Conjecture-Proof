#!/usr/bin/env python3
"""TH17: x-shared torus-shaped pairs (Theorem 6) and the third torus form (Theorem 4).

Vertex of the graph S: a pair (x^p (x^e y)^q , x^M (x^f y)^N).
  --selftest   (0) at the end: the third-form graph of Theorem 6* (orbit conditions, two-sided brute force);
               (1) Theorem 4: (x^2 y)^(2k+1) (xy)^-(6k+3-+1) is conjugate in H_A to x^(3k+1) y^(6k+2-+1);
               (2) brute force of the classification used in Theorem 6 at the start vertices and at all
                   vertices of the shear orbit up to word length 3 in the shears, for small (p,q);
               (3) ping-pong: |M| > 3 off the trivial start shears, no degenerate syllable in the orbit.
  --cert OUTDIR  one-move certificates T(2;3k+1,6k+1) -> third torus form, k = 1, 2
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g_torus as T  # noqa: E402
import g_cert as C  # noqa: E402
import th17_levels as L  # noqa: E402

red, inv, power = T.red, T.inv, T.power


def shape(m, f, n):
    """the word x^m (x^f y)^n"""
    return red(power("x", m) + power(power("x", f) + "y", n))


def conj_pm(w1, w2, theta_inv, a, b):
    """is w1 conjugate to w2^{+-1} in <x,y | theta(x^a y^b)> ?"""
    c1 = T.torus_class(red(T.apply(theta_inv, w1)), a, b)
    return any(c1 == T.torus_class(red(T.apply(theta_inv, v)), a, b) for v in (w2, inv(w2)))


def frozen_coords(m, f, n):
    """theta^-1 for the relator x^m (x^f y)^n = theta(x^m y^n), theta: y -> x^f y"""
    return ("x", red(power("x", -f) + "y"))


def brute_vertex(p, e, q, M, f, N, B, ns):
    """parameter triples (a,b,n), |a| <= B[0], |b| <= B[1], n in ns, with x^a (x^b y)^n conjugate (+-) to
    one relator modulo the other; s1 = conjugates of r1 (r2 frozen), s2 = conjugates of r2 (r1 frozen)"""
    r1, r2 = shape(p, e, q), shape(M, f, N)
    ti1, ti2 = frozen_coords(p, e, q), frozen_coords(M, f, N)
    cl = lambda w, ti, a, b: T.torus_class(red(T.apply(ti, w)), a, b)
    tg2 = {cl(r2, ti1, p, q), cl(inv(r2), ti1, p, q)}
    tg1 = {cl(r1, ti2, M, N), cl(inv(r1), ti2, M, N)}
    s1, s2 = set(), set()
    for a in range(-B[0], B[0] + 1):
        for b in range(-B[1], B[1] + 1):
            for n in ns:
                w = shape(a, b, n)
                if cl(w, ti1, p, q) in tg2:
                    s2.add((a, b, n))
                if cl(w, ti2, M, N) in tg1:
                    s1.add((a, b, n))
    return s1, s2


def predicted(p, e, q, M, f, B, ns, R=40):
    """Lemmas 6.1 and 6.2: the same two sets, from the closed formulas (c = e - f)."""
    c = e - f
    inbox = lambda t: abs(t[0]) <= B[0] and abs(t[1]) <= B[1] and t[2] in ns
    pos = set()                     # positive-exponent descriptions (P, C, n) in z-coordinates
    if (p + c) % M == 0:            # degenerate killer: pass to its Lemma S partner
        p, q = p - M + 2 * c, q - 2
    for mu in range(-R, R + 1):
        pos.add((p - mu * q * M, c + mu * M, q))                                  # (alpha)
        if (p - c) % M == 0:                                                      # (gamma), Lemma S type
            pos.add((p + M - 2 * c - mu * (q + 2) * M, c + mu * M, q + 2))
    s1 = set()
    for (P, C, n) in pos:
        for (a, b, m) in ((P, C, n), (P - n * M, -C, -n)):                        # (beta): the flip
            for t in ((a, b + f, m), (-a, b + f, -m)):                            # cyclic inverse
                if inbox(t):
                    s1.add(t)
    return s1


def predicted_y(p, e, q, M, f, B, ns, R=40):
    c = e - f
    inbox = lambda t: abs(t[0]) <= B[0] and abs(t[1]) <= B[1] and t[2] in ns
    s2 = set()
    for ka in range(-R, R + 1):
        for (M1, c1) in ((M + 2 * ka * p, c + ka * p), (-M + 2 * ka * p, c - M + ka * p)):
            for t in ((M1, e - c1, 2), (-M1, e - c1, -2)):
                if inbox(t):
                    s2.add(t)
    return s2


def orbit(p, q, depth):
    """shear orbit of (p,e,M,f) = (p,0,3,-1): reduced words of length <= depth in U_i, V_mu (|i|,|mu| <= 2)"""
    out = {(p, 0, 3, -1): ""}
    frontier = [((p, 0, 3, -1), "")]
    for _ in range(depth):
        new = []
        for (pp, e, M, f), last in frontier:
            for kind in "UV":
                if kind == last:
                    continue
                for i in (-2, -1, 1, 2):
                    v = (pp, e, M - 2 * i * pp, f + i * pp) if kind == "U" else (pp - i * q * M, e + i * M, M, f)
                    if v not in out:
                        out[v] = kind
                        new.append((v, kind))
        frontier = new
    return out


def orbit3(P0, Q, depth):
    """N = 3: shear orbit of T*(P0,-Q), normalised start (p,e,M,f) = (-P0,0,2,-1) with exponent Q"""
    out = {(-P0, 0, 2, -1): ""}
    frontier = [((-P0, 0, 2, -1), "")]
    for _ in range(depth):
        new = []
        for (pp, e, M, f), last in frontier:
            for kind in "UV":
                if kind == last:
                    continue
                for i in (-2, -1, 1, 2):
                    v = (pp, e, M - 3 * i * pp, f + i * pp) if kind == "U" else (pp - i * Q * M, e + i * M, M, f)
                    if v not in out:
                        out[v] = kind
                        new.append((v, kind))
        frontier = new
    return out


def selftest3():
    """third-form graph (Theorem 6*): orbit conditions and two-sided brute force of the shape conjugates"""
    nv = 0
    for (P0, Q) in ((3, 8), (3, 10), (5, 14), (5, 16), (7, 20)):
        for (pp, e, M, f) in orbit3(P0, Q, 5):
            c = e - f
            nv += 1
            assert abs(pp) >= 3 and M % 3 == 2 and abs(3 * pp - Q * (M - 3 * c)) == 1
            assert c % pp and (M - c) % pp and M % pp
            if abs(M) == 2:
                assert M == 2 and (pp + P0) % (2 * Q) == 0
            else:
                assert abs(M) >= 7 and c % M and pp % M and (pp + c) % M
    nb = 0
    for (P0, Q, verts) in ((3, 8, ((-3, 0, 2, -1), (-3, 0, 11, -4), (-19, 2, 2, -1))), (3, 10, ((-3, 0, 2, -1),)),
                           (5, 14, ((-5, 0, 2, -1),))):
        orb = orbit3(P0, Q, 2)
        ns = [sg * n for sg in (1, -1) for n in (1, 2, 3, 4, 5, Q - 2, Q - 1, Q, Q + 1, Q + 2)]
        for (pp, e, M, f) in verts:
            assert (pp, e, M, f) in orb
            c = e - f
            B = (min(abs(pp) + Q * abs(M) + 8, 60), abs(M) + abs(pp) + 4)
            s1, s2 = brute_vertex(pp, e, Q, M, f, 3, B, ns)
            inbox = lambda t: abs(t[0]) <= B[0] and abs(t[1]) <= B[1] and t[2] in ns
            t1, t2 = set(), set()
            for mu in range(-40, 41):
                a, b = pp - mu * Q * M, c + mu * M + f
                t1 |= {t for t in ((a, b, Q), (-a, b, -Q)) if inbox(t)}
                M1, c1 = M + 3 * mu * pp, c + mu * pp
                t2 |= {t for t in ((M1, e - c1, 3), (-M1, e - c1, -3)) if inbox(t)}
            assert s1 == t1 and s2 == t2 and s1 and s2, (pp, e, M, f, sorted(s1 ^ t1)[:5], sorted(s2 ^ t2)[:5])
            nb += 1
    print("th17_shear third-form self-test passed: %d orbit vertices checked, %d vertices brute-forced" % (nv, nb))


def selftest():
    # (1) Theorem 4
    for k in range(0, 8):
        for q in (6 * k + 1, 6 * k + 3):
            w3 = red(power("xxy", 2 * k + 1) + power("xy", -(q + 1)))
            assert L.cls(w3) == L.cls(L.tword(3 * k + 1, q)), (k, q)
    # G5 family = T(2;4,.) row
    for kk in range(1, 12):
        assert L.cls(red("x" + "y" * (2 * kk + 1) + "xYY")) == L.cls(L.tword(4, 2 * kk + 3))
    # (3) ping-pong and non-degeneracy along the shear orbit
    nv = 0
    for (p, q) in ((4, 7), (4, 9), (7, 13), (7, 15), (10, 19), (5, 9), (5, 11), (8, 15)):
        for (pp, e, M, f) in orbit(p, q, 5):
            c = e - f
            nv += 1
            assert M % 2 == 1 and abs(pp) >= 4 and abs(M) >= 3
            if M == 3:
                assert (pp - p) % (3 * q) == 0 and c == 1 + (p - pp) // q
            else:
                assert abs(M) > 3 and c % M and (pp - c) % M and (pp + c) % M and pp % M
            assert c % pp and (M - c) % pp
            assert abs(2 * pp - q * (M - 2 * c)) == 1          # the invariant D
    # (2) brute force of Lemmas 6.1 / 6.2 (two-sided, on parameter boxes)
    nb = 0
    for (p, q, verts) in ((4, 7, ((4, 0, 3, -1), (4, 0, 11, -5), (-17, 3, 3, -1), (4, 0, -5, 3))),
                          (5, 9, ((5, 0, 3, -1),)), (4, 9, ((4, 0, 3, -1),))):
        orb = orbit(p, q, 2)
        ns = [s * n for s in (1, -1) for n in (1, 2, 3, 4, q - 2, q, q + 2)]
        for (pp, e, M, f) in verts:
            assert (pp, e, M, f) in orb
            B = (max(abs(pp) + q * abs(M) + 8, 2 * abs(pp) + abs(M) + 8), abs(M) + abs(pp) + 4)
            if B[0] > 90:
                B = (90, 12)
            s1, s2 = brute_vertex(pp, e, q, M, f, 2, B, ns)
            assert s1 == predicted(pp, e, q, M, f, B, ns), (pp, e, M, f, sorted(s1 ^ predicted(pp, e, q, M, f, B, ns))[:6])
            assert s2 == predicted_y(pp, e, q, M, f, B, ns), (pp, e, M, f, sorted(s2 ^ predicted_y(pp, e, q, M, f, B, ns))[:6])
            assert s1 and s2
            nb += 1
    print("th17_shear self-test passed: %d orbit vertices checked, %d vertices brute-forced" % (nv, nb))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        selftest3()
    elif "--cert" in sys.argv:
        out = sys.argv[sys.argv.index("--cert") + 1]
        for k in (1, 2):
            src = L.tword(3 * k + 1, 6 * k + 1)
            dst = red(power("xxy", 2 * k + 1) + power("xy", -(6 * k + 2)))
            cert = C.Cert(src, L.A)
            C.acm_edge(cert, 0, L.THETA, 3, 2, L.to_xz(dst))
            assert cert.s == [dst, L.A], cert.s
            cj = cert.to_json()
            cj["note"] = "one ACM move with x^2 y X y frozen (research-th17 Thm 4), level %d" % k
            name = "th17_T2_%d_%d_to_third_form" % (3 * k + 1, 6 * k + 1)
            with open(os.path.join(out, name + ".json"), "w") as fh:
                json.dump(cj, fh)
            print(name, len(cj["moves"]), "moves", C.replay(cj))
    else:
        print(__doc__)
