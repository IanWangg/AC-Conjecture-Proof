"""Independent Stallings folding and signed-cycle tests for conjugated pairs.

No external packages. Finite tests alone do not establish AC nontriviality.
The accompanying report supplies the finite-tail reduction and exact scope.
"""
import argparse
import json
from pathlib import Path
from collections import deque, Counter

LETTERS = 'xXyY'
POWER_REPRESENTATIVES = (
    'XXXXYxxxy', 'XXXXyxxxY', 'XXXYxxYxy', 'XXXyXYxxy',
    'XXXyxYXyy', 'XXXyxYxxY', 'XXXyxxYXy', 'XXXyyXYxy',
    'XXYxxYYxy', 'XXyXYxYxy', 'XXyxYXyyy', 'XXyxYYXyy',
    'XXyxYYxxY', 'XXyxYxYXy', 'XXyyXYYxy', 'XXyyyXYxy',
    'XYYYYxyyy', 'XYYYxyXyy', 'XYYYxyyyy', 'XYYxyXyyy',
    'XYxYYYxyy', 'XYxYYxyXy', 'XYxYYxyyy', 'XYxYxyXyy')
BRAID_REPRESENTATIVES = ('XXYxxYxy', 'XXyXYxxy')


def inverse(w):
    return w[::-1].swapcase()


def reduce(w):
    stack = []
    for c in w:
        if stack and stack[-1] == c.swapcase():
            stack.pop()
        else:
            stack.append(c)
    return ''.join(stack)


def valid_graph(encoded):
    assert len(encoded) % 4 == 0
    vertices = len(encoded)//4
    for a in range(vertices):
        for c in range(4):
            b = encoded[4*a+c]
            assert -1 <= b < vertices
            if b >= 0:
                assert encoded[4*b+(c ^ 1)] == a


def reduced_words(bound):
    layer = ['']
    yield ''
    for _ in range(bound):
        layer = [w+c for w in layer for c in LETTERS
                 if not w or w[-1] != c.swapcase()]
        yield from layer


def folded_graph(u, v, q):
    """Fold a barbell with cyclic loops u,v and joining path q.

    The result is the based graph of <u, q v q^-1>. An explicit DSU
    implementation is independent of the previous subgroup-graph scripts.
    """
    parent = [0]
    edges = []

    def vertex():
        n = len(parent)
        parent.append(n)
        return n

    def path(start, word, closed=False):
        at = start
        for i, letter in enumerate(word):
            target = start if closed and i == len(word)-1 else vertex()
            edges.append((at, LETTERS.index(letter), target))
            at = target
        return at

    path(0, u, True)
    other = path(0, q)
    path(other, v, True)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    while True:
        outgoing = {}
        merged = False
        for a, label, b in edges:
            a, b = find(a), find(b)
            for source, c, target in ((a, label, b), (b, label ^ 1, a)):
                old = outgoing.get((source, c))
                if old is None:
                    outgoing[source, c] = target
                elif find(old) != find(target):
                    parent[find(target)] = find(old)
                    merged = True
                    break
            if merged:
                break
        if not merged:
            break

    adjacency = {}
    for a, label, b in edges:
        a, b = find(a), find(b)
        adjacency.setdefault(a, {})[label] = b
        adjacency.setdefault(b, {})[label ^ 1] = a
    ids = {find(0): 0}
    queue = deque([find(0)])
    encoded = []
    while queue:
        at = queue.popleft()
        for label in range(4):
            target = adjacency.get(at, {}).get(label)
            if target is not None and target not in ids:
                ids[target] = len(ids)
                queue.append(target)
            encoded.append(-1 if target is None else ids[target])
    return tuple(encoded)


def line_dag(encoded, alphabet, forbidden, certificate=False):
    edges = [(at, LETTERS[c], encoded[4*at+c])
             for at in range(len(encoded)//4) for c in range(4)
             if encoded[4*at+c] >= 0 and LETTERS[c] in alphabet]
    by_source = {}
    for i, e in enumerate(edges):
        by_source.setdefault(e[0], []).append(i)
    adjacency = [[j for j in by_source.get(e[2], [])
                  if not (e[1] == edges[j][1] == forbidden)] for e in edges]
    indegree = [0]*len(edges)
    for row in adjacency:
        for j in row:
            indegree[j] += 1
    queue = deque(i for i, d in enumerate(indegree) if d == 0)
    order = []
    while queue:
        i = queue.popleft()
        order.append(i)
        for j in adjacency[i]:
            indegree[j] -= 1
            if indegree[j] == 0:
                queue.append(j)
    return (order if len(order) == len(edges) else None) if certificate else len(order) == len(edges)


def passes(encoded):
    return all(line_dag(encoded, alphabet, c)
               for alphabet in ('xy', 'xY', 'Xy', 'XY') for c in alphabet)


def run(u, v, bound=None):
    if bound is None:
        bound = len(u)//2 + len(v)//2
    seen = {}
    failures = []
    hist = Counter()
    total = 0
    for q in reduced_words(bound):
        total += 1
        graph = folded_graph(u, v, q)
        valid_graph(graph)
        if graph in seen:
            continue
        seen[graph] = q
        hist[len(graph)//4] += 1
        if not passes(graph):
            failures.append({'q': q, 'vertices': len(graph)//4,
                             'graph': list(graph)})
    return {'u': u, 'v': v, 'tail_bound': bound, 'tails_tested': total,
            'unique_based_graphs': len(seen), 'vertex_histogram': dict(sorted(hist.items())),
            'signed_criterion_failures': failures}


def catalogue(source=None, crosscheck=None):
    if source:
        data = json.loads(Path(source).read_text())['enumeration']
        assert tuple(data['power9_in_braid']['cyclic_inverse_representatives']) == POWER_REPRESENTATIVES
        assert tuple(data['braid8_in_torus']['cyclic_inverse_representatives']) == BRAID_REPRESENTATIVES
    # Every primitive-containing control must fail this sufficient absence test.
    assert not passes(folded_graph('x', 'y', ''))
    assert not passes(folded_graph('xxY', 'xyxYXY', 'xyXXy'))
    pairs = [('xxxYYYY', 'xyxYXY')]
    pairs += [('xxxYYYY', w) for w in BRAID_REPRESENTATIVES]
    pairs += [(w, 'xyxYXY') for w in POWER_REPRESENTATIVES]
    pairs += [(w, 'XXyxYxxY') for w in ('yXYXyxx', 'YxYXyyx')]
    rows = []
    for u, v in pairs:
        assert all(reduce(w) == w and w[0] != w[-1].swapcase() for w in (u, v))
        assert passes(folded_graph(u, u, ''))
        assert passes(folded_graph(v, v, ''))
        row = run(u, v)
        if crosscheck:
            for q in reduced_words(row['tail_bound']):
                assert folded_graph(u, v, q) == crosscheck((u, reduce(q+v+inverse(q))))[0]
        assert not row['signed_criterion_failures']
        rows.append(row)
        print(json.dumps({k: row[k] for k in ('u','v','tails_tested','unique_based_graphs')}
                         | {'criterion_failures': len(row['signed_criterion_failures'])}), flush=True)
    total = sum(row['tails_tested'] for row in rows)
    graphs = sum(row['unique_based_graphs'] for row in rows)
    assert (len(rows), total, graphs) == (29, 123901, 118802)
    return {'format': 'arbitrary-tail-overlap-audit-v1', 'status': 'PASS',
            'ordinary_AC_goal_solved': False, 'representative_pairs': len(rows),
            'total_short_tails_tested': total,
            'distinct_graphs_counted_within_each_pair_family': graphs,
            'signed_acyclic_line_graphs_checked': 8*graphs,
            'primitive_containing_positive_controls_rejected': 2,
            'crosschecked_against_prior_fold': crosscheck is not None,
            'arbitrary_independent_conjugating_tails_covered_by_bridge_lemma': True,
            'arbitrary_interspersed_AC_moves_covered': False, 'pairs': rows}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source')
    parser.add_argument('--crosscheck-directory', help='Optional directory containing stallings_search.py')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    crosscheck = None
    if args.crosscheck_directory:
        import sys
        sys.path.insert(0, args.crosscheck_directory)
        from stallings_search import graph as crosscheck
    result = catalogue(args.source, crosscheck)
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
