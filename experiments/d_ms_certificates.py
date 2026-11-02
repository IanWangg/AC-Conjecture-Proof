#!/usr/bin/env python3
"""Turn d_acsearch HIT/PATH output for exact (Sigma) Miller-Schupp targets
into one ordinary-AC certificate per hit: AK(3) -> exact benchmark tuple.

Usage:
  python3 experiments/d_ms_certificates.py RUN_OUTPUT MS_TARGETS OUT_DIR [SRC START1 START2 PREFIX]
(optional: only hits of source index SRC, starting from the exact tuple
(START1, START2); output files PREFIX_to_msNNNN.json; default: source 0 = AK(3)).
RUN_OUTPUT : stdout of d_acsearch run with --exact-targets MS_TARGETS
MS_TARGETS : the MS.tgt file written by d_prepare_targets.py
Every certificate is replayed with experiments/elementary_verify.py
before it is written.  Standard library only.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import d_certify  # noqa: E402
import elementary_verify  # noqa: E402

AK3 = ("xxxYYYY", "xyxYXY")


def main(run, tgt, outdir, src="0", s1=AK3[0], s2=AK3[1], prefix="d_ak3"):
    start = (s1, s2)
    words = {}
    for line in open(tgt):
        i, a, b = line.split()
        words[i] = (a, b)
    paths = {}
    hitsrc = {}
    for line in open(run):
        if line.startswith("HIT "):
            f = line.split()
            hitsrc.setdefault(f[2], f[-1])
        if line.startswith("PATH "):
            tag = line.split()[1]
            states = re.findall(r"\[([xXyY]+) ([xXyY]+)\]", line)
            if tag.startswith("MS:") and hitsrc.get(tag) == src:
                paths.setdefault(tag, states)
    os.makedirs(outdir, exist_ok=True)
    summary = []
    for tag in sorted(paths, key=lambda t: int(t.split(":")[1])):
        target = words[tag]
        cert = d_certify.certificate(paths[tag], start, target,
                                     f"{start} -> 1190MS benchmark line {tag.split(':')[1]} "
                                     f"(ACSolverX data/1190MS.txt, commit 6a12515), exact tuple")
        r = elementary_verify.replay(cert)
        assert r["endpoint"] == list(target)
        fn = os.path.join(outdir, f"{prefix}_to_ms{int(tag.split(':')[1]):04d}.json")
        with open(fn, "w") as f:
            json.dump(cert, f, separators=(",", ":"))
        summary.append((tag, target, len(paths[tag]) - 1, r["moves"], r["peak_total_length"]))
        print(f"{tag} {target[0]} {target[1]} len={len(target[0]) + len(target[1])} "
              f"cyclic_steps={len(paths[tag]) - 1} elementary={r['moves']} peak={r['peak_total_length']} -> {fn}")
    print(f"{len(summary)} certificates written and replayed")


if __name__ == "__main__":
    main(*sys.argv[1:])
