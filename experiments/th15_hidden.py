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
    python3 experiments/th15_hidden.py --sym N K OUT.json    # Sym_N -> T_K(Sym_N); N = 2 is P1
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


def sym_cert(n, k):
    """Sym_n = (x^-1 y^n x y^-(n+1), y^-1 x^n y x^-(n+1)) -> T_k(Sym_n), relators cyclically
    reduced and in this order (for n = 2: P1 of research-i, target as in i_p1_aut_x_xy.json)."""
    bp = bs(n, n + 1)
    s2 = red("Y" + "x" * n + "y" + "X" * (n + 1))
    cert, _ = hidden_transvection(n, n + 1, k, s2)          # (s2, beta') -> (T_k s2, T_k beta')
    b = Build(cert["target"][0], cert["target"][1])
    for i in (0, 1):                                         # cyclically reduce both relators
        while len(b.st[i]) >= 2 and b.st[i][0] == INV[b.st[i][-1]]:
            b.conj(i, INV[b.st[i][0]])
    assert b.st[1] in fam.rots(bp)
    while b.st[1] != bp:
        b.conj(1, INV[b.st[1][0]])
    moves = [{**m, "i": 1 - m["i"], **({"j": 1 - m["j"]} if "j" in m else {})} for m in cert["moves"] + b.moves]
    out = {"format": "ordinary-ac-elementary-v1", "start": [bp, s2], "target": [b.st[1], b.st[0]], "moves": moves,
           "description": f"Sym_{n} = (x^-1 y^{n} x y^-{n + 1}, y^-1 x^{n} y x^-{n + 1}) -> T_{k}(Sym_{n}) "
                          f"(cyclically reduced), T_k = (x -> x y^{k}): hidden transvection of the first "
                          f"relator (research-th15 Lemma T, Corollary 8); n = 2 is P1 = MS(2, x^-2 y^-1 x^2 y)"}
    r = elementary_verify.replay(out)
    assert r["endpoint"] == out["target"]
    assert fam.cyc(tk(k, s2)) in fam.rots(out["target"][1])
    return out, r


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
    for n in range(1, 7):
        for k in (1, -1, 2):
            sym_cert(n, k)
            cnt += 1
    print(f"selftest passed: {cnt} hidden-transvection certificates built and replayed "
          f"(8 BS relators x^-1 y^m x y^-n', random partners; M_n -> (b-rotation, beta'_n), n = 2..8; random MS(n,w); Sym_n, n = 1..6)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--selftest"]:
        selftest()
    elif a[:1] == ["--sym"]:
        cert, r = sym_cert(int(a[1]), int(a[2]))
        with open(a[3], "w") as f:
            json.dump(cert, f)
        print(f"Sym_{a[1]} -> T_{a[2]}(Sym_{a[1]}): {r['moves']} moves, peak {r['peak_total_length']}, "
              f"start {cert['start']}, target {cert['target']}, wrote {a[3]}")
    elif a[:1] == ["--ms"]:
        cert, r, wk = ms(int(a[1]), a[2], int(a[3]))
        with open(a[4], "w") as f:
            json.dump(cert, f)
        print(f"MS({a[1]},{a[2]}) -> MS({a[1]},{wk}): {r['moves']} moves, peak {r['peak_total_length']}, wrote {a[4]}")
    else:
        print(__doc__)
