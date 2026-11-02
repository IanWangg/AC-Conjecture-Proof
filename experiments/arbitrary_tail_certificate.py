"""Finite signed-cycle certificate for every relative conjugating tail.

The finite graph check is combined with the shortest-double-coset/barbell
lemma proved in research-o.md. No finite tail bound is itself extrapolated.
Only Python's standard library is used; folding is implemented here rather
than imported from the earlier M code used during discovery.
"""
import argparse
import base64
from collections import deque
import gzip
import heapq
import json
from pathlib import Path

LETTERS='xXyY'
P='xxxYYYY'
B='xyxYXY'


def inverse(word):
    return word.swapcase()[::-1]


def freely_reduce(word):
    result=[]
    for letter in word:
        if result and result[-1]==letter.swapcase():result.pop()
        else:result.append(letter)
    return ''.join(result)


def reduced_words(bound):
    layer=['']
    yield ''
    for _ in range(bound):
        layer=[w+c for w in layer for c in LETTERS
               if not w or c!=w[-1].swapcase()]
        yield from layer


def fold(words):
    """Batch union-find folds of a bouquet; canonical base-first encoding."""
    arcs=[]
    size=1
    for word in words:
        at=0
        for position,letter in enumerate(word):
            end=0 if position==len(word)-1 else size
            if end:size+=1
            arcs.append((at,letter,end))
            arcs.append((end,letter.swapcase(),at))
            at=end
    parent=list(range(size))

    def find(v):
        while parent[v]!=v:
            parent[v]=parent[parent[v]]
            v=parent[v]
        return v

    while True:
        changed=False
        exits={}
        for start,letter,end in arcs:
            start,end=find(start),find(end)
            key=start,letter
            if key in exits:
                previous=find(exits[key])
                if previous!=end:
                    parent[max(previous,end)]=min(previous,end)
                    changed=True
            else:exits[key]=end
        if not changed:break
    transitions={}
    for start,letter,end in arcs:
        key=find(start),letter
        value=find(end)
        assert key not in transitions or transitions[key]==value
        transitions[key]=value
    names={find(0):0}
    queue=deque(names)
    encoding=[]
    while queue:
        start=queue.popleft()
        for letter in LETTERS:
            end=transitions.get((start,letter))
            if end is None:encoding.append(-1)
            else:
                if end not in names:
                    names[end]=len(names)
                    queue.append(end)
                encoding.append(names[end])
    return tuple(encoding)


def line_graph(encoded,alphabet,blocked):
    edges=[(start,letter,encoded[4*start+i])
           for start in range(len(encoded)//4)
           for i,letter in enumerate(LETTERS)
           if letter in alphabet and encoded[4*start+i]>=0]
    outgoing={}
    for index,(start,letter,end) in enumerate(edges):
        outgoing.setdefault(start,[]).append(index)
    return [[j for j in outgoing.get(end,[])
             if not (letter==edges[j][1]==blocked)]
            for start,letter,end in edges]


def topological_order(adjacency):
    indegrees=[0]*len(adjacency)
    for row in adjacency:
        for end in row:indegrees[end]+=1
    ready=[v for v,d in enumerate(indegrees) if d==0]
    heapq.heapify(ready)
    order=[]
    while ready:
        start=heapq.heappop(ready)
        order.append(start)
        for end in adjacency[start]:
            indegrees[end]-=1
            if not indegrees[end]:heapq.heappush(ready,end)
    assert len(order)==len(adjacency),'criterion inconclusive: a signed cycle remains'
    return order


def orders(encoded):
    return {alphabet+'/'+blocked:topological_order(line_graph(encoded,alphabet,blocked))
            for alphabet in ('xy','xY','Xy','XY') for blocked in alphabet}


def check_graph(encoded,proof):
    assert len(encoded)%4==0
    vertices=len(encoded)//4
    for start in range(vertices):
        for i in range(4):
            end=encoded[4*start+i]
            assert type(end) is int and -1<=end<vertices
            if end>=0:assert encoded[4*end+(i^1)]==start
    for alphabet in ('xy','xY','Xy','XY'):
        for blocked in alphabet:
            adjacency=line_graph(encoded,alphabet,blocked)
            order=proof[alphabet+'/'+blocked]
            assert sorted(order)==list(range(len(adjacency)))
            position={v:i for i,v in enumerate(order)}
            assert all(position[start]<position[end]
                       for start,row in enumerate(adjacency) for end in row)


def make():
    bound=len(P)//2+len(B)//2
    graphs={}
    for q in reduced_words(bound):
        encoded=fold((P,freely_reduce(q+B+inverse(q))))
        if encoded not in graphs:graphs[encoded]=orders(encoded)
    return {'format':'relative-conjugating-tail-primitive-exclusion-v1',
            'u':P,'v':B,'shortest_double_coset_bound':bound,
            'reduced_tails_checked':1+2*(3**bound-1),
            'graphs':[{'encoded':list(encoded),'orders':proof}
                      for encoded,proof in sorted(graphs.items())]}


def verify(certificate):
    assert certificate['format']=='relative-conjugating-tail-primitive-exclusion-v1'
    assert certificate['u']==P and certificate['v']==B
    bound=certificate['shortest_double_coset_bound']
    assert bound==len(P)//2+len(B)//2==6
    expected_count=1+2*(3**bound-1)
    assert certificate['reduced_tails_checked']==expected_count==1457
    saved={tuple(row['encoded']):row['orders'] for row in certificate['graphs']}
    assert len(saved)==len(certificate['graphs'])==1378
    for encoded,proof in saved.items():check_graph(encoded,proof)
    seen=set()
    count=0
    for q in reduced_words(bound):
        encoded=fold((P,freely_reduce(q+B+inverse(q))))
        assert encoded in saved
        seen.add(encoded)
        count+=1
    assert count==expected_count and seen==set(saved)
    # Each isolated cyclic factor must itself be nonprimitive for the
    # long-tail barbell case. Their single-cycle graphs meet the same test.
    for word in (P,B):orders(fold((word,)))
    # Positive control: a basis graph must fail this sufficient criterion.
    rejected=False
    try:orders(fold(('x','y')))
    except AssertionError:rejected=True
    assert rejected
    return {'status':'PASS','ordinary_AC_goal_solved':False,
            'theorem_scope':'<a p a^-1,c b c^-1> contains no primitive for every a,c in F2; no arbitrary interspersed Nielsen/AC moves',
            'finite_reduced_tails':count,'finite_unique_based_graphs':len(seen),
            'checked_acyclic_line_graphs':8*len(seen),
            'unbounded_extension':'shortest-double-coset/barbell lemma proved in research-o.md',
            'independent_folding_implementation':True,
            'long_tail_cycle_factors_checked':2,
            'basis_positive_control_rejected':True}


def save(path,value):
    raw=(json.dumps(value,separators=(',',':'))+'\n').encode()
    if str(path).endswith('.gz.b64'):
        raw=base64.b64encode(gzip.compress(raw,mtime=0))+b'\n'
    Path(path).write_bytes(raw)


def load(path):
    raw=Path(path).read_bytes()
    if str(path).endswith('.gz.b64'):raw=gzip.decompress(base64.b64decode(raw))
    return json.loads(raw)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--certificate')
    parser.add_argument('--verify')
    parser.add_argument('--output')
    args=parser.parse_args()
    certificate=load(args.verify) if args.verify else make()
    if args.certificate:save(args.certificate,certificate)
    result=verify(certificate)
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
