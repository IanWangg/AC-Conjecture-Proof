"""Compile the five energy-20 releases from the strict Round 16 stable path."""

import argparse
from io import BytesIO
import json
from pathlib import Path

from elementary_verify import replay
from round03_stable_proof_pivot import canonical
from round04_stable_proof_paths import edge
from round06_stable_proof_cap23_charts import compact_row
from round06_stable_proof_strict_escape import StrictPath
from round07_stable_proof_compile_join import lift_from
from round15_stable_proof_splice import align, statistics

ENDPOINT = ("XXYYYxYXY", "XXYYxYXXyxxY")


def compile_suffix(route, cap):
    marked = lift_from(ENDPOINT, route, cap)
    with BytesIO() as sink:
        path = StrictPath(ENDPOINT, sink)
        for slot, row in enumerate(path.rows):
            align(path, slot, canonical(row))
        for destination in marked[1:]:
            _, moves = edge(tuple(path.rows), destination, cap, "xXyY")
            path.extend(moves)
        assert compact_row(path.rows) == compact_row(route[-1])
        assert sum(map(len, path.rows)) == 20
        assert path.cyclic_peak <= cap
        suffix = dict(format="ordinary-ac-elementary-v1", start=list(ENDPOINT),
                      target=path.rows, moves=list(map(json.loads, sink.getvalue().splitlines()[1:])))
    replay(suffix)
    return suffix


def stable_suffix(prefix, suffix, output):
    with output.open("wb") as sink:
        path = StrictPath(prefix[0]["start"], sink)
        path.extend(prefix[1:-1])
        assert tuple(path.rows) == ENDPOINT == tuple(suffix["start"])
        assert path.cyclic_peak == 33 and path.peak_rank == 3
        path.extend(suffix["moves"])
        assert path.rows == suffix["target"] and path.cyclic_peak == 33
        path.record((json.dumps({"target": path.rows}, separators=(",", ":")) + "\n").encode())
        return statistics(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prefix", type=Path)
    parser.add_argument("destinations", type=Path)
    parser.add_argument("output_directory", type=Path)
    args = parser.parse_args()
    prefix = list(map(json.loads, args.prefix.read_text().splitlines()))
    routes = json.loads(args.destinations.read_text())
    args.output_directory.mkdir(parents=True, exist_ok=True)
    receipts = []
    for i, route in enumerate(routes, 1):
        route = list(map(tuple, route))
        cap = max(sum(map(len, pair)) for pair in route)
        suffix = compile_suffix(route, cap)
        output = args.output_directory / f"ordinary-{i}.json"
        output.write_text(json.dumps(suffix, separators=(",", ":")) + "\n")
        receipt = stable_suffix(prefix, suffix, args.output_directory / f"stable-{i}.jsonl")
        receipts.append(dict(products=len(route) - 1, ordinary_cyclic_peak=cap,
                             ordinary=replay(suffix), stable=receipt))
    print(json.dumps(receipts, indent=2))


if __name__ == "__main__":
    main()
