"""Test one cyclic product after small nonautomorphic substitutions."""

from functools import cache
from itertools import product
import json

from euclidean_primitive_audit import primitive_cyclic_word
from round03_stable_proof_pivot import canonical, cyclic, rotations
from round10_stable_proof_wirtinger import PUBLISHED_PAIR, START, frozen_repair
from stallings_search import inverse, reduce


primitive = cache(primitive_cyclic_word)


def substitutions():
    for letters in product("xXyY", repeat=5):
        word = "".join(letters)
        if reduce(word) != word or primitive(cyclic(word)):
            continue
        for letter in "xy":
            if (word.lower().count(letter) == 3
                and abs(word.count(letter) - word.count(letter.upper())) == 1):
                yield letter, word


def replace(row, letter, image):
    back = inverse(image)
    return canonical("".join(image if x == letter else back if x == letter.upper() else x for x in row))


def screen(rows, replacements):
    images = {}
    for a, word in replacements:
        child = tuple(replace(row, a, word) for row in rows)
        images.setdefault(child, (a, word))
    candidates = 0
    positive = []
    for (u, v), substitution in images.items():
        for p, q in product(rotations(u), rotations(v)):
            candidates += 1
            candidate = cyclic(p + q)
            if primitive(candidate):
                positive.append(dict(image_pair=(u, v), replacement=substitution,
                                     rotations=(p, q), primitive=candidate))
                break
    return dict(distinct_ordered_cyclic_image_pairs=len(images),
                zero_bridge_rotation_products_tested=candidates, positive=positive)


if __name__ == "__main__":
    wrong, _ = frozen_repair()["wrong_and_corrected_rank_two_pairs"]
    replacements = tuple(substitutions())
    cases = {"AK3": START[:2], "published_length25": PUBLISHED_PAIR, "wrong_W_chart": wrong}
    print(json.dumps(dict(nonprimitive_images_of_self_exponent_one=len(replacements),
                          cases={label: screen(rows, replacements) for label, rows in cases.items()}),
                     indent=2))
