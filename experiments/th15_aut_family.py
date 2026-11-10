#!/usr/bin/env python3
"""TH15: uniform ordinary-AC realization of Aut(F2) on AK(n), all n >= 2.

Notation: X = x^-1, Y = y^-1, b = xyxYXY, p_n = x^n Y^(n+1), AK(n) = (p_n, b).
sigma = swap x <-> y;  a = (x -> xY, y -> y).  sigma, a and Inn(F2) generate Aut(F2).

Closed-form paths (each step replaces ONE relator r by cyc(g * r') with r' a rotation
of r and g a rotation of the OTHER relator or of its inverse: an ordinary-AC composite):

  swap  (2n+1 steps, b frozen, every multiplier a rotation of b^-1):
     p_n -> w_1 -> ... -> w_n -> w'_1 -> ... -> w'_n -> q_n = y^n X^(n+1)
     w_k  = y^k x y x^(n-k+1) Y^(n+1) X Y X          (= y^k D x^(n-k) Y^(n+1) D^-1, D = xyx)
     w'_j = y^n X^(j-1) y x Y^(n+1-j) X Y X          (= y^n X^j D Y^(n+1-j) D^-1)
  a = (x -> xY)  (2n+1 steps, frozen relator alternates):
     I   b frozen:   u_k = x^(n-k) Y^n x y^k X Y,  k = 0..n-1      (u_0 = p_n)
     II  u_(n-1) frozen:  b -> b1 = X Y^(n+1) x y^n                 (a BS(n,n+1) relator)
     III b1 frozen:  u_(n-1) -> v_0 = x x y^(n-1) X Y^(n+2)
     IV  v_0 frozen: b1 -> b2 = y x y X X                           (= a(b)^-1 rotated)
     V   b2 frozen:  v_m = x x y^(n-1-m) X Y^(n+2) (xY)^m, m = 0..n-1; v_(n-1) ~ (xY)^n Y^(n+1)

    python3 experiments/th15_aut_family.py --selftest
    python3 experiments/th15_aut_family.py --check 2 200
    python3 experiments/th15_aut_family.py --cert swap|a|hub|hubT|ms N OUT.json
    python3 experiments/th15_aut_family.py --batch 2 8
    python3 experiments/th15_aut_family.py --nielsen N [OUTDIR]   (see th15_transport.py)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import d_certify  # noqa: E402
import elementary_verify  # noqa: E402

INV = {"x": "X", "X": "x", "y": "Y", "Y": "y"}


def red(w):
    out = []
    for ch in w:
        if out and out[-1] == INV[ch]:
            out.pop()
        else:
            out.append(ch)
    return "".join(out)


def inv(w):
    return "".join(INV[ch] for ch in reversed(w))


def cyc(w):
    w = red(w)
    while len(w) >= 2 and w[0] == INV[w[-1]]:
        w = w[1:-1]
    return w


def rots(w):
    return [w[i:] + w[:i] for i in range(len(w))]


def same_cyclic(a, b):
    return len(a) == len(b) and b in rots(a)


class Path:
    """A list of states (pairs of cyclically reduced words) joined by checked cyclic products."""

    def __init__(self, first, second):
        assert cyc(first) == first and cyc(second) == second
        self.states = [(first, second)]
        self.steps = []

    def step(self, i, g, r, expect, side="L"):
        """relator i := expect, where expect == cyc(g r) (side "L") or cyc(r g) (side "R") as
        cyclic words; r must be a rotation of the current relator i or of its inverse, and g a
        rotation of the other relator or of its inverse.  (Rotation = conjugation, inversion and
        right multiplication are ordinary AC moves, so each step is an ordinary-AC composite.)"""
        cur = list(self.states[-1])
        other = cur[1 - i]
        assert g in rots(other) or g in rots(inv(other)), ("multiplier", g, other)
        assert r in rots(cur[i]) or r in rots(inv(cur[i])), ("rotation", r, cur[i])
        new = cyc(g + r) if side == "L" else cyc(r + g)
        assert cyc(expect) == expect and same_cyclic(new, expect), (g, r, new, expect)
        cur[i] = expect
        self.states.append(tuple(cur))
        self.steps.append((i, g, r, side))

    def peak(self):
        return max(len(s[0]) + len(s[1]) for s in self.states)


B = "xyxYXY"


def p(n):
    return "x" * n + "Y" * (n + 1)


def swap_path(n):
    """(p_n, b) -> (q_n, b): 2n+1 cyclic products, multipliers rotations of b^-1."""
    assert n >= 1
    x, X, y, Y = "x", "X", "y", "Y"
    w = {k: y * k + "xy" + x * (n - k + 1) + Y * (n + 1) + "XYX" for k in range(1, n + 1)}
    wp = {j: y * n + X * (j - 1) + "yx" + Y * (n + 1 - j) + "XYX" for j in range(1, n + 1)}
    q = y * n + X * (n + 1)
    P = Path(p(n), B)
    P.step(0, "XYXyxy", p(n), w[1])
    for k in range(1, n):
        P.step(0, "yxyXYX", "xy" + x * (n - k + 1) + Y * (n + 1) + "XYX" + y * k, w[k + 1])
    P.step(0, "yxyXYX", "xyx" + Y * (n + 1) + "XYX" + y * n, wp[1])
    for j in range(1, n):
        P.step(0, "XyxyXY", "yx" + Y * (n + 1 - j) + "XYX" + y * n + X * (j - 1), wp[j + 1])
    P.step(0, "XyxyXY", "yxYXYX" + y * n + X * (n - 1), q)
    assert len(P.steps) == 2 * n + 1
    return P


def a_words(n):
    x, X, y, Y = "x", "X", "y", "Y"
    u = {k: x * (n - k) + Y * n + x + y * k + "XY" for k in range(1, n)}
    u[0] = p(n)
    b1 = X + Y * (n + 1) + x + y * n
    v = {m: "xx" + y * (n - 1 - m) + X + Y * (n + 2) + "xY" * m for m in range(0, n - 1)}
    v[n - 1] = "xY" * n + Y * (n + 1)
    return u, b1, v, "yxyXX"


def a_path(n):
    """(p_n, b) -> ((xY)^n Y^(n+1), yxyXX), i.e. a(AK(n)) up to rotation/inversion: 2n+1 products."""
    assert n >= 2
    x, X, y, Y = "x", "X", "y", "Y"
    u, b1, v, b2 = a_words(n)
    P = Path(p(n), B)
    # I (b frozen): u_(k+1) = (X u_k x) * XyxyXY
    for k in range(0, n - 1):
        r = x * (n - k - 1) + Y * n + x + y * k + "XYx" if k >= 1 else x * (n - 1) + Y * (n + 1) + x
        P.step(0, "XyxyXY", r, u[k + 1], side="R")
    # II (u_(n-1) frozen): b1 = cyc( (X u_(n-1) x) * XyxyXY ),  XyxyXY a rotation of b^-1
    P.step(1, Y * n + x + y * (n - 1) + "XYx", "XyxyXY", b1, side="L")
    # III (b1 frozen): v_0 = cyc( (Y^(n+1) x y^n X) * u_(n-1) )
    P.step(0, Y * (n + 1) + x + y * n + X, u[n - 1], v[0], side="L")
    # IV (v_0 frozen): b2 = cyc( (x y^n X Y^(n+1)) * (y^(n+1) x Y^(n-1) X X y) )
    P.step(1, y * (n + 1) + x + Y * (n - 1) + "XXy", x + y * n + X + Y * (n + 1), b2, side="R")
    # V (b2 frozen): v_(m+1) = cyc( YxxYX * (x y^(n-1-m) X Y^(n+2) x (Yx)^m) )
    for m in range(0, n - 1):
        r = x + y * (n - 1 - m) + X + Y * (n + 2) + x + "Yx" * m
        P.step(0, "YxxYX", r, v[m + 1], side="L")
    assert len(P.steps) == 2 * n + 1
    return P


def beta(n):
    """The Baumslag-Solitar relator beta_n = x^-1 y^-(n+1) x y^n."""
    return "X" + "Y" * (n + 1) + "x" + "y" * n


def hub_path(n, twist=False):
    """(p_n, b) -> (beta_n, b) by n cyclic products with b frozen (Lemma H); with twist=True
    three more products with beta_n frozen take b to a(b) = xxYXY (Lemma T made explicit)."""
    assert n >= 2
    x, X, y, Y = "x", "X", "y", "Y"
    u, _, v, _ = a_words(n)
    P = Path(p(n), B)
    for k in range(0, n):
        r = x * (n - k - 1) + Y * n + x + y * k + "XYx" if k >= 1 else x * (n - 1) + Y * (n + 1) + x
        P.step(0, "XyxyXY", r, u[k + 1] if k < n - 1 else beta(n), side="R")
    if twist:
        c1 = x + y * (n + 1) + "xYX" + Y * (n + 2)
        P.step(1, Y * (n + 1) + x + y * n + X, B, c1)
        P.step(1, x + y * n + X + Y * (n + 1), y * (n + 1) + "xYX" + Y * (n + 2) + x, v[0])
        P.step(1, "YX" + y * (n + 1) + x + Y * (n - 1), y * (n - 1) + X + Y * (n + 2) + "xx", "xxYXY")
    return P


def betap(n):
    """Miller-Schupp orientation beta'_n = x^-1 y^n x y^-(n+1)."""
    return "X" + "y" * n + "x" + "Y" * (n + 1)


def ms_path(n):
    """(p_n, b) -> (beta'_n, b) by n cyclic products (b frozen), then three products with
    beta'_n frozen take b to XYxxY: the endpoint is C's M_n = MS(n, y^-1 x^2 y^-1)."""
    assert n >= 2
    x, X, y, Y = "x", "X", "y", "Y"
    f = {k: x * k + "YX" + y * (n - k) + x + Y * n for k in range(0, n)}       # f_0 ~ beta'_n
    P = Path(p(n), B)
    P.step(0, "YXyxyX", x + Y * (n + 1) + x * (n - 1), f[n - 1])
    for k in range(n - 1, 0, -1):
        P.step(0, "YXyxyX", "xYX" + y * (n - k) + x + Y * n + x * (k - 1), f[k - 1] if k > 1 else betap(n))
    c1 = x + Y * n + "xYX" + y * (n - 1)
    v0 = "xx" + Y * (n + 2) + X + y * (n - 1)
    P.step(1, y * n + x + Y * (n + 1) + X, B, c1)
    P.step(1, x + Y * (n + 1) + X + y * n, Y * n + "xYX" + y * (n - 1) + x, v0)
    P.step(1, X + Y * n + x + y * (n + 1), Y * (n + 1) + X + y * (n - 1) + "xxY", "XYxxY")
    assert len(P.steps) == n + 3
    return P


def mechanism_identities(n):
    """Free-group identities behind Lemmas S and T (exact equalities of reduced words)."""
    x, X, y, Y = "x", "X", "y", "Y"
    bt, D = beta(n), "xyx"
    # Lemma S: D x D^-1 = b y,  D y D^-1 = x b^-1,  swap(b) = b^-1
    assert red(D + x + inv(D)) == red(B + y) and red(D + y + inv(D)) == red(x + inv(B))
    assert "".join({"x": "y", "y": "x", "X": "Y", "Y": "X"}[c] for c in B) == inv(B)
    # Lemma T: T = (x -> xy): T(beta) = Y beta y;  y^-(n+1) x y^(n+1) = (x beta X) T(x)
    T = {"x": "xy", "X": "YX", "y": "y", "Y": "Y"}
    assert red("".join(T[c] for c in bt)) == red(Y + bt + y)
    assert red(Y * (n + 1) + x + y * (n + 1)) == red(x + bt + X + "xy")
    # T(XYxxY) is a rotation of b (C's bridge word), a(b) = xxYXY
    assert red("".join(T[c] for c in "XYxxY")) in rots(B)
    assert red("".join({"x": "xY", "X": "yX", "y": "y", "Y": "Y"}[c] for c in B)) == "xxYXY"
    return True


def check(lo, hi):
    for n in range(lo, hi + 1):
        S = swap_path(n)
        assert S.states[-1] == ("y" * n + "X" * (n + 1), B) and S.peak() == 2 * n + 13
        assert all(len(s[0]) in (2 * n + 1, 2 * n + 5, 2 * n + 7) for s in S.states)
        if n >= 2:
            A = a_path(n)
            assert A.states[-1] == ("xY" * n + "Y" * (n + 1), "yxyXX")
            assert A.peak() == 4 * n + 7, (n, A.peak())
            H = hub_path(n, twist=True)
            assert H.states[n] == (beta(n), B) and H.states[-1] == (beta(n), "xxYXY")
            assert len(H.steps) == n + 3 and H.peak() == 4 * n + 10
            M = ms_path(n)
            assert M.states[n] == (betap(n), B) and M.states[-1] == (betap(n), "XYxxY")
            assert M.peak() == 4 * n + 7, (n, M.peak())
        mechanism_identities(n)
    print(f"closed-form paths verified for n = {lo}..{hi}: swap 2n+1 cyclic products (peak 2n+13); "
          f"a = (x->xY) 2n+1 cyclic products (peak 4n+7); hub (p_n,b)->(beta_n,b)->(beta_n,xxYXY) "
          f"n+3 products (peak 4n+10); (p_n,b)->(beta'_n,b)->M_n n+3 products (peak 4n+7); every multiplier is a rotation of the frozen relator or its "
          f"inverse; Lemma S / Lemma T free-group identities hold")


TARGETS = {
    "swap": lambda n: ("y" * n + "X" * (n + 1), "yxyXYX"),
    "a": lambda n: ("xY" * n + "Y" * (n + 1), "xxYXY"),
    "hub": lambda n: (beta(n), B),
    "hubT": lambda n: (beta(n), "xxYXY"),
    "ms": lambda n: (betap(n), "XYxxY"),
}


def certificate(kind, n):
    P = {"swap": swap_path, "a": a_path, "hub": hub_path,
         "hubT": lambda m: hub_path(m, twist=True), "ms": ms_path}[kind](n)
    start = (p(n), B)
    target = TARGETS[kind](n)
    what = {"swap": "phi(AK(n)) exactly, phi = swap x<->y",
            "a": "phi(AK(n)) exactly, phi = a = (x -> x y^-1, y -> y)",
            "hub": "(beta_n, b), beta_n = x^-1 y^-(n+1) x y^n (Baumslag-Solitar hub)",
            "hubT": "H_n = (beta_n, xxYXY) = a(beta_n, b) up to rotation (length 2n+8)",
            "ms": "M_n = MS(n, y^-1 x^2 y^-1) = (x^-1 y^n x y^-(n+1), x^-1 y^-1 x^2 y^-1) (C's bridge)"}[kind]
    cert = d_certify.certificate(P.states, start, target,
                                 f"AK({n}) = (x^{n} Y^{n + 1}, xyxYXY) -> {what}: "
                                 f"uniform closed-form path of research-th15.md ({len(P.steps)} cyclic "
                                 f"products), compiled to strict elementary moves.")
    r = elementary_verify.replay(cert)
    assert r["endpoint"] == list(target)
    return cert, r


def main():
    args = sys.argv[1:]
    if args[:1] == ["--check"]:
        check(int(args[1]), int(args[2]))
    elif args[:1] == ["--cert"]:
        kind, n, out = args[1], int(args[2]), args[3]
        cert, r = certificate(kind, n)
        with open(out, "w") as f:
            json.dump(cert, f, indent=1)
        print(json.dumps({"kind": kind, "n": n, "moves": r["moves"],
                          "peak_total_length": r["peak_total_length"], "endpoint": r["endpoint"], "path": out}))
    elif args[:1] == ["--batch"]:
        for n in range(int(args[1]), int(args[2]) + 1):
            for kind in ("swap", "a", "hub", "hubT", "ms"):
                cert, r = certificate(kind, n)
                print(f"n={n} {kind}: {r['moves']} elementary moves, peak {r['peak_total_length']}, "
                      f"endpoint {tuple(r['endpoint'])} verified")
    elif args[:1] == ["--selftest"]:
        check(2, 40)
        for kind in ("swap", "a"):
            cert, r = certificate(kind, 3)
            bad = json.loads(json.dumps(cert))
            bad["moves"][len(bad["moves"]) // 2]["i"] ^= 1
            try:
                ok = elementary_verify.replay(bad)["endpoint"] == cert["target"]
            except Exception:
                ok = False
            assert not ok, "corrupted certificate was accepted"
        print("selftest passed (identities n = 2..40; n = 3 certificates replay; corrupted ones rejected)")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
