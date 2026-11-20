"""Check mixed three-phase envelopes over the external energy-24 pair."""

import argparse
from collections import Counter, deque
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd

from primitive_map_pairs import LETTERS, decide, fold, follow, inverse, reduce, verify_absence
from round10_ac_disproof_outsider_quotient import graph_rank
from round11_ac_disproof_wirtinger import ROSE, verify_single_voltage
from round13_ac_disproof_external import PAIR
from round15_ac_disproof_two_phases import verify_refinement
from round16_ac_disproof_two_phases import AK3
from round17_ac_disproof_three_phases import (
    check_character, conjugated_copies, cumulative_fold, multiple_copies, primitive_or_absence,
)
from u_verify_voltage_phase import fold_word_arcs
from v_vertex_identification import fold_identification, spanning
from v_voltage_cycle_review import review


def weighted_fold(graph, first, second):
    """Fold the two vertices with height difference -1, tracking forced differences."""
    size = len(graph) // 4
    parent = list(range(size))
    offset = [0] * size
    arcs = [[edge if graph[edge] >= 0 else -1 for edge in range(4 * v, 4 * v + 4)]
            for v in range(size)]

    def root(vertex):
        if parent[vertex] != vertex:
            top, rise = root(parent[vertex])
            parent[vertex] = top
            offset[vertex] += rise
        return parent[vertex], offset[vertex]

    pending = deque([(first, second, -1)])
    modulus = 0
    while pending:
        a, b, difference = pending.popleft()
        top_a, height_a = root(a)
        top_b, height_b = root(b)
        translation = difference + height_a - height_b
        if top_a == top_b:
            modulus = gcd(modulus, translation)
            continue
        parent[top_b] = top_a
        offset[top_b] = translation
        for letter, right in enumerate(arcs[top_b]):
            if right < 0:
                continue
            left = arcs[top_a][letter]
            if left < 0:
                arcs[top_a][letter] = right
                continue
            left_height = root(left // 4)[1]
            right_height = root(right // 4)[1]
            pending.append((graph[left], graph[right], right_height - left_height))

    roots = [root(v) for v in range(size)]
    names = {roots[0][0]: 0}
    order = [roots[0][0]]
    folded, weights = [], []
    for top in order:
        for edge in arcs[top]:
            if edge < 0:
                folded.append(-1)
                weights.append(0)
                continue
            end = graph[edge]
            target, height = roots[end]
            if target not in names:
                names[target] = len(order)
                order.append(target)
            folded.append(names[target])
            weights.append(height - roots[edge // 4][1])
    projection = [names[top] for top, _ in roots]

    def zero(value):
        return value % modulus == 0 if modulus else value == 0

    assert zero(roots[first][1] - roots[second][1] - 1)
    for edge, end in enumerate(graph):
        if end < 0:
            continue
        vertex, letter = divmod(edge, 4)
        projected_edge = 4 * projection[vertex] + letter
        assert folded[projected_edge] == projection[end]
        assert zero(weights[projected_edge] - roots[end][1] + roots[vertex][1])
    for edge, end in enumerate(folded):
        if end >= 0:
            vertex, letter = divmod(edge, 4)
            assert zero(weights[edge] + weights[4 * end + (letter ^ 1)])
    return tuple(folded), tuple(weights), modulus


def normalized_weights(graph, weights):
    paths = spanning(graph)[0]
    heights = []
    for v in range(len(paths)):
        height = vertex = 0
        for letter in paths[v]:
            edge = 4 * vertex + LETTERS.index(letter)
            height += weights[edge]
            vertex = graph[edge]
        assert vertex == v
        heights.append(height)
    values = tuple(heights[e // 4] + weights[e] - heights[end] if end >= 0 else 0
                   for e, end in enumerate(graph))
    sign = next((1 if value > 0 else -1 for value in values if value), 1)
    return tuple(sign * value for value in values)


@lru_cache(maxsize=12000)
def integer_certificate(graph, weights):
    broad_inequalities = refined_inequalities = 0
    for test in review(graph, weights)["checks"]:
        if test["status"] == "PASS":
            broad_inequalities += verify_single_voltage(graph, weights, test)
            continue
        letters = [LETTERS[index] for index in test["alphabet"]]
        a = letters[test["forbidden_double"]]
        b = letters[1 - test["forbidden_double"]]
        for pattern in (a + b + a, b * 3):
            receipt = verify_refinement(graph, weights, "".join(letters), (a * 2, pattern))
            refined_inequalities += receipt["inequalities"]
    return broad_inequalities, refined_inequalities


def finite_cover(graph, weights, modulus):
    size = len(graph) // 4
    if size * modulus > 255:
        raise ValueError("Finite cover exceeds the partial-map implementation limit")
    cover = []
    for level in range(modulus):
        for edge, end in enumerate(graph):
            target_level = (level + weights[edge]) % modulus
            cover.append(size * target_level + end if end >= 0 else -1)
    return tuple(cover)


def first_representatives(gap_limit):
    source = fold(PAIR)
    if gap_limit:
        for length in range(2, gap_limit + 1):
            for letters in product(LETTERS, repeat=length):
                word = "".join(letters)
                if reduce(word) != word:
                    continue
                if any(follow(source, 0, word[:i]) >= 0
                       and follow(source, 0, inverse(word[i:])) >= 0 for i in range(length + 1)):
                    continue
                yield None, None, word
        return
    paths = spanning(source)[0]
    for a, b in combinations(range(len(paths)), 2):
        for first, last in ((a, b), (b, a)):
            yield first, last, reduce(paths[first] + inverse(paths[last]))


def census(second, gap_limit=0):
    groups = {}
    for first, last, t in first_representatives(gap_limit):
        words = conjugated_copies(PAIR, dict.fromkeys(("", t, second, reduce(second + t))))
        n = fold((*PAIR, t, second))
        j = fold(words)
        groups.setdefault((n, j), []).append((first, last, t))

    totals = Counter()
    checksum = sha256()
    examples = {}
    for (n, j), representatives in groups.items():
        t = representatives[0][2]
        words = conjugated_copies(PAIR, dict.fromkeys(("", t, second, reduce(second + t))))
        assert tuple(fold_word_arcs(words)) == j
        assert tuple(fold_word_arcs((*PAIR, t, second))) == n
        locations = spanning(j)[0]
        image = [follow(n, 0, locations[v]) for v in range(len(locations))]
        assert min(image) >= 0
        for a, b in combinations(range(len(locations)), 2):
            totals["last_vertex_pairs"] += 1
            if n != ROSE and cumulative_fold(n, *sorted((image[a], image[b]))) != ROSE:
                totals["proper_cumulative"] += 1
                continue
            k, weights, modulus = weighted_fold(j, a, b)
            assert k == fold_identification(j, a, b)[0]
            status, primitive = primitive_or_absence(k)
            if status == "ABSENT":
                totals["whole_primitive_free"] += 1
                totals["partial_map_pair_states"] += primitive["closed_map_pair_states_checked"]
                checksum.update(repr((t, a, b, k, "whole")).encode())
                continue
            if not modulus:
                voltage = normalized_weights(k, weights)
                try:
                    broad, refined = integer_certificate(k, voltage)
                except AssertionError:
                    result = "unresolved_integer"
                else:
                    totals["broad_inequalities"] += broad
                    totals["refined_inequalities"] += refined
                    result = "integer_character"
                checksum.update(repr((t, a, b, k, voltage, result)).encode())
            else:
                cover = finite_cover(k, weights, modulus)
                cert = decide(cover, 0, save_certificate=True)
                if cert["status"] == "ABSENT":
                    verify_absence(cert)
                    result = "finite_cover_primitive_free"
                else:
                    assert cert["status"] == "PRIMITIVE"
                    primitive = cert["witness"]
                    result = "primitive_in_kernel"
                checksum.update(repr((t, a, b, k, weights, modulus, result)).encode())
            totals[result] += 1
            if result != "integer_character":
                examples.setdefault(result, {"first": t, "second": second,
                    "last": reduce(locations[a] + inverse(locations[b])), "modulus": modulus,
                    "primitive": primitive, "folded_graph": k})
    return {"source": PAIR, "second": second, "first_gap_word_limit": gap_limit,
            "ordered_source_pairs": sum(map(len, groups.values())),
            "distinct_initial_core_pairs": len(groups), **dict(totals),
            "examples": examples, "case_digest": checksum.hexdigest()}


def literal_controls():
    p, b = AK3
    center = conjugated_copies(AK3, ("x",))
    far_p, far_b = conjugated_copies(AK3, ("xx",))
    categories = {
        "stationary_first_row_p": (p, *center, far_p, far_b),
        "stationary_first_row_b": (b, *center, far_p, far_b),
        "moving_p": (*AK3, *center, far_p),
    }
    rows = {}
    for name, words in categories.items():
        graph = fold((*words, "Y"))
        assert tuple(fold_word_arcs((*words, "Y"))) == graph
        rows[name] = {"generators": words, "graph": graph, "rank": graph_rank(graph),
                      **check_character(graph, words, "Y")}
    far_b_envelope = fold((*AK3, *center, far_b, "Y"))
    assert far_b_envelope == ROSE
    return {"relative_words": ("x", "x", "Y"), "cases": rows,
            "moving_b_coarse_envelope": far_b_envelope,
            "arbitrary_stationary_row": literal_fibre_product(center + (far_p, far_b))}


def literal_fibre_product(words):
    source = fold(AK3)
    b_graph = fold((*words, "Y"))
    assert tuple(fold_word_arcs((*words, "Y"))) == b_graph
    kernel = check_character(b_graph, words, "Y")
    _, _, chords, _ = spanning(b_graph)
    weights = [0] * len(b_graph)
    for (a, letter, _), (index, sign) in chords.items():
        weights[4 * a + letter] = sign * kernel["character"][index]

    fibre = {(0, 0): ("", 0)}
    order = [(0, 0)]
    for a, b in order:
        prefix, height = fibre[a, b]
        for letter, symbol in enumerate(LETTERS):
            edge = 4 * b + letter
            target = source[4 * a + letter], b_graph[edge]
            if min(target) < 0:
                continue
            new_height = height + weights[edge]
            if target in fibre:
                assert fibre[target][1] == new_height
            else:
                fibre[target] = (prefix + symbol, new_height)
                order.append(target)

    assert len(fibre) == 12
    assert len({(b, fibre[a, b][1]) for a, b in fibre}) == len(fibre)
    gapless = []
    for (a, b), (c, d) in combinations(fibre, 2):
        if a != c:
            continue
        representative = reduce(fibre[a, b][0] + inverse(fibre[c, d][0]))
        assert follow(source, 0, representative) == 0
        enlarged = fold((*words, representative, "Y"))
        assert fold_identification(b_graph, b, d)[0] == enlarged
        certificate = check_character(enlarged, (*words, representative), "Y")
        gapless.append({"left": (a, b), "right": (c, d), "representative": representative,
                        "graph": enlarged, "character": certificate["character"]})
    assert [check["representative"] for check in gapless] == list(AK3)

    explored = 0
    for a, b in fibre:
        for alphabet in ("xy", "xY", "Xy", "XY"):
            letters = tuple(LETTERS.index(symbol) for symbol in alphabet)
            for forbidden in letters:
                seen = {(a, -1)}
                frontier = [(a, -1)]
                for vertex, previous in frontier:
                    if previous != -1:
                        for c, d in fibre:
                            assert c != vertex or b_graph[4 * d + (previous ^ 1)] >= 0
                    for letter in letters:
                        target = source[4 * vertex + letter]
                        if target < 0 or previous == letter == forbidden:
                            continue
                        if previous == -1 and b_graph[4 * b + letter] >= 0:
                            continue
                        state = target, letter
                        if state not in seen:
                            seen.add(state)
                            frontier.append(state)
                explored += len(seen) - 1
    assert explored > 0
    return {"graph": b_graph, "base_kernel": kernel, "fibre_states": [
        {"source_vertex": a, "overgroup_vertex": b, "path": path, "height": height}
        for (a, b), (path, height) in fibre.items()], "gapless_merges": gapless,
        "signed_double_free_gap_states": explored, "signed_double_free_gaps": 0}


def quotient_controls():
    finite = fold(("xxx", "y"))
    graph, weights, modulus = weighted_fold(finite, 0, 1)
    assert graph == ROSE and modulus == 3
    finite_result = decide(finite_cover(graph, weights, modulus), 0)
    assert finite_result["status"] == "PRIMITIVE"
    assert finite_result["witness"]["cyclic_primitive_word"] == "y"

    infinite = fold(("xy",))
    graph, weights, modulus = weighted_fold(infinite, 0, 1)
    assert graph == ROSE and modulus == 0 and weights[0] + weights[2] == 0

    literal = fold(multiple_copies(AK3, "x"))
    paths = spanning(literal)[0]
    first, second = next((a, b) for a, b in product(paths, repeat=2)
                         if reduce(paths[a] + inverse(paths[b])) == "Y")
    graph, weights, modulus = weighted_fold(literal, first, second)
    assert graph == ROSE and modulus == 1
    return {"finite_source": ["xxx", "y"], "finite_order": 3,
            "finite_kernel_primitive": finite_result["witness"],
            "infinite_source": ["xy"], "infinite_kernel_primitive": "xy",
            "literal_AK3_rose_order": modulus}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--second", choices=("x", "y"))
    parser.add_argument("--first-gap-at-most", type=int, choices=(2, 3), default=0)
    args = parser.parse_args()
    if args.second:
        result = census(args.second, args.first_gap_at_most)
    else:
        result = {"literal_AK3": literal_controls(), "quotient_controls": quotient_controls()}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
