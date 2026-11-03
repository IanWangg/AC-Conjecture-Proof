"""Independently validate V's raw initial-H Farey source corpus.

Regenerates every retained source using only strict coordinate Nielsen
operations; compares all source cyclic classes to T's matrix enumeration.
Can compile a selected rotated candidate's actual entry prefix.
"""
import argparse
import hashlib
import json
from pathlib import Path
from nielsen_basis_classes import canonical,cyclic,enumerate_classes,inverse,reduce,length,read_payload
from elementary_verify import replay


def source_prefix(n,signs,program):
    start=['x'*n+'Y'*(n+1),'xyxYXY'];state=list(start);moves=[]
    columns=[[signs[0],0],[0,signs[1]]]
    energies=[sum(map(lambda w:len(cyclic(w)),state))]
    def emit(op,i,**kw):
        moves.append(dict(op=op,i=i,**kw))
        if op=='invert':state[i]=inverse(state[i])
        elif op=='multiply':state[i]=reduce(state[i]+state[kw['j']])
        else:state[i]=reduce(kw['g']+state[i]+inverse(kw['g']))
        energies.append(sum(len(cyclic(w)) for w in state))
    for i,s in enumerate(signs):
        assert s in (-1,1)
        if s<0:emit('invert',i)
    boundary=[sum(len(cyclic(w)) for w in state)]
    for letter in program:
        if letter=='L':
            emit('invert',1);emit('invert',0);emit('multiply',1,j=0)
            emit('invert',1);emit('invert',0)
            columns[1]=[a+b for a,b in zip(*columns)]
        elif letter=='R':
            emit('multiply',0,j=1)
            columns[0]=[a+b for a,b in zip(*columns)]
        else:raise ValueError('invalid Farey operation')
        e=sum(len(cyclic(w)) for w in state)
        assert e==sum(length(n,*v) for v in columns)
        assert e>boundary[-1]
        boundary.append(e)
    cert={'format':'ordinary-ac-elementary-v1','start':start,'target':state,
          'moves':moves,'scope':'Actual initial-H Nielsen prelude; no conjugation inserted'}
    return cert,columns,energies


def candidate_prefix(n,row):
    cert,columns,energies=source_prefix(n,row['signs'],row['basis_program'])
    assert cert['target']==row['raw_basis']
    state=list(cert['target'])
    def emit(op,i,**kw):
        cert['moves'].append(dict(op=op,i=i,**kw))
        if op=='invert':state[i]=inverse(state[i])
        else:state[i]=reduce(kw['g']+state[i]+inverse(kw['g']))
    for i,target in enumerate(row['pair']):
        while len(state[i])>1 and state[i][0]==state[i][-1].swapcase():
            emit('conjugate',i,g=state[i][0].swapcase())
        choices=[]
        for flip in (0,1):
            w=inverse(state[i]) if flip else state[i]
            for cut in range(len(w)):
                if w[cut:]+w[:cut]==target:choices.append((flip+cut,flip,w[:cut]))
        _,flip,prefix=min(choices)
        if flip:emit('invert',i)
        for c in prefix:emit('conjugate',i,g=c.swapcase())
        assert state[i]==target
    cert['target']=state
    cert['scope']='Actual Nielsen prelude plus specified independent rotations'
    return cert,replay(cert)


def audit(source,n,cap):
    raw=read_payload(source);rows=[json.loads(l) for l in raw.splitlines() if l.strip()]
    expected,enumeration=enumerate_classes(n,cap)
    actual=set();total=0;maxraw=maxcyc=0
    for index,row in enumerate(rows):
        assert row['source_index']==index
        cert,columns,energies=source_prefix(n,row['signs'],row['basis_program'])
        assert columns==row['matrix_columns']
        assert cert['target']==row['raw_basis']
        assert list(map(cyclic,cert['target']))==row['cyclic_basis']
        assert sum(len(w) for w in row['cyclic_basis'])==row['cyclic_energy']
        assert max(energies)<=cap
        checked=replay(cert)
        total+=checked['moves'];maxraw=max(maxraw,checked['peak_total_length']);maxcyc=max(maxcyc,max(energies))
        actual.add(tuple(sorted(map(canonical,row['cyclic_basis']))))
    assert actual==set(expected),{'missing':len(set(expected)-actual),'extra':len(actual-set(expected))}
    assert len(actual)==len(rows)
    return {'status':'PASS','ordinary_AC_goal_solved':False,'n':n,'endpoint_cyclic_cap':cap,
            'source_jsonl_sha256':hashlib.sha256(raw).hexdigest(),
            'source_transport_sha256':hashlib.sha256(Path(source).read_bytes()).hexdigest(),
            'actual_raw_basis_programs_independently_regenerated':len(rows),
            'strict_Nielsen_only_source_moves_replayed':total,
            'maximum_strict_raw_source_peak':maxraw,'maximum_cyclic_source_peak':maxcyc,
            'all_source_family_keys_equal_independent_matrix_enumeration':True,
            'source_corpus_contains_no_intermediate_independent_conjugations':True,
            'matrix_enumeration':enumeration,
            'scope':'Source coverage and actual initial-H basis provenance only; downstream primitive exclusions belong to V/U'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('source');parser.add_argument('--n',type=int,default=3)
    parser.add_argument('--cap',type=int,default=120);parser.add_argument('--candidate-index',type=int)
    parser.add_argument('--certificate');parser.add_argument('--output',required=True)
    args=parser.parse_args()
    if args.candidate_index is None:result=audit(args.source,args.n,args.cap)
    else:
        row=[json.loads(l) for l in read_payload(args.source).splitlines() if l.strip()][args.candidate_index]
        cert,result=candidate_prefix(args.n,row)
        assert args.certificate
        Path(args.certificate).write_text(json.dumps(cert,indent=2)+'\n')
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
