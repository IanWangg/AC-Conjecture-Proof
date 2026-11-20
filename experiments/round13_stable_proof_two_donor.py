"""Find single-occurrence chart relators in a two-donor finite completion."""

import argparse
from collections import deque
import json
from pathlib import Path

from free_waypoint_search import conj_ops
from round03_stable_proof_pivot import canonical, det
from round04_stable_proof_paths import replay
from round05_stable_proof_projections import each_available_chart
from round08_ak3_acm_replay import AnnotatedFold, donor_rotations, orient, word_power
from round11_stable_proof_reverse import certificate
from stallings_search import inverse, reduce


LETTERS = "xXyYzZ"
WIDTH = 10


def height_function(rows, receiver):
    fixed = [slot for slot in range(3) if slot != receiver]
    denominator = det([rows[i] for i in [receiver, *fixed]])
    assert abs(denominator) == 1
    return {a: det([a, *(rows[i] for i in fixed)]) // denominator for a in LETTERS}


def harvest(graph, paths, heights):
    found = {}
    for removed in "xyz":
        allowed = [a for a in LETTERS if a.lower() != removed]
        for origin in paths:
            after = graph.follow(origin, removed)
            if after is None:
                continue
            pending = deque([(after, heights[removed], removed)])
            visited = {(after, heights[removed], removed)}
            while pending:
                at, height, word = pending.popleft()
                if at == origin and abs(height) == 1:
                    found.setdefault(canonical(word), (word, origin, height))
                    break
                if len(word) >= WIDTH:
                    continue
                for a in allowed:
                    if a == word[-1].swapcase():
                        continue
                    end = graph.follow(at, a)
                    key = end, height + heights[a], a
                    if end is not None and key not in visited:
                        visited.add(key)
                        pending.append((end, key[1], word + a))
    return found


def compile_terminal(rows, receiver, graph, paths, records, winner):
    word, origin, weight = winner
    path = paths[origin]
    expression = graph.express(path + word + inverse(path))
    expanded, product = [], []
    power = 0
    for symbol in expression:
        sign = 1 if symbol > 0 else -1
        slot, stem, orientation = records[abs(symbol) - 1]
        exponent = sign * orientation
        expanded.append(stem + orient(rows[slot], exponent) + inverse(stem))
        if slot == receiver:
            power += exponent
        else:
            product.append((slot, exponent, reduce(word_power(rows[receiver], power) + stem)))
    assert power == weight and reduce("".join(expanded)) == reduce(path + word + inverse(path))
    moves = [{"op": "invert", "i": receiver}] if power < 0 else []
    for slot, sign, g in reversed(product):
        if sign > 0:
            moves.append({"op": "invert", "i": slot})
        moves.extend(conj_ops(slot, g))
        moves.extend(({"op": "invert", "i": receiver}, {"op": "multiply", "i": receiver, "j": slot},
                      {"op": "invert", "i": receiver}))
        moves.extend(conj_ops(slot, inverse(g)))
        if sign > 0:
            moves.append({"op": "invert", "i": slot})
    moves.extend(conj_ops(receiver, inverse(path)))
    target = [*rows]
    target[receiver] = word
    proof = certificate(rows, moves, target)
    return proof, {"based_expression_terms": len(expression), "donor_factors": len(product),
                   "strict": replay(proof)}


def search(rows, depth):
    summaries, candidates = [], {}
    for receiver in range(3):
        graph = AnnotatedFold(LETTERS)
        graph.petal(rows[receiver], 1)
        records = [(receiver, "", 1)]
        indexed = set()
        snapshots = []
        for stage in range(depth + 1):
            paths = graph.paths()
            found = harvest(graph, paths, height_function(rows, receiver))
            snapshots.append({"vertices": len(paths), "allocated_vertices": len(graph.parent),
                              "literal_charts": len(found)})
            for key, witness in sorted(found.items()):
                marked = (*rows[:receiver], witness[0], *rows[receiver + 1:])
                for pair, chart in each_available_chart(marked):
                    if chart["chart"] != "literal" or chart["pivot"] != witness[0]:
                        continue
                    score = sum(map(len, pair)), len(witness[0]), stage, receiver, pair
                    candidates.setdefault((receiver, key), (score, stage, receiver, witness[0]))
            if stage == depth or len(paths) > 1800:
                break
            for slot in range(3):
                if slot == receiver:
                    continue
                for at in paths.values():
                    for rotation, (tail, sign) in sorted(donor_rotations(rows[slot]).items()):
                        conjugator = reduce(at + tail)
                        source = slot, conjugator, sign
                        if source in indexed:
                            continue
                        indexed.add(source)
                        records.append(source)
                        graph.petal(reduce(at + rotation + inverse(at)), len(records))
            if len(graph.parent) > 420000:
                break
        summaries.append(snapshots)
    return summaries, sorted(candidates.values())


def reconstruct(rows, receiver, word, depth):
    graph = AnnotatedFold(LETTERS)
    graph.petal(rows[receiver], 1)
    records, indexed = [(receiver, "", 1)], set()
    for stage in range(depth + 1):
        paths = graph.paths()
        found = harvest(graph, paths, height_function(rows, receiver))
        if canonical(word) in found:
            return compile_terminal(rows, receiver, graph, paths, records, found[canonical(word)])
        for slot in range(3):
            if slot == receiver:
                continue
            for at in paths.values():
                for rotation, (tail, sign) in sorted(donor_rotations(rows[slot]).items()):
                    conjugator = reduce(at + tail)
                    source = slot, conjugator, sign
                    if source in indexed:
                        continue
                    indexed.add(source)
                    records.append(source)
                    graph.petal(reduce(at + rotation + inverse(at)), len(records))
    raise ValueError("selected target not reached")


def coefficients(rows, pivot):
    return tuple(det((*rows[:slot], pivot, *rows[slot + 1:])) // det(rows) for slot in range(3))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("depth", type=int)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--both-donors", action="store_true")
    args = parser.parse_args()
    original = json.loads(args.source.read_text())
    rows = tuple(original["target"])
    if any(canonical(word) != word for word in rows):
        raise ValueError("source endpoint must use cyclic canonical words")
    stages, candidates = search(rows, args.depth)
    output = {"source": rows, "stages_by_receiver": stages,
              "shortest_literal_return_slots_weight_capped_at": WIDTH,
              "eligible_single_occurrence_receivers": len(candidates)}
    genuine = [candidate for candidate in candidates if all(coefficients(rows, candidate[3])[i]
                                                            for i in range(3) if i != candidate[2])]
    output["literal_charts_with_two_nonzero_donor_coefficients"] = len(genuine)
    selected = genuine if args.both_donors else candidates
    if selected:
        score, depth, receiver, word = selected[0]
        continuation, receipt = reconstruct(rows, receiver, word, depth)
        proof = certificate(original["start"], original["moves"] + continuation["moves"], continuation["target"])
        args.ledger.write_text(json.dumps(proof, separators=(",", ":")) + "\n")
        output.update({"selected": {"quotient": score[-1], "fixed_donor_completion_stage": depth,
                                    "receiver": receiver, "word": word,
                                    "basis_homology_coefficients": coefficients(rows, word),
                                    "continuation": receipt,
                                    "composed": replay(proof)},
                       "sample": [{"slot": item[2], "word": item[3], "pair": item[0][-1]}
                                  for item in candidates[:20]]})
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
