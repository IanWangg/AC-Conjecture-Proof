"""Compile a short marked-chart route using isolated stable changes only."""

import argparse
from contextlib import nullcontext
import json
from pathlib import Path

from free_waypoint_search import normalize
from round03_stable_proof_pivot import canonical
from round05_stable_chart_transport import evaluate
from round06_stable_proof_strict_escape import StrictPath, exchange, initial_proofs, transport, translation, value
from stallings_search import inverse

ROOT = Path(__file__).resolve().parents[1]
PREFIX = ROOT / "certificates/round06_stable_proof_cap23_escape.json"


def compile_path(prefix, plan, sink):
    path = StrictPath(prefix["start"][:2], sink)
    path.add({"op": "stabilize", "generator": "z"})
    proofs = initial_proofs(path.rows)
    for move in prefix["moves"]:
        path.add(move)
        transport(proofs, move)
    assert tuple(path.rows) == tuple(prefix["target"])
    assert all(value(proof, path.rows) == name for name, proof in proofs.items())
    marks = dict(zip("xyz", "xyz"))
    boundaries = []
    for g, donor, left in plan["marker_changes"]:
        exchange(path, proofs, marks, g, donor, left)
        boundaries.append(path.total)

    mark_string = "".join(marks.values())
    named = tuple(canonical(row.translate(translation(mark_string, "xyz"))) for row in path.rows)
    assert named == tuple(plan["resulting_ambient_rows"])
    pivot_slot = named.index(plan["pivot"])
    g = marks[plan["eliminated"]]
    pivot = plan["pivot"].translate(translation("xyz", mark_string))
    assert pivot.lower().count(g) == 1
    if g.upper() in pivot:
        pivot = inverse(pivot)
    offset = pivot.index(g)
    pivot = pivot[offset:] + pivot[:offset]
    _, moves = normalize(tuple(path.rows), pivot_slot, pivot)
    for move in moves:
        path.add(move)
        transport(proofs, move)

    replacement = inverse(pivot[1:])
    retained_old = path.rows.copy()
    for i in range(len(path.rows)):
        if i != pivot_slot:
            path.change_occurrences(i, g, replacement, pivot_slot)
            assert path.rows[i] == evaluate(retained_old[i], g, replacement)
    correction = [(i, sign, evaluate(conjugator, g, replacement))
                  for i, sign, conjugator in proofs[g] if i != pivot_slot]
    path.append_normal_product(pivot_slot, replacement, correction)
    path.add({"op": "destabilize", "generator": g, "i": pivot_slot})
    remaining = [marks[letter] for letter in "xyz" if letter != plan["eliminated"]]
    found = sorted(canonical(row.translate(translation("".join(remaining), "xy"))) for row in path.rows)
    assert found == plan["pair"]
    path.record((json.dumps({"target": path.rows}, separators=(",", ":")) + "\n").encode("ascii"))
    return dict(moves=path.total, move_counts=dict(path.counts), exchange_boundaries=boundaries,
                rank_peak=path.peak_rank, raw_peak=path.raw_peak, cyclic_peak=path.cyclic_peak,
                final_relabeling=dict(zip(remaining, "xy")), final_words=path.rows, cyclic_pair=found,
                strict_ledger_sha256=path.digest.hexdigest())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scan_result", type=Path)
    parser.add_argument("index", type=int)
    parser.add_argument("--write-ledger", type=Path)
    args = parser.parse_args()
    plan = json.loads(args.scan_result.read_text())["earliest_outside"][args.index]
    with args.write_ledger.open("wb") if args.write_ledger else nullcontext() as sink:
        result = compile_path(json.loads(PREFIX.read_text()), plan, sink)
    print(json.dumps(result, indent=2))
