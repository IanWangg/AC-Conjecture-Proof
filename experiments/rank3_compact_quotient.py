"""Direct small finite quotient for the rank3 primitive-replacement test.

The14-dimensional algebra is the degree3 truncation overF5 modulo the
kernel of one alpha-invariant cubic functional. All basis products and
the induced automorphism are explicitly checked, including associativity.
"""
from collections import deque
from itertools import product
import argparse
import hashlib
import json
from pathlib import Path

P=5
L={'aba':4,'abb':4,'abc':1,'aca':1,'acb':4,'baa':1,'bab':1,
   'bac':4,'bcb':4,'bcc':4,'caa':4,'cab':1,'cbb':1,'cbc':1}
MONOMIALS=['']+list('abc')+[''.join(w) for w in product('abc',repeat=2)]+['#']
INDEX={w:i for i,w in enumerate(MONOMIALS)}
SIZE=len(MONOMIALS)
ONE=(1,)+(0,)*(SIZE-1)


def basis(i,coefficient=1):
    v=[0]*SIZE;v[i]=coefficient%P;return tuple(v)


def basis_product(u,v):
    if u=='':return (INDEX[v],1)
    if v=='':return (INDEX[u],1)
    if '#' in (u,v):return (0,0)
    w=u+v
    if len(w)<=2:return (INDEX[w],1)
    if len(w)==3:return (INDEX['#'],L.get(w,0))
    return (0,0)


TABLE=[[basis_product(u,v) for v in MONOMIALS] for u in MONOMIALS]


def add(a,b,sign=1):return tuple((u+sign*v)%P for u,v in zip(a,b))
def multiply(a,b):
    out=[0]*SIZE
    for i,u in enumerate(a):
        if u:
            for j,v in enumerate(b):
                if v:
                    target,c=TABLE[i][j]
                    out[target]+=u*v*c
    return tuple(c%P for c in out)
def inverse(a):
    out,power,v=ONE,ONE,add(a,ONE,-1)
    for k in range(1,4):power=multiply(power,v);out=add(out,power,-1 if k%2 else 1)
    assert multiply(a,out)==ONE
    return out
LETTERS={c:add(ONE,basis(INDEX[c])) for c in 'abc'}
LETTERS.update({c.upper():inverse(v) for c,v in list(LETTERS.items())})


def word(w):
    out=ONE
    for c in w:out=multiply(out,LETTERS[c])
    return out


def substitution(images):
    cols=[]
    for monomial in MONOMIALS:
        # '#' is represented by abc, since L(abc)=1.
        out=ONE
        for c in ('abc' if monomial=='#' else monomial):out=multiply(out,add(word(images[c]),ONE,-1))
        cols.append(out)
    return cols


def apply(cols,value):
    out=[0]*SIZE
    for i,c in enumerate(value):
        if c:
            for j,d in enumerate(cols[i]):
                if d:out[j]+=c*d
    return tuple(c%P for c in out)


def operator_columns(left,right):return [multiply(multiply(left,basis(i)),right) for i in range(SIZE)]


def experiment():
    # These controls do not assume that L was derived correctly.
    for i,j,k in product(range(SIZE),repeat=3):
        a,b,c=basis(i),basis(j),basis(k)
        assert multiply(multiply(a,b),c)==multiply(a,multiply(b,c))
    alpha=substitution({'a':'b','b':'c','c':'aB'})
    back=substitution({'a':'ca','b':'a','c':'b'})
    for i in range(SIZE):
        assert apply(alpha,apply(back,basis(i)))==basis(i)
        assert apply(back,apply(alpha,basis(i)))==basis(i)
        for j in range(SIZE):
            assert apply(alpha,multiply(basis(i),basis(j)))==multiply(alpha[i],alpha[j])
    aa,bb,cc=(LETTERS[c] for c in 'abc');alpha_order=0
    while True:
        aa,bb,cc=apply(alpha,aa),apply(alpha,bb),apply(alpha,cc);alpha_order+=1
        if (aa,bb,cc)==tuple(LETTERS[c] for c in 'abc'):break
        assert alpha_order<10000
    right=[operator_columns(ONE,LETTERS[c]) for c in 'abcABC']
    members={ONE};queue=deque([ONE])
    while queue:
        element=queue.popleft()
        for transform in right:
            nxt=apply(transform,element)
            if nxt not in members:members.add(nxt);queue.append(nxt)
    transforms=[]
    images=dict(zip('abcABC',('b','c','aB','B','C','bA')))
    for c in 'abcABC':transforms.append(operator_columns(LETTERS[c],inverse(word(images[c]))))
    start=word('bCB');orbit={start};queue=deque([start])
    while queue:
        element=queue.popleft()
        for transform in transforms:
            nxt=apply(transform,element)
            if nxt not in orbit:orbit.add(nxt);queue.append(nxt)
    candidates=[];v=ONE
    while True:
        candidates.append(v);v=multiply(v,LETTERS['a'])
        if v==ONE:break
        assert len(candidates)<100
    hits=[k for k,v in enumerate(candidates) if v in orbit]
    def alpha_power(value,n):
        for _ in range(n%alpha_order):value=apply(alpha,value)
        return value
    def semiproduct(u,v):return (multiply(u[0],alpha_power(v[0],u[1])),(u[1]+v[1])%alpha_order)
    def semi_inverse(u):return (alpha_power(inverse(u[0]),-u[1]),(-u[1])%alpha_order)
    x,y=(ONE,1),(LETTERS['a'],0)
    original={'x':x,'y':y,'X':semi_inverse(x),'Y':semi_inverse(y)}
    def original_word(w):
        ans=(ONE,0)
        for c in w:ans=semiproduct(ans,original[c])
        return ans
    assert original_word('XXXyxYxxY')==(ONE,0)
    assert original_word('xyxYXY')==(start,1)
    def encode(v):return sum(c*P**i for i,c in enumerate(v))
    digest=hashlib.sha256(b''.join(v.to_bytes(8,'little') for v in sorted(map(encode,orbit)))).hexdigest()
    return {'status':'PASS','coefficient_field':P,'algebra_dimension':SIZE,
            'associativity_basis_triples_checked':SIZE**3,'alpha_basis_product_checks':SIZE**2,
            'finite_fiber_group_order':len(members),'alpha_order':alpha_order,
            'finite_semidirect_group_order':len(members)*alpha_order,
            'complete_twisted_orbit':True,'twisted_orbit_states':len(orbit),
            'candidate_order':len(candidates),'candidate_k_residues_seen':hits,
            'orbit_sha256':digest,'original_relation_and_braid_images_checked':True,
            'free_group_AC_goal_solved':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output');args=p.parse_args();result=experiment()
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
