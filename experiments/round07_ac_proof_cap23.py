"""Audit every one-donor splice of the cap-23 ledger and replay its literal chart."""

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from free_waypoint_search import normalize
from round01_geometric_archive import check_whitehead_cuts, minimal_pair
from round02_ac_proof_controls import invert, multiply
from round03_ac_proof_controls import replay_between, substitute
from round03_stable_proof_pivot import canonical, det
from round04_stable_proof_paths import replay as replay_rank_three
from round05_ak3_orbit_audit import compact_membership
from round05_ac_proof_charts import add_conjugate, conjugations, make_chart
from round05_stable_proof_chartless import minima
from round06_ac_proof_excursions import advance
from stallings_search import apply, inverse, reduce


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates/round06_stable_proof_cap23_escape.json"


def whitehead_map(letters, multiplier, side):
    return {
        a: a if a == multiplier.lower() else
        (multiplier if a in side else "") + a + (inverse(multiplier) if a.upper() in side else "")
        for a in letters
    }


def rank_two_automorphisms():
    maps = []
    for m in "xXyY":
        other = "y" if m.lower() == "x" else "x"
        for include_lower, include_upper in product((False, True), repeat=2):
            side = m + (other if include_lower else "") + (other.upper() if include_upper else "")
            maps.append(whitehead_map("xy", m, side))
    for marking in permutations("xy"):
        for signs in product((False, True), repeat=2):
            maps.append({letter: image.upper() if negative else image
                         for letter, image, negative in zip("xy", marking, signs)})
    return maps


RANK_TWO_MAPS = rank_two_automorphisms()


@lru_cache(maxsize=None)
def donor_orbit(word):
    (smallest,) = minimal_pair((word,))
    check_whitehead_cuts((smallest,))
    seen = {smallest}
    frontier = [smallest]
    for current in frontier:
        for marking in RANK_TWO_MAPS:
            image = canonical(substitute(current, marking))
            if len(image) == len(smallest) and image not in seen:
                seen.add(image)
                frontier.append(image)
    return {"length": len(smallest), "key": min(seen), "minimal_classes": len(seen)}


@lru_cache(maxsize=None)
def primitive_chart(word):
    """Return one rank-two quotient marking, or prove that no pivot exists."""
    marking = {a: a for a in "xyz"}
    (minimum,), descent, *_ = minima((word,))
    if len(minimum) != 1:
        return None
    for move in (*descent, None):
        pivot = canonical(substitute(word, marking))
        for axis in "xyz":
            if pivot.lower().count(axis) == 1:
                complement = dict(zip((a for a in "xyz" if a != axis), "xy"))
                projection = make_chart(pivot, axis, complement)
                result = {a: substitute(v, projection) for a, v in marking.items()}
                assert not substitute(word, result)
                return result
        assert move is not None
        change = whitehead_map("xyz", move["multiplier"], move["cut"])
        marking = {a: substitute(w, change) for a, w in marking.items()}
    raise AssertionError("Whitehead descent never exposes the primitive")


def exponent(word):
    return tuple(word.count(a) - word.count(a.upper()) for a in "xyz")


def normal(first, second):
    x, y, z = exponent(first)
    a, b, c = exponent(second)
    vector = (y * c - z * b, z * a - x * c, x * b - y * a)
    return max(vector, tuple(-v for v in vector))


def ledger_states(certificate):
    states = [tuple(certificate["start"])]
    conditional = []
    for step, move in enumerate(certificate["moves"], 1):
        previous = states[-1]
        following = apply(previous, move)
        states.append(following)
        if move["op"] == "multiply":
            conditional.append((step, move["i"], move["j"], previous[move["j"]]))
        else:
            assert tuple(map(canonical, previous)) == tuple(map(canonical, following))
    assert states[-1] == tuple(certificate["target"])
    return states, conditional


def interval_screen(states, products):
    times = [0, *(step for step, *_ in products)]
    cyclic_rows = [tuple(map(canonical, states[t])) for t in times]
    assert all(abs(det(rows)) == 1 for rows in cyclic_rows)
    charts = [{i: chart for i, word in enumerate(rows) if (chart := primitive_chart(word)) is not None}
              for rows in cyclic_rows]
    blocks = tuple(combinations(range(3), 2))
    retains = [
        {(pivot, donor): donor_orbit(canonical(substitute(rows[donor], marking)))
         for pivot, marking in available.items() for donor in range(3) if pivot != donor}
        for rows, available in zip(cyclic_rows, charts)
    ]

    def obstructions(left, right, first, last, block):
        left_normal = normal(*(cyclic_rows[left][i] for i in block))
        right_normal = normal(*(cyclic_rows[right][i] for i in block))
        if left_normal != right_normal:
            return "different_endpoint_block_lattices"
        first_donor, = set(block) - {first}
        last_donor, = set(block) - {last}
        if retains[left][first, first_donor] != retains[right][last, last_donor]:
            return "different_retained_donor_automorphism_orbits"
        return "passes_necessary_tests"

    stats = Counter()
    nonzero_outgoing = 0
    allowed = {}
    for right, after in enumerate(charts):
        for left, before in enumerate(charts[:right + 1]):
            for first, last in product(before, after):
                if left == right and first == last:
                    continue
                for block in blocks:
                    if not {first, last} <= set(block):
                        continue
                    verdict = obstructions(left, right, first, last, block)
                    stats[verdict] += 1
                    if verdict == "passes_necessary_tests":
                        allowed.setdefault((right, last), set()).add((left, first))
                        enclosure = normal(*(cyclic_rows[left][i] for i in block))
                        nonzero_outgoing += any(
                            sum(a * b for a, b in zip(enclosure, exponent(word)))
                            for _, receiver, donor, word in products[left:right]
                            if receiver not in block and donor in block
                        )
        if right:
            for pivot in set(after).intersection(charts[right - 1]) - {products[right - 1][1]}:
                allowed.setdefault((right, pivot), set()).add((right - 1, pivot))

    reachable = {(0, 2)}
    for right, after in enumerate(charts):
        while True:
            more = {(right, pivot) for pivot in after if allowed.get((right, pivot), set()) & reachable}
            if more <= reachable:
                break
            reachable.update(more)
    assert {(i, pivot) for i, pivot in reachable if i == len(charts) - 1} == {(len(charts) - 1, 1)}
    assert all(charts)
    assert times[-1] == 140 and cyclic_rows[-1] == tuple(map(canonical, states[-1]))
    return {
        "stages": [{"strict_step": t, "signed_cyclic_rows": rows, "primitive_slots": list(available),
                    "slots_reachable_in_overapproximation": [pivot for pivot in available if (i, pivot) in reachable]}
                   for i, (t, rows, available) in enumerate(zip(times, cyclic_rows, charts))],
        "interval_tests": dict(sorted(stats.items())),
        "surviving_candidates_with_nonzero_outgoing_homology": nonzero_outgoing,
        "step_140_distinct_donor_orbits_for_selected_slot_0": [retains[-2][0, 1], retains[-1][0, 1]],
        "last_two_stages_same_vertex_tests": [
            {"strict_step": times[t], "pivot_slots": [a, b],
             "retained_donor_orbit_descriptions": [retains[t][a, b], retains[t][b, a]]}
            for t in (len(charts) - 2, len(charts) - 1) for a, b in combinations(charts[t], 2)
        ],
    }


def orient_to(pair, slot, target):
    core = target
    tail = ""
    while len(core) > 1 and core[0] == core[-1].swapcase():
        tail += core[0]
        core = core[1:-1]
    _, moves = normalize(pair, slot, core)
    moves.extend(conjugations(slot, tail))
    assert advance(pair, moves)[slot] == target
    return moves


def projected_move(move, pivot, slots, chart):
    if move["i"] == pivot:
        return []
    recipient = slots.index(move["i"])
    if move["op"] == "invert":
        return [invert(recipient)]
    if move["op"] == "conjugate":
        return conjugations(recipient, substitute(move["g"], chart))
    if move["j"] == pivot:
        return []
    return [multiply(recipient, slots.index(move["j"]))]


def conjugate_factors(factors, word):
    return [(reduce(word + tail), negative) for tail, negative in factors]


def inverse_factors(factors):
    return [(word, not negative) for word, negative in reversed(factors)]


def factor_word(donor, factors):
    return reduce("".join(word + (inverse(donor) if negative else donor) + inverse(word)
                          for word, negative in factors))


def move_to_literal_y_chart(state, projected, left):
    """Switch from slot zero to slot one at the step-134 vertex."""
    native = make_chart(state[1], "y", {"x": "x", "z": "y"})
    lift = ("x", "zyy")
    common_left = tuple(substitute(word, left) for word in lift)
    common_native = tuple(substitute(word, native) for word in lift)
    assert common_left == ("x", "xyXXX") and common_native == ("x", "XXXXy")
    carry = {"x": "x", "y": "xxxxxyXXX"}
    right = {a: substitute(word, carry) for a, word in native.items()}
    assert tuple(substitute(word, right) for word in lift) == common_left

    donor = substitute("XXzYZ", left)
    moves = orient_to(projected, 1, donor)
    z_factors = [("xxxx", True), ("xx", True)]
    y_factors = inverse_factors(z_factors) + conjugate_factors(z_factors, "XX") + [("", False)]
    changes = {"x": [], "y": conjugate_factors(y_factors, inverse(left["z"])), "z": z_factors}
    for letter in "xyz":
        changes[letter.upper()] = conjugate_factors(inverse_factors(changes[letter]), inverse(right[letter]))
    for letter, factors in changes.items():
        assert factor_word(donor, factors) == reduce(substitute(letter, right) + inverse(substitute(letter, left)))

    outsider = state[2]
    for i, letter in enumerate(outsider):
        suffix = substitute(outsider[i:], left)
        for conjugator, negative in conjugate_factors(changes[letter], inverse(suffix)):
            moves.extend(add_conjugate(0, 1, conjugator, negative))
    pair = advance(projected, moves)
    assert pair[0] == substitute(outsider, right) and pair[1] == donor
    moves.extend(orient_to(pair, 1, substitute(state[0], right)))
    return moves, right, {
        "ambient_common_lift": lift,
        "left_basis": common_left,
        "right_native_basis": common_native,
        "transported_right_chart": right,
        "signed_conjugate_counts_for_generator_changes": {a: len(changes[a]) for a in "xyz"},
        "ordinary_moves_in_splice": len(moves),
    }


def literal_y_replay(certificate, states):
    initial = states[0][:2]
    pair = initial
    chart = {"x": "x", "y": "y", "z": ""}
    pivot = 2
    slots = (0, 1)
    strict = []
    splice_record = None

    def emit(moves):
        nonlocal pair
        strict.extend(moves)
        pair = advance(pair, moves)

    def verify_endpoint(padded):
        assert substitute(padded[pivot], chart) == ""
        assert pair == tuple(substitute(padded[i], chart) for i in slots)

    for step, move in enumerate(certificate["moves"], 1):
        emit(projected_move(move, pivot, slots, chart))
        padded = states[step]
        verify_endpoint(padded)
        if step == 102:
            pivot = 0
            slots = (2, 1)
            chart = make_chart(padded[pivot], "z", {"x": "x", "y": "y"})
            emit(orient_to(pair, 0, substitute(padded[2], chart)))
            verify_endpoint(padded)
        elif step == 134:
            moves, chart, splice_record = move_to_literal_y_chart(padded, pair, chart)
            pivot = 1
            slots = (2, 0)
            emit(moves)
            verify_endpoint(padded)
    assert splice_record is not None
    proof = replay_between(list(initial), list(pair), strict)
    report = {"splice_at_step_134": splice_record, "rank_two_replay": proof, "moves": strict}
    current = initial
    peak = sum(map(len, map(canonical, current)))
    for move in strict:
        current = apply(current, move)
        peak = max(peak, sum(map(len, map(canonical, current))))
    report["cyclic_peak"] = peak
    report["literal_native_projection"] = tuple(
        substitute(states[-1][i], make_chart(states[-1][1], "y", {"x": "x", "z": "y"})) for i in slots
    )
    return report


def main(catalogue):
    data = CERTIFICATE.read_bytes()
    certificate = json.loads(data)
    states, products = ledger_states(certificate)
    y_chart = literal_y_replay(certificate, states)
    y_chart["ordinary_cap29_membership"] = members = {
        label: compact_membership(catalogue, *map(canonical, words))
        for label, words in (("native", y_chart["literal_native_projection"]),
                             ("carried", y_chart["rank_two_replay"]["endpoint"]))
    }
    assert all(result["present"] for result in members.values())
    return {
        "rank_three_certificate_sha256": sha256(data).hexdigest(),
        "rank_three_replay": replay_rank_three(certificate),
        "interval_compiler_screen": interval_screen(states, products),
        "ordinary_literal_y_projection": y_chart,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cap29_catalogue", type=Path)
    print(json.dumps(main(parser.parse_args().cap29_catalogue), indent=2))
