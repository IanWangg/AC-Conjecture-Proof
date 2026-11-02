"""Exact controls for the arbitrary-tail-to-finite-bridge reduction.

Uses endpoint periodic-word overlaps, not the component generator.
The accompanying proof handles unbounded tails; these are exact controls.
"""
import argparse
import json
from pathlib import Path
from arbitrary_tail_catalogue import reduce,inverse,reduced_words


def cyclic(word):
    word=reduce(word)
    lo,hi=0,len(word)
    while hi-lo>1 and word[lo]==word[hi-1].swapcase():
        lo+=1
        hi-=1
    return word[lo:hi]


def orbit(word):
    return {w[i:]+w[:i] for w in (word,inverse(word)) for i in range(len(w))} or {''}


def key(word):
    return min(orbit(cyclic(word)))


def matched_axis_prefix(path,word):
    """Length of [1,path]'s initial segment contained in the word's axis."""
    best=0
    for direction in (word,inverse(word)):
        i=0
        while i<len(path) and path[i]==direction[i%len(direction)]:
            i+=1
        best=max(best,i)
    return best


def verify_example(u,v,q):
    assert u and v and cyclic(u)==u and cyclic(v)==v and reduce(q)==q
    left=matched_axis_prefix(q,u)
    right=matched_axis_prefix(inverse(q),v)
    distance=max(0,len(q)-left-right)
    p=q[:left]
    a=reduce(inverse(p)+u+p)
    assert len(a)==len(u) and a in orbit(u)
    actual=key(u+q+v+inverse(q))
    if distance:
        end=len(q)-right
        t=q[left:end]
        at_other=q[:end]
        b=reduce(inverse(at_other)+q+v+inverse(q)+at_other)
        assert len(b)==len(v) and b in orbit(v)
        reconstruction=a+t+b+inverse(t)
        assert cyclic(reconstruction)==reconstruction
        assert len(reconstruction)==len(u)+len(v)+2*distance
    else:
        t=''
        b=reduce(inverse(p)+q+v+inverse(q)+p)
        assert len(b)==len(v) and b in orbit(v)
        reconstruction=a+b
    assert key(reconstruction)==actual
    return distance


def run(bound):
    pairs=[('xxxYYYY','xyxYXY'),('yXYXyxx','YxYXyyx'),
           ('XXXYYxy','XXyxYY'),('x','y'),('xx','x'),
           ('xy','xy'),('xyXY','x'),('xxxY','xYY')]
    total=intersecting=disjoint=maximum=0
    for u,v in pairs:
        for q in reduced_words(bound):
            for a in (u,inverse(u)):
                for b in (v,inverse(v)):
                    d=verify_example(a,b,q)
                    total+=1
                    intersecting+=d==0
                    disjoint+=d>0
                    maximum=max(maximum,d)
    return {'status':'PASS','ordinary_AC_goal_solved':False,
            'tail_length_test_bound':bound,'control_pairs':len(pairs),
            'literal_signed_products_tested':total,
            'intersecting_axes_products':intersecting,
            'disjoint_axes_products':disjoint,
            'maximum_axis_distance_tested':maximum,
            'all_products_exactly_reconstructed_from_rotations_and_geodesic_bridges':True,
            'all_disjoint_cyclic_lengths_equal_sum_plus_twice_distance':True,
            'unbounded_completeness_depends_on_proof':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--tail-bound',type=int,default=6)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    result=run(args.tail_bound)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
