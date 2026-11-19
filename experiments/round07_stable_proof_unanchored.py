"""Replay actual singleton deletions for the three low unanchored chart orbits."""

import argparse
from contextlib import nullcontext
import json
from pathlib import Path

from free_waypoint_search import conj_ops
from round03_stable_proof_pivot import canonical
from round04_stable_proof_paths import compile_rank_three, edge, replay
from round07_stable_proof_compile_chart import compile_path
from stallings_search import apply, inverse


def rank_three_path(pair_route, excursion):
    certificate = compile_rank_three(pair_route, [])
    state = tuple(certificate["target"])
    assert set(state) == {"XXXYxyy", "XXyyxY", "Z"}
    if "XXXYxZyy" in excursion[0]:
        pivot, recipient = state.index("Z"), state.index("XXXYxyy")
        insert = conj_ops(pivot, inverse("yy"))
        insert += [{"op": "multiply", "i": recipient, "j": pivot}]
        insert += conj_ops(pivot, "yy")
        for move in insert:
            state = apply(state, move)
        assert state[recipient] == "XXXYxZyy"
        certificate["moves"].extend(insert)
        certificate["macro_boundaries"].append(len(certificate["moves"]))
    for target in excursion:
        state, operations = edge(state, target, 23, "xXyYzZ")
        certificate["moves"].extend(operations)
        certificate["macro_boundaries"].append(len(certificate["moves"]))
    certificate["target"] = state
    return certificate


def run(pair_route, excursion, casting, ledger):
    prefix = rank_three_path(pair_route, excursion)
    proof = replay(prefix)
    ordered = list(map(canonical, proof["target"]))
    assert sorted(ordered) == casting["rank_three_rows"]
    plan = {"marker_changes": [], "resulting_ambient_rows": ordered, "eliminated": casting["eliminated"],
            "pivot": casting["pivot"], "pair": casting["projected_pair"]}
    strict_receipt = compile_path(prefix, plan, ledger)
    assert strict_receipt["rank_peak"] == 3
    return prefix, {"rank_three_prefix": proof, "literal_pivot": casting["pivot"],
                    "eliminated_letter": casting["eliminated"], "strict_stable": strict_receipt}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pair_route", type=Path)
    parser.add_argument("excursion", type=Path)
    parser.add_argument("orbit_receipt", type=Path)
    parser.add_argument("case", type=int)
    parser.add_argument("prefix_certificate", type=Path)
    parser.add_argument("--write-ledger", type=Path)
    args = parser.parse_args()
    movie = [tuple(line.split()) for line in args.excursion.open()]
    source = json.loads(args.orbit_receipt.read_text())["minimal_missing_orbits"][args.case]["restated_source"]
    with args.write_ledger.open("wb") if args.write_ledger else nullcontext() as sink:
        prefix, result = run(json.loads(args.pair_route.read_text()), movie, source, sink)
    args.prefix_certificate.write_text(json.dumps(prefix, indent=2) + "\n")
    print(json.dumps(result, indent=2))
