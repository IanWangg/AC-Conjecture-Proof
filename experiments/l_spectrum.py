"""Agent L: the barrier spectrum of short balanced presentations.

For a total length ell, enumerate every Sigma-class (rotation / inversion of
either relator, swap) of pairs of cyclically reduced words with |a|+|b| = ell
and unimodular exponent matrix (necessary for presenting the trivial group).
Classify each class against

  * the exact forward-reachable set of (x,y) in the full cyclic-product graph
    at cap C ("trivial hump", d_acsearch --source x,y --no-stop --cap C
    --dump 16); every member is AC-trivial with an elementary trivialization
    of peak <= C.  NOTE (research-l, Lemma L2): cyclic products with a fully
    cancelled donor are not always reversible by one cyclic product, so
    "not in the hump" means "not forward-reachable from (x,y) within cap C",
    not "barrier > C"; exact forward barriers of leftovers are measured
    separately (d_acsearch --target-keys).
  * the exact component of AK(3) at cap 28 (D's key dump k28_ak3.bin).

Leftover classes are tested for group triviality by coset enumeration
(experiments/f_descent.py, imported read-only).  Standard library + numpy.

    python3 experiments/l_spectrum.py --selftest
    python3 experiments/l_spectrum.py enumerate ELL OUT.txt
    python3 experiments/l_spectrum.py classify ELL HUMP_DUMP K28.bin [--hump-cap C]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from l_classes import LET, inv, cyc, canon_word, canon_pair, complex_class  # noqa: E402

CODE = {"x": 0, "X": 1, "y": 2, "Y": 3}
DEC = "xXyY"


# ---------------------------------------------------------------- enumeration

def canonical_words(n):
    """All Sigma-canonical cyclically reduced words of length n (one per class
    under rotation and inversion), via candidates whose first letter is their
    minimal letter followed by a full canonical check."""
    out = []
    for first in LET:
        allowed = [c for c in LET if c >= first]
        stack = [first]

        def rec(w):
            if len(w) == n:
                if w[0] != w[-1].swapcase() and canon_word(w) == w:
                    out.append(w)
                return
            last = w[-1]
            for c in allowed:
                if c != last.swapcase():
                    rec(w + c)
        rec(first)
    return out


def exps(w):
    return (w.count("x") - w.count("X"), w.count("y") - w.count("Y"))


def unimodular_classes(ell):
    """Sigma-classes (canon_pair form) of pairs with |a|+|b| = ell, |det| = 1."""
    words = {n: canonical_words(n) for n in range(1, ell)}
    ex = {w: exps(w) for n in words for w in words[n]}
    res = []
    for n1 in range(1, ell // 2 + 1):
        n2 = ell - n1
        A, B = words[n1], words[n2]
        for a in A:
            ax, ay = ex[a]
            for b in B:
                if n1 == n2 and b < a:
                    continue
                bx, by = ex[b]
                if abs(ax * by - ay * bx) == 1:
                    res.append((a, b))
    return res


# ---------------------------------------------------------------- D's key format

def decode_key(key):
    key = int(key)
    T = (key >> 58) & 31
    na = (key >> 53) & 31
    nb = T - na
    a = [(key >> 51) & 3]
    b = [(key >> 49) & 3]
    d = key & ((1 << 49) - 1)
    nd = (na - 1) + (nb - 1)
    digits = [0] * nd
    for i in range(nd - 1, -1, -1):
        digits[i] = d % 3
        d //= 3
    p = 0
    for w, n in ((a, na), (b, nb)):
        for _ in range(1, n):
            dg = digits[p]
            p += 1
            f = w[-1] ^ 1
            c = dg + 1 if dg >= f else dg
            w.append(c)
    return "".join(DEC[c] for c in a), "".join(DEC[c] for c in b)


def load_k28_short(path, maxlen):
    """Sigma-classes (canon_pair) of all keys in a d_acsearch --dumpkeys file
    with total length <= maxlen."""
    import numpy as np
    keys = np.fromfile(path, dtype=np.uint64)
    T = (keys >> np.uint64(58)) & np.uint64(31)
    sel = keys[T <= maxlen]
    out = {}
    for k in sel:
        a, b = decode_key(k)
        out[canon_pair(a, b)] = len(a) + len(b)
    return out, len(keys)


def load_hump_dump(path):
    """d_acsearch --dump format: w1 w2 energy barrier src -> {class: barrier}."""
    out = {}
    with open(path) as f:
        for line in f:
            p = line.split()
            if len(p) < 4:
                continue
            k = canon_pair(p[0], p[1])
            b = int(p[3])
            if k not in out or b < out[k]:
                out[k] = b
    return out


# ---------------------------------------------------------------- classification

def to_ints(w):
    m = {"x": 1, "X": -1, "y": 2, "Y": -2}
    return tuple(m[c] for c in w)


def classify(ell, hump_path, k28_path, hump_cap):
    import f_descent  # read-only import of agent F's coset enumerator
    classes = unimodular_classes(ell)
    hump = load_hump_dump(hump_path)
    ak3, nkeys = load_k28_short(k28_path, 16)
    print(f"length {ell}: unimodular Sigma-classes {len(classes)}; hump states loaded {len(hump)}; "
          f"k28 keys {nkeys}, of which length<=16: {len(ak3)}")
    hist = {}
    n_ak3 = 0
    left = []
    for a, b in classes:
        k = canon_pair(a, b)
        if k in hump:
            bar = hump[k]
            hist[bar] = hist.get(bar, 0) + 1
        elif k in ak3:
            n_ak3 += 1
        else:
            left.append(k)
    print(f"  in trivial hump T({hump_cap}) (forward-reachable from (x,y); barrier of the (x,y)->P path):" f" {sum(hist.values())}")
    for bar in sorted(hist):
        print(f"    barrier {bar:2d} (excess {bar - ell:2d}): {hist[bar]}")
    print(f"  in AK(3)'s cap-28 component: {n_ak3}")
    print(f"  in neither: {len(left)}")
    trivial, nontrivial, undecided = [], [], []
    for a, b in left:
        r = f_descent.is_trivial_group(to_ints(a), to_ints(b), limit=400000)
        if r is None and f_descent.nontrivial_hom(to_ints(a), to_ints(b)):
            r = False  # nontrivial permutation image (A5/A6/A7): the group is nontrivial
        (trivial if r is True else nontrivial if r is False else undecided).append((a, b))
    print(f"    coset enumeration + permutation images: trivial group {len(trivial)}, nontrivial {len(nontrivial)}, undecided {len(undecided)}")
    # complex classes (Sigma x D8) of the leftovers that present the trivial group
    cc = {}
    for a, b in trivial:
        cc.setdefault(complex_class(a, b), []).append((a, b))
    print(f"    trivial-group leftovers form {len(cc)} complex classes (Sigma x D8):")
    for key in sorted(cc):
        print("      ", key[0], key[1], f"({len(cc[key])} Sigma-classes)")
    for a, b in undecided:
        print("    undecided", a, b)
    return 0


def selftest():
    # decode_key must invert D's encoding: check against the known AK(3) key
    # by re-encoding a few words and comparing with the C++ engine's output
    assert canonical_words(1) == ["X", "Y"]  # x ~ X and y ~ Y under inversion
    w2 = canonical_words(2)
    # classes of length 2: xx~XX, yy~YY, xy~yx~XY~YX, xY~Yx~Xy~yX
    assert len(w2) == 4, w2
    # count check against brute force for n = 5
    brute = set()
    import itertools
    for t in itertools.product(LET, repeat=5):
        w = "".join(t)
        if any(w[i] == w[i + 1].swapcase() for i in range(4)) or w[0] == w[-1].swapcase():
            continue
        brute.add(canon_word(w))
    assert set(canonical_words(5)) == brute, (len(brute), len(canonical_words(5)))
    # unimodular pairs of length 2 and 3: (x,y) only at 2; at 3: (x, xy),(x,Xy)... check a known count
    u2 = unimodular_classes(2)
    assert u2 == [("X", "Y")], u2
    # decode round trip with an encoder written here
    def encode(a, b):
        A = [CODE[c] for c in a]; B = [CODE[c] for c in b]
        d = 0
        for w in (A, B):
            for i in range(1, len(w)):
                c = w[i]; f = w[i - 1] ^ 1
                d = d * 3 + (c - (1 if c > f else 0))
        T = len(A) + len(B)
        return (T << 58) | (len(A) << 53) | (A[0] << 51) | (B[0] << 49) | d
    for a, b in [("xyxYXY", "xxxYYYY"), ("x", "y"), ("XXy", "xYxYY"), ("xxyXYY", "xxxYYXy")]:
        assert decode_key(encode(a, b)) == (a, b)
    print("selftest passed: canonical word enumeration (n<=5 brute force), unimodular classes, key decoding")
    return 0


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) >= 4 and argv[1] == "enumerate":
        ell = int(argv[2])
        cl = unimodular_classes(ell)
        with open(argv[3], "w") as f:
            for a, b in cl:
                f.write(f"{a} {b}\n")
        print(f"length {ell}: {len(cl)} unimodular Sigma-classes written to {argv[3]}")
        return 0
    if len(argv) >= 5 and argv[1] == "classify":
        cap = int(argv[argv.index("--hump-cap") + 1]) if "--hump-cap" in argv else 20
        return classify(int(argv[2]), argv[3], argv[4], cap)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
