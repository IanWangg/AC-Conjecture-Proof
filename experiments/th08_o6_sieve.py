#!/usr/bin/env python3
"""TH08 spot-check of research-o Theorem O6 (independent re-implementation, no imports from o_*).
H = <a,b,t | t a t^-1 = b^-1 a, t b t^-1 = a^-1 b^2> (index 2 in G_c, t = y^2).
If k_n ~ x^s y in G_c then k_n^2 = a^n B A b^n A t is H-conjugate to a^s b^s t or to b^s (b^-1 a)^s t.
For every hom rho: H -> PSL(2,p) the traces up to sign must then agree; sieve over s mod 1092."""
from math import gcd
def mul(A,B,p):
    a,b,c,d=A; e,f,g,h=B
    return ((a*e+b*g)%p,(a*f+b*h)%p,(c*e+d*g)%p,(c*f+d*h)%p)
def inv(A,p):
    a,b,c,d=A; return (d%p,(-b)%p,(-c)%p,a%p)
def norm(A,p):
    B=tuple((-v)%p for v in A); return min(A,B)
def powm(A,k,p):
    R=(1,0,0,1)
    for _ in range(k): R=mul(R,A,p)
    return R
def order(A,p):
    R=A; k=1
    while norm(R,p)!=(1,0,0,1) and norm(R,p)!=norm((1,0,0,1),p): R=mul(R,A,p); k+=1
    return k
def atr(A,p):
    t=(A[0]+A[3])%p; return min(t,p-t)
def lcm(a,b): return a*b//gcd(a,b)
def homs(p):
    G=sorted({norm((a,b,c,d),p) for a in range(p) for b in range(p) for c in range(p) for d in range(p) if (a*d-b*c)%p==1})
    seen=set(); reps=[]
    for T in G:                       # conjugacy class representatives for T
        if T in seen: continue
        reps.append(T)
        for g in G: seen.add(norm(mul(mul(g,T,p),inv(g,p),p),p))
    out=[]
    for T in reps:
        Ti=inv(T,p)
        for A in G:
            Ai=inv(A,p); B=mul(mul(A,T,p),mul(Ai,Ti,p),p)      # b = a t a^-1 t^-1
            if norm(mul(mul(T,B,p),Ti,p),p)==norm(mul(Ai,mul(B,B,p),p),p): out.append((A,B,T))
    return len(G),out
def allowed(A,B,T,n,p):
    Ai=inv(A,p); Bi=inv(B,p); C=mul(Bi,A,p)
    P=lcm(lcm(order(A,p),order(B,p)),order(C,p))
    k2=mul(mul(mul(powm(A,n,p),mul(Bi,Ai,p),p),mul(powm(B,n,p),Ai,p),p),T,p)
    tk=atr(k2,p); ok=set()
    for s in range(P):
        c1=mul(mul(powm(A,s,p),powm(B,s,p),p),T,p); c2=mul(mul(powm(B,s,p),powm(C,s,p),p),T,p)
        if tk in (atr(c1,p),atr(c2,p)): ok.add(s)
    return P,ok
if __name__=="__main__":
    L=1092; surv={n:set(range(L)) for n in range(1,9)}; first_empty={}
    for p in (7,13):
        size,hs=homs(p); nonab=[h for h in hs if norm(mul(h[0],h[1],p),p)!=norm(mul(h[1],h[0],p),p)]
        print(f"p={p}: |PSL(2,p)|={size}, homs (T up to conj)={len(hs)}, non-abelian fibre image={len(nonab)}")
        for (A,B,T) in hs:
            for n in range(1,9):
                P,ok=allowed(A,B,T,n,p); assert L%P==0
                surv[n]={s for s in surv[n] if s%P in ok}
                if not ok and n not in first_empty: first_empty[n]=(p,A,B,T,P)
    for n in range(1,9):
        sm=sorted(surv[n], key=lambda s: min(s,L-s))[:4]
        print(f"n={n}: surviving s mod {L}: {len(surv[n])}", [s if s<=L//2 else s-L for s in sm], "single-hom witness:" , first_empty.get(n))
    # O's explicit witness
    p=13; A=(0,2,6,8); B=(1,11,6,2); T=(0,1,12,5)
    assert all((M[0]*M[3]-M[1]*M[2])%p==1 for M in (A,B,T))
    r1=norm(mul(mul(T,A,p),inv(T,p),p),p)==norm(mul(inv(B,p),A,p),p)
    r2=norm(mul(mul(T,B,p),inv(T,p),p),p)==norm(mul(inv(A,p),mul(B,B,p),p),p)
    print("witness: relations",r1,r2,"orders",order(A,p),order(B,p),order(mul(inv(B,p),A,p),p))
    for n in range(1,9):
        P,ok=allowed(A,B,T,n,p); print(f"  n={n}: period {P}, allowed residues {sorted(ok)}")
