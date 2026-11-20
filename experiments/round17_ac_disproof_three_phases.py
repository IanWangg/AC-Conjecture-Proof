"""Check three phases whose first two relative words repeat a source-path word."""

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json

from primitive_map_pairs import LETTERS, decide, fold, follow, inverse, reduce, verify_absence
from round10_ac_disproof_outsider_quotient import graph_rank
from round11_ac_disproof_wirtinger import ROSE
from round13_ac_disproof_external import PAIR, kernel_basis
from round15_ac_disproof_two_phases import check_kernel
from round16_ac_disproof_two_phases import AK3
from u_verify_voltage_phase import fold_relation, fold_word_arcs
from v_vertex_identification import fold_identification, spanning


def conjugated_copies(pair, conjugators):
    return tuple(reduce(t + row + inverse(t)) for t in conjugators for row in pair)


def multiple_copies(pair, word, powers=(0, 1, 2)):
    conjugators = [word * exponent for exponent in powers]
    return conjugated_copies(pair, conjugators)


def dot(left, right):
    assert len(left) == len(right)
    return sum(a * b for a, b in zip(left, right))


def check_character(graph, words, added):
    _, chords, _, coordinates = spanning(graph)
    if len(words) + 1 == len(chords):
        return check_kernel(graph, words, added)
    rows = [coordinates(word) for word in words]
    character, = kernel_basis(rows)
    assert abs(dot(character, coordinates(added))) == 1
    for indices in combinations(range(len(words)), len(chords) - 1):
        sub_basis = tuple(kernel_basis([rows[i] for i in indices]))
        if sub_basis == (character,):
            checked = check_kernel(graph, [words[i] for i in indices], added)
            assert not any(dot(checked["character"], row) for row in rows)
            return checked
    raise AssertionError("No character-defining subset")


@lru_cache(maxsize=30000)
def cumulative_fold(graph, first, second):
    result = fold_identification(graph, first, second)[0]
    assert tuple(fold_relation(graph, (first, second))[0]) == result
    return result


@lru_cache(maxsize=40000)
def primitive_or_absence(graph):
    cert = decide(graph, 0, save_certificate=True)
    if cert["status"] == "ABSENT":
        return "ABSENT", verify_absence(cert)
    assert cert["status"] == "PRIMITIVE"
    return "PRIMITIVE", cert["witness"]


def census(second_power):
    source = fold(PAIR)
    paths = spanning(source)[0]
    representatives = {}
    powers = tuple(sorted({0, 1, second_power, second_power + 1}))
    rank = 2 * len(powers)
    for a, b in combinations(range(len(paths)), 2):
        t = reduce(paths[a] + inverse(paths[b]))
        j = fold(multiple_copies(PAIR, t, powers))
        n = fold((*PAIR, t))
        assert graph_rank(j) == rank and graph_rank(n) == 3
        representatives.setdefault((n, j), []).append((a, b, t))

    total = Counter()
    checksum = sha256()
    records = []
    rank_drop_example = None
    for (n, j), source_pairs in representatives.items():
        t = source_pairs[0][2]
        words = multiple_copies(PAIR, t, powers)
        paths = spanning(j)[0]
        images = [follow(n, 0, paths[v]) for v in range(len(paths))]
        assert min(images) >= 0 and tuple(fold_word_arcs(words)) == j
        counts = Counter()
        for a, b in combinations(range(len(paths)), 2):
            r = reduce(paths[a] + inverse(paths[b]))
            cumulative = cumulative_fold(n, *sorted((images[a], images[b])))
            if cumulative != ROSE:
                counts["proper_cumulative"] += 1
                checksum.update(repr((t, a, b, cumulative)).encode())
                continue
            k = fold_identification(j, a, b)[0]
            assert tuple(fold_relation(j, (a, b))[0]) == k
            status, primitive_test = primitive_or_absence(k)
            if status == "ABSENT":
                witness = primitive_test
                counts["primitive_free_core"] += 1
                counts["partial_map_pair_states"] += witness["closed_map_pair_states_checked"]
            else:
                witness = check_character(k, words, r)
                enlarged_rank = graph_rank(k)
                counts[f"character_rank_{enlarged_rank}"] += 1
                counts["broad_inequalities"] += witness["broad_inequalities"]
                counts["balanced_gap_inequalities"] += sum(
                    row["inequalities"] for row in witness["refined"])
                if enlarged_rank < rank and rank_drop_example is None:
                    _, _, _, coordinates = spanning(k)
                    rank_drop_example = {
                        "representative": t, "third_relative_word": r,
                        "enlarged_core": k, "ambient_primitive_loop": primitive_test,
                        "coordinate_rows": [coordinates(w) for w in words],
                        "third_relative_coordinates": coordinates(r), **witness,
                    }
            checksum.update(repr((t, a, b, k, witness)).encode())
        total.update(counts)
        records.append({"source_pairs": source_pairs, "vertices_before_last_fold": len(j) // 4,
                        **dict(counts)})

    expected_classes, *expected_counts = {
        1: (68, 51804, 5952, 12836, 138),
        2: (68, 91042, 11734, 19927, 348),
        3: (84, 127721, 25843, 24566, 278),
    }[second_power]
    assert len(representatives) == expected_classes and sum(map(len, representatives.values())) == 136
    rank_drop_count = sum(value for field, value in total.items()
                          if field.startswith("character_rank_") and field != f"character_rank_{rank + 1}")
    assert (total["proper_cumulative"], total["primitive_free_core"],
            total[f"character_rank_{rank + 1}"], rank_drop_count) == tuple(expected_counts)
    assert rank_drop_example is not None
    return {"source": PAIR, "second_power": second_power, "powers": powers,
            "source_vertex_pairs": 136, "distinct_core_pairs": expected_classes,
            **dict(total), "cases": records, "case_digest": checksum.hexdigest(),
            "rank_drop_example": rank_drop_example}


def source_image_control(first, second, third, expected_sizes, expected_contacts=()):
    source = fold(PAIR)
    paths = spanning(source)[0]
    conjugators = tuple(dict.fromkeys(("", first, second, reduce(second + first))))
    words = (*conjugated_copies(PAIR, conjugators), third)
    graph = fold(words)
    assert tuple(fold_word_arcs(words)) == graph
    assert fold((*PAIR, first, second, third)) == ROSE
    images = []
    for conjugator in conjugators:
        root = follow(graph, 0, conjugator)
        assert root >= 0
        image = [follow(graph, root, paths[vertex]) for vertex in range(len(paths))]
        vertices = set(image)
        assert min(vertices) >= 0
        edges = set()
        for edge, end in enumerate(source):
            if end < 0:
                continue
            vertex, letter = divmod(edge, len(LETTERS))
            start, end = image[vertex], image[end]
            assert graph[4 * start + letter] == end
            edges.add((start, letter, end))
        images.append({"conjugator": conjugator, "vertices": sorted(vertices),
                       "rank": 1 + len(edges) // 2 - len(vertices)})
    assert tuple(len(image["vertices"]) for image in images) == expected_sizes
    contacts = []
    for i, j in combinations(range(len(images)), 2):
        common = set(images[i]["vertices"]) & set(images[j]["vertices"])
        if common:
            assert len(images[i]["vertices"]) == len(paths) == len(images[j]["vertices"])
            contacts.append((i, j, sorted(common)))
    assert tuple((i, j, len(vertices)) for i, j, vertices in contacts) == expected_contacts
    return {"relative_words": (first, second, third), "enlarged_graph": graph,
            "rank": graph_rank(graph), "source_images": images, "contacts": contacts}


def ak3_control():
    marked = multiple_copies(AK3, "x")
    enlarged = fold((*marked, "Y"))
    assert graph_rank(fold(marked)) == 6
    assert enlarged == ROSE and tuple(fold_word_arcs((*marked, "Y"))) == ROSE
    return {"source": AK3, "first": "x", "second": "x", "third": "Y",
            "six_generators": marked, "enlarged_graph": enlarged}


def image_controls():
    return [source_image_control("xY", "xY", "y", (9, 17, 17)),
            source_image_control("xY", "XY", "y", (9, 17, 17, 17)),
            source_image_control("xY", "xxx", "y", (9, 17, 17, 17), ((1, 2, 2),))]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--power", type=int, choices=(1, 2, 3))
    args = parser.parse_args()
    if args.power:
        print(json.dumps(census(args.power), indent=2))
        return
    print(json.dumps({"energy24": [census(1), census(2), census(3)],
                      "source_image_controls": image_controls(),
                      "literal_AK3_envelope_escape": ak3_control()}, indent=2))


if __name__ == "__main__":
    main()
