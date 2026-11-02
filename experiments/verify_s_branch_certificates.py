"""Independent literal-polynomial replay of S's three finite certificates.

No constructor, Gaussian solver, word-reduction routine, or algebra table
is imported from branch_finite_filters.py. The finite algebras are rebuilt
using monomial dictionaries. D is checked by dual linear witnesses; E/F
by closed twisted-orbit supersets containing the actual braid image.
"""
import argparse
import base64
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path


DATA={
 'D':dict(letters='ab',images={'a':'b','b':'AbAb'},W='baBabAbA',x=('a',2),y=('b',3),relator='XXXyxYXyy',braid='yxyXYX',candidate='a'),
 'E':dict(letters='abc',images={'a':'b','b':'c','c':'Bacc'},W='aBac',x=('a',2),y=('',1),relator='XXYxxYYxy',braid='xyxYXY',candidate='a'),
 'F':dict(letters='ab',images={'a':'b','b':'aB'},W='baBaBaBAbA',x=('b',0),y=('b',1),relator='XXyXYxYxy',braid='yxyXYX',candidate='b')}


class PolynomialAlgebra:
    def __init__(self,letters,p,degree,L):
        self.letters,self.p,self.degree,self.L=letters,p,degree,L
        assert p in (5,17)
        assert all(len(w)==degree and set(w)<=set(letters) and 0<c<p for w,c in L.items())
        self.basis=['']+[''.join(w) for length in range(1,degree) for w in product(letters,repeat=length)]+['#']
        self.one={'':1};self.size=len(self.basis)
        self.gens={c:{'':1,c:1} for c in letters}
        self.gens.update({c.upper():self.inverse(v) for c,v in list(self.gens.items())})

    def add(self,a,b,factor=1):
        out=dict(a)
        for w,c in b.items():
            value=(out.get(w,0)+factor*c)%self.p
            if value:out[w]=value
            else:out.pop(w,None)
        return out
    def scale(self,a,c):return {w:v*c%self.p for w,v in a.items() if v*c%self.p}
    def mul(self,a,b):
        out={}
        for u,c in a.items():
            for v,d in b.items():
                if not u:w,coefficient=v,1
                elif not v:w,coefficient=u,1
                elif '#' in (u,v) or len(u)+len(v)>self.degree:continue
                elif len(u)+len(v)==self.degree:w,coefficient='#',self.L.get(u+v,0)
                else:w,coefficient=u+v,1
                total=(out.get(w,0)+c*d*coefficient)%self.p
                if total:out[w]=total
                else:out.pop(w,None)
        return out
    def inverse(self,a):
        assert a.get('',0)==1
        n=self.add(a,self.one,-1);out=self.one;term=self.one
        for k in range(1,self.degree+1):
            term=self.mul(term,n);out=self.add(out,term,-1 if k%2 else 1)
        assert self.mul(a,out)==self.one and self.mul(out,a)==self.one
        return out
    def word(self,w):
        out=self.one
        for c in w:out=self.mul(out,self.gens[c])
        return out
    def vector(self,a):return tuple(a.get(w,0) for w in self.basis)
    def poly(self,v):
        assert len(v)==self.size and all(type(c)==int and 0<=c<self.p for c in v)
        return {w:c for w,c in zip(self.basis,v) if c}
    def make_alpha(self,images):
        columns={}
        representative=min(self.L)
        for w in self.basis:
            full=representative if w=='#' else w
            answer=self.one
            for c in full:answer=self.mul(answer,self.add(self.word(images[c]),self.one,-1))
            if w=='#':answer=self.scale(answer,pow(self.L[representative],-1,self.p))
            columns[w]=answer
        return columns
    def apply(self,columns,a):
        out={}
        for w,c in a.items():out=self.add(out,columns[w],c)
        return out


def verify_structure(a,model,claimed_order=None):
    data=DATA[model];alpha=a.make_alpha(data['images'])
    bases=[{w:1} for w in a.basis]
    for u,v,w in product(bases,repeat=3):
        assert a.mul(a.mul(u,v),w)==a.mul(u,a.mul(v,w))
    for u,v in product(bases,repeat=2):
        assert a.apply(alpha,a.mul(u,v))==a.mul(a.apply(alpha,u),a.apply(alpha,v))
    original=tuple(a.vector(a.gens[c]) for c in a.letters)
    current=[a.gens[c] for c in a.letters];order=0
    while True:
        order+=1;current=[a.apply(alpha,v) for v in current]
        if tuple(a.vector(v) for v in current)==original:break
        assert order<10000
    if claimed_order is not None:assert order==claimed_order
    for basis in bases:
        v=basis
        for _ in range(order):v=a.apply(alpha,v)
        assert v==basis
    def ap(value,k):
        for _ in range(k%order):value=a.apply(alpha,value)
        return value
    def mul(u,v):return a.mul(u[0],ap(v[0],u[1])),(u[1]+v[1])%order
    def inv(u):return ap(a.inverse(u[0]),-u[1]),(-u[1])%order
    values={c:(a.word(data[c][0]),data[c][1]%order) for c in 'xy'}
    values.update({c.upper():inv(v) for c,v in list(values.items())})
    def original_word(w):
        out=a.one,0
        for c in w:out=mul(out,values[c])
        return out
    assert original_word(data['relator'])==(a.one,0)
    assert original_word(data['braid'])==(a.word(data['W']),1)
    if model=='D':
        assert original_word('xxYxY')==(a.gens['a'],0)
        assert original_word('yX')==(a.one,1)
    elif model=='E':
        assert original_word('xYY')==(a.gens['a'],0)
        assert original_word('y')==(a.one,1)
    else:
        assert original_word('Yxy')==(a.gens['a'],0)
        assert original_word('x')==(a.gens['b'],0)
        assert original_word('Xy')==(a.one,1)
    return alpha,order


def candidate_powers(a,model):
    c=a.gens[DATA[model]['candidate']];out=[];v=a.one
    while True:
        out.append(v);v=a.mul(v,c)
        if v==a.one:return out
        assert len(out)<1000


def verify_linear(source):
    data=json.loads(Path(source).read_text());assert data['model']=='D'
    a=PolynomialAlgebra('ab',data['prime'],data['degree'],data['functional'])
    alpha,order=verify_structure(a,'D',16)
    candidates=candidate_powers(a,'D');assert len(candidates)==17
    assert data['residues_with_unit_solution']==[] and data['unit_solutions']==[]
    witnesses=data['linear_inconsistency_certificates']
    assert sorted(row['candidate_residue'] for row in witnesses)==list(range(17))
    W=a.word(DATA['D']['W'])
    for row in witnesses:
        k=row['candidate_residue'];dual=row['dual_vector'];assert len(dual)==a.size
        assert all(type(c)==int and 0<=c<a.p for c in dual)
        columns=[]
        for w in a.basis:
            left=a.mul({w:1},W);right=a.mul(candidates[k],alpha[w])
            columns.append(a.vector(a.add(left,right,-1)))
        for column in columns[1:]:assert sum(c*d for c,d in zip(dual,column))%a.p==0
        assert sum(c*d for c,d in zip(dual,columns[0]))%a.p==a.p-1
    return dict(status='PASS',model='D',algebra_dimension=a.size,prime=a.p,
                alpha_order=order,associativity_basis_checks=a.size**3,
                original_relator_and_braid_images_checked=True,
                all_candidate_residues_excluded=17,dual_linear_witnesses_verified=17,
                no_Gaussian_solver_imported=True,ambient_unit_group_order=a.p**(a.size-1),
                finite_semidirect_target_order=a.p**(a.size-1)*order,
                ordinary_AC_goal_solved=False)


def verify_orbit(source):
    raw=gzip.decompress(base64.b64decode(Path(source).read_bytes()))
    data=json.loads(raw);assert data['format']=='s-finite-twisted-orbit-v1'
    model=data['model'];assert model in ('E','F')
    a=PolynomialAlgebra(DATA[model]['letters'],data['prime'],data['degree'],data['functional'])
    alpha,order=verify_structure(a,model,data['alpha_order'])
    states={tuple(v) for v in data['states']};assert len(states)==len(data['states'])
    for v in states:assert a.poly(v).get('',0)==1
    assert a.vector(a.word(DATA[model]['W'])) in states
    candidates=candidate_powers(a,model)
    assert all(a.vector(v) not in states for v in candidates)
    # Independently construct each linear transformation by literal products.
    operators=[]
    for c in DATA[model]['letters']+DATA[model]['letters'].upper():
        left=a.gens[c];right=a.inverse(a.apply(alpha,left))
        columns=[a.vector(a.mul(a.mul(left,{w:1}),right)) for w in a.basis]
        operators.append(columns)
    count=0
    for state in states:
        for columns in operators:
            out=[0]*a.size
            for i,c in enumerate(state):
                if c:
                    for j,d in enumerate(columns[i]):
                        if d:out[j]+=c*d
            out=tuple(c%a.p for c in out)
            assert out in states
            count+=1
    return dict(status='PASS',model=model,algebra_dimension=a.size,prime=a.p,
                alpha_order=order,associativity_basis_checks=a.size**3,
                original_relator_and_braid_images_checked=True,
                closed_orbit_superset_states=len(states),closure_edges_checked=count,
                all_candidate_residues_excluded=len(candidates),
                independent_literal_monomial_arithmetic=True,
                orbit_sha256=hashlib.sha256(b''.join(sorted(bytes(v) for v in states))).hexdigest(),
                ordinary_AC_goal_solved=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('certificate');parser.add_argument('--output',required=True)
    args=parser.parse_args()
    result=verify_orbit(args.certificate) if args.certificate.endswith('.gz.b64') else verify_linear(args.certificate)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
