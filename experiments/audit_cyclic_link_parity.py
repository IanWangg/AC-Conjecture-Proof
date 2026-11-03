"""Construct and independently verify parity exclusions for an exact TSV.

For the theorem in the report, input is the already independently audited
258032-state C22 catalogue reconstructed from its published manifest.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import time
from planar_link_parity import decide
from verify_link_parity import verify_certificate

p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--output',required=True)
p.add_argument('--expected-source-sha256',default='cd9ba5781a1efcb1bf1b8a72c9a392b79de1cd915da6a520b8f33a4390787fa3')
args=p.parse_args();raw=Path(args.input).read_bytes();source_hash=hashlib.sha256(raw).hexdigest()
assert source_hash==args.expected_source_sha256
started=time.monotonic();counts=Counter();digest=hashlib.sha256();total=0;witness_count=0
for total,row in enumerate(raw.decode().splitlines(),1):
    words=row.split('\t');cert=decide(words)
    assert cert['status']=='PARITY_OBSTRUCTION',cert
    review=verify_certificate(cert);assert review['status']=='PASS'
    counts[cert['kind']]+=1;witness_count+=review['equations']
    digest.update((json.dumps(cert,sort_keys=True,separators=(',',':'))+'\n').encode())
    if total%10000==0:print(total,dict(counts),flush=True)
result={'status':'PASS','literal_cyclic_tuples':total,'model_counts':dict(counts),
        'independently_verified_XOR_equations':witness_count,
        'source_tsv_sha256':source_hash,'certificate_stream_sha256':digest.hexdigest(),
        'seconds':time.monotonic()-started,'ordinary_AC_goal_solved':False,
        'scope':'No orientable compatible planar link for these literal cyclic tuples; no all-tail or global AC invariant asserted'}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
