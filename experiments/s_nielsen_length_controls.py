"""Independent finite controls for rank-two cyclic-basis sublevels.

Symbolic edge counts are checked against freely cyclically reduced graph
paths. Integer matrix tests and weighted-core tests are controls, not
substitutes for the all-matrix mathematical descent proof.
"""
from collections import deque
from functools import lru_cache
from itertools import product
import argparse
import json
from math import gcd
from pathlib import Path


def inverse(w):return w.swapcase()[::-1]


def cyclic_reduce(w):
    stack=[]
    for c in w:
        if stack and stack[-1]==c.swapcase():stack.pop()
        else:stack.append(c)
    first,last=0,len(stack)
    while last-first>1 and stack[first]==stack[last-1].swapcase():first+=1;last-=1
    return ''.join(stack[first:last])


@lru_cache(None)
def euclid(a,b):
    assert a>=0 and b>=0 and gcd(a,b)==1
    if not a:return 'b'
    if not b:return 'a'
    if a==b:return 'ab'
    if a>b:return euclid(a-b,b).replace('b','ab')
    return euclid(a,b-a).replace('a','ab')


def lengths(a,b,shape):
    if shape=='rose':return abs(a),0,abs(b)
    if shape=='theta':return abs(a+b),abs(a),abs(b)
    assert shape=='barbell'
    return abs(a),2*min(abs(a),abs(b)),abs(b)


RAYS=((0,-1),(1,-1),(1,0),(1,1),(0,1))
CONES=tuple(zip(RAYS,RAYS[1:]))


def coordinates(v,first,second):
    det=first[0]*second[1]-first[1]*second[0]
    assert abs(det)==1
    return ((v[0]*second[1]-v[1]*second[0])//det,
            (first[0]*v[1]-first[1]*v[0])//det)


def matrix_control(u,v):
    # Search signs independently, rather than reuse the draft's slope casework.
    selected=None
    for su,sv in product((-1,1),repeat=2):
        a=tuple(su*c for c in u);b=tuple(sv*c for c in v)
        for first,second in CONES:
            ca,cb=coordinates(a,first,second),coordinates(b,first,second)
            if min(*ca,*cb)>=0:selected=a,b,ca,cb;break
        if selected:break
    if selected is None:
        assert {tuple(map(abs,u)),tuple(map(abs,v))}=={(1,0),(0,1)}
        return 'axis_exception'
    a,b,ca,cb=selected
    if set((ca,cb))=={(1,0),(0,1)}:return 'boundary_pair'
    if ca[0]>=cb[0] and ca[1]>=cb[1]:large,small=a,b
    else:
        assert cb[0]>=ca[0] and cb[1]>=ca[1]
        large,small=b,a
    difference=tuple(x-y for x,y in zip(large,small))
    assert difference!=(0,0)
    assert abs(difference[0]*small[1]-difference[1]*small[0])==1
    for shape in ('rose','theta','barbell'):
        ll=lengths(*large,shape);ls=lengths(*small,shape);ld=lengths(*difference,shape)
        assert ll==tuple(x+y for x,y in zip(ls,ld))
        assert any(ls)
    return 'strict_symbolic_descent'


def run(vector_bound=20,matrix_bound=12,weight_bound=8):
    graph_bases={'rose':('p','r'),'theta':('pQ','pR'),'barbell':('p','qrQ')}
    vector_count=0;word_checks=0
    for a,b in product(range(-vector_bound,vector_bound+1),repeat=2):
        if gcd(a,b)!=1:continue
        word=euclid(abs(a),abs(b))
        if a<0:word=word.replace('a','A')
        if b<0:word=word.replace('b','B')
        for shape,(left,right) in graph_bases.items():
            table=dict(a=left,b=right,A=inverse(left),B=inverse(right))
            path=cyclic_reduce(''.join(table[c] for c in word))
            actual=tuple(sum(c.lower()==letter for c in path) for letter in 'pqr')
            assert actual==lengths(a,b,shape)
            word_checks+=1
        vector_count+=1
    counts={}
    vals=range(-matrix_bound,matrix_bound+1)
    for a,b,c,d in product(vals,repeat=4):
        if abs(a*d-b*c)!=1:continue
        result=matrix_control((a,b),(c,d));counts[result]=counts.get(result,0)+1
    core_vectors=(((1,0),(0,1)),((0,1),(1,-1)),((1,-1),(1,0)),
                  ((1,0),(1,1)),((1,1),(0,1)))
    adjacent=({1,2,3,4},{0,2},{0,1},{0,4},{0,3})
    sublevels=0
    for shape in ('rose','theta','barbell'):
        for weights in product(range(1,weight_bound+1),repeat=3):
            energies=[]
            for u,v in core_vectors:
                counts2=tuple(x+y for x,y in zip(lengths(*u,shape),lengths(*v,shape)))
                energies.append(sum(c*w for c,w in zip(counts2,weights)))
            for cap in set(energies):
                allowed={i for i,e in enumerate(energies) if e<=cap}
                reached={min(allowed)};queue=deque(reached)
                while queue:
                    for nxt in adjacent[queue.popleft()]&allowed-reached:
                        reached.add(nxt);queue.append(nxt)
                assert reached==allowed
                sublevels+=1
    # Essential scope control: actual Nielsen-only low sublevels need not be
    # connected before identifying simultaneous conjugation.
    first=('x','y');second=('yxY','y')
    assert sum(len(cyclic_reduce(w)) for w in first)==2
    assert sum(len(cyclic_reduce(w)) for w in second)==2
    for i in (0,1):
        j=1-i
        for x,y in product((1,-1),repeat=2):
            u=first[i] if x==1 else inverse(first[i]);v=first[j] if y==1 else inverse(first[j])
            assert len(cyclic_reduce(u+v))+len(first[j])==3
    return dict(status='PASS',ordinary_AC_goal_solved=False,
                signed_coprime_vectors_checked=vector_count,symbolic_graph_word_checks=word_checks,
                vector_coordinate_bound=vector_bound,unimodular_matrices_checked=sum(counts.values()),
                matrix_entry_bound=matrix_bound,matrix_classification=counts,
                positive_edge_weight_bound=weight_bound,finite_core_sublevels_checked=sublevels,
                actual_Nielsen_only_energy2_counterexample_verified=True,
                unbounded_lemma_requires_mathematical_proof=True,
                raw_peak_reduction_claimed=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    args=parser.parse_args();result=run()
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
