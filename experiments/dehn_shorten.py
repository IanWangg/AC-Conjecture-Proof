"""Certificate-producing greedy cyclic relator substitutions in the FREE group.

This is a search heuristic, not a complete enumeration or obstruction.
Every accepted shortening is explicitly compiled into ordinary AC moves.
"""
import argparse
import json
from pathlib import Path
import first_order_correction as f


def cyclic_core(word):
    a,b=0,len(word)
    while b>a+1 and word[a]==word[b-1].swapcase():a+=1;b-=1
    return word[:a],word[a:b]


def longest(a,b):
    """Longest cyclic common substring, returning length and start indices."""
    n,m=len(a),len(b)
    aa,bb=a+a,b+b
    below=[0]*(2*m+1)
    best=(0,0,0)
    for i in range(2*n-1,-1,-1):
        row=[0]*(2*m+1)
        for j in range(2*m-1,-1,-1):
            if aa[i]==bb[j]:
                row[j]=min(n,m,1+below[j+1])
                if i<n and j<m and row[j]>best[0]:best=(row[j],i,j)
        below=row
    return best


def shorten(start,max_steps=100):
    state=list(start);moves=[];trace=[]
    def apply(op):
        nonlocal state
        state=f.apply(state,op);moves.append(op)
    def cyclic(i):
        prefix,core=cyclic_core(state[i])
        if prefix:apply({'op':'conjugate','i':i,'word':f.m.free_inverse(prefix)})
        assert state[i]==core
    for i in (0,1):cyclic(i)
    for step in range(max_steps):
        if not state[0] or not state[1]:break
        candidates=[]
        for i in (0,1):
            j=1-i
            for negative in (False,True):
                donor=f.m.free_inverse(state[j]) if negative else state[j]
                t,a,b=longest(state[i],f.m.free_inverse(donor))
                gain=2*t-len(donor)
                if gain>0:candidates.append((gain,i,negative,t,a,b))
        if not candidates:break
        gain,i,negative,t,a,b=max(candidates)
        j=1-i
        old=sum(map(len,state));n=len(state[i]);m=len(state[j])
        recipient_rotation=(a+t)%n
        prefix=state[i][:recipient_rotation]
        if prefix:apply({'op':'conjugate','i':i,'word':f.m.free_inverse(prefix)})
        if negative:apply({'op':'invert','i':j})
        donor_rotation=(-b-t)%m
        donor_prefix=state[j][:donor_rotation]
        if donor_prefix:apply({'op':'conjugate','i':j,'word':f.m.free_inverse(donor_prefix)})
        # Check the planned cancelling boundary before using it.
        assert state[i][-t:]==f.m.free_inverse(state[j][:t])
        apply({'op':'multiply','i':i,'j':j})
        if donor_prefix:apply({'op':'conjugate','i':j,'word':donor_prefix})
        if negative:apply({'op':'invert','i':j})
        cyclic(i)
        new=sum(map(len,state))
        assert new<=old-gain<old
        trace.append({'step':step+1,'recipient':i,'cancelled_letters':t,
                      'old_total':old,'new_total':new,'lengths':list(map(len,state))})
    return state,moves,trace


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('certificate')
    parser.add_argument('--output',required=True)
    parser.add_argument('--summary')
    parser.add_argument('--close-to-start',action='store_true')
    args=parser.parse_args()
    parent=f.load(args.certificate)
    target,moves,trace=shorten(parent['target'])
    closing=[]
    if args.close_to_start:
        for i,wanted in enumerate(parent['start']):
            found=False
            for negative in (False,True):
                s=f.m.free_inverse(target[i]) if negative else target[i]
                for k in range(len(s)):
                    if s[k:]+s[:k]!=wanted:continue
                    if negative:
                        op={'op':'invert','i':i};target=f.apply(target,op);closing.append(op)
                    prefix,suffix=s[:k],s[k:]
                    g=f.m.free_inverse(prefix) if len(prefix)<=len(suffix) else suffix
                    if g:
                        op={'op':'conjugate','i':i,'word':g};target=f.apply(target,op);closing.append(op)
                    found=True;break
                if found:break
            if not found:raise ValueError('shortened tuple is not in the ordered initial cyclic/inverse orbit')
        assert target==parent['start']
        moves+=closing
    cert={'format':'ordinary-ac-word-conjugation-v1',
          'scope':'Actual free-group AC path through an optimized first-order quotient lift and greedy shortening; no basis claimed',
          'start':parent['start'],'target':target,'moves':parent['moves']+moves,
          'greedy_shortening_trace':trace}
    f.save(args.output,cert)
    report={'initial_free_lengths':list(map(len,parent['target'])),
            'final_free_lengths':list(map(len,target)),
            'final_free_words':target,'shortening_steps':len(trace),
            'added_word_operations':len(moves),'ordinary_free_goal_solved':target==['x','y'],
            'closing_word_operations':len(closing),'closed_loop':args.close_to_start,
            'trace':trace}
    if args.summary:Path(args.summary).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
