"""Exact finite vertex-identification overgroups and rank-three characters.

This is an exploratory overgroup reduction, not an AC invariant. In rank
three the character kills the original H0 and sends its extra generator
to one. Rank-dropping folds are reported explicitly.
"""
import argparse,json,sys
from collections import deque
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'research_r'))
from primitive_map_pairs import fold,follow,inverse,reduce,LETTERS,validate_graph

def fold_identification(encoded,first,second):
    n=len(encoded)//4;parent=list(range(n))
    def root(v):
        while parent[v]!=v:parent[v]=parent[parent[v]];v=parent[v]
        return v
    parent[max(first,second)]=min(first,second)
    while True:
        changed=False;out={}
        for a in range(n):
            for c,b in enumerate(encoded[4*a:4*a+4]):
                if b<0:continue
                x,y=root(a),root(b)
                if (x,c) in out and root(out[x,c])!=y:
                    z=root(out[x,c]);parent[max(y,z)]=min(y,z);changed=True
                else:out[x,c]=y
        if not changed:break
    arcs={(root(a),c):root(b) for a in range(n)
          for c,b in enumerate(encoded[4*a:4*a+4]) if b>=0}
    names={root(0):0};queue=deque([root(0)]);result=[]
    while queue:
        a=queue.popleft()
        for c in range(4):
            b=arcs.get((a,c),-1)
            if b>=0 and b not in names:names[b]=len(names);queue.append(b)
            result.append(names[b] if b>=0 else -1)
    validate_graph(result)
    return tuple(result),[names[root(a)] for a in range(n)]

def spanning(encoded,base=0):
    def edge_key(a,c,b):return min((a,c,b),(b,c^1,a))
    paths={base:''};tree=set();queue=deque([base])
    while queue:
        a=queue.popleft()
        for c,b in enumerate(encoded[4*a:4*a+4]):
            if b>=0 and b not in paths:
                paths[b]=paths[a]+LETTERS[c];tree.add(edge_key(a,c,b));queue.append(b)
    edges={edge_key(a,c,b) for a in range(len(encoded)//4)
           for c,b in enumerate(encoded[4*a:4*a+4]) if b>=0}
    extra=sorted(edges-tree);arc={}
    for i,(a,c,b) in enumerate(extra):arc[a,c,b]=(i,1);arc[b,c^1,a]=(i,-1)
    def coordinates(word,start=base):
        at=start;result=[0]*len(extra)
        for c in word:
            letter=LETTERS.index(c);end=encoded[4*at+letter]
            assert end>=0
            if (at,letter,end) in arc:
                i,s=arc[at,letter,end];result[i]+=s
            at=end
        assert at==start
        return result
    return paths,extra,arc,coordinates

def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def dot(a,b):return sum(x*y for x,y in zip(a,b))

def positive_primitive_words(cap):
    if cap<1:return
    pending=[('x','y')]
    seen=set()
    while pending:
        a,b=pending.pop()
        for w in (a,b):
            if w not in seen:seen.add(w);yield w
        if len(a)+len(b)<=cap:
            pending.extend(((a,a+b),(a+b,b)))

def word_voltage(encoded,voltages,word,start):
    at=start;value=0
    for letter in word:
        c=LETTERS.index(letter);end=encoded[4*at+c]
        if end<0:return None
        value+=voltages[4*at+c];at=end
    return value if at==start else None

def kernel_primitive(encoded,voltages,words):
    for positive in words:
        for alphabet in ('xy','xY','Xy','XY'):
            word=positive.translate(str.maketrans('xy',alphabet))
            for base in range(len(encoded)//4):
                if word_voltage(encoded,voltages,word,base)==0:
                    return dict(cyclic_word=word,loop_vertex=base,
                                based_word=None,voltage=0)
    return None

def analyze(cap,n=3):
    assert n>=2 and cap>=0
    initial=('x'*n+'Y'*(n+1),'xyxYXY')
    original=fold(initial);paths,_,_,_=spanning(original)
    words=sorted(positive_primitive_words(cap),key=lambda w:(len(w),w))
    records=[]
    for a in range(len(original)//4):
        for b in range(a+1,len(original)//4):
            graph,projection=fold_identification(original,a,b)
            routes,extra,arc,coords=spanning(graph);rank=len(extra)
            record=dict(identified_vertices=[a,b],graph=list(graph),rank=rank,
                        vertex_projection=projection)
            assert rank in (2,3)
            assert all(follow(graph,0,w)==0 for w in initial)
            if rank==3:
                p,q=map(coords,initial)
                t=reduce(paths[a]+inverse(paths[b]));r=coords(t)
                character=cross(p,q);det=dot(character,r);assert abs(det)==1
                character=[x//det for x in character]
                voltages=[0]*len(graph)
                for (x,c,y),(i,s) in arc.items():voltages[4*x+c]=s*character[i]
                assert all(word_voltage(graph,voltages,w,0)==0 for w in initial)
                assert word_voltage(graph,voltages,t,0)==1
                witness=kernel_primitive(graph,voltages,words)
                if witness:
                    s=routes[witness['loop_vertex']]
                    witness['based_word']=reduce(s+witness['cyclic_word']+inverse(s))
                    assert word_voltage(graph,voltages,witness['based_word'],0)==0
                record.update(extra_generator=t,tree_chord_character=character,
                              edge_voltages=voltages,kernel_primitive_witness=witness)
            records.append(record)
    return dict(status='COMPLETE_VERTEX_IDENTIFICATION_CLASSIFICATION',ordinary_AC_goal_solved=False,
                AK_parameter=n,original_pair=list(initial),original_graph=list(original),
                distinct_vertex_pairs=len(records),rank2_pairs=sum(r['rank']==2 for r in records),
                rank3_pairs=sum(r['rank']==3 for r in records),
                rank3_kernels_with_explicit_primitive=sum(bool(r.get('kernel_primitive_witness')) for r in records),
                primitive_candidate_length_cap=cap,positive_primitive_words_tested=len(words),
                scope='All vertex identifications; primitive search is bounded and only explicit positive witnesses are conclusive.',
                records=records)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--cap',type=int,default=100);parser.add_argument('--n',type=int,default=3);parser.add_argument('--output',required=True)
    args=parser.parse_args();result=analyze(args.cap,args.n)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','original_graph')},indent=2))
