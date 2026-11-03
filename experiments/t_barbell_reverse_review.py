"""Independent edge-bridge audit of V's known-trivial collapsed anchors.

Uses R's fold, but recognizes barbells by deleting every undirected edge
and testing connectivity, not by V's branch-to-branch path classifier.
"""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
from primitive_map_pairs import fold
from nielsen_basis_classes import canonical,enumerate_classes

LETTERS='xXyY'


def collapsed(encoded):
    n=len(encoded)//4
    arcs=[[(c,encoded[4*v+c]) for c in range(4) if encoded[4*v+c]>=0] for v in range(n)]
    assert all(len(a)>=2 for a in arcs)
    edges=[];arc_edge={}
    for v in range(n):
        for c,w in arcs[v]:
            if (v,c) in arc_edge:continue
            k=len(edges);edges.append((v,w));arc_edge[v,c]=arc_edge[w,c^1]=k
    assert len(edges)-n+1==2
    bridges=set()
    for blocked,(start,target) in enumerate(edges):
        reached={start};queue=deque([start])
        while queue:
            v=queue.popleft()
            for c,w in arcs[v]:
                if arc_edge[v,c]!=blocked and w not in reached:
                    reached.add(w);queue.append(w)
        if target not in reached:bridges.add(blocked)
    if not bridges:return None
    remaining=set(range(n));cycles=[]
    while remaining:
        start=min(remaining);component={start};queue=deque([start]);remaining.remove(start)
        while queue:
            v=queue.popleft()
            for c,w in arcs[v]:
                if arc_edge[v,c] not in bridges and w in remaining:
                    remaining.remove(w);component.add(w);queue.append(w)
        internal=[(v,c,w) for v in component for c,w in arcs[v] if arc_edge[v,c] not in bridges]
        if not internal:continue
        assert all(sum(arc_edge[v,c] not in bridges for c,w in arcs[v])==2 for v in component)
        attachment=[v for v in component if any(arc_edge[v,c] in bridges for c,w in arcs[v])]
        assert len(attachment)==1
        start=at=attachment[0];previous=-1;word=''
        while True:
            choices=[(c,w) for c,w in arcs[at] if arc_edge[at,c] not in bridges and c!=previous]
            assert choices
            c,w=min(choices);word+=LETTERS[c];at=w;previous=c^1
            if at==start:break
            assert len(word)<=n+1
        cycles.append(canonical(word))
    assert len(cycles)==2
    return tuple(sorted(cycles))


def run(paths,v_result):
    rows=barbells=0;anchors=set();hashes=[]
    for path in paths:
        raw=Path(path).read_bytes();hashes.append(hashlib.sha256(raw).hexdigest())
        for line in raw.decode().splitlines():
            if not line.strip():continue
            pair=line.split('\t');assert len(pair)==2;rows+=1
            key=collapsed(fold(pair))
            if key is None:continue
            barbells+=1;anchors.add(key)
    expected=json.loads(Path(v_result).read_text())
    vkeys={tuple(sorted(canonical(w) for w in row['cycle_pair'])) for row in expected['anchors']}
    assert anchors==vkeys
    assert barbells==expected['barbell_reverse_rows']
    matrix,enumeration=enumerate_classes(3,40)
    assert not anchors.intersection(matrix)
    return dict(status='PASS',ordinary_AC_goal_solved=False,input_reverse_rows=rows,
                reverse_tsv_sha256=hashes,independently_detected_barbell_rows=barbells,
                distinct_collapsed_cycle_families=len(anchors),
                maximum_collapsed_cycle_energy=max(map(lambda p:sum(map(len,p)),anchors)),
                exact_anchor_keys_equal_V=True,
                matched_initial_H_cap40_matrix_classes=0,
                classification='Independent per-edge connectivity deletion; R batch folding reused',
                scope='Finite specified reverse corpora only; no unrestricted AC invariant')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('reverse',nargs='+')
    parser.add_argument('--v-result',required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args();result=run(args.reverse,args.v_result)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
