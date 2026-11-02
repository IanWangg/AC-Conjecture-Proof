"""Discovery search after a short initial coordinate Nielsen prelude.

The literal ledgers are kept for every chosen basis. Independently conjugate
the resulting two words and inspect the actual subgroup, rather than any
group quotient. Inconclusive signed-cycle tests are not proof of primitives.
"""
import argparse
import json
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'research_m'))
from stallings_search import nielsen_move,primitive
import arbitrary_tail_certificate as ac


def cyclic(word):
    word=ac.freely_reduce(word)
    while len(word)>1 and word[0]==word[-1].swapcase():word=word[1:-1]
    return word


def orbit_min(word):
    word=cyclic(word)
    return min(v[k:]+v[:k] for v in (word,ac.inverse(word)) for k in range(len(v)))


def family_key(state):
    return tuple(sorted(map(orbit_min,state)))


def first_preludes(depth,max_cyclic_total):
    initial=(ac.P,ac.B)
    states={initial:[]}
    representatives={family_key(initial):(initial,[])}
    layer=[initial]
    for level in range(depth):
        following=[]
        for state in layer:
            for recipient in (0,1):
                for left in (False,True):
                    for negative in (False,True):
                        other,moves=nielsen_move(state,recipient,left,negative)
                        if other in states:continue
                        states[other]=states[state]+moves
                        following.append(other)
                        if sum(map(len,map(cyclic,other)))<=max_cyclic_total:
                            representatives.setdefault(family_key(other),(other,states[other]))
        layer=following
    return representatives


def scan_pair(u,v,max_tail=None):
    # The long-tail barbell lemma requires both cyclic factors themselves
    # to be nonprimitive. Certify these directly as well as via M's
    # initial-subgroup theorem.
    for word in (u,v):ac.orders(ac.fold((word,)))
    bound=len(u)//2+len(v)//2
    if max_tail is not None:bound=min(bound,max_tail)
    seen=set()
    bad=[]
    total=0
    started=time.monotonic()
    for q in ac.reduced_words(bound):
        total+=1
        key=ac.fold((u,ac.freely_reduce(q+v+ac.inverse(q))))
        if key in seen:continue
        seen.add(key)
        try:ac.orders(key)
        except AssertionError:
            bad.append({'q':q,'encoded':key})
    return {'u':u,'v':v,'tail_bound':bound,
            'complete_finite_reduction':max_tail is None or bound==len(u)//2+len(v)//2,
            'reduced_tails':total,'unique_graphs':len(seen),'inconclusive_graphs':bad,
            'seconds':time.monotonic()-started}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--depth',type=int,default=1)
    parser.add_argument('--max-cyclic-total',type=int,default=19)
    parser.add_argument('--max-tail',type=int)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    families=first_preludes(args.depth,args.max_cyclic_total)
    rows=[]
    for key,(state,moves) in sorted(families.items(),key=lambda row:(sum(map(len,row[0])),row[0])):
        result=scan_pair(*key,max_tail=args.max_tail)
        result['prelude_endpoint']=state
        result['prelude_strict_moves']=moves
        rows.append(result)
        print(json.dumps({'u':key[0],'v':key[1],'tails':result['reduced_tails'],
                          'graphs':result['unique_graphs'],'inconclusive':len(result['inconclusive_graphs'])}),flush=True)
        Path(args.output).write_text(json.dumps({'depth':args.depth,'families':rows},indent=2)+'\n')
