#!/usr/bin/env python3
"""TH17: killers of the trefoil group in the families T(2;p,q), AK(n), K(a,b,c).

Coordinates.  A = x^2 y X y = x^3 z^2 with z = X y, so H_A = F/<<A>> =
<x,z | x^3 z^2> (trefoil group), zeta = x^3 = z^-2 central, H_A/<zeta> =
C_3 * C_2.  THETA = (x -> x, z -> Xy); in THETA-coordinates the letter 'y'
stands for z.  The class of a word is g_torus.torus_class(., 3, 2) =
(central exponent, syllable necklace), a complete conjugacy invariant
(research-g Lemma 1 / research-j Lemma J0).

  --selftest        dictionary (Thm 1), coincidences (Thm 2), family K (Thm 3)
  --cert OUTDIR     write the two one-move certificates of Cor. 2.3
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g_torus as T  # noqa: E402
import g_cert as C  # noqa: E402

THETA = ("x", "Xy")
THETA_INV = ("x", "xy")
MU = ("xy", "Y")            # mu(b(x,y)) = A:  b = xyxYXY in the basis (xy, Y)
TAU = ("X", "Y")            # outer automorphism of H_A in (x,z)-coordinates
A = "xxyXy"


def to_xz(w):
    return T.red(T.apply(THETA_INV, w))


def cls(w):
    """class in H_A of a word w in x,y"""
    return T.torus_class(to_xz(w), 3, 2)


def neck(c):
    """x-exponent necklace (minimal rotation) of a class; z-syllables are all z^1"""
    e = tuple(s[1] for s in c[1] if s[0] == "x")
    return min(e[i:] + e[:i] for i in range(len(e))) if e else ()


def orbit(w):
    """classes of w, w^-1, tau(w), tau(w)^-1 (tau applied in (x,z)-coordinates)"""
    u = to_xz(w)
    return frozenset(T.torus_class(v, 3, 2) for v in
                     (u, T.inv(u), T.apply(TAU, u), T.inv(T.apply(TAU, u))))


def tword(p, q):
    return T.red(T.power("x", p) + T.power("y", q))


def predicted(p, q):
    """Theorem 1 (q >= 3): (central exponent, necklace) of x^p y^q in H_A."""
    k, r = divmod(p, 3)
    if r == 1:
        return k, (1,) * (q - 1) + (2,)
    if r == 2:
        return k, (1,) * (q - 3) + (2,)
    return k, (1,) * q


def kword(a, b, c):
    """K(a,b,c) = sigma1^a sigma2^-b Delta^2c in the basis (u,v)=(xy,Y), as a word in x,y"""
    w = T.power("x", a) + T.power("y", -b) + T.power("xy", 3 * c)
    return T.red(T.apply(MU, w))


def selftest():
    assert T.red(T.apply(THETA, "xxxyy")) == A
    assert T.cyc(T.apply(MU, "xyxYXY")) == A
    # Theorem 1
    n1 = 0
    for p in range(-20, 21):
        for q in range(3, 40):
            z, nk = predicted(p, q)
            c = cls(tword(p, q))
            assert c[0] == z and neck(c) == min(nk[i:] + nk[:i] for i in range(len(nk))), (p, q, c)
            assert all(s[1] == 1 for s in c[1] if s[0] == "y")
            n1 += 1
    # Lemma S (a = 2) is an equality of classes, for every q >= 3 and every k
    for k in range(-6, 7):
        for q in range(3, 40):
            assert cls(tword(3 * k + 1, q)) == cls(tword(3 * k + 2, q + 2))
    # braid form: x^(3k+1) y^q = Delta^2k sigma1 sigma2^-(q-1) in the basis (u,v)
    for k in range(0, 5):
        for q in range(1, 20):
            assert cls(tword(3 * k + 1, q)) == cls(kword(1, q - 1, k))
    # Theorem 2: coincidences among trivial-group members, up to inversion and tau
    mem = {}
    for k in range(0, 12):
        for q in (6 * k + 1, 6 * k + 3):
            mem[("T", 3 * k + 1, q)] = orbit(tword(3 * k + 1, q))
        for q in (6 * k + 3, 6 * k + 5):
            mem[("T", 3 * k + 2, q)] = orbit(tword(3 * k + 2, q))
    for n in range(1, 25):
        mem[("AK", n)] = orbit(T.red(T.apply(MU, T.power("x", n) + T.power("y", -(n + 1)))))
    mem[("G5", 2)] = orbit("xyyyyyxYY")
    mem[("G5", 3)] = orbit("xyyyyyyyxYY")
    groups = {}
    for name, o in mem.items():
        groups.setdefault(o, []).append(name)
    multi = sorted(sorted(map(str, g)) for g in groups.values() if len(g) > 1)
    for g in multi:
        tl = [eval(s) for s in g]
        ts = sorted(x for x in tl if x[0] == "T")
        assert len(ts) == 2 and ts[1][1] == ts[0][1] + 1 and ts[1][2] == ts[0][2] + 2, g
        for x in tl:
            if x[0] == "AK":
                assert x[1] == 1 and ts[0][1:] == (1, 3)
            if x[0] == "G5":
                assert ts[0][1:] == {2: (4, 7), 3: (4, 9)}[x[1]]
    assert len(multi) == 24
    # Theorem 3: family K(a,b,c), necklace 2^a 1^b up to the symmetries
    n3 = 0
    for a in range(1, 9):
        for b in range(1, 9):
            for c in range(-2, 3):
                kc = cls(kword(a, b, c))
                assert kc[0] == c and neck(kc) == (1,) * b + (2,) * a, (a, b, c, kc)
                n3 += 1
    # Theorem 3(2) against coset enumeration (research-f's f_descent)
    import f_descent as FD
    from math import gcd
    cv = {"x": 1, "X": -1, "y": 2, "Y": -2}
    n4 = 0
    for a in range(1, 7):
        for b in range(1, 13):
            for c in (-1, 0, 1, 2):
                if abs(a - b + 6 * c) == 1:
                    triv = FD.is_trivial_group([cv[ch] for ch in A], [cv[ch] for ch in kword(a, b, c)])
                    assert triv == (gcd(a, b) == 1), (a, b, c, triv)
                    n4 += 1
    assert n4 == 24
    print("th17_levels self-test passed: %d dictionary cases, %d members, %d coincidence groups, %d K-cases"
          % (n1, len(mem), len(multi), n3))


def one_move(killer_from, killer_to):
    """certificate (A, killer_from) -> (killer_to, A) by one A-frozen ACM move"""
    cert = C.Cert(A, killer_from)
    C.acm_edge(cert, 1, THETA, 3, 2, to_xz(killer_to))
    cert.rotate_to(0, A) if cert.s[0] != A else None
    assert cert.s == [A, killer_to], cert.s
    C.swap(cert)
    assert cert.s == [killer_to, A]
    return cert.to_json()


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    elif "--cert" in sys.argv:
        out = sys.argv[sys.argv.index("--cert") + 1]
        for name, src, dst in (("th17_c3_to_T2_4_7_one_move", "xyyyyyxYY", tword(4, 7)),
                               ("th17_r74member_to_T2_4_9", "xyyyyyyyxYY", tword(4, 9))):
            cj = one_move(src, dst)
            cj["note"] = "one ACM move with x^2 y X y frozen (research-th17 Cor. 2.3)"
            with open(os.path.join(out, name + ".json"), "w") as f:
                json.dump(cj, f)
            print(name, len(cj["moves"]), "moves", C.replay(cj))
    else:
        print(__doc__)
