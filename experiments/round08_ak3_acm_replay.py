"""Recover a strict free-group ledger from a finite ACM completion."""

import argparse
from collections import deque
import json
from pathlib import Path

from elementary_verify import inverse, reduce, replay
from free_waypoint_search import conj_ops, cyclic


LETTERS = "xXyY"
FORMAT = "ordinary-ac-elementary-v1"


def multiply(*parts):
    result = []
    for part in parts:
        for symbol in part:
            if result and result[-1] == -symbol:
                result.pop()
            else:
                result.append(symbol)
    return tuple(result)


def reverse(word):
    return tuple(-symbol for symbol in reversed(word))


def orient(word, sign):
    return word if sign > 0 else inverse(word)


class AnnotatedFold:
    """Keep a path with freely trivial label for each representative change."""

    def __init__(self):
        self.parent = []
        self.size = []
        self.transport = []
        self.arcs = []
        self.new_vertex()

    def new_vertex(self):
        at = len(self.parent)
        self.parent.append(at)
        self.size.append(1)
        self.transport.append(())
        self.arcs.append([None] * 4)
        return at

    def find(self, at):
        segments = []
        while self.parent[at] != at:
            segments.append(self.transport[at])
            at = self.parent[at]
        return at, multiply(*reversed(segments))

    def trace(self, arc):
        a, b, token = arc
        _, start = self.find(a)
        target, finish = self.find(b)
        return target, multiply(start, token, reverse(finish))

    def add_arc(self, start, letter, end, token):
        pending = []
        for a, b, label, weight in ((start, end, letter, token),
                                     (end, start, letter ^ 1, reverse(token))):
            at, _ = self.find(a)
            arc = (a, b, weight)
            old = self.arcs[at][label]
            if old is None:
                self.arcs[at][label] = arc
            else:
                pending.append((old, arc))
        while pending:
            first, second = pending.pop()
            a, first_word = self.trace(first)
            b, second_word = self.trace(second)
            if a == b:
                continue
            connector = multiply(reverse(first_word), second_word)
            if self.size[a] < self.size[b]:
                a, b = b, a
                connector = reverse(connector)
            self.parent[b] = a
            self.size[a] += self.size[b]
            self.transport[b] = connector
            for label, arc in enumerate(self.arcs[b]):
                if arc is None:
                    continue
                old = self.arcs[a][label]
                if old is None:
                    self.arcs[a][label] = arc
                else:
                    pending.append((old, arc))

    def petal(self, word, symbol):
        at = 0
        for index, letter in enumerate(word, 1):
            finish = index == len(word)
            new = 0 if finish else self.new_vertex()
            self.add_arc(at, LETTERS.index(letter), new, (symbol,) if finish else ())
            at = new

    def paths(self):
        root, _ = self.find(0)
        queue = deque([root])
        visited = {root: ''}
        while queue:
            at = queue.popleft()
            for letter, arc in zip(LETTERS, self.arcs[at]):
                if arc is None:
                    continue
                end, _ = self.find(arc[1])
                if end not in visited:
                    visited[end] = visited[at] + letter
                    queue.append(end)
        return visited

    def follow(self, at, word):
        for letter in word:
            arc = self.arcs[at][LETTERS.index(letter)]
            if arc is None:
                return None
            at, _ = self.find(arc[1])
        return at

    def express(self, word):
        root, tail = self.find(0)
        at = root
        parts = [reverse(tail)]
        for letter in word:
            arc = self.arcs[at][LETTERS.index(letter)]
            at, part = self.trace(arc)
            parts.append(part)
        if root != at:
            raise ValueError("word is not based at the root")
        return multiply(*parts, tail)


def donor_rotations(word):
    rotations = {}
    for sign in (1, -1):
        oriented = orient(word, sign)
        for index in range(len(oriented)):
            prefix, suffix = oriented[:index], oriented[index:]
            rotations.setdefault(suffix + prefix, (inverse(prefix), sign))
    return rotations


def word_power(word, exponent):
    return orient(word, exponent) * abs(exponent)


def recover(receiver, donor, target, max_depth):
    if any(not word or cyclic(word) != word for word in (receiver, donor, target)):
        raise ValueError("expected nonempty cyclically reduced words")
    graph = AnnotatedFold()
    graph.petal(receiver, 1)
    rotations = donor_rotations(donor)
    sources = [(None, 1)]
    indexed = set()
    sizes = []
    for depth in range(max_depth + 1):
        paths = graph.paths()
        sizes.append(len(paths))
        for at, path in paths.items():
            if graph.follow(at, target) == at:
                based = path + target + inverse(path)
                expression = graph.express(based)
                expanded = []
                factors = []
                power = 0
                for symbol in expression:
                    sign = 1 if symbol > 0 else -1
                    conjugator, donor_sign = sources[abs(symbol) - 1]
                    if conjugator is None:
                        power += sign
                        expanded.append(orient(receiver, sign))
                        continue
                    exponent = donor_sign * sign
                    expanded.append(conjugator + orient(donor, exponent) + inverse(conjugator))
                    factors.append((reduce(word_power(receiver, power) + conjugator), exponent))
                if abs(power) != 1 or reduce(''.join(expanded)) != reduce(based):
                    raise AssertionError("fold provenance failed exact free-group verification")
                return {'graph_sizes': sizes, 'source_count': len(sources),
                        'expression_length': len(expression), 'power': power,
                        'factors': factors, 'base_path': path}
        if depth == max_depth:
            break
        for path in paths.values():
            for rotation in sorted(rotations):
                tail, sign = rotations[rotation]
                conjugator = reduce(path + tail)
                if (conjugator, sign) in indexed:
                    continue
                indexed.add((conjugator, sign))
                sources.append((conjugator, sign))
                graph.petal(reduce(path + rotation + inverse(path)), len(sources))
    raise ValueError("the target is absent through the requested depth")


def invert(slot):
    return {'op': 'invert', 'i': slot}


def compile_move(pair, slot, target, depth):
    donor = 1 - slot
    receipt = recover(pair[slot], pair[donor], target, depth)
    moves = [invert(slot)] if receipt['power'] < 0 else []
    for conjugator, sign in reversed(receipt['factors']):
        if sign > 0:
            moves.append(invert(donor))
        moves.extend(conj_ops(donor, conjugator))
        moves.extend((invert(slot), {'op': 'multiply', 'i': slot, 'j': donor}, invert(slot)))
        moves.extend(conj_ops(donor, inverse(conjugator)))
        if sign > 0:
            moves.append(invert(donor))
    moves.extend(conj_ops(slot, inverse(receipt['base_path'])))
    endpoint = list(pair)
    endpoint[slot] = target
    certificate = {'format': FORMAT, 'start': list(pair), 'target': endpoint, 'moves': moves}
    receipt.update(replay(certificate))
    return certificate, receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('slot', type=int, choices=(0, 1))
    parser.add_argument('target')
    parser.add_argument('depth', type=int)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    source = json.loads(args.source.read_text())
    replay(source)
    continuation, receipt = compile_move(source['target'], args.slot, args.target, args.depth)
    continuation['start'] = source['start']
    continuation['moves'] = source['moves'] + continuation['moves']
    receipt['composed'] = replay(continuation)
    args.output.write_text(json.dumps(continuation, separators=(',', ':')) + '\n')
    print(json.dumps(receipt, sort_keys=True))


if __name__ == '__main__':
    main()
