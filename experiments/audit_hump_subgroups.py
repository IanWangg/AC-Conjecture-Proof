"""Independent forced-doubles audit of the literal first-departure catalogue.

Uses I's graph folding and a separate directed-edge DFS, not M's SCC or
topological-order implementation. No claim about arbitrary conjugating tails.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
from braid_relation_module import stallings
import first_hump as h


def orbit(word):
    return {t[k:]+t[:k] for t in (word, h.inverse(word)) for k in range(len(t))}


def has_cycle_without_double(arcs, alphabet, forbidden):
    edges = [tuple(e) for e in arcs if e[1] in alphabet]
    outgoing = {}
    for i, (source, label, target) in enumerate(edges):
        outgoing.setdefault(source, []).append(i)
    color = [0]*len(edges)

    def visit(i):
        if color[i] == 1:
            return True
        if color[i] == 2:
            return False
        color[i] = 1
        _, previous, vertex = edges[i]
        for j in outgoing.get(vertex, ()):
            label = edges[j][1]
            if previous == label == forbidden:
                continue
            if visit(j):
                return True
        color[i] = 2
        return False
    return any(visit(i) for i in range(len(edges)) if color[i] == 0)


def forced_doubles(arcs):
    return all(not has_cycle_without_double(arcs, alphabet, letter)
               for alphabet in ('xy', 'xY', 'Xy', 'XY') for letter in alphabet)


def audit():
    assert not forced_doubles(stallings(['x', 'y'])['arcs'])
    data = h.enumeration()
    power_words = set().union(*(orbit(w) for w in data['power9_in_braid']['cyclic_inverse_representatives']))
    braid_words = set().union(*(orbit(w) for w in data['braid8_in_torus']['cyclic_inverse_representatives']))
    assert len(power_words) == 432 and len(braid_words) == 32
    pairs = {(p, b) for p in power_words for b in orbit(h.B)}
    pairs.update((p, b) for p in orbit(h.P) for b in braid_words)
    assert len(pairs) == 5632
    sizes = Counter()
    for pair in sorted(pairs):
        graph = stallings(pair)
        assert graph['rank'] == 2
        if not forced_doubles(graph['arcs']):
            raise AssertionError('a candidate subgroup requires further primitive analysis: '+repr(pair))
        sizes[graph['vertices']] += 1
    for pair in [('yXYXyxx', h.BP), ('YxYXyyx', h.BP)]:
        assert forced_doubles(stallings(pair)['arcs'])
    return {'status': 'PASS', 'independent_folding': 'I graph implementation',
            'independent_cycle_algorithm': 'directed-edge DFS avoiding each repeated letter',
            'raw_power_words': 432, 'raw_braid_words': 32,
            'literal_pairs_with_frozen_rotations_and_inverses': len(pairs),
            'all_forced_doubles_checks_pass': True, 'graph_vertex_counts': dict(sorted(sizes.items())),
            'two_additional_strict_waypoint_subgroups_checked': True,
            'scope': 'Literal cyclically reduced catalogue; arbitrary independent conjugating tails and later AC moves excluded',
            'ordinary_AC_goal_solved': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    args = parser.parse_args()
    result = audit()
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
