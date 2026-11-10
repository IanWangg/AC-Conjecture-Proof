"""TH19 bounded brute-force check of TH04 Theorem 6.6 (T10): torus-type cyclic words W = cyc(u^a v^c) conjugate, in
T = <x,y | x^2 = y^(2n+1)>, to P^+-1 for P = N_n = (x Y^n)^2 (x Y^(n+1))^3 (node 2) and for the node-3 class
(t-exponent necklace n+1,n,n,n+1,n,n,n+1).  TH04: only P^+-1 and iota'(P)^+-1, iota' = (x -> y^(2n+1) X).
Bases: BFS ball of Aut(F2), total length <= LCAP; exponents 2 <= |a|,|c| <= E."""
import sys
sys.path.insert(0, "experiments")
from th19_lib import *
LCAP, E, DEPTH = int(sys.argv[1]) if len(sys.argv) > 1 else 15, 4, 9
gens = [{"x": "xy", "y": "y"}, {"x": "xY", "y": "y"}, {"x": "x", "y": "yx"}, {"x": "x", "y": "yX"}, {"x": "y", "y": "x"}, {"x": "X", "y": "y"}]
ball = {("x", "y")}; fr = [("x", "y")]
for depth in range(DEPTH):
    nx = []
    for (a, b_) in fr:
        for g in gens:
            img = (subst(g["x"], {"x": a, "y": b_}), subst(g["y"], {"x": a, "y": b_}))
            if img not in ball and len(img[0]) + len(img[1]) <= LCAP: ball.add(img); nx.append(img)
    fr = nx
exps = [e for e in range(-E, E+1) if abs(e) >= 2]
words = set()
for (u, v) in ball:
    for a in exps:
        ua = u*a if a > 0 else inv(u)*(-a)
        for c in exps:
            words.add(cyc(ua + (v*c if c > 0 else inv(v)*(-c))))
print(f"{len(ball)} bases, {len(words)} torus-type words")
for n in (2, 3, 4):
    q = 2*n + 1
    key = lambda w: (q*expo(w)[0] + 2*expo(w)[1], neck_pq(w, 2, q))
    io = {"x": "y"*q + "X", "y": "y"}
    N = ("x" + "Y"*n)*2 + ("x" + "Y"*(n+1))*3
    P3 = "x" + "Y"*n + ("x" + "Y"*(n+1))*2 + "x" + "Y"*n + ("x" + "Y"*(n+1))*2 + "x" + "Y"*n
    for name, P in (("node 2 (N_n)", N), ("node 3 class", P3)):
        tgt = {key(P), key(inv(P))}
        hits = {canon(w) for w in words if abs(q*expo(w)[0] + 2*expo(w)[1]) == 1 and key(w) in tgt}
        extra = ""
        if name.startswith("node 2"):
            extra = f"; equal to {{N_n, iota'(N_n)}}: {hits == {canon(N), canon(subst(N, io))}}"
        else:
            extra = f"; closed under iota': {all(canon(subst(h, io)) in hits for h in hits)}; lengths {sorted(len(h) for h in hits)}"
        print(f"n={n}, {name}: {len(hits)} torus-type cyclic classes up to inversion{extra}")
