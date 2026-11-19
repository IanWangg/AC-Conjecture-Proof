"""Summarize the direct rank-three enumeration and its bounded truncation."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


def check(directory, cap):
    census = json.loads((directory / f"ak3-{cap}-counts.json").read_text())
    assert census["cyclic_cap"] == cap
    digest = hashlib.sha256()
    energies = Counter()
    last = None
    total = 0
    with (directory / f"ak3-{cap}.tsv").open("rb") as source:
        for line in source:
            digest.update(line)
            rows = tuple(line.split())
            assert len(rows) == 3 and b"Z" in rows and tuple(sorted(rows)) == rows
            assert last is None or last < rows
            last = rows
            energy = sum(map(len, rows))
            assert energy <= cap
            energies[energy] += 1
            total += 1
    assert total == census["discovered_vertices"]
    return {
        **census,
        "catalogue_sha256": digest.hexdigest(),
        "rows_with_a_z_singleton": total,
        "energy_counts": dict(sorted(energies.items())),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    print(json.dumps([check(args.directory, cap) for cap in (18, 19)], indent=2))
