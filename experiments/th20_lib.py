#!/usr/bin/env python3
"""TH20 referee helpers (standard library only): free-group words over x,X,y,Y (and z,Z),
automorphisms, conjugacy, pieces of a symmetrized set, coset enumeration wrapper, certificate info."""
import json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

def red(w):
    o = []
    for ch in w:
        if o and o[-1] == ch.swapcase(): o.pop()
        else: o.append(ch)
    return "".join(o)
def inv(w): return w.swapcase()[::-1]
def cyc(w):
    w = red(w)
    while len(w) > 1 and w[0] == w[-1].swapcase(): w = w[1:-1]
    return w
def conj(u, v):
    """conjugate in the free group"""
    u, v = cyc(u), cyc(v)
    return len(u) == len(v) and (u in v + v)
def conj_pm(u, v): return conj(u, v) or conj(u, inv(v))
def P(s):
    """parse 'x^3 y^-4 x y X' style or plain letters into a letter word"""
    out = []
    for tok in s.replace("*", " ").split():
        if "^" in tok:
            b, e = tok.split("^"); e = int(e)
            out.append(b * e if e >= 0 else inv(b) * (-e))
        else: out.append(tok)
    return red("".join(out))
def pw(w, e): return red(w * e) if e >= 0 else red(inv(w) * (-e))
def aut(img, w):
    """img: dict x->word, y->word; letterwise substitution, freely reduced"""
    return red("".join(img[ch] if ch.islower() else inv(img[ch.lower()]) for ch in w))
def expo(w): return (w.count("x") - w.count("X"), w.count("y") - w.count("Y"))
def toint(w): return tuple({"x": 1, "X": -1, "y": 2, "Y": -2, "z": 3, "Z": -3}[c] for c in w)
def trivial(*rels, limit=400000):
    """coset enumeration over the trivial subgroup... (index of <x> then check); returns True/False/None"""
    import f_descent
    R = [toint(red(r)) for r in rels]
    gens = sorted({abs(c) for r in R for c in r})
    idx = f_descent.coset_index(R, (1,), limit)
    if idx is None: return None
    if idx != 1: return False
    idx2 = f_descent.coset_index(R, (2,), limit) if 2 in gens else 1
    if idx2 is None: return None
    if idx2 != 1: return False
    if 3 in gens:
        idx3 = f_descent.coset_index(R, (3,), limit)
        if idx3 is None: return None
        if idx3 != 1: return False
    # all generators lie in <x>, so the group is cyclic = <x>; index of <y> is 1 so group = <y>; abelian:
    return abs_det_one(rels)
def abs_det_one(rels):
    if len(rels) != 2: return None
    (a, b), (c, d) = expo(rels[0]), expo(rels[1])
    return abs(a * d - b * c) == 1
def symmetrized(rels):
    S = set()
    for r in rels:
        r = cyc(r)
        for q in (r, inv(r)):
            for i in range(len(q)): S.add(q[i:] + q[:i])
    return S
def pieces(rels):
    """maximal common prefixes of distinct elements of the symmetrized closure; returns
    (max piece length, min relator length, dict relator-> min number of pieces needed (greedy exact))"""
    S = sorted(symmetrized(rels))
    pref = {}
    for r in S:
        for k in range(1, len(r) + 1): pref.setdefault(r[:k], set()).add(r)
    piece = {p for p, rs in pref.items() if len(rs) >= 2}
    mx = max((len(p) for p in piece), default=0)
    def minpieces(r):
        # min number of pieces whose product is the cyclic word r (try all rotations, DP on linear word)
        best = None
        for i in range(len(r)):
            q = r[i:] + r[:i]; n = len(q); INF = 10**9; d = [INF] * (n + 1); d[0] = 0
            for a in range(n):
                if d[a] < INF:
                    for b in range(a + 1, n + 1):
                        if q[a:b] in piece: d[b] = min(d[b], d[a] + 1)
                        else: break
            if d[n] < INF and (best is None or d[n] < best): best = d[n]
        return best
    return mx, min(len(r) for r in S), {r: minpieces(r) for r in {cyc(x) for x in rels}}, piece
def cert_info(path):
    import elementary_verify as ev
    c = json.load(open(path))
    r = ev.replay(c)
    return {"path": os.path.basename(path), "start": c["start"], "target": c["target"], "moves": r["moves"], "peak": r["peak_total_length"]}
if __name__ == "__main__":
    for p in sys.argv[1:]:
        try: print(json.dumps(cert_info(p)))
        except Exception as e: print("FAIL", p, repr(e))

def torus_inv(w, p, q):
    """Own implementation: complete conjugacy invariant of w in <x,y | x^p y^q> (|p|,|q|>=2):
    (central exponent of z = x^p, minimal rotation of the cyclic syllable sequence)."""
    P_, Q_ = abs(p), abs(q)
    zx = 1 if p > 0 else -1          # x^P = z^zx
    zy = -1 if q > 0 else 1          # y^Q = z^zy   (x^p y^q = 1  =>  y^q = z^-1)
    runs = []
    for ch in red(w):
        g = ch.lower(); e = 1 if ch.islower() else -1
        if runs and runs[-1][0] == g: runs[-1][1] += e
        else: runs.append([g, e])
    z = 0
    changed = True
    while changed:
        changed = False
        new = []
        for g, e in runs:
            k, r = divmod(e, P_ if g == "x" else Q_)
            if k: z += k * (zx if g == "x" else zy); changed = True
            if r == 0: changed = True; continue
            if new and new[-1][0] == g: new[-1][1] += r; changed = True
            else: new.append([g, r])
        runs = new
        if len(runs) >= 2 and runs[0][0] == runs[-1][0]:
            runs[0][1] += runs[-1][1]; runs.pop(); changed = True
    t = tuple((g, e) for g, e in runs)
    if len(t) > 1: t = min(t[i:] + t[:i] for i in range(len(t)))
    return (z, t)
