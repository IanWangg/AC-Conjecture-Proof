"""Sufficient unbounded primitive exclusion by consecutive run lengths.

If a positive primitive has isolated a's, every intervening b-run has
length k or k+1 for a single k. Finite b-paths give a finite weighted
a-edge graph. Acyclicity for each possible k excludes every such word.
If an infinite b-path is encountered the test remains inconclusive.
"""
import arbitrary_tail_certificate as ac
from euclidean_primitive_audit import positive
from math import gcd


def make(encoded,alphabet,isolated):
    other=next(letter for letter in alphabet if letter!=isolated)
    ia=ac.LETTERS.index(isolated)
    ib=ac.LETTERS.index(other)
    vertices=len(encoded)//4
    # Single-generator primitive loops are outside the positive two-letter
    # run argument, so reject them explicitly.
    if any(encoded[4*v+i]==v for v in range(vertices) for i in (ia,ib)):
        return None
    edges=[(v,encoded[4*v+ia]) for v in range(vertices) if encoded[4*v+ia]>=0]
    origins={start:i for i,(start,end) in enumerate(edges)}
    transitions=[]
    for i,(start,end) in enumerate(edges):
        at=end
        visited={at}
        for length in range(1,vertices+1):
            at=encoded[4*at+ib]
            if at<0:break
            if at in origins:transitions.append((i,origins[at],length))
            if at in visited:return None
            visited.add(at)
        else:return None
    maximum=max((length for i,j,length in transitions),default=0)
    orders={}
    for k in range(1,maximum+1):
        adjacency=[[] for _ in edges]
        for i,j,length in transitions:
            if length in (k,k+1):adjacency[i].append(j)
        try:orders[str(k)]=ac.topological_order(adjacency)
        except AssertionError:return None
    return {'alphabet':alphabet,'isolated_letter':isolated,
            'a_edges':[list(edge) for edge in edges],
            'weighted_transitions':[list(t) for t in transitions],
            'topological_orders_for_k':orders,
            'maximum_recorded_run':maximum}


def verify(encoded,certificate):
    recomputed=make(encoded,certificate['alphabet'],certificate['isolated_letter'])
    assert recomputed is not None and recomputed==certificate
    return True


def positive_controls():
    count=0
    for a in range(1,13):
        for b in range(1,13):
            if gcd(a,b)!=1:continue
            word=positive(a,b)
            isolated='x' if a<=b else 'y'
            for alphabet in ('xy','xY','Xy','XY'):
                table=str.maketrans({'x':alphabet[0],'y':alphabet[1]})
                encoded=ac.fold((word.translate(table),))
                chosen=isolated.translate(table)
                assert make(encoded,alphabet,chosen) is None
                count+=1
    return count
