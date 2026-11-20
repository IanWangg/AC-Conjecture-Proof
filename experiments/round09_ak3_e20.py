"""Check the cap-36 enclosure and compile the cap-37 marked ordinary join."""

import argparse
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from elementary_verify import replay
from free_waypoint_search import canonical, cyclic
from round05_ak3_orbit_audit import MAPS
from round06_stable_proof_cap23_charts import compact_row
from round07_automorphism_transport import normalize_pair
from round07_stable_proof_compile_join import compile_local_caps, lift_from
from round08_ak3_acm_search import cyclic_peak


ROOT = Path(__file__).resolve().parents[1]
E20 = ("XXXYYXYXy", "XYYXyXYYxyy")
MARKED = ("XXXYXyXyy", "XYXyyXYYxyy")


def rows(path):
    return [tuple(line.split()) for line in path.read_text().splitlines()]


def prepare(work, literal_path, destination):
    cap36 = json.loads((work / "e20x36.json").read_text())
    check = json.loads((work / "e20x36.audit.json").read_text())
    prim = json.loads((work / "e20x36.primitive.json").read_text())
    assert cap36["closed"] and not cap36["primitive_found"] and not cap36["target_found"]
    assert cap36["minimum_cyclic_energy"] == 20
    assert check["status"] == "CLOSED_AND_CONNECTED" and check["cyclic_cap"] == cap36["cyclic_cap"] == 36
    assert check["signed_permutation_orbits"] == cap36["discovered_orbits"] == prim["rows"]
    assert check["rotation_product_candidates"] == cap36["product_candidates"]
    assert check["admitted_neighbors"] == cap36["admitted_product_candidates"]
    assert not prim["primitive_coordinates"]

    matches = [mark for mark in MAPS if tuple(canonical(word.translate(mark)) for word in E20) == MARKED]
    assert len(matches) == 1 and compact_row(E20) == compact_row(MARKED)
    stable_rank3 = json.loads((ROOT / "results/round09_stable_proof_e20_rank3.json").read_text())
    assert tuple(stable_rank3["strict_signed_chart"]["projected_pair"]) == MARKED

    local_path = rows(work / "e20x37.route.tsv")
    local_run = json.loads((work / "e20x37.json").read_text())
    prefix = json.loads((work / "e20anchor.orbit.json").read_text())
    assert local_run["target_found"] and local_run["cyclic_cap"] == 37
    assert prefix["cyclic_cap"] == 29 and local_path[-1] == tuple(prefix["orbit_route"][-1])
    there = lift_from(MARKED, local_path, 37)
    back = lift_from(there[-1], prefix["orbit_route"][::-1], 29)
    with TemporaryDirectory() as scratch:
        folder = Path(scratch)
        (folder / "roots.tsv").write_text("\t".join(back[-1]) + "\n")
        subprocess.run([str(literal_path), "22", str(folder / "roots.tsv"), str(folder / "signed.json")],
                       check=True, capture_output=True)
        seed = json.loads((folder / "signed.json").read_text())
    route = list(map(tuple, seed["route"])) + back[-2::-1] + there[-2::-1]
    assert max(sum(map(len, pair)) for pair in route) == 37
    cert, _ = compile_local_caps(route, 37)
    cert["moves"].extend(normalize_pair(tuple(cert["target"]), MARKED))
    cert["target"] = list(MARKED)
    verified = replay(cert)
    assert cyclic_peak(cert) == 37 and all(word == cyclic(word) for word in cert["target"])
    destination.write_text(json.dumps(cert, separators=(",", ":")) + "\n")
    return {
        "original_projection": E20,
        "literal_endpoint_shared_with_stable_certificate": MARKED,
        "translation_from_original_projection": "xXyY".translate(matches[0]),
        "cap36_generator": cap36,
        "cap36_independent_closure": check,
        "cap36_independent_primitive": prim,
        "cap37_local_join_scan": local_run,
        "cap37_orbit_route_to_cap29_anchor": local_path,
        "cap29_orbit_route_from_AK3": prefix["orbit_route"],
        "strict_replay": {**verified, "cyclic_peak": 37},
        "sharp_ordinary_cyclic_entry_peak": 37,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("work", "literal_path", "destination"):
        parser.add_argument(name, type=Path)
    print(json.dumps(prepare(**vars(parser.parse_args())), indent=2))
