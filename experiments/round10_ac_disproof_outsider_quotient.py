"""Test cyclic sign-pure words in the free quotient of rank-four extensions."""

import argparse
import base64
from collections import Counter, deque
import gzip
import hashlib
from itertools import combinations
import json
from math import gcd
from pathlib import Path

from elementary_verify import replay
from free_waypoint_search import conj_ops
from primitive_map_pairs import LETTERS, decide, fold, follow, inverse, verify_absence
from round10_one_outside_kernel import build
from stallings_search import reduce
from v_vertex_identification import fold_identification, spanning
from verify_second_phase import verify_potentials
from verify_vertex_voltage import loop_voltage, verify

ROOT = Path(__file__).resolve().parents[1]
CHORDS = "abcdefgh"
ALPHABETS = ("xy", "xY", "Xy", "XY")


def substitute(word, images):
    return reduce("".join(images[letter] for letter in word))


def chord_words(graph, words):
    _, chords, arcs, _ = spanning(graph)
    assert len(chords) == len(words) <= len(CHORDS)
    result = []
    for word in words:
        at = 0
        read = []
        for letter in word:
            signed = LETTERS.index(letter)
            end = graph[4 * at + signed]
            assert end >= 0
            chord = arcs.get((at, signed, end))
            if chord is not None:
                i, sign = chord
                read.append(CHORDS[i] if sign > 0 else CHORDS[i].upper())
            at = end
        assert at == 0
        result.append(reduce("".join(read)))
    return tuple(result), arcs


def shorten_once(rows, expressions):
    """Find a shorter basis through non-increasing elementary Nielsen moves."""
    initial_total = sum(map(len, rows))
    seen = {rows}
    search = deque([(rows, expressions)])
    while search:
        previous, old_expressions = search.popleft()
        for i, row in enumerate(previous):
            for j, donor in enumerate(previous):
                if i == j:
                    continue
                for sign in (1, -1):
                    factor = donor if sign > 0 else inverse(donor)
                    expr = old_expressions[j] if sign > 0 else inverse(old_expressions[j])
                    for left in (False, True):
                        replacement = reduce(factor + row if left else row + factor)
                        if len(replacement) > len(row):
                            continue
                        changed = previous[:i] + (replacement,) + previous[i + 1:]
                        if changed in seen:
                            continue
                        old_expression = old_expressions[i]
                        new_expression = reduce(expr + old_expression if left else old_expression + expr)
                        new_expressions = old_expressions[:i] + (new_expression,) + old_expressions[i + 1:]
                        if sum(map(len, changed)) < initial_total:
                            return changed, new_expressions
                        seen.add(changed)
                        search.append((changed, new_expressions))
    raise ValueError(f"Nielsen plateau lacked a decreasing move: {rows}")


def invert_marking(marking):
    names = CHORDS[:len(marking)]
    rows, expressions = marking, tuple(names)
    while any(len(row) != 1 for row in rows):
        rows, expressions = shorten_once(rows, expressions)
    inverted = {}
    for row, expression in zip(rows, expressions):
        inverted[row] = expression
        inverted[row.swapcase()] = inverse(expression)
    original = dict(zip(names, marking))
    original.update({name.upper(): inverse(word) for name, word in zip(names, marking)})
    assert set(inverted) == set(original)
    for chord, expression in inverted.items():
        assert substitute(expression, original) == chord
    for name, word in original.items():
        assert substitute(word, inverted) == name
    return inverted


def quotient_weights(graph, rows):
    marking, arcs = chord_words(graph, rows)
    expressions = invert_marking(marking)
    weights = [""] * len(graph)
    for (source, signed, _), (chord, sign) in arcs.items():
        label = CHORDS[chord] if sign > 0 else CHORDS[chord].upper()
        weights[4 * source + signed] = reduce(expressions[label].translate(str.maketrans("", "", "aAbB")))
    return weights, expressions


def saturate_identity(edges, size):
    """Return a relation with proof paths for exactly identity-labelled input paths."""
    nullable = [{i: ""} for i in range(size)]
    outgoing = [{} for _ in range(size)]
    for source, target, quotient_letter, ambient_letter in edges:
        if not quotient_letter:
            nullable[source].setdefault(target, ambient_letter)
        else:
            outgoing[source].setdefault(quotient_letter, []).append((target, ambient_letter))
    while True:
        old_size = sum(map(len, nullable))
        for middle in range(size):
            for source in range(size):
                if middle in nullable[source]:
                    prefix = nullable[source][middle]
                    for target, suffix in tuple(nullable[middle].items()):
                        if target not in nullable[source]:
                            nullable[source][target] = prefix + suffix
        for source, by_label in enumerate(outgoing):
            for letter, beginnings in by_label.items():
                for middle, prefix in beginnings:
                    for end, interior in tuple(nullable[middle].items()):
                        for target, suffix in outgoing[end].get(letter.swapcase(), ()):
                            if target not in nullable[source]:
                                nullable[source][target] = prefix + interior + suffix
        if old_size == sum(map(len, nullable)):
            return nullable


def check_closed_identity(edges, relation):
    """Recheck the finite inclusion certificate without using witness strings."""
    pairs = [set(row) for row in relation]
    for source, ends in enumerate(pairs):
        assert source in ends and all(pairs[end] <= ends for end in ends)
    for source, target, label, _ in edges:
        if not label:
            assert target in pairs[source]
    labelled_edges = [(a, b, c) for a, b, c, _ in edges if c]
    for a, b, c in labelled_edges:
        for p, q, d in labelled_edges:
            if d == c.swapcase() and p in pairs[b]:
                assert q in pairs[a]


def exact_cycle(graph, weights, alphabet, blocked):
    """Decide whether the cyclic language has a nonempty path of weight one."""
    letters = tuple(map(LETTERS.index, alphabet))
    states = [(vertex, j) for vertex in range(len(graph) // 4) for j, letter in enumerate(letters)
              if graph[4 * vertex + letter] >= 0]
    names = {state: k for k, state in enumerate(states)}
    arcs = []
    size = len(states)
    for start, (vertex, j) in enumerate(states):
        letter = letters[j]
        end = graph[4 * vertex + letter]
        weight = weights[4 * vertex + letter]
        for k in range(2):
            if j == k == blocked or (end, k) not in names:
                continue
            source = start
            for i, value in enumerate(weight or "_"):
                target = names[end, k]
                if i + 1 < len(weight):
                    target = size
                    size += 1
                arcs.append((source, target, "" if value == "_" else value, alphabet[j] if i == 0 else ""))
                source = target
    # Flag an actual edge, including an edge with epsilon quotient label.
    layered = [(u + layer * size, v + size, label, letter)
               for u, v, label, letter in arcs for layer in (0, 1)]
    relation = saturate_identity(layered, 2 * size)
    check_closed_identity(layered, relation)
    for v, (vertex, _) in enumerate(states):
        if v + size in relation[v]:
            word = relation[v][v + size]
            assert word and follow(graph, vertex, word) == vertex
            assert not any(letter in word for letter in set(LETTERS) - set(alphabet))
            assert 2 * alphabet[blocked] not in word + word[0]
            assert weight_of_loop(graph, weights, word, vertex) == ""
            return {"alphabet": alphabet, "blocked": alphabet[blocked], "vertex": vertex, "word": word}
    return None


def weight_of_loop(graph, weights, word, vertex):
    at = vertex
    out = []
    for letter in word:
        edge = 4 * at + LETTERS.index(letter)
        out.append(weights[edge])
        at = graph[edge]
        assert at >= 0
    assert at == vertex
    return reduce("".join(out))


def primitive_word(word):
    size = len(word)
    y = sum(letter in "yY" for letter in word)
    if gcd(size, y) != 1:
        return False
    euclid = "".join("y" if (i + 1) * y // size > i * y // size else "x" for i in range(size))
    return word.lower() in euclid + euclid


def audit_historical():
    old = json.loads((ROOT / "certificates/v_vertex_identification_results.json").read_text())
    encoded = (ROOT / "certificates/x_second_phase_data.json.gz.b64").read_text()
    historical = json.loads(gzip.decompress(base64.b64decode(encoded)))
    records = historical["extensions"]["records"]
    classified = {row["second_identification_index"]: row["status"]
                  for row in historical["affine_parameters"]["records"]}
    abelian = {row["second_identification_index"]: row["witness"]
               for row in historical["uniform_primitives"]["records"] if row["witness"]}
    base = old["original_pair"]
    cache, counts, cases = {}, Counter(), []
    expected = {(p, a, b) for p, parent in enumerate(old["records"])
                for a, b in combinations(range(len(parent["graph"]) // 4), 2)}
    assert {(row["first_case_index"], *row["second_vertices"]) for row in records} == expected
    for index, row in enumerate(records):
        parent = old["records"][row["first_case_index"]]
        a, b = row["second_vertices"]
        graph, _ = fold_identification(parent["graph"], a, b)
        assert list(graph) == row["graph"]
        rank = sum(end >= 0 for end in graph) // 2 + 1 - len(graph) // 4
        assert row["rank"] == rank
        counts[f"rank_{rank}"] += 1
        if rank != 4:
            continue
        paths, *_ = spanning(parent["graph"])
        outside = [parent["extra_generator"], reduce(paths[a] + inverse(paths[b]))]
        assert fold(base + outside) == graph
        weights, expressions = quotient_weights(graph, base + outside)
        assert [weight_of_loop(graph, weights, word, 0) for word in base + outside] == ["", "", "c", "d"]
        if graph not in cache:
            hits = [hit for alphabet in ALPHABETS for blocked in (0, 1)
                    if (hit := exact_cycle(graph, weights, alphabet, blocked)) is not None]
            cache[graph] = hits
        hits = cache[graph]
        # Different pair histories can change quotient markings. Recheck actual identities.
        assert all(not weight_of_loop(graph, weights, hit["word"], hit["vertex"]) for hit in hits)
        status = "excluded" if not hits else "primitive" if any(primitive_word(h["word"]) for h in hits) else "unresolved"
        counts[status] += 1
        classification = classified[index]
        counts[f"{classification}/{status}"] += 1
        abelian_weight = None
        if index in abelian:
            word = abelian[index]["cyclic_word"]
            abelian_weight = weight_of_loop(graph, weights, word, abelian[index]["loop_vertex"])
            assert not abelian_weight or all(abelian_weight.count(c) == abelian_weight.count(c.upper()) for c in "cd")
            counts["old_abelian_primitive_survives" if not abelian_weight else "old_abelian_primitive_rejected"] += 1
            if not abelian_weight:
                assert hits and primitive_word(word)
        cases.append({"second_index": index, "status": status, "prior_status": classification,
                      "inverse_marking": [expressions[c] for c in CHORDS[:rank]], "witnesses": hits,
                      "old_abelian_primitive_free_image": abelian_weight})
    return {"counts": dict(sorted(counts.items())), "distinct_rank_four_graphs": len(cache), "rank_four_cases": cases}, set(cache)


def graph_rank(graph):
    return sum(end >= 0 for end in graph) // 2 + 1 - len(graph) // 4


def principal_quotients(base):
    original = fold(base)
    seen = {original}
    todo = [original]
    outgoing = {}
    for graph in todo:
        children = []
        for a, b in combinations(range(len(graph) // 4), 2):
            child, _ = fold_identification(graph, a, b)
            children.append((child, a, b))
            if child not in seen:
                seen.add(child)
                todo.append(child)
        outgoing[graph] = children
    return outgoing


def ranked_outsiders(base, table):
    initial = fold(base)
    outsiders = {initial: ()}
    todo = [initial]
    for graph in todo:
        paths, *_ = spanning(graph)
        rank = graph_rank(graph)
        for child, a, b in table[graph]:
            if child in outsiders or graph_rank(child) != rank + 1:
                continue
            outsiders[child] = outsiders[graph] + (reduce(paths[a] + inverse(paths[b])),)
            todo.append(child)
    return outsiders


def audit_principal(base, historical_rank_four=None):
    table = principal_quotients(base)
    original = fold(base)
    assert {graph for graph in table if graph_rank(graph) == 2} == {original, fold(("x", "y"))}
    if historical_rank_four is not None:
        assert {graph for graph in table if graph_rank(graph) == 4} == historical_rank_four
    outsiders = ranked_outsiders(base, table)
    counts = Counter()
    cases = []
    for graph in sorted(table, key=lambda graph: (graph_rank(graph), graph)):
        rank = graph_rank(graph)
        if rank < 3:
            continue
        if graph not in outsiders:
            counts[f"rank_{rank}_not_covered"] += 1
            cases.append({"graph": graph, "rank": rank, "status": "not_covered"})
            continue
        rows = base + list(outsiders[graph])
        assert fold(rows) == graph
        weights, expressions = quotient_weights(graph, rows)
        assert [weight_of_loop(graph, weights, word, 0) for word in rows] == ["", "", *CHORDS[2:rank]]
        hits = [hit for alphabet in ALPHABETS for blocked in (0, 1)
                if (hit := exact_cycle(graph, weights, alphabet, blocked)) is not None]
        status = "excluded" if not hits else "primitive" if any(primitive_word(h["word"]) for h in hits) else "unresolved"
        counts[f"rank_{rank}_{status}"] += 1
        cases.append({"graph": graph, "rank": rank, "outsiders": outsiders[graph], "status": status,
                      "inverse_marking": [expressions[c] for c in CHORDS[:rank]], "witnesses": hits})
    original_absence = verify_absence(decide(original, save_certificate=True))
    return {"base": base, "principal_quotients_by_rank": dict(sorted(Counter(map(graph_rank, table)).items())),
            "source_primitive_map_pairs_checked": original_absence["closed_map_pair_states_checked"],
            "counts": dict(sorted(counts.items())), "cases": cases}


def audit_nested(maximum=6):
    control = json.loads((ROOT / "results/round09_bridge_collar_control.json").read_text())
    left, right = control["lobes"]
    old_bridge = control["bridge"]
    report = {}
    candidates = ["X"]
    for length in range(2, maximum + 1):
        candidates = [p + c for p in candidates for c in LETTERS if c != p[-1].swapcase()]
        counts = Counter()
        for bridge in (word for word in candidates if word[-1] == "y"):
            pair = [left, bridge + right + inverse(bridge)]
            original = control["entry"]
            moves = original["moves"] + conj_ops(1, reduce(bridge + inverse(old_bridge)))
            replay({**original, "moves": moves, "target": pair})
            finite = build(pair)
            checked = verify(finite["identifications"], finite["potentials"])
            counts["bridges"] += 1
            for key in ("vertex_identifications_independently_refolded", "signed_double_free_graphs_independently_reconstructed",
                        "cyclic_components_independently_recognized", "integer_potential_inequalities_checked"):
                counts[key] += checked[key]
        report[length] = dict(counts)
    return report


def audit_controls():
    original = json.loads((ROOT / "certificates/v_ak2_vertex_identification_results.json").read_text())
    count = 0
    for row in original["records"]:
        known = row["kernel_primitive_witness"]
        if known is None:
            continue
        graph = tuple(row["graph"])
        generators = original["original_pair"] + [row["extra_generator"]]
        assert fold(generators) == graph
        weights, _ = quotient_weights(graph, generators)
        word, vertex = known["cyclic_word"], known["loop_vertex"]
        assert primitive_word(word) and not weight_of_loop(graph, weights, word, vertex)
        assert any(exact_cycle(graph, weights, signs, forbidden) for signs in ALPHABETS for forbidden in (0, 1))
        count += 1
    assert count == 3
    return {"known_primitive_kernel_witnesses_replayed": count, "source": original["original_pair"]}


def audit_rank_three_exception(ak3):
    report = json.loads((ROOT / "results/round10_rank_three_overgroups.json").read_text())["AK3"]
    missed = [list(row["graph"]) for row in ak3["cases"] if row["status"] == "not_covered"]
    exceptional = report["rank_three_additional_cores"]
    assert [row["graph"] for row in exceptional] == missed
    assert len(missed) == 1
    row, = exceptional
    graph, weights = row["graph"], row["edge_voltages"]
    assert all(loop_voltage(graph, weights, word) == 0 for word in ak3["base"])
    for at in range(len(graph) // 4):
        for i in range(4):
            target = graph[4 * at + i]
            if target >= 0:
                assert weights[4 * at + i] == -weights[4 * target + (i ^ 1)]
    inequalities = verify_potentials(graph, weights, row["certificate"])
    assert inequalities == row["inequalities"] == 24
    literal_rows, _ = chord_words(graph, ak3["base"] + ["x"])
    assert literal_rows == ("aaabb", "aC", "a")
    return {"graph": graph, "inequalities_independently_checked": inequalities,
            "marked_source_rows_in_chord_basis": literal_rows[:2]}


def summarize(result, name):
    cases = result.pop(name)
    result["case_digest_sha256"] = hashlib.sha256(json.dumps(cases, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result["first_not_covered_graphs"] = [row["graph"] for row in cases if row["status"] == "not_covered"]
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true", help="retain per-quotient inverse markings and outcomes")
    args = parser.parse_args()
    historical, graphs = audit_historical()
    ak3 = audit_principal(["xxxYYYY", "xyxYXY"], graphs)
    energy17 = audit_principal(["xxyXYXy", "xxYXYxYYXY"])
    exceptional = audit_rank_three_exception(ak3)
    assert all(row["status"] in {"excluded", "not_covered"} for row in ak3["cases"])
    assert all(row["status"] == "excluded" for row in energy17["cases"])
    if not args.full:
        rejected = next(row for row in historical["rank_four_cases"] if row["old_abelian_primitive_free_image"])
        historical["first_rejected_abelian_witness"] = rejected
        summarize(historical, "rank_four_cases")
        summarize(ak3, "cases")
        summarize(energy17, "cases")
    print(json.dumps({"research_x_double_identifications": historical, "ak3": ak3, "energy17": energy17,
                      "exceptional_ak3_rank_three_voltage_replay": exceptional,
                      "nested_bridges": audit_nested(), "positive_control": audit_controls()}, indent=2))
