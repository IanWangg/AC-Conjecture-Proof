"""Exact F2 primitive-coordinate audit via Nielsen uniqueness.

This uses positive Euclidean primitive representatives and cyclic rotation,
not Whitehead descent. The mathematical equivalence is proved in O's
cyclic review. Python's standard library is sufficient.
"""
import argparse
from functools import lru_cache
import hashlib
import json
from math import gcd
from pathlib import Path


@lru_cache(None)
def positive(a,b):
    assert a>=0 and b>=0 and gcd(a,b)==1
    if a==0:return 'y'
    if b==0:return 'x'
    if a==b:return 'xy'
    if a>b:return positive(a-b,b).replace('y','xy')
    return positive(a,b-a).replace('x','xy')


def primitive_cyclic_word(word):
    for alphabet in ('xy','xY','Xy','XY'):
        if not set(word)<=set(alphabet):continue
        a=word.count(alphabet[0])
        b=word.count(alphabet[1])
        if gcd(a,b)!=1:return False
        model=positive(a,b).translate(str.maketrans({'x':alphabet[0],'y':alphabet[1]}))
        return len(word)==len(model) and word in model+model
    return False


def validate_cyclic(word):
    assert word and set(word)<=set('xXyY')
    assert all(a!=b.swapcase() for a,b in zip(word,word[1:]+word[:1]))


def controls():
    count=0
    for a in range(26):
        for b in range(26):
            if gcd(a,b)!=1:continue
            word=positive(a,b)
            assert word.count('x')==a and word.count('y')==b
            for alphabet in ('xy','xY','Xy','XY'):
                signed=word.translate(str.maketrans({'x':alphabet[0],'y':alphabet[1]}))
                for cut in (0,len(signed)//2):
                    assert primitive_cyclic_word(signed[cut:]+signed[:cut])
                    count+=1
    for word in ('xx','xxxYYYY','xyxYXY','xxxyy'):
        validate_cyclic(word)
        assert not primitive_cyclic_word(word)
    assert primitive_cyclic_word('xxyxy')
    return count


def audit(path):
    content=Path(path).read_bytes()
    states=json.loads(content)
    assert all(isinstance(pair,list) and len(pair)==2 for pair in states)
    words=sorted({word for pair in states for word in pair})
    positives=[]
    rejected={'mixed_signs':0,'noncoprime_exponents':0,'wrong_cyclic_word':0}
    for word in words:
        validate_cyclic(word)
        if primitive_cyclic_word(word):
            positives.append(word)
            continue
        alphabets=[a for a in ('xy','xY','Xy','XY') if set(word)<=set(a)]
        if not alphabets:rejected['mixed_signs']+=1
        elif gcd(word.count(alphabets[0][0]),word.count(alphabets[0][1]))!=1:
            rejected['noncoprime_exponents']+=1
        else:rejected['wrong_cyclic_word']+=1
    return {'status':'PASS','ordinary_AC_goal_solved':False,
            'catalogue_sha256':hashlib.sha256(content).hexdigest(),
            'states':len(states),'distinct_cyclic_coordinate_orbits':len(words),
            'primitive_coordinates':positives,'rejections':rejected,
            'positive_signed_rotation_controls':controls(),
            'method':'Nielsen uniqueness plus exact positive Euclidean representatives and cyclic rotations; no Whitehead descent',
            'scope':'Displayed cyclic coordinate classes and every free conjugate/inverse of them; not arbitrary elements of their generated subgroups'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('catalogue')
    parser.add_argument('--output')
    args=parser.parse_args()
    result=audit(args.catalogue)
    text=json.dumps(result,indent=2)+'\n'
    if args.output:Path(args.output).write_text(text)
    print(text,end='')
