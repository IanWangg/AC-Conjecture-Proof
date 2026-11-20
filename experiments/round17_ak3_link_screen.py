"""Screen literal cyclic waypoints using independently verified parity witnesses."""

import argparse
import hashlib
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from planar_link_parity import decide
from verify_link_parity import verify_certificate


def screen_rows(rows):
    counts = Counter()
    exceptions = []
    witness_rows = 0
    for row in rows:
        words = row.split()
        result = decide(words)
        status = result["status"]
        counts[status] += 1
        if status == "PARITY_OBSTRUCTION":
            checked = verify_certificate(result)
            assert checked["status"] == "PASS"
            counts[result["kind"]] += 1
            witness_rows += checked["equations"]
        else:
            exceptions.append(result)
    return counts, exceptions, witness_rows


def screen(input_path, workers):
    raw = input_path.read_bytes()
    rows = raw.decode("ascii").splitlines()
    chunk_size = 2048
    chunks = [rows[i:i + chunk_size] for i in range(0, len(rows), chunk_size)]
    counts = Counter()
    exceptions = []
    witness_rows = 0
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for part_counts, part_exceptions, part_witness_rows in pool.map(screen_rows, chunks):
            counts.update(part_counts)
            exceptions.extend(part_exceptions)
            witness_rows += part_witness_rows
    return {
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "rows": len(rows),
        "counts": dict(sorted(counts.items())),
        "independently_verified_witness_equations": witness_rows,
        "exceptions": exceptions,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    print(json.dumps(screen(args.input, args.workers), indent=2))


if __name__ == "__main__":
    main()
