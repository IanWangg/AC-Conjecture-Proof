"""Saturate the one-spare degree-eight corridor with ordinary length-16 paths."""

from functools import cache
import json
from pathlib import Path

from round01_stable_disproof_search import AK3, MagnusQuotient, ONE
from round06_stable_disproof_tiers import apply, independent_replay


def instruction(move):
    kind = move["op"]
    if kind == "invert":
        return kind, move["i"]
    if kind == "swap":
        return kind, 0, 1
    if kind == "multiply":
        return kind, move["i"], move["j"], move["sign"]
    return kind, move["i"], "xy".index(move["g"].lower()), (-1 if move["g"].isupper() else 1)


def search():
    root = Path(__file__).resolve().parents[1] / "results"
    preceding = json.loads((root / "round09_stable_disproof_searches.json").read_text())
    padded = preceding["one_spare_degree_nine_middle_budget_sixteen"]
    assert padded["spare_rows"] == 1 and padded["radii"] == [8, 8] and not padded["ordered"]
    boundary = next(tier for tier in padded["tiers"] if tier["degree"] == 8)
    left, right = boundary["widths"]
    assert left[-1] == boundary["midpoints"] == right[-1]
    expected = left + right[-2::-1]

    degree = 8
    graph = MagnusQuotient(2, degree)
    source = tuple(map(graph.evaluate, AK3))
    witness = json.loads((root / "round07_magnus_d8_witness.json").read_text())
    moves = [instruction(move) for move in witness["moves"]]
    assert witness["degree"] == degree and len(moves) == 16
    replayed = independent_replay(degree, 0, moves, erased=True)
    assert sorted(replayed) == [0, 1]
    layers = [{tuple(sorted(source))}]
    for move in moves:
        source = apply(graph, source, move)
        layers.append({tuple(sorted(source))})
    assert layers[-1] == {tuple(sorted(graph.generators))}

    @cache
    def adjacent(state):
        return set(graph.neighbors(state, True))

    profiles = [list(map(len, layers))]
    for span in (2, 3, 4):
        while True:
            before = list(map(len, layers))
            for t in range(len(layers) - span):
                forward = layers[t]
                for _ in range(span - 1):
                    forward = {child for state in forward for child in adjacent(state)}
                reverse = {child for state in layers[t + span] for child in adjacent(state)}
                layers[t + span - 1].update(forward & reverse)
            if list(map(len, layers)) == before:
                break
        profiles.append(list(map(len, layers)))
    assert profiles[-1] == expected
    assert all(ONE not in pair for layer in layers for pair in layer)
    return {"degree": degree, "middle_budget": 16, "one_spare_complete_widths": expected,
            "ordinary_seed_and_bridge_widths": profiles, "bridge_lengths": [2, 3, 4],
            "ordinary_seed_replayed_order": replayed, "total_corridor_incidences": sum(expected),
            "all_one_spare_corridor_vertices_idle": True}


if __name__ == "__main__":
    print(json.dumps(search(), indent=2, sort_keys=True))
