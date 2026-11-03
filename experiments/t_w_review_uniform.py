"""Independent labelled-corner and exhaustive initial AK controls for W.

No W modules are imported. The uniform proof is symbolic in the review;
the finite index controls and full AK2/AK3 order enumerations check its
conventions separately.
"""
import argparse
from collections import Counter
from itertools import combinations,permutations,product
import json
from pathlib import Path

LETTERS='xXyY'
BLOCKS=((1,2,3),(0,3,2),(0,1,3),(0,2,1))


def link(n):
    words=['x'*n+'Y'*(n+1),'xyxYXY'];ends=[];sheets={};incident=[[] for _ in range(4)];offset=0
    for word in words:
        for i,c in enumerate(word):
            e=offset+i;ends.append((LETTERS.index(c.swapcase()),LETTERS.index(word[(i+1)%len(word)])))
            incident[ends[-1][0]].append(2*e);incident[ends[-1][1]].append(2*e+1)
            before=2*(offset+(i-1)%len(word))+1;sheets[before]=2*e;sheets[2*e]=before
        offset+=len(word)
    return ends,sheets,incident


def reference(ends):
    orders=[[] for _ in range(4)]
    for v in range(4):
        for neighbor in BLOCKS[v]:
            edges=[e for e,pair in enumerate(ends) if set(pair)=={v,neighbor}]
            if v>neighbor:edges.reverse()
            orders[v].extend(2*e+int(ends[e][1]==v) for e in edges)
    return orders


def orientation(order,triple):
    a,b,c=(order.index(d) for d in triple)
    return int(a<b<c or b<c<a or c<a<b)


def uniform(n):
    ends,sheets,incident=link(n);orders=reference(ends);m=2*n+1
    triples=[(0,(2*(n-2)+1,2*(2*n)+1,2*(m+1)+1)),
             (2,(2*n,2*(n+1),2*m+1)),
             (2,(2*n,2*(n+1),2*(m+3)))]
    comparisons={(n-1,m+2):1,(n,n+1):2};rows=[]
    for vertex,triple in triples:
        assert all(d in incident[vertex] for d in triple)
        paired=tuple(sheets[d] for d in triple)
        assert all(d in incident[vertex^1] for d in paired)
        mask=0
        for side in (triple,paired):
            for da,db in combinations(side,2):
                ea,eb=sorted((da//2,db//2))
                if set(ends[ea])==set(ends[eb]):mask^=comparisons[ea,eb]
        first=orientation(orders[vertex],triple);second=orientation(orders[vertex^1],paired)
        rows.append(dict(mask=mask,rhs=1^first^second,reference_orientation=[first,second]))
    assert [r['mask'] for r in rows]==[1,2,3]
    assert [r['rhs'] for r in rows]==[0,0,1]
    assert [r['reference_orientation'] for r in rows]==[[1,0],[1,0],[1,1]]
    return rows


def exhaustive(n):
    ends,sheets,incident=link(n);histogram=Counter();orders=[None]*4
    choices=[[(darts[0],)+tail for tail in permutations(darts[1:])] for darts in (incident[0],incident[2])]
    for x,y in product(*choices):
        orders[0]=x;orders[1]=tuple(sheets[d] for d in x[::-1]);orders[2]=y;orders[3]=tuple(sheets[d] for d in y[::-1])
        successor={a:b for order in orders for a,b in zip(order,order[1:]+order[:1])}
        unseen=set(successor);faces=0
        while unseen:
            faces+=1;at=next(iter(unseen))
            while at in unseen:
                unseen.remove(at);at=successor[at^1]
        genus_twice=2-4+len(ends)-faces
        assert genus_twice>=0 and genus_twice%2==0
        histogram[genus_twice//2]+=1
    assert (sum(histogram.values()),min(histogram))==((2880,1) if n==2 else (86400,2))
    return dict(n=n,compatible_rotation_systems=sum(histogram.values()),minimum_genus=min(histogram),genus_histogram=dict(sorted(histogram.items())))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    rows=[uniform(n) for n in range(2,257)]
    result=dict(status='PASS',ordinary_AC_goal_solved=False,
                independence='No W imports; corner and sheet reconstruction, reference chart and genus calculation independent',
                uniform_index_control_n=[2,256],uniform_equation_masks=[1,2,3],uniform_rhs=[0,0,1],
                uniform_reference_orientations=[[1,0],[1,0],[1,1]],exhaustive_initial_controls=[exhaustive(2),exhaustive(3)],
                scope='Finite index/exhaustive controls; the uniform all-n claim uses the symbolic proof in the review')
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
