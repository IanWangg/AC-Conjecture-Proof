"""Recover short exact Magnus paths from native midpoint receipts."""

import argparse
import json
from pathlib import Path

from round01_magnus_distance import evaluate, generator, inverse, multiply
from round01_stable_disproof_search import AK3, MagnusQuotient

LETTERS = "xXyY"


def successors(group, state):
    for i, row in enumerate(state):
        j = 1 - i
        changes = [(group.inverse(row), {"op": "invert", "i": i})]
        for sign in (1, -1):
            donor = state[j] if sign == 1 else group.inverse(state[j])
            changes.append((group.multiply(row, donor), {"op": "multiply", "i": i, "j": j, "sign": sign}))
        for index, letter in enumerate(LETTERS):
            u = group.signed_generators[index // 2][index % 2]
            changed = group.multiply(group.multiply(u, row), group.inverse(u))
            changes.append((changed, {"op": "conjugate", "i": i, "g": letter}))
        for value, move in changes:
            if value != row:
                yield (value, state[1]) if i == 0 else (state[0], value), move
    if state[0] != state[1]:
        yield state[::-1], {"op": "swap"}


def inverse_instruction(step):
    if step["op"] == "conjugate":
        return {**step, "g": step["g"].swapcase()}
    if step["op"] == "multiply":
        return {**step, "sign": -step["sign"]}
    return step


def path(group, start, goals, bound):
    parents = [{start: None}, {goal: None for goal in goals}]
    frontiers = [[start], list(goals)]
    middle = start if start in parents[1] else None
    for _ in range(bound):
        if middle is not None:
            break
        side = min(range(2), key=lambda i: len(frontiers[i]))
        following = []
        for state in frontiers[side]:
            for neighbor, move in successors(group, state):
                if neighbor in parents[side]:
                    continue
                parents[side][neighbor] = state, move
                following.append(neighbor)
                if neighbor in parents[1 - side]:
                    middle = neighbor
                    break
            if middle is not None:
                break
        frontiers[side] = following
    if middle is None:
        raise ValueError(f"No path of at most {bound} instructions")

    left, right = [], []
    at = middle
    while parents[0][at] is not None:
        at, move = parents[0][at]
        left.append(move)
    at = middle
    while parents[1][at] is not None:
        at, move = parents[1][at]
        right.append(inverse_instruction(move))
    return list(reversed(left)) + right, at


def independently_replay(degree, moves):
    rows = [evaluate(word, degree) for word in AK3]
    for step in moves:
        operation = step["op"]
        if operation == "swap":
            rows.reverse()
            continue
        i = step["i"]
        if operation == "invert":
            rows[i] = inverse(rows[i], degree)
        elif operation == "multiply":
            donor = rows[step["j"]]
            rows[i] = multiply(rows[i], donor if step["sign"] == 1 else inverse(donor, degree), degree)
        else:
            index = LETTERS.index(step["g"])
            mark = generator(index // 2)
            if index % 2:
                mark = inverse(mark, degree)
            rows[i] = multiply(multiply(mark, rows[i], degree), inverse(mark, degree), degree)
    marks = (generator(0), generator(1))
    assert set(rows) == set(marks)
    return ["xy"[marks.index(row)] for row in rows]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("native_receipt", type=Path)
    args = parser.parse_args()
    record = json.loads(args.native_receipt.read_text())
    assert record["spare_rows"] == 0
    midpoint = tuple(int(poly, 16) for poly in record["midpoint_hex"])
    degree = record["degree"]
    group = MagnusQuotient(2, degree)
    start = tuple(map(group.evaluate, AK3))
    targets = [group.generators]
    midpoints = [midpoint]
    if not record["ordered"]:
        targets.append(group.generators[::-1])
        midpoints.append(midpoint[::-1])
    left, actual_midpoint = path(group, start, midpoints, record["radii"][0])
    right, endpoint = path(group, actual_midpoint, targets, record["radii"][1])
    moves = left + right
    if record.get("distance") is not None:
        assert len(moves) == record["distance"]
    else:
        assert record["path_within_budget"] and len(moves) <= sum(record["radii"])
    marking = independently_replay(degree, moves)
    assert tuple(group.generators["xy".index(letter)] for letter in marking) == endpoint
    print(json.dumps({
        "degree": degree, "moves": moves, "length": len(moves), "target_order": marking,
        "start_to_midpoint_length": len(left), "independent_monomial_replay": True,
    }, indent=2))


if __name__ == "__main__":
    main()
