import argparse
from collections import Counter
import json
from pathlib import Path
import random
import subprocess
from planar_link_parity import decide,model
from thickening_rotations import analyse_orders

p=argparse.ArgumentParser();p.add_argument('--binary',required=True);p.add_argument('--prefix',required=True);args=p.parse_args()
rng=random.Random(20261102)
cases=[('x','y'),('xyXY','xyXY'),('xx','yy'),('xxYYY','xxxYYYY'),('xxxYYYY','xyxYXY')]
for _ in range(1000):
    words=[]
    for _ in range(2):
        n=rng.randrange(1,6)
        while True:
            w=''
            for _ in range(n):
                w+=rng.choice([c for c in 'xXyY' if not w or c!=w[-1].swapcase()])
            if w[0]!=w[-1].swapcase():break
        words.append(w)
    cases.append(tuple(words))
source=Path(args.prefix+'.tsv');target=Path(args.prefix+'.jsonl')
source.write_text(''.join('\t'.join(words)+'\n' for words in cases))
subprocess.run([args.binary,'--batch',str(source),str(target),'2000000'],check=True)
results=[json.loads(line) for line in target.read_text().splitlines()]
counts=Counter();kind_counts=Counter();certificates=0
for words,native in zip(cases,results):
    assert list(words)==native['words']
    result=decide(words);counts[(native['status'],result['status'])]+=1
    if result['status']!='NOT_SUPPORTED':kind_counts[(result['kind'],native['status'])]+=1
    if native['status']=='PLANAR_COMPATIBLE':
        assert result['status']!='PARITY_OBSTRUCTION'
        detail=analyse_orders(words,native['best_orders'])
        assert detail['total_genus']==0
        certificates+=1
    if result['status']=='PARITY_OBSTRUCTION':
        assert native['status']!='PLANAR_COMPATIBLE'
        mask=rhs=0
        for row in result['contradiction_rows']:
            mask^=row['mask'];rhs^=row['rhs']
        assert mask==0 and rhs==1
summary={'status':'PASS','seed':20261102,'cases':len(cases),'verified_native_positive_witnesses':certificates,
         'outcome_counts':[{'native':a,'parity':b,'count':n} for (a,b),n in sorted(counts.items())],
         'model_counts':[{'model':a,'native':b,'count':n} for (a,b),n in sorted(kind_counts.items())]}
Path(args.prefix+'_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
