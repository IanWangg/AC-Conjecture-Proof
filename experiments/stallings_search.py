"""Heuristic ordinary-AC search by exact based subgroup graphs.

All candidate operations are free-word AC operations. Graph canonicalization
is a search key, never a claimed additional move or a completeness theorem.
"""
import argparse
from collections import deque
import json
from pathlib import Path
import random
import time

LETTERS = 'xXyY'


def inverse(w):
    return w.swapcase()[::-1]


def reduce(w):
    stack = []
    for c in w:
        if stack and stack[-1] == c.swapcase():
            stack.pop()
        else:
            stack.append(c)
    return ''.join(stack)


def apply(state, move):
    words = list(state)
    i = move['i']
    if move['op'] == 'invert':
        words[i] = inverse(words[i])
    elif move['op'] == 'multiply':
        words[i] = reduce(words[i] + words[move['j']])
    else:
        g = move['g']
        words[i] = reduce(g + words[i] + inverse(g))
    return tuple(words)


def nielsen_move(state, i, left, negative):
    """Strict primitive expansion; donor and its orientation are restored."""
    j = 1-i
    if not left:
        ops = ([{'op':'invert','i':j}] if negative else [])
        ops += [{'op':'multiply','i':i,'j':j}]
        ops += ([{'op':'invert','i':j}] if negative else [])
    elif negative:
        ops = [{'op':'invert','i':i}, {'op':'multiply','i':i,'j':j}, {'op':'invert','i':i}]
    else:
        ops = [{'op':'invert','i':i}, {'op':'invert','i':j},
               {'op':'multiply','i':i,'j':j}, {'op':'invert','i':i}, {'op':'invert','i':j}]
    for op in ops:
        state = apply(state, op)
    return state, ops


def nielsen_reduce(state):
    ledger = []
    while True:
        best = None
        total = sum(map(len, state))
        for i in range(2):
            for left in (False, True):
                for negative in (False, True):
                    nxt, ops = nielsen_move(state, i, left, negative)
                    if sum(map(len, nxt)) < total:
                        candidate = (sum(map(len, nxt)), nxt, ops)
                        if best is None or candidate[:2] < best[:2]:
                            best = candidate
        if best is None:
            return state, ledger
        state = best[1]
        ledger.extend(best[2])


def graph(words):
    """Repeated graph folding; labels are stored together with inverse arcs."""
    arcs, size = [], 1
    for word in words:
        v = 0
        for k, c in enumerate(word):
            w = 0 if k == len(word)-1 else size
            if w:
                size += 1
            arcs.extend(((v,c,w),(w,c.swapcase(),v)))
            v = w
    parent = list(range(size))

    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    while True:
        transitions = {}
        changed = False
        for v,c,w in arcs:
            v,w = root(v),root(w)
            if (v,c) in transitions and root(transitions[v,c]) != w:
                u = root(transitions[v,c])
                parent[max(u,w)] = min(u,w)
                changed = True
                break
            transitions[v,c] = w
        if not changed:
            break
    edges = {(root(v),c,root(w)) for v,c,w in arcs}
    transitions = {(v,c):w for v,c,w in edges}
    base = root(0)
    names = {base:0}
    queue = deque([base])
    encoded = []
    while queue:
        v = queue.popleft()
        for c in LETTERS:
            w = transitions.get((v,c))
            if w is None:
                encoded.append(-1)
            else:
                if w not in names:
                    names[w] = len(names)
                    queue.append(w)
                encoded.append(names[w])
    rank = len(edges)//2-len(names)+1
    assert rank == 2
    return tuple(encoded), len(names)


def cyclic(w):
    w = reduce(w)
    while len(w)>1 and w[0] == w[-1].swapcase():
        w = w[1:-1]
    return w


def primitive(w):
    w = cyclic(w)
    while len(w)>1:
        best = w
        for target in 'xy':
            other = 'y' if target == 'x' else 'x'
            for donor in (other,other.swapcase()):
                for left in (False,True):
                    image = donor+target if left else target+donor
                    transformed = ''.join(image if c==target else inverse(image) if c==target.swapcase() else c for c in w)
                    transformed = cyclic(transformed)
                    if len(transformed)<len(best):
                        best = transformed
        if len(best)==len(w):
            return False
        w=best
    return len(w)==1


def search(n=3, iterations=10000, seed=0, max_length=100, max_prelude=5, temperature=0.55, restart_mix=0.0):
    rng = random.Random(seed)
    start = ('x'*n+'Y'*(n+1),'xyxYXY')
    initial_key, initial_vertices = graph(start)
    nodes = [{'words':start,'parent':None,'moves':[],'vertices':initial_vertices}]
    seen = {initial_key:0}
    current = 0
    best = 0
    minimum_vertices = initial_vertices
    minimum_raw = sum(map(len,start))
    minimum_word = min(map(len,start))
    attempts = 0
    discarded_length = 0
    primitive_node = None
    begun = time.monotonic()
    for attempts in range(1,iterations+1):
        # Restart among many promising subgroups, retaining some high barriers.
        if attempts % 40 == 0:
            if rng.random()<restart_mix:
                current=rng.randrange(len(nodes))
            else:
                pool = sorted(range(len(nodes)), key=lambda k:(nodes[k]['vertices'],sum(map(len,nodes[k]['words']))))
                current = rng.choice(pool[:min(100,len(pool))])
        state = nodes[current]['words']
        moves = []
        for _ in range(rng.randrange(max_prelude+1)):
            state, ops = nielsen_move(state,rng.randrange(2),bool(rng.randrange(2)),bool(rng.randrange(2)))
            moves.extend(ops)
            if sum(map(len,state))>max_length:
                break
        if sum(map(len,state))>max_length:
            discarded_length += 1
            continue
        if primitive(state[0]) or primitive(state[1]):
            _, vertices=graph(state)
            minimum_vertices=min(minimum_vertices,vertices)
            minimum_raw=min(minimum_raw,sum(map(len,state)))
            minimum_word=min(minimum_word,min(map(len,state)))
            primitive_node=len(nodes)
            best=primitive_node
            nodes.append({'words':state,'parent':current,'moves':moves,'vertices':vertices})
            break
        op = {'op':'conjugate','i':rng.randrange(2),'g':rng.choice(LETTERS)}
        state = apply(state,op)
        moves.append(op)
        state, ops = nielsen_reduce(state)
        moves.extend(ops)
        if sum(map(len,state))>max_length:
            discarded_length += 1
            continue
        key, vertices = graph(state)
        if primitive(state[0]) or primitive(state[1]) or vertices==1:
            minimum_vertices=min(minimum_vertices,vertices)
            minimum_raw=min(minimum_raw,sum(map(len,state)))
            minimum_word=min(minimum_word,min(map(len,state)))
            primitive_node=len(nodes)
            best=primitive_node
            nodes.append({'words':state,'parent':current,'moves':moves,'vertices':vertices})
            seen.setdefault(key,primitive_node)
            break
        if key not in seen:
            index = len(nodes)
            seen[key] = index
            nodes.append({'words':state,'parent':current,'moves':moves,'vertices':vertices})
            minimum_raw = min(minimum_raw,sum(map(len,state)))
            minimum_word = min(minimum_word,min(map(len,state)))
            if vertices < minimum_vertices:
                minimum_vertices = vertices
                best = index
            # Tempered geometric random walk. This is a heuristic decision.
            difference = vertices-nodes[current]['vertices']
            if difference <= 0 or rng.random() < temperature**difference:
                current = index
        elif rng.random() < 0.1:
            current = seen[key]
    path = []
    at = best
    while nodes[at]['parent'] is not None:
        path.append(nodes[at]['moves'])
        at = nodes[at]['parent']
    moves = [move for chunk in path[::-1] for move in chunk]
    state = start
    peak = sum(map(len,state))
    for move in moves:
        state = apply(state,move)
        peak = max(peak,sum(map(len,state)))
    assert state == nodes[best]['words']
    report = {'n':n,'seed':seed,'attempted_macro_moves':attempts,
              'unique_based_subgroups':len(seen),'stored_waypoints':len(nodes),
              'max_retained_macro_boundary_total':max_length,
              'maximum_random_Nielsen_prelude':max_prelude,'discarded_over_length':discarded_length,
              'temperature_acceptance_base':temperature,'restart_uniform_probability':restart_mix,
              'initial_vertices':initial_vertices,'minimum_vertices_found':minimum_vertices,
              'minimum_normalized_total_length':minimum_raw,'minimum_normalized_coordinate_length':minimum_word,
              'primitive_waypoint_found':primitive_node is not None,
              'best_endpoint':state,'best_strict_moves':len(moves),'best_strict_peak':peak,
              'seconds':round(time.monotonic()-begun,4),
              'scope':'Heuristic finite free-group search; no exhaustive AC exclusion'}
    cert = {'format':'ordinary-ac-elementary-v1','start':list(start),'target':list(state),'moves':moves}
    return report,cert


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--n',type=int,default=3)
    parser.add_argument('--iterations',type=int,default=10000)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--max-length',type=int,default=100)
    parser.add_argument('--max-prelude',type=int,default=5)
    parser.add_argument('--temperature',type=float,default=0.55)
    parser.add_argument('--restart-mix',type=float,default=0.0)
    parser.add_argument('--output')
    parser.add_argument('--certificate')
    args=parser.parse_args()
    report,cert=search(args.n,args.iterations,args.seed,args.max_length,args.max_prelude,args.temperature,args.restart_mix)
    if args.output:
        Path(args.output).write_text(json.dumps(report,indent=2)+'\n')
    if args.certificate:
        Path(args.certificate).write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps(report,indent=2))
