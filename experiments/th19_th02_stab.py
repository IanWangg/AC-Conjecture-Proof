"""TH19 check of TH02 Prop. 7 via Whitehead level sets (own code): stabilizer in Out(F2) = GL2(Z) of the cyclic word
x^p y^q up to inversion.  By Whitehead's peak-reduction theorem two minimal cyclic words in one Aut-orbit are joined by
Whitehead automorphisms through minimal words; in rank 2 these are, modulo inner automorphisms, the signed permutations and
x -> x y^+-1, y -> y x^+-1.  BFS over (cyclic word, matrix) pairs inside the level set."""
import sys
sys.path.insert(0, "experiments")
from th19_lib import *
G = [({"x": "xy", "y": "y"}, ((1, 0), (1, 1))), ({"x": "xY", "y": "y"}, ((1, 0), (-1, 1))),
     ({"x": "x", "y": "yx"}, ((1, 1), (0, 1))), ({"x": "x", "y": "yX"}, ((1, -1), (0, 1))),
     ({"x": "y", "y": "x"}, ((0, 1), (1, 0))), ({"x": "X", "y": "y"}, ((-1, 0), (0, 1))), ({"x": "x", "y": "Y"}, ((1, 0), (0, -1)))]
mm = lambda A, B: tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
rc = lambda w: min(rots(cyc(w)))
def stab(p, q):
    r = "x"*p + ("y"*q if q > 0 else "Y"*(-q)); L = len(r)
    # minimality: no generator shortens r
    assert all(len(cyc(subst(r, g))) >= L for g, _ in G)
    start = (rc(r), ((1, 0), (0, 1))); seen = {start}; fr = [start]; level = {rc(r)}
    while fr:
        nx = []
        for (w, M) in fr:
            for g, Mg in G:
                w2 = cyc(subst(w, g))
                if len(w2) != L: continue
                st = (rc(w2), mm(Mg, M)); level.add(st[0])
                if st not in seen:
                    assert len(seen) < 200000, "stabilizer looks infinite"
                    seen.add(st); nx.append(st)
        fr = nx
    targets = {rc(r), rc(inv(r))}
    return sorted(M for (w, M) in seen if w in targets), len(level)
for (p, q) in [(3, 4), (3, 5), (4, 5), (3, 7), (5, 7), (5, 8), (2, 3), (2, 5), (2, 7), (2, 9), (2, -5)]:
    S, lv = stab(p, q)
    print(f"x^{p} y^{q}: level set {lv} cyclic words; stabilizer up to inversion has {len(S)} elements:", S)
