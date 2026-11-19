"""Compare chart projections with all ambient-marked representatives in C29."""

import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from round01_geometric_archive import check_whitehead_cuts, image, length, minimal_pair
from round05_ak3_orbit_audit import word_orbit
from round05_stable_proof_projections import each_available_chart
from round06_stable_proof_cap23_charts import compact_row


def signed_key(pair):
    return min(tuple(sorted(rows)) for rows in zip(*(word_orbit(word) for word in pair)))


MOVES = tuple((letter, letter + signed if right else signed + letter)
              for (letter, donor) in (("x", "y"), ("y", "x"))
              for signed, right in product((donor, donor.upper()), (False, True)))


def projected_sources(partial):
    projections = {}
    digest = sha256()
    scanned = 0
    with partial.open("rb") as input_file:
        for raw in input_file:
            digest.update(raw)
            rows = tuple(raw.decode("ascii").split())
            if any(word.lower().count("z") == 1 for word in rows):
                continue
            scanned += 1
            for pair, details in each_available_chart(rows):
                projections.setdefault(signed_key(pair), {"rank_three_rows": rows, "projected_pair": pair, **details})
    return projections, scanned, digest.hexdigest()


def explore(projections, cap):
    minima = {}
    skipped = []
    for pair, origin in sorted(projections.items()):
        minimum = signed_key(minimal_pair(pair))
        check_whitehead_cuts(minimum)
        if length(minimum) > cap:
            skipped.append((minimum, origin))
        else:
            minima.setdefault(minimum, []).append((pair, origin))

    all_nodes = {}
    records = {}
    for minimum in sorted(minima, key=lambda pair: (length(pair), pair)):
        if minimum in all_nodes:
            records[all_nodes[minimum]]["inputs"].extend(minima[minimum])
            continue
        count = 0
        queue = deque([minimum])
        all_nodes[minimum] = minimum
        while queue:
            state = queue.popleft()
            count += 1
            for letter, replacement in MOVES:
                nxt = image(state, letter, replacement)
                if length(nxt) > cap:
                    continue
                key = signed_key(nxt)
                if key in all_nodes:
                    assert all_nodes[key] == minimum
                else:
                    all_nodes[key] = minimum
                    queue.append(key)
        records[minimum] = {"states": count, "inputs": minima[minimum], "known_ordinary_example": None}
    return all_nodes, records, skipped


def run(partial, cap29):
    sources, screened, source_hash = projected_sources(partial)
    all_nodes, records, skipped = explore(sources, 29)
    signatures = {compact_row(pair): anchor for pair, anchor in all_nodes.items()}
    assert len(signatures) == len(all_nodes)
    file_hash = sha256()
    with cap29.open("rb") as stream:
        for row in stream:
            file_hash.update(row)
            if row in signatures:
                entry = records[signatures[row]]
                if entry["known_ordinary_example"] is None:
                    entry["known_ordinary_example"] = row.decode("ascii").split()
    known = [(anchor, row) for anchor, row in records.items() if row["known_ordinary_example"]]
    missing = [(anchor, row) for anchor, row in records.items() if not row["known_ordinary_example"]]
    first_missing = []
    for anchor, row in sorted(missing, key=lambda data: (length(data[0]), data[0]))[:8]:
        source = min(row["inputs"], key=lambda data: (length(data[0]), data[0]))[1]
        first_missing.append(dict(whitehead_minimum=anchor, restated_source=source,
                                  ambient_orbit_sublevel_size=row["states"], source_orbits=len(row["inputs"])))
    return dict(cap=29, partial_sha256=source_hash, compact_rank_two_cap29_sha256=file_hash.hexdigest(),
                no_fixed_z_chart_states=screened, source_signed_projection_orbits=len(sources),
                sources_with_minimum_above_cap=len(skipped),
                sources_minimum_histogram_above_cap=dict(sorted(Counter(length(p) for p, _ in skipped).items())),
                searched_ambient_orbits=len(records), searched_signed_states=len(all_nodes),
                ambient_orbits_with_anchor=len(known), ambient_orbits_missing_anchor=len(missing),
                source_orbits_with_anchor=sum(len(r["inputs"]) for _, r in known),
                source_orbits_missing_anchor=sum(len(r["inputs"]) for _, r in missing) + len(skipped),
                minimal_missing_orbits=first_missing)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rank_three_partial", type=Path)
    parser.add_argument("rank_two_compact", type=Path)
    options = parser.parse_args()
    print(json.dumps(run(options.rank_three_partial, options.rank_two_compact), indent=2))
