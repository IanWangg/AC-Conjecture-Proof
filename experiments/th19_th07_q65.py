"""TH19 cross-note check: TH07 §6.5 asks whether kappa_n = xYxyX^(n-1)y (killer of the mirror image of F_n) is conjugate to
k_n = x^n YXyy in G_c = <x,y | xyxYYXy>.  TH03's mod-2 invariant eps (Thm T16, verified in th19_th03_mirror.py) is a
conjugacy invariant of degree-1 elements; here eps(kappa_n) = eps(k_n) + 1 for all n (by the closed form
eps(kappa_n) = C(4-n,2) + 1, eps(k_n) = C(n+1,2), difference 4n-6+1), so kappa_n is never conjugate to k_n.
Both words have y-exponent 1, so kappa_n is not conjugate to k_n^-1 either."""
import sys, io, contextlib
sys.path.insert(0, "experiments")
with contextlib.redirect_stdout(io.StringIO()):
    import th19_th03_t14 as T
    import th19_th03_mirror as Mi
res = []
for n in range(1, 21):
    kap, kn = "xYxy" + "X"*(n-1) + "y", "x"*n + "YXyy"
    (u, d), (v, e) = T.nf(kap), T.nf(kn)
    assert d == e == 1
    res.append(Mi.eps(u) != Mi.eps(v))
    assert Mi.eps(u) == ((4-n)*(3-n)//2 + 1) % 2 and Mi.eps(v) == ((n+1)*n//2) % 2
print("eps(kappa_n) != eps(k_n) for n = 1..20:", all(res), "; closed forms confirmed")
