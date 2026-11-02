"""Construct a short AC prefix aligned in B3 and free abelianization."""
import argparse
import json
from pathlib import Path
import first_order_correction as f


def apply_path(start,moves):
    state=start[:]
    for move in moves:state=f.apply(state,move)
    return state


def signed_expansion(path):
    result=[]
    for kind,i,*rest in path:
        if kind=='multiply':
            j=1-i
            if rest[0]<0:result.append({'op':'invert','i':j})
            result.append({'op':'multiply','i':i,'j':j})
            if rest[0]<0:result.append({'op':'invert','i':j})
        elif kind=='conjugate':result.append({'op':'conjugate','i':i,'g':rest[0]})
        else:result.append({'op':'invert','i':i})
    return result


def aligned(n=3):
    if n!=3:raise ValueError('this explicit braid prefix is for AK(3)')
    # Batch all three initial inverse-donor multiplications together.
    moves=[{'op':'invert','i':1}]+[{'op':'multiply','i':0,'j':1}]*3+[{'op':'invert','i':1}]
    # Research E's path: its first two negative multiplications share an
    # unchanged donor, so invert and restore that donor only once.
    moves += [
        {'op':'invert','i':0}, {'op':'multiply','i':1,'j':0},
        {'op':'conjugate','i':1,'g':'Y'}, {'op':'conjugate','i':1,'g':'X'},
        {'op':'multiply','i':1,'j':0}, {'op':'invert','i':0},
        {'op':'conjugate','i':0,'g':'X'}, {'op':'multiply','i':0,'j':1},
        {'op':'conjugate','i':0,'g':'X'}, {'op':'conjugate','i':0,'g':'X'},
        {'op':'conjugate','i':0,'g':'y'}, {'op':'invert','i':0},
        {'op':'multiply','i':1,'j':0}, {'op':'invert','i':0}]
    return moves


def certificate(moves,n=3):
    start=['x'*n+'Y'*(n+1),'xyxYXY']
    target=apply_path(start,moves)
    assert [f.m.evaluate(w) for w in target]==[f.m.evaluate(c) for c in 'xy']
    exponents=[[w.count('x')-w.count('X'),w.count('y')-w.count('Y')] for w in target]
    assert exponents==[[1,0],[0,1]]
    return {'format':'ordinary-ac-elementary-v1',
            'scope':'Prefix to the free basis only in F/[F,N]; actual free endpoint recorded',
            'start':start,'target':target,'moves':moves,
            'free_exponent_vectors':exponents}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--search')
    parser.add_argument('--n',type=int,default=3)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    if args.search:
        search=json.loads(Path(args.search).read_text())
        moves=signed_expansion(search['moves'])
    else:moves=aligned(args.n)
    cert=certificate(moves,args.n)
    Path(args.output).write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps({'strict_moves':len(moves),'free_lengths':list(map(len,cert['target'])),
                      'free_exponent_vectors':cert['free_exponent_vectors']},indent=2))
