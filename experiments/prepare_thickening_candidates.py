"""Record ambient Nielsen descent solely as a thickening search device.

These are ambient generator automorphisms, NOT elementary AC moves.
No negative inference about unsampled presentation complexes is made.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

def inverse(w):
    return w.swapcase()[::-1]

def cyclic(w):
    stack=[]
    for c in w:
        if stack and stack[-1] == c.swapcase():
            stack.pop()
        else:
            stack.append(c)
    a,b=0,len(stack)
    while b>a+1 and stack[a] == stack[b-1].swapcase():
        a,b=a+1,b-1
    return ''.join(stack[a:b])

def canon_word(w):
    return min(v[k:]+v[:k] for v in (w,inverse(w)) for k in range(len(v)))

def canon_pair(words):
    return tuple(sorted(map(canon_word,words)))

def transform(words,op):
    target,donor,left=op
    image=donor+target if left else target+donor
    mapping={target:image,target.swapcase():inverse(image)}
    return tuple(cyclic(''.join(mapping.get(c,c) for c in w)) for w in words)

OPS=[(target,donor,left) for target in 'xy' for donor in ('yY' if target=='x' else 'xX') for left in (False,True)]

def descend(words):
    state=tuple(words)
    history=[]
    while True:
        choices=[(sum(map(len,t)),t,op) for op in OPS for t in [transform(state,op)]]
        length,new,op=min(choices)
        if length>=sum(map(len,state)):
            return canon_pair(state),history
        history.append(op)
        state=new

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--tsv',required=True);p.add_argument('--provenance',required=True)
    args=p.parse_args();seen={}
    for index,row in enumerate(Path(args.input).read_text().splitlines()):
        words=row.split('\t');key,program=descend(words)
        if key not in seen:
            seen[key]={'source_index':index,'source_words':words,'ambient_nielsen_program':program,'candidate_words':key}
    keys=sorted(seen,key=lambda x:(sum(map(len,x)),x))
    Path(args.tsv).write_text(''.join('\t'.join(x)+'\n' for x in keys))
    Path(args.provenance).write_text(json.dumps({'scope':'Ambient Nielsen search candidates, not AC ledgers',
        'distinct_candidates':len(keys),'energy_histogram':dict(sorted(Counter(sum(map(len,x)) for x in keys).items())),
        'candidates':[seen[x] for x in keys]},indent=2)+'\n')
    print(len(keys),Counter(sum(map(len,x)) for x in keys))
