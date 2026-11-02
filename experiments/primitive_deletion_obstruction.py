"""Checks supporting the unbounded one-step primitive obstruction for AK(3).

The theorem uses Nielsen uniqueness of rank-two primitive conjugacy classes;
finite parameter checks here verify formulas, not the unbounded conclusion.
No AC trivialization or global AC invariant is asserted.
"""
from collections import deque
import argparse
import json


def inv(w):
    return w.swapcase()[::-1]


def red(w):
    out = []
    for c in w:
        if c not in 'xXyY':
            raise ValueError('bad free letter')
        if out and out[-1] == c.swapcase():
            out.pop()
        else:
            out.append(c)
    return ''.join(out)


def power(w, k):
    return red((w if k >= 0 else inv(w))*abs(k))


def exponents(w):
    return (w.count('x')-w.count('X'), w.count('y')-w.count('Y'))


def product(a, b):
    return (a[0]*b[0]+a[1]*b[2], a[0]*b[1]+a[1]*b[3],
            a[2]*b[0]+a[3]*b[2], a[2]*b[1]+a[3]*b[3])


def matrix_inverse(a):
    return a[3], -a[1], -a[2], a[0]


U = (1, 1, 0, 1)
V = (1, 0, -1, 1)
MATRICES = {'x':U, 'X':matrix_inverse(U), 'y':V, 'Y':matrix_inverse(V)}


def matrix(w):
    ans = (1, 0, 0, 1)
    for c in w:
        ans = product(ans, MATRICES[c])
    return ans


def trace(w):
    a = matrix(w)
    return a[0] + a[3]


def braid_primitive(k):
    # c=xY, d=x form a free basis; c^k d is primitive.
    return red(power('xY', k)+'x')


def braid_cyclic_syllables(word):
    images = {'x':((1,2),(0,1)), 'X':((0,1),(1,1)),
              'y':((0,1),(1,2)), 'Y':((1,1),(0,1))}
    syllables = []
    for c in word:
        for factor,power_ in images[c]:
            if syllables and syllables[-1][0] == factor:
                power_ += syllables.pop()[1]
            power_ %= (2,3)[factor]
            if power_:
                syllables.append((factor,power_))
    while len(syllables)>1 and syllables[0][0] == syllables[-1][0]:
        factor,a = syllables.pop()
        _,b = syllables.pop(0)
        residue = (a+b) % (2,3)[factor]
        if residue:
            syllables.insert(0,(factor,residue))
    return len(syllables)


def torus_primitive(n, k):
    # m=xY and w=m^n Y form a free basis; w^k m is primitive.
    m = 'xY'
    w = m*n+'Y'
    return red(power(w, k)+m)


def substitute(word, first, second):
    values = {'x':first, 'X':inv(first), 'y':second, 'Y':inv(second)}
    return red(''.join(values[c] for c in word))


def verify_torus_basis(n, k):
    u, w = torus_primitive(n,k), 'xY'*n+'Y'
    # In formal generators A=x and B=y representing u,w, respectively,
    # m=B^-k A, old x=m B^-1 m^n, old y=B^-1 m^n.
    m = red(power('y',-k)+'x')
    inverse_x = red(m+'Y'+power(m,n))
    inverse_y = red('Y'+power(m,n))
    assert substitute(inverse_x,u,w) == 'x'
    assert substitute(inverse_y,u,w) == 'y'
    assert substitute(u,inverse_x,inverse_y) == 'x'
    assert substitute(w,inverse_x,inverse_y) == 'y'


def torus_nf(n, word):
    """Exact central-extension normal form z^c * residues, z=x^n=y^(n+1)."""
    central, syllables = 0, []
    for c in word:
        factor = 0 if c.lower() == 'x' else 1
        exponent = 1 if c.islower() else -1
        if syllables and syllables[-1][0] == factor:
            exponent += syllables.pop()[1]
        turns, residue = divmod(exponent,n+factor)
        central += turns
        if residue:
            syllables.append((factor,residue))
    return central, tuple(syllables)


def cyclic_necklace(n, word):
    """Cyclic free-product normal form in C_n*C_(n+1), modulo rotation."""
    syllables = list(torus_nf(n,word)[1])
    while len(syllables) > 1 and syllables[0][0] == syllables[-1][0]:
        factor, a = syllables.pop()
        _, b = syllables.pop(0)
        residue = (a+b) % (n+factor)
        if residue:
            syllables.insert(0,(factor,residue))
    if not syllables:
        return ()
    return min(tuple(syllables[j:]+syllables[:j]) for j in range(len(syllables)))


def ak2_control():
    n, k = 2, -2
    u, b = torus_primitive(n,k), 'xyxYXY'
    assert exponents(u) == (-3,5)
    assert cyclic_necklace(n,u) == cyclic_necklace(n,b)
    target = torus_nf(n,u)
    queue = deque([''])
    while queue:
        g = queue.popleft()
        if torus_nf(n,g+b+inv(g)) == target:
            verify_torus_basis(n,k)
            return {'primitive_word':u, 'exponent_vector':[-3,5],
                    'conjugator_g':g, 'exact_identity_in_T2':'u = g b g^-1',
                    'normal_form':target, 'primitive_basis_partner':'xYxYY'}
        if len(g) < 6:
            for c in 'xXyY':
                if not g or g[-1] != c.swapcase():
                    queue.append(g+c)
    raise AssertionError('AK2 conjugacy control not found')


def checks():
    # The braid relation is exact already in these integral matrices.
    assert matrix('xyx') == matrix('yxy')
    seq = [2,4]
    for _ in range(20):
        seq.append(3*seq[-1]-seq[-2])
    assert seq[:5] == [2,4,10,26,68]
    for k in range(-20,21):
        u = braid_primitive(k)
        assert sum(exponents(u)) == 1
        assert trace(u) == seq[k if k>=0 else -k-1]
        m = k if k>=0 else -k-1
        assert braid_cyclic_syllables(u) == 4*m+2
    assert trace('xxxYYYY') == 14
    assert seq[2] < 14 < seq[3]
    for n in range(2,21):
        p = 'x'*n+'Y'*(n+1)
        assert trace(p) == n*(n+1)+2
        assert braid_cyclic_syllables(p) == 4*n+2
        assert seq[n] > trace(p)
    assert braid_cyclic_syllables('x'+'YY') == braid_cyclic_syllables(braid_primitive(1)) == 6
    assert trace('xYY') == trace(braid_primitive(1)) == 4
    rows = []
    b = 'xyxYXY'
    for n in range(3,16):
        candidate_six = []
        for k in range(-12,13):
            u = torus_primitive(n,k)
            assert exponents(u) == (1+n*k,-1-(n+1)*k)
            assert (n+1)*exponents(u)[0]+n*exponents(u)[1] == 1
            verify_torus_basis(n,k)
            necklace = cyclic_necklace(n,u)
            predicted = 2*(n*k+1) if k>=0 else 2*(n*(-k)-1)
            assert len(necklace) == predicted
            assert necklace != cyclic_necklace(n,b)
            if len(necklace) == 6:
                candidate_six.append(k)
        rows.append({'n':n,'parameters_checked':[-12,12],
                     'six_syllable_parameters':candidate_six})
    # Trace alone is insufficient: n=56 passes trace with m=8, but the
    # cyclic syllable lengths immediately differ (226 versus34).
    assert trace('x'*56+'Y'*57) == trace(braid_primitive(8)) == 3194
    assert braid_cyclic_syllables('x'*56+'Y'*57) == 226
    assert braid_cyclic_syllables(braid_primitive(8)) == 34
    control = ak2_control()
    return {'status':'PASS','braid_trace_sequence_prefix':seq[:8],
            'AK3_power_trace':14,'trace_gap':[10,26],
            'torus_checks':rows,'AK2_exception_control':control,
            'trace_alone_incomplete_control':{'n':56,'k':8,'common_trace':3194,
                                              'power_syllables':226,'primitive_syllables':34},
            'uniform_braid_formula_check':'n=2..20; all-n proof in report',
            'scope':'Formula checks for unbounded primitive-deletion theorem; not an AC solution'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    args = parser.parse_args()
    result = checks()
    if args.output:
        with open(args.output,'w') as stream:
            json.dump(result,stream,indent=2)
            stream.write('\n')
    print(json.dumps(result,indent=2))
