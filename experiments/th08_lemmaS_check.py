#!/usr/bin/env python3
"""TH08 spot-check of research-i Lemma S (free-word replay of the five steps) and of the
'defect 2 => AC-trivial without congruence' remark (Euclid on exponent rows, Lemma E / G 2.4(b))."""
def inv(w): return w[::-1].swapcase()
def red(w):
    o=[]
    for ch in w:
        if o and o[-1]==ch.swapcase(): o.pop()
        else: o.append(ch)
    return "".join(o)
def pw(l,e): return (l*e) if e>=0 else (l.swapcase()*(-e))
def rots(w): return {w[i:]+w[:i] for i in range(len(w))} or {""}
def cyc(w):
    w=red(w)
    while len(w)>1 and w[0]==w[-1].swapcase(): w=w[1:-1]
    return w
def lemma_S(a,k,q):
    m=a+1; A=red(pw("x",a)+"yXy"); z="Xy"; Z=inv(z); c=pw("x",m); C=inv(c)
    assert red(c+z+z)==A                                   # A = c z^2 as free words
    P=red(pw("y",q)+"x"+Z)
    rel=red(P+z+pw("x",m*k)); assert rel==red(pw("y",q)+pw("x",1+m*k))      # step 1 (a rotation of B)
    ins=0
    for j in range(k):                                     # step 2: insert [c,z] = A * (z A^-1 z^-1)
        left=red(P+c*j) if m>=0 else red(P+pw("x",m*j)); right=red(z+pw("x",m*(k-j)))
        assert red(left+right)==rel
        comm=red(A+z+inv(A)+Z); assert comm==red(c+z+C+Z)
        rel=red(left+comm+right); ins+=2
        assert rel==red(P+pw("x",m*(j+1))+z+pw("x",m*(k-j-1)))
    assert rel==red(P+pw("x",m*k)+z)
    rel=red(z+P+pw("x",m*k))                               # step 3: conjugate by z
    left=red(z+pw("y",q)+"x"); right=red(Z+pw("x",m*k)); assert red(left+right)==rel
    rel=red(left+red(z+A+Z)+right); ins+=1                 # step 4: insert z A z^-1
    assert rel==red("X"+pw("y",q+2)+pw("x",m*(k+1)))
    target=red(pw("x",m*k+m-1)+pw("y",q+2))                # step 5: rotate
    assert cyc(rel)==cyc(target) or cyc(rel) in rots(cyc(target)), (a,k,q,rel,target)
    assert ins==2*k+1
def euclid_trivial(m,n,p,q):
    """row operations r_i <- r_i +- r_j on words x^e y^f; returns True if (x^m y^n, x^p y^q) reduces to (x^+-1, y^+-1)."""
    r=[[m,n],[p,q]]; steps=0
    while steps<10000:
        steps+=1
        if sorted(map(lambda v:(abs(v[0]),abs(v[1])),r))==[(0,1),(1,0)]: return True
        i=0 if abs(r[0][0])+abs(r[0][1])>=abs(r[1][0])+abs(r[1][1]) else 1; j=1-i
        best=min(((abs(r[i][0]+s*r[j][0])+abs(r[i][1]+s*r[j][1])),s) for s in (1,-1))
        if best[0]>=abs(r[i][0])+abs(r[i][1]): return False
        s=best[1]; r[i]=[r[i][0]+s*r[j][0], r[i][1]+s*r[j][1]]
    return False
if __name__=="__main__":
    cnt=0
    for a in range(-8,9):
        for k in range(0,6):
            for q in range(-9,10): lemma_S(a,k,q); cnt+=1
    print("Lemma S: five steps verified as free-word identities on",cnt,"instances (a in [-8,8], k in [0,5], q in [-9,9])")
    lemma_S(2,1,7); print("  concrete instance T(2;4,7) -> T(2;5,9): ok")
    # defect-2 partners of x^m y^n where Prop. M's congruence FAILS but Lemma E still trivializes
    from math import gcd
    bad=0; tot=0
    for m in range(2,13):
        for n in range(2,13):
            if gcd(m,n)!=1 or (n-1)%m==0 or (n+1)%m==0 or (m-1)%n==0 or (m+1)%n==0: continue
            for i in range(-40,41):
                for j in range(-40,41):
                    if abs(n*i-m*j)==1:
                        tot+=1; bad+= (not euclid_trivial(m,n,i,j))
    print(f"non-congruent torus types (e.g. (5,7),(5,8)): {tot} defect-2 pairs (x^m y^n, x^i y^j), Euclid fails on {bad}")
