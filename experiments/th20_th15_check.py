#!/usr/bin/env python3
"""TH20 independent check of TH15's closed-form paths (words typed from TH15's formulas, checked
with my own cyclic-product test; TH15's code is not imported).
For each consecutive pair of states exactly one relator changes, and the new relator must be a
rotation of cyc(G*R) with R a rotation of the old relator^{+-1} and G a rotation of the other
relator^{+-1}  (an ordinary-AC composite).  Endpoints are compared with my own sigma, a images."""
import sys
sys.dont_write_bytecode = True
from th20_lib import red, inv, cyc, conj, aut

def rots(w): return {w[i:] + w[:i] for i in range(len(w))}
def one_product(old, other, new):
    Rs = rots(old) | rots(inv(old)); Gs = rots(other) | rots(inv(other))
    return any(conj(g + r, new) for r in Rs for g in Gs)
def chain_ok(states):
    for (a0, b0), (a1, b1) in zip(states, states[1:]):
        assert all(cyc(w) == w for w in (a1, b1))
        if b0 == b1: assert one_product(a0, b0, a1), (a0, b0, a1)
        elif a0 == a1: assert one_product(b0, a0, b1), (b0, a0, b1)
        else: raise AssertionError("both relators changed")
    return len(states) - 1
B = "xyxYXY"
def swap_states(n):
    x, X, y, Y = "x", "X", "y", "Y"
    st = [(x * n + Y * (n + 1), B)]
    for k in range(1, n + 1): st.append((y * k + "xy" + x * (n - k + 1) + Y * (n + 1) + "XYX", B))
    for j in range(1, n + 1): st.append((y * n + X * (j - 1) + "yx" + Y * (n + 1 - j) + "XYX", B))
    st.append((y * n + X * (n + 1), B))
    return st
def a_states(n):
    x, X, y, Y = "x", "X", "y", "Y"
    u = lambda k: x * (n - k) + Y * n + x + y * k + "XY" if k else x * n + Y * (n + 1)
    b1 = X + Y * (n + 1) + x + y * n
    v = lambda m: "xx" + y * (n - 1 - m) + X + Y * (n + 2) + "xY" * m if m < n - 1 else "xY" * n + Y * (n + 1)
    st = [(u(k), B) for k in range(0, n)]            # I: b frozen
    st.append((u(n - 1), b1))                         # II
    st.append((v(0), b1))                             # III
    st.append((v(0), "yxyXX"))                        # IV
    st += [(v(m), "yxyXX") for m in range(1, n)]      # V
    return st
SIG = {"x": "y", "y": "x"}; A = {"x": "xY", "y": "y"}
for n in range(2, 13):
    p = "x" * n + "Y" * (n + 1)
    s = swap_states(n); ns = chain_ok(s)
    assert conj(s[-1][0], aut(SIG, p)) and conj(inv(s[-1][1]), aut(SIG, B))
    t = a_states(n); na = chain_ok(t)
    assert conj(t[-1][0], aut(A, p)) and conj(inv(t[-1][1]), aut(A, B))
    assert ns == 2 * n + 1 and na == 2 * n + 1
    if n in (3, 5):
        print("n=%d swap chain:" % n, " -> ".join(w for w, _ in s))
        print("n=%d a chain:" % n, " -> ".join("(%s,%s)" % st for st in t))
print("TH15 closed-form chains: every step is one cyclic product, endpoints = sigma(AK(n)), a(AK(n)) up to rotation/inversion, n = 2..12")
# --- Propositions C and D of the final note (hub path and C's bridge), words typed from the note
def hub_states(n):
    x, X, y, Y = "x", "X", "y", "Y"
    u = lambda k: x * (n - k) + Y * n + x + y * k + "XY" if k else x * n + Y * (n + 1)
    beta = X + Y * (n + 1) + x + y * n
    st = [(u(k), B) for k in range(0, n)] + [(beta, B)]
    st += [(beta, x + y * (n + 1) + x + "YX" + Y * (n + 2)), (beta, "xx" + y * (n - 1) + X + Y * (n + 2)), (beta, "xxYXY")]
    return st
def bridge_states(n):
    x, X, y, Y = "x", "X", "y", "Y"
    f = lambda k: red(x * k + "YX" + y * (n - k) + x + Y * n)
    betap = X + y * n + x + Y * (n + 1)
    st = [(cyc(f(k)), B) for k in range(n, 0, -1)] + [(betap, B)]
    st += [(betap, x + Y * n + x + "YX" + y * (n - 1)), (betap, "xx" + Y * (n + 2) + X + y * (n - 1)), (betap, "XYxxY")]
    return st
for n in range(2, 11):
    h = hub_states(n); assert chain_ok(h) == n + 3
    d = bridge_states(n); assert chain_ok(d) == n + 3 and conj(d[n][0], "X" + "y" * n + "x" + "Y" * (n + 1))
print("TH15 Prop. C (AK(n) -> H_n = (XY^(n+1)xy^n, xxYXY)) and Prop. D (AK(n) -> M_n = (Xy^nxY^(n+1), XYxxY)): n+3 cyclic products each, n = 2..10")
