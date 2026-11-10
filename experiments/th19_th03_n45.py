"""TH19: third independent check of the isospectral cases of TH03 (n = 4, 5).
H = <a,b,t | t a t^-1 = b^-1 a, t b t^-1 = a^-1 b^2>;  homs H -> PSL(2,p), p = 7, 13:
all A in SL(2,p), T over class representatives, B := A T A^-1 T^-1 (relation 1), relation 2 up to sign.
k_n^2 = a^n b^-1 a^-1 b^n a^-1 t and (x^s y)^2 = a^s b^s t in H; non-conjugate if some hom gives different |trace|.
(The G_c-class of g^2 is one H-class because g centralizes g^2, so no twist by y is needed.)"""
import itertools
def run(p):
    def mm(M, N): return ((M[0]*N[0]+M[1]*N[2]) % p, (M[0]*N[1]+M[1]*N[3]) % p, (M[2]*N[0]+M[3]*N[2]) % p, (M[2]*N[1]+M[3]*N[3]) % p)
    def inv(M): return (M[3], (-M[1]) % p, (-M[2]) % p, M[0])
    def neg(M): return tuple((-e) % p for e in M)
    def pw(M, n):
        if n < 0: M, n = inv(M), -n
        R = (1, 0, 0, 1)
        for _ in range(n): R = mm(R, M)
        return R
    SL = [M for M in itertools.product(range(p), repeat=4) if (M[0]*M[3]-M[1]*M[2]) % p == 1]
    seen, reps = set(), []
    for M in SL:
        if M in seen: continue
        reps.append(M)
        for g in SL: seen.add(mm(mm(g, M), inv(g)))
    atr = lambda M: min((M[0]+M[3]) % p, (-(M[0]+M[3])) % p)
    pairs = [(1, -2), (2, -2), (1, 3), (2, 3), (3, 4), (3, -3), (4, -4), (4, 5), (5, -5), (5, 6)]
    sep = {q: 0 for q in pairs}; homs = 0
    for T in reps:
        Ti = inv(T)
        for A in SL:
            Ai = inv(A)
            B = mm(mm(A, T), mm(Ai, Ti))
            L = mm(mm(T, B), Ti); R = mm(Ai, mm(B, B))
            if L != R and L != neg(R): continue
            Bi = inv(B)
            if mm(A, B) in (mm(B, A), neg(mm(B, A))): continue   # abelian fibre image: skip
            homs += 1
            for (n, s) in pairs:
                k2 = mm(mm(mm(pw(A, n), mm(Bi, Ai)), mm(pw(B, n), Ai)), T)
                g2 = mm(mm(pw(A, s), pw(B, s)), T)
                if atr(k2) != atr(g2): sep[(n, s)] += 1
    print(f"p={p}: |SL(2,p)|={len(SL)}, class reps {len(reps)}, homs with non-abelian fibre image {homs}")
    print("   (n,s): number of separating homs:", sep)
    return sep
tot = {}
for p in (7, 13):
    for q, v in run(p).items(): tot[q] = tot.get(q, 0) + v
assert tot[(1, -2)] == 0 and tot[(2, -2)] == 0, "control failed: k_1 ~ k_2 ~ x^-2 y must never be separated"
for q in [(4, -4), (4, 5), (5, -5), (5, 6), (3, 4), (3, -3)]:
    assert tot[q] > 0, q
print("OK: controls (1,-2),(2,-2) never separated; (4,-4),(4,5),(5,-5),(5,6) each separated by some hom")
