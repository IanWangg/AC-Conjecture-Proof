"""Exact BFS distances in PSL(2,p) for AK(3) and the standard pair.

Finite instruction alphabet: invert either entry; right multiply it by the
other entry or its inverse; conjugate it by x, x^-1, y, or y^-1. Each costs 1.
No arbitrary-word conjugations are assigned unit cost. This differs from the
positive-multiplication-only certificate verifier's cost convention.
"""
from array import array
from collections import deque
import json
import sys


def experiment(p):
    def canonical(a):
        a = tuple(v % p for v in a)
        return min(a, tuple(-v % p for v in a))

    def product(a, b):
        a0, a1, a2, a3 = a
        b0, b1, b2, b3 = b
        return canonical((a0*b0+a1*b2, a0*b1+a1*b3,
                          a2*b0+a3*b2, a2*b1+a3*b3))

    def inv(a):
        return canonical((a[3], -a[1], -a[2], a[0]))

    one = canonical((1, 0, 0, 1))
    x, y = canonical((1, 1, 0, 1)), canonical((1, 0, -1, 1))
    signed = [x, inv(x), y, inv(y)]
    elements = [one]
    ids = {one: 0}
    for a in elements:
        for g in signed:
            b = product(a, g)
            if b not in ids:
                ids[b] = len(elements)
                elements.append(b)
    size = len(elements)
    if size != p * (p*p - 1) // 2:
        raise ValueError("expected an odd prime and the full PSL group")
    table = [array('I', (ids[product(a, b)] for b in elements)) for a in elements]
    inverses = [ids[inv(a)] for a in elements]
    conjugates = [[ids[product(product(g, a), inv(g))] for a in elements]
                  for g in signed]
    ix, iy = ids[x], ids[y]

    def word(w):
        ans = 0
        letters = dict(zip('xXyY', [ix, inverses[ix], iy, inverses[iy]]))
        for c in w:
            ans = table[ans][letters[c]]
        return ans

    start = (word('xxxYYYY'), word('xyxYXY'))
    target = (ix, iy)
    start_id, target_id = start[0]*size+start[1], ix*size+iy
    distance = array('i', [-1]) * (size*size)
    parent = array('i', [-1]) * (size*size)
    parent_op = bytearray(size*size)
    distance[start_id] = 0
    queue = deque([start_id])
    moves = [('invert', 0), ('invert', 1),
             ('multiply', 0, 1), ('multiply', 0, -1),
             ('multiply', 1, 1), ('multiply', 1, -1)]
    moves += [('conjugate', i, g) for i in (0, 1) for g in 'xXyY']
    popped = 0
    while queue and distance[target_id] < 0:
        current = queue.popleft()
        popped += 1
        a, b = divmod(current, size)
        neighbors = [inverses[a]*size+b, a*size+inverses[b],
                     table[a][b]*size+b, table[a][inverses[b]]*size+b,
                     a*size+table[b][a], a*size+table[b][inverses[a]]]
        neighbors += [row[a]*size+b for row in conjugates]
        neighbors += [a*size+row[b] for row in conjugates]
        for op, nxt in enumerate(neighbors):
            if distance[nxt] < 0:
                distance[nxt] = distance[current] + 1
                parent[nxt], parent_op[nxt] = current, op
                queue.append(nxt)
    if distance[target_id] < 0:
        raise AssertionError("disconnected quotient")
    path = []
    at = target_id
    while at != start_id:
        path.append(moves[parent_op[at]])
        at = parent[at]
    path.reverse()
    # Replay the shortest path through direct matrix operations, separately
    # from the integer-index neighbor arithmetic used by BFS.
    state = [elements[a] for a in start]
    for op in path:
        i = op[1]
        if op[0] == 'invert':
            state[i] = inv(state[i])
        elif op[0] == 'multiply':
            donor = state[1-i]
            state[i] = product(state[i], donor if op[2] == 1 else inv(donor))
        else:
            g = signed['xXyY'.index(op[2])]
            state[i] = product(product(g, state[i]), inv(g))
    assert state == [x, y]
    return {'prime': p, 'group_order': size, 'distance': distance[target_id],
            'states_popped_before_target_discovery': popped,
            'states_discovered': sum(d >= 0 for d in distance),
            'start_matrices': [elements[a] for a in start],
            'target_matrices': [x, y], 'shortest_path': path}


if __name__ == '__main__':
    primes = list(map(int, sys.argv[1:])) or [3, 5, 7, 11]
    print(json.dumps({'alphabet': 'inversion, signed-right-multiplication, signed-generator-conjugation',
                      'results': [experiment(p) for p in primes]}, indent=2))
