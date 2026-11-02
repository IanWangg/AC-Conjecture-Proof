"""Compile an actual ordinary-AC completion from a primitive-relator waypoint.

Ambient automorphisms are a derivation device. Every resulting operation is
transported back and explicitly expanded into the strict relator primitives.
"""
import argparse
import json
from pathlib import Path
from stallings_search import inverse, reduce, apply, nielsen_move, primitive


def substitute(word, images):
    table = {'x':images[0], 'X':inverse(images[0]),
             'y':images[1], 'Y':inverse(images[1])}
    return reduce(''.join(table[c] for c in word))


def aut_images(op, undo=False):
    kind = op[0]
    images = ['x','y']
    if kind == 'nielsen':
        _,i,left,negative = op
        if undo:
            negative = not negative
        d = images[1-i]
        if negative:
            d = inverse(d)
        images[i] = d+images[i] if left else images[i]+d
    elif kind == 'inner':
        g = inverse(op[1]) if undo else op[1]
        images = [reduce(g+w+inverse(g)) for w in images]
    elif kind == 'swap':
        images = ['y','x']
    else:
        images[op[1]] = inverse(images[op[1]])
    return images


def primitive_aut(word, index):
    ops = []
    current = word

    def change(op):
        nonlocal current
        current = substitute(current,aut_images(op))
        ops.append(op)

    while len(current)>1:
        if current[0] == current[-1].swapcase():
            change(('inner',current[0].swapcase()))
            continue
        best = None
        for i in range(2):
            for left in (False,True):
                for negative in (False,True):
                    op = ('nielsen',i,left,negative)
                    nxt = substitute(current,aut_images(op))
                    cyclic = nxt
                    while len(cyclic)>1 and cyclic[0] == cyclic[-1].swapcase():
                        cyclic=cyclic[1:-1]
                    if len(cyclic)<len(current):
                        item = (len(cyclic),nxt,op)
                        if best is None or item<best:
                            best=item
        if best is None:
            raise ValueError('word is not primitive')
        change(best[2])
    target = 'xy'[index]
    if current.lower()!=target:
        change(('swap',))
    if current.isupper():
        change(('invert',index))
    assert current==target
    forward=['x','y']
    for op in ops:
        forward=[substitute(w,aut_images(op)) for w in forward]
    backward=['x','y']
    for op in ops[::-1]:
        backward=[substitute(w,aut_images(op,True)) for w in backward]
    assert [substitute(w,forward) for w in backward]==['x','y']
    assert [substitute(w,backward) for w in forward]==['x','y']
    assert substitute(word,forward)==target
    return ops,forward,backward


def complete(parent):
    state = tuple(parent['target'])
    index = next((i for i,w in enumerate(state) if primitive(w)),None)
    if index is None:
        raise ValueError('no primitive relator at waypoint')
    ops,forward,backward=primitive_aut(state[index],index)
    transformed=tuple(substitute(w,forward) for w in state)
    donor='xy'[index]
    assert transformed[index]==donor
    other=1-index
    model=transformed
    model_moves=[]

    def model_emit(op):
        nonlocal model
        model=apply(model,op)
        model_moves.append(op)

    def model_conjugate(i,word):
        for g in word[::-1]:
            model_emit({'op':'conjugate','i':i,'g':g})

    # Delete each donor-generator letter by a conjugated donor, then restore it.
    while donor in model[other] or donor.swapcase() in model[other]:
        word=model[other]
        position=next(k for k,c in enumerate(word) if c.lower()==donor)
        c=word[position]
        suffix=word[position+1:]
        if c.islower():
            model_emit({'op':'invert','i':index})
        model_conjugate(index,inverse(suffix))
        model_emit({'op':'multiply','i':other,'j':index})
        model_conjugate(index,suffix)
        if c.islower():
            model_emit({'op':'invert','i':index})
        assert model[other]==reduce(word[:position]+suffix)
        assert model[index]==donor
    if model[other]=='xy'[other].swapcase():
        model_emit({'op':'invert','i':other})
    assert model==('x','y')

    ledger=list(parent['moves'])
    actual=tuple(parent['target'])

    def emit(move):
        nonlocal actual
        actual=apply(actual,move)
        ledger.append(move)

    def conjugate(i,word):
        for g in word[::-1]:
            emit({'op':'conjugate','i':i,'g':g})

    def coordinate_nielsen(i,left,negative):
        nonlocal actual
        actual2,part=nielsen_move(actual,i,left,negative)
        for move in part:
            emit(move)
        assert actual==actual2

    def swap():
        a,b=actual
        coordinate_nielsen(0,False,False)
        emit({'op':'invert','i':1})
        coordinate_nielsen(1,False,False)
        conjugate(1,b)
        coordinate_nielsen(0,False,True)
        conjugate(0,inverse(a))
        assert actual==(b,a)

    for move in model_moves:
        if move['op']=='conjugate':
            conjugate(move['i'],substitute(move['g'],backward))
        else:
            emit(move)
    assert actual==tuple(backward)
    # Coordinate operations precompose; reverse the ambient derivation order.
    for op in ops[::-1]:
        if op[0]=='nielsen':
            coordinate_nielsen(*op[1:])
        elif op[0]=='swap':
            swap()
        elif op[0]=='invert':
            emit({'op':'invert','i':op[1]})
        else:
            q=substitute(op[1],actual)
            conjugate(0,q)
            conjugate(1,q)
    assert actual==('x','y')
    return {'format':'ordinary-ac-elementary-v1','start':parent['start'],
            'target':['x','y'],'moves':ledger,'primitive_waypoint':parent['target'],
            'primitive_coordinate':index,'waypoint_prefix_moves':len(parent['moves']),
            'ambient_aut_derivation':ops,'forward_images':forward,'inverse_images':backward,
            'scope':'Exact free-group AC certificate; no ambient automorphism is used as an unexpanded move'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('waypoint_certificate')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    result=complete(json.loads(Path(args.waypoint_certificate).read_text()))
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'strict_moves':len(result['moves']),
                      'waypoint_prefix':result['waypoint_prefix_moves'],'target':result['target']},indent=2))
