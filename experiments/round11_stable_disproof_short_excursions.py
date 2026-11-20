"""Lift all short activated windows of the degree-nine one-spare corridor."""

import argparse
from functools import cache
import json

from round01_stable_disproof_search import AK3, MagnusQuotient, ONE
from round06_stable_disproof_tiers import apply, independent_replay, instruction_labels
from round10_stable_disproof_neighborhood import pack
from round10_stable_disproof_saturate import corridor_data, saturation, widths


def activated_windows(low, layers, span):
    @cache
    def active_neighbors(state):
        return {candidate for candidate in low.neighbors(state, True) if ONE not in candidate}

    for start in range(len(layers) - span + 1):
        entering = set().union(*map(active_neighbors, layers[start]))
        leaving = set().union(*map(active_neighbors, layers[start + span - 1]))
        if span == 2:
            middle = [entering.intersection(leaving)]
        else:
            compatible = {state: active_neighbors(state).intersection(leaving) for state in entering}
            middle = [{state for state, following in compatible.items() if following},
                      set().union(*compatible.values())]
        if all(middle):
            yield start, layers[:start + 1] + middle + layers[start + span - 1:]


def lift_window(low, high, allowed):
    new_generator = high.generators[2]
    start = tuple(sorted(zip((*map(low.evaluate, AK3), ONE),
                             (*map(high.evaluate, AK3), new_generator))))
    goal = tuple(sorted(zip((*low.generators, ONE), high.generators)))
    menu = tuple(instruction_labels(3, 2, False))
    layers = [{start}]
    for layer in allowed[1:]:
        following = set()
        for state in layers[-1]:
            projected, full = zip(*state)
            for move in menu:
                low_image = apply(low, projected, move)
                if tuple(sorted(low_image)) in layer:
                    high_image = apply(high, full, move)
                    following.add(tuple(sorted(zip(low_image, high_image))))
        layers.append(following)

    if goal not in layers[-1]:
        return widths(layers), None

    # Recover an actual labelled witness from the unordered lift.
    path = [goal]
    for layer in reversed(layers[:-1]):
        left, right = zip(*path[-1])
        for move in menu:
            previous = tuple(sorted(zip(apply(low, left, move), apply(high, right, move))))
            if previous in layer:
                path.append(previous)
                break
        else:
            raise AssertionError("missing predecessor in a reversible graph")
    left, right = (*map(low.evaluate, AK3), ONE), (*map(high.evaluate, AK3), new_generator)
    marks = []
    for target in path[-2::-1]:
        for move in menu:
            next_left, next_right = apply(low, left, move), apply(high, right, move)
            if tuple(sorted(zip(next_left, next_right))) == target:
                left, right = next_left, next_right
                marks.append(move)
                break
        else:
            raise AssertionError("could not follow an unordered edge in the marking")
    endpoint_order = independent_replay(high.degree, 1, marks)
    return widths(layers), {"moves": marks, "independently_replayed_endpoint": endpoint_order}


def search(degree):
    paths, _ = saturation()
    assert widths(paths) == corridor_data()
    low = MagnusQuotient(2, 9)
    high = MagnusQuotient(3, degree)
    padded = [{tuple(sorted((*map(pack, pair), ONE))) for pair in tick} for tick in paths]
    records = []
    for span in (2, 3):
        for tick, allowed in activated_windows(low, padded, span):
            exact_widths, witness = lift_window(low, high, allowed)
            records.append({"excursion_instructions": span, "entry_tick": tick,
                            "allowed_widths": widths(allowed), "lifted_widths": exact_widths,
                            "witness": witness})
    return {"rank_two_projection_degree": 9, "full_rank_three_degree": degree,
            "middle_budget": 18, "conjugating_generators": ["x", "y"],
            "windows_with_low_excursions": len(records),
            "windows_retained_in_full_rank": sum(row["witness"] is not None for row in records),
            "windows": records}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("degree", type=int)
    args = parser.parse_args()
    if not 1 <= args.degree <= 10:
        parser.error("degree must be between one and ten")
    print(json.dumps(search(args.degree), indent=2))
