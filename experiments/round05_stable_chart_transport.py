"""Verify the defining exchanges behind the intrinsic rank-two projection."""

import json
from pathlib import Path
import sys

from round03_stable_proof_pivot import canonical
from round04_chart_screen import chart_projections
from round04_stable_proof_paths import replay
from round05_stable_proof_chartless import minima, whitehead_image
from round05_stable_proof_projections import rank_two_orbit
from stallings_search import inverse, reduce

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates/round05_stable_proof_chart_escape22.json"


def evaluate(word, generator, replacement):
    signed = {generator: replacement, generator.upper(): inverse(replacement)}
    return reduce("".join(signed.get(letter, letter) for letter in word))


def defining_exchange(rows, generator, letter, left):
    # Introduce t = letter^(-1) generator, or t = generator letter^(-1).
    right_hand_side = inverse(letter) + generator if left else generator + inverse(letter)
    definition = "t" + inverse(right_hand_side)
    replacement = letter + "t" if left else "t" + letter
    assert definition.lower().count(generator) == definition.count("t") == 1
    assert evaluate(definition, generator, replacement) == ""
    substituted = [evaluate(row, generator, replacement) for row in rows]
    assert all(generator not in row.lower() for row in substituted)
    return tuple(evaluate(row, "t", generator) for row in substituted), {
        "introduced_relator": definition, "eliminated": generator,
    }


def membership(path, pairs):
    keys = {"\t".join(pair).encode() + b"\n": name
            for name, rows in pairs.items() for pair in rank_two_orbit(rows)}
    with path.open("rb") as stream:
        found = {keys[line] for line in stream if line in keys}
    return {name: name in found for name in pairs}


def main(cap27, cap28):
    checked = replay(json.loads(CERTIFICATE.read_text()))
    original = tuple(map(canonical, checked["target"]))
    pivot_slot = original.index("XZxYxzy")
    rows = original
    _, descent, *_ = minima((rows[pivot_slot],))
    receipts = []
    for move in descent:
        multiplier, cut = move["multiplier"], move["cut"]
        expected = whitehead_image(rows, multiplier, cut)
        exchanges = []
        for generator in "xyz":
            if generator == multiplier.lower():
                continue
            if generator in cut:
                rows, step = defining_exchange(rows, generator, multiplier, left=True)
                exchanges.append(step)
            if generator.upper() in cut:
                rows, step = defining_exchange(rows, generator, inverse(multiplier), left=False)
                exchanges.append(step)
        rows = tuple(map(canonical, rows))
        assert rows == expected
        assert rows[pivot_slot] == move["result"][0]
        receipts.append({"descent": move, "defining_exchanges": exchanges, "rows": rows})

    assert rows[pivot_slot] == "Y"
    rename = str.maketrans("zZ", "yY")
    intrinsic_pair = sorted(canonical(evaluate(w, "y", "").translate(rename))
                            for slot, w in enumerate(rows) if slot != pivot_slot)
    (eliminated, pivot, literal_pair), = chart_projections(original)
    assert eliminated == "x" and pivot == "XYZYzy"
    pairs = {"marked_x": literal_pair, "intrinsic": intrinsic_pair}
    hits27, hits28 = membership(cap27, pairs), membership(cap28, pairs)
    assert hits27 == hits28 == {"marked_x": True, "intrinsic": False}
    print(json.dumps({
        "rank_three_replay": checked,
        "maximum_rank_of_stable_connection": 4,
        "defining_exchange_count": sum(len(stage["defining_exchanges"]) for stage in receipts),
        "whitehead_stages": receipts,
        "rank_two_projections": pairs,
        "in_exact_ordinary_cyclic_components": {"27": hits27, "28": hits28},
    }, indent=2))


if __name__ == "__main__":
    main(*map(Path, sys.argv[1:]))
