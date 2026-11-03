"""T's independent H1 theorem-instance audit, using T's own review helpers.

No V/X modules are imported. Initial fold is reconstructed from the
literal geometric basis; every quotient, character pullback and signed
SCC potential is checked exactly. No bounded primitive enumeration used.
"""
import argparse
from collections import deque
from itertools import combinations
import hashlib
import json
from pathlib import Path
try:
    from t_x_review_cells import LETTERS,inverse,reduce,validate,quotient,value,potentials
except ModuleNotFoundError:
    from x_review_cells import LETTERS,inverse,reduce,validate,quotient,value,potentials
from nielsen_basis_classes import read_payload


def fold_words(words):
    edges=[];size=1
    for word in words:
        at=0
        for i,letter in enumerate(word):
            w=0 if i+1==len(word) else size
            if w:size+=1
            c=LETTERS.index(letter);edges.extend(((at,c,w),(w,c^1,at)));at=w
    parent=list(range(size))
    def root(v):
        while parent[v]!=v:v=parent[v]
        return v
    while True:
        changed=False;seen={}
        for v,c,w in edges:
            a,b=root(v),root(w);key=a,c
            if key in seen and root(seen[key])!=b:
                other=root(seen[key]);parent[max(other,b)]=min(other,b);changed=True
            else:seen[key]=b
        if not changed:break
    arcs={(root(v),c):root(w) for v,c,w in edges};names={root(0):0};queue=deque([root(0)]);graph=[]
    while queue:
        v=queue.popleft()
        for c in range(4):
            w=arcs.get((v,c),-1)
            if w>=0 and w not in names:names[w]=len(names);queue.append(w)
            graph.append(names[w] if w>=0 else -1)
    return graph


def audit_instance(data,weighted):
    pair=data['original_pair'];graph=fold_words(pair)
    assert graph==data['original_graph'] and validate(graph)==2
    routes={0:''};queue=deque([0])
    while queue:
        v=queue.popleft()
        for c in range(4):
            w=graph[4*v+c]
            if w>=0 and w not in routes:routes[w]=routes[v]+LETTERS[c];queue.append(w)
    weights={tuple(r['identified_vertices']):r for r in weighted['results']}
    expected=set(combinations(range(len(graph)//4),2));assert len(weights)==len(weighted['results'])==len(expected)
    seen=set();inequalities=pullbacks=components=0
    for row in data['records']:
        a,b=row['identified_vertices'];key=a,b;assert key not in seen;seen.add(key)
        new,projection=quotient(graph,a,b);assert new==row['graph'] and projection==row['vertex_projection'] and validate(new)==3
        voltage=row['edge_voltages'];assert len(voltage)==len(new)
        for v in range(len(new)//4):
            for c in range(4):
                if (w:=new[4*v+c])>=0:assert voltage[4*v+c]==-voltage[4*w+(c^1)]
        extra=reduce(routes[a]+inverse(routes[b]));assert extra==row['extra_generator']
        assert [value(new,voltage,w) for w in pair]==[0,0] and value(new,voltage,extra)==1
        f={0:0};queue=deque([0])
        while queue:
            v=queue.popleft()
            for c in range(4):
                w=graph[4*v+c]
                if w>=0 and w not in f:f[w]=f[v]+voltage[4*projection[v]+c];queue.append(w)
        for v in range(len(graph)//4):
            for c in range(4):
                w=graph[4*v+c]
                if w>=0:assert f[w]-f[v]==voltage[4*projection[v]+c];pullbacks+=1
        certificate=weights[key];inequalities+=potentials(new,voltage,certificate)
        components+=sum(len(check['cyclic_components']) for check in certificate['checks'])
    assert seen==expected
    return dict(complete_vertex_identifications=len(seen),signed_double_free_automata=8*len(seen),
                cyclic_SCCs=components,integer_potential_inequalities=inequalities,
                directed_pullback_equalities=pullbacks,original_graph_vertices=len(graph)//4)


def run(paths):
    raw=[read_payload(path) for path in paths]
    if len(paths)==1:
        source=json.loads(raw[0]);selected=[row for row in source['records'] if row['rotation_offsets']==[0,4]]
        assert len(selected)==1
        data=selected[0]['identification_data'];weighted=selected[0]['cycle_certificates']
        assert data['original_pair']==['xxxYYYY','XYxyxY']
        data=dict(data,original_pair=['yXYXyx','yyyyXXX'])
    else:
        assert len(paths)==2;data,weighted=[json.loads(r) for r in raw]
    p='xxxYYYY';b='xyxYXY';rotated='XYxyxY';geometric=['yXYXyx','yyyyXXX']
    assert geometric==[inverse(rotated),inverse(p)] and data['original_pair']==geometric
    P,Q,R='y','XYxyx','xxxYYY'
    assert [reduce(P+inverse(Q)),reduce(P+inverse(R))]==geometric
    assert len({w[0] for w in (P,Q,R)})==3 and len({inverse(w)[0] for w in (P,Q,R)})==3
    state=[p,b];moves=[]
    for g in ('Y','X'):
        state[1]=reduce(g+state[1]+inverse(g));moves.append(dict(op='conjugate',i=1,g=g))
    assert state==[p,rotated]
    prefix=dict(format='ordinary-ac-elementary-v1',start=[p,b],target=state,moves=moves)
    checked=audit_instance(data,weighted);assert checked['original_graph_vertices']==11
    return dict(status='PASS',ordinary_AC_goal_solved=False,actual_source_pair=[p,rotated],
                geometric_basis=geometric,theta_path_lengths=[len(P),len(Q),len(R)],
                strict_AK3_entry=prefix,**checked,
                input_sha256=[hashlib.sha256(r).hexdigest() for r in raw],
                independence='No V/X imports; T literal fold, quotient, coboundary and Tarjan/potential audit',
                scope='One specified reachable H1 and its arbitrary two-conjugate family; not every successor or unrestricted AC path')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('inputs',nargs='+');parser.add_argument('--output',required=True);args=parser.parse_args()
    result=run(args.inputs);Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
