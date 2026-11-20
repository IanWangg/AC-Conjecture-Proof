"""Enumerate common outer-block receivers and test the middle block."""

import argparse
from itertools import permutations
import json
from pathlib import Path
import subprocess

from elementary_verify import replay
from round07_automorphism_transport import normalize_pair
from round08_ac_proof_two_donors import reverse_moves
from round08_ak3_acm_replay import compile_move
from round10_stable_proof_wirtinger import cycle_type, permutation_evaluator
from round11_ak3_targeted_acm import BASIS, load


A, B, C = "XXYYxyyyxYY", "XXYxyXyxYY", "XXYYxyXyyxYY"
OUTER = ((1, 24, 25_000_000), (2, 20, 350_000_000), (2, 24, 400_000_000))
OUTER_ALLOCATION = 90_000
INNER_DEPTH = 6
INNER_ALLOCATION = 2_000_000


def middle_separator(word):
    for degree in range(2, 8):
        identity = tuple(range(1, degree + 1))
        group = list(permutations(identity))
        types = set()
        for x in group:
            shape = cycle_type(x)
            if shape in types:
                continue
            types.add(shape)
            for y in group:
                evaluate = permutation_evaluator((x, y, identity))
                if evaluate(word) != identity:
                    continue
                source, target = map(evaluate, (B, C))
                old_type, new_type = map(cycle_type, (source, target))
                if old_type != new_type:
                    return {"degree": degree, "generator_images": {"x": x, "y": y},
                            "source_image": source, "target_image": target,
                            "source_cycle_type": old_type, "target_cycle_type": new_type}
    return None


def direct(executable, receiver, donor, words):
    return json.loads(subprocess.check_output(
        [str(executable), receiver, donor, str(INNER_DEPTH), str(INNER_ALLOCATION)],
        input="\n".join(words), text=True))


def run(product, target, output):
    outer = []
    words = set()
    for depth, length, budget in OUTER:
        chart = json.loads(subprocess.check_output(
            [str(product), A, B, C, str(depth), str(OUTER_ALLOCATION), str(length), str(budget)], text=True))
        outer.append({"requested_stage": depth, "visit_budget": budget, **chart})
        words.update(chart["common_middles"])
    before = dict(direct(target, A, B, sorted(words))["hits"])
    after = dict(direct(target, A, C, sorted(words))["hits"])
    assert words == before.keys() == after.keys()

    original = load("wrong")
    correction = load("correct")
    assert original["target"] == [A, B] and correction["start"] == [C, A]
    candidates = []
    for word in sorted(words, key=lambda row: (len(row), row)):
        first, _ = compile_move((A, B), 0, word, before[word])
        last, _ = compile_move((A, C), 0, word, after[word])
        forward = direct(target, B, word, [C])
        reverse = direct(target, C, word, [B])
        separator = middle_separator(word)
        assert separator is None or not (forward["hits"] or reverse["hits"])
        candidate = {
            "word": word,
            "outer_before_stage": before[word], "outer_after_stage": after[word],
            "outer_before_replay": replay(first), "outer_after_replay": replay(last),
            "middle_forward": forward, "middle_reverse": reverse, "middle_separator": separator,
        }
        candidates.append(candidate)
        if not (forward["hits"] or reverse["hits"]):
            continue
        if forward["hits"]:
            middle, _ = compile_move((word, B), 1, C, forward["hits"][0][1])
            bridge = middle["moves"]
        else:
            middle, _ = compile_move((word, C), 1, B, reverse["hits"][0][1])
            bridge = list(reverse_moves(middle["moves"]))
        ledger = dict(original, target=list(BASIS), moves=(
            original["moves"] + first["moves"] + bridge + list(reverse_moves(last["moves"]))
            + normalize_pair((A, C), (C, A)) + correction["moves"]))
        candidate["joined_replay"] = replay(ledger)
        output.write_text(json.dumps(ledger, separators=(",", ":")) + "\n")
        break
    return {"marked_relators": {"A": A, "B": B, "C": C}, "outer_allocation_cap": OUTER_ALLOCATION,
            "inner_requested_stage": INNER_DEPTH, "inner_allocation_cap": INNER_ALLOCATION,
            "outer": outer, "candidates": candidates}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("product", "target", "output"):
        parser.add_argument(name, type=Path)
    print(json.dumps(run(**vars(parser.parse_args())), indent=2))
