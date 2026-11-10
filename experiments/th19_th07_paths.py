"""TH19 check of TH07 Cor. C1/C2 (free-word identities only): w_n is a rotation of U1(n-1,0) and conjugate to p_n^-+1 in B;
triangles (w_n, d_n, e_n), (w_n, a_n, d_n), (d_n, a_n, c) in the sense 't is the cyclic reduction of a product of
rotations of r^+-1 and s^+-1'; lengths; S_3 versus D/E's second length-13 pair."""
import sys
sys.path.insert(0, "experiments")
from th19_lib import *
def triangle(r, s, t):
    T = canon(t)
    return any(canon(a + b_) == T for a in orb(r) for b_ in orb(s))
for n in range(3, 9):
    p = "x"*n + "Y"*(n+1); b = "xyxYXY"; c = "xyxYYXy"
    w = "x"*n + "y" + "X"*(n+1) + "Y"; e = "x"*(n-1) + "yyXY"; d = "x"*n + "YXyy"; a = "x"*n + "yXYXy"
    U1 = "Y" + "x"*(n-1) + "x" + "y" + "X"*n + "X"      # U1(n-1,0) = Y x^n y X^(n+1)
    r = dict(w_rot_U1=canon(w) == canon(U1), w_in_Cn=conj_in_B(w, p) or conj_in_B(w, inv(p)),
             tri_w_d_e=triangle(w, e, d), tri_w_a_d=triangle(w, a, d), tri_d_a_c=triangle(d, a, c),
             lens=(len(p)+len(b), len(w)+len(b), len(w)+len(e), len(d)+len(e), len(d)+len(c)))
    print(f"n={n}:", r, "expected lens", (2*n+7, 2*n+9, 3*n+6, 2*n+7, n+11))
S3 = ("xxxYXyy", "xxyyXY"); Q = ("xxyXYY", "xxxYYXy")
img = [canon(subst(wd, {"x": "X", "y": "y"})) for wd in S3]
print("S_3 under x->X equals D/E's pair Q up to rotation/inversion and order:", sorted(img) == sorted(canon(q) for q in Q))
# ---- Cor. C3 (balanced chain): K's triangles with hub w_n, and the stated lengths
okc = True
for n in range(3, 11):
    w = "x"*n + "y" + "X"*(n+1) + "Y"; d = "x"*n + "YXyy"; e = "x"*(n-1) + "yyXY"
    a = lambda m: "x"*m + "yXYXy"; bm = lambda m: "x"*n + "YXy" + "X"*(n-m) + "y"; cm = lambda m: "x"*(n-1) + "y" + "X"*(n-m) + "yXY"
    assert canon(bm(n)) == canon(d) and canon(cm(n)) == canon(e)
    for m in range(1, n+1):
        t1 = triangle(w, a(m), bm(m)); t2 = triangle(w, bm(m), cm(m)); t3 = (m == n) or triangle(w, cm(m), a(m+1))
        L = (len(w)+len(a(m)) == 2*n+8+m, len(bm(m))+len(a(m)) == 2*n+9, len(bm(m))+len(cm(m)) == 4*n+7-2*m)
        okc = okc and t1 and t2 and t3 and all(L)
print("Cor. C3: triangles (w,a_m,b_m), (w,b_m,c_m), (w,c_m,a_{m+1}) and the stated lengths, 3 <= n <= 10, 1 <= m <= n:", okc)
# ---- Cor. C5/C6 (frames theta_m: x -> x, y -> x^(m-1) y; staircase X_m = (g_m, v_m))
okf = True
for n in range(3, 10):
    w = "x"*n + "y" + "X"*(n+1) + "Y"; p = "x"*n + "Y"*(n+1); beta = "yxyXYX"
    U = "x" + "Y" + "x"*(n-2) + "Y" + "X" + "y" + "X"*(n-1) + "y"            # U2(n-2,1)
    okf = okf and (conj_in_B(U, p) or conj_in_B(U, inv(p)))
    for m in range(1, n):
        th = {"x": "x", "y": "x"*(m-1) + "y"}
        g = "x" + "Y" + "x"*(n-1-m) + "Y" + "X" + "y" + "X"*(n-m) + "y"
        v = "y" + "x"*m + "yXYX"
        okf = okf and canon(subst(w, th)) == canon(w) and canon(subst(beta, th)) == canon(v) \
                  and canon(subst(U, th)) == canon(g) and len(cyc(g)) == 2*n+5-2*m and len(g) + len(v) == 2*n+10-m
    okf = okf and canon("x" + "YY" + "XyXy") == canon("XyXyxYY")              # g_{n-1} = f
print("Cor. C5/C6: theta_m(w_n) ~ w_n, theta_m(beta) ~ v_m, theta_m(U2(n-2,1)) ~ g_m with the stated lengths, U2(n-2,1) in C_n; 3 <= n <= 9:", okf)
