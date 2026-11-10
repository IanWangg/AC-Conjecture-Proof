#!/usr/bin/env python3
"""TH11 (experiment): graph of c-frozen killer classes of AK(3)'s AC class under "c-moving links".
Vertex: a class of killers w of G_c = <x,y|c>, recorded by the exact invariants (kappa, J-hat, N).
Link: from a representative (c, w), one cyclic product c -> c' = cyc(rot(c^+-1) rot(w^+-1)) such that
c' is an automorphic image psi(c) of c; then (c, psi^-1(w)) is again a state with first relator c, and it
is AC-equivalent to (c, w) whenever Aut(F2) is AC-realized on the class (AK(3): research-d Lemma D6).
For every class met we test the exact necessary condition for a one-move primitive exit:
(kappa, J-hat, N)(w) = (kappa, J-hat, N)(x^s y) for some s.     Bounded exploration, NOT exhaustive.
Usage: python3 experiments/th11_classgraph.py --selftest [maxclasses]
"""
import sys, time
from collections import deque
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import th11_kc as K, th11_nil as NIL, th11_trace as TR, o_gc
from th11_stab import inv, cyc
C = "xyxYYXy"
def rots(w): return [w[i:] + w[:i] for i in range(len(w))]
def links(w):
    out = {}
    for U in rots(C) + rots(inv(C)):
        for V in rots(w) + rots(inv(w)):
            c2 = cyc(U + V)
            if not c2: continue
            w2 = K.pull_back(c2, w)
            if w2 is None: continue
            w2 = cyc(w2); key = K.classify(w2)
            if key not in out or len(w2) < len(out[key]): out[key] = w2
    return out
def reps(w, extra=2, cap=24):
    """short words in the c-frozen class of w (twisted-conjugacy BFS in normal forms)."""
    u, k = o_gc.nf(w)
    if k == -1: u, k = o_gc.nf(inv(w))
    seen = {u}; dq = deque([u]); L = len(u) + extra
    while dq and len(seen) < 4 * cap:
        v = dq.popleft()
        for t in [o_gc.twisted_conj(g, v) for g in "aAbB"] + [o_gc.phi_pow(1, v), o_gc.phi_pow(-1, v)]:
            if len(t) <= L and t not in seen: seen.add(t); dq.append(t)
    ws = sorted({cyc(o_gc.to_word((v, 1))) for v in seen}, key=len)[:cap]
    return ws
def explore(start="xxxYXyy", maxclasses=60, tmax=150):
    t0 = time.time()
    prim = {}
    for s in range(-60, 61):
        prim.setdefault((NIL.kappa_tri(s), NIL.Jhat_x(s)), []).append(s)
    Nx = {s: TR.as_int(TR.N(NIL.power("a", s))) for s in range(-14, 16)}
    cls = {K.classify(start): (start, 0, None)}; dq = deque([K.classify(start)]); edges = set(); exits = []
    while dq and len(cls) < maxclasses and time.time() - t0 < tmax:
        key = dq.popleft(); w, d, _ = cls[key]
        for r in reps(w):
            for k2, w2 in links(r).items():
                edges.add((key, k2))
                if k2 not in cls:
                    cls[k2] = (w2, d + 1, key); dq.append(k2)
                    cand = [s for s in prim.get(k2[:2], []) if Nx.get(s) == k2[2]]
                    if cand: exits.append((k2, w2, cand))
    return cls, edges, exits

if __name__ == "__main__":
    mc = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    assert set(links("XyxYxxy")) >= {(0, 1, 20), (1, 1, 20)}          # Q-mirror class is linked to P_3 and its mirror
    cls, edges, exits = explore(maxclasses=mc)
    for key, (w, d, par) in sorted(cls.items(), key=lambda kv: (kv[1][1], kv[0])):
        print("depth", d, "class (kappa,J-hat,N) =", key, "rep", w, "from", par)
    print("classes:", len(cls), " links:", len(edges), " primitive-exit candidates:", exits)
    print("th11_classgraph self-test passed")
