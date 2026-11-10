#!/usr/bin/env python3
"""TH08 sanity check of Theorem TH08-C (research-th08 section 3.2) on small finite groups.
Statement tested: for a 2-generated group Q = <a,b>, an abelian normal subgroup N (NOT assumed to lie in [Q,Q])
and an admissible pair P of Q:   image of P in Q/N is AC-equivalent to (aN,bN)  ==>  P ~ (a,b) in Q.
Everything is brute force: AC classes by BFS over all pairs (inversion, right multiplication by the other
coordinate or its inverse, conjugation by generators, swap).  Finite groups cannot prove the theorem; a
violation would refute it (note that normal generation of P is not assumed, unlike in BLM's theorem)."""
import itertools, sys
def mul(p,q): return tuple(p[i] for i in q)
def inv(p):
    r=[0]*len(p)
    for i,v in enumerate(p): r[v]=i
    return tuple(r)
def closure(gens,n):
    e=tuple(range(n)); S={e}; fr=[e]
    while fr:
        g=fr.pop()
        for s in gens:
            h=mul(g,s)
            if h not in S: S.add(h); fr.append(h)
    return S
def ncl(elts,G,n):
    conj={mul(mul(inv(q),g),q) for g in elts for q in G}
    return closure(list(conj),n) if conj else {tuple(range(n))}
def ac_class(start,gens,red=lambda g:g,mulf=mul,invf=inv):
    start=(red(start[0]),red(start[1])); seen={start}; fr=[start]
    while fr:
        s,t=fr.pop()
        nb=[(red(invf(s)),t),(s,red(invf(t))),(red(mulf(s,t)),t),(red(mulf(s,invf(t))),t),
            (s,red(mulf(t,s))),(s,red(mulf(t,invf(s)))),(t,s)]
        for q in gens:
            nb.append((red(mulf(mulf(invf(q),s),q)),t)); nb.append((s,red(mulf(mulf(invf(q),t),q))))
        for x in nb:
            if x not in seen: seen.add(x); fr.append(x)
    return seen
def test(name,a,b,n):
    G=closure([a,b],n); Gl=sorted(G); e=tuple(range(n))
    D=ncl([mul(mul(inv(g),inv(h)),mul(g,h)) for g in Gl for h in Gl],G,n)          # derived subgroup
    cos=lambda g,N: min(mul(g,x) for x in N)                                          # coset representative gN
    abm={g:cos(g,D) for g in Gl}
    adm=ac_class((abm[a],abm[b]),[],red=lambda g:abm[g])                              # GL2(Z)-orbit of (ab a, ab b)
    CQ=ac_class((a,b),[a,b])
    normals={frozenset(ncl([g],G,n)) for g in Gl}|{frozenset(ncl([g,h],G,n)) for g in Gl for h in Gl}
    res=[]
    for N in normals:
        if len(N)==1 or any(mul(g,h)!=mul(h,g) for g in N for h in N): continue      # abelian, nontrivial
        red=lambda g,N=N: cos(g,N)
        CN=ac_class((a,b),[a,b],red=red)
        bad=sum(1 for s in Gl for t in Gl if (abm[s],abm[t]) in adm and (red(s),red(t)) in CN and (s,t) not in CQ)
        res.append((len(N), N<=frozenset(D), bad))
    print(f"{name}: |Q|={len(G)}, |[Q,Q]|={len(D)}, |AC class of (a,b)|={len(CQ)}; abelian normal N (|N|, N inside [Q,Q], violations):",sorted(res))
    return sum(r[2] for r in res)
if __name__=="__main__":
    P=lambda *cyc,n: tuple((lambda d:[d.get(i,i) for i in range(n)])({c[i]:c[(i+1)%len(c)] for c in cyc for i in range(len(c))}))
    tot=0
    tot+=test("D4",P((0,2),n=4),P((0,1,2,3),n=4),4)
    tot+=test("D6 = C2 x S3",P((1,5),(2,4),n=6),P((0,1,2,3,4,5),n=6),6)
    tot+=test("C3 x S3",P((0,1),(3,4,5),n=6),P((0,1,2),n=6),6)
    tot+=test("C2 x S4",P((0,1),(4,5),n=6),P((0,1,2,3),n=6),6)
    tot+=test("SD16 = <8-cycle c, t: i -> 3i mod 8>",P((0,1,2,3,4,5,6,7),n=8),P((1,3),(2,6),(5,7),n=8),8)
    tot+=test("C2 x A5",P((0,1,2),(5,6),n=7),P((0,1,2,3,4),n=7),7)
    tot+=test("C3 : C4 (order 12)",P((0,1),(3,4,5,6),n=7),P((0,1,2),n=7),7)
    print("total violations:",tot)
