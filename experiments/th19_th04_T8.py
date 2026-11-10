"""TH19 bounded brute-force check of TH04 Theorem 6.4 (T8): torus-type cyclic words W = cyc(u^a v^c), (u,v) a basis of F2,
|a|,|c| >= 2, that are conjugate to b^+-1 (b = xyxYXY) in G_n = <x,y | x^n = y^(n+1)>.  TH04: only W = b^+-1 (n >= 3).
Bases: BFS ball of Aut(F2) (Nielsen generators), total length <= LCAP; exponents 2 <= |a|,|c| <= E."""
import sys
sys.path.insert(0, "experiments")
from th19_lib import *
LCAP, E, DEPTH = 16, 5, 8
gens = [{"x": "xy", "y": "y"}, {"x": "xY", "y": "y"}, {"x": "x", "y": "yx"}, {"x": "x", "y": "yX"}, {"x": "y", "y": "x"}, {"x": "X", "y": "y"}]
ball = {("x", "y")}; fr = [("x", "y")]
for depth in range(DEPTH):
    nx = []
    for (a, b_) in fr:
        for g in gens:
            img = (subst(g["x"], {"x": a, "y": b_}), subst(g["y"], {"x": a, "y": b_}))
            if img not in ball and len(img[0]) + len(img[1]) <= LCAP: ball.add(img); nx.append(img)
    fr = nx
b = "xyxYXY"; exps = [e for e in range(-E, E+1) if abs(e) >= 2]
words = set()
for (u, v) in ball:
    for a in exps:
        ua = u*a if a > 0 else inv(u)*(-a)
        for c in exps:
            words.add(cyc(ua + (v*c if c > 0 else inv(v)*(-c))))
print(f"{len(ball)} bases, {len(words)} distinct torus-type cyclic representatives (as words)")
for n in (2, 3, 4, 5, 6):
    key = lambda w: ((n+1)*expo(w)[0] + n*expo(w)[1], neck_pq(w, n, n+1))
    tgt = {key(b), key(inv(b))}
    hits = {canon(w) for w in words if abs((n+1)*expo(w)[0] + n*expo(w)[1]) == 1 and key(w) in tgt}
    print(f"n={n}: torus-type words conjugate to b^+-1 in G_n: {len(hits)} cyclic classes up to inversion;"
          f" all equal to b: {hits == {canon(b)}}", sorted(hits, key=len)[:4] if hits != {canon(b)} else "")
