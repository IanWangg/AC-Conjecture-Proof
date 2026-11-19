"""Test the infinite-cyclic-cover obstruction for rank-three two-row blocks."""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

from round03_stable_proof_pivot import canonical, exponent
from round04_stable_proof_seeds import orbit
from stallings_search import inverse


def cyclic_weights(pair):
    (a, b, c), (d, e, f) = map(exponent, pair)
    return (b * f - c * e, c * d - a * f, a * e - b * d)


def fox_images(word, weights):
    images = [Counter() for _ in weights]
    height = 0
    for letter in word:
        at = "xyz".index(letter.lower())
        step = weights[at]
        if letter.islower():
            images[at][height] += 1
            height += step
        else:
            height -= step
            images[at][height] -= 1
    assert height == 0
    return [dict((i, n) for i, n in image.items() if n) for image in images]


def cyclic_cover_obstruction(pair):
    weights = cyclic_weights(pair)
    omit = min((j for j, n in enumerate(weights) if n), key=lambda j: abs(weights[j]))
    i, j = [a for a in range(3) if a != omit]
    left, right = [fox_images(word, weights) for word in pair]
    determinant = Counter()
    for sign, first, second in ((1, left[i], right[j]), (-1, left[j], right[i])):
        for a, u in first.items():
            for b, v in second.items():
                determinant[a + b] += sign * u * v
    support = sorted((k, v) for k, v in determinant.items() if v)
    required = abs(weights[omit])
    nonunit = len(support) != required
    if not nonunit:
        first, coeff = support[0]
        nonunit = abs(coeff) != 1 or any(entry != (first + k, coeff)
                                          for k, entry in enumerate(support))
    return nonunit, weights, omit, support


def scan(path: Path, pivotless_only: bool = False):
    blocks = {}
    count = 0
    for line in path.open():
        triple = tuple(line.split())
        if pivotless_only and any(w.count("z") + w.count("Z") == 1 for w in triple):
            continue
        count += 1
        for pair in combinations(triple, 2):
            blocks.setdefault(pair, triple)

    surviving = []
    for pair, triple in sorted(blocks.items()):
        obstructed, weights, omit, support = cyclic_cover_obstruction(pair)
        if not obstructed:
            surviving.append(dict(pair=pair, triple=triple, weights=weights,
                                  omitted_column=omit, determinant=support))
    return dict(considered_triples=count, distinct_blocks=len(blocks),
                excluded_by_cyclic_cover=len(blocks) - len(surviving),
                candidates=surviving)


def check_remaining(candidates):
    counts = Counter(min(orbit(row["pair"])) for row in candidates)
    witnesses = {
        ("XXXXYYY", "XYZYXyxz"): ((4, 3, 2, 1, 0), (0, 1, 3, 4, 2), (0, 2, 4, 3, 1)),
        ("XXXXYYY", "XYZyxYXz"): ((4, 3, 2, 1, 0), (0, 1, 3, 4, 2), (0, 4, 1, 3, 2)),
        ("XXXYZXzxY", "XYxYXy"): ((4, 3, 1, 0, 2), (1, 3, 0, 4, 2), (0, 2, 1, 4, 3)),
        ("XXXYZZZ", "XXYxyXZYZ"): ((4, 3, 2, 0, 1), (0, 3, 2, 4, 1), (4, 3, 1, 2, 0)),
    }
    hnn = ("XXYZYXz", "XYxYXy")
    assert set(counts) == {*witnesses, hnn}
    result = []
    identity = tuple(range(5))

    def multiply(p, q):
        return tuple(p[i] for i in q)

    for pair, images in witnesses.items():
        assert all(set(p) == set(identity) for p in images)
        assert any(multiply(p, q) != multiply(q, p) for p, q in combinations(images, 2))
        marks = dict(zip("xyz", images))
        marks.update({a.upper(): tuple(p.index(i) for i in identity)
                      for a, p in list(marks.items())})
        for word in pair:
            value = identity
            for letter in word:
                value = multiply(value, marks[letter])
            assert value == identity
        result.append(dict(pair=pair, count=counts[pair], nonabelian_S5_images=images))

    relation, braid = hnn
    assert canonical(braid.translate(str.maketrans("yY", "Yy"))) == canonical("xyxYXY")
    a, b = inverse("xy"), "yxx"
    assert relation == inverse(b) + "Z" + a + "z"
    assert sum(n * w for n, w in zip(exponent(braid), (1, -1, 0))) == 0
    assert sum(n * w for n, w in zip(exponent(b), (1, -1, 0))) == 1

    def mm(p, q):
        return tuple(sum(p[2 * i + k] * q[2 * k + j] for k in range(2))
                     for i, j in ((0, 0), (0, 1), (1, 0), (1, 1)))

    x, y = (1, 1, 0, 1), (1, 0, 1, 1)
    marked = {"x": x, "X": (1, -1, 0, 1), "y": y, "Y": (1, 0, -1, 1)}
    value = (1, 0, 0, 1)
    for letter in braid:
        value = mm(value, marked[letter])
    assert value == (1, 0, 0, 1) and mm(x, y) != mm(y, x)
    trace = mm(x, y)[0] + mm(x, y)[3]
    assert trace == 3
    result.append(dict(pair=hnn, count=counts[hnn], base="B_3",
                       associated_cycle_generators=[a, b], trace_xy=trace,
                       abelianized_exponent_of_yxx=1))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("states", type=Path)
    parser.add_argument("--pivotless-only", action="store_true")
    parser.add_argument("--with-witnesses", action="store_true")
    args = parser.parse_args()
    result = scan(args.states, args.pivotless_only)
    if args.with_witnesses:
        result["remaining_block_witnesses"] = check_remaining(result.pop("candidates"))
    print(json.dumps(result, indent=2))
