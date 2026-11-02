"""Separate follow-up: alpha(a)=b, alpha(b)=c, alpha(c)=aB.

Tests W=bCB against all a^k in a finite characteristic mod2 Magnus image.
This is a different deletion quotient from the core Research K result.
"""
from collections import deque
from itertools import product
import argparse
import hashlib
import json
from pathlib import Path


class Algebra:
    def __init__(self,degree):
        self.degree=degree
        self.monomials=[()]
        for length in range(1,degree+1):
            self.monomials.extend(product(range(3),repeat=length))
        self.indices={w:i for i,w in enumerate(self.monomials)}
        self.size=len(self.monomials)
        self.table=[[self.indices[a+b] if len(a)+len(b)<=degree else -1 for b in self.monomials] for a in self.monomials]
        self.letters={c:1|(1<<self.indices[(i,)]) for i,c in enumerate('abc')}
        self.letters.update({c.upper():self.inverse(v) for c,v in list(self.letters.items())})

    def multiply(self,a,b):
        ans=0
        while a:
            bit=a&-a;i=bit.bit_length()-1;a^=bit
            rest=b
            while rest:
                bit=rest&-rest;j=bit.bit_length()-1;rest^=bit
                target=self.table[i][j]
                if target>=0:ans^=1<<target
        return ans

    def inverse(self,a):
        ans,power,v=1,1,a^1
        for _ in range(self.degree):
            power=self.multiply(power,v);ans^=power
        assert self.multiply(a,ans)==1
        return ans

    def evaluate(self,word):
        ans=1
        for c in word:ans=self.multiply(ans,self.letters[c])
        return ans

    @staticmethod
    def apply(columns,value):
        ans=0
        while value:
            bit=value&-value;value^=bit;ans^=columns[bit.bit_length()-1]
        return ans


def experiment(degree,budget=1000000):
    r=Algebra(degree)
    images=dict(zip('abcABC',('b','c','aB','B','C','bA')))
    back=dict(zip('abcABC',('ca','a','b','AC','A','B')))
    for c in 'abcABC':
        for first,second in ((images,back),(back,images)):
            assert r.evaluate(''.join(second[d] for d in first[c]))==r.letters[c]
    substitution=[]
    for monomial in r.monomials:
        value=1
        for i in monomial:value=r.multiply(value,r.evaluate(images['abc'[i]])^1)
        substitution.append(value)
    alpha_order=0
    current=tuple(r.letters[c] for c in 'abc')
    while True:
        current=tuple(r.apply(substitution,v) for v in current);alpha_order+=1
        if current==tuple(r.letters[c] for c in 'abc'):break
        assert alpha_order<100000
    columns=[]
    for c in 'abcABC':
        left,right=r.letters[c],r.inverse(r.evaluate(images[c]))
        columns.append([r.multiply(r.multiply(left,1<<i),right) for i in range(r.size)])
    start=r.evaluate('bCB')
    seen={start};queue=deque([start]);processed=0
    while queue:
        value=queue.popleft();processed+=1
        for col in columns:
            nxt=r.apply(col,value)
            if nxt not in seen:seen.add(nxt);queue.append(nxt)
        if len(seen)>budget:break
    candidate=r.letters['a'];powers=[];value=1
    while True:
        powers.append(value);value=r.multiply(value,candidate)
        if value==1:break
        assert len(powers)<=2**degree
    width=(r.size+7)//8
    return {'degree':degree,'coefficient_field':2,'fiber_rank':3,
            'vector_size':r.size,'alpha_order_on_fiber_image':alpha_order,
            'complete_twisted_orbit':not queue,'orbit_states':len(seen),
            'states_processed':processed,'candidate_order':len(powers),
            'candidate_k_residues_seen':[k for k,p in enumerate(powers) if p in seen],
            'orbit_sha256':hashlib.sha256(b''.join(v.to_bytes(width,'little') for v in sorted(seen))).hexdigest(),
            'scope':'One rank3 deletion-quotient primitive test; no global AC conclusion'}


def central_lift(budget=1000000):
    low,high=Algebra(3),Algebra(4)
    images=dict(zip('abcABC',('b','c','aB','B','C','bA')))
    lowmask=(1<<low.size)-1
    substitution=[]
    for monomial in high.monomials:
        value=1
        for i in monomial:value=high.multiply(value,high.evaluate(images['abc'[i]])^1)
        substitution.append(value)
    # Image of I-alpha on the entire homogeneous tensor degree4 space.
    # This deliberately allows more kernel corrections than the actual
    # free-group image. Rejection therefore remains a necessary obstruction.
    basis={}
    for i in range(low.size,high.size):
        vector=(1<<i)^substitution[i]
        assert not(vector&lowmask)
        while vector:
            pivot=vector.bit_length()-1
            if pivot in basis:vector^=basis[pivot]
            else:basis[pivot]=vector;break
    def residual(vector):
        while vector:
            pivot=vector.bit_length()-1
            if pivot not in basis:return vector
            vector^=basis[pivot]
        return 0
    left_columns=[]
    twist_columns=[]
    for c in 'abcABC':
        left_columns.append([low.multiply(low.letters[c],1<<i) for i in range(low.size)])
        left,right=high.letters[c],high.inverse(high.evaluate(images[c]))
        twist_columns.append([high.multiply(high.multiply(left,1<<i),right) for i in range(high.size)])
    powers=[];value=1
    while True:
        powers.append(value);value=high.multiply(value,high.letters['a'])
        if value==1:break
        assert len(powers)<100
    seen={1:high.evaluate('bCB')}
    queue=deque([1]);processed=0;checks=[]
    while queue:
        q=queue.popleft();value=seen[q];processed+=1
        for k,target in enumerate(powers):
            if (value&lowmask)==(target&lowmask):
                defect=value^target
                remainder=residual(defect)
                checks.append({'k':k,'q_degree3_hex':hex(q),'defect_hex':hex(defect),
                               'remainder_hex':hex(remainder),'linear_lift_possible':not remainder})
        for left,twist in zip(left_columns,twist_columns):
            qnext=low.apply(left,q)
            tnext=high.apply(twist,value)
            if qnext not in seen:seen[qnext]=tnext;queue.append(qnext)
            else:assert(seen[qnext]&lowmask)==(tnext&lowmask)
        if len(seen)>budget:break
    return {'coefficient_field':2,'fiber_rank':3,'low_degree':3,'high_degree':4,
            'complete_fiber_enumeration':not queue,'fiber_degree3_states':len(seen),
            'states_processed':processed,'full_tensor_central_dimension':high.size-low.size,
            'image_I_minus_alpha_rank':len(basis),'candidate_order_high':len(powers),
            'matching_lower_conjugators':checks,
            'candidate_residues_not_excluded':sorted(set(c['k'] for c in checks if c['linear_lift_possible'])),
            'scope':'Overapproximate all central degree4 corrections; rejection is rigorous, acceptance is inconclusive'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--degree',type=int,default=3);p.add_argument('--budget',type=int,default=1000000);p.add_argument('--output');p.add_argument('--central-lift',action='store_true');args=p.parse_args()
    result=central_lift(args.budget) if args.central_lift else experiment(args.degree,args.budget)
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
