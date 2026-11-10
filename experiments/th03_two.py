#!/usr/bin/env python3
"""Agent TH03: (1) the degree-4 twisted trace L4 on G_c; (2) the exact list of short c-frozen
neighbours of P_3; (3) the second move (k' frozen) for the neighbours of length <= 9.

Uses th03_uniform (I, J, normal forms in G_c) and th03_q2 (twisted traces).
    python3 experiments/th03_two.py --selftest        (about 1 minute)
"""
import itertools
import random
import sys
from collections import deque

sys.dont_write_bytecode = True
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
import th03_q2 as q
import th03_uniform as t

class Gen(q.GK):
    """F(t_0..t_{r-1}) with an endomorphism given by the images of the generators."""
    def __init__(self, images, D, rational=True):
        self.images, self.n, self.D = images, len(images), D
        self.mons = [m for d in range(D + 1) for m in itertools.product(range(self.n), repeat=d)]
        self.idx = {m: i for i, m in enumerate(self.mons)}
        self.PsiX = [self.magnus(im) for im in images]
        for P in self.PsiX: P[()] = P.get((), 0) - 1
        self.traces = self._traces() if rational else None
    def psi(self, w):
        out = []
        for g in w:
            im = self.images[abs(g) - 1]; out.extend(im if g > 0 else q.inv(im))
        return q.red(out)

def traces_mod2(G):
    rows = []
    for r in q.relations(G):
        b = 0
        for m, c in r.items():
            if c % 2: b |= 1 << G.idx[m]
        if b: rows.append(b)
    piv = {}
    for b in rows:
        while b:
            c = b.bit_length() - 1
            if c in piv: b ^= piv[c]
            else: piv[c] = b; break
    basis = []
    for fc in (c for c in range(len(G.mons)) if c not in piv):
        l = 1 << fc
        for c in sorted(piv):
            if bin(piv[c] & l & ~(1 << c)).count("1") % 2: l |= 1 << c
        assert all(bin(b & l).count("1") % 2 == 0 for b in rows)
        basis.append(l)
    return basis
def ev2(G, basis, u):
    P = G.magnus(u)
    return tuple(sum(c for m, c in P.items() if (l >> G.idx[m]) & 1) % 2 for l in basis)

# ---------------------------------------------------------------- (1) L4 on G_c = F(a,b) x|_phi Z
L4 = {'ba': 1, 'aaa': 1, 'aab': 1, 'aba': -1, 'abb': 1, 'baa': 2, 'bab': -1, 'bba': 3, 'bbb': 1, 'aaaa': 1,
      'aaab': 1, 'aaba': -1, 'aabb': 1, 'abaa': -2, 'abab': -1, 'abbb': 1, 'baab': -2, 'baba': -1,
      'babb': -1, 'bbaa': 2, 'bbba': 2, 'bbbb': 1}
def W(s): return tuple({'a': 1, 'A': -1, 'b': 2, 'B': -2}[ch] for ch in s)
def l4_setup():
    G = Gen([(2,), (-2, 1)], 4)                       # phi(a) = b, phi(b) = B a
    l = [q.Fr(L4.get("".join('ab'[i] for i in m), 0)) for m in G.mons]
    assert all(G.ev(l, r) == 0 for r in q.relations(G))
    return G, (lambda s: G.ev(l, G.magnus(W(s))))

# ---------------------------------------------------------------- (2) short words with I = 20
def bfs_class(u0, L=13):
    seen, dq = {u0}, deque([u0])
    while dq:
        u = dq.popleft()
        nb = [t.phi(u)] + [t.red(v + u + t.inv(t.phi(v))) for v in 'aAbB']
        for w in nb:
            if len(w) <= L and w not in seen: seen.add(w); dq.append(w)
    return seen
def census(maxlen=9):
    pts = [t.rational_point(2), t.rational_point(3)]
    Jk = [t.J(p, 'aaaBA') for p in pts]
    C1, C2 = bfs_class('aaaBA'), bfs_class('AAba')
    assert not (C1 & C2)
    out = {}
    for L in range(1, maxlen + 1):
        for tup in itertools.product('xXyY', repeat=L):
            w = "".join(tup)
            if w.count('y') - w.count('Y') != 1: continue
            if any(w[i] == w[(i + 1) % L].swapcase() for i in range(L)): continue
            if min(w[i:] + w[:i] for i in range(L)) != w: continue
            u, k = t.nf(w)
            if t.I(u) != 20: continue
            if u in C1: tag = 'k3'
            elif u in C2: tag = 'mirror'
            elif [t.J(p, u) for p in pts] == Jk: tag = 'undecided'
            else: tag = 'excluded'
            out.setdefault((L, tag), []).append(w)
    return out

# ---------------------------------------------------------------- (3) Magnus rewriting of <x,y | k'>
def structure(k):
    """k' of y-exponent 1 and x-exponent m: t = y x^m, t_i = x^i t x^-i.  Returns
    (m, lo, rank, images, inverse images) if the extreme t_i occur once each (Brown), else None."""
    m = k.count('x') - k.count('X'); assert k.count('y') - k.count('Y') == 1
    sub = {'x': 'x', 'X': 'X', 'y': 't' + ('X' * m if m >= 0 else 'x' * (-m)),
           'Y': ('x' * m if m >= 0 else 'X' * (-m)) + 'T'}
    lev, seq = 0, []
    for ch in "".join(sub[c] for c in k):
        if ch == 'x': lev += 1
        elif ch == 'X': lev -= 1
        else: seq.append((1 if ch == 't' else -1, lev))
    assert lev == 0
    red = []
    for g in seq:
        if red and red[-1][1] == g[1] and red[-1][0] == -g[0]: red.pop()
        else: red.append(g)
    while len(red) >= 2 and red[0][1] == red[-1][1] and red[0][0] == -red[-1][0]: red = red[1:-1]
    lo = min(i for _, i in red); r = max(i for _, i in red) - lo
    seq = [(e, i - lo) for e, i in red]
    if sum(i == r for _, i in seq) != 1 or sum(i == 0 for _, i in seq) != 1: return None
    def solve(idx, shift):
        p = next(a for a, (e, i) in enumerate(seq) if i == idx); e = seq[p][0]
        rest = tuple(s * (i + 1 - shift) for s, i in seq[p + 1:] + seq[:p])
        return q.inv(rest) if e == 1 else rest
    images = [(i + 2,) for i in range(r - 1)] + [solve(r, 0)]
    inv_images = [solve(0, 1)] + [(i,) for i in range(1, r)]
    def ap(imgs, w):
        out = []
        for g in w:
            im = imgs[abs(g) - 1]; out.extend(im if g > 0 else q.inv(im))
        return q.red(out)
    for g in range(1, r + 1):                          # psi is an automorphism with inverse inv_images
        assert ap(images, ap(inv_images, (g,))) == (g,) == ap(inv_images, ap(images, (g,)))
    return m, lo, r, images, inv_images, sub
def nf_general(word, st):
    m, lo, r, images, inv_images, sub = st
    def ap(imgs, w):
        out = []
        for g in w:
            im = imgs[abs(g) - 1]; out.extend(im if g > 0 else q.inv(im))
        return q.red(out)
    pre = 'X' * lo if lo >= 0 else 'x' * (-lo)
    u, k = (), 0
    for ch in pre + "".join(sub[c] for c in word) + pre.swapcase():
        if ch == 'x': k += 1
        elif ch == 'X': k -= 1
        else:
            g = (1,) if ch == 't' else (-1,)
            for _ in range(abs(k)): g = ap(images, g) if k > 0 else ap(inv_images, g)
            u = q.red(u + g)
    return u, k
def second_move(kp, D, mod2=False, moved='xyxYYXy'):
    """Is `moved` (default c) conjugate in <x,y | k'> to a primitive x t^j ?  Returns the list of
    surviving j (rational traces: all integers j; mod 2: residues mod 8), or None if not handled."""
    st = structure(kp)
    if st is None: return None
    assert nf_general(kp, st) == ((), 0)
    uc, kc = nf_general(moved, st); assert kc == 1
    G = Gen(st[3], D, rational=not mod2)
    if mod2:
        assert D < 8
        B = traces_mod2(G); ic = ev2(G, B, uc)
        return [j for j in range(8) if ev2(G, B, (2,) * j) == ic]
    ic, co, cand = G.Inv(uc), G.power_poly(1), None
    for rr in range(len(G.traces)):
        poly = [co[k_][rr] for k_ in range(D + 1)]; poly[0] -= ic[rr]
        if any(poly):
            rts = set(q.integer_roots(poly)); cand = rts if cand is None else cand & rts
    return None if cand is None else sorted(cand)

def traces_modp(G, p):
    """F_p-valued twisted traces (numpy elimination); used for the ascending-HNN target of T15."""
    import numpy as np
    rows = q.relations(G); N = len(G.mons)
    M = np.zeros((len(rows), N), dtype=np.int64)
    for a, r in enumerate(rows):
        for m, c in r.items(): M[a, G.idx[m]] = c % p
    piv, r0 = [], 0
    for c in range(N):
        nz = np.nonzero(M[r0:, c])[0]
        if len(nz) == 0: continue
        pr = r0 + int(nz[0])
        if pr != r0: M[[r0, pr]] = M[[pr, r0]]
        M[r0] = (M[r0] * pow(int(M[r0, c]), p - 2, p)) % p
        col = M[:, c].copy(); col[r0] = 0
        nzr = np.nonzero(col)[0]
        if len(nzr): M[nzr] = (M[nzr] - np.outer(col[nzr], M[r0])) % p
        piv.append(c); r0 += 1
        if r0 == len(rows): break
    basis = []
    for fc in (c for c in range(N) if c not in set(piv)):
        l = [0] * N; l[fc] = 1
        for i, c in enumerate(piv): l[c] = int(-M[i, fc]) % p
        basis.append(l)
    for l in basis:                                    # verify: every relation is killed
        assert all(sum(l[G.idx[m]] * c for m, c in r.items()) % p == 0 for r in rows)
    return basis

def second_move_ascending(D=8, p=3):
    """k' = XYYxyxyXy: y-exponent 1, x-exponent 0, relator T_{-1}T_{-1} t_0 t_1 t_0 (t = y, t_i = x^i t x^-i):
    Brown fails (t_{-1} twice); G_{k'} is the mapping torus of the injective endomorphism
    theta(t_0) = t_1, theta(t_1) = T_1 t_0 t_0 T_1 of F(t_0,t_1).  Degree-1 elements f x, f' x are
    conjugate only if f' = v f theta(v)^-1, so twisted traces apply.  Returns the surviving j mod p^e."""
    images = [(2,), (-2, 1, 1, -2)]
    G = Gen(images, D, rational=False)
    def nf_asc(word):                                  # conjugate by x so that all levels are >= 0
        u, k = (), 0
        for ch in 'x' + word.replace('y', 't').replace('Y', 'T') + 'X':
            if ch == 'x': k += 1
            elif ch == 'X': k -= 1
            else:
                assert k >= 0
                g = (1,) if ch == 't' else (-1,)
                for _ in range(k): g = G.psi(g)
                u = q.red(u + g)
        return u, k
    assert nf_asc('XYYxyxyXy') == ((), 0)
    uc, kc = nf_asc('xyxYYXy'); assert kc == 1
    B = traces_modp(G, p)
    ev = lambda u: tuple(sum(l[G.idx[m]] * c for m, c in G.magnus(u).items()) % p for l in B)
    e = 1
    while p ** e <= D: e += 1
    ic = ev(uc)
    return len(B), [j for j in range(p ** e) if ev(nf_asc('x' + 'y' * j)[0]) == ic]

def second_move_mod9(kp, D=3, period=None):
    """Z/9-valued twisted traces for a target k' satisfying Brown's criterion: F_3-valued traces l0 are
    lifted to l = l0 + 3 l1 with R l = 0 (mod 9) (R the integer relation matrix; verified), and the
    invariants of c and of x t^j are compared for all j mod 27 ((1+X)^27 = 1 mod (9, X^4)).
    Returns (number of F_3-traces, number of independent lifts, surviving j mod 27)."""
    import numpy as np
    assert D <= 3
    def null_mod(M, p):
        M = M.copy() % p; R_, N_ = M.shape; piv, r0 = [], 0
        for c in range(N_):
            nz = np.nonzero(M[r0:, c])[0]
            if len(nz) == 0: continue
            pr = r0 + int(nz[0])
            if pr != r0: M[[r0, pr]] = M[[pr, r0]]
            M[r0] = (M[r0] * pow(int(M[r0, c]), p - 2, p)) % p
            col = M[:, c].copy(); col[r0] = 0
            nzr = np.nonzero(col)[0]
            if len(nzr): M[nzr] = (M[nzr] - np.outer(col[nzr], M[r0])) % p
            piv.append(c); r0 += 1
            if r0 == R_: break
        ps, basis = set(piv), []
        for fc in (c for c in range(N_) if c not in ps):
            l = np.zeros(N_, dtype=np.int64); l[fc] = 1
            for i, c in enumerate(piv): l[c] = (-M[i, fc]) % p
            basis.append(l)
        return basis
    st = structure(kp); assert st is not None and nf_general(kp, st) == ((), 0)
    uc, kc = nf_general('xyxYYXy', st); assert kc == 1
    G = Gen(st[3], D, rational=False); rows = q.relations(G); N = len(G.mons)
    per = 27 if period is None else period
    R = np.zeros((len(rows), N), dtype=np.int64)
    for a, rr in enumerate(rows):
        for m, c in rr.items(): R[a, G.idx[m]] = c
    B0 = null_mod(R, 3)
    aug = np.concatenate([R % 3] + [((R.dot(l) // 3) % 3).reshape(-1, 1) for l in B0], axis=1)
    lifts = []
    for v in null_mod(aug, 3):
        if v[N:].any():
            l = (sum(int(ci) * B0[i] for i, ci in enumerate(v[N:])) + 3 * v[:N]) % 9
            assert not (R.dot(l) % 9).any()            # l is a Z/9-valued twisted trace
            lifts.append(l)
    gens = lifts + [3 * l for l in B0]
    ev = lambda u: tuple(int(sum(int(l[G.idx[m]]) * c for m, c in G.magnus(u).items()) % 9) for l in gens)
    ic = ev(uc)
    return len(B0), len(lifts), [j for j in range(per) if ev((2,) * j) == ic]

def q2_modp(n, D, p):
    """Q2(n) with F_p-valued twisted traces of degree <= D < p for psi_n: (#traces, surviving j mod p)."""
    assert D < p
    G = Gen([(i + 2,) for i in range(n - 1)] + [(n, 1)], D, rational=False)
    B = traces_modp(G, p)
    ev = lambda u: tuple(sum(l[G.idx[m]] * c for m, c in G.magnus(u).items()) % p for l in B)
    ic = ev((2, -3, -2))                               # c = (t_1 T_2 T_1, 1)
    return len(B), [j for j in range(p) if ev((2,) * j) == ic]

# ---------------------------------------------------------------- (4) the mod-2 invariant eps (mirror theorem)
def eps(u):
    """eps(u) = C(p+1,2) + C(q+1,2) + mu_ab(u) mod 2, (p,q) the exponent sums of u in a, b and
    mu_ab = sum of e_i e_j over pairs (a-letter at i) before (b-letter at j).  It is the F_2-valued
    twisted trace a + b + aa + ab + bb of degree 2 for phi, and eps(alpha(g)) = eps(g) + 1."""
    sg = lambda ch: 1 if ch.islower() else -1
    p = sum(sg(ch) for ch in u if ch in 'aA'); qq = sum(sg(ch) for ch in u if ch in 'bB')
    mu, seen_a = 0, 0
    for ch in u:
        if ch in 'aA': seen_a += sg(ch)
        else: mu += seen_a * sg(ch)
    return (p * (p + 1) // 2 + qq * (qq + 1) // 2 + mu) % 2
def alpha_nf(u): return t.red(u.swapcase() + 'b')      # alpha(u,1) = (iota(u) b, 1)

def selftest_eps():
    rnd = random.Random(13)
    G = Gen([(2,), (-2, 1)], 2, rational=False)
    l = sum(1 << G.idx[m] for m in [(0,), (1,), (0, 0), (0, 1), (1, 1)])
    for r in q.relations(G):                           # the six identities (TT) mod 2
        assert sum(c for m, c in r.items() if (l >> G.idx[m]) & 1) % 2 == 0
    for _ in range(500):
        u = t.red("".join(rnd.choice('aAbB') for _ in range(rnd.randint(0, 12))))
        v = t.red("".join(rnd.choice('aAbB') for _ in range(rnd.randint(1, 7))))
        assert eps(u) == ev2(G, [l], W(u))[0]          # closed form = Magnus evaluation
        assert eps(t.red(v + u + t.inv(t.phi(v)))) == eps(u) == eps(t.phi(u))
        assert eps(alpha_nf(u)) == (eps(u) + 1) % 2    # the mirror flips eps
        assert t.I(alpha_nf(u)) == t.I(u)
    pw = lambda s: 'a' * s if s >= 0 else 'A' * (-s)
    assert all(eps(pw(s)) == (s * (s + 1) // 2) % 2 for s in range(-20, 21))
    assert all(eps('a' * n + 'BA') == (n * (n + 1) // 2) % 2 for n in range(1, 30))
    assert eps('aBA') == eps('aaBA') == eps('AA') == 1 and eps('aaa') == 0     # k_1 ~ k_2 ~ x^-2 y, not x^3 y
    assert eps('') == eps('A') == 0 and eps('a') == eps('aa') == 1            # y ~ Xy ; xy ~ xxy
    assert eps('aaaaBA') != eps('aaaaa') and eps('aaaaaBA') != eps('AAAAA')   # (n,s) = (4,5), (5,-5)
    return True

# ---------------------------------------------------------------- (5) the k_3-frozen side: neighbours (c', k_3)
def census_b(maxlen=8, cap=13):
    """Cyclically reduced words w with lambda(w) = 1 (lambda(x) = 1, lambda(y) = -2), |w| <= maxlen,
    whose rational degree-3 twisted-trace invariant in G_{k_3} equals that of c; 'class' = found in the
    BFS class of c (explicit twisted conjugators), 'undecided' otherwise."""
    G = q.GK(3, 3)
    uc, _ = G.nf('xyxYYXy'); ic = G.Inv(uc)
    seen, dq = {uc}, deque([uc])
    while dq:
        u = dq.popleft()
        nb = [G.psi(u), G.psi_inv(u)] + [q.red((g,) + u + q.inv(G.psi((g,)))) for g in (1, 2, 3, -1, -2, -3)]
        for w in nb:
            if len(w) <= cap and w not in seen: seen.add(w); dq.append(w)
    out = {}
    for L in range(1, maxlen + 1):
        for tup in itertools.product('xXyY', repeat=L):
            w = "".join(tup)
            if (w.count('x') - w.count('X')) - 2 * (w.count('y') - w.count('Y')) != 1: continue
            if any(w[i] == w[(i + 1) % L].swapcase() for i in range(L)): continue
            if min(w[i:] + w[:i] for i in range(L)) != w: continue
            u, k = G.nf(w); assert k == 1
            if G.Inv(u) == ic: out.setdefault('class' if u in seen else 'undecided', []).append(w)
    return out
def selftest_b():
    cb = census_b(8)
    assert cb == {'class': ['XXyxYY', 'XyxyxYY', 'XXXYxyxY']}, cb      # XyxyxYY is a rotation of c
    k3 = 'xxxYXyy'; G = q.GK(3, 1)
    assert G.nf('Y' + 'xyxYYXy' + 'y' + t.inv('yxYYXX')) == ((), 0)     # Y c y = yxYYXX mod <<k_3>>
    assert G.nf('xyxYYXy' + t.inv('xyxYXXXY')) == ((), 0)               # c = xyxYXXXY mod <<k_3>>
    # second moves with c' frozen: is k_3 conjugate to a primitive in <x,y | c'> ?  (frozen word = c'^-1)
    assert second_move('yyXYxx', 6, True, moved=k3) == []               # c' = XXyxYY, mod 2, degree 6
    assert second_move('yXYXyxxx', 3, False, moved=k3) == []            # c' = XXXYxyxY, rational, degree 3
    return cb

EXPECTED = {(6, 'excluded'): 3, (7, 'k3'): 2, (7, 'mirror'): 1, (7, 'excluded'): 6, (8, 'k3'): 2, (8, 'mirror'): 4,
            (8, 'excluded'): 5, (9, 'k3'): 3, (9, 'mirror'): 6, (9, 'excluded'): 11}
K3_CLASS = ['XyyxxxY', 'XYxxyXy', 'XyyxYYxy', 'XYXyxxxy', 'XyyxYxyxY', 'XyyxYxYxy', 'XYYxyxyXy']

def selftest():
    rnd = random.Random(7)
    G, L = l4_setup()                                  # (1) L4
    pw = lambda s: 'a' * s if s >= 0 else 'A' * (-s)
    assert all(L(pw(s)) == q.binom(s + 1, 4) >= 0 for s in range(-30, 31))
    kn = [L('a' * n + 'BA') for n in range(1, 10)]
    assert kn == [1, 1, -1, -5, -10, -14, -14, -6, 15]
    assert L('aBA') == L('aaBA') == L('AA') == L('aaa') == 1          # controls: k_1 ~ k_2 ~ x^-2 y
    for _ in range(200):
        u = t.red("".join(rnd.choice('aAbB') for _ in range(rnd.randint(0, 9))))
        v = t.red("".join(rnd.choice('aAbB') for _ in range(rnd.randint(1, 6))))
        assert L(t.red(v + u + t.inv(t.phi(v)))) == L(u) == L(t.phi(u))
    cs = census(9)                                     # (2) census of words with I = 20
    assert {k: len(v) for k, v in cs.items()} == EXPECTED, {k: len(v) for k, v in cs.items()}
    k3 = [w for (Lw, tag), ws in sorted(cs.items()) if tag == 'k3' for w in ws]
    assert k3 == K3_CLASS, k3
    res = {}                                           # (3) second moves
    for kp, D, m2 in (('XyyxxxY', 3, False), ('XYXyxxxy', 3, False), ('XyyxYxyxY', 3, False),
                      ('XYxxyXy', 6, True), ('XyyxYYxy', 4, True)):
        res[kp] = second_move(kp, D, m2); assert res[kp] == [], (kp, res[kp])
    assert second_move('XYYxyxyXy', 3) is None and structure('XYYxyxyXy') is None
    assert second_move('XyyxYxYxy', 3) is None         # rank 5: only the constant trace in degree <= 3
    try:
        res['asc'] = second_move_ascending(8, 3); assert res['asc'] == (13, []), res['asc']
        res['mod9'] = second_move_mod9('XyyxYxYxy', 3); assert res['mod9'] == (3, 3, []), res['mod9']
        assert second_move_mod9('XyyxxxY', 3)[2] == []      # control: agrees with the rational result for k_3
        res['q2_7'] = q2_modp(7, 3, 7); assert res['q2_7'] == (3, []), res['q2_7']          # Q2(7)
        res['q2_8'] = second_move_mod9('x' * 8 + 'YXyy', 3); assert res['q2_8'] == (3, 3, []), res['q2_8']   # Q2(8)
    except ImportError:
        res['asc'] = res['mod9'] = res['q2_7'] = res['q2_8'] = 'numpy missing: not re-checked'
    assert selftest_eps()                              # (4) mirror theorem
    res['b'] = selftest_b()                            # (5) the k_3-frozen side
    mirror = [w for (Lw, tag), ws in cs.items() if tag == 'mirror' for w in ws]
    assert len(mirror) == 11 and all(eps(t.nf(w)[0]) == 1 for w in mirror) and eps('aaaBA') == 0
    return kn, cs, res

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        kn, cs, res = selftest()
        print("th03_two self-test passed")
        print("L4(x^s y) = C(s+1,4) >= 0;  L4(k_n), n = 1..9:", [str(a) for a in kn])
        for key in sorted(cs): print("  length %d, %-9s:" % key, len(cs[key]), cs[key] if key[1] in ('k3', 'mirror') else '')
        print("eps: twisted trace mod 2, flipped by alpha; the 11 mirror words have eps = 1 != 0 = eps(k_3): not neighbours")
        print("Q2(7): F_7-valued traces of degree 3, (#traces, surviving j mod 7) =", res['q2_7'], "; Q2(8): Z/9-valued, degree 3, (#F_3-traces, #lifts, surviving j mod 27) =", res['q2_8'])
        print("k_3-frozen neighbours (c', k_3) of P_3 with |c'| <= 8:", res['b'], "; second move excluded for each")
        print("second move (c ~ primitive in <x,y|k'>) excluded for all seven k' of T14:")
        print("  XyyxxxY (= k_3), XYXyxxxy, XyyxYxyxY: rational traces, degree 3;  XYxxyXy: mod 2, degree 6;  XyyxYYxy: mod 2, degree 4")
        print("  XYYxyxyXy (ascending HNN; mod 3, degree 8; (#traces, surviving j mod 9)):", res['asc'])
        print("  XyyxYxYxy (rank 5; Z/9-valued, degree 3; (#F_3-traces, #lifts, surviving j mod 27)):", res['mod9'])
    else:
        print(__doc__)
