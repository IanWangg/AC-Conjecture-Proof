"""Alternate receivers on both sides, then search directly for finite-chart joins."""

import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from hashlib import sha256
import json
from pathlib import Path
import subprocess

from elementary_verify import replay
from free_waypoint_search import canonical
from round01_ak3_archive import FILE_PATTERNS, REVERSE_ARCHIVE, certificate, entries, trace
from round05_ak3_orbit_audit import MAPS
from round07_automorphism_transport import normalize_pair
from round08_ac_proof_two_donors import reverse_moves
from round08_ak3_acm_replay import compile_move
from round08_ak3_acm_search import cyclic_peak, order, record, scan, search


ROOT = Path(__file__).resolve().parents[1]
LEDGERS = {
    "waypoint": "round10_ak3_e17_cap32.json",
    "wrong": "round10_stable_proof_wirtinger_wrong.json",
    "correct": "round10_stable_proof_wirtinger_correct.json",
}
START = ("xxxYYYY", "xyxYXY")
BASIS = ("x", "y")
PARAMETERS = {"stages": 5, "allocation_cap": 300000, "horizon": 24, "bases": 96,
              "beam": 72, "alternations": 7, "maximum_energy": 42, "workers": 4}
QUICK = {"stages": 3, "allocation_cap": 90000, "horizon": 20, "bases": 32,
         "beam": 16, "alternations": 4}


def load(name):
    result = json.loads((ROOT / "certificates" / LEDGERS[name]).read_text())
    replay(result)
    return result


def nodes_of(name, executable):
    settings = PARAMETERS
    ledger = load(name)
    seed = tuple(ledger["start"] if name == "correct" else ledger["target"])
    runner = partial(scan, executable, settings["stages"], settings["allocation_cap"],
                     settings["horizon"], settings["bases"])
    report, nodes = search(name, seed, runner, settings["beam"], settings["alternations"],
                           settings["maximum_energy"], settings["workers"])
    nodes.extend((seed, slot, ()) for slot in (0, 1))
    best = {}
    for node in sorted(nodes, key=order):
        best.setdefault(node[0], node)
    return report, list(best.values())


def targeted(executable, pair, receiver, words):
    settings = PARAMETERS
    return json.loads(subprocess.check_output(
        [str(executable), pair[receiver], pair[1 - receiver], str(settings["stages"]),
         str(settings["allocation_cap"])], input="\n".join(words), text=True))


def add_targets(mapping, pair, source, map_index):
    image = tuple(canonical(word.translate(MAPS[map_index])) for word in pair)
    for slot in (0, 1):
        mapping[image[1 - slot]].setdefault(image[slot], source + (map_index,))


def target_index(archive, correct):
    mapping = defaultdict(dict)
    for node in correct:
        for map_index in range(len(MAPS)):
            add_targets(mapping, node[0], ("correct", node), map_index)
    locations = json.loads(archive.with_suffix(".sources.json").read_text())
    pairs = archive.read_text().splitlines()
    assert len(pairs) == len(locations)
    for row, location in zip(pairs, locations):
        pair = tuple(row.split())
        assert len(pair) == 2
        for map_index in range(len(MAPS)):
            add_targets(mapping, pair, ("archive", tuple(location)), map_index)
    return mapping


def directed_search(executable, nodes, mapping):
    queries = []
    hits = []
    for node in nodes:
        pair, _, _ = node
        for slot in (0, 1):
            targets = mapping.get(canonical(pair[1 - slot]))
            if targets:
                queries.append((node, slot, tuple(sorted(targets))))

    def task(item):
        node, slot, words = item
        return targeted(executable, node[0], slot, words)

    largest_graph = 0
    stops = 0
    with ThreadPoolExecutor(max_workers=PARAMETERS["workers"]) as executor:
        for (node, slot, _), receipt in zip(queries, executor.map(task, queries)):
            largest_graph = max(largest_graph, max(receipt["graph_sizes"]))
            stops += int(receipt["allocation_stop"])
            for word, stage in receipt["hits"]:
                hits.append((node, slot, word, stage, mapping[canonical(node[0][1 - slot])][word]))
    return {"charts": len(queries), "target_word_checks": sum(len(row[2]) for row in queries),
            "largest_graph": largest_graph, "allocation_stops": stops, "hits": len(hits)}, hits


def append_route(ledger, route):
    for slot, word, stage in route:
        suffix, _ = compile_move(tuple(ledger["target"]), slot, word, stage)
        ledger["moves"].extend(suffix["moves"])
        ledger["target"] = suffix["target"]


def reverse_suffix(source, archives):
    kind, details, index = source
    if kind == "correct":
        ledger = load("correct")
        from_correct = {"start": ledger["start"], "target": ledger["start"][:], "moves": []}
        append_route(from_correct, details[2])
        assert tuple(from_correct["target"]) == details[0]
        endpoint = tuple(from_correct["target"])
        instructions = list(reverse_moves(from_correct["moves"])) + ledger["moves"]
        target = BASIS
    else:
        member, step = details
        name, start, moves, printed = next(item for item in entries(archives, REVERSE_ARCHIVE, FILE_PATTERNS[1])
                                           if item[0] == member)
        states = list(trace(start, moves, printed, name))
        endpoint = states[step]
        suffix = certificate(endpoint, moves[step:])
        instructions = suffix["moves"]
        target = tuple(suffix["target"])
    marking = MAPS[index]
    marked = tuple(word.translate(marking) for word in endpoint)
    instructions = [{**move, "g": move["g"].translate(marking)} if move["op"] == "conjugate" else move
                    for move in instructions]
    target = tuple(word.translate(marking) for word in target)
    return marked, instructions + normalize_pair(target, BASIS)


def compile_join(name, hit, archives):
    node, slot, word, stage, source = hit
    ledger = load(name)
    append_route(ledger, node[2] + ((slot, word, stage),))
    receiver = tuple(ledger["target"])
    marked, moves_to_basis = reverse_suffix(source, archives)
    ledger["moves"].extend(normalize_pair(receiver, marked) + moves_to_basis)
    ledger["target"] = list(BASIS)
    replay(ledger)
    return ledger


def run(acm, target_acm, archive, archives, output_certificate):
    positive = targeted(target_acm, ("XXYYxyXyyxYY", "XXYYxyyyxYY"), 0,
                        ("X", "XXYxyXyxYY"))
    assert [word for word, _ in positive["hits"]] == ["X"]
    control, check = compile_move(("XXYYxyXyyxYY", "XXYYxyyyxYY"), 0, "X", positive["hits"][0][1])
    assert replay(control) == {field: check[field] for field in replay(control)}
    reverse_report, correct = nodes_of("correct", acm)
    mapping = target_index(archive, correct)
    receipts = {}
    for name in ("wrong", "waypoint"):
        report, nodes = nodes_of(name, acm)
        checked, hits = directed_search(target_acm, nodes, mapping)
        receipts[name] = {"beam": report, "distinct_marked_pairs": len(nodes), "direct_checks": checked,
                          "lowest_energy_pairs": [record(node) for node in sorted(nodes, key=order)[:6]]}
        if hits:
            ledger = compile_join(name, hits[0], archives)
            output_certificate.write_text(json.dumps(ledger, separators=(",", ":")) + "\n")
            receipts[name]["success"] = {**replay(ledger), "cyclic_peak": cyclic_peak(ledger)}
            break
    return {"parameters": PARAMETERS, "archive_tsv_sha256": sha256(archive.read_bytes()).hexdigest(),
            "positive_control": {"checks": positive, "strict_replay": replay(control)},
            "reverse_beam": reverse_report, "reverse_marked_pairs": len(correct),
            "reverse_donor_keys": len(mapping), "forward": receipts}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("acm", "target_acm", "archive", "archives", "output_certificate"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--quick", action="store_true")
    args = vars(parser.parse_args())
    if args.pop("quick"):
        PARAMETERS.update(QUICK)
    print(json.dumps(run(**args), indent=2))
