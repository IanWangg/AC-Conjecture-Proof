"""Expand actual cyclic product edges into strict ordinary AC primitives."""
import argparse
import json
from pathlib import Path
from free_waypoint_search import normalize, expand_edge, canonical, cyclic, apply
from elementary_verify import replay


def compile_path(path):
    assert path['format'] == 'cyclic-edge-path-v1'
    state = tuple(path['start'])
    moves = []
    for i in (0,1):
        state, more = normalize(state,i,canonical(state[i]))
        moves.extend(more)
    for edge in path['edges']:
        state, more = expand_edge(state,(edge['i'],edge['u'],edge['v'],edge['q']))
        moves.extend(more)
    assert list(state) == path['target']
    certificate = dict(format='ordinary-ac-elementary-v1',start=path['start'],
                       target=path['target'],moves=moves,
                       scope='Explicit heuristic endpoint path; no free-basis claim')
    result = replay(certificate)
    state = tuple(path['start'])
    peak = sum(len(cyclic(w)) for w in state)
    for move in moves:
        state = apply(state,move)
        peak = max(peak,sum(len(cyclic(w)) for w in state))
    result['cyclic_total_peak'] = peak
    result['cyclic_product_edges'] = len(path['edges'])
    result['ordinary_AC_goal_solved'] = False
    return certificate,result


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('--certificate',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    cert,result=compile_path(json.loads(Path(args.path).read_text()))
    Path(args.certificate).write_text(json.dumps(cert,indent=2)+'\n')
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
