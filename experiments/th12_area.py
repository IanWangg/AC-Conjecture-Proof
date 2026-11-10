"""TH12: generator area of AK(n), count-matrix calculus, and linear move bounds.

Standard library only.  `python3 experiments/th12_area.py --selftest` checks:
 (1) the explicit free-group identities expressing x and y as products of
     conjugates of r^{+-1}, s^{+-1} over AK(n) (Theorem 2), n = 1..NMAX;
 (2) the permutation model of Theorem 4 (r acts trivially, Fix(s) = [1,n-3]);
 (3) the SL_2(Z) facts used in Theorem 3 (exhaustive over transvection words);
 (4) the Fibonacci bound of Theorem 1 (exhaustive over L/R words);
 (5) the backward bookkeeping of Theorem 1 on the repository's AK(1), AK(2) certificates
     and on 200 random reversed instruction paths; (6) verified area bounds over P_3.
Words: x,y and X,Y (uppercase = inverse).
"""
import itertools, json, os, sys

def red(w):
    out = []
    for c in w:
        if out and out[-1] == c.swapcase(): out.pop()
        else: out.append(c)
    return "".join(out)
def inv(w): return w.swapcase()[::-1]
def conj(g, u): return red(g + u + inv(g))          # g u g^-1
def prod(factors, rel):                              # factors: (g, name, sign)
    w = ""
    for g, name, e in factors:
        u = rel[name] if e > 0 else inv(rel[name])
        w = red(w + conj(g, u))
    return w
def ak(n): return {"r": "x"*n + "Y"*(n+1), "s": "xyxYXY"}

def x_factors(n):
    D = "xyx"
    f = [(red(inv(D) + "y"*i), "s", +1) for i in range(n+1)]
    return f + [(inv(D), "r", -1), ("XY", "r", +1), ("X", "r", -1)]
def y_factors(n):
    f = [("", "r", -1)] + [("y"*i, "s", +1) for i in range(n)]
    return f + [(red("y"*n + "x" + "Y"*n), "r", -1), (red("y"*n + "x" + "Y"*(n+1)), "r", +1)]

def check_identities(nmax):
    for n in range(1, nmax+1):
        rel = ak(n)
        fx, fy = x_factors(n), y_factors(n)
        assert prod(fx, rel) == "x", n
        assert prod(fy, rel) == "y", n
        cx = (sum(1 for f in fx if f[1] == "r"), sum(1 for f in fx if f[1] == "s"))
        cy = (sum(1 for f in fy if f[1] == "r"), sum(1 for f in fy if f[1] == "s"))
        assert cx == (3, n+1) and cy == (3, n), (n, cx, cy)
        # the r-conjugators of the x-identity have length <= 3 for every n
        assert max(len(g) for g, nm, e in fx if nm == "r") <= 3
    return nmax

def check_model(nmax):
    for n in range(4, nmax+1):
        px = {i: i+1 for i in range(1, n)}; px[n] = 1; px[0] = 0
        py = {i: i+1 for i in range(0, n)}; py[n] = 0
        act = {"x": px, "y": py, "X": {v: k for k, v in px.items()}, "Y": {v: k for k, v in py.items()}}
        def ap(p, w):
            for c in w: p = act[c][p]
            return p
        rel = ak(n)
        assert all(ap(p, rel["r"]) == p for p in range(n+1))
        fix = [p for p in range(n+1) if ap(p, rel["s"]) == p]
        assert fix == list(range(1, n-2)), (n, fix)
        for p in range(1, n+1):                      # +-1 behaviour inside [1,n]
            for c, d in (("x", 1), ("y", 1), ("X", -1), ("Y", -1)):
                if 1 <= p+d <= n: assert act[c][p] == p+d
    return nmax

def mul(A, B):
    return ((A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]),
            (A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]))
I2 = ((1, 0), (0, 1)); L = ((1, 1), (0, 1)); R = ((1, 0), (1, 1))
Li = ((1, -1), (0, 1)); Ri = ((1, 0), (-1, 1)); Sp = ((0, 1), (-1, 0))
TV = {"L": L, "R": R, "l": Li, "r": Ri}
ABS = {"L": L, "R": R, "l": L, "r": R}
def neg(A): return tuple(tuple(-v for v in row) for row in A)

def check_sl2(nmax):
    """For Sigma0 = [[-1,n+1],[-1,n]]: all words d*t_1..t_mu (d in {+-I,+-S'})
    of length mu <= n+2 equal to Sigma0, with their unsigned products."""
    res = {}
    for n in range(1, nmax+1):
        S0 = ((-1, n+1), (-1, n))
        found = {}
        for mu in range(0, n+3):
            for word in itertools.product("LRlr", repeat=mu):
                M = I2; C = I2
                for c in word: M = mul(M, TV[c]); C = mul(C, ABS[c])
                for dn, d in (("I", I2), ("-I", neg(I2)), ("S", Sp), ("-S", neg(Sp))):
                    if mul(d, M) == S0:
                        Cd = C if dn in ("I", "-I") else mul(((0, 1), (1, 0)), C)
                        found.setdefault(mu, []).append(("".join(word), dn, Cd))
        mus = sorted(found)
        assert mus[0] == n+1, (n, mus)
        for w, dn, C in found[n+1]:                   # minimal words: C = |Sigma0|
            assert C == ((1, n+1), (1, n)), (n, w, C)
        ok = [(w, dn, C) for w, dn, C in found.get(n+2, []) if C[0][0] >= 3 and C[1][0] >= 3
              and C[0][1] >= n+1 and C[1][1] >= n]
        expect = sorted("L" + "R"*(j-2) + "L" + "r" + "l"*(n-j+1) for j in range(3, n+2))
        assert sorted(w for w, dn, C in ok) == expect, (n, ok)
        assert all(dn in ("I", "-I") for w, dn, C in found.get(n+2, []))
        res[n] = (len(found[n+1]), len(found.get(n+2, [])), len(ok))
    return res

def check_fib(mmax):
    F = [0, 1]
    while len(F) < mmax+5: F.append(F[-1]+F[-2])
    for mu in range(0, mmax+1):
        best_sum = best_row = best_ent = 0
        for word in itertools.product((L, R), repeat=mu):
            M = I2
            for t in word: M = mul(M, t)
            best_sum = max(best_sum, sum(map(sum, M)))
            best_row = max(best_row, sum(M[0]), sum(M[1]))
            best_ent = max(best_ent, max(map(max, M)))
        assert (best_ent, best_row, best_sum) == (F[mu+1], F[mu+2], F[mu+3]), mu
    return mmax

def bookkeeping(cert):
    """Theorem 1 made executable: from an ordinary-ac-elementary-v1 certificate
    ending at (x,y), build explicit expressions of x and y as products of
    conjugates of the START relators and verify them by free reduction."""
    assert cert["format"] == "ordinary-ac-elementary-v1"
    assert [red(w) for w in cert["target"]] == ["x", "y"]
    start = [red(w) for w in cert["start"]]
    moves = cert["moves"]
    expr = {"x": [("", 0, 1)], "y": [("", 1, 1)]}
    for mv in reversed(moves):
        op, i = mv["op"], mv["i"]
        for wname in expr:
            new = []
            for g, c, e in expr[wname]:
                if c != i: new.append((g, c, e)); continue
                if op == "invert": new.append((g, c, -e))
                elif op == "conjugate": new.append((red(g + mv["g"]), c, e))
                elif op == "multiply":
                    j = mv["j"]
                    new += [(g, i, 1), (g, j, 1)] if e > 0 else [(g, j, -1), (g, i, -1)]
            expr[wname] = new
    out = {}
    for wname in ("x", "y"):
        w = ""
        for g, c, e in expr[wname]:
            w = red(w + conj(g, start[c] if e > 0 else inv(start[c])))
        assert w == wname, "bookkeeping failed"
        cnt = [sum(1 for f in expr[wname] if f[1] == c) for c in (0, 1)]
        sgn = [sum(f[2] for f in expr[wname] if f[1] == c) for c in (0, 1)]
        out[wname] = {"count": cnt, "signed": sgn, "radius": max(len(f[0]) for f in expr[wname])}
    mu = sum(1 for mv in moves if mv["op"] == "multiply")
    kappa = sum(1 for mv in moves if mv["op"] == "conjugate")
    F = [0, 1]
    while len(F) < mu+5: F.append(F[-1]+F[-2])
    tot = sum(out[w]["count"][c] for w in out for c in (0, 1))
    assert tot <= F[mu+3] and all(sum(out[w]["count"]) <= F[mu+2] for w in out)
    assert all(out[w]["radius"] <= kappa for w in out)
    return {"start": start, "moves": len(moves), "mu": mu, "kappa": kappa, "x": out["x"], "y": out["y"]}

def transport(cert):
    """Expressions of the TARGET relators over the START relators of a certificate
    (Theorem 1 for an arbitrary target).  Returns (factor lists, count matrix)."""
    start = [red(w) for w in cert["start"]]; target = [red(w) for w in cert["target"]]
    expr = [[("", 0, 1)], [("", 1, 1)]]
    for mv in reversed(cert["moves"]):
        op, i = mv["op"], mv["i"]
        for t in (0, 1):
            new = []
            for g, c, e in expr[t]:
                if c != i: new.append((g, c, e)); continue
                if op == "invert": new.append((g, c, -e))
                elif op == "conjugate": new.append((red(g + mv["g"]), c, e))
                else:
                    j = mv["j"]
                    new += [(g, i, 1), (g, j, 1)] if e > 0 else [(g, j, -1), (g, i, -1)]
            expr[t] = new
    for t in (0, 1):
        w = ""
        for g, c, e in expr[t]:
            w = red(w + conj(g, start[c] if e > 0 else inv(start[c])))
        assert w == target[t], "transport failed"
    cnt = [[sum(1 for f in expr[t] if f[1] == c) for c in (0, 1)] for t in (0, 1)]
    return expr, cnt

def reverse_cert(cert):
    mv2 = []
    for mv in reversed(cert["moves"]):
        if mv["op"] == "invert": mv2.append(dict(mv))
        elif mv["op"] == "conjugate": mv2.append({"op": "conjugate", "i": mv["i"], "g": mv["g"].swapcase()})
        else:
            j = mv["j"]
            mv2 += [{"op": "invert", "i": j}, {"op": "multiply", "i": mv["i"], "j": j}, {"op": "invert", "i": j}]
    return {"format": cert["format"], "start": cert["target"], "target": cert["start"], "moves": mv2}

def area_over_p3(certpath):
    """Verified upper bounds for Area_{P_3}(x), Area_{P_3}(y): compose (I_x),(I_y)
    with the expressions of r, s over P_3 = (c,k) read off K's certificate."""
    cert = json.load(open(certpath))
    start = [red(w) for w in cert["start"]]
    idx = {"r": start.index("xxxYYYY"), "s": start.index("xyxYXY")}
    rexpr, cnt = transport(reverse_cert(cert))       # AK(3) relators over P_3
    P = [red(w) for w in cert["target"]]
    out = {}
    for wname, fac in (("x", x_factors(3)), ("y", y_factors(3))):
        w = ""; c = [0, 0]
        for g, nm, e in fac:
            sub = rexpr[idx[nm]]
            sub = sub if e > 0 else [(f, j, -d) for f, j, d in reversed(sub)]
            for f, j, d in sub:
                w = red(w + conj(red(g + f), P[j] if d > 0 else inv(P[j]))); c[j] += 1
        assert w == wname
        out[wname] = c
    return {"AK3 relators over P3 (count matrix, rows in certificate start order)": cnt, "x": out["x"], "y": out["y"]}

def random_paths(trials=200, length=30, seed=12):
    """Theorem 1 stress test: random instruction paths from (x,y) outwards, reversed
    into trivialization certificates, then pushed through bookkeeping()."""
    import random
    rnd = random.Random(seed); worst = (0, 0)
    for _ in range(trials):
        moves = []
        for _ in range(length):
            q = rnd.random(); i = rnd.randrange(2)
            if q < 0.2: moves.append({"op": "invert", "i": i})
            elif q < 0.45: moves.append({"op": "multiply", "i": i, "j": 1 - i})
            else: moves.append({"op": "conjugate", "i": i, "g": rnd.choice("xXyY")})
        st = ["x", "y"]
        for mv in moves:
            i = mv["i"]
            if mv["op"] == "invert": st[i] = inv(st[i])
            elif mv["op"] == "multiply": st[i] = red(st[i] + st[mv["j"]])
            else: st[i] = conj(mv["g"], st[i])
        fwd = {"format": "ordinary-ac-elementary-v1", "start": ["x", "y"], "target": st, "moves": moves}
        res = bookkeeping(reverse_cert(fwd))          # asserts identities, Fibonacci, radius <= kappa
        worst = max(worst, (res["mu"], res["x"]["count"][0] + res["x"]["count"][1]))
    return trials, worst

def ak1_calibration():
    """All shortest instruction paths AK(1) -> (x,y) (E: d_F = 8): the set of
    (mu, kappa) they realize, by bidirectional BFS of depth 4 + 4."""
    def nbrs(st):
        a, b = st
        yield (inv(a), b), "I"; yield (a, inv(b)), "I"; yield (b, a), "S"
        yield (red(a + b), b), "M"; yield (red(a + inv(b)), b), "M"
        yield (a, red(b + a)), "M"; yield (a, red(b + inv(a))), "M"
        for g in "xXyY":
            yield (red(inv(g) + a + g), b), "C"; yield (a, red(inv(g) + b + g)), "C"
    def layers(start, depth):
        cur = {start: {(0, 0)}}; seen = {start: 0}; out = [cur]
        for d in range(1, depth + 1):
            nxt = {}
            for st, pk in cur.items():
                for st2, typ in nbrs(st):
                    if st2 in seen and seen[st2] < d: continue
                    s = nxt.setdefault(st2, set())
                    for mu, ka in pk: s.add((mu + (typ == "M"), ka + (typ == "C")))
            for st2 in nxt: seen[st2] = d
            cur = nxt; out.append(cur)
        return out
    A = layers(("xYY", "xyxYXY"), 4); B = layers(("x", "y"), 4)
    for total in range(0, 9):
        pk = set()
        for i in range(max(0, total - 4), min(4, total) + 1):
            for st in set(A[i]) & set(B[total - i]):
                for m1, k1 in A[i][st]:
                    for m2, k2 in B[total - i][st]: pk.add((m1 + m2, k1 + k2))
        if pk: return total, sorted(pk)
    return None

def check_pn_braid(nmax):
    """Exact identities over P_n = (c, k), c = xyxYYXy, k = x^n YXyy, with a = x, b = yxY:
       y = c^-1 a b a^-n k   and
       a b a b^-1 a^-1 b^-1 = [u k u^-1][u a^-1 k^-1 a u^-1] c [b c^-1 b^-1],  u = a b a^(1-n)."""
    for n in range(2, nmax+1):
        rel = {"c": "xyxYYXy", "k": "x"*n + "YXyy"}
        a, b = "x", "yxY"
        assert red(inv(rel["c"]) + a + b + inv(a)*n + rel["k"]) == "y"
        u = red(a + b + inv(a)*(n-1))
        lhs = red(a + b + a + inv(b) + inv(a) + inv(b))
        fac = [(u, "k", 1), (red(u + inv(a)), "k", -1), ("", "c", 1), (b, "c", -1)]
        assert prod(fac, rel) == lhs, n
    return nmax

def area_over_pn(nmax):
    """Proposition 8: with a = x, b = yxY the AK relators r(a,b) = a^n b^-(n+1) and
    s(a,b) = abaBAB have 3 resp. 4 factors over P_n = (c,k); substituting into (I_x)
    gives an explicit expression of x over P_n with 4n+13 factors, checked by free reduction."""
    sub = {"x": "x", "y": "yxY", "X": "X", "Y": "yXY"}
    S = lambda w: red("".join(sub[ch] for ch in w))
    out = {}
    for n in range(2, nmax+1):
        rel = {"c": "xyxYYXy", "k": "x"*n + "YXyy"}
        a, b = "x", "yxY"
        u = red(a + b + inv(a)*(n-1))
        sfac = [(u, "k", 1), (red(u + inv(a)), "k", -1), ("", "c", 1), (b, "c", -1)]
        rfac = [("", "k", 1), ("y", "k", -1), (red(b*n + inv(a)), "c", -1)]
        assert prod(sfac, rel) == S("xyxYXY") and prod(rfac, rel) == S("x"*n + "Y"*(n+1)), n
        fac = []
        for g, nm, e in x_factors(n):
            subf = sfac if nm == "s" else rfac
            subf = subf if e > 0 else [(f, j, -d) for f, j, d in reversed(subf)]
            fac += [(red(S(g) + f), j, d) for f, j, d in subf]
        assert prod(fac, rel) == "x", n
        cnt = (sum(1 for f in fac if f[1] == "c"), sum(1 for f in fac if f[1] == "k"))
        assert cnt == (2*n+5, 2*n+8), (n, cnt)
        out[n] = cnt
    return nmax, out[3]

def pn_area3(R, ns=(2, 3, 4)):
    """Experiment: is x or y a product of <= 3 conjugates of c^{+-1}, k^{+-1} over P_n
    with all conjugators of length <= R?  (meet in the middle: pairs vs singles)"""
    ball = [""]; layer = [""]
    for _ in range(R):
        layer = [w + ch for w in layer for ch in "xXyY" if not (w and w[-1] == ch.swapcase())]
        ball += layer
    res = {}
    for n in ns:
        rel = {"c": "xyxYYXy", "k": "x"*n + "YXyy"}
        S = set(conj(g, u) for g in ball for u in (rel["c"], inv(rel["c"]), rel["k"], inv(rel["k"])))
        pairs = set(red(u + v) for u in S for v in S)
        res[n] = {tg: (tg in S) or any(red(inv(u) + tg) in pairs for u in S) for tg in ("x", "y")}
    return res

def bounded_area_pn(nmax):
    """Proposition 9: over P_n = (c,k) the generator x has an explicit expression with
    11 factors for EVERY n >= 2 (7 on c, 4 on k), and y one with 11(n+2)+2 factors.
    Notation a = x, b = yxY, s = abaBAB (4 factors by (P2)), C = y c y^-1,
    Psi = a b a^-2 b = [(abAA) C (abAA)^-1][(abA) C (abA)^-1] C^-1 (y s y^-1),
    b = (a^-1 s a) (aBA) Psi (aBA)^-1,  x = y^-1 b y,  y = c^-1 a b a^-n k."""
    def cj(g, fac): return [(red(g + f), j, d) for f, j, d in fac]
    def invf(fac): return [(f, j, -d) for f, j, d in reversed(fac)]
    for n in range(2, nmax+1):
        rel = {"c": "xyxYYXy", "k": "x"*n + "YXyy"}
        a, b, A, B = "x", "yxY", "X", "yXY"
        u = red(a + b + A*(n-1))
        sfac = [(u, "k", 1), (red(u + A), "k", -1), ("", "c", 1), (b, "c", -1)]          # s(a,b)
        C = [("y", "c", 1)]
        Psi = cj(red(a + b + A + A), C) + cj(red(a + b + A), C) + invf(C) + cj("y", sfac)
        assert prod(Psi, rel) == red(a + b + A + A + b), n
        bfac = cj(A, sfac) + cj(red(a + B + A), Psi)
        assert prod(bfac, rel) == b, n
        xfac = cj("Y", bfac)                                                              # x = y^-1 b y
        assert prod(xfac, rel) == "x" and len(xfac) == 11, n
        assert (sum(1 for f in xfac if f[1] == "c"), sum(1 for f in xfac if f[1] == "k")) == (7, 4)
        yfac = [("", "c", -1)] + xfac + bfac + invf(xfac)*n + [("", "k", 1)]              # y = c^-1 a b a^-n k
        assert prod(yfac, rel) == "y" and len(yfac) == 11*(n+2) + 2, n
    return nmax

def check_s_nfree():
    """(P2) in n-independent form: s(a,b) = (aba) [u, x^-1] (aba)^-1 c (b c^-1 b^-1), u = YXyy,
    where [u, x^-1] = u X U x = x^-n (k X K x) x^n for every n."""
    a, b, c, u = "x", "yxY", "xyxYYXy", "YXyy"
    lhs = red(a + b + a + inv(b) + inv(a) + inv(b))
    com = red(u + "X" + inv(u) + "x")
    assert red(a + b + a + com + inv(a + b + a) + c + b + inv(c) + inv(b)) == lhs
    for n in range(0, 20):
        k = "x"*n + u
        assert red("X"*n + k + "X" + inv(k) + "x" + "x"*n) == com
    return True

def _layers(start, depth):
    def nbrs(st):
        a, b = st
        yield (inv(a), b), "I"; yield (a, inv(b)), "I"; yield (b, a), "S"
        yield (red(a + b), b), "M"; yield (red(a + inv(b)), b), "M"
        yield (a, red(b + a)), "M"; yield (a, red(b + inv(a))), "M"
        for g in "xXyY":
            yield (red(inv(g) + a + g), b), "C"; yield (a, red(inv(g) + b + g)), "C"
    cur = {start: {(0, 0)}}; seen = {start: 0}; out = [cur]
    for d in range(1, depth + 1):
        nxt = {}
        for st, pk in cur.items():
            for st2, typ in nbrs(st):
                if st2 in seen and seen[st2] < d: continue
                s = nxt.setdefault(st2, set())
                for mu, ka in pk: s.add((mu + (typ == "M"), ka + (typ == "C")))
        for st2 in nxt: seen[st2] = d
        cur = nxt; out.append(cur)
    return out

def window_calibration(ns=(2, 3, 4)):
    """Sharpness of Propositions 6 and 7 on the AC-trivial family V_n = (x^n Y^(n+1), xY):
    same Sigma as AK(n) (so mu >= n+1) and the model of Lemma 4.1 with window [1,n-1]
    (so kappa >= n-1).  Exhaustive bidirectional BFS (5+5) over the 15 instructions."""
    B = _layers(("x", "y"), 5); out = {}
    for n in ns:
        A = _layers(("x"*n + "Y"*(n+1), "xY"), 5); best = None
        for total in range(0, 11):
            pk = set()
            for i in range(max(0, total - 5), min(5, total) + 1):
                for st in set(A[i]) & set(B[total - i]):
                    for m1, k1 in A[i][st]:
                        for m2, k2 in B[total - i][st]: pk.add((m1 + m2, k1 + k2))
            if pk: best = (total, sorted(pk)); break
        assert best and best[0] == 2*n + 2, (n, best)
        assert min(m for m, k in best[1]) == n + 1 and min(k for m, k in best[1]) == n - 1, (n, best)
        out[n] = best
    return out

def vn_path(nmax):
    """Explicit trivialization of V_n = (x^n Y^(n+1), xY) by 2n+2 instructions
    (mu = n+2, kappa = n, no inversion or swap), for every n >= 2."""
    for n in range(2, nmax+1):
        u0, u1 = "x"*n + "Y"*(n+1), "xY"; steps = 0
        for _ in range(n-1):
            u0 = red(u0 + inv(u1)); u0 = red("X" + u0 + "x"); steps += 2      # x^j Y^(j+1) -> x^(j-1) Y^j
        assert u0 == "xYY"
        u1 = red(u1 + inv(u0)); u1 = red("X" + u1 + "x")                       # u1 = y
        u0 = red(u0 + u1); u0 = red(u0 + u1); steps += 4                       # u0 = x
        assert (u0, u1) == ("x", "y") and steps == 2*n + 2, n
    return nmax

def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    if "--cert" in argv:
        path = argv[argv.index("--cert") + 1]
        print(json.dumps(bookkeeping(json.load(open(path)))))
        return
    if "--pn-area3" in argv:
        R = int(argv[argv.index("--pn-area3") + 1])
        print("area <= 3 over P_n with radius <= %d (n: {x: found, y: found}):" % R, pn_area3(R))
        return
    if "--selftest" in argv:
        print("identities x,y over AK(n) verified for n = 1..%d" % check_identities(40))
        print("permutation model verified for n = 4..%d" % check_model(60))
        res = check_sl2(5)
        print("SL2(Z) word classification (n: #words mu=n+1, #words mu=n+2, #admissible):", res)
        print("Fibonacci bounds verified for mu <= %d" % check_fib(14))
        for name in ("e_ak1_trivialization.json", "e_ak2_peak13_trivialization.json"):
            p = os.path.join(here, "..", "certificates", name)
            if os.path.exists(p):
                print(name, json.dumps(bookkeeping(json.load(open(p)))))
        for name in ("k_ak3_to_p3.json", "k_ak3_to_p3_uniform.json"):
            p = os.path.join(here, "..", "certificates", name)
            if os.path.exists(p):
                print("P_3 transport via", name, json.dumps(area_over_p3(p)))
        print("random reversed paths through bookkeeping (trials, (max mu, its x-area)):", random_paths())
        print("P_n braid identity (area <= 4 for s(x, yxY) over P_n) verified for n = 2..%d" % check_pn_braid(40))
        print("Proposition 8 (x over P_n with 4n+13 factors) verified for n = 2..%d; counts (c,k) for n=3: %s" % area_over_pn(30))
        print("Proposition 9 (x over P_n with 11 factors for every n; y with 11(n+2)+2) verified for n = 2..%d" % bounded_area_pn(30))
        print("n-independent form of (P2) verified:", check_s_nfree())
        print("V_n = (x^n Y^(n+1), xY): d_F and (mu,kappa) of all shortest paths:", window_calibration())
        print("explicit (2n+2)-instruction trivialization of V_n verified for n = 2..%d" % vn_path(40))
        cal = ak1_calibration()
        assert cal[0] == 8 and all(mu >= 4 and ka >= 1 for mu, ka in cal[1])
        print("AK(1): d_F = %d; (mu, kappa) of its shortest paths: %s" % cal)
        print("TH12 selftest OK")
        return
    print(__doc__)

if __name__ == "__main__":
    main(sys.argv[1:])
