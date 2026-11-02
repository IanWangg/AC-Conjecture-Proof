"""Small finite Magnus-algebra filters for the unclassified power9 branches.

All groups are explicit generated subgroups of units in finite associative
algebras. A hit is inconclusive; a complete missed conjugacy orbit is an
unbounded necessary-condition obstruction, subject to the character proof.
"""
from collections import deque
from itertools import product
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path


def inverse_word(w): return w.swapcase()[::-1]


def nullspace(matrix, p):
    a=[list(row) for row in matrix]
    columns=len(a[0]); pivots=[]; row=0
    for col in range(columns):
        chosen=next((r for r in range(row,len(a)) if a[r][col]%p),None)
        if chosen is None:continue
        a[row],a[chosen]=a[chosen],a[row]
        scale=pow(a[row][col]%p,-1,p)
        a[row]=[(x*scale)%p for x in a[row]]
        for r in range(len(a)):
            if r!=row and a[r][col]%p:
                c=a[r][col]%p;a[r]=[(x-c*y)%p for x,y in zip(a[r],a[row])]
        pivots.append(col);row+=1
        if row==len(a):break
    out=[]
    for free in range(columns):
        if free in pivots:continue
        v=[0]*columns;v[free]=1
        for i,col in enumerate(pivots):v[col]=-a[i][free]%p
        out.append(tuple(v))
    return out


class Algebra:
    def __init__(self,letters,p=5,functional=None,degree=3):
        self.p=p;self.letters=letters;self.L=functional;self.degree=degree
        self.monomials=['']+[''.join(w) for length in range(1,degree) for w in product(letters,repeat=length)]
        self.monomials+=['#'] if functional is not None else [''.join(w) for w in product(letters,repeat=degree)]
        self.index={w:i for i,w in enumerate(self.monomials)};self.size=len(self.monomials)
        self.one=self.basis(0)
        self.table=[]
        for u in self.monomials:
            row=[]
            for v in self.monomials:
                if not u:row.append((self.index[v],1));continue
                if not v:row.append((self.index[u],1));continue
                if '#' in (u,v) or len(u)+len(v)>degree:row.append((0,0));continue
                w=u+v
                if len(w)==degree and functional is not None:row.append((self.index['#'],functional.get(w,0)%p))
                else:row.append((self.index[w],1))
            self.table.append(row)
        self.generators={c:self.add(self.one,self.basis(self.index[c])) for c in letters}
        self.generators.update({c.upper():self.inverse(v) for c,v in list(self.generators.items())})

    def basis(self,i):return tuple(int(j==i) for j in range(self.size))
    def add(self,a,b,sign=1):return tuple((u+sign*v)%self.p for u,v in zip(a,b))
    def mul(self,a,b):
        out=[0]*self.size
        for i,c in enumerate(a):
            if c:
                for j,d in enumerate(b):
                    if d:
                        target,coefficient=self.table[i][j]
                        if coefficient:out[target]+=c*d*coefficient
        return tuple(c%self.p for c in out)
    def inverse(self,a):
        v=self.add(a,self.one,-1);out=self.one;power=self.one
        for k in range(1,self.degree+1):power=self.mul(power,v);out=self.add(out,power,-1 if k%2 else 1)
        assert self.mul(a,out)==self.one
        return out
    def word(self,w):
        out=self.one
        for c in w:out=self.mul(out,self.generators[c])
        return out
    def operator(self,left,right):return [self.mul(self.mul(left,self.basis(i)),right) for i in range(self.size)]
    def substitution(self,images):
        output=[]
        for monomial in self.monomials:
            if monomial=='#':
                representative=next(w for w,c in self.L.items() if c%self.p)
                scale=pow(self.L[representative]%self.p,-1,self.p)
            else:representative=monomial;scale=1
            value=self.one
            for c in representative:value=self.mul(value,self.add(self.word(images[c]),self.one,-1))
            output.append(tuple(c*scale%self.p for c in value))
        return output
    def apply(self,columns,value):
        out=[0]*self.size
        for i,c in enumerate(value):
            if c:
                for j,d in enumerate(columns[i]):
                    if d:out[j]+=c*d
        return tuple(c%self.p for c in out)


MODELS={
 'D':dict(letters='ab',images={'a':'b','b':'AbAb'},W='baBabAbA',x=('a',2),y=('b',3),relator='XXXyxYXyy'),
 'E':dict(letters='abc',images={'a':'b','b':'c','c':'Bacc'},W='aBac',x=('a',2),y=('',1),relator='XXYxxYYxy'),
 'F':dict(letters='ab',images={'a':'b','b':'aB'},W='baBaBaBAbA',x=('b',0),y=('b',1),relator='XXyXYxYxy',candidate='b')}

SELECTED={
 'D':(17,4,{'abaa':15,'abab':6,'abba':6,'abbb':16,'baaa':2,'baab':11,'baba':11,'babb':1}),
 'E':(5,3,{'bac':3,'cbb':1,'acb':4,'cab':1,'bab':2,'bcc':3,'abc':2,'aba':4,'bcb':4,'abb':3,'cac':1,'acc':4,'cbc':2,'baa':1}),
 'F':(5,4,{'abaa':1,'abab':4,'abbb':4,'baaa':4,'baab':1,'babb':1})}


def functionals(model,p,degree=3):
    data=MODELS[model];algebra=Algebra(data['letters'],p,degree=degree)
    alpha=algebra.substitution(data['images'])
    top=[i for i,w in enumerate(algebra.monomials) if len(w)==degree]
    # A row functional L satisfies L alpha=L, hence (alpha^T-I)L=0.
    equations=[[alpha[i][j]-int(i==j) for j in top] for i in top]
    basis=nullspace(equations,p)
    return [{algebra.monomials[i]:c for i,c in zip(top,v) if c} for v in basis]


def affine_solution(matrix,rhs,p):
    """Return one solution, or None, for a possibly rectangular finite system."""
    a=[list(row)+[b%p] for row,b in zip(matrix,rhs)]
    columns=len(matrix[0]);pivots=[];row=0
    for col in range(columns):
        chosen=next((r for r in range(row,len(a)) if a[r][col]%p),None)
        if chosen is None:continue
        a[row],a[chosen]=a[chosen],a[row]
        scale=pow(a[row][col]%p,-1,p);a[row]=[(x*scale)%p for x in a[row]]
        for r in range(len(a)):
            if r!=row and a[r][col]%p:
                c=a[r][col]%p;a[r]=[(x-c*y)%p for x,y in zip(a[r],a[row])]
        pivots.append(col);row+=1
        if row==len(a):break
    if any(not any(r[:columns]) and r[-1]%p for r in a):return None
    x=[0]*columns
    for r,col in enumerate(pivots):x[col]=a[r][-1]%p
    assert all(sum(c*d for c,d in zip(r,x))%p==b%p for r,b in zip(matrix,rhs))
    return tuple(x)


def affine_obstruction(matrix,rhs,p):
    """A checkable dual witness lambda A=0, lambda rhs=1, or None."""
    rows=len(matrix);columns=len(matrix[0])
    a=[list(r)+[b%p] for r,b in zip(matrix,rhs)]
    weights=[[int(i==j) for j in range(rows)] for i in range(rows)]
    at=0
    for col in range(columns):
        chosen=next((r for r in range(at,rows) if a[r][col]%p),None)
        if chosen is None:continue
        a[at],a[chosen]=a[chosen],a[at];weights[at],weights[chosen]=weights[chosen],weights[at]
        scale=pow(a[at][col]%p,-1,p)
        a[at]=[c*scale%p for c in a[at]];weights[at]=[c*scale%p for c in weights[at]]
        for r in range(rows):
            if r!=at and a[r][col]%p:
                c=a[r][col]%p
                a[r]=[(u-c*v)%p for u,v in zip(a[r],a[at])]
                weights[r]=[(u-c*v)%p for u,v in zip(weights[r],weights[at])]
        at+=1
        if at==rows:break
    for r in range(rows):
        if not any(a[r][:columns]) and a[r][-1]%p:
            scale=pow(a[r][-1]%p,-1,p);w=tuple(c*scale%p for c in weights[r])
            assert all(sum(w[i]*matrix[i][j] for i in range(rows))%p==0 for j in range(columns))
            assert sum(w[i]*rhs[i] for i in range(rows))%p==1
            return w
    return None


def linear_filter(model,p,functional,degree):
    data=MODELS[model];a=Algebra(data['letters'],p,functional,degree)
    alpha=a.substitution(data['images']);W=a.word(data['W'])
    candidates=[];v=a.one
    while True:
        candidates.append(v);v=a.mul(v,a.generators[data.get('candidate','a')])
        if v==a.one:break
        assert len(candidates)<10000
    hits=[];solutions=[];obstructions=[]
    for k,target in enumerate(candidates):
        # qW=target*alpha(q), with q_0=1. Every such q is a unit.
        columns=[a.add(a.mul(a.basis(i),W),a.mul(target,alpha[i]),-1) for i in range(a.size)]
        equations=[[columns[i][j] for i in range(1,a.size)] for j in range(a.size)]
        rhs=[-columns[0][j] for j in range(a.size)]
        answer=affine_solution(equations,rhs,p)
        if answer is not None:
            q=(1,)+answer
            assert a.mul(q,W)==a.mul(target,a.apply(alpha,q))
            hits.append(k);solutions.append(q)
        else:
            witness=affine_obstruction(equations,rhs,p)
            assert witness is not None
            obstructions.append({'candidate_residue':k,'dual_vector':witness})
    return {'format':'s-unit-linear-obstruction-v1','model':model,'prime':p,'degree':degree,'functional':functional,
            'algebra_dimension':a.size,'candidate_order':len(candidates),
            'residues_with_unit_solution':hits,'unit_solutions':solutions,
            'linear_inconsistency_certificates':obstructions}


def experiment(model='D',p=5,functional=None,group_order=False,degree=3,orbit_output=None):
    data=MODELS[model];a=Algebra(data['letters'],p,functional,degree)
    alpha=a.substitution(data['images'])
    # Direct finite algebra checks validate any compressed top-degree quotient.
    for i,j,k in product(range(a.size),repeat=3):
        u,v,w=a.basis(i),a.basis(j),a.basis(k)
        assert a.mul(a.mul(u,v),w)==a.mul(u,a.mul(v,w))
    for i,j in product(range(a.size),repeat=2):
        assert a.apply(alpha,a.mul(a.basis(i),a.basis(j)))==a.mul(alpha[i],alpha[j])
    gens=data['letters']+data['letters'].upper()
    transforms=[a.operator(a.generators[c],a.inverse(a.apply(alpha,a.generators[c]))) for c in gens]
    start=a.word(data['W']);orbit={start};queue=deque([start])
    while queue:
        item=queue.popleft()
        for op in transforms:
            nxt=a.apply(op,item)
            if nxt not in orbit:orbit.add(nxt);queue.append(nxt)
    candidates=[];v=a.one
    while True:
        candidates.append(v);v=a.mul(v,a.generators[data.get('candidate','a')])
        if v==a.one:break
        assert len(candidates)<100
    hits=[k for k,v in enumerate(candidates) if v in orbit]
    current=[a.generators[c] for c in data['letters']];initial=tuple(current);order=0
    while True:
        current=[a.apply(alpha,v) for v in current];order+=1
        if tuple(current)==initial:break
        assert order<100000
    def alpha_power(v,k):
        for _ in range(k%order):v=a.apply(alpha,v)
        return v
    def semi_mul(u,v):return (a.mul(u[0],alpha_power(v[0],u[1])),(u[1]+v[1])%order)
    def semi_inv(u):return (alpha_power(a.inverse(u[0]),-u[1]),-u[1]%order)
    values={c:(a.word(data[c][0]),data[c][1]%order) for c in 'xy'}
    values.update({c.upper():semi_inv(v) for c,v in list(values.items())})
    def original(w):
        out=(a.one,0)
        for c in w:out=semi_mul(out,values[c])
        return out
    assert original(data['relator'])==(a.one,0)
    braid='xyxYXY' if model=='E' else 'yxyXYX'
    assert original(braid)==(start,1)
    count=None
    if group_order:
        ops=[a.operator(a.one,a.generators[c]) for c in gens]
        members={a.one};queue=deque([a.one])
        while queue:
            v=queue.popleft()
            for op in ops:
                nxt=a.apply(op,v)
                if nxt not in members:members.add(nxt);queue.append(nxt)
        assert all(a.apply(alpha,v) in members for v in members)
        count=len(members)
    encoded=sorted(bytes(v) for v in orbit)
    if orbit_output:
        certificate={'format':'s-finite-twisted-orbit-v1','model':model,'prime':p,'degree':degree,
                     'functional':functional,'alpha_order':order,'states':[list(v) for v in sorted(orbit)]}
        raw=json.dumps(certificate,separators=(',',':')).encode()
        Path(orbit_output).write_bytes(base64.b64encode(gzip.compress(raw,mtime=0))+b'\n')
    return dict(status='PASS',model=model,coefficient_prime=p,degree=degree,algebra_dimension=a.size,
                functional=functional,associativity_checks=a.size**3,
                automorphism_basis_product_checks=a.size**2,alpha_order=order,
                complete_twisted_orbit=True,orbit_states=len(orbit),candidate_order=len(candidates),
                candidate_residues_seen=hits,finite_fiber_group_order=count,
                original_relation_and_braid_images_checked=True,
                orbit_sha256=hashlib.sha256(b''.join(encoded)).hexdigest(),
                ordinary_AC_goal_solved=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--model',choices=MODELS,default='D')
    parser.add_argument('--prime',type=int,default=5);parser.add_argument('--functional',type=int)
    parser.add_argument('--degree',type=int,default=3);parser.add_argument('--functional-file')
    parser.add_argument('--selected',action='store_true');parser.add_argument('--linear',action='store_true')
    parser.add_argument('--orbit-certificate')
    parser.add_argument('--group-order',action='store_true');parser.add_argument('--output')
    args=parser.parse_args()
    fs=functionals(args.model,args.prime,args.degree) if args.functional is not None else None
    L=None if fs is None else fs[args.functional]
    if args.functional_file:
        L=json.loads(Path(args.functional_file).read_text())
        if 'functional' in L:L=L['functional']
    if args.selected:args.prime,args.degree,L=SELECTED[args.model]
    if args.linear:result=linear_filter(args.model,args.prime,L,args.degree)
    else:result=experiment(args.model,args.prime,L,args.group_order,args.degree,args.orbit_certificate)
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
