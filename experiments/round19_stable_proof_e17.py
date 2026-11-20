"""Independently lift the chartless cap-28 transfers from the first E17 marking."""

import argparse
import json
from pathlib import Path

from round03_stable_proof_pivot import canonical
from round04_stable_proof_paths import edge
from round06_stable_proof_cap23_charts import compact_row
from round06_stable_proof_strict_escape import StrictPath
from round09_stable_proof_lift_excursion import signed_rows
from round15_stable_proof_splice import align, statistics


def lift(start, route):
    choices = {tuple(map(canonical, start)): []}
    assert tuple(sorted(next(iter(choices)))) in signed_rows(route[0])
    for goal in route[1:]:
        marked = signed_rows(goal)
        next_choices = {}
        for source, prefix in choices.items():
            for target in sorted(marked):
                if len(set(source) & set(target)) < 2:
                    continue
                local_cap = max(sum(map(len, source)), sum(map(len, target)))
                state, moves = edge(source, target, local_cap, "xXyYzZ")
                assert tuple(sorted(state)) == target
                candidate = prefix + moves
                if state not in next_choices or len(candidate) < len(next_choices[state]):
                    next_choices[state] = candidate
        assert next_choices
        choices = next_choices
    targets = [
        (state, moves, state.index("Z"))
        for state, moves in choices.items()
        if "Z" in state and sum("z" in word.lower() for word in state) == 1
    ]
    assert targets, "the lifted chart did not preserve the auxiliary generator"
    return min(targets, key=lambda item: (len(item[1]), item[0]))


def compile_routes(ordinary, routes, catalogue, output_directory):
    start = tuple(ordinary["target"])
    minima = [tuple(row.split()) for row in catalogue.read_text().splitlines()
              if sum(map(len, row.split())) == 17]
    assert start == minima[0] and len(minima) == 9
    output_directory.mkdir(parents=True, exist_ok=True)
    receipts = []
    for index in range(1, 10):
        route = [tuple(row) for row in routes[str(index)]]
        goal, moves, slot = lift((*start, "z"), route)
        output = output_directory / f"stable-{index}.jsonl"
        with output.open("wb") as sink:
            path = StrictPath(ordinary["start"], sink)
            path.extend(ordinary["moves"])
            assert tuple(path.rows) == start and path.cyclic_peak == 33
            path.add({"op": "stabilize", "generator": "z"})
            for row, word in enumerate(path.rows):
                align(path, row, canonical(word))
            path.extend(moves)
            assert tuple(path.rows) == goal
            align(path, slot, "z")
            path.add({"op": "destabilize", "generator": "z", "i": slot})
            assert compact_row(path.rows) == compact_row(minima[index-1])
            path.record((json.dumps({"target": path.rows}, separators=(",", ":")) + "\n").encode())
            receipts.append(dict(
                signed_release=minima[index-1], cyclic_products=len(route) - 1,
                excursion_cyclic_peak=max(sum(map(len, point)) for point in route),
                excursion_steps=path.total - len(ordinary["moves"]),
                complete=statistics(path),
            ))
    return receipts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ordinary_entry", type=Path)
    parser.add_argument("orbit_routes", type=Path)
    parser.add_argument("minima", type=Path)
    parser.add_argument("output_directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(compile_routes(
        json.loads(args.ordinary_entry.read_text()), json.loads(args.orbit_routes.read_text()), args.minima,
        args.output_directory,
    ), indent=2))


if __name__ == "__main__":
    main()
