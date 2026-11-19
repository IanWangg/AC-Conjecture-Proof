"""Compile and verify the cap-23 intrinsic escape to a new rank-two pair."""

import argparse
import json
from pathlib import Path

from free_waypoint_search import conj_ops
from round03_stable_proof_pivot import canonical
from round04_stable_proof_paths import compile_rank_three, edge, replay
from round05_ak3_orbit_audit import compact_membership
from round05_stable_chart_transport import defining_exchange, evaluate
from round05_stable_proof_chartless import minima, whitehead_image
from stallings_search import apply, inverse

TARGET = ("XXzYZ", "XYXzYZxyy", "XzyZYYZxy")
PROJECTION = ("XXXYxyxyXYY", "XYXYYXyXYYXy")


def compile_path(pair_route, excursion):
    certificate = compile_rank_three(pair_route, [])
    state = tuple(certificate["target"])
    assert set(state) == {"XXXYYxy", "XXyxYY", "Z"}
    singleton = state.index("Z")
    recipient = state.index("XXXYYxy")
    suffix = "xy"
    insertion = conj_ops(singleton, inverse(suffix))
    insertion += [{"op": "multiply", "i": recipient, "j": singleton}]
    insertion += conj_ops(singleton, suffix)
    for move in insertion:
        state = apply(state, move)
    assert sorted(state) == sorted(("XXXYYZxy", "XXyxYY", "Z"))
    certificate["moves"].extend(insertion)
    certificate["macro_boundaries"].append(len(certificate["moves"]))
    for goal in excursion:
        state, moves = edge(state, goal, 23, "xXyYzZ")
        certificate["moves"].extend(moves)
        certificate["macro_boundaries"].append(len(certificate["moves"]))
    assert tuple(sorted(state)) == TARGET
    certificate["target"] = state
    return certificate


def verify_projection(certificate, cap29):
    checked = replay(certificate)
    rows = tuple(map(canonical, checked["target"]))
    slot = rows.index("XzyZYYZxy")
    _, descent, *_ = minima((rows[slot],))
    records = []
    for move in descent:
        multiplier, cut = move["multiplier"], move["cut"]
        expected = whitehead_image(rows, multiplier, cut)
        exchanges = []
        for letter in "xyz":
            if letter == multiplier.lower():
                continue
            if letter in cut:
                rows, step = defining_exchange(rows, letter, multiplier, left=True)
                exchanges.append(step)
            if letter.upper() in cut:
                rows, step = defining_exchange(rows, letter, inverse(multiplier), left=False)
                exchanges.append(step)
        rows = tuple(map(canonical, rows))
        assert rows == expected and rows[slot] == move["result"][0]
        records.append({"descent": move, "defining_exchanges": exchanges, "rows": rows})
    assert rows[slot] == "Z"
    final = tuple(sorted(canonical(evaluate(row, "z", "")) for i, row in enumerate(rows) if i != slot))
    assert final == PROJECTION
    member = compact_membership(cap29, *final)
    assert not member["present"]
    return {"rank_three_replay": checked, "whitehead_stages": records,
            "defining_exchanges": sum(len(stage["defining_exchanges"]) for stage in records),
            "maximum_rank_of_stable_connection": 4, "rank_two_projection": final,
            "cap29_membership": member}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("pair_route", "excursion", "cap29", "certificate"):
        parser.add_argument(arg, type=Path)
    args = parser.parse_args()
    excursion = [tuple(line.split()) for line in args.excursion.open()]
    certificate = compile_path(json.loads(args.pair_route.read_text()), excursion)
    args.certificate.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps(verify_projection(certificate, args.cap29), indent=2))
