"""Certificate of primitive absence in a finite literal first-hump catalogue.

Each subgroup statement covers all word lengths. The finite catalogue and
literal representative scope are explicit; independent conjugating tails
and subsequent AC paths are not identified with these subgroups.
"""
import argparse
import base64
import gzip
import heapq
import json
from pathlib import Path
from stallings_search import graph,inverse,reduce

P='xxxYYYY';B='xyxYXY'
LETTERS='xXyY'


def orbit(word):
    return {w[k:]+w[:k] for w in (word,inverse(word)) for k in range(len(w))}


def pairs_from_catalogue(power,braid,rotate_frozen):
    pairs=set()
    for word in braid:
        pairs|={(fixed,recipient) for fixed in (orbit(P) if rotate_frozen else (P,))
                for recipient in orbit(word)}
    for word in power:
        pairs|={(recipient,fixed) for fixed in (orbit(B) if rotate_frozen else (B,))
                for recipient in orbit(word)}
    return sorted(pairs)


def line_graph(encoded,alphabet,blocked):
    vertices=len(encoded)//4
    edges=[(v,LETTERS[i],encoded[4*v+i]) for v in range(vertices) for i in range(4)
           if encoded[4*v+i]>=0 and LETTERS[i] in alphabet]
    adjacency=[[] for _ in edges]
    for i,e in enumerate(edges):
        for j,f in enumerate(edges):
            if e[2]==f[0] and not (e[1]==f[1]==blocked):
                adjacency[i].append(j)
    return adjacency


def topological_order(adjacency):
    indegree=[0]*len(adjacency)
    for row in adjacency:
        for j in row:indegree[j]+=1
    ready=[i for i,d in enumerate(indegree) if d==0]
    heapq.heapify(ready)
    order=[]
    while ready:
        i=heapq.heappop(ready);order.append(i)
        for j in adjacency[i]:
            indegree[j]-=1
            if indegree[j]==0:heapq.heappush(ready,j)
    assert len(order)==len(adjacency),'a potentially primitive signed cycle remains'
    return order


def dag_certificate(encoded):
    return {alphabet+'/'+blocked:topological_order(line_graph(encoded,alphabet,blocked))
            for alphabet in ('xy','xY','Xy','XY') for blocked in alphabet}


def verify_graph(encoded,orders):
    assert len(encoded)%4==0
    vertices=len(encoded)//4
    for v in range(vertices):
        for i in range(4):
            w=encoded[4*v+i]
            assert type(w) is int and -1<=w<vertices
            if w>=0:assert encoded[4*w+(i^1)]==v
    for alphabet in ('xy','xY','Xy','XY'):
        for blocked in alphabet:
            adjacency=line_graph(encoded,alphabet,blocked)
            order=orders[alphabet+'/'+blocked]
            assert sorted(order)==list(range(len(adjacency)))
            index={node:k for k,node in enumerate(order)}
            assert all(index[i]<index[j] for i,row in enumerate(adjacency) for j in row)


def construct(first_hump_result):
    source=json.loads(Path(first_hump_result).read_text())['enumeration']
    power=source['power9_in_braid']['cyclic_inverse_representatives']
    braid=source['braid8_in_torus']['cyclic_inverse_representatives']
    assert len(power)==24 and len(braid)==2
    for words,length in ((power,9),(braid,8)):
        assert len(set(words))==len(words)
        assert all(len(w)==length and reduce(w)==w and w[0]!=w[-1].swapcase() for w in words)
    original=pairs_from_catalogue(power,braid,False)
    expanded=pairs_from_catalogue(power,braid,True)
    assert len(original)==464 and len(expanded)==5632
    assert set(original)<=set(expanded)
    graphs=[];ids={}
    for pair in expanded:
        encoded,vertices=graph(pair)
        if encoded not in ids:
            ids[encoded]=len(graphs)
            graphs.append({'encoded_based_graph':list(encoded),'topological_orders':dag_certificate(encoded)})
    return {'format':'signed-double-free-cycle-DAG-certificate-v1',
            'scope':'Primitive absence in the listed literal subgroups at all word lengths; no global AC invariant',
            'root_catalogue_credit':'Root exact short-hump enumeration; M expanded frozen rotations and supplied signed-double DAG proof',
            'fixed_power':P,'fixed_braid':B,'power9_representatives':power,'braid8_representatives':braid,
            'original_fixed_literal_pairs':len(original),'expanded_literal_pairs':len(expanded),
            'unique_based_subgroup_graphs':len(graphs),'graphs':graphs}


def verify(cert):
    assert cert['format']=='signed-double-free-cycle-DAG-certificate-v1'
    assert cert['fixed_power']==P and cert['fixed_braid']==B
    power,braid=cert['power9_representatives'],cert['braid8_representatives']
    expected=pairs_from_catalogue(power,braid,True)
    assert len(expected)==cert['expanded_literal_pairs']==5632
    assert len(pairs_from_catalogue(power,braid,False))==cert['original_fixed_literal_pairs']==464
    assert len(cert['graphs'])==cert['unique_based_subgroup_graphs']==1340
    graph_index={tuple(row['encoded_based_graph']):i for i,row in enumerate(cert['graphs'])}
    assert len(graph_index)==len(cert['graphs'])
    for record in cert['graphs']:
        verify_graph(record['encoded_based_graph'],record['topological_orders'])
    used=set()
    for pair in expected:
        actual,vertices=graph(pair)
        assert actual in graph_index
        used.add(graph_index[actual])
    assert len(used)==len(cert['graphs'])
    branch=('xxxYYYY','xxyXXyXY')
    inverse_branch=('xxxYYYY','yxYxxYXX')
    assert inverse(branch[1])==inverse_branch[1]
    assert graph(branch)[0]==graph(inverse_branch)[0]
    return {'status':'PASS','original_literal_pairs':464,'expanded_literal_pairs':5632,
            'unique_based_subgroup_graphs':1340,'certified_acyclic_line_graphs':8*1340,
            'all_stored_graphs_refolded':True,'all_word_lengths_within_each_subgroup_covered':True,
            'independent_conjugating_tails_covered':False,'ordinary_AC_goal_solved':False}


def load(path):
    raw=Path(path).read_bytes()
    if str(path).endswith('.gz.b64'):raw=gzip.decompress(base64.b64decode(raw))
    return json.loads(raw)


def save(path,data):
    raw=(json.dumps(data,separators=(',',':'))+'\n').encode()
    if str(path).endswith('.gz.b64'):raw=base64.b64encode(gzip.compress(raw,mtime=0))+b'\n'
    Path(path).write_bytes(raw)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source')
    parser.add_argument('--certificate')
    parser.add_argument('--verify')
    parser.add_argument('--output')
    args=parser.parse_args()
    if args.verify:cert=load(args.verify)
    else:
        cert=construct(args.source)
        if args.certificate:save(args.certificate,cert)
    result=verify(cert)
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
