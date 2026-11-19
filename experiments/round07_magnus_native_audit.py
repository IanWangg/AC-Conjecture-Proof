"""Compare complete native Magnus balls to independent Python arithmetic."""

import argparse
import json
from subprocess import check_output

from round01_stable_disproof_search import ak3_bounded_test
from round05_stable_disproof_retractions import packed_search, set_search


def native(executable, degree, spare, radius, ordered=False):
    args = [executable, str(degree), str(spare), str(radius)]
    if ordered:
        args.append("--ordered")
    return json.loads(check_output(args))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("executable")
    args = parser.parse_args()
    results = []
    controls = ((4, 3, 7), (5, 2, 9), (6, 1, 11), (7, 0, 10), (8, 0, 10), (9, 0, 10), (10, 0, 10))
    for degree, spare, radius in controls:
        actual = native(args.executable, degree, spare, radius)
        expected = set_search(degree, spare, radius) if degree <= 5 else packed_search(degree, spare, radius)
        assert actual["distance"] == expected["distance"] is None
        assert actual["visited"] == expected["visited"]
        assert sum(actual["radii"]) == expected["last_radius"] == radius
        results.append({"degree": degree, "spare_rows": spare, "tested_radius": radius,
                        "balls": actual["visited"], "complete_exclusion": True})
    positive = native(args.executable, 5, 0, 11, ordered=True)
    assert positive["distance"] == ak3_bounded_test(5, 0, 11, unordered=False)["distance"] == 11
    print(json.dumps({"complete_negative_controls": results,
                      "ordered_positive_control": {"degree": 5, "distance": 11}}, indent=2))


if __name__ == "__main__":
    main()
