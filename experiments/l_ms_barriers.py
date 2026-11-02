"""Agent L: triage of the 1190 Miller-Schupp benchmark presentations against exact
components of the full cyclic-product graph.

Key encoding is a line-by-line port of d_acsearch.cpp's Sigma-canonical 64-bit
key (letters x,X,y,Y -> 0,1,2,3; canonical rotation/inversion; shorter word
first, then lexicographic), validated in --selftest against a --dump file and
the matching --dumpkeys file produced by the C++ engine.

    python3 experiments/l_ms_barriers.py --selftest DUMP.txt KEYS.bin
    python3 experiments/l_ms_barriers.py triage MS_FILE SOLVED_FILE K16 K18 K20 K28AK3 [K28MS2A K28MS2B]

MS_FILE: Shehper et al. all_presentations.txt (int arrays, 0-padded, two
relators of max_relator_length = len/2).  Standard library + numpy.
"""
import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from l_classes import red, inv, cyc  # noqa: E402

CODE = {"x": 0, "X": 1, "y": 2, "Y": 3}
DEC = "xXyY"
INTMAP = {1: "x", -1: "X", 2: "y", -2: "Y"}


# ------------------------------------------------------------- D's key format

def _canon_word_D(w):
    """w: list of letter codes, cyclically reduced.  Returns the canonical
    rotation of w or of w^-1 (numeric lexicographic minimum)."""
    n = len(w)
    t = [c ^ 1 for c in reversed(w)]
    best = None
    for u in (w, t):
        uu = u + u
        for i in range(n):
            r = uu[i:i + n]
            if best is None or r < best:
                best = r
    return best


def _encode_ordered(a, b):
    d = 0
    for w in (a, b):
        for i in range(1, len(w)):
            c = w[i]
            f = w[i - 1] ^ 1
            d = d * 3 + (c - (1 if c > f else 0))
    T = len(a) + len(b)
    return (T << 58) | (len(a) << 53) | (a[0] << 51) | (b[0] << 49) | d


def key_of_pair(a, b):
    """a, b: words (strings).  Cyclically reduces, then D's Sigma-key."""
    A = [CODE[c] for c in cyc(a)]
    B = [CODE[c] for c in cyc(b)]
    if not A or not B or len(A) + len(B) > 31:
        return None
    ca, cb = _canon_word_D(A), _canon_word_D(B)
    if (len(ca), ca) <= (len(cb), cb):
        return _encode_ordered(ca, cb)
    return _encode_ordered(cb, ca)


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
            w.append(dg + 1 if dg >= f else dg)
    return "".join(DEC[c] for c in a), "".join(DEC[c] for c in b)


class KeySet:
    def __init__(self, path):
        import numpy as np
        k = np.fromfile(path, dtype=np.uint64)
        k.sort()
        self.k = k
        self.np = np

    def __contains__(self, key):
        if key is None:
            return False
        i = self.np.searchsorted(self.k, self.np.uint64(key))
        return i < len(self.k) and int(self.k[i]) == key

    def __len__(self):
        return len(self.k)


# ------------------------------------------------------------- MS data

def parse_ms_line(line):
    arr = ast.literal_eval(line.strip())
    m = len(arr) // 2
    r = ["".join(INTMAP[v] for v in arr[:m] if v != 0),
         "".join(INTMAP[v] for v in arr[m:] if v != 0)]
    return r


def load_ms(path):
    with open(path) as f:
        return [parse_ms_line(l) for l in f if l.strip()]


# ------------------------------------------------------------- triage

def triage(ms_path, solved_path, keyfiles):
    pres = load_ms(ms_path)
    solved = {tuple(p) for p in load_ms(solved_path)}
    sets = {name: KeySet(p) for name, p in keyfiles.items()}
    for name, s in sets.items():
        print(f"keyset {name}: {len(s)} keys")
    rows = []
    summary = {}
    for idx, (a, b) in enumerate(pres):
        k = key_of_pair(a, b)
        tag = "unencodable(>31)" if k is None else None
        if tag is None:
            if "hump16" in sets and k in sets["hump16"]:
                tag = "hump<=16"
            elif "hump18" in sets and k in sets["hump18"]:
                tag = "hump17-18"
            elif "hump20" in sets and k in sets["hump20"]:
                tag = "hump19-20"
            elif "ak3" in sets and k in sets["ak3"]:
                tag = "AK3-class(cap28)"
            elif "ms2a" in sets and k in sets["ms2a"]:
                tag = "MS2a-class(cap28)"
            elif "ms2b" in sets and k in sets["ms2b"]:
                tag = "MS2b-class(cap28)"
            else:
                tag = "outside(barrier>20)"
        st = "solved" if (a, b) in solved else "unsolved"
        rows.append((idx, a, b, len(cyc(a)) + len(cyc(b)), st, tag))
        summary[(st, tag)] = summary.get((st, tag), 0) + 1
    for (st, tag), n in sorted(summary.items()):
        print(f"{st:9s} {tag:22s} {n}")
    return rows


def selftest(dump_path, keys_path):
    ks = KeySet(keys_path)
    n = 0
    with open(dump_path) as f:
        for line in f:
            p = line.split()
            if len(p) < 2:
                continue
            k = key_of_pair(p[0], p[1])
            assert k in ks, (p, k)
            assert decode_key(k) and key_of_pair(*decode_key(k)) == k
            # Sigma invariance: rotate / invert / swap
            a, b = p[0], p[1]
            assert key_of_pair(b[2:] + b[:2], inv(a)) == k
            n += 1
    print(f"selftest passed: {n} dump states found in key file, round trips and Sigma invariance ok")
    return 0


def main(argv):
    if len(argv) >= 4 and argv[1] == "--selftest":
        return selftest(argv[2], argv[3])
    if len(argv) >= 8 and argv[1] == "triage":
        names = ["hump16", "hump18", "hump20", "ak3", "ms2a", "ms2b"]
        files = dict(zip(names, argv[4:]))
        rows = triage(argv[2], argv[3], files)
        out = os.environ.get("L_TRIAGE_OUT")
        if out:
            with open(out, "w") as f:
                for r in rows:
                    f.write(" ".join(map(str, r)) + "\n")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
