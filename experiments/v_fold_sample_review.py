"""Independently refold deterministic final-source rotation samples."""
import hashlib,json,random,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'research_r'))
from primitive_map_pairs import fold

def generate(source,target):
    rng=random.Random(2718281828)
    sources=[json.loads(s) for s in Path(source).read_text().splitlines()]
    pairs=[]
    for row in sources:
        u,v=row['cyclic_basis']
        for _ in range(3):
            a,b=rng.randrange(len(u)),rng.randrange(len(v))
            pairs.append((u[a:]+u[:a],v[b:]+v[:b]))
    Path(target).write_text(''.join(a+'\t'+b+'\n' for a,b in pairs))

def review(source,graphs,target):
    rows=[json.loads(s) for s in Path(graphs).read_text().splitlines()]
    for row in rows:
        assert list(fold(row['pair']))==row['graph']
        assert row['DAG_proves_primitive_absence']
    result=dict(status='PASS',ordinary_AC_goal_solved=False,
        independently_refolded_rotation_pairs=len(rows),
        maximum_graph_vertices=max(len(row['graph'])//4 for row in rows),
        source_jsonl_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest(),
        sample_graph_jsonl_sha256=hashlib.sha256(Path(graphs).read_bytes()).hexdigest(),
        scope='Independent R batch-identification folds agree exactly with extended Q folds on three deterministic rotations per source; sample only.')
    Path(target).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':
    if sys.argv[1]=='generate':generate(*sys.argv[2:])
    else:review(*sys.argv[2:])
