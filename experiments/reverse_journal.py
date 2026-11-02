"""Replay a compact known-trivial-side parent journal and candidate corpus.

The actual words are regenerated from every signed rotation/product edge.
Q's unbased keys are independently checked using R's Python folding.
"""
import argparse
import base64
from collections import deque
import gzip
import hashlib
import json
from pathlib import Path
from primitive_map_pairs import LETTERS,fold,inverse,reduce


def cyclic(word):
    word = reduce(word)
    while len(word)>1 and word[0] == word[-1].swapcase():
        word = word[1:-1]
    return word


def canonical(word):
    word = cyclic(word)
    return min(w[i:]+w[:i] for w in (word,inverse(word)) for i in range(len(w))) if word else ''


def oriented(word,sign,cut):
    word = inverse(word) if sign else word
    assert 0 <= cut < len(word)
    return word[cut:]+word[:cut]


def load(path):
    raw = Path(path).read_bytes()
    if str(path).endswith('.gz.b64'):
        raw = gzip.decompress(base64.b64decode(raw))
    result = json.loads(raw)
    assert result['format'] == 'r-known-trivial-reverse-journal-v1'
    return result,raw


def regenerate(journal):
    states = [tuple(map(canonical,journal['start']))]
    depths = [0]
    peaks = [sum(map(len,states[0]))]
    for index,edge in enumerate(journal['edges'],1):
        parent,i,sa,sb,ra,rb,q = edge
        assert 0 <= parent < index and i in (0,1) and sa in (0,1) and sb in (0,1)
        assert reduce(q) == q
        old = states[parent]
        u = oriented(old[i],sa,ra)
        v = oriented(old[1-i],sb,rb)
        product = canonical(u+q+v+inverse(q))
        assert product
        words = list(old)
        words[i] = product
        state = tuple(words)
        assert sum(map(len,state)) <= journal['energy_cap']
        a,b = ((w.count('x')-w.count('X'),w.count('y')-w.count('Y')) for w in state)
        assert abs(a[0]*b[1]-a[1]*b[0]) == 1
        states.append(state)
        depths.append(depths[parent]+1)
        peaks.append(max(peaks[parent],sum(map(len,state))))
    assert len(states) == journal['state_count']
    return states,depths,peaks


def unbased_key(encoded):
    size = len(encoded)//4
    degrees = [sum(v>=0 for v in encoded[4*i:4*i+4]) for i in range(size)]
    assert min(degrees) >= 2
    assert sum(degrees)//2-size+1 == 2
    branches = [i for i,d in enumerate(degrees) if d>=3]
    assert 1 <= len(branches) <= 2
    keys = []
    for base in branches:
        names = {base:0}
        queue = deque([base])
        code = []
        while queue:
            at = queue.popleft()
            for end in encoded[4*at:4*at+4]:
                if end >= 0 and end not in names:
                    names[end] = len(names)
                    queue.append(end)
                code.append(names[end]+1 if end>=0 else 0)
        keys.append(bytes(code))
    return min(keys)


def candidates(journal,states):
    result = []
    for node,cut0,cut1,dag in journal['candidates']:
        assert 0 <= node < len(states)
        a,b = states[node]
        assert 0 <= cut0 < len(a) and 0 <= cut1 < len(b)
        result.append((a[cut0:]+a[:cut0],b[cut1:]+b[:cut1]))
    return result


def audit(path,tsv_output=None):
    journal,raw = load(path)
    states,depths,peaks = regenerate(journal)
    pairs = candidates(journal,states)
    keys = set()
    for pair in pairs:
        encoded = fold(pair)
        assert 7 <= len(encoded)//4 <= 21
        assert sum(map(len,pair)) <= journal['candidate_energy_cap']
        key = unbased_key(encoded)
        assert key not in keys
        keys.add(key)
    tsv = ''.join(a+'\t'+b+'\n' for a,b in pairs).encode()
    assert hashlib.sha256(tsv).hexdigest() == journal['candidate_tsv_sha256']
    if tsv_output:
        Path(tsv_output).write_bytes(tsv)
    return {'status':'PASS','ordinary_AC_goal_solved':False,
            'journal_sha256':hashlib.sha256(raw).hexdigest(),
            'start':journal['start'],'all_parent_product_edges_checked':len(journal['edges']),
            'regenerated_cyclic_states':len(states),
            'reverse_core_candidates_independently_folded':len(pairs),
            'distinct_reverse_unbased_keys':len(keys),
            'candidate_tsv_sha256':hashlib.sha256(tsv).hexdigest(),
            'maximum_accepted_cyclic_sum':max(peaks),
            'maximum_parent_depth':max(depths),
            'scope':'Actual known-trivial-side finite corpus; no global negative inference'}


def compile_candidate(path,index):
    from free_waypoint_search import normalize,expand_edge,apply
    from elementary_verify import replay
    journal,_ = load(path)
    states,depths,peaks = regenerate(journal)
    target = candidates(journal,states)[index]
    at = journal['candidates'][index][0]
    chain = []
    while at:
        chain.append(at)
        at = journal['edges'][at-1][0]
    state = tuple(journal['start'])
    moves = []
    for i in (0,1):
        state,extra = normalize(state,i,canonical(state[i]))
        moves.extend(extra)
    for at in reversed(chain):
        parent,i,sa,sb,ra,rb,q = journal['edges'][at-1]
        old = states[parent]
        edge = (i,oriented(old[i],sa,ra),oriented(old[1-i],sb,rb),q)
        state,extra = expand_edge(state,edge)
        moves.extend(extra)
        assert state == states[at]
    for i in (0,1):
        state,extra = normalize(state,i,target[i])
        moves.extend(extra)
    assert state == target
    certificate = {'format':'ordinary-ac-elementary-v1','start':journal['start'],
                   'target':list(target),'moves':moves,
                   'scope':'Exact known-trivial-side candidate; no AK3 path asserted'}
    result = replay(certificate)
    actual = tuple(certificate['start'])
    peak = sum(len(cyclic(w)) for w in actual)
    for move in moves:
        actual = apply(actual,move)
        peak = max(peak,sum(len(cyclic(w)) for w in actual))
    result.update(cyclic_total_peak=peak,cyclic_product_edges=len(chain),
                  candidate_index=index,candidate_node=journal['candidates'][index][0],
                  ordinary_AC_goal_solved=False)
    return certificate,result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('journal')
    parser.add_argument('--tsv-output')
    parser.add_argument('--candidate-index',type=int)
    parser.add_argument('--certificate')
    parser.add_argument('--output',required=True)
    args = parser.parse_args()
    if args.candidate_index is not None:
        assert args.certificate
        certificate,result = compile_candidate(args.journal,args.candidate_index)
        Path(args.certificate).write_text(json.dumps(certificate,indent=2)+'\n')
    else:
        result = audit(args.journal,args.tsv_output)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
