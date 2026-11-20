"""Exclude the 22 reciprocal archive contacts from the new energy-20 minima."""

import argparse
from collections import defaultdict
from fractions import Fraction
import json
from pathlib import Path
from struct import pack
import subprocess
from tempfile import TemporaryDirectory

from elementary_verify import inverse
from round10_ac_proof_blocks import vectors
from round12_ak3_reciprocal_charts import reverse_index
from round14_ak3_bs_atlas import packed_cyclic
from round14_ak3_sheared_separators import separate
from round15_ak3_four_audit import valuation
from round15_ak3_torus_atlas import apply, key
from round17_ak3_minima_slopes import MINIMA

SCALE = Fraction(3, 2)
DONOR = "XXXyyxxYY"
STANDARD = "xxyyXXYYY"
SWAP = str.maketrans("xXyY", "yYxX")


def multiply(left, right):
    if isinstance(left, int):
        return left + right
    return left[0] + SCALE**left[1] * right[0], left[1] + right[1]


def edge_image(factor):
    if isinstance(factor, int):
        return (Fraction(0), factor // 2) if factor % 2 == 0 else None
    return None if factor[0] else 2 * factor[1]


def normalize(sequence):
    while True:
        for i, factor in enumerate(sequence):
            if factor in (0, (0, 0)):
                sequence.pop(i)
                break
            if i + 1 < len(sequence) and type(factor) is type(sequence[i + 1]):
                sequence[i:i + 2] = [multiply(factor, sequence[i + 1])]
                break
            if len(sequence) > 1 and (edge := edge_image(factor)) is not None:
                if i:
                    sequence[i - 1:i + 1] = [multiply(sequence[i - 1], edge)]
                else:
                    sequence[:2] = [multiply(edge, sequence[1])]
                break
        else:
            return sequence


def affine_datum(word):
    marked = word.translate(SWAP)
    height = vectors(marked)[0]
    assert abs(height) == 1
    if height < 0:
        marked = inverse(marked)
    factors = {"x": 1, "X": -1, "y": (Fraction(1), 0), "Y": (Fraction(-1), 0)}
    blocks = normalize([factors[c] for c in marked])
    while len(blocks) > 1 and type(blocks[0]) is type(blocks[-1]):
        blocks = normalize(blocks[1:] + blocks[:1])
    assert len(blocks) == 2
    if not isinstance(blocks[0], int):
        blocks.reverse()
    translation, stable_height = blocks[1]
    assert translation and blocks[0] + 2 * stable_height == 1
    shift = SCALE**-stable_height * translation
    return {"adjusted_translation": str(shift),
            "valuation_sum": valuation(shift, 2) + valuation(shift, 3)}


def primitive_class(executable, donor, receiver):
    assert key(apply(donor, ("y", "x"))) == key(STANDARD)
    with TemporaryDirectory() as directory:
        work = Path(directory)
        atlas, sample = work / "atlas.tsv", work / "pair.bin"
        atlas.write_text(f"{key(donor)}\t2\t2\ty\tx\n")
        words = sorted(map(packed_cyclic, (donor, receiver)))
        sample.write_bytes(pack("=4Q", *words, *words))
        receipt = json.loads(subprocess.check_output([str(executable), str(atlas), str(sample)]))
    assert receipt["seeds_checked"] == 1 and sum(r[2] for r in receipt["occurrences"]) == 1
    if receipt["hit"] is None:
        return None
    return receipt["hit"]["target_y_exponent"]


def run(reciprocal, archive, permutations, root_bs):
    atlas, rows = reverse_index(archive, 56)
    initial = json.loads(reciprocal.read_bytes())
    queries = defaultdict(set)
    assert len(initial["forward_receipts"]) == 10
    for scan in initial["forward_receipts"]:
        _, fixed = scan["pair"]
        for new_donor, _ in scan["hits"]:
            for partner in atlas[new_donor]:
                queries[partner, new_donor].add(fixed)
    tests = separate(permutations, [(s, e, w) for (s, e), w in sorted(queries.items())], 9, 4)
    affine, hnn = [], []
    for test in tests:
        archived, donor = test["source_row"], test["frozen_donor"]
        for reached in test["unresolved"]:
            assert donor == DONOR
            first, second = affine_datum(archived), affine_datum(reached)
            evidence = {"archived": archived, "reached": reached, "donor": donor,
                        "archived_affine": first, "reached_affine": second}
            if first["valuation_sum"] != second["valuation_sum"]:
                affine.append(evidence)
            else:
                expected = primitive_class(root_bs, donor, archived)
                assert expected is not None
                assert primitive_class(root_bs, donor, reached) is None
                hnn.append({**evidence, "archived_primitive_exponent": expected})
    initial["exact_last_block"] = {
        "archive_rows": rows, "permutation_charts": tests,
        "permutation_contacts": sum(len(t["witnesses"]) for t in tests),
        "affine_contacts": affine, "hnn_contacts": hnn,
        "total": sum(map(len, queries.values())),
    }
    initial["additional_frozen_exclusions"] = [
        {"donor": a, "receiver": b, "primitive_class": primitive_class(root_bs, a, b)}
        for a, b in MINIMA if key(a) == key(DONOR)
    ]
    assert len(initial["additional_frozen_exclusions"]) == 2
    assert all(r["primitive_class"] is None for r in initial["additional_frozen_exclusions"])
    return initial


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("reciprocal", "archive", "permutations", "root_bs"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.reciprocal, args.archive, args.permutations, args.root_bs), indent=2))
