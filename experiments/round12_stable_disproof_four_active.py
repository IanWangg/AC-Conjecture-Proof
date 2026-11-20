"""Compare short four-active intervals with three-slot formal balls."""

from collections import Counter, defaultdict
import json

from round11_stable_disproof_symbolic4 import ordinary
from round12_stable_disproof_symbolic6 import cyclic_relation, inverse, reduce, substitute_removed


def ball(start, radius, targets=None):
    reached = frontier = {start}
    for _ in range(radius):
        if targets is not None and targets <= reached:
            break
        frontier = {tuple(sorted(v)) for u in frontier for v in ordinary(u)} - reached
        reached = reached.union(frontier)
    return reached


def terminal_cases(span):
    result = set()
    for copy in ("a", "A"):
        states = {("a", "b", "c", copy)}
        for _ in range(span - 2):
            states = {child for state in states for child in ordinary(state) if "" not in child}
        for state in states:
            for i, removed in enumerate(state):
                answer = tuple(sorted(state[:i] + state[i + 1:]))
                for j, donor in enumerate(state):
                    if i != j:
                        result.add((removed, donor, answer))
                        result.add((removed, inverse(donor), answer))
    return result


def elimination(relation, letter):
    i = relation.lower().index(letter)
    word = reduce(inverse(relation[:i]) + inverse(relation[i + 1:]))
    if relation[i].isupper():
        word = inverse(word)
    return {letter: word, letter.upper(): inverse(word)}


def powers_from_relation(relation):
    for i in range(len(relation)):
        w = relation[i:] + relation[:i]
        if len(w) == 5 and w == w[0] * 2 + w[2] + w[0] + w[2] and w[0].lower() != w[2].lower():
            # U^2 V U V = U (UV)^2 = 1, with t the value of UV.
            u, v = w[0], w[2]
            return {u: "TT", inverse(u): "tt", v: "ttt", inverse(v): "TTT"}
    raise AssertionError(f"unhandled relation {relation}")


def search(span):
    original = ("a", "b", "c")
    reached = ball(original, span)
    candidates = terminal_cases(span)
    counts = Counter()
    relations = defaultdict(list)
    for removed, donor, surviving in sorted(candidates):
        if surviving in reached:
            counts["literal_replacement"] += 1
        elif substitute_removed(removed, donor, surviving) in reached:
            counts["substitute_last_equality"] += 1
        else:
            relations[cyclic_relation(removed + inverse(donor))].append((removed, donor, surviving))

    checked = {}
    for relation, cases in sorted(relations.items()):
        letter = next((c for c in "abc" if relation.lower().count(c) == 1), None)
        if letter is not None:
            method = "eliminate_single_occurrence"
            marking = elimination(relation, letter)
        elif relation == "AAAAA":
            # An active a is nonidentity. This is impossible in a free group or a finite 2-group.
            counts["impossible_order_five"] += len(cases)
            checked[relation] = {"method": "impossible_order_five", "covered_cases": len(cases),
                                 "example_case": cases[0]}
            continue
        else:
            assert span == 4
            method = "cyclic_power_substitution"
            marking = powers_from_relation(relation)
        substitutions = str.maketrans(marking)

        def substitute(rows):
            return tuple(sorted(reduce(row.translate(substitutions)) for row in rows))

        targets = {substitute(surviving) for _, _, surviving in cases}
        # Drop the cache between relations to keep the largest test bounded in memory.
        ordinary.cache_clear()
        quotient_ball = ball(substitute(original), span, targets)
        assert targets <= quotient_ball
        counts[method] += len(cases)
        checked[relation] = {"method": method, "substitution": marking, "covered_cases": len(cases),
                             "formal_vertices_through_last_target": len(quotient_ball), "example_case": cases[0]}

    assert sum(counts.values()) == len(candidates)
    return {"span": span, "formal_rank_three_radius_ball": len(reached), "all_terminal_templates": len(candidates),
            "counts": counts, "last_equality_classes": checked}


if __name__ == "__main__":
    print(json.dumps([search(span) for span in (2, 3, 4)], indent=2))
