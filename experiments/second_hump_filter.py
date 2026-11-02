"""Primitive replacement filter at the new fixed relator YxYXyyx.

Fiber a=x,b=yxY,stablet=y; alpha(a)=b,alpha(b)=aB.
The inverse length8 braid replacement has coefficient W=BAbb beforet.
"""
from collections import deque
import argparse
import hashlib
import json
from pathlib import Path
from twisted_magnus import Magnus2


def experiment(degree=5):
    ring=Magnus2(degree)
    images={'a':'b','b':'aB','A':'B','B':'bA'}
    substitution=[]
    for i in range(ring.size):
        image=1
        for shift in reversed(range(ring.length[i])):
            c='ab'[(ring.value[i]>>shift)&1]
            image=ring.product(image,ring.evaluate(images[c])^1)
        substitution.append(image)
    aa,bb,alpha_order=ring.a,ring.b,0
    while True:
        aa,bb=ring.apply(substitution,aa),ring.apply(substitution,bb);alpha_order+=1
        if (aa,bb)==(ring.a,ring.b):break
        assert alpha_order<100000
    def alpha(v,n):
        for _ in range(n%alpha_order):v=ring.apply(substitution,v)
        return v
    def multiply(u,v):return (ring.product(u[0],alpha(v[0],u[1])),(u[1]+v[1])%alpha_order)
    def inverse(u):return (alpha(ring.inverse(u[0]),-u[1]),(-u[1])%alpha_order)
    x,y=(ring.a,0),(1,1)
    letters={'x':x,'y':y,'X':inverse(x),'Y':inverse(y)}
    def original(word):
        value=(1,0)
        for c in word:value=multiply(value,letters[c])
        return value
    assert original('YxYXyyx')==(1,0)
    assert original('yXXyXYxx')==(ring.evaluate('BAbb'),1)
    transformations=[]
    for c in 'abAB':transformations.append(ring.columns(ring.letters[c],ring.inverse(ring.evaluate(images[c]))))
    start=ring.evaluate('BAbb');seen={start};queue=deque([start])
    while queue:
        value=queue.popleft()
        for transform in transformations:
            nxt=ring.apply(transform,value)
            if nxt not in seen:seen.add(nxt);queue.append(nxt)
    candidates=[];value=1
    while True:
        candidates.append(value);value=ring.product(value,ring.a)
        if value==1:break
        assert len(candidates)<100
    width=(ring.size+7)//8
    return {'degree':degree,'coefficient_field':2,'fixed_relator':'YxYXyyx',
            'target_original_word':'yXXyXYxx','target_fiber_word':'BAbb',
            'primitive_candidate':'a^k*t','complete_twisted_orbit':True,
            'orbit_states':len(seen),'candidate_order':len(candidates),
            'candidate_k_residues_seen':[k for k,v in enumerate(candidates) if v in seen],
            'alpha_order':alpha_order,
            'orbit_sha256':hashlib.sha256(b''.join(v.to_bytes(width,'little') for v in sorted(seen))).hexdigest(),
            'original_relation_and_target_checked':True,'free_group_AC_goal_solved':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--degree',type=int,default=5);p.add_argument('--output');args=p.parse_args();result=experiment(args.degree)
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
