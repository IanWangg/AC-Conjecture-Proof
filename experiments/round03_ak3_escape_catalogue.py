"""Extract exactly the low-energy cap-25 escape tuples and a stratified sample."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import random


def difference(smaller, larger):
    with smaller.open("rb") as old, larger.open("rb") as new:
        previous_old = previous_new = b""
        lower = old.readline()
        for upper in new:
            assert upper > previous_new, "larger catalogue must be sorted and duplicate-free"
            previous_new = upper
            if upper < lower or not lower:
                yield upper
            elif upper == lower:
                assert lower > previous_old, "smaller catalogue must be sorted and duplicate-free"
                previous_old = lower
                lower = old.readline()
            else:
                raise ValueError("smaller catalogue is not contained in the larger catalogue")
        assert not lower, "unmatched rows remain in the smaller catalogue"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cap24", type=Path)
    parser.add_argument("cap25", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    counts = Counter()
    samples = {}
    rng = random.Random(20261119)
    for row in difference(args.cap24, args.cap25):
        energy = len(row) - 2  # One tab and one newline.
        counts[energy] += 1
        bucket = samples.setdefault(energy, [])
        if len(bucket) < 128:
            bucket.append(row)
        else:
            index = rng.randrange(counts[energy])
            if index < len(bucket):
                bucket[index] = row
    minimum = min(counts)
    lowest = b"".join(sorted(samples[minimum]))
    assert len(samples[minimum]) == counts[minimum]
    sample = b"".join(row for energy in sorted(samples) for row in sorted(samples[energy]))
    (args.output / "lowest.tsv").write_bytes(lowest)
    (args.output / "sample.tsv").write_bytes(sample)
    result = {"minimum_escape_energy": minimum, "all_escapes": dict(sorted(counts.items())),
              "sample_rows": sum(map(len, samples.values())),
              "lowest_sha256": sha256(lowest).hexdigest(), "sample_sha256": sha256(sample).hexdigest()}
    (args.output / "catalogue.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
