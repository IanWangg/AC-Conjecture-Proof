#!/usr/bin/env python3
"""TH15, Lemma T (hidden transvection of a Baumslag-Solitar relator) as strict certificates.

beta = x^-1 y^m x y^-n2,  T_k = (x -> x y^k, y -> y),  k = (n2 - m) * i,  d = y^(m i).
In F:  d x d^-1 = E_i * T_k(x),  E_i = y^(mi) x y^(-n2 i) x^-1 = a product of |i| conjugates of
(x beta x^-1)^(+-1).  For any word s = t_1...t_L put W_j = T_k(t_1..t_j) d t_(j+1)..t_L d^-1; then
W_0 = d s d^-1, W_L = T_k(s) and W_j = W_(j-1) * (conjugates of beta^(+-1)).  The certificate is:
conjugate s by d; insert the conjugates one by one (conjugate beta, [invert], multiply, undo);
finally conjugate beta by y^-k.  It runs from (s, beta) to (T_k(s), T_k(beta)) EXACTLY.

    python3 experiments/th15_hidden.py --selftest
    python3 experiments/th15_hidden.py --ms N W K OUT.json   # MS(N,W) -> MS(N, W(xy^K,y) y^-K)
"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import elementary_verify  # noqa: E402
import th15_aut_family as fam  # noqa: E402

red, inv, INV = fam.red, fam.inv, fam.INV


def ypow(e):
    return "y" * e if e >= 0 else "Y" * (-e)


def bs(m, n2):
    return red("X" + ypow(m) + "x" + ypow(-n2))


def tk(k, w):
    img = {"x": "x" + ypow(k), "X": ypow(-k) + "X", "y": "y", "Y": "Y"}
    return red("".join(img[c] for c in w))


def e_factors(m, n2, i):
    """[(g, eps)] with prod g beta^eps g^-1 == y^(mi) x y^(-n2 i) X in F."""
    if i >= 0:
        fs = [(red(ypow(m * l) + "x"), 1) for l in range(i - 1, -1, -1)]
    else:
        fs = [(red(ypow(-m * (l + 1)) + "x"), -1) for l in range(-i - 1, -1, -1)]
    beta, w = bs(m, n2), ""
    for g, eps in fs:
        w = red(w + g + (beta if eps > 0 else inv(beta)) + inv(g))
    assert w == red(ypow(m * i) + "x" + ypow(-n2 * i) + "X"), (m, n2, i)
    return fs


class Build:
    def __init__(self, s, beta):
        self.st = [red(s), beta]
        self.moves = []

    def conj(self, idx, word):          # r_idx := word r_idx word^-1
        for g in reversed(word):
            self.moves.append({"op": "conjugate", "i": idx, "g": g})
            self.st[idx] = red(g + self.st[idx] + INV[g])

    def insert(self, h, eps):           # r_0 := r_0 * h beta^eps h^-1, beta restored
        self.conj(1, h)
        if eps < 0:
            self.moves.append({"op": "invert", "i": 1})
            self.st[1] = inv(self.st[1])
        self.moves.append({"op": "multiply", "i": 0, "j": 1})
        self.st[0] = red(self.st[0] + self.st[1])
        if eps < 0:
            self.moves.append({"op": "invert", "i": 1})
            self.st[1] = inv(self.st[1])
        self.conj(1, inv(h))


def hidden_transvection(m, n2, i, s):
    """Strict certificate (s, beta) -> (T_k(s), T_k(beta)), k = (n2 - m) i."""
    s = red(s)
    k, d, beta = (n2 - m) * i, ypow(m * i), bs(m, n2)
    E = e_factors(m, n2, i)
    Einv = [(g, -eps) for g, eps in reversed(E)]
    b = Build(s, beta)
    b.conj(0, d)
    txi = inv(tk(k, "x"))
    for j, t in enumerate(s):
        R = red(d + s[j + 1:] + inv(d))
        if t == "x":                    # C = T(x)^-1 E^-1 T(x)
            fs = [(red(txi + g), eps) for g, eps in Einv]
        elif t == "X":                  # C = E
            fs = E
        else:
            fs = []
        for g, eps in fs:
            b.insert(red(inv(R) + g), eps)
        assert b.st[0] == red(tk(k, s[:j + 1]) + R), (j, t)
    b.conj(1, ypow(-k))
    target = [tk(k, s), tk(k, beta)]
    assert b.st == target and target[1] == red(ypow(-k) + beta + ypow(k))
    cert = {"format": "ordinary-ac-elementary-v1", "start": [s, beta], "target": target, "moves": b.moves,
            "description": f"hidden transvection (research-th15 Lemma T): (s, beta) -> (T_k(s), T_k(beta)), "
                           f"beta = x^-1 y^{m} x y^-{n2}, k = {k}, T_k = (x -> x y^k)"}
    r = elementary_verify.replay(cert)
    assert r["endpoint"] == target
    return cert, r


def ms(n, w, k):
    """MS(n,w) = (x^-1 w, beta'_n) -> MS(n, w_k) = (x^-1 w(xy^k,y) y^-k, beta'_n) exactly."""
    cert, _ = hidden_transvection(n, n + 1, k, "X" + w)
    b = Build(cert["target"][0], cert["target"][1])
    b.conj(0, ypow(k))
    b.conj(1, ypow(k))
    wk = red(tk(k, w) + ypow(-k))
    assert b.st == [red("X" + wk), bs(n, n + 1)], (b.st, wk)
    cert["moves"] += b.moves
    cert["target"] = b.st
    cert["description"] = (f"MS({n},{w}) -> MS({n},{wk}) (relator order: x^-1 w, then the BS relator): "
                           f"hidden transvection T_{k} of research-th15 Corollary 6")
    r = elementary_verify.replay(cert)
    assert r["endpoint"] == b.st
    return cert, r, wk


def selftest():
    rnd = random.Random(15)
    cnt = 0
    for m, n2 in [(2, 3), (3, 4), (4, 3), (-4, -3), (1, 2), (2, 5), (3, 1), (-2, 3)]:
        for i in (1, -1, 2, -2):
            for _ in range(6):
                s = red("".join(rnd.choice("xXyY") for _ in range(rnd.randint(1, 9)))) or "x"
                hidden_transvection(m, n2, i, s)
                cnt += 1
    for n in range(2, 9):            # C's bridge word: T(XYxxY) is a rotation of b
        cert, r, wk = ms(n, "YxxY", 1)
        assert red("X" + wk) in fam.rots(fam.B), wk
        cnt += 1
    for n in (2, 3, 4):
        for k in (1, -1, 2, -3):
            for _ in range(4):
                w = red("".join(rnd.choice("xXyY") for _ in range(rnd.randint(2, 8)))) or "y"
                ms(n, w, k)
                cnt += 1
    print(f"selftest passed: {cnt} hidden-transvection certificates built and replayed "
          f"(8 BS relators x^-1 y^m x y^-n', random partners; M_n -> (b-rotation, beta'_n), n = 2..8; random MS(n,w))")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--selftest"]:
        selftest()
    elif a[:1] == ["--ms"]:
        cert, r, wk = ms(int(a[1]), a[2], int(a[3]))
        with open(a[4], "w") as f:
            json.dump(cert, f)
        print(f"MS({a[1]},{a[2]}) -> MS({a[1]},{wk}): {r['moves']} moves, peak {r['peak_total_length']}, wrote {a[4]}")
    else:
        print(__doc__)
