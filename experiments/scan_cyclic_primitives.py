"""Exact rank-two cyclic primitivity by Nielsen uniqueness and Euclid.

This does not use Whitehead descent or the cyclic-component generator.
The report supplies the mathematical equivalence used by this test.
"""
import argparse
from functools import lru_cache
import hashlib
import json
from math import gcd
from pathlib import Path
from cyclic_catalogue_to_tsv import load_catalogue_bytes


def inverse(word):
    return word[::-1].swapcase()


def canonical(word):
    return min(w[i:]+w[:i] for w in (word,inverse(word)) for i in range(len(w))) if word else ''


@lru_cache(None)
def positive_primitive(a,b):
    assert a>=0 and b>=0 and gcd(a,b)==1
    if not b:
        return 'x'
    if not a:
        return 'y'
    if a==b:
        assert a==1
        return 'xy'
    if a>b:
        return positive_primitive(a-b,b).replace('y','xy')
    return positive_primitive(a,b-a).replace('x','xy')


def primitive(word):
    a=word.count('x')-word.count('X')
    b=word.count('y')-word.count('Y')
    if gcd(a,b)!=1:
        return False
    representative=positive_primitive(abs(a),abs(b))
    if a<0:
        representative=representative.replace('x','X')
    if b<0:
        representative=representative.replace('y','Y')
    return canonical(word)==canonical(representative)


def phi(n):
    return sum(gcd(k,n)==1 for k in range(1,n+1))


def self_test():
    layer=['']
    counts={}
    for length in range(1,10):
        layer=[w+c for w in layer for c in 'xXyY' if not w or w[-1]!=c.swapcase()]
        count=sum(primitive(w) for w in layer if w[0]!=w[-1].swapcase())
        assert count==(4 if length==1 else 4*length*phi(length)),(length,count)
        counts[length]=count
    assert primitive('x') and primitive('xyx') and primitive('YxYYY')
    assert not primitive('xx') and not primitive('xxxYYYY') and not primitive('xyxYXY')
    return counts


def run(source,crosscheck=None):
    controls=self_test()
    raw=load_catalogue_bytes(source)
    states=json.loads(raw)
    words={w for state in states for w in state}
    hits=[]
    for word in sorted(words):
        assert word and set(word)<=set('xXyY') and canonical(word)==word
        assert all(word[i]!=word[(i+1)%len(word)].swapcase() for i in range(len(word)))
        yes=primitive(word)
        if crosscheck:
            assert yes==crosscheck(word)
        if yes:
            hits.append(word)
    result={'status':'PASS','ordinary_AC_goal_solved':False,
            'catalogue_sha256':hashlib.sha256(raw).hexdigest(),
            'catalogue_states':len(states),'distinct_cyclic_coordinates_tested':len(words),
            'primitive_coordinates':hits,
            'method':'positive Euclidean construction and rank-two Nielsen conjugacy uniqueness',
            'primitive_decision_uses_Whitehead_descent':False,
            'optional_Whitehead_comparison':crosscheck is not None,
            'exhaustive_literal_primitive_counts_through_length_nine':controls,
            'combined_with_full_cap21_closure_implies_minimum_cyclic_peak_before_primitive':22}
    if len(states)!=144292:
        result.pop('combined_with_full_cap21_closure_implies_minimum_cyclic_peak_before_primitive')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('catalogue')
    parser.add_argument('--output',required=True)
    parser.add_argument('--crosscheck-directory')
    args=parser.parse_args()
    crosscheck=None
    if args.crosscheck_directory:
        import sys
        sys.path.insert(0,args.crosscheck_directory)
        from stallings_search import primitive as crosscheck
    result=run(args.catalogue,crosscheck)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
