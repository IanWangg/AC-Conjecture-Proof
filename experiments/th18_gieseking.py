#!/usr/bin/env python3
"""TH18 (section 2.10): the group  Gamma = <x,y | x^2 y^2 = y x>  (w = xxyyXY).

alpha = (x -> xy, y -> Y) maps K's frozen relator c = xyxYYXy to w exactly, so
Gamma is O's punctured-torus bundle group.  With y = x^-1 a, a_i = x^i a x^-i,
the relator reads a_2 a_1 = a_0, hence Gamma = F(a,b) x| <x> with
phi = conj by x:  a -> b, b -> a b^-1.  An element of height 1 is f*x, and
f x ~ f' x  iff  f' = g phi^k(f) phi(g)^-1  (twisted conjugacy).  A primitive
of F(x,y) of height 1 is conjugate to (xy)^j x = a^j x.

  python3 experiments/th18_gieseking.py --selftest
  python3 experiments/th18_gieseking.py --table      # bounded searches of section 2.10
"""
import heapq
import sys


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


def subst(m, w):
    return red("".join(m[c] if c in m else inv(m[c.swapcase()]) for c in w))


PHI, PHI_INV = {"a": "b", "b": "aB"}, {"a": "ba", "b": "a"}
ALPHA = {"x": "xy", "y": "Y"}


def phi_pow(w, h):
    for _ in range(abs(h)):
        w = subst(PHI if h > 0 else PHI_INV, w)
    return w


def to_fx(word):
    """word in x,y  ->  (f, h) with word = f x^h in F(a,b) x| <x>."""
    f, h = "", 0
    for ch in word:
        if ch == "x":
            h += 1
        elif ch == "X":
            h -= 1
        elif ch == "y":                      # y = x^-1 a
            f, h = red(f + phi_pow("a", h - 1)), h - 1
        else:                                # y^-1 = a^-1 x
            f, h = red(f + phi_pow("A", h)), h + 1
    return f, h


def ball(word, nodes, cap):
    """Twisted conjugates of the height-1 element `word` (best-first, bounded)."""
    f, h = to_fx(word)
    if h == -1:
        f, h = to_fx(inv(word))
    assert h == 1
    seen, heap = {f}, [(len(f), f)]
    while heap and len(seen) < nodes:
        _, g = heapq.heappop(heap)
        for u in [subst(PHI, g), subst(PHI_INV, g)] + [red(c + g + inv(subst(PHI, c))) for c in "aAbB"]:
            if len(u) <= cap and u not in seen:
                seen.add(u)
                heapq.heappush(heap, (len(u), u))
    return seen


def exits(ballset):
    return sorted((u for u in ballset if set(u) <= {"a"} or set(u) <= {"A"}), key=len)


def rel(m):
    return "X" + "y" * m + "x" + "Y" * (m + 1)


def killer_ak(n):                            # alpha(x^n Y X y y) = (xy)^n X Y Y
    return subst(ALPHA, "x" * n + "YXyy")


def selftest():
    assert subst(ALPHA, "xyxYYXy") == "xxyyXY"
    assert all(subst(PHI, subst(PHI_INV, g)) == g == subst(PHI_INV, subst(PHI, g)) for g in "ab")
    assert to_fx("xxyyXY") == ("", 0) and to_fx("xy") == ("a", 0) and to_fx("xyxyx") == ("aa", 1)
    assert killer_ak(3) == "xyxyxyXYY" and to_fx(rel(4))[1] == 1 and to_fx(killer_ak(3))[1] == 1
    for m, j in ((1, ""), (2, "aa"), (3, "aa")):
        assert j in exits(ball(rel(m), 2000, 30)), m
    print("th18_gieseking self-test passed")


def table():
    R = {m: ball(rel(m), 300000 if m >= 4 else 2000, 40) for m in range(1, 7)}
    for m in R:
        print("r_%d  (AK_2(%d)):  explored %6d  shortest %-10s exits a^j: %s"
              % (m, m, len(R[m]), min(R[m], key=len), exits(R[m])[:3]))
    for n in range(1, 7):
        K = ball(killer_ak(n), 40000, 26)
        print("AK(%d) killer %-16s shortest %-8s exits %s  meets r_m-balls for m in %s"
              % (n, killer_ak(n), min(K, key=len), exits(K)[:2], [m for m in R if K & R[m]]))


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif sys.argv[1:] == ["--table"]:
        table()
    else:
        print(__doc__)
