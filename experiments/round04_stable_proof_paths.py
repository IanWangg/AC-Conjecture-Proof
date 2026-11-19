"""Compile and independently replay a cyclic path through rank-three excursions."""

import argparse
import json
from itertools import product
from pathlib import Path

from free_waypoint_search import normalize, conj_ops
from round03_stable_proof_pivot import canonical, cyclic, rotations, tails
from stallings_search import inverse, reduce, apply

START = ("xxxYYYY", "xyxYXY", "z")


def edge(state, goal, cap, alphabet):
    energy = sum(map(len, state))
    choices = []
    for i, j in product(range(len(state)), repeat=2):
        if i == j:
            continue
        fixed = [w for k, w in enumerate(state) if k != i]
        missing = list(goal)
        for w in fixed:
            if w not in missing:
                break
            missing.remove(w)
        else:
            expected, = missing
            bound = max(0, (cap - energy - len(state[j])) // 2)
            for a, b, (q, q_inv) in product(rotations(state[i]), rotations(state[j]), tails(bound)):
                if not set(q) <= set(alphabet):
                    continue
                if canonical(a + q + b + q_inv) != expected:
                    continue
                new, prefix = normalize(state, i, a)
                new, steps = normalize(new, j, b)
                ops = prefix + steps + conj_ops(j, q)
                for op in conj_ops(j, q):
                    new = apply(new, op)
                step = dict(op="multiply", i=i, j=j)
                new = apply(new, step)
                ops.append(step)
                for k in (i, j):
                    new, steps = normalize(new, k, canonical(new[k]))
                    ops.extend(steps)
                assert tuple(sorted(new)) == goal
                choices.append((len(ops), i, j, a, b, q, new, ops))
    if not choices:
        raise ValueError(f"No bounded cyclic edge from {state} to {goal}")
    *_, new, ops = min(choices, key=lambda row: row[:6])
    return new, ops


def compile_rank_three(rank_two_route, excursion):
    cap = rank_two_route["cyclic_cap"] + 1
    ordinary = [tuple(sorted([*row, "Z"])) for row in rank_two_route["route"]]
    assert tuple(sorted(map(canonical, START))) == ordinary[0]
    current = START
    moves = []
    for i in range(3):
        current, steps = normalize(current, i, canonical(current[i]))
        moves.extend(steps)
    boundaries = [len(moves)]
    for expected in ordinary[1:] + excursion:
        current, steps = edge(current, expected, cap, "xXyYzZ")
        moves.extend(steps)
        boundaries.append(len(moves))
    return {"format": "rank-three-ac-elementary-v1", "start": START, "target": current,
            "maximum_cyclic_length": cap, "moves": moves, "macro_boundaries": boundaries}


def replay(certificate):
    if certificate["format"] != "rank-three-ac-elementary-v1":
        raise ValueError("Wrong certificate format")
    state = list(certificate["start"])
    assert len(state) == len(certificate["target"]) == 3
    assert all(w and set(w) <= set("xXyYzZ") and reduce(w) == w for w in state)
    lengths = [sum(map(len, state))]
    energies = [sum(len(cyclic(w)) for w in state)]
    one_occurrence = []
    for step, move in enumerate(certificate["moves"], 1):
        i = move["i"]
        assert type(i) is int and i in range(3)
        if move["op"] == "invert" and set(move) == {"op", "i"}:
            state[i] = inverse(state[i])
        elif move["op"] == "multiply" and set(move) == {"op", "i", "j"}:
            j = move["j"]
            assert type(j) is int and j in range(3) and i != j
            state[i] = reduce(state[i] + state[j])
        elif move["op"] == "conjugate" and set(move) == {"op", "i", "g"}:
            g = move["g"]
            assert type(g) is str and len(g) == 1 and g in "xXyYzZ"
            state[i] = reduce(g + state[i] + inverse(g))
        else:
            raise ValueError(f"Invalid move {step}")
        lengths.append(sum(map(len, state)))
        energies.append(sum(len(cyclic(w)) for w in state))
        one_occurrence.append(any(cyclic(w).count("z") + cyclic(w).count("Z") == 1 for w in state))
    assert state == list(certificate["target"])
    assert max(energies) <= certificate["maximum_cyclic_length"]
    return dict(moves=len(lengths) - 1, raw_peak=max(lengths), cyclic_peak=max(energies),
                target=state, first_pivotless_step=next((i for i, has in enumerate(one_occurrence, 1)
                                                       if not has), None))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    build = sub.add_parser("compile")
    build.add_argument("rank_two_route", type=Path)
    build.add_argument("excursion", type=Path)
    build.add_argument("certificate", type=Path)
    check = sub.add_parser("verify")
    check.add_argument("certificate", type=Path)
    args = parser.parse_args()
    if args.mode == "compile":
        rank_two = json.loads(args.rank_two_route.read_text())
        excursion = [tuple(line.split()) for line in args.excursion.read_text().splitlines()]
        certificate = compile_rank_three(rank_two, excursion)
        args.certificate.write_text(json.dumps(certificate, indent=2) + "\n")
    else:
        certificate = json.loads(args.certificate.read_text())
    print(json.dumps(replay(certificate), indent=2))
