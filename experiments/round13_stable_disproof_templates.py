"""Attach auxiliary coefficient transitions to the 136 residual width-six templates."""

from collections import defaultdict
import json
from pathlib import Path

from round11_stable_disproof_symbolic4 import inverse, parity
from round12_stable_disproof_short_savings import marked_formal_children


def transitions():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results/round12_stable_disproof_short_savings.json").read_text())
    residual = data["unrestricted_interval_templates"][-1]["unresolved_templates"]
    relations = {(row["removed"], row["signed_donor"], tuple(row["remaining_pair"])): row["last_equality_class"]
                 for row in residual}
    layer = {(("a", "b", copy), 4) for copy in "aA"}
    for _ in range(4):
        layer = {child for state in layer for child in marked_formal_children(*state)}
    marks_by_template = defaultdict(set)
    projected = set()
    for rows, mask in layer:
        for i, removed in enumerate(rows):
            rest = sorted((word, (mask >> j) & 1) for j, word in enumerate(rows) if i != j)
            pair, marks = zip(*rest)
            for j, donor in enumerate(rows):
                if i == j:
                    continue
                for signed in (donor, inverse(donor)):
                    key = (removed, signed, pair)
                    if key in relations:
                        assert ((mask >> i) ^ (mask >> j)) & 1
                        assert marks != (0, 0)
                        marks_by_template[key].add(marks)
                        projected.add((relations[key] or "-", *pair, *marks,
                                       *(p[0] + 2 * p[1] for p in map(parity, pair))))
    assert set(marks_by_template) == set(relations) and len(marks_by_template) == 136
    assert all(len(marks) == 1 for marks in marks_by_template.values())
    return sorted(projected)


if __name__ == "__main__":
    for line in transitions():
        print(*line)
