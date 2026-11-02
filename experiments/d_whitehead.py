#!/usr/bin/env python3
"""Independent (Python, stdlib) Whitehead canonical form of a pair of cyclic
words in F(x,y) up to Aut(F2), used to cross-check d_acsearch --autmatch.

Rank-2 Whitehead automorphisms act on conjugacy classes, up to inner
automorphisms, as x->xy, x->xY, y->yx, y->yX (type II) and the 8 signed
permutations (type I).  Whitehead's theorem for tuples of cyclic words: a
non-minimal tuple is shortened by a type-II map, and the minimal tuples of an
orbit form one class under type-I/II maps through minimal tuples (peak
reduction).  The canonical form is the least Sigma-canonical pair over that
set (Sigma = rotations, inversions, relator swap).

Usage: python3 experiments/d_whitehead.py w1 w2 [w1' w2' ...]
       python3 experiments/d_whitehead.py --self-test
"""
import random
import sys

INV = {"x": "X", "X": "x", "y": "Y", "Y": "y"}
MAPS = [{"x": "xy", "X": "YX"}, {"x": "xY", "X": "yX"},
        {"y": "yx", "Y": "XY"}, {"y": "yX", "Y": "xY"}]


def cycred(w):
    out = []
    for c in w:
        if out and out[-1] == INV[c]:
            out.pop()
        else:
            out.append(c)
    w = "".join(out)
    while len(w) >= 2 and w[0] == INV[w[-1]]:
        w = w[1:-1]
    return w


def inverse(w):
    return "".join(INV[c] for c in reversed(w))


def canon_word(w):
    return min(u[k:] + u[:k] for u in (w, inverse(w)) for k in range(len(w)))


def canon_pair(p):
    return tuple(sorted(canon_word(w) for w in p))


def apply(m, p):
    return tuple(cycred("".join(m.get(c, c) for c in w)) for w in p)


def signed_perms(p):
    out = []
    for swap in (False, True):
        for sx in (False, True):
            for sy in (False, True):
                t = {}
                for c in "xXyY":
                    base = c.lower()
                    if swap:
                        base = "y" if base == "x" else "x"
                    neg = c.isupper() ^ (sx if base == "x" else sy)
                    t[c] = base.upper() if neg else base
                out.append(tuple("".join(t[c] for c in w) for w in p))
    return out


def aut_canon(p):
    p = tuple(cycred(w) for w in p)
    improved = True
    while improved:
        improved = False
        for m in MAPS:
            q = apply(m, p)
            if all(q) and sum(map(len, q)) < sum(map(len, p)):
                p, improved = q, True
                break
    L = sum(map(len, p))
    seen = {canon_pair(p)}
    stack = [p]
    while stack:
        cur = stack.pop()
        for m in MAPS:
            q = apply(m, cur)
            if all(q) and sum(map(len, q)) == L:
                c = canon_pair(q)
                if c not in seen:
                    seen.add(c)
                    stack.append(q)
            assert not (all(q) and sum(map(len, q)) < L), "not minimal"
    best = min(canon_pair(g) for s in seen for g in signed_perms(s))
    return L, best


def selftest():
    rng = random.Random(7)
    L, c = aut_canon(("x", "y"))
    assert L == 2
    a = aut_canon(("xxxYYYY", "xyxYXY"))
    assert a[0] == 13
    n = 0
    for _ in range(300):
        p = tuple(cycred("".join(rng.choice("xXyY") for _ in range(rng.randint(2, 7)))) for _ in range(2))
        if not all(p):
            continue
        q = rng.choice(signed_perms(p))
        for _ in range(3):
            q = apply(rng.choice(MAPS), q)
        if not all(q):
            continue
        assert aut_canon(p) == aut_canon(q), (p, q)
        n += 1
    print(f"self-test passed: {n} random automorphism-invariance checks")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        selftest()
    else:
        args = sys.argv[1:]
        for k in range(0, len(args), 2):
            L, c = aut_canon((args[k], args[k + 1]))
            print(args[k], args[k + 1], "-> Aut-minimal length", L, "canonical", " ".join(c))
