"""Audit a cyclic rank-three excursion using the certified rank-two catalogue."""

import argparse
import hashlib
import json
from collections import Counter, deque
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path

from planar_link_parity import decide as parity_decide
from round01_geometric_archive import check_whitehead_cuts, minimal_pair
from verify_link_parity import verify_certificate


def reduced(word):
    out = []
    for letter in word:
        if out and letter == out[-1].swapcase():
            out.pop()
        else:
            out.append(letter)
    return "".join(out)


def cyclic(word):
    word = reduced(word)
    a, b = 0, len(word)
    while b > a + 1 and word[a] == word[b - 1].swapcase():
        a += 1
        b -= 1
    return word[a:b]


@lru_cache(maxsize=160_000)
def rotations(word):
    inverse = word[::-1].swapcase()
    return tuple(sorted({w[i:] + w[:i] for w in (word, inverse) for i in range(len(w))}))


def canonical(word):
    word = cyclic(word)
    return rotations(word)[0] if word else ""


def erase(word):
    return canonical(word.replace("z", "").replace("Z", ""))


def one_occurrence_projections(rows):
    for slot, word in enumerate(rows):
        pivot = [i for i, a in enumerate(word) if a.lower() == "z"]
        if len(pivot) != 1:
            continue
        i = pivot[0]
        augment = word[i + 1:] + word[:i]
        image = augment[::-1].swapcase() if word[i] == "z" else augment
        inverse = image[::-1].swapcase()
        yield tuple(sorted(
            canonical("".join(image if a == "z" else inverse if a == "Z" else a for a in other))
            for j, other in enumerate(rows) if j != slot
        ))


@lru_cache(maxsize=None)
def xy_expansions(word, pairs):
    """Undo cyclic cancellations before inserting the erased letters."""
    words = {word}
    for _ in range(pairs):
        words = {
            rotations(w[:i] + a + a.swapcase() + w[i:])[0]
            for w in words
            for i in range(len(w))
            for a in "xXyY"
        }
    return tuple(sorted(words))


@lru_cache(maxsize=None)
def lifts(word, degree):
    """Enumerate cyclic words of length len(word)+degree over this projection."""
    assert degree >= 0 and word
    if not degree:
        return (word,)
    candidates = set()
    width = len(word) + degree
    for deleted in range(degree, 0, -2):
        for raw in xy_expansions(word, (degree - deleted) // 2):
            for positions in combinations(range(width), deleted):
                for signs in product("zZ", repeat=deleted):
                    inserted = dict(zip(positions, signs))
                    original = iter(raw)
                    lift = "".join(
                        inserted[i] if i in inserted else next(original) for i in range(width)
                    )
                    key = canonical(lift)
                    if len(key) == width:
                        assert erase(key) == word
                        candidates.add(key)
    return tuple(sorted(candidates))


def exponent(word):
    return [word.count(a) - word.count(a.upper()) for a in "xyz"]


def det(rows):
    (a, b, c), (d, e, f), (g, h, i) = map(exponent, rows)
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


@lru_cache(maxsize=None)
def tails(bound):
    words = [""]
    layer = [""]
    for _ in range(bound):
        layer = [
            word + letter
            for word in layer
            for letter in "xXyYzZ"
            if not word or letter != word[-1].swapcase()
        ]
        words.extend(layer)
    return [(w, w[::-1].swapcase()) for w in words]


def neighbors(rows, cap):
    energy = sum(map(len, rows))
    menu_size = 0
    allowed = set()
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            bound = max(0, (cap - energy - len(rows[j])) // 2)
            allowance = cap - energy + len(rows[i])
            for a, b, (tail, inverse) in product(
                rotations(rows[i]), rotations(rows[j]), tails(bound)
            ):
                menu_size += 1
                word = cyclic(a + tail + b + inverse)
                if len(word) <= allowance:
                    changed = list(rows)
                    changed[i] = canonical(word)
                    allowed.add(tuple(sorted(changed)))
    return allowed, menu_size


def read_catalogue(path, cap):
    digest = hashlib.sha256()
    low = set()
    weighted = Counter()
    boundary_pairs = set()
    count = 0
    with path.open("rb") as stream:
        for raw in stream:
            digest.update(raw)
            first, second = raw.decode("ascii").split()
            count += 1
            if len(first) + len(second) <= cap - 1:
                low.add((first, second))
            for old, other in ((first, second), (second, first)):
                weight = 2 * len(old) + len(other) + 1
                if weight <= cap:
                    weighted[weight] += 1
                    boundary_pairs.add((old, other))
    assert count == 5_562_224
    assert digest.hexdigest() == "acb60bac212c4d14ecbdfc251e87d35f191676b0321bc446d4d6928587ae1978"
    assert min(weighted, default=20) == 20
    return low, boundary_pairs, dict(sorted(weighted.items())), digest.hexdigest()


def first_exits(boundary_pairs, cap):
    seeds = set()
    source_count = 0
    for donor, other in boundary_pairs:
        slack = cap - 2 * len(donor) - len(other)
        assert slack >= 1
        for donor_degree in range(slack + 1):
            for other_degree in range(slack - donor_degree + 1):
                if donor_degree == 0 and donor_degree + other_degree == slack:
                    # A z-free donor requires the new row to supply at least
                    # one added z-letter, by the z-exponent sum.
                    continue
                for old_donor, old_other in product(
                    lifts(donor, donor_degree), lifts(other, other_degree)
                ):
                    energy = 1 + len(old_donor) + len(old_other)
                    if energy > cap:
                        continue
                    source_count += 1
                    bound = max(0, (cap - energy - len(old_donor)) // 2)
                    for sign, rotation, (tail, inverse) in product(
                        "zZ", rotations(old_donor), tails(bound)
                    ):
                        word = cyclic(sign + tail + rotation + inverse)
                        if len(word) + energy - 1 <= cap:
                            rows = tuple(sorted((canonical(word), old_donor, old_other)))
                            assert abs(det(rows)) == 1 and "Z" not in rows
                            seeds.add(rows)
    return seeds, source_count


def test(path, cap):
    low, pairs, from_counts, digest = read_catalogue(path, cap)
    seeds, boundary_sources = first_exits(pairs, cap)
    queue = deque(sorted(seeds))
    seen = set(seeds)
    reentries = set()
    pivot_projections = set()
    missing_pivot = 0
    two_pivots = 0
    pivot_free_rank_two = set()
    pivot_free_with_z = set()
    lost = set()
    checks = 0
    while queue:
        rows = queue.popleft()
        assert abs(det(rows)) == 1
        projected = list(one_occurrence_projections(rows))
        pivot_projections.update(projected)
        missing_pivot += not projected
        two_pivots += len(projected) >= 2
        if not projected:
            lost.add(rows)
        if len(projected) == 1:
            nonpivots = tuple(w for w in rows if w.count("z") + w.count("Z") != 1)
            if any("z" in w.lower() for w in nonpivots):
                pivot_free_with_z.add(nonpivots)
            else:
                pivot_free_rank_two.add(nonpivots)
        successors, checked = neighbors(rows, cap)
        checks += checked
        for target in sorted(successors):
            if "Z" in target:
                reentries.add(tuple(sorted(erase(w) for w in target if w != "Z")))
            elif target not in seen:
                queue.append(target)
                seen.add(target)
    unknown = reentries - low
    unknown_pivots = pivot_projections - low
    minimal_nonpivots = {minimal_pair(pair) for pair in pivot_free_rank_two}
    obstructed = 0
    for pair in minimal_nonpivots:
        check_whitehead_cuts(pair)
        certificate = parity_decide(pair)
        if certificate["status"] == "PARITY_OBSTRUCTION":
            verify_certificate(certificate)
            obstructed += 1
    return {
        "cap": cap,
        "rank_two_catalogue_sha256": digest,
        "rank_two_pairs_of_length_at_most_cap_minus_one": len(low),
        "boundary_projected_ordered_pairs_by_weight": from_counts,
        "first_exit_source_lifts_examined": boundary_sources,
        "first_exit_overapproximation": len(seeds),
        "non_z_states_examined": len(seen),
        "product_candidates_examined": checks,
        "reentry_projections": len(reentries),
        "reentry_projections_outside_certified_component": sorted(unknown),
        "minimum_row_length_without_z_singleton": min(
            (min(map(len, rows)) for rows in seen), default=None
        ),
        "one_occurrence_pivot_projection_pairs": len(pivot_projections),
        "one_occurrence_projections_not_certified_at_length_cap_minus_one": len(unknown_pivots),
        "states_with_at_least_two_one_occurrence_pivots": two_pivots,
        "states_without_a_one_occurrence_pivot": missing_pivot,
        "example_without_a_one_occurrence_pivot": min(lost, default=None),
        "distinct_rank_two_blocks_omitting_the_only_pivot": len(pivot_free_rank_two),
        "whitehead_minimized_block_keys": len(minimal_nonpivots),
        "minimized_block_keys_with_verified_parity_obstruction": obstructed,
        "omitting_the_only_pivot_but_still_using_z": len(pivot_free_with_z),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalogue", type=Path)
    parser.add_argument("caps", type=int, nargs="+", choices=(19, 20, 21, 22, 23))
    args = parser.parse_args()
    result = [test(args.catalogue, cap) for cap in args.caps]
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
