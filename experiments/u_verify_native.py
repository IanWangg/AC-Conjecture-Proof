"""Independent integer-tuple checks for U's native decision records.

No C++ detector code or R map/composition routine is imported.
"""
import json
from collections import deque

LETTERS='xXyY'


def inverse(w):return w.swapcase()[::-1]


def reduce(w):
    out=[]
    for c in w:
        assert c in LETTERS
        if out and out[-1]==c.swapcase():out.pop()
        else:out.append(c)
    return ''.join(out)


def graph(record):
    encoded=record['graph'];assert encoded and len(encoded)%4==0
    n=len(encoded)//4
    assert record['vertices']==n
    for i,end in enumerate(encoded):
        assert type(end)==int and -1<=end<n
        if end>=0:assert encoded[4*end+((i%4)^1)]==i//4
    seen={0};todo=deque([0])
    while todo:
        vertex=todo.popleft()
        for end in encoded[4*vertex:4*vertex+4]:
            if end>=0 and end not in seen:seen.add(end);todo.append(end)
    assert len(seen)==n
    return encoded,n


def follow(encoded,start,w):
    for c in w:
        if start<0:return -1
        start=encoded[4*start+LETTERS.index(c)]
    return start


def verify_absence(record):
    assert record['status']=='ABSENT'
    encoded,n=graph(record);stride=n+1;total=0
    assert [row['alphabet'] for row in record['alphabets']]==['xy','xY','Xy','XY']
    for row in record['alphabets']:
        assert row['status']=='ABSENT'
        pairs={tuple(v) for v in row['closed_total_map_pairs']}
        assert len(pairs)==len(row['closed_total_map_pairs'])==row['discovered']==row['processed']
        initial=[]
        for c in row['alphabet']:
            initial.extend(n if encoded[4*v+LETTERS.index(c)]<0 else encoded[4*v+LETTERS.index(c)] for v in range(n))
            initial.append(n)
        assert tuple(initial) in pairs
        for pair in pairs:
            assert len(pair)==2*stride and all(type(v)==int and 0<=v<=n for v in pair)
            a,b=pair[:stride],pair[stride:]
            assert a[n]==b[n]==n
            assert all(a[v]!=v and b[v]!=v for v in range(n))
            ab=tuple(b[a[v]] for v in range(stride))
            assert a+ab in pairs and ab+b in pairs
        total+=len(pairs)
    assert total==record['pair_states']
    return total


def verify_positive(record):
    assert record['status']=='PRIMITIVE'
    encoded,n=graph(record);w=record['witness']
    assert w['alphabet'] in ('xy','xY','Xy','XY') and w['component'] in (0,1)
    a,b=w['alphabet']
    for op in w['program']:
        if op=='L':b=a+b
        elif op=='R':a=a+b
        else:raise AssertionError('invalid positive Nielsen program')
    assert w['expanded'] and w['cyclic_word']==(a,b)[w['component']]
    assert 0<=w['vertex']<n
    assert follow(encoded,0,w['base_path'])==w['vertex']
    assert follow(encoded,w['vertex'],w['cyclic_word'])==w['vertex']
    based=reduce(w['base_path']+w['cyclic_word']+inverse(w['base_path']))
    assert based==w['based_word'] and follow(encoded,0,based)==0
    return based


def verify(record):
    if record['status']=='ABSENT':return {'status':'PASS','closed_states':verify_absence(record)}
    if record['status']=='PRIMITIVE':return {'status':'PASS','primitive_word':verify_positive(record)}
    assert record['status']=='INCOMPLETE'
    return {'status':'INCOMPLETE','negative_conclusion_accepted':False}


if __name__=='__main__':
    import argparse
    from pathlib import Path
    parser=argparse.ArgumentParser();parser.add_argument('decisions');parser.add_argument('--output')
    args=parser.parse_args();content=Path(args.decisions).read_text()
    try:
        parsed=json.loads(content);rows=parsed if isinstance(parsed,list) else [parsed]
    except json.JSONDecodeError:
        rows=[json.loads(line) for line in content.splitlines() if line.strip()]
    reports=[verify(row) for row in rows]
    out={'records_checked':len(rows),'closed_states_checked':sum(r.get('closed_states',0) for r in reports),
         'positive_witnesses_checked':sum('primitive_word' in r for r in reports),
         'incomplete_records':sum(r['status']=='INCOMPLETE' for r in reports),'ordinary_AC_goal_solved':False}
    content=json.dumps(out,indent=2)+'\n'
    if args.output:Path(args.output).write_text(content)
    print(content,end='')
