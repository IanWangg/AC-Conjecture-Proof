#!/usr/bin/env python3
"""TH20 independent check of TH11's table: coker(1 - phi) on gamma_k/gamma_{k+1} = L_k(Z^2) (free Lie ring,
Lyndon basis), k = 1..8, for phi_ab: X -> Y, Y -> X - Y  (phi(a) = b, phi(b) = b^-1 a).  Own code."""
import sys
from math import gcd
sys.dont_write_bytecode = True
K = 8
def lyndon(n):                       # Lyndon words over {0,1} of length exactly n (Duval)
    out = []; w = [-1]
    while w:
        w[-1] += 1
        if len(w) == n: out.append(tuple(w))
        m = len(w)
        while len(w) < n: w.append(w[len(w) - m])
        while w and w[-1] == 1: w.pop()
    return out
LYN = {n: lyndon(n) for n in range(1, K + 1)}
ALL = {w for n in LYN for w in LYN[n]}
def add(p, q, c=1):
    r = dict(p)
    for m, v in q.items():
        r[m] = r.get(m, 0) + c * v
        if r[m] == 0: del r[m]
    return r
def mul(p, q): 
    r = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items(): r[m1 + m2] = r.get(m1 + m2, 0) + c1 * c2
    return {m: c for m, c in r.items() if c}
BR = {}
def br(w):
    if w in BR: return BR[w]
    if len(w) == 1: BR[w] = {w: 1}; return BR[w]
    j = next(i for i in range(1, len(w)) if w[i:] in ALL)      # longest proper Lyndon suffix
    u, v = br(w[:j]), br(w[j:])
    BR[w] = add(mul(u, v), mul(v, u), -1); return BR[w]
SUB = {0: {(1,): 1}, 1: {(0,): 1, (1,): -1}}                    # X -> Y, Y -> X - Y
def subst(p):
    r = {}
    for m, c in p.items():
        t = {(): c}
        for l in m: t = mul(t, SUB[l])
        r = add(r, t)
    return r
def coords(p, n):
    c = {}; p = dict(p)
    while p:
        m = min(p); assert m in ALL, "not a Lie polynomial"
        c[m] = p[m]; p = add(p, br(m), -c[m])
    return [c.get(w, 0) for w in LYN[n]]
def snf_diag(M):
    M = [r[:] for r in M]; n = len(M); d = []
    for t in range(n):
        while True:
            piv = min(((abs(M[i][j]), i, j) for i in range(t, n) for j in range(t, n) if M[i][j]), default=None)
            if piv is None: return d + [0] * (n - t)
            _, i, j = piv; M[t], M[i] = M[i], M[t]
            for r in M: r[t], r[j] = r[j], r[t]
            done = True
            for i in range(t + 1, n):
                q = M[i][t] // M[t][t]
                if q: M[i] = [a - q * b for a, b in zip(M[i], M[t])]
                if M[i][t]: done = False
            for j in range(t + 1, n):
                q = M[t][j] // M[t][t]
                if q:
                    for r in M: r[j] -= q * r[t]
                if M[t][j]: done = False
            if done:
                bad = next(((i, j) for i in range(t + 1, n) for j in range(t + 1, n) if M[i][j] % M[t][t]), None)
                if bad is None: break
                M[t] = [a + b for a, b in zip(M[t], M[bad[0]])]
        d.append(abs(M[t][t]))
    return d
for n in range(1, K + 1):
    cols = [coords(subst(br(w)), n) for w in LYN[n]]            # images of basis vectors
    dim = len(LYN[n])
    M = [[(1 if i == j else 0) - cols[j][i] for j in range(dim)] for i in range(dim)]
    d = snf_diag(M)
    desc = " + ".join((["Z^%d" % d.count(0)] if d.count(0) else []) + ["Z/%d" % e for e in sorted(d) if e > 1]) or "0"
    print("k=%d  dim L_k = %2d  coker(1 - phi_k) = %s" % (n, dim, desc))
