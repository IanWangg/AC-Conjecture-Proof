"""Pack a reverse walk's complete parent/provenance data without word copies."""
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path
from reverse_journal import regenerate


def pack(prefix,target):
    prefix = str(prefix)
    nodes = [json.loads(s) for s in Path(prefix+'.nodes.jsonl').read_text().splitlines()]
    candidates = [json.loads(s) for s in Path(prefix+'.pairs.jsonl').read_text().splitlines()]
    result = json.loads(Path(prefix+'.results.json').read_text())
    edges = [[n['parent'],n['i'],n['sa'],n['sb'],n['ra'],n['rb'],n['q']] for n in nodes[1:]]
    records = []
    for index,row in enumerate(candidates):
        assert row['index'] == index
        node = nodes[row['node']]
        assert node['words'] == row['source_state']
        cuts = [next(k for k in range(len(word)) if word[k:]+word[:k] == target_word)
                for word,target_word in zip(node['words'],row['pair'])]
        records.append([row['node'],*cuts,row['DAG_absence']])
    journal = {'format':'r-known-trivial-reverse-journal-v1','start':result['start'],
               'seed':result['seed'],'energy_cap':result['heuristic_energy_cap'],
               'candidate_energy_cap':result['reverse_candidate_energy_cap'],
               'state_count':len(nodes),
               'candidate_tsv_sha256':hashlib.sha256(Path(prefix+'.pairs.tsv').read_bytes()).hexdigest(),
               'edges':edges,'candidates':records}
    states,depths,peaks = regenerate(journal)
    assert all(list(words) == node['words'] for words,node in zip(states,nodes))
    raw = json.dumps(journal,separators=(',',':')).encode()+b'\n'
    encoded = base64.b64encode(gzip.compress(raw,compresslevel=9,mtime=0))+b'\n'
    Path(target).write_bytes(encoded)
    eligible = [(depths[node],i) for i,(node,_,_,_) in enumerate(records) if peaks[node]>=23]
    chosen = min(eligible)[1] if eligible else 0
    return {'status':'PASS','ordinary_AC_goal_solved':False,
            'states':len(states),'edges':len(edges),'candidates':len(records),
            'decoded_bytes':len(raw),'encoded_bytes':len(encoded),
            'decoded_sha256':hashlib.sha256(raw).hexdigest(),
            'encoded_sha256':hashlib.sha256(encoded).hexdigest(),
            'selected_candidate_index':chosen,'selected_node':records[chosen][0],
            'selected_path_depth':depths[records[chosen][0]],
            'selected_cyclic_trajectory_peak':peaks[records[chosen][0]]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('prefix')
    parser.add_argument('--journal',required=True)
    parser.add_argument('--output',required=True)
    args = parser.parse_args()
    result = pack(args.prefix,args.journal)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
