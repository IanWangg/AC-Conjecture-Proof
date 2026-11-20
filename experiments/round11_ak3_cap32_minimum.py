"""Compile the minimum-energy cap-32 frontier route in a fixed marking."""

import argparse
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from elementary_verify import replay
from round07_automorphism_transport import normalize_pair
from round07_stable_proof_compile_join import compile_local_caps, lift_from
from round08_ak3_acm_search import cyclic_peak


def read_route(path):
    return [tuple(line.split()) for line in path.read_text().splitlines()]


def compile_entry(outer, bridge, inner, literal_path, destination):
    anchored = json.loads(outer.read_text())
    outer_orbits = [tuple(pair) for pair in anchored["orbit_route"]]
    assert anchored["cyclic_cap"] == 32 and outer_orbits[0] == tuple(anchored["lower_anchor"])
    target = outer_orbits[-1]
    assert sum(map(len, target)) == 20
    outward = lift_from(target, outer_orbits[::-1], 32)
    middle = lift_from(outward[-1], read_route(bridge), 31)
    inward = lift_from(middle[-1], read_route(inner), 29)
    with TemporaryDirectory() as scratch:
        path = Path(scratch)
        (path / "target.tsv").write_text("\t".join(inward[-1]) + "\n")
        subprocess.run([str(literal_path.resolve()), "22", str(path / "target.tsv"),
                        str(path / "route.json")], check=True, capture_output=True)
        initial = [tuple(pair) for pair in json.loads((path / "route.json").read_text())["route"]]
    assert initial[-1] == inward[-1]
    route = initial + inward[-2::-1] + middle[-2::-1] + outward[-2::-1]
    certificate, _ = compile_local_caps(route, 32)
    certificate["moves"].extend(normalize_pair(tuple(certificate["target"]), target))
    certificate["target"] = list(target)
    checked = replay(certificate)
    peak = cyclic_peak(certificate)
    assert peak == 32
    destination.write_text(json.dumps(certificate, separators=(",", ":")) + "\n")
    return {"anchored_frontier_route": anchored, "bridge_cap31": read_route(bridge),
            "bridge_cap29": read_route(inner), "full_cyclic_route": route,
            "independent_strict_replay": {**checked, "cyclic_peak": peak}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("outer", "bridge", "inner", "literal_path", "destination"):
        parser.add_argument(name, type=Path)
    print(json.dumps(compile_entry(**vars(parser.parse_args())), indent=2))
