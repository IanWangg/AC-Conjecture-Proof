"""The same three synchronized triple equations obstruct initial AK(n).

The unbounded statement is the labelled-corner proof in the report.
This script controls the indices and exact XOR on n=2,...,32.
"""
from itertools import combinations
import json
from pathlib import Path
from k4_rotation_parity import equations

def certificate(n):
    assert n>=2
    words=['x'*n+'Y'*(n+1),'xyxYXY']
    m=2*n+1
    triples=[(0,[2*(n-2)+1,2*(m-1)+1,2*(m+1)+1]),
             (2,[2*n,2*(n+1),2*m+1]),
             (2,[2*n,2*(n+1),2*(m+3)])]
    system=equations(words)
    lookup={(r['vertex'],tuple(r['triple'])):r for r in system['equations']}
    rows=[lookup[v,tuple(sorted(t))] for v,t in triples]
    mask=rhs=0
    for row in rows:mask^=row['mask'];rhs^=row['rhs']
    assert mask==0 and rhs==1
    expected_pairs={(n-1,m+2),(n,n+1)}
    used={tuple(system['variables'][j]) for row in rows for j in range(len(system['variables'])) if row['mask']>>j&1}
    assert used==expected_pairs
    compact_vars=sorted(used)
    compact_rows=[]
    for row in rows:
        bits=0
        for j,pair in enumerate(compact_vars):
            if row['mask']>>system['variables'].index(list(pair))&1:bits^=1<<j
        compact_rows.append(dict(row,mask=bits))
    assert [r['mask'] for r in compact_rows]==[1,2,3]
    assert [r['rhs'] for r in compact_rows]==[0,0,1]
    return {'status':'PARITY_OBSTRUCTION','n':n,'words':words,'kind':'K4',
            'variables':[list(p) for p in compact_vars],
            'base_orders':system['base_orders'],'contradiction_rows':compact_rows}

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--directory',required=True)
    args=parser.parse_args();directory=Path(args.directory);directory.mkdir(parents=True,exist_ok=True)
    results=[certificate(n) for n in range(2,33)]
    (directory/'uniform_ak_parity_controls.json').write_text(json.dumps({
        'status':'PASS','controlled_n':[r['n'] for r in results],
        'uniform_rhs':[0,0,1],'uniform_masks':[1,2,3],
        'proof_scope':'Unbounded proof is geometric, not extrapolation from these controls'},indent=2)+'\n')
    (directory/'ak3_uniform_parity_certificate.json').write_text(json.dumps(certificate(3),indent=2)+'\n')
    print('PASS',len(results),'uniform three-equation controls')
