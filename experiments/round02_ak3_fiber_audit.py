"""Audit the finite bridge labels and directly fold sampled product graphs."""

import argparse
import json
from functools import cache
from pathlib import Path

from elementary_verify import inverse
from round02_ak3_fiber_replay import rotations
from stallings_search import LETTERS, graph


def two_lift_words(marked_graph):
    arrows, vertices = marked_graph
    pending = [("", tuple(range(vertices)))]
    for word, images in pending:
        if len(word) > 9:
            raise ValueError("out of range for the audited cores")
        for i, letter in enumerate(LETTERS):
            if word and word[-1] == letter.swapcase():
                continue
            targets = tuple(arrows[4 * a + i] for a in images if arrows[4 * a + i] >= 0)
            if len(targets) >= 2:
                pending.append((word + letter, targets))
    return [word for word, _ in pending if word]


def product_ranks(left, right):
    g, n = left
    h, m = right
    seen = set()
    ranks = []
    for a in range(n):
        for b in range(m):
            if (a, b) in seen:
                continue
            pending = [(a, b)]
            seen.add((a, b))
            darts = 0
            for x, y in pending:
                left_arcs = g[4 * x : 4 * x + 4]
                right_arcs = h[4 * y : 4 * y + 4]
                for end in zip(left_arcs, right_arcs):
                    if min(end) < 0:
                        continue
                    darts += 1
                    if end not in seen:
                        seen.add(end)
                        pending.append(end)
            ranks.append(darts // 2 - len(pending) + 1)
    return ranks


def has_loop(marked_graph, word):
    arrows, vertices = marked_graph
    letters = [LETTERS.index(c) for c in word]
    for a in range(vertices):
        v = a
        for c in letters:
            v = arrows[4 * v + c]
            if v < 0:
                break
        if v == a:
            return True
    return False


def audit(directory, source_file, target_file, native_file):
    def rows(name):
        return [tuple(line.split("\t")) for line in (directory / name).read_text().splitlines()]

    left_rows = rows(source_file)
    right_rows = rows(target_file)
    native = json.loads((directory / native_file).read_text())
    samples = [right_rows[(i * len(right_rows)) // 11] for i in range(11)]
    checked_lobes = checked_barbells = checked_rotations = 0

    assert len(left_rows) == len(native["sources"])
    for source, statistics in zip(left_rows, native["sources"]):
        g = graph(source)
        words = two_lift_words(g)
        assert statistics["source"] == list(source)
        assert len(words) == statistics["multilift_words"]
        assert max(map(len, words)) == statistics["longest_multilift_word"]

        @cache
        def loop(word):
            return has_loop(g, word)

        for u, v in right_rows:
            # The lifting map for a nontrivial cyclic lobe has no nontrivial
            # orbit of size >1 because any power would lift to a loop twice.
            assert not (loop(u) and loop(v))
            checked_lobes += 1

        for u, v in samples:
            first, second = rotations(u), rotations(v)
            for q in words:
                a = next((w for w in first if q[0] not in (w[0], inverse(w[-1]))), None)
                b = next((w for w in reversed(second) if inverse(q[-1]) not in (w[0], inverse(w[-1]))), None)
                if a and b:
                    h = graph((a, q + b + inverse(q)))
                    assert sum(product_ranks(g, h)) <= 1
                    checked_barbells += 1
            for a in first:
                for b in second:
                    h = graph((a, b))
                    ranks = product_ranks(g, h)
                    assert sum(ranks) <= 1 or (ranks.count(2) == 1 and h[1] == 1)
                    checked_rotations += 1

    return {
        "all_single_lobe_controls": checked_lobes,
        "sampled_barbells": checked_barbells,
        "sampled_rotations": checked_rotations,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work_directory", type=Path)
    root = parser.parse_args().work_directory
    record = {
        "four_waypoints": audit(root, "sources.tsv", "reverse44.tsv", "fiber_tails44.json"),
        "initial_rotation_cores": audit(
            root, "sources_initial_rotations.tsv", "reverse32.tsv", "fiber_initial_rotations.json"
        ),
    }
    print(json.dumps(record, indent=2))
