"""Smaller exact first-order correction from a short central-quotient path.

Imports Research I's proved correction macros, but changes the prefix,
group representative choices, and ordering of kernel cells. The actual
free endpoint is recorded and is never silently replaced by the basis.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import first_order_correction as f

m=f.m


class Representatives:
    def __init__(self,depth=12):
        self.words={m.IDENTITY:''}
        layer=[m.IDENTITY]
        for _ in range(depth):
            nxt=[]
            for g in layer:
                for c in 'xXyY':
                    h=m.product(g,m.LETTERS[c])
                    if h not in self.words:
                        self.words[h]=self.words[g]+c
                        nxt.append(h)
            layer=nxt

    def __call__(self,g):
        if g not in self.words:self.words[g]=f.representative(g)
        return self.words[g]

    def add_prefixes(self,words):
        for word in words:
            g=m.IDENTITY
            for i,c in enumerate(word):
                g=m.product(g,m.LETTERS[c])
                if g not in self.words or len(self.words[g])>i+1:self.words[g]=word[:i+1]


def decompose(k,representative):
    assert m.augment(k)==0
    output=[{},{}]
    for g,coefficient in k.items():
        suffix=m.IDENTITY
        for c in representative(g)[::-1]:
            i='xy'.index(c.lower())
            if c.islower():output[i]=m.add(output[i],{suffix:-coefficient})
            else:output[i]=m.add(output[i],{m.product(m.LETTERS[c],suffix):coefficient})
            suffix=m.product(m.LETTERS[c],suffix)
        assert suffix==g
    reconstructed={}
    for c,h in zip('xy',output):
        reconstructed=m.add(reconstructed,m.ring_product({m.IDENTITY:1,m.evaluate(c):-1},h))
    assert reconstructed==k
    return output


def kernel_word(h,representative):
    factors=[]
    for g,coefficient in h.items():
        q=representative(g)
        cell=f.BRAID if coefficient>0 else m.free_inverse(f.BRAID)
        factors.append((q,q+cell*abs(coefficient)+m.free_inverse(q)))
    factors.sort()
    word=m.free_reduce(''.join(v for _,v in factors))
    assert m.evaluate(word)==m.IDENTITY
    assert m.fox(word)==tuple(m.ring_product(h,d) for d in m.fox(f.BRAID))
    return word


def compile_prefix(parent,representative,coordinate_order=(0,1),own_first=(True,True)):
    state=parent['target'][:]
    initial=f.errors(state)
    assert [m.augment(k) for k in initial]==[0,0]
    representative.add_prefixes(state)
    correction=[];phases=[];peak=sum(map(len,state))
    for i in coordinate_order:
        k=f.errors(state)[i]
        a,b=decompose(k,representative)
        desired=[m.add({},a,-1),m.add({},b,-1)]
        directions=(True,False) if own_first[i] else (False,True)
        for own in directions:
            h=kernel_word(desired[i if own else 1-i],representative)
            ops=f.own_macro(i,h) if own else f.cross_macro(i,h)
            for op in ops:
                state=f.apply(state,op);correction.append(op)
                peak=max(peak,sum(map(len,state)))
            phases.append({'recipient':i,'own_direction':own,'conjugator_length':len(h),
                           'module_support':[len(v) for v in f.errors(state)],
                           'free_lengths':list(map(len,state))})
        assert f.errors(state)[i]=={}
    assert f.errors(state)==[{},{}]
    moves=parent['moves']+correction
    strict=sum(len(op.get('word',op.get('g'))) if op['op']=='conjugate' else
               3 if op['op']=='multiply' and op.get('sign',1)<0 else 1 for op in moves)
    cert={'format':'ordinary-ac-word-conjugation-v1',
          'scope':'Short central prefix and optimized first-order quotient correction; not a free basis',
          'start':parent['start'],'target':state,'quotient_target':['x','y'],
          'kernel_relator':f.BRAID,'moves':moves,
          'source_prefix_strict_moves':len(parent['moves']),
          'correction_word_operations':len(correction),
          'expanded_single_generator_move_count':strict,
          'initial_module_supports':list(map(len,initial)),
          'initial_module_norms':list(map(m.l1,initial)),
          'final_free_lengths':list(map(len,state)),
          'final_free_word_sha256':[hashlib.sha256(w.encode()).hexdigest() for w in state],
          'final_module_coefficients':[[],[]],
          'peak_at_recorded_word_operations':peak,'phases':phases,
          'coordinate_order':coordinate_order,'own_first':own_first}
    return cert


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('prefixes',nargs='+')
    parser.add_argument('--output',required=True)
    parser.add_argument('--summary')
    args=parser.parse_args()
    representative=Representatives()
    best=None;records=[]
    for path in args.prefixes:
        parent=json.loads(Path(path).read_text())
        for order in ((0,1),(1,0)):
            for own_first in itertools.product((False,True),repeat=2):
                cert=compile_prefix(parent,representative,order,own_first)
                record={'prefix':path,'coordinate_order':order,'own_first':own_first,
                        'expanded_moves':cert['expanded_single_generator_move_count'],
                        'free_lengths':cert['final_free_lengths']}
                records.append(record)
                score=(sum(record['free_lengths']),record['expanded_moves'])
                if best is None or score<best[0]:best=(score,cert)
    report=f.verify(best[1]);report['variants']=records
    f.save(args.output,best[1])
    if args.summary:Path(args.summary).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
