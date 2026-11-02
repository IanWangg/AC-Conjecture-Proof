"""Complete finite raw-word peak search for ordinary rank-two AC moves.

Quotient only by relator inversion and permutation, which preserve lengths.
NO cyclic reduction, cyclic rotation, ambient automorphism, or GS restriction.
All free words remain raw freely reduced words; conjugation is by one letter.
"""
import argparse
from collections import Counter, deque
import json
import time


def inverse(word):
    return word.swapcase()[::-1]


def reduce(word):
    out = []
    for c in word:
        if out and out[-1] == c.swapcase():
            out.pop()
        else:
            out.append(c)
    return ''.join(out)


def canonical(pair):
    return tuple(sorted(min(w, inverse(w)) for w in pair))


def neighbors(pair, cap):
    """Full induced quotient graph, not merely moves from one orientation.

    If the recipient's orientation is negative then multiplying and then
    inverting back also emits LEFT multiplication. Both recipient signs are
    essential to make the inversion quotient complete.
    """
    for i in (0, 1):
        j = 1-i
        a, b = pair[i], pair[j]
        for oriented_a in (a, inverse(a)):
            for oriented_b in (b, inverse(b)):
                c = reduce(oriented_a + oriented_b)
                if len(c) + len(b) <= cap:
                    yield canonical((c, b))
        for g in 'xXyY':
            c = reduce(g + a + inverse(g))
            if len(c) + len(b) <= cap:
                yield canonical((c, b))


def search(n, cap, budget=1000000):
    start = canonical(('x'*n + 'Y'*(n+1), 'xyxYXY'))
    if sum(map(len, start)) > cap:
        raise ValueError('cap excludes the starting presentation')
    seen = {start}
    queue = deque([start])
    popped = 0
    target = None
    minimum = sum(map(len, start))
    minimum_pair = start
    begun = time.monotonic()
    while queue:
        pair = queue.popleft()
        popped += 1
        energy = sum(map(len, pair))
        if energy < minimum:
            minimum, minimum_pair = energy, pair
        if pair == ('X', 'Y'):
            target = pair
            break
        for nxt in neighbors(pair, cap):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
        if len(seen) > budget:
            break
    complete = not queue and target is None
    return {'n': n, 'cap': cap, 'start': start,
            'complete_component_exhaustion': complete,
            'target_reached': target is not None,
            'states_discovered': len(seen), 'states_processed': popped,
            'minimum_total_length': minimum, 'minimum_pair': minimum_pair,
            'energy_counts': dict(sorted(Counter(sum(map(len, s)) for s in seen).items())),
            'seconds': round(time.monotonic()-begun, 4)}


def selftest():
    # Directly generate all primitive neighbors from all representatives in
    # the inversion/permutation orbit. Equality checks completeness of our
    # quotient generator independently of its orientation formula.
    from itertools import product
    for pair in [('xY', 'xyX'), ('xyxYXY', 'xxxYYYY'), ('x', 'y')]:
        pair = canonical(pair)
        for cap in (sum(map(len, pair)), sum(map(len, pair))+2):
            expected = set()
            for signs in product((1, -1), repeat=2):
                oriented = tuple(w if sign == 1 else inverse(w)
                                 for w, sign in zip(pair, signs))
                for i in (0, 1):
                    j = 1-i
                    candidates = [reduce(oriented[i] + oriented[j]),
                                  reduce(oriented[i] + inverse(oriented[j]))]
                    candidates += [reduce(g+oriented[i]+inverse(g)) for g in 'xXyY']
                    for c in candidates:
                        if len(c)+len(oriented[j]) <= cap:
                            expected.add(canonical((c, oriented[j])))
            assert set(neighbors(pair, cap)) == expected
    print('selftest: exact quotient adjacency matched all oriented primitive neighbors')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=3)
    parser.add_argument('--cap', type=int, default=15)
    parser.add_argument('--budget', type=int, default=1000000)
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    if args.selftest:
        selftest()
    print(json.dumps(search(args.n, args.cap, args.budget), indent=2))
