"""Bound padded Magnus paths by ranked-alphabet walks with spare identity rows."""

import argparse
from functools import cache
import json

from round01_magnus_distance import ONE as SET_ONE, evaluate, generator
from round01_stable_disproof_search import AK3, ONE, MagnusQuotient, bounded_distance


def endpoints(rows, basis, identity, padding):
    tail = (identity,) * padding
    return tuple(sorted((*rows, *tail))), tuple(sorted((*basis, *tail)))


def packed_search(degree, padding, radius):
    group = MagnusQuotient(2, degree)
    start, target = endpoints(map(group.evaluate, AK3), group.generators, ONE, padding)
    result = bounded_distance(start, target, group, radius, unordered=True)
    group.multiply.cache_clear()
    group.inverse.cache_clear()
    return dict(degree=degree, spare_rows=padding, limit=radius, **result)


def set_search(degree, padding, limit):
    """Rebuild the layer check with explicit monomial sets and interned values."""
    ids = {}
    polynomials = []

    def intern(value):
        index = ids.get(value)
        if index is None:
            index = len(polynomials)
            ids[value] = index
            polynomials.append(value)
        return index

    @cache
    def multiply(a, b):
        terms = set()
        for head in polynomials[a]:
            for tail in polynomials[b]:
                if len(head) + len(tail) <= degree:
                    word = head + tail
                    terms.symmetric_difference_update((word,))
        return intern(frozenset(terms))

    identity = intern(SET_ONE)

    @cache
    def inverse(a):
        # Test the inverse using the uniform exponent bound U^(2^l)=1.
        exponent = (1 << degree.bit_length()) - 1
        result, power = identity, a
        while exponent:
            if exponent & 1:
                result = multiply(result, power)
            exponent >>= 1
            if exponent:
                power = multiply(power, power)
        assert multiply(a, result) == identity
        return result

    basis = tuple(intern(generator(i)) for i in range(2))
    letters = tuple((a, inverse(a)) for a in basis)
    start, target = endpoints((intern(evaluate(w, degree)) for w in AK3), basis, identity, padding)
    assert start != target
    seen = [{start}, {target}]
    frontier = [seen[0].copy(), seen[1].copy()]
    distance = None
    for radius in range(1, limit + 1):
        side = min(range(2), key=lambda i: len(frontier[i]))
        this, opposite = seen[side], seen[1 - side]
        following = set()
        for rows in frontier[side]:
            inverses = [inverse(row) for row in rows]
            for i, a in enumerate(rows):
                rest = rows[:i] + rows[i + 1 :]
                changes = {inverses[i]}
                for j, b in enumerate(rows):
                    if j != i:
                        changes.add(multiply(a, b))
                        changes.add(multiply(a, inverses[j]))
                for x, xinv in letters:
                    changes.add(multiply(multiply(x, a), xinv))
                    changes.add(multiply(multiply(xinv, a), x))
                changes.discard(a)
                for changed in changes:
                    successor = tuple(sorted(rest + (changed,)))
                    if successor in opposite:
                        distance = radius
                        break
                    if successor not in this:
                        following.add(successor)
                if distance is not None:
                    break
            if distance is not None:
                break
        if distance is not None or not following:
            break
        frontier[side] = following
        this.update(following)
    return dict(degree=degree, spare_rows=padding, limit=limit, distance=distance,
                last_radius=radius, visited=list(map(len, seen)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--independent", action="store_true",
                        help="also check all essential cases with monomial-set arithmetic")
    parser.add_argument("--extended", action="store_true",
                        help="check all positive-padding possibilities at stable length fourteen")
    args = parser.parse_args()

    if args.extended:
        exclusions = [packed_search(7, 1, 12), packed_search(6, 2, 10), packed_search(4, 3, 8)]
        assert all(result["distance"] is None for result in exclusions)
        print(json.dumps({"positive_padding_exclusions_at_stable_length_14": exclusions}, indent=2))
        return

    critical = [packed_search(6, 1, 11), packed_search(5, 2, 9), packed_search(4, 3, 7)]
    assert all(result["distance"] is None for result in critical)
    control = packed_search(5, 1, 11)
    assert control["distance"] == 10
    extension = packed_search(6, 2, 10)
    assert extension["distance"] is None
    if args.independent:
        for item in critical:
            reference = set_search(item["degree"], item["spare_rows"], item["limit"])
            assert item == reference, (item, reference)
    print(json.dumps({
        "degree_seven_padding_exclusions": critical,
        "degree_five_one_identity_control": control,
        "stronger_two_identity_exclusion": extension,
        "degree_seven_stable_distance": {"ordered": 14, "unordered": 14},
    }, indent=2))


if __name__ == "__main__":
    main()
