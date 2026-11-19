"""Check complete free-word balls against the native word-ID search."""

import argparse
import json
from subprocess import check_output

from stallings_search import inverse, reduce


def neighbors(state):
    inverses = tuple(map(inverse, state))
    for i, row in enumerate(state):
        unchanged = state[:i] + state[i + 1:]
        edited = {inverses[i]}
        for letter in "xXyY":
            edited.add(reduce(letter + row + inverse(letter)))
        for j, other in enumerate(state):
            if i != j:
                edited.add(reduce(row + other))
                edited.add(reduce(row + inverses[j]))
        for word in edited:
            if word != row:
                yield tuple(sorted(unchanged + (word,)))


def literal(spare, bound):
    tail = ("",) * spare
    start = tuple(sorted(("xxxYYYY", "xyxYXY") + tail))
    finish = tuple(sorted(("x", "y") + tail))
    seen = [{start}, {finish}]
    frontier = [set(ball) for ball in seen]
    radii = [0, 0]
    for _ in range(bound):
        side = min(range(2), key=lambda i: len(frontier[i]))
        next_front = {
            adjacent for row in frontier[side] for adjacent in neighbors(row)
            if adjacent not in seen[side]
        }
        assert next_front.isdisjoint(seen[1 - side])
        radii[side] += 1
        seen[side].update(next_front)
        frontier[side] = next_front
    return {"radii": radii, "visited": list(map(len, seen))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("native_search")
    args = parser.parse_args()
    comparisons = []
    for spare, bound in ((0, 10), (1, 8), (2, 8), (3, 6), (4, 6)):
        result = literal(spare, bound)
        native = json.loads(check_output([args.native_search, str(spare), str(bound)]))
        assert native["distance"] is None
        assert result == {key: native[key] for key in result}
        comparisons.append({"spare_rows": spare, "bound": bound, **result})
    print(json.dumps(comparisons, indent=2))


if __name__ == "__main__":
    main()
