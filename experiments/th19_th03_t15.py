"""TH19 partial independent check of TH03 Prop. T15 (second move: is c conjugate to a primitive element in G_{k'} = <x,y | k'>?)
for the five first-move targets k' that satisfy Brown's criterion and are decided by field-valued twisted traces:
k_3 = xxxYXyy, XYXyxxxy, XyyxYxyxY (rational, degree 3), XYxxyXy (F_2, degree 6), XyyxYYxy (F_2, degree 4).
Own Magnus rewriting: t = y x^m (m = x-exponent of k'), t_i = x^i t x^-i, G_{k'} = F(t_lo..t_{hi-1}) x|_psi <x>.
Primitive candidates of degree 1 are x t^j = (t_1^j, 1).  Not covered here: XyyxYxYxy (Z/9 traces), XYYxyxyXy (ascending HNN)."""
import sys, io, contextlib
from fractions import Fraction as Fr
sys.path.insert(0, "experiments")
with contextlib.redirect_stdout(io.StringIO()):
    import th19_th03_tt as TT
def winv(w): return [(i, -e) for (i, e) in reversed(w)]
def wred(w):
    out = []
    for g in w:
        if out and out[-1][0] == g[0] and out[-1][1] == -g[1]: out.pop()
        else: out.append(g)
    return out
def analyse(kp, c="xyxYYXy"):
    m = kp.count("x") - kp.count("X"); assert kp.count("y") - kp.count("Y") == 1
    def levels(w):                 # (x,y)-word -> list of (t-index, sign), final level;  y = t x^-m, Y = x^m t^-1
        L, out = 0, []
        for ch in w:
            if ch == "x": L += 1
            elif ch == "X": L -= 1
            elif ch == "y": out.append((L, 1)); L -= m
            else: L += m; out.append((L, -1))
        return out, L
    K, L = levels(kp); assert L == 0
    idx = [i for i, _ in K]; lo, hi = min(idx), max(idx); r = hi - lo
    assert idx.count(lo) == 1 and idx.count(hi) == 1 and r >= 1, "Brown's criterion fails"
    def solve(which):              # t_which = word in the other indices
        p = idx.index(which); rest = K[p+1:] + K[:p]; eps = K[p][1]
        return winv(rest) if eps == 1 else rest
    Whi = [(i - lo, e) for i, e in solve(hi)]                 # t_hi in generators g_0..g_{r-1}
    Wlo = [(i - lo - 1, e) for i, e in solve(lo)]             # t_{lo-1} in generators
    def ap(w, fwd):
        out = []
        for (i, e) in w:
            if fwd: img = [(i+1, 1)] if i < r-1 else Whi
            else:   img = [(i-1, 1)] if i >= 1 else Wlo
            out += img if e == 1 else winv(img)
        return wred(out)
    assert all(ap(ap([(i, 1)], True), False) == [(i, 1)] for i in range(r))
    def tgen(Lv):
        w = [(0, 1)]
        for _ in range(abs(Lv - lo)): w = ap(w, Lv > lo)
        return w
    def nf(w):
        toks, Lf = levels(w); u = []
        for (i, e) in toks: u = wred(u + (tgen(i) if e == 1 else winv(tgen(i))))
        return u, Lf
    assert nf(kp) == ([], 0)
    uc, d = nf(c)
    if d == -1: uc, d = nf(c.swapcase()[::-1])
    assert d == 1
    return r, [ap([(i, 1)], True) for i in range(r)], uc, tgen(1)
def decide(kp, D, mod):
    r, psi, uc, P1 = analyse(kp)
    al = TT.Alg(r, D)
    PsiX = {}
    for i in range(r):
        A = al.M(psi[i]); A[()] = A.get((), 0) - 1; PsiX[i] = {mn: v for mn, v in A.items() if v}
    rows = TT.tt_rows(al, PsiX); ns = TT.nullspace(rows, len(al.mons), mod=mod)
    cM = al.M(uc); N = al.M(P1); N[()] = N.get((), 0) - 1; N = {mn: v for mn, v in N.items() if v}
    pows = [{(): 1}]
    for _ in range(D): pows.append(al.mul(pows[-1], N))
    def binom(j, k):
        v = Fr(1)
        for i in range(k): v = v * (j - i) / (i + 1)
        return int(v)
    def val(l, j): return sum(binom(j, k) * TT.ev(al, l, pows[k]) for k in range(D + 1))
    if mod:
        ok = [j for j in range(16) if all((val(l, j) - TT.ev(al, l, cM)) % mod == 0 for l in ns)]
        return r, len(ns), f"residues j mod 16 allowed: {ok}"
    ok = [j for j in range(-400, 401) if all(val(l, j) == TT.ev(al, l, cM) for l in ns)]
    # rigorous for all integers j: take one trace whose polynomial f(j) = val(l,j) - l(c) is not identically zero and
    # bound its roots (Cauchy bound in the monomial basis); the bound must be <= 400
    bound = None
    for l in ns:
        a = [Fr(TT.ev(al, l, pows[k])) for k in range(D + 1)]; a[0] -= TT.ev(al, l, cM)
        mono = [Fr(0)] * (D + 1)                     # sum_k a_k C(j,k) in powers of j
        for k in range(D + 1):
            poly = [Fr(1)]
            for i in range(k):                       # multiply by (j - i)/(i + 1)
                poly = [(poly[t-1] if t >= 1 else 0) - i * (poly[t] if t < len(poly) else 0) for t in range(len(poly) + 1)]
                poly = [x / (i + 1) for x in poly]
            for t, x in enumerate(poly): mono[t] += a[k] * x
        dg = max((t for t in range(D + 1) if mono[t] != 0), default=-1)
        if dg == -1: continue
        b = 0 if dg == 0 else 1 + max(abs(mono[t] / mono[dg]) for t in range(dg))
        bound = b if bound is None else min(bound, b)
    assert bound is not None and bound <= 400, bound
    # a trace whose values on P1^j are constant in j but differ from its value on c excludes every j
    const = any(all(TT.ev(al, l, pows[k]) == 0 for k in range(1, D + 1)) and TT.ev(al, l, {(): 1}) != TT.ev(al, l, cM) for l in ns)
    deg = max((max((k for k in range(D + 1) if TT.ev(al, l, pows[k]) != 0), default=0) for l in ns), default=0)
    return r, len(ns), f"integers j allowed: {ok} (all integers covered: root bound {float(bound):.1f} <= 400)"
for kp, D, mod in [("xxxYXyy", 3, None), ("XYXyxxxy", 3, None), ("XyyxYxyxY", 3, None), ("XYxxyXy", 6, 2), ("XyyxYYxy", 4, 2)]:
    r, dim, res = decide(kp, D, mod)
    print(f"k' = {kp}: rank {r}, twisted traces of degree <= {D} over {'Q' if not mod else 'F_'+str(mod)}: dimension {dim}; {res}")
