"""TH19 check of TH09 Theorem 6 (Gieseking side): with O's witness hom rho: H -> PSL(2,13),
|tr rho(v^2)| for the BS(1,2)-type killers v_j^+ = v(x, x^j y), v_j^- = v(X, x^j y) of G_c = <x,y | xyxYYXy>
versus |tr rho(k_n^2)|.  Own normal form: G_c = F(a,b) x|_phi Z, a = x, b = yxY, phi(a) = b, phi(b) = b^-1 a."""
import sys
sys.path.insert(0, "experiments")
from th19_lib import red, inv, cyc
p = 13
PHI = {"a": "b", "b": "Ba"}; PHII = {"a": "ab", "b": "a"}
def app(u, img):
    full = {"a": img["a"], "b": img["b"], "A": inv(img["a"]).translate(str.maketrans("xXyY", "xXyY")), "B": inv(img["b"])}
    return "".join(full[c] for c in u)
def fred(u):  # free reduction on a,b,A,B
    out = []
    for c in u:
        if out and out[-1] == c.swapcase(): out.pop()
        else: out.append(c)
    return "".join(out)
def phik(u, k):
    for _ in range(abs(k)): u = fred(app(u, PHI if k > 0 else PHII))
    return u
def nf(w):
    u, k = "", 0
    for ch in w:
        if ch == "x": u = fred(u + phik("a", k))
        elif ch == "X": u = fred(u + phik("A", k))
        elif ch == "y": k += 1
        else: k -= 1
    return u, k
assert nf("xyxYYXy") == ("", 0), "c must be trivial in G_c"
assert nf("xxxYXyy") == ("aaaBA", 1)
def mm(M, N): return ((M[0]*N[0]+M[1]*N[2]) % p, (M[0]*N[1]+M[1]*N[3]) % p, (M[2]*N[0]+M[3]*N[2]) % p, (M[2]*N[1]+M[3]*N[3]) % p)
def minv(M): return (M[3], (-M[1]) % p, (-M[2]) % p, M[0])
RA, RB, RT = (0, 2, 6, 8), (1, 11, 6, 2), (0, 1, 12, 5)
G = {"a": RA, "b": RB, "A": minv(RA), "B": minv(RB)}
def rho(u):
    R = (1, 0, 0, 1)
    for c in u: R = mm(R, G[c])
    return R
# relations of H: t a t^-1 = b^-1 a, t b t^-1 = a^-1 b^2 (up to sign)
sgn = lambda M: {M, tuple((-e) % p for e in M)}
assert mm(mm(RT, RA), minv(RT)) in sgn(rho("Ba")) and mm(mm(RT, RB), minv(RT)) in sgn(rho("Abb"))
def sqtrace(w):
    u, k = nf(w)
    assert abs(k) == 1
    if k == 1: M = mm(rho(fred(u + phik(u, 1))), RT)            # (u,1)^2 = (u phi(u), 2)
    else:      M = mm(rho(fred(u + phik(u, -1))), minv(RT))      # (u,-1)^2 = (u phi^-1(u), -2)
    t = (M[0] + M[3]) % p
    return min(t, p - t)
def v(P, Q): return cyc(inv(P) + Q + P + inv(Q) + inv(Q))
xj = lambda j: "x"*j if j >= 0 else "X"*(-j)
plus = [sqtrace(v("x", red(xj(j) + "y"))) for j in range(0, 14)]
minus = [sqtrace(v("X", red(xj(j) + "y"))) for j in range(0, 14)]
print("|tr| of v_j^+ squared, j=0..13:", plus)
print("|tr| of v_j^- squared, j=0..13:", minus)
kn = {n: sqtrace("x"*n + "YXyy") for n in range(1, 9)}
print("|tr| of k_n squared, n=1..8:", kn)
cand = set(plus) | set(minus)
print("n in 1..8 excluded by this single hom (trace not among the candidates):", [n for n in kn if kn[n] not in cand])
assert plus[:7] == plus[7:] and minus[:7] == minus[7:]
