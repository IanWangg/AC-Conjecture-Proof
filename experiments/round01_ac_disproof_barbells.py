"""Exhaust finite first-phase barbell sources and audit V's kernel certificates.

The bridge bound applies to the first-phase source graph only. Each
certified source has arbitrary subsequent Nielsen words and tails.
"""
import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
from pathlib import Path

from primitive_map_pairs import LETTERS, fold, follow, inverse, reduce, witness
from v_vertex_identification import cross, dot, fold_identification, spanning, word_voltage
from v_voltage_cycle_review import review
from verify_vertex_voltage import verify


def rotations(word):
    return list(dict.fromkeys(word[i:] + word[:i] for i in range(len(word))))


def reduced_words(length, prefix=""):
    if len(prefix) == length:
        yield prefix
        return
    for letter in LETTERS:
        if not prefix or letter != inverse(prefix[-1]):
            yield from reduced_words(length, prefix + letter)


def sources(parameter, bridge):
    power = "x" * parameter + "Y" * (parameter + 1)
    braid = "xyxYXY"
    for p in rotations(power):
        if bridge[0] in (p[0], inverse(p[-1])):
            continue
        for b in rotations(braid):
            if inverse(bridge[-1]) not in (b[0], inverse(b[-1])):
                yield p, b


def source_graph(p, b, bridge):
    initial = [p, bridge + b + inverse(bridge)]
    graph = fold(initial)
    assert len(graph) // 4 == len(p) + len(b) + len(bridge) - 1
    assert sorted(sum(end >= 0 for end in graph[4 * v:4 * v + 4])
                  for v in range(len(graph) // 4)) == [2] * (len(graph) // 4 - 2) + [3, 3]
    return initial, graph


def character_record(initial, original, paths, a, b):
    graph, projection = fold_identification(original, a, b)
    _, extra, arcs, coordinates = spanning(graph)
    t = reduce(paths[a] + inverse(paths[b]))
    if len(extra) != 3:
        return dict(identified_vertices=[a, b], rank=len(extra))
    h = cross(*map(coordinates, initial))
    determinant = dot(h, coordinates(t))
    assert abs(determinant) == 1
    weights = [0] * len(graph)
    for (v, c, _), (i, sign) in arcs.items():
        weights[4 * v + c] = sign * h[i] // determinant
    return dict(identified_vertices=[a, b], graph=graph, rank=3,
                vertex_projection=projection, extra_generator=t, edge_voltages=weights)


def analyze(p, b, bridge):
    initial, original = source_graph(p, b, bridge)
    return audit_core(initial, original)


def audit_core(initial, original):
    paths, _, _, _ = spanning(original)
    records, potentials, unresolved = [], [], []
    for a in sorted(paths):
        for j in range(a + 1, len(paths)):
            record = character_record(initial, original, paths, a, j)
            if record["rank"] != 3:
                unresolved.append(dict(vertices=[a, j], rank=record["rank"]))
                continue
            test = review(record["graph"], record["edge_voltages"])
            records.append(record)
            potentials.append(dict(identified_vertices=[a, j], **test))
            if test["status"] != "PASS":
                unresolved.append(dict(vertices=[a, j], rank=3))
    if unresolved:
        return None, unresolved
    data = dict(original_pair=initial, original_graph=original, records=records)
    cert = dict(results=potentials)
    audit = verify(data, cert)
    digest = hashlib.sha256(json.dumps([data, cert], separators=(",", ":")).encode()).hexdigest()
    return dict(audit, certificate_sha256=digest), unresolved


def controls():
    p, b, bridge = "YYxxxYY", "xyxYXY", "x"
    (p, q), _ = source_graph(p, b, bridge)
    rotations_checked = p_loops = 0
    for p_rotation in rotations("xxxYYYY"):
        for b_rotation in rotations(b):
            graph = fold([p_rotation, b_rotation])
            rotations_checked += 1
            for v in range(len(graph) // 4):
                if follow(graph, v, p) == v:
                    p_loops += 1
                    assert follow(graph, v, q) != v
                    assert follow(graph, v, q + p) < 0
    source, graph = source_graph("xYYYx", "yxYXYx", "y")
    paths, _, _, _ = spanning(graph)
    row = character_record(source, graph, paths, 0, 3)
    assert row["extra_generator"] == "Y"
    quotient, weights = row["graph"], row["edge_voltages"]
    primitive = witness(quotient, "xY", "RLRL", 1, 2)
    word = primitive["cyclic_primitive_word"]
    assert word == "xYxYYxYY"
    assert word_voltage(quotient, weights, word, 2) == 0
    assert review(quotient, weights)["status"] == "UNRESOLVED"
    return dict(rotation_sources_checked=rotations_checked,
                seed_power_loops=p_loops, seed_containing_rotation_graphs=0,
                QP_readable_at_seed_power_loops=0,
                AK2_barbell=dict(source=source, identified_vertices=[0, 3],
                                primitive_in_coarse_kernel=primitive))


def external_waypoints():
    pairs = [["XXyXYYYxxYxyy", "XYxYYxY"], ["XXyyxYxyxYYXy", "XYxYYxY"]]
    audits = []
    for pair in pairs:
        audit, unresolved = audit_core(pair, fold(pair))
        assert not unresolved
        audits.append(dict(pair=pair, audit=audit))
    return audits


def analyze_source(source):
    audit, unresolved = analyze(*source)
    return source, audit, unresolved


def run(max_bridge, pool=None):
    rows = {}
    for length in range(1, max_bridge + 1):
        totals = Counter(sources=0, certified_sources=0, vertex_identifications=0,
                         signed_automata=0, cyclic_components=0, inequalities=0)
        failures = []
        digest = hashlib.sha256()
        cases = ((p, b, q) for q in reduced_words(length) for p, b in sources(3, q))
        if pool is None:
            audits = map(analyze_source, cases)
        else:
            audits = pool.map(analyze_source, cases, chunksize=8)
        for (p, b, q), audit, unresolved in audits:
            totals["sources"] += 1
            if unresolved:
                failures.append(dict(power=p, braid=b, bridge=q, cases=unresolved))
                continue
            totals["certified_sources"] += 1
            totals["vertex_identifications"] += audit["vertex_identifications_independently_refolded"]
            totals["signed_automata"] += audit["signed_double_free_graphs_independently_reconstructed"]
            totals["cyclic_components"] += audit["cyclic_components_independently_recognized"]
            totals["inequalities"] += audit["integer_potential_inequalities_checked"]
            digest.update(bytes.fromhex(audit["certificate_sha256"]))
        assert totals["sources"] == 42 * 3 ** (length - 1)
        rows[length] = dict(totals, unresolved_sources=failures,
                            certificates_sha256=digest.hexdigest())
        print(length, totals, "unresolved", len(failures), flush=True)
    # This particular barbell has an independent positive/negative check in
    # the report, and is singled out for the unbounded bridge construction.
    audit, unresolved = analyze("YYxxxYY", "xyxYXY", "x")
    assert not unresolved
    return dict(bridge_max=max_bridge, by_length=rows, length_one_seed=audit,
                controls=controls(), external_waypoints=external_waypoints())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-bridge", type=int, default=4)
    parser.add_argument("--jobs", type=int, default=1, help="parallel source workers")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_bridge < 1:
        parser.error("--max-bridge must be positive")
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    if args.jobs == 1:
        result = run(args.max_bridge)
    else:
        with ProcessPoolExecutor(max_workers=args.jobs) as pool:
            result = run(args.max_bridge, pool)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
