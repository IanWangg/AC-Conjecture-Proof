"""TH19 checks of TH09.
(1) BS(1,2) = <x,y | x^-1 y x = y^2> (faithful affine rep y: z->z+1, x: z->z/2): every word of x-exponent +-1 is
    conjugate to x^+-1 (explicit conjugator y^v, v in Z[1/2]); so all killers are conjugates of x^+-1.
(2) Trefoil side (TH09 Prop. 4.1, Thm 4): the words v_j^+- are BS(1,2)-type; which are conjugate in B to p_n^+-1.
(3) Bounded completeness: every BS(1,2)-type word theta(XyxYY), theta in a BFS ball of Aut(F2), that is a partner of b
    has the necklace class (up to inversion) of some v_j^+-.
(4) T(n,n+1) side: no v in the ball is conjugate to b^+-1 in <x,y | x^n = y^(n+1)>, 3 <= n <= 7 (bounded)."""
import sys, random
from fractions import Fraction as Fr
sys.path.insert(0, "experiments")
from th19_lib import *
# ---------- (1)
def aff(w):   # affine map z -> m z + c as (m, c); composition of letters left to right as group product
    m, c = Fr(1), Fr(0)
    G = {"x": (Fr(1, 2), Fr(0)), "X": (Fr(2), Fr(0)), "y": (Fr(1), Fr(1)), "Y": (Fr(1), Fr(-1))}
    for ch in w:
        m2, c2 = G[ch]
        m, c = m*m2, m*c2 + c          # (m,c)*(m2,c2): z -> m(m2 z + c2) + c
    return (m, c)
assert aff("XyxYY") == (1, 0)
random.seed(1)
for _ in range(2000):
    L = random.randint(1, 14)
    w = red("".join(random.choice("xXyY") for _ in range(L)))
    e = expo(w)[0]
    if abs(e) != 1: continue
    m, c = aff(w)                       # conj by translation z->z+v: (1,v)(m,c)(1,-v) = (m, c + v - m v)
    v = -c / (1 - m)                    # 1-m = 1/2 or -1: a unit of Z[1/2]
    assert v.denominator & (v.denominator - 1) == 0, "conjugator not in Z[1/2]"
    assert (m, c + v - m*v) == (m, 0) and (m, Fr(0)) == aff("x" if e == 1 else "X")
print("(1) BS(1,2): every sampled word of x-exponent +-1 is conjugate to x^+-1 by a translation in Z[1/2]")
# ---------- (2)
def v(P, Q): return cyc(inv(P) + Q + P + inv(Q) + inv(Q))
def vplus(j):  return cyc("yxYX" + "yX"*j + "X") if j >= 0 else cyc("yxYY" + "xY"*(-j-1) + "X")
def vminus(j): return cyc("YxyXX" + "yX"*j) if j >= 0 else cyc("YxyXY" + "xY"*(-j-1))
P = "xY"
for j in range(-40, 41):
    Q = red(P*j + "x") if j >= 0 else red(inv(P)*(-j) + "x")
    assert canon(v(P, Q)) == canon(vplus(j)) and canon(v(inv(P), Q)) == canon(vminus(j)), j
fam = {}
for j in range(-40, 41):
    for name, w in (("+", vplus(j)), ("-", vminus(j))):
        for u in (w, inv(w)):
            fam.setdefault((sum(expo(u)), c2c3_necklace(u)), []).append((j, name))
hits = {}
for n in range(1, 13):
    p = "x"*n + "Y"*(n+1)
    for u in (p, inv(p)):
        k = (sum(expo(u)), c2c3_necklace(u))
        if k in fam: hits[n] = sorted(set(fam[k]))
print("(2) n <= 12 with some v_j^+- (|j| <= 40) conjugate in B to p_n^+-1:", hits)
assert conj_in_B("yxYXyXX", "xxYYY") or conj_in_B("yxYXyXX", inv("xxYYY"))
# ---------- (3),(4)
gens = [{"x": "xy", "y": "y"}, {"x": "xY", "y": "y"}, {"x": "x", "y": "yx"}, {"x": "x", "y": "yX"},
        {"x": "y", "y": "x"}, {"x": "X", "y": "y"}]
ball = {("x", "y")}; frontier = [("x", "y")]
for depth in range(7):
    nxt = []
    for (a, b) in frontier:
        for g in gens:
            img = (subst(g["x"], {"x": a, "y": b}), subst(g["y"], {"x": a, "y": b}))
            if img not in ball and len(img[0]) + len(img[1]) <= 40:
                ball.add(img); nxt.append(img)
    frontier = nxt
words = {canon(subst("XyxYY", {"x": a, "y": b})) for (a, b) in ball}
partners = [w for w in words if abs(sum(expo(w))) == 1]
miss = [w for w in partners if (sum(expo(w)), c2c3_necklace(w)) not in fam]
print(f"(3) ball: {len(ball)} automorphisms, {len(words)} BS(1,2)-type cyclic words, {len(partners)} partners of b;"
      f" not in the family v_j^+- (|j|<=40): {len(miss)}", [m for m in miss if len(m) <= 40][:3])
def neck(w, p, q):
    s = []
    for ch in w:
        g = "s" if ch in "xX" else "t"; m = p if g == "s" else q; e = 1 if ch in "xy" else m - 1
        if s and s[-1][0] == g:
            e2 = (s[-1][1] + e) % m; s.pop()
            if e2: s.append((g, e2))
        else: s.append((g, e))
    while len(s) >= 2 and s[0][0] == s[-1][0]:
        g = s[0][0]; m = p if g == "s" else q; e = (s[0][1] + s[-1][1]) % m; s = s[1:-1]
        if e: s = [(g, e)] + s
    return min(tuple(s[i:] + s[:i]) for i in range(len(s))) if s else ()
b = "xyxYXY"
for n in range(2, 8):
    key = lambda w: ((n+1)*expo(w)[0] + n*expo(w)[1], neck(w, n, n+1))
    tgt = {key(b), key(inv(b))}
    h = [w for w in words if key(w) in tgt]
    print(f"(4) n={n}: BS(1,2)-type words in the ball conjugate to b^+-1 in <x,y|x^n=y^(n+1)>: {len(h)}", h[:2])
