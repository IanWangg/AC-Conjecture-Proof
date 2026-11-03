"""Compile sampled subgroup phases to strict, literal ordinary AC moves.

The stored path contains real raw Nielsen preludes and final coordinate
conjugacy choices. A spanning-tree basis change is compiled through the
existing exact formal-basis bridge, never treated as a free operation.
"""
import argparse
import json
from pathlib import Path
from primitive_map_pairs import fold
from h_basis_bridge import spanning_basis, compile_match
from stallings_search import nielsen_move
from free_waypoint_search import normalize, cyclic
from elementary_verify import replay


def compile_path(path, parent=None):
    assert path['format'] == 'coupled-h-phase-path-v1'
    if parent is None:
        parent = {'format': 'ordinary-ac-elementary-v1',
                  'start': path['start'], 'target': path['start'], 'moves': []}
    replay(parent)
    assert parent['target'] == path['start']
    state = tuple(path['start'])
    moves = list(parent['moves'])
    stage_results = []
    for stage in path['stages']:
        graph = fold(state)
        _, basis, _, _ = spanning_basis(graph, 0)
        bridge, _ = compile_match({
            'status': 'MATCH', 'canonical_unbased_graph': list(graph),
            'forward_rotated_pair': basis, 'reverse_pair': list(state),
            'forward_original_base': 0, 'reverse_original_base': 0})
        assert bridge['start'] == list(state)
        moves.extend(bridge['moves'])
        state = tuple(basis)
        for code in stage['prelude']:
            assert isinstance(code, int) and 0 <= code < 8
            state, more = nielsen_move(state, code & 1, bool(code & 2), bool(code & 4))
            moves.extend(more)
        raw_source = state
        for i in range(2):
            state, more = normalize(state, i, stage['target'][i])
            moves.extend(more)
        assert list(state) == stage['target']
        stage_results.append({'bridge_strict_moves': len(bridge['moves']),
                              'raw_source': list(raw_source),
                              'source_cyclic_energy': sum(len(cyclic(w)) for w in raw_source)})
    assert list(state) == path['target']
    certificate = {'format': 'ordinary-ac-elementary-v1',
                   'start': parent['start'], 'target': list(state), 'moves': moves,
                   'scope': 'Strict sampled subgroup-phase path; no completion asserted'}
    result = {'status': 'PASS', 'ordinary_AC_goal_solved': False,
              'strict_replay': replay(certificate), 'stages': stage_results}
    return certificate, result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('--parent')
    parser.add_argument('--certificate', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    parent = json.loads(Path(args.parent).read_text()) if args.parent else None
    cert, result = compile_path(json.loads(Path(args.path).read_text()), parent)
    Path(args.certificate).write_text(json.dumps(cert, indent=2)+'\n')
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
