"""Independent quality gate for G's product synchronization certificate.

Uses H's Torus class, a separately written C2*C3-plus-exponent braid
evaluator, and the root strict free-word verifier. No G code is imported.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path

from torus_family import Torus, inverse, reduce


def braid_normal(syllables):
    out = []
    for factor,power in syllables:
        if out and out[-1][0] == factor:
            power += out.pop()[1]
        power %= (2,3)[factor]
        if power:
            out.append((factor,power))
    return tuple(out)


def braid_evaluate(word):
    images = {'x':((1,2),(0,1)), 'X':((0,1),(1,1)),
              'y':((0,1),(1,2)), 'Y':((1,1),(0,1))}
    if not set(word) <= set(images):
        raise ValueError('invalid alphabet')
    return (sum(1 if c.islower() else -1 for c in word),
            braid_normal(s for c in word for s in images[c]))


def braid_multiply(a,b):
    return a[0]+b[0], braid_normal(a[1]+b[1])


def braid_inverse(a):
    return -a[0], braid_normal((f,-p) for f,p in reversed(a[1]))


def freeze(value):
    return tuple(map(freeze,value)) if isinstance(value,list) else value


def bare_replay(ledger, start=('x','y')):
    pair = list(start)
    for coordinate,sign in ledger:
        donor = pair[1-coordinate]
        pair[coordinate] = reduce(pair[coordinate]+(donor if sign == 1 else inverse(donor)))
    return pair


def review(path):
    data = json.loads(Path(path).read_text())
    here = Path(__file__).resolve().parent
    candidates = [here/'elementary_verify.py',here.parent/'root'/'elementary_verify.py']
    verifier_path = next(candidate for candidate in candidates if candidate.exists())
    spec = importlib.util.spec_from_file_location('strict_root_reviewer',verifier_path)
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    strict = verifier.replay(data)
    torus = Torus(3)

    def product_evaluate(word):
        return braid_evaluate(word),torus.evaluate(word)

    def product_multiply(a,b):
        return braid_multiply(a[0],b[0]),torus.multiply(a[1],b[1])

    def product_inverse(a):
        return braid_inverse(a[0]),torus.inverse(a[1])

    # Central controls ensure that equality in a smaller free-product
    # quotient is not silently substituted for equality in either factor.
    assert braid_evaluate('xyxyxy') == (6,())
    assert torus.evaluate('xxx') == torus.evaluate('yyyy') == (1,())
    assert braid_evaluate('xyxYXY') == (0,())
    assert torus.evaluate('xxxYYYY') == (0,())

    identity = ((0,()),(0,()))
    diagonal = [product_evaluate('x'),product_evaluate('y')]
    pure_checks = []
    for factor,field in [(0,'pure_braid_generator_words'),(1,'pure_torus_generator_words')]:
        for generator,word in zip('xy',data[field]):
            expected = list(identity)
            expected[factor] = diagonal['xy'.index(generator)][factor]
            assert product_evaluate(word) == tuple(expected)
            pure_checks.append({'factor':('B3','T_3')[factor],
                                'generator':generator,'word_length':len(word),'passed':True})

    pb = [(0,-1)]*3+[(1,-1),(1,-1),(0,1),(1,-1)]
    pt = [(1,-1),(0,1),(1,1),(1,1),(0,1)]
    expected_bare = ['xyXyyyX','yyyX']
    assert bare_replay(pb) == bare_replay(pt) == expected_bare
    assert data['common_bare_Nielsen_images'] == expected_bare
    pb_inverse = [(i,-sign) for i,sign in reversed(pb)]
    assert bare_replay(pb_inverse,bare_replay(pb)) == ['x','y']
    assert bare_replay(pt,bare_replay(pb_inverse)) == ['x','y']

    quotient = list(map(product_evaluate,data['start']))
    free = list(data['start'])
    bare = ['x','y']
    peak = sum(map(len,free))
    phases = {entry['moves_so_far']:entry for entry in data['phase_endpoints']}
    phase_checks = []
    for step,move in enumerate(data['moves'],1):
        i = move['i']
        if move['op'] == 'invert':
            quotient[i] = product_inverse(quotient[i])
            free[i] = inverse(free[i])
            bare[i] = inverse(bare[i])
        elif move['op'] == 'multiply':
            j = move['j']
            quotient[i] = product_multiply(quotient[i],quotient[j])
            free[i] = reduce(free[i]+free[j])
            bare[i] = reduce(bare[i]+bare[j])
        else:
            g = move['g']
            quotient_g = product_evaluate(g)
            quotient[i] = product_multiply(product_multiply(quotient_g,quotient[i]),product_inverse(quotient_g))
            free[i] = reduce(g+free[i]+inverse(g))
        assert quotient == list(map(product_evaluate,free))
        peak = max(peak,sum(map(len,free)))
        if step in phases:
            entry = phases[step]
            assert list(map(len,free)) == entry['free_lengths']
            assert tuple(quotient) == freeze(entry['quotient_pair'])
            phase_checks.append({'moves_so_far':step,'exact_phase_endpoint_passed':True})
    assert quotient == diagonal
    assert free == data['target'] == strict['endpoint']
    assert bare == expected_bare
    assert free != ['x','y']
    assert list(map(len,free)) == [2539,2159]
    assert peak == strict['peak_total_length'] == 4698
    counts = Counter(move['op'] for move in data['moves'])
    assert counts == {'conjugate':156,'multiply':19,'invert':16}
    return {'status':'PASS','reviewer':'H','certificate_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            'scope':'Independent upper-certificate and synchronization-proof review; finite-ball lower bound not independently re-enumerated here',
            'G_implementation_imported':False,'torus_implementation':'H Torus(3)',
            'braid_implementation':'independent C2*C3 normal forms plus total exponent',
            'pure_factor_word_checks':pure_checks,'exact_common_bare_Nielsen_images':expected_bare,
            'bare_inverse_and_cancellation_passed':True,'phase_checks':phase_checks,
            'primitive_counts':dict(counts),'quotient_endpoint':'diagonal (x,y) in B3 times T_3',
            'free_endpoint_lengths':list(map(len,free)),'peak_free_total_length':peak,
            'ordinary_free_group_goal_solved':False,'synchronization_proof_issue_found':False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate')
    parser.add_argument('--output')
    args = parser.parse_args()
    report = review(args.certificate)
    if args.output:
        Path(args.output).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
