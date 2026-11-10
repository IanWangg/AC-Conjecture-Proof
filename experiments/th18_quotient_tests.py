#!/usr/bin/env python3
"""TH18 (section 2.10): finite-quotient tests for one-move exits.

Frozen word w = x^2 y^beta X Y (so that (r_n, w) ~AC AK_beta(n), Theorem T9).
A primitive conjugate to r_n^{+-1} modulo w is conjugate to v^j y^{+-1},
v = x y^(beta-1).  A quotient in which the image of r_n has a cycle type
(resp. +-trace) different from those of all v^j y^{+-1} PROVES that no such
primitive exists; "no separation" proves nothing.  All homomorphisms to
PSL(2,p) are enumerated up to conjugacy (x over class representatives of
SL(2,p), y over SL(2,p), w -> +-1).

  python3 experiments/th18_quotient_tests.py --selftest
  python3 experiments/th18_quotient_tests.py N BETA P1 P2 ...     # PSL(2,p) trace test
"""
import sys

def mm(A,B,p): return ((A[0]*B[0]+A[1]*B[2])%p,(A[0]*B[1]+A[1]*B[3])%p,(A[2]*B[0]+A[3]*B[2])%p,(A[2]*B[1]+A[3]*B[3])%p)
def mi(A,p): return (A[3]%p,(-A[1])%p,(-A[2])%p,A[0]%p)
def ev(word,X,Y,p):
    m={'x':X,'y':Y,'X':mi(X,p),'Y':mi(Y,p)}; r=(1,0,0,1)
    for ch in word: r=mm(r,m[ch],p)
    return r
def sl2(p): return [(a,b,c,d) for a in range(p) for b in range(p) for c in range(p) for d in range(p) if (a*d-b*c)%p==1]
def xreps(p):
    nr=next(v for v in range(2,p) if all((u*u-v)%p for u in range(p)))
    return [(0,p-1,1,t) for t in range(p)]+[(1,nr,0,1),(p-1,(-nr)%p,0,p-1),(1,1,0,1),(p-1,p-1,0,p-1),(1,0,0,1),(p-1,0,0,p-1)]
yp=lambda e: 'y'*e if e>=0 else 'Y'*-e
def psl_test(n,beta,primes):
    w="xx"+yp(beta)+"XY"; r="X"+"y"*n+"x"+"Y"*(n+1); v="x"+yp(beta-1)
    for p in primes:
        I=(1,0,0,1); mI=(p-1,0,0,p-1); G=sl2(p)
        for X in xreps(p):
            for Y in G:
                if ev(w,X,Y,p) not in (I,mI): continue
                tr=(lambda M:(M[0]+M[3])%p)
                t=tr(ev(r,X,Y,p)); V=ev(v,X,Y,p); cand=set()
                for eps in (Y,mi(Y,p)):
                    P=eps
                    for _ in range(4*p+4):
                        cand.add(tr(P)); cand.add((-tr(P))%p); P=mm(V,P,p)
                    Vi=mi(V,p); P=eps
                    for _ in range(4*p+4):
                        cand.add(tr(P)); cand.add((-tr(P))%p); P=mm(Vi,P,p)
                if t not in cand:
                    return ("SEPARATED in PSL(2,%d)"%p, X, Y, "tr(r)=%d"%t, "primitive traces", sorted(cand))
    return ("no separation for p in %s"%(primes,),)


def selftest():
    assert psl_test(3, -1, [5, 7])[0] == "SEPARATED in PSL(2,7)"       # agrees with G2(b)
    assert psl_test(3, 1, [5, 7])[0].startswith("no separation")       # an exit exists (T6)
    assert psl_test(3, 2, [5, 7])[0].startswith("no separation")       # an exit exists (2.10)
    print("th18_quotient_tests self-test passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif len(sys.argv) >= 4:
        print(psl_test(int(sys.argv[1]), int(sys.argv[2]), [int(v) for v in sys.argv[3:]]))
    else:
        print(__doc__)
