#!/usr/bin/env python3
"""TH08 sanity check of Theorem P1 (research-th08 section 3) on a finite image of G0 x G1 for AK(3).
G0 = <x,y | x^3 = y^4> -> S4 (x=(0 1 2), y=(0 1 2 3));  G1 = <x,y | xyx = yxy> -> SL(2,5).
Elements of Q = image of F in S4 x SL(2,5) are pairs (perm, matrix).  The three steps of the proof are
replayed with explicit elements and every membership 'multiplier in normal closure of the other coordinate'
is checked by brute force inside Q.  (A finite image cannot prove P1; it can only catch a wrong step.)"""
P=5
def pm(a,b): return tuple(a[i] for i in b)          # composition: first b then a (any fixed convention)
def pinv(a):
    r=[0]*len(a)
    for i,v in enumerate(a): r[v]=i
    return tuple(r)
def mm(A,B):
    a,b,c,d=A; e,f,g,h=B
    return ((a*e+b*g)%P,(a*f+b*h)%P,(c*e+d*g)%P,(c*f+d*h)%P)
def minv(A): a,b,c,d=A; return (d%P,(-b)%P,(-c)%P,a%P)
def mul(g,h): return (pm(g[0],h[0]), mm(g[1],h[1]))
def inv(g): return (pinv(g[0]), minv(g[1]))
E=((0,1,2,3),(1,0,0,1))
X=((1,2,0,3),(1,1,0,1)); Y=((1,2,3,0),(1,0,P-1,1))
def word(w):
    r=E
    for ch in w: r=mul(r,{'x':X,'y':Y,'X':inv(X),'Y':inv(Y)}[ch])
    return r
def closure(gens,normal_in=None):
    S={E}; frontier=[E]; gens=list(gens)
    if normal_in is not None:                       # normal closure: close generators under conjugation first
        conj=set(gens); fr=list(gens)
        while fr:
            g=fr.pop()
            for q in normal_in:
                h=mul(mul(inv(q),g),q)
                if h not in conj: conj.add(h); fr.append(h)
        gens=list(conj)
    while frontier:
        g=frontier.pop()
        for s in gens:
            h=mul(g,s)
            if h not in S: S.add(h); frontier.append(h)
    return S
if __name__=="__main__":
    assert word("xxx")[0]==word("yyyy")[0] and word("xyx")[1]==word("yxy")[1]      # relations of G0, G1 hold
    Q=closure([X,Y]); print("|Q| =",len(Q),"(S4 x SL(2,5) has order",24*120,")")
    gensQ=[X,Y,inv(X),inv(Y)]
    proj0=lambda g:(g[0],E[1]); proj1=lambda g:(E[0],g[1])
    u0=word("xxxYYYY"); u1=word("xyxYXY")
    row0=proj1(u0); row1=proj0(u1)                  # pi(u0) = (1,k), pi(u1) = (k',1) in G0 x G1
    assert row0 in Q and row1 in Q
    N1=closure([row1],gensQ)
    alpha=proj0(mul(inv(Y),u1)); assert alpha in N1   # step 1: alpha = y^-1 k' in G0, (alpha,1) in <<row1>>
    row0=mul(row0,alpha)
    N0=closure([row0],gensQ)
    d=proj1(word("xxxYYY")); m2=mul(inv(row0),d); assert d in N0 and m2 in N0   # step 2
    row1=mul(row1,m2); assert row1==Y; print("step 2: row 1 = pi(y) exactly")
    NY=closure([Y],gensQ)
    m3=mul(inv(row0),word("xYY")); assert m3 in NY    # step 3: row 0 -> pi(x y^-2)
    row0=mul(row0,m3); assert row0==word("xYY")
    print("step 3: pair = (pi(x y^-2), pi(y)), a Nielsen image of (pi(x), pi(y)); all memberships verified")
