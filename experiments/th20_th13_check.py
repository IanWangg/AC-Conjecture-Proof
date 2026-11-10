#!/usr/bin/env python3
"""TH20 independent checks for TH13 (family AK(k;p) = (x^p Y^(p+1), W_k), W_k = (xy)^k x ((yx)^k y)^-1).
(1) phi_k/psi_k are inverse automorphisms; psi_k(x^2 Y^(2k+1)) ~ W_k (free conjugacy).
(2) duality: phi_k(x^p Y^(p+1)) ~ V_{k,p} in <x,y | x^2 = y^(2k+1)>  (own torus invariant th20_lib.torus_inv),
    V_{k,p} = (y^k x)^p y^k ((x y^k)^p x)^-1; necklace has t-exponents (k+1)^p k^(p+1).
(3) trivial group by coset enumeration for AK(k;p) and D(k;p) = (V_{k,p}, x^2 Y^(2k+1)), small k,p.
(4) the stored duality certificates end at (red psi_k(V_{k,p}), W_k) and start at AK(k;p)."""
import json, sys
sys.dont_write_bytecode = True
from th20_lib import red, inv, cyc, conj, aut, torus_inv, trivial, cert_info

def W(k): return red("xy" * k + "x" + inv("yx" * k + "y"))
def pw(p): return "x" * p + "Y" * (p + 1)
def V(k, p): c = "y" * k; return red((c + "x") * p + c + inv(("x" + c) * p + "x"))
def psi(k): return {"x": "x" + "xy" * k, "y": "xy"}
def phi(k): return {"x": "x" + "Y" * k, "y": "y" * k + "Xy"}
for k in range(1, 9):
    for g in "xy":
        assert aut(phi(k), aut(psi(k), g)) == g and aut(psi(k), aut(phi(k), g)) == g
    R = "xx" + "Y" * (2 * k + 1)
    assert conj(aut(psi(k), R), W(k)) and conj(aut(phi(k), W(k)), R)
    for p in range(1, 9):
        a = torus_inv(aut(phi(k), pw(p)), 2, -(2 * k + 1)); b = torus_inv(V(k, p), 2, -(2 * k + 1))
        assert a == b, (k, p)
        ts = sorted(e for g, e in a[1] if g == "y")
        assert ts == [k] * (p + 1) + [k + 1] * p and len(a[1]) == 4 * p + 2
        # not conjugate to the inverse (so the move is p_p -> psi_k(V), not its inverse)
        assert torus_inv(inv(V(k, p)), 2, -(2 * k + 1)) != a
print("(1),(2) OK for k,p <= 8: phi_k(p_p) ~ V_{k,p} in <x^2=y^(2k+1)>, necklace (k+1)^p k^(p+1)")
bad = []
for k in range(1, 5):
    for p in range(1, 6):
        t1 = trivial(pw(p), W(k)); t2 = trivial(V(k, p), "xx" + "Y" * (2 * k + 1))
        if not (t1 and t2): bad.append((k, p, t1, t2))
print("(3) coset enumeration: AK(k;p), D(k;p) trivial for k<=4, p<=5; exceptions:", bad)
for (k, p) in [(2, 2), (2, 3), (3, 3)]:
    i = cert_info("../certificates/th13_dual_k%d_p%d.json" % (k, p))
    assert i["start"] == [pw(p), W(k)], i["start"]
    assert i["target"] == [aut(psi(k), V(k, p)), W(k)], (k, p)
    print("(4) th13_dual_k%d_p%d.json: start = AK(%d;%d), target = (red psi_k(V_{k,p}), W_k), %d moves" % (k, p, k, p, i["moves"]))
for name, st in [("th13_ak_2_2_trivialization", ["xxYYY", W(2)]), ("th13_ak_2_1_trivialization", ["xYY", W(2)]), ("th13_ak_3_1_trivialization", ["xYY", W(3)])]:
    i = cert_info("../certificates/%s.json" % name); assert i["start"] == st and i["target"] == ["x", "y"]
    print("(4) %s: start %s -> (x,y), %d moves" % (name, st, i["moves"]))
