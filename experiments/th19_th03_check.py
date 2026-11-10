"""TH19 independent exact check of TH03 (figure-eight / Gieseking invariant I).
Z[w], w^2 = -1-w, elements (p,q) = p+qw.  Matrices from research-th03 Prop. T1.
Checks: T1(i),(iii),(iv); I(u) in Z; sigma(s)=I(a^s), tau(n)=I(a^n b^-1 a^-1); recurrence
u(n+4)=3u(n+3)-u(n+2)+3u(n+1)-u(n); sigma(s)=sigma(1-s); all solutions of tau(n)=sigma(s) in a box;
induction base for 'd(n+1) >= 2 d(n) > 0' (three consecutive n), which propagates through the recurrence."""
import sys
def add(a,b): return (a[0]+b[0], a[1]+b[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]-a[1]*b[1])
def cj(a): return (a[0]-a[1], -a[1])
def neg(a): return (-a[0], -a[1])
Z0,ONE,W = (0,0),(1,0),(0,1); W2 = (-1,-1)
def mm(A,B): return tuple(tuple(add(mul(A[i][0],B[0][j]), mul(A[i][1],B[1][j])) for j in range(2)) for i in range(2))
def det(A): return add(mul(A[0][0],A[1][1]), neg(mul(A[0][1],A[1][0])))
def minv(A):
    assert det(A) == ONE
    return ((A[1][1], neg(A[0][1])), (neg(A[1][0]), A[0][0]))
def mc(A): return tuple(tuple(cj(e) for e in r) for r in A)
def tr(A): return add(A[0][0], A[1][1])
I2 = ((ONE,Z0),(Z0,ONE))
A = ((ONE,ONE),(W,(1,1)))
B = (((1,-1),W),((1,1),Z0))
Y = ((W2,Z0),(W2,W))
assert det(A)==ONE and det(B)==ONE and det(Y)==ONE
Ai,Bi,Yi = minv(A),minv(B),minv(Y)
assert mm(Y,mc(A)) == mm(B,Y), "T1(i) first identity"
assert mm(Y,mc(B)) == mm(mm(Bi,A),Y), "T1(i) second identity"
T = mm(Y,mc(Y))
assert T == ((ONE,Z0),(neg(W),ONE))
assert mm(mm(T,A),minv(T)) == mm(Bi,A) and mm(mm(T,B),minv(T)) == mm(Ai,mm(B,B)), "T1(iii)"
assert tr(A)==(2,1) and tr(B)==(1,-1) and tr(mm(A,B))==(1,-1)
assert tr(mm(mm(A,B),mm(Ai,Bi))) == (-2,0), "parabolic commutator"
def mpow(M,n):
    if n < 0: M = minv(M); n = -n
    R = I2
    for _ in range(n): R = mm(R,M)
    return R
def Iinv(M):
    N = mm(M,Y); t = tr(mm(N,mc(N)))
    assert t[1] == 0, "I not a rational integer"
    return t[0]
def sigma(s): return Iinv(mpow(A,s))
def tau(n): return Iinv(mm(mpow(A,n), mm(Bi,Ai)))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
sg = {s: sigma(s) for s in range(-N-3, N+5)}
ta = {n: tau(n) for n in range(-N-3, N+5)}
for seq in (sg, ta):
    for n in range(-N-3, N+1):
        assert seq[n+4] == 3*seq[n+3] - seq[n+2] + 3*seq[n+1] - seq[n], "recurrence"
assert all(sg[s] == sg[1-s] for s in range(-N, N+1)), "sigma(s)=sigma(1-s)"
print("sigma(0..9) =", [sg[s] for s in range(10)])
print("tau(1..9)   =", [ta[n] for n in range(1, 10)])
sols = [(n,s) for n in range(1, N+1) for s in range(-N, N+1) if ta[n] == sg[s]]
print(f"solutions of tau(n)=sigma(s), 1<=n<={N}, |s|<={N}:", sols)
bad = [n for n in range(6, N+1) if not (sg[n] < ta[n] < sg[n+1])]
print("n in [6,N] violating sigma(n)<tau(n)<sigma(n+1):", bad)
print("sigma strictly increasing on 1..N:", all(sg[s] < sg[s+1] for s in range(1, N)))
print("tau strictly increasing on 2..N:", all(ta[n] < ta[n+1] for n in range(2, N)))
# induction base: if d(k+1) >= 2 d(k) > 0 for k = m, m+1, m+2 then (recurrence) d(m+4) >= 2.5 d(m+3), so it propagates
def base(name, d, lo=1, hi=40):
    for m in range(lo, hi):
        if all(d(k+1) >= 2*d(k) > 0 for k in (m, m+1, m+2)):
            print(f"  {name}: doubling base holds from m = {m}"); return m
    print(f"  {name}: NO base found")
base("d1(n)=tau(n)-sigma(n)", lambda n: ta[n]-sg[n])
base("d2(n)=sigma(n+1)-tau(n)", lambda n: sg[n+1]-ta[n])
base("ds(s)=sigma(s+1)-sigma(s)", lambda s: sg[s+1]-sg[s])
base("dt(n)=tau(n+1)-tau(n)", lambda n: ta[n+1]-ta[n])
print("small n table (n, sigma(n), tau(n), sigma(n+1)):", [(n, sg[n], ta[n], sg[n+1]) for n in range(1, 9)])
