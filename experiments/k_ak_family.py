#!/usr/bin/env python3
"""Uniform ordinary-AC bridge AK(n) -> P_n = (xyxYYXy, x^n YXyy), all n >= 2.

Research agent K, 2026-11-02.  Standard library only (re-uses the repository's
d_certify.py compiler and elementary_verify.py replayer, both standard library).

Notation: X = x^-1, Y = y^-1,  b = xyxYXY,  p_n = x^n Y^(n+1),  AK(n) = (b, p_n).
Closed-form words (exact free words, all n >= 2, 1 <= k <= n+1, 1 <= m <= n-1):

    u_k = x^(n-1) Y^(n+1-k) x y X^k Y          (u_1 = cyc(p_n b^-1), u_(n+1) = w_n)
    v_n = x^(n-1) y X^(n-1) y X Y
    w_n = x^n y X^(n+1) Y                      (a Baumslag-Solitar BS(n,n+1) relator)
    a_m = x^m y X Y X y,  b_m = x^n Y X y X^(n-m) y,  c_m = x^(n-1) y X^(n-m) y X Y
    d_n = x^n Y X y y,    c   = x y x Y Y X y            (c_1 = v_n, a_n: last of phase B)

Path (each step: replace one relator by cyc(g * r) with g a rotation of the OTHER
relator or of its inverse, i.e. an ordinary AC composite):
  A1  (b, p_n) -> (u_1, p_n) -> (u_1, v_n)
  A2  (u_k, v_n) -> (u_(k+1), v_n),  k = 1..n                [u_(k+1) = cyc(rho u_k)]
  B   (w_n, c_1=v_n) -> (w_n, a_2) -> ... : c_m -> a_(m+1) -> b_(m+1) -> c_(m+1) ... -> a_n
  C   (w_n, a_n) -> (d_n, a_n) -> (d_n, c)
Total 4n-1 cyclic products, packaged peak total length 4n+5 for n >= 3 (14 for n = 2).

    python3 experiments/k_ak_family.py --check 2 200        # closed-form identities, no engine
    python3 experiments/k_ak_family.py --cert N OUT.json    # elementary certificate AK(N)->P_N
    python3 experiments/k_ak_family.py --batch 2 40         # certificates n=2..40, replayed
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
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
    """a and b equal as cyclic words (same rotation class)."""
    return len(a) == len(b) and b in rots(a)


def is_rotation_of(g, r):
    return g in rots(r) or g in rots(inv(r))


def words(n):
    x, X, y, Y = "x", "X", "y", "Y"
    b = "xyxYXY"
    p = x * n + Y * (n + 1)
    u = {k: x * (n - 1) + Y * (n + 1 - k) + "xy" + X * k + Y for k in range(1, n + 2)}
    v = x * (n - 1) + y + X * (n - 1) + "yXY"
    w = x * n + y + X * (n + 1) + Y
    a = {m: x * m + "yXYXy" for m in range(1, n + 1)}
    bb = {m: x * n + "YXy" + X * (n - m) + y for m in range(1, n)}
    c = {m: x * (n - 1) + y + X * (n - m) + "yXY" for m in range(1, n)}
    d = x * n + "YXyy"
    cfin = "xyxYYXy"
    return dict(b=b, p=p, u=u, v=v, w=w, a=a, bb=bb, c=c, d=d, cfin=cfin)


def path(n):
    """Return the list of states (ordered pairs of exact cyclic words) and, for each
    step, the multiplier g and the identity new = cyc(g * old) with g a rotation of
    the other relator or its inverse.  Raises if any identity fails."""
    assert n >= 2
    W = words(n)
    b, p, u, v, w, a, bb, c, d, cfin = (W[k] for k in ("b", "p", "u", "v", "w", "a", "bb", "c", "d", "cfin"))
    assert u[n + 1] == w, (u[n + 1], w)
    assert c[1] == v
    states = [(b, p)]
    steps = []

    def step(i, g, expect):
        """Replace relator i of the current state by cyc(g * r_i); g must be a rotation of
        the other relator or of its inverse; result must equal `expect` as a cyclic word."""
        cur = list(states[-1])
        other = cur[1 - i]
        if not is_rotation_of(g, other):
            raise AssertionError(f"n={n}: multiplier {g} is not a rotation of {other}^(+-1)")
        new = cyc(g + cur[i])
        if not same_cyclic(new, expect):
            raise AssertionError(f"n={n}: expected {expect}, got {new}")
        cur[i] = expect
        states.append(tuple(cur))
        steps.append((i, g))

    # Phase A1.  (b, p) -> (u_1, p): u_1 = cyc(p b^-1) = cyc(b^-1 ... ) ; realised as
    # relator 0 <- cyc(g * b) with g = rotation of p^-1 placed so that result is u_1^-1,
    # then we record u_1 (inversion is an AC move and is handled by the compiler's
    # Sigma-normalisation).  Simpler: left-multiply b by p: cyc(p * b^-1)... we use the
    # exact identity u_1 = cyc(p * inv(b)), i.e. new relator 0 := cyc(p * inv(b)).
    cur = list(states[-1])
    new = cyc(p + inv(b))
    if not same_cyclic(new, u[1]):
        raise AssertionError("A1 step 1")
    states.append((u[1], p)); steps.append((0, "p*inv(b)"))
    # (u_1, p) -> (u_1, v):  v = cyc( r * p ) with r a rotation of u_1 ; identity:
    #   rotation r = y X Y x^(n-1) Y^n x  of u_1 ;  r * p  = yXY x^(n-1) Y^n x x^n Y^(n+1)
    #   ... we instead use the verified identity v = inv(cyc(p * s)) with s = rotation of
    #   inv(u_1) = y^n X^(n-1) y x Y X; equivalently v = cyc(inv(s) * inv(p)) and inv(p)
    #   is p inverted (an AC move).  Check the exact identity:
    s = "y" * n + "X" * (n - 1) + "yxYX"
    assert is_rotation_of(s, u[1])
    if not same_cyclic(cyc(inv(s) + inv(p)), v):
        raise AssertionError("A1 step 2")
    states.append((u[1], v)); steps.append((1, "inv(s)*inv(p)"))
    # Phase A2: u_(k+1) = cyc(rho * u_k), rho = y X Y x^(n-1) y X^(n-1), a rotation of v.
    rho = "yXY" + "x" * (n - 1) + "y" + "X" * (n - 1)
    for k in range(1, n + 1):
        step(0, rho, u[k + 1])
    # now state = (w, v) with w = u_(n+1); phase B acts on relator 1 with w frozen.
    sigma_inv = "Xy" + "x" * (n + 1) + "Y" + "X" * (n - 1)    # rotation of w
    kappa_inv = "XY" + "x" * n + "y" + "X" * n                 # rotation of inv(w)
    step(1, sigma_inv, a[2])                                   # c_1 = v -> a_2
    for m in range(2, n):
        tau_inv = "X" * (n - m) + "y" + "x" * (n + 1) + "Y" + "X" * m   # rotation of w
        step(1, tau_inv, bb[m])                                # a_m -> b_m
        step(1, kappa_inv, c[m])                               # b_m -> c_m
        step(1, sigma_inv, a[m + 1])                           # c_m -> a_(m+1)
    # Phase C: (w, a_n) -> (d, a_n): d = cyc(a_n * w') with w' = y x^(n+1) Y X^n (rotation of w)
    wprime = "y" + "x" * (n + 1) + "Y" + "X" * n
    assert is_rotation_of(wprime, w)
    if not same_cyclic(cyc(a[n] + wprime), d):
        raise AssertionError("C step 1")
    states.append((d, a[n])); steps.append((0, "a_n*w'"))
    # (d, a_n) -> (d, c): c = cyc(d * inv(a_n))
    if not same_cyclic(cyc(d + inv(a[n])), cfin):
        raise AssertionError("C step 2")
    states.append((d, cfin)); steps.append((1, "d*inv(a_n)"))
    return states, steps


def check(lo, hi):
    for n in range(lo, hi + 1):
        st, steps = path(n)
        assert len(steps) == 4 * n - 1, (n, len(steps))
        peak = max(len(s[0]) + len(s[1]) for s in st)
        assert peak == max(4 * n + 5, 3 * n + 8), (n, peak)   # 14 for n=2, 4n+5 for n>=3
        assert st[-1] == (words(n)["d"], "xyxYYXy")
    print(f"closed-form path verified for n = {lo}..{hi}: 4n-1 cyclic products, packaged peak max(4n+5,3n+8), "
          f"endpoint (x^n YXyy, xyxYYXy) up to rotation")


def certificate(n):
    st, _ = path(n)
    # d_certify takes Sigma-canonical-ish states "w1 w2" (any rotation works: it re-finds
    # moves up to Sigma) and exact start/target tuples.
    start = ("xyxYXY", "x" * n + "Y" * (n + 1))
    target = ("xyxYYXy", "x" * n + "YXyy")
    lines = [(s[0], s[1]) for s in st]
    cert = d_certify.certificate(lines, start, target,
                                 f"AK({n}) = (xyxYXY, x^{n} Y^{n + 1}) -> P_{n} = (xyxYYXy, x^{n} YXyy): "
                                 f"uniform closed-form path of research-k.md (4n-1 cyclic products, "
                                 f"packaged peak 4n+5), compiled to strict elementary moves.")
    r = elementary_verify.replay(cert)
    assert r["endpoint"] == list(target)
    return cert, r


def main():
    args = sys.argv[1:]
    if args[:1] == ["--check"]:
        check(int(args[1]), int(args[2]))
    elif args[:1] == ["--cert"]:
        n, out = int(args[1]), args[2]
        cert, r = certificate(n)
        with open(out, "w") as f:
            json.dump(cert, f, indent=1)
        print(json.dumps({"n": n, "moves": r["moves"], "peak_total_length": r["peak_total_length"],
                          "endpoint": r["endpoint"], "path": out}))
    elif args[:1] == ["--batch"]:
        lo, hi = int(args[1]), int(args[2])
        for n in range(lo, hi + 1):
            cert, r = certificate(n)
            print(f"n={n} elementary_moves={r['moves']} peak={r['peak_total_length']} endpoint={r['endpoint']}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
