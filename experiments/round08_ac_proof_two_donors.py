"""Replay rank-three ordinary splices whose two retained donors change."""

import json
from pathlib import Path

from elementary_verify import replay as replay_rank_two
from round01_geometric_archive import check_whitehead_cuts, minimal_pair
from round02_ac_proof_controls import conjugate, invert, multiply
from round03_ac_proof_controls import substitute
from round04_stable_proof_paths import replay as replay_rank_three
from round05_ac_proof_charts import add_conjugate, conjugations
from round05_stable_proof_chartless import minima
from stallings_search import apply, cyclic, inverse, reduce


ROOT = Path(__file__).resolve().parents[1]


def replay(start, moves, alphabet):
    rows = tuple(start)
    assert len(rows) == len(alphabet)
    assert all(reduce(word) == word for word in rows)
    raw = sum(map(len, rows))
    energy = sum(len(cyclic(word)) for word in rows)
    recipients = set()
    for move in moves:
        i = move["i"]
        assert 0 <= i < len(rows)
        if move["op"] == "multiply":
            assert 0 <= move["j"] < len(rows) and i != move["j"]
            assert i == len(rows) - 1 or move["j"] != len(rows) - 1
            recipients.add(i)
        elif move["op"] == "conjugate":
            assert len(move["g"]) == 1 and move["g"].lower() in alphabet
        else:
            assert move["op"] == "invert"
        rows = apply(rows, move)
        assert all(letter.lower() in alphabet for row in rows for letter in row)
        raw = max(raw, sum(map(len, rows)))
        energy = max(energy, sum(len(cyclic(word)) for word in rows))
    return {"start": start, "target": rows, "steps": len(moves), "max_raw": raw,
            "max_cyclic": energy, "product_receivers": sorted(recipients), "moves": moves}


def reverse_moves(moves):
    for move in reversed(moves):
        i = move["i"]
        if move["op"] == "multiply":
            yield from add_conjugate(i, move["j"], "", True)
        elif move["op"] == "conjugate":
            yield conjugate(i, inverse(move["g"]))
        else:
            yield invert(i)


def embed(moves, slots, marking):
    for move in moves:
        i = slots[move["i"]]
        if move["op"] == "multiply":
            yield multiply(i, slots[move["j"]])
        elif move["op"] == "conjugate":
            yield conjugate(i, substitute(move["g"], marking))
        else:
            yield invert(i)


def entangle(tail, first_power, second_power):
    return [*conjugations(1, tail), *[multiply(0, 1)] * first_power,
            *[multiply(1, 0)] * second_power]


def whitehead(word):
    (minimum,), descent, _, degrees, cuts = minima((word,))
    assert cuts == degrees
    return {"word": minimum, "length": len(minimum), "descent": descent,
            "minimum_cuts": cuts, "degrees": degrees}


def rank_two_minimum(word):
    (minimum,) = minimal_pair((word,))
    check_whitehead_cuts((minimum,))
    return len(minimum)


def exponent(word, alphabet):
    return [word.count(a) - word.count(a.upper()) for a in alphabet]


def determinant(first, second):
    a, b = first
    c, d = second
    return a * d - b * c


def chart_rows(rows, slots, marking):
    return tuple(substitute(rows[i], marking) for i in slots)


def control(t, w):
    left = entangle("xz", 1, 2)
    right = entangle("yzz", 2, 3)
    untangle = list(reverse_moves(left))
    *left_donors, _ = replay(("z", t, w), left, "xyz")["target"]
    q = "z" + inverse(t)
    *right_donors, _ = replay((q, t, w), right, "xyz")["target"]
    donor_proofs = [[whitehead(word) for word in donors]
                    for donors in (left_donors, right_donors)]
    sizes = [{proof["length"] for proof in side} for side in donor_proofs]
    assert all(size > 1 for side in sizes for size in side) and not sizes[0] & sizes[1]
    t_proof = whitehead(t)
    assert t_proof["length"] > 1
    assert abs(determinant(exponent(t, "xy"), exponent(w, "xy"))) == 1

    padded_start = ("a", *left_donors, w)
    padded_tail = "azX"
    padded_moves = [
        *embed(untangle, (1, 2), {}),
        *add_conjugate(0, 2, "", True),
        *embed(right, (0, 2), {"z": "a"}),
        *add_conjugate(3, 0, padded_tail, False),
        conjugate(3, "y"),
    ]
    padded = replay(padded_start, padded_moves, "xyza")
    padded_end = padded["target"]
    assert padded_start[0] == "a" and padded_end[1] == "z"
    pi0, pi1 = {"a": ""}, {"z": "", "a": "z"}
    common_lifts = "x", "y", "za"
    for projection in (pi0, pi1):
        assert tuple(substitute(word, projection) for word in common_lifts) == tuple("xyz")
    start = chart_rows(padded_start, (1, 2, 3), pi0)
    end = chart_rows(padded_end, (0, 2, 3), pi1)
    correction = "y" + substitute(padded_tail, pi1)
    ordinary_moves = [
        conjugate(2, "y"),
        *untangle,
        *add_conjugate(0, 1, "", True),
        *right,
        *add_conjugate(2, 0, correction, False),
    ]
    ordinary = replay(start, ordinary_moves, "xyz")
    assert ordinary["target"] == end and end[:2] == tuple(right_donors)
    assert ordinary["product_receivers"] == [0, 1, 2]
    independent = replay_rank_three({"format": "rank-three-ac-elementary-v1",
                                     "start": start, "target": end,
                                     "moves": ordinary_moves,
                                     "maximum_cyclic_length": ordinary["max_cyclic"]})
    assert independent["raw_peak"] == ordinary["max_raw"]
    assert independent["cyclic_peak"] == ordinary["max_cyclic"]
    return {"rank_two_seed": [t, w], "quotient_relator_whitehead": t_proof,
            "common_lifts": common_lifts, "deleted_slots": [0, 1],
            "chart_substitutions": [pi0, pi1], "prepared_donors": [("z", t), (q, t)],
            "donor_whitehead": donor_proofs, "padded": padded, "ordinary": ordinary}


def rank_two_controls():
    controls = []
    for m, d, expected in [(1, 4, True), (2, 2, False)]:
        h = "x" + "y" * m
        q = h * d + "y"
        u, v = exponent(q, "xy")
        assert v == 5 and u in (2, 4)
        assert rank_two_minimum(q) == 1
        compatible = u % v in (1, v - 1)
        quotient_image_of_native_generator = pow(u, -1, v)
        assert compatible == expected
        if compatible:
            assert h == "xy" and abs(determinant([1, 1], [u, v])) == 1
        controls.append({"p": "x", "q": q, "q_free_basis_partner": h,
                         "abelianization": [u, v], "pushout_order": v,
                         "right_native_generator_image_mod_order": quotient_image_of_native_generator,
                         "common_lift_and_complement": h if compatible else None})
    return controls


def main():
    certificates = ROOT / "certificates"
    audit = json.loads((ROOT / "results/round07_stable_proof_ordinary_peaks.json").read_text())
    seeds = [("torus_knot", "xxYYY", "xY", None)]
    paths = [("W23", "round07_ak3_marked_waypoint30.json", None)]
    for i, row in enumerate(audit["independent_audit"][:3]):
        paths.append((f"cap31_{i + 1}", f"round07_stable_proof_entry{i}.json", row["seed"]))
    rank_two = {}
    for name, path, seed in paths:
        certificate = json.loads((certificates / path).read_text())
        receipt = replay_rank_two(certificate)
        assert receipt["endpoint"] == certificate["target"]
        if seed is None:
            seed = receipt["endpoint"]
        assert sorted(seed) == sorted(receipt["endpoint"])
        seeds.append((name, *seed, path))
        initial = [rank_two_minimum(word) for word in certificate["start"]]
        terminal = [rank_two_minimum(word) for word in seed]
        assert not set(initial) & set(terminal)
        rank_two[name] = {"AK3_minima": initial, "waypoint_minima": terminal}
    results = {}
    for name, t, w, path in seeds:
        results[name] = {"seed_certificate": path, **control(t, w)}
    assert reduce(substitute("xxYYY", {"x": "y"})) == "Y"
    print(json.dumps({"rank_two_compatibility": rank_two_controls(),
                      "rank_two_waypoints": rank_two, "splices": results}, indent=2))


if __name__ == "__main__":
    main()
