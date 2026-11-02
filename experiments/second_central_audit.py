"""Actual next-central-kernel defects of the optimized first-order endpoint.

Uses a genuine Schreier free basis of N, not arbitrary conjugates of b.
For w in N', computes its class in N'/[F,N']=(Lambda^2 Z[B3])_B3.
This is a path-specific diagnostic and is not an AC invariant.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import first_order_correction as f

m=f.m


def transversal(targets,max_depth=18,budget=2000000):
    words={m.IDENTITY:''};layer=[m.IDENTITY]
    for depth in range(max_depth+1):
        if targets<=words.keys():return words,depth
        nxt=[]
        for g in layer:
            for c in 'xXyY':
                h=m.product(g,m.LETTERS[c])
                if h not in words:
                    words[h]=words[g]+c;nxt.append(h)
                    if len(words)>budget:raise RuntimeError('transversal budget reached')
        layer=nxt
    raise RuntimeError('transversal depth reached')


def key_orientation(d):
    if d==m.IDENTITY:return None,0
    rev=m.inverse(d)
    if rev==d:raise AssertionError('unexpected nonidentity order-two B3 element')
    return (d,1) if d<rev else (rev,-1)


def wedge(a,b):
    result=defaultdict(int)
    for g,c in a.items():
        for h,e in b.items():
            key,sign=key_orientation(m.product(m.inverse(g),h))
            if sign:result[key]+=sign*c*e
    return m.clean(result)


def audit(words):
    targets={m.IDENTITY}
    paths=[]
    for word in words:
        g=m.IDENTITY;path=[]
        for c in word:
            h=m.product(g,m.LETTERS[c]);targets.add(h)
            path.append((g,c,h));g=h
        assert g==m.IDENTITY
        paths.append(path)
    reps,depth=transversal(targets)
    basis={};forms=[]
    for path,word in zip(paths,words):
        form=[]
        for g,c,h in path:
            edge=(g,c) if c.islower() else (h,c.lower())
            sign=1 if c.islower() else -1
            if edge not in basis:
                start,letter=edge
                end=m.product(start,m.LETTERS[letter])
                cell=m.free_reduce(reps[start]+letter+m.free_inverse(reps[end]))
                basis[edge]={'word':cell,'coefficient':m.module_coefficient(cell) if cell else {}}
            if not basis[edge]['word']:continue
            if form and form[-1][0]==edge and form[-1][1]==-sign:form.pop()
            else:form.append((edge,sign))
        reconstructed=m.free_reduce(''.join(basis[e]['word'] if s==1 else m.free_inverse(basis[e]['word']) for e,s in form))
        assert reconstructed==word
        forms.append(form)
    # A separate small check of the used Schreier generators' abelian
    # independence, under I's exact N_ab -> Z[B3] isomorphism.
    pivots={}
    for generator in basis.values():
        if not generator['word']:continue
        row={g:c%101 for g,c in generator['coefficient'].items() if c%101}
        while row:
            lead=min(row)
            if lead not in pivots:
                scale=pow(row[lead],-1,101)
                pivots[lead]={g:c*scale%101 for g,c in row.items()}
                break
            scale=row[lead]
            for g,c in pivots[lead].items():
                row[g]=(row.get(g,0)-scale*c)%101
                if not row[g]:row.pop(g)
    assert len(pivots)==sum(bool(v['word']) for v in basis.values())
    records=[]
    for form in forms:
        abelian=defaultdict(int);module={};q={}
        for edge,sign in form:
            abelian[edge]+=sign
            delta=m.add({},basis[edge]['coefficient'],sign)
            q=m.add(q,wedge(module,delta))
            module=m.add(module,delta)
        assert not m.clean(abelian) and not module
        assert all(c%2==0 for c in q.values())
        q={g:c//2 for g,c in q.items()}
        records.append({'schreier_length':len(form),'schreier_abelianization_zero':True,
                        'next_central_support':len(q),'next_central_l1':m.l1(q),
                        'next_central_class':[{'coefficient':c,'B3_exponent':g[0],
                                               'C2C3_syllables':g[1],
                                               'representative':f.representative(g)} for g,c in sorted(q.items())]})
    # Communtator control fixes the sign and factor-of-two convention.
    a,b={m.IDENTITY:1},{m.evaluate('x'):1};module={};q={}
    for v in (a,b,m.add({},a,-1),m.add({},b,-1)):
        q=m.add(q,wedge(module,v));module=m.add(module,v)
    assert q==m.add({},wedge(a,b),2) and len(q)==1
    return {'transversal_depth':depth,'transversal_vertices':len(reps),
            'needed_prefix_vertices':len(targets),
            'nonempty_schreier_generators_used':sum(bool(v['word']) for v in basis.values()),
            'schreier_module_rank_mod101':len(pivots),
            'residuals':records,
            'scope':'Next-central defect of this actual endpoint, not a global AC invariant'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('certificate')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    cert=f.load(args.certificate)
    words=[m.free_reduce(w+c.swapcase()) for w,c in zip(cert['target'],'xy')]
    result=audit(words)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='residuals'}|{
        'residual_summaries':[{k:v for k,v in r.items() if k!='next_central_class'} for r in result['residuals']]},indent=2))
