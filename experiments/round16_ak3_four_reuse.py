"""Replay fourth-block contacts with the retained Round 15 quotient markings."""

import argparse
import json
from collections import defaultdict
from hashlib import sha256
from pathlib import Path

from round15_ak3_four_audit import audit


def contacts(groups):
    return {(f, s, e) for s, left, right in groups for f in left for e in right if f != e}


def pack(raw, baseline):
    raw_bytes = raw.read_bytes()
    base_bytes = baseline.read_bytes()
    receipt = json.loads(raw_bytes)
    earlier = json.loads(base_bytes)
    by_donor = defaultdict(set)
    for e, s, choices in receipt.pop("fourth_queries"):
        by_donor[s].update((f, e) for f in choices)
    groups = []
    for s, pairs in sorted(by_donor.items()):
        left, right = [sorted({pair[i] for pair in pairs}) for i in (0, 1)]
        assert pairs == {(f, e) for f in left for e in right if f != e}
        groups.append([s, left, right])
    previous = contacts(earlier["last_contacts"])
    current = contacts(groups)
    assert previous <= current
    receipt["raw_search_sha256"] = sha256(raw_bytes).hexdigest()
    receipt["previous_receipt_sha256"] = sha256(base_bytes).hexdigest()
    receipt["previous_contacts"] = len(previous)
    receipt["added_contacts"] = len(current - previous)
    receipt["last_contacts"] = groups
    receipt["permutation_markings"] = earlier["permutation_markings"]
    receipt["fourth_exact_obstructions"] = audit(receipt)
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path)
    parser.add_argument("baseline", type=Path)
    args = parser.parse_args()
    print(json.dumps(pack(args.raw, args.baseline), separators=(",", ":")))
