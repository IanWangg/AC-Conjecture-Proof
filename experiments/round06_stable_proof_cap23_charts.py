"""Search the existing cap-23 prefix for primitive and geometric projections."""

import argparse
from collections import Counter
from functools import cache
from hashlib import sha256
import json
from pathlib import Path

from elementary_verify import inverse
from euclidean_primitive_audit import primitive_cyclic_word
from round05_ak3_orbit_audit import MAPS, rotations
from round05_stable_proof_projections import each_available_chart, geometry_screen, rank_two_orbit

ENCODE = str.maketrans("xXyY", "0123")
DECODE = str.maketrans("0123", "xXyY")


@cache
def word_images(word):
    images = []
    for transform in MAPS:
        w = word.translate(transform)
        images.append(min(min(rotations(w.translate(ENCODE))), min(rotations(inverse(w).translate(ENCODE)))))
    return tuple(images)


def compact_row(pair):
    key = min(tuple(sorted(image, key=lambda word: (len(word), word)))
              for image in zip(*(word_images(word) for word in pair)))
    return ("\t".join(word.translate(DECODE) for word in key) + "\n").encode("ascii")


def screen(path, cap29, reverse, basis_index_tsv=None):
    digest = sha256()
    counts = Counter()
    sources = {}
    with path.open("rb") as stream:
        for raw in stream:
            digest.update(raw)
            counts["input_states"] += 1
            # A short old-letter row may give an immediate free pivot.
            rows = tuple(raw.decode("ascii").split())
            no_z = all(word.lower().count("z") != 1 for word in rows)
            short = any(len(word) <= 2 and "z" not in word.lower() for word in rows)
            if not (no_z or short):
                continue
            counts["screened_states"] += 1
            counts["states_without_fixed_z_chart"] += no_z
            counts["states_with_short_z_free_row"] += short
            for pair, details in each_available_chart(rows):
                counts[details["chart"] + "_charts"] += 1
                key = min(rank_two_orbit(pair))
                sources.setdefault(key, {"rank_three_rows": rows, "projected_pair": pair, **details})

    reverse_pairs = {min(rank_two_orbit(tuple(line.split()))) for line in reverse.open()}
    signatures = {compact_row(pair): pair for pair in sources}
    assert len(signatures) == len(sources)
    with cap29.open("rb") as stream:
        hits = {signatures[line] for line in stream if line in signatures}
    absent = sorted(sources.keys() - hits, key=lambda pair: (sum(map(len, pair)), pair))
    return {
        "counts": dict(counts),
        "input_sha256": digest.hexdigest(),
        "distinct_projection_orbits": len(sources),
        "projection_hits_cap29": len(hits),
        "projection_primitive_examples": [sources[pair] for pair in sorted(sources)
                                           if any(primitive_cyclic_word(word) for word in pair)],
        "reverse_pair_hits": [sources[pair] for pair in sorted(sources.keys() & reverse_pairs)],
        "shortest_pairs_absent_from_cap29": [sources[pair] for pair in absent[:8]],
        "geometry": geometry_screen(sources, basis_index_tsv),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prefix_states", type=Path)
    parser.add_argument("compact_cap29", type=Path)
    parser.add_argument("reverse", type=Path)
    parser.add_argument("--basis-index-tsv", type=Path)
    args = parser.parse_args()
    print(json.dumps(screen(args.prefix_states, args.compact_cap29, args.reverse, args.basis_index_tsv), indent=2))
