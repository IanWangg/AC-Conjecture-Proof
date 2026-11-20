"""Independently verify permutation separations in the fourth receiving block."""

import argparse
import json
from collections import defaultdict
from hashlib import sha256
from pathlib import Path

from round14_ak3_sheared_separators import separate


def run(executable, contacts, degree, workers):
    source = contacts.read_bytes()
    receipt = json.loads(source)
    grouped = defaultdict(set)
    for e, s, words in receipt["fourth_queries"]:
        for f in words:
            grouped[f, s].add(e)
    tasks = [(f, s, targets) for (f, s), targets in sorted(grouped.items())]
    records = separate(executable, tasks, degree, workers)
    excluded = sum(len(record["witnesses"]) for record in records)
    total = sum(len(targets) for _, _, targets in tasks)
    return {
        "contacts_sha256": sha256(source).hexdigest(),
        "contacts": total,
        "distinct_frozen_donors": len({s for _, s, _ in tasks}),
        "degree_cap": degree,
        "exactly_excluded": excluded,
        "unresolved": total - excluded,
        "records": records,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("executable", type=Path)
    parser.add_argument("contacts", type=Path)
    parser.add_argument("--degree", type=int, default=9)
    parser.add_argument("--workers", type=int, default=4)
    options = parser.parse_args()
    print(
        json.dumps(
            run(options.executable, options.contacts, options.degree, options.workers),
            indent=2,
        )
    )
