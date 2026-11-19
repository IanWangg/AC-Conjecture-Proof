"""Prepare the fibre tests and compile a positive result into ordinary AC moves."""

import argparse
import hashlib
import json
from itertools import product
from pathlib import Path

from complete_primitive import complete, substitute
from elementary_verify import inverse, reduce, replay
from h_basis_bridge import reverse_ledger, spanning_basis
from round01_ak3_archive import expand, pair_key
from stallings_search import LETTERS, apply, graph, nielsen_move


FORWARD = (
    ("XXyXYYYxxYxyy", "XYxYYxY"),
    ("XXyyxYxyxYYXy", "XYxYYxY"),
    ("xxxYYYY", "xyxYXY"),
    ("xxYYYXYXXyxyxxxxxYYYXYXy", "XYXYxxyxyyyXX"),
)
CONTROLS = (("xyxyXY", "yxyXY"), ("x", "yXyxYx"))


def dump_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def write_pairs(path, entries):
    path.write_text("".join("\t".join(entry) + "\n" for entry in entries))


def vector(word):
    return tuple(word.count(c) - word.count(c.upper()) for c in "xy")


def graph_key(encoded, vertices):
    words = []
    for root in range(vertices):
        names = {root: 0}
        queue = [root]
        code = []
        for i in queue:
            for j in encoded[4 * i : 4 * i + 4]:
                if j >= 0 and j not in names:
                    names[j] = len(queue)
                    queue.append(j)
                code.append(names.get(j, -1))
        assert len(queue) == vertices
        words.append(tuple(code))
    return min(words)


def rotations(word):
    return tuple(word[i:] + word[:i] for i in range(len(word)))


def prepare(directory, catalogue):
    directory.mkdir(parents=True, exist_ok=True)
    write_pairs(directory / "sources.tsv", FORWARD)
    write_pairs(directory / "ctlA.tsv", [CONTROLS[0]])
    write_pairs(directory / "ctlB.tsv", [CONTROLS[1]])
    write_pairs(directory / "ctlA_canonical.tsv", [pair_key(CONTROLS[0])])
    write_pairs(directory / "ctlB_canonical.tsv", [pair_key(CONTROLS[1])])

    all_roots = product(*(rotations(word) for word in FORWARD[2]))
    unique_roots = {}
    for words in all_roots:
        unique_roots.setdefault(graph_key(*graph(words)), words)
    assert len(unique_roots) == 21
    write_pairs(directory / "sources_initial_rotations.tsv", unique_roots.values())
    targets = [tuple(row.split()) for row in catalogue.read_text().splitlines()]
    for cap in (32, 44):
        rows = [words for words in targets if sum(map(len, words)) <= cap]
        write_pairs(directory / f"reverse{cap}.tsv", rows)


def core_and_tail(word):
    cutoff = 0
    while len(word) - 2 * cutoff > 1 and word[cutoff] == word[-1 - cutoff].swapcase():
        cutoff += 1
    return word[cutoff : len(word) - cutoff], word[:cutoff]


def conjugator(start, target):
    core, tail = core_and_tail(start)
    dest, stem = core_and_tail(target)
    for i, image in enumerate(rotations(core)):
        if image == dest:
            g = reduce(stem + inverse(core[:i]) + inverse(tail))
            assert reduce(g + start + inverse(g)) == target
            return g
    raise ValueError(f"nonconjugate free words: {start!r} and {target!r}")


def standard_with_vectors(columns):
    (a, b), (c, d) = [list(x) for x in columns]
    assert abs(a * d - b * c) == 1
    matrix = [[a, b], [c, d]]
    steps = []

    def swap():
        matrix.reverse()
        steps.append(("swap",))

    def negate(i):
        matrix[i] = [-e for e in matrix[i]]
        steps.append(("invert", i))

    def add(i, coefficient):
        for _ in range(abs(coefficient)):
            steps.append(("add", i, coefficient < 0))
        matrix[i] = [e + coefficient * f for e, f in zip(matrix[i], matrix[1 - i])]

    while matrix[1][0] != 0:
        add(0, -(matrix[0][0] // matrix[1][0]))
        swap()
    if matrix[0][0] < 0:
        negate(0)
    if matrix[1][1] < 0:
        negate(1)
    add(0, -matrix[0][1])
    assert matrix == [[1, 0], [0, 1]]
    moves = []
    words = ("x", "y")
    for op in reversed(steps):
        if op[0] == "add":
            _, i, negative = op
            words, part = nielsen_move(words, i, False, not negative)
        else:
            part = expand(words, op, undo=True)
            for move in part:
                words = apply(words, move)
        moves.extend(part)
    assert list(map(vector, words)) == list(columns)
    return words, moves


def compile_side(words, matches, coordinate):
    encoded, _ = graph(words)
    _, basis, rewrite, _ = spanning_basis(encoded, 0)
    start_marked = list(map(rewrite, words))
    moves = complete({
        "format": "ordinary-ac-elementary-v1", "start": start_marked,
        "target": start_marked, "moves": [],
    })["moves"]
    marked = [item[coordinate] for item in matches]
    word_basis, finish = standard_with_vectors(list(map(vector, marked)))
    assert all(conjugator(w, reduce(m)) is not None for w, m in zip(word_basis, marked))

    strict_moves = []
    state = tuple(words)

    def emit(move):
        nonlocal state
        state = apply(state, move)
        strict_moves.append(move)

    def conjugate(i, g):
        for c in reversed(g):
            emit({"op": "conjugate", "i": i, "g": c})

    for move in moves + finish:
        if move["op"] == "conjugate":
            conjugate(move["i"], substitute(move["g"], basis))
        else:
            emit(move)
    assert tuple(substitute(w, basis) for w in word_basis) == state
    for i, item in enumerate(matches):
        conjugate(i, conjugator(state[i], item["ambient"]))
    return strict_moves


def compile_join(data):
    assert data["status"] == "MATCH"
    left = compile_side(data["left"], data["loops"], "left_marked")
    right = compile_side(data["right"], data["loops"], "right_marked")
    certificate = {
        "format": "ordinary-ac-elementary-v1", "start": data["left"], "target": data["right"],
        "moves": left + reverse_ledger(right),
    }
    return certificate, replay(certificate)


def summarize(directory):
    def load(name):
        return json.loads((directory / name).read_text())

    def exact(data, sources, target_count):
        assert data["target_mode"] == "all_tails"
        assert data["target_rows"] == target_count
        assert len(data["sources"]) == sources
        for row in data["sources"]:
            assert row["max_cyclic_components"] <= 1
            assert row["rank_two_products"] == row["full_ambient_targets"]
            assert row["source_passes_direct_DAG_test"] == 1
            assert row["multilift_barbells"] == row["rank_filtered_barbells"]
            assert row["inconclusive_lattice"] == 0
            assert row["unresolved_two_lobes"] == 0
        return data

    control = load("control_fiber.json")
    _, replayed = compile_join(control)
    prior = load("control_older.json")
    assert prior["status"] == "COMPLETE_NO_ALL_TAIL_SUBGROUP_MATCH"
    names = ("sources.tsv", "sources_initial_rotations.tsv", "reverse32.tsv", "reverse44.tsv")
    return {
        "status": "COMPLETE_NO_JOIN_IN_TESTED_SCOPE",
        "ordinary_AK3_trivialization_found": False,
        "input_sha256": {
            name: hashlib.sha256((directory / name).read_bytes()).hexdigest() for name in names
        },
        "four_waypoints": exact(load("fiber_tails44.json"), 4, 16943),
        "initial_rotation_cores": exact(load("fiber_initial_rotations.json"), 21, 9257),
        "independent_direct_audit": load("fiber_direct_audit.json"),
        "positive_control": {
            "previous_test": prior,
            "fiber_join": control,
            "strict_replay": replayed,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_subparsers(dest="action", required=True)
    prep = action.add_parser("prepare")
    prep.add_argument("directory", type=Path)
    prep.add_argument("archive_tsv", type=Path)
    positive = action.add_parser("compile")
    positive.add_argument("join", type=Path)
    positive.add_argument("certificate", type=Path)
    report = action.add_parser("summary")
    report.add_argument("directory", type=Path)
    report.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.action == "prepare":
        prepare(args.directory, args.archive_tsv)
    elif args.action == "compile":
        cert, info = compile_join(json.loads(args.join.read_text()))
        dump_json(args.certificate, cert)
        print(json.dumps(info))
    else:
        dump_json(args.output, summarize(args.directory))


if __name__ == "__main__":
    main()
