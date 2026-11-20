"""Audit chart intervals of the 544-move rank-three AK(3) excursion."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from round03_ac_proof_controls import substitute
from round03_stable_proof_pivot import canonical, det
from round04_stable_proof_paths import replay
from round06_stable_proof_cap23_charts import compact_row
from round07_ac_proof_cap23 import donor_orbit, ledger_states, normal, primitive_chart
from stallings_search import reduce


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates/round09_stable_proof_e20_rank3.json"


def projected(rows, pivot):
    chart = primitive_chart(rows[pivot])
    return tuple(canonical(substitute(word, chart)) for i, word in enumerate(rows) if i != pivot)


def membership(path, keys):
    covered = set()
    with path.open("rb") as catalogue:
        for row in catalogue:
            if row in keys:
                covered.add(row)
            if covered == keys:
                break
    return covered


def screen(states, products):
    times = [0, *(step for step, *_ in products)]
    rows = [tuple(map(canonical, states[t])) for t in times]
    assert rows[-1] == tuple(map(canonical, states[-1]))
    assert all(abs(det(triple)) == 1 for triple in rows)
    pivots = [tuple(i for i, word in enumerate(triple) if primitive_chart(word)) for triple in rows]
    blocks = tuple(combinations(range(3), 2))
    planes = [{block: normal(*(triple[i] for i in block)) for block in blocks} for triple in rows]
    donors = [{(pivot, donor): donor_orbit(canonical(substitute(triple[donor], primitive_chart(triple[pivot]))))
               for pivot in available for donor in range(3) if pivot != donor}
              for triple, available in zip(rows, pivots)]

    edges = {}
    counts = Counter()
    for end, after in enumerate(pivots):
        if end:
            for pivot in set(after).intersection(pivots[end - 1]) - {products[end - 1][1]}:
                edges.setdefault((end, pivot), set()).add((end - 1, pivot))
                counts["fixed_pivot_edges"] += 1
        for start, before in enumerate(pivots[:end + 1]):
            for first, last in product(before, after):
                if (start, first) == (end, last):
                    continue
                for block in blocks:
                    if first not in block or last not in block:
                        continue
                    if planes[start][block] != planes[end][block]:
                        counts["different_block_lattice"] += 1
                        continue
                    first_donor, = set(block) - {first}
                    last_donor, = set(block) - {last}
                    if donors[start][first, first_donor] != donors[end][last, last_donor]:
                        counts["different_donor_orbit"] += 1
                        continue
                    counts["passes_both_necessary_tests"] += 1
                    edges.setdefault((end, last), set()).add((start, first))

    reachable = {(0, 2)}
    for stage, before in enumerate(pivots):
        while True:
            more = {(stage, pivot) for pivot in before if edges.get((stage, pivot), set()) & reachable}
            if more <= reachable:
                break
            reachable.update(more)
    records = [{"strict_step": time, "cyclic_rows": triple, "projections": [
        {"pivot": pivot, "pair": projected(triple, pivot), "one_donor_overapproximation_reaches": (i, pivot) in reachable}
        for pivot in pivots[i]]} for i, (time, triple) in enumerate(zip(times, rows))]
    return counts, records


def short_substitution_keys(pair):
    candidates = Counter()
    for letter in "xy":
        for size in (4, 5):
            for letters in product("xXyY", repeat=size):
                word = "".join(letters)
                occurrences = word.count(letter)
                if occurrences < 2 or occurrences - word.count(letter.upper()) != 1 or reduce(word) != word:
                    continue
                image = tuple(canonical(substitute(row, {letter: word})) for row in pair)
                candidates[compact_row(image)] += 1
    return candidates


def main(cap30, e20_component):
    data = CERTIFICATE.read_bytes()
    certificate = json.loads(data)
    replay_result = replay(certificate)
    states, products = ledger_states(certificate)
    counts, stages = screen(states, products)
    chart_records = [chart for stage in stages for chart in stage["projections"]]
    for chart in chart_records:
        chart["catalogue_key"] = compact_row(chart["pair"]).decode("ascii").rstrip("\n")
    keys = {(chart["catalogue_key"] + "\n").encode("ascii") for chart in chart_records}
    substitutions = short_substitution_keys(certificate["start"][:2])
    queries = keys | substitutions.keys()
    cap30_all = membership(cap30, queries)
    cap36_all = membership(e20_component, queries)
    cap30_presence = cap30_all & keys
    cap36_presence = cap36_all & keys
    for chart in chart_records:
        key = (chart["catalogue_key"] + "\n").encode("ascii")
        chart["ordinary_ancestry_catalogue"] = (
            "AK3_cap30" if key in cap30_presence else "E20_cap36" if key in cap36_presence else None
        )
    assert not cap30_presence & cap36_presence
    assert len(stages[-1]["projections"]) == 2
    assert not any(chart["one_donor_overapproximation_reaches"] for chart in stages[-1]["projections"])
    return {
        "source": CERTIFICATE.name,
        "source_sha256": sha256(data).hexdigest(),
        "rank_three_replay": replay_result,
        "cyclic_product_count": len(products),
        "interval_counts": dict(sorted(counts.items())),
        "chart_occurrence_counts": dict(Counter(chart["ordinary_ancestry_catalogue"] or "unmatched"
                                               for chart in chart_records)),
        "distinct_chart_classes": len(keys),
        "cap30_chart_classes": len(cap30_presence),
        "e20_cap36_chart_classes": len(cap36_presence),
        "direct_noninvertible_substitutions": {
            "single_generator_image_lengths": [4, 5],
            "positive_self_exponent": 1,
            "valid_substitutions": sum(substitutions.values()),
            "distinct_signed_cyclic_pairs": len(substitutions),
            "signed_pair_energies": dict(sorted(Counter(len(key) - 2 for key in substitutions).items())),
            "AK3_cap30_hits": len(cap30_all & substitutions.keys()),
            "E20_cap36_hits": len(cap36_all & substitutions.keys()),
        },
        "stages": stages,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cap30", type=Path)
    parser.add_argument("e20_cap36", type=Path)
    args = parser.parse_args()
    print(json.dumps(main(args.cap30, args.e20_cap36), indent=2))
