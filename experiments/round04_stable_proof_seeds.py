"""Generate certified singleton exit seeds or audit all short pivots in a scan."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from euclidean_primitive_audit import primitive_cyclic_word
from round03_stable_proof_pivot import canonical, first_exits

CAP_HASH = {
    21: "6ed07aa9a47059516cac8cf2bac255684c5a2d63437c17d321ba4cf510be6894",
    22: "cd9ba5781a1efcb1bf1b8a72c9a392b79de1cd915da6a520b8f33a4390787fa3",
    26: "3bce0c9dbd0791990a97230f451f1f068d4d648f8bcf58d156a1861785ea1893",
}


def signed_actions():
    for swap, inv_x, inv_y, inv_z in product((False, True), repeat=4):
        x, y = ("y", "x") if swap else ("x", "y")
        x = x.upper() if inv_x else x
        y = y.upper() if inv_y else y
        z = "Z" if inv_z else "z"
        yield str.maketrans("xXyYzZ", "".join(c + c.swapcase() for c in (x, y, z)))


def orbit(words):
    return {tuple(sorted(canonical(w.translate(action)) for w in words))
            for action in signed_actions()}


def prepare(path, cap, output):
    raw = path.read_bytes()
    hash_value = sha256(raw).hexdigest()
    if hash_value != CAP_HASH[cap - 1]:
        raise ValueError("Input does not match the certified rank-two component")
    component = {tuple(l.split()) for l in raw.decode("ascii").splitlines()}
    if not orbit(("xxxYYYY", "xyxYXY")) <= component:
        raise ValueError("Rank-two component does not certify all signed-basis images")
    ordered = sorted({(r, s) for a, b in component for r, s in ((a, b), (b, a))
                      if 2 * len(r) + len(s) + 1 <= cap})
    seeds, source_count = first_exits(ordered, cap)
    output.write_text("".join("\t".join(t) + "\n" for t in sorted(seeds)))
    return dict(cap=cap, rank_two_catalogue_sha256=hash_value,
                ordered_boundary_pairs=len(ordered), examined_singleton_lifts=source_count,
                first_exit_seeds=len(seeds))


def short_pivot_audit(states, catalogue, reverse=None):
    pairs, zero = set(), set()
    short = Counter()
    rows = 0
    for line in states.open():
        triple = line.split()
        rows += 1
        for i, w in enumerate(triple):
            if "z" not in w.lower():
                zero.add(w)
            if len(w) != 2:
                continue
            short[w] += 1
            a, b = w
            if a.lower() == "z":
                a, b = b, a
            if a.lower() not in "xy" or b.lower() != "z":
                continue
            image = a.swapcase() if b == "z" else a
            sub = str.maketrans("zZ", image + image.swapcase())
            pairs.add(tuple(sorted(canonical(v.translate(sub)) for j, v in enumerate(triple)
                                   if i != j)))
    distinct_projected_words = {w for pair in pairs for w in pair}
    primitives = sorted(w for w in distinct_projected_words if primitive_cyclic_word(w))
    digest = sha256()
    remaining = set(pairs)
    for raw in catalogue.open("rb"):
        digest.update(raw)
        if len(raw) <= 22:
            remaining.discard(tuple(raw.decode("ascii").split()))
    if digest.hexdigest() != CAP_HASH[26]:
        raise ValueError("Invalid cap-26 catalogue")
    result = dict(states=rows, length_two_rows=dict(sorted(short.items())), projected_pairs=len(pairs),
                  primitive_projected_rows=primitives, unmatched_against_cap26=sorted(remaining),
                  distinct_z_free_rows=len(zero),
                  primitive_z_free_rows=sorted(w for w in zero if primitive_cyclic_word(w)))
    if reverse is not None:
        literal = {tuple(line.split()) for line in reverse.open()}
        expanded = set().union(*(orbit(pair) for pair in pairs))
        result["signed_projected_pairs"] = len(expanded)
        result["known_trivial_archive_matches"] = sorted(expanded & literal)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    build = sub.add_parser("prepare")
    build.add_argument("catalogue", type=Path)
    build.add_argument("cap", type=int, choices=(22, 23))
    build.add_argument("output", type=Path)
    audit = sub.add_parser("short-pivots")
    audit.add_argument("states", type=Path)
    audit.add_argument("catalogue", type=Path)
    audit.add_argument("--reverse", type=Path)
    args = parser.parse_args()
    if args.mode == "prepare":
        result = prepare(args.catalogue, args.cap, args.output)
    else:
        result = short_pivot_audit(args.states, args.catalogue, args.reverse)
    print(json.dumps(result, indent=2))
