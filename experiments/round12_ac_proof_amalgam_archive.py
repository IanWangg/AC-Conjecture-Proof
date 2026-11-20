"""Exact reciprocal first-stage archive screen for the second energy-20 donor."""

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path

from elementary_verify import inverse, replay
from round03_stable_proof_pivot import reduced as reduce
from round08_ak3_acm_replay import compile_move
from round10_ac_proof_blocks import marked_group, vectors
from round11_ak3_targeted_acm import reverse_suffix
from round12_ak3_frozen_primitives import SECOND_DONOR, SECOND_RECEIVER
from round12_ak3_reciprocal_charts import reverse_index
from stallings_search import graph


# a=u0, b=u1, c=x u0 x^-1, d=x u1 x^-1 in the free kernel.
PHI = ("c", "d", "abA", "aabA")
PSI = ("dC", "cDcdC", "a", "b")
BETA_INV = ("bA", "a")
SEPARATORS = {
    "XXXXYYxxyyyXYYYYxxxxyy": ((2, 3, 4, 5, 6, 7, 8, 9, 1), (1, 9, 7, 2, 6, 5, 8, 4, 3)),
    "XXXXyxxyyxYxxYY": ((2, 3, 4, 5, 1, 7, 8, 9, 10, 6), (2, 3, 6, 10, 7, 4, 1, 5, 8, 9)),
}


def substitute(word, images):
    positive = "abcd"[:len(images)]
    marking = dict(zip(positive + positive.upper(), (*images, *map(inverse, images))))
    return reduce("".join(marking[letter] for letter in word))


@lru_cache(maxsize=None)
def shifted(letter, power):
    if power == 0:
        return letter
    sign = 1 if power > 0 else -1
    return substitute(shifted(letter, power - sign), PHI if sign > 0 else PSI)


@lru_cache(maxsize=None)
def shift_vector(power):
    """phi^power(a) in the appropriate factor's abelianization."""
    factor = power % 2
    v = (1, 0)
    steps = power // 2
    for _ in range(abs(steps)):
        x, y = v
        v = (y, x + y) if steps > 0 else (y - x, x)
    return factor, v


def height(word):
    return word.count("x") - word.count("X") + 2 * (word.count("y") - word.count("Y"))


def kernel_word(word):
    level = 0
    pieces = []
    for letter in word:
        if letter == "x":
            level += 1
        elif letter == "X":
            level -= 1
        elif letter == "y":
            pieces.append(shifted("A", level))
            level += 2
        else:
            level -= 2
            pieces.append(shifted("a", level))
    return reduce("".join(pieces)), level


def vector_push(groups, factor, vector):
    x, y = vector
    if groups and groups[-1][0] == factor:
        _, (a, b) = groups.pop()
        x, y = x + a, y + b
    if x or y:
        groups.append((factor, (x, y)))


def vector_shift(syllable):
    factor, (x, y) = syllable
    return (1, (x, y)) if factor == 0 else (0, (y, x + y))


def vector_kernel(word):
    level = 0
    groups = []
    for letter in word:
        if letter == "x":
            level += 1
        elif letter == "X":
            level -= 1
        elif letter == "y":
            factor, (x, y) = shift_vector(level)
            vector_push(groups, factor, (-x, -y))
            level += 2
        else:
            level -= 2
            vector_push(groups, *shift_vector(level))
    assert level == 1
    while len(groups) > 1 and groups[0][0] != groups[-1][0]:
        vector_push(groups, *vector_shift(groups.pop(0)))
    if len(groups) != 1:
        return None
    return (vector_shift(groups[0]) if groups[0][0] else groups[0])[1]


def fibonacci_index(vector):
    """Find the unique i with vector=2*M^i(1,0), over every integer i."""
    size = sum(map(abs, vector))
    for direction in (1, -1):
        v = (2, 0)
        i = 0
        while sum(map(abs, v)) <= size:
            if v == vector:
                return i
            x, y = v
            v = (y, x + y) if direction > 0 else (y - x, x)
            i += direction
    return None


def free_syllables(word):
    groups = []
    current = ""
    last_factor = None
    for letter in word:
        factor = int(letter.lower() in "cd")
        if last_factor != factor:
            if current:
                groups.append(current)
            current = letter
            last_factor = factor
        else:
            current += letter
    if current:
        groups.append(current)
    return groups


def factor(word):
    return int(word[0].lower() in "cd")


def cyclic_kernel(kernel):
    groups = free_syllables(kernel)
    while len(groups) > 1 and factor(groups[0]) != factor(groups[-1]):
        moved = substitute(groups.pop(0), PHI)
        middle = reduce(groups.pop() + moved)
        if middle:
            groups.append(middle)
    if len(groups) != 1:
        return None
    single = groups[0]
    return substitute(single, PHI) if factor(single) else single


def check(word, coefficient):
    delta = height(word)
    if abs(delta) != 1:
        return "wrong_height", None
    oriented = word if delta == 1 else inverse(word)
    projected = vector_kernel(oriented)
    if projected is None:
        return "wrong_homology_syllable_count", None
    index = fibonacci_index(projected)
    if index is None:
        return "outside_fibonacci_orbit", None
    marked, power = kernel_word(oriented)
    assert power == 1
    actual = cyclic_kernel(marked)
    expected = substitute(coefficient, tuple(shifted(letter, 2 * (index + 3)) for letter in "ab"))
    details = {"orientation": delta, "fibonacci_index": index, "conjugator_power_of_x_squared": index + 3,
               "normalized_fiber_coefficient": actual, "required_fiber_coefficient": expected}
    if actual == expected:
        return "conjugate", details
    return "wrong_free_word", details


def reciprocal_checks(hits, index, archives, certificates):
    assert {row["reverse_donor"] for row in hits} == set(SEPARATORS)
    results = []
    for number, row in enumerate(hits, 1):
        donor = row["reverse_donor"]
        x, y = SEPARATORS[donor]
        image, identity, _, inv, cycle_type = marked_group("symmetric", len(x), x, y)
        assert image(donor) == identity
        want = cycle_type(image(SECOND_DONOR))
        assert want == cycle_type(inv(image(SECOND_DONOR)))
        prefix, _ = compile_move((SECOND_DONOR, SECOND_RECEIVER), 1, donor, 1)
        if certificates is not None:
            path = certificates / f"round12_ac_proof_amalgam_forward{number}.json"
            path.write_text(json.dumps(prefix, separators=(",", ":")) + "\n")
        contacts = []
        for word in row["reverse_receivers"]:
            got = cycle_type(image(word))
            assert got != want and got == cycle_type(inv(image(word)))
            provenance = index[donor][word]
            entry = {"receiver": word, "cycle_type": got, "archive_source": provenance}
            if archives is not None:
                endpoint, suffix = reverse_suffix(provenance, archives)
                tail = {"format": prefix["format"], "start": list(endpoint),
                        "target": ["x", "y"], "moves": suffix}
                entry["ordinary_basis_suffix"] = replay(tail)
            contacts.append(entry)
        results.append({"donor": donor, "permutation_marking": {"x": x, "y": y},
                        "forward_replay": replay(prefix), "source_donor_cycle_type": want,
                        "excluded_reciprocal_contacts": contacts})
    return results


def other_frozen_primitive():
    """Finite PSL(2,11) certificate for both infinite primitive slope tails."""
    p = 11
    identity, neg_identity = (1, 0, 0, 1), (p - 1, 0, 0, p - 1)
    x, y = (0, 10, 1, 1), (0, 2, 5, 4)

    def multiply(left, right):
        a, b, c, d = left
        e, f, g, h = right
        return ((a * e + b * g) % p, (a * f + b * h) % p,
                (c * e + d * g) % p, (c * f + d * h) % p)

    def invert(matrix):
        a, b, c, d = matrix
        assert (a * d - b * c) % p == 1
        return d, -b % p, -c % p, a

    images = dict(zip("xXyY", (x, invert(x), y, invert(y))))

    def image(word):
        value = identity
        for letter in word:
            value = multiply(value, images[letter])
        return value

    def squared_trace(matrix):
        return (matrix[0] + matrix[3]) ** 2 % p

    assert vectors(SECOND_DONOR) == (2, -1) and vectors(SECOND_RECEIVER) == (5, -2)
    assert image(SECOND_RECEIVER) == neg_identity
    fixed = squared_trace(image(SECOND_DONOR))
    records = []
    for initial, period, base in (("xxY", "xxYxxYx", (2, -1)), ("xxxY", "xxxYxxY", (3, -1))):
        assert vectors(initial) == base and vectors(period) == (5, -2)
        assert graph((initial, period))[1] == 1
        power, traces = identity, []
        while True:
            candidate = multiply(image(initial), power)
            trace = squared_trace(candidate)
            assert trace == squared_trace(invert(candidate)) and trace != fixed
            traces.append(trace)
            power = multiply(power, image(period))
            if power in (identity, neg_identity):
                break
        records.append({"initial": initial, "period": period, "projective_order": len(traces),
                        "squared_trace_residues": traces})
    return {"prime": p, "x": x, "y": y, "frozen_word": SECOND_RECEIVER,
            "frozen_image": image(SECOND_RECEIVER), "receiver": SECOND_DONOR,
            "receiver_image": image(SECOND_DONOR), "receiver_squared_trace": fixed, "tails": records}


def run(archive, archives, certificates):
    cap = 56
    for letter in "abcdABCD":
        assert substitute(substitute(letter, PHI), PSI) == letter
        assert substitute(substitute(letter, PSI), PHI) == letter
    assert kernel_word(SECOND_DONOR) == ("", 0)
    u_minus3 = "a"
    for _ in range(3):
        u_minus3 = substitute(u_minus3, BETA_INV)
    coeff = reduce(u_minus3 * 2)
    assert check(SECOND_RECEIVER, coeff)[0] == "conjugate"
    # Independently generated marked conjugates and inserted donor products.
    controls = []
    for w in ("x", "y", "xyXXy", "XXYxy"):
        value = reduce(w + SECOND_RECEIVER + inverse(w) + SECOND_DONOR)
        assert check(value, coeff)[0] == "conjugate"
        controls.append(value)
    assert check("x", coeff)[0] != "conjugate"
    assert check("xxxY", coeff)[0] != "conjugate"
    index, source_count = reverse_index(archive, cap)
    counts = Counter()
    hits = []
    last_cases = []
    for donor, sources in sorted(index.items()):
        status, fields = check(donor, coeff)
        counts[status] += 1
        if status == "conjugate":
            hits.append({"reverse_donor": donor, "reverse_receivers": sorted(sources), **fields})
        elif status == "wrong_free_word":
            last_cases.append({"reverse_donor": donor, **fields})
    return {"fixed_donor": SECOND_DONOR, "receiver": SECOND_RECEIVER, "required_coefficient": coeff,
            "reverse_source_pairs": source_count, "reverse_donors": len(index), "reverse_energy": cap,
            "reverse_tsv_sha256": sha256(archive.read_bytes()).hexdigest(), "counts": dict(counts),
            "exact_conjugacy_hits": hits, "wrong_free_word_cases": last_cases, "positive_controls": controls,
            "reciprocal_checks": reciprocal_checks(hits, index, archives, certificates),
            "other_frozen_primitive_exclusion": other_frozen_primitive()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--archives", type=Path)
    parser.add_argument("--certificates", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.archive, args.archives, args.certificates), indent=2))
