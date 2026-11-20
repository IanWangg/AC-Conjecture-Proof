"""Certify primitive incidence in the two literal four-conjugation prefix groups."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json

from primitive_map_pairs import LETTERS, compose, fold
from round06_stable_disproof_conjugations import START, envelope
from round19_ac_disproof_four_conjugations import EXPECTED
from round17_ac_disproof_three_phases import conjugated_copies
from u_verify_voltage_phase import fold_word_arcs
from v_vertex_identification import spanning


ALPHABETS = ("xy", "xY", "Xy", "XY")
CAPS = (6, 4)
ZERO = (0, 0, 0, 0)


def invert_integer_matrix(matrix):
    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    rows = [list(map(Fraction, row)) + [Fraction(i == j) for j in range(size)]
            for i, row in enumerate(matrix)]
    for i in range(size):
        pivot = next(j for j in range(i, size) if rows[j][i])
        rows[i], rows[pivot] = rows[pivot], rows[i]
        divisor = rows[i][i]
        rows[i] = [value / divisor for value in rows[i]]
        for j, row in enumerate(rows):
            if j != i:
                factor = row[i]
                rows[j] = [a - factor * b for a, b in zip(row, rows[i])]
    inverse = [[int(value) for value in row[size:]] for row in rows]
    assert all(rows[i][size:] == inverse[i] for i in range(size))
    for left, right in ((matrix, inverse), (inverse, matrix)):
        for i, row in enumerate(left):
            for j, column in enumerate(zip(*right)):
                assert sum(a * b for a, b in zip(row, column)) == (i == j)
    return inverse


def hop_map(graph, letter):
    size = len(graph) // 4
    return bytes(graph[i] if graph[i] >= 0 else size
                 for i in range(letter, len(graph), 4))


def primitive_count_census(graph, alphabet):
    size = len(graph) // 4
    start = ((hop_map(graph, LETTERS.index(alphabet[0])), (1, 0)),
             (hop_map(graph, LETTERS.index(alphabet[1])), (0, 1)))
    states = {start}
    queue = [start]
    mixed = set()
    checksum = sha256()

    for left, right in queue:
        a, a_counts = left
        b, b_counts = right
        for mapping, counts in (left, right):
            if min(counts) >= 2 and any(vertex == target for vertex, target in enumerate(mapping)):
                mixed.add(counts)
        joined = (compose(a, b, size), tuple(
            min(cap, ca + cb) for cap, ca, cb in zip(CAPS, a_counts, b_counts)))
        for successor in ((left, joined), (joined, right)):
            if successor not in states:
                states.add(successor)
                queue.append(successor)
        checksum.update(repr((left, right)).encode())

    for left, right in states:
        mapping = bytes(right[0][v] if v < size else size for v in left[0])
        counts = tuple(min(CAPS[i], left[1][i] + right[1][i]) for i in range(2))
        joined = (mapping, counts)
        assert (left, joined) in states and (joined, right) in states
    return {"alphabet": alphabet, "closed_states": len(states),
            "mixed_counts": sorted(mixed), "state_digest": checksum.hexdigest()}


def plus(left, right):
    return tuple(a + b for a, b in zip(left, right))


def minus(left, right):
    return tuple(a - b for a, b in zip(left, right))


def unary_profiles(graph, weights, single, repeat):
    single_index, repeat_index = map(LETTERS.index, (single, repeat))
    for start in range(len(graph) // 4):
        edge = start * 4 + single_index
        at, value = graph[edge], weights[edge]
        locations = {}
        trace = []
        while at >= 0 and at not in locations:
            locations[at] = len(trace)
            trace.append(value)
            edge = at * 4 + repeat_index
            at, value = graph[edge], plus(value, weights[edge])
        if start not in locations:
            continue
        first_count = locations[start]
        if at >= 0 and first_count >= locations[at]:
            period = len(trace) - locations[at]
            increment = minus(value, trace[locations[at]])
        else:
            period = None
            increment = None
        yield (single, repeat, start, first_count, trace[first_count], period, increment)


def source_case(t, s, mixed_expected, profiles_expected):
    marked = (*START, *conjugated_copies(START, (s, s + t)))
    graph = fold((*marked, t))
    assert tuple(fold_word_arcs((*marked, t))) == graph and len(graph) // 4 == 8
    assert graph == envelope(t + s + t) == envelope(t + s + t.swapcase())
    _, chords, arcs, coordinates = spanning(graph)
    assert len(chords) == len(marked) == 6
    marked_rows = [coordinates(word) for word in marked]
    inverse = invert_integer_matrix(marked_rows)
    edge_weights = [ZERO] * len(graph)
    for (a, label, _), (i, sign) in arcs.items():
        edge_weights[4 * a + label] = tuple(sign * value for value in inverse[i][2:])
    profiles = [
        profile
        for single, repeat in (("x", "y"), ("x", "Y"), ("y", "x"), ("y", "X"))
        for profile in unary_profiles(graph, edge_weights, single, repeat)
    ]
    assert profiles == profiles_expected
    counts = [primitive_count_census(graph, alphabet) for alphabet in ALPHABETS]
    assert [row["mixed_counts"] for row in counts] == [[mixed_expected], [], [], [mixed_expected]]
    return {"first_two_letters": t + s, "core": graph, "marked_generators": marked,
            "marked_chord_rows": marked_rows, "inverse_marking": inverse,
            "quotient_edge_weights": edge_weights, "mixed_primitive_count_census": counts,
            "one_letter_profiles": profiles}


def main():
    p = (1, 0, -1, 0)
    x_special = (1, 0, -1, 1)
    y_special = (1, 0, -1, -1)
    x_case = [
        ("x", "y", 0, 0, p, 4, (3, 0, -3, 0)),
        ("x", "y", 6, 0, x_special, None, None),
        ("x", "Y", 0, 0, p, 4, (-3, 0, 3, 0)),
        ("x", "Y", 6, 0, x_special, None, None),
        ("y", "x", 3, 0, p, 3, (4, 0, -3, 0)),
        ("y", "X", 3, 0, p, 3, (-4, 0, 3, 0)),
    ]
    y_case = [
        ("x", "y", 3, 0, p, 4, (3, 0, -4, 0)),
        ("x", "Y", 3, 0, p, 4, (-3, 0, 4, 0)),
        ("y", "x", 0, 0, p, 3, (4, 0, -4, 0)),
        ("y", "x", 7, 0, y_special, None, None),
        ("y", "X", 0, 0, p, 3, (-4, 0, 4, 0)),
        ("y", "X", 7, 0, y_special, None, None),
    ]
    results = [source_case("x", "y", (5, 3), x_case),
               source_case("y", "x", (2, 3), y_case)]
    print(json.dumps({"source": START, "checked_four_conjugation_schedules": EXPECTED,
                      "prefix_certificates": results}, indent=2))


if __name__ == "__main__":
    main()
