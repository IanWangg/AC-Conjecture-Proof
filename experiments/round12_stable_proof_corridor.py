"""Independently check and lift the chartless corridor from the R11 excursion."""

import argparse
from array import array
from collections import deque
from functools import cache
from hashlib import sha256
import json
from pathlib import Path

from euclidean_primitive_audit import primitive_cyclic_word
from free_waypoint_search import normalize
from round01_geometric_archive import check_whitehead_cuts, length, minimal_pair
from round03_stable_proof_pivot import canonical, neighbors
from round04_stable_proof_paths import edge, replay
from round05_stable_proof_chartless import minima
from round05_stable_proof_projections import each_available_chart, geometry_screen
from round06_stable_proof_cap23_charts import compact_row
from round07_stable_proof_automorphic_charts import signed_key
from round09_stable_proof_lift_excursion import signed_rows
from round09_stable_proof_rank_three_chart import compile_chart
from round11_stable_proof_reverse import certificate, read

START = ("XXYYxyyyxYZY", "XYYXyxy", "XYYXyxyz")
ALPHABET = "xXyYzZ"
WIDTH = 21


@cache
def rank_three_key(rows):
    return tuple(sorted(min(tuple(sorted(mark, key=lambda word: (len(word), word)))
                            for mark in signed_rows(rows))))


@cache
def primitive(word):
    return any(word.lower().count(g) == 1 for g in "xyz") or len(minima((word,))[0][0]) == 1


def pivot_count(rows):
    return sum(map(primitive, rows))


def lift(prefix, orbit_route, cap):
    endpoint = tuple(replay(prefix)["target"])
    assert tuple(sorted(map(canonical, endpoint))) in signed_rows(orbit_route[0])
    moves = prefix["moves"].copy()
    for i, row in enumerate(endpoint):
        endpoint, steps = normalize(endpoint, i, canonical(row))
        moves.extend(steps)
    boundaries = [len(moves)]
    for goal in orbit_route[1:]:
        successors, _ = neighbors(endpoint, cap)
        representative = min(successors & signed_rows(goal))
        endpoint, steps = edge(endpoint, representative, cap, ALPHABET)
        moves.extend(steps)
        boundaries.append(len(moves))
    return certificate(prefix["start"], moves, endpoint), boundaries


def native_nodes(prefix):
    nodes = []
    for line in Path(str(prefix) + ".nodes.tsv").read_text().splitlines():
        anchor, count, *rows = line.split()
        assert len(rows) == 3
        nodes.append((int(anchor), int(count), tuple(rows)))
    return nodes


def native_projections(prefix):
    for line in Path(str(prefix) + ".pairs.tsv").read_text().splitlines():
        first, second, anchor, *rows = line.split()
        assert len(rows) == 3
        yield (first, second), int(anchor), tuple(rows)


def traced_route(nodes, parent):
    trace = []
    while parent < len(nodes):
        last = parent
        parent, _, rows = nodes[parent]
        assert parent < last or last == 0
        trace.append(rows)
    return trace[::-1]


def independent_closure(prefix, cap):
    nodes = native_nodes(prefix)
    root = rank_three_key(START)
    assert nodes[0][2] == root and pivot_count(root) == 2
    checked_products = 0
    marked_donor_changes = 0
    donor = next(word for word in START if not primitive(canonical(word)))
    donor_orbit = {row for point in signed_rows((donor, donor, donor)) for row in point}

    def menu(rows):
        nonlocal checked_products, marked_donor_changes
        found, products = neighbors(rows, cap)
        checked_products += products
        assert all(3 <= length(state) <= cap and max(map(len, state)) <= WIDTH for state in found)
        source_donor = (set(rows) & donor_orbit) if not pivot_count(rows) else set()
        result = {}
        for key in found:
            count = pivot_count(key)
            if source_donor and not count and not source_donor.intersection(key):
                marked_donor_changes += 1
            result[rank_three_key(key)] = count
        return result

    one_pivot = {key for key, count in menu(root).items() if count == 1}
    assert one_pivot == {key for _, count, key in nodes if count == 1}
    reached = set()
    for key in one_pivot:
        reached.update(dest for dest, count in menu(key).items() if not count)
    seeds = len(reached)
    queue = deque(reached)
    charted = set()
    while queue:
        for key, count in menu(queue.popleft()).items():
            if count:
                charted.add(key)
            elif key not in reached:
                reached.add(key)
                queue.append(key)
    assert reached == {key for _, count, key in nodes if not count}
    assert {rows for _, _, rows in native_projections(prefix)} <= charted
    return {"cap": cap, "one_pivot_orbits": len(one_pivot), "chartless_seeds": seeds,
            "chartless_orbits": len(reached), "charted_first_exits": len(charted),
            "literal_menu_checks": checked_products,
            "marked_donor_changes_on_chartless_edges": marked_donor_changes}


def choose_exit(prefix, original_energy):
    nodes = native_nodes(prefix)
    candidates = []
    for pair, anchor, exit_rows in native_projections(prefix):
        # Compare independently minimized quotient energies, which distinguish ambient classes.
        reference = length(minimal_pair(pair))
        if reference == original_energy:
            continue
        if not any(signed_key(p) == signed_key(pair) and details["chart"] == "literal"
                   for p, details in each_available_chart(exit_rows)):
            continue
        route = [*traced_route(nodes, anchor), exit_rows]
        candidates.append((reference, length(pair), len(route), pair, route))
    return min(candidates)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def donor_release(work, artifact_directory):
    fixed = next(word for word in START if not primitive(canonical(word)))
    family = {row for point in signed_rows((fixed, fixed, fixed)) for row in point}
    chartless34 = [rows for _, count, rows in native_nodes(work / "final34") if not count]
    assert len(chartless34) == 505 and all(sum(row in family for row in rows) == 1 for rows in chartless34)
    depths, offsets = array("I"), array("Q")
    best = None
    lost = 0
    path = work / "final35.nodes.tsv"
    with path.open("rb") as stream:
        for index, line in enumerate(iter(stream.readline, b"")):
            parent, count, *rows = line.decode().split()
            depth = 0 if index == 0 else 1 + depths[int(parent)]
            depths.append(depth)
            offsets.append(stream.tell() - len(line))
            if int(count) or any(row in family for row in rows):
                continue
            lost += 1
            choice = (depth, length(rows), index)
            best = choice if best is None else min(best, choice)
        assert best is not None
        route = []
        index = best[-1]
        while index < len(depths):
            stream.seek(offsets[index])
            parent, _, *rows = stream.readline().decode().split()
            route.append(tuple(rows))
            index = int(parent)
    route.reverse()
    assert all(not pivot_count(point) for point in route[2:])
    proof, boundaries = lift(read("round11_stable_proof_source_excursion.json"), route, 35)
    assert all(canonical(row) not in family for row in proof["target"])
    if artifact_directory:
        write_json(artifact_directory / "round12_stable_proof_corridor_donor_release.json", proof)
    return {"original_donor": fixed, "cap34_chartless_orbits_with_donor": len(chartless34),
            "partial_cap35_chartless_orbits_without_donor": lost,
            "selected_orbit_route": route, "boundary_instructions": boundaries,
            "primitive_counts": list(map(pivot_count, route)), "strict_replay": replay(proof)}


def geometric_positive(work):
    source = read("round11_stable_proof_geometric_suffix.json")
    point = tuple(source["start"])
    initial = certificate(point, [], point)
    route_file = work / "finalcontrol.route.tsv"
    orbit_route = [tuple(line.split()) for line in route_file.read_text().splitlines()]
    proof, boundaries = lift(initial, orbit_route, 30)
    assert not pivot_count(tuple(map(canonical, point)))
    projected = [{"pair": pair, **chart} for pair, chart in each_available_chart(tuple(proof["target"]))
                 if any(primitive_cyclic_word(word) for word in pair)]
    assert projected and len(orbit_route) == 2
    return {"original_strict_suffix": replay(source), "one_product_replay": replay(proof),
            "orbit_route": orbit_route, "boundaries": boundaries, "primitive_projections": projected,
            "strict_ledger": proof}


def analyze(work, reverse, artifact_directory):
    prefix = work / "final31"
    initial = read("round11_stable_proof_source_excursion.json")
    initial_rows = tuple(initial["target"])
    assert tuple(START) == initial_rows
    original_pairs = {signed_key(pair) for pair, _ in each_available_chart(initial_rows)}
    assert len(original_pairs) == 1
    original = min(original_pairs)
    original_minimum = minimal_pair(original)
    check_whitehead_cuts(original_minimum)
    minimum, _, _, pair, route = choose_exit(prefix, length(original_minimum))
    proof, boundaries = lift(initial, route, 31)
    for row in route[2:-1]:
        assert not pivot_count(row)
    selected = [(p, c) for p, c in each_available_chart(tuple(proof["target"]))
                if signed_key(p) == signed_key(pair) and c["chart"] == "literal"]
    assert selected
    chosen, chart = min(selected, key=lambda item: (item[0], item[1]["eliminated"]))
    assert length(minimal_pair(chosen)) == minimum and minimum != length(original_minimum)
    pivot = list(proof["target"]).index(chart["pivot"])

    compiled = {}
    if artifact_directory:
        artifact_directory.mkdir(parents=True, exist_ok=True)
        write_json(artifact_directory / "round12_stable_proof_corridor_prefix.json", proof)
        with (artifact_directory / "round12_stable_proof_corridor_chart.jsonl").open("wb") as sink:
            compiled = compile_chart(proof, pivot, sink, literal=chart["eliminated"])
        assert signed_key(compiled["final_words"]) == signed_key(pair)

    sources = {pair: {"rank_three_rows": rows} for pair, _, rows in native_projections(work / "final34")}
    archive = {signed_key(tuple(line.split())) for line in reverse.read_text().splitlines()}
    archive_hits = sorted(archive & sources.keys())
    geometry = geometry_screen(sources, work / "projection-minima28.tsv")
    projected_sublevel = {compact_row(minimum) for pair in sources if length(minimum := minimal_pair(pair)) <= 32}
    (work / "projection-minima32.tsv").write_bytes(b"".join(sorted(projected_sublevel)))
    native = {str(cap): json.loads((work / f"final{cap}.json").read_text())
              for cap in range(30, 39) if (work / f"final{cap}.json").stat().st_size}
    audit = independent_closure(work / "final31", 31)
    assert audit["charted_first_exits"] == native["31"]["exit_orbits"]
    return {"source": START, "source_projection": original, "source_minimum": original_minimum,
            "native_runs": native, "independent_cap31_closure": audit,
            "selected_chart_switch": {"route": route, "rank_three_replay": replay(proof),
                                      "primitive_counts_at_orbit_boundaries": list(map(pivot_count, route)),
                                      "boundary_instructions": boundaries, "pivot_slot": pivot,
                                      "projected_pair": chosen, "projection_chart": chart,
                                      "projection_minimum": minimal_pair(chosen),
                                      "strict_stable_projection": compiled},
            "cap34_projection_checks": {"known_trivial_archive_pairs": len(archive),
                                        "archive_sha256": sha256(reverse.read_bytes()).hexdigest(),
                                        "exact_archive_hits": archive_hits,
                                        "distinct_minima_through32": len(projected_sublevel), **geometry},
            "chartless_donor_release": donor_release(work, artifact_directory),
            "geometric_control": geometric_positive(work)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path)
    parser.add_argument("reverse", type=Path)
    parser.add_argument("--certificates", type=Path)
    parser.add_argument("--independent-cap", type=int, choices=(31, 34))
    args = parser.parse_args()
    result = independent_closure(args.work / f"final{args.independent_cap}", args.independent_cap) \
        if args.independent_cap else analyze(args.work, args.reverse, args.certificates)
    print(json.dumps(result, indent=2))
