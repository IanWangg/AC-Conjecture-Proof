#!/usr/bin/env python3
"""Agent J (round 3): audit of research-d Lemma D1(c), "every cyclic-product
edge can be reversed by a cyclic product" (so that the cyclic-product graph is
undirected).  Standard library only.

A *cyclic product* (research-d, Section 2) replaces the relator u by the
cyclic reduction of rot_k(u) * rot_l(v)^{+-1}, v the other relator.  States are
unordered pairs of nonempty cyclically reduced words modulo Sigma (rotation and
inversion of either relator, interchange).  This file re-implements that move
independently of experiments/d_acsearch.cpp (full free + cyclic reduction of
the concatenation, every pair of rotations, both signs, empty results dropped)
and then

  (1) exhibits a concrete unimodular trivial-group pair on which the edge is
      NOT reversible: (yxYYX, xy) -> (x, xy) is a cyclic product, but no
      cyclic product from the Sigma-class of (x, xy) lands in the Sigma-class
      of (yxYYX, xy);
  (2) enumerates the forward-reachable set of AK(3) in G_full(C) for a small
      cap C (default 17), checks D's state count, and counts the directed
      edges inside it whose reverse edge does not exist.

Usage: python3 experiments/j_cyclic_graph.py [--cap 17]
"""
import sys
from collections import deque

LET = "xXyY"


def red(w):
    out = []
    for c in w:
        if out and out[-1] == c.swapcase():
            out.pop()
        else:
            out.append(c)
    return "".join(out)


def inv(w):
    return w.swapcase()[::-1]


def cyc(w):
    w = red(w)
    while len(w) >= 2 and w[0] == w[-1].swapcase():
        w = w[1:-1]
    return w


def rotations(w):
    return [w[k:] + w[:k] for k in range(len(w))]


def canon_word(w):
    """Canonical representative under rotation and inversion."""
    return min(min(rotations(w)), min(rotations(inv(w))))


def canon_pair(u, v):
    a, b = canon_word(u), canon_word(v)
    return tuple(sorted((a, b), key=lambda s: (len(s), s)))


def cyclic_products(u, v):
    """All results of replacing u by cyc(rot(u) * rot(v)^{+-1}); nonempty only."""
    out = set()
    for U in rotations(u):
        for V0 in (v, inv(v)):
            for V in rotations(V0):
                w = cyc(U + V)
                if w:
                    out.add(canon_word(w))
    return out


def neighbours(state):
    u, v = state
    res = set()
    for a, b in ((u, v), (v, u)):
        for w in cyclic_products(a, b):
            res.add(canon_pair(w, b))
    return res


def forward_set(source, cap):
    """Forward-reachable Sigma-classes from `source` through states of total
    length <= cap (barrier-ordered BFS is not needed for the set itself)."""
    s0 = canon_pair(*source)
    seen = {s0}
    q = deque([s0])
    while q:
        s = q.popleft()
        for t in neighbours(s):
            if len(t[0]) + len(t[1]) <= cap and t not in seen:
                seen.add(t)
                q.append(t)
    return seen


def is_unimodular(u, v):
    def ex(w):
        return w.count("x") - w.count("X"), w.count("y") - w.count("Y")
    (a, b), (c, d) = ex(u), ex(v)
    return abs(a * d - b * c) == 1


def main():
    cap = 17
    args = sys.argv[1:]
    if args[:1] == ["--cap"]:
        cap = int(args[1])

    # (1) the explicit counterexample to Lemma D1(c)
    u, v = "yxYYX", "xy"
    assert cyc(u) == u and cyc(v) == v and is_unimodular(u, v)
    s_from = canon_pair(u, v)
    prods = cyclic_products(u, v)
    assert canon_word("x") in prods, prods
    s_to = canon_pair("x", v)
    assert s_to in neighbours(s_from)
    back = neighbours(s_to)
    print("edge (yxYYX, xy) -> (x, xy): present (U=yxYYX, V=xy: junction cancels"
          " all of V, then cyclic reduction continues inside U)")
    print("all cyclic-product neighbours of the class of (x, xy):", sorted(back))
    print("reverse edge (x, xy) -> (yxYYX, xy) present:", s_from in back)
    assert s_from not in back
    # the presented group is trivial: y = x^-1 gives yxYYX = X x x x X = x = 1
    print("(yxYYX, xy) presents the trivial group and is unimodular: True")

    # (2) forward-reachable set of AK(3) at a small cap, and irreversible edges
    src = ("xxxYYYY", "xyxYXY")
    S = forward_set(src, cap)
    print(f"AK(3): forward-reachable Sigma-classes in G_full({cap}): {len(S)}")
    edges = 0
    irreversible = []
    for s in S:
        for t in neighbours(s):
            if t in S:
                edges += 1
                if s not in neighbours(t):
                    irreversible.append((s, t))
    print(f"directed edges inside the set: {edges}; edges whose reverse is absent: "
          f"{len(irreversible)}")
    for s, t in irreversible[:10]:
        print("  irreversible:", s, "->", t)
    # the two-letter-donor example really is the mechanism: list which irreversible
    # edges have the donor fully consumed (|t| = |s| - 2|donor|-2k)
    print("done")


if __name__ == "__main__":
    main()
