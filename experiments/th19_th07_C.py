"""TH19 check of TH07 Theorem C in G = <x,y | y x^(n+1) y^-1 = x^n> (w_n = x^n y X^(n+1) Y), beta = yxyXYX = b^-1.
Word problem by Britton reduction (own code).  (1) the explicit conjugacies v_j = x^(n(j-1)) beta x^(-n(j-1)),
e_n = x^(n^2-1) beta x^(-(n^2-1)).  (2) all cyclically reduced words of length <= n+3 conjugate to beta^+-1, by Collins'
lemma with a bounded search over conjugators x^t (|t| <= T): compare with TH07's list (rotations of v_j^+-1, |j| <= n-2,
and of e_n^+-1).  (2) is exhaustive in the words and bounded only in t."""
import sys
sys.path.insert(0, "experiments")
from th19_lib import *
def toks(w):
    out = []
    for c in w:
        if c in "xX":
            e = 1 if c == "x" else -1
            if out and out[-1][0] == "x": out[-1] = ("x", out[-1][1] + e)
            else: out.append(("x", e))
        else: out.append(("y", 1 if c == "y" else -1))
    return [t for t in out if t[1] != 0]
def britton(t, n):
    t = list(t); changed = True
    while changed:
        changed = False
        s = []                      # merge x-powers, drop zeros
        for a in t:
            if a[0] == "x" and s and s[-1][0] == "x": s[-1] = ("x", s[-1][1] + a[1])
            else: s.append(a)
            if s[-1][0] == "x" and s[-1][1] == 0: s.pop()
        t = s
        for i in range(len(t) - 1):
            if t[i][0] != "y": continue
            j = i + 1; k = 0
            if t[j][0] == "x": k = t[j][1]; j += 1
            if j < len(t) and t[j][0] == "y" and t[j][1] == -t[i][1]:
                if t[i][1] == 1 and k % (n + 1) == 0:   new = ("x", k // (n + 1) * n)
                elif t[i][1] == -1 and k % n == 0:      new = ("x", k // n * (n + 1))
                else: continue
                t = t[:i] + [new] + t[j+1:]; changed = True; break
    return t
def trivial(w_tokens, n): return britton(w_tokens, n) == []
def tinv(t): return [(a, -e) for (a, e) in reversed(t)]
def conj_by_xt(v, u, n, T):
    """exists |t| <= T with x^t u x^-t = v ?"""
    return any(trivial([("x", t)] + u + [("x", -t)] + tinv(v), n) for t in range(-T, T + 1))
beta = "yxyXYX"
def conj_to_beta_pm(w, n, T):
    tw = toks(w)
    if sum(e for a, e in tw if a == "y") not in (1, -1): return False
    # cyclic Britton reduction: rotate and reduce until stable
    for _ in range(4 * len(w) + 8):
        r = britton(tw, n)
        if len(r) >= 2 and r[0][0] == "y" or len(r) >= 2 and r[-1][0] == "y":
            r2 = britton(r[1:] + r[:1], n)
        else:
            r2 = britton(r[1:] + r[:1], n) if r else r
        if len(r2) >= len(r) and r2 != r and sum(1 for a in r2 if a[0] == "y") == sum(1 for a in r if a[0] == "y"):
            tw = r2
            # try all rotations for a shorter stable-letter count
            best = min((britton(r[i:] + r[:i], n) for i in range(len(r))), key=lambda z: sum(1 for a in z if a[0] == "y"))
            tw = best; break
        tw = r2
    ny = sum(1 for a in tw if a[0] == "y")
    best = tw
    for i in range(len(tw)):
        z = britton(tw[i:] + tw[:i], n)
        if sum(1 for a in z if a[0] == "y") < sum(1 for a in best if a[0] == "y"): best = z
    tw = best
    if sum(1 for a in tw if a[0] == "y") != 3: return False
    for u in (toks(beta), toks(inv(beta))):
        for i in range(len(tw) + 1):
            v = tw[i:] + tw[:i]
            if v and v[-1][0] == "y":
                for j in range(len(u) + 1):
                    uu = u[j:] + u[:j]
                    if uu and uu[-1][0] == "y" and conj_by_xt(v, uu, n, T): return True
    return False
for n in (3, 4, 5):
    ok1 = all(trivial(toks("x"*(n*(j-1)) if j >= 1 else "X"*(n*(1-j))) + toks(beta) + toks("X"*(n*(j-1)) if j >= 1 else "x"*(n*(1-j)))
                      + tinv(toks("y" + ("x"*j if j >= 0 else "X"*(-j)) + "yXYX")), n) for j in range(-6, 7))
    en = "x"*(n-1) + "yyXY"
    ok2 = trivial(toks("x"*(n*n-1)) + toks(beta) + toks("X"*(n*n-1)) + tinv(toks(en)), n)
    print(f"n={n}: (1) v_j = x^(n(j-1)) beta x^-(n(j-1)) for |j|<=6: {ok1}; e_n = x^(n^2-1) beta x^-(n^2-1): {ok2}")
for n in (3, 4):
    claimed = set()
    for j in range(-(n-2), n-1):
        claimed |= orb("y" + ("x"*j if j >= 0 else "X"*(-j)) + "yXYX")
    claimed |= orb("x"*(n-1) + "yyXY")
    found = set()
    for L in range(1, n + 4):
        for w in cyc_words(L):
            if conj_to_beta_pm(w, n, 12*n): found.add(w)
    print(f"n={n}: (2) words of length <= {n+3} conjugate to beta^+-1 (t-search |t|<={12*n}): {len(found)}; claimed list: {len(claimed)};"
          f" equal: {found == claimed}; found-claimed: {sorted(found-claimed)[:4]}; claimed-found: {sorted(claimed-found)[:4]}")
