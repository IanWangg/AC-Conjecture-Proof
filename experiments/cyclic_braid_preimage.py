#!/usr/bin/env python3
"""Exact checks supporting the unbounded cyclic braid-preimage theorem.

The theorem is proved in research-n.md; this finite checker validates its
identities, conventions, uniform formulas and positive exceptions. It is
not a bounded search offered as a substitute for the proof.
Standard library only. Matrices are flattened row-major integer tuples.
"""
import argparse
import json
import random
from pathlib import Path

I = (1, 0, 0, 1)
U = (1, 1, 0, 1)
V = (1, 0, -1, 1)


def mul(A, B):
    a, b, c, d = A
    e, f, g, h = B
    return (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h)


def inv(A):
    a, b, c, d = A
    assert a*d-b*c == 1
    return (d, -b, -c, a)


def det(A):
    return A[0]*A[3]-A[1]*A[2]


def trace(A):
    return A[0]+A[3]


def sub(A, B):
    return tuple(a-b for a, b in zip(A, B))


def scale(k, A):
    return tuple(k*a for a in A)


def power(A, k):
    if k < 0:
        return power(inv(A), -k)
    result = I
    while k:
        if k & 1:
            result = mul(result, A)
        A = mul(A, A)
        k //= 2
    return result


def comm(A, B):
    return mul(mul(mul(A, B), inv(A)), inv(B))


MAT = dict(x=U, y=V, X=inv(U), Y=inv(V))
SWAP = str.maketrans('xyXY', 'yxYX')
FLIP = str.maketrans('xyXY', 'XYxy')


def inverse_word(w):
    return w.translate(FLIP)[::-1]


def reduce_word(w):
    out = []
    for a in w:
        if out and out[-1].swapcase() == a:
            out.pop()
        else:
            out.append(a)
    return ''.join(out)


def evaluate(w):
    A = I
    for a in w:
        A = mul(A, MAT[a])
    return A


def fp_mul(a, b):
    """Exact normal form in C2*C3, syllables (factor, nonzero residue)."""
    out = list(a)
    for f, e in b:
        if out and out[-1][0] == f:
            e = (out.pop()[1]+e) % (2 if f == 'S' else 3)
        if e:
            out.append((f, e))
    return tuple(out)


FP = dict(x=(('T', 2), ('S', 1)),
          X=(('S', 1), ('T', 1)),
          y=(('S', 1), ('T', 2)),
          Y=(('T', 1), ('S', 1)))


def fp_evaluate(w):
    a = ()
    for c in w:
        a = fp_mul(a, FP[c])
    return a


def cyclic_fp(w):
    w = tuple(w)
    while len(w) > 1 and w[0][0] == w[-1][0]:
        w = fp_mul(w[1:], w[:1])
    return w


def f(T, k):
    """f_0=0, f_1=1, f_(j+1)=T f_j-f_(j-1), all integral j."""
    if k < 0:
        return -f(T, -k)
    a, b = 0, 1
    for _ in range(k):
        a, b = b, T*b-a
    return a


def primitive_v(k):
    return reduce_word(('xY'*k if k >= 0 else 'yX'*(-k))+'x')


def reduced_words(max_length):
    words = ['']
    level = ['']
    for _ in range(max_length):
        level = [w+a for w in level for a in 'xyXY'
                 if not w or a != w[-1].swapcase()]
        words.extend(level)
    return words


def check():
    assert mul(mul(U, V), U) == mul(mul(V, U), V)
    assert evaluate('xyxYXY') == I
    assert trace(comm(U, V)) == 3
    matrix_cases = 0
    coefficient_cases = 0
    tested_B = [evaluate(w) for w in reduced_words(4)]
    for n in range(2, 51):
        p = 'x'*n+'Y'*(n+1)
        C = evaluate(p)
        T = n*(n+1)+2
        assert C == (n*(n+1)+1, n, n+1, 1)
        assert trace(C) == T
        assert len(cyclic_fp(fp_evaluate(p))) == 4*n+2
        for m in range(-12, 13):
            A = power(C, m)
            u = f(T, m)
            assert A == sub(scale(u, C), scale(f(T, m-1), I))
            if abs(m) >= 2:
                assert abs(u) >= T > 1
            coefficient_cases += 1
            if n <= 12 and abs(m) <= 5:
                for B in tested_B:
                    delta = det(sub(mul(A, B), mul(B, A)))
                    assert delta == 2-trace(comm(A, B))
                    assert delta == u*u*det(sub(mul(C, B), mul(B, C)))
                    if abs(m) >= 2:
                        assert delta % (u*u) == 0 and delta != -1
                    matrix_cases += 1

    s = [2, 4]
    for _ in range(98):
        s.append(3*s[-1]-s[-2])
    for n in range(2, 100):
        assert s[n] > n*(n+1)+2
    for k in range(-40, 41):
        w = primitive_v(k)
        j = k if k >= 0 else -k-1
        assert trace(evaluate(w)) == s[j]
        assert len(cyclic_fp(fp_evaluate(w))) == 4*j+2
        assert w.count('x')-w.count('X')+w.count('y')-w.count('Y') == 1

    # Every pair here is obtained by actual free-basis Nielsen operations.
    # This independently checks the commutator-trace convention on long,
    # signed primitive words, not only the special v_k family.
    rng = random.Random(20261102)
    pair = ['x', 'y']
    for _ in range(2000):
        i = rng.randrange(2)
        j = 1-i
        op = rng.randrange(4)
        if op == 0:
            pair[i] = inverse_word(pair[i])
        elif op == 1:
            pair.reverse()
        elif op == 2:
            pair[i] = reduce_word(pair[i]+pair[j])
        else:
            pair[i] = reduce_word(pair[j]+pair[i])
        assert trace(comm(*map(evaluate, pair))) == 3
        if sum(map(len, pair)) > 200:
            pair = ['x', 'y']

    # In n=1 the original power is primitive: x y^-2 is obtained from
    # x by two right Nielsen multiplications by y^-1.
    assert evaluate('xYY') == (3, 1, 2, 1)
    # A uniform proof needs the free-product invariant, not just trace.
    assert trace(evaluate('x'*56+'Y'*57)) == s[8] == 3194
    assert len(cyclic_fp(fp_evaluate('x'*56+'Y'*57))) == 226
    assert len(cyclic_fp(fp_evaluate(primitive_v(8)))) == 34
    return {
        'status': 'PASS',
        'ordinary_AC_goal_solved': False,
        'theorem_scope': 'For n>=2, the full B3-preimage of any conjugate '
                         'of <x^n y^(-n-1)> contains no F2-primitive word.',
        'unbounded_proof': 'research/research-n.md',
        'commutator_trace': 3,
        'determinant_commutator_constant': -1,
        'coefficient_identity_cases': coefficient_cases,
        'matrix_divisibility_cases': matrix_cases,
        'primitive_Nielsen_basis_checks': 2000,
        'AK3_power_matrix': list(evaluate('xxxYYYY')),
        'AK3_f_m_for_m_0_through_5': [f(14, i) for i in range(6)],
        'n1_exception_primitive': 'xYY',
        'AK2_compatibility': 'The arbitrary-tail initial subgroup theorem '
                            'also holds for n=2, which has ordinary AC '
                            'certificates elsewhere; it is not AC-invariant.',
        'trace_collision_control_n': 56,
        'trace_collision_control_primitive_index': 8,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output')
    args = parser.parse_args()
    result = check()
    rendered = json.dumps(result, indent=2)+'\n'
    if args.output:
        Path(args.output).write_text(rendered)
    print(rendered, end='')
