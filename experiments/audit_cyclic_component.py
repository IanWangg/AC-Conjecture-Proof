"""Independent string-based closed-set audit for cyclic AC certificates.

No search implementation is imported. The axes proof in the associated
reports supplies the passage from rotation products to all conjugates.
"""
import argparse
import base64
from collections import deque
from functools import lru_cache
import json
import gzip
from pathlib import Path


def inverse(w):
    return ''.join(c.swapcase() for c in w[::-1])


def reduced(w):
    out = []
    for c in w:
        assert c in 'xXyY'
        if out and out[-1].swapcase() == c:
            out.pop()
        else:
            out.append(c)
    while len(out) > 1 and out[0].swapcase() == out[-1]:
        out = out[1:-1]
    return ''.join(out)


@lru_cache(None)
def variants(w):
    w = reduced(w)
    return tuple(sorted({v[i:]+v[:i] for v in (w,inverse(w)) for i in range(len(v))})) or ('',)


@lru_cache(None)
def canonical(w):
    w = reduced(w)
    if not w:
        return ''
    return min(v[i:]+v[:i] for v in (w,inverse(w)) for i in range(len(v)))


def key(words):
    return tuple(sorted(map(canonical,words)))


def audit(source, cap, n=3):
    data = Path(source).read_bytes()
    if str(source).endswith('.gz.b64'):
        data = gzip.decompress(base64.b64decode(data))
    rows = json.loads(data)
    states = {tuple(row) for row in rows}
    assert len(states) == len(rows)
    initial = key(('x'*n+'Y'*(n+1),'xyxYXY'))
    assert initial in states
    minimum_sum = min(sum(map(len,s)) for s in states)
    minimum_word = min(len(w) for s in states for w in s)
    bridge_lower = min(sum(map(len,s))+min(map(len,s))+2 for s in states)
    assert bridge_lower > cap, 'disjoint-axis products not excluded by this certificate'
    neighbors = {}
    total = accepted = 0
    for s in states:
        assert len(s) == 2 and s == key(s)
        assert sum(map(len,s)) <= cap
        adjacent = set()
        for i in (0,1):
            j = 1-i
            for u in variants(s[i]):
                for v in variants(s[j]):
                    total += 1
                    w = canonical(u+v)
                    if len(w)+len(s[j]) > cap:
                        continue
                    nxt = tuple(sorted((w,s[j])))
                    assert nxt in states, ('not closed',s,nxt)
                    adjacent.add(nxt)
                    accepted += 1
        neighbors[s] = adjacent
    seen = {initial}
    queue = deque([initial])
    while queue:
        for nxt in neighbors[queue.popleft()]-seen:
            seen.add(nxt)
            queue.append(nxt)
    assert seen == states, 'certificate contains disconnected states'
    return dict(status='PASS', ordinary_AC_goal_solved=False, cap=cap,
                states=len(states), minimum_cyclic_sum=minimum_sum,
                minimum_cyclic_word_length=minimum_word,
                minimum_disjoint_axis_neighbor_energy=bridge_lower,
                rotated_signed_product_checks=total,
                accepted_directed_product_checks=accepted,
                independently_verified_closed_and_connected=True,
                independent_string_arithmetic=True,
                proof_of_all_conjugates_required='intersecting/disjoint Cayley-tree axes lemma')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('catalogue')
    parser.add_argument('--cap',type=int,required=True)
    parser.add_argument('--n',type=int,default=3)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    result=audit(args.catalogue,args.cap,args.n)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
