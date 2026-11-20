"""Reduce five literal conjugations by exact marked subgroup tests."""

from collections import Counter
from functools import lru_cache
from itertools import product
import json

from primitive_map_pairs import LETTERS, inverse, reduce
from round06_stable_disproof_conjugations import START
from round17_ac_disproof_three_phases import conjugated_copies
from round19_ac_disproof_four_conjugations import (
    ROSE, SOURCE, complete, free_block, primitive_test,
)
from v_vertex_identification import spanning


@lru_cache(None)
def envelope(sequence):
    if not sequence:
        return SOURCE
    return free_block(envelope(sequence[:-1]), "", sequence[-1])


def marked_incidence_excluded(sequence):
    """R20 obstruction on reaching two primitives with unimodular slopes."""
    return (sequence[:2] in ("xy", "yx") and len(sequence) >= 3
            and all(letter.lower() == sequence[0] for letter in sequence[2:]))


def binary_vector(coordinates):
    return sum((coefficient % 2) << i for i, coefficient in enumerate(coordinates))


@lru_cache(None)
def primitive_incidence(core):
    _, chords, arcs, coordinates = spanning(core)
    vertex_scale = 1 << len(chords)
    voltage_mask = vertex_scale - 1
    weights = {(vertex, letter): 1 << index
               for (vertex, letter, _), (index, _) in arcs.items()}

    def generator_map(letter):
        return tuple(target * vertex_scale + weights.get((start, letter), 0)
                     if target >= 0 else -1
                     for start, target in enumerate(core[letter::4]))

    def append(first, second):
        def hop(encoded):
            if encoded < 0:
                return -1
            vertex, weight = divmod(encoded, vertex_scale)
            return second[vertex] ^ weight if second[vertex] >= 0 else -1
        return tuple(map(hop, first))

    signatures = set()
    counts = {}
    for alphabet in ("xy", "xY", "Xy", "XY"):
        x, y = map(LETTERS.index, alphabet)
        initial = ((generator_map(x), 1), (generator_map(y), 2))
        queue = [initial]
        seen = {initial}
        for left, right in queue:
            for mapping, slope in (left, right):
                signatures.update((encoded & voltage_mask, slope)
                                  for vertex, encoded in enumerate(mapping)
                                  if encoded >= 0 and encoded // vertex_scale == vertex)
            combined = (append(left[0], right[0]), left[1] ^ right[1])
            for successor in ((left, combined), (combined, right)):
                if successor not in seen:
                    seen.add(successor)
                    queue.append(successor)
        counts[alphabet] = len(seen)
    return signatures, counts, coordinates


@lru_cache(None)
def source_incidence(sequence):
    core = envelope(sequence)
    signatures, counts, coordinates = primitive_incidence(core)
    variants = [""]
    for letter in sequence[1:]:
        variants += [reduce(letter + word) for word in variants]

    def rows(first_letter):
        return [tuple(binary_vector(coordinates(word)) for word in
                      conjugated_copies(START, (reduce(variant + first_letter),)))
                for variant in variants]

    stationary, receiver = rows(""), rows(sequence[0])
    cases = []
    for u, v in product((1, 2, 3), repeat=2):
        if u == v:
            continue
        space = {0}
        for axis, pairs in ((u, stationary), (v, receiver)):
            for p, b in pairs:
                row = (p if axis & 1 else 0) ^ (b if axis & 2 else 0)
                if row not in space:
                    space.update({previous ^ row for previous in space})
        slopes = sorted({slope for voltage, slope in signatures if voltage in space})
        cases.append({"source_row_parities": (u, v), "subspace_size": len(space),
                      "compatible_primitive_slope_parities": slopes})
    return {"prefix": sequence, "vertices": len(core) // 4, "closed_map_pair_states": counts,
            "pairs_of_source_parities": cases}


@lru_cache(None)
def last_pair_possible(core, relative):
    if core == ROSE:
        return True
    if free_block(core, "", relative) != ROSE or not primitive_test(core)[0]:
        return False
    return all(complete(core, direction)["completing_word"] is not None
               for direction in (relative, inverse(relative)))


def blocks_of(sequence, mask):
    blocks = [sequence[0]]
    for mark, letter in zip(mask, sequence[1:]):
        if mark == "1":
            blocks.append(letter)
        else:
            blocks[-1] += letter
    return blocks


@lru_cache(None)
def transports(block):
    counts = Counter()
    for receivers in product((0, 1), repeat=len(block)):
        pair = ["", ""]
        for letter, index in zip(block, receivers):
            pair[index] = reduce(letter + pair[index])
        if sum(map(len, pair)) == len(block):
            counts[tuple(pair)] += 1
    return tuple(counts.items())


def possible_assignments(sequence, mask):
    if mask[-1] == "0":
        return 0
    blocks = blocks_of(sequence, mask)
    groups = {SOURCE: 1}
    for block in blocks[:-1]:
        advanced = Counter()
        for core, paths in groups.items():
            for pair, multiplicity in transports(block):
                advanced[free_block(core, *pair)] += paths * multiplicity
        groups = advanced
    return sum(paths * multiplicity
               for core, paths in groups.items()
               for (a, b), multiplicity in transports(blocks[-1])
               if last_pair_possible(core, reduce(inverse(a) + b)))


def coarse_status(sequence):
    if envelope(sequence) != ROSE:
        return "final_envelope_proper"
    prefix = envelope(sequence[:-1])
    if not primitive_test(prefix)[0]:
        return "prefinal_envelope_primitive_free"
    if prefix == ROSE:
        return "prefinal_envelope_rose"
    if not last_pair_possible(prefix, sequence[-1]):
        return "necessary_directional_test_failed"
    if marked_incidence_excluded(sequence[:-1]):
        return "marked_source_incidence_exclusion"
    provenance = source_incidence(sequence[:-1])
    if all(len(row["compatible_primitive_slope_parities"]) <= 1
           for row in provenance["pairs_of_source_parities"]):
        return "binary_source_incidence_exclusion"
    return "proper_prefinal_envelope_passes"


def main():
    statuses = Counter()
    mask_census = Counter()
    surviving = []
    no_mask = []
    binary_cases = {}
    masks = tuple("".join(bits) for bits in product("01", repeat=4))
    for letters in product(LETTERS, repeat=5):
        sequence = "".join(letters)
        status = coarse_status(sequence)
        statuses[status] += 1
        if status in ("binary_source_incidence_exclusion", "proper_prefinal_envelope_passes"):
            binary_cases[sequence[:-1]] = source_incidence(sequence[:-1])
        if status not in ("prefinal_envelope_rose", "proper_prefinal_envelope_passes"):
            continue
        counts = {mask: count for mask in masks
                  if (count := possible_assignments(sequence, mask))}
        if counts:
            mask_census.update(counts.keys())
            surviving.append({"sequence": sequence, "status": status, "receiver_assignments": counts})
        else:
            no_mask.append(sequence)
    assert statuses == {"final_envelope_proper": 312, "prefinal_envelope_primitive_free": 292,
                        "prefinal_envelope_rose": 368, "marked_source_incidence_exclusion": 16,
                        "binary_source_incidence_exclusion": 8, "proper_prefinal_envelope_passes": 28}
    assert len(binary_cases) == 18
    print(json.dumps({
        "source": START, "coarse_counts": dict(statuses), "excluded_after_gap_tests": no_mask,
        "surviving_schedule_count": len(surviving),
        "schedules_by_allowed_mask": dict(sorted(mask_census.items())),
        "minimum_nonempty_gaps": min(mask.count("1") for mask in mask_census),
        "proper_prefinal_binary_cases": list(binary_cases.values()),
        "surviving_schedules": surviving,
    }, indent=2))


if __name__ == "__main__":
    main()
