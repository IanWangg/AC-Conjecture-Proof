"""Heuristic cyclic-state ordinary-AC search with an exact strict ledger.

It enumerates a stated finite menu of signed rotated products with short
relative conjugators. Canonicalization uses actual relator conjugation
and inversion, expanded in the emitted certificate. No exhaustiveness
claim for the entire ordinary or cyclic AC graph is made.
"""
import argparse
from collections import deque
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
for d in (HERE, HERE.parent/'research_m', HERE.parent/'root'):
    sys.path.insert(0, str(d))
from stallings_search import apply, inverse, reduce, primitive


def cyclic(w):
    w = reduce(w)
    while len(w)>1 and w[0] == w[-1].swapcase():
        w = w[1:-1]
    return w


def variants(w):
    w = cyclic(w)
    return sorted({v[k:]+v[:k] for v in (w, inverse(w))
                   for k in range(len(v))})


def canonical(w):
    return min(variants(w)) if w else ''


def conj_ops(i, g):
    return [{'op':'conjugate','i':i,'g':c} for c in g[::-1]]


def normalize(state, i, target=None):
    ops = []
    word = state[i]
    tail = ''
    while len(word)>1 and word[0] == word[-1].swapcase():
        tail += word[0]
        word = word[1:-1]
    ops.extend(conj_ops(i, inverse(tail)))
    if target is None:
        target = canonical(word)
    for sign in (1, -1):
        v = word if sign == 1 else inverse(word)
        for k in range(len(v)):
            if v[k:]+v[:k] == target:
                if sign == -1:
                    ops.append({'op':'invert','i':i})
                ops.extend(conj_ops(i, inverse(v[:k])))
                for op in ops:
                    state = apply(state, op)
                assert state[i] == target
                return state, ops
    if word == target == '':
        for op in ops:
            state = apply(state, op)
        return state, ops
    raise AssertionError((word, target))


def words_upto(length):
    level = ['']
    out = ['']
    for _ in range(length):
        level = [w+a for w in level for a in 'xXyY'
                 if not w or a != w[-1].swapcase()]
        out.extend(level)
    return out


def expand_edge(state, edge):
    i, u, v, q = edge
    j = 1-i
    ops = []
    state, more = normalize(state, i, u)
    ops.extend(more)
    state, more = normalize(state, j, v)
    ops.extend(more)
    more = conj_ops(j, q)
    for op in more:
        state = apply(state, op)
    ops.extend(more)
    op = {'op':'multiply','i':i,'j':j}
    state = apply(state, op)
    ops.append(op)
    for k in range(2):
        state, more = normalize(state, k)
        ops.extend(more)
    return state, ops


def search(start, cap, max_states, tail_length, seconds, catalogue=None, stop_at_primitive=True):
    begun = time.monotonic()
    initial = tuple(map(canonical, start))
    nodes = [(initial, None, None)]
    seen = {tuple(sorted(initial)): 0}
    queue = deque([0])
    best = 0
    lowest = sum(map(len, initial))
    edges = 0
    primitive_node = None
    tails = words_upto(tail_length)
    variant_cache = {}
    canonical_cache = {}
    reason = 'menu_component_exhausted'
    while queue:
        at = queue.popleft()
        state = nodes[at][0]
        vv = [variant_cache.setdefault(w, variants(w)) for w in state]
        for i in range(2):
            j = 1-i
            for u in vv[i]:
                for v in vv[j]:
                    for q in tails:
                        edges += 1
                        raw = reduce(u+q+v+inverse(q))
                        w = canonical_cache.get(raw)
                        if w is None:
                            w = canonical(raw)
                            canonical_cache[raw] = w
                        if len(w)+len(state[j]) > cap:
                            continue
                        nxt = list(state)
                        nxt[i] = w
                        nxt = tuple(nxt)
                        key = tuple(sorted(nxt))
                        if key in seen:
                            continue
                        index = len(nodes)
                        seen[key] = index
                        nodes.append((nxt, at, (i,u,v,q)))
                        queue.append(index)
                        length = sum(map(len,nxt))
                        if length < lowest:
                            lowest = length
                            best = index
                            print('new minimum', lowest, nxt, 'nodes', len(nodes), flush=True)
                        hit_primitive = primitive(w) or primitive(state[j])
                        if hit_primitive and (stop_at_primitive or all(len(z)==1 for z in nxt)):
                            primitive_node = index
                            best = index
                            reason = 'primitive_coordinate'
                            queue.clear()
                            break
                        if len(nodes) >= max_states:
                            reason = 'state_limit'
                            queue.clear()
                            break
                    if reason in ('primitive_coordinate','state_limit'):
                        break
                if reason in ('primitive_coordinate','state_limit'):
                    break
            if reason in ('primitive_coordinate','state_limit'):
                break
        if reason in ('primitive_coordinate','state_limit'):
            break
        if time.monotonic()-begun > seconds:
            reason = 'time_limit'
            break
        if at % 100 == 0:
            print('processed',at,'nodes',len(nodes),'queue',len(queue),
                  'edges',edges,'seconds',round(time.monotonic()-begun,2),flush=True)
    path = []
    at = best
    while nodes[at][1] is not None:
        path.append(nodes[at][2])
        at = nodes[at][1]
    actual = tuple(start)
    moves = []
    for i in range(2):
        actual, ops = normalize(actual,i)
        moves.extend(ops)
    for edge in path[::-1]:
        actual, ops = expand_edge(actual,edge)
        moves.extend(ops)
    assert actual == nodes[best][0]
    peak = sum(map(len,start))
    cyclic_peak = sum(len(cyclic(w)) for w in start)
    state = tuple(start)
    for op in moves:
        state = apply(state,op)
        peak = max(peak,sum(map(len,state)))
        cyclic_peak = max(cyclic_peak,sum(len(cyclic(w)) for w in state))
    assert state == actual
    if catalogue:
        Path(catalogue).write_text(json.dumps(sorted(seen),separators=(',',':'))+'\n')
    report = {'status':'PASS','ordinary_AC_goal_solved':False,
              'start':list(start),'target':list(actual),'cyclic_boundary_cap':cap,
              'relative_conjugator_menu_max_length':tail_length,
              'retained_states_modulo_inversion_rotation_permutation':len(nodes),
              'menu_edges_tested':edges,'termination':reason,
              'primitive_coordinate_found':primitive_node is not None,
              'minimum_cyclic_total':lowest,'new_strict_moves':len(moves),
              'minimum_cyclic_coordinate_length':min(len(w) for row in nodes for w in row[0]),
              'new_strict_peak':peak,'seconds':round(time.monotonic()-begun,4),
              'new_cyclic_peak':cyclic_peak,
              'scope':'Valid paths plus heuristic finite menu; no complete AC exclusion'}
    certificate = {'format':'ordinary-ac-elementary-v1','start':list(start),
                   'target':list(actual),'moves':moves}
    return report, certificate


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start',nargs=2,default=['yXYXyxx','YxYXyyx'])
    parser.add_argument('--cap',type=int,default=18)
    parser.add_argument('--states',type=int,default=20000)
    parser.add_argument('--tail',type=int,default=1)
    parser.add_argument('--seconds',type=float,default=120)
    parser.add_argument('--output',required=True)
    parser.add_argument('--certificate',required=True)
    parser.add_argument('--catalogue')
    parser.add_argument('--until-basis',action='store_true')
    args = parser.parse_args()
    report,cert = search(args.start,args.cap,args.states,args.tail,args.seconds,args.catalogue,not args.until_basis)
    Path(args.output).write_text(json.dumps(report,indent=2)+'\n')
    Path(args.certificate).write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
