"""Compile an actual AC certificate in F/[N,N], N=<<xyxYXY>>.

Requires the synchronized product quotient lift from Research G. Uses only
ordinary relator inversion/multiplication and ambient-word conjugation.
Every word conjugation has an explicit finite generator expansion.
"""
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path
import braid_relation_module as m

BRAID='xyxYXY'


def representative(g):
    """A direct exact B3 representative; no bounded word search."""
    pieces=[]
    for factor,power in g[1]:
        pieces.append('xyx' if factor==0 else 'xy'*power)
    tail=''.join(pieces)
    exponent=sum(1 if c.islower() else -1 for c in tail)
    assert (g[0]-exponent)%6==0
    central=(g[0]-exponent)//6
    word=m.free_reduce(('xyxyxy'*central if central>=0 else 'YXYXYX'*(-central))+tail)
    assert m.evaluate(word)==g
    return word


def augmentation_decomposition(k):
    """K=(1-x)A+(1-y)B via right telescoping of group words."""
    assert m.augment(k)==0
    output=[{},{}]
    for g,coefficient in k.items():
        suffix=m.IDENTITY
        for c in representative(g)[::-1]:
            i='xy'.index(c.lower())
            if c.islower():
                output[i]=m.add(output[i],{suffix:-coefficient})
            else:
                output[i]=m.add(output[i],{m.product(m.LETTERS[c],suffix):coefficient})
            suffix=m.product(m.LETTERS[c],suffix)
        assert suffix==g
    reconstructed={}
    for c,a in zip('xy',output):
        reconstructed=m.add(reconstructed,m.ring_product(m.add({m.IDENTITY:1},{m.evaluate(c):1},-1),a))
    assert reconstructed==k
    return output


def kernel_word(h):
    factors=[]
    for g,coefficient in sorted(h.items()):
        q=representative(g)
        cell=BRAID if coefficient>0 else m.free_inverse(BRAID)
        factors.extend((q+cell+m.free_inverse(q)) for _ in range(abs(coefficient)))
    word=m.free_reduce(''.join(factors))
    assert m.evaluate(word)==m.IDENTITY
    db=m.fox(BRAID)
    assert m.fox(word)==tuple(m.ring_product(h,d) for d in db)
    return word


def apply(state,move):
    result=list(state)
    i=move['i']
    if type(i) is not int or i not in (0,1):
        raise ValueError('invalid relator index')
    if move['op']=='invert':
        result[i]=m.free_inverse(result[i])
    elif move['op']=='multiply':
        j=move['j']
        if type(j) is not int or j not in (0,1) or j==i:
            raise ValueError('recipient and donor must differ')
        if move.get('sign',1) not in (-1,1):
            raise ValueError('invalid multiplication sign')
        donor=result[j] if move.get('sign',1)==1 else m.free_inverse(result[j])
        result[i]=m.free_reduce(result[i]+donor)
    elif move['op']=='conjugate':
        g=move.get('word',move.get('g'))
        if not isinstance(g,str) or not set(g)<=set('xXyY'):
            raise ValueError('invalid conjugator')
        result[i]=m.free_reduce(g+result[i]+m.free_inverse(g))
    else:
        raise ValueError('invalid operation')
    return result


def errors(state):
    words=[m.free_reduce(w+m.free_inverse(c)) for w,c in zip(state,'xy')]
    assert [m.evaluate(w) for w in words]==[m.IDENTITY,m.IDENTITY]
    return [m.module_coefficient(w) for w in words]


def own_macro(i,h):
    return [{'op':'conjugate','i':i,'word':h}]


def cross_macro(i,h):
    c='xy'[i]
    return [{'op':'conjugate','i':i,'word':c},
            {'op':'multiply','i':i,'j':1-i,'sign':1},
            {'op':'conjugate','i':i,'word':h},
            {'op':'multiply','i':i,'j':1-i,'sign':-1},
            {'op':'conjugate','i':i,'word':m.free_inverse(h)},
            {'op':'conjugate','i':i,'word':c.swapcase()}]


def selftest():
    # Check both macros on nontrivial kernel errors by exact free-word replay
    # and independent Fox calculation, not just the formal derived formula.
    sample=['x'+BRAID,'y'+m.free_inverse(BRAID)]
    before=errors(sample)
    h='x'+BRAID+'X'
    H={m.evaluate('x'):1}
    for i in (0,1):
        for cross,macro in ((False,own_macro(i,h)),(True,cross_macro(i,h))):
            state=sample[:]
            for move in macro:
                state=apply(state,move)
            after=errors(state)
            target_letter='xy'[1-i if cross else i]
            expected=m.add(before[i],m.ring_product(m.add({m.IDENTITY:1},{m.evaluate(target_letter):1},-1),H))
            assert after[i]==expected
            assert after[1-i]==before[1-i]


def compile_certificate(source):
    with open(source) as stream:
        parent=json.load(stream)
    state=list(parent['target'])
    initial_errors=errors(state)
    assert [m.augment(k) for k in initial_errors]==[0,0]
    correction=[]
    phases=[]
    peak=sum(map(len,state))
    for i in (0,1):
        k=errors(state)[i]
        a,b=augmentation_decomposition(k)
        desired=[m.add({},a,-1),m.add({},b,-1)]
        for own in (True,False):
            index=i if own else 1-i
            h=kernel_word(desired[index])
            moves=own_macro(i,h) if own else cross_macro(i,h)
            for move in moves:
                state=apply(state,move)
                correction.append(move)
                peak=max(peak,sum(map(len,state)))
            phases.append({'recipient':i,'own_direction':own,'conjugator_length':len(h),
                           'module_support':[len(e) for e in errors(state)],
                           'free_lengths':list(map(len,state))})
        assert errors(state)[i]=={}
    assert errors(state)==[{},{}]
    moves=parent['moves']+correction
    endpoint=list(parent['start'])
    for move in moves:
        endpoint=apply(endpoint,move)
    assert endpoint==state
    assert state!=['x','y']
    strict_count=0
    for move in moves:
        if move['op']=='conjugate':
            strict_count+=len(move.get('word',move.get('g')))
        elif move['op']=='multiply' and move.get('sign',1)==-1:
            strict_count+=3
        else:
            strict_count+=1
    return {'format':'ordinary-ac-word-conjugation-v1',
            'scope':'AC trivialization only in F/[N,N], N=normal closure of xyxYXY; not in F',
            'start':parent['start'],'target':state,'quotient_target':['x','y'],
            'kernel_relator':BRAID,'moves':moves,
            'source_prefix_strict_moves':len(parent['moves']),
            'correction_word_operations':len(correction),
            'expanded_single_generator_move_count':strict_count,
            'initial_module_supports':list(map(len,initial_errors)),
            'initial_module_norms':list(map(m.l1,initial_errors)),
            'final_free_lengths':list(map(len,state)),
            'final_free_word_sha256':[hashlib.sha256(w.encode()).hexdigest() for w in state],
            'final_module_coefficients':[[],[]],
            'peak_at_recorded_word_operations':peak,'phases':phases}


def verify(cert):
    assert cert['format']=='ordinary-ac-word-conjugation-v1'
    current=list(cert['start'])
    count=0
    expanded_peak_upper=0
    for move in cert['moves']:
        if move['op']=='conjugate':
            length=len(move.get('word',move.get('g')))
            count+=length
            expanded_peak_upper=max(expanded_peak_upper,sum(map(len,current))+2*length)
        elif move['op']=='multiply' and move.get('sign',1)==-1:
            count+=3
        else:
            count+=1
        current=apply(current,move)
        expanded_peak_upper=max(expanded_peak_upper,sum(map(len,current)))
    assert current==cert['target']
    assert errors(current)==[{},{}]
    assert current!=['x','y']
    assert count==cert['expanded_single_generator_move_count']
    assert list(map(len,current))==cert['final_free_lengths']
    assert [hashlib.sha256(w.encode()).hexdigest() for w in current]==cert['final_free_word_sha256']
    return {'status':'PASS','quotient':'F/[N,N], N=<<xyxYXY>>',
            'word_operations':len(cert['moves']),
            'expanded_single_generator_move_count':count,
            'expanded_raw_peak_upper_bound':expanded_peak_upper,
            'final_free_lengths':list(map(len,current)),
            'free_group_goal_solved':False}


def load(path):
    raw=Path(path).read_bytes()
    if str(path).endswith('.gz.b64'):
        raw=gzip.decompress(base64.b64decode(raw))
    return json.loads(raw)


def save(path,data):
    raw=(json.dumps(data,indent=2)+'\n').encode()
    if str(path).endswith('.gz.b64'):
        raw=base64.b64encode(gzip.compress(raw,mtime=0))+b'\n'
    Path(path).write_bytes(raw)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',default='certificates/product_quotient_lift.json')
    parser.add_argument('--output')
    parser.add_argument('--verify')
    parser.add_argument('--endpoint-output')
    parser.add_argument('--report-output')
    args=parser.parse_args()
    selftest()
    if args.verify:
        saved=load(args.verify)
    else:
        saved=compile_certificate(args.source)
        if args.output:
            save(args.output,saved)
    report=verify(saved)
    if args.endpoint_output:
        Path(args.endpoint_output).write_text('\n'.join(saved['target'])+'\n')
    if args.report_output:
        Path(args.report_output).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
