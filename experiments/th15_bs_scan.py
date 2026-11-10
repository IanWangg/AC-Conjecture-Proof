#!/usr/bin/env python3
"""TH15: scan a dump of states ("w1 w2 ..." per line) for relators of Baumslag-Solitar type,
i.e. cyclic words theta(x^-1 y^m x y^-n') with theta in Aut(F2).  By research-th15 Lemma T such a
relator with m != n' carries a hidden transvection, so the stabilizer of the class is infinite.

Recognizer: greedy Whitehead reduction of the single cyclic word by x->xy^(+-1), y->yx^(+-1)
(rank 2: a non-minimal cyclic word is shortened by one of them); the minimal words of the orbit of
x^-1 y^m x y^-n' (|m|+|n'| > 2) are its signed-permutation images, i.e. exactly the cyclic words
containing one generator exactly twice, once with each sign.  Sound always; complete by
Whitehead's theorem (classical) for |m|+|n'| > 2.

    python3 experiments/th15_bs_scan.py --selftest
    python3 experiments/th15_bs_scan.py DUMP        (reads only the first two columns)
"""
import sys
sys.dont_write_bytecode = True
INV = {"x": "X", "X": "x", "y": "Y", "Y": "y"}
MAPS = [{"x": "xy", "X": "YX"}, {"x": "xY", "X": "yX"}, {"y": "yx", "Y": "XY"}, {"y": "yX", "Y": "xY"}]


def cycred(w):
    out = []
    for c in w:
        if out and out[-1] == INV[c]:
            out.pop()
        else:
            out.append(c)
    i, j = 0, len(out) - 1
    while i < j and out[i] == INV[out[j]]:
        i += 1
        j -= 1
    return "".join(out[i:j + 1])


def minimal(w):
    w = cycred(w)
    improved = True
    while improved:
        improved = False
        for m in MAPS:
            q = cycred("".join(m.get(c, c) for c in w))
            if len(q) < len(w):
                w, improved = q, True
                break
    return w


def bs_type(w):
    """None, or (m, n') up to the obvious symmetries if w is of Baumslag-Solitar type."""
    w = minimal(w)
    for g, G, h, H in (("x", "X", "y", "Y"), ("y", "Y", "x", "X")):
        if w.count(g) == 1 and w.count(G) == 1 and len(w) > 2:
            r = w[w.index(G):] + w[:w.index(G)]          # G h^i g h^j
            k = r.index(g)
            a, b = r[1:k], r[k + 1:]
            i = len(a) if set(a) <= {h} else -len(a)
            j = len(b) if set(b) <= {h} else -len(b)
            if len(set(a)) == 1 and len(set(b)) <= 1:
                return (i, -j)
    return None


def selftest():
    import random
    rnd = random.Random(7)
    def rand_aut(w, steps):
        for _ in range(steps):
            m = rnd.choice(MAPS + [{"x": "y", "y": "x", "X": "Y", "Y": "X"}, {"x": "X", "X": "x"}])
            w = cycred("".join(m.get(c, c) for c in w))
        return w
    for m, n2 in [(1, 2), (2, 3), (3, 4), (4, 3), (2, 5), (3, -2), (5, 6)]:
        base = "X" + ("y" * m) + "x" + ("Y" * n2 if n2 > 0 else "y" * (-n2))
        for _ in range(200):
            assert bs_type(rand_aut(base, rnd.randint(0, 6))) is not None, (m, n2)
    for w in ("xyxYXY", "xxxYYYY", "xxxxyXy", "xyyyxYY", "xyxYYXy", "xxyyy", "xxxYXyy"):
        assert bs_type(w) is None, w
    print("selftest passed: 1400 random automorphic images of 7 BS relators recognized; "
          "braid, torus, T(a;p,q)-type and K's relators rejected")


def scan(path):
    cache, hits, nstates, nhit_states = {}, {}, 0, 0
    for line in open(path):
        p = line.split()
        if len(p) < 2:
            continue
        nstates += 1
        found = False
        for w in p[:2]:
            if w not in cache:
                cache[w] = bs_type(w)
            t = cache[w]
            if t is not None:
                found = True
                key = tuple(sorted(map(abs, t)))
                if key not in hits:
                    hits[key] = [0, (p[0], p[1])]
                hits[key][0] += 1
        nhit_states += found
    print(f"{path}: {nstates} states, {len(cache)} distinct relator words, "
          f"{nhit_states} states with a relator of Baumslag-Solitar type")
    for key in sorted(hits):
        print(f"  BS type {{|m|,|n'|}} = {key}: {hits[key][0]} occurrences, e.g. {hits[key][1]}")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        for f in sys.argv[1:]:
            scan(f)
