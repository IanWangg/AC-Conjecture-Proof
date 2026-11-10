#!/usr/bin/env python3
"""TH20 checks for TH11 (uses TH11's th11_nil.KJ for the nilpotent invariants -- NOT independent for
the definition of (kappa,J) -- and my own exact holonomy invariant tau from th20_theta_holonomy.py).
(1) closed forms T4 against th11_nil.KJ on n in [-40,60], s in [-40,40] (>= 5 points per class mod 4);
(2) Jhat := J - kappa is theta0-invariant and kappa flips, on 250 random words + twisted-conjugacy invariance;
(3) Diophantine part of T5: all (n,s) with Jhat(k_n) = Jhat(x^s y), kappa equal, |n| <= 2000 (Runge bound: -18..30);
(4) T6: all pairs n<m<=3000 with Jhat(k_n) = Jhat(k_m); exact tau to separate the survivors."""
import sys, random
sys.dont_write_bytecode = True
sys.argv = [sys.argv[0], "1", "1"]
import th20_theta_holonomy as H
import th11_nil as T
from math import comb, isqrt
def C(n, k):   # generalized binomial, integer n
    num = 1
    for i in range(k): num *= (n - i)
    f = 1
    for i in range(2, k + 1): f *= i
    assert num % f == 0
    return num // f
Jk = lambda n: -(n * (n + 1) * (n * n - 11 * n + 22)) // 24
Js = lambda s: -C(s + 1, 4)
kk = lambda n: C(n + 1, 2) % 2
for n in range(-40, 61):          # fast series version of TH11 (KJ_ser), cross-checked with KJ for |n| <= 6
    k, J = T.KJ_ser(T.ser_killer(n)); assert (k, J - k) == (kk(n), Jk(n)), n
    if abs(n) <= 6: assert T.KJ(T.killer(n)) == (k, J)
for s in range(-40, 41):
    k, J = T.KJ_ser(T.ser_pow(T._MA, s)); assert (k, J - k) == (kk(s), Js(s)), s
    if abs(s) <= 6: assert T.KJ(T.power("a", s)) == (k, J)
print("(1) closed forms kappa, Jhat = J - kappa agree with th11_nil.KJ for n in [-40,60], s in [-40,40]")
rnd = random.Random(2026)
for _ in range(250):
    u = T.red("".join(rnd.choice("aAbB") for _ in range(rnd.randint(0, 12))))
    v = T.red("".join(rnd.choice("aAbB") for _ in range(rnd.randint(1, 7))))
    k, J = T.KJ(u); assert T.KJ(T.tw(v, u)) == (k, J)
    k2, J2 = T.KJ(T.theta(u)); assert k2 == 1 - k and J2 - k2 == J - k, (u, k, J, k2, J2)
print("(2) 250 random words: (kappa,J) twisted-conjugacy invariant; theta0 flips kappa and preserves Jhat")
sol = []
for n in range(-2000, 2001):
    # Jhat(k_n) = Jhat(x^s y)  <=>  (s^2-s-1)^2 = n^4-10n^3+11n^2+22n+1
    R = n**4 - 10 * n**3 + 11 * n * n + 22 * n + 1
    if R < 0: continue
    w = isqrt(R)
    if w * w != R: continue
    for ww in (w, -w):               # s^2 - s - 1 = ww
        D = 5 + 4 * ww
        if D >= 0 and isqrt(D) ** 2 == D:
            for s in {(1 + isqrt(D)) // 2, (1 - isqrt(D)) // 2}:
                if s * s - s - 1 == ww and kk(s) == kk(n): sol.append((n, s))
print("(3) (n,s) with equal (kappa,Jhat), |n| <= 2000:", sorted(set(sol)))
tauk = lambda n: H.tau(H.W(("a", n), ("b", -1), ("a", -1), ("b", n), ("a", -1)))
taus = lambda s: {H.tau(H.W(("a", s), ("b", s))), H.tau(H.mm(H.mpow(H.B, s), H.mpow(H.BiA, s)))}
print("    tau(k_9^2) in tau-set of x^5 y:", tauk(9) in taus(5))
seen = {}; pairs = []
for n in range(1, 3001): seen.setdefault(Jk(n), []).append(n)
for J, L in seen.items():
    for i in range(len(L)):
        for j in range(i + 1, len(L)): pairs.append((L[i], L[j], "same kappa" if kk(L[i]) == kk(L[j]) else "kappa differs"))
print("(4) pairs n<m<=3000 with Jhat(k_n)=Jhat(k_m):", pairs)
for n, m, _ in pairs: print("    tau(k_%d^2) == tau(k_%d^2): %s" % (n, m, tauk(n) == tauk(m)))
