#!/usr/bin/env python3
"""Agent M: thickenability sweep of the low-energy slice of an engine key dump.

Reads a binary file of 64-bit Sigma-keys in D's encoding (d_acsearch --dumpkeys /
m_acsearch --dumpkeys, width 1), decodes every state of total length <= E,
reduces to complex classes (Sigma x the 8 signed letter permutations, which
preserve the presentation complex up to homeomorphism), and runs F's
polynomial thickenability test `f_thicken.thickenable_fast` on one representative
per class.  A thickenable state anywhere in a forward set of AK(3) would make
AK(3) AC-trivial (research-f Theorem 2.1, externally reported, with J's classical
sketch), so this is a trivialization detector, not an obstruction.

With a third argument `defect`, additionally computes F's meridian defect
(`f_landscape.meridian_defect`, Nielsen depth 5: smallest cyclic syllable length of a
partner relator in C_p*C_q over the relators that admit a torus-knot form) for every
complex class and reports the distribution; a defect-2 state through a relator of one
of the types occurring in AK(3)'s class would be an immediate trivialization (I, Prop. M).

Usage:
  python3 experiments/m_lowenergy_thicken.py KEYS.bin E [defect]
  python3 experiments/m_lowenergy_thicken.py --selftest
Standard library + f_thicken / f_landscape only (no numpy needed).
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import f_thicken as FT  # noqa: E402
import f_landscape as FL  # noqa: E402

LET = "xXyY"
INV = {"x": "X", "X": "x", "y": "Y", "Y": "y"}


def inv_code(c):
    return c ^ 1


def decode_key(key):
    """D's 64-bit encoding: (T<<58)|(na<<53)|(a0<<51)|(b0<<49)|base-3 digits."""
    T = (key >> 58) & 31
    na = (key >> 53) & 31
    nb = T - na
    a0 = (key >> 51) & 3
    b0 = (key >> 49) & 3
    d = key & ((1 << 49) - 1)
    nd = (na - 1) + (nb - 1)
    digits = [0] * nd
    for i in range(nd - 1, -1, -1):
        digits[i] = d % 3
        d //= 3
    p = 0
    words = []
    for n, first in ((na, a0), (nb, b0)):
        w = [first]
        for _ in range(1, n):
            f = inv_code(w[-1])
            c = digits[p]
            p += 1
            if c >= f:
                c += 1
            w.append(c)
        words.append("".join(LET[c] for c in w))
    return words[0], words[1]


def encode_pair(a, b):
    """Python port of D's key_of_pair (for the self-test)."""
    def canon_word(w):
        cands = [u[k:] + u[:k] for u in (w, "".join(INV[c] for c in reversed(w))) for k in range(len(w))]
        # D compares by letter codes x<X<y<Y, which is the order of LET
        return min(cands, key=lambda s: [LET.index(c) for c in s])

    def enc(p, q):
        d = 0
        for w in (p, q):
            for i in range(1, len(w)):
                c = LET.index(w[i])
                f = inv_code(LET.index(w[i - 1]))
                d = d * 3 + (c - (1 if c > f else 0))
        return (len(p) + len(q)) << 58 | len(p) << 53 | LET.index(p[0]) << 51 | LET.index(q[0]) << 49 | d
    ca, cb = canon_word(a), canon_word(b)
    ka, kb = [LET.index(c) for c in ca], [LET.index(c) for c in cb]
    if (len(ca), ka) <= (len(cb), kb):
        return enc(ca, cb)
    return enc(cb, ca)


def signed_perm_images(a, b):
    for g in range(8):
        def img(c):
            base = LET.index(c) & 2
            sgn = LET.index(c) & 1
            if g & 1:
                base ^= 2
            if (base == 0 and (g & 2)) or (base == 2 and (g & 4)):
                sgn ^= 1
            return LET[base | sgn]
        yield "".join(img(c) for c in a), "".join(img(c) for c in b)


def complex_key(a, b):
    return min(encode_pair(u, v) for u, v in signed_perm_images(a, b))


def sweep(path, emax, defect=False):
    n = 0
    low = []
    with open(path, "rb") as f:
        while True:
            buf = f.read(8 * 65536)
            if not buf:
                break
            for (k,) in struct.iter_unpack("<Q", buf):
                n += 1
                if ((k >> 58) & 31) <= emax:
                    low.append(k)
    classes = {}
    for k in low:
        a, b = decode_key(k)
        classes.setdefault(complex_key(a, b), (a, b))
    thick = []
    for ck, (a, b) in classes.items():
        r1, r2 = FT.cyc_reduce(FT.parse(a)), FT.cyc_reduce(FT.parse(b))
        if FT.thickenable_fast(r1, r2):
            thick.append((a, b))
    by_len = {}
    for k in low:
        by_len[(k >> 58) & 31] = by_len.get((k >> 58) & 31, 0) + 1
    out = {"keys_read": n, "states_le_E": len(low), "by_length": {int(k): v for k, v in sorted(by_len.items())},
           "complex_classes": len(classes), "thickenable_classes": len(thick), "thickenable": thick}
    if defect:
        dist = {}
        examples = {}
        for ck, (a, b) in classes.items():
            d = FL.meridian_defect(FT.cyc_reduce(FT.parse(a)), FT.cyc_reduce(FT.parse(b)), depth=5)
            key = "none" if d is None else int(d)
            dist[key] = dist.get(key, 0) + 1
            if d is not None and (key not in examples or len(a) + len(b) < sum(map(len, examples[key]))):
                examples[key] = (a, b)
        out["meridian_defect_distribution"] = {str(k): v for k, v in sorted(dist.items(), key=lambda kv: (isinstance(kv[0], str), kv[0]))}
        out["meridian_defect_examples"] = {str(k): v for k, v in examples.items()}
    return out


def selftest():
    import random
    rng = random.Random(7)
    for _ in range(2000):
        def rw(n):
            while True:
                w = [rng.choice(LET)]
                for _ in range(n - 1):
                    w.append(rng.choice([c for c in LET if c != INV[w[-1]]]))
                if n == 1 or w[0] != INV[w[-1]]:
                    return "".join(w)
        a, b = rw(rng.randint(1, 14)), rw(rng.randint(1, 14))
        k = encode_pair(a, b)
        a2, b2 = decode_key(k)
        assert encode_pair(a2, b2) == k, (a, b, a2, b2)
        assert sorted((len(a), len(b))) == sorted((len(a2), len(b2)))
    # D's documented key of AK(3) (research-m): 0x34c0000000012878
    assert encode_pair("xxxYYYY", "xyxYXY") == 0x34c0000000012878, hex(encode_pair("xxxYYYY", "xyxYXY"))
    assert decode_key(0x34c0000000012878) == ("xyxYXY", "xxxYYYY")
    assert FT.thickenable_fast(FT.parse("x"), FT.parse("y"))
    assert not FT.thickenable_fast(FT.cyc_reduce(FT.parse("xxxYYYY")), FT.cyc_reduce(FT.parse("xyxYXY")))
    assert len(set(complex_key(*p) for p in signed_perm_images("xxxYYYY", "xyxYXY"))) == 1
    assert FL.meridian_defect(FT.parse("xxxYYYY"), FT.parse("xyxYXY"), depth=5) == 6   # F: AK(3) has defect 6
    assert FL.meridian_defect(FT.parse("xxxxyXy"), FT.parse("xyyyxYY"), depth=5) == 10  # F3.2: C4 (10 and 10)
    print("m_lowenergy_thicken self-test passed: 2000 key round trips, AK(3) key, controls")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
    elif len(sys.argv) in (3, 4):
        import json
        print(json.dumps(sweep(sys.argv[1], int(sys.argv[2]), defect=(len(sys.argv) == 4))))
    else:
        print(__doc__)
