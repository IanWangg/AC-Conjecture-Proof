"""Exact ordinary-AC entry and deletion-quotient model for a cyclic15 state.

The searches in this file are finite checks, not an AC obstruction. Research
K separately supplies an unbounded finite-quotient exclusion for this model.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
from elementary_verify import inverse, reduce, replay
from psl2z_search import normal_word, evaluate as braid_evaluate
from torus_search import evaluate as torus_evaluate

P, B, BP = 'xxxYYYY', 'xyxYXY', 'XXyxYxxY'
R = 'XXXyxYxxY'
FACTORS = [(1, 'XXy'), (-1, 'XX'), (1, 'xyxYXXX'), (-1, 'xyxYXXXy')]
POWER_FACTORS = [(-1, 'XXyxYXY'), (-1, 'XyxYXY'), (-1, 'yxYXY')]


def fixed_entry(recipient, prefix, factors, target):
    donor = 1-recipient
    start = [P, B]
    base = reduce(prefix+start[recipient]+inverse(prefix))
    difference = ''
    for sign, q in factors:
        relator = start[donor] if sign == 1 else inverse(start[donor])
        difference = reduce(difference + q + relator + inverse(q))
    assert difference == reduce(target[recipient] + inverse(base))
    state, moves = [P, B], []

    def emit(op, i, **args):
        moves.append(dict(op=op, i=i, **args))
        if op == 'invert':
            state[i] = inverse(state[i])
        elif op == 'multiply':
            state[i] = reduce(state[i] + state[args['j']])
        else:
            g = args['g']
            state[i] = reduce(g + state[i] + inverse(g))

    def conjugate(i, word):
        for g in reversed(word):
            emit('conjugate', i, g=g)

    # Left multiply by the factors in reverse order. The donor is restored
    # literally after every operation; no quotient equality is used as a move.
    conjugate(recipient, prefix)
    for sign, q in reversed(factors):
        conjugate(donor, q)
        if sign == 1:
            emit('invert', donor)
        emit('invert', recipient)
        emit('multiply', recipient, j=donor)
        emit('invert', recipient)
        if sign == 1:
            emit('invert', donor)
        conjugate(donor, inverse(q))
    assert state == target
    cert = {'format': 'ordinary-ac-elementary-v1', 'start': [P, B],
            'target': target, 'moves': moves,
            'scope': 'Reachable cyclic15 state; not a trivialization',
            'recipient': recipient, 'initial_conjugator': prefix,
            'fixed_donor_factors': [{'sign': s, 'conjugator': q} for s, q in factors]}
    replay(cert)
    return cert


def entry_certificate():
    return fixed_entry(1, '', FACTORS, [P, BP])


def power_entry_certificate():
    return fixed_entry(0, 'yXX', POWER_FACTORS, [R, B])


def kernel_inverse(word):
    return word.swapcase()[::-1]


def kernel_reduce(word):
    out = []
    for c in word:
        if out and out[-1] == c.swapcase():
            out.pop()
        else:
            out.append(c)
    return ''.join(out)


@lru_cache(maxsize=None)
def alpha(word, power=1):
    forward = dict(a='b', A='B', b='aB', B='bA')
    backwards = dict(a='ba', A='AB', b='a', B='A')
    substitution = forward if power >= 0 else backwards
    for _ in range(abs(power)):
        word = kernel_reduce(''.join(substitution[c] for c in word))
    return word


def q_evaluate(word):
    images = {'x': ('', 1), 'X': ('', -1), 'y': ('aB', 1), 'Y': ('B', -1)}
    u, exponent = '', 0
    for c in word:
        v, step = images[c]
        u = kernel_reduce(u + alpha(v, exponent))
        exponent += step
    return u, exponent


@lru_cache(maxsize=None)
def alpha3(word, power=1):
    forward = dict(a='b', A='B', b='c', B='C', c='aB', C='bA')
    backwards = dict(a='ca', A='AC', b='a', B='A', c='b', C='B')
    substitution = forward if power >= 0 else backwards
    for _ in range(abs(power)):
        word = kernel_reduce(''.join(substitution[c] for c in word))
    return word


def q3_evaluate(word):
    images = {'x': ('', 1), 'X': ('', -1), 'y': ('a', 0), 'Y': ('A', 0)}
    u, exponent = '', 0
    for c in word:
        v, step = images[c]
        u = kernel_reduce(u + alpha3(v, exponent))
        exponent += step
    return u, exponent


def second_q2_evaluate(word):
    images = {'x': ('a', 0), 'X': ('A', 0), 'y': ('', 1), 'Y': ('', -1)}
    u, exponent = '', 0
    for c in word:
        v, step = images[c]
        u = kernel_reduce(u + alpha(v, exponent))
        exponent += step
    return u, exponent


def cyclic_syllables(syllables, orders):
    out = list(syllables)
    while len(out) > 1 and out[0][0] == out[-1][0]:
        factor, left = out.pop(0)
        right = out.pop()[1]
        power = (left + right) % orders[factor]
        if power:
            out.append((factor, power))
    return tuple(out)


def necklace(syllables, orders):
    s = cyclic_syllables(syllables, orders)
    return min((s[k:] + s[:k] for k in range(len(s))), default=())


def exponent_vector(word):
    return word.count('x')-word.count('X'), word.count('y')-word.count('Y')


def free_necklace(word):
    return min(t[k:]+t[:k] for t in (word, inverse(word)) for k in range(len(t)))


def cyclic_words(size):
    def visit(prefix):
        if len(prefix) == size:
            if prefix[0] != prefix[-1].swapcase():
                yield prefix
            return
        for c in 'xXyY':
            if not prefix or c != prefix[-1].swapcase():
                yield from visit(prefix+c)
    yield from visit('')


def enumeration():
    # In either central-extension group, free-product conjugacy together
    # with the infinite abelian character is an exact conjugacy test.
    p_targets = {(sum(exponent_vector(w)), necklace(normal_word(w), (2, 3))) for w in (P, inverse(P))}
    b_targets = {(4*exponent_vector(w)[0]+3*exponent_vector(w)[1],
                  necklace(torus_evaluate(w)[1], (3, 4))) for w in (B, inverse(B))}
    result = {}
    for size, target, mode in [(8, b_targets, 'braid8_in_torus'), (9, p_targets, 'power9_in_braid')]:
        candidates = []
        for word in cyclic_words(size):
            x, y = exponent_vector(word)
            key = (4*x+3*y, necklace(torus_evaluate(word)[1], (3, 4))) if mode.startswith('braid') else (x+y, necklace(normal_word(word), (2, 3)))
            if key in target:
                candidates.append(word)
        result[mode] = {'raw_candidates': len(candidates),
                        'cyclic_inverse_representatives': sorted({free_necklace(w) for w in candidates})}
    # The two new frozen-braid orbits are related by simultaneous inversion.
    b2 = 'xyXXYxxY'
    assert free_necklace(BP.swapcase()) == free_necklace(b2)
    result['braid8_two_orbit_claim'] = set(result['braid8_in_torus']['cyclic_inverse_representatives']) == {free_necklace(BP), free_necklace(b2)}
    swap = str.maketrans('xXyY', 'yYxX')
    representatives = set(result['power9_in_braid']['cyclic_inverse_representatives'])
    symmetry_classes = []
    while representatives:
        word = min(representatives)
        orbit = {free_necklace(w) for w in (word, word.swapcase(), word.translate(swap), word.swapcase().translate(swap))}
        assert orbit <= set(result['power9_in_braid']['cyclic_inverse_representatives'])
        symmetry_classes.append(sorted(orbit))
        representatives -= orbit
    result['power9_signed_symmetry_classes'] = symmetry_classes
    return result


def selftest():
    for c in 'aAbB':
        assert alpha(alpha(c), -1) == c and alpha(alpha(c, -1)) == c
    assert q_evaluate(BP) == ('', 0)
    assert q_evaluate('XXyx') == ('a', 0)
    assert q_evaluate('Xy') == ('b', 0)
    assert q_evaluate('xY') == ('bA', 0)
    assert q_evaluate(inverse(P)) == ('abbAbA', 1)
    assert torus_evaluate(B) == torus_evaluate(BP)
    assert q_evaluate(B) != ('', 0)
    for c in 'aAbBcC':
        assert alpha3(alpha3(c), -1) == c and alpha3(alpha3(c, -1)) == c
    assert q3_evaluate(R) == ('', 0)
    assert q3_evaluate('y') == ('a', 0)
    assert q3_evaluate('xyX') == ('b', 0)
    assert q3_evaluate('xxyXX') == ('c', 0)
    assert q3_evaluate(B) == ('bCB', 1)
    for q, target in [('aBB', 'yXYXyxx'), ('BB', 'YxYXyyx')]:
        image = kernel_reduce(q+'abbAbA'+kernel_inverse(alpha(q)))
        assert q_evaluate(target) == (image, 1)
    assert second_q2_evaluate('YxYXyyx') == ('', 0)
    assert second_q2_evaluate(inverse(BP)) == ('BAbb', 1)
    substitution = {'x': 'X', 'X': 'x', 'y': 'Yx', 'Y': 'Xy'}
    image_u1 = reduce(''.join(substitution[c] for c in 'yXYXyxx'))
    image_bp = reduce(''.join(substitution[c] for c in BP))
    assert image_u1 == 'YxyxYX' and braid_evaluate(image_u1) == (1, 0, 0, 1)
    matrix = braid_evaluate(image_bp)
    assert abs(matrix[0]+matrix[3]) == 14


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--entry-output')
    parser.add_argument('--power-entry-output')
    parser.add_argument('--output')
    args = parser.parse_args()
    selftest()
    cert = entry_certificate()
    if args.entry_output:
        Path(args.entry_output).write_text(json.dumps(cert, indent=2)+'\n')
    power_cert = power_entry_certificate()
    if args.power_entry_output:
        Path(args.power_entry_output).write_text(json.dumps(power_cert, indent=2)+'\n')
    result = {'entry_replay': replay(cert), 'new_deletion_quotient': 'F(a,b) semidirect_alpha Z',
              'alpha': {'a': 'b', 'b': 'aB'}, 'power_inverse_normal_form': ['abbAbA', 1],
              'primitive_candidate_kernel': '(bA)^k', 'enumeration': enumeration(),
              'power9_entry_replay': replay(power_cert),
              'power9_deletion_quotient': {'fiber_rank': 3, 'alpha': {'a': 'b', 'b': 'c', 'c': 'aB'},
                                           'braid_normal_form': ['bCB', 1], 'primitive_candidate_kernel': 'a^k'},
              'actual_twisted_edges': [{'fiber_conjugator': 'aBB', 'target': 'yXYXyxx'},
                                       {'fiber_conjugator': 'BB', 'target': 'YxYXyyx'}],
              'u1_braid_model': {'images': {'x': 'U^-1', 'y': 'V^-1 U'},
                                 'bprime_image': 'UU V^-1 U^-1 V U^-3 V', 'bprime_trace_absolute': 14},
              'u2_free_by_cyclic_model': {'stable': 'y', 'fiber_a': 'x',
                                          'bprime_inverse_kernel': 'BAbb', 'primitive_kernel': 'a^k'},
              'scope': 'Exact reachable waypoint and finite classifications; no free-group solution'}
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
