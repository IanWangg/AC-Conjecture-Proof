"""Compare the E17 chartless exits and independently check the cap-28 graph."""

import argparse
import hashlib
from itertools import product
import json
from pathlib import Path

from round03_stable_proof_pivot import canonical, cyclic, neighbors, rotations, tails
from round06_stable_proof_cap23_charts import compact_row
from round09_stable_proof_lift_excursion import signed_rows
from round12_stable_proof_corridor import native_nodes, native_projections, pivot_count, rank_three_key


def first_entrances(root, cap):
    pivot = next(i for i, row in enumerate(root) if len(row) == 1)
    energy = sum(map(len, root))
    found = set()
    terms = 0
    for donor in (i for i in range(3) if i != pivot):
        bound = max(0, (cap - energy - len(root[donor])) // 2)
        allowance = cap - energy + 1
        for a, b, (g, back) in product(rotations(root[pivot]), rotations(root[donor]), tails(bound)):
            terms += 1
            receiver = cyclic(a + g + b + back)
            if len(receiver) > allowance:
                continue
            target = list(root)
            target[pivot] = canonical(receiver)
            if pivot_count(tuple(target)) == 0:
                found.add(rank_three_key(tuple(target)))
    return found, terms


def independent_28(work):
    nodes = native_nodes(work / "exact28-m1")
    root = nodes[0][2]
    closed_at27, terms27 = first_entrances(root, 27)
    assert not closed_at27
    direct, terms28 = first_entrances(root, 28)
    assert direct == {rows for parent, count, rows in nodes if parent == 0 and count == 0}
    reached = set(direct)
    pending = sorted(direct)
    exits = set()
    terms = 0
    for point in pending:
        destinations, count = neighbors(point, 28)
        terms += count
        for row in destinations:
            orbit = rank_three_key(row)
            if pivot_count(orbit):
                exits.add(orbit)
            elif orbit not in reached:
                reached.add(orbit)
                pending.append(orbit)
    assert reached == {rows for _, count, rows in nodes if count == 0}
    assert {rows for _, _, rows in native_projections(work / "exact28-m1")} <= exits
    return dict(cap27_entrance_candidates=terms27, cap28_entrance_candidates=terms28,
                cap28_entrances=len(direct), cap28_chartless_orbits=len(reached),
                cap28_charted_exits=len(exits), stack_product_candidates=terms)


def sample(work):
    measurements = {}
    short_donor = {triple[0] for triple in signed_rows(("xxyXYY",) * 3)}
    for cap, ordinary_cap in ((28, 17), (29, 17), (30, 19), (31, 19), (32, 21), (33, 21)):
        prefix = work / f"exact{cap}-m1"
        nodes = {rows for _, count, rows in native_nodes(prefix) if count == 0}
        exits = {compact_row(pair) for pair, _, _ in native_projections(prefix)}
        baseline = set((work / f"ordinary{ordinary_cap}.tsv").read_bytes().splitlines(keepends=True))
        assert exits == baseline
        minimum_free_bridge = min(sum(map(len, row)) + min(map(len, row)) + 2 for row in nodes)
        minimum_donor_sum = min(sum(sorted(map(len, row))[:2]) for row in nodes)
        assert minimum_free_bridge > cap and cap - minimum_donor_sum <= 21
        donor_counts = [sum(word in short_donor for word in row) for row in nodes]
        assert max(donor_counts) == 1
        donor_released = donor_counts.count(0)
        assert donor_released == (528 if cap == 33 else 0)
        receipt = json.loads(prefix.with_suffix(".json").read_text())
        assert receipt["closed"] and receipt["chartless_discovered"] == len(nodes)
        measurements[cap] = {
            "chartless_orbits": len(nodes),
            "first_entrance_orbits": receipt["chartless_seeds"],
            "charted_exit_orbits": receipt["exit_orbits"],
            "native_candidates": receipt["candidates"],
            "projection_orbits": len(exits),
            "identical_rank_two_cap": ordinary_cap,
            "projection_sha256": hashlib.sha256(b"".join(sorted(exits))).hexdigest(),
            "minimum_free_bridge_energy_after_entry": minimum_free_bridge,
            "maximum_output_word_width_after_entry": cap - minimum_donor_sum,
            "states_without_length_six_donor": donor_released,
        }
        if cap in (28, 32):
            for i in range(2, 10):
                other = work / f"exact{cap}-m{i}"
                assert nodes == {rows for _, count, rows in native_nodes(other) if count == 0}
                assert exits == {compact_row(pair) for pair, _, _ in native_projections(other)}
    cap27 = [
        json.loads((work / f"exact27-m{i}.json").read_text())
        for i in range(1, 10)
    ]
    assert all(row["chartless_seeds"] == 0 for row in cap27)
    return dict(first_source=measurements, cap27_all_nine_no_entry=True,
                cap28_and_cap32_all_nine_same_native_chartless_sets=True,
                independent_stack_28=independent_28(work))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    print(json.dumps(sample(args.work), indent=2))
