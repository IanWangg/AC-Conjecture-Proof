"""Find short marked basis exchanges exposing a literal deletion chart."""

import argparse
from collections import Counter
from itertools import product
import json
from pathlib import Path

from euclidean_primitive_audit import primitive_cyclic_word
from round03_stable_proof_pivot import canonical
from round04_chart_screen import chart_projections
from round05_stable_chart_transport import defining_exchange
from round06_stable_proof_cap23_charts import compact_row

ROOT = Path(__file__).resolve().parents[1]
PREFIX = ROOT / "certificates/round06_stable_proof_cap23_escape.json"
TRANVECTIONS = tuple((g, a, left) for g, a, left in product("xyz", "xXyYzZ", (True, False))
                      if g != a.lower())


def search(cap29, max_exchanges, state_cap):
    start = tuple(json.loads(PREFIX.read_text())["target"])
    visited = {start: ()}
    frontier = [start]
    projections = {}
    hist = []
    for depth in range(max_exchanges + 1):
        hist.append(len(frontier))
        following = []
        for rows in frontier:
            for letter, pivot, pair in chart_projections(rows):
                if sum(map(len, pair)) > 29:
                    continue
                key = compact_row(pair)
                candidate = (len(visited[rows]), sum(map(len, pair)), tuple(visited[rows]), rows, letter, pivot, pair)
                if key not in projections or candidate < projections[key]:
                    projections[key] = candidate
            if depth == max_exchanges:
                continue
            for marked, multiplier, left in TRANVECTIONS:
                changed, _ = defining_exchange(rows, marked, multiplier, left)
                state = tuple(map(canonical, changed))
                if sum(map(len, state)) > state_cap or state in visited:
                    continue
                visited[state] = (*visited[rows], (marked, multiplier, left))
                following.append(state)
        frontier = following

    with cap29.open("rb") as stream:
        hits = {row for row in stream if row in projections}
    missing = sorted(candidate for key, candidate in projections.items() if key not in hits)
    possible_primitive = sorted(candidate for candidate in projections.values()
                                if any(primitive_cyclic_word(word) for word in candidate[-1]))

    def record(candidate):
        depth, energy, changes, rank_three, letter, pivot, pair = candidate
        return dict(exchanges=depth, marker_changes=changes, resulting_ambient_rows=rank_three,
                    eliminated=letter, pivot=pivot, pair=pair, energy=energy)

    return dict(maximum_exchanges=max_exchanges, symbolic_rank_three_cap=state_cap,
                state_layers=hist, projection_orbits=len(projections), in_cap29=len(hits),
                outside_by_minimum_exchange_count=dict(sorted(Counter(row[0] for row in missing).items())),
                primitive_projections=[record(row) for row in possible_primitive],
                earliest_outside=[record(row) for row in missing[:8]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cap29", type=Path)
    parser.add_argument("--exchanges", type=int, default=3)
    parser.add_argument("--state-cap", type=int, default=40)
    args = parser.parse_args()
    print(json.dumps(search(args.cap29, args.exchanges, args.state_cap), indent=2))
