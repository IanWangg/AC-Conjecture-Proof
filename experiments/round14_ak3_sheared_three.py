"""Try three changing-receiver blocks against the novel sheared archive."""

import argparse
import json
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path

from elementary_verify import reduce
from free_waypoint_search import canonical
from round10_ac_proof_blocks import vectors
from round12_ak3_reciprocal_charts import chart, chart_summary
from round13_ak3_three_blocks import blocks
from round14_ak3_sheared_archive import ROOT, SEEDS, index, transformed_suffix


def control(targeted, archive, archives):
    location = next(
        item
        for item in json.loads(archive.with_suffix(".sources.json").read_text())
        if item == ["n2row1_pureAC_moves.txt", 21]
    )
    source = (tuple(location), 0, 0)
    endpoint, suffix = transformed_suffix(source, archives)
    s, e = map(canonical, endpoint)
    h = canonical(reduce(s + e))
    d = canonical(reduce(e + h))
    r = canonical(reduce(h + d))
    assert len({r, d, h, e, s}) == 5
    scans = [
        chart(targeted, pair, [word], 2, 25000)
        for pair, word in (((r, d), h), ((d, h), e), ((s, e), h))
    ]
    stages = tuple(run["hits"][0][1] for run in scans)
    _, replayed = blocks(r, d, h, e, s, stages, (endpoint, suffix))
    return {
        "source": source,
        "forward": (r, d),
        "reverse": (s, e),
        "common_receiver": h,
        "stages": stages,
        **replayed,
    }


def first_intermediates(first_receipt, exact_receipt):
    result = {}
    for family in json.loads(first_receipt.read_bytes())["first_families"]:
        r, d = family["pair"]
        for h, stage in family["first_intermediates"]:
            result[family["source"], r, d, h] = stage
    for i, trial in enumerate(json.loads(exact_receipt.read_bytes())["trials"]):
        r, d = (
            canonical(trial[key]) for key in ("source_receiver", "source_fixed_donor")
        )
        for h, stage in trial["forward_finite_completion"]["hits"]:
            if h != r:
                key = (i, r, d, h)
                result[key] = min(result.get(key, stage), stage)
    return result


def run(args):
    atlas, admissible = index(args.archive, args.energy)
    before = first_intermediates(args.first_receipt, args.exact_receipt)
    print(
        f"Indexed {len(atlas)} sheared donor keys and {len(before)} first choices",
        file=sys.stderr,
        flush=True,
    )
    by_vector = defaultdict(list)
    for donor in sorted(atlas):
        by_vector[vectors(donor)].append(donor)
    prefixes = [
        json.loads((ROOT / "certificates" / certificate).read_bytes())
        for certificate, _, _ in SEEDS
    ]
    positive = control(args.targeted, args.archive, args.archives)
    contacts = defaultdict(lambda: defaultdict(list))
    centers, terminals, wins = [], [], []

    def center(item):
        (number, r, d, h), first_stage = item
        x, y = vectors(h)
        candidates = sorted(
            word
            for (a, b), words in by_vector.items()
            if abs(a * y - b * x) == 1
            for word in words
            if word != d
        )
        outcome = chart(
            args.index_executable, (d, h), candidates, args.depth, args.allocation
        )
        return (number, r, d, h, first_stage), len(candidates), outcome

    def terminal(item):
        (s, e), candidates = item
        targets = sorted(candidates)
        executable = args.targeted if len(targets) == 1 else args.index_executable
        return (
            s,
            e,
            len(targets),
            chart(executable, (s, e), targets, args.depth, args.allocation),
        )

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for (number, r, d, h, first_stage), checks, outcome in pool.map(
            center, sorted(before.items())
        ):
            centers.append({"pair": (d, h), "word_checks": checks, **outcome})
            for e, center_stage in outcome["hits"]:
                for s in atlas[e]:
                    if s != h:
                        contacts[s, e][h].append(
                            (number, r, d, first_stage, center_stage)
                        )
        print(
            f"Completed {len(centers)} middle charts; {len(contacts)} reverse charts",
            file=sys.stderr,
            flush=True,
        )
        for s, e, checks, outcome in pool.map(terminal, sorted(contacts.items())):
            terminals.append({"pair": (s, e), "word_checks": checks, **outcome})
            for h, third_stage in outcome["hits"]:
                number, r, d, first_stage, center_stage = contacts[s, e][h][0]
                stages = (first_stage, center_stage, third_stage)
                suffix = transformed_suffix(atlas[e][s], args.archives)
                ledger, checked = blocks(
                    r, d, h, e, s, stages, suffix, prefixes[number]
                )
                wins.append(
                    {
                        "source": number,
                        "first": (r, d),
                        "middle": (h, e),
                        "reverse": (s, e),
                        "stages": stages,
                        **checked,
                    }
                )
                if args.certificate:
                    args.certificate.write_text(
                        json.dumps(ledger, separators=(",", ":")) + "\n"
                    )
                break
            if wins:
                break
    pairs_by_frozen = defaultdict(set)
    for (s, e), rows in contacts.items():
        for h in rows:
            pairs_by_frozen[h, e].add(s)
    third_queries = [
        (h, e, sorted(targets)) for (h, e), targets in sorted(pairs_by_frozen.items())
    ]
    return {
        "archive_sha256": sha256(args.archive.read_bytes()).hexdigest(),
        "energy": args.energy,
        "first_receipt_sha256": sha256(args.first_receipt.read_bytes()).hexdigest(),
        "exact_receipt_sha256": sha256(args.exact_receipt.read_bytes()).hexdigest(),
        "unmarked_shears_within_energy": admissible,
        "novel_donor_keys": len(atlas),
        "novel_ordered_marked_pairs": sum(map(len, atlas.values())),
        "depth": args.depth,
        "allocation": args.allocation,
        "first_choices": len(before),
        "positive_control": positive,
        "center": chart_summary(centers),
        "reverse": chart_summary(terminals),
        "planned_reverse_charts": len(contacts),
        "third_queries": third_queries,
        "verified_joins": wins,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "targeted",
        "index-executable",
        "archive",
        "archives",
        "first-receipt",
        "exact-receipt",
    ):
        parser.add_argument(name.replace("-", "_"), type=Path)
    parser.add_argument("--energy", type=int, default=56)
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--allocation", type=int, default=650000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--certificate", type=Path)
    print(json.dumps(run(parser.parse_args()), indent=2))
