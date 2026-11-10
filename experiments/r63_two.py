#!/usr/bin/env python3
"""R6-3: two-move census of P_3 = (c, k_3) through c-frozen neighbours (c, k') with |k'| = 10, 11.
Step 1 (first move, c frozen): k' cyclically reduced, y-exponent 1, I(k') = 20 (TH03 T2), eps(k') = eps(k_3) (T16),
  J(k') = J(k_3) at two rational points (T6); survivors are confirmed conjugate to k_3 in G_c by explicit
  twisted-conjugacy BFS (bidirectional, normal-form length caps), else 'undecided'.
Step 2 (second move, k' frozen): is c conjugate in G_{k'} to a primitive x t^j (t = y x^m), or to the inverse of a
  BS(1,2)-type killer (research-th09 Thm 3(d)): Q Q P^-1 Q^-1 P ('bs+') or Q Q P Q^-1 P^-1 ('bs-'), Q = x t^j, P = t?
  Decided with twisted traces (TH03 Lemma T11a): rational (values are polynomials of degree <= D in j),
  F_2 (period 8, D <= 7), F_p (period p^e > D).  Usage: r63_two.py [--selftest] [L ...]"""
import itertools, sys, time
from collections import deque
from fractions import Fraction as Fr
import th03_uniform as t, th03_q2 as q, th03_two as tw

C, K3 = 'xyxYYXy', 'xxxYXyy'

def cyc_words(L):
    """cyclically reduced words of length L, y-exponent 1, lexicographically least rotation."""
    inv = {'x': 'X', 'X': 'x', 'y': 'Y', 'Y': 'y'}
    def rec(w):
        if len(w) == L:
            if w[-1] != inv[w[0]]: yield w
            return
        for ch in 'xXyY':
            if not w or ch != inv[w[-1]]: yield from rec(w + ch)
    for w in rec(''):
        if w.count('y') - w.count('Y') != 1: continue
        if min(w[i:] + w[:i] for i in range(L)) != w: continue
        yield w

def bfs(u0, cap, limit=400000):
    seen, dq = {u0: None}, deque([u0])
    while dq and len(seen) < limit:
        u = dq.popleft()
        for w in [t.phi(u)] + [t.red(v + u + t.inv(t.phi(v))) for v in 'aAbB']:
            if len(w) <= cap and w not in seen: seen[w] = u; dq.append(w)
    return seen

def census(L, C1, pts, Jk, e0, cap2=None):
    out = {}
    for w in cyc_words(L):
        u, k = t.nf(w); assert k == 1
        if t.I(u) != 20: continue
        if tw.eps(u) != e0: tag = 'eps'                      # mirror class, excluded by T16
        elif [t.J(p, u) for p in pts] != Jk: tag = 'J'
        elif u in C1: tag = 'k3'
        else:
            S = bfs(u, cap2 or max(len(u) + 2, 15))
            tag = 'k3' if any(v in C1 for v in S) else 'undecided'
        out.setdefault(tag, []).append(w)
    return out

# ------------------------------------------------------------------ second move
def tpow(m, j):
    tt = 'y' + ('x' * m if m >= 0 else 'X' * (-m))
    return tt * j if j >= 0 else t.inv(tt) * (-j)
def fam(kind, m, j):
    Q, P = 'x' + tpow(m, j), tpow(m, 1)
    Qi, Pi = t.inv(Q), t.inv(P)
    return {'prim': Q, 'bs+': Q + Q + Pi + Qi + P, 'bs-': Q + Q + P + Qi + Pi}[kind]
KINDS = ('prim', 'bs+', 'bs-')

def rational_test(st, D, moved=C, NF=None):
    NF = NF or tw.nf_general
    G = tw.Gen(st[3], D); m = st[0]
    uc, kc = NF(moved, st); assert kc == 1
    ic = G.Inv(uc); res = {}
    for kind in KINDS:
        vals = []
        for j in range(D + 1):
            u, k = NF(fam(kind, m, j), st); assert k == 1; vals.append(G.Inv(u))
        cand = None
        for rr in range(len(G.traces)):
            v = [vals[j][rr] for j in range(D + 1)]
            poly = []                                            # Newton forward differences = binomial basis
            while v: poly.append(v[0]); v = [v[i + 1] - v[i] for i in range(len(v) - 1)]
            poly[0] -= ic[rr]
            if any(poly):
                rts = set(q.integer_roots(poly)); cand = rts if cand is None else cand & rts
        res[kind] = 'all' if cand is None else sorted(cand)
    return len(G.traces), res

def modp_test(st, D, p, moved=C, NF=None):
    NF = NF or tw.nf_general
    G = tw.Gen(st[3], D, rational=False); m = st[0]
    B = tw.traces_modp(G, p)
    per = p
    while per <= D: per *= p
    ev = lambda u: tuple(sum(l[G.idx[mm]] * c for mm, c in G.magnus(u).items()) % p for l in B)
    uc, kc = NF(moved, st); assert kc == 1
    ic = ev(uc); res = {}
    for kind in KINDS:
        res[kind] = [j for j in range(per) if ev(NF(fam(kind, m, j), st)[0]) == ic]
    return len(B), per, res

def structure_asc(k):
    """Brown fails but the top t-level occurs once: G_k is the mapping torus of the injective endomorphism
    theta (t_i -> t_{i+1}, t_{r-1} -> solution for t_r) of F(t_0..t_{r-1}) (Magnus-Moldavanskii, Freiheitssatz)."""
    m = k.count('x') - k.count('X')
    sub = {'x': 'x', 'X': 'X', 'y': 't' + ('X' * m if m >= 0 else 'x' * (-m)),
           'Y': ('x' * m if m >= 0 else 'X' * (-m)) + 'T'}
    lev, seq = 0, []
    for ch in "".join(sub[c] for c in k):
        if ch == 'x': lev += 1
        elif ch == 'X': lev -= 1
        else: seq.append((1 if ch == 't' else -1, lev))
    red = []
    for g in seq:
        if red and red[-1][1] == g[1] and red[-1][0] == -g[0]: red.pop()
        else: red.append(g)
    while len(red) >= 2 and red[0][1] == red[-1][1] and red[0][0] == -red[-1][0]: red = red[1:-1]
    lo = min(i for _, i in red); r = max(i for _, i in red) - lo
    seq = [(e, i - lo) for e, i in red]
    if sum(i == r for _, i in seq) != 1: return None
    p = next(a for a, (e, i) in enumerate(seq) if i == r); e = seq[p][0]
    rest = tuple(s_ * (i + 1) for s_, i in seq[p + 1:] + seq[:p])
    images = [(i + 2,) for i in range(r - 1)] + [q.inv(rest) if e == 1 else rest]
    return m, lo, r, images, None, sub
def nf_asc(word, st):
    m, lo, r, images, _, sub = st
    def ap(w):
        out = []
        for g in w:
            im = images[abs(g) - 1]; out.extend(im if g > 0 else q.inv(im))
        return q.red(out)
    lv, mn = 0, 0
    for ch in "".join(sub[c] for c in word):
        if ch == 'x': lv += 1
        elif ch == 'X': lv -= 1
        else: mn = min(mn, lv)
    sh = -mn                                           # conjugate by a power of x: every t-letter at level >= 0
    pre = 'x' * sh if sh >= 0 else 'X' * (-sh)
    u, k = (), 0
    for ch in pre + "".join(sub[c] for c in word) + pre.swapcase():
        if ch == 'x': k += 1
        elif ch == 'X': k -= 1
        else:
            assert k >= 0
            g = (1,) if ch == 't' else (-1,)
            for _ in range(k): g = ap(g)
            u = q.red(u + g)
    return u, k
def second(kp, log):
    st, NF, mv = tw.structure(kp), tw.nf_general, C
    if st is None:
        st, NF = structure_asc(kp), nf_asc
        if st is None:      # bottom level unique: apply sigma (x <-> X); the three families are sigma+inverse stable
            kp = kp.translate(str.maketrans('xX', 'Xx')); mv = t.inv(C.translate(str.maketrans('xX', 'Xx')))
            st = structure_asc(kp)
            if st is None: log("  %s: Brown fails, no unique extreme level -> not handled" % kp); return None
            log("  sigma(k') = %s, moved relator sigma(c)^-1 = %s" % (kp, mv))
        log("  %s: ascending HNN (top t-level once)" % kp)
    assert NF(kp, st) == ((), 0)
    r = st[2]; open_ = set(KINDS); log("  %s: m=%d rank=%d" % (kp, st[0], r))
    for D in (3, 4):
        if r ** D > 300: break
        nt, res = rational_test(st, D, moved=mv, NF=NF); log("    rational D=%d: %d traces, surviving j: %s" % (D, nt, res))
        open_ = {k for k in open_ if res[k] != []}
        if not open_: return 'excluded'
    for p, D in [(2, 4), (2, 5), (2, 6), (3, 3), (5, 3), (7, 3), (3, 4), (2, 7), (3, 5), (3, 6), (5, 5), (2, 8), (3, 8)]:
        if r ** D > 3000: continue
        nb, per, res = modp_test(st, D, p, moved=mv, NF=NF); res = {k: res[k] for k in open_}
        log("    F_%d D=%d: %d traces, surviving j mod %d: %s" % (p, D, nb, per, res))
        open_ = {k for k in open_ if res[k] != []}
        if not open_: return 'excluded'
    return 'open:' + ",".join(sorted(open_))

def selftest(log):
    # positive controls: a member of each family is found by the family test, for one target with Brown OK
    kp = 'XyyxYYxy'; st = tw.structure(kp)
    for kind in KINDS:
        w = fam(kind, st[0], 2)
        nt, res = rational_test(st, 3, moved=w); assert res[kind] == 'all' or 2 in res[kind], (kind, res)
        nb, per, res2 = modp_test(st, 4, 2, moved=w); assert 2 % per in res2[kind], (kind, res2)
    # TH03 T14 lengths <= 9 reproduced
    log("selftest ok (family controls)")

if __name__ == '__main__':
    t0 = time.time(); log = lambda s: (print(s, flush=True))
    args = sys.argv[1:]
    if '--selftest' in args: selftest(log); args.remove('--selftest')
    pts = [t.rational_point(2), t.rational_point(3)]
    u3, _ = t.nf(K3); Jk = [t.J(p, u3) for p in pts]; e0 = tw.eps(u3)
    C1 = bfs(u3, int(dict(a.split('=') for a in args if '=' in a).get('cap', 15)))
    log("class of k3: %d normal forms (cap)" % len(C1))
    for L in [int(a) for a in args if '=' not in a]:
        out = census(L, C1, pts, Jk, e0)
        log("L=%d: %s  (%.0fs)" % (L, {k: len(v) for k, v in out.items()}, time.time() - t0))
        for tag in ('k3', 'undecided'): log("  %s: %s" % (tag, out.get(tag, [])))
        for kp in out.get('k3', []) + out.get('undecided', []):
            log("  second move %s -> %s" % (kp, second(kp, log)))
