"""Test reciprocal donor replacements against a verified reverse catalogue."""

import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import subprocess

from elementary_verify import reduce, replay
from free_waypoint_search import canonical
from round05_ak3_orbit_audit import MAPS
from round07_automorphism_transport import normalize_pair
from round08_ac_proof_two_donors import reverse_moves
from round08_ak3_acm_replay import compile_move
from round08_ak3_acm_search import cyclic_peak
from round10_ac_proof_blocks import vectors
from round11_ak3_targeted_acm import BASIS, load, reverse_suffix


@lru_cache(maxsize=None)
def vector(word):
    return vectors(word)


def candidate_donors(donor, words):
    dx, dy = vector(donor)
    return [word for word in words if abs(vector(word)[0] * dy - vector(word)[1] * dx) == 1]


def chart(executable, pair, words, depth, limit):
    assert words
    return json.loads(subprocess.check_output([str(executable), *pair, str(depth), str(limit)],
                                             input="\n".join(words), text=True))


def chart_summary(receipts):
    return {"charts": len(receipts),
            "word_checks": sum(record["word_checks"] for record in receipts),
            "allocation_stops": sum(record["allocation_stop"] for record in receipts),
            "last_completed_stage_histogram": {
                stage: sum(len(record["graph_sizes"]) == stage + 1 for record in receipts)
                for stage in sorted({len(record["graph_sizes"]) - 1 for record in receipts})},
            "largest_graph": max((max(record["graph_sizes"]) for record in receipts), default=0),
            "word_hits": sum(len(record["hits"]) for record in receipts)}


def reciprocal(executable, forwards, reverse, depth, limit, workers):
    """Reverse maps each retained donor to its verified changing rows."""
    forward_queries = {}
    pending = defaultdict(lambda: defaultdict(list))
    forward_receipts = []
    for r, d in sorted({pair for a, b in forwards for pair in ((a, b), (b, a))}):
        words = candidate_donors(d, sorted(reverse))
        if words:
            forward_queries[r, d] = words

    def task(item):
        pair, words = item
        return {"pair": pair, "word_checks": len(words), **chart(executable, pair, words, depth, limit)}

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for scan in pool.map(task, forward_queries.items()):
            r, d = scan["pair"]
            forward_receipts.append(scan)
            for e, stage in scan["hits"]:
                for s in sorted(reverse[e]):
                    pending[s, e][d].append((r, stage))

        reverse_receipts = []
        joins = []
        for scan in pool.map(task, [(pair, sorted(words)) for pair, words in sorted(pending.items())]):
            s, e = scan["pair"]
            reverse_receipts.append(scan)
            for d, backwards_stage in scan["hits"]:
                for r, forwards_stage in pending[s, e][d]:
                    joins.append({"forward_pair": (r, d), "reverse_pair": (s, e),
                                  "intermediate": (e, d), "forward_stage": forwards_stage,
                                  "reverse_stage": backwards_stage})
    return {"forward": chart_summary(forward_receipts), "reverse": chart_summary(reverse_receipts),
            "forward_receipts": forward_receipts, "reverse_receipts": reverse_receipts, "joins": joins}


def ledger_for_join(join, suffix, endpoint, prefix=None):
    forward, reverse = tuple(join["forward_pair"]), tuple(join["reverse_pair"])
    e, d = join["intermediate"]
    left, _ = compile_move(forward, 0, e, join["forward_stage"])
    right, _ = compile_move(reverse, 0, d, join["reverse_stage"])
    moves = left["moves"] + normalize_pair((e, d), (d, e)) + list(reverse_moves(right["moves"]))
    moves += normalize_pair(reverse, endpoint) + suffix
    start = list(forward)
    if prefix is not None:
        moves = prefix["moves"] + normalize_pair(tuple(prefix["target"]), forward) + moves
        start = prefix["start"]
    ledger = {"format": "ordinary-ac-elementary-v1", "start": start, "target": list(BASIS), "moves": moves}
    replay(ledger)
    return ledger


def control(executable, reference):
    suffix = load("correct")
    c, a = map(canonical, suffix["start"])
    f = (canonical(reduce(c + "x" + a + "X")), a)
    r = (canonical(reduce(a + "x" + c + "X")), c)
    assert len(set(f + r)) == 4
    outcome = reciprocal(executable, [f], {r[1]: {r[0]}}, 2, 20000, 1)
    assert outcome == reciprocal(reference, [f], {r[1]: {r[0]}}, 2, 20000, 1)
    assert {tuple(join["intermediate"]) for join in outcome["joins"]} == {(c, a), (c, f[0])}
    tail, _ = compile_move(r, 0, a, 1)
    suffix_moves = tail["moves"] + normalize_pair(tuple(tail["target"]), tuple(suffix["start"])) + suffix["moves"]
    for join in outcome["joins"]:
        ledger = ledger_for_join(join, suffix_moves, r)
        join.update(strict_replay=replay(ledger), cyclic_peak=cyclic_peak(ledger))
    return {"reference_checks": 3, "joins": outcome["joins"]}


def forward_pairs(path, energy):
    with path.open() as source:
        for row in source:
            pair = tuple(row.split())
            assert len(pair) == 2
            if sum(map(len, pair)) > energy:
                break
            yield tuple(map(canonical, pair))


def reverse_index(archive, energy):
    index = defaultdict(dict)
    locations = json.loads(archive.with_suffix(".sources.json").read_text())
    rows = archive.read_text().splitlines()
    assert len(rows) == len(locations)
    count = 0
    for row, location in zip(rows, locations):
        if len(row) - 1 > energy:
            continue
        count += 1
        for marking, table in enumerate(MAPS):
            a, b = (canonical(word.translate(table)) for word in row.split())
            source = ("archive", tuple(location), marking)
            index[a].setdefault(b, source)
            index[b].setdefault(a, source)
    return index, count


def run(args):
    reverse, rows = reverse_index(args.archive, args.reverse_energy)
    forward = list(forward_pairs(args.forward, args.forward_energy))
    assert forward and reverse
    positive = control(args.executable, args.reference)
    outcome = reciprocal(args.executable, forward, reverse, args.depth, args.allocation, args.workers)
    if outcome["joins"] and args.archives is not None:
        prefix = json.loads(args.prefix.read_text()) if args.prefix else None
        for join in outcome["joins"]:
            s, e = join["reverse_pair"]
            endpoint, suffix = reverse_suffix(reverse[e][s], args.archives)
            matching = prefix if prefix and sorted(map(canonical, prefix["target"])) == sorted(join["forward_pair"]) else None
            ledger = ledger_for_join(join, suffix, endpoint, matching)
            join["strict_replay"] = replay(ledger)
            join["strict_start"] = ledger["start"]
            join["cyclic_peak"] = cyclic_peak(ledger)
            if matching is not None and args.output is not None:
                args.output.write_text(json.dumps(ledger, separators=(",", ":")) + "\n")
                break
    return {"forward_energy": args.forward_energy, "reverse_energy": args.reverse_energy,
            "requested_stages": args.depth, "allocation_cap": args.allocation,
            "forward_pairs": len(forward), "reverse_pairs": rows, "reverse_donors": len(reverse),
            "canonical_forward_prefix_sha256": sha256("".join("\t".join(p) + "\n" for p in forward).encode()).hexdigest(),
            "reverse_tsv_sha256": sha256(args.archive.read_bytes()).hexdigest(),
            "positive_control": positive, **outcome}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("executable", "reference", "forward", "archive"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--forward-energy", type=int, default=22)
    parser.add_argument("--reverse-energy", type=int, default=56)
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--allocation", type=int, default=350000)
    parser.add_argument("--workers", type=int, default=4)
    for name in ("archives", "prefix", "output"):
        parser.add_argument("--" + name, type=Path)
    print(json.dumps(run(parser.parse_args()), indent=2))
