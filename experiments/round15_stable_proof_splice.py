"""Replay a lower-energy replacement for each over-cap excursion."""

import argparse
import json
from hashlib import sha256
from io import BytesIO
from pathlib import Path

from free_waypoint_search import conj_ops, normalize
from round03_stable_proof_pivot import canonical, cyclic
from round04_stable_proof_paths import edge, replay
from round06_stable_proof_strict_escape import StrictPath
from round11_stable_proof_reverse import certificate
from stallings_search import apply


def energy(rows):
    return sum(len(cyclic(word)) for word in rows)


def marked(rows):
    return tuple(sorted(map(canonical, rows)))


def align(path, slot, target):
    if path.rows[slot] == target:
        return
    core = cyclic(target)
    stem = target[:(len(target) - len(core)) // 2]
    _, steps = normalize(tuple(path.rows), slot, core)
    path.extend(steps)
    path.extend(conj_ops(slot, stem))
    assert path.rows[slot] == target


def replace(path, rank_three, route):
    cap = route["cyclic_cap"]
    old = [tuple(path.rows)]
    for step in rank_three:
        old.append(apply(old[-1], step))
    cursor = 0
    changes = []
    for replacement in route["detours"]:
        left, right = replacement["original_steps"]
        assert cursor <= left < right < len(old)
        assert energy(old[left]) <= cap and energy(old[right]) <= cap
        over_cap = [index for index in range(left + 1, right) if energy(old[index]) > cap]
        assert over_cap
        path.extend(rank_three[cursor:left])
        assert tuple(path.rows) == old[left]
        before = path.total
        for slot, word in enumerate(path.rows):
            align(path, slot, canonical(word))
        for point in (*replacement["interior"], marked(old[right])):
            point = tuple(point)
            assert tuple(sorted(map(canonical, point))) == point
            if marked(path.rows) != point:
                local_cap = max(energy(path.rows), energy(point))
                assert local_cap <= cap
                _, steps = edge(tuple(path.rows), point, local_cap, "xXyYzZ")
                path.extend(steps)
        for slot, word in enumerate(old[right]):
            align(path, slot, word)
        assert tuple(path.rows) == old[right], (left, right, path.rows, old[right])
        changes.append({"original_steps": [left, right], "over_cap_instructions": len(over_cap),
                        "new_steps": [before, path.total]})
        cursor = right
    path.extend(rank_three[cursor:])
    assert tuple(path.rows) == old[-1] and path.cyclic_peak <= cap
    return changes


def splice(raw, route):
    ledger = list(map(json.loads, raw.splitlines()))
    stabilize, delete = ledger[1], ledger[-2]
    start, target = tuple(ledger[0]["start"]), tuple(ledger[-1]["target"])
    assert stabilize == {"op": "stabilize", "generator": "z"}
    assert delete["op"] == "destabilize" and delete["generator"] == "z"
    with BytesIO() as sink:
        path = StrictPath(start, sink)
        path.add(stabilize)
        changes = replace(path, ledger[2:-2], route)
        path.add(delete)
        assert tuple(path.rows) == target
        path.record((json.dumps({"target": path.rows}, separators=(",", ":")) + "\n").encode())
        new = list(map(json.loads, sink.getvalue().splitlines()))
    return new, changes, statistics(path)


def statistics(path):
    return {
        "moves": path.total,
        "rank_peak": path.peak_rank,
        "raw_peak": path.raw_peak,
        "cyclic_peak": path.cyclic_peak,
        "final_words": path.rows,
        "sha256": path.digest.hexdigest(),
    }


def compact(path, moves, target):
    rows = tuple(path.rows)
    trail = [tuple(map(canonical, rows))]
    indices = {trail[0]: 0}
    for move in moves:
        rows = apply(rows, move)
        point = tuple(map(canonical, rows))
        if point in indices:
            while len(trail) > indices[point] + 1:
                del indices[trail.pop()]
        else:
            indices[point] = len(trail)
            trail.append(point)
    assert rows == target
    for slot, word in enumerate(trail[0]):
        align(path, slot, word)
    for point in trail[1:]:
        local_cap = max(energy(path.rows), energy(point))
        _, moves = edge(tuple(path.rows), tuple(sorted(point)), local_cap, "xXyYzZ")
        path.extend(moves)
        assert tuple(path.rows) == point
    for slot, word in enumerate(target):
        align(path, slot, word)
    return len(trail) - 1


def stable_output(ledger, cap, output):
    start, stabilize = ledger[0]["start"], ledger[1]
    final, delete = ledger[-1]["target"], ledger[-2]
    target = final[:]
    target.insert(delete["i"], delete["generator"])
    with output.open("wb") as sink:
        path = StrictPath(start, sink)
        path.add(stabilize)
        count = compact(path, ledger[2:-2], tuple(target))
        path.add(delete)
        assert path.rows == final and path.cyclic_peak <= cap
        path.record((json.dumps({"target": path.rows}, separators=(",", ":")) + "\n").encode())
    return {"product_edges": count, **statistics(path)}


def prefix_output(source, route, output):
    start, target = tuple(source["start"]), tuple(source["target"])
    assert start[-1] == "z"
    stabilize = {"op": "stabilize", "generator": "z"}
    with BytesIO() as sink:
        path = StrictPath(start[:2], sink)
        path.add(stabilize)
        changes = replace(path, source["moves"], route)
        spliced = list(map(json.loads, sink.getvalue().splitlines()[2:]))
    with BytesIO() as sink:
        path = StrictPath(start[:2], sink)
        path.add(stabilize)
        count = compact(path, spliced, target)
        moves = list(map(json.loads, sink.getvalue().splitlines()[2:]))
    proof = certificate(start, moves, target)
    receipt = replay(proof)
    assert receipt["cyclic_peak"] <= route["cyclic_cap"]
    output.write_text(json.dumps(proof, separators=(",", ":")) + "\n")
    return {"detours": changes, "compact": {"product_edges": count, **receipt,
                                             "sha256": sha256(output.read_bytes()).hexdigest()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("route", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--prefix", action="store_true", help="preserve the literal rank-three endpoint")
    args = parser.parse_args()
    raw, route_bytes = args.source.read_bytes(), args.route.read_bytes()
    route = json.loads(route_bytes)
    receipt = {
        "source_sha256": sha256(raw).hexdigest(),
        "route_sha256": sha256(route_bytes).hexdigest(),
        "cap": route["cyclic_cap"],
    }
    if args.prefix:
        receipt.update(prefix_output(json.loads(raw), route, args.output))
    else:
        ledger, changes, spliced = splice(raw, route)
        receipt.update(detours=changes, spliced=spliced,
                       compact=stable_output(ledger, route["cyclic_cap"], args.output))
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
