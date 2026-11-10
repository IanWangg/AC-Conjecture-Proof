"""TH19: identify the trefoil-killer necklace (TH09 §7) of the presentations in TH09's certificates and of AK(3), C3.
For a pair (partner, r) with r of trefoil type, find theta in a BFS ball of Aut(F2) with theta(r) a rotation of (xxYYY)^+-1,
and print the t-exponent necklace of theta(partner) in C2*C3 (x->s, y->t), up to rotation/reversal/complement."""
import sys
sys.path.insert(0, "experiments")
from th19_lib import *
gens = [{"x": "xy", "y": "y"}, {"x": "xY", "y": "y"}, {"x": "x", "y": "yx"}, {"x": "x", "y": "yX"}, {"x": "y", "y": "x"}, {"x": "X", "y": "y"}]
ball = {("x", "y")}; fr = [("x", "y")]
for depth in range(7):
    nx = []
    for (a, b) in fr:
        for g in gens:
            img = (subst(g["x"], {"x": a, "y": b}), subst(g["y"], {"x": a, "y": b}))
            if img not in ball and len(img[0]) + len(img[1]) <= 24: ball.add(img); nx.append(img)
    fr = nx
def necklace(partner, r):
    for (a, b) in sorted(ball, key=lambda t: len(t[0]) + len(t[1])):
        th = {"x": a, "y": b}
        if canon(subst(r, th)) == canon("xxYYY"):
            nk = neck_pq(subst(partner, th), 2, 3)
            e = tuple(x[1] for x in nk if x[0] == "t")
            if len(e) * 2 != len(nk): return ("not alternating", nk)
            k = len(e); orbit = set()
            for M in (e, e[::-1]):
                for C in (M, tuple(3 - v for v in M)):
                    for i in range(k): orbit.add(C[i:] + C[:i])
            return "".join(map(str, min(orbit)))
    return None
for name, partner, r in [("AK(3)", "xxxYYYY", "xyxYXY"), ("AK(2)", "xxYYY", "xyxYXY"), ("C3", "xyyyyyxYY", "xxyXy"),
                         ("TH09 x7 certificate start", "XXXYXXYxxy", "XYYXy"), ("TH09 k9 certificate start", "XyXyXYXyXYxyxyxYxY", "xxYYY"),
                         ("AK(4)", "xxxxYYYYY", "xyxYXY")]:
    print(f"{name}: partner {partner}, trefoil-type relator {r}: necklace {necklace(partner, r)}")
