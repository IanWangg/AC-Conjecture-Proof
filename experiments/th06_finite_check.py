#!/usr/bin/env python3
"""TH06: exhaustive checks of the generalized-instruction distance d* in small finite groups.

For a finite group Q = <a,b> the moves are the 7 Nielsen instructions and
"replace u_i by any conjugate" (one move).  For every pair (a e0, b e1), e_i in Q',
the exact distance to (a,b) is computed by BFS, and the two-conjugation lemma
(Lemma 1.1/1.2 of research-th06.md) is tested directly:  {(a^g b)^g' b^-1} = a Q' ?

  python3 experiments/th06_finite_check.py            (all groups below, < 1 minute)
  python3 experiments/th06_finite_check.py --selftest (the small ones + assertions)
"""
import sys
from collections import deque

def perm(cycles, n):
    p = list(range(n))
    for cyc in cycles:
        for i, v in enumerate(cyc):
            p[v] = cyc[(i + 1) % len(cyc)]
    return tuple(p)

def pmul(p, q):                      # first p then q
    return tuple(q[i] for i in p)

def mmul(p):                         # 2x2 matrices mod p
    return lambda A, B: ((A[0]*B[0]+A[1]*B[2]) % p, (A[0]*B[1]+A[1]*B[3]) % p,
                         (A[2]*B[0]+A[3]*B[2]) % p, (A[2]*B[1]+A[3]*B[3]) % p)

def amul(A, B):                      # affine maps v -> vM + t over F_3, stored as (M, t)
    M = mmul(3)(A[0], B[0])
    t = ((A[1][0]*B[0][0] + A[1][1]*B[0][2] + B[1][0]) % 3, (A[1][0]*B[0][1] + A[1][1]*B[0][3] + B[1][1]) % 3)
    return (M, t)

GROUPS = {   # name: (a, b, multiplication, identity)
    # C3^2:Q8 (order 72): abelian-by-nilpotent, derived length 3, neither nilpotent nor metabelian
    "C3^2:Q8": (((0, 2, 1, 0), (1, 0)), ((1, 1, 1, 2), (0, 0)), amul, ((1, 0, 0, 1), (0, 0))),
    "S3":      (perm([(0, 1)], 3), perm([(0, 1, 2)], 3), pmul, tuple(range(3))),
    "A4":      (perm([(0, 1, 2)], 4), perm([(0, 1), (2, 3)], 4), pmul, tuple(range(4))),
    "F20":     (perm([(1, 2, 4, 3)], 5), perm([(0, 1, 2, 3, 4)], 5), pmul, tuple(range(5))),
    "D8xC3~":  (perm([(0, 1, 2, 3), (4, 5, 6)], 7), perm([(0, 2), (4, 5, 6)], 7), pmul, tuple(range(7))),
    "S4":      (perm([(0, 1)], 4), perm([(0, 1, 2, 3)], 4), pmul, tuple(range(4))),
    "SL(2,3)": ((1, 1, 0, 1), (0, 2, 1, 0), mmul(3), (1, 0, 0, 1)),
    "SL(2,3)b": ((1, 1, 0, 1), (0, 1, 2, 1), mmul(3), (1, 0, 0, 1)),
    "GL(2,3)": ((1, 1, 0, 1), (0, 1, 1, 0), mmul(3), (1, 0, 0, 1)),
    "A5":      (perm([(0, 1, 2)], 5), perm([(0, 1, 2, 3, 4)], 5), pmul, tuple(range(5))),
    "S5":      (perm([(0, 1)], 5), perm([(0, 1, 2, 3, 4)], 5), pmul, tuple(range(5))),
    "SL(2,5)": ((1, 1, 0, 1), (0, 4, 1, 0), mmul(5), (1, 0, 0, 1)),
}

def analyse(name):
    a, b, mul, one = GROUPS[name]
    elems, dq = {one: 0}, deque([one])
    while dq:
        g = dq.popleft()
        for s in (a, b):
            h = mul(g, s)
            if h not in elems:
                elems[h] = len(elems)
                dq.append(h)
                assert len(elems) <= 240, "group too large for this script"
    E = list(elems)
    n = len(E)
    M = [[elems[mul(g, h)] for h in E] for g in E]
    inv = [row.index(0) for row in M]
    conj = lambda u, g: M[M[inv[g]][u]][g]
    def closure(gens):
        S, dq = {0}, deque([0])
        while dq:
            g = dq.popleft()
            for s in gens:
                h = M[g][s]
                if h not in S:
                    S.add(h)
                    dq.append(h)
        return S
    comm = lambda S, T: closure({M[M[inv[g]][inv[h]]][M[g][h]] for g in S for h in T})
    G = set(range(n))
    D1 = comm(G, G)
    D2 = comm(D1, D1)
    D3 = comm(D2, D2)
    D4 = comm(D3, D3)
    dl = 1 if len(D1) == 1 else 2 if len(D2) == 1 else 3 if len(D3) == 1 else 4 if len(D4) == 1 else None
    lower, nilp = G, False
    for _ in range(12):
        lower = comm(lower, G)
        if len(lower) == 1:
            nilp = True
            break
    ia, ib = elems[a], elems[b]
    cls = [sorted({conj(u, g) for g in range(n)}) for u in range(n)]
    start = (ia, ib)
    dist, dq = {start: 0}, deque([start])
    while dq:
        u, v = st = dq.popleft()
        d = dist[st] + 1
        nb = [(inv[u], v), (u, inv[v]), (v, u), (M[u][v], v), (M[u][inv[v]], v),
              (u, M[v][u]), (u, M[v][inv[u]])]
        nb += [(w, v) for w in cls[u]] + [(u, w) for w in cls[v]]
        for t in nb:
            if t not in dist:
                dist[t] = d
                dq.append(t)
    T = [(M[ia][e0], M[ib][e1]) for e0 in D1 for e1 in D1]
    if dl is not None:               # soluble: every such pair normally generates Q
        assert all(t in dist for t in T), "some pair with standard abelianization unreachable"
    T = [t for t in T if t in dist]  # (not soluble: the AC class of (a,b) inside the coset)
    dmax = max(dist[t] for t in T)
    got = {M[conj(M[conj(ia, g)][ib], h)][inv[ib]] for g in range(n) for h in range(n)}
    lemma = got == {M[ia][e] for e in D1}
    centre2 = all(M[z][g] == M[g][z] for z in D2 for g in range(n))
    kind = ("nilpotent" if nilp else "metabelian" if dl == 2 else
            "Q'' central" if (dl and centre2) else
            f"soluble, derived length {dl}" if dl else "not soluble")
    # --- identities used in Lemmas 1.3 and 1.4 of research-th06.md
    cm = lambda g, h: M[M[inv[g]][inv[h]]][M[g][h]]
    for u0 in range(0, n, 5):
        for v in range(0, n, 3):
            for mu in range(0, n, 2):                # the 8 instructions of Lemma 1.4(ii)
                x0, x1 = M[u0][inv[v]], conj(v, ia)
                x0 = M[x0][x1]; x1 = conj(x1, mu)
                x0 = M[x0][inv[x1]]; x1 = conj(x1, M[M[inv[mu]][inv[ia]]][mu])
                x0 = M[x0][x1]; x1 = conj(x1, inv[mu])
                assert (x0, x1) == (M[u0][cm(cm(ia, v), mu)], v)
    if dl and centre2:                               # Lemma 1.4(i): Q'' = {[c, mu]}
        assert {cm(cm(ia, ib), mu) for mu in D1} == D2
    K = [D for D in (D1, D2, D3) if len(D) > 1 and len(comm(D, D)) == 1]
    if K:                                            # Lemma 1.3: [a,K][ba,K] = [K,Q]
        K, ba = K[0], M[ib][ia]
        assert {M[cm(ia, m)][cm(ba, m2)] for m in K for m2 in K} == comm(K, G)
    return {"group": name, "order": n, "kind": kind, "|Q'|": len(D1), "pairs": len(T),
            "max d* over pairs (a e0, b e1)": dmax, "two-conjugation lemma for (a,b)": lemma}

def lemma_all_pairs(name, sample=None, seed=1):
    """Lemma 1.1/1.2 for every (or `sample` random) generating pair (p,q) of the group."""
    import random
    a, b, mul, one = GROUPS[name]
    elems, dq = [one], deque([one])
    seen = {one}
    while dq:
        g = dq.popleft()
        for s in (a, b):
            h = mul(g, s)
            if h not in seen:
                seen.add(h); elems.append(h); dq.append(h)
    idx = {g: i for i, g in enumerate(elems)}
    n = len(elems)
    M = [[idx[mul(g, h)] for h in elems] for g in elems]
    inv = [row.index(0) for row in M]
    conj = lambda u, g: M[M[inv[g]][u]][g]
    def gen(S):
        T, dq = {0}, deque([0])
        while dq:
            g = dq.popleft()
            for s in S:
                h = M[g][s]
                if h not in T:
                    T.add(h); dq.append(h)
        return T
    D1 = gen({M[M[inv[g]][inv[h]]][M[g][h]] for g in range(n) for h in range(n)})
    pairs = [(p, q) for p in range(n) for q in range(n) if len(gen({p, q})) == n]
    if sample:
        pairs = random.Random(seed).sample(pairs, sample)
    for p, q in pairs:
        cls = {conj(p, g) for g in range(n)}
        got = {M[conj(M[pg][q], h)][inv[q]] for pg in cls for h in range(n)}
        assert got == {M[p][e] for e in D1}, (name, p, q)
    return len(pairs)

def congruence_check():
    """Lemma 1.5 in SL_2(Z/27): two layers K_1 > K_2 > 1; Psi(m,m') covers a*K_1 for u_1 = b*k_1."""
    mul = mmul(27)
    def inv(A):
        return (A[3] % 27, -A[1] % 27, -A[2] % 27, A[0] % 27)
    cj = lambda u, g: mul(mul(inv(g), u), g)
    K = [(1 + 3*i, 3*j, 3*k, d) for i in range(9) for j in range(9) for k in range(9)
         for d in range(1, 27, 3) if ((1 + 3*i) * d - 9*j*k) % 27 == 1]
    assert len(K) == 729
    a, b = (1, 1, 0, 1), (1, 0, 1, 1)
    target = {mul(a, k) for k in K}
    for k1 in (K[0], K[100], K[500]):
        u1 = mul(b, k1)
        u1i = inv(u1)
        cls = {cj(a, m) for m in K}
        got = {mul(cj(mul(am, u1), m2), u1i) for am in cls for m2 in K}
        assert got == target
    return len(K)

BOUND = {"nilpotent": 8, "metabelian": 8, "Q'' central": 24, "soluble, derived length 3": 32}

if __name__ == "__main__":
    names = ["S3", "A4", "F20", "D8xC3~", "C3^2:Q8", "S4", "SL(2,3)", "SL(2,3)b", "GL(2,3)"] if "--selftest" in sys.argv else list(GROUPS)
    for nm in names:
        r = analyse(nm)
        print(r)
        if r["kind"] in BOUND:
            assert r["max d* over pairs (a e0, b e1)"] <= BOUND[r["kind"]]
        if nm == "C3^2:Q8":                         # Lemma 1.2 beyond the metabelian case
            assert r["order"] == 72 and r["max d* over pairs (a e0, b e1)"] <= 8
            assert r["two-conjugation lemma for (a,b)"]
        if r["kind"] in ("nilpotent", "metabelian"):
            assert r["two-conjugation lemma for (a,b)"]
    for nm in ("S3", "A4", "F20", "D8xC3~"):
        print(f"two-conjugation lemma for all {lemma_all_pairs(nm)} generating pairs of {nm}: OK")
    print(f"two-conjugation lemma for {lemma_all_pairs('C3^2:Q8', sample=12)} random generating pairs of C3^2:Q8: OK")
    print(f"Lemma 1.5 in SL_2(Z/27), |K_1| = {congruence_check()}: four instructions with conjugators in K_1 cover a*K_1: OK")
    print("checks passed" if "--selftest" not in sys.argv else "selftest passed")
