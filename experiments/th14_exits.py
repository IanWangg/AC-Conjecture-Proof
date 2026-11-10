"""TH14 experiment: stable exits for rank-2 presentations (research-th14.md, section 5).

For a pair (a,b) and every conjugator g with |g| <= L (both orders of the pair), let K = <g a g^-1, b>.
  exit E1 (Theorem B'): K has corank <= 1, i.e. <K,t> = F2 for some t  ==> (a,b) is AC-trivial after ONE
          stabilization.
  exit E2 (Theorems B, B2): a proper rank-2 subgroup H = <p,q> > K, so (gag^-1, b) = W o (p,q); reported with
          the rewriting W, the basis P = (p,q), their cyclic lengths, and whether H has corank <= 1.
Usage:  python3 experiments/th14_exits.py L [--members FILE | --pair a b]     (default: AK(3) class members
        read from the certificates of this repository)
        python3 experiments/th14_exits.py --selftest
"""
import glob
import json
import os
import sys
from th14_stallings import (stallings, rank, is_rose, corank1, quotients, basis_and_rewriter, subst,
                            words_upto, red, inv, cyc)

AK3 = ('xxxYYYY', 'xyxYXY')


def members_from_certificates():
    mem = {AK3}
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'certificates')
    for f in sorted(glob.glob(os.path.join(root, '*.json'))):
        try:
            c = json.load(open(f))
        except Exception:
            continue
        if c.get('format') != 'ordinary-ac-elementary-v1':
            continue
        s, t = tuple(cyc(w) for w in c['start']), tuple(cyc(w) for w in c['target'])
        key = lambda p: tuple(sorted(p))
        if key(s) == key(AK3) or key(t) == key(AK3):
            mem.add(s)
            mem.add(t)
    return sorted(mem, key=lambda p: (len(p[0]) + len(p[1]), p))


def scan(pair, L, verbose=True):
    """Returns (number of subgroups tested, list of E1 hits, list of E2 hits)."""
    e1, e2, n = [], [], 0
    for a, b in (pair, pair[::-1]):
        for g in words_upto(L):
            ga = red(g + a + inv(g))
            G = stallings([ga, b])
            n += 1
            if rank(G) != 2:
                continue
            if corank1(G) is not None:
                e1.append((ga, b))
            for H in quotients(G):
                if rank(H) == 2 and not is_rose(H) and H != G:
                    basis, rw = basis_and_rewriter(H)
                    W = (rw(ga), rw(b))
                    assert subst(W[0], *basis) == ga and subst(W[1], *basis) == red(b)
                    e2.append((ga, b, tuple(basis), W, corank1(H) is not None))
    return n, e1, e2


def report(pair, L):
    n, e1, e2 = scan(pair, L)
    best = None
    for ga, b, P, W, c1 in e2:
        lw = len(cyc(W[0])) + len(cyc(W[1]))
        lp = len(cyc(P[0])) + len(cyc(P[1]))
        if best is None or (lw, lp) < best[0]:
            best = ((lw, lp), ga, b, P, W, c1)
    print(json.dumps({'pair': pair, 'len': len(pair[0]) + len(pair[1]), 'L': L, 'subgroups': n,
                      'E1_hits': len(e1), 'E2_hits': len(e2), 'E1_first': e1[:1],
                      'E2_best': best}))
    return e1, e2


def selftest():
    # E1 positive control: (x^-2 y^-1 x, y) is corank 1 (t = x) -- and has a primitive relator anyway
    _, e1, _ = scan(('XXYx', 'y'), 0)
    assert e1
    # E2 positive control: U o (p,q) with U = AK(2)-like pair and (p,q) = (x, y x^2 y^-1 ... ) must be detected
    U = ('xxYYY', 'xyxYXY')
    p, q = 'xx', 'yXXX'           # <xx, yXXX>: unimodular, proper subgroup of rank 2
    V = (subst(U[0], p, q), subst(U[1], p, q))
    _, _, e2 = scan(V, 0)
    assert any(set(P) == {'xx', 'yx'} and c1 and (subst(W[0], *P), subst(W[1], *P)) == (ga, b)
               for (ga, b, P, W, c1) in e2), e2
    # negative control: the standard basis and AK(3) with L = 0
    n, e1, e2 = scan(AK3, 0)
    assert not e1 and not e2
    print('th14_exits self-test passed')


if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        selftest()
    else:
        L = int(sys.argv[1])
        if '--pair' in sys.argv:
            i = sys.argv.index('--pair')
            mems = [(sys.argv[i + 1], sys.argv[i + 2])]
        else:
            mems = members_from_certificates()
        tot1 = tot2 = 0
        for m in mems:
            e1, e2 = report(m, L)
            tot1 += len(e1)
            tot2 += len(e2)
        print('# members', len(mems), 'L', L, 'E1 hits', tot1, 'E2 hits', tot2)
