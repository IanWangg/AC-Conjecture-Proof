#!/usr/bin/env python3
"""Agent TH03: independent 40-line re-check of the twisted traces used in research-th03 (no imports
from the other th03_* scripts; monomials are strings).  Checks (TT) for l (Theorem T11), L4 (T13) and
l_2 mod 2 (T16), and the values that the proofs use.

    python3 experiments/th03_check.py        (prints 'th03_check passed')
"""
import itertools

def mul(P, Q, D):
    R = {}
    for a, ca in P.items():
        for b, cb in Q.items():
            if len(a) + len(b) <= D: R[a + b] = R.get(a + b, 0) + ca * cb
    return {m: c for m, c in R.items() if c}
def ev(l, P): return sum(l.get(m, 0) * c for m, c in P.items())
def magnus(word, D):                      # word: generators as lower case, inverses as upper case
    P = {'': 1}
    for ch in word:
        g = ch.lower()
        L = {'': 1, g: 1} if ch.islower() else {g * d: (-1) ** d for d in range(D + 1)}
        P = mul(P, L, D)
    return P
def violations(l, PsiX, alphabet, D, mod=0):
    """Number of pairs (i, m) with l(X_i m) != l(m Psi(X_i)); also returns the number of pairs."""
    cnt = bad = 0
    for i in alphabet:
        for d in range(D):
            for m in map(''.join, itertools.product(alphabet, repeat=d)):
                diff = ev(l, mul({i: 1}, {m: 1}, D)) - ev(l, mul({m: 1}, PsiX[i], D))
                cnt += 1; bad += (diff % mod != 0) if mod else (diff != 0)
    return cnt, bad
def binom(j, k):
    r = 1
    for i in range(k): r = r * (j - i) // (i + 1)   # exact: the running product is an integer
    return r

# T11: psi_3 on F(p,q,r) = F(t_0,t_1,t_2): p -> q -> r -> r p ; letters 0,1,2 of the note are p,q,r
tr = str.maketrans('012', 'pqr')
L3 = {k.translate(tr): v for k, v in {'00': 1, '01': 1, '02': 1, '10': 1, '11': 1, '12': 1, '21': 1, '22': 1,
      '002': 1, '010': -1, '012': -1, '020': -2, '021': 1, '022': 1, '100': 1, '101': -1, '102': 1, '110': 1,
      '120': -1, '121': -1, '200': 1, '201': -2, '202': -1, '210': 2, '211': 1, '212': -1, '221': 1}.items()}
Psi3 = {'p': {'q': 1}, 'q': {'r': 1}, 'r': {'r': 1, 'p': 1, 'rp': 1}}
assert violations(L3, Psi3, 'pqr', 3) == (39, 0)
assert ev(L3, magnus('qRQ', 3)) == -2                                  # c = (t_1 T_2 T_1, 1)
assert all(ev(L3, magnus(('q' if j > 0 else 'Q') * abs(j), 3)) == binom(j, 2) >= 0 for j in range(-60, 61))

# T13: phi on F(a,b): a -> b, b -> B a
L4 = {'ba': 1, 'aaa': 1, 'aab': 1, 'aba': -1, 'abb': 1, 'baa': 2, 'bab': -1, 'bba': 3, 'bbb': 1, 'aaaa': 1,
      'aaab': 1, 'aaba': -1, 'aabb': 1, 'abaa': -2, 'abab': -1, 'abbb': 1, 'baab': -2, 'baba': -1,
      'babb': -1, 'bbaa': 2, 'bbba': 2, 'bbbb': 1}
def psi_phi(D):
    Pb = magnus('Ba', D); Pb[''] = Pb.get('', 0) - 1
    return {'a': {'b': 1}, 'b': {m: c for m, c in Pb.items() if c}}
assert violations(L4, psi_phi(4), 'ab', 4) == (30, 0)
assert [ev(L4, magnus('a' * n + 'BA', 4)) for n in range(1, 10)] == [1, 1, -1, -5, -10, -14, -14, -6, 15]
assert all(ev(L4, magnus(('a' if s > 0 else 'A') * abs(s), 4)) == binom(s + 1, 4) >= 0 for s in range(-40, 41))

# T16: l_2 = a + b + aa + ab + bb mod 2
L2 = {'a': 1, 'b': 1, 'aa': 1, 'ab': 1, 'bb': 1}
assert violations(L2, psi_phi(2), 'ab', 2, mod=2) == (6, 0)
eps = lambda u: ev(L2, magnus(u, 2)) % 2
assert eps('aBA') == eps('aaBA') == eps('AA') == 1 and eps('aaa') == 0   # k_1 ~ k_2 ~ x^-2 y ; x^3 y differs
assert all(eps(u.swapcase() + 'b') != eps(u) for u in ('', 'a', 'aaaBA', 'abAB', 'bbaBa', 'AAba', 'aaaaBA'))
print("th03_check passed")
