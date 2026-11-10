"""TH19 independent check of TH09 Theorem 6 (full sieve, n = 5, 8): BS(1,2)-type killers v_j^+ = (b a^-j B A, -1),
v_j^- = (a B a^-j, -1) of G_c versus k_n = (a^n B A, 1); squares in H = <a,b,t>:
(v_j^+)^2 = b a^-j B A . a (ab)^-j A (ab)^-1 . t^-1,  (v_j^-)^2 = a B a^-j . a b A (ab)^-j . t^-1,  k_n^2 = a^n B A b^n A . t.
All homs H -> PSL(2,p), p = 7, 13, with non-abelian fibre image (own enumeration, as in th19_th03_n45.py);
a residue j mod 1092 survives for n if |tr| agrees in every hom."""
import itertools
def homs(p):
    def mm(M, N): return ((M[0]*N[0]+M[1]*N[2]) % p, (M[0]*N[1]+M[1]*N[3]) % p, (M[2]*N[0]+M[3]*N[2]) % p, (M[2]*N[1]+M[3]*N[3]) % p)
    def inv(M): return (M[3], (-M[1]) % p, (-M[2]) % p, M[0])
    neg = lambda M: tuple((-e) % p for e in M)
    SL = [M for M in itertools.product(range(p), repeat=4) if (M[0]*M[3]-M[1]*M[2]) % p == 1]
    seen, reps = set(), []
    for M in SL:
        if M in seen: continue
        reps.append(M)
        for g in SL: seen.add(mm(mm(g, M), inv(g)))
    out = []
    for T in reps:
        Ti = inv(T)
        for A in SL:
            Ai = inv(A); B = mm(mm(A, T), mm(Ai, Ti))
            L = mm(mm(T, B), Ti); R = mm(Ai, mm(B, B))
            if L != R and L != neg(R): continue
            if mm(A, B) in (mm(B, A), neg(mm(B, A))): continue
            out.append((A, B, T))
    return out, mm, inv
MOD = 1092; NS = range(1, 9)
surv = {(n, sg): set(range(MOD)) for n in NS for sg in "+-"}
nh = 0
for p in (7, 13):
    H, mm, inv = homs(p); nh += len(H)
    atr = lambda M: min((M[0]+M[3]) % p, (-(M[0]+M[3])) % p)
    I = (1, 0, 0, 1)
    for (A, B, T) in H:
        Ai, Bi, Ti = inv(A), inv(B), inv(T); AB = mm(A, B); ABi = inv(AB)
        pa, pab = [I], [I]                         # powers of a^-1 and (ab)^-1
        for _ in range(MOD): pa.append(mm(pa[-1], Ai)); pab.append(mm(pab[-1], ABi))
        left_p = lambda j: mm(mm(mm(B, pa[j]), mm(Bi, Ai)), mm(mm(A, pab[j]), mm(Ai, ABi)))
        left_m = lambda j: mm(mm(mm(A, Bi), pa[j]), mm(mm(AB, Ai), pab[j]))
        tp = [atr(mm(left_p(j), Ti)) for j in range(MOD)]
        tm = [atr(mm(left_m(j), Ti)) for j in range(MOD)]
        An = I; Bn = I
        for n in NS:
            An = mm(An, A); Bn = mm(Bn, B)
            tk = atr(mm(mm(mm(An, mm(Bi, Ai)), mm(Bn, Ai)), T))
            surv[(n, "+")] = {j for j in surv[(n, "+")] if tp[j] == tk}
            surv[(n, "-")] = {j for j in surv[(n, "-")] if tm[j] == tk}
print(f"{nh} homs (p = 7, 13)")
for n in NS:
    print(f"n={n}: surviving j mod 1092: v^+ {sorted(surv[(n,'+')])[:6]}  v^- {sorted(surv[(n,'-')])[:6]}")
