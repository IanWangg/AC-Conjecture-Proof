"""Exact free-word control for AC moves on three relators in F(x,y)."""

import json

from elementary_verify import inverse, reduce


def redundant_coordinate_control(n):
    p = 'x' * n + 'Y' * (n + 1)
    b = 'xyxYXY'
    start = [p, b, '']
    state = start.copy()
    moves = []
    peak = sum(map(len, state))

    def emit(op, i, **args):
        nonlocal peak
        if op == 'invert':
            state[i] = inverse(state[i])
        elif op == 'multiply':
            j = args['j']
            assert i != j
            state[i] = reduce(state[i] + state[j])
        else:
            g = args['g']
            assert op == 'conjugate' and len(g) == 1
            state[i] = reduce(g + state[i] + inverse(g))
        moves.append(dict(op=op, i=i, **args))
        peak = max(peak, sum(map(len, state)))

    def multiply_conjugate(i, j, word, sign):
        saved_donor = state[j]
        if sign < 0:
            emit('invert', j)
        for g in reversed(word):
            emit('conjugate', j, g=g)
        emit('multiply', i, j=j)
        for g in word:
            emit('conjugate', j, g=inverse(g))
        if sign < 0:
            emit('invert', j)
        assert state[j] == saved_donor

    # x = b D^-1 f, where D = [p,y] (yx) p (yx)^-1 and
    # f = (x^(n-1) b x^-(n-1)) ... (x b x^-1) b.
    factors = [(1, '', 1), (0, 'yx', -1), (0, 'y', 1), (0, '', -1)]
    factors.extend((1, 'x' * k, 1) for k in reversed(range(n)))
    for donor, conjugator, sign in factors:
        multiply_conjugate(2, donor, conjugator, sign)
    assert state == [p, b, 'x']

    for i in (0, 1):
        while any(letter in 'xX' for letter in state[i]):
            position = next(k for k, letter in enumerate(state[i]) if letter in 'xX')
            prefix = state[i][:position]
            letter = state[i][position]
            suffix = state[i][position + 1:]
            multiply_conjugate(i, 2, inverse(suffix), -1 if letter == 'x' else 1)
            assert state[i] == reduce(prefix + suffix)
    assert state == ['Y' * (n + 1), 'Y', 'x']

    emit('invert', 1)
    for _ in range(n + 1):
        emit('multiply', 0, j=1)
    assert state == ['', 'y', 'x']
    return dict(n=n, start=start, endpoint=state, moves=moves,
                move_count=len(moves), peak_total_length=peak)


if __name__ == '__main__':
    print(json.dumps({
        'ambient_generators': ['x', 'y'],
        'relator_coordinates': 3,
        'ak3_trace': redundant_coordinate_control(3),
        'family_control_move_counts': {
            n: redundant_coordinate_control(n)['move_count'] for n in range(2, 9)
        },
    }, indent=2))
