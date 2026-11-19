"""Check the original-letter conjugation budget after auxiliary erasure."""

from itertools import product
import json

from primitive_map_pairs import decide, fold, inverse, verify_absence
from round02_ac_disproof_controls import signed_graphs_acyclic
from round05_ac_disproof_third_phase_audit import graph_basis


START = ("xxxYYYY", "xyxYXY")
LETTERS = "xXyY"


def join(words, letter):
    return (*words, *(letter + word + inverse(letter) for word in words))


def envelope(sequence):
    words = START
    core = fold(words)
    for letter in sequence:
        shortened = graph_basis(core)
        assert fold(shortened) == core
        words = join(words, letter)
        core = fold(words)
        assert fold(join(shortened, letter)) == core
    return core


def main():
    exclusions = []
    for conjugations in range(3):
        stages = []
        for sequence in product(LETTERS, repeat=conjugations):
            core = envelope(sequence)
            assert signed_graphs_acyclic(core)
            receipt = decide(core, save_certificate=True)
            assert receipt["status"] == "ABSENT"
            verification = verify_absence(receipt)
            stages.append({
                "sequence": "".join(sequence),
                "vertices": len(core) // 4,
                "closed_map_pair_states": verification["closed_map_pair_states_checked"],
            })
        exclusions.append(stages)
    positive = []
    for sequence in product(LETTERS, repeat=3):
        core = envelope(sequence)
        if not signed_graphs_acyclic(core):
            receipt = decide(core, save_certificate=True)
            assert receipt["status"] == "PRIMITIVE"
            positive.append({
                "sequence": "".join(sequence),
                "vertices": len(core) // 4,
                "witness": receipt["witness"],
            })
    assert len(positive) == 8
    assert len(envelope(("x", "x", "y"))) == 4
    print(json.dumps({
        "excluded_marked_conjugation_sequences": exclusions,
        "first_primitive_admitting_envelope_depth": 3,
        "positive_envelopes_at_depth_three": positive,
    }, indent=2))


if __name__ == "__main__":
    main()
