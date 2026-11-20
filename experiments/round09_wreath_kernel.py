"""Synchronize the braid relation-module path with an infinite wreath marking."""

import hashlib
import json

from braid_relation_module import IDENTITY as BRAID_ONE, evaluate as braid_value, fox
from elementary_verify import inverse, reduce, replay
from round03_frozen_donors import perm_inv, perm_mul
from round04_chart_lifts import ONE as IDENTITY, X as THREE_CYCLE, Y as FIVE_CYCLE
from round04_finite_corrections import BRAID, SOURCE, commutator

ONE = (0, {})
MARKS = {"x": (1, {}), "y": (0, {0: THREE_CYCLE, 1: FIVE_CYCLE})}


def product(left, right):
    height, lamps = left[0], left[1].copy()
    for offset, value in right[1].items():
        place = height + offset
        merged = perm_mul(lamps.get(place, IDENTITY), value)
        if merged == IDENTITY:
            lamps.pop(place, None)
        else:
            lamps[place] = merged
    return height + right[0], lamps


def invert(element):
    height, lamps = element
    return -height, {place - height: perm_inv(value) for place, value in lamps.items()}


SIGNED = {**MARKS, **{letter.upper(): invert(element) for letter, element in MARKS.items()}}


def evaluate(word):
    result = ONE
    for letter in word:
        result = product(result, SIGNED[letter])
    return result


def replay_lamps(word):
    position, lamps = 0, {}
    for letter in word:
        if letter == "x":
            position += 1
        elif letter == "X":
            position -= 1
        else:
            for site, permutation in ((position, THREE_CYCLE), (position + 1, FIVE_CYCLE)):
                step = permutation if letter == "y" else perm_inv(permutation)
                lamps[site] = perm_mul(lamps.get(site, IDENTITY), step)
    return position, {site: value for site, value in lamps.items() if value != IDENTITY}


def shift(place):
    return "x" * place if place >= 0 else "X" * -place


def conjugate(word, by):
    return reduce(by + word + inverse(by))


def orbit(permutation):
    """Conjugators acting at site zero by all conjugates of a local value."""
    queue = [permutation]
    reached = {permutation: ""}
    for current in queue:
        for word, action in (("y", THREE_CYCLE), ("Xyx", FIVE_CYCLE)):
            following = perm_mul(perm_mul(action, current), perm_inv(action))
            if following not in reached:
                reached[following] = reduce(word + reached[current])
                queue.append(following)
    return reached


def factor_table(permutation):
    actions = orbit(permutation)
    queue = [IDENTITY]
    reached = {IDENTITY: ()}
    for current in queue:
        for action, conjugator in actions.items():
            following = perm_mul(current, action)
            if following not in reached:
                reached[following] = (*reached[current], conjugator)
                queue.append(following)
    assert len(reached) == 60
    return reached


def local_derived_seed():
    local = commutator("y", "xyX")
    assert set(evaluate(local)[1]) == {1}
    two_sites = commutator(BRAID, local)
    assert set(evaluate(two_sites)[1]) == {1, 2}
    translated = conjugate(two_sites, "x")
    assert set(evaluate(translated)[1]) == {2, 3}
    # Both entries of the outer commutator belong to the normal closure of BRAID.
    for word in orbit(evaluate(translated)[1][2]).values():
        twist = conjugate(word, shift(2))
        candidate = commutator(two_sites, conjugate(translated, twist))
        if evaluate(candidate) != ONE:
            assert set(evaluate(candidate)[1]) == {2}
            return conjugate(candidate, shift(-2))
    raise AssertionError("no nontrivial single-site commutator")


def local_lifts(seed):
    height, lamps = evaluate(seed)
    assert height == 0 and set(lamps) == {0}
    table = {}
    for permutation, factors in factor_table(lamps[0]).items():
        lift = reduce("".join(conjugate(seed, by) for by in factors))
        assert evaluate(lift) == (0, {0: permutation} if permutation != IDENTITY else {})
        table[permutation] = lift
    return table


def word_of_factors(donor, factors):
    return reduce("".join(conjugate(donor if sign == 1 else inverse(donor), by) for by, sign in factors))


def local_donor_update(donor, lifts, kind):
    if kind == "shift":
        assert evaluate(donor)[0] == 1
        g, h = lifts[THREE_CYCLE], lifts[FIVE_CYCLE]
        # [h,[g,donor]] isolates the site-zero component of [g,donor].
        factors = ((reduce(h + g), 1), (h, -1), ("", 1), (g, -1))
    else:
        assert evaluate(donor) == MARKS["y"]
        factors = ((lifts[FIVE_CYCLE], 1), ("", -1))
    value = evaluate(word_of_factors(donor, factors))
    assert value[0] == 0 and set(value[1]) == {0}
    return factors, value[1][0]


def timed_product(recipient, conjugator, sign):
    donor = 1 - recipient
    conjugations = [{"op": "conjugate", "i": donor, "g": letter} for letter in reversed(conjugator)]
    restore = [{"op": "conjugate", "i": donor, "g": letter} for letter in reversed(inverse(conjugator))]
    inversion = [{"op": "invert", "i": donor}] if sign == -1 else []
    return conjugations + inversion + [{"op": "multiply", "i": recipient, "j": donor}] + inversion + restore


def correct(rows, moves, recipient, mark, lifts, kind):
    donor = rows[1 - recipient]
    height, difference = product(invert(evaluate(rows[recipient])), MARKS[mark])
    assert height == 0
    base, action = local_donor_update(donor, lifts, kind)
    table = factor_table(action)
    factors = []
    blocks = 0
    for place, permutation in sorted(difference.items()):
        for by in table[permutation]:
            moved = reduce(shift(place) + by)
            factors.extend((reduce(moved + prefix), sign) for prefix, sign in base)
            blocks += 1
    correction = word_of_factors(donor, factors)
    assert evaluate(correction) == (0, difference)
    for by, sign in factors:
        moves.extend(timed_product(recipient, by, sign))
    rows[recipient] = reduce(rows[recipient] + correction)
    assert evaluate(rows[recipient]) == MARKS[mark]
    return {"corrected_row": recipient, "sites": sorted(difference), "local_blocks": blocks,
            "donor_products": len(factors), "through_move": len(moves)}


def main():
    source = json.loads(SOURCE.read_text())
    seed = local_derived_seed()
    lifts = local_lifts(seed)
    rows = list(source["target"])
    initial_images = list(map(evaluate, rows))
    assert [image[0] for image in initial_images] == [1, 0]
    assert initial_images != list(MARKS.values())
    moves = list(source["moves"])
    stages = [correct(rows, moves, 1, "y", lifts, "shift"),
              correct(rows, moves, 0, "x", lifts, "lamps")]
    checked = replay({**source, "moves": moves, "target": rows})
    assert list(map(replay_lamps, checked["endpoint"])) == list(MARKS.values())
    braid_audit = []
    for row, mark in zip(rows, "xy"):
        residual = reduce(inverse(mark) + row)
        assert braid_value(residual) == BRAID_ONE
        derivatives = [len(derivative) for derivative in fox(residual)]
        assert derivatives == [0, 0]
        braid_audit.append({"row": mark, "fox_supports": derivatives})
    print(json.dumps({
        "wreath_group": "restricted wreath product A5 wr Z",
        "local_seed_in_braid_derived": seed,
        "number_of_explicit_single_site_lifts_in_braid_derived": len(lifts),
        "initial_lamp_sites_after_braid_path": [sorted(image[1]) for image in initial_images],
        "stages": stages,
        "strict_free_moves": checked["moves"],
        "raw_peak": checked["peak_total_length"],
        "free_endpoint_lengths": list(map(len, rows)),
        "free_endpoint_sha256": [hashlib.sha256(row.encode()).hexdigest() for row in rows],
        "independent_wreath_lamp_replay_matches_basis": True,
        "independent_braid_fox_audit": braid_audit,
    }, indent=2))


if __name__ == "__main__":
    main()
