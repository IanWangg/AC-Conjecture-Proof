"""Remove six-instruction activated intervals using their last equality."""

from collections import Counter
from functools import cache
from itertools import permutations
import json

from round01_stable_disproof_search import MagnusQuotient
from round11_stable_disproof_symbolic4 import candidates, exponent_difference, inverse, pair_ball, reduce


def cyclic_relation(word):
    word = reduce(word)
    while len(word) > 1 and word[0] == word[-1].swapcase():
        word = word[1:-1]
    if not word:
        return ""
    return min(rotation[start:] + rotation[:start]
               for rotation in (word, inverse(word)) for start in range(len(word)))


def substitute_removed(removed, donor, pair):
    before, after = (donor, removed) if donor in pair else (inverse(donor), inverse(removed))
    replacement = list(pair)
    replacement[replacement.index(before)] = after
    return tuple(sorted(replacement))


@cache
def rules(relation):
    result = set()
    for word in (relation, inverse(relation)):
        for start in range(len(word)):
            rotation = word[start:] + word[:start]
            for cut in range((len(word) + 1) // 2, len(word)):
                result.add((rotation[:cut], inverse(rotation[cut:])))
    return tuple(sorted(result))


@cache
def rewrites(word, relation):
    reached = frontier = {word}
    for _ in range(2):
        following = set()
        for current in frontier:
            for before, after in rules(relation):
                following.update(reduce(current[:i] + after + current[i + len(before):])
                                 for i in range(len(current) - len(before) + 1)
                                 if current.startswith(before, i))
        frontier = following - reached
        reached = reached.union(frontier)
    return tuple(sorted(reached))


def degree_three_evaluations():
    quotient = MagnusQuotient(2, 3)
    elements = frontier = {1}
    while frontier:
        frontier = {quotient.multiply(a, x) for a in frontier for x in quotient.generators} - elements
        elements = elements.union(frontier)
    assert all(quotient.inverse(a) in elements for a in elements)
    pairs = [(a, b) for a, b in permutations(sorted(elements), 2)
             if (a >> 1) & 3 and (b >> 1) & 3 and (a >> 1) & 3 != (b >> 1) & 3]

    @cache
    def count_solutions(relation):
        solutions = 0
        for a, b in pairs:
            marking = dict(zip("abxy", (a, b, *quotient.generators)))
            marking.update({letter.upper(): quotient.inverse(value) for letter, value in tuple(marking.items())})
            image = 1
            for letter in relation:
                image = quotient.multiply(image, marking[letter])
            solutions += image == 1
        return solutions

    return len(elements), len(pairs), count_solutions


def main():
    radius = pair_ball(6)
    triples = set(candidates(6))
    count_elements, count_pairs, solutions = degree_three_evaluations()
    counts = Counter()
    relations = Counter()
    rewrites_used = []
    for removed, donor, pair in sorted(triples):
        if pair in radius:
            counts["literal_replacement"] += 1
            continue
        if substitute_removed(removed, donor, pair) in radius:
            counts["restated_last_equality"] += 1
            continue
        if any(coefficient % 16 for coefficient in exponent_difference(removed, donor)):
            counts["abelianization_modulo_sixteen"] += 1
            continue
        relation = cyclic_relation(removed + inverse(donor))
        relations[relation] += 1
        if not solutions(relation):
            counts["degree_three_obstruction"] += 1
            continue
        survivor = next((target for a in rewrites(pair[0], relation) for b in rewrites(pair[1], relation)
                         if (target := tuple(sorted((a, b)))) in radius), None)
        assert survivor is not None, (removed, donor, pair)
        counts["two_rewrites_per_row"] += 1
        rewrites_used.append([removed, donor, pair, relation, survivor])
    assert sum(counts.values()) == len(triples)
    print(json.dumps({"formal_rank_two_radius_six": len(radius), "all_terminal_templates": len(triples),
                      "counts": counts, "degree_three_group_elements": count_elements,
                      "degree_three_ordered_independent_pairs": count_pairs,
                      "last_equality_classes": {rel: {"templates": count, "degree_three_solutions": solutions(rel)}
                                                for rel, count in sorted(relations.items())},
                      "rewrite_witnesses": rewrites_used}, indent=2))


if __name__ == "__main__":
    main()
