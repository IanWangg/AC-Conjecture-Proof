"""Independent exact audit: no V/X constructor, solver or search imports.

Successful kernels use integer potential inequalities. No-extension
cases use dual linear rows. Infeasible affine families use actual finite
cycles as necessary constraints; completeness of cycle enumeration is
unneeded for those negative feasibility certificates.
"""
import argparse
from collections import Counter,deque
from fractions import Fraction as F
from itertools import combinations
import json
from math import gcd
from pathlib import Path

LETTERS='xXyY'
def inverse(word):return word.swapcase()[::-1]
def reduce(word):
    out=[]
    for c in word:
        if out and out[-1]==c.swapcase():out.pop()
        else:out.append(c)
    return ''.join(out)
def path_value(graph,voltage,word,base=0):
    at=base;value=F(0)
    for c in word:
        j=LETTERS.index(c);end=graph[4*at+j];assert end>=0
        value+=voltage[4*at+j];at=end
    assert at==base
    return value
def spanning(graph):
    def edge(a,c,b):return min((a,c,b),(b,c^1,a))
    paths={0:''};tree=set();queue=deque([0])
    while queue:
        a=queue.popleft()
        for c in range(4):
            b=graph[4*a+c]
            if b>=0 and b not in paths:
                paths[b]=paths[a]+LETTERS[c];tree.add(edge(a,c,b));queue.append(b)
    assert len(paths)==len(graph)//4
    all_edges={edge(a,c,b) for a in range(len(graph)//4) for c in range(4) if (b:=graph[4*a+c])>=0}
    chords=sorted(all_edges-tree);arcs={}
    for i,(a,c,b) in enumerate(chords):arcs[a,c,b]=(i,1);arcs[b,c^1,a]=(i,-1)
    basis=[reduce(paths[a]+LETTERS[c]+inverse(paths[b])) for a,c,b in chords]
    def coordinates(word):
        result=[0]*len(chords);at=0
        for letter in word:
            c=LETTERS.index(letter);end=graph[4*at+c];assert end>=0
            if (at,c,end) in arcs:
                i,s=arcs[at,c,end];result[i]+=s
            at=end
        assert at==0
        return result
    return basis,coordinates,arcs,paths
def quotient(graph,a,b):
    n=len(graph)//4;eq=[[i==j or {i,j}=={a,b} for j in range(n)] for i in range(n)]
    changed=True
    while changed:
        changed=False
        for k in range(n):
            for i in range(n):
                if eq[i][k]:
                    for j in range(n):
                        if eq[k][j] and not eq[i][j]:eq[i][j]=True;changed=True
        for i in range(n):
            for j in range(n):
                if not eq[i][j]:continue
                for c in range(4):
                    u,v=graph[4*i+c],graph[4*j+c]
                    if u>=0 and v>=0 and not eq[u][v]:eq[u][v]=eq[v][u]=True;changed=True
    roots=[next(j for j in range(n) if eq[i][j]) for i in range(n)]
    edges={(roots[i],c):roots[v] for i in range(n) for c in range(4) if (v:=graph[4*i+c])>=0}
    names={roots[0]:0};queue=deque([roots[0]]);encoded=[]
    while queue:
        u=queue.popleft()
        for c in range(4):
            v=edges.get((u,c),-1)
            if v>=0 and v not in names:names[v]=len(names);queue.append(v)
            encoded.append(names[v] if v>=0 else -1)
    return encoded,[names[r] for r in roots]
def determinant3(a,b,c):return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def rank3(matrix):return any(determinant3(*[[row[c] for c in cols] for row in matrix]) for cols in combinations(range(len(matrix[0])),3))
def automaton(graph,alphabet,blocked):
    states=[2*v+i for v in range(len(graph)//4) for i,c in enumerate(alphabet) if graph[4*v+c]>=0]
    arcs=[]
    for state in states:
        v,i=divmod(state,2);c=alphabet[i];end=graph[4*v+c]
        for j,d in enumerate(alphabet):
            if i==j==blocked:continue
            if graph[4*end+d]>=0:arcs.append((state,2*end+j,4*v+c))
    reach={v:{v} for v in states}
    for a,b,_ in arcs:reach[a].add(b)
    for k in states:
        for i in states:
            if k in reach[i]:reach[i]|=reach[k]
    groups={frozenset(j for j in states if j in reach[i] and i in reach[j]) for i in states}
    cyclic={g for g in groups if any(a in g and b in g for a,b,_ in arcs)}
    return states,arcs,cyclic
def verify_potentials(graph,voltage,certificate):
    assert certificate['status']=='PASS'
    assert len(certificate['checks'])==8
    seen=set();inequalities=0
    for item in certificate['checks']:
        alphabet=tuple(item['alphabet']);blocked=item['forbidden_double'];seen.add((alphabet,blocked))
        assert alphabet in ((0,2),(0,3),(1,2),(1,3)) and blocked in (0,1)
        _,arcs,cyclic=automaton(graph,alphabet,blocked)
        assert {frozenset(c['states']) for c in item['cyclic_components']}==cyclic
        for component in item['cyclic_components']:
            group=component['states'];sign=component['strict_cycle_voltage_sign'];assert sign in (-1,1)
            q=dict(zip(group,component['potential']));assert len(q)==len(group)
            assert all(type(x) is int for x in component['potential'])
            for a,b,edge in arcs:
                if a in q and b in q:
                    assert q[b]<=q[a]+len(group)*sign*voltage[edge]-1;inequalities+=1
    assert len(seen)==8
    return inequalities
def intersect(a,b):
    lo=b[0] if a[0] is None else a[0] if b[0] is None else max(a[0],b[0])
    hi=b[1] if a[1] is None else a[1] if b[1] is None else min(a[1],b[1])
    return None if lo is not None and hi is not None and lo>=hi else (lo,hi)
def sign_range(pairs,sign):
    result=(None,None)
    for a,b in pairs:
        a,b=sign*a,sign*b
        if a==0:
            if b<=0:return None
        else:
            bound=-b/a;result=intersect(result,(bound,None) if a>0 else (None,bound))
            if result is None:return None
    return result
def affine_voltages(graph,base,direction):
    _,_,arc,_=spanning(graph);p=[F(0)]*len(graph);q=[F(0)]*len(graph)
    for (a,c,b),(i,s) in arc.items():p[4*a+c]=s*direction[i];q[4*a+c]=s*base[i]
    return p,q
def verify_infeasible(graph,p,q,row):
    allowed=[(None,None)];cycles=0
    for check in row['cycle_checks']:
        alphabet=tuple(check['alphabet']);blocked=check['forbidden_double']
        _,arcs,cyclic=automaton(graph,alphabet,blocked);group=frozenset(check['states']);assert group in cyclic
        edge_index={(a,b):edge for a,b,edge in arcs};pairs=[]
        for witness in check['cycle_witnesses']:
            path=witness['states'];assert path and len(set(path))==len(path) and set(path)<=group
            a=b=F(0)
            for u,v in zip(path,path[1:]+path[:1]):
                edge=edge_index[u,v];a+=p[edge];b+=q[edge]
            assert [str(a),str(b)]==witness['coefficients'];pairs.append((a,b));cycles+=1
        choices=[v for sign in (1,-1) if (v:=sign_range(pairs,sign)) is not None]
        allowed=list({v for prior in allowed for choice in choices if (v:=intersect(prior,choice)) is not None})
    assert not allowed
    return cycles
def primitive_cyclic(word):
    assert word and reduce(word)==word and word[0]!=word[-1].swapcase()
    x=sum(c in 'xX' for c in word);y=len(word)-x
    assert gcd(x,y)==1
    assert not ('x' in word and 'X' in word) and not ('y' in word and 'Y' in word)
    mechanical=''.join('y' if ((i+1)*y)//len(word)>(i*y)//len(word) else 'x' for i in range(len(word)))
    translated=word.translate(str.maketrans('XY','xy'))
    assert any(translated==mechanical[i:]+mechanical[:i] for i in range(len(word)))
    return True

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('original');p.add_argument('extensions');p.add_argument('intervals');p.add_argument('duals');p.add_argument('primitives');p.add_argument('--output',required=True);args=p.parse_args()
    original=json.loads(Path(args.original).read_text());data=json.loads(Path(args.extensions).read_text());intervals=json.loads(Path(args.intervals).read_text());duals=json.loads(Path(args.duals).read_text());primitives=json.loads(Path(args.primitives).read_text())
    affine={r['second_identification_index']:r for r in intervals['records']};dual={r['second_identification_index']:r['dual_integer_row'] for r in duals['records']}
    primitive={r['second_identification_index']:r['witness'] for r in primitives['records'] if r['witness']}
    expected={(i,a,b) for i,parent in enumerate(original['records']) for a,b in combinations(range(len(parent['graph'])//4),2)}
    actual=[(r['first_case_index'],*r['second_vertices']) for r in data['records']]
    assert len(actual)==len(set(actual)) and set(actual)==expected
    counts=Counter();inequalities=cycles=positive=0
    for index,row in enumerate(data['records']):
        parent=original['records'][row['first_case_index']];old=parent['graph'];a,b=row['second_vertices'];graph,projection=quotient(old,a,b)
        assert graph==row['graph'] and projection==row['vertex_projection']
        basis,_,_,_=spanning(old);_,coordinates,_,_=spanning(graph)
        assert basis==row['old_basis_words'];matrix=[coordinates(w) for w in basis]
        assert len(basis)==3 and len(matrix[0])==row['rank']
        rhs=[path_value(old,parent['edge_voltages'],w) for w in basis]
        assert matrix==row['coordinate_rows'] and rhs==list(map(F,row['old_character']))
        if index in dual:
            assert row['rank']==2
            assert graph==[0,0,0,0], 'all551 observed rank2 quotients are the ambient rose'
            coefficients=dual[index];assert len(coefficients)==3
            assert all(sum(c*r[j] for c,r in zip(coefficients,matrix))==0 for j in range(len(matrix[0])))
            assert sum(c*y for c,y in zip(coefficients,rhs))!=0
            counts['NO_CHARACTER_EXTENSION']+=1;continue
        assert rank3(matrix)
        if index in affine:
            assert row['rank']==4 and row['extension_free_dimension']==1
            entry=affine[index];base=list(map(F,row['rational_particular']));direction=list(map(F,row['rational_directions'][0]))
            assert any(direction) and all(sum(a*b for a,b in zip(r,base))==y for r,y in zip(matrix,rhs))
            assert all(sum(a*b for a,b in zip(r,direction))==0 for r in matrix)
            if entry['status']=='STRICT_CYCLE_FAMILY_INFEASIBLE':
                pvol,qvol=affine_voltages(graph,base,direction);cycles+=verify_infeasible(graph,pvol,qvol,entry)
                counts['AFFINE_CYCLE_FAMILY_INFEASIBLE']+=1
                if index in primitive:
                    witness=primitive[index];word=witness['cyclic_word'];vertex=witness['loop_vertex'];primitive_cyclic(word)
                    assert path_value(graph,pvol,word,vertex)==path_value(graph,qvol,word,vertex)==0
                    at=0
                    for letter in witness['base_path']:
                        at=graph[4*at+LETTERS.index(letter)];assert at>=0
                    assert at==vertex
                    assert reduce(witness['base_path']+word+inverse(witness['base_path']))==witness['based_word']
                    assert path_value(graph,pvol,witness['based_word'])==path_value(graph,qvol,witness['based_word'])==0
                    positive+=1
                continue
            certificate=entry
        else:
            assert row['rank']==3 and row['extension_free_dimension']==0
            certificate=row['certificate']
        voltage=certificate['edge_voltages'];assert len(voltage)==len(graph)
        for v in range(len(graph)//4):
            for c in range(4):
                if (w:=graph[4*v+c])>=0:assert voltage[4*v+c]==-voltage[4*w+(c^1)]
        values=[path_value(graph,voltage,w) for w in basis]
        scale=next(value/old_value for value,old_value in zip(values,rhs) if old_value)
        assert scale and all(value==scale*old_value for value,old_value in zip(values,rhs))
        inequalities+=verify_potentials(graph,voltage,certificate['cycle_certificate']);counts['CERTIFIED_EXTENSION_KERNEL']+=1
    result={'status':'PASS','second_identifications':len(data['records']),'counts':dict(counts),
            'integer_potential_inequalities':inequalities,'actual_affine_cycle_witnesses':cycles,
            'uniform_affine_primitive_witnesses':positive,'ordinary_AC_goal_solved':False}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
