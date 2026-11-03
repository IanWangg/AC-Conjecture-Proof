"""Extract bridge-collapsed known-trivial anchors from verified reverse cores.

The core basis change is Nielsen, then one coordinate conjugation removes
the bridge. Any actual match still needs strict entry/basis/source ledgers.
"""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
for folder in (HERE,HERE.parent/'research_r',HERE.parent/'root'):
    sys.path.insert(0,str(folder))
from primitive_map_pairs import fold,inverse,reduce

LETTERS='xXyY'


def cyclic(w):
    w=reduce(w)
    while len(w)>1 and w[0]==w[-1].swapcase():w=w[1:-1]
    return w


def canon(w):
    w=cyclic(w)
    return min(v[i:]+v[:i] for v in (w,inverse(w)) for i in range(len(v)))


def key(pair):return tuple(sorted(map(canon,pair)))


def geometry(encoded):
    n=len(encoded)//4
    degree=[sum(v>=0 for v in encoded[4*i:4*i+4]) for i in range(n)]
    branches=[i for i,d in enumerate(degree) if d>=3]
    if len(branches)!=2 or any(degree[v]!=3 for v in branches):return None
    def path(start,letter):
        word='';at=start;c=letter
        while True:
            word+=LETTERS[c];end=encoded[4*at+c]
            assert end>=0
            if degree[end]!=2:return end,word
            choices=[j for j,v in enumerate(encoded[4*end:4*end+4]) if v>=0 and j!=(c^1)]
            assert len(choices)==1
            at,c=end,choices[0]
    a,b=branches
    aa=[path(a,c) for c in range(4) if encoded[4*a+c]>=0]
    bb=[path(b,c) for c in range(4) if encoded[4*b+c]>=0]
    loops_a=[w for end,w in aa if end==a]
    loops_b=[w for end,w in bb if end==b]
    bridge=[w for end,w in aa if end==b]
    if len(loops_a)!=2 or len(loops_b)!=2 or len(bridge)!=1:return None
    assert loops_a[0]==inverse(loops_a[1]) and loops_b[0]==inverse(loops_b[1])
    u,v,q=min(loops_a),min(loops_b),bridge[0]
    assert u and v and q
    return dict(branch_base=a,other_branch=b,cycle_pair=[u,v],bridge=q,
                uncollapsed_basis=[u,reduce(q+v+inverse(q))])


def run(sources,reverse_paths):
    source_bytes=Path(sources).read_bytes()
    source_rows=[json.loads(line) for line in source_bytes.splitlines() if line.strip()]
    source_map={key(row['cyclic_basis']):row for row in source_rows}
    anchors={};matches=[];rows=barbells=0
    for corpus,path in enumerate(reverse_paths):
        for index,line in enumerate(Path(path).read_text().splitlines()):
            pair=line.split('\t');assert len(pair)==2;rows+=1
            encoded=fold(pair);description=geometry(encoded)
            if description is None:continue
            barbells+=1;anchor_key=key(description['cycle_pair'])
            record=dict(reverse_corpus=corpus,reverse_index=index,reverse_pair=pair,
                        graph=list(encoded),**description)
            anchors.setdefault(anchor_key,record)
            if anchor_key in source_map:
                matches.append(dict(source=source_map[anchor_key],reverse=record))
    return dict(status='MATCH' if matches else 'COMPLETE_NO_MATCH',ordinary_AC_goal_solved=False,
                input_reverse_rows=rows,barbell_reverse_rows=barbells,
                distinct_collapsed_cycle_families=len(anchors),
                compared_initial_Nielsen_families=len(source_map),
                source_jsonl_sha256=hashlib.sha256(source_bytes).hexdigest(),
                matches=matches,anchors=list(anchors.values()))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('sources');parser.add_argument('reverse',nargs='+');parser.add_argument('--output',required=True)
    args=parser.parse_args();result=run(args.sources,args.reverse)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('matches','anchors')},indent=2))
    if result['matches']:print(json.dumps(result['matches'][0],indent=2))
