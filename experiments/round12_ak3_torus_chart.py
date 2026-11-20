"""Exact arbitrary-length conjugacy in the frozen (2,7) energy-20 chart."""

import argparse
from hashlib import sha256
import json
from pathlib import Path

from elementary_verify import inverse, reduce
from round03_frozen_donors import cycle_type
from round10_ac_proof_blocks import marked_group, vectors
from round12_ak3_reciprocal_charts import reverse_index


DONOR, RECEIVER = "xxxxxyXXy", "xxyxxyyXYXY"
MODULI = (7, 2)
# The two factors are x and z, where z = x^-2 y.
IMAGES = {"x": ((0, 1),), "X": ((0, 6),), "y": ((0, 2), (1, 1)), "Y": ((1, 1), (0, 5))}


def push(syllables, factor, exponent):
    if syllables and syllables[-1][0] == factor:
        exponent += syllables.pop()[1]
    exponent %= MODULI[factor]
    if exponent:
        syllables.append((factor, exponent))


def cyclic_syllables(word):
    syllables = []
    for letter in word:
        for factor, exponent in IMAGES[letter]:
            push(syllables, factor, exponent)
    while len(syllables) > 1 and syllables[0][0] == syllables[-1][0]:
        factor, exponent = syllables.pop(0)
        push(syllables, factor, exponent)
    return tuple(syllables)


def signature(word):
    x, y = vectors(word)
    cyclic = cyclic_syllables(word)
    least = min((cyclic[i:] + cyclic[:i] for i in range(len(cyclic))), default=())
    return 2 * x - 3 * y, least


def primitive_obstruction():
    want = cyclic_syllables(RECEIVER)
    assert len(want) == 10 and any(factor == 0 and power == 6 for factor, power in want)
    period = "xxyxy"
    assert cyclic_syllables(period) == ((0, 4), (1, 1), (0, 3), (1, 1))
    controls = []
    for initial, sign, expected_power in (("xxy", 1, 4), ("xy", -1, 3)):
        assert cyclic_syllables(initial) == ((0, expected_power), (1, 1))
        target = initial + period * 2
        target = target if sign == 1 else inverse(target)
        model = cyclic_syllables(target)
        assert len(model) == len(want)
        assert {power for factor, power in model if factor == 0} <= {3, 4}
        controls.append({"initial": initial, "period": period, "orientation": sign,
                         "only_length_compatible_power": 2, "syllables": model})
    return {"receiver_cyclic_syllables": want, "primitive_tails": controls}


def run(archive, cap):
    assert signature(DONOR) == (0, ()) and signature(RECEIVER)[0] == 1
    # The literal donor is x^7 z^2 in the transformed marking.
    assert reduce("x" * 7 + "XXy" * 2) == DONOR
    witness = reduce("xy" + RECEIVER + inverse("xy") + "Y" + DONOR + "y")
    assert signature(witness) == signature(RECEIVER)
    assert signature("xxy") != signature(RECEIVER)
    index, source_count = reverse_index(archive, cap)
    signature_target = signature(RECEIVER)
    hits = []
    query_count = 0
    for donor, sources in sorted(index.items()):
        x, y = vectors(donor)
        delta = 2 * x - 3 * y
        if abs(delta) != 1:
            continue
        query_count += 1
        oriented = donor if delta == 1 else inverse(donor)
        if signature(oriented) == signature_target:
            hits.append({"donor_cyclic_key": donor, "orientation": delta,
                         "reverse_receivers": sorted(sources)})
    return {"fixed_donor": DONOR, "receiver": RECEIVER, "receiver_signature": signature_target,
            "reverse_energy": cap, "reverse_source_pairs": source_count, "reverse_donors": len(index),
            "weight_one_target_words": query_count, "exact_conjugacy_hits": hits,
            "positive_signature_check": witness, "all_primitive_lengths": primitive_obstruction(),
            "reverse_tsv_sha256": sha256(archive.read_bytes()).hexdigest()}


def check_separators(report, separators):
    expected = {(entry["donor_cyclic_key"], word) for entry in report["exact_conjugacy_hits"]
                for word in entry["reverse_receivers"]}
    checked = set()
    for donor, witnesses, unresolved in separators:
        assert all((donor, word) in expected for word in unresolved)
        for word, witness in witnesses.items():
            assert (donor, word) in expected - checked
            checked.add((donor, word))
            x, y = (tuple(witness["marking"][letter]) for letter in "xy")
            image, identity, _, invert, _ = marked_group("symmetric", len(x), x, y)
            assert image(donor) == identity
            source, target = image(DONOR), image(word)
            assert cycle_type(source) == cycle_type(invert(source)) == tuple(witness["source_shape"])
            assert cycle_type(target) == cycle_type(invert(target)) == tuple(witness["target_shape"])
            assert cycle_type(source) != cycle_type(target)
    return {"separated_contacts": len(checked), "unresolved_contacts": sorted(expected - checked)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--reverse-energy", type=int, default=56)
    parser.add_argument("--separators", type=Path)
    args = parser.parse_args()
    report = run(args.archive, args.reverse_energy)
    if args.separators:
        report["reciprocal_separators"] = check_separators(report, json.loads(args.separators.read_text()))
    print(json.dumps(report, indent=2))
