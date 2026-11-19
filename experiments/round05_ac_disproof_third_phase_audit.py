"""Independently count continuation cases and refold sample overgroups."""

import argparse
from itertools import combinations, product
import json
from pathlib import Path
import random

from elementary_verify import replay
from primitive_map_pairs import LETTERS, decide, fold, follow, inverse, reduce, verify_absence
from round02_ac_disproof_controls import audit_joins, rebased_join, signed_graphs_acyclic
from round03_ac_disproof_bridges import BRAID, POWER, rotations
from round04_ac_disproof_chain_audit import (
    EXAMPLE, basis, endpoint_paths, four_chains, free_directions, starts_reading,
)
from v_vertex_identification import spanning


FIVE = (("xxxYYYY", "XXXyyyy", "XXyyyyX", "xyxYXY", "YXYxyx"), "XyyX")
AK2 = ("xYYYx", "yxYXYx", "y")


def graph_basis(graph, base=0):
    paths, chords, *_ = spanning(graph, base)
    return [reduce(paths[a] + LETTERS[c] + inverse(paths[b])) for a, c, b in chords]


def first_cores(mode):
    if mode in ("four", "five"):
        yield fold(basis(*(EXAMPLE if mode == "four" else FIVE)))
        return
    for p, b in product(rotations(POWER), rotations(BRAID)):
        if mode == "rotation":
            yield fold((p, b))
        elif mode == "short":
            for c in sorted(free_directions(p)):
                if inverse(c) in free_directions(b):
                    yield fold((p, c + b + inverse(c)))


def reduced_words(length):
    words = [""]
    for _ in range(length):
        words = [w + c for w in words for c in LETTERS if not w or c != inverse(w[-1])]
    return words


def choices(graph, words):
    n = len(graph) // 4
    for w in words:
        a_letter = LETTERS.index(w[0])
        b_letter = LETTERS.index(inverse(w[-1]))
        starts = [v for v in range(n) if graph[4 * v + a_letter] < 0]
        ends = [v for v in range(n) if graph[4 * v + b_letter] < 0]
        for a, b in product(starts, ends):
            if (a, b, w) < (b, a, inverse(w)):
                yield a, b, w


def bridged_overgroup(graph, a, b, bridge):
    paths, *_ = spanning(graph)
    words = graph_basis(graph)
    relative = [reduce(inverse(paths[a]) + h + paths[a]) for h in words]
    transport = bridge + inverse(paths[b])
    relative += [reduce(transport + h + inverse(transport)) for h in words]
    return fold(relative)


def graph_tests(graph):
    n = len(graph) // 4
    return 1 + n * (n - 1) // 2


def refold_samples(graphs, seed):
    rng = random.Random(seed)
    tests = exact_states = 0
    for graph in graphs:
        words, (paths, *_) = graph_basis(graph), spanning(graph)
        cases = list(combinations(sorted(paths), 2))
        for a, b in rng.sample(cases, min(10, len(cases))):
            joined = rebased_join(words, paths, a, b)
            assert signed_graphs_acyclic(joined)
            tests += 1
            if (a, b) == cases[0] or tests % 7 == 0:
                receipt = decide(joined, save_certificate=True)
                assert receipt["status"] == "ABSENT"
                exact_states += verify_absence(receipt)["closed_map_pair_states_checked"]
    return tests, exact_states


def audit_mode(mode, receipt, exceptions, seed):
    assert exceptions.stat().st_size == 0
    stages = receipt["by_middle_gap_length"]
    cores = list(first_cores(mode))
    assert len(cores) == (42 if mode in ("rotation", "short") else 1)
    rng = random.Random(seed)
    tested = selected = exact_states = 0
    for length, row in enumerate(stages):
        assert row["length"] == length and row["first_sources"] == len(cores)
        assert row["certified_first_sources"] == len(cores)
        middle_count = finals = 0
        middle_sample = []
        selected_sources = set(rng.sample(range(len(cores)), min(3, len(cores))))
        connectors = reduced_words(length)
        for index, graph in enumerate(cores):
            n = len(graph) // 4
            if length == 0:
                paths, *_ = spanning(graph)
                words = graph_basis(graph)
                middle_graphs = [graph, *(
                    rebased_join(words, paths, a, b) for a, b in combinations(sorted(paths), 2)
                )]
                middle_count += graph_tests(graph)
                finals += sum(map(graph_tests, middle_graphs))
                if index in selected_sources:
                    middle_sample.extend(rng.sample(middle_graphs, 3))
                continue
            middle_choices = list(choices(graph, connectors))
            middle_count += len(middle_choices)
            nn = 2 * n + length - 1
            finals += len(middle_choices) * (1 + nn * (nn - 1) // 2)
            if index in selected_sources:
                for a, b, w in rng.sample(middle_choices, 3):
                    middle = bridged_overgroup(graph, a, b, w)
                    assert len(middle) // 4 == nn
                    middle_sample.append(middle)
        assert middle_count == row["middle_overgroups"] == row["certified_middle_overgroups"]
        assert finals == row["final_graphs"] == row["DAG_excluded"]
        assert row["primitive_positives"] == row["incomplete"] == row["exact_excluded"] == 0
        assert all(signed_graphs_acyclic(g) for g in middle_sample)
        sent, state_count = refold_samples(middle_sample, seed + length)
        selected += len(middle_sample)
        tested += sent
        exact_states += state_count
    return {
        "sampled_middle_overgroups": selected,
        "independent_last_join_refolds": tested,
        "independent_exact_closed_map_states": exact_states,
    }


def ak2_control(receipt, exceptions):
    p, b, bridge = AK2
    words = p, bridge + b + inverse(bridge)
    core = fold(words)
    prior = audit_joins(words, core)
    assert prior["checked_joins"] == prior["dag_exclusions"] == 55
    lines = exceptions.read_text().splitlines()
    assert len(lines) == sum(r["primitive_positives"] for r in receipt["by_middle_gap_length"])
    assert all(json.loads(line)["status"] == "PRIMITIVE" for line in lines)
    witness = json.loads(lines[0])
    assert witness["root"] == list(AK2)
    assert witness["middle"] == [0, 5, ""]
    # Native vertex 5 is the attachment of the second lobe. Its rebased
    # generators are obtained along the one-edge connector.
    middle = fold([*words, *(reduce(inverse(bridge) + h + bridge) for h in words)])
    assert decide(middle)["status"] == "ABSENT"
    paths, *_ = spanning(middle)
    final = rebased_join(graph_basis(middle), paths, *witness["last"])
    assert list(final) == witness["graph"]
    assert follow(final, 0, witness["based_word"]) == 0
    u, v = witness["alphabet"]
    for operation in witness["program"]:
        if operation == "R":
            u += v
        else:
            assert operation == "L"
            v = u + v
    assert (u, v)[witness["component"]] == witness["primitive"]
    return {
        "prior_two_copy_audit": prior,
        "first_positive_outer_join": {k: v for k, v in witness.items() if k != "graph"},
    }


def literal_iteration(receipt, exceptions):
    root = fold((POWER, BRAID))

    def joins(graph):
        paths, *_ = spanning(graph)
        words = graph_basis(graph)
        yield graph
        for a, b in combinations(sorted(paths), 2):
            yield rebased_join(words, paths, a, b)

    first = list(joins(root))
    second = [last for graph in first for last in joins(graph)]
    stages = receipt["stages"]
    assert receipt["source_vertices"] == len(root) // 4 == 10
    counts = [1, len(first), len(second), sum(map(graph_tests, second))]
    assert [row["graphs"] for row in stages] == counts
    for row in stages[:3]:
        assert row["DAG_excluded"] == row["graphs"]
        assert row["exact_excluded"] == row["primitive_positives"] == row["incomplete"] == 0
    last = stages[-1]
    assert last["DAG_excluded"] + last["exact_excluded"] + last["primitive_positives"] == counts[-1]
    assert last["incomplete"] == 0

    witness = json.loads(exceptions.read_text().splitlines()[0])
    assert witness["path"] == [[0, 1], [0, 1], [0, 19]]
    graph = root
    formations = []
    for a, b in witness["path"]:
        paths, *_ = spanning(graph)
        words = graph_basis(graph)
        assert decide(graph)["status"] == "ABSENT"
        formations.append({
            "source_vertices": len(graph) // 4, "source_rank": len(words),
            "tree_path_to_first_vertex": paths[a], "tree_path_to_second_vertex": paths[b],
        })
        graph = rebased_join(words, paths, a, b)
    assert list(graph) == witness["graph"] == [0, 0, 0, 0]
    assert witness["primitive"] == witness["based_word"] == "x"
    return {"native": receipt, "independent": {"counts": counts, "formations": formations, "witness": witness}}


def middle_bridge_family():
    p, b, first = "YYYYxxx", BRAID, "x"
    core = fold((p, first + b + inverse(first)))
    right = follow(core, 0, first)
    samples = []
    for m in (0, 1, 4, 20):
        read_forward = first + (b + inverse(first) + p + first) * m
        q = read_forward + "YY" + first
        assert reduce(q) == q and follow(core, 0, read_forward) == right
        assert q[0] in free_directions(p) and inverse(q[-1]) in free_directions(b)
        assert follow(core, right, "Y") == -1
        assert follow(core, right, inverse(first)) == 0 and follow(core, 0, "y") == -1
        samples.append({"parameter": m, "length": len(q), "residual": "YY"})
    return {"first_barbell": [p, b, first], "samples": samples}


def new_bridge_language():
    lobes, connectors = FIVE
    p, r, s, t, b = lobes
    c, d, e, f = connectors
    q0 = c + r + d + s + e + t + f
    graph = fold(basis(lobes, connectors))
    target = follow(graph, 0, connectors)
    assert reduce(q0) == q0 and follow(graph, 0, q0) == target
    assert follow(graph, 0, q0 + b + inverse(q0)) == 0

    older = [fold(basis(*source)) for source in four_chains()]
    assert len(older) == 7200
    assert starts_reading(older, q0) == starts_reading(older, inverse(q0)) == 0
    shortest_in_chart = []
    length_counts = []
    for length, paths in endpoint_paths(graph, target, free_directions(p), free_directions(b), len(q0)):
        if not paths:
            continue
        unreadable = sorted(w for w in paths if not starts_reading(older, w))
        if unreadable and not shortest_in_chart:
            shortest_in_chart = unreadable
        length_counts.append({
            "length": length, "legal_paths": len(paths), "unreadable_paths": len(unreadable),
        })
    assert len(shortest_in_chart) == 4 and len(shortest_in_chart[0]) == 17
    initial_rotation = "xyx"
    assert reduce(inverse(initial_rotation) + BRAID + initial_rotation) == b
    entry_controls = []
    for bridge in [shortest_in_chart[0], q0]:
        conjugator = reduce(bridge + inverse(initial_rotation))
        moves = [{"op": "conjugate", "i": 1, "g": c} for c in reversed(conjugator)]
        target_words = [p, bridge + b + inverse(bridge)]
        assert follow(graph, 0, target_words[1]) == 0
        checked = replay({
            "format": "ordinary-ac-elementary-v1",
            "start": [POWER, BRAID],
            "target": target_words,
            "moves": moves,
        })
        entry_controls.append({
            "bridge": bridge, "conjugator": conjugator,
            "strict_moves": checked["moves"], "endpoint": checked["endpoint"],
        })
    extended = set()
    for signs in product((t, inverse(t)), repeat=4):
        q = q0 + b + inverse(f)
        q += "".join(w + f + b + inverse(f) for w in signs)
        q += t + f
        assert reduce(q) == q and inverse(q[-1]) in free_directions(b)
        assert follow(graph, 0, q) == target
        assert follow(graph, 0, q + b + inverse(q)) == 0
        extended.add(q)
    assert len(extended) == 16
    return {
        "lobes": lobes,
        "connectors": connectors,
        "bridge": q0,
        "bridge_length": len(q0),
        "older_four_lobe_cores": len(older),
        "older_start_vertices_checked": sum(len(g) // 4 for g in older),
        "older_full_readings": 0,
        "older_one_letter_shorter_prefix_readings": starts_reading(older, q0[:-1]),
        "legal_endpoint_paths_by_length": length_counts,
        "shortest_escape_bridges_in_this_chart": shortest_in_chart,
        "strict_AK3_entries": entry_controls,
        "equal_length_extended_samples": len(extended),
        "extended_sample_length": len(next(iter(extended))),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    report = {}
    for i, mode in enumerate(("rotation", "short", "four", "five", "ak2_barbell")):
        native = json.loads((args.work / f"{mode}.json").read_text())
        exceptions = args.work / f"{mode}.exceptions.jsonl"
        if mode == "ak2_barbell":
            audit = ak2_control(native, exceptions)
        else:
            audit = audit_mode(mode, native, exceptions, 20261119 + i)
        report[mode] = {"native": native, "independent": audit}
    report["literal_zero_gap_iteration"] = literal_iteration(
        json.loads((args.work / "literal.json").read_text()),
        args.work / "literal.exceptions.jsonl",
    )
    report["long_middle_bridges"] = middle_bridge_family()
    report["outside_four_lobe_language"] = new_bridge_language()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
