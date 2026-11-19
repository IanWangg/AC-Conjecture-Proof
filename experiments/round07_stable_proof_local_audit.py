"""Independently verify small closed cyclic components and their cap-entry routes."""

import argparse
from collections import deque
from functools import cache
from itertools import product
import json
from pathlib import Path

from euclidean_primitive_audit import primitive_cyclic_word
from round03_stable_proof_pivot import canonical
from round06_stable_proof_cap23_charts import compact_row
from stallings_search import inverse, reduce

STARTS = (
    ("XXYXyxYxyXYxy", "XYXyXYXyyxYxy"),
    ("XXXYXyyxYYxyXYYxy", "XYXyXyxYYxy"),
    ("XXXYXyxxYXyyxYxy", "XXYXyxYxyXYxy"),
)
MARKED = ("XXYxyXYxyxYXy", "XXyXYXyxYxyxYxy")


@cache
def rotations(word):
    return {w[i:] + w[:i] for w in (word, inverse(word)) for i in range(len(word))}


@cache
def bridges(bound):
    tail = [""]
    level = [""]
    for _ in range(bound):
        level = [v + a for v in level for a in "xXyY" if not v or v[-1] != a.swapcase()]
        tail.extend(level)
    return [(word, inverse(word)) for word in tail]


def successors(pair, cap):
    found = set()
    examined = admitted = 0
    for receiver, donor in (pair, pair[::-1]):
        bound = max(0, (cap - len(receiver) - 2 * len(donor)) // 2)
        for u, v, (bridge, reverse) in product(rotations(receiver), rotations(donor), bridges(bound)):
            examined += 1
            change = canonical(reduce(u + bridge + v + reverse))
            if len(change) + len(donor) <= cap:
                assert change
                admitted += 1
                found.add(compact_row((change, donor)))
    return found, examined, admitted


def catalogue(path):
    raw = path.read_bytes().splitlines(keepends=True)
    out = {line: tuple(line.decode("ascii").split()) for line in raw}
    assert len(out) == len(raw) and all(compact_row(pair) == line for line, pair in out.items())
    return out


def check(work, c29):
    # Each entry uses a bounded ordinary invariant followed by an exact
    # quotient path into the independently checked AK(3) component.
    references = ("cap30_anchored", "minimum28_c30", "minimum29_c30", "marked0_c36")
    routes = ("cap31_anchored", "minimum28_c31", "minimum29_c31", "marked0_c37")
    expected_targets = set()
    results = []
    for seed, ref, route, lower in zip((*STARTS, MARKED), references, routes, (30, 30, 30, 36)):
        closed = catalogue(work / (ref + ".tsv"))
        assert compact_row(seed) in closed
        attempted = accepted = 0
        links = {}
        for key, pair in closed.items():
            assert sum(map(len, pair)) <= lower
            assert not any(primitive_cyclic_word(word) for word in pair)
            neighbors, examined, admitted = successors(pair, lower)
            assert neighbors <= closed.keys()
            links[key] = neighbors
            attempted += examined
            accepted += admitted
        reached = {compact_row(seed)}
        pending = deque(reached)
        while pending:
            new = links[pending.popleft()] - reached
            reached.update(new)
            pending.extend(new)
        assert reached == closed.keys()
        generated = json.loads((work / (ref + ".json")).read_text())
        assert (generated["expanded_orbits"], generated["product_candidates"], generated["admitted_product_candidates"]) == (
            len(closed), attempted, accepted
        )
        assert generated["cyclic_cap"] == lower and generated["closed"] and not generated["target_found"]
        route_file = work / (route + ".route.tsv")
        path = list(catalogue(route_file).values())
        assert compact_row(path[0]) == compact_row(seed)
        for u, v in zip(path, path[1:]):
            assert compact_row(v) in successors(u, lower + 1)[0]
        assert max(map(lambda pair: sum(map(len, pair)), path)) == lower + 1
        expected_targets.add(compact_row(path[-1]))
        results.append(dict(seed=seed, independently_checked_cap=lower, signed_orbits=len(closed), products=attempted,
                            minimum_cyclic_energy=min(sum(map(len, pair)) for pair in closed.values()),
                            primitive_free_enclosure=True, route_one_above_cap=path,
                            anchor=path[-1], cyclic_products_to_anchor=len(path) - 1,
                            ordinary_minimum_entry_peak=lower + 1))
    with c29.open("rb") as checkfile:
        found = {row for row in checkfile if row in expected_targets}
    assert found == expected_targets
    return {"independent_audit": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("working_directory", type=Path)
    parser.add_argument("compact_c29", type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.working_directory, args.compact_c29), indent=2))
