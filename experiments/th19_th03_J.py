"""TH19: exact re-check of TH03 Prop. T6 (rational point p = 2 of the phi^2-fixed character curve)."""
from fractions import Fraction as Fr
def mm(M, N): return ((M[0][0]*N[0][0]+M[0][1]*N[1][0], M[0][0]*N[0][1]+M[0][1]*N[1][1]),
                      (M[1][0]*N[0][0]+M[1][1]*N[1][0], M[1][0]*N[0][1]+M[1][1]*N[1][1]))
def det(M): return M[0][0]*M[1][1]-M[0][1]*M[1][0]
def inv(M): d = det(M); return ((M[1][1]/d, -M[0][1]/d), (-M[1][0]/d, M[0][0]/d))
def pw(M, n):
    if n < 0: M, n = inv(M), -n
    R = ((Fr(1), Fr(0)), (Fr(0), Fr(1)))
    for _ in range(n): R = mm(R, M)
    return R
A = ((Fr(5, 3), Fr(-1)), (Fr(1), Fr(0))); B = ((Fr(2), Fr(0)), (Fr(5, 6), Fr(1, 2)))
T = ((Fr(12, 19), Fr(-3, 19)), (Fr(-14, 19), Fr(1)))
Ai, Bi = inv(A), inv(B)
assert det(A) == 1 and det(B) == 1 and det(T) == Fr(186, 361)
assert mm(T, A) == mm(mm(Bi, A), T) and mm(T, B) == mm(mm(Ai, mm(B, B)), T), "intertwiner relations of H"
def J(M): M = mm(M, T); t = M[0][0]+M[1][1]; return t*t/det(T)
def Jx(s): return J(mm(pw(A, s), pw(B, s)))                                   # (x^s y)^2 = (a^s b^s, 2)
def Jk(n): return J(mm(mm(pw(A, n), mm(Bi, Ai)), mm(pw(B, n), Ai)))           # k_n^2 = (a^n B A b^n A, 2)
print("J(k_1), J(k_2), J(x^-2 y), J(x^3 y):", Jk(1), Jk(2), Jx(-2), Jx(3))
print("J(k_4) =", Jk(4), " J(x^5 y) =", Jx(5), " J(x^-4 y) =", Jx(-4))
print("J(k_5) =", Jk(5), " J(x^6 y) =", Jx(6), " J(x^-5 y) =", Jx(-5))
assert Jk(1) == Jk(2) == Jx(-2) == Fr(3751, 7776)
assert Jk(4) not in (Jx(5), Jx(-4)) and Jk(5) not in (Jx(6), Jx(-5))
print("OK")
