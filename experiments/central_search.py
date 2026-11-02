"""Exact AC search in F/[F,N] = B3 x Z, N=<<xyxYXY>>.

The extra Z coordinate is the x exponent sum of the original free word.
No quotient equality is silently used as a free-group move.
"""
import argparse
from collections import deque
import json
import time
import braid_relation_module as m


def mul(a,b):
    return m.product(a[0],b[0]), a[1]+b[1]


def inv(a):
    return m.inverse(a[0]), -a[1]


ONE=(m.IDENTITY,0)
X=(m.evaluate('x'),1)
Y=(m.evaluate('y'),0)
SIGNED=(X,inv(X),Y,inv(Y))
MOVES=[('invert',0),('invert',1),('multiply',0,1),('multiply',0,-1),
       ('multiply',1,1),('multiply',1,-1)]
MOVES += [('conjugate',i,g) for i in (0,1) for g in 'xXyY']


def evaluate(word):
    out=ONE
    for c in word:
        out=mul(out,SIGNED['xXyY'.index(c)])
    return out


START=(evaluate('xxxYYYY'),evaluate('xyxYXY'))
TARGET=(X,Y)


def apply(state,op):
    a,b=state
    if op==0:return inv(a),b
    if op==1:return a,inv(b)
    if op<6:
        i,sign=MOVES[op][1:]
        vals=list(state)
        donor=vals[1-i]
        vals[i]=mul(vals[i],donor if sign==1 else inv(donor))
        return tuple(vals)
    i,g=divmod(op-6,4)
    vals=list(state)
    vals[i]=mul(mul(SIGNED[g],vals[i]),inv(SIGNED[g]))
    return tuple(vals)


def inverse_op(op):
    return op if op<2 else op^1 if op<6 else 6+((op-6)^1)


def ball(start,depth,budget):
    seen={start:(None,None,0)}
    layer=[start]
    counts=[1]
    for d in range(depth):
        nxt=[]
        for state in layer:
            for op in range(14):
                other=apply(state,op)
                if other not in seen:
                    seen[other]=(state,op,d+1)
                    nxt.append(other)
                    if len(seen)>budget:return seen,counts,False
        counts.append(len(nxt));layer=nxt
    return seen,counts,True


def path(seen,at):
    result=[]
    while seen[at][0] is not None:
        at,op,_=seen[at]
        result.append(op)
    return result[::-1]


def search(depth,budget):
    begun=time.monotonic()
    forward,fc,fd=ball(START,depth,budget)
    backward,bc,bd=ball(TARGET,depth,budget)
    common=forward.keys()&backward.keys()
    result={'group':'F/[F,N] = B3 x Z, N=<<xyxYXY>>','depth':depth,
            'forward_layer_sizes':fc,'backward_layer_sizes':bc,
            'forward_states':len(forward),'backward_states':len(backward),
            'complete':fd and bd,'seconds':round(time.monotonic()-begun,3)}
    if common:
        meet=min(common,key=lambda s:forward[s][2]+backward[s][2])
        ops=path(forward,meet)+[inverse_op(op) for op in path(backward,meet)[::-1]]
        state=START
        for op in ops:state=apply(state,op)
        assert state==TARGET
        result.update(path_found=True,move_ids=ops,moves=[MOVES[op] for op in ops],
                      distance=len(ops) if fd and bd else None)
    else:
        result.update(path_found=False,distance_lower_bound=2*depth+1 if fd and bd else None)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--depth',type=int,default=6)
    parser.add_argument('--budget',type=int,default=1000000)
    parser.add_argument('--output')
    parser.add_argument('--n',type=int,default=3)
    args=parser.parse_args()
    if args.n<2:raise ValueError('require n>=2')
    START=(evaluate('x'*args.n+'Y'*(args.n+1)),evaluate('xyxYXY'))
    for state in (START,TARGET):
        for op in range(14):assert apply(apply(state,op),inverse_op(op))==state
    assert evaluate('xyxYXY')==(m.IDENTITY,1)
    result=search(args.depth,args.budget)
    result['n']=args.n
    result['start_words']=['x'*args.n+'Y'*(args.n+1),'xyxYXY']
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
