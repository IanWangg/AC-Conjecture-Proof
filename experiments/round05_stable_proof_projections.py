"""Screen deletion charts after loss of the fixed new-generator pivot."""

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from euclidean_primitive_audit import primitive_cyclic_word
from planar_link_parity import decide as parity_decide
from round01_geometric_archive import check_whitehead_cuts, minimal_pair
from round03_stable_proof_pivot import canonical
from round04_chart_screen import chart_projections
from round05_stable_proof_chartless import minima, whitehead_image
from round05_stable_proof_geometry import planar_orders
from verify_link_parity import verify_certificate


def rank_two_orbit(pair):
    for swap, inv_x, inv_y in product((False, True), repeat=3):
        x, y = ("y", "x") if swap else ("x", "y")
        x = x.upper() if inv_x else x
        y = y.upper() if inv_y else y
        markings = str.maketrans("xXyY", x + x.swapcase() + y + y.swapcase())
        yield tuple(sorted(canonical(w.translate(markings)) for w in pair))


@lru_cache(maxsize=None)
def intrinsic_chart(word):
    (minimum,), moves, *_ = minima((word,))
    return moves if len(minimum) == 1 else None


def each_available_chart(rows):
    for eliminated, pivot, pair in chart_projections(rows):
        yield pair, {"chart": "literal", "eliminated": eliminated, "pivot": pivot}
    for slot, word in enumerate(rows):
        if any(word.lower().count(g) == 1 for g in "xyz"):
            continue
        descent = intrinsic_chart(word)
        if descent is None:
            continue
        changed = rows
        for move in descent:
            changed = whitehead_image(changed, move["multiplier"], move["cut"])
        isolated = changed[slot]
        assert len(isolated) == 1
        for eliminated, pivot, pair in chart_projections(changed):
            if pivot == isolated:
                yield pair, {
                    "chart": "intrinsic", "original_pivot": word,
                    "eliminated": eliminated, "pivot": pivot, "whitehead_descent": descent,
                }


def linked_catalogue(catalogue, wanted):
    match = set()
    for line in catalogue.open("rb"):
        if line in wanted:
            match.add(wanted[line])
    return match


def geometry_screen(sources, basis_index_tsv):
    minima_by_key = {}
    for pair, source in sources.items():
        minimum = min(rank_two_orbit(minimal_pair(pair)))
        minima_by_key.setdefault(minimum, source)
    if basis_index_tsv is not None:
        small_pairs = sorted({image for pair in minima_by_key if sum(map(len, pair)) <= 28
                              for image in rank_two_orbit(pair)})
        basis_index_tsv.write_text("".join("\t".join(pair) + "\n" for pair in small_pairs))
    counts = Counter()
    remaining = []
    for pair, source in sorted(minima_by_key.items()):
        check_whitehead_cuts(pair)
        verdict = parity_decide(pair)
        if verdict["status"] == "PARITY_OBSTRUCTION":
            verify_certificate(verdict)
            counts["parity_obstructed"] += 1
        elif sum(map(len, pair)) <= 24:
            rotations = planar_orders(pair)
            if rotations["planar"]:
                counts["planar"] += 1
                remaining.append(dict(minimal_pair=pair, **source, rotations=rotations))
            else:
                counts["rotation_obstructed"] += 1
        else:
            counts["unresolved_above_rotation_scan_cap"] += 1
            remaining.append(dict(minimal_pair=pair, **source, parity_status=verdict["status"]))
    return dict(minimal_rank_two_signed_orbits=len(minima_by_key),
                classifications=dict(counts), remaining=remaining)


def run(states, catalogues, reverse, basis_index_tsv):
    sources = {}
    raw_sources = {}
    counts = Counter()
    for line in states.open():
        rows = tuple(line.split())
        counts["total_prefix_orbits"] += 1
        if any(w.lower().count("z") == 1 for w in rows):
            continue
        counts["no_z_pivot_prefix_orbits"] += 1
        for pair, details in each_available_chart(rows):
            counts[details["chart"] + "_charts"] += 1
            key = min(rank_two_orbit(pair))
            sources.setdefault(key, {"rank_three_rows": rows, "projected_pair": pair, **details})
            raw_sources.setdefault(pair, key)
    for pair in list(sources):
        raw_sources.update({image: pair for image in rank_two_orbit(pair)})
    wanted = {("\t".join(pair) + "\n").encode(): key for pair, key in raw_sources.items()}
    matches = {
        cap: linked_catalogue(path, wanted)
        for cap, path in catalogues
    }
    lower_unmatched = sorted(
        (pair for pair in sources if pair not in matches[catalogues[-1][0]]),
        key=lambda p: (sum(map(len, p)), p),
    )
    reverse_matches = linked_catalogue(reverse, wanted)
    return {
        **dict(counts),
        "signed_projection_orbits": len(sources),
        "primitive_projection_examples": [
            sources[pair] for pair in sources if any(primitive_cyclic_word(w) for w in pair)
        ],
        "input_tsv_sha256": sha256(states.read_bytes()).hexdigest(),
        "catalogue_hits": {cap: len(found) for cap, found in matches.items()},
        "projection_energy_histogram": dict(sorted(Counter(sum(map(len, p)) for p in sources).items())),
        "unmatched_energy_histogram": dict(sorted(Counter(sum(map(len, p)) for p in lower_unmatched).items())),
        "shortest_unmatched_examples": [sources[pair] for pair in lower_unmatched[:8]],
        "known_trivial_reverse_hits": [sources[pair] for pair in sorted(reverse_matches)],
        "geometry_screen": geometry_screen(sources, basis_index_tsv),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("states", type=Path)
    parser.add_argument("reverse", type=Path)
    parser.add_argument("catalogues", nargs="+", metavar="CAP:PATH")
    parser.add_argument("--basis-index-tsv", type=Path)
    args = parser.parse_args()
    catalogues = [(int(cap), Path(path)) for item in args.catalogues
                  for cap, path in [item.split(":", 1)]]
    assert all(a < b for (a, _), (b, _) in zip(catalogues, catalogues[1:]))
    print(json.dumps(run(args.states, catalogues, args.reverse, args.basis_index_tsv), indent=2))
