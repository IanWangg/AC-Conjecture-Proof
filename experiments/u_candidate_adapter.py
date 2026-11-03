"""Format-only adapter from Q/V candidate JSONL to native detector TSV."""
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path


def adapt(source,target):
    raw=Path(source).read_bytes()
    if str(source).endswith('.gz.b64'):
        raw=gzip.decompress(base64.b64decode(raw))
    rows=[json.loads(line) for line in raw.splitlines() if line.strip()]
    output=[]
    for index,row in enumerate(rows):
        a,b=row['pair']
        assert all(isinstance(w,str) and set(w)<=set('xXyY') for w in (a,b))
        graph=row['graph']
        assert len(graph)%4==0 and all(type(v)==int for v in graph)
        # Candidate corpora carry an original base; based fold samples use 0.
        output.append(f'{index}\t{a}\t{b}\t{row.get("original_base",0)}\t'+','.join(map(str,graph))+'\n')
    encoded=''.join(output).encode()
    Path(target).write_bytes(encoded)
    return {'records':len(rows),'source_sha256':hashlib.sha256(raw).hexdigest(),
            'tsv_sha256':hashlib.sha256(encoded).hexdigest()}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('source');parser.add_argument('target')
    args=parser.parse_args();print(json.dumps(adapt(args.source,args.target)))
