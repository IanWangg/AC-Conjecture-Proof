"""Strict replay, exact fixed-donor fillings, and signed-DAG waypoint audit.

No quotient evaluator is imported. Primitive absence follows from M's
rank-two signed-conjugacy lemma and the explicit directed acyclicity.
"""
import argparse
import json
from pathlib import Path
from elementary_verify import inverse,reduce,replay
from stallings_search import graph

P='xxxYYYY'
B='xyxYXY'
BP='XXyxYxxY'


def audit(path):
    cert=json.loads(Path(path).read_text())
    assert cert['start']==[P,B]
    target=cert['target']
    assert target[1]==BP
    replay_result=replay(cert)
    q=cert['quotient_conjugator']
    base=reduce(q+inverse(P)+inverse(q))
    difference=reduce(target[0]+inverse(base))
    assert difference==cert['free_difference']
    product=''
    for factor in cert['fixed_bprime_factorization']:
        sign,conjugator=factor['sign'],factor['conjugator']
        assert type(sign) is int and sign in (1,-1)
        cell=BP if sign==1 else inverse(BP)
        product=reduce(product+conjugator+cell+inverse(conjugator))
    assert product==difference
    encoded,size=graph(target)
    arcs=[]
    for v in range(size):
        for index,c in enumerate('xXyY'):
            w=encoded[4*v+index]
            if w>=0:arcs.append((v,c,w))
    assert len(arcs)//2-size+1==2
    topological={}
    for alphabet in ('xy','xY','Xy','XY'):
        outgoing={v:[] for v in range(size)}
        incoming={v:0 for v in range(size)}
        for a,c,b in arcs:
            if c in alphabet:
                outgoing[a].append(b)
                incoming[b]+=1
        ready=sorted(v for v in range(size) if incoming[v]==0)
        order=[]
        while ready:
            v=ready.pop(0)
            order.append(v)
            for w in outgoing[v]:
                incoming[w]-=1
                if incoming[w]==0:
                    ready.append(w)
                    ready.sort()
        assert len(order)==size
        positions={v:i for i,v in enumerate(order)}
        assert all(positions[a]<positions[b] for a,c,b in arcs if c in alphabet)
        topological[alphabet]=order
    return {'target':target,'strict_replay':replay_result,
            'fixed_donor_factor_count':len(cert['fixed_bprime_factorization']),
            'free_difference_factorization_verified':True,
            'subgroup_vertices':size,'subgroup_unoriented_edges':len(arcs)//2,
            'subgroup_rank':2,'arcs':arcs,'signed_topological_orders':topological,
            'whole_subgroup_contains_no_primitive_F2_element':True,
            'scope':'Exact reachable waypoint and unbounded subgroup-specific primitive obstruction; no global AC result'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('certificates',nargs='+')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    results=[audit(path) for path in args.certificates]
    Path(args.output).write_text(json.dumps({'status':'PASS','waypoints':results},indent=2)+'\n')
    print(json.dumps({'status':'PASS','waypoints':[
        {k:r[k] for k in ('target','fixed_donor_factor_count','subgroup_vertices',
                         'whole_subgroup_contains_no_primitive_F2_element')}|
        {'strict_moves':r['strict_replay']['moves'],'strict_peak':r['strict_replay']['peak_total_length']}
        for r in results]},indent=2))
