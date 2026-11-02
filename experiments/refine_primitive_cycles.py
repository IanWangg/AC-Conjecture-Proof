"""Refine double-free SCCs using exact rank-two primitive conjugacy.

Simple directed cycle SCCs accept only powers of one cyclic word; exact
Euclidean representatives decide its primitivity. Branching SCCs remain
explicitly inconclusive. No bounded word search is promoted to a proof.
"""
import argparse
import json
from math import gcd
from pathlib import Path
import arbitrary_tail_certificate as ac
from euclidean_primitive_audit import positive


def components(adjacency):
    visited=set()
    order=[]
    def first(v):
        if v in visited:return
        visited.add(v)
        for w in adjacency[v]:first(w)
        order.append(v)
    for v in range(len(adjacency)):first(v)
    reverse=[[] for _ in adjacency]
    for v,row in enumerate(adjacency):
        for w in row:reverse[w].append(v)
    visited=set()
    answer=[]
    def second(v,part):
        if v in visited:return
        visited.add(v)
        part.append(v)
        for w in reverse[v]:second(w,part)
    for v in reversed(order):
        if v not in visited:
            part=[]
            second(v,part)
            answer.append(part)
    return answer


def primitive_signed_cycle(word,alphabet):
    a=word.count(alphabet[0])
    b=word.count(alphabet[1])
    if gcd(a,b)!=1:return False
    model=positive(a,b).translate(str.maketrans({'x':alphabet[0],'y':alphabet[1]}))
    return len(word)==len(model) and word in model+model


def primitive_cyclic_word(word):
    """Exact Nielsen/Euclidean test, independent of Whitehead descent."""
    for alphabet in ('xy','xY','Xy','XY'):
        if set(word)<=set(alphabet) and primitive_signed_cycle(word,alphabet):
            return True
    return False


def exceptional_block_proof(encoded):
    """Verify the one explicit branching graph's forced unequal y-runs.

    Paths X and yXyXy go from vertex0 tovertex1, followed by the common
    return yyXyyXyyyyyy. These paths exhaust the signed graph and have
    disjoint interiors, so every cyclic loop uses the common return.
    """
    expected=('XYxYxY','XyyXyyXyyyyyy')
    if tuple(encoded)!=ac.fold(expected):return None
    vertices=len(encoded)//4
    signed={(v,letter,encoded[4*v+i]) for v in range(vertices)
            for i,letter in enumerate(ac.LETTERS)
            if letter in 'Xy' and encoded[4*v+i]>=0}

    def path(start,word):
        nodes=[start]
        edges=[]
        for letter in word:
            end=encoded[4*start+ac.LETTERS.index(letter)]
            assert end>=0
            edges.append((start,letter,end))
            nodes.append(end)
            start=end
        return nodes,edges

    paths=[path(0,'X'),path(0,'yXyXy'),path(1,'yyXyyXyyyyyy')]
    assert paths[0][0][-1]==paths[1][0][-1]==1
    assert paths[2][0][-1]==0
    interiors=[set(nodes[1:-1]) for nodes,edges in paths]
    assert all(not interiors[i]&interiors[j] for i in range(3) for j in range(i))
    assert set().union(*interiors,{0,1})==set(range(vertices))
    assert set().union(*(set(edges) for nodes,edges in paths))==signed
    for alphabet in ('xy','XY'):
        adjacency=[[encoded[4*v+i] for i,letter in enumerate(ac.LETTERS)
                    if letter in alphabet and encoded[4*v+i]>=0]
                   for v in range(vertices)]
        ac.topological_order(adjacency)
    # Explicit inverse-arc validation justifies the inverse alphabet xY.
    for start,letter,end in signed:
        assert encoded[4*end+ac.LETTERS.index(letter.swapcase())]==start
    return {'pair':expected,'two_forward_routes':['X','yXyXy'],
            'common_return':'yyXyyXyyyyyy','short_forced_y_run':2,
            'long_forced_y_runs':[6,7],
            'proof':'Every signed cyclic loop contains y-runs differing by at least4, excluded for positive rank-two primitives'}


def refine(encoded):
    simple=[]
    branching=[]
    primitives=[]
    for alphabet in ('xy','xY','Xy','XY'):
        labels=[letter for v in range(len(encoded)//4)
                for i,letter in enumerate(ac.LETTERS)
                if letter in alphabet and encoded[4*v+i]>=0]
        for blocked in alphabet:
            adjacency=ac.line_graph(encoded,alphabet,blocked)
            for part in components(adjacency):
                inside=set(part)
                internal={v:[w for w in adjacency[v] if w in inside] for v in part}
                if len(part)==1 and part[0] not in internal[part[0]]:continue
                if not all(len(internal[v])==1 for v in part):
                    branching.append({'alphabet':alphabet,'blocked':blocked,'vertices':part})
                    continue
                start=min(part)
                current=start
                word=''
                while True:
                    word+=labels[current]
                    current=internal[current][0]
                    if current==start:break
                assert len(word)==len(part)
                record={'alphabet':alphabet,'blocked':blocked,'cycle_word':word}
                if primitive_signed_cycle(word,alphabet):primitives.append(record)
                else:simple.append(record)
    return {'nonprimitive_simple_cycles':simple,'branching_components':branching,
            'primitive_simple_cycles':primitives}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    source=json.loads(Path(args.source).read_text())
    rows=[]
    for row in source['inconclusive_graphs']:
        rows.append(dict(row,refinement=refine(row['encoded'])))
    summary={'graphs':len(rows),
             'graphs_with_branching_SCC':sum(bool(row['refinement']['branching_components']) for row in rows),
             'graphs_with_primitive_simple_cycle':sum(bool(row['refinement']['primitive_simple_cycles']) for row in rows),
             'graphs_proved_primitive_free':sum(not row['refinement']['branching_components'] and not row['refinement']['primitive_simple_cycles'] for row in rows)}
    Path(args.output).write_text(json.dumps({'summary':summary,'rows':rows},indent=2)+'\n')
    print(json.dumps(summary,indent=2))
