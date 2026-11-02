"""Odd-characteristic central-lift filter for the rank3 deletion quotient.

alpha(a)=b, alpha(b)=c, alpha(c)=aB; W=bCB, candidates a^k.
Enumerates the full degree2 fiber image and overapproximates its central
degree3 lift by the full tensor space. A rejected parameter is impossible;
a surviving one is inconclusive.
"""
from collections import deque
from itertools import product
import argparse
import json
from pathlib import Path


class Algebra:
    def __init__(self,degree,prime):
        self.degree,self.p=degree,prime
        self.monomials=[()]
        for length in range(1,degree+1):self.monomials.extend(product(range(3),repeat=length))
        self.indices={w:i for i,w in enumerate(self.monomials)}
        self.size=len(self.monomials)
        self.one=(1,)+(0,)*(self.size-1)
        self.table=[[self.indices[a+b] if len(a)+len(b)<=degree else -1 for b in self.monomials] for a in self.monomials]
        self.letters={}
        for i,c in enumerate('abc'):
            v=list(self.one);v[self.indices[(i,)]]=1;self.letters[c]=tuple(v)
        self.letters.update({c.upper():self.inverse(v) for c,v in list(self.letters.items())})

    def add(self,a,b,sign=1):return tuple((u+sign*v)%self.p for u,v in zip(a,b))
    def multiply(self,a,b):
        out=[0]*self.size
        for i,u in enumerate(a):
            if not u:continue
            for j,v in enumerate(b):
                if not v:continue
                k=self.table[i][j]
                if k>=0:out[k]+=u*v
        return tuple(v%self.p for v in out)
    def inverse(self,a):
        out,power=self.one,self.one;v=self.add(a,self.one,-1)
        for n in range(1,self.degree+1):
            power=self.multiply(power,v);out=self.add(out,power,-1 if n%2 else 1)
        assert self.multiply(a,out)==self.one
        return out
    def evaluate(self,word):
        out=self.one
        for c in word:out=self.multiply(out,self.letters[c])
        return out
    def columns(self,left,right):
        cols=[]
        for i in range(self.size):
            e=[0]*self.size;e[i]=1
            image=self.multiply(self.multiply(left,e),right)
            cols.append([(j,c) for j,c in enumerate(image) if c])
        return cols
    def apply(self,cols,value):
        out=[0]*self.size
        for i,c in enumerate(value):
            if c:
                for j,d in cols[i]:out[j]+=c*d
        return tuple(c%self.p for c in out)


def experiment(prime,budget=200000):
    low,high=Algebra(2,prime),Algebra(3,prime)
    images=dict(zip('abcABC',('b','c','aB','B','C','bA')))
    inverse=dict(zip('abcABC',('ca','a','b','AC','A','B')))
    for c in 'abcABC':
        for first,second in ((images,inverse),(inverse,images)):
            assert high.evaluate(''.join(second[d] for d in first[c]))==high.letters[c]
    substitution=[]
    for w in high.monomials:
        value=high.one
        for i in w:value=high.multiply(value,high.add(high.evaluate(images['abc'[i]]),high.one,-1))
        substitution.append(value)
    basis={}
    for i in range(low.size,high.size):
        e=[0]*high.size;e[i]=1
        vector=list(high.add(e,substitution[i],-1))
        assert not any(vector[:low.size])
        while any(vector):
            pivot=max(j for j,c in enumerate(vector) if c)
            if pivot not in basis:
                scale=pow(vector[pivot],-1,prime);basis[pivot]=tuple(c*scale%prime for c in vector);break
            scale=vector[pivot];vector=[(c-scale*d)%prime for c,d in zip(vector,basis[pivot])]
    def residual(vector):
        vector=list(vector)
        while any(vector):
            pivot=max(j for j,c in enumerate(vector) if c)
            if pivot not in basis:return tuple(vector)
            scale=vector[pivot];vector=[(c-scale*d)%prime for c,d in zip(vector,basis[pivot])]
        return tuple(vector)
    left=[low.columns(low.letters[c],low.one) for c in 'abcABC']
    twist=[high.columns(high.letters[c],high.inverse(high.evaluate(images[c]))) for c in 'abcABC']
    powers=[];value=high.one
    while True:
        powers.append(value);value=high.multiply(value,high.letters['a'])
        if value==high.one:break
        assert len(powers)<=prime**2
    seen={low.one:high.evaluate('bCB')};queue=deque([low.one]);processed=0;checks=[]
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
    return {'coefficient_field':prime,'fiber_rank':3,'low_degree':2,'high_degree':3,
            'complete_fiber_enumeration':not queue,'fiber_degree2_states':len(seen),'states_processed':processed,
            'full_tensor_central_dimension':high.size-low.size,'image_I_minus_alpha_rank':len(basis),
            'candidate_order_high':len(powers),'matching_lower_conjugators':checks,
            'candidate_residues_not_excluded':sorted(set(c['k'] for c in checks if c['linear_lift_possible'])),
            'scope':'Full central tensor overapproximation: rejection rigorous, acceptance inconclusive'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prime',type=int,default=5);p.add_argument('--budget',type=int,default=200000);p.add_argument('--output');args=p.parse_args()
    result=experiment(args.prime,args.budget)
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
