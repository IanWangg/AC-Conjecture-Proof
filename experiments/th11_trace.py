#!/usr/bin/env python3
"""TH11: exact holonomy traces for H = F(a,b) x| <t>, t = y^2 (index 2 in G_c), in Q(w), w^2+w+1=0.
rho(a)=A, rho(b)=B, rho(t)=T (explicit matrices, taken from the coordinator's fig8_check.py and
re-verified here: det = 1,  T A = B^-1 A T,  T B = A^-1 B^2 T, i.e. the two relations of H).
For a degree-1 element g = (u,1) of G_c, g^2 = (u phi(u), 2) = u phi(u) t and
     N(g) := tr( rho(u phi(u)) T )      (an H-conjugacy invariant of g^2).
If g ~ g' in G_c then N(g) = N(g') or N(g) = N(y g' y^-1) (research-o 6).
Usage: python3 experiments/th11_trace.py --selftest
"""
import sys
from fractions import Fraction as Fr

class W:                                   # p + q w
    __slots__ = ("p", "q")
    def __init__(s, p=0, q=0): s.p, s.q = Fr(p), Fr(q)
    def __add__(s, o): return W(s.p + o.p, s.q + o.q)
    def __sub__(s, o): return W(s.p - o.p, s.q - o.q)
    def __mul__(s, o): return W(s.p * o.p - s.q * o.q, s.p * o.q + s.q * o.p - s.q * o.q)
    def __eq__(s, o): return s.p == o.p and s.q == o.q
    def __repr__(s): return f"{s.p}" if s.q == 0 else f"({s.p}+{s.q}w)"
def mm(M, N):
    return tuple(tuple(M[i][0] * N[0][j] + M[i][1] * N[1][j] for j in range(2)) for i in range(2))
def adj(M): return ((M[1][1], W(0) - M[0][1]), (W(0) - M[1][0], M[0][0]))
def det(M): return M[0][0] * M[1][1] - M[0][1] * M[1][0]
def tr(M): return M[0][0] + M[1][1]
th = Fr(1, 3)
A = ((W(0, -1), W(-th, -2 * th)), (W(1, -1), W(1)))
B = ((W(2, 2), W(-th, th)), (W(-2, -1), W(0, -1)))
T = ((W(1), W(0)), (W(-1, 1), W(1)))
Ai, Bi = adj(A), adj(B)
I2 = ((W(1), W(0)), (W(0), W(1)))
MAT = {"a": A, "A": Ai, "b": B, "B": Bi}

def red(w):
    out = []
    for ch in w:
        if out and out[-1] == ch.swapcase(): out.pop()
        else: out.append(ch)
    return "".join(out)
def inv(w): return w.swapcase()[::-1]
PHI = {"a": "b", "b": "Ba"}
def phi(u): return red("".join(PHI[ch] if ch.islower() else inv(PHI[ch.lower()]) for ch in u))
def power(w, n): return w * n if n >= 0 else inv(w) * (-n)
def rho(u):
    R = I2
    for ch in u: R = mm(R, MAT[ch])
    return R
def N(u):
    """signed trace of rho(g^2), g = (u,1)."""
    return tr(mm(rho(red(u + phi(u))), T))
def killer(n): return power("a", n) + "BA"
def theta(u): return red("".join({"a": "A", "A": "a", "b": "B", "B": "b"}[ch] for ch in u) + "b")
def as_int(z):
    assert z.q == 0 and z.p.denominator == 1, z
    return int(z.p)

def selftest():
    assert det(A) == W(1) and det(B) == W(1) and det(T) == W(1)
    assert mm(T, A) == mm(mm(Bi, A), T) and mm(T, B) == mm(mm(Ai, mm(B, B)), T)   # relations of H
    assert tr(A) == W(1, -1) and tr(B) == W(2, 1)
    e = {n: as_int(N(killer(n))) for n in range(-9, 15)}
    d = {s: as_int(N(power("a", s))) for s in range(-14, 16)}
    print("N(k_n),  n=-3..12:", [e[n] for n in range(-3, 13)])
    print("N(x^s y), s=-3..12:", [d[s] for s in range(-3, 13)])
    # conjugation by y and theta0 do not change N on these elements
    for n in range(-4, 10):
        u = killer(n)
        assert N(phi(u)) == N(u) and N(theta(u)) == N(u)
        assert N(phi(power("a", n))) == N(power("a", n))
    # (9,5): the only pair left open by (kappa, J-hat)
    assert e[9] == 16562 and d[5] == 74 and as_int(N(phi(power("a", 5)))) == 74
    print("k_9 vs x^5 y: N =", e[9], "vs", d[5], "-> not conjugate in G_c")
    # (6,7): k_6 vs theta0(k_7), k_7 vs theta0(k_6)
    for n, m in ((6, 7), (7, 6)):
        up = theta(killer(m))
        assert e[n] not in (as_int(N(up)), as_int(N(phi(up))))
    print("k_6 vs theta0(k_7), k_7 vs theta0(k_6): N =", e[6], "vs", e[7], "-> not conjugate in G_c")
    # reflection identity  N(k_n) + N(k_{4-n}) = N(x^{n+1}y) + N(x^{n-4}y)   (signed traces)
    for n in range(-9, 14):
        if -9 <= 4 - n <= 14: assert e[n] + e[4 - n] == d[n + 1] + d[n - 4], n
    assert all(d[s] == d[1 - s] for s in range(-13, 15))
    print("identity N(k_n)+N(k_{4-n}) = N(x^{n+1}y)+N(x^{n-4}y) verified for n = -9..13; N(x^s y) = N(x^{1-s} y)")
    print("coincidences N(k_n) = N(x^s y), 1<=n<=14, |s|<=14:",
          [(n, s) for n in range(1, 15) for s in range(-14, 16) if e[n] == d[s]])
    print("th11_trace self-test passed")

if __name__ == "__main__":
    selftest()
