"""TH19 check of the Z/9 case of TH03 Prop. T15: k' = XyyxYxYxy (rank 5).  Own computation: F_3-valued twisted traces of
degree <= 3, Hensel lift of each to a Z/9-valued twisted trace (solve the inhomogeneous F_3-system), then test all
residues j mod 27 for l(M(t_1^j)) = l(M(c)) mod 9.  ((1+N)^27 = 1 mod (9, N^4), so j matters only mod 27.)"""
import sys, io, contextlib
sys.path.insert(0, "experiments")
with contextlib.redirect_stdout(io.StringIO()):
    import th19_th03_tt as TT
    import th19_th03_t15 as T15
kp, D = "XyyxYxYxy", 3
r, psi, uc, P1 = T15.analyse(kp)
al = TT.Alg(r, D); n = len(al.mons)
PsiX = {}
for i in range(r):
    A = al.M(psi[i]); A[()] = A.get((), 0) - 1; PsiX[i] = {mn: v for mn, v in A.items() if v}
rows = TT.tt_rows(al, PsiX)
ns3 = TT.nullspace(rows, n, mod=3)
print(f"rank {r}, {len(rows)} relations, F_3-valued twisted traces of degree <= {D}: dimension {len(ns3)}")
# F_3 test first
cM = al.M(uc); N = al.M(P1); N[()] = N.get((), 0) - 1; N = {mn: v for mn, v in N.items() if v}
def Mpow(j):
    R = {(): 1}; B = dict(N); B[()] = B.get((), 0) + 1; e = j
    while e:
        if e & 1: R = al.mul(R, B)
        B = al.mul(B, B); e >>= 1
    return R
ok3 = [j for j in range(9) if all((TT.ev(al, l, Mpow(j)) - TT.ev(al, l, cM)) % 3 == 0 for l in ns3)]
print("F_3: residues j mod 9 allowed:", ok3)
# Hensel lift: l = l0 + 3 l1 with rows.l = 0 mod 9
lifts = []
for l0 in ns3:
    l0 = {k: v % 3 for k, v in l0.items()}
    e = []
    for row in rows:
        s = sum(v * l0.get(k, 0) for k, v in row.items())
        assert s % 3 == 0
        e.append((s // 3) % 3)
    aug = []
    for i, row in enumerate(rows):                                      # unknowns l1 (n of them) and a last variable = 1
        rr = dict(row); rr[n] = e[i]; aug.append(rr)
    sol = [v for v in TT.nullspace(aug, n + 1, mod=3) if v.get(n, 0) % 3 != 0]
    if not sol: print("   a trace does not lift"); continue
    v = sol[0]; c = pow(v[n], -1, 3)
    l1 = {k: (val * c) % 3 for k, val in v.items() if k != n}
    l = {k: (l0.get(k, 0) + 3 * l1.get(k, 0)) % 9 for k in set(l0) | set(l1)}
    assert all(sum(val * l.get(k, 0) for k, val in row.items()) % 9 == 0 for row in rows)
    lifts.append(l)
print(f"Z/9-valued lifts found: {len(lifts)} (all {len(rows)} relations hold mod 9)")
ok9 = [j for j in range(27) if all((TT.ev(al, l, Mpow(j)) - TT.ev(al, l, cM)) % 9 == 0 for l in lifts)]
print("Z/9: residues j mod 27 allowed:", ok9)
