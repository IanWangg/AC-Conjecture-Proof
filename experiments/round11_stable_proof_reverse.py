"""Compile the two marked Wirtinger endpoints and verified reverse roots."""

import argparse
import json
from pathlib import Path

from elementary_verify import replay as replay_pair
from free_waypoint_search import normalize
from round03_stable_proof_pivot import canonical, cyclic, neighbors
from round04_stable_proof_paths import edge, replay
from round05_stable_proof_chartless import whitehead_image
from round07_automorphism_transport import normalize_pair
from round08_ac_proof_two_donors import reverse_moves
from round09_stable_proof_lift_excursion import signed_rows
from round10_stable_proof_wirtinger import factor, frozen_repair, literal_clearing
from stallings_search import apply, inverse


ROOT = Path(__file__).resolve().parents[1]
MARKING = str.maketrans("xyzXYZ", "zxyZXY")
START = ("xxxYYYY", "xyxYXY", "z")


def read(name):
    return json.loads((ROOT / "certificates" / name).read_text())


def states(start, moves):
    yield tuple(start)
    for move in moves:
        start = apply(start, move)
        yield tuple(start)


def certificate(start, moves, target):
    path = list(states(start, moves))
    assert path[-1] == tuple(target)
    peak = max(sum(len(cyclic(row)) for row in point) for point in path)
    proof = {"format": "rank-three-ac-elementary-v1", "start": start, "target": target,
             "maximum_cyclic_length": peak, "moves": moves}
    replay(proof)
    return proof


def repair_endpoints():
    proof = frozen_repair()
    endpoints = []
    for row in proof["wrong_and_corrected_row"]:
        defining_tuple = (*proof["fixed_rows"], row)
        for step in proof["fixed_whitehead_descent"]:
            defining_tuple = whitehead_image(defining_tuple, step["multiplier"], step["cut"])
        mark = tuple(word.translate(MARKING) for word in defining_tuple)
        assert mark[0] == "Z"
        endpoints.append((mark[1], mark[2], mark[0]))
    return endpoints


def corrected_suffix(correct):
    pair = read("round10_stable_proof_wirtinger_correct.json")
    assert replay_pair(pair)["endpoint"] == ["x", "y"]
    pivot = {"op": "invert", "i": 2}
    cleared, clear = literal_clearing(apply(correct, pivot), "z", 2)
    marked = tuple(map(canonical, cleared[:2]))
    placement = [marked.index(canonical(word)) for word in pair["start"]]
    align = []
    for slot, word in zip(placement, pair["start"]):
        cleared, steps = normalize(cleared, slot, word)
        align.extend(steps)
    carried = [{key: placement[value] if key in {"i", "j"} else value for key, value in move.items()}
               for move in pair["moves"]]
    final = tuple("xy"[placement.index(slot)] for slot in range(2))
    finish = normalize_pair(final, tuple("xy"))
    return certificate(correct, [pivot, *clear, *align, *carried, *finish], tuple("xyz"))


def source_prefix(wrong):
    pair = read("round10_stable_proof_wirtinger_wrong.json")
    replay_pair(pair)
    pivot = {"op": "invert", "i": 2}
    cleared, clear = literal_clearing(apply(wrong, pivot), "z", 2)
    align = normalize_pair(tuple(pair["target"]), cleared[:2])
    return certificate(START, [*pair["moves"], *align, *reverse_moves(clear), pivot], wrong)


def geometric_suffix():
    pair = read("w_geometric_nonprimitive_full.json")
    checked = replay_pair(pair)
    p, q = pair["start"]
    tail = "xZXYz"
    last = "z" + tail + p + inverse(tail)
    moves = factor(2, 0, -1, tail)
    alignment = normalize_pair(tuple(checked["endpoint"]), tuple("xy"))
    return certificate((p, q, last), [*moves, *pair["moves"], *alignment], tuple("xyz"))


def write_tsv(path, points):
    with path.open("w") as output:
        for point in sorted({tuple(sorted(map(canonical, row))) for row in points}):
            output.write("\t".join(point) + "\n")


def lift_source_route(route, cap):
    wrong, _ = repair_endpoints()
    prefix = source_prefix(wrong)
    current = wrong
    moves = prefix["moves"].copy()
    assert tuple(sorted(map(canonical, current))) in signed_rows(route[0])
    for i in range(3):
        current, steps = normalize(current, i, canonical(current[i]))
        moves.extend(steps)
    for representative in route[1:]:
        targets, _ = neighbors(current, cap)
        endpoint = min(targets & signed_rows(representative))
        current, steps = edge(current, endpoint, cap, "xXyYzZ")
        moves.extend(steps)
    return certificate(START, moves, current)


def prepare(directory):
    directory.mkdir(parents=True, exist_ok=True)
    wrong, correct = repair_endpoints()
    prefix = source_prefix(wrong)
    suffix = corrected_suffix(correct)
    geometric = geometric_suffix()
    ledgers = {"wrong_prefix": prefix, "correct_suffix": suffix, "geometric_suffix": geometric}
    for name, proof in ledgers.items():
        (directory / f"{name}.json").write_text(json.dumps(proof, indent=2) + "\n")
    write_tsv(directory / "wrong.tsv", [wrong])
    write_tsv(directory / "correct.tsv", [correct])
    control = next(row for row in states(correct, suffix["moves"])
                   if sum(len(cyclic(word)) for word in row) == 24)
    write_tsv(directory / "control-target.tsv", [control])
    reverse_points = [row for proof in (suffix, geometric)
                      for row in states(proof["start"], proof["moves"])]
    write_tsv(directory / "reverse-roots.tsv", reverse_points)
    return {name: replay(proof) for name, proof in ledgers.items()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--lift-source-route", type=Path)
    parser.add_argument("--cap", type=int, default=27)
    args = parser.parse_args()
    result = prepare(args.directory)
    if args.lift_source_route:
        route = [tuple(line.split()) for line in args.lift_source_route.read_text().splitlines()]
        proof = lift_source_route(route, args.cap)
        (args.directory / "source_excursion.json").write_text(json.dumps(proof, indent=2) + "\n")
        result["source_excursion"] = replay(proof)
    print(json.dumps(result, indent=2))
