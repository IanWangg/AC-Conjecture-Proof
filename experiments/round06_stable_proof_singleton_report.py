"""Regenerate every feasible first exit and collect the exact enclosure reports."""

import argparse
from hashlib import sha256
import json
from pathlib import Path

from round03_stable_proof_pivot import first_exits
from round04_stable_proof_seeds import CAP_HASH
from round05_ak3_orbit_audit import seed_images


def digest(path):
    value = sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def pairs(path, cap):
    assert digest(path) == CAP_HASH[cap]
    return {tuple(line.split()) for line in path.open()}


def weighted_boundary(rows, cap):
    return {(u, v) for a, b in rows for u, v in ((a, b), (b, a)) if 2 * len(u) + len(v) + 1 <= cap}


def prepare(cap21, cap22, directory):
    old, enlarged = pairs(cap21, 21), pairs(cap22, 22)
    assert old <= enlarged
    assert seed_images(cap22)["all_seed_images_present"]
    records = []
    for cap in (20, 21, 22):
        boundary = weighted_boundary(enlarged, cap)
        assert boundary == weighted_boundary(old, cap)
        seeds, examined = first_exits(sorted(boundary), cap)
        path = directory / f"seeds{cap}.tsv"
        path.write_text("".join("\t".join(row) + "\n" for row in sorted(seeds)))
        records.append({"cap": cap, "ordered_boundary_pairs": len(boundary), "same_boundary_in_C21": True,
                        "considered_rank_three_source_lifts": examined, "literal_seeds": len(seeds),
                        "seed_sha256": digest(path)})
    return {"rank_two_invariant_sha256": CAP_HASH[22], "signed_rank_two_seed_images_verified": True,
            "seeds": records}


def summarize(directory, cap22, cap):
    generated = json.loads((directory / f"full{cap}.json").read_text())
    audited = json.loads((directory / f"audit{cap}.json").read_text())
    assert all(generated[key] == val for key, val in audited.items())
    returns_path = directory / f"full{cap}.returns.tsv"
    all_returns = {tuple(row.split()) for row in returns_path.open()}
    assert len(all_returns) == generated["reentry_projections"]
    present = pairs(cap22, 22)
    missing = sorted(all_returns - present)
    assert len(missing) == generated["projections_outside_invariant"]
    return {**generated, "independent_closure_and_reentry_audit": True,
            "missing_projections": missing, "return_sha256": digest(returns_path),
            "catalogue_sha256": digest(directory / f"full{cap}.states.tsv")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "summarize"))
    parser.add_argument("cap21", type=Path)
    parser.add_argument("cap22", type=Path)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--controls-only", action="store_true")
    args = parser.parse_args()
    if args.mode == "prepare":
        report = prepare(args.cap21, args.cap22, args.directory)
    else:
        caps = (20, 21) if args.controls_only else (20, 21, 22)
        report = {"seed_preparation": json.loads((args.directory / "seeds.json").read_text()),
                  "enclosures": [summarize(args.directory, args.cap22, cap) for cap in caps]}
        assert all(row["cap"] == cap for row, cap in zip(report["enclosures"], caps))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
