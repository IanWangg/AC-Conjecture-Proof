"""TH19 independent check of TH03 Theorem T11 (Q2(3): k_3-frozen primitive exit from P_3 does not exist).
G_{k_3} = <x,y | x^3 Y X y y> = F(t0,t1,t2) x|_psi <x>, t = y x^2, psi: t0->t1->t2->t2 t0.
Own truncated Magnus algebra Z<X0,X1,X2>/(deg > 3).  Checks: (0) normal forms: k_3 -> (1,0), c -> (t1 t2^-1 t1^-1, 1),
x t^j -> (t1^j, 1); (1) the 39 identities (TT) for the functional l of the note; (2) l(M(v u psi(v)^-1)) = l(M(u)) on random
u, v; (3) l(M(t1^j)) = j(j-1)/2 for |j| <= 60 (and as a polynomial identity); (4) l(M(t1 t2^-1 t1^-1)) = -2."""
import random, itertools
D = 3
def mul(A, B):
    out = {}
    for m1, a in A.items():
        for m2, b in B.items():
            if len(m1) + len(m2) <= D:
                m = m1 + m2; out[m] = out.get(m, 0) + a*b
    return {m: v for m, v in out.items() if v}
def add(A, B, s=1):
    out = dict(A)
    for m, v in B.items(): out[m] = out.get(m, 0) + s*v
    return {m: v for m, v in out.items() if v}
ONE = {(): 1}
def gen(i, e):      # Magnus image of t_i^e, e = +-1
    if e == 1: return {(): 1, (i,): 1}
    return {(): 1, (i,): -1, (i, i): 1, (i, i, i): -1}
# words in t0,t1,t2: lists of (i, e)
def M(word):
    R = ONE
    for (i, e) in word: R = mul(R, gen(i, e))
    return R
def winv(w): return [(i, -e) for (i, e) in reversed(w)]
def wred(w):
    out = []
    for g in w:
        if out and out[-1][0] == g[0] and out[-1][1] == -g[1]: out.pop()
        else: out.append(g)
    return out
PSI = {0: [(1, 1)], 1: [(2, 1)], 2: [(2, 1), (0, 1)]}
PSII = {0: [(1, -1), (2, 1)], 1: [(0, 1)], 2: [(1, 1)]}      # psi^-1: t0 -> t1^-1 t2, t1 -> t0, t2 -> t1
def ap(w, table):
    out = []
    for (i, e) in w: out += table[i] if e == 1 else winv(table[i])
    return wred(out)
assert all(ap(ap([(i, 1)], PSI), PSII) == [(i, 1)] and ap(ap([(i, 1)], PSII), PSI) == [(i, 1)] for i in range(3))
def psik(w, k):
    for _ in range(abs(k)): w = ap(w, PSI if k > 0 else PSII)
    return w
def nf(xyword):     # x -> level+1 ; y = t x^-2 ; Y = x^2 t^-1
    u, k = [], 0
    for ch in xyword:
        if ch == "x": k += 1
        elif ch == "X": k -= 1
        elif ch == "y": u = wred(u + psik([(0, 1)], k)); k -= 2
        else: k += 2; u = wred(u + psik([(0, -1)], k))
    return u, k
assert nf("xxxYXyy") == ([], 0), nf("xxxYXyy")
assert nf("xyxYYXy") == ([(1, 1), (2, -1), (1, -1)], 1), nf("xyxYYXy")
for j in range(-5, 6):      # x t^j with t = y x^2
    w = "x" + ("yxx"*j if j >= 0 else "XXY"*(-j))
    assert nf(w) == ([(1, 1 if j > 0 else -1)]*abs(j), 1), (j, nf(w))
print("(0) normal forms: k_3 -> (1,0); c -> (t1 t2^-1 t1^-1, 1); x t^j -> (t1^j, 1), |j| <= 5")
L = {}
for s in "00 01 02 10 11 12 21 22".split(): L[tuple(map(int, s))] = 1
for s in "002 021 022 100 102 110 200 211 221".split(): L[tuple(map(int, s))] = 1
for s in "010 012 101 120 121 202 212".split(): L[tuple(map(int, s))] = -1
L[(2, 1, 0)] = 2; L[(0, 2, 0)] = -2; L[(2, 0, 1)] = -2
def ell(A): return sum(v * L.get(m, 0) for m, v in A.items())
PsiX = {0: {(1,): 1}, 1: {(2,): 1}, 2: {(2,): 1, (0,): 1, (2, 0): 1}}
bad = 0; cnt = 0
for d in range(0, D):
    for m in itertools.product(range(3), repeat=d):
        for i in range(3):
            cnt += 1
            if ell({(i,) + m: 1}) != ell(mul({m: 1}, PsiX[i])): bad += 1
print(f"(1) twisted-trace identities (TT): {cnt} checked, {bad} violated")
random.seed(5); viol = 0
for _ in range(400):
    u = wred([(random.randrange(3), random.choice((1, -1))) for _ in range(random.randint(0, 9))])
    v = wred([(random.randrange(3), random.choice((1, -1))) for _ in range(random.randint(1, 7))])
    if ell(M(wred(v + u + winv(ap(v, PSI))))) != ell(M(u)): viol += 1
print(f"(2) invariance under twisted conjugation u -> v u psi(v)^-1 on 400 random pairs: {viol} violations")
vals = {j: ell(M([(1, 1 if j > 0 else -1)]*abs(j))) for j in range(-60, 61)}
print("(3) l(M(t1^j)) == j(j-1)/2 for |j| <= 60:", all(vals[j] == j*(j-1)//2 for j in vals), "; min value", min(vals.values()))
print("(4) l(M(t1 t2^-1 t1^-1)) =", ell(M([(1, 1), (2, -1), (1, -1)])))
