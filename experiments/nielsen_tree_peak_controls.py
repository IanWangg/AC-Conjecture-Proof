"""Exact controls for rank-two cyclic basis-sublevel connectivity.

The unbounded proof is in nielsen-cyclic-sublevels.md. Finite controls
verify the geometric length formulas and descent conventions only.
"""
import argparse
from itertools import product,combinations
import json
from math import gcd
from pathlib import Path


def inv(w):return w.swapcase()[::-1]


def cyclic(w):
    out=[]
    for c in w:
        if out and out[-1]==c.swapcase():out.pop()
        else:out.append(c)
    while len(out)>1 and out[0]==out[-1].swapcase():out=out[1:-1]
    return ''.join(out)


def positive(a,b):
    assert gcd(a,b)==1
    if not a:return 'y'
    if not b:return 'x'
    if a==b:return 'xy'
    if a>b:return positive(a-b,b).replace('y','xy')
    return positive(a,b-a).replace('x','xy')


def model(a,b):
    w=positive(abs(a),abs(b))
    return w.translate(str.maketrans({'x':'X' if a<0 else 'x','y':'Y' if b<0 else 'y'}))


def length(shape,weights,v):
    p,q,r=weights;a,b=v
    if shape=='rose':return abs(a)*p+abs(b)*r
    if shape=='theta':return abs(a+b)*p+abs(a)*q+abs(b)*r
    return abs(a)*p+abs(b)*r+2*min(abs(a),abs(b))*q


def matrix_energy(shape,weights,M):return sum(length(shape,weights,v) for v in M)


def neighbors(M):
    for i in (0,1):
        for sign in (-1,1):
            nxt=list(M)
            nxt[i]=tuple(a+sign*b for a,b in zip(M[i],M[1-i]))
            yield tuple(nxt)


def quotient(M):
    def orient(v):return tuple(-c for c in v) if next(c for c in v if c)<0 else tuple(v)
    return tuple(sorted(map(orient,M)))


def checks(vector_bound=12,matrix_bound=8):
    weights_list=((1,1,1),(1,2,5),(7,3,2),(3,3,9))
    images={'rose':('p','r'),'theta':('pQ','pR'),'barbell':('p','qrQ')}
    formulas=descents=0;max_steps=0
    for shape,images_pair in images.items():
        for weights in weights_list:
            for a,b in product(range(-vector_bound,vector_bound+1),repeat=2):
                if gcd(a,b)!=1:continue
                w=model(a,b)
                substitution={'x':images_pair[0],'y':images_pair[1],
                              'X':inv(images_pair[0]),'Y':inv(images_pair[1])}
                reduced=cyclic(''.join(substitution[c] for c in w))
                actual=sum(dict(zip('pqr',weights))[c.lower()] for c in reduced)
                assert actual==length(shape,weights,(a,b))
                formulas+=1
            minimum=(sum(weights)+min(weights) if shape=='theta' else weights[0]+weights[2])
            for a,b,c,d in product(range(-matrix_bound,matrix_bound+1),repeat=4):
                if abs(a*d-b*c)!=1:continue
                M=((a,b),(c,d));steps=0
                while True:
                    value=matrix_energy(shape,weights,M)
                    choices=sorted((matrix_energy(shape,weights,nxt),nxt) for nxt in neighbors(M))
                    if choices[0][0]>=value:break
                    M=choices[0][1];steps+=1
                assert matrix_energy(shape,weights,M)==minimum
                max_steps=max(max_steps,steps);descents+=1
            rays=((1,0),(0,1),(1,-1),(1,1))
            core={quotient((u,v)) for u,v in combinations(rays,2) if abs(u[0]*v[1]-u[1]*v[0])==1}
            assert len(core)==5
            minima={M for M in core if matrix_energy(shape,weights,M)==minimum}
            pending=[next(iter(minima))];seen=set(pending)
            while pending:
                M=pending.pop()
                for n in neighbors(M):
                    k=quotient(n)
                    if k in minima-seen:seen.add(k);pending.append(k)
            assert seen==minima
    return {'status':'PASS','ordinary_AC_goal_solved':False,
            'geometric_primitive_length_formula_checks':formulas,
            'unimodular_matrix_descent_controls':descents,
            'maximum_strict_descent_steps_in_controls':max_steps,
            'vector_entry_bound':vector_bound,'matrix_entry_bound':matrix_bound,
            'geometric_shapes':['rose','theta','barbell'],
            'weight_triples':[list(w) for w in weights_list],
            'finite_core_minimum_connectedness_checked':True,
            'actual_Nielsen_only_sublevel_connectivity_claimed':False,
            'scope':'Finite controls for the separate unbounded cyclic-state quotient proof'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    args=parser.parse_args();result=checks()
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
