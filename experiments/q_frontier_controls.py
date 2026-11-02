"""Compile and strictly replay every saved distance-two bridge macro.

Word arithmetic/replay comes from the independent elementary verifier.
Input records are Q's stated finite frontier, not a whole cap23 component.
"""
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path
from cyclic_catalogue_to_tsv import load_catalogue_bytes
from elementary_verify import reduce,inverse,replay


def cyclic(w):
    w=reduce(w)
    while len(w)>1 and w[0]==w[-1].swapcase():w=w[1:-1]
    return w


def canonical(w):
    w=cyclic(w)
    return min(v[i:]+v[:i] for v in (w,inverse(w)) for i in range(len(v))) if w else ''


def cyclic_peak(certificate):
    state=list(certificate['start'])
    peak=sum(len(cyclic(w)) for w in state)
    for move in certificate['moves']:
        i=move['i']
        if move['op']=='invert':state[i]=inverse(state[i])
        elif move['op']=='multiply':state[i]=reduce(state[i]+state[move['j']])
        else:state[i]=reduce(move['g']+state[i]+inverse(move['g']))
        peak=max(peak,sum(len(cyclic(w)) for w in state))
    assert state==certificate['target']
    return peak


def macro(row):
    state=list(row['source'])
    moves=[]
    def emit(op,i,**kw):
        moves.append(dict(op=op,i=i,**kw))
        if op=='invert':state[i]=inverse(state[i])
        elif op=='multiply':state[i]=reduce(state[i]+state[kw['j']])
        else:state[i]=reduce(kw['g']+state[i]+inverse(kw['g']))
    def normalize(i,target):
        while len(state[i])>1 and state[i][0]==state[i][-1].swapcase():
            emit('conjugate',i,g=state[i][0].swapcase())
        options=[]
        for flip in (0,1):
            w=inverse(state[i]) if flip else state[i]
            for cut in range(len(w)):
                if w[cut:]+w[:cut]==target:options.append((flip+cut,flip,w[:cut]))
        _,flip,prefix=min(options)
        if flip:emit('invert',i)
        for c in prefix:emit('conjugate',i,g=c.swapcase())
        assert state[i]==target
    i=row['recipient']
    j=1-i
    normalize(i,row['receiver_rotation'])
    normalize(j,row['donor_rotation'])
    assert len(row['bridge'])==2 and reduce(row['bridge'])==row['bridge']
    for g in reversed(row['bridge']):emit('conjugate',j,g=g)
    emit('multiply',i,j=j)
    normalize(i,canonical(state[i]))
    normalize(j,row['source'][j])
    assert sorted(state)==row['state']
    certificate={'format':'ordinary-ac-elementary-v1','start':row['source'],
                 'target':state,'moves':moves,
                 'scope':'One explicit distance-two bridge edge from the stated source; not a basis'}
    result=replay(certificate)
    assert result['peak_total_length']==27
    assert sum(map(len,state))==23
    return certificate,result


def run(source,frontier,entry=None):
    catalogue_bytes=load_catalogue_bytes(source)
    catalogue=json.loads(catalogue_bytes)
    raw=Path(frontier).read_bytes()
    if str(frontier).endswith('.gz.b64'):raw=gzip.decompress(base64.b64decode(raw))
    rows=[json.loads(line) for line in raw.splitlines()]
    states=set()
    total_moves=0
    first=None
    for row in rows:
        assert catalogue[row['source_index']]==row['source']
        certificate,result=macro(row)
        total_moves+=result['moves']
        assert tuple(row['state']) not in states
        states.add(tuple(row['state']))
        if first is None:first=certificate
    full=None
    if entry:
        prefix=json.loads(Path(entry).read_text())
        replay(prefix)
        assert prefix['start']==['xxxYYYY','xyxYXY']
        if prefix['target']==first['start']:
            extension=first['moves']
            target=first['target']
        else:
            assert prefix['target']==first['start'][::-1]
            extension=[dict(move,i=1-move['i'],**({'j':1-move['j']} if 'j' in move else {})) for move in first['moves']]
            target=first['target'][::-1]
        full={'format':prefix['format'],'start':prefix['start'],'target':target,
              'moves':prefix['moves']+extension,
              'scope':'Exact AK3 path to a stated cyclic-energy23 frontier word pair; not a basis'}
        full_result=replay(full)
        full_result['cyclic_peak_total_length']=cyclic_peak(full)
    else:full_result=None
    return {'status':'PASS','ordinary_AC_goal_solved':False,
            'source_decoded_json_sha256':hashlib.sha256(catalogue_bytes).hexdigest(),
            'frontier_jsonl_sha256':hashlib.sha256(raw).hexdigest(),
            'strict_bridge_macros_replayed':len(rows),
            'total_strict_macro_moves_replayed':total_moves,
            'every_macro_raw_peak':27,'every_endpoint_cyclic_energy':23,
            'first_source':first['start'],'full_AK3_example_replay':full_result},full


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source_manifest')
    parser.add_argument('frontier_jsonl')
    parser.add_argument('--entry-certificate')
    parser.add_argument('--full-certificate')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    result,certificate=run(args.source_manifest,args.frontier_jsonl,args.entry_certificate)
    if args.full_certificate:
        assert certificate
        Path(args.full_certificate).write_text(json.dumps(certificate,indent=2)+'\n')
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
