"""Fast necessary GF(2) obstruction for synchronized planar K4 multigraphs.

Every bundle of parallel edges is consecutive in a planar K4 embedding.
Its local permutation changes a triple's orientation by the parity of
within-bundle inversions. Pairwise comparisons are relaxed to independent
bits, so inconsistency is a sound negative certificate. Consistency alone
does NOT establish that the comparisons form linear orders.
"""
from itertools import combinations,product,permutations
import json
from pathlib import Path
from thickening_rotations import link

def orientation(order,triple):
    positions=[order.index(d) for d in triple]
    a,b,c=positions
    return int((a<b<c) or (b<c<a) or (c<a<b))

def simple_k4_orders():
    choices=[]
    for v in range(4):
        neighbors=[x for x in range(4) if x!=v]
        choices.append([(neighbors[0],)+x for x in permutations(neighbors[1:])])
    for orders in product(*choices):
        darts=[(a,b) for a in range(4) for b in range(4) if a!=b]
        sigma={(a,b):(a,orders[a][(orders[a].index(b)+1)%3]) for a,b in darts}
        unseen=set(darts);faces=0
        while unseen:
            faces+=1;at=min(unseen);start=at
            while True:
                unseen.remove(at)
                at=sigma[at[::-1]]
                if at==start:break
        if faces==4:
            return orders
    raise AssertionError('K4 has a planar embedding')

K4=simple_k4_orders()

def equations(words):
    incidence,paired,endpoints=link(words)
    bundles={}
    for e,(a,b) in enumerate(endpoints):
        bundles.setdefault(tuple(sorted((a,b))),[]).append(e)
    if len(bundles)!=6:
        return None
    variables=[]
    for bundle in sorted(bundles):
        variables.extend(combinations(bundles[bundle],2))
    indices={pair:i for i,pair in enumerate(variables)}
    orders=[]
    for v in range(4):
        order=[]
        for neighbor in K4[v]:
            edges=bundles[tuple(sorted((v,neighbor)))]
            if v>neighbor:edges=edges[::-1]
            order.extend(2*e+(endpoints[e][1]==v) for e in edges)
        orders.append(order)
    def flips(triple):
        bits=0
        for a,b in combinations(triple,2):
            ea,eb=a//2,b//2
            if tuple(sorted(endpoints[ea]))==tuple(sorted(endpoints[eb])):
                bits ^= 1<<indices[tuple(sorted((ea,eb)))]
        return bits
    rows=[]
    for v in (0,2):
        for triple in combinations(incidence[v],3):
            other=tuple(paired[d] for d in triple)
            rhs=1^orientation(orders[v],triple)^orientation(orders[v^1],other)
            rows.append({'vertex':v,'triple':list(triple),
                         'mask':flips(triple)^flips(other),'rhs':rhs})
    return {'variables':[list(p) for p in variables],'base_orders':orders,'equations':rows}

def decide(words):
    system=equations(words)
    if system is None:
        return {'status':'NOT_K4','words':words}
    pivots={}
    for index,row in enumerate(system['equations']):
        bits,rhs,proof=row['mask'],row['rhs'],1<<index
        while bits:
            pivot=bits.bit_length()-1
            if pivot not in pivots:
                pivots[pivot]=(bits,rhs,proof)
                break
            old=pivots[pivot]
            bits^=old[0];rhs^=old[1];proof^=old[2]
        if not bits and rhs:
            used=[i for i in range(len(system['equations'])) if proof>>i&1]
            return {'status':'PARITY_OBSTRUCTION','words':words,
                    'variable_count':len(system['variables']),
                    'equation_count':len(system['equations']),
                    'contradiction_rows':[system['equations'][i] for i in used],
                    'base_orders':system['base_orders'],
                    'variables':system['variables']}
    return {'status':'PARITY_CONSISTENT','words':words,
            'variable_count':len(system['variables']),
            'equation_count':len(system['equations']),
            'linear_rank':len(pivots)}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('words',nargs='+');p.add_argument('--output',required=True)
    args=p.parse_args();result=decide(args.words)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
