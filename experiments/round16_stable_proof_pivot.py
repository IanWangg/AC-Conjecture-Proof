"""Compile a single-pivot tail from the strict Round 15 literal chart."""

import argparse
import json
from pathlib import Path

from round03_stable_proof_pivot import canonical
from round04_stable_proof_paths import edge, replay
from round06_stable_proof_strict_escape import StrictPath
from round14_stable_proof_local_chart import LITERAL, START, TARGET
from round15_stable_proof_splice import align, statistics
from stallings_search import inverse


def clear(path, prefix):
    replay(prefix)
    assert tuple(prefix["start"]) == START and tuple(prefix["target"]) == LITERAL
    path.add({"op": "stabilize", "generator": "z"})
    path.extend(prefix["moves"])
    pivot = inverse(path.rows[0])
    index = pivot.index("z")
    tail = pivot[index + 1 :] + pivot[:index]
    align(path, 0, "z" + tail)
    for slot, word in enumerate(TARGET, 1):
        path.change_occurrences(slot, "z", inverse(tail), 0)
        align(path, slot, word)
    assert path.rows == ["zXyxxyy", *TARGET]
    return statistics(path) | {"final_words": path.rows.copy()}


def compile_route(prefix, route, output, stop_after=None):
    with output.open("wb") as sink:
        path = StrictPath(START[:2], sink)
        cleared = clear(path, prefix)
        if route is not None:
            points = [tuple(row.split()) for row in route.read_text().splitlines()]
            if stop_after is not None:
                assert 0 < stop_after < len(points)
                points = points[:stop_after + 1]
            assert points[-1][0] == "Z"
            assert all("z" not in row.lower() for row in points[-1][1:])
            for slot, word in enumerate(path.rows):
                align(path, slot, canonical(word))
            assert tuple(path.rows) == points[0]
            for point in points[1:]:
                cap = max(sum(map(len, path.rows)), sum(map(len, point)))
                _, moves = edge(tuple(path.rows), tuple(sorted(point)), cap, "xXyYzZ")
                path.extend(moves)
                assert tuple(path.rows) == point
            target = points[-1][1:]
            for slot, word in enumerate(("z", *target)):
                align(path, slot, word)
            path.add({"op": "destabilize", "generator": "z", "i": 0})
            assert tuple(path.rows) == target
        path.record((json.dumps({"target": path.rows}, separators=(",", ":")) + "\n").encode())
        return {
            "cleared_prefix": cleared,
            "tail_products": 0 if route is None else len(points) - 1,
            "complete": statistics(path),
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("literal_prefix", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--route", type=Path)
    parser.add_argument("--stop-after", type=int)
    args = parser.parse_args()
    prefix = json.loads(args.literal_prefix.read_text())
    print(json.dumps(compile_route(prefix, args.route, args.output, args.stop_after), indent=2))


if __name__ == "__main__":
    main()
