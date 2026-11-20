"""Generate exact single-generator tests of the once-stabilized orbit."""

import argparse
import hashlib
import json
from pathlib import Path

from stallings_search import cyclic, inverse

ALPHABET = "xXyYzZ"


def reduced_words(limit):
    layer = [""]
    for _ in range(limit):
        layer = [word + letter for word in layer for letter in ALPHABET
                 if not word or word[-1] != letter.swapcase()]
        yield from layer


def substitutions(limit):
    for target in "xyz":
        for word in reduced_words(limit):
            if word.count(target) < 2 or word.count(target) - word.count(target.upper()) != 1:
                continue
            yield target, word, str.maketrans({target: word, target.upper(): inverse(word)})


def generate(source, output, maximum):
    menu = list(substitutions(maximum))
    read_digest = hashlib.sha256()
    write_digest = hashlib.sha256()
    rows = 0
    maximum_energy = maximum_coordinate = 0
    with source.open("rb") as values, output.open("wb") as derived:
        for raw in values:
            read_digest.update(raw)
            triple = raw.decode("ascii").split()[:3]
            if len(triple) != 3:
                raise ValueError("a source row needs three coordinates")
            rows += 1
            for _, _, marking in menu:
                image = tuple(cyclic(word.translate(marking)) for word in triple)
                assert all(image)
                maximum_coordinate = max(maximum_coordinate, *map(len, image))
                maximum_energy = max(maximum_energy, sum(map(len, image)))
                line = ("\t".join(image) + "\n").encode("ascii")
                derived.write(line)
                write_digest.update(line)
    return {"source_tuples": rows, "substitution_word_limit": maximum,
            "substitutions": len(menu), "candidate_tuples": rows * len(menu),
            "maximum_candidate_coordinate_length": maximum_coordinate,
            "maximum_candidate_energy": maximum_energy,
            "source_sha256": read_digest.hexdigest(), "candidate_sha256": write_digest.hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--maximum", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(generate(args.source, args.output, args.maximum), indent=2))


if __name__ == "__main__":
    main()
