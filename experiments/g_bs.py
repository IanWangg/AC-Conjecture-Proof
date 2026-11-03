#!/usr/bin/env python3
"""Agent G: exact normal forms and a conjugacy SEARCH in
    B = BS(m,n) = <x, y | x^-1 y^m x = y^n>   (stable letter t = x, base a = y).

Normal form (HNN extension, right coset representatives; unique by Britton's
lemma):  a^{e_0} t^{d_1} a^{e_1} ... t^{d_r} a^{f}  with no pinch, where the
exponent e_{i-1} in front of t^{d_i} lies in [0,|m|-1] if d_i = +1 (coset of
<a^m>, since a^m t = t a^n) and in [0,|n|-1] if d_i = -1 (a^n t^-1 = t^-1 a^m).

`conjugate(g, h, window)` returns a certificate (rotation, s, inverted) with
g = a^s h* a^-s (h* a cyclic permutation of h or h^-1, Collins' lemma) when it
finds one; such positives are exact (checked by normal-form equality).  A
negative answer only means "none with |s| <= window", i.e. it is a bounded
search, NOT a proof of non-conjugacy -- except that unequal t-length (the
number of stable letters of a cyclically reduced form) or unequal image in
H_1 = Z (x -> 1) DOES prove non-conjugacy.

Run `python3 experiments/g_bs.py --selftest`.
"""
import random
import sys


def _floor_res(c, M):
    e = c % M
    return e, (c - e) // M


def normal_form(w, m, n):
    """Return (blocks, f): blocks = [(e, d), ...] meaning a^e t^d, then a^f."""
    M, N = abs(m), abs(n)
    blocks = []
    c = 0
    for ch in w:
        if ch in "yY":
            c += 1 if ch == "y" else -1
            continue
        d = 1 if ch == "x" else -1
        if blocks and blocks[-1][1] == -d:
            # possible pinch t^-d a^c t^d
            if d == 1 and c % M == 0:          # t^-1 a^{mk} t = a^{nk}
                e_prev, _ = blocks.pop()
                c = e_prev + (c // m) * n
                continue
            if d == -1 and c % N == 0:         # t a^{nk} t^-1 = a^{mk}
                e_prev, _ = blocks.pop()
                c = e_prev + (c // n) * m
                continue
        if d == 1:                             # a^c t = a^e a^{m k} t = a^e t a^{n k}
            e, k = _floor_res(c, M)
            k = k * (1 if m > 0 else -1)       # a^{M k'} = a^{m (k' sign)}
            blocks.append((e, 1))
            c = n * k
        else:                                  # a^c t^-1 = a^e t^-1 a^{m k}
            e, k = _floor_res(c, N)
            k = k * (1 if n > 0 else -1)
            blocks.append((e, -1))
            c = m * k
    return tuple(blocks), c


def nf_word(nf):
    blocks, f = nf
    out = []
    for e, d in blocks:
        out.append(("y" * e) if e >= 0 else ("Y" * -e))
        out.append("x" if d == 1 else "X")
    out.append(("y" * f) if f >= 0 else ("Y" * -f))
    return "".join(out)


def equal(u, v, m, n):
    return normal_form(u, m, n) == normal_form(v, m, n)


def inv(w):
    return w.swapcase()[::-1]


def red(w):
    out = []
    for c in w:
        if out and out[-1] == c.swapcase():
            out.pop()
        else:
            out.append(c)
    return "".join(out)


def cyclic_reduce(w, m, n, limit=10000):
    """A cyclically reduced normal-form word conjugate to w: rotate so that it
    starts with a stable letter, then remove a cyclic pinch t^{d_r} a^f t^{d_1}
    (d_r = -d_1, f divisible by m resp. n) by conjugating with t^{-d_1}."""
    M, N = abs(m), abs(n)
    w = nf_word(normal_form(w, m, n))
    for _ in range(limit):
        blocks, f = normal_form(w, m, n)
        if not blocks:
            return w
        e0 = blocks[0][0]
        if e0:
            w = nf_word(normal_form("Y" * e0 + w + "y" * e0, m, n))
            blocks, f = normal_form(w, m, n)
        d1, dr = blocks[0][1], blocks[-1][1]
        if len(blocks) >= 2 and dr == -d1 and ((d1 == 1 and f % M == 0) or (d1 == -1 and f % N == 0)):
            t1 = "x" if d1 == 1 else "X"
            w = nf_word(normal_form(inv(t1) + w + t1, m, n))
            continue
        return w
    raise RuntimeError("cyclic reduction did not terminate")


def tlen(w, m, n):
    return len(normal_form(cyclic_reduce(w, m, n), m, n)[0])


def xexp(w):
    return w.count("x") - w.count("X")


def rotations_at_t(w):
    """Cyclic permutations of the word w that start with a t-letter."""
    return [w[i:] + w[:i] for i in range(len(w)) if w[i] in "xX"]


def conjugate(g, h, m, n, window=60):
    """Search for g ~ h^{+-1} in BS(m,n).  Returns a witness or None."""
    gc = cyclic_reduce(g, m, n)
    tg = len(normal_form(gc, m, n)[0])
    for inverted, hh in ((False, h), (True, inv(h))):
        if xexp(gc) != xexp(hh):
            continue
        hc = cyclic_reduce(hh, m, n)
        if len(normal_form(hc, m, n)[0]) != tg:
            continue
        nfg = normal_form(gc, m, n)
        # Collins: conjugate cyclically reduced elements have cyclically
        # permuted stable-letter sign sequences (sound necessary condition)
        sg = tuple(d for _, d in nfg[0])
        sh = tuple(d for _, d in normal_form(hc, m, n)[0])
        if tg and not any(sh[i:] + sh[:i] == sg for i in range(len(sh))):
            continue
        if tg == 0:
            # elliptic elements: only literal equality is reported (no claim otherwise)
            if nfg == normal_form(hc, m, n):
                return (hc, 0, inverted)
            continue
        for hs in rotations_at_t(hc):
            for s in range(-window, window + 1):
                a = ("y" * s) if s >= 0 else ("Y" * -s)
                if normal_form(a + hs + inv(a), m, n) == nfg:
                    return (hs, s, inverted)
    return None


def selftest():
    rng = random.Random(11)
    for (m, n) in ((3, 4), (2, 3), (1, 2), (4, 5), (-2, 3)):
        R = "X" + ("y" * m if m > 0 else "Y" * -m) + "x" + ("Y" * n if n > 0 else "y" * -n)
        for _ in range(300):
            w = "".join(rng.choice("xXyY") for _ in range(rng.randint(0, 12)))
            g = "".join(rng.choice("xXyY") for _ in range(rng.randint(0, 5)))
            k = rng.randrange(len(w) + 1)
            r = R if rng.random() < 0.5 else inv(R)
            j = rng.randrange(len(r))
            w2 = w[:k] + g + r[j:] + r[:j] + inv(g) + w[k:]
            assert normal_form(w, m, n) == normal_form(w2, m, n), (m, n, w, w2)
            # normal form word represents the same element
            assert normal_form(nf_word(normal_form(w, m, n)), m, n) == normal_form(w, m, n)
        # conjugacy positives
        for _ in range(60):
            w = "".join(rng.choice("xXyY") for _ in range(rng.randint(1, 8)))
            g = "".join(rng.choice("xXyY") for _ in range(rng.randint(0, 4)))
            if tlen(w, m, n) == 0:
                continue
            assert conjugate(g + w + inv(g), w, m, n, window=40) is not None, (m, n, w, g)
    # distinct t-lengths are never conjugate
    assert conjugate("xyX", "xy", 3, 4) is None
    print("g_bs self-test passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
