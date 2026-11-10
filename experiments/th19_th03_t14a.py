"""TH19: positive part of TH03 Prop. T14(a) by an own twisted-conjugacy BFS in G_c = F(a,b) x|_phi Z:
which cyclic words w (y-exponent 1, length <= 9) with I(w) = 20 and J(w) = J(k_3) have normal form (u,1) with u in the
Reidemeister class R(a^3 B A) = {v u0 phi(v)^-1}, explored with |u| <= CAP.  Hits are exact (explicit conjugator chain);
misses are bounded."""
import sys
sys.path.insert(0, "experiments")
from th19_lib import cyc_words, expo
import th19_th03_t14 as T      # reuses nf, Iinv, J (prints its own two lines first)
CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 15
u0 = T.nf("xxxYXyy")[0]
seen = {u0}; fr = [u0]
while fr:
    nx = []
    for u in fr:
        cands = [T.fred(g + u + T.phik(g, 1).swapcase()[::-1]) for g in "aAbB"] + [T.phik(u, 1), T.phik(u, -1)]
        for v in cands:
            if len(v) <= CAP and v not in seen: seen.add(v); nx.append(v)
    fr = nx
print(f"BFS in R(a^3BA) with cap {CAP}: {len(seen)} elements")
Jk = T.J(u0); hits, miss, done = [], [], set()
for L in range(1, 10):
    for w in cyc_words(L):
        if expo(w)[1] != 1: continue
        r = min(w[i:] + w[:i] for i in range(L))
        if r in done: continue
        done.add(r)
        u, k = T.nf(w)
        if T.Iinv(u) == 20 and T.J(u) == Jk:
            (hits if u in seen else miss).append(r)
print("conjugate to k_3 (explicit BFS chain):", len(hits), sorted(hits, key=lambda s: (len(s), s)))
print("not reached within the cap:", len(miss), "by length", {L: sum(1 for m in miss if len(m) == L) for L in (7, 8, 9)})
