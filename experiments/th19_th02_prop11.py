"""TH19 check of TH02 Prop. 11: free identities of the reduction, the abelianization constraint, the word counts, and an
independent exclusion of all Z of length 12 and 14 by random finite quotients of H = <x0,x1,x2 | x1^3 = x2 x0^2 x2>
(images: x0, x2 random in S_n, x1 = a cube root of x2 x0^2 x2 that is a power of it)."""
import sys, random, itertools
sys.path.insert(0, "experiments")
from th19_lib import red, inv
xi = lambda i: red(("y"*i if i >= 0 else "Y"*(-i)) + "x" + ("Y"*i if i >= 0 else "y"*(-i)))
assert red(xi(0)*3 + inv(xi(1)) + inv(xi(-1))*2 + inv(xi(1))) == "xxxyXYYXXyyXY", "r1"
assert red(xi(0) + xi(3) + "y") == "xyyyxYY" and red(inv(xi(0)) + inv(xi(3)) + "y") == "XyyyXYY", "s_w, eps_x(s_w)"
print("free identities: r1 = x0^3 x1^-1 x_-1^-2 x1^-1, s_w = x0 x3 y, eps_x(s_w) = x0^-1 x3^-1 y  -- OK")
def count(L):    # reduced words in p,q (letters p,P,q,Q) of length L with exponent sums (-6, 6), by DP
    from collections import defaultdict
    st = defaultdict(int); st[(None, 0, 0)] = 1
    for _ in range(L):
        nx = defaultdict(int)
        for (last, a, b), c in st.items():
            for ch, da, db in (("p", 1, 0), ("P", -1, 0), ("q", 0, 1), ("Q", 0, -1)):
                if last is not None and last == ch.swapcase(): continue
                nx[(ch, a+da, b+db)] += c
        st = nx
    return sum(c for (l, a, b), c in st.items() if (a, b) == (-6, 6))
print("counts of reduced Z with exponent sums (-6,6), lengths 12..18:", [count(L) for L in (12, 14, 16, 18)])
def perm_ops(n):
    mul = lambda p, q: tuple(q[p[i]] for i in range(n))          # p then q
    def inv_(p):
        r = [0]*n
        for i, j in enumerate(p): r[j] = i
        return tuple(r)
    def pw(p, k):
        if k < 0: p, k = inv_(p), -k
        r = tuple(range(n))
        while k:
            if k & 1: r = mul(r, p)
            p = mul(p, p); k >>= 1
        return r
    def order(p):
        k, q = 1, p
        while q != tuple(range(n)): q = mul(q, p); k += 1
        return k
    return mul, inv_, pw, order
random.seed(19); quots = []
while len(quots) < 6:
    n = random.choice([7, 8, 9]); mul, inv_, pw, order = perm_ops(n)
    x0 = tuple(random.sample(range(n), n)); x2 = tuple(random.sample(range(n), n))
    w = mul(mul(x2, pw(x0, 2)), x2); o = order(w)
    if o % 3 == 0: continue
    x1 = pw(w, pow(3, -1, o)); assert pw(x1, 3) == w
    quots.append((n, x0, x1, x2, mul, inv_, pw))
def violates(Z, q):
    n, x0, x1, x2, mul, inv_, pw = q
    def ev(word, P, Q):
        r = tuple(range(n))
        for ch in word: r = mul(r, {"p": P, "P": inv_(P), "q": Q, "Q": inv_(Q)}[ch])
        return r
    lhs = mul(mul(ev(Z, x0, x1), mul(inv_(x2), inv_(x0))), inv_(ev(Z, x1, x2)))
    return lhs != mul(x2, x0)
def words(L):
    def rec(pref, a, b):
        if len(pref) == L:
            if (a, b) == (-6, 6): yield pref
            return
        rem = L - len(pref)
        if abs(a + 6) + abs(b - 6) > rem: return
        for ch, da, db in (("p", 1, 0), ("P", -1, 0), ("q", 0, 1), ("Q", 0, -1)):
            if pref and pref[-1] == ch.swapcase(): continue
            yield from rec(pref + ch, a + da, b + db)
    yield from rec("", 0, 0)
for L in (12, 14):
    tot = surv = 0
    for Z in words(L):
        tot += 1
        if not any(violates(Z, q) for q in quots): surv += 1
    print(f"length {L}: {tot} words, not excluded by my {len(quots)} random quotients: {surv}")
