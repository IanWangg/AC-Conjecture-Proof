"""Scan complete bounded product menus and exact terminal quotient criteria."""

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
from struct import pack
import subprocess
from tempfile import TemporaryDirectory

from euclidean_primitive_audit import primitive_cyclic_word
from free_waypoint_search import canonical
from round13_ak3_exact_center import independent_menu
from round14_ak3_bs_atlas import packed_cyclic
from round17_ak3_minima_slopes import MINIMA


def product_menu(binary, pairs, cap):
    payload = "".join(f"{a}\t{b}\n" for a, b in pairs)
    run = subprocess.run([str(binary), str(cap)], input=payload, text=True,
                         check=True, capture_output=True)
    menu = defaultdict(set)
    for row in run.stdout.splitlines():
        number, donor, receiver = row.split()
        number = int(number)
        assert donor == pairs[number][0]
        menu[number].add(canonical(receiver))
    return menu, json.loads(run.stderr)


def check(binary, *args):
    return json.loads(subprocess.check_output([str(binary), *map(str, args)]))


def run(args):
    # Keep the signed native marking while comparing independent cyclic classes.
    seeds = [pair for p in MINIMA for pair in (p, p[::-1])]
    first, first_receipt = product_menu(args.exact_center, seeds, 40)
    checks = 0
    for i, (donor, receiver) in enumerate(seeds):
        expected, work = independent_menu(donor, receiver, 40)
        assert expected == first[i]
        checks += work
    one = {(canonical(seeds[i][0]), output) for i, words in first.items() for output in words}
    alternate = sorted((changed, fixed) for fixed, changed in one)
    second, second_receipt = product_menu(args.exact_center, alternate, 40)
    two = {(canonical(alternate[i][0]), output) for i, words in second.items() for output in words}
    all_pairs = sorted(one | two)
    assert all(not primitive_cyclic_word(w) for w in {w for pair in all_pairs for w in pair})
    with TemporaryDirectory() as directory:
        work = Path(directory)
        tsv, packed = work / "pairs.tsv", work / "pairs.bin"
        data = "".join(f"{a}\t{b}\n" for a, b in all_pairs).encode()
        tsv.write_bytes(data)
        with packed.open("wb") as stream:
            for pair in all_pairs:
                words = sorted(map(packed_cyclic, pair))
                stream.write(pack("=4Q", *words, *words))
        scans = {
            "primitive_product": check(args.primitive_step, tsv, 6),
            "torus": check(args.torus, args.torus_atlas, packed),
            "consecutive_bs": check(args.bs, args.bs_atlas, packed),
            "root_adjoined_bs": check(args.root_bs, args.root_bs_atlas, packed),
        }
    for key, value in scans.items():
        assert value["complete"] and value["hit"] is None, (key, value["hit"])
        assert value.get("rows_checked", value.get("seeds_checked")) == len(all_pairs)
    torus, bs, root = (scans.pop(key) for key in ("torus", "consecutive_bs", "root_adjoined_bs"))
    return {
        "cap": 40,
        "first": first_receipt, "first_independent_rotation_checks": checks,
        "second_alternating": second_receipt, "distinct_first": len(one),
        "distinct_second": len(two), "distinct_union": len(all_pairs),
        "union_sha256": sha256(data).hexdigest(),
        "primitive_product": scans["primitive_product"],
        "quotient_donor_occurrences": {
            "torus": sum(value["marked_rows"] for value in torus["torus_counts"]),
            "consecutive_bs": sum(bs["candidates"].values()),
            "root_adjoined_bs": sum(value[2] for value in root["occurrences"]),
        },
        "root_adjoined_occurrences_by_type": [r for r in root["occurrences"] if r[2]],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("exact_center", "primitive_step", "torus", "torus_atlas",
                 "bs", "bs_atlas", "root_bs", "root_bs_atlas"):
        parser.add_argument(name, type=Path)
    print(json.dumps(run(parser.parse_args()), indent=2))
