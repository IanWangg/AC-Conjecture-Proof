"""Apply V's unbounded criterion to all42 initial rotation successors.

The source pairs are actual independently conjugated AK3 relators. This
does not cover a preceding arbitrary Nielsen basis or disjoint axes with
an arbitrary bridge. The construction and cycle solver are V's algorithms.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
for directory in (HERE.parent/'research_v',HERE.parent/'research_r',HERE.parent/'root'):
    sys.path.insert(0,str(directory))
try:
    from v_vertex_identification import fold,spanning,fold_identification,reduce,inverse,cross,dot
    from v_voltage_cycle_review import review
except ImportError:
    from vertex_identification import fold,spanning,fold_identification,reduce,inverse,cross,dot
    from voltage_cycle_review import review
from verify_vertex_voltage import verify

def analyze(pair):
    original=fold(pair);paths,_,_,_=spanning(original);records=[];certificates=[]
    for a,b in combinations(range(len(original)//4),2):
        graph,projection=fold_identification(original,a,b)
        _,extra,arc,coordinates=spanning(graph);rank=len(extra)
        row={'identified_vertices':[a,b],'graph':list(graph),'rank':rank,'vertex_projection':projection}
        if rank==3:
            p,q=map(coordinates,pair);t=reduce(paths[a]+inverse(paths[b]));r=coordinates(t)
            h=cross(p,q);d=dot(h,r)
            if abs(d)==1:
                h=[x//d for x in h];weights=[0]*len(graph)
                for (v,c,w),(i,s) in arc.items():weights[4*v+c]=s*h[i]
                row.update(extra_generator=t,tree_chord_character=h,edge_voltages=weights,kernel_primitive_witness=None)
                certificates.append({'identified_vertices':[a,b],**review(graph,weights)})
            else:row['character_construction_unresolved_determinant']=d
        records.append(row)
    data={'original_pair':list(pair),'original_graph':list(original),'records':records}
    cert={'results':certificates}
    complete=len(certificates)==len(records) and all(r['status']=='PASS' for r in certificates)
    independent=verify(data,cert) if complete else None
    return data,cert,independent

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
    source=('xxxYYYY','xyxYXY');records=[]
    for i in range(len(source[0])):
        for j in range(len(source[1])):
            pair=[source[0][i:]+source[0][:i],source[1][j:]+source[1][:j]]
            data,cert,audit=analyze(pair)
            records.append({'rotation_offsets':[i,j],'status':'PASS' if audit else 'UNRESOLVED',
                            'identification_data':data,'cycle_certificates':cert,'independent_audit':audit})
    summary={'status':'PASS' if all(r['status']=='PASS' for r in records) else 'PARTIAL',
        'ordinary_AC_goal_solved':False,'literal_initial_rotation_successors':len(records),
        'fully_certified_successors':sum(r['status']=='PASS' for r in records),
        'unresolved_successors':sum(r['status']!='PASS' for r in records),
        'vertex_identifications':sum(len(r['identification_data']['records']) for r in records),
        'integer_potential_inequalities':sum(r['independent_audit']['integer_potential_inequalities_checked'] for r in records if r['independent_audit']),
        'records':records}
    Path(args.output).write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='records'},indent=2))
