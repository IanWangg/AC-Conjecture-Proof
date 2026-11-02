"""Exact controls for a primitive-free cyclic-preimage theorem in T(3,4).

The unbounded proof is in torus-cyclic-preimage.md; finite controls do not
replace that proof. Uses only Python's standard library.
"""
import argparse
import json
from pathlib import Path

I = (1, 0, 0, 1)
A = (0, -1, 1, -1)
B = (0, -1, 1, 0)


def mul(a, b):
    return (a[0]*b[0]+a[1]*b[2], a[0]*b[1]+a[1]*b[3],
            a[2]*b[0]+a[3]*b[2], a[2]*b[1]+a[3]*b[3])


def inv(a):
    assert det(a) == 1
    return a[3], -a[1], -a[2], a[0]


def det(a):
    return a[0]*a[3]-a[1]*a[2]


def tr(a):
    return a[0]+a[3]


def sub(a, b):
    return tuple(u-v for u, v in zip(a, b))


def power(a, n):
    if n < 0:
        return power(inv(a), -n)
    out = I
    while n:
        if n % 2:
            out = mul(out, a)
        a = mul(a, a)
        n //= 2
    return out


def comm(a, b):
    return mul(mul(mul(a, b), inv(a)), inv(b))


def matrix(word, first=A, second=B):
    letters = dict(x=first, X=inv(first), y=second, Y=inv(second))
    out = I
    for c in word:
        out = mul(out, letters[c])
    return out


def inverse_word(w):
    return w.swapcase()[::-1]


def torus_necklace(n, w):
    stack = []
    for c in w:
        f, exponent = (0 if c.lower() == 'x' else 1), (1 if c.islower() else -1)
        if stack and stack[-1][0] == f:
            exponent += stack.pop()[1]
        exponent %= n+f
        if exponent:
            stack.append((f, exponent))
    while len(stack) > 1 and stack[0][0] == stack[-1][0]:
        f, exponent = stack.pop()
        exponent = (exponent+stack.pop(0)[1]) % (n+f)
        if exponent:
            stack.insert(0, (f, exponent))
    # Only cyclic syllable length is used; choosing a rotation is unnecessary.
    return tuple(stack)


def checks():
    assert power(A, 3) == I and power(B, 4) == I
    assert tr(comm(A, B)) == 3
    b = matrix('xyxYXY')
    assert b == (1, 1, 2, 3) and tr(b) == 4
    # Exhaustive finite balls are arithmetic controls, not the proof.
    ball = {I}
    for _ in range(5):
        ball |= {mul(c, g) for c in ball for g in (A, inv(A), B, inv(B))}
    count = 0
    for c in ball:
        for d in ball:
            assert det(sub(mul(c, d), mul(d, c))) == 2-tr(comm(c, d))
            count += 1
    chebyshev = [0, 1]
    for _ in range(12):
        chebyshev.append(4*chebyshev[-1]-chebyshev[-2])
    for m in range(1, 13):
        rhs = sub(tuple(chebyshev[m]*v for v in b),
                  tuple(chebyshev[m-1]*v for v in I))
        assert power(b, m) == rhs
        if m >= 2:
            assert chebyshev[m] > 1
        for d in ball:
            lhs = det(sub(mul(power(b, m), d), mul(d, power(b, m))))
            rhs_det = chebyshev[m]**2*det(sub(mul(b, d), mul(d, b)))
            assert lhs == rhs_det
    # For n=3 mod12 and n=8 mod12, these two matrices, in the
    # indicated order, give the same useful quotient representation.
    ns = [n for n in range(3, 201) if n % 12 in (3, 8)]
    for n in ns:
        first, second = (A, B) if n % 12 == 3 else (B, A)
        assert matrix('x'*n+'Y'*(n+1), first, second) == I
        assert tr(comm(first, second)) == 3
        assert tr(matrix('xyxYXY', first, second)) == 4
        assert len(torus_necklace(n, 'xyxYXY')) == 6
        w = 'xY'*n+'Y'
        for k in range(-30, 31):
            primitive = (w*k if k >= 0 else inverse_word(w)*(-k))+'xY'
            length = len(torus_necklace(n, primitive))
            assert length == (2*(n*k+1) if k >= 0 else 2*(n*(-k)-1))
            assert length != 6
    # Positive primitive control: {x,y} itself has commutator trace3.
    assert tr(comm(matrix('x'), matrix('y'))) == 3
    return {'status': 'PASS', 'x_image': A, 'y_image': B,
            'x_order': 3, 'y_order': 4,
            'commutator_image': comm(A, B), 'commutator_trace': 3,
            'braid_image': b, 'braid_trace': tr(b),
            'matrix_ball_size': len(ball), 'determinant_identity_pairs': count,
            'chebyshev_prefix_trace4': chebyshev[:8],
            'positive_power_identities_checked': [1, 12],
            'uniform_congruence_classes': [3, 8], 'modulus': 12,
            'formula_control_n_values': ns, 'formula_control_k_range': [-30, 30],
            'unbounded_proof_in_report': True, 'ordinary_AC_goal_solved': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    args = parser.parse_args()
    result = checks()
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
