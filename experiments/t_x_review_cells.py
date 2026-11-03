"""T's second-phase audit using exact parameter sign cells.

No V/X modules are imported. Quotients use deterministic union folding;
SCCs use Tarjan; affine infeasibility tests each real sign cell rather
than constructing/intersecting sign intervals. Primitivity uses T's
previous signed Euclidean representative, not X's mechanical word code.
"""
import argparse
from collections import Counter,deque
from fractions import Fraction as F
from itertools import combinations
import hashlib
import json
from pathlib import Path
from nielsen_basis_classes import representative,canonical,read_payload

LETTERS='xXyY'


def inverse(w):return w.swapcase()[::-1]


def reduce(w):
    s=[]
    for c in w:
        if s and s[-1]==c.swapcase():s.pop()
        else:s.append(c)
    return ''.join(s)


def validate(graph):
    n=len(graph)//4;assert n and len(graph)==4*n
    for v in range(n):
        for c in range(4):
            w=graph[4*v+c];assert -1<=w<n
            if w>=0:assert graph[4*w+(c^1)]==v
    seen={0};queue=deque([0])
    while queue:
        v=queue.popleft()
        for w in graph[4*v:4*v+4]:
            if w>=0 and w not in seen:seen.add(w);queue.append(w)
    assert len(seen)==n
    return sum(w>=0 for w in graph)//2-n+1


def quotient(old,a,b):
    n=len(old)//4;parent=list(range(n))
    def root(x):
        while parent[x]!=x:x=parent[x]
        return x
    def join(x,y):
        x,y=root(x),root(y)
        if x==y:return False
        parent[max(x,y)]=min(x,y);return True
    join(a,b)
    while True:
        grouped={};changed=False
        for v in range(n):
            for c in range(4):
                w=old[4*v+c]
                if w<0:continue
                key=(root(v),c)
                if key in grouped:changed=join(grouped[key],w) or changed
                else:grouped[key]=w
        if not changed:break
    arcs={(root(v),c):root(w) for v in range(n) for c in range(4) if (w:=old[4*v+c])>=0}
    names={root(0):0};queue=deque([root(0)]);answer=[]
    while queue:
        v=queue.popleft()
        for c in range(4):
            w=arcs.get((v,c),-1)
            if w>=0 and w not in names:names[w]=len(names);queue.append(w)
            answer.append(names[w] if w>=0 else -1)
    return answer,[names[root(v)] for v in range(n)]


def cohomology(graph):
    edge=lambda v,c,w:min((v,c,w),(w,c^1,v))
    paths={0:''};tree=set();queue=deque([0])
    while queue:
        v=queue.popleft()
        for c in range(4):
            w=graph[4*v+c]
            if w>=0 and w not in paths:
                paths[w]=paths[v]+LETTERS[c];tree.add(edge(v,c,w));queue.append(w)
    edges={edge(v,c,w) for v in range(len(graph)//4) for c in range(4) if (w:=graph[4*v+c])>=0}
    chords=sorted(edges-tree);indices={}
    for i,(v,c,w) in enumerate(chords):indices[4*v+c]=(i,1);indices[4*w+(c^1)]=(i,-1)
    basis=[reduce(paths[v]+LETTERS[c]+inverse(paths[w])) for v,c,w in chords]
    def coefficients(word):
        answer=[0]*len(chords);at=0
        for letter in word:
            index=4*at+LETTERS.index(letter);at=graph[index];assert at>=0
            if index in indices:i,s=indices[index];answer[i]+=s
        assert at==0
        return answer
    def voltages(character):
        assert len(character)==len(chords)
        answer=[F(0)]*len(graph)
        for j,(i,s) in indices.items():answer[j]=s*character[i]
        return answer
    return basis,coefficients,voltages,len(chords)


def value(graph,voltage,word,base=0):
    at=base;total=F(0)
    for letter in word:
        index=4*at+LETTERS.index(letter);at=graph[index];assert at>=0;total+=voltage[index]
    assert at==base
    return total


def rank3(matrix):
    def det(c):
        a,b,d=([r[j] for j in c] for r in matrix)
        return a[0]*(b[1]*d[2]-b[2]*d[1])-a[1]*(b[0]*d[2]-b[2]*d[0])+a[2]*(b[0]*d[1]-b[1]*d[0])
    return any(det(c) for c in combinations(range(len(matrix[0])),3))


def automaton(graph,alphabet,blocked):
    assert tuple(alphabet) in ((0,2),(0,3),(1,2),(1,3)) and blocked in (0,1)
    states=[2*v+i for v in range(len(graph)//4) for i,c in enumerate(alphabet) if graph[4*v+c]>=0]
    outgoing={s:[] for s in states};arcs=[]
    for state in states:
        v,i=divmod(state,2);edge=4*v+alphabet[i];w=graph[edge]
        for j,c in enumerate(alphabet):
            if i==j==blocked:continue
            if graph[4*w+c]>=0:arcs.append((state,2*w+j,edge));outgoing[state].append(2*w+j)
    index={};low={};stack=[];onstack=set();groups=[]
    def visit(v):
        index[v]=low[v]=len(index);stack.append(v);onstack.add(v)
        for w in outgoing[v]:
            if w not in index:visit(w);low[v]=min(low[v],low[w])
            elif w in onstack:low[v]=min(low[v],index[w])
        if low[v]==index[v]:
            group=set()
            while True:
                w=stack.pop();onstack.remove(w);group.add(w)
                if w==v:break
            groups.append(frozenset(group))
    for v in states:
        if v not in index:visit(v)
    cyclic={g for g in groups if len(g)>1 or any(a==b and a in g for a,b,_ in arcs)}
    return arcs,cyclic


def potentials(graph,voltage,certificate):
    assert certificate['status']=='PASS';seen=set();inequalities=0
    for check in certificate['checks']:
        alphabet=tuple(check['alphabet']);blocked=check['forbidden_double'];key=alphabet,blocked
        assert key not in seen;seen.add(key);arcs,cyclic=automaton(graph,alphabet,blocked)
        saved=check['cyclic_components'];assert {frozenset(c['states']) for c in saved}==cyclic and len(saved)==len(cyclic)
        for component in saved:
            group=component['states'];q=dict(zip(group,component['potential']));assert len(q)==len(group)==len(component['potential'])
            sign=component['strict_cycle_voltage_sign'];assert sign in (-1,1)
            for u,v,edge in arcs:
                if u in q and v in q:
                    assert q[v]-q[u]<=len(group)*sign*voltage[edge]-1;inequalities+=1
    assert len(seen)==8
    return inequalities


def sign_cells(graph,p,q,entry):
    constraints=[];actual_cycles=0
    for check in entry['cycle_checks']:
        arcs,cyclic=automaton(graph,tuple(check['alphabet']),check['forbidden_double'])
        group=frozenset(check['states']);assert group in cyclic
        indices={(a,b):edge for a,b,edge in arcs};pairs=[]
        for witness in check['cycle_witnesses']:
            path=witness['states'];assert path and len(path)==len(set(path)) and set(path)<=group
            aa=bb=F(0)
            for u,v in zip(path,path[1:]+path[:1]):
                edge=indices[u,v];aa+=p[edge];bb+=q[edge]
            assert [str(aa),str(bb)]==witness['coefficients'];pairs.append((aa,bb));actual_cycles+=1
        assert pairs;constraints.append(pairs)
    roots=sorted({-b/a for pairs in constraints for a,b in pairs if a})
    if roots:
        samples=roots+[roots[0]-1,roots[-1]+1]+[(a+b)/2 for a,b in zip(roots,roots[1:])]
    else:samples=[F(0)]
    for parameter in samples:
        possible=all(all(a*parameter+b>0 for a,b in pairs) or all(a*parameter+b<0 for a,b in pairs) for pairs in constraints)
        assert not possible,('feasible sign cell',entry['second_identification_index'],str(parameter))
    return actual_cycles,len(samples),len(roots)


def run(paths):
    containers=[read_payload(path) for path in paths]
    if len(paths)==2:
        bundle=json.loads(containers[1]);keys=('extensions','affine_parameters','dual_obstructions','uniform_primitives')
        raw=[containers[0]]+[(json.dumps(bundle[key])+'\n').encode() for key in keys]
    else:
        assert len(paths)==5;raw=containers
    original,data,intervals,duals,primitives=[json.loads(r) for r in raw]
    affine={r['second_identification_index']:r for r in intervals['records']};dual={r['second_identification_index']:r['dual_integer_row'] for r in duals['records']}
    positive={r['second_identification_index']:r['witness'] for r in primitives['records'] if r['witness']}
    assert len(affine)==len(intervals['records']) and len(dual)==len(duals['records'])
    expected={(i,a,b) for i,parent in enumerate(original['records']) for a,b in combinations(range(len(parent['graph'])//4),2)}
    seen=set();counts=Counter();inequalities=cycles=samples=roots=primitive_count=0;dimensions=Counter();failure_ranks=Counter()
    for i,row in enumerate(data['records']):
        parent_index=row['first_case_index'];parent=original['records'][parent_index];old=parent['graph'];a,b=row['second_vertices'];key=parent_index,a,b
        assert key in expected and key not in seen;seen.add(key)
        graph,projection=quotient(old,a,b);assert graph==row['graph'] and projection==row['vertex_projection']
        r=validate(graph);basis,_,_,oldrank=cohomology(old);_,coords,volts,newrank=cohomology(graph)
        assert oldrank==3 and r==newrank==row['rank'] and basis==row['old_basis_words']
        matrix=[coords(w) for w in basis];rhs=[value(old,parent['edge_voltages'],w) for w in basis]
        assert matrix==row['coordinate_rows'] and rhs==list(map(F,row['old_character']))
        if i in dual:
            u=dual[i];assert len(u)==3 and any(u)
            assert all(sum(u[k]*matrix[k][j] for k in range(3))==0 for j in range(r))
            assert sum(u[k]*rhs[k] for k in range(3))!=0
            assert i not in affine;counts['NO_CHARACTER_EXTENSION']+=1;failure_ranks[r]+=1;continue
        assert rank3(matrix)
        base=list(map(F,row['rational_particular']));directions=[list(map(F,d)) for d in row['rational_directions']]
        assert len(base)==r and len(directions)==r-3==row['extension_free_dimension']
        assert all(len(d)==r for d in directions)
        assert all(sum(x*y for x,y in zip(m,base))==target for m,target in zip(matrix,rhs))
        assert all(any(d) and all(sum(x*y for x,y in zip(m,d))==0 for m in matrix) for d in directions)
        dimensions[r-3]+=1
        if i in affine:
            assert r==4 and len(directions)==1
            entry=affine[i]
            if entry['status']=='STRICT_CYCLE_FAMILY_INFEASIBLE':
                p,q=volts(directions[0]),volts(base);c,s,t=sign_cells(graph,p,q,entry);cycles+=c;samples+=s;roots+=t
                counts['AFFINE_STRICT_CYCLE_FAMILY_INFEASIBLE']+=1
                if i in positive:
                    witness=positive[i];word=witness['cyclic_word'];vertex=witness['loop_vertex']
                    ax=word.count('x')-word.count('X');by=word.count('y')-word.count('Y')
                    euclidean=representative(ax,by).translate(str.maketrans('aAbB','xXyY'))
                    assert canonical(word)==canonical(euclidean)
                    assert value(graph,p,word,vertex)==value(graph,q,word,vertex)==0
                    at=0
                    for c in witness['base_path']:at=graph[4*at+LETTERS.index(c)];assert at>=0
                    assert at==vertex and reduce(witness['base_path']+word+inverse(witness['base_path']))==witness['based_word']
                    assert value(graph,p,witness['based_word'])==value(graph,q,witness['based_word'])==0;primitive_count+=1
                continue
            assert entry['status']=='STRICT_CYCLE_FAMILY_FEASIBLE';certificate=entry
        else:
            assert r==3 and not directions;certificate=row['certificate']
        voltage=certificate['edge_voltages'];assert len(voltage)==len(graph)
        for v in range(len(graph)//4):
            for c in range(4):
                if (w:=graph[4*v+c])>=0:assert voltage[4*v+c]==-voltage[4*w+(c^1)]
        pulled=[value(graph,voltage,w) for w in basis]
        ratios={x/y for x,y in zip(pulled,rhs) if y};assert len(ratios)==1 and (scale:=next(iter(ratios)))
        assert all(x==scale*y for x,y in zip(pulled,rhs))
        inequalities+=potentials(graph,voltage,certificate['cycle_certificate']);counts['CERTIFIED_EXTENSION_KERNEL']+=1
    assert seen==expected and len(original['records'])==45 and len(data['records'])==1015
    assert set(positive)<=set(affine)
    return dict(status='PASS',ordinary_AC_goal_solved=False,first_parent_graphs=len(original['records']),
                complete_second_vertex_pair_coverage=len(seen),counts=dict(counts),full_affine_dimensions=dict(dimensions),
                no_extension_graph_rank_counts=dict(failure_ranks),
                integer_potential_inequalities=inequalities,actual_affine_cycle_witnesses=cycles,
                parameter_roots_tested=roots,parameter_root_and_open_cell_samples=samples,
                uniform_affine_primitive_witnesses=primitive_count,
                input_sha256=[hashlib.sha256(r).hexdigest() for r in raw],
                input_container_sha256=[hashlib.sha256(r).hexdigest() for r in containers],
                independence='No V/X imports; quotient folding, Tarjan SCCs, exact sign-cell partition; T Euclidean primitive routine reused',
                scope='Specified quotient/character families only; neither actual AC successor reachability nor a global obstruction')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('inputs',nargs='+');parser.add_argument('--output',required=True);args=parser.parse_args()
    result=run(args.inputs);Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
