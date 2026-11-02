"""Compile exact one-relator rewrites by short rotations of both coordinates.

Returned ledgers are strict ordinary AC paths. The bounded rewrite searches
are only a discovery device; no exhaustion or optimal-peak claim is made.
"""
import argparse
from collections import deque
import json
from pathlib import Path
from elementary_verify import inverse,reduce,replay

P='xxxYYYY'; B='xyxYXY'; BP='XXyxYxxY'


def find_path(start,target,relator,cap,budget=100000):
    patterns=[]
    for base,sign in ((relator,1),(inverse(relator),-1)):
        for k in range(len(base)):
            rotated=base[k:]+base[:k]
            for cut in range(len(base)+1):
                patterns.append((rotated[:cut],inverse(rotated[cut:]),sign,base[:k]))
    parents={start:None}
    queue=deque([start])
    while queue and len(parents)<=budget:
        current=queue.popleft()
        if current==target:
            path=[];at=target
            while parents[at] is not None:
                previous,move=parents[at]
                path.append(move);at=previous
            return path[::-1],len(parents)
        for position in range(len(current)+1):
            for pattern,replacement,sign,rotation_prefix in patterns:
                if not current.startswith(pattern,position):continue
                changed=reduce(current[:position]+replacement+current[position+len(pattern):])
                if len(changed)>cap or changed in parents:continue
                move={'before':current,'position':position,'pattern':pattern,'replacement':replacement,
                      'sign':sign,'rotation_prefix':rotation_prefix,'after':changed}
                parents[changed]=(current,move);queue.append(changed)
    raise RuntimeError('bounded word-rewrite search did not find target')


class Ledger:
    def __init__(self,start,moves=()):
        self.start=list(start);self.state=list(start);self.moves=[]
        for move in moves:self.emit(move)
    def emit(self,move):
        i=move['i'];op=move['op'];self.moves.append(move)
        if op=='invert':self.state[i]=inverse(self.state[i])
        elif op=='multiply':self.state[i]=reduce(self.state[i]+self.state[move['j']])
        else:
            g=move['g'];self.state[i]=reduce(g+self.state[i]+inverse(g))
    def inv(self,i):self.emit({'op':'invert','i':i})
    def conjugate(self,i,word):
        for g in word[::-1]:self.emit({'op':'conjugate','i':i,'g':g})
    def rewrite(self,i,move):
        j=1-i
        assert self.state[i]==move['before']
        donor=self.state[j]
        prefix=move['before'][:move['position']]
        rotation_prefix=move['rotation_prefix']
        if move['sign']==-1:self.inv(j)
        self.conjugate(j,inverse(rotation_prefix))
        self.conjugate(i,inverse(prefix))
        self.inv(i)
        self.emit({'op':'multiply','i':i,'j':j})
        self.inv(i)
        self.conjugate(i,prefix)
        self.conjugate(j,rotation_prefix)
        if move['sign']==-1:self.inv(j)
        assert self.state[i]==move['after'] and self.state[j]==donor
    def certificate(self,**metadata):
        cert={'format':'ordinary-ac-elementary-v1','start':self.start,
              'target':self.state[:],'moves':self.moves[:],**metadata}
        replay(cert)
        return cert


def construct(directory):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    entry_path,entry_visits=find_path(B,BP,P,11)
    entry=Ledger([P,B])
    for move in entry_path:entry.rewrite(1,move)
    assert entry.state==[P,BP]
    entry_cert=entry.certificate(scope='Exact low-peak entry to cyclic15; not a trivialization',
                                 word_rewrite_path=entry_path,word_search_states=entry_visits)
    (directory/'hump_low_peak_entry.json').write_text(json.dumps(entry_cert,indent=2)+'\n')
    summaries=[{'name':'entry','rewrite_cells':len(entry_path),**replay(entry_cert)}]
    for name,q,target,cap in [('u1','XXyxYxYx','yXYXyxx',23),
                              ('u2','YxYx','YxYXyyx',17)]:
        ledger=Ledger([P,B],entry.moves)
        ledger.inv(0);ledger.conjugate(0,q)
        base=ledger.state[0]
        path,visits=find_path(base,target,BP,cap)
        for move in path:ledger.rewrite(0,move)
        factors=[{'sign':-move['sign'],
                  'conjugator':reduce(move['before'][:move['position']]+inverse(move['rotation_prefix']))}
                 for move in path[::-1]]
        difference=reduce(target+inverse(base))
        product=''
        for factor in factors:
            c=factor['conjugator'];r=BP if factor['sign']==1 else inverse(BP)
            product=reduce(product+c+r+inverse(c))
        assert product==difference
        cert=ledger.certificate(scope='Exact low-peak AC path to new reachable waypoint; not a trivialization',
                                hump_entry_prefix_moves=len(entry.moves),quotient_conjugator=q,
                                free_difference=difference,fixed_bprime_factorization=factors,
                                word_rewrite_path=path,word_search_states=visits)
        assert cert['target']==[target,BP]
        (directory/('hump_low_peak_'+name+'.json')).write_text(json.dumps(cert,indent=2)+'\n')
        summaries.append({'name':name,'rewrite_cells':len(path),**replay(cert)})
    (directory/'hump_low_peak_results.json').write_text(json.dumps(summaries,indent=2)+'\n')
    return summaries


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--directory',required=True)
    args=parser.parse_args()
    print(json.dumps(construct(args.directory),indent=2))
