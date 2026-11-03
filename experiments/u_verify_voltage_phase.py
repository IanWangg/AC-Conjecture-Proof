"""Independent finite verifier for V's unbounded one-phase certificate.

No V/R folding, character, SCC, or Bellman-Ford implementation is imported.
Folding uses an equivalence relation closed under labeled transitions;
SCCs use transitive reachability; supplied potentials are checked directly.
"""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
from u_verify_native import graph as validate_record,follow,inverse,reduce,verify_absence

LETTERS='xXyY'


def validate(g):
    validate_record({'graph':g,'vertices':len(g)//4})


def fold_relation(g,identified=None):
    n=len(g)//4;classes=[{v} for v in range(n)]
    def merge(a,b):
        left=next(group for group in classes if a in group)
        right=next(group for group in classes if b in group)
        if left is right:return False
        left.update(right);classes.remove(right);return True
    if identified:merge(*identified)
    while True:
        change=False
        for group in classes:
            for c in range(4):
                targets=[g[4*v+c] for v in group if g[4*v+c]>=0]
                for w in targets[1:]:
                    if merge(targets[0],w):change=True;break
                if change:break
            if change:break
        if not change:break
    groups={v:min(group) for group in classes for v in group};out={}
    for v in range(n):
        for c,w in enumerate(g[4*v:4*v+4]):
            if w>=0:
                key=groups[v],c;target=groups[w]
                if key in out:assert out[key]==target
                out[key]=target
    named={groups[0]:0};queue=deque([groups[0]]);answer=[]
    while queue:
        v=queue.popleft()
        for c in range(4):
            target=out.get((v,c))
            if target is None:answer.append(-1)
            else:
                if target not in named:named[target]=len(named);queue.append(target)
                answer.append(named[target])
    validate(answer)
    return answer,[named[groups[v]] for v in range(n)]


def fold_word_arcs(words):
    # General multi-edge bouquet: every letter is first an isolated two-vertex
    # edge; endpoint identifications attach the loops. Transition conflicts are
    # then closed by a separate union-of-sets procedure.
    edges=[];links=[];count=1
    for raw in words:
        word=reduce(raw);at=0
        for i,c in enumerate(word):
            a,b=count,count+1;count+=2
            edges.append((a,LETTERS.index(c),b));links.append((at,a))
            at=b
        links.append((at,0))
    groups=[{v} for v in range(count)]
    def merge(a,b):
        left=next(s for s in groups if a in s);right=next(s for s in groups if b in s)
        if left is right:return False
        left.update(right);groups.remove(right);return True
    for a,b in links:merge(a,b)
    all_edges=edges+[(b,c^1,a) for a,c,b in edges]
    while True:
        cls={v:min(s) for s in groups for v in s};seen={};changed=False
        for a,c,b in all_edges:
            key=cls[a],c
            if key in seen and merge(seen[key],b):changed=True;break
            seen[key]=b
        if not changed:break
    cls={v:min(s) for s in groups for v in s};out={(cls[a],c):cls[b] for a,c,b in all_edges}
    named={cls[0]:0};queue=deque([cls[0]]);result=[]
    while queue:
        v=queue.popleft()
        for c in range(4):
            end=out.get((v,c))
            if end is None:result.append(-1)
            else:
                if end not in named:named[end]=len(named);queue.append(end)
                result.append(named[end])
    validate(result);return result


def paths(g):
    out={0:''};queue=deque([0])
    while queue:
        v=queue.popleft()
        for c,w in enumerate(g[4*v:4*v+4]):
            if w>=0 and w not in out:out[w]=out[v]+LETTERS[c];queue.append(w)
    return out


def rank(g):return sum(v>=0 for v in g)//2-len(g)//4+1


def voltage_word(g,w,word,base=0):
    total=0;at=base
    for c in word:
        i=4*at+LETTERS.index(c);assert g[i]>=0
        total+=w[i];at=g[i]
    assert at==base;return total


def verify_character(original,row,original_paths,original_words=('xxxYYYY','xyxYXY')):
    g=row['graph'];weights=row['edge_voltages'];projection=row['vertex_projection'];n=len(g)//4
    assert len(weights)==len(g) and all(type(x)==int for x in weights)
    for v in range(n):
        for c,end in enumerate(g[4*v:4*v+4]):
            if end>=0:assert weights[4*v+c]==-weights[4*end+(c^1)]
    # Pullback to H0 is an exact coboundary, a direct cohomological certificate
    # that every original based loop has zero character.
    potential={0:0};queue=deque([0]);checked=0
    while queue:
        v=queue.popleft()
        for c,end in enumerate(original[4*v:4*v+4]):
            if end<0:continue
            assert g[4*projection[v]+c]==projection[end]
            value=potential[v]+weights[4*projection[v]+c]
            if end in potential:assert potential[end]==value
            else:potential[end]=value;queue.append(end)
            checked+=1
    assert len(potential)==len(original)//4
    a,b=row['identified_vertices'];t=reduce(original_paths[a]+inverse(original_paths[b]))
    assert t==row['extra_generator']
    assert potential[a]-potential[b]==voltage_word(g,weights,t)==1
    assert all(voltage_word(g,weights,w)==0 for w in original_words)
    return checked


def make_character(g,original_words,t):
    # Independently derive the normalized character in a BFS chord basis.
    tree_paths=paths(g)
    def edge(a,c,b):return min((a,c,b),(b,c^1,a))
    tree=set()
    for v,p in tree_paths.items():
        if not p:continue
        parent=follow(g,0,p[:-1]);tree.add(edge(parent,LETTERS.index(p[-1]),v))
    edges={edge(v,c,end) for v in range(len(g)//4) for c,end in enumerate(g[4*v:4*v+4]) if end>=0}
    chords=sorted(edges-tree);assert len(chords)==3
    def coords(word):
        answer=[0]*3;at=0
        for letter in word:
            c=LETTERS.index(letter);end=g[4*at+c];assert end>=0
            e=edge(at,c,end)
            if e in chords:answer[chords.index(e)]+=1 if e==(at,c,end) else -1
            at=end
        assert at==0;return answer
    a,b=map(coords,original_words);r=coords(t)
    cross=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
    denominator=sum(x*y for x,y in zip(cross,r));assert abs(denominator)==1
    character=[x//denominator for x in cross];weights=[0]*len(g)
    for (a,c,b),value in zip(chords,character):weights[4*a+c]=value;weights[4*b+(c^1)]=-value
    return weights


def automaton(g,weights,alphabet,blocked):
    states={2*v+i for v in range(len(g)//4) for i,c in enumerate(alphabet) if g[4*v+c]>=0}
    arcs=[]
    for state in sorted(states):
        v,i=divmod(state,2);c=alphabet[i];end=g[4*v+c]
        for j,d in enumerate(alphabet):
            if i==j==blocked or g[4*end+d]<0:continue
            arcs.append((state,2*end+j,weights[4*v+c]))
    # Warshall reachability is independent of V's two-pass DFS SCC code.
    reach={v:{v} for v in states}
    for a,b,_ in arcs:reach[a].add(b)
    for middle in sorted(states):
        for start in states:
            if middle in reach[start]:reach[start].update(reach[middle])
    pending=set(states);components=[]
    while pending:
        first=min(pending);group={v for v in pending if v in reach[first] and first in reach[v]}
        pending-=group
        edges=[edge for edge in arcs if edge[0] in group and edge[1] in group]
        if edges:components.append((frozenset(group),edges))
    return components


def verify_cycles(row,certificate):
    assert certificate['status']=='PASS';g=row['graph'];weights=row['edge_voltages']
    checks={(tuple(c['alphabet']),c['forbidden_double']):c for c in certificate['checks']}
    assert len(checks)==len(certificate['checks'])==8
    inequalities=0;components_checked=0
    for x in (0,1):
        for y in (2,3):
            for blocked in (0,1):
                check=checks[(x,y),blocked];assert check['status']=='PASS'
                expected=automaton(g,weights,(x,y),blocked)
                provided={frozenset(c['states']):c for c in check['cyclic_components']}
                assert len(provided)==len(check['cyclic_components'])
                assert set(provided)=={group for group,_ in expected}
                for group,arcs in expected:
                    c=provided[group];assert len(c['states'])==len(group)
                    sign=c['strict_cycle_voltage_sign'];assert type(sign)==int and sign in (-1,1)
                    assert len(c['potential'])==len(group) and all(type(v)==int for v in c['potential'])
                    potential=dict(zip(c['states'],c['potential']))
                    for a,b,w in arcs:
                        assert potential[b]-potential[a]<=len(group)*sign*w-1
                        inequalities+=1
                    components_checked+=1
    return inequalities,components_checked


def ak2_control():
    original=fold_word_arcs(('xxYYY','xyxYXY'));p=paths(original)
    a_word,b_word='XXyyy','YXyyXyx'
    choices=[(a,b) for a in range(len(original)//4) for b in range(len(original)//4)
             if follow(original,a,a_word)==a and follow(original,b,b_word)==b]
    assert choices and all(a!=b for a,b in choices)
    data=[]
    for a,b in choices:
        quotient,_=fold_relation(original,(a,b));r=rank(quotient)
        assert r==3
        t=reduce(p[a]+inverse(p[b]));assert follow(quotient,0,t)==0
        weights=make_character(quotient,('xxYYY','xyxYXY'),t)
        row={'graph':quotient,'edge_voltages':weights,'vertex_projection':fold_relation(original,(a,b))[1],
             'identified_vertices':[a,b],'extra_generator':t}
        verify_character(original,row,p,('xxYYY','xyxYXY'))
        first,second='x','Y'
        for op in 'RLRL':
            if op=='L':second=first+second
            else:first=first+second
        word=second;assert word=='xYxYYxYY'
        zero_loops=[v for v in range(len(quotient)//4)
                    if follow(quotient,v,word)==v and voltage_word(quotient,weights,word,v)==0]
        assert zero_loops
        data.append({'cut_vertices':[a,b],'quotient_rank':r,'extra_generator':t,
                     'zero_voltage_primitive':word,'signed_primitive_basis_program':'xY:RLRL:component1',
                     'loop_vertices':zero_loops})
    return {'status':'PASS','original_vertices':len(original)//4,'positive_phase_pair':[a_word,b_word],
            'matching_cut_pairs':data,'scope':'Known AK(2) positive phase has a rank-three character but an explicit zero-voltage primitive; strict cycle-sign exclusion fails'}


def run(overgroups,potentials,initial_absence):
    data=json.loads(Path(overgroups).read_text());cert=json.loads(Path(potentials).read_text())
    original=fold_word_arcs(('xxxYYYY','xyxYXY'));assert original==data['original_graph']
    assert len(original)//4==10 and rank(original)==2
    assert data['original_pair']==['xxxYYYY','xyxYXY']
    negatives=json.loads(Path(initial_absence).read_text());assert negatives['graph']==original
    initial_states=verify_absence(negatives)
    by_pair={tuple(r['identified_vertices']):r for r in data['records']}
    checks={tuple(r['identified_vertices']):r for r in cert['results']}
    pairs={(a,b) for a in range(10) for b in range(a+1,10)}
    assert len(by_pair)==len(data['records'])==len(checks)==len(cert['results'])==45
    assert set(by_pair)==set(checks)==pairs
    original_paths=paths(original);edge_checks=inequalities=components_checked=0
    for pair in sorted(pairs):
        row=by_pair[pair];quotient,projection=fold_relation(original,pair)
        assert quotient==row['graph'] and projection==row['vertex_projection']
        assert rank(quotient)==row['rank']==3
        edge_checks+=verify_character(original,row,original_paths)
        count,number=verify_cycles(row,checks[pair]);inequalities+=count;components_checked+=number
    return {'status':'PASS','ordinary_AC_goal_solved':False,
            'original_vertices':10,'independent_initial_absence_states_checked':initial_states,
            'all_unordered_vertex_pairs_checked':45,'rank_three_quotients_checked':45,
            'character_pullback_edge_equalities_checked':edge_checks,
            'normalizations_character_of_extra_generator_equals_one':45,
            'signed_forbidden_double_automata_checked':360,
            'cyclic_components_checked':components_checked,'integer_potential_inequalities_checked':inequalities,
            'AK2_positive_control':ak2_control(),
            'input_sha256':{Path(p).name:hashlib.sha256(Path(p).read_bytes()).hexdigest()
                            for p in (overgroups,potentials,initial_absence)},
            'scope':'Finite certificates for unrestricted-length one-phase primitive exclusion; no global AC invariant'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('overgroups');parser.add_argument('potentials')
    parser.add_argument('--initial-absence',required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args();result=run(args.overgroups,args.potentials,args.initial_absence)
    content=json.dumps(result,indent=2)+'\n';Path(args.output).write_text(content);print(content,end='')
