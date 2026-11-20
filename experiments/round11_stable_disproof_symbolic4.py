"""Cover four- and five-instruction excursions by formal rank-two replays."""

import argparse
from functools import cache
import json

from quotient_certificates import inverse_word as inverse, reduce_word as reduce


@cache
def ordinary(rows):
    result = set()
    for i, row in enumerate(rows):
        images = {inverse(row)}
        for letter in "xXyY":
            images.add(reduce(letter + row + inverse(letter)))
        for j, donor in enumerate(rows):
            if i != j:
                images.add(reduce(row + donor))
                images.add(reduce(row + inverse(donor)))
        result.update(rows[:i] + (image,) + rows[i + 1:] for image in images)
    return result


def pair_ball(radius):
    reached = frontier = {("a", "b")}
    for _ in range(radius):
        frontier = {tuple(sorted(child)) for state in frontier for child in ordinary(state)} - reached
        reached = reached.union(frontier)
    return reached


def parity(word):
    return tuple(word.lower().count(generator) % 2 for generator in "ab")


def candidates(span):
    for orientation in ("a", "A"):
        layer = {("a", "b", orientation)}
        for _ in range(span - 2):
            layer = {child for state in layer for child in ordinary(state) if "" not in child}
        for state in layer:
            for i, removed in enumerate(state):
                for j, donor in enumerate(state):
                    if i == j or parity(removed) != parity(donor):
                        continue
                    pair = tuple(sorted(state[:i] + state[i + 1:]))
                    yield removed, donor, pair
                    yield removed, inverse(donor), pair


def exponent_difference(left, right):
    return tuple(left.count(letter) - left.count(letter.upper()) - right.count(letter) + right.count(letter.upper())
                 for letter in "ab")


def search(span):
    large = pair_ball(span)
    short = pair_ball(2) if span == 4 else large
    triples = set(candidates(span))
    exceptions = []
    witnesses = []
    for removed, signed_donor, pair in sorted(triples):
        if pair in large:
            continue
        # The hypothesized last cancellation supplies removed = signed_donor.
        replaced = list(pair)
        if signed_donor in replaced:
            replaced[replaced.index(signed_donor)] = removed
        else:
            replaced[replaced.index(inverse(signed_donor))] = inverse(removed)
        formal_target = tuple(sorted(replaced))
        item = {"removed": removed, "signed_donor_equal_to_removed": signed_donor,
                "remaining_pair": pair, "pair_after_using_return_equality": formal_target}
        if formal_target in short:
            exceptions.append(item)
            continue
        assert span == 5
        difference = exponent_difference(removed, signed_donor)
        if any(value % 16 for value in difference):
            item.update(obstruction="abelianization_modulo_sixteen", coefficient_difference=difference)
        else:
            assert (removed, signed_donor) == ("aBA", "B")
            item.update(obstruction="commutation_with_independent_linear_terms")
        witnesses.append(item)
    report = {f"rank_two_formal_ball_{'four' if span == 4 else 'five'}": len(large),
              "terminal_symbolic_cases": len(triples),
              "cases_using_last_cancellation_equality": exceptions}
    if witnesses:
        report["impossible_last_cancellations"] = witnesses
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("span", type=int, nargs="?", default=4, choices=(4, 5))
    print(json.dumps(search(parser.parse_args().span), indent=2))
