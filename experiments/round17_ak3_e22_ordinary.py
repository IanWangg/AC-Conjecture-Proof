"""Lift a signed-orbit boundary bridge from AK(3) to its exact ordered endpoint."""

import argparse
import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from elementary_verify import replay
from round07_automorphism_transport import normalize_pair
from round07_stable_proof_compile_join import compile_local_caps, lift_from
from round08_ak3_acm_search import cyclic_peak

E22 = ("XXYYYxYXY", "XXYYxYXXyxxY")


def rows(path):
    return [tuple(line.split()) for line in path.read_text().splitlines()]


def compile_path(reverse, middle, inner, literal_path):
    entry = json.loads(reverse.read_bytes())
    if "orbit_route" in entry:
        cap = entry["cyclic_cap"]
        target_pair = tuple(entry["orbit_route"][-1])
        orbit_path = entry["orbit_route"][::-1]
        assert orbit_path[-1] == entry["lower_anchor"]
    else:
        cap = entry["cap"]
        assert cap == 37 and entry["seed_anchor"]
        target_pair = E22
        orbit_path = entry["route"] + [entry["seed_anchor"]]
    outward = lift_from(target_pair, orbit_path, cap)
    to_low = lift_from(outward[-1], rows(middle), 32)
    to_inner = lift_from(to_low[-1], rows(inner), 29)
    with TemporaryDirectory() as scratch:
        work = Path(scratch)
        target = work / "target.tsv"
        target.write_text("\t".join(to_inner[-1]) + "\n")
        literal = work / "literal.json"
        subprocess.run([str(literal_path.resolve()), "22", str(target), str(literal)],
                       check=True, capture_output=True)
        base = [tuple(pair) for pair in json.loads(literal.read_bytes())["route"]]
    assert base[-1] == to_inner[-1]
    full = base + to_inner[-2::-1] + to_low[-2::-1] + outward[-2::-1]
    certificate, first_replay = compile_local_caps(full, cap)
    certificate["moves"].extend(normalize_pair(tuple(certificate["target"]), target_pair))
    certificate["target"] = list(target_pair)
    final = replay(certificate)
    final["cyclic_peak"] = cyclic_peak(certificate)
    assert final["cyclic_peak"] == cap
    return certificate, {"pre_normalization": first_replay, "final": final, "marked_cyclic_route": full}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("reverse", "middle", "inner", "literal_path", "certificate"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    proof, receipt = compile_path(args.reverse, args.middle, args.inner, args.literal_path)
    args.certificate.write_text(json.dumps(proof, separators=(",", ":")) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
