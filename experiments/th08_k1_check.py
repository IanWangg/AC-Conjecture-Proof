#!/usr/bin/env python3
"""TH08 spot-check of research-k Theorem K1 (independent of k_ak_family.py).
Replays the 4n-1 cyclic products AK(n) -> P_n in closed form and checks, for each step,
(1) the multiplier is a rotation of the frozen relator or of its inverse, and
(2) cyc(multiplier * current) is a rotation of the claimed word (current may be inverted first)."""
import sys
def inv(w): return w[::-1].swapcase()
def red(w):
    o=[]
    for ch in w:
        if o and o[-1]==ch.swapcase(): o.pop()
        else: o.append(ch)
    return "".join(o)
def cyc(w):
    w=red(w)
    while len(w)>1 and w[0]==w[-1].swapcase(): w=w[1:-1]
    return w
def rots(w): return {w[i:]+w[:i] for i in range(len(w))}
def same(u,v): return len(u)==len(v) and u in rots(v)
def step(cur,frozen,mult,claim,log,left=True,invert=False):
    assert cyc(frozen)==frozen and (mult in rots(frozen) or mult in rots(inv(frozen))), ("multiplier",mult,frozen)
    r=inv(cur) if invert else cur
    new=cyc(mult+r) if left else cyc(r+mult)
    assert same(new,claim), ("identity",new,claim)
    log.append((new,frozen)); return claim
def run(n):
    x,X,y,Y="x","X","y","Y"; log=[]
    b="xyxYXY"; p=x*n+Y*(n+1)
    u=lambda k: x*(n-1)+Y*(n+1-k)+"xy"+X*k+"Y"
    v=x*(n-1)+y+X*(n-1)+"yXY"; w=x*n+y+X*(n+1)+Y
    a=lambda m: x*m+"yXYXy"; bb=lambda m: x*n+"YXy"+X*(n-m)+y; c_=lambda m: x*(n-1)+y+X*(n-m)+"yXY"
    d=x*n+"YXyy"; c="xyxYYXy"
    assert u(n+1)==w and c_(1)==v
    cur=step(p,b,inv(b),u(1),log,left=False)                       # A1a: u_1 = cyc(p_n b^-1)
    sinv="xyXY"+x*(n-1)+Y*n
    v_=step(p,cur,sinv,v,log,invert=True)                           # A1b: v_n = cyc(s^-1 p_n^-1)
    rho="yXY"+x*(n-1)+y+X*(n-1)
    for k in range(1,n+1): cur=step(cur,v_,rho,u(k+1),log)          # A2
    assert cur==w
    sig=X+y+x*(n+1)+Y+X*(n-1); kap="XY"+x*n+y+X*n
    e=step(v_,w,sig,a(2),log)                                       # B: c_1 -> a_2
    for m in range(2,n):
        tau=X*(n-m)+y+x*(n+1)+Y+X*m
        e=step(e,w,tau,bb(m),log); e=step(e,w,kap,c_(m),log); e=step(e,w,sig,a(m+1),log)
    assert e==a(n)
    wp=y+x*(n+1)+Y+X*n
    new=cyc(e+wp); assert wp in rots(inv(w)) and same(new,d); log.append((new,e))   # C1: d_n = cyc(a_n w'), a_n multiplies w'
    new2=cyc(d+inv(e)); assert same(new2,c); log.append((new2,d))                   # C2: c = cyc(d_n a_n^-1)
    assert len(log)==4*n-1
    return max(len(s)+len(t) for s,t in log)
if __name__=="__main__":
    lo,hi=(int(sys.argv[1]),int(sys.argv[2])) if len(sys.argv)>2 else (2,40)
    for n in range(lo,hi+1):
        peak=run(n)
        if n<=6 or n==hi: print(f"n={n}: {4*n-1} cyclic products verified, peak cyclic total length {peak} (4n+5={4*n+5})")
    print("K1 closed-form path verified for n =",lo,"..",hi)
