"""Run the bounded alternating fixed-donor search from the marked energy-17 entry."""

import argparse
from functools import partial
import json
from pathlib import Path

from elementary_verify import replay
from round08_ak3_acm_replay import compile_move
from round08_ak3_acm_search import catalogue_key, cyclic_peak, order, record, scan, search


def run(executable, catalogue, entry, destination):
    source = json.loads(entry.read_text())
    pair = tuple(source["target"])
    runner = partial(scan, executable, 5, 350_000, 22, 96)
    rounds, candidates = search("E17", pair, runner, 36, 8, 34, 3)
    best = {}
    for node in sorted(candidates, key=order):
        best.setdefault(catalogue_key(node[0]), node)
    outstanding = {key for key in best if len(key) - 2 <= 31}
    with catalogue.open("rb") as rows:
        for row in rows:
            outstanding.discard(row)
            if not outstanding:
                break
    absent = outstanding | {key for key in best if len(key) - 2 > 31}
    hits = [hit for row in rounds["rounds"] for hit in row["exact_primitive_hits"]]
    result = {"parameters": {"stages": 5, "allocation": 350_000, "horizon": 22, "bases": 96,
                             "width": 36, "alternations": 8, "maximum": 34},
              "search": rounds, "literal_endpoints": len(candidates), "signed_orbits": len(best),
              "orbits_absent_from_cap31": len(absent), "primitive_endpoints_found": len(hits)}
    if hits or absent:
        endpoint = hits[0] if hits else record(min((best[key] for key in absent), key=order))
        for slot, word, stage in endpoint["route"]:
            suffix, _ = compile_move(source["target"], slot, word, stage)
            source["target"] = suffix["target"]
            source["moves"].extend(suffix["moves"])
        summary = replay(source)
        summary["cyclic_peak"] = cyclic_peak(source)
        destination.write_text(json.dumps(source, separators=(",", ":")) + "\n")
        result.update(selected_certificate_endpoint=endpoint, strict_replay=summary)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("executable", "catalogue", "entry", "destination"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(**vars(args)), indent=2))
