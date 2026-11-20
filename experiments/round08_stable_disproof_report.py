"""Verify and collect the round-eight padded-erasure and abelian search receipts."""

import argparse
import json
from pathlib import Path


def records(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def summarize(directory):
    erasures = []
    for degree, padding, budget in ((8, 2, 14), (7, 3, 12), (6, 4, 10)):
        path = directory / f"d{degree}-k{padding}-L{budget}.json"
        row = json.loads(path.read_text())
        assert (row["degree"], row["spare_rows"], row["limit"]) == (degree, padding, budget)
        assert row["distance"] is None and not row["ordered"] and row["final_boundary_candidates"] > 0
        erasures.append(row)

    graph_directory = directory / "wide"
    graphs = json.loads((graph_directory / "graphs.json").read_text())
    parity = iter(records(graph_directory / "parity.jsonl"))
    graph_results = []
    for group in graphs:
        results = []
        for edges in group["representatives"]:
            row = next(parity)
            assert row["edges"] == edges and row["matching_matrix_pairs"] == 0
            assert not row["witness"]
            results.append(row)
        graph_results.append({
            "padding": group["padding"],
            "degree_four_vertex": group["degree_four_vertex"],
            "labeled_graphs": group["labeled_graphs"],
            "marked_representatives": len(results),
            "prefix_matrices": sum(row["prefix_matrices"] for row in results),
            "inverse_suffix_matrices": sum(row["inverse_suffix_matrices"] for row in results),
            "matching_matrix_pairs": 0,
            "graphs": results,
        })
    assert next(parity, None) is None
    assert [row["marked_representatives"] for row in graph_results] == [2, 7, 25, 8]

    signed = [records(directory / f"signed-k{k}.jsonl") for k in (1, 2)]
    for group, first, last, padding in zip(signed, (3, 5), (7, 9), (1, 2)):
        assert [row["products"] for row in group] == list(range(first, last + 1))
        assert all(row["padding"] == padding for row in group)
        assert all(row["matching_state_pairs"] == 0 for row in group[:-1])
        assert group[-1]["matching_state_pairs"] > 0 and group[-1]["witness"]
    return {
        "stable_budget": 18,
        "rank_two_magnus_erasures": erasures,
        "tight_crossing_parity": graph_results,
        "signed_integral_abelianization": [row for group in signed for row in group],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(summarize(args.directory), indent=2))


if __name__ == "__main__":
    main()
