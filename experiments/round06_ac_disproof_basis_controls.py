"""Independently replay simultaneous basis choices and rank-four join witnesses."""

import argparse
from itertools import combinations, groupby, product
import json
from pathlib import Path
import random

from elementary_verify import replay
from euclidean_primitive_audit import primitive_cyclic_word
from free_waypoint_search import conj_ops, normalize
from primitive_map_pairs import LETTERS, decide, fold, follow, inverse, reduce
from round02_ac_disproof_controls import signed_graphs_acyclic
from round05_ac_disproof_third_phase_audit import graph_basis
from stallings_search import apply
from v_vertex_identification import spanning


AK3 = ("xxxYYYY", "xyxYXY")
AK2 = ("xxYYY", "xyxYXY")


def abstract_reduce(word):
    stack = []
    for letter in word:
        if stack and stack[-1] == letter.swapcase():
            stack.pop()
        else:
            stack.append(letter)
    return "".join(stack)


def factor(letter):
    return int(letter.lower() in "cd")


def cyclic_syllables(word):
    syllables = ["".join(run) for _, run in groupby(abstract_reduce(word), factor)]
    while len(syllables) > 1 and factor(syllables[0][0]) == factor(syllables[-1][0]):
        combined = abstract_reduce(syllables[-1] + syllables[0])
        syllables = ([combined] if combined else []) + syllables[1:-1]
    return syllables


def strip_end_pairs(word, reducer=reduce):
    word = reducer(word)
    trim = 0
    while trim * 2 + 1 < len(word) and word[trim] == word[-1 - trim].swapcase():
        trim += 1
    return word[:trim], word[trim:len(word) - trim]


def cyclic_root(word):
    tail, cyclic = strip_end_pairs(word, abstract_reduce)
    for size in range(1, len(cyclic) + 1):
        if len(cyclic) % size == 0 and cyclic[:size] * (len(cyclic) // size) == cyclic:
            return tail + cyclic[:size] + inverse(tail)
    raise AssertionError("nonempty syllable required")


def basis_test(word):
    syllables = cyclic_syllables(word)
    if len(syllables) < 2:
        return {"status": "ONE_FACTOR", "syllables": syllables}
    roots, slopes = [], []
    for block, marked in enumerate(("ab", "cd")):
        factors = [item for item in syllables if factor(item[0]) == block]
        root = cyclic_root(factors[0])
        if any(abstract_reduce(root + item) != abstract_reduce(item + root) for item in factors):
            return {"status": "NONCYCLIC_BLOCK", "syllables": syllables, "obstructed_block": block}
        marked_image = root.translate(str.maketrans(marked + marked.upper(), "xyXY"))
        if not primitive_cyclic_word(strip_end_pairs(marked_image)[1]):
            return {"status": "NONPRIMITIVE_ROOT", "syllables": syllables, "root": root}
        roots.append(root)
        slopes.append([root.count(c) - root.count(c.upper()) for c in marked])
    (a, b), (c, d) = slopes
    determinant = a * d - b * c
    return {
        "status": "REALIZABLE" if abs(determinant) == 1 else "INCOMPATIBLE_SLOPES",
        "syllables": syllables, "roots": roots, "slopes": slopes, "determinant": determinant,
    }


def expand(word, marking):
    images = dict(zip("abcd", marking))
    images.update({letter.upper(): inverse(w) for letter, w in list(images.items())})
    return reduce("".join(images[c] for c in word))


def rebased_marks(rows, vertices):
    paths, *_ = spanning(fold(rows))
    return [reduce(inverse(paths[v]) + w + paths[v]) for v in vertices for w in rows]


def express(target, marks, budget=12):
    """Find the word in the four-copy marking via exact bidirectional equality."""
    signed = [(letter, word) for name, w in zip("abcd", marks)
              for letter, word in ((name, w), (name.upper(), inverse(w)))]
    visited = [{"": ""}, {target: ""}]
    frontier = [dict(side) for side in visited]
    for _ in range(budget):
        side = min(range(2), key=lambda i: len(frontier[i]))
        following = {}
        for state, trace in frontier[side].items():
            for letter, image in signed:
                next_state = reduce(state + image)
                program = trace + letter
                if next_state in visited[1 - side]:
                    other = visited[1 - side][next_state]
                    found = program + inverse(other) if side == 0 else other + inverse(program)
                    assert expand(found, marks) == target
                    return abstract_reduce(found)
                if next_state not in visited[side]:
                    following[next_state] = program
        visited[side].update(following)
        frontier[side] = following
    return None


def positive_ak2():
    source = fold(AK2)
    assert signed_graphs_acyclic(source)
    examples = []
    for vertices in ((1, 4), (3, 7), (5, 6)):
        marks = rebased_marks(AK2, vertices)
        joint = fold(marks)
        assert len(graph_basis(joint)) == 4
        verdict = decide(joint)
        assert verdict["status"] == "PRIMITIVE"
        witness = verdict["witness"]
        based = witness["based_primitive_word"]
        word = express(based, marks)
        assert word is not None
        criteria = basis_test(word)
        assert criteria["status"] == "REALIZABLE"
        roots = [expand(root, marks) for root in criteria["roots"]]
        actual = fold(roots)
        cyclic = witness["cyclic_primitive_word"]
        assert primitive_cyclic_word(cyclic)
        assert any(follow(actual, v, cyclic) == v for v in range(len(actual) // 4))
        examples.append({
            "vertices": vertices, "ambient_primitive": cyclic, "abstract_word": word,
            "basis_test": criteria, "actual_placed_pair": roots,
        })
    return examples


def replay_ak2_entry(example):
    paths, *_ = spanning(fold(AK2))
    a, b = example["vertices"]
    assert example["abstract_word"] == "cDa"
    first, second = example["actual_placed_pair"]
    program = [{"op": "invert", "i": 1}, {"op": "multiply", "i": 1, "j": 0}]
    program += conj_ops(1, AK2[0])
    program += conj_ops(0, inverse(paths[a]))
    program += conj_ops(1, inverse(paths[b]))
    program.append({"op": "multiply", "i": 1, "j": 0})
    primitive = reduce(second + first)
    assert primitive_cyclic_word(strip_end_pairs(primitive)[1])
    ledger = {"format": "ordinary-ac-elementary-v1", "start": list(AK2),
              "target": [first, primitive], "moves": program}
    return {"ledger": ledger, "replayed": replay(ledger)}


def replay_new_ak3_branch():
    power, braid, bridge = "XYxxxYYYYxyxY", "YXYxyx", "Y"
    original = fold(AK3)
    first_vertices = [v for v in range(len(original) // 4) if follow(original, v, power) == v]
    second_vertices = [v for v in range(len(original) // 4) if follow(original, v, braid) == v]
    assert len(first_vertices) == len(second_vertices) == 1
    assert follow(original, first_vertices[0], bridge) < 0
    assert follow(original, second_vertices[0], inverse(bridge)) < 0
    assert bridge not in (power[0], inverse(power[-1]), inverse(braid[0]), braid[-1])

    product_move = {"op": "multiply", "i": 0, "j": 1}
    rows = apply(AK3, product_move)
    rows, a = normalize(rows, 0, power)
    rows, b = normalize(rows, 1, braid)
    bridge_moves = conj_ops(1, bridge)
    for move in bridge_moves:
        rows = apply(rows, move)
    first_placement = list(rows)
    assert first_placement == [power, bridge + braid + inverse(bridge)]
    moves = [product_move] + a + b + bridge_moves
    first_step = len(moves)
    rows = apply(rows, product_move)
    rows, a = normalize(rows, 0, strip_end_pairs(rows[0])[1])
    rows, b = normalize(rows, 1, strip_end_pairs(rows[1])[1])
    moves += [product_move] + a + b
    ledger = {"format": "ordinary-ac-elementary-v1", "start": list(AK3),
              "target": list(rows), "moves": moves}
    return {
        "first_placement": first_placement, "first_placement_step": first_step,
        "first_axes_gap": 1, "first_unread_gap": 1, "old_loop_vertices": first_vertices + second_vertices,
        "basis_masses": [3, 3], "second_axes_gap": 0, "ledger": ledger, "replayed": replay(ledger),
    }


def signed_pair(pair):
    return tuple(sorted(min(word, inverse(word)) for word in pair))


def direct_marked_bases(rows, bound):
    """At mass at most four at least one coordinate has norm one."""
    if not 2 <= bound <= 4:
        raise ValueError("independent normal forms are implemented for mass two to four")
    yield rows
    for initial, donor in (rows, rows[::-1]):
        for signed in (donor, inverse(donor)):
            for power in range(1, bound - 1):
                yield initial + signed * power, donor


def rotations(word):
    cyclic = strip_end_pairs(word)[1]
    return sorted({cyclic[i:] + cyclic[:i] for i in range(len(cyclic))})


def direct_placements(rows, bound, gap):
    if gap not in (0, 1):
        raise ValueError("independent placements cover gaps zero and one")
    for a, b in direct_marked_bases(rows, bound):
        for u, v in product(rotations(a), rotations(b)):
            yield signed_pair((u, v))
            if gap:
                unavailable = {u[0], inverse(u[-1]), inverse(v[0]), v[-1]}
                for c in LETTERS:
                    if c not in unavailable:
                        yield signed_pair((u, c + v + inverse(c)))


def graph_key(graph):
    codes = []
    for root in range(len(graph) // 4):
        if sum(v >= 0 for v in graph[root * 4:root * 4 + 4]) < 3:
            continue
        todo = [root]
        names = {root: 0, -1: -1}
        encoding = []
        for v in todo:
            for w in graph[v * 4:v * 4 + 4]:
                if w not in names:
                    names[w] = len(todo)
                    todo.append(w)
                encoding.append(names[w])
        assert len(encoding) == len(graph)
        codes.append(tuple(encoding))
    return min(codes)


def independent_census(native):
    a, b = native["first_basis_bound"], native["second_basis_bound"]
    first = set(direct_placements(AK3, a, native["first_geodesic_gap"]))
    second = set()
    for marking in first:
        second.update(direct_placements(marking, b, native["second_geodesic_gap"]))
    # The direct Nielsen words can orient a stored connector oppositely.
    # Labelled unbased core keys give the physical independent comparison.
    keys = {graph_key(fold(pair)) for pair in second}
    covered = sum(1 + (len(key) // 4) * (len(key) // 4 - 1) // 2 for key in keys)
    assert len(keys) == native["distinct_second_cores"]
    assert covered == native["vertex_pairs_covered"]
    rng = random.Random(741)
    sampled = 0
    for core in rng.sample(sorted(keys), min(len(keys), 12)):
        marks = graph_basis(core)
        paths, *_ = spanning(core)
        based = [[reduce(inverse(path) + w + path) for w in marks] for path in paths.values()]
        choices = list(combinations(range(len(based)), 2))
        for i, j in rng.sample(choices, min(12, len(choices))):
            fresh = fold(based[i] + based[j])
            assert signed_graphs_acyclic(fresh)
            sampled += 1
    return {"first_marked_pairs": len(first), "second_marked_pairs": len(second),
            "second_unbased_cores": len(keys), "third_join_placements_represented": covered,
            "independent_sampled_four_word_refolds": sampled}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipts", type=Path, nargs="+")
    parser.add_argument("--uncompressed", type=Path)
    args = parser.parse_args()
    replays = []
    for receipt in args.receipts:
        native = json.loads(receipt.read_text())
        assert native["primitive_positives"] == native["incomplete"] == 0
        replays.append({"native": native, "independent": independent_census(native)})
    positives = positive_ak2()
    controls = {
        "ak2_literal_positives": positives,
        "ak2_strict_path_to_primitive": replay_ak2_entry(positives[0]),
        "ak3_new_first_bridge_path": replay_new_ak3_branch(),
        "noncyclic_syllables": basis_test("acbd"),
        "slope_determinant": basis_test("acdd"),
        "nonprimitive_root": basis_test("abaBcd"),
    }
    assert controls["noncyclic_syllables"]["status"] == "NONCYCLIC_BLOCK"
    assert controls["slope_determinant"]["status"] == "INCOMPATIBLE_SLOPES"
    assert controls["nonprimitive_root"]["status"] == "NONPRIMITIVE_ROOT"
    receipt = {"bounded_basis_scans": replays, "rank_four_controls": controls}
    if args.uncompressed:
        raw = json.loads(args.uncompressed.read_text())
        assert raw["DAG_excluded"] == raw["vertex_pairs_covered"]
        assert raw["exact_excluded"] == raw["primitive_positives"] == raw["incomplete"] == 0
        matched = [r["native"] for r in replays
                   if all(raw[k] == r["native"][k] for k in ("first_basis_bound", "second_basis_bound",
                      "first_geodesic_gap", "second_geodesic_gap", "distinct_second_cores", "vertex_pairs_covered"))]
        assert len(matched) == 1 and matched[0]["DAG_excluded"] < raw["DAG_excluded"]
        receipt["uncompressed_control"] = raw
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
