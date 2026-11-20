"""Compile the energy-17 cap-31 entry from its two cyclic route segments."""

import argparse
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from elementary_verify import replay
from round07_automorphism_transport import normalize_pair
from round07_stable_proof_compile_join import compile_local_caps, lift_from
from round08_ak3_acm_search import cyclic_peak


TARGET = ("xxyXYXy", "xxYXYxYYXY")


def read_route(path):
    return [tuple(line.split()) for line in path.read_text().splitlines()]


def compile_entry(bridge, anchor, literal_path, destination):
    outer = lift_from(TARGET, read_route(bridge), 31)
    inner = lift_from(outer[-1], read_route(anchor), 29)
    with TemporaryDirectory() as scratch:
        path = Path(scratch)
        (path / "target.tsv").write_text("\t".join(inner[-1]) + "\n")
        subprocess.run([str(literal_path), "22", str(path / "target.tsv"), str(path / "route.json")],
                       check=True, capture_output=True)
        initial = [tuple(pair) for pair in json.loads((path / "route.json").read_text())["route"]]
    assert initial[-1] == inner[-1]
    route = initial + inner[-2::-1] + outer[-2::-1]
    certificate, _ = compile_local_caps(route, 31)
    certificate["moves"].extend(normalize_pair(tuple(certificate["target"]), TARGET))
    certificate["target"] = list(TARGET)
    checked = replay(certificate)
    peak = cyclic_peak(certificate)
    assert peak == 31
    destination.write_text(json.dumps(certificate, separators=(",", ":")) + "\n")
    return {"bridge_orbit_route_to_cap29": read_route(bridge),
            "anchor_orbit_route_to_cap22": read_route(anchor), "full_cyclic_route": route,
            "independent_strict_replay": {**checked, "cyclic_peak": peak},
            "sharp_ordinary_cyclic_entry_peak": peak}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("bridge", "anchor", "literal_path", "destination"):
        parser.add_argument(name, type=Path)
    print(json.dumps(compile_entry(**vars(parser.parse_args())), indent=2))
