"""Verify finite quotient separations of exact sheared reciprocal contacts."""

import argparse
import json
import subprocess
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path

from round10_ac_proof_blocks import marked_group


def separate(executable, tasks, degree, workers):
    def run(task):
        original, donor, targets = task
        output = subprocess.check_output(
            [str(executable), donor, original, str(degree)],
            input="\n".join(sorted(targets)),
            text=True,
        )
        witnesses = {}
        for line in output.splitlines():
            target, x, y = line.split("\t")
            assert target in targets and target not in witnesses
            x, y = tuple(map(int, x.split(","))), tuple(map(int, y.split(",")))
            assert len(x) == len(y) <= degree
            image, identity, _, invert, classify = marked_group(
                "symmetric", len(x), x, y
            )
            assert image(donor) == identity
            old, new = image(original), image(target)
            old_type, new_type = classify(old), classify(new)
            assert old_type != new_type
            assert (
                classify(invert(old)) == old_type and classify(invert(new)) == new_type
            )
            witnesses[target] = {
                "x": x,
                "y": y,
                "receiver_type": old_type,
                "target_type": new_type,
            }
        return {
            "source_row": original,
            "frozen_donor": donor,
            "tested_receivers": sorted(targets),
            "witnesses": witnesses,
            "unresolved": sorted(targets - witnesses.keys()),
        }

    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(run, tasks))


def report(executable, contacts, maximum, workers):
    source = contacts.read_bytes()
    receipt = json.loads(source)
    if "third_queries" in receipt:
        tasks = [
            (original, donor, set(targets))
            for original, donor, targets in receipt["third_queries"]
        ]
    else:
        grouped = defaultdict(set)
        for trial in receipt["trials"]:
            for entry in trial["contacts"]:
                target, donor = entry["pair"]
                grouped[trial["source_fixed_donor"], donor].add(target)
        tasks = [
            (original, donor, targets)
            for (original, donor), targets in sorted(grouped.items())
        ]
    records = separate(executable, tasks, maximum, workers)
    return {
        "contacts_sha256": sha256(source).hexdigest(),
        "degree_cap": maximum,
        "contacts": sum(len(targets) for _, _, targets in tasks),
        "exactly_excluded": sum(len(entry["witnesses"]) for entry in records),
        "records": records,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("executable", type=Path)
    parser.add_argument("contacts", type=Path)
    parser.add_argument("--degree", type=int, default=9)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    print(
        json.dumps(
            report(args.executable, args.contacts, args.degree, args.workers), indent=2
        )
    )
