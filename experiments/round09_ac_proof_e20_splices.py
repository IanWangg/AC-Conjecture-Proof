"""Compile exact ordinary replacements for two chart changes at step 394."""

import argparse
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from elementary_verify import replay
from free_waypoint_search import canonical
from round03_ak3_escape_replay import START
from round06_stable_proof_cap23_charts import compact_row
from round07_ac_proof_cap23 import donor_orbit, ledger_states
from round07_automorphism_transport import normalize_pair
from round07_stable_proof_compile_join import compile_local_caps, lift_from
from round08_ac_proof_two_donors import reverse_moves
from round08_ak3_acm_search import cyclic_peak
from round09_ac_proof_e20_intervals import CERTIFICATE, ROOT, projected


def e20_route(path):
    return [tuple(line.split()) for line in path.read_text().splitlines()]


def attach_to_ak3(lifted, cap, literal_search):
    """Attach a cap-22 signed AK(3) alignment and reverse the lifted route."""
    initial = tuple(sorted(map(canonical, START)))
    route = [initial]
    if lifted[-1] != initial:
        with TemporaryDirectory() as scratch:
            folder = Path(scratch)
            (folder / "signed.tsv").write_text("\t".join(lifted[-1]) + "\n")
            process = subprocess.run([str(literal_search), "22", str(folder / "signed.tsv"),
                                      str(folder / "signed.json")], capture_output=True, text=True)
            if process.returncode:
                raise RuntimeError(process.stderr)
            route = list(map(tuple, json.loads((folder / "signed.json").read_text())["route"]))
    assert route[-1] == lifted[-1]
    certificate, _ = compile_local_caps(route + lifted[-2::-1], cap)
    assert tuple(certificate["start"]) == START
    return certificate


def exact_endpoint(certificate, target):
    if tuple(map(canonical, certificate["target"])) != tuple(map(canonical, target)):
        assert tuple(map(canonical, reversed(certificate["target"]))) == tuple(map(canonical, target))
        # Move the row permutation to the short initial pair before replaying
        # the rest with both row indices exchanged.
        assert tuple(certificate["start"]) == START
        swapped = [{key: 1 - value if key in ("i", "j") else value for key, value in move.items()}
                   for move in certificate["moves"]]
        certificate["moves"] = normalize_pair(START, START[::-1]) + swapped
        certificate["target"].reverse()
    certificate["moves"].extend(normalize_pair(tuple(certificate["target"]), target))
    certificate["target"] = list(target)
    replay(certificate)
    return certificate


def main(work, literal, certificates):
    stable = json.loads(CERTIFICATE.read_text())
    states, products = ledger_states(stable)
    assert next(move for move in products if move[0] == 394)[1:3] == (2, 1)
    right = projected(states[394], 2)
    entry = json.loads((ROOT / "results/round09_ak3_e20.json").read_text())
    local = e20_route(work / "e20-right.route.tsv")
    assert json.loads((work / "e20-right.json").read_text())["target_found"]
    marked = tuple(entry["literal_endpoint_shared_with_stable_certificate"])
    assert compact_row(local[0]) == compact_row(marked)
    assert compact_row(local[-1]) == compact_row(right)
    there = lift_from(right, local[::-1], 36)
    at_cap37 = lift_from(there[-1], entry["cap37_orbit_route_to_cap29_anchor"], 37)
    at_cap29 = lift_from(at_cap37[-1], entry["cap29_orbit_route_from_AK3"][::-1], 29)
    root_to_right = exact_endpoint(attach_to_ak3(there + at_cap37[1:] + at_cap29[1:], 37, literal), right)
    assert cyclic_peak(root_to_right) == 37

    trials = (("vertex", 394, 1, 22), ("product", 393, 2, 29))
    reports = []
    for mode, time, pivot, cap in trials:
        left = projected(states[time], pivot)
        left_path = json.loads((work / f"{mode}_left.json").read_text())
        assert left_path["cyclic_cap"] == cap
        lifted = lift_from(left, left_path["orbit_route"][::-1], cap)
        root_to_left = exact_endpoint(attach_to_ak3(lifted, cap, literal), left)
        assert cyclic_peak(root_to_left) <= cap
        splice = {
            "format": "ordinary-ac-elementary-v1", "start": list(left), "target": list(right),
            "moves": list(reverse_moves(root_to_left["moves"])) + root_to_right["moves"],
        }
        strict = replay(splice)
        assert cyclic_peak(splice) == 37
        left_orbits = [donor_orbit(word) for word in left]
        right_orbits = [donor_orbit(word) for word in right]
        assert {entry["key"] for entry in left_orbits}.isdisjoint(entry["key"] for entry in right_orbits)
        name = f"round09_ac_proof_e20_{mode}_splice.json"
        (certificates / name).write_text(json.dumps(splice, separators=(",", ":")) + "\n")
        reports.append({
            "chart_change": mode, "left_step_pivot": [time, pivot], "right_step_pivot": [394, 2],
            "left_pair": left, "right_pair": right, "root_to_left_orbit_route": left_path["orbit_route"],
            "root_to_left_maximum_cyclic_length": cyclic_peak(root_to_left),
            "left_individual_automorphism_orbits": left_orbits,
            "right_individual_automorphism_orbits": right_orbits,
            "both_receiver_identities_are_necessary": True, "sharp_ordinary_cyclic_peak": 37,
            "strict_replay": strict, "certificate": name,
        })
    return {"cap36_orbit_route_from_E20_to_right": local, "strict_ordinary_splices": reports}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("work", "literal", "certificates"):
        parser.add_argument(name, type=Path)
    print(json.dumps(main(**vars(parser.parse_args())), indent=2))
