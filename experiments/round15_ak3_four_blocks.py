"""Search four changing receiving blocks against the one-shear archive."""

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from itertools import chain
from pathlib import Path

from elementary_verify import reduce, replay
from free_waypoint_search import canonical
from round04_stable_proof_paths import edge
from round07_automorphism_transport import normalize_pair
from round08_ac_proof_two_donors import reverse_moves
from round08_ak3_acm_replay import compile_move
from round08_ak3_acm_search import cyclic_peak
from round10_ac_proof_blocks import vectors
from round12_ak3_reciprocal_charts import chart, chart_summary
from round13_ak3_exact_center import independent_menu
from round14_ak3_sheared_archive import ROOT, SEEDS, index, transformed_suffix
from round14_ak3_sheared_three import first_intermediates


def compile_blocks(words, stages, suffix, prefix=None):
    r, d, h, f, s, e = words
    assert r != h and d != f and h != s and f != e
    first_stage, third_stage, fourth_stage = stages
    first, _ = compile_move((r, d), 0, h, first_stage)
    middle_cap = len(h) + max(len(d), len(f))
    middle, product_moves = edge((h, d), tuple(sorted((h, f))), middle_cap, "xXyY")
    assert middle == (h, f)
    third, _ = compile_move(middle, 0, s, third_stage)
    fourth, _ = compile_move((s, e), 1, f, fourth_stage)
    assert third["target"] == fourth["target"] == [s, f]
    endpoint, tail = suffix
    segments = [
        first["moves"],
        product_moves,
        third["moves"],
        list(reverse_moves(fourth["moves"])),
    ]
    moves = (
        list(chain.from_iterable(segments)) + normalize_pair((s, e), endpoint) + tail
    )
    start = [r, d]
    if prefix is not None:
        start = prefix["start"]
        moves = (
            prefix["moves"] + normalize_pair(tuple(prefix["target"]), (r, d)) + moves
        )
    ledger = {
        "format": "ordinary-ac-elementary-v1",
        "start": start,
        "target": ["x", "y"],
        "moves": moves,
    }
    return ledger, {
        **replay(ledger),
        "cyclic_peak": cyclic_peak(ledger),
        "receiving_block_instructions": list(map(len, segments)),
    }


def control(targeted, archives):
    origin = (("n2row1_pureAC_moves.txt", 21), 0, 0)
    suffix = transformed_suffix(origin, archives)
    s, e = map(canonical, suffix[0])
    f = canonical(reduce(e + s))
    h = canonical(reduce(s + f))
    d = canonical(reduce(f + h))
    r = canonical(reduce(h + d))
    words = (r, d, h, f, s, e)
    assert len(set(words)) == 6
    tests = (((r, d), h), ((h, f), s), ((e, s), f))
    scans = [chart(targeted, pair, [target], 2, 100000) for pair, target in tests]
    stages = [item["hits"][0][1] for item in scans]
    ledger, checked = compile_blocks(words, stages, suffix)
    return ledger, {
        "words": words,
        "stages": stages,
        "archive_origin": origin,
        **checked,
    }


def middle_inputs(args):
    records = sorted(
        first_intermediates(args.first_receipt, args.exact_receipt).items()
    )
    data = "".join(h + "\t" + d + "\n" for (_, _, d, h), _ in records)
    run = subprocess.run(
        [str(args.exact_center), str(args.middle_energy)],
        input=data,
        text=True,
        check=True,
        capture_output=True,
    )
    outputs = defaultdict(set)
    for row in run.stdout.splitlines():
        index, h, f = row.split()
        index = int(index)
        assert records[index][0][3] == h
        outputs[index].add(canonical(f))
    found, checks = {}, 0
    for number, ((origin, r, d, h), stage) in enumerate(records):
        independently, tested = independent_menu(h, d, args.middle_energy)
        assert independently == outputs[number]
        checks += tested
        for f in sorted(independently):
            found.setdefault((h, f), (origin, r, d, stage))
    return found, {
        "first_choices": len(records),
        "independent_rotation_checks": checks,
        "distinct_marked_outputs": len(found),
        **json.loads(run.stderr),
    }


def run(args):
    positive, positive_receipt = control(args.targeted, args.archives)
    if args.control_ledger is not None:
        args.control_ledger.write_text(
            json.dumps(positive, separators=(",", ":")) + "\n"
        )
    middle, choice_receipt = middle_inputs(args)
    print(
        f"Complete second-product menus give {len(middle)} ordered pairs",
        file=sys.stderr,
        flush=True,
    )
    atlas, admissible = index(args.archive, args.archive_energy)
    by_vector = defaultdict(list)
    for word in sorted(atlas):
        by_vector[vectors(word)].append(word)

    def third(pair):
        h, f = pair
        x, y = vectors(f)
        words = sorted(
            word
            for (a, b), options in by_vector.items()
            if abs(a * y - b * x) == 1
            for word in options
            if word != h
        )
        assert words
        outcome = chart(args.index_executable, pair, words, args.depth, args.allocation)
        return {"pair": pair, "word_checks": len(words), **outcome}

    found_third = []
    queries = defaultdict(lambda: defaultdict(list))
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for result in pool.map(third, sorted(middle)):
            found_third.append(result)
            h, f = result["pair"]
            for s, stage in result["hits"]:
                for e in atlas[s]:
                    if e != f:
                        queries[e, s][f].append((h, stage))
    print(
        f"{len(found_third)} third charts produce {len(queries)} reverse charts",
        file=sys.stderr,
        flush=True,
    )
    determined = [
        (e, s, sorted(options)) for (e, s), options in sorted(queries.items())
    ]
    attempts, joins = [], []
    prefixes = [
        json.loads((ROOT / "certificates" / name).read_bytes()) for name, _, _ in SEEDS
    ]

    def fourth(query):
        e, s, targets = query
        scanner = args.targeted if len(targets) == 1 else args.index_executable
        return {
            "pair": (e, s),
            "word_checks": len(targets),
            **chart(scanner, (e, s), targets, args.depth, args.allocation),
        }

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for result in pool.map(fourth, determined):
            attempts.append(result)
            e, s = result["pair"]
            for f, fourth_stage in result["hits"]:
                h, third_stage = queries[e, s][f][0]
                origin, r, d, first_stage = middle[h, f]
                stages = (first_stage, third_stage, fourth_stage)
                words = (r, d, h, f, s, e)
                suffix = transformed_suffix(atlas[s][e], args.archives)
                certificate, checked = compile_blocks(
                    words, stages, suffix, prefixes[origin]
                )
                joins.append(
                    {"source": origin, "words": words, "stages": stages, **checked}
                )
                if args.certificate is not None:
                    args.certificate.write_text(
                        json.dumps(certificate, separators=(",", ":")) + "\n"
                    )
                break
            if joins:
                break
    return {
        "archive_sha256": sha256(args.archive.read_bytes()).hexdigest(),
        "first_receipt_sha256": sha256(args.first_receipt.read_bytes()).hexdigest(),
        "exact_receipt_sha256": sha256(args.exact_receipt.read_bytes()).hexdigest(),
        "archive_energy": args.archive_energy,
        "middle_energy": args.middle_energy,
        "depth": args.depth,
        "allocation": args.allocation,
        "unmarked_shears_within_energy": admissible,
        "novel_donor_keys": len(atlas),
        "novel_ordered_marked_pairs": sum(map(len, atlas.values())),
        "positive_control": positive_receipt,
        "second_product": choice_receipt,
        "third": chart_summary(found_third),
        "fourth": chart_summary(attempts),
        "third_charts": found_third,
        "planned_reverse_charts": len(queries),
        "fourth_queries": determined,
        "verified_joins": joins,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "targeted",
        "index_executable",
        "exact_center",
        "archive",
        "archives",
        "first_receipt",
        "exact_receipt",
    ):
        parser.add_argument(name, type=Path)
    parser.add_argument("--archive-energy", type=int, default=56)
    parser.add_argument("--middle-energy", type=int, default=34)
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--allocation", type=int, default=450000)
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--control-ledger", type=Path)
    print(json.dumps(run(parser.parse_args()), indent=2))
