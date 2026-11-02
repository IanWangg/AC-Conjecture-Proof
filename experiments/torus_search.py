"""Exact finite-radius AC search in <x,y | x^3=y^4>.

Elements use the central-extension normal form z^k times an alternating
C3*C4 syllable word, z=x^3=y^4. No finite reduction is used.
"""
import argparse
import json
import time


def normal(k, syllables):
    out = []
    for factor, power in syllables:
        order = (3, 4)[factor]
        if out and out[-1][0] == factor:
            power += out.pop()[1]
        turns, power = divmod(power, order)
        k += turns
        if power:
            out.append((factor, power))
    return k, tuple(out)


def multiply(a, b):
    return normal(a[0] + b[0], a[1] + b[1])


def inverse(a):
    return normal(-a[0], ((factor, -power) for factor, power in a[1][::-1]))


ONE = (0, ())
X = (0, ((0, 1),))
Y = (0, ((1, 1),))
SIGNED = (X, inverse(X), Y, inverse(Y))
MOVES = [('invert', 0), ('invert', 1),
         ('multiply', 0, 1), ('multiply', 0, -1),
         ('multiply', 1, 1), ('multiply', 1, -1)]
MOVES += [('conjugate', i, g) for i in (0, 1) for g in 'xXyY']


def evaluate(word):
    ans = ONE
    for c in word:
        ans = multiply(ans, SIGNED['xXyY'.index(c)])
    return ans


START = (ONE, evaluate('xyxYXY'))
TARGET = (X, Y)
PATH8 = (2, 10, 4, 10, 4, 2, 13, 11)


def apply(state, op):
    values = list(state)
    kind, i, *rest = MOVES[op]
    if kind == 'invert':
        values[i] = inverse(values[i])
    elif kind == 'multiply':
        donor = values[1-i]
        values[i] = multiply(values[i], donor if rest[0] > 0 else inverse(donor))
    else:
        g = SIGNED['xXyY'.index(rest[0])]
        values[i] = multiply(multiply(g, values[i]), inverse(g))
    return tuple(values)


def inverse_op(op):
    if op < 2:
        return op
    if op < 6:
        return op ^ 1
    return 6 + ((op-6) ^ 1)


def ball(start, depth, budget):
    seen = {start: (None, None, 0)}
    frontier = [start]
    counts = [1]
    for level in range(depth):
        nxt = []
        for state in frontier:
            for op in range(14):
                other = apply(state, op)
                if other not in seen:
                    seen[other] = (state, op, level+1)
                    nxt.append(other)
                    if len(seen) >= budget:
                        return seen, counts, False
        frontier = nxt
        counts.append(len(nxt))
    return seen, counts, True


def path_to(seen, at):
    out = []
    while seen[at][0] is not None:
        at, op, _ = seen[at]
        out.append(op)
    return out[::-1]


def search(depth, budget):
    begun = time.monotonic()
    forward, fc, fd = ball(START, depth, budget)
    backward, bc, bd = ball(TARGET, depth, budget)
    common = forward.keys() & backward.keys()
    result = {'group': '<x,y | x^3=y^4>', 'depth_per_side': depth,
              'forward_layer_sizes': fc, 'backward_layer_sizes': bc,
              'forward_states': len(forward), 'backward_states': len(backward),
              'complete': fd and bd,
              'seconds': round(time.monotonic()-begun, 4)}
    if common:
        meet = min(common, key=lambda s: forward[s][2] + backward[s][2])
        path = path_to(forward, meet)
        path += [inverse_op(op) for op in path_to(backward, meet)[::-1]]
        state = START
        for op in path:
            state = apply(state, op)
        assert state == TARGET
        result.update({'path_found': True, 'move_ids': path,
                       'moves': [MOVES[op] for op in path],
                       'distance': len(path) if fd and bd else None})
    else:
        result.update({'path_found': False,
                       'distance_lower_bound': 2*depth+1 if fd and bd else None})
    return result


def free_inverse(word):
    return word.swapcase()[::-1]


def free_reduce(word):
    out = []
    for c in word:
        if out and out[-1] == c.swapcase():
            out.pop()
        else:
            out.append(c)
    return ''.join(out)


def free_apply(state, op):
    values = list(state)
    kind, i, *rest = MOVES[op]
    if kind == 'invert':
        values[i] = free_inverse(values[i])
    elif kind == 'multiply':
        donor = values[1-i]
        values[i] = free_reduce(values[i] + (donor if rest[0] > 0 else free_inverse(donor)))
    else:
        g = rest[0]
        values[i] = free_reduce(g + values[i] + free_inverse(g))
    return tuple(values)


def factor_word(factors, relator):
    result = ''
    for conjugator, sign in factors:
        result = free_reduce(result + conjugator +
                             (relator if sign == 1 else free_inverse(relator)) +
                             free_inverse(conjugator))
    return result


def marker_factors(word):
    """w(q) = (product of prefix-conjugates of q) * w(1)."""
    prefix = ''
    factors = []
    for c in word:
        if c in 'qQ':
            factors.append((prefix, 1 if c == 'q' else -1))
        else:
            prefix = free_reduce(prefix + c)
    return factors, prefix


def certificate():
    p, b = 'xxxYYYY', 'xyxYXY'
    actual = (p, b)
    formal = ('q', b)
    zero = ('', b)
    quotient = START
    primitive = []
    for op in PATH8:
        kind, i, *rest = MOVES[op]
        if kind == 'multiply':
            assert rest[0] == 1
            primitive.append({'op': 'multiply', 'i': i, 'j': 1-i})
        else:
            primitive.append({'op': 'conjugate', 'i': i, 'g': rest[0]})
        actual, formal, zero = [free_apply(state, op) for state in (actual, formal, zero)]
        quotient = apply(quotient, op)
        assert tuple(evaluate(w) for w in actual) == quotient
    assert quotient == TARGET
    # Exact independent symbolic identity for the zero-start replay:
    # f*f0^-1 = [p,y] * (yx)p(yx)^-1, f0=b^-1*x.
    d_factors = [('', 1), ('y', -1), ('yx', 1)]
    zero_error_prefixes = [b, 'XY']
    all_factors = []
    residuals = []
    for i, target in enumerate(('x', 'y')):
        introduced, deleted = marker_factors(formal[i])
        assert deleted == zero[i]
        expanded = free_reduce(''.join(p if c == 'q' else free_inverse(p) if c == 'Q' else c
                                       for c in formal[i]))
        assert expanded == actual[i]
        static = [(free_reduce(zero_error_prefixes[i] + g), sign) for g, sign in d_factors]
        assert factor_word(static, p) == free_reduce(zero[i]+free_inverse(target))
        factors = introduced + static
        residual = free_reduce(actual[i] + free_inverse(target))
        assert factor_word(factors, p) == residual
        assert residual
        all_factors.append([{'conjugator': g, 'sign': sign} for g, sign in factors])
        residuals.append(residual)
    assert list(map(len, all_factors)) == [6, 5]
    return {'format': 'ordinary-ac-elementary-v1',
            'scope': 'Torus quotient certificate lifted to its actual free-group endpoint, not the basis',
            'start': [p, b], 'target': actual, 'moves': primitive,
            'quotient_target': ['x', 'y'],
            'quotient_group': '<x,y | x^3=y^4>',
            'free_endpoint_lengths': list(map(len, actual)),
            'free_basis_residuals': residuals,
            'residual_factorization_relator': p,
            'residual_factorizations': all_factors,
            'zero_start_replay_endpoint': zero}


def verify_factorizations(saved):
    """Check stored relative filling identities without regenerating a path."""
    p = saved['residual_factorization_relator']
    if p != 'xxxYYYY' or saved['quotient_target'] != ['x', 'y']:
        raise ValueError('wrong relator or quotient target')
    if len(saved['target']) != 2 or len(saved['residual_factorizations']) != 2:
        raise ValueError('two endpoints and factorizations required')
    for actual, target, encoded in zip(saved['target'], ('x', 'y'), saved['residual_factorizations']):
        if not isinstance(actual, str) or not set(actual) <= set('xXyY'):
            raise ValueError('invalid endpoint word')
        factors = []
        for item in encoded:
            if type(item['sign']) is not int or item['sign'] not in (-1, 1) or not set(item['conjugator']) <= set('xXyY'):
                raise ValueError('invalid factor')
            factors.append((item['conjugator'], item['sign']))
        if factor_word(factors, p) != free_reduce(actual+free_inverse(target)):
            raise ValueError('relative filling identity failed')
        if evaluate(actual) != evaluate(target):
            raise ValueError('quotient endpoint failed')
    return {'factor_counts': list(map(len, saved['residual_factorizations'])),
            'free_endpoint_lengths': list(map(len, saved['target'])),
            'quotient_endpoint': ['x', 'y']}


def selftest():
    assert evaluate('xxx') == evaluate('yyyy') == (1, ())
    assert evaluate('xxxYYYY') == ONE
    assert evaluate('xxx') != ONE
    assert evaluate('xyxYXY') != ONE
    assert evaluate('xxxy') == evaluate('yxxx')
    assert evaluate('xxxxy') != evaluate('yxxxx')
    for word in ['', 'xyxYXY', 'XXyxYxxY', 'xxxYYYY', 'XYxyxxyYY']:
        a = evaluate(word)
        assert multiply(a, inverse(a)) == ONE
    for state in (START, TARGET):
        for op in range(14):
            assert apply(apply(state, op), inverse_op(op)) == state
    assert list(map(len, certificate()['target'])) == [45, 32]
    assert verify_factorizations(certificate())['factor_counts'] == [6, 5]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--depth', type=int, default=4)
    parser.add_argument('--budget', type=int, default=500000)
    parser.add_argument('--output')
    parser.add_argument('--certificate')
    parser.add_argument('--verify-factorizations')
    args = parser.parse_args()
    if args.verify_factorizations:
        with open(args.verify_factorizations) as f:
            print(json.dumps(verify_factorizations(json.load(f)), indent=2))
        raise SystemExit(0)
    selftest()
    result = search(args.depth, args.budget)
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
            f.write('\n')
    if args.certificate:
        with open(args.certificate, 'w') as f:
            json.dump(certificate(), f, indent=2)
            f.write('\n')
    print(json.dumps(result, indent=2))
