"""Independent word-ledger and B3 Fox replay of the first-order certificate.

No imports from its constructor or relation-module implementation. Passing
means equality in F/[N,N], never that the actual free endpoint is the basis.
"""
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path
from elementary_verify import inverse, reduce

IMAGES = {'x': ((1, 2), (0, 1)), 'X': ((0, 1), (1, 1)),
          'y': ((0, 1), (1, 2)), 'Y': ((1, 1), (0, 1))}
IDENTITY = (0, ())


def fox(word):
    """B3 image plus two left Fox derivatives in integral Z[B3]."""
    stack, exponent = [], 0
    coefficients = [{}, {}]

    def add(i, key, coefficient):
        new = coefficients[i].get(key, 0) + coefficient
        if new:
            coefficients[i][key] = new
        else:
            coefficients[i].pop(key, None)

    for c in word:
        if c not in IMAGES:
            raise ValueError('word outside the free alphabet')
        i = 0 if c in 'xX' else 1
        if c.islower():
            add(i, (exponent, tuple(stack)), 1)
        for factor, power in IMAGES[c]:
            modulus = 2 if factor == 0 else 3
            if stack and stack[-1][0] == factor:
                power = (power + stack.pop()[1]) % modulus
            if power:
                stack.append((factor, power))
        exponent += 1 if c.islower() else -1
        if c.isupper():
            add(i, (exponent, tuple(stack)), -1)
    return (exponent, tuple(stack)), coefficients


def verify(path):
    raw = Path(path).read_bytes()
    if str(path).endswith('.gz.b64'):
        raw = gzip.decompress(base64.b64decode(raw))
    cert = json.loads(raw)
    if cert.get('format') != 'ordinary-ac-word-conjugation-v1':
        raise ValueError('unsupported word-ledger format')
    if cert['start'] != ['xxxYYYY', 'xyxYXY']:
        raise ValueError('wrong initial presentation')
    if fox('xyxYXY')[0] != IDENTITY or fox('xyxyxy')[0] == IDENTITY:
        raise AssertionError('braid quotient central control failed')
    current = cert['start'][:]
    count, boundary_peak, expanded_upper = 0, sum(map(len, current)), sum(map(len, current))
    for move in cert['moves']:
        i = move['i']
        if type(i) is not int or i not in (0, 1):
            raise ValueError('invalid coordinate')
        if move['op'] == 'invert':
            current[i] = inverse(current[i])
            count += 1
        elif move['op'] == 'multiply':
            j, sign = move['j'], move.get('sign', 1)
            if type(j) is not int or j not in (0, 1) or j == i or type(sign) is not int or sign not in (1, -1):
                raise ValueError('invalid multiplication')
            donor = current[j] if sign == 1 else inverse(current[j])
            current[i] = reduce(current[i] + donor)
            count += 1 if sign == 1 else 3
        elif move['op'] == 'conjugate':
            g = move.get('word', move.get('g'))
            if not isinstance(g, str) or not set(g) <= set('xXyY'):
                raise ValueError('invalid conjugating word')
            expanded_upper = max(expanded_upper, sum(map(len, current)) + 2*len(g))
            current[i] = reduce(g + current[i] + inverse(g))
            count += len(g)
        else:
            raise ValueError('unknown operation')
        boundary_peak = max(boundary_peak, sum(map(len, current)))
        expanded_upper = max(expanded_upper, sum(map(len, current)))
    if current != cert['target']:
        raise ValueError('actual free endpoint mismatch')
    if current == ['x', 'y']:
        raise AssertionError('unexpected free basis; requires separate full goal audit')
    for word, target in zip(current, 'xy'):
        image, derivatives = fox(word)
        target_image, target_derivatives = fox(target)
        if image != target_image or derivatives != target_derivatives:
            raise AssertionError('nonzero first-order quotient error')
    if count != cert['expanded_single_generator_move_count']:
        raise ValueError('expansion count mismatch')
    if [hashlib.sha256(w.encode()).hexdigest() for w in current] != cert['final_free_word_sha256']:
        raise ValueError('free word digest mismatch')
    return {'status': 'PASS', 'independent_free_and_Fox_replay': True,
            'quotient': 'F/[N,N], N=normal closure of xyxYXY',
            'word_operations': len(cert['moves']), 'expanded_single_generator_moves': count,
            'boundary_raw_peak': boundary_peak, 'expanded_raw_peak_upper_bound': expanded_upper,
            'actual_free_endpoint_lengths': list(map(len, current)), 'free_group_goal_solved': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate')
    parser.add_argument('--output')
    args = parser.parse_args()
    report = verify(args.certificate)
    if args.output:
        Path(args.output).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
