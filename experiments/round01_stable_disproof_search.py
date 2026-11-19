"""Fixed-rank exact search of characteristic-two Magnus quotients.

Each polynomial is a packed nonnegative integer. Monomial bits are grouped
by degree, then by their lexicographic indices in that rank.
"""
import json
from functools import lru_cache

AK3 = ((1, 1, 1, -2, -2, -2, -2), (1, 2, 1, -2, -1, -2))
ONE = 1


class MagnusQuotient:
    def __init__(self, rank, degree):
        self.rank = rank
        self.degree = degree
        self.width = [rank ** i for i in range(degree + 1)]
        self.offset = [sum(self.width[:i]) for i in range(degree + 1)]
        self.mask = [(1 << width) - 1 for width in self.width]
        self.multiply = lru_cache(maxsize=150_000)(self.multiply_uncached)
        self.inverse = lru_cache(maxsize=80_000)(self.inverse_uncached)
        self.generators = tuple(ONE | (1 << (1 + i)) for i in range(rank))
        self.signed_generators = tuple((g, self.inverse(g)) for g in self.generators)

    def multiply_uncached(self, lhs, rhs):
        # Both factors have constant one. Handle the terms involving a
        # constant before multiplying their positive-degree parts.
        result = lhs ^ rhs ^ ONE
        rhs_parts = [(rhs >> self.offset[j]) & self.mask[j] for j in range(1, self.degree)]
        for i in range(1, self.degree):
            block = (lhs >> self.offset[i]) & self.mask[i]
            while block:
                monomial = block & -block
                pos = monomial.bit_length() - 1
                for j, part in enumerate(rhs_parts[: self.degree - i], start=1):
                    result ^= part << (self.offset[i + j] + pos * self.width[j])
                block ^= monomial
        return result

    def inverse_uncached(self, poly):
        # Sum the geometric series in poly + 1 through its nilpotence bound.
        tail = poly ^ ONE
        result = poly
        power = tail
        for _ in range(2, self.degree + 1):
            power = self.multiply(power | ONE, poly) ^ ONE ^ power ^ tail
            if power == 0:
                break
            result ^= power
        return result

    def evaluate(self, word):
        value = ONE
        for letter in word:
            positive, negative = self.signed_generators[abs(letter) - 1]
            value = self.multiply(value, positive if letter > 0 else negative)
        return value

    def neighbors(self, rows, unordered):
        inverses = tuple(self.inverse(row) for row in rows)
        for i, row in enumerate(rows):
            other_rows = rows[:i] + rows[i + 1 :]
            new_rows = {inverses[i]}
            for j, other in enumerate(rows):
                if i != j:
                    new_rows.add(self.multiply(row, other))
                    new_rows.add(self.multiply(row, inverses[j]))
            for positive, negative in self.signed_generators:
                new_rows.add(self.multiply(self.multiply(positive, row), negative))
                new_rows.add(self.multiply(self.multiply(negative, row), positive))
            new_rows.discard(row)
            for new_row in new_rows:
                if unordered:
                    yield tuple(sorted(other_rows + (new_row,)))
                else:
                    yield rows[:i] + (new_row,) + rows[i + 1 :]
            if not unordered:
                for j in range(i + 1, len(rows)):
                    yield rows[:i] + (rows[j],) + rows[i + 1 : j] + (row,) + rows[j + 1 :]


def bounded_distance(initial, target, quotient, limit, unordered):
    """Expand one full breadth-first layer at a time from either endpoint."""
    if initial == target:
        return {"distance": 0, "last_radius": 0, "visited": [1, 1]}
    seen = [{initial}, {target}]
    frontier = [seen[0].copy(), seen[1].copy()]
    for radius in range(1, limit + 1):
        side = min(range(2), key=lambda i: len(frontier[i]))
        following = set()
        for state in frontier[side]:
            for neighbor in quotient.neighbors(state, unordered):
                if neighbor in seen[1 - side]:
                    return {
                        "distance": radius,
                        "last_radius": radius,
                        "visited": [len(states) for states in seen],
                    }
                if neighbor not in seen[side]:
                    following.add(neighbor)
        if not following:
            break
        frontier[side] = following
        seen[side].update(following)
    return {"distance": None, "last_radius": radius, "visited": [len(states) for states in seen]}


def ak3_bounded_test(degree, extra_rows, limit, unordered=True):
    quotient = MagnusQuotient(2 + extra_rows, degree)
    start = tuple(quotient.evaluate(word) for word in AK3) + quotient.generators[2:]
    target = quotient.generators
    if unordered:
        start, target = tuple(sorted(start)), tuple(sorted(target))
    result = bounded_distance(start, target, quotient, limit, unordered)
    result.update(degree=degree, extra_rows=extra_rows, limit=limit, unordered=unordered)
    # The cached bound methods refer back to the quotient object.
    quotient.multiply.cache_clear()
    quotient.inverse.cache_clear()
    return result


def main():
    results = [ak3_bounded_test(d, 0, upper) for d, upper in enumerate((1, 3, 5, 9, 11), 1)]
    assert [run["distance"] for run in results] == [1, 3, 5, 9, 10]
    ordered = ak3_bounded_test(5, 0, 11, unordered=False)
    assert ordered["distance"] == 11
    results.append(ordered)
    for extra in (1, 2):
        # An ordered stable path of length <=10 would also minimize the
        # unordered stable distance, determined from these same bounds.
        limit = 10 - 2 * extra
        search = ak3_bounded_test(5, extra, limit)
        assert search["distance"] is None
        results.append(search)
    print(json.dumps({"degree_five_stable": {"ordered": 11, "unordered": 10}, "runs": results}, indent=2))


if __name__ == "__main__":
    main()
