"""Sufficient unbounded zero-voltage primitive-loop exclusion.

Each signed-double-free edge-state SCC must have all directed cycles of
one strict voltage sign. A finite Bellman-Ford potential certifies that.
Failures of the sufficient test are explicitly unresolved.
"""
import argparse,json
from pathlib import Path

def components(states,arcs):
    out={v:[] for v in states};back={v:[] for v in states}
    for a,b,w in arcs:out[a].append(b);back[b].append(a)
    seen=set();order=[]
    def dfs(v):
        seen.add(v)
        for w in out[v]:
            if w not in seen:dfs(w)
        order.append(v)
    for v in states:
        if v not in seen:dfs(v)
    seen=set();answer=[]
    def rev(v,group):
        seen.add(v);group.append(v)
        for w in back[v]:
            if w not in seen:rev(w,group)
    for v in reversed(order):
        if v not in seen:
            group=[];rev(v,group);answer.append(sorted(group))
    return answer

def potential(group,arcs,sign):
    # Every simple cycle has at most N edges. Integer total voltage >=1
    # iff transformed weights N*sign*w-1 have no negative cycle.
    n=len(group);dist={v:0 for v in group}
    for i in range(n):
        changed=False
        for a,b,w in arcs:
            candidate=dist[a]+n*sign*w-1
            if dist[b]>candidate:dist[b]=candidate;changed=True
        if not changed:return [dist[v] for v in group]
    return None

def review(graph,voltage):
    n=len(graph)//4;checks=[]
    for x in (0,1):
        for y in (2,3):
            alphabet=(x,y)
            for blocked in (0,1):
                states=[2*v+i for v in range(n) for i,c in enumerate(alphabet) if graph[4*v+c]>=0]
                arcs=[]
                for state in states:
                    v,i=divmod(state,2);c=alphabet[i];end=graph[4*v+c]
                    for j,d in enumerate(alphabet):
                        if i==j==blocked:continue
                        if graph[4*end+d]>=0:arcs.append((state,2*end+j,voltage[4*v+c]))
                groups=components(states,arcs);certificates=[]
                for group in groups:
                    chosen=set(group);edges=[e for e in arcs if e[0] in chosen and e[1] in chosen]
                    if not edges:continue
                    sign=0;values=None
                    for s in (1,-1):
                        values=potential(group,edges,s)
                        if values is not None:sign=s;break
                    certificates.append(dict(states=group,strict_cycle_voltage_sign=sign,potential=values))
                checks.append(dict(alphabet=list(alphabet),forbidden_double=blocked,
                    status='PASS' if all(c['strict_cycle_voltage_sign'] for c in certificates) else 'UNRESOLVED',
                    cyclic_components=certificates))
    return dict(status='PASS' if all(c['status']=='PASS' for c in checks) else 'UNRESOLVED',checks=checks)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('input');parser.add_argument('--output',required=True)
    args=parser.parse_args();data=json.loads(Path(args.input).read_text());results=[]
    for row in data['records']:
        if row['rank']!=3:continue
        results.append(dict(identified_vertices=row['identified_vertices'],**review(row['graph'],row['edge_voltages'])))
    result=dict(status='PASS' if all(r['status']=='PASS' for r in results) else 'PARTIAL',ordinary_AC_goal_solved=False,
                rank3_cases=len(results),fully_certified_cases=sum(r['status']=='PASS' for r in results),
                unresolved_cases=sum(r['status']!='PASS' for r in results),results=results)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))
    print('Unresolved pairs:',[r['identified_vertices'] for r in results if r['status']!='PASS'])
