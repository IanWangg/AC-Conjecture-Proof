"""Lift the residual isolated width-eight traces through quadratic and cubic old data."""

import argparse
from collections import defaultdict
from functools import cache
from itertools import product
import json
from pathlib import Path
import sys

from round01_stable_disproof_search import MagnusQuotient, ONE
from round06_magnus_corridor import encode
from round06_stable_disproof_tiers import apply, instruction_labels
from round11_stable_disproof_symbolic4 import inverse
from round12_stable_disproof_symbolic6 import cyclic_relation
from round13_stable_disproof_width_seven import formal_step, terminal_template


def emit_targets(path):
    data = json.loads(Path(path).read_text())
    for row in data["last_equality_tests"]["unresolved_templates"]:
        print(row["removed"], row["signed_donor"], *row["remaining_pair"])


def basis_values(group):
    elements = frontier = {ONE}
    while frontier:
        frontier = {group.multiply(a, x) for a in frontier for x in group.generators} - elements
        elements = elements | frontier
    result = defaultdict(list)
    for element in sorted(elements):
        result[(element >> group.offset[1]) & 3].append(element)
    return result


def pure_embedding(low, high):
    map_bits = [(1 << (low.offset[degree] + encode(word, 2)), 1 << (high.offset[degree] + encode(word, 3)))
                for degree in range(low.degree + 1) for word in product(range(2), repeat=degree)]
    return cache(lambda value: sum(target for source, target in map_bits if value & source))


def z_mask(group):
    return sum(1 << (group.offset[degree] + encode(word, 3))
               for degree in range(1, group.degree + 1) for word in product(range(3), repeat=degree) if 2 in word)


def old_generator_exchange(group):
    terms = [(1 << (group.offset[degree] + encode(word, 2)),
              1 << (group.offset[degree] + encode(tuple(1 - index for index in word), 2)))
             for degree in range(group.degree + 1) for word in product(range(2), repeat=degree)]
    return cache(lambda value: sum(target for source, target in terms if value & source))


def read_paths(stream):
    records = []
    paths = []
    menu = tuple(instruction_labels(3, 2, False))
    for line in stream:
        kind, *items = line.split()
        if kind == "V":
            alpha, beta, count, *widths = map(int, items)
            records.append({"old_linear_parts": [alpha, beta], "trace_count": count, "symbolic_layer_widths": widths})
        elif kind == "W":
            alpha, beta, negative, *indices = map(int, items)
            moves = tuple(menu[index] for index in indices)
            state = ("a", "b", "A" if negative else "a"), 4
            for move in moves[:-1]:
                state = formal_step(state, move)
                assert state is not None
            template = terminal_template(state, moves[-1])
            paths.append((alpha, beta, negative, moves, template))
        elif kind != "R":
            raise ValueError(f"unexpected record {kind}")
    assert len(paths) == sum(row["trace_count"] for row in records)
    return records, paths


def passes(group, embedding, mask, a, b, negative, moves, exact):
    auxiliary = group.generators[2]
    a, b = embedding(a), embedding(b)
    rows = (a, b, group.multiply(auxiliary, group.inverse(a) if negative else a))
    for move in moves:
        rows = apply(group, rows, move)
    killed = moves[-1][1]
    if exact and rows[killed] != auxiliary:
        return False
    return all((row & mask) == ((auxiliary & mask) if i == killed else 0) for i, row in enumerate(rows))


def search(stream, collect_guards=False):
    records, paths = read_paths(stream)
    low = MagnusQuotient(2, 3)
    three = MagnusQuotient(3, 3)
    four = MagnusQuotient(3, 4)
    mask_three, mask_four = z_mask(three), z_mask(four)
    embed_three, embed_four = pure_embedding(low, three), pure_embedding(low, four)
    values = basis_values(low)
    x, y = low.generators

    @cache
    def allowed_pairs(alpha, beta, relation):
        pairs = []
        for a, b in product(values[alpha], values[beta]):
            symbols = dict(zip("abxy", (a, b, x, y)))
            symbols.update({k.upper(): low.inverse(v) for k, v in tuple(symbols.items())})
            result = ONE
            for letter in relation:
                result = low.multiply(result, symbols[letter])
            if result == ONE:
                pairs.append((a, b))
        return pairs

    survivors_three = defaultdict(set)
    survivors_four = defaultdict(set)
    all_templates = set()
    guards = set()
    exchange_word = str.maketrans("xXyY", "yYxX")
    exchange_value = old_generator_exchange(low)
    for alpha, beta, negative, moves, template in paths:
        removed, donor, pair = template
        relation = cyclic_relation(removed + inverse(donor))
        all_templates.add(template)
        for a, b in allowed_pairs(alpha, beta, relation):
            rule = a, b, relation or "-", *pair
            if collect_guards and rule in guards:
                continue
            if passes(three, embed_three, mask_three, a, b, negative, moves, True):
                survivors_three[template].add((alpha, beta))
                if passes(four, embed_four, mask_four, a, b, negative, moves, False):
                    survivors_four[template].add((alpha, beta))
                    if not collect_guards:
                        break
                    guards.add(rule)
                    changed_relation = cyclic_relation(relation.translate(exchange_word)) or "-"
                    changed_pair = sorted(word.translate(exchange_word) for word in pair)
                    guards.add((exchange_value(a), exchange_value(b), changed_relation, *changed_pair))

    if collect_guards:
        return sorted(guards)
    return {"trace_layers": records, "terminal_templates_traced": len(all_templates),
            "templates_surviving_exact_rank_three_degree_three": len(survivors_three),
            "templates_surviving_mixed_rank_three_degree_four": [
                {"removed": removed, "signed_donor": donor, "remaining_pair": pair, "old_linear_parts": sorted(markings)}
                for (removed, donor, pair), markings in sorted(survivors_four.items())]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--targets", help="print terminal templates from the first-comparison JSON")
    mode.add_argument("--guards", action="store_true", help="print all retained cubic input assignments for the traces")
    args = parser.parse_args()
    if args.targets:
        emit_targets(args.targets)
    elif args.guards:
        for rule in search(sys.stdin, collect_guards=True):
            print(*rule)
    else:
        print(json.dumps(search(sys.stdin), indent=2, sort_keys=True))
