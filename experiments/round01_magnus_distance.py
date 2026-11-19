"""Replay the small-distance and word-support controls for the modulus-2 tower."""

import json
from functools import cache
from itertools import groupby

ONE = frozenset({()})


@cache
def generator(index):
    return frozenset({(), (index,)})


@cache
def multiply(left, right, degree):
    result = set()
    for a in left:
        for b in right:
            if len(a) + len(b) <= degree:
                term = a + b
                if term in result:
                    result.remove(term)
                else:
                    result.add(term)
    return frozenset(result)


@cache
def inverse(poly, degree):
    positive = poly - ONE
    result = power = ONE
    for _ in range(degree):
        power = multiply(power, positive, degree)
        if not power:
            break
        result ^= power
    return result


def evaluate(word, degree):
    result = ONE
    for letter in word:
        factor = generator(abs(letter) - 1)
        if letter < 0:
            factor = inverse(factor, degree)
        result = multiply(result, factor, degree)
    return result


@cache
def insert_variable(poly, index):
    return frozenset(tuple(j + (j >= index) for j in term) for term in poly)


@cache
def delete_variable(poly, index):
    return frozenset(
        tuple(j - (j > index) for j in term) for term in poly if index not in term
    )


def neighbors(rows, degree, stable, rank_cap):
    rank = len(rows)
    inverses = tuple(inverse(row, degree) for row in rows)
    for i, row in enumerate(rows):
        prefix, suffix = rows[:i], rows[i + 1 :]
        yield prefix + (inverses[i],) + suffix
        for j, donor in enumerate(rows):
            if i == j:
                continue
            yield prefix + (multiply(row, donor, degree),) + suffix
            yield prefix + (multiply(row, inverses[j], degree),) + suffix
            if i < j:
                yield prefix + (donor,) + rows[i + 1 : j] + (row,) + rows[j + 1 :]
        for j in range(rank):
            a = generator(j)
            b = inverse(a, degree)
            for left, right in ((a, b), (b, a)):
                product = multiply(multiply(left, row, degree), right, degree)
                yield prefix + (product,) + suffix
    if stable:
        for g in range(rank):
            for i, row in enumerate(rows):
                survivors = rows[:i] + rows[i + 1 :]
                if row == generator(g) and all(
                    g not in term for survivor in survivors for term in survivor
                ):
                    yield tuple(delete_variable(survivor, g) for survivor in survivors)
        if rank < rank_cap:
            for g in range(rank + 1):
                reindexed = tuple(insert_variable(row, g) for row in rows)
                for i in range(rank + 1):
                    yield reindexed[:i] + (generator(g),) + reindexed[i:]


def bounded_distance(start, target, degree, move_bound, stable):
    """Exhaust the two balls up to a combined radius of move_bound."""
    if start == target:
        return 0
    assert len(start) == len(target)
    # Equal endpoint ranks require one deletion for each insertion.
    rank_cap = len(start) + move_bound // 2
    visited = [{start}, {target}]
    frontiers = [{start}, {target}]
    for combined_radius in range(1, move_bound + 1):
        side = min(range(2), key=lambda i: len(frontiers[i]))
        seen_here, seen_other = visited[side], visited[1 - side]
        next_frontier = set()
        for rows in frontiers[side]:
            for successor in neighbors(rows, degree, stable, rank_cap):
                if successor in seen_other:
                    return combined_radius
                if successor not in seen_here:
                    next_frontier.add(successor)
        if not next_frontier:
            break
        seen_here.update(next_frontier)
        frontiers[side] = next_frontier
    return None


def word_support_controls():
    words_checked = support_checks = 0
    for rank in range(1, 4):
        letters = tuple(i * sign for i in range(1, rank + 1) for sign in (1, -1))
        frontier = [()]
        for degree in range(1, 6):
            frontier = [
                word + (a,) for word in frontier for a in letters if not word or a != -word[-1]
            ]
            for word in frontier:
                runs = [(i - 1, len(tuple(run))) for i, run in groupby(map(abs, word))]
                witness = tuple(i for i, length in runs for _ in range(length & -length))
                polynomial = evaluate(word, degree)
                assert witness in polynomial
                for i in range(rank):
                    assert any(i in term for term in polynomial) == (i in witness)
                    support_checks += 1
                words_checked += 1
    assert evaluate((2,) * 8, 7) == ONE
    assert evaluate((2,) * 8, 8) == ONE | {(1,) * 8}
    return {
        "reduced_words_checked": words_checked,
        "generator_support_checks": support_checks,
        "eighth_power_first_visible_degree": 8,
    }


def main():
    controls = word_support_controls()
    distances = []
    words = ((1, 1, 1, -2, -2, -2, -2), (1, 2, 1, -2, -1, -2))
    target = (generator(0), generator(1))
    for degree, expected in enumerate((1, 3, 5, 9, 11), start=1):
        start = tuple(evaluate(word, degree) for word in words)
        ordinary = bounded_distance(start, target, degree, expected, stable=False)
        assert ordinary == expected
        stable = None
        if degree <= 4:
            stable = bounded_distance(start, target, degree, ordinary, stable=True)
            assert stable == ordinary
        distances.append({"degree": degree, "ordinary_distance": ordinary, "stable_distance": stable})
        for fn in (multiply, inverse, insert_variable, delete_variable):
            fn.cache_clear()
    print(json.dumps({"word_support_controls": controls, "ak3": distances}, indent=2))


if __name__ == "__main__":
    main()
