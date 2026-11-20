"""Check the optional compact degree-five membership against the hash layout."""

import argparse
import json
import subprocess

from round06_stable_disproof_tiers import independent_replay


def compare(executable):
    cases = ((6, (5, 6), False), (6, (6, 6), False), (6, (6, 6), True), (7, (7, 7), False))
    records = []
    for degree, radii, ordered in cases:
        command = [executable, str(degree), *map(str, radii), "--first-arrivals", "--ledger"]
        if ordered:
            command.append("--ordered")
        for partial in (False, True):
            options = [*command, "--partial-degree-six"] if partial else command
            plain = json.loads(subprocess.run(options, text=True, capture_output=True, check=True).stdout)
            actual = json.loads(subprocess.run([*options, "--compact-degree-five"], text=True,
                                              capture_output=True, check=True).stdout)
            compact = actual.pop("compact_degree_five")
            assert plain == actual
            tier = next(row for row in actual["tiers"] if row["degree"] == 5)
            assert compact["layers"] == sum(map(len, tier["widths"]))
            assert compact["pairs"] == sum(map(sum, tier["widths"]))
            assert compact["second_id_bytes"] == 4 * compact["pairs"]
            replay = independent_replay(degree, 0, actual["moves"], erased=True) if actual["path_within_budget"] else None
            records.append({"degree": degree, "radii": radii, "ordered": ordered, "partial_degree_six": partial,
                            "path_within_budget": actual["path_within_budget"], "full_tiers_agree": True,
                            "final_midpoints": actual["tiers"][-1]["midpoints"], "compact": compact,
                            "independently_replayed_order": replay})
    return {"comparisons": records}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corridor", help="path to the rebuilt native corridor executable")
    print(json.dumps(compare(parser.parse_args().corridor), indent=2, sort_keys=True))
