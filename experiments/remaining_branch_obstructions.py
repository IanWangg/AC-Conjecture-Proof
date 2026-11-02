"""Small exact checks for two further first-hump primitive exclusions.

The unbounded conclusions are analytic (Britton/Collins and transfer of
K's finite certificate); these finite checks validate the stated formulas.
"""
import argparse
import json
from pathlib import Path


def inverse(w):return w.swapcase()[::-1]
def reduce(w):
    out=[]
    for c in w:
        if out and out[-1]==c.swapcase():out.pop()
        else:out.append(c)
    return ''.join(out)
def power(w,k):return reduce((w if k>=0 else inverse(w))*abs(k))


def alpha(w,k=1):
    positive=dict(a='b',A='B',b='aB',B='bA')
    negative=dict(a='ba',A='AB',b='a',B='A')
    rule=positive if k>=0 else negative
    for _ in range(abs(k)):w=reduce(''.join(rule[c] for c in w))
    return w


def free_by_cyclic(w):
    images={'x':('',1),'X':('',-1),'y':('a',2),'Y':(alpha('A',-2),-2)}
    u,e='',0
    for c in w:
        v,f=images[c];u=reduce(u+alpha(v,e));e+=f
    return u,e


def hnn_tokens(w):
    answer=[0]
    for c in w:
        if c in 'xX':answer[-1]+=1 if c=='x' else -1
        else:answer.extend((c,0))
    return answer


def hnn_reduced(w,n):
    """Britton-reduce for <x,y | Y x^n y = x^(n+1)> over <x>."""
    data=hnn_tokens(w)
    while True:
        changed=False
        for i in range(1,len(data)-3,2):
            if data[i]==data[i+2]:continue
            divisor=n if data[i]=='Y' else n+1
            multiplier=n+1 if data[i]=='Y' else n
            if data[i+1]%divisor:continue
            data[i-1]+=data[i+1]//divisor*multiplier+data[i+3]
            del data[i:i+4]
            changed=True;break
        if not changed:return data


def normal_syllables(word):
    images={'x':((1,2),(0,1)),'X':((0,1),(1,1)),
            'y':((0,1),(1,2)),'Y':((1,1),(0,1))}
    out=[]
    for c in word:
        for factor,power_ in images[c]:
            if out and out[-1][0]==factor:power_+=out.pop()[1]
            power_%=(2,3)[factor]
            if power_:out.append((factor,power_))
    return out


def necklace(w):
    s=normal_syllables(w)
    while len(s)>1 and s[0][0]==s[-1][0]:
        factor,p=s.pop(0);p+=s.pop()[1];p%=(2,3)[factor]
        if p:s.append((factor,p))
    return min((tuple(s[k:]+s[:k]) for k in range(len(s))),default=())


def checks():
    b='xyxYXY';rA='XXXXYxxxy';rC='XXXyXYxxy';p='xxxYYYY'
    assert necklace(rA)==necklace(p)==necklace(rC)
    assert [sum(1 if c.islower() else -1 for c in w) for w in (p,rA,rC)]==[-1,-1,-1]
    bs=[]
    for n in range(2,51):
        assert len(hnn_reduced(b,n))==7
        assert len(hnn_reduced(b+b,n))==13
        for k in range(-20,21):
            primitive=power('x',k)+'y'
            assert len(hnn_reduced(primitive,n))==3
        bs.append(n)
    # Sharp exception: in BS(1,2), (XY) b (yx) reduces to x^2 Y.
    assert hnn_reduced(reduce('XY'+b+'yx'),1)==[2,'Y',0]
    for c in 'aAbB':
        assert alpha(alpha(c),-1)==c and alpha(alpha(c,-1))==c
    assert free_by_cyclic(rC)==('',0)
    assert free_by_cyclic('yXX')==('a',0)
    assert free_by_cyclic('xyXXX')==('b',0)
    W,e=free_by_cyclic(inverse(b))
    assert (W,e)==('abbAbA',1)
    candidate,e=free_by_cyclic('XXy')
    assert (candidate,e)==('aba',0)
    assert candidate==alpha('a',-2)==alpha(inverse('bA'),-4)
    for k in range(-12,13):
        assert power(candidate,k)==alpha(power('bA',-k),-4)
        assert free_by_cyclic(power('XXy',k)+'x')==(power(candidate,k),1)
    return {'BS_family_formula_checks':'n=2..50, candidate exponents -20..20',
            'BS_braid_cyclic_stable_length':3,'BS_primitive_candidate_stable_length':1,
            'BS_n1_exception':'(XY) b (yx) = x^2 Y',
            'classA_relator':rA,'classC_relator':rC,
            'both_relators_conjugate_to_original_power_in_B3':True,
            'classC_fiber_alpha':{'a':'b','b':'aB'},
            'classC_braid_inverse_normal_form':[W,1],
            'classC_primitive_kernel':candidate,
            'classC_transfer_identity':'aba = alpha^-4((bA)^-1)',
            'scope':'Analytic single-coordinate primitive exclusions; not a global AC obstruction'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args()
    result=checks()
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
