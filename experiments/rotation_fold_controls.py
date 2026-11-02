"""Independently compare Q's C++ fold/key/DAG with M and O implementations.

All scripts are installed together under experiments/ in the repository.
Controls validate conventions; the proof of the reduction is in Q's report.
"""
import argparse
from collections import deque
import json
from pathlib import Path
import random
import subprocess
import tempfile
from cyclic_catalogue_to_tsv import load_catalogue_bytes
from stallings_search import graph
import arbitrary_tail_certificate as ac


def unbased(encoded):
    size=len(encoded)//4
    branches=[v for v in range(size) if sum(w>=0 for w in encoded[4*v:4*v+4])>=3]
    assert len(branches) in (1,2)
    codes=[]
    for base in branches:
        names={base:0}
        queue=deque([base])
        code=[]
        while queue:
            v=queue.popleft()
            for w in encoded[4*v:4*v+4]:
                if w<0:code.append(-1)
                else:
                    if w not in names:
                        names[w]=len(names)
                        queue.append(w)
                    code.append(names[w])
        assert len(names)==size
        codes.append(tuple(code))
    return min(codes)


def run(source,binary):
    data=json.loads(load_catalogue_bytes(source))
    rng=random.Random(749821)
    pairs=[('x','y'),('xxY','xyxYXY')]
    for _ in range(5000):
        a,b=rng.choice(data)
        i,j=rng.randrange(len(a)),rng.randrange(len(b))
        pairs.append((a[i:]+a[:i],b[j:]+b[:j]))
    with tempfile.TemporaryDirectory(prefix='q-fold-controls-') as folder:
        src=Path(folder)/'input.tsv'
        dst=Path(folder)/'output.jsonl'
        src.write_text(''.join(a+'\t'+b+'\n' for a,b in pairs))
        subprocess.run([str(Path(binary).resolve()),'--folds',str(src),str(dst)],check=True)
        records=[json.loads(line) for line in dst.read_text().splitlines()]
    assert len(records)==len(pairs)
    dag=0
    for pair,row in zip(pairs,records):
        encoded=graph(pair)[0]  # M's one-fold-at-a-time implementation.
        assert unbased(encoded)==tuple(row['graph'])
        try:
            ac.orders(encoded)  # O's independent line-graph/topological test.
            expected=True
        except AssertionError:
            expected=False
        assert row['DAG_proves_primitive_absence']==expected
        dag+=expected
        base=row['original_base']
        for word in pair:
            at=base
            for c in word:
                at=row['graph'][4*at+'xXyY'.index(c)]
                assert at>=0
            assert at==base
    assert not records[0]['DAG_proves_primitive_absence']
    assert not records[1]['DAG_proves_primitive_absence']
    return {'status':'PASS','ordinary_AC_goal_solved':False,
            'source_pairs':len(data),'independently_folded_pairs':len(pairs),
            'deterministic_random_seed':749821,
            'C++_fold_and_unbased_key_match_M_fold':True,
            'C++_DAG_matches_O_topological_test':True,
            'DAG_primitive_absence_controls':dag,
            'primitive_containing_positive_controls_rejected':2,
            'every_actual_pair_accepted_at_recorded_original_base':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('catalogue')
    parser.add_argument('binary')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    result=run(args.catalogue,args.binary)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
