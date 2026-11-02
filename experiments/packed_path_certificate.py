"""Compile a packed-search orbit path into strict ordinary AC primitives.

Relator swaps introduced by orbit normalization are explicitly expanded;
their expansion may raise the raw peak above the orbit path's cap.
"""
import argparse
import json
from pathlib import Path
from elementary_verify import inverse, reduce, replay


def compile_path(result):
    n = result['n']
    state = ['x'*n + 'Y'*(n+1), 'xyxYXY']
    moves = []

    def emit(op, i, **kwargs):
        moves.append(dict(op=op, i=i, **kwargs))
        if op == 'invert':
            state[i] = inverse(state[i])
        elif op == 'multiply':
            state[i] = reduce(state[i] + state[kwargs['j']])
        else:
            g = kwargs['g']
            state[i] = reduce(g + state[i] + inverse(g))

    def multiply(i, j, sign=1):
        if sign < 0:
            emit('invert', j)
        emit('multiply', i, j=j)
        if sign < 0:
            emit('invert', j)

    def conjugate(i, word):
        for g in reversed(word):
            emit('conjugate', i, g=g)

    def swap():
        a, b = state
        multiply(0, 1)
        emit('invert', 1)
        multiply(1, 0)
        conjugate(1, b)
        multiply(0, 1, -1)
        conjugate(0, inverse(a))
        assert state == [b, a]

    def normalize(target):
        if target[0] not in (state[0], inverse(state[0])):
            swap()
        for i in range(2):
            if state[i] != target[i]:
                emit('invert', i)
        if state != target:
            raise ValueError('path contains a non-orbit normalization')

    path = result['best_path']
    if not path or path[0]['edge'] != 255:
        raise ValueError('missing initial path node')
    normalize(path[0]['words'])
    for node in path[1:]:
        edge = node['edge']
        if 0 <= edge < 8:
            i, signs = divmod(edge, 4)
            sa, sb = divmod(signs, 2)
            if sa:
                emit('invert', i)
            multiply(i, 1-i, -1 if sb else 1)
        elif 8 <= edge < 16:
            i, g = divmod(edge-8, 4)
            emit('conjugate', i, g='xXyY'[g])
        else:
            raise ValueError('invalid edge code')
        normalize(node['words'])
    certificate = {'format': 'ordinary-ac-elementary-v1',
                   'start': ['x'*n + 'Y'*(n+1), 'xyxYXY'],
                   'target': state[:], 'moves': moves,
                   'search_cap': result['cap'],
                   'scope': 'Strict expansion of an orbit path; expanded peak may exceed search cap'}
    replay(certificate)
    return certificate


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('result')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    certificate = compile_path(json.loads(Path(args.result).read_text()))
    Path(args.output).write_text(json.dumps(certificate, indent=2)+'\n')
    print(json.dumps(replay(certificate), sort_keys=True))
