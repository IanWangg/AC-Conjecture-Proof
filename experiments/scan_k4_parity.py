import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import time
from k4_rotation_parity import decide

p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--prefix',required=True);p.add_argument('--limit',type=int,default=0);p.add_argument('--general',action='store_true')
args=p.parse_args();start=time.monotonic();counts=Counter();digest=hashlib.sha256();rows=Path(args.input).read_text().splitlines()
if args.general:
    from planar_link_parity import decide
if args.limit:rows=rows[:args.limit]
exceptions=[];witness_rows=0
for i,row in enumerate(rows):
    result=decide(row.split('\t'));counts[result['status']]+=1
    if result['status']=='PARITY_OBSTRUCTION':
        witness_rows+=len(result['contradiction_rows'])
        bits=rhs=0
        for equation in result['contradiction_rows']:
            bits^=equation['mask'];rhs^=equation['rhs']
        assert bits==0 and rhs==1
    else:
        exceptions.append({'source_index':i,**result})
    digest.update((json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode())
    if i%10000==9999:print(i+1,dict(counts),flush=True)
summary={'status':'COMPLETE_SPECIFIED_ROWS','input_rows':len(rows),'counts':dict(counts),
         'source_sha256':hashlib.sha256(Path(args.input).read_bytes()).hexdigest(),
         'logical_result_stream_sha256':digest.hexdigest(),'contradiction_equations_total':witness_rows,
         'seconds':time.monotonic()-start,'ordinary_AC_goal_solved':False}
Path(args.prefix+'_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
Path(args.prefix+'_exceptions.json').write_text(json.dumps(exceptions,indent=2)+'\n')
print(json.dumps(summary,indent=2))
