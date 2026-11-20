"""Lift the cap-37 signed-orbit bridge to the exact ordered E22 endpoint."""

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
    assert entry["cap"] == 37 and entry["seed_anchor"]
    outward = lift_from(E22, entry["route"] + [entry["seed_anchor"]], 37)
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
    certificate, first_replay = compile_local_caps(full, 37)
    certificate["moves"].extend(normalize_pair(tuple(certificate["target"]), E22))
    certificate["target"] = list(E22)
    final = replay(certificate)
    final["cyclic_peak"] = cyclic_peak(certificate)
    assert final["cyclic_peak"] == 37
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
