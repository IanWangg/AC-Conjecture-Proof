"""Independent planar multigraph chart controls for Research W.

Enumerate every cyclic vertex order directly, with no sheet-pairing
assumption and no imports from W's constructor or verifier. Check each
spherical embedding against the claimed full planar chart.
"""
import argparse
from itertools import combinations,permutations,product
import json
from pathlib import Path


def cyclic_equal(a,b):
    return len(a)==len(b) and any(a==b[i:]+b[:i] for i in range(len(b)))


def graph(simple,multiplicity):
    ends=[pair for pair,m in zip(simple,multiplicity) for _ in range(m)]
    incident=[[] for _ in range(4)];bundles={}
    for e,(a,b) in enumerate(ends):
        incident[a].append(2*e);incident[b].append(2*e+1)
        bundles.setdefault((a,b),[]).append(e)
    return ends,incident,bundles


def planar(orders,ends):
    sigma=[-1]*(2*len(ends))
    for order in orders:
        for a,b in zip(order,order[1:]+order[:1]):sigma[a]=b
    unseen=set(range(len(sigma)));faces=0
    while unseen:
        faces+=1;at=next(iter(unseen))
        while at in unseen:
            unseen.remove(at);at=sigma[at^1]
    return 4-len(ends)+faces==2


def block(orders,vertex,edges):
    order=orders[vertex];selected=set(edges)
    flags=[d//2 in selected for d in order]
    starts=[i for i in range(len(order)) if flags[i] and not flags[i-1]]
    assert len(starts)==1,('nonconsecutive bundle',vertex,edges,orders)
    at=starts[0];found=[]
    while flags[at]:
        found.append(order[at]//2);at=(at+1)%len(order)
    assert set(found)==selected
    return found


def check_chart(kind,orders,ends,bundles):
    neighbors=[[] for _ in range(4)]
    for a,b in bundles:neighbors[a].append(b);neighbors[b].append(a)
    roots=[v for v in range(4) if len(neighbors[v])==3]
    arms=[v for v in range(4) if len(neighbors[v])==2]
    for (a,b),edge_ids in bundles.items():
        if kind=='DIAMOND' and a in roots and b in roots:continue
        assert block(orders,a,edge_ids)==block(orders,b,edge_ids)[::-1]
    if kind=='K4':
        reference=((1,2,3),(0,3,2),(0,1,3),(0,2,1))
        compressed=[]
        for v,order in enumerate(orders):
            labels=[ends[d//2][1-(d%2)] for d in order]
            compressed.append(tuple(labels[i] for i in range(len(labels)) if labels[i]!=labels[i-1]))
        assert any(all(cyclic_equal(compressed[v],reference[v][::sign]) for v in range(4)) for sign in (1,-1))
    elif kind=='DIAMOND':
        u,v=roots;w,z=arms;direct=bundles[min(u,v),max(u,v)]
        def items(root):
            labels=[]
            for dart in orders[root]:
                other=ends[dart//2][1-dart%2]
                labels.append(0 if other==w else 1 if other==z else 2+direct.index(dart//2))
            return tuple(labels[i] for i in range(len(labels)) if labels[i]!=labels[i-1])
        first,second=items(u),items(v)
        assert len(first)==len(second)==2+len(direct)
        assert cyclic_equal(first,second[::-1])


def run():
    families=[('K4',list(combinations(range(4),2)),2,9),
              ('C4',[(0,1),(1,2),(2,3),(0,3)],3,8),
              ('DIAMOND',[(0,1),(0,2),(0,3),(1,2),(1,3)],2,8)]
    result=[]
    for kind,simple,maximum,edge_cap in families:
        graphs=orders_tested=spherical=0
        for multiplicity in product(range(1,maximum+1),repeat=len(simple)):
            if sum(multiplicity)>edge_cap:continue
            graphs+=1;ends,incident,bundles=graph(simple,multiplicity)
            choices=[[(darts[0],)+tail for tail in permutations(darts[1:])] for darts in incident]
            for orders in product(*choices):
                orders_tested+=1
                if not planar(orders,ends):continue
                spherical+=1;check_chart(kind,orders,ends,bundles)
        result.append(dict(kind=kind,multigraphs=graphs,all_rotation_systems_checked=orders_tested,
                           spherical_rotation_systems=spherical,all_spherical_orders_fit_chart=True,
                           maximum_bundle_multiplicity=maximum,maximum_total_edges=edge_cap))
    return dict(status='PASS',ordinary_AC_goal_solved=False,independence='No W imports; all vertex cyclic orders, no sheet constraints',
                scope='Finite chart-completeness controls only; geometric proof remains mathematical',checks=result)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    result=run();Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
