"""Exact bounded search in B3 times <x,y|x^3=y^4>, with diagonal x,y."""
import argparse
import json
import time
import torus_search as torus


def bn(syllables):
    out = []
    for factor, power in syllables:
        if out and out[-1][0] == factor:
            power += out.pop()[1]
        power %= (2, 3)[factor]
        if power:
            out.append((factor, power))
    return tuple(out)


def bm(a, b):
    return a[0]+b[0], bn(a[1]+b[1])


def bi(a):
    return -a[0], bn((factor, -power) for factor, power in a[1][::-1])


def mul(a, b):
    return bm(a[0], b[0]), torus.multiply(a[1], b[1])


def inv(a):
    return bi(a[0]), torus.inverse(a[1])


ONE = ((0, ()), torus.ONE)
X = ((1, ((1, 2), (0, 1))), torus.X)
Y = ((1, ((0, 1), (1, 2))), torus.Y)
SIGNED = (X, inv(X), Y, inv(Y))


def evaluate(word):
    answer = ONE
    for c in word:
        answer = mul(answer, SIGNED['xXyY'.index(c)])
    return answer


START = (evaluate('xxxYYYY'), evaluate('xyxYXY'))
TARGET = (X, Y)
BRAID_PATH = (5, 13, 11, 5, 7, 2, 7, 7, 8, 5)
BRAID_ALIGNED = (3, 3, 3) + BRAID_PATH
TORUS_ALIGNED = (5,) + torus.PATH8


def apply(state, op):
    values = list(state)
    kind, i, *rest = torus.MOVES[op]
    if kind == 'invert':
        values[i] = inv(values[i])
    elif kind == 'multiply':
        donor = values[1-i]
        values[i] = mul(values[i], donor if rest[0] > 0 else inv(donor))
    else:
        g = SIGNED['xXyY'.index(rest[0])]
        values[i] = mul(mul(g, values[i]), inv(g))
    return tuple(values)


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


def search(depth, budget):
    begun = time.monotonic()
    forward, fc, fd = ball(START, depth, budget)
    backward, bc, bd = ball(TARGET, depth, budget)
    common = forward.keys() & backward.keys()
    result = {'group': 'B3 times T(3,4)', 'depth_per_side': depth,
              'forward_layer_sizes': fc, 'backward_layer_sizes': bc,
              'forward_states': len(forward), 'backward_states': len(backward),
              'complete': fd and bd, 'seconds': round(time.monotonic()-begun, 3)}
    if common:
        meet = min(common, key=lambda s: forward[s][2]+backward[s][2])
        path = torus.path_to(forward, meet)
        path += [torus.inverse_op(op) for op in torus.path_to(backward, meet)[::-1]]
        at = START
        for op in path:
            at = apply(at, op)
        assert at == TARGET
        result.update({'path_found': True, 'move_ids': path,
                       'moves': [torus.MOVES[op] for op in path],
                       'distance': len(path) if fd and bd else None})
    else:
        result.update({'path_found': False,
                       'distance_lower_bound': 2*depth+1 if fd and bd else None})
    return result


def free_path(state, path, conjugators=None):
    for op in path:
        if op >= 6 and conjugators is not None:
            _, i, g = torus.MOVES[op]
            word = conjugators[g]
            values = list(state)
            values[i] = torus.free_reduce(word + values[i] + torus.free_inverse(word))
            state = tuple(values)
        else:
            state = torus.free_apply(state, op)
    return state


def product_certificate():
    p, b = 'xxxYYYY', 'xyxYXY'
    pure_b = free_path((p, ''), BRAID_PATH)
    pure_t = free_path(('', b), torus.PATH8)
    assert evaluate(pure_b[0]) == (X[0], torus.ONE)
    assert evaluate(pure_b[1]) == (Y[0], torus.ONE)
    assert evaluate(pure_t[0]) == ((0, ()), torus.X)
    assert evaluate(pure_t[1]) == ((0, ()), torus.Y)
    replacements_b = dict(zip('xXyY', (pure_b[0], torus.free_inverse(pure_b[0]),
                                      pure_b[1], torus.free_inverse(pure_b[1]))))
    replacements_t = dict(zip('xXyY', (pure_t[0], torus.free_inverse(pure_t[0]),
                                      pure_t[1], torus.free_inverse(pure_t[1]))))
    bare_b = tuple(op for op in BRAID_ALIGNED if op < 6)
    bare_t = tuple(op for op in TORUS_ALIGNED if op < 6)
    assert free_path(('x', 'y'), bare_b) == free_path(('x', 'y'), bare_t)
    inverse_bare = tuple(torus.inverse_op(op) for op in bare_b[::-1])
    state = [p, b]
    quotient = START
    strict_moves = []
    peak = sum(map(len, state))
    phase_endpoints = []

    def primitive(move):
        nonlocal quotient, peak
        strict_moves.append(move)
        i = move['i']
        if move['op'] == 'invert':
            state[i] = torus.free_inverse(state[i])
            quotient = apply(quotient, i)
        elif move['op'] == 'multiply':
            state[i] = torus.free_reduce(state[i] + state[1-i])
            quotient = apply(quotient, 2 if i == 0 else 4)
        else:
            g = move['g']
            state[i] = torus.free_reduce(g+state[i]+torus.free_inverse(g))
            quotient = apply(quotient, 6+4*i+'xXyY'.index(g))
        peak = max(peak, sum(map(len, state)))

    for phase, path, replacements in (
        ('aligned-braid-path-with-pure-braid-conjugators', BRAID_ALIGNED, replacements_b),
        ('inverse-common-bare-Nielsen-word', inverse_bare, None),
        ('aligned-torus-path-with-pure-torus-conjugators', TORUS_ALIGNED, replacements_t),
    ):
        for op in path:
            kind, i, *rest = torus.MOVES[op]
            if kind == 'invert':
                primitive({'op': 'invert', 'i': i})
            elif kind == 'multiply':
                if rest[0] == -1:
                    primitive({'op': 'invert', 'i': 1-i})
                primitive({'op': 'multiply', 'i': i, 'j': 1-i})
                if rest[0] == -1:
                    primitive({'op': 'invert', 'i': 1-i})
            else:
                assert replacements is not None
                # Applying one-letter conjugations in reverse word order
                # composes to conjugation by the stated ambient word.
                for g in replacements[rest[0]][::-1]:
                    primitive({'op': 'conjugate', 'i': i, 'g': g})
        assert tuple(evaluate(w) for w in state) == quotient
        phase_endpoints.append({'phase': phase, 'moves_so_far': len(strict_moves),
                                'free_lengths': list(map(len, state)),
                                'quotient_pair': quotient})
    assert quotient == TARGET
    assert tuple(state) != ('x', 'y')
    return {'format': 'ordinary-ac-elementary-v1',
            'scope': 'Synchronized B3-times-torus quotient certificate, not a free-group trivialization',
            'start': [p, b], 'target': state, 'moves': strict_moves,
            'quotient_group': 'B3 times <x,y | x^3=y^4>',
            'quotient_target': ['x', 'y'],
            'free_endpoint_lengths': list(map(len, state)),
            'peak_free_total_length': peak,
            'pure_braid_generator_words': pure_b,
            'pure_torus_generator_words': pure_t,
            'common_bare_Nielsen_images': free_path(('x', 'y'), bare_b),
            'phase_endpoints': phase_endpoints}


def verify_saved(saved):
    """Replay a saved ledger without regenerating its synchronization program."""
    if saved.get('format') != 'ordinary-ac-elementary-v1':
        raise ValueError('wrong format')
    if saved['start'] != ['xxxYYYY', 'xyxYXY']:
        raise ValueError('wrong start')
    raw = list(saved['start'])
    group = START
    peak = sum(map(len, raw))
    for move in saved['moves']:
        i = move.get('i')
        if type(i) is not int or i not in (0, 1):
            raise ValueError('invalid coordinate')
        if move.get('op') == 'invert' and set(move) == {'op', 'i'}:
            op = i
            raw[i] = torus.free_inverse(raw[i])
        elif move.get('op') == 'multiply' and set(move) == {'op', 'i', 'j'}:
            if type(move['j']) is not int or move['j'] != 1-i:
                raise ValueError('invalid donor')
            op = 2 if i == 0 else 4
            raw[i] = torus.free_reduce(raw[i] + raw[1-i])
        elif move.get('op') == 'conjugate' and set(move) == {'op', 'i', 'g'}:
            g = move['g']
            if not isinstance(g, str) or len(g) != 1 or g not in 'xXyY':
                raise ValueError('invalid conjugator')
            op = 6+4*i+'xXyY'.index(g)
            raw[i] = torus.free_reduce(g+raw[i]+torus.free_inverse(g))
        else:
            raise ValueError('invalid primitive')
        group = apply(group, op)
        peak = max(peak, sum(map(len, raw)))
    if raw != saved['target']:
        raise ValueError('actual free endpoint mismatch')
    if group != TARGET or tuple(evaluate(w) for w in raw) != TARGET:
        raise ValueError('quotient endpoint is not the diagonal basis')
    return {'strict_moves': len(saved['moves']), 'free_endpoint_lengths': list(map(len, raw)),
            'peak_free_total_length': peak, 'quotient_endpoint': ['x', 'y'],
            'ordinary_free_group_goal_solved': raw == ['x', 'y']}


def selftest():
    assert START[0][1] == torus.ONE and START[1][0] == (0, ())
    assert evaluate('xxxYYYY') != ONE and evaluate('xyxYXY') != ONE
    assert mul(START[0], START[1]) == mul(START[1], START[0])
    assert evaluate('xyxyxy')[0] == (6, ())
    assert evaluate('xyxyxy')[0] != (0, ())
    assert evaluate('xxx')[1] == (1, ())
    assert mul(X, Y) != mul(Y, X)
    for state in (START, TARGET):
        for op in range(14):
            assert apply(apply(state, op), torus.inverse_op(op)) == state


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--depth', type=int, default=5)
    parser.add_argument('--budget', type=int, default=500000)
    parser.add_argument('--output')
    parser.add_argument('--certificate')
    parser.add_argument('--certificate-only', action='store_true')
    parser.add_argument('--verify-certificate')
    args = parser.parse_args()
    selftest()
    if args.verify_certificate:
        with open(args.verify_certificate) as f:
            print(json.dumps(verify_saved(json.load(f)), indent=2))
        raise SystemExit(0)
    if args.certificate:
        saved = product_certificate()
        with open(args.certificate, 'w') as f:
            json.dump(saved, f, indent=2)
            f.write('\n')
        print(json.dumps({'strict_moves': len(saved['moves']),
                          'free_endpoint_lengths': saved['free_endpoint_lengths'],
                          'peak_free_total_length': saved['peak_free_total_length']}))
    if args.certificate_only:
        raise SystemExit(0)
    result = search(args.depth, args.budget)
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
            f.write('\n')
    print(json.dumps(result, indent=2))
