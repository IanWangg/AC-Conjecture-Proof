#!/usr/bin/env python3
"""th02_survey.py (agent TH02): stabilizers Stab[r] (in GL2(Z) = Out(F2)) of all
relators r occurring in a state dump, by BFS through Whitehead level sets.

Lemma 0 of research-th02: an element phi of Stab[r] is realized on (r,s) iff
phi(s) ~ s^{+-1} in F/<<r>>.  This survey lists which relators have a stabilizer
larger than {+-I} and which matrices occur, i.e. where the vertex mechanism
could possibly produce something.  It does NOT test condition (b).

Usage: python3 experiments/th02_survey.py --self-test
       python3 experiments/th02_survey.py DUMP [maxlen]
"""
import sys
sys.dont_write_bytecode = True
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from th02_scan import (INV, MAPS, cycred, mmul, minv, reduce_word, _signed_perms, hidden_reflection, D6)

I2 = ((1, 0), (0, 1))


def canon(u):
    inv = "".join(INV[c] for c in reversed(u))
    return min(t[k:] + t[:k] for t in (u, inv) for k in range(len(u)))


def stab_min(w0, limit=4000):
    """stabilizer matrices of the minimal cyclic word w0 (canonical); None if > limit states."""
    L = len(w0); moves = MAPS + _signed_perms()
    seen = {(w0, I2)}; todo = [(w0, I2)]
    while todo:
        c, M = todo.pop()
        for m, mat in moves:
            q = cycred("".join(m.get(ch, ch) for ch in c))
            if len(q) == L:
                st = (canon(q), mmul(mat, M))
                if st not in seen:
                    seen.add(st); todo.append(st)
                    if len(seen) > limit:
                        return None
    return {M for c, M in seen if c == w0}


def kind(M):
    det = M[0][0] * M[1][1] - M[0][1] * M[1][0]; tr = M[0][0] + M[1][1]
    m2 = tuple(tuple(e % 2 for e in r) for r in M)
    sgn = 1 if m2 in (((1, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (1, 0))) else -1
    return det, tr, det * sgn


def survey(path, maxlen):
    cache = {}; words = set()
    for line in open(path):
        p = line.split()
        words.update(w for w in p[:2] if len(w) <= maxlen)
    stats = {}; big = {}; infinite = 0
    for w in words:
        m, M = reduce_word(w); c = canon(m)
        # stabilizer of c, transported to w: c = pi(m) for a rotation/inversion only, so same matrices
        if c not in cache:
            cache[c] = stab_min(c)
        S = cache[c]
        if S is None:
            infinite += 1; continue
        Sw = {mmul(minv(M), mmul(g, M)) for g in S}
        stats[len(Sw)] = stats.get(len(Sw), 0) + 1
        hr = hidden_reflection(w)
        for g in Sw:
            if g in (I2, ((-1, 0), (0, -1))):
                continue
            if hr and g in (hr[0], tuple(tuple(-e for e in r) for r in hr[0])):
                continue
            big.setdefault((kind(g), g in D6), []).append((w, g))
    print("distinct relator words of length <= %d: %d; minimal forms %d; infinite stabilizers %d"
          % (maxlen, len(words), len(cache), infinite))
    print("stabilizer orders (count of words):", dict(sorted(stats.items())))
    print("stabilizer elements other than +-I and +-(hidden reflection), by (det, trace, chi), inD6:")
    for k, v in sorted(big.items()):
        print("  ", k, "count", len(v), "e.g.", v[0])
    if not big:
        print("   none")


def self_test():
    assert stab_min(canon("xxxyyyy")) == {I2, ((-1, 0), (0, -1))}
    assert len(stab_min(canon("xxyyyyy"))) == 4
    assert stab_min(canon("x")) is None
    assert kind(((0, 1), (1, 0))) == (-1, 0, 1) and kind(((-1, 0), (0, 1))) == (-1, 0, -1)
    assert kind(((1, 0), (1, 1))) == (1, 2, -1)
    # the commutator is fixed by everything: infinite
    assert stab_min(canon("xyXY")) is None
    print("th02_survey self-test OK")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    elif len(sys.argv) > 1:
        survey(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 16)
    else:
        print(__doc__)
