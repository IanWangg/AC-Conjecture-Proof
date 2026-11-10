#!/usr/bin/env python3
"""Agent TH07 (round 5): finite checks and certificates for research/research-th07.md.

  python3 experiments/th07_exits.py --selftest          # all checks below, about 1 minute
  python3 experiments/th07_exits.py --cert 3 de OUT     # AK(3) -> (d_3, e_3) elementary certificate
  python3 experiments/th07_exits.py --cert 3 v0 OUT     # AK(3) -> (w_3, yyXYX)
  python3 experiments/th07_exits.py --cert 5 F OUT      # AK(5) -> F_5 (frame state, length 16); also route P
  python3 experiments/th07_exits.py --whitehead 3 8     # Aut(F2)-minimal lengths of first-exit states
  python3 experiments/th07_exits.py --frames 4 11 -3 7  # least lengths in the frame classes theta_m(C_n)

Checked: (A) Theorem A closed forms against exhaustive enumeration (n <= 4);
(B) Theorem B against enumeration (n <= 5, both frozen power relators);
(C) Theorem C: w_n in C_n, the frame words and e_n, d_n in the class of b^-1 modulo
w_n (explicit conjugators x^t, Britton reduction in BS(n+1,n)), and the list of class
members of length <= n+3 against a bounded-conjugator search (n = 3, 4);
(D) the triangle identities and the length profiles of the ACM paths of section 5.
Standard library only; imports research-j's enumeration and research-d's compiler.
"""
import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import j_first_increase as J      # noqa: E402
import d_certify                  # noqa: E402
import elementary_verify          # noqa: E402

T = {'x': 1, 'X': -1, 'y': 2, 'Y': -2}
B = 'xyxYXY'
BI = 'yxyXYX'


def red(w):
    out = []
    for ch in w:
        if out and out[-1] == ch.swapcase():
            out.pop()
        else:
            out.append(ch)
    return ''.join(out)


def inv(w):
    return w.swapcase()[::-1]


def cyc(w):
    w = red(w)
    while len(w) >= 2 and w[0] == w[-1].swapcase():
        w = w[1:-1]
    return w


def rots(w):
    return {w[k:] + w[:k] for k in range(len(w))}


def same(a, b):
    a, b = cyc(a), cyc(b)
    return len(a) == len(b) and b in rots(a)


def same_pm(a, b):
    return same(a, b) or same(a, inv(b))


def P(letter, k):
    return letter * k if k >= 0 else letter.swapcase() * (-k)


def tup(w):
    return tuple(T[ch] for ch in w)


def words(n):
    W = dict(p='x' * n + 'Y' * (n + 1), w='x' * n + 'y' + 'X' * (n + 1) + 'Y',
             d='x' * n + 'YXyy', e='x' * (n - 1) + 'yyXY', c='xyxYYXy')
    W['a'] = {m: 'x' * m + 'yXYXy' for m in range(1, n + 1)}
    W['b'] = {m: 'x' * n + 'YXy' + 'X' * (n - m) + 'y' for m in range(1, n + 1)}
    W['cc'] = {m: 'x' * (n - 1) + 'y' + 'X' * (n - m) + 'yXY' for m in range(1, n + 1)}
    W['z'] = {i: cyc('x' * (n - 1) + 'Y' * i + 'xy' + 'X' * (n + 1 - i) + 'Y') for i in range(n + 2)}
    return W


def v(j):
    """frame word v_j = y x^j y X Y X (v_1 = b^-1)."""
    return cyc('y' + P('x', j) + 'yXYX')


def U1(n, a, c):
    return 'Y' + 'x' * a + 'Y' * c + 'xy' + 'X' * (n - c) + 'y' * (n - 1 - a) + 'X'


def U2(n, a, c):
    return 'x' + 'Y' * c + 'x' * a + 'YX' + 'y' * (n - 1 - a) + 'X' * (n - c) + 'y'


def theta(j, w):
    """automorphism x -> x, y -> x^(j-1) y, applied to a cyclic word."""
    m = {'x': 'x', 'X': 'X', 'y': P('x', j - 1) + 'y', 'Y': 'Y' + P('x', 1 - j)}
    return cyc(''.join(m[ch] for ch in w))


def in_C(u, n):
    """exact test (Lemma J0): u conjugate to p_n^{+-1} in the braid group B."""
    p = tup('x' * n + 'Y' * (n + 1))
    u = tup(cyc(u))
    s, ab = J.sig_C2C3(u), sum(J.exps(u))
    return (s == J.sig_C2C3(p) and ab == -1) or (s == J.sig_C2C3(J.inverse(p)) and ab == 1)


# ---------- BS(n+1, n) = <x, y | y x^(n+1) Y = x^n>, relator w_n ----------

def bs_trivial(w, n):
    s = []
    for ch in red(w):
        if ch in 'xX':
            s.append(['x', 1 if ch == 'x' else -1])
        else:
            s.append(['y', 1 if ch == 'y' else -1])
    changed = True
    while changed:
        changed = False
        t = []
        for a in s:                      # merge x-powers, drop x^0
            if a[0] == 'x' and t and t[-1][0] == 'x':
                t[-1][1] += a[1]
                if t[-1][1] == 0:
                    t.pop()
            elif a[1] != 0:
                t.append(list(a))
        s = t
        for i in range(len(s) - 1):      # Britton pinches
            if s[i][0] != 'y':
                continue
            if s[i + 1][0] == 'y' and s[i + 1][1] == -s[i][1]:
                s[i:i + 2] = []
                changed = True
                break
            if i + 2 < len(s) and s[i + 1][0] == 'x' and s[i + 2][0] == 'y' and s[i + 2][1] == -s[i][1]:
                k = s[i + 1][1]
                if s[i][1] == 1 and k % (n + 1) == 0:
                    s[i:i + 3] = [['x', k // (n + 1) * n]]
                    changed = True
                    break
                if s[i][1] == -1 and k % n == 0:
                    s[i:i + 3] = [['x', k // n * (n + 1)]]
                    changed = True
                    break
    return not s


def bs_conj(v1, v2, n, bound=None):
    """some rotation of v1, conjugated by x^t (|t| <= bound), equals v2 modulo w_n?"""
    bound = bound or 2 * n * (n + 1) + 2
    for u in sorted(rots(cyc(v1))):
        for t in sorted(range(-bound, bound + 1), key=abs):
            if bs_trivial(P('x', t) + u + P('x', -t) + inv(v2), n):
                return u, t
    return None


def triple_word(j):
    return cyc('y' + P('x', j[0]) + 'y' + P('x', j[1]) + 'Y' + P('x', j[2]))


def transfer_path(n, target, start=(1, -1, -1)):
    """least-peak path of transfer moves +-T_i in the lattice of Theorem C (each move is
    one cyclic product with a rotation of w_n^{+-1})."""
    Ts = [(-n, n + 1, 0), (0, -(n + 1), n), (n + 1, 0, -n)]
    moves = [tuple(s * a for a in t) for t in Ts for s in (1, -1)]
    ln = lambda j: 3 + sum(map(abs, j))
    for cap in range(max(ln(start), ln(target)), 12 * n + 40):
        prev, todo = {start: None}, [start]
        while todo:
            j = todo.pop(0)
            for mv in moves:
                k = tuple(a + b for a, b in zip(j, mv))
                if k not in prev and ln(k) <= cap and k[1] % (n + 1) != 0 and k[2] % n != 0:
                    prev[k] = j
                    todo.append(k)
        if target in prev:
            out, j = [], target
            while j is not None:
                out.append(j)
                j = prev[j]
            return out[::-1]
    raise RuntimeError('no transfer path')


# ---------- triangles, ACM paths, certificates ----------

def triangle(r, s, t):
    """t is a cyclic product of rotations of r^{+-1} and s^{+-1} (then any two of
    r, s, t are conjugate up to inversion modulo the third)."""
    for r1 in (r, inv(r)):
        for a in rots(r1):
            for s1 in (s, inv(s)):
                for b in rots(s1):
                    if same_pm(cyc(a + b), t):
                        return True
    return False


def acm_ok(old, new, n):
    """validity of the ACM move old -> new (one relator changes), by an exact test
    (frozen b, frozen w_n) or by a chain of triangles through the hubs w_n, a_n."""
    W = words(n)
    f1 = next(f for f in old if any(same_pm(f, g) for g in new))      # the frozen relator
    r1 = next(r for r in old if not same_pm(r, f1))
    r2 = next(r for r in new if not same_pm(r, f1))
    if same_pm(f1, B):
        return in_C(r1, n) and in_C(r2, n)
    if same_pm(f1, W['w']):
        return any(bs_conj(x, r2, n) for x in (r1, inv(r1)))
    for j in range(-n - 2, n + 3):          # frozen frame word v_j: exact test theta_j^-1(r) in C_n
        if same_pm(f1, v(j)):
            return in_C(theta(2 - j, r1), n) and in_C(theta(2 - j, r2), n)
    # triangle(u, f1, u') means u' is conjugate to u^{+-1} modulo f1; chain through the hubs w_n, a_n
    seen, todo = [r1], [r1]
    while todo:
        u = todo.pop()
        for t in (r2, W['w'], W['a'][n]):
            if not any(same_pm(t, s0) for s0 in seen) and triangle(u, f1, t):
                seen.append(t)
                todo.append(t)
    return any(same_pm(r2, s0) for s0 in seen)


def acm_path(n, route, m=None):
    W = words(n)
    st = [(W['p'], B), (W['w'], B)]
    if route == 'v0':
        return st + [(W['w'], v(0))]
    if route == 'F':                        # frame state F_n = theta_{n-1}(U2(n-2,1), b^-1)
        return st + [(W['w'], v(n - 1)), (FWORD, v(n - 1))]
    if route in ('de', 'P'):
        st += [(W['w'], W['e']), (W['d'], W['e'])]
    else:                                   # balanced chain entering at frame m
        st += [(W['w'], W['a'][m]), (W['b'][m], W['a'][m])]
        for k in range(m, n):
            st += [(W['b'][k], W['cc'][k]), (W['a'][k + 1], W['cc'][k]), (W['a'][k + 1], W['b'][k + 1])]
        st += [(W['b'][n], W['cc'][n])]
    return st + [(W['d'], W['c'])] if route != 'de' else st


def product_path(n, route):
    """the same routes as chains of single cyclic products (for certificates)."""
    W = words(n)
    st = [(W['z'][i], B) for i in range(n + 1, -1, -1)]
    goal = (0, -1, -1) if route == 'v0' else (0, -1, n - 1)
    st += [(W['w'], triple_word(j)) for j in transfer_path(n, goal)[1:]]
    if route in ('de', 'P'):
        st.append((W['d'], W['e']))
    if route == 'P':
        st += [(W['d'], W['w']), (W['d'], W['a'][n]), (W['d'], W['c'])]
    return st


FWORD = 'XyXyxYY'


def theta_raw(j, w):
    m = {'x': 'x', 'X': 'X', 'y': P('x', j - 1) + 'y', 'Y': 'Y' + P('x', 1 - j)}
    return red(''.join(m[ch] for ch in w))


def chain_in_C(n, src, dst):
    """cyclic products with rotations of b^{+-1}, inside C_n at lengths <= 2n+5, from src to dst^{+-1};
    returns the list of factor pairs (A, Bs) with next = cyc(A + Bs)."""
    key = lambda w: min(rots(w))
    prev, todo = {key(src): None}, [key(src)]
    goal = {key(dst), key(inv(dst))}
    while todo:
        u = todo.pop(0)
        if u in goal:
            out = []
            while prev[u] is not None:
                u, A, Bs = prev[u]
                out.append((A, Bs))
            return out[::-1]
        for A in sorted(rots(u)):
            for Bs in sorted(rots(B) | rots(BI)):
                w = cyc(A + Bs)
                if len(w) <= 2 * n + 5 and key(w) not in prev:
                    prev[key(w)] = (u, A, Bs)
                    todo.append(key(w))
    raise RuntimeError('no chain')


def set_literal(bld, i, word):
    """conjugate/invert relator i until it is literally the reduced word `word`."""
    word = red(word)
    k = 0
    while len(word) - 2 * k >= 2 and word[k] == word[len(word) - 1 - k].swapcase():
        k += 1
    bld.cyclic_reduce(i)
    assert d_certify.orient(bld, i, word[k:len(word) - k])
    bld.conj_word(i, word[:k])
    assert bld.state[i] == word


def certificate_F(n):
    """AK(n) -> F_n: cyclic products to (w_n, v_{n-1}), then the theta_{n-1}-image of a chain in C_n."""
    W = words(n)
    st = [(W['z'][i], B) for i in range(n + 1, -1, -1)]
    st += [(W['w'], triple_word(j)) for j in transfer_path(n, (n - 1, -1, -1))[1:]]
    bld = d_certify.build(st, (W['p'], B), (W['w'], v(n - 1)))
    for A, Bs in chain_in_C(n, W['w'], U2(n, n - 2, 1)):
        set_literal(bld, 0, theta_raw(n - 1, A))
        set_literal(bld, 1, theta_raw(n - 1, Bs))
        bld.multiply(0)
        bld.cyclic_reduce(0)
    target = (FWORD, v(n - 1))
    bld.cyclic_reduce(1)
    assert d_certify.orient(bld, 0, target[0]) and d_certify.orient(bld, 1, target[1])
    cert = {'format': 'ordinary-ac-elementary-v1', 'start': [W['p'], B], 'target': list(target), 'moves': bld.moves,
            'description': f"AK({n}) -> F_{n} = (XyXyxYY, y x^{n - 1} y XYX) of research-th07.md: cyclic products to "
                           f"(w_n, v_(n-1)), then the image under theta_(n-1): y -> x^(n-2) y of a chain of cyclic "
                           f"products inside C_n from w_n to U2(n-2,1); compiled to strict elementary moves."}
    r = elementary_verify.replay(cert)
    assert r['endpoint'] == list(target)
    return cert, r, None


def certificate(n, route):
    if route == 'F':
        return certificate_F(n)
    W = words(n)
    target = {'v0': (W['w'], 'yyXYX'), 'de': (W['d'], W['e']), 'P': (W['d'], W['c'])}[route]
    st = product_path(n, route)
    desc = (f"AK({n}) -> {target}: route '{route}' of research-th07.md (power-side exit through the "
            f"Baumslag-Solitar relator w_n = x^n y X^(n+1) Y), expanded into {len(st) - 1} cyclic products "
            f"and compiled to strict elementary moves; the ACM-level peak is smaller than the elementary peak.")
    cert = d_certify.certificate(st, (W['p'], B), target, desc)
    r = elementary_verify.replay(cert)
    assert r['endpoint'] == list(target)
    return cert, r, max(len(a) + len(b) for a, b in st)


def selftest(full=False):
    # (A) Theorem A
    for n in (1, 2, 3, 4):
        S = set()
        for a in range(n):
            for c in range(n + 1):
                S |= J.orbit(tup(U1(n, a, c))) | J.orbit(tup(U2(n, a, c)))
        exact = set(J.power_side(n, 2 * n + 3)[1])
        assert exact == S and len(S) == 4 * n * (n + 1) * (2 * n + 3), n
        print(f'A  n={n}: {len(S)} words of length 2n+3 in C_n = 4n(n+1)(2n+3), closed forms match enumeration')
    # (B) Theorem B
    for n in (3, 4, 5) if full else (3, 4):
        for swapped in (False, True):
            g, G = ('y', 'Y') if swapped else ('x', 'X')
            claim = set(J.orbit(J.BRAID))
            for i in [i for i, ch in enumerate(B) if ch == g]:
                for k in [k for k, ch in enumerate(B) if ch == G]:
                    lst = list(B)
                    lst[i], lst[k] = G * (n - 1), g * (n - 1)
                    claim |= J.orbit(tup(''.join(lst)))
            found = set()
            for L in range(1, 2 * n + 3):
                found |= set(J.braid_side(n, L, swapped)[1])
            assert found == claim and len(claim) == 12 + 8 * n + 8, (n, swapped)
        print(f'B  n={n}: class of b in G_n and G_n\' up to length 2n+2 = Orb(b) + {8 * n + 8} words of length 2n+2')
    # (C) Theorem C
    for n in range(3, 13):
        W = words(n)
        assert same(W['z'][n + 1], W['p']) and same(W['z'][0], W['w'])
        assert all(in_C(W['z'][i], n) and len(W['z'][i]) <= 2 * n + 3 for i in range(n + 2))
        assert all(triangle(B, W['z'][i], W['z'][i - 1]) for i in range(1, n + 2))
        assert all(same(v(j), theta(j, BI)) and same(theta(j, W['w']), W['w']) for j in range(-n, n + 1))
        assert all(same(W['a'][m], v(m)) and same_pm(W['b'][m], theta(m, U1(n, n - 1, 1))) for m in range(1, n + 1))
        assert same(W['e'], W['cc'][n]) and same(W['d'], W['b'][n]) and same(W['w'], U1(n, n - 1, 0))
        assert all(same(W['cc'][m], theta(m, W['cc'][1])) for m in range(1, n + 1))
        for m in range(2, n + 1):           # automorphic images Q_m of P_n (remark in section 5)
            cm = theta(1 - (n - m), W['c'])
            assert len(cm) == 2 * (n - m) + 5 + (2 if m == n else 0) and triangle(W['b'][m], W['a'][m], cm)
        if n <= (8 if full else 6):
            for t in [v(j) for j in range(-2, n + 1)] + [W['e'], W['d']]:
                assert bs_conj(BI, t, n), (n, t)
    print('C  w_n in C_n via the chain z_i (n <= 12); frame words, e_n, d_n conjugate to b^-1 modulo w_n')
    for n in (3, 4):
        W = words(n)
        claim = set()
        for t in [v(j) for j in range(-(n - 2), n - 1)] + [W['e']]:
            claim |= rots(t) | rots(inv(t))
        found = set()
        for L in range(1, n + 4):
            for u in J.cyclically_reduced_words(L):
                s = ''.join('xXyY'[(abs(a) - 1) * 2 + (a < 0)] for a in u)
                if s != min(rots(s) | rots(inv(s))) or abs(s.count('y') - s.count('Y')) != 1:
                    continue
                if bs_conj(BI, s, n) or bs_conj(B, s, n):
                    found |= rots(s) | rots(inv(s))
        assert found == claim, (n, sorted(found ^ claim))
        print(f'C  n={n}: class of b modulo w_n up to length n+3 (bounded conjugators x^t): {len(claim)} words, as in Theorem C')
    # (D) ACM paths
    for n in range(3, 9 if full else 7):
        W = words(n)
        assert same_pm(theta(n - 1, U2(n, n - 2, 1)), FWORD)
        piv = {(nm, a, c) for nm, U in (('U1', U1), ('U2', U2)) for a in range(n) for c in range(n + 1)
               if in_C(theta(0, U(n, a, c)), n) or in_C(theta(2, U(n, a, c)), n)}
        assert piv == {('U1', n - 1, 0), ('U2', n - 1, 0)}      # only the BS words lie in C_n and tau^{+-1}(C_n)
        assert all(len(theta(m, U2(n, n - 2, 1))) == 2 * n + 5 - 2 * m for m in range(1, n))
        for route, m in [('v0', None), ('de', None), ('P', None), ('F', None)] + [('chain', m) for m in range(2, n)]:
            st = acm_path(n, route, m)
            assert all(acm_ok(st[i], st[i + 1], n) for i in range(len(st) - 1)), (n, route, m)
            peak = max(len(a) + len(b) for a, b in st)
            want = {'v0': 2 * n + 9, 'de': 3 * n + 6, 'P': 3 * n + 6, 'F': 3 * n + 7}.get(route) or max(2 * n + 9, 2 * n + 8 + m, 4 * n + 7 - 2 * m)
            assert peak == want, (n, route, m, peak)
        best = min(max(2 * n + 9, 2 * n + 8 + m, 4 * n + 7 - 2 * m) for m in range(2, n))
        assert best == 2 * n + 8 + (2 * n + 1) // 3
        print(f'D  n={n}: ACM paths verified; peaks 2n+9={2 * n + 9} (to (w_n,yyXYX)), 3n+6={3 * n + 6} (to (d_n,e_n) and P_n), '
              f'balanced chain to P_n: {best}')
    for route in ('v0', 'de', 'P', 'F'):
        cert, r, cp = certificate(3, route)
        print(f"E  n=3 route {route}: certificate replays, {r['moves']} moves, elementary peak {r['peak_total_length']}, "
              f"cyclic-product peak {cp}, endpoint {r['endpoint']}")
    print('selftest passed')


def whitehead_table(lo, hi):
    """experiment: Aut(F2)-minimal total length (research-d's d_whitehead.aut_canon) of every
    first-exit state (U, b), U in the list of Theorem A, and of AK(n), S_n, P_n, F_n."""
    import d_whitehead
    for n in range(lo, hi + 1):
        W, res = words(n), {}
        for nm, U in (('U1', U1), ('U2', U2)):
            for a in range(n):
                for c in range(n + 1):
                    L, cp = d_whitehead.aut_canon((U(n, a, c), B))
                    res.setdefault(L, []).append((f'{nm}({a},{c})', cp))
        named = {k: d_whitehead.aut_canon(pair) for k, pair in
                 (('AK', (W['p'], B)), ('S', (W['d'], W['e'])), ('P', (W['d'], W['c'])), ('F', (FWORD, v(n - 1))))}
        print(f'n={n}: Aut-minimal lengths of the {2 * n * (n + 1)} first-exit states (U,b) up to inversion: '
              f'{ {L: len(x) for L, x in sorted(res.items())} };  2n+9={2 * n + 9}, 2n+8={2 * n + 8}, n+11={n + 11}')
        Lmin = min(res)
        print(f'   shortest orbit: {[x[0] for x in res[Lmin]]} -> {res[Lmin][0][1]};  same orbit as F_n: '
              f'{res[Lmin][0][1] == named["F"][1]}')
        print('   ' + '; '.join(f'{k}_n: {val[0]} {val[1]}' for k, val in named.items()))


def frame_scan(n, lmax, lo, hi):
    """experiment: least length of a cyclically reduced word u (|u| <= lmax) in theta_m(C_n), i.e. conjugate
    to w_n^{+-1} modulo the frame word v_m (exact test), and the total length with v_m."""
    cand = []
    for L in range(1, lmax + 1):
        for u in J.cyclically_reduced_words(L):
            s = ''.join('xXyY'[(abs(a) - 1) * 2 + (a < 0)] for a in u)
            if s == min(rots(s) | rots(inv(s))):
                cand.append(s)
    for m in range(lo, hi + 1):
        best, ex = None, []
        for s in cand:
            if best is not None and len(s) > best:
                break
            if in_C(theta(2 - m, s), n):
                best = len(s)
                ex.append(s)
        tot = None if best is None else best + len(v(m))
        print(f'n={n} frame m={m}: |v_m|={len(v(m))}, least length in theta_m(C_n) = {best} '
              f'({len(ex)} words up to rotation/inversion, e.g. {ex[:2]}), total {tot}')


def main():
    a = sys.argv[1:]
    if a[:1] == ['--frames']:
        return frame_scan(*map(int, a[1:5]))
    if a[:1] == ['--whitehead']:
        return whitehead_table(int(a[1]), int(a[2]))
    if a[:1] == ['--selftest']:
        selftest(full='--full' in a)
    elif a[:1] == ['--cert']:
        cert, r, cp = certificate(int(a[1]), a[2])
        with open(a[3], 'w') as f:
            json.dump(cert, f, indent=1)
        print(json.dumps({'n': int(a[1]), 'route': a[2], 'moves': r['moves'], 'peak_total_length': r['peak_total_length'],
                          'cyclic_product_peak': cp, 'endpoint': r['endpoint'], 'path': a[3]}))
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
