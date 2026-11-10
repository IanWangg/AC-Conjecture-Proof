"""TH19 check of the counts in TH03 Prop. T14: cyclically reduced words w of y-exponent 1 and length <= 9 with I(w) = 20
(TH03: 43 cyclic words; 25 of them with J(w) != J(k_3), by length 6:3, 7:6, 8:5, 9:11; the other 18 by length 7:3, 8:6, 9:9)."""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, "experiments")
from th19_lib import cyc_words, canon, expo, inv
def fred(u):
    out = []
    for c in u:
        if out and out[-1] == c.swapcase(): out.pop()
        else: out.append(c)
    return "".join(out)
PHI = {"a": "b", "b": "Ba", "A": "B", "B": "Ab"}; PHII = {"a": "ab", "b": "a", "A": "BA", "B": "A"}
def phik(u, k):
    for _ in range(abs(k)): u = fred("".join((PHI if k > 0 else PHII)[c] for c in u))
    return u
def nf(w):
    u, k = "", 0
    for ch in w:
        if ch == "x": u = fred(u + phik("a", k))
        elif ch == "X": u = fred(u + phik("A", k))
        elif ch == "y": k += 1
        else: k -= 1
    return u, k
# Z[w] matrices (TH03 T1)
def add(a, b): return (a[0]+b[0], a[1]+b[1])
def mul(a, b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]-a[1]*b[1])
def cj(a): return (a[0]-a[1], -a[1])
def mm(A, B): return tuple(tuple(add(mul(A[i][0], B[0][j]), mul(A[i][1], B[1][j])) for j in range(2)) for i in range(2))
def minv(A): return ((A[1][1], (-A[0][1][0], -A[0][1][1])), ((-A[1][0][0], -A[1][0][1]), A[0][0]))
Z0, ONE, W = (0, 0), (1, 0), (0, 1)
A = ((ONE, ONE), (W, (1, 1))); B = (((1, -1), W), ((1, 1), Z0)); Y = (((-1, -1), Z0), ((-1, -1), W))
G = {"a": A, "b": B, "A": minv(A), "B": minv(B)}
def Iinv(u):
    R = ((ONE, Z0), (Z0, ONE))
    for c in u: R = mm(R, G[c])
    N = mm(R, Y); Nc = tuple(tuple(cj(e) for e in r) for r in N); t = add(mm(N, Nc)[0][0], mm(N, Nc)[1][1])
    assert t[1] == 0
    return t[0]
# rational point (TH03 Prop. T6)
A2 = ((Fr(5, 3), Fr(-1)), (Fr(1), Fr(0))); B2 = ((Fr(2), Fr(0)), (Fr(5, 6), Fr(1, 2))); T2 = ((Fr(12, 19), Fr(-3, 19)), (Fr(-14, 19), Fr(1)))
def m2(M, N): return ((M[0][0]*N[0][0]+M[0][1]*N[1][0], M[0][0]*N[0][1]+M[0][1]*N[1][1]), (M[1][0]*N[0][0]+M[1][1]*N[1][0], M[1][0]*N[0][1]+M[1][1]*N[1][1]))
def i2(M): d = M[0][0]*M[1][1]-M[0][1]*M[1][0]; return ((M[1][1]/d, -M[0][1]/d), (-M[1][0]/d, M[0][0]/d))
G2 = {"a": A2, "b": B2, "A": i2(A2), "B": i2(B2)}; dT = T2[0][0]*T2[1][1]-T2[0][1]*T2[1][0]
def J(u):
    R = ((Fr(1), Fr(0)), (Fr(0), Fr(1)))
    for c in fred(u + phik(u, 1)): R = m2(R, G2[c])
    R = m2(R, T2); t = R[0][0]+R[1][1]; return t*t/dT
k3 = nf("xxxYXyy")[0]; assert Iinv(k3) == 20
Jk = J(k3); same, diff, seen = {}, {}, set()
for L in range(1, 10):
    for w in cyc_words(L):
        if expo(w)[1] != 1: continue
        r = min(w[i:] + w[:i] for i in range(L))
        if r in seen: continue
        seen.add(r)
        u, k = nf(w)
        if Iinv(u) == 20:
            d = same if J(u) == Jk else diff
            d[L] = d.get(L, 0) + 1
print("cyclic words (up to rotation), y-exponent 1, length <= 9, I = 20:", sum(same.values()) + sum(diff.values()))
print("  with J = J(k_3), by length:", dict(sorted(same.items())), " with J != J(k_3), by length:", dict(sorted(diff.items())))
