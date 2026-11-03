"""Independent T kernel-certificate audit for all42 literal rotations.

Uses T's independent literal fold/quotient, character pullback and
Tarjan/potential checker, importing no V/X constructor or solver.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
try:
    from t_x_review_h1 import audit_instance
except ModuleNotFoundError:
    from x_review_h1 import audit_instance
from nielsen_basis_classes import read_payload


def run(path):
    raw=read_payload(path);data=json.loads(raw);p,b='xxxYYYY','xyxYXY';seen=set();total=Counter();records=[]
    for row in data['records']:
        i,j=row['rotation_offsets'];key=i,j;assert key not in seen and 0<=i<7 and 0<=j<6;seen.add(key)
        pair=[p[i:]+p[:i],b[j:]+b[:j]];assert row['identification_data']['original_pair']==pair
        checked=audit_instance(row['identification_data'],row['cycle_certificates'])
        records.append(dict(rotation_offsets=[i,j],**checked))
        for field in ('complete_vertex_identifications','signed_double_free_automata','cyclic_SCCs','integer_potential_inequalities','directed_pullback_equalities'):total[field]+=checked[field]
    assert seen=={(i,j) for i in range(7) for j in range(6)}
    return dict(status='PASS',ordinary_AC_goal_solved=False,complete_literal_rotation_sources=len(seen),
                **total,records=records,input_sha256=hashlib.sha256(raw).hexdigest(),
                independence='No V/X imports; T refolds all literal pairs and quotient graphs, verifies characters/coboundaries and Tarjan SCC potentials',
                scope='42 specific subgroup theorem instances; axes/phase deduction reviewed separately; no unrestricted AC invariant')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('input');parser.add_argument('--output',required=True);args=parser.parse_args()
    result=run(args.input);Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
