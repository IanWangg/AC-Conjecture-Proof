"""Exact real-parameter feasibility of V's sufficient strict-cycle test.

Enumerate every directed simple cycle in each finite SCC. Its affine
voltage gives a strict linear inequality. Intersect the two possible
cycle-sign intervals per SCC. Empty feasibility concerns this sufficient
certificate family only, not primitive existence.
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
for directory in (HERE.parent/'research_v',HERE.parent/'research_r',HERE):sys.path.insert(0,str(directory))
try:
    from v_vertex_identification import spanning
    from v_voltage_cycle_review import components,review
except ImportError:
    from vertex_identification import spanning
    from voltage_cycle_review import components,review
from kernel_second_phase import make_voltage

def interval_intersection(a,b):
    lo=b[0] if a[0] is None else a[0] if b[0] is None else max(a[0],b[0])
    hi=b[1] if a[1] is None else a[1] if b[1] is None else min(a[1],b[1])
    return None if lo is not None and hi is not None and lo>=hi else (lo,hi)

def sign_interval(cycles,sign):
    lo=hi=None
    for a,b in cycles:
        a,b=sign*a,sign*b
        if not a:
            if b<=0:return None
        elif a>0:
            v=-b/a;lo=v if lo is None else max(lo,v)
        else:
            v=-b/a;hi=v if hi is None else min(hi,v)
    return interval_intersection((lo,hi),(None,None))

def cycle_coefficients(group,arcs):
    chosen=set(group);out={v:[] for v in group}
    for a,b,p,q in arcs:
        if a in chosen and b in chosen:out[a].append((b,p,q))
    answer={};count=0
    for root in sorted(group):
        def dfs(at,seen,p,q,path):
            nonlocal count
            for end,a,b in out[at]:
                if end==root:
                    answer.setdefault((p+a,q+b),list(path));count+=1
                elif end>root and end not in seen:
                    dfs(end,seen|{end},p+a,q+b,path+(end,))
        dfs(root,{root},F(0),F(0),(root,))
    return answer,count

def feasibility(graph,base,direction):
    _,_,arc,_=spanning(graph)
    a=[F(0)]*len(graph);b=[F(0)]*len(graph)
    for (v,c,w),(i,s) in arc.items():a[4*v+c]=s*direction[i];b[4*v+c]=s*base[i]
    intervals=[(None,None)];checks=[];cycle_count=0
    for x in (0,1):
        for y in (2,3):
            alphabet=(x,y)
            for blocked in (0,1):
                states=[2*v+i for v in range(len(graph)//4) for i,c in enumerate(alphabet) if graph[4*v+c]>=0]
                arcs=[]
                for state in states:
                    v,i=divmod(state,2);c=alphabet[i];end=graph[4*v+c]
                    for j,d in enumerate(alphabet):
                        if i==j==blocked:continue
                        if graph[4*end+d]>=0:arcs.append((state,2*end+j,a[4*v+c],b[4*v+c]))
                groups=components(states,[(u,v,0) for u,v,_,_ in arcs])
                for group in groups:
                    cycles,count=cycle_coefficients(group,arcs)
                    if not cycles:continue
                    cycle_count+=count
                    choices=[v for sign in (1,-1) if (v:=sign_interval(cycles,sign)) is not None]
                    intervals=list(dict.fromkeys(v for old in intervals for choice in choices if (v:=interval_intersection(old,choice)) is not None))
                    checks.append({'alphabet':list(alphabet),'forbidden_double':blocked,
                        'states':group,'simple_cycle_count':count,
                        'distinct_cycle_coefficients':[[str(a),str(b)] for a,b in sorted(cycles)],
                        'cycle_witnesses':[{'coefficients':[str(a),str(b)],'states':cycles[a,b]} for a,b in sorted(cycles)],
                        'strict_sign_intervals':[[None if z is None else str(z) for z in interval] for interval in choices]})
    return intervals,checks,cycle_count

def sample(interval):
    lo,hi=interval
    if lo is None and hi is None:return F(0)
    if lo is None:return hi-1
    if hi is None:return lo+1
    return (lo+hi)/2

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--output',required=True);args=p.parse_args()
    data=json.loads(Path(args.input).read_text());results=[];feasible=cycles=0
    for index,row in enumerate(data['records']):
        if row.get('extension_free_dimension')!=1:continue
        base=list(map(F,row['rational_particular']));direction=list(map(F,row['rational_directions'][0]))
        intervals,checks,count=feasibility(row['graph'],base,direction);cycles+=count
        result={'second_identification_index':index,'first_case_index':row['first_case_index'],
            'second_vertices':row['second_vertices'],
            'status':'STRICT_CYCLE_FAMILY_FEASIBLE' if intervals else 'STRICT_CYCLE_FAMILY_INFEASIBLE',
            'allowed_open_intervals':[[None if z is None else str(z) for z in interval] for interval in intervals],
            'cycle_checks':checks}
        if intervals:
            parameter=sample(intervals[0]);character=[v+parameter*w for v,w in zip(base,direction)]
            _,_,arc,_=spanning(row['graph']);voltage,coeffs=make_voltage(row['graph'],arc,character)
            cert=review(row['graph'],voltage);assert cert['status']=='PASS'
            result.update(parameter=str(parameter),character=coeffs,edge_voltages=voltage,cycle_certificate=cert)
            feasible+=1
        results.append(result)
    result={'status':'COMPLETE_EXACT_ONE_PARAMETER_CYCLE_FAMILY','ordinary_AC_goal_solved':False,
        'one_parameter_cases':len(results),'feasible_cases':feasible,'infeasible_cases':len(results)-feasible,
        'directed_simple_cycles_enumerated':cycles,'scope':'Exact feasibility of sufficient same-sign-cycle character family; infeasible is not a primitive witness.',
        'records':results}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
