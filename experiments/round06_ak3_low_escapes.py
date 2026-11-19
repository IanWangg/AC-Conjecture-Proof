"""Extract the complete low-energy difference between compact cap catalogues."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


def collect(previous, current, output, energy):
    length_bound = energy + 2  # tab plus newline
    with previous.open("rb") as source:
        old_short = {line for line in source if len(line) <= length_bound}
    digest = sha256()
    counts = Counter()
    with current.open("rb") as source, output.open("wb") as target:
        for line in source:
            if len(line) <= length_bound and line not in old_short:
                target.write(line)
                digest.update(line)
                counts[len(line) - 2] += 1
    return {"maximum_energy": energy, "new_orbits_by_energy": dict(sorted(counts.items())),
            "output_sha256": digest.hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("previous", "current", "output"):
        parser.add_argument(name, type=Path)
    parser.add_argument("energy", type=int)
    args = parser.parse_args()
    print(json.dumps(collect(args.previous, args.current, args.output, args.energy), indent=2))


if __name__ == "__main__":
    main()
