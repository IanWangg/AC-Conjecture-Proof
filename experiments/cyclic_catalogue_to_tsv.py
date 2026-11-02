"""Format-only JSON-to-TSV adapter for the independent C++ closure audit."""
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path


def load_catalogue_bytes(source):
    """Read JSON, one gzip/base64 file, or a hash-verified split manifest."""
    path=Path(source)
    raw=path.read_bytes()
    if str(path).endswith('.gz.b64'):
        return gzip.decompress(base64.b64decode(raw))
    if not raw.lstrip().startswith(b'{'):
        return raw
    manifest=json.loads(raw)
    if manifest.get('format')!='ac-cyclic-component-gzip-base64-parts-v1':
        raise ValueError('unsupported catalogue manifest')
    chunks=[]
    for name in manifest['parts']:
        chunk=(path.parent/name).read_bytes()
        if hashlib.sha256(chunk).hexdigest()!=manifest['part_sha256'][name]:
            raise ValueError('compressed catalogue part hash mismatch: '+name)
        chunks.append(chunk)
    encoded=b''.join(chunks)
    if len(encoded)!=manifest['encoded_bytes'] or hashlib.sha256(encoded).hexdigest()!=manifest['encoded_sha256']:
        raise ValueError('assembled compressed catalogue mismatch')
    decoded=gzip.decompress(base64.b64decode(encoded))
    if len(decoded)!=manifest['decoded_json_bytes'] or hashlib.sha256(decoded).hexdigest()!=manifest['decoded_json_sha256']:
        raise ValueError('decoded catalogue mismatch')
    return decoded


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('target')
    args=parser.parse_args()
    raw=load_catalogue_bytes(args.source)
    states=json.loads(raw)
    assert isinstance(states,list)
    for pair in states:
        assert isinstance(pair,list) and len(pair)==2
        assert all(isinstance(w,str) and w and set(w)<=set('xXyY') for w in pair)
    tsv=''.join(a+'\t'+b+'\n' for a,b in states).encode()
    Path(args.target).write_bytes(tsv)
    print(json.dumps({'rows':len(states),'source_sha256':hashlib.sha256(raw).hexdigest(),
                      'tsv_sha256':hashlib.sha256(tsv).hexdigest()}))
