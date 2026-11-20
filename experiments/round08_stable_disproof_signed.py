"""Meet in the middle on signed integral exponent vectors and crossing counts."""

import argparse
from collections import defaultdict
import json


def add_row(matrix, receiver, donor, sign):
    row = tuple(a + sign * b for a, b in zip(matrix[receiver], matrix[donor]))
    return (*matrix[:receiver], row, *matrix[receiver + 1:])


def signed_vectors(vectors):
    return tuple(sorted(min(vector, tuple(-value for value in vector)) for vector in vectors))


def signed_columns(matrix):
    return signed_vectors(zip(*matrix))


def identity(rank):
    return tuple(tuple(int(i == j) for j in range(rank)) for i in range(rank))


def check(padding, depth):
    rank = padding + 2
    unit = identity(rank)
    basis = ((-1, 4, *(0,) * padding), (-1, 3, *(0,) * padding), *unit[2:])
    inverse = ((3, -4, *(0,) * padding), (1, -1, *(0,) * padding), *unit[2:])
    cuts = range(1, 1 << padding)
    start_counts = (0,) * len(cuts)
    menus = []
    for i in range(rank):
        for j in range(rank):
            if i == j:
                continue
            separation = tuple(((cut << 2) >> i ^ (cut << 2) >> j) & 1 for cut in cuts)
            for sign in (-1, 1):
                menus.append(((i, j, sign), separation))

    def states(start, radius):
        current = {(start, start_counts): None}
        history = [current]
        for _ in range(radius):
            following = {}
            for matrix, counts in current:
                for move, separation in menus:
                    new_matrix = add_row(matrix, *move)
                    new_counts = tuple(min(3, old + extra) for old, extra in zip(counts, separation))
                    following.setdefault((new_matrix, new_counts), ((matrix, counts), move))
            history.append(following)
            current = following
        return history

    def trace(history, final):
        moves = []
        for layer in reversed(history[1:]):
            final, move = layer[final]
            moves.append(move)
        return moves[::-1]

    left = states(inverse, depth // 2)
    right = states(unit, depth - depth // 2)
    keys = defaultdict(list)
    for state in left[-1]:
        keys[signed_columns(state[0])].append(state)
    hits = 0
    witness = None
    for state in right[-1]:
        matrix, counts = state
        for prefix in keys[signed_columns(matrix)]:
            if any(a + b < 3 for a, b in zip(counts, prefix[1])):
                continue
            hits += 1
            if witness is None:
                path = trace(left, prefix)
                path += [(i, j, -sign) for i, j, sign in reversed(trace(right, state))]
                endpoint = unit
                crossings = [0] * len(cuts)
                separation = dict(menus)
                for move in path:
                    endpoint = add_row(endpoint, *move)
                    for index, additional in enumerate(separation[move]):
                        crossings[index] += additional
                assert signed_vectors(endpoint) == signed_vectors(basis)
                assert min(crossings) >= 3
                witness = {"moves": path, "endpoint": endpoint, "cut_crossings": crossings}
    return {"padding": padding, "products": depth, "prefix_states": len(left[-1]),
            "inverse_suffix_states": len(right[-1]), "matching_state_pairs": hits, "witness": witness}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("padding", type=int, choices=(1, 2, 3))
    parser.add_argument("first", type=int)
    parser.add_argument("last", type=int)
    args = parser.parse_args()
    for products in range(args.first, args.last + 1):
        print(json.dumps(check(args.padding, products)), flush=True)


if __name__ == "__main__":
    main()
