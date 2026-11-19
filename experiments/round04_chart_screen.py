"""Check every one-occurrence generator elimination on the cap-22 rank-three witness."""

import argparse
import json
from collections import Counter
from pathlib import Path

from planar_link_parity import decide
from round01_geometric_archive import check_whitehead_cuts, exponent_vector, minimal_pair
from round03_stable_proof_pivot import canonical
from round04_stable_proof_paths import replay
from stallings_search import apply, inverse, reduce
from verify_link_parity import verify_certificate

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates/round04_stable_proof_pivotless22.json"


def chart_projections(rows):
    for i, row in enumerate(rows):
        for letter in "xyz":
            if row.count(letter) + row.count(letter.upper()) != 1:
                continue
            oriented = row if letter in row else inverse(row)
            pivot = oriented.index(letter)
            replacement = inverse(oriented[pivot + 1 :] + oriented[:pivot])
            values = {letter: replacement, letter.upper(): inverse(replacement)}
            survivors = [name for name in "xyz" if name != letter]
            labels = str.maketrans("".join(survivors + [name.upper() for name in survivors]), "xyXY")
            quotient = tuple(sorted(
                canonical(reduce("".join(values.get(c, c) for c in word)).translate(labels))
                for j, word in enumerate(rows) if j != i
            ))
            yield letter, row, quotient


def screen(catalogue):
    certificate = json.loads(CERTIFICATE.read_bytes())
    proof = replay(certificate)
    raw = tuple(certificate["start"])
    cyclic_states = {}
    for step, move in enumerate([None, *certificate["moves"]]):
        if move is not None:
            raw = apply(raw, move)
        state = tuple(sorted(map(canonical, raw)))
        cyclic_states.setdefault(state, step)
    screens = {}
    counts = Counter()
    states_with_chart = 0
    for state, step in cyclic_states.items():
        charts = list(chart_projections(state))
        states_with_chart += bool(charts)
        for letter, pivot, pair in charts:
            counts[letter] += 1
            screens.setdefault(pair, {"source_step": step, "eliminated": letter, "pivot": pivot})
    expected = {"\t".join(pair) + "\n": pair for pair in screens}
    found = set()
    with catalogue.open() as stream:
        for row in stream:
            if row in expected:
                found.add(expected[row])
    minimized = {minimal_pair(pair) for pair in screens}
    parity_counts = Counter()
    for pair in minimized:
        a, b = exponent_vector(pair[0])
        c, d = exponent_vector(pair[1])
        assert abs(a * d - b * c) == 1
        assert sum(map(len, pair)) > 2
        check_whitehead_cuts(pair)
        result = decide(pair)
        if result["status"] == "PARITY_OBSTRUCTION":
            verify_certificate(result)
        parity_counts[result["status"]] += 1
    target = tuple(sorted(map(canonical, proof["target"])))
    return {
        "distinct_rank_three_cyclic_states": len(cyclic_states),
        "states_with_at_least_one_chart": states_with_chart,
        "chart_counts_by_eliminated_generator": dict(sorted(counts.items())),
        "distinct_rank_two_projections": len(screens),
        "in_cap_26_component": len(found),
        "unmatched": [{"projection": pair, **screens[pair]} for pair in sorted(set(screens) - found)],
        "distinct_whitehead_minima": len(minimized),
        "independent_planar_parity_checks": dict(sorted(parity_counts.items())),
        "final_state_charts": [
            {"eliminated": letter, "pivot": pivot, "projection": pair}
            for letter, pivot, pair in chart_projections(target)
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalogue", type=Path)
    args = parser.parse_args()
    print(json.dumps(screen(args.catalogue), indent=2))
