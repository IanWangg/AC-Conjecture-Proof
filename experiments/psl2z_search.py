"""Exact bounded AC search in PSL(2,Z), never in a finite reduction.

Fourteen symmetric instructions: invert a coordinate; right multiply by
the other coordinate or its inverse; conjugate by x,X,y,Y. Words in this
quotient are matrices modulo their simultaneous scalar sign.
"""
from collections import deque
import argparse
import json
import time


def canonical(a):
    for v in a:
        if v:
            return a if v > 0 else tuple(-v for v in a)
    raise ValueError('zero matrix')


def mul(a, b):
    return canonical((a[0]*b[0]+a[1]*b[2], a[0]*b[1]+a[1]*b[3],
                      a[2]*b[0]+a[3]*b[2], a[2]*b[1]+a[3]*b[3]))


def inv(a):
    return canonical((a[3], -a[1], -a[2], a[0]))


ONE = (1, 0, 0, 1)
X = (1, 1, 0, 1)
Y = (1, 0, -1, 1)
SIGNED = (X, inv(X), Y, inv(Y))
MOVES = [('invert', 0), ('invert', 1),
         ('multiply', 0, 1), ('multiply', 0, -1),
         ('multiply', 1, 1), ('multiply', 1, -1)]
MOVES += [('conjugate', i, g) for i in (0, 1) for g in 'xXyY']


def evaluate(word):
    ans = ONE
    for c in word:
        ans = mul(ans, SIGNED['xXyY'.index(c)])
    return ans


START = (evaluate('xxxYYYY'), evaluate('xyxYXY'))
TARGET = (X, Y)
PATH10 = (5, 13, 11, 5, 7, 2, 7, 7, 8, 5)


def apply(state, op):
    a, b = state
    if op == 0:
        return inv(a), b
    if op == 1:
        return a, inv(b)
    if op < 6:
        i, sign = MOVES[op][1:]
        values = [a, b]
        donor = values[1-i]
        values[i] = mul(values[i], donor if sign > 0 else inv(donor))
        return tuple(values)
    i = (op-6)//4
    g = SIGNED[(op-6)%4]
    values = [a, b]
    values[i] = mul(mul(g, values[i]), inv(g))
    return tuple(values)


def inverse_op(op):
    if op < 2:
        return op
    if op < 6:
        return op ^ 1
    return 6 + ((op-6) ^ 1)


def ball(start, depth, max_states):
    seen = {start: (None, None)}
    frontier = [start]
    counts = [1]
    for level in range(depth):
        nxt = []
        for state in frontier:
            for op in range(14):
                other = apply(state, op)
                if other not in seen:
                    seen[other] = (state, op)
                    nxt.append(other)
                    if len(seen) > max_states:
                        return seen, counts, False
        frontier = nxt
        counts.append(len(nxt))
    return seen, counts, True


def path_to(seen, at):
    out = []
    while seen[at][0] is not None:
        at, op = seen[at]
        out.append(op)
    return out[::-1]


def search(depth, max_states=1000000):
    t = time.monotonic()
    forward, fc, fd = ball(START, depth, max_states)
    backward, bc, bd = ball(TARGET, depth, max_states)
    common = forward.keys() & backward.keys()
    result = {'depth_per_side': depth,
              'start': START, 'target': TARGET,
              'forward_layer_sizes': fc, 'backward_layer_sizes': bc,
              'forward_states': len(forward), 'backward_states': len(backward),
              'complete': fd and bd,
              'seconds': round(time.monotonic()-t, 3)}
    if common:
        meet = min(common, key=lambda s: len(path_to(forward,s))+len(path_to(backward,s)))
        path = path_to(forward, meet)
        path += [inverse_op(op) for op in path_to(backward, meet)[::-1]]
        state = START
        for op in path:
            state = apply(state, op)
        assert state == TARGET
        result.update({'path_found': True, 'move_ids': path,
                       'shortest_distance_within_complete_search': len(path) if fd and bd else None,
                       'moves': [MOVES[op] for op in path]})
    else:
        result.update({'path_found': False,
                       'certified_distance_lower_bound': 2*depth+1 if fd and bd else None})
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


def normal_reduce(word):
    """Independent normal forms in <S,T | S^2=T^3=1>."""
    out = []
    for factor, power in word:
        modulus = 2 if factor == 0 else 3
        if out and out[-1][0] == factor:
            power += out.pop()[1]
        power %= modulus
        if power:
            out.append((factor,power))
    return tuple(out)


NORMAL_IMAGES = {'x': ((1,2),(0,1)), 'X': ((0,1),(1,1)),
                 'y': ((0,1),(1,2)), 'Y': ((1,1),(0,1))}


def normal_word(word):
    return normal_reduce(syllable for c in word for syllable in NORMAL_IMAGES[c])


def certificate():
    free_state = ('xxxYYYY','xyxYXY')
    matrix_state = START
    table = [{'step':0, 'matrices':matrix_state}]
    elementary = []
    for step,op in enumerate(PATH10,1):
        kind, i, *rest = MOVES[op]
        if kind == 'multiply':
            if rest[0] < 0:
                elementary.append({'op':'invert','i':1-i})
            elementary.append({'op':'multiply','i':i,'j':1-i})
            if rest[0] < 0:
                elementary.append({'op':'invert','i':1-i})
        elif kind == 'invert':
            elementary.append({'op':'invert','i':i})
        else:
            elementary.append({'op':'conjugate','i':i,'g':rest[0]})
        free_state = free_apply(free_state,op)
        matrix_state = apply(matrix_state,op)
        assert tuple(evaluate(w) for w in free_state) == matrix_state
        table.append({'step':step,'move':MOVES[op],'matrices':matrix_state})
    assert matrix_state == TARGET
    assert [normal_word(w) for w in free_state] == [normal_word('x'),normal_word('y')]
    exponents = [sum(1 if c.islower() else -1 for c in w) for w in free_state]
    # Together with the normal forms, equality of these exponent sums proves
    # equality in B3=<s,t | s^2=t^3>, since the central kernel has exponent 6.
    assert exponents == [1, 1]
    assert free_state != ('x','y')
    assert all(free_reduce(w+free_inverse(t)) for w,t in zip(free_state,('x','y')))
    return {'format':'ordinary-ac-elementary-v1',
            'scope':'Free-word lift of a B3 quotient certificate; target is NOT the free basis',
            'start':['xxxYYYY','xyxYXY'], 'target':free_state,
            'quotient_target':['x','y'], 'moves':elementary,
            'quotient_signed_moves':[MOVES[op] for op in PATH10],
            'matrix_table':table,
            'free_endpoint_lengths':list(map(len,free_state)),
            'endpoint_braid_exponent_sums':exponents,
            'free_basis_residuals':[free_reduce(w+free_inverse(t)) for w,t in zip(free_state,('x','y'))]}


def selftest():
    assert START == ((13,3,4,1), ONE)
    for state in (START, TARGET):
        for op in range(14):
            assert apply(apply(state,op), inverse_op(op)) == state
    assert evaluate('xyxYXY') == ONE
    assert evaluate('xyxyxy') == ONE
    assert evaluate('xx') != ONE
    assert normal_word('xyxYXY') == ()
    assert normal_word('xyxyxy') == ()
    # Projection alone loses the central generator z=(xy)^3. Its exponent
    # sum detects precisely the gap used by the B3 endpoint argument.
    assert evaluate('xyxyxy') == ONE
    assert sum(1 if c.islower() else -1 for c in 'xyxyxy') == 6
    assert normal_word('xx') != ()
    assert certificate()['quotient_target'] == ['x','y']
    print('exact matrix and inverse-move controls passed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--depth', type=int, default=4)
    parser.add_argument('--max-states', type=int, default=1000000)
    parser.add_argument('--output')
    parser.add_argument('--certificate')
    args = parser.parse_args()
    selftest()
    result = search(args.depth, args.max_states)
    if args.output:
        with open(args.output,'w') as f:
            json.dump(result, f, indent=2)
            f.write('\n')
    if args.certificate:
        with open(args.certificate,'w') as f:
            json.dump(certificate(), f, indent=2)
            f.write('\n')
    print(json.dumps(result, indent=2))
