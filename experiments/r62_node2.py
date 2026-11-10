#!/usr/bin/env python3
"""Agent R6-2: P2's own tuple (r2, k) = (XyyxYYY, XXXYxxY).  Find an automorphism beta of F2
with beta(k) cyclically equal to c^{+-1} or w0^{+-1} (w0 = xxyyXY = alpha(c)) by BFS (cap 13,
elementary Nielsen automorphisms), then decide beta(r2) ~ x^s y in G_c with TH03's invariants."""
import os, sys
from collections import deque
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import th03_uniform as t, th03_two as q2
red, inv = t.red, t.inv
def cyc(w):
    w = red(w)
    while len(w) > 1 and w[0] == w[-1].swapcase(): w = w[1:-1]
    return w
def canon(w):
    w = cyc(w); rots = [w[i:] + w[:i] for i in range(len(w))]; wi = inv(w)
    return min(rots + [wi[i:] + wi[:i] for i in range(len(wi))])
def aut(img, w): return red("".join(img[ch] if ch.islower() else inv(img[ch.lower()]) for ch in w))
def compose(f, g):            # (f then g): x -> g(f(x))
    return {k: aut(g, v) for k, v in f.items()}
GENS = [{'x': 'xy', 'y': 'y'}, {'x': 'yx', 'y': 'y'}, {'x': 'xY', 'y': 'y'}, {'x': 'Yx', 'y': 'y'},
        {'x': 'x', 'y': 'yx'}, {'x': 'x', 'y': 'xy'}, {'x': 'x', 'y': 'yX'}, {'x': 'x', 'y': 'Xy'},
        {'x': 'X', 'y': 'y'}, {'x': 'x', 'y': 'Y'}, {'x': 'y', 'y': 'x'}]
def find(src, goal, cap=13):
    start = canon(src); seen = {start: {'x': 'x', 'y': 'y'}}; dq = deque([start])
    goals = {canon(goal), canon("xxyyXY")}
    while dq:
        w = dq.popleft()
        if w in goals: return seen[w]
        for g in GENS:
            v = canon(aut(g, w))
            if len(v) <= cap and v not in seen:
                seen[v] = compose(seen[w], g); dq.append(v)
    return None
if __name__ == "__main__":
    R2, K, C = 'XyyxYYY', 'XXXYxxY', 'xyxYYXy'
    beta = find(K, C)
    print("beta:", beta)
    if beta:
        bk, br = aut(beta, K), aut(beta, R2)
        print("beta(k) =", bk, "canon ok:", canon(bk) == canon(C), " beta(r2) =", br)
        u, k = t.nf(br)
        if k == -1: u, k = t.nf(inv(br))
        print("nf:", (u, k))
        if abs(k) == 1:
            G4, L4 = q2.l4_setup()
            Iu = t.I(u); print("I =", Iu, "eps =", q2.eps(u), "L4 =", L4(u),
                               "sigma-match:", [s for s in range(-80, 81) if t.sigma(s) == Iu])
