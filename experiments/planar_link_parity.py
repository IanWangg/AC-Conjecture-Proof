"""Parity relaxation of planar paired rotations for K4, diamond and C4.

Only PARITY_OBSTRUCTION is a conclusion. PARITY_CONSISTENT is unresolved:
the independent comparison bits may not define transitive linear orders.
The diamond model includes arbitrary interleaving of direct edges with
the two long branches; it does not falsely force the direct edges to be
consecutive.
"""
from itertools import combinations
from collections import Counter
from thickening_rotations import link
from k4_rotation_parity import equations as k4_equations,orientation

def model(words):
    incidence,paired,ends=link(words)
    bundles={}
    for e,pair in enumerate(ends):
        bundles.setdefault(tuple(sorted(pair)),[]).append(e)
    if len(bundles)==6:
        return {'kind':'K4',**k4_equations(words)}
    neighbors=[{b if a==v else a for a,b in bundles if v in (a,b)} for v in range(4)]
    degrees=sorted(map(len,neighbors))
    variables=[];index={}
    def variable(key):
        key=tuple(key)
        if key not in index:
            index[key]=len(variables);variables.append(list(key))
        return 1<<index[key]
    def edge_bits(darts):
        result=0
        for a,b in combinations(darts,2):
            ea,eb=sorted((a//2,b//2))
            if sorted(ends[ea])==sorted(ends[eb]):
                result^=variable(('edge',ea,eb))
        return result
    def darts_at(edges,v):
        return [2*e+int(ends[e][1]==v) for e in edges]
    if len(bundles)==4 and degrees==[2,2,2,2]:
        kind='C4';orders=[]
        for v in range(4):
            order=[]
            for other in sorted(neighbors[v]):
                edges=bundles[tuple(sorted((v,other)))]
                order+=darts_at(edges if v<other else edges[::-1],v)
            orders.append(order)
        features=lambda v,triple:edge_bits(triple)
    elif len(bundles)==5 and degrees==[2,2,3,3]:
        kind='DIAMOND'
        u,v=sorted(i for i in range(4) if len(neighbors[i])==3)
        w,z=sorted(i for i in range(4) if len(neighbors[i])==2)
        branch_edges={}
        for root in (u,v):
            branch_edges[root]={0:bundles[tuple(sorted((root,w)))],
                                1:bundles[tuple(sorted((root,z)))]}
        direct=bundles[tuple(sorted((u,v)))]
        for i,e in enumerate(direct,2):
            branch_edges[u][i]=branch_edges[v][i]=[e]
        items=list(range(2+len(direct)))
        orders=[None]*4
        dart_branch={}
        for root,item_order in ((u,items),(v,items[::-1])):
            orders[root]=[]
            for item in item_order:
                darts=darts_at(branch_edges[root][item],root)
                orders[root]+=darts
                dart_branch.update({d:item for d in darts})
        for interior,item in ((w,0),(z,1)):
            orders[interior]=[]
            for root in (u,v):
                orders[interior]+=darts_at(branch_edges[root][item][::-1],interior)
        def features(vertex,triple):
            if vertex not in (u,v):
                return edge_bits(triple)
            labels=[dart_branch[d] for d in triple]
            if len(set(labels))<3:
                return edge_bits(triple)
            bits=0
            # Item0 is fixed as the first item in the circular order.
            for a,b in combinations(sorted(labels),2):
                if a:
                    bits^=variable(('branch',a,b))
            return bits
    else:
        return None
    rows=[]
    for vertex in (0,2):
        for triple in combinations(incidence[vertex],3):
            other=tuple(paired[d] for d in triple)
            rhs=1^orientation(orders[vertex],triple)^orientation(orders[vertex^1],other)
            rows.append({'vertex':vertex,'triple':list(triple),
                         'mask':features(vertex,triple)^features(vertex^1,other),'rhs':rhs})
    return {'kind':kind,'variables':variables,'base_orders':orders,'equations':rows}

def decide(words):
    system=model(words)
    if system is None:
        return {'status':'NOT_SUPPORTED','words':words}
    pivots={};rows=system['equations']
    for index,row in enumerate(rows):
        bits,rhs,proof=row['mask'],row['rhs'],1<<index
        while bits:
            pivot=bits.bit_length()-1
            if pivot not in pivots:
                pivots[pivot]=(bits,rhs,proof)
                break
            old=pivots[pivot];bits^=old[0];rhs^=old[1];proof^=old[2]
        if not bits and rhs:
            selected=[rows[i] for i in range(len(rows)) if proof>>i&1]
            return {'status':'PARITY_OBSTRUCTION','words':words,'kind':system['kind'],
                    'variable_count':len(system['variables']),'equation_count':len(rows),
                    'contradiction_rows':selected,'base_orders':system['base_orders'],
                    'variables':system['variables']}
    return {'status':'PARITY_CONSISTENT','words':words,'kind':system['kind'],
            'variable_count':len(system['variables']),'equation_count':len(rows),
            'linear_rank':len(pivots)}

if __name__=='__main__':
    import argparse,json
    from pathlib import Path
    p=argparse.ArgumentParser();p.add_argument('words',nargs='+');p.add_argument('--output',required=True)
    args=p.parse_args();result=decide(args.words)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
