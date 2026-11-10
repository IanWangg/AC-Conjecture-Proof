"""TH19 check of TH03 Prop. T12 for n = 7 (F_7-valued twisted traces, degree 3) and n = 8 (Z/9-valued, degree 3), and of the
positive control n = 2 (c ~ x (yx)^-3 in G_{k_2}).  G_{k_n} = F(t_0..t_{n-1}) x|_psi Z, psi: t_i -> t_{i+1}, t_{n-1} -> t_{n-1} t_0;
c = (t_1 t_2^-1 t_1^-1, 1) for n >= 3, candidates x t^j = (t_1^j, 1)."""
import sys, io, contextlib
sys.path.insert(0, "experiments")
with contextlib.redirect_stdout(io.StringIO()):
    import th19_th03_tt as TT
    import th19_th03_t15 as T15
def data(n, D):
    al, rows = TT.setup(n, D)
    cM = al.M([(1, 1), (2, -1), (1, -1)]); B = al.M([(1, 1)])
    P = [{(): 1}]
    for _ in range(27): P.append(al.mul(P[-1], B))
    return al, rows, cM, P
al, rows, cM, P = data(7, 3); ns = TT.nullspace(rows, len(al.mons), mod=7)
ok = [j for j in range(7) if all((TT.ev(al, l, P[j]) - TT.ev(al, l, cM)) % 7 == 0 for l in ns)]
print(f"n=7: {len(al.mons)} monomials, F_7-valued traces of degree <= 3: dimension {len(ns)}; residues j mod 7 allowed: {ok}")
al, rows, cM, P = data(8, 3); n = len(al.mons); ns3 = TT.nullspace(rows, n, mod=3)
ok3 = [j for j in range(9) if all((TT.ev(al, l, P[j]) - TT.ev(al, l, cM)) % 3 == 0 for l in ns3)]
lifts = []
for l0 in ns3:
    l0 = {k: v % 3 for k, v in l0.items()}; aug = []
    for row in rows:
        s = sum(v * l0.get(k, 0) for k, v in row.items()); assert s % 3 == 0
        rr = dict(row); rr[n] = (s // 3) % 3; aug.append(rr)
    sol = [v for v in TT.nullspace(aug, n + 1, mod=3) if v.get(n, 0) % 3 != 0]
    if not sol: continue
    v = sol[0]; cinv = pow(v[n], -1, 3)
    l = {k: (l0.get(k, 0) + 3 * ((v.get(k, 0) * cinv) % 3)) % 9 for k in set(l0) | set(v) if k != n}
    assert all(sum(val * l.get(k, 0) for k, val in row.items()) % 9 == 0 for row in rows)
    lifts.append(l)
ok9 = [j for j in range(27) if all((TT.ev(al, l, P[j]) - TT.ev(al, l, cM)) % 9 == 0 for l in lifts)]
print(f"n=8: {n} monomials, F_3-valued traces: dimension {len(ns3)}, residues j mod 9 allowed: {ok3}; Z/9 lifts: {len(lifts)}; residues j mod 27 allowed: {ok9}")
# control n = 2: normal forms in G_{k_2} via the general rewriting of th19_th03_t15 (k_2 = xxYXyy), c vs x (yx)^-3 conjugated by yxYY
r, psi, uc, P1 = T15.analyse("xxYXyy")
print("n=2 control: rank", r, "; normal form of c:", uc, "; t_1 =", P1, "(TH03: c ~ (t_1^-3, 1), i.e. j = -3)")
