"""Prepare rank-three chart lookups and replay a remasked release prefix."""

import argparse
from array import array
from io import BytesIO
import json
from pathlib import Path

from free_waypoint_search import normalize
from round04_stable_proof_paths import replay
from round05_stable_proof_projections import each_available_chart
from round05_stable_proof_chartless import minima
from round06_stable_proof_cap23_charts import compact_row
from round06_stable_proof_strict_escape import StrictPath
from round09_stable_proof_rank_three_chart import (
    IDENTITY, START, apply_marking, basic_ledger, compile_chart, compose, transport, whitehead_factors,
)
from round11_stable_proof_reverse import certificate
from round12_stable_proof_corridor import lift


def remask(prefix):
    rows = tuple(replay(prefix)["target"])
    minimized, descent, *_ = minima(rows)
    factors = [factor for move in reversed(descent) for factor in whitehead_factors(move, True)]
    with BytesIO() as sink:
        path = StrictPath(START[:2], sink)
        path.add({"op": "stabilize", "generator": "z"})
        marking = IDENTITY
        for basic in factors:
            transport(path, basic_ledger(basic), marking)
            marking = compose(marking, basic)
        transport(path, prefix["moves"], marking)
        assert path.rows == [apply_marking(word, marking) for word in rows]
        for slot, target in enumerate(minimized):
            _, moves = normalize(tuple(path.rows), slot, target)
            path.extend(moves)
        assert tuple(path.rows) == minimized
        moves = [json.loads(line) for line in sink.getvalue().splitlines()[2:]]
    proof = certificate(START, moves, minimized)
    return proof, {"marked_images": dict(zip("xyz", marking)), "descent": descent, "strict": replay(proof)}


def collect(files, output, archive, cap):
    counts = {}
    entries = {}
    for path in files:
        eligible = 0
        with path.open() as stream:
            for line in stream:
                a, b, *_ = line.split()
                if len(a) + len(b) > cap or max(len(a), len(b)) > 31:
                    continue
                eligible += 1
                key = compact_row((a, b))
                entries.setdefault(key, (path.name, line.rstrip().split("\t")))
        counts[path.name] = eligible
    output.write_bytes(b"".join(sorted(entries)))
    exact = set(entries) & {compact_row(tuple(line.split())) for line in archive.read_text().splitlines()}
    return {"eligible_marked_pairs_by_file": counts, "union_signed_orbits": len(entries),
            "energies": dict(sorted(histogram(entries).items())),
            "exact_reverse_hits": [entries[row] for row in sorted(exact)]}


def histogram(rows):
    counts = {}
    for row in rows:
        energy = len(row) - 2
        counts[energy] = counts.get(energy, 0) + 1
    return counts


def coverage(targets_path, lower, outside):
    remaining = set(targets_path.read_bytes().splitlines(keepends=True))
    remaining = {key for key in remaining if len(key) <= 34}
    receipts = {}
    for label, path in (("cap31", lower), ("cap32_additions", outside)):
        found = 0
        with path.open("rb") as source:
            for row in source:
                if row in remaining:
                    remaining.remove(row)
                    found += 1
        receipts[label] = found
    ordered = sorted(remaining, key=lambda w: (len(w), w))
    return {"match_counts": receipts, "not_in_generated_cap32": len(ordered),
            "absent_by_energy": histogram(ordered),
            "shortest_absent": [row.decode().split() for row in ordered[:12]]}


def lift_absent(root, nodes, pairs, coverage_receipt, ledger, rank_three):
    absent = {compact_row(pair) for pair in coverage_receipt["shortest_absent"]}
    possible = []
    for line in pairs.open():
        first, second, parent, *rows = line.split()
        if len(first) + len(second) > 32:
            continue
        if compact_row((first, second)) in absent:
            possible.append((int(parent), tuple(rows), (first, second)))
    assert possible
    offsets, depths = array("Q"), array("I")
    with nodes.open("rb") as source:
        while (line := source.readline()):
            offsets.append(source.tell() - len(line))
            parent, count, *_ = line.split()
            depths.append(0 if len(depths) == 0 else depths[int(parent)] + 1)
        for parent, target, native_projection in sorted(
            possible, key=lambda record: (sum(map(len, record[2])), depths[record[0]], record)
        ):
            route = [target]
            at = parent
            while at < len(offsets):
                source.seek(offsets[at])
                previous, _, *r = source.readline().decode().split()
                route.append(tuple(r))
                at = int(previous)
            route.reverse()
            proof, bounds = lift(root, route, 31)
            for projected, chart in each_available_chart(tuple(proof["target"])):
                key = compact_row(projected)
                if key not in absent:
                    continue
                slot = proof["target"].index(chart["pivot"] if chart["chart"] == "literal" else chart["original_pivot"])
                with BytesIO() as sink:
                    result = compile_chart(proof, slot, sink,
                                           literal=chart["eliminated"] if chart["chart"] == "literal" else None)
                    if compact_row(result["final_words"]) not in absent:
                        continue
                    ledger.write_bytes(sink.getvalue())
                rank_three.write_text(json.dumps(proof, separators=(",", ":")) + "\n")
                return {"orbit_route": route, "boundaries": bounds, "chart": chart,
                        "native_projection": native_projection, "rank_three_replay": replay(proof),
                        "full_strict_stable_replay": result,
                        "absent_compact_projection": compact_row(result["final_words"]).decode().split()}
    raise AssertionError("no selected projection replays in the same marked cap32 exclusion set")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    remask_args = sub.add_parser("remask")
    remask_args.add_argument("source", type=Path)
    remask_args.add_argument("ledger", type=Path)
    collect_args = sub.add_parser("collect")
    collect_args.add_argument("output", type=Path)
    collect_args.add_argument("archive", type=Path)
    collect_args.add_argument("cap", type=int)
    collect_args.add_argument("files", nargs="+", type=Path)
    coverage_args = sub.add_parser("coverage")
    for name in ("targets", "lower", "outside"):
        coverage_args.add_argument(name, type=Path)
    lift_args = sub.add_parser("lift")
    for name in ("root", "nodes", "pairs", "coverage", "ledger", "rank_three"):
        lift_args.add_argument(name, type=Path)
    args = parser.parse_args()
    if args.mode == "remask":
        proof, output = remask(json.loads(args.source.read_text()))
        args.ledger.write_text(json.dumps(proof, separators=(",", ":")) + "\n")
    elif args.mode == "collect":
        output = collect(args.files, args.output, args.archive, args.cap)
    elif args.mode == "coverage":
        output = coverage(args.targets, args.lower, args.outside)
    else:
        output = lift_absent(json.loads(args.root.read_text()), args.nodes, args.pairs,
                             json.loads(args.coverage.read_text()), args.ledger, args.rank_three)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
