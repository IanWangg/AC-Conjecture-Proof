"""Uniform AC path in T_n=<x,y | x^n=y^(n+1)>; not in the free group.

Only strict primitives are used: positive right multiplication and signed
single-generator conjugation g*r*g^-1. The saved free lift has its ACTUAL
free endpoint, rather than an implicit quotient endpoint.
"""
import argparse
import json


def inverse(word):
    return word.swapcase()[::-1]


def reduce(word):
    stack = []
    for letter in word:
        if letter not in 'xXyY':
            raise ValueError('invalid letter')
        if stack and stack[-1] == letter.swapcase():
            stack.pop()
        else:
            stack.append(letter)
    return ''.join(stack)


def exponent_vector(word):
    return [word.count('x')-word.count('X'), word.count('y')-word.count('Y')]


class Torus:
    """Normal form z^k followed by alternating nonidentity finite residues.

    z=x^n=y^(n+1). A syllable (0,a) means x^a; (1,a) means y^a.
    The central exponent is retained: this is not merely C_n*C_(n+1).
    """
    def __init__(self, n):
        if type(n) is not int or n < 2:
            raise ValueError('n must be an integer >=2')
        self.n = n

    def normal(self, central, syllables):
        out = []
        for factor, power in syllables:
            if out and out[-1][0] == factor:
                power += out.pop()[1]
            turns, power = divmod(power, self.n+factor)
            central += turns
            if power:
                out.append((factor, power))
        return central, tuple(out)

    def multiply(self, a, b):
        return self.normal(a[0]+b[0], a[1]+b[1])

    def inverse(self, a):
        return self.normal(-a[0], ((f,-p) for f,p in reversed(a[1])))

    def evaluate(self, word):
        return self.normal(0, ((0 if c.lower() == 'x' else 1,
                                1 if c.islower() else -1) for c in word))


def moves(n):
    if type(n) is not int or n < 2:
        raise ValueError('n must be an integer >=2')
    path = [{'op':'multiply','i':0,'j':1}]
    for _ in range(n-1):
        path += [{'op':'conjugate','i':1,'g':'x'},
                 {'op':'multiply','i':1,'j':0}]
    path += [{'op':'multiply','i':0,'j':1},
             {'op':'conjugate','i':1,'g':'Y'},
             {'op':'conjugate','i':1,'g':'X'}]
    return path


def meridian_moves(n):
    path = [{'op':'multiply','i':0,'j':1}]
    for _ in range(n-1):
        path += [{'op':'conjugate','i':1,'g':'Y'},
                 {'op':'multiply','i':1,'j':0}]
    path.append({'op':'multiply','i':0,'j':1})
    return path


def replay_free(start, path):
    state = list(map(reduce, start))
    peak = sum(map(len, state))
    for move in path:
        i = move['i']
        if move['op'] == 'multiply':
            state[i] = reduce(state[i]+state[move['j']])
        elif move['op'] == 'conjugate':
            g = move['g']
            state[i] = reduce(g+state[i]+inverse(g))
        else:
            raise ValueError('unknown primitive')
        peak = max(peak, sum(map(len, state)))
    return state, peak


def verify_family_member(n):
    group = Torus(n)
    b = 'xyxYXY'
    # Independently check the closed formula for every cancellation-loop
    # stage in the free group, with first coordinate fixed exactly as b.
    recipient = b
    for k in range(n):
        expected = 'x'*(k+1)+'yx'+'Y'*(k+1)+'XY'
        assert recipient == expected
        if k != n-1:
            recipient = reduce('x'+recipient+'X'+b)
    assert group.evaluate(recipient) == group.evaluate(inverse(b)+'x')
    ideal, _ = replay_free(['',b], moves(n))
    assert list(map(group.evaluate, ideal)) == [group.evaluate('x'),group.evaluate('y')]
    meridian_recipient = 'xY'
    for k in range(n):
        assert meridian_recipient == 'Y'*k+'x'*(k+1)+'Y'
        if k != n-1:
            meridian_recipient = reduce('Y'+meridian_recipient+'y'+'xY')
    meridian_endpoint, _ = replay_free(['','xY'],meridian_moves(n))
    assert list(map(group.evaluate,meridian_endpoint)) == [group.evaluate('x'),group.evaluate('y')]
    assert len(meridian_moves(n)) == 2*n
    power = 'x'*n+'Y'*(n+1)
    assert group.evaluate(power) == (0, ())
    assert group.evaluate('x'*n) == group.evaluate('y'*(n+1)) == (1, ())
    start = [power,b]
    actual, peak = replay_free(start,moves(n))
    assert list(map(group.evaluate, actual)) == [group.evaluate('x'),group.evaluate('y')]
    expected_vectors = [[n*n+n+1,-(n+1)*(n+1)], [n*n,1-n*n-n]]
    vectors = list(map(exponent_vector, actual))
    assert vectors == expected_vectors
    assert actual != ['x','y']
    assert len(moves(n)) == 2*n+2
    return {'n':n,'strict_moves':len(moves(n)),
            'meridian_strict_moves':len(meridian_moves(n)),
            'free_endpoint_lengths':list(map(len,actual)),
            'free_peak_total_length':peak,
            'endpoint_exponent_vectors':vectors,
            'quotient_endpoint':['x','y'],
            'quotient_central_power_test':'x^n=y^(n+1)=z != 1'}


def certificate(n):
    start = ['x'*n+'Y'*(n+1),'xyxYXY']
    endpoint, peak = replay_free(start,moves(n))
    verify_family_member(n)
    return {'format':'ordinary-ac-elementary-v1',
            'scope':'Actual free lift of a torus-quotient path; endpoint is not the free basis',
            'n':n,'start':start,'target':endpoint,'moves':moves(n),
            'quotient':f'<x,y | x^{n}=y^{n+1}>',
            'quotient_target':['x','y'],
            'free_peak_total_length':peak,
            'endpoint_exponent_vectors':list(map(exponent_vector,endpoint))}


def selftest():
    rows = [verify_family_member(n) for n in range(2,41)]
    for n in (2,3,4,7,12):
        group = Torus(n)
        for word in ('','x','Y','xyxYXY','XXyxYxxY','XYxyxxyYY'):
            element = group.evaluate(word)
            assert group.multiply(element,group.inverse(element)) == (0,())
            assert group.evaluate(word+inverse(word)) == (0,())
        assert group.evaluate('x'*n+'y') == group.evaluate('y'+'x'*n)
    return {'parameters_checked':'n=2..40','family_checks_passed':len(rows),
            'scope':'Finite implementation checks; the note gives the all-n symbolic proof'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n',type=int,default=3)
    parser.add_argument('--selftest',action='store_true')
    parser.add_argument('--output')
    args = parser.parse_args()
    report = verify_family_member(args.n)
    if args.selftest:
        report['selftest'] = selftest()
    if args.output:
        with open(args.output,'w') as stream:
            json.dump(certificate(args.n),stream,indent=2)
            stream.write('\n')
    print(json.dumps(report,indent=2))
