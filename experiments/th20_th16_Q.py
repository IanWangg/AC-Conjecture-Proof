#!/usr/bin/env python3
"""TH20 check of TH16 Theorem H(a),(b): Q = (q1, q2) = (xxyXYY, xxxYYXy) is an ACM local minimum.
(a) in G_{q1}: transport by beta = (x -> xYX, y -> YX) to G_c (beta(q1) ~ c); for every cyclically reduced W,
    |W| <= 6, degree +-1, separate W from q2^{+-1} by exact invariants of G_c: own holonomy (trace of squares,
    both twists) and TH11's (kappa, Jhat).   (b) in G_{q2}: sieve by all homomorphisms G_{q2} -> S_5, S_6
    (cycle type of W vs q1^{+-1}).  A word NOT separated is listed (no conclusion for it)."""
import sys, itertools
sys.dont_write_bytecode = True
sys.argv = sys.argv[:1] + ["1", "1"]
from th20_lib import red, inv, cyc, conj, aut
import o_gc as O, th11_nil as T, th20_theta_holonomy as H
q1, q2, c = "xxyXYY", "xxxYYXy", "xyxYYXy"
beta = {"x": "xYX", "y": "YX"}
assert conj(aut(beta, q1), c), aut(beta, q1)
def words(L):
    def rec(p):
        if len(p) == L:
            if p[0] != p[-1].swapcase(): yield p
            return
        for ch in "xXyY":
            if not p or p[-1] != ch.swapcase(): yield from rec(p + ch)
    yield from rec("")
def wp(u):
    out = []
    for ch in u:
        l = ch.lower(); e = 1 if ch.islower() else -1
        if out and out[-1][0] == l: out[-1] = (l, out[-1][1] + e)
        else: out.append((l, e))
    return out
def inv_c(word):           # invariants in G_c of the element beta(word), normalized to degree +1
    u, k = O.nf(aut(beta, word))
    if k == -1: u, k = O.nf(inv(aut(beta, word)))
    assert k == 1, k
    sq = lambda v: H.tau(H.W(*wp(v))) if v else None
    taus = frozenset([sq(O.red(u + O.phi_pow(1, u))), sq(O.red(O.phi_pow(1, u) + O.phi_pow(2, u)))])
    kap, J = T.KJ(u)
    return taus, (kap, J)
tq = inv_c(q2); left = []
for L in range(1, 7):
    for w in words(L):
        e = sum((ch == "x") - (ch == "X") + (ch == "y") - (ch == "Y") for ch in w)
        if abs(e) != 1: continue
        ti = inv_c(w)
        if ti[0] & tq[0] and ti[1] == tq[1]: left.append(w)
print("(a) words of length <= 6, degree +-1, not separated from q2^{+-1} in G_{q1}:", left)
# (b) homomorphisms G_{q2} -> S_n
def perm_mul(p, q): return tuple(q[i] for i in p)          # apply p then q
def perm_inv(p):
    r = [0] * len(p)
    for i, j in enumerate(p): r[j] = i
    return tuple(r)
def ev(word, X, Y):
    g = {"x": X, "X": perm_inv(X), "y": Y, "Y": perm_inv(Y)}; r = tuple(range(len(X)))
    for ch in word: r = perm_mul(r, g[ch])
    return r
def ctype(p):
    seen = set(); t = []
    for i in range(len(p)):
        if i in seen: continue
        j, l = i, 0
        while j not in seen: seen.add(j); j = p[j]; l += 1
        t.append(l)
    return tuple(sorted(t))
cand = [w for L in range(1, 6) for w in words(L) if abs(sum((ch == "x") - (ch == "X") + 2 * ((ch == "y") - (ch == "Y")) for ch in w)) == 1]
alive = set(cand)
for n in (5, 6):
    perms = list(itertools.permutations(range(n))); idp = tuple(range(n))
    for X in perms:
        for Y in perms:
            if ev(q2, X, Y) != idp: continue
            t1 = {ctype(ev(q1, X, Y)), ctype(ev(inv(q1), X, Y))}
            alive = {w for w in alive if ctype(ev(w, X, Y)) in t1}
    print("(b) after S_%d: %d of %d candidate words (length <= 5, degree +-1 in G_{q2}) not separated from q1^{+-1}" % (n, len(alive), len(cand)), sorted(alive)[:12])
