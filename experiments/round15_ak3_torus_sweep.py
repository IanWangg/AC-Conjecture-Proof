"""Check disjoint torus-atlas boundary shards in parallel."""

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def scan(binary, atlas, shards, work, workers):
    paths = sorted(shards.glob("unique.*.bin"), key=lambda f: int(f.name.split(".")[1]))
    if not paths or not workers:
        raise ValueError("need compact boundary shards and positive workers")
    batches = [paths[i::workers] for i in range(workers) if paths[i::workers]]

    def run(index, paths):
        with (work / f"torus.part{index}.log").open("w") as log:
            data = subprocess.check_output([binary, atlas, *paths], stderr=log)
        out = json.loads(data)
        if out["complete"]:
            assert out["seeds_checked"] == sum(p.stat().st_size for p in paths) // 32
        (work / f"torus.part{index}.json").write_bytes(data)
        return out

    with ThreadPoolExecutor(max_workers=workers) as pool:
        reports = list(pool.map(lambda args: run(*args), enumerate(batches)))
    keys = reports[0]["atlas_marked_keys"]
    assert all(result["atlas_marked_keys"] == keys for result in reports)
    totals = []
    for group in zip(*(result["torus_counts"] for result in reports)):
        p, q = group[0]["p"], group[0]["q"]
        assert all((row["p"], row["q"]) == (p, q) for row in group)
        totals.append(
            {
                "p": p,
                "q": q,
                **{
                    col: sum(r[col] for r in group)
                    for col in (
                        "marked_rows",
                        "receiver_weight_one",
                        "target_length_matches",
                    )
                },
            }
        )
    return {
        "atlas_marked_keys": keys,
        "shards": len(paths),
        "workers": workers,
        "complete": all(x["complete"] for x in reports),
        "seeds_checked": sum(x["seeds_checked"] for x in reports),
        "hits": [x["hit"] for x in reports if x["hit"]],
        "torus_counts": totals,
    }


if __name__ == "__main__":
    binary, atlas, shards, work, workers = sys.argv[1:]
    print(
        json.dumps(
            scan(Path(binary), Path(atlas), Path(shards), Path(work), int(workers)),
            indent=2,
        )
    )
