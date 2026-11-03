"""Y's independent rotation-source coverage and actual-entry audit.

Imports no X/V/T graph or AC code. This does not recheck the weighted
kernel certificates; T separately audits those. It refolds all 42 literal
source pairs, checks complete offset and vertex-pair coverage, and emits
strict actual AK3 entries with only single-generator conjugations.
"""
import argparse
import base64
from collections import Counter,deque
import gzip
import hashlib
from itertools import combinations,product
import json
from pathlib import Path

LETTERS='xXyY'
START=['xxxYYYY','xyxYXY']


def read_payload(path):
    raw=Path(path).read_bytes()
    if str(path).endswith('.b64'):raw=base64.b64decode(raw)
    return gzip.decompress(raw) if raw.startswith(b'\x1f\x8b') else raw


def inverse(word):return word.swapcase()[::-1]


def reduce(word):
    out=[]
    for c in word:
        assert c in LETTERS
        if out and out[-1]==c.swapcase():out.pop()
        else:out.append(c)
    return ''.join(out)


def fold_words(words):
    edges=[];vertices=1
    for word in words:
        at=0
        for i,letter in enumerate(word):
            end=0 if i+1==len(word) else vertices
            if end:vertices+=1
            c=LETTERS.index(letter);edges.extend(((at,c,end),(end,c^1,at)));at=end
    representative=list(range(vertices))
    def root(v):
        while representative[v]!=v:
            representative[v]=representative[representative[v]];v=representative[v]
        return v
    while True:
        seen={};changed=False
        for v,c,w in edges:
            v,w=root(v),root(w)
            if (v,c) in seen:
                other=root(seen[v,c])
                if other!=w:representative[max(other,w)]=min(other,w);changed=True
            else:seen[v,c]=w
        if not changed:break
    arcs={(root(v),c):root(w) for v,c,w in edges}
    names={root(0):0};queue=deque([root(0)]);encoded=[]
    while queue:
        v=queue.popleft()
        for c in range(4):
            w=arcs.get((v,c),-1)
            if w>=0 and w not in names:names[w]=len(names);queue.append(w)
            encoded.append(names[w] if w>=0 else -1)
    for v in range(len(encoded)//4):
        for c in range(4):
            if (w:=encoded[4*v+c])>=0:assert encoded[4*w+(c^1)]==v
    assert sum(w>=0 for w in encoded)//2-len(encoded)//4+1==2
    return encoded


def entry(offsets):
    state=list(START);moves=[];peak=sum(map(len,state))
    for coordinate,cut in enumerate(offsets):
        word=START[coordinate]
        # Prefix cancellation performs a left rotation; a shorter suffix
        # conjugator performs the same rotation by moving letters right.
        letters=(c.swapcase() for c in word[:cut]) if cut<=len(word)-cut else reversed(word[cut:])
        for letter in letters:
            moves.append(dict(op='conjugate',i=coordinate,g=letter))
            state[coordinate]=reduce(letter+state[coordinate]+inverse(letter))
            peak=max(peak,sum(map(len,state)))
    target=[w[c:]+w[:c] for w,c in zip(START,offsets)]
    assert state==target and peak==13
    assert len(moves)==sum(min(c,len(w)-c) for w,c in zip(START,offsets))
    return dict(format='ordinary-ac-elementary-v1',start=list(START),target=target,moves=moves),peak


def replay(certificate):
    state=list(certificate['start']);peak=sum(map(len,state))
    for move in certificate['moves']:
        assert move['op']=='conjugate' and move['i'] in (0,1) and len(move['g'])==1 and move['g'] in LETTERS
        i,g=move['i'],move['g'];state[i]=reduce(g+state[i]+inverse(g));peak=max(peak,sum(map(len,state)))
    assert state==certificate['target']
    return len(certificate['moves']),peak


def audit(source):
    raw=read_payload(source);data=json.loads(raw)
    expected=set(product(range(7),range(6)));seen=set();pairs=set();vertex_histogram=Counter();moves_histogram=Counter();entries=[]
    identifications=total_moves=0
    for record in data['records']:
        offsets=tuple(record['rotation_offsets']);assert offsets in expected and offsets not in seen;seen.add(offsets)
        target=[w[c:]+w[:c] for w,c in zip(START,offsets)]
        assert tuple(target) not in pairs;pairs.add(tuple(target))
        original=record['identification_data'];assert original['original_pair']==target
        graph=fold_words(target);assert graph==original['original_graph']
        n=len(graph)//4;vertex_histogram[n]+=1
        expected_identifications=set(combinations(range(n),2))
        actual=[tuple(r['identified_vertices']) for r in original['records']]
        certificates=[tuple(r['identified_vertices']) for r in record['cycle_certificates']['results']]
        assert len(actual)==len(set(actual)) and set(actual)==expected_identifications
        assert len(certificates)==len(set(certificates)) and set(certificates)==expected_identifications
        assert record['status']=='PASS' and record['independent_audit']['status']=='PASS'
        assert all(r['rank']==3 for r in original['records'])
        identifications+=len(actual)
        certificate,peak=entry(offsets);count,second_peak=replay(certificate);assert peak==second_peak
        entries.append(dict(rotation_offsets=list(offsets),certificate=certificate,moves=count,raw_peak=peak))
        total_moves+=count;moves_histogram[count]+=1
    assert seen==expected and len(pairs)==42 and identifications==2272 and total_moves==135
    return dict(status='PASS',ordinary_AC_goal_solved=False,
                source_decoded_sha256=hashlib.sha256(raw).hexdigest(),literal_rotation_pairs=42,
                all_offsets_exactly_once=True,source_graphs_independently_folded=42,
                source_graph_vertex_histogram=dict(sorted(vertex_histogram.items())),
                complete_vertex_pair_index_coverage=identifications,
                actual_strict_entry_ledgers=len(entries),total_entry_conjugations=total_moves,
                maximum_entry_moves=max(moves_histogram),maximum_raw_entry_peak=13,
                entry_move_histogram=dict(sorted(moves_histogram.items())),
                weighted_kernel_inequalities_rechecked_here=False,
                independence='No imports from X/V/T graph or AC code; exact literal folds and conjugation-only replay',
                scope='Finite source/entry coverage and restricted endpoint-intersection phase proof; no unrestricted AC invariant'),entries


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('source');parser.add_argument('--output',required=True);parser.add_argument('--entries',required=True);args=parser.parse_args()
    result,entries=audit(args.source)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');Path(args.entries).write_text(json.dumps(entries,indent=2)+'\n')
    print(json.dumps(result,indent=2))
