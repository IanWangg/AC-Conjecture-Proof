"""Odd-characteristic degree4 lift filter for W=BAbb versus a^k.

Uses full degree3 fiber enumeration and allows ALL homogeneous degree4
unit corrections, hence rejections are necessary and survivors inconclusive.
"""
from collections import deque
from itertools import product
import argparse
import json
from pathlib import Path
from twisted_magnus_odd import Algebra


class Algebra2(Algebra):
    def __init__(self,degree,prime):
        self.degree,self.p=degree,prime
        self.monomials=[()]
        for length in range(1,degree+1):self.monomials.extend(product(range(2),repeat=length))
        self.indices={w:i for i,w in enumerate(self.monomials)};self.size=len(self.monomials)
        self.one=(1,)+(0,)*(self.size-1)
        self.table=[[self.indices[a+b] if len(a)+len(b)<=degree else -1 for b in self.monomials] for a in self.monomials]
        self.letters={}
        for i,c in enumerate('ab'):
            v=list(self.one);v[self.indices[(i,)]]=1;self.letters[c]=tuple(v)
        self.letters.update({c.upper():self.inverse(v) for c,v in list(self.letters.items())})


def experiment(prime,budget=100000):
    low,high=Algebra2(3,prime),Algebra2(4,prime)
    images=dict(zip('abAB',('b','aB','B','bA')))
    back=dict(zip('abAB',('ba','a','AB','A')))
    for c in 'abAB':
        for first,second in ((images,back),(back,images)):
            assert high.evaluate(''.join(second[d] for d in first[c]))==high.letters[c]
    basis={}
    for i in range(low.size,high.size):
        image=high.one
        for j in high.monomials[i]:image=high.multiply(image,high.add(high.evaluate(images['ab'[j]]),high.one,-1))
        e=[0]*high.size;e[i]=1;vector=list(high.add(e,image,-1))
        while any(vector):
            pivot=max(j for j,c in enumerate(vector) if c)
            if pivot not in basis:
                factor=pow(vector[pivot],-1,prime);basis[pivot]=tuple(c*factor%prime for c in vector);break
            factor=vector[pivot];vector=[(c-factor*d)%prime for c,d in zip(vector,basis[pivot])]
    def residual(vector):
        vector=list(vector)
        for pivot in sorted(basis,reverse=True):
            factor=vector[pivot]
            if factor:vector=[(c-factor*d)%prime for c,d in zip(vector,basis[pivot])]
        return tuple(vector)
    left=[low.columns(low.letters[c],low.one) for c in 'abAB']
    twist=[high.columns(high.letters[c],high.inverse(high.evaluate(images[c]))) for c in 'abAB']
    powers=[];value=high.one
    while True:
        powers.append(value);value=high.multiply(value,high.letters['a'])
        if value==high.one:break
        assert len(powers)<=prime**2
    seen={low.one:high.evaluate('BAbb')};queue=deque([low.one]);processed=0;checks=[]
    while queue:
        q=queue.popleft();value=seen[q];processed+=1
        for k,target in enumerate(powers):
            if value[:low.size]==target[:low.size]:
                defect=high.add(value,target,-1);rem=residual(defect)
                checks.append({'k':k,'linear_lift_possible':not any(rem),
                               'remainder':[(high.monomials[j],c) for j,c in enumerate(rem) if c]})
        for l,t in zip(left,twist):
            qnext=low.apply(l,q);tnext=high.apply(t,value)
            if qnext not in seen:seen[qnext]=tnext;queue.append(qnext)
            else:assert seen[qnext][:low.size]==tnext[:low.size]
        if len(seen)>budget:break
    return {'coefficient_field':prime,'fiber_rank':2,'low_degree':3,'high_degree':4,
            'complete_fiber_enumeration':not queue,'fiber_degree3_states':len(seen),'states_processed':processed,
            'full_tensor_central_dimension':high.size-low.size,'image_I_minus_alpha_rank':len(basis),
            'candidate_order_high':len(powers),'matching_lower_conjugators':checks,
            'candidate_residues_not_excluded':sorted(set(c['k'] for c in checks if c['linear_lift_possible'])),
            'scope':'Full central tensor overapproximation: rejection rigorous, acceptance inconclusive'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prime',type=int,default=5);p.add_argument('--budget',type=int,default=100000);p.add_argument('--output');args=p.parse_args();result=experiment(args.prime,args.budget)
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
