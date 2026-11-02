"""Agent L: complex-class canonical forms and set comparisons for rank-2 pairs.

Words use x, X = x^-1, y, Y = y^-1.  A *complex class* is a pair of cyclically
reduced words taken modulo

  Sigma = <rotation of either relator, inversion of either relator, swap>
  D8    = the 8 signed permutations of {x, y}  (x<->y, x->X, y->Y).

Every element of Sigma is a composite of ordinary AC moves (research-d,
Lemma D1); a signed permutation is an automorphism of F(x,y), so by Lemma D2
AC-triviality is constant on complex classes.  Two files of pairs can be
compared class by class.  Standard library only.

    python3 experiments/l_classes.py --selftest
    python3 experiments/l_classes.py canon FILE [--maxlen T] [--col2]      # classes
    python3 experiments/l_classes.py compare FILE_A FILE_B [--maxlen T] [--col2]

Input line format: two words separated by whitespace; extra columns ignored.
With --col2 the file is d_acsearch's --dump format "w1 w2 energy barrier src"
and --maxlen filters on the energy column; otherwise on cyclic total length.
"""
import sys

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


def canon_word(w):
    """least string among rotations of w and of w^-1 (w cyclically reduced)."""
    n = len(w)
    if n == 0:
        return w
    best = None
    for u in (w, inv(w)):
        uu = u + u
        for i in range(n):
            r = uu[i:i + n]
            if best is None or r < best:
                best = r
    return best


def canon_pair(a, b):
    ca, cb = canon_word(cyc(a)), canon_word(cyc(b))
    return (ca, cb) if (len(ca), ca) <= (len(cb), cb) else (cb, ca)


def _perm_table(g):
    # g bit0: swap x<->y ; bit1: invert x ; bit2: invert y  (applied to the
    # letters after the swap, as in d_acsearch's aut8 images)
    tab = {}
    for c in LET:
        base = c.lower()
        up = c.isupper()
        if g & 1:
            base = "y" if base == "x" else "x"
        if (base == "x" and g & 2) or (base == "y" and g & 4):
            up = not up
        tab[c] = base.upper() if up else base
    return tab


PERMS = [_perm_table(g) for g in range(8)]


def apply_perm(tab, w):
    return "".join(tab[c] for c in w)


def complex_class(a, b):
    """canonical representative of the Sigma x D8 class of the pair (a, b)."""
    a, b = cyc(a), cyc(b)
    best = None
    for tab in PERMS:
        p = canon_pair(apply_perm(tab, a), apply_perm(tab, b))
        if best is None or (len(p[0]) + len(p[1]), p) < (len(best[0]) + len(best[1]), best):
            best = p
    return best


def sigma_class(a, b):
    return canon_pair(a, b)


def read_pairs(path, maxlen=None, col2=False):
    out = []
    with open(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) < 2 or parts[0].startswith("#"):
                continue
            # tolerate an id column (d_prepare_targets format: "id w1 w2")
            if len(parts) >= 3 and not set(parts[0]) <= set(LET):
                parts = parts[1:]
            a, b = parts[0], parts[1]
            if not (set(a) <= set(LET) and set(b) <= set(LET)):
                continue
            if maxlen is not None:
                if col2 and len(parts) >= 3 and parts[2].isdigit():
                    if int(parts[2]) > maxlen:
                        continue
                elif len(cyc(a)) + len(cyc(b)) > maxlen:
                    continue
            out.append((a, b))
    return out


def classes_of(pairs):
    return {complex_class(a, b) for a, b in pairs}


def selftest():
    # class invariance under random Sigma x D8 elements
    import random
    rng = random.Random(11)

    def rword(n):
        while True:
            w = [rng.choice(LET)]
            while len(w) < n:
                c = rng.choice(LET)
                if c != w[-1].swapcase():
                    w.append(c)
            w = "".join(w)
            if len(w) < 2 or w[0] != w[-1].swapcase():
                return w
    checks = 0
    for _ in range(3000):
        a, b = rword(rng.randint(1, 9)), rword(rng.randint(1, 9))
        k = complex_class(a, b)
        # random transformation
        tab = rng.choice(PERMS)
        a2, b2 = apply_perm(tab, a), apply_perm(tab, b)
        r = rng.randrange(len(a2)); a2 = a2[r:] + a2[:r]
        r = rng.randrange(len(b2)); b2 = b2[r:] + b2[:r]
        if rng.random() < 0.5:
            a2 = inv(a2)
        if rng.random() < 0.5:
            b2 = inv(b2)
        if rng.random() < 0.5:
            a2, b2 = b2, a2
        # conjugate by a random word (cyclic reduction must undo it)
        h = rword(rng.randint(0, 3)) if rng.random() < 0.5 else ""
        a2 = red(h + a2 + inv(h))
        assert complex_class(a2, b2) == k, (a, b, a2, b2)
        checks += 1
    assert complex_class("xxxYYYY", "xyxYXY") == complex_class("yyyXXXX", "yxyXYX")
    assert complex_class("xxxYYYY", "xyxYXY") != complex_class("xxyXYY", "xxxYYXy")
    assert complex_class("x", "y") == complex_class("Y", "X") == ("X", "Y")
    # the AK(3) class representative: 13 letters, two relators
    k = complex_class("xxxYYYY", "xyxYXY")
    assert len(k[0]) + len(k[1]) == 13
    print(f"selftest passed: {checks} random invariance checks")
    return 0


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) < 3:
        print(__doc__)
        return 2
    maxlen = None
    col2 = "--col2" in argv
    if "--maxlen" in argv:
        maxlen = int(argv[argv.index("--maxlen") + 1])
    cmd = argv[1]
    if cmd == "canon":
        pairs = read_pairs(argv[2], maxlen, col2)
        cl = classes_of(pairs)
        print(f"pairs {len(pairs)} classes {len(cl)}")
        for a, b in sorted(cl, key=lambda p: (len(p[0]) + len(p[1]), p)):
            print(a, b)
        return 0
    if cmd == "compare":
        A = classes_of(read_pairs(argv[2], maxlen, col2))
        B = classes_of(read_pairs(argv[3], maxlen, col2))
        onlyA, onlyB = A - B, B - A
        print(f"A classes {len(A)}  B classes {len(B)}  common {len(A & B)}  onlyA {len(onlyA)}  onlyB {len(onlyB)}")
        def hist(S):
            h = {}
            for a, b in S:
                h[len(a) + len(b)] = h.get(len(a) + len(b), 0) + 1
            return dict(sorted(h.items()))
        print("A by length", hist(A))
        print("B by length", hist(B))
        if onlyA:
            print("onlyA by length", hist(onlyA))
        if onlyB:
            print("onlyB by length", hist(onlyB))
        for a, b in sorted(onlyA, key=lambda p: (len(p[0]) + len(p[1]), p))[:20]:
            print("onlyA", a, b)
        for a, b in sorted(onlyB, key=lambda p: (len(p[0]) + len(p[1]), p))[:20]:
            print("onlyB", a, b)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
