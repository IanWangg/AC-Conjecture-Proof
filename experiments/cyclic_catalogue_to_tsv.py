"""Format-only JSON-to-TSV adapter for the independent C++ closure audit."""
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('target')
    args=parser.parse_args()
    raw=Path(args.source).read_bytes()
    if args.source.endswith('.gz.b64'):
        raw=gzip.decompress(base64.b64decode(raw))
    states=json.loads(raw)
    assert isinstance(states,list)
    for pair in states:
        assert isinstance(pair,list) and len(pair)==2
        assert all(isinstance(w,str) and w and set(w)<=set('xXyY') for w in pair)
    tsv=''.join(a+'\t'+b+'\n' for a,b in states).encode()
    Path(args.target).write_bytes(tsv)
    print(json.dumps({'rows':len(states),'source_sha256':hashlib.sha256(raw).hexdigest(),
                      'tsv_sha256':hashlib.sha256(tsv).hexdigest()}))
