"""Independent replay of small planar-link XOR contradiction certificates.

No constructor, folding code, Gaussian solver, or topology search is
imported. The geometric planar-chart completeness is proved in the report.
"""
from itertools import combinations


def verify_certificate(cert):
    alphabet='xXyY';ends=[];sheets={};incident=[[] for _ in range(4)]
    offset=0
    for word in cert['words']:
        n=len(word)
        assert n and all(c in alphabet for c in word)
        for i,c in enumerate(word):
            nxt=word[(i+1)%n]
            assert c.swapcase()!=nxt
            pair=(alphabet.index(c.swapcase()),alphabet.index(nxt))
            edge=offset+i;ends.append(pair)
            incident[pair[0]].append(2*edge);incident[pair[1]].append(2*edge+1)
            before=2*(offset+(i+n-1)%n)+1;after=2*edge
            sheets[before]=after;sheets[after]=before
        offset+=n
    orders=cert['base_orders'];position={}
    for v,order in enumerate(orders):
        assert sorted(order)==sorted(incident[v])
        position.update({d:i for i,d in enumerate(order)})
    sigma={d:order[(i+1)%len(order)] for order in orders for i,d in enumerate(order)}
    unused=set(sigma);faces=0
    while unused:
        faces+=1;start=min(unused);at=start
        while True:
            unused.remove(at);at=sigma[at^1]
            if at==start:break
    # All supported charts have four nonisolated vertices and are connected.
    assert all(incident) and 4-len(ends)+faces==2
    edges={}
    for e,pair in enumerate(ends):edges.setdefault(tuple(sorted(pair)),[]).append(e)
    neighbors=[set() for _ in range(4)]
    for a,b in edges:neighbors[a].add(b);neighbors[b].add(a)
    kind=cert.get('kind','K4')
    variables={tuple(pair):j for j,pair in enumerate(cert['variables'])}

    def block_sequence(vertex,edge_ids):
        selected=set(edge_ids);order=orders[vertex]
        marks=[d//2 in selected for d in order]
        starts=[i for i in range(len(order)) if marks[i] and not marks[i-1]]
        assert len(starts)==1
        found=[];at=starts[0]
        while marks[at]:
            found.append(order[at]//2);at=(at+1)%len(order)
        assert sorted(found)==sorted(selected)
        return found

    def bit(key):
        key=tuple(key)
        assert key in variables, ('unlisted comparison',key)
        return 1<<variables[key]

    def edge_feature(triple):
        mask=0
        for a,b in combinations(triple,2):
            a,b=sorted((a//2,b//2))
            if set(ends[a])==set(ends[b]):
                key=(a,b) if kind=='K4' else ('edge',a,b)
                mask^=bit(key)
        return mask

    if kind=='K4':
        assert len(edges)==6
        for (a,b),edge_ids in edges.items():
            assert block_sequence(a,edge_ids)==edge_ids
            assert block_sequence(b,edge_ids)==edge_ids[::-1]
        feature=lambda vertex,triple:edge_feature(triple)
    elif kind=='C4':
        assert len(edges)==4 and sorted(map(len,neighbors))==[2,2,2,2]
        for (a,b),edge_ids in edges.items():
            assert block_sequence(a,edge_ids)==edge_ids
            assert block_sequence(b,edge_ids)==edge_ids[::-1]
        feature=lambda vertex,triple:edge_feature(triple)
    else:
        assert kind=='DIAMOND' and len(edges)==5
        assert sorted(map(len,neighbors))==[2,2,3,3]
        roots=sorted(v for v in range(4) if len(neighbors[v])==3)
        inner=sorted(set(range(4))-set(roots));u,v=roots;w,z=inner
        direct=edges[tuple(sorted(roots))]
        direct_item={e:2+i for i,e in enumerate(direct)}
        def item(root,dart):
            e=dart//2;a,b=ends[e];other=b if a==root else a
            if other==w:return 0
            if other==z:return 1
            assert other in roots
            return direct_item[e]
        items=list(range(2+len(direct)))
        for root,expected in ((u,items),(v,items[::-1])):
            sequence=[item(root,d) for d in orders[root]]
            starts=[i for i in range(len(sequence)) if sequence[i]!=sequence[i-1]]
            compressed=[sequence[i] for i in starts]
            assert len(compressed)==len(items)
            assert any(compressed==expected[j:]+expected[:j] for j in range(len(items)))
            for interior in (w,z):
                edge_ids=edges[tuple(sorted((root,interior)))]
                assert block_sequence(root,edge_ids)==edge_ids
                assert block_sequence(interior,edge_ids)==edge_ids[::-1]
        def feature(vertex,triple):
            if vertex not in roots:return edge_feature(triple)
            labels=[item(vertex,d) for d in triple]
            if len(set(labels))<3:return edge_feature(triple)
            mask=0
            for a,b in combinations(sorted(labels),2):
                if a:mask^=bit(('branch',a,b))
            return mask

    def oriented(v,triple):
        a,b,c=[position[d] for d in triple]
        return int((a<b<c) or (b<c<a) or (c<a<b))

    xor_mask=xor_rhs=0
    for row in cert['contradiction_rows']:
        v=row['vertex'];triple=row['triple']
        assert v in (0,2) and len(set(triple))==3
        assert all(d in incident[v] for d in triple)
        paired=tuple(sheets[d] for d in triple)
        assert all(d in incident[v^1] for d in paired)
        mask=feature(v,triple)^feature(v^1,paired)
        rhs=1^oriented(v,triple)^oriented(v^1,paired)
        assert (mask,rhs)==(row['mask'],row['rhs'])
        xor_mask^=mask;xor_rhs^=rhs
    assert xor_mask==0 and xor_rhs==1
    return {'status':'PASS','kind':kind,'equations':len(cert['contradiction_rows']),
            'literal_words':cert['words']}


if __name__=='__main__':
    import argparse,json
    from pathlib import Path
    p=argparse.ArgumentParser();p.add_argument('certificates',nargs='+');p.add_argument('--output',required=True)
    args=p.parse_args();results=[verify_certificate(json.loads(Path(x).read_text())) for x in args.certificates]
    Path(args.output).write_text(json.dumps({'status':'PASS','checks':results},indent=2)+'\n')
    print('PASS',len(results),'independent XOR certificates')
