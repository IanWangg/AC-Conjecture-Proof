"""Test one actual final conjugated row against the three-conjugation envelopes."""

from collections import deque
from itertools import combinations, product
import json
from pathlib import Path

from primitive_map_pairs import fold, follow, inverse, reduce
from round05_ac_disproof_third_phase_audit import graph_basis
from round06_stable_disproof_conjugations import LETTERS, START, envelope
from v_vertex_identification import fold_identification, spanning

ROSE = fold(("x", "y"))


def completing_conjugate(core, letter, donor_core=None):
    basis = graph_basis(core)
    assert fold(basis) == core
    if donor_core is None:
        donor_core = core
    donor_basis = graph_basis(donor_core)
    assert fold(donor_basis) == donor_core
    conjugate = fold([reduce(letter + word + inverse(letter)) for word in donor_basis])
    paths, *_ = spanning(core)
    switches = [[] for _ in paths]
    for a, b in combinations(range(len(paths)), 2):
        representative = reduce(paths[a] + inverse(paths[b]))
        quotient, _ = fold_identification(core, a, b)
        assert fold((*basis, representative)) == quotient
        if quotient == ROSE:
            switches[a].append(b)
            switches[b].append(a)

    initial = (False, 0, 0, -1)
    parents = {initial: None}
    queue = deque([initial])
    witness = None
    while queue:
        state = queue.popleft()
        suffix, first, second, previous = state
        if suffix and first == second == 0 and witness is None:
            witness = state
        transitions = []
        if not suffix:
            transitions.extend(((True, vertex, second, previous), "") for vertex in switches[first])
        for index, symbol in enumerate(LETTERS):
            if index == (previous ^ 1):
                continue
            first_next = core[4 * first + index]
            second_next = conjugate[4 * second + index]
            if first_next >= 0 and second_next >= 0:
                transitions.append(((suffix, first_next, second_next, index), symbol))
        for target, symbol in transitions:
            if target not in parents:
                parents[target] = (state, symbol)
                queue.append(target)

    word = None
    if witness is not None:
        reversed_letters = []
        target = witness
        while parents[target] is not None:
            target, symbol = parents[target]
            reversed_letters.append(symbol)
        word = "".join(reversed(reversed_letters))
        assert word == reduce(word)
        assert follow(donor_core, 0, reduce(inverse(letter) + word + letter)) == 0
        assert fold((*basis, word)) == ROSE
    return {"core_vertices": len(paths), "vertex_pairs_folding_to_rose": sum(map(len, switches)) // 2,
            "product_automaton_states": len(parents), "completing_word": word}


def main():
    old_path = Path(__file__).resolve().parents[1] / "results/round06_stable_disproof_conjugations.json"
    old = json.loads(old_path.read_text())
    positives = {item["sequence"] for item in old["positive_envelopes_at_depth_three"]}
    cases = []
    for prefix in map("".join, product(LETTERS, repeat=2)):
        core = envelope(prefix)
        for letter in LETTERS:
            if prefix + letter in positives:
                cases.append({"sequence": prefix + letter, **completing_conjugate(core, letter)})
    survivors = [case["sequence"] for case in cases if case["completing_word"] is not None]
    assert survivors == ["xxY"]
    once = envelope("x")
    twice = envelope("xx")
    skipped_middle = fold((*START, *("xx" + word + "XX" for word in START)))
    no_product_cases = {
        "first_gap_same_receiver": completing_conjugate(skipped_middle, "Y"),
        "first_gap_distinct_receivers": completing_conjugate(once, "Y"),
        "last_gap_same_receiver": completing_conjugate(once, "Yx"),
        "last_gap_distinct_receivers": completing_conjugate(twice, "Y", once),
    }
    assert all(case["completing_word"] is None for case in no_product_cases.values())
    print(json.dumps({"start": START, "envelope_excluded": 64 - len(cases),
                      "final_receiver_cases": cases, "three_conjugation_schedules_remaining": survivors,
                      "product_free_intervals": no_product_cases}, indent=2))


if __name__ == "__main__":
    main()
