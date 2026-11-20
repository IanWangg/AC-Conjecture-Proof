"""Verify the first-chart projections and lift their isolated charts."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from euclidean_primitive_audit import primitive_cyclic_word
from round03_stable_proof_pivot import canonical
from round04_chart_screen import chart_projections
from round06_stable_proof_cap23_charts import compact_row
from round06_stable_proof_strict_escape import StrictPath
from round07_stable_proof_local_audit import catalogue, successors
from round09_stable_proof_lift_excursion import signed_rows
from round12_stable_proof_corridor import native_nodes, pivot_count
from round15_stable_proof_splice import align, statistics
from round20_stable_proof_replay import lift_route


def projections(prefix, roots):
    nodes = native_nodes(prefix)
    receipt = json.loads(prefix.with_suffix(".json").read_text())
    cap = receipt["cap"]
    assert receipt["closed"] and not receipt["hit"] and not receipt["mixed"]
    assert not receipt["word_width_omissions"] and not receipt["positive_bridges"]
    donor_orbit = {row[0] for row in signed_rows(("xxyXYY",) * 3)}
    keys, isolated = set(), set()
    energies = Counter()
    seed_count = 0
    first_bridge = cap + 100
    width = 0
    for index, (parent, pivots, rows) in enumerate(nodes):
        assert set(rows).isdisjoint(donor_orbit)
        assert pivots == pivot_count(rows)
        if index < len(roots):
            assert parent == 2**64 - 1 and rows in roots
            seed_count += 1
        else:
            assert parent < index and nodes[parent][1] == 0
        if pivots:
            assert pivots == 1 and sum(len(row) == 1 for row in rows) == 1
            for eliminated, _, pair in chart_projections(rows):
                assert not any(map(primitive_cyclic_word, pair))
                key = compact_row(pair)
                keys.add(key)
                if sum(eliminated in row.lower() for row in rows) == 1:
                    isolated.add(key)
        else:
            energies[sum(map(len, rows))] += 1
            first_bridge = min(first_bridge, sum(map(len, rows)) + min(map(len, rows)) + 2)
            width = max(width, cap - sum(sorted(map(len, rows))[:2]))
    assert seed_count == len(roots) and len(nodes) == receipt["discovered"]
    assert len({rows for _, _, rows in nodes}) == len(nodes)
    assert sum(energies.values()) == receipt["expanded"]
    assert first_bridge > cap and width <= 21
    for suffix, checked in ((".pairs.tsv", keys), (".isolated.tsv", isolated)):
        listed = {compact_row(line.split()[:2]) for line in Path(str(prefix) + suffix).read_text().splitlines()}
        assert checked == listed
    return keys, isolated, {
        "chartless_energy_histogram": dict(sorted(energies.items())),
        "first_possible_positive_bridge_energy": first_bridge,
        "maximum_allowed_output_word_width": width,
        "projection_sha256": sha256(b"".join(sorted(keys))).hexdigest(),
        "isolated_projection_sha256": sha256(b"".join(sorted(isolated))).hexdigest(),
    }


def traced_route(nodes, index):
    trace = []
    while index != 2**64 - 1:
        parent, _, rows = nodes[index]
        trace.append(rows)
        assert parent == 2**64 - 1 or parent < index
        index = parent
    return trace[::-1]


def route_inputs(earlier, current, isolated_keys):
    older = native_nodes(earlier)
    old_ids = {rows: i for i, (_, count, rows) in enumerate(older) if not count}
    newer = native_nodes(current)
    recipes = []
    isolated_lines = Path(str(current) + ".isolated.tsv").read_text().splitlines()
    isolated_rows = {compact_row(line.split()[:2]): line for line in isolated_lines}
    assert set(isolated_rows) == isolated_keys
    for line in Path(str(current) + ".pairs.tsv").read_text().splitlines():
        key = compact_row(line.split()[:2])
        isolated = key in isolated_keys
        if isolated:
            line = isolated_rows[key]
        left, right, index, pivot, *rows = line.split()
        path = traced_route(newer, int(index))
        assert tuple(rows) == path[-1] and rows[int(pivot)] == "X"
        prefix = traced_route(older, old_ids[path[0]])
        recipes.append({"projected": [left, right], "entry": prefix, "donor_free": path,
                        "isolated": isolated})
    return recipes


def compile_routes(ordinary, routes, output_directory):
    receipts = []
    donor_orbit = {row[0] for row in signed_rows(("xxyXYY",) * 3)}
    output_directory.mkdir(parents=True, exist_ok=True)
    for i, route in enumerate(routes, 1):
        entry = [tuple(row) for row in route["entry"]]
        free = [tuple(row) for row in route["donor_free"]]
        start = tuple(ordinary["target"]) + ("z",)
        assert entry[-1] == free[0]
        goal, moves = lift_route(start, entry + free[1:], require_isolated=route["isolated"])
        cutoff = next(j for j in range(1, len(entry)) if not set(entry[j]).intersection(donor_orbit))
        assert all(set(rows).isdisjoint(donor_orbit) for rows in entry[cutoff:] + free)
        with (output_directory / f"stable-{i:02d}.jsonl").open("wb") as sink:
            path = StrictPath(ordinary["start"], sink)
            path.extend(ordinary["moves"])
            path.add({"op": "stabilize", "generator": "z"})
            for slot, word in enumerate(path.rows):
                align(path, slot, canonical(word))
            released = False
            for move in moves:
                path.add(move)
                donor_present = not set(map(canonical, path.rows)).isdisjoint(donor_orbit)
                assert not (released and donor_present)
                released |= not donor_present
            assert released and tuple(path.rows) == goal
            slot = goal.index("Z")
            first_chart = path.total
            if not route["isolated"]:
                for recipient in range(3):
                    if recipient != slot:
                        path.change_occurrences(recipient, "z", "", slot)
            align(path, slot, "z")
            path.add({"op": "destabilize", "generator": "z", "i": slot})
            assert compact_row(path.rows) == compact_row(route["projected"])
            assert path.cyclic_peak == 38
            path.record((json.dumps({"target": path.rows}, separators=(",", ":")) + "\n").encode())
            receipts.append(statistics(path) | {"signed_projection": route["projected"],
                                                "isolated_first_chart": route["isolated"],
                                                "instructions_after_first_chart": path.total - first_chart,
                                                "local_products": len(entry) + len(free) - 2})
    return receipts


def ordinary_component(comparison, start):
    listed = catalogue(comparison)
    root = compact_row(start)
    reached, queue = {root}, [root]
    count = 0
    for key in queue:
        adjacent, checked, _ = successors(listed[key], 22)
        count += checked
        assert adjacent <= listed.keys()
        for neighbor in sorted(adjacent - reached):
            reached.add(neighbor)
            queue.append(neighbor)
    assert reached == listed.keys()
    return listed, count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path)
    parser.add_argument("roots", type=Path)
    parser.add_argument("earlier", type=Path)
    parser.add_argument("ordinary", type=Path)
    parser.add_argument("comparison", type=Path)
    args = parser.parse_args()
    roots = {tuple(line.split()) for line in args.roots.read_text().splitlines()}
    excluded = {row[0] for row in signed_rows(("xxyXYY",) * 3)}
    assert roots == {rows for _, pivots, rows in native_nodes(args.earlier)
                     if not pivots and set(rows).isdisjoint(excluded)}
    settled = {}
    for cap in (38, 39):
        settled[cap] = projections(args.work / f"all{cap}", roots)
    assert settled[38][:2] == settled[39][:2]
    keys, isolated, _ = settled[38]
    ordinary = json.loads(args.ordinary.read_text())
    ordinary_keys, ordinary_checks = ordinary_component(args.comparison, ordinary["target"])
    assert keys == {key for key, rows in ordinary_keys.items() if sum(map(len, rows)) in (17, 22)}
    assert isolated == {key for key, rows in ordinary_keys.items() if sum(map(len, rows)) == 22}
    recipes = route_inputs(args.earlier, args.work / "all38", isolated)
    (args.work / "first_exit_routes.json").write_text(json.dumps(recipes, indent=2) + "\n")
    strict = compile_routes(ordinary, recipes, args.work / "strict")
    print(json.dumps({
        "native": {cap: json.loads((args.work / f"all{cap}.json").read_text()) for cap in settled},
        "independent_chart_checks": {cap: row[2] for cap, row in settled.items()},
        "projection_orbits": len(keys), "isolated_projection_orbits": len(isolated),
        "ordinary_comparison_orbits": len(ordinary_keys),
        "ordinary_cap22_independent_candidates": ordinary_checks,
        "equals_energy_17_and_22_slices_of_ordinary_cap22": True,
        "strict": strict,
    }, indent=2))


if __name__ == "__main__":
    main()
