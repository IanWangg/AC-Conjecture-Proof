"""TH19 check of TH03 Prop. T18(a): cyclically reduced words c' of length <= 8 that can be conjugate to c^+-1 in
G_{k_3} = F(t0,t1,t2) x|_psi <x>: all rational twisted traces of degree <= 3 (3-dimensional space, recomputed here) must
agree with those of c.  TH03: exactly the rotations/inverses of XXyxYY, c = xyxYYXy and XXXYxyxY survive; and
Y c y = yxYYXX, c = xyxYXXXY hold in G_{k_3} (normal forms).  Imports my own th19_th03_q2 (normal form) and th19_th03_tt
(solver); both print their own check lines first."""
import sys, io, contextlib
sys.path.insert(0, "experiments")
from th19_lib import cyc_words, expo, inv, canon
with contextlib.redirect_stdout(io.StringIO()):
    import th19_th03_q2 as Q2
    import th19_th03_tt as TT
al, rows = TT.setup(3, 3); ns = TT.nullspace(rows, len(al.mons))
assert len(ns) == 3
def invariants(w):
    u, k = Q2.nf(w)
    if k == -1: u, k = Q2.nf(inv(w))
    if k != 1: return None
    A = al.M(u)
    return tuple(TT.ev(al, l, A) for l in ns)
c = "xyxYYXy"; target = invariants(c)
assert Q2.nf("YxyxYYXyy") == Q2.nf("yxYYXX"), "Y c y = yxYYXX in G_{k_3}"
assert Q2.nf(c) == Q2.nf("xyxYXXXY"), "c = xyxYXXXY in G_{k_3}"
print("normal-form identities Y c y = yxYYXX and c = xyxYXXXY hold in G_{k_3}; invariants of c:", target)
surv = {}
for L in range(1, 9):
    for w in cyc_words(L):
        e = expo(w)
        if abs(e[0] - 2*e[1]) != 1: continue          # degree lambda(x) = 1, lambda(y) = -2
        if invariants(w) == target or invariants(inv(w)) == target: surv.setdefault(canon(w), L)
print("cyclic words (up to rotation/inversion) of length <= 8 with the twisted-trace invariants of c:", sorted(surv.items(), key=lambda t: t[1]))
