"""Exact outward-then-second-product search from the certified energy-15 waypoint."""

from collections import Counter
import argparse
import json
from pathlib import Path

from elementary_verify import replay
from free_waypoint_search import canonical, conj_ops, cyclic, expand_edge, inverse, variants, words_upto
from stallings_search import apply, primitive


def neighbours(state, cap, counters):
    for i in (0, 1):
        j = 1 - i
        bound = max(0, (cap - len(state[i]) - 2 * len(state[j])) // 2)
        tails = [(q, inverse(q)) for q in words_upto(bound)]
        for u in variants(state[i]):
            for v in variants(state[j]):
                for q, reverse in tails:
                    counters["products"] += 1
                    receiving = cyclic(u + q + v + reverse)
                    if len(receiving) + len(v) > cap:
                        continue
                    counters["admitted"] += 1
                    yield tuple(sorted((canonical(receiving), canonical(v)))), (i, u, v, q)


def trajectory(cert, middle, first, goal, second):
    start = tuple(cert["start"])
    current = tuple(cert["target"])
    ledger = list(cert["moves"])
    parent = tuple(sorted(current))
    for expected, edge in ((middle, first), (goal, second)):
        i, u, v, q = edge
        concrete_index = current.index(parent[i])
        current, ops = expand_edge(current, (concrete_index, u, v, q))
        assert tuple(sorted(current)) == expected
        ledger.extend(ops)
        parent = expected
    result = {
        "format": "ordinary-ac-elementary-v1",
        "start": list(start),
        "target": list(current),
        "moves": ledger,
    }
    receipt = replay(result)
    current = start
    peak = sum(map(len, current))
    for move in ledger:
        current = apply(current, move)
        peak = max(peak, sum(len(cyclic(w)) for w in current))
    receipt["cyclic_peak"] = peak
    return result, receipt


def barbell_control():
    start = ("xyxyXY", "y")
    bridge = "yx"
    moves = conj_ops(1, bridge) + [
        {"op": "invert", "i": 1},
        {"op": "multiply", "i": 0, "j": 1},
        {"op": "invert", "i": 1},
    ] + conj_ops(1, inverse(bridge))
    result = {
        "format": "ordinary-ac-elementary-v1",
        "start": list(start),
        "target": ["x", "y"],
        "moves": moves,
    }
    assert replay(result)["moves"] == 7
    return result


def write_json(path, record):
    path.write_text(json.dumps(record, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("anchor_certificate", type=Path)
    parser.add_argument("cap26_tsv", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    original = json.loads(args.anchor_certificate.read_text())
    replay(original)
    anchor = tuple(sorted(original["target"]))
    assert tuple(map(canonical, anchor)) == anchor
    assert sum(map(len, anchor)) == 15
    counters = [Counter(), Counter()]
    outgoing = {}
    cap = 28
    for pair, edge in neighbours(anchor, cap, counters[0]):
        if sum(map(len, pair)) > 26:
            outgoing.setdefault(pair, edge)
    reached = {}
    for middle in sorted(outgoing):
        for pair, edge in neighbours(middle, cap, counters[1]):
            reached.setdefault(pair, (middle, edge))
    universe = set(outgoing) | set(reached)
    below = {tuple(w.encode() for w in pair): pair for pair in universe if sum(map(len, pair)) <= 26}
    with args.cap26_tsv.open("rb") as source:
        for line in source:
            key = tuple(line.rstrip(b"\n").split(b"\t"))
            below.pop(key, None)
    novel_return = sorted(below.values(), key=lambda p: (sum(map(len, p)), p))
    novel = sorted({*outgoing, *novel_return, *(p for p in reached if sum(map(len, p)) > 26)})
    second_only = [p for p in novel if p not in outgoing]
    candidates = novel_return or second_only or [p for p in novel if p in reached]
    endpoint = min(candidates, key=lambda p: (
        sum(map(len, p)), sum(map(len, reached[p][0])), p
    ))
    middle, second = reached[endpoint]
    result, receipt = trajectory(original, middle, outgoing[middle], endpoint, second)
    assert receipt["cyclic_peak"] == max(26, sum(map(len, middle)), sum(map(len, endpoint)))
    positives = [list(pair) for pair in novel if any(primitive(w) for w in pair)]
    for name, rows in (("novel", novel), ("novel-return", novel_return)):
        (args.output / f"{name}.tsv").write_text("".join("\t".join(pair) + "\n" for pair in rows))
    write_json(args.output / "outward-witness.json", result)
    write_json(args.output / "barbell-control.json", barbell_control())
    write_json(args.output / "outward.json", {
        "anchor": list(anchor),
        "local_cap": cap,
        "product_counts": [dict(c) for c in counters],
        "first_outgoing_states": dict(sorted(Counter(sum(map(len, p)) for p in outgoing).items())),
        "two_step_distinct_states": len(reached),
        "novel_states": dict(sorted(Counter(sum(map(len, p)) for p in novel).items())),
        "primitive_coordinate_positives": positives,
        "new_outside_cap26_states_below_the_ceiling": len(novel_return),
        "outside_cap26_witness": {
            "goal": list(endpoint),
            "first_outside_pair": list(middle),
            "concrete_first_edge": outgoing[middle],
            "concrete_second_edge": second,
            **receipt,
        },
    })


if __name__ == "__main__":
    main()
