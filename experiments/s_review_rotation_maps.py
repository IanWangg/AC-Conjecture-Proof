"""Independent integer-tuple replay of Q/R's exceptional negative proofs.

No R partial-map, folding, or certificate code is imported. M's earlier
one-fold-at-a-time graph constructor provides an independent refold.
This checks all exceptions, not Q's 24-million direct-DAG enumeration.
"""
import argparse
import base64
from collections import deque
import gzip
import hashlib
import json
from pathlib import Path
from stallings_search import graph as independently_fold

LETTERS='xXyY'
ALPHABETS=('xy','xY','Xy','XY')
SOURCE_SHA='2c8d0ac4c58f590de7151eae3dd09577d2365bf0e858887d801ce24c5c609c8e'


def load_bytes(source):
    path=Path(source);raw=path.read_bytes()
    if path.name.endswith('.gz.b64'):
        return gzip.decompress(base64.b64decode(raw,validate=False))
    if not raw.lstrip().startswith(b'{'):return raw
    manifest=json.loads(raw)
    if 'parts' not in manifest:return raw
    pieces=[]
    for name in manifest['parts']:
        value=(path.parent/name).read_bytes()
        assert hashlib.sha256(value).hexdigest()==manifest['part_sha256'][name]
        pieces.append(value)
    joined=b''.join(pieces)
    assert len(joined)==manifest['encoded_bytes']
    assert hashlib.sha256(joined).hexdigest()==manifest['encoded_sha256']
    decoded=gzip.decompress(base64.b64decode(joined))
    suffix='jsonl' if 'decoded_jsonl_bytes' in manifest else 'json'
    assert len(decoded)==manifest['decoded_'+suffix+'_bytes']
    assert hashlib.sha256(decoded).hexdigest()==manifest['decoded_'+suffix+'_sha256']
    return decoded


def rebase(encoded,base):
    assert len(encoded)%4==0
    n=len(encoded)//4
    assert 0<=base<n
    for vertex in range(n):
        for letter in range(4):
            target=encoded[4*vertex+letter]
            assert type(target)==int and -1<=target<n
            if target>=0:assert encoded[4*target+(letter^1)]==vertex
    order={base:0};queue=deque([base]);out=[]
    while queue:
        at=queue.popleft()
        for target in encoded[4*at:4*at+4]:
            if target>=0 and target not in order:
                order[target]=len(order);queue.append(target)
            out.append(order[target] if target>=0 else -1)
    assert len(order)==n
    return tuple(out)


def closed_maps(certificate,expected_graph):
    assert certificate['format']=='f2-primitive-map-pairs-compact-v1'
    assert tuple(certificate['encoded_graph'])==expected_graph
    n=len(expected_graph)//4
    assert certificate['vertices']==n
    pool=[]
    for entries in certificate['partial_maps_as_sparse_pairs']:
        mapping=[-1]*n;defined=set()
        for position,target in entries:
            assert type(position)==type(target)==int
            assert 0<=position<n and 0<=target<n and position not in defined
            defined.add(position);mapping[position]=target
        pool.append(tuple(mapping))
    names={value:i for i,value in enumerate(pool)}
    assert len(names)==len(pool)
    rows=certificate['alphabets']
    assert tuple(row['alphabet'] for row in rows)==ALPHABETS
    total=0;maximum=0
    for row in rows:
        states={tuple(pair) for pair in row['closed_map_pair_indices']}
        assert len(states)==len(row['closed_map_pair_indices'])
        for pair in states:
            assert len(pair)==2 and all(type(i)==int and 0<=i<len(pool) for i in pair)
        initial=[]
        for letter in row['alphabet']:
            value=tuple(expected_graph[4*at+LETTERS.index(letter)] for at in range(n))
            assert value in names;initial.append(names[value])
        assert tuple(initial) in states
        for first_id,second_id in states:
            first,second=pool[first_id],pool[second_id]
            assert all(at!=end for mapping in (first,second) for at,end in enumerate(mapping))
            # Word UV follows U first, then V. Missing value is -1 here,
            # deliberately differing from R's byte sentinel n.
            product_map=tuple(-1 if first[at]<0 else second[first[at]] for at in range(n))
            assert product_map in names
            product_id=names[product_map]
            assert (first_id,product_id) in states
            assert (product_id,second_id) in states
        total+=len(states);maximum=max(maximum,len(states))
    return total,maximum


def review(source,candidates,proof_manifest):
    source_bytes=load_bytes(source)
    assert hashlib.sha256(source_bytes).hexdigest()==SOURCE_SHA
    catalogue=json.loads(source_bytes)
    raw=load_bytes(candidates);candidate_rows=[json.loads(line) for line in raw.splitlines() if line.strip()]
    manifest=json.loads(Path(proof_manifest).read_bytes())
    assert hashlib.sha256(raw).hexdigest()==manifest['candidate_jsonl_sha256']
    assert len(candidate_rows)==manifest['candidate_records']
    proof_bytes=load_bytes(proof_manifest)
    seen=set();total=maximum=0
    for line in proof_bytes.splitlines():
        row=json.loads(line);index=row['candidate_index']
        assert type(index)==int and 0<=index<len(candidate_rows) and index not in seen
        seen.add(index);candidate=candidate_rows[index]
        original=catalogue[candidate['source_index']]
        assert candidate['source']==original
        assert row['pair']==candidate['pair']
        for actual,cyclic_word in zip(row['pair'],original):
            assert len(actual)==len(cyclic_word) and actual in cyclic_word+cyclic_word
        expected=independently_fold(tuple(row['pair']))[0]
        assert expected==rebase(candidate['graph'],candidate['original_base'])
        count,largest=closed_maps(row['certificate'],expected)
        total+=count;maximum=max(maximum,largest)
    assert seen==set(range(len(candidate_rows)))
    assert total==manifest['finite_map_pair_states']
    return dict(status='PASS',ordinary_AC_goal_solved=False,
                source_catalogue_sha256=SOURCE_SHA,
                candidate_jsonl_sha256=hashlib.sha256(raw).hexdigest(),
                proof_jsonl_sha256=hashlib.sha256(proof_bytes).hexdigest(),
                exception_records_checked=len(seen),
                closed_integer_tuple_map_pair_states_checked=total,
                maximum_pair_states_per_graph_alphabet=maximum,
                all_exception_pairs_independently_refolded=True,
                all_source_indices_and_rotation_memberships_verified=True,
                imports_R_map_or_certificate_code=False,
                Q_full_direct_DAG_enumeration_replayed_in_this_review=False,
                scope='Independent exception proof replay plus mathematical Q/R review; no AC solution')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('catalogue');parser.add_argument('candidates');parser.add_argument('proof_manifest')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    result=review(args.catalogue,args.candidates,args.proof_manifest)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
