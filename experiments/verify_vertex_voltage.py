"""Check the finite kernel certificates without the constructor or SCC solver.

Uses R's independent loop fold and computes mutual reachability directly.
Potential inequalities are replayed, not solved or assumed from statuses.
"""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
from primitive_map_pairs import fold, inverse, reduce, validate_graph, LETTERS


def paths(graph):
    answer = {0:''}
    todo = deque([0])
    while todo:
        a = todo.popleft()
        for c in range(4):
            b = graph[4*a+c]
            if b >= 0 and b not in answer:
                answer[b] = answer[a]+LETTERS[c]
                todo.append(b)
    return answer


def loop_voltage(graph, weights, word):
    at = value = 0
    for letter in word:
        c = LETTERS.index(letter)
        value += weights[4*at+c]
        at = graph[4*at+c]
        assert at >= 0
    assert at == 0
    return value


def verify(data, certificates):
    original = tuple(data['original_graph'])
    initial = data['original_pair']
    assert tuple(fold(initial)) == original
    n = len(original)//4
    original_paths = paths(original)
    by_pair = {tuple(r['identified_vertices']):r for r in certificates['results']}
    records = {tuple(r['identified_vertices']):r for r in data['records']}
    expected = {(a,b) for a in range(n) for b in range(a+1,n)}
    assert set(records) == set(by_pair) == expected
    components_checked = inequalities = tests = 0
    for pair in sorted(expected):
        row = records[pair]
        a,b = pair
        t = reduce(original_paths[a]+inverse(original_paths[b]))
        assert row['extra_generator'] == t
        graph = tuple(row['graph'])
        validate_graph(graph)
        assert tuple(fold(initial+[t])) == graph
        size = len(graph)//4
        edges = sum(v >= 0 for v in graph)//2
        assert edges-size+1 == row['rank'] == 3
        projection = row['vertex_projection']
        assert len(projection) == n and projection[0] == 0
        assert projection[a] == projection[b]
        for v in range(n):
            for c in range(4):
                end = original[4*v+c]
                if end >= 0:
                    assert graph[4*projection[v]+c] == projection[end]
        weights = row['edge_voltages']
        assert len(weights) == len(graph) and all(type(w) is int for w in weights)
        for v in range(size):
            for c in range(4):
                end = graph[4*v+c]
                if end >= 0:
                    assert weights[4*v+c] == -weights[4*end+(c^1)]
        assert all(loop_voltage(graph, weights, w) == 0 for w in initial)
        assert loop_voltage(graph, weights, t) == 1
        checks = {(tuple(c['alphabet']),c['forbidden_double']):c
                  for c in by_pair[pair]['checks']}
        expected_checks = {((x,y),blocked) for x in (0,1) for y in (2,3) for blocked in (0,1)}
        assert set(checks) == expected_checks
        for (alphabet,blocked), cert in checks.items():
            states = {2*v+i for v in range(size) for i,c in enumerate(alphabet)
                      if graph[4*v+c] >= 0}
            arcs = []
            successors = {s:set() for s in states}
            for s in states:
                v,i = divmod(s,2)
                c = alphabet[i]
                end = graph[4*v+c]
                for j,d in enumerate(alphabet):
                    if i == j == blocked or graph[4*end+d] < 0:
                        continue
                    target = 2*end+j
                    arcs.append((s,target,weights[4*v+c]))
                    successors[s].add(target)
            reach = {}
            for start in states:
                seen = {start}
                todo = [start]
                while todo:
                    at = todo.pop()
                    for end in successors[at]-seen:
                        seen.add(end)
                        todo.append(end)
                reach[start] = seen
            groups = {frozenset(v for v in states if v in reach[s] and s in reach[v])
                      for s in states}
            cyclic = {g for g in groups if any(a in g and b in g for a,b,_ in arcs)}
            claimed = {frozenset(c['states']):c for c in cert['cyclic_components']}
            assert set(claimed) == cyclic
            for group, item in claimed.items():
                assert len(item['states']) == len(group)
                sign = item['strict_cycle_voltage_sign']
                assert sign in (-1,1)
                potentials = item['potential']
                assert len(potentials) == len(group) and all(type(v) is int for v in potentials)
                h = dict(zip(item['states'],potentials))
                for a,b,w in arcs:
                    if a in group and b in group:
                        assert h[b] <= h[a]+len(group)*sign*w-1
                        inequalities += 1
                components_checked += 1
            tests += 1
    return {'status':'PASS','ordinary_AC_goal_solved':False,
            'original_graph_vertices':n, 'vertex_identifications_independently_refolded':len(expected),
            'rank_three_cases':len(expected), 'character_values_on_p_b_t':[0,0,1],
            'signed_double_free_graphs_independently_reconstructed':tests,
            'cyclic_components_independently_recognized':components_checked,
            'integer_potential_inequalities_checked':inequalities,
            'constructor_or_Bellman_Ford_solver_imported':False,
            'scope':'Finite certificate audit for the unbounded restricted kernel theorem; no global AC invariant'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('identifications')
    parser.add_argument('potentials')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = verify(json.loads(Path(args.identifications).read_text()),
                    json.loads(Path(args.potentials).read_text()))
    result['input_sha256'] = [hashlib.sha256(Path(p).read_bytes()).hexdigest()
                              for p in (args.identifications,args.potentials)]
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
