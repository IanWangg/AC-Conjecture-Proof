"""R6-4: search the conjugacy class of the partner relator, in the one-relator group of the frozen
relator, for T(2,n)-type words u^2 v^n and Baumslag-Solitar-type words u^-1 v^m u v^-(m+-1)
((u,v) a basis of F reached by Nielsen moves).  Conjugacy test (exact): G = <x,y|r> with r a torus
relator is a central extension of a free product P = Z/p * Z/q by an infinite cyclic group whose
generator has nonzero image under the abelianization character chi; so g ~ g' in G iff their images
are conjugate in P (cyclically reduced normal forms agree up to rotation) and chi(g) = chi(g').
Usage: python3 r64_search.py [--self-test] [--case A|S] [--len L] [--nmax N]
"""
import sys
from itertools import product

INV = {'x': 'X', 'X': 'x', 'y': 'Y', 'Y': 'y'}
def red(w):
    out = []
    for c in w:
        if out and out[-1] == INV[c]: out.pop()
        else: out.append(c)
    return ''.join(out)
def inv(w): return ''.join(INV[c] for c in reversed(w))
def pw(w, n): return red(w * n) if n >= 0 else red(inv(w) * (-n))
def ab(w): return (w.count('x') - w.count('X'), w.count('y') - w.count('Y'))

# group specs: orders of the two factors, images of x, y (token lists), character values
SPECS = {
    # G_A, A = x^4yXy = x^5 z^2, z = Xy: P = <a>_5 * <b>_2, x -> a, y -> a b ; chi(x)=2, chi(y)=-3
    'A': dict(orders=(5, 2), x=[(0, 1)], y=[(0, 1), (1, 1)], chi=(2, -3), partner='xxxxxxxxyyyyy'),
    # G_s, s = x^8 y^5: P = <a>_8 * <c>_5, x -> a, y -> c ; chi(x)=5, chi(y)=-8
    'S': dict(orders=(8, 5), x=[(0, 1)], y=[(1, 1)], chi=(5, -8), partner='xxxxyXy'),
}

def tokens(w, sp):
    o = sp['orders']; t = []
    for c in w:
        base = sp[c.lower()]
        if c.islower(): t.extend(base)
        else: t.extend((f, (-e) % o[f]) for f, e in reversed(base))
    return t

def necklace(w, sp):
    o = sp['orders']; st = []
    for f, e in tokens(w, sp):
        if st and st[-1][0] == f:
            ne = (st[-1][1] + e) % o[f]; st.pop()
            if ne: st.append((f, ne))
        else:
            st.append((f, e % o[f]))
    while len(st) >= 2 and st[0][0] == st[-1][0]:
        f = st[0][0]; ne = (st[0][1] + st[-1][1]) % o[f]; st.pop(); st.pop(0)
        if ne: st.insert(0, (f, ne))
    if len(st) <= 1: return ('ell', tuple(st))
    if st[0][0] == 1: st = st[1:] + st[:1]
    pairs = [(st[i][1], st[i + 1][1]) for i in range(0, len(st), 2)]
    return min(tuple(pairs[i:] + pairs[:i]) for i in range(len(pairs)))

def chi(w, sp):
    a, b = ab(w); return sp['chi'][0] * a + sp['chi'][1] * b

def mul(P, Q): return tuple(tuple(sum(P[i][k] * Q[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def D6():
    gens = [((-1, 0), (0, -1)), ((-1, 0), (-1, 1)), ((-1, 3), (0, 1))]
    G = {((1, 0), (0, 1))}; fr = list(G)
    while fr:
        nf = []
        for g in fr:
            for h in gens:
                k = mul(g, h)
                if k not in G: G.add(k); nf.append(k)
        fr = nf
    return G

def bases(L):
    seen = {('x', 'y')}; fr = [('x', 'y')]
    while fr:
        nf = []
        for u, v in fr:
            for nu, nv in ((red(u + v), v), (red(u + inv(v)), v), (red(v + u), v), (red(inv(v) + u), v),
                           (u, red(v + u)), (u, red(v + inv(u))), (u, red(u + v)), (u, red(inv(u) + v))):
                if len(nu) + len(nv) <= L and (nu, nv) not in seen:
                    seen.add((nu, nv)); nf.append((nu, nv))
        fr = nf
    return seen

def search(case, L, nmax, out=print):
    sp = SPECS[case]; s = sp['partner']; Ns = necklace(s, sp); Nsi = necklace(inv(s), sp); cs = chi(s, sp)
    d6 = D6(); hits = []
    for u, v in sorted(bases(L), key=lambda b: (len(b[0]) + len(b[1]), b)):
        for (p, q) in ((u, v), (v, u), (inv(u), v), (u, inv(v))):
            P = tuple(zip(ab(p), ab(q)))  # columns ab(p), ab(q)
            for n in range(-nmax, nmax + 1, 2):  # T(2,n): p^2 q^n, n odd
                w = red(pw(p, 2) + pw(q, n)); c = chi(w, sp)
                if c not in (cs, -cs): continue
                N = necklace(w, sp)
                if (c == cs and N == Ns) or (c == -cs and N == Nsi):
                    det = P[0][0] * P[1][1] - P[0][1] * P[1][0]
                    B = ((-1, 0), (-n, 1)); Pi = ((P[1][1] * det, -P[0][1] * det), (-P[1][0] * det, P[0][0] * det))
                    R = mul(mul(P, B), Pi); hits.append(('T2', w, p, q, n, R, R in d6)); out(hits[-1])
            for m in range(-nmax, nmax + 1):  # BS: p^-1 q^m p q^-(m+e)
                for e in (1, -1):
                    w = red(inv(p) + pw(q, m) + p + pw(q, -(m + e))); c = chi(w, sp)
                    if c not in (cs, -cs): continue
                    N = necklace(w, sp)
                    if (c == cs and N == Ns) or (c == -cs and N == Nsi):
                        hits.append(('BS', w, p, q, m, e)); out(hits[-1])
    seen = set(); res = []
    for h in hits:
        key = (h[0], h[1])
        if key in seen: continue
        seen.add(key); res.append(h)
    return res

def self_test():
    sp = SPECS['A']
    assert necklace('xxxxxyyyyy', sp) != necklace('xxxxxxxxyyyyy', sp)
    assert necklace('xxxxyXy', sp) == ('ell', ())          # A dies in P (A = x^5 z^2)
    assert chi('xxxxyXy', sp) == 0 and chi('xxxxxxxxyyyyy', sp) == 1
    # conjugates of s and products with conjugates of A keep necklace and chi
    s = 'xxxxxxxxyyyyy'
    for g in ('xy', 'YYx', 'xyXXy'):
        w = red(g + s + inv(g) + 'yXy' + 'xxxxyXy' + 'Yx' + 'Y')
        w2 = red(g + s + inv(g) + 'Y' + 'xyX' + 'xxxxyXy' + 'xYX' + 'y')
        assert necklace(w2, sp) == necklace(s, sp) and chi(w2, sp) == 1
    spS = SPECS['S']; assert necklace('xxxxxxxxyyyyy', spS) == ('ell', ()) and chi('xxxxyXy', spS) == -1
    assert len(D6()) == 12
    print('r64_search self-test passed')

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--self-test' in a: self_test(); sys.exit()
    case = a[a.index('--case') + 1] if '--case' in a else 'A'
    L = int(a[a.index('--len') + 1]) if '--len' in a else 10
    nmax = int(a[a.index('--nmax') + 1]) if '--nmax' in a else 15
    r = search(case, L, nmax, out=lambda h: print(h, flush=True))
    print('case', case, 'L', L, 'nmax', nmax, 'hits', len(r), 'outside D6:',
          sum(1 for h in r if h[0] == 'T2' and not h[6]), 'BS:', sum(1 for h in r if h[0] == 'BS'))

def torus_scan(B=40):
    """Same-basis torus forms: all (p,q), |p|,|q| <= B, with x^p y^q ~ (x^8y^5)^{+-1} in G_A, and all a,
    |a| <= B, with x^a yXy ~ (x^4yXy)^{+-1} in G_s (s = x^8y^5)."""
    sp = SPECS['A']; s = sp['partner']; N1, N2 = necklace(s, sp), necklace(inv(s), sp)
    resA = [(p, q) for p in range(-B, B + 1) for q in range(-B, B + 1)
            for w in [red(pw('x', p) + pw('y', q))]
            if (chi(w, sp) == 1 and necklace(w, sp) == N1) or (chi(w, sp) == -1 and necklace(w, sp) == N2)]
    sp = SPECS['S']; A = sp['partner']; N1, N2 = necklace(A, sp), necklace(inv(A), sp); cA = chi(A, sp)
    resS = [a for a in range(-B, B + 1) for w in [red(pw('x', a) + 'yXy')]
            if (chi(w, sp) == cA and necklace(w, sp) == N1) or (chi(w, sp) == -cA and necklace(w, sp) == N2)]
    return resA, resS
