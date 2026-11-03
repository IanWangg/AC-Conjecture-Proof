"""Compile retained barbell-start sampled paths with actual entry moves."""
import argparse
import json
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
for directory in (HERE.parent/'root',HERE.parent/'research_r',HERE.parent/'research_m',HERE.parent/'research_n'):
    sys.path.insert(0,str(directory))
from compile_h_phase_path import compile_path
from elementary_verify import replay
from expose_hidden_primitive import expose
from complete_primitive import complete
from stallings_search import apply

p=argparse.ArgumentParser();p.add_argument('prefix');p.add_argument('--q',required=True);p.add_argument('--n',type=int,default=3)
args=p.parse_args();prefix=Path(args.prefix);path=json.loads(Path(args.prefix+'.path.json').read_text())
start=['x'*args.n+'Y'*(args.n+1),'xyxYXY'];state=tuple(start);moves=[]
for letter in args.q[::-1]:
    move={'op':'conjugate','i':1,'g':letter};moves.append(move);state=apply(state,move)
parent={'format':'ordinary-ac-elementary-v1','start':start,'target':list(state),'moves':moves}
assert parent['target']==path['start'];replay(parent)
cert,result=compile_path(path,parent)
Path(args.prefix+'.strict.json').write_text(json.dumps(cert,indent=2)+'\n')
result['entry_conjugator']=args.q;result['entry_strict_moves']=len(moves)
if Path(args.prefix+'.hit.json').exists():
    hit=json.loads(Path(args.prefix+'.hit.json').read_text())
    assert hit['status']=='PRIMITIVE' and hit['expanded']
    waypoint,details=expose(cert,hit['based_word']);full=complete(waypoint)
    result['hidden_primitive_exposure']=details;result['full_completion_replay']=replay(full)
    Path(args.prefix+'.waypoint.json').write_text(json.dumps(waypoint,indent=2)+'\n')
    Path(args.prefix+'.full.json').write_text(json.dumps(full,indent=2)+'\n')
Path(args.prefix+'.strict_review.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='stages'},indent=2))
