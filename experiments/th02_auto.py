#!/usr/bin/env python3
"""th02_auto.py (agent TH02): automatic hidden-reflection certificates.

find_theta(w): for a cyclic word w of type T(2,n) returns (theta, theta^-1, n)
with w conjugate to theta(x^2 y^n)^{+-1} (Whitehead reduction, tracking the
automorphisms).  auto_reflect(pair, i) then builds the Theorem TH02.1
certificate pair -> beta(pair).  --write produces the certificates for
Y = T(4;7,5) (infinite stabilizer) and for AK(3) (swap, uniform in n).

Usage: python3 experiments/th02_auto.py --self-test | --write
"""
import json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from th02_hidden import (red, inv, pw, subst, compose, matrix, mmul, reflect_cert, Cert, run,
                         reverse_moves, transport_moves, replay, T)
from th02_scan import cycred, hidden_reflection
from th02_acm import aut_inverse

WH = [{"x": "xy", "y": "y"}, {"x": "xY", "y": "y"}, {"x": "x", "y": "yx"}, {"x": "x", "y": "yX"}]
ID = {"x": "x", "y": "y"}


def find_theta(w):
    w = cycred(w); Phi = dict(ID)                     # current word = Phi(original), cyclically
    improved = True
    while improved:
        improved = False
        for m in WH:
            q = cycred(subst(w, m))
            if len(q) < len(w):
                w, Phi, improved = q, compose(m, Phi), True
                break
    for a, b in (("x", "y"), ("y", "x")):
        for c in (a, a.upper()):
            if w.count(c) == 2 and w.count(c.swapcase()) == 0:
                k0 = w.index(c); v = w[k0:] + w[:k0]; k1 = v.index(c, 1)
                ex = lambda s: s.count(b) - s.count(b.upper())
                s1, s2 = v[1:k1], v[k1 + 1:]
                if len(s1) != abs(ex(s1)) or len(s2) != abs(ex(s2)):
                    continue
                i, k = ex(s1), ex(s2)                 # w ~ (c b^i)^2 b^(k-i)
                th_min = {"x": red(c + pw(b, i)), "y": b}
                theta = compose(aut_inverse(Phi), th_min)
                return theta, aut_inverse(theta), k - i
    return None


def auto_reflect(pair, i, label=""):
    theta, theta_inv, n = find_theta(pair[i])
    return reflect_cert(pair, i, theta, theta_inv, n, label)


def engine_path_cert(states, start, target):
    import d_certify
    return d_certify.certificate(states, tuple(start), tuple(target), "engine path")


Y = ["xxxxyXy", "xxxxxxxyyyyy"]                      # T(4;7,5), relators in the engine's order
Y_PATH = [("xxxxyXy", "xxxxxxxyyyyy"), ("xxxxyXy", "xxxyyyyxY"), ("xxxxyXy", "xyXYYYXy")]
Y2 = ["xxxxyXy", "xyXYYYXy"]                         # double-T(2,.) form: types T(2,5), T(2,3)
AK3 = ["xxxYYYY", "xyxYXY"]


def y_certs():
    c1 = engine_path_cert(Y_PATH, Y, Y2)                         # Y -> Y2
    C = run(Y, c1["moves"])
    for i in (0, 1):
        C.to(i, Y2[i])
    c1 = C.cert(Y2, "TH02: Y = T(4;7,5) -> Y' = (x^4yXy, xyXY^3Xy) (types T(2,5), T(2,3)); "
                "engine path of two A-frozen cyclic products expanded by d_certify.")
    c2, bt = auto_reflect(Y2, 1, "of xyXY^3Xy (type T(2,3)) on Y'")   # Y2 -> bt(Y2)
    c3, bA = auto_reflect(Y, 0, "of x^4yXy on Y")                      # Y -> bA(Y)
    to_bt = c1["moves"] + c2["moves"] + transport_moves(reverse_moves(c1["moves"]), bt)
    moves = c3["moves"] + transport_moves(to_bt, bA)
    h = compose(bA, bt); M = matrix(h)
    C = run(Y, moves)
    c4 = C.cert([subst(w, h) for w in Y],
                "TH02 Theorem 6: Y = T(4;7,5) -> h(Y) exactly, h = beta_A o beta_t = (x -> %s, y -> %s), "
                "matrix (rows) %s, trace %d (hyperbolic): the stabilizer of the class of Y is infinite."
                % (h["x"], h["y"], M, M[0][0] + M[1][1]))
    return {"th02_y_to_double_form.json": c1, "th02_y_reflect_t.json": c2, "th02_y_hyperbolic.json": c4}, (bA, bt, h)


def self_test():
    for w, R, n in (("xxxxyXy", ((1, -3), (0, -1)), 5), ("xyyyxYY", ((-1, 0), (-1, 1)), 5),
                    ("xyxYXY", ((0, 1), (1, 0)), 3), ("xyXYYYXy", ((-2, 1), (-3, 2)), 3)):
        for other in ("xxyXYYxy", "yxxYXy", "xxxYYYY"):
            c, beta = auto_reflect([w, other], 0)
            replay(c)
            assert matrix(beta) == R and hidden_reflection(w) == (R, n), (w, matrix(beta))
    certs, (bA, bt, h) = y_certs()
    for c in certs.values():
        replay(c)
    M = matrix(h)
    assert M[0][0] + M[1][1] == 5 and M[0][0] * M[1][1] - M[0][1] * M[1][0] == 1
    for n in range(1, 7):                                         # swap on AK(n), uniform
        ak = [red(pw("x", n) + pw("Y", n + 1)), "xyxYXY"]
        c, beta = auto_reflect(ak, 1); replay(c)
        assert matrix(beta) == ((0, 1), (1, 0))
    # Theorem 5: G's form (psi(W_n), b) of AK(n): reflection [[-1,3],[0,1]] for every n, and an
    # independent exact check of research-g Theorem G1 (psi(W_n) ~ (x^n Y^(n+1))^+-1 mod <<b>>)
    from th02_acm import Frozen, tword, canon, I2
    psi = {"x": "xyx", "y": "yx"}
    M0 = next(M for M in (((a, b), (c, d)) for a in range(-2, 3) for b in range(-2, 3)
                          for c in range(-2, 3) for d in range(-2, 3) if a * d - b * c in (1, -1))
              if canon(tword(M, 1)) == canon("xyxYXY"))
    fr = Frozen(M0, 1)
    for n in range(1, 7):
        Wn = "xy" * n + "x" + "Y" + "XY" * n
        wn = cycred(subst(Wn, psi))
        assert hidden_reflection(wn) == (((-1, 3), (0, 1)), 2 * n + 1), (n, hidden_reflection(wn))
        ak = red(pw("x", n) + pw("Y", n + 1))
        assert fr.cls(wn) in (fr.cls(ak), fr.cls(inv(ak))), n
        c, beta = auto_reflect([wn, "xyxYXY"], 0); replay(c)
        assert matrix(beta) == ((-1, 3), (0, 1))
    print("th02_auto self-test OK")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    elif "--write" in sys.argv:
        out = os.path.join(os.path.dirname(HERE), "certificates")
        certs, _ = y_certs()
        certs["th02_ak3_swap_hidden.json"] = auto_reflect(AK3, 1, "of the braid relator on AK(3) (matrix = swap)")[0]
        for name, c in certs.items():
            res = replay(c)
            json.dump(c, open(os.path.join(out, name), "w"), separators=(",", ":"))
            print(name, json.dumps(res)[:300])
    else:
        print(__doc__)
