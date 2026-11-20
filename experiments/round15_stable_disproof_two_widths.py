"""Build the marked terminal transitions for width six and width seven."""

from collections import defaultdict
from itertools import permutations, product

from round11_stable_disproof_symbolic4 import inverse, parity
from round12_stable_disproof_short_savings import marked_formal_children
from round12_stable_disproof_symbolic6 import cyclic_relation
from round13_stable_disproof_templates import transitions as width_six
from round13_stable_disproof_width_seven import strict_comparison


def marked_width_seven():
    residual, _ = strict_comparison()
    targets = defaultdict(set)
    for removed, donor, pair in residual:
        equality = cyclic_relation(removed + inverse(donor))
        columns = [p[0] + 2 * p[1] for p in map(parity, pair)]
        for order in permutations(range(3)):
            values = removed, *pair
            rows = tuple(values[index] for index in order)
            recipient = order.index(0)
            donors = [j for j, row in enumerate(rows) if j != recipient and row in (donor, inverse(donor))]
            for marks in product(range(2), repeat=2):
                if marks == (0, 0):
                    continue
                for donor_row in donors:
                    auxiliary = [0, *marks]
                    auxiliary[0] = marks[order[donor_row] - 1] ^ 1
                    mask = sum(auxiliary[index] << row for row, index in enumerate(order))
                    targets[(rows, mask)].add((equality or "-", *pair, *marks, *columns))

    layer = {(("a", "b", copy), 4) for copy in "aA"}
    for _ in range(4):
        layer = {child for state in layer for child in marked_formal_children(*state)}
    desired = set(targets)
    hits = {child for state in layer for child in marked_formal_children(*state) & desired}
    found = {rule for state in hits for rule in targets[state]}
    assert len(found) == 5769
    return sorted(found)


if __name__ == "__main__":
    for span, rows in ((6, width_six()), (7, marked_width_seven())):
        for line in rows:
            print(span, *line)
