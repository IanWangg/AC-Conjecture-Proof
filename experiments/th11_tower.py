#!/usr/bin/env python3
"""TH11: where can nilpotent (Reidemeister) invariants of phi-twisted conjugacy live?
phi acts on L_k = gamma_k F / gamma_{k+1} F (degree-k part of the free Lie ring on X,Y) through its
abelianization  X -> Y, Y -> X - Y.  We compute the matrix Phi_k in the Lyndon basis and the Smith
normal form of I - Phi_k, i.e. the group coker(1 - phi_k), for k = 1..KMAX.
For k <= 4 the fibres of  R(phi; F/gamma_{k+1}) -> R(phi; F/gamma_k)  are exactly these cokernels
(research-th11, Section 5); for k >= 5 they are quotients of them.
Usage: python3 experiments/th11_tower.py --selftest [KMAX]
"""
import sys
from itertools import product

def padd(p, q, c=1):
    r = dict(p)
    for m, v in q.items():
        r[m] = r.get(m, 0) + c * v
        if r[m] == 0: del r[m]
    return r
def pmul(p, q):
    r = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            m = m1 + m2; r[m] = r.get(m, 0) + c1 * c2
    return {m: c for m, c in r.items() if c}
def bracket(p, q): return padd(pmul(p, q), pmul(q, p), -1)

def is_lyndon(w): return all(w < w[i:] for i in range(1, len(w)))
_P = {}
def lyndon_poly(w):
    """standard bracketing of the Lyndon word w; leading (lex-smallest) monomial is w."""
    if w in _P: return _P[w]
    if len(w) == 1: r = {w: 1}
    else:
        i = next(i for i in range(1, len(w)) if is_lyndon(w[i:]))     # longest proper Lyndon suffix
        r = bracket(lyndon_poly(w[:i]), lyndon_poly(w[i:]))
    _P[w] = r
    return r
def basis(k): return [w for w in product((0, 1), repeat=k) if is_lyndon(w)]
def coords(f, B):
    f = dict(f); c = {w: 0 for w in B}
    while f:
        m = min(f); assert m in c, "not a Lie polynomial"
        c[m] += f[m]; f = padd(f, lyndon_poly(m), -f[m])
    return [c[w] for w in B]
SUB = {0: {(1,): 1}, 1: {(0,): 1, (1,): -1}}                # X -> Y,  Y -> X - Y
def subst(f):
    r = {}
    for m, c in f.items():
        t = {(): c}
        for i in m: t = pmul(t, SUB[i])
        r = padd(r, t)
    return r
def phi_matrix(k):
    B = basis(k)
    cols = [coords(subst(lyndon_poly(w)), B) for w in B]
    return [[cols[j][i] for j in range(len(B))] for i in range(len(B))]
def smith_diag(M):
    """diagonal of the Smith normal form of an integer matrix (elementary divisors, then zeros)."""
    M = [r[:] for r in M]; n = len(M); m = len(M[0]) if n else 0; d = []; t = 0
    while t < min(n, m):
        piv = [(abs(M[i][j]), i, j) for i in range(t, n) for j in range(t, m) if M[i][j]]
        if not piv: break
        _, i, j = min(piv)
        M[t], M[i] = M[i], M[t]
        for r in M: r[t], r[j] = r[j], r[t]
        done = False
        while not done:
            done = True
            for i in range(t + 1, n):
                q = M[i][t] // M[t][t]
                if q: M[i] = [a - q * b for a, b in zip(M[i], M[t])]
                if M[i][t]: M[t], M[i] = M[i], M[t]; done = False
            for j in range(t + 1, m):
                q = M[t][j] // M[t][t]
                if q:
                    for r in M: r[j] -= q * r[t]
                if M[t][j]:
                    for r in M: r[t], r[j] = r[j], r[t]
                    done = False
            if done:
                bad = [(i, j) for i in range(t + 1, n) for j in range(t + 1, m) if M[i][j] % M[t][t]]
                if bad:
                    i = bad[0][0]; M[t] = [a + b for a, b in zip(M[t], M[i])]; done = False
        d.append(abs(M[t][t])); t += 1
    return d + [0] * (min(n, m) - len(d))

def tower(kmax):
    out = {}
    for k in range(1, kmax + 1):
        P = phi_matrix(k); n = len(P)
        D = smith_diag([[(1 if i == j else 0) - P[i][j] for j in range(n)] for i in range(n)])
        out[k] = (n, [x for x in D if x != 1])
    return out

if __name__ == "__main__":
    kmax = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    assert [len(basis(k)) for k in range(1, 9)] == [2, 1, 2, 3, 6, 9, 18, 30]      # Witt's formula
    assert phi_matrix(1) == [[0, 1], [1, -1]] and phi_matrix(2) == [[-1]]
    assert smith_diag([[2, 4], [6, 8]]) == [2, 4] and smith_diag([[1, 0, 1], [0, 2, -2], [1, -1, 2]]) == [1, 1, 0]
    res = tower(kmax)
    assert res[1][1] == [] and res[2][1] == [2] and res[3][1] == [] and res[4][1] == [0]
    for k, (n, D) in res.items():
        print(f"k={k}: rank L_k = {n:2d}; coker(1 - phi_k) = " + (" + ".join("Z" if x == 0 else f"Z/{x}" for x in D) or "0"))
    print("th11_tower self-test passed")
