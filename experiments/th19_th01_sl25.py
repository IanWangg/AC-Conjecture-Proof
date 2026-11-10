"""TH19 check of TH01 Prop. 4.4 (finite part): K = SL(2,5).  Classes of non-central elements under conjugacy and inversion,
and the graph with edges u -- u[kappa,c] whenever (cu)^{o(c)} and u[kappa,c] are non-central (the hypotheses under which
Lemma 2.3 + Cor. 2.2 of TH01 give (u,t) ~ (u[kappa,c],t) in <K,t | [t,z]>).  [g,h] = g^-1 h^-1 g h."""
import itertools
p = 5
def mm(M, N): return ((M[0]*N[0]+M[1]*N[2]) % p, (M[0]*N[1]+M[1]*N[3]) % p, (M[2]*N[0]+M[3]*N[2]) % p, (M[2]*N[1]+M[3]*N[3]) % p)
def inv(M): return (M[3], (-M[1]) % p, (-M[2]) % p, M[0])
I = (1, 0, 0, 1); Z = (4, 0, 0, 4)
K = [M for M in itertools.product(range(p), repeat=4) if (M[0]*M[3]-M[1]*M[2]) % p == 1]
def order(M):
    n, P = 1, M
    while P != I: P = mm(P, M); n += 1
    return n
def pw(M, n):
    P = I
    for _ in range(n): P = mm(P, M)
    return P
nc = [u for u in K if u not in (I, Z)]
par = {u: u for u in nc}
def find(u):
    while par[u] != u: par[u] = par[par[u]]; u = par[u]
    return u
def union(a, b): par[find(a)] = find(b)
for u in nc:
    union(u, inv(u))
    for g in K: union(u, mm(mm(inv(g), u), g))
cls = {}
for u in nc: cls.setdefault(find(u), []).append(u)
print(f"|K| = {len(K)}, non-central: {len(nc)}; classes under conjugacy and inversion: {len(cls)}, orders {sorted(order(v[0]) for v in cls.values())}")
ords = {c: order(c) for c in K}
edges = 0
for u in nc:
    for c in K:
        cu = pw(mm(c, u), ords[c])
        if cu in (I, Z): continue
        ci = inv(c)
        for kap in K:
            w = mm(u, mm(mm(inv(kap), ci), mm(kap, c)))
            if w in (I, Z): continue
            if find(u) != find(w): union(u, w); edges += 1
print("components after adding the commutator-transfer edges:", len({find(u) for u in nc}))
