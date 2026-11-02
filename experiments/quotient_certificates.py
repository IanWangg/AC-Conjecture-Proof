#!/usr/bin/env python3
"""Exact quotient checks, not a free-group AC trivialization.

Run: python3 quotient_certificates.py
Uses only Python's standard library. Uppercase letters denote inverse letters.
"""
from collections import defaultdict, deque
import json


def reduce_word(word):
    stack = []
    for letter in word:
        if stack and stack[-1] == letter.swapcase():
            stack.pop()
        else:
            stack.append(letter)
    return ''.join(stack)


def inverse_word(word):
    return word[::-1].swapcase()


def class2_multiply(u, v):
    a, b, k = u
    d, e, l = v
    return (a + d, b + e, k + l - b * d)


def class2_value(word):
    letters = {'x': (1, 0, 0), 'X': (-1, 0, 0),
               'y': (0, 1, 0), 'Y': (0, -1, 0)}
    result = (0, 0, 0)
    for letter in word:
        result = class2_multiply(result, letters[letter])
    return result


def magnus(word, degree=3):
    result = {'': 1}
    for letter in word:
        if letter.islower():
            factor = {'': 1, letter: 1}
        else:
            factor = {letter.lower() * k: (-1) ** k
                      for k in range(degree + 1)}
        product = defaultdict(int)
        for a, ca in result.items():
            for b, cb in factor.items():
                if len(a + b) <= degree:
                    product[a + b] += ca * cb
        result = {a: c for a, c in product.items() if c}
    return result


def class2_path(n):
    """Literal moves: invert, right multiply positively, generator conjugate, swap."""
    assert n >= 1
    moves = [('invert', 1)]
    moves += [('multiply', 0, 1)] * n
    moves += [('invert', 1), ('invert', 0)]
    moves += [('conjugate', 0, 'x')] * (n * (n - 1) // 2)
    moves += [('multiply', 1, 0), ('conjugate', 1, 'y'), ('swap',)]
    return moves


def replay_free(n, moves=None):
    relators = ['x' * n + 'Y' * (n + 1), 'xyxYXY']
    for move in class2_path(n) if moves is None else moves:
        if move[0] == 'invert':
            i = move[1]
            relators[i] = inverse_word(relators[i])
        elif move[0] == 'multiply':
            _, i, j = move
            relators[i] = reduce_word(relators[i] + relators[j])
        elif move[0] == 'conjugate':
            _, i, g = move
            relators[i] = reduce_word(inverse_word(g) + relators[i] + g)
        else:
            assert move[0] == 'swap'
            relators.reverse()
    return relators


def conjugate_word(i, word):
    return [('conjugate', i, letter) for letter in word]


def multiply_inverse(i, j):
    return [('invert', j), ('multiply', i, j), ('invert', j)]


def ak3_class3_path():
    """48 literal moves; endpoint equals (x,y) modulo gamma_4, not in F."""
    c = 'XYxy'
    moves = class2_path(3)
    # Fix the x coordinate's -2 Lx + Ly, then y coordinate's -Lx + Ly.
    moves += conjugate_word(0, c + c)
    moves += [('multiply', 0, 1)]
    moves += conjugate_word(0, c)
    moves += multiply_inverse(0, 1)
    moves += conjugate_word(0, inverse_word(c))
    moves += conjugate_word(1, c)
    moves += [('multiply', 1, 0)]
    moves += conjugate_word(1, c)
    moves += multiply_inverse(1, 0)
    moves += conjugate_word(1, inverse_word(c))
    return moves


def compose(a, b):
    """Permutation composition a after b."""
    return tuple(a[b[i]] for i in range(len(a)))


def pinv(a):
    result = [0] * len(a)
    for i, j in enumerate(a):
        result[j] = i
    return tuple(result)


def cycle(size, *entries):
    result = list(range(size))
    for a, b in zip(entries, entries[1:] + entries[:1]):
        result[a] = b
    return tuple(result)


def finite_group(x, y):
    identity = tuple(range(len(x)))
    generated = {identity}
    queue = deque([identity])
    while queue:
        u = queue.popleft()
        for g in (x, y, pinv(x), pinv(y)):
            v = compose(u, g)
            if v not in generated:
                generated.add(v)
                queue.append(v)
    return generated


def pvalue(word, x, y):
    letters = {'x': x, 'X': pinv(x), 'y': y, 'Y': pinv(y)}
    result = tuple(range(len(x)))
    for letter in word:
        result = compose(result, letters[letter])
    return result


def neighbors(pair, x, y):
    """15-move symmetric alphabet: 2 inversions, swap, 4 products, 8 conjugations."""
    a, b = pair
    yield (pinv(a), b)
    yield (a, pinv(b))
    yield (b, a)
    for g in (b, pinv(b)):
        yield (compose(a, g), b)
    for g in (a, pinv(a)):
        yield (a, compose(b, g))
    for g in (x, pinv(x), y, pinv(y)):
        gi = pinv(g)
        yield (compose(compose(gi, a), g), b)
        yield (a, compose(compose(gi, b), g))


def quotient_distance(n, x, y):
    start = (pvalue('x' * n + 'Y' * (n + 1), x, y),
             pvalue('xyxYXY', x, y))
    target = (x, y)
    queue = deque([start])
    distances = {start: 0}
    while queue:
        current = queue.popleft()
        if current == target:
            return distances[current]
        for nxt in neighbors(current, x, y):
            if nxt not in distances:
                distances[nxt] = distances[current] + 1
                queue.append(nxt)
    raise AssertionError('Unexpected disconnected finite-quotient images')


def main():
    assert class2_value('XYxy') == (0, 0, 1)
    assert class2_value('xyxYXY') == (1, -1, -1)
    for n in range(1, 31):
        final = replay_free(n)
        assert [class2_value(w) for w in final] == [(1, 0, 0), (0, 1, 0)]
        assert len(class2_path(n)) == n + n * (n - 1) // 2 + 6
    final = replay_free(3)
    assert final != ['x', 'y']
    residuals = [reduce_word(final[0] + 'X'), reduce_word(final[1] + 'Y')]
    leading = []
    for residual in residuals:
        expansion = magnus(residual)
        assert not any(0 < len(m) < 3 for m in expansion)
        leading.append({m: c for m, c in sorted(expansion.items()) if len(m) == 3})
    expected = [
        {'xxy': -2, 'xyx': 4, 'xyy': 1, 'yxx': -2, 'yxy': -2, 'yyx': 1},
        {'xxy': -1, 'xyx': 2, 'xyy': 1, 'yxx': -1, 'yxy': -2, 'yyx': 1},
    ]
    assert leading == expected
    class3_final = replay_free(3, ak3_class3_path())
    assert len(ak3_class3_path()) == 48
    assert class3_final != ['x', 'y']
    class3_residuals = [reduce_word(class3_final[0] + 'X'),
                        reduce_word(class3_final[1] + 'Y')]
    class4_errors = []
    for residual in class3_residuals:
        assert magnus(residual, 3) == {'': 1}
        class4_errors.append({m: c for m, c in sorted(magnus(residual, 4).items())
                              if len(m) == 4})
    assert all(class4_errors)
    examples = [
        ('S3', cycle(3, 0, 1), cycle(3, 0, 1, 2), 6),
        ('S4', cycle(4, 0, 1), cycle(4, 0, 1, 2, 3), 24),
        ('A5', cycle(5, 0, 1, 2), cycle(5, 0, 1, 2, 3, 4), 60),
    ]
    distances = {}
    for label, x, y, order in examples:
        assert len(finite_group(x, y)) == order
        distances[label] = quotient_distance(3, x, y)
    print(json.dumps({
        'class2_checks': 'AK(n), n=1..30',
        'ak3_literal_move_count': len(class2_path(3)),
        'ak3_final_free_words': final,
        'ak3_degree3_residuals': leading,
        'ak3_class3_literal_move_count': len(ak3_class3_path()),
        'ak3_class3_final_free_word_lengths': [len(w) for w in class3_final],
        'ak3_class3_path_degree4_residuals': class4_errors,
        'ak3_finite_quotient_distances_15_move_alphabet': distances,
        'scope': 'Class-2/3 quotient trivializations only; no free-group AC solution',
    }, indent=2))


if __name__ == '__main__':
    main()
