"""Verify and compile the cap-24 intrinsic energy-27 branch."""

import argparse
from collections import deque
import json
from pathlib import Path

from euclidean_primitive_audit import primitive_cyclic_word
from round04_chart_screen import chart_projections
from round04_stable_proof_paths import compile_rank_three, edge, replay
from round05_stable_proof_chartless import whitehead_image
from round06_stable_proof_cap23_charts import compact_row
from round07_stable_proof_compile_join import finish, lift_from
from round07_stable_proof_local_audit import catalogue, successors


PAIR = ("XXXYYXXXYYXXXYYYY", "XXYYxxyxyy")
TARGET = ("XXZxZ", "XYYYXzXz", "XYxyyZxZxyz")


def audit(work, cap29):
    closed = catalogue(work / "branch27_c35.tsv")
    neighbors = {}
    attempted = accepted = 0
    for key, pair in closed.items():
        found, examined, admitted = successors(pair, 35)
        assert found <= closed.keys()
        assert not any(primitive_cyclic_word(row) for row in pair)
        neighbors[key] = found
        attempted += examined
        accepted += admitted
    reached = {compact_row(PAIR)}
    pending = deque(reached)
    while pending:
        fresh = neighbors[pending.popleft()] - reached
        reached.update(fresh)
        pending.extend(fresh)
    assert reached == closed.keys()
    generated = json.loads((work / "branch27_c35.json").read_text())
    assert generated["closed"] and generated["expanded_orbits"] == len(closed)
    assert generated["product_candidates"] == attempted and generated["admitted_product_candidates"] == accepted
    path = list(catalogue(work / "branch27_c36.route.tsv").values())
    assert compact_row(path[0]) == compact_row(PAIR)
    assert max(sum(map(len, row)) for row in path) == 36
    for u, v in zip(path, path[1:]):
        assert compact_row(v) in successors(u, 36)[0]
    target = compact_row(path[-1])
    with cap29.open("rb") as file:
        assert any(row == target for row in file)
    return dict(cap35_signed_orbits=len(closed), cap35_product_candidates=attempted,
                cap35_admitted_candidates=accepted, cap35_minimum_energy=min(sum(map(len, p)) for p in closed.values()),
                cap35_no_primitive=True, cap36_exact_anchor_route=path, sharp_ordinary_entry_peak=36)


def rank_three(work):
    route = json.loads((work / "branch27_pair.json").read_text())
    excursion = [tuple(line.split()) for line in (work / "branch27_parent.tsv").open()]
    certificate = compile_rank_three(route, excursion)
    target, moves = edge(certificate["target"], TARGET, 24, "xXyYzZ")
    certificate["target"] = target
    certificate["moves"].extend(moves)
    certificate["maximum_cyclic_length"] = 24
    certificate["macro_boundaries"].append(len(certificate["moves"]))
    summary = replay(certificate)
    proof = json.loads((work / "first_anchors.json").read_text())["shortest_uncovered_examples"][0]
    assert proof["projected_pair"] == list(PAIR)
    assert sorted(summary["target"]) == proof["rank_three_rows"]
    rows = tuple(summary["target"])
    pivot_slot = rows.index(proof["original_pivot"])
    for descent in proof["whitehead_descent"]:
        rows = whitehead_image(rows, descent["multiplier"], descent["cut"])
        assert rows[pivot_slot] == descent["result"][0]
    assert rows[pivot_slot] == "Z" and ("z", "Z", PAIR) in set(chart_projections(rows))
    return certificate, dict(rank_three_replay=summary, intrinsic_chart=proof, maximum_rank_of_stable_connection=4)


def prepare(work):
    orbit_route = list(catalogue(work / "branch27_c36.route.tsv").values())
    there = lift_from(PAIR, orbit_route, 36)
    rooted = json.loads((work / "branch27_anchor.orbit.json").read_text())["orbit_route"]
    back = lift_from(there[-1], rooted[::-1], 29)
    pieces = dict(literal_route_back_to_signed_AK3=back, literal_route_to_anchor=there, signed_AK3=back[-1], cyclic_cap=36)
    (work / "branch27_segments.json").write_text(json.dumps(pieces, indent=2) + "\n")
    return back[-1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("audit", "rank-three", "prepare", "finish"))
    parser.add_argument("work", type=Path)
    parser.add_argument("--cap29", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    if args.mode == "prepare":
        print(*prepare(args.work), sep="\t")
    else:
        if args.mode == "audit":
            assert args.cap29
            result = audit(args.work, args.cap29)
        elif args.mode == "rank-three":
            certificate, result = rank_three(args.work)
        else:
            pieces = json.loads((args.work / "branch27_segments.json").read_text())
            signed = json.loads((args.work / "branch27_signed.json").read_text())["route"]
            certificate, result = finish(pieces, signed)
        if args.mode != "audit":
            assert args.certificate
            args.certificate.write_text(json.dumps(certificate, indent=2) + "\n")
        print(json.dumps(result, indent=2))
