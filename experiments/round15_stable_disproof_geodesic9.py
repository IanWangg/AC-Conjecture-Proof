"""Test whether an isolated width-nine interval could compress onto a geodesic."""

from functools import cache
import json

from round01_stable_disproof_search import MagnusQuotient, ONE
from round10_stable_disproof_neighborhood import pack
from round10_stable_disproof_saturate import corridor_data, saturation, widths


def search():
    low = MagnusQuotient(2, 9)
    corridor, _ = saturation()
    assert widths(corridor) == corridor_data()
    idle = [{tuple(sorted((ONE, pack(a), pack(b)))) for a, b in layer} for layer in corridor]

    @cache
    def active_radius_four(t):
        layer = idle[t]
        for _ in range(4):
            layer = {child for state in layer for child in low.neighbors(state, True) if ONE not in child}
        return layer

    records = []
    for t in range(len(idle) - 8):
        left, right = active_radius_four(t), active_radius_four(t + 8)
        matches = set()
        checked = 0
        for state in right:
            for child in low.neighbors(state, True):
                checked += 1
                if child in left:
                    matches.add(child)
        assert not matches
        records.append({"entry_tick": t, "exit_geodesic_tick": t + 8, "widths_at_depth_four": [len(left), len(right)],
                        "boundary_checks": checked, "midpoints": len(matches)})
    return {"degree": 9, "active_interval_width": 9, "compressed_budget": 17, "geodesic_windows": records}


if __name__ == "__main__":
    print(json.dumps(search(), indent=2, sort_keys=True))
