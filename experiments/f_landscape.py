#!/usr/bin/env python3
"""Classify presentations by Aut(F2)-invariant thickenability obstructions.

Research agent F, 2026-11-02.  Standard library only.

For each presentation (r1, r2) of the trivial group report:
  * the Alexander polynomial of <x,y|r_i> for i = 1, 2 (Fox calculus);
  * type "Alexander-asymmetric" if some Delta_i is asymmetric (Proposition F2: then no
    image of the presentation under Aut(F2), rotations, inversions or swap is
    thickenable);
  * type "torus-meridian" if some r_i is carried by an automorphism to a
    torus-knot relator x^p y^q and the other relator's image has cyclic
    syllable length != 2 in C_|p| * C_|q| (Proposition F3);
  * "unobstructed" otherwise (no conclusion).

Usage: python3 experiments/f_landscape.py FILE   (lines "LEN w1 w2 [NAME]")
       python3 experiments/f_landscape.py --selftest
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import f_thicken as T  # noqa: E402
import f_knotlike as K  # noqa: E402


def classify(r1, r2, depth=5):
    d1, d2 = K.alexander(r1), K.alexander(r2)
    info = {"delta1": d1, "delta2": d2}
    if not K.symmetric(d1) or not K.symmetric(d2):
        info["type"] = "Alexander-asymmetric"
        return info
    for i, (u, v) in enumerate(((r1, r2), (r2, r1))):
        m = K.meridian_test(u, v, depth)
        if m and m["syllable_length"] != 2:
            info["type"] = "torus-meridian"
            info["torus_relator"] = i + 1
            info["torus"] = (m["p"], m["q"])
            info["partner_syllables"] = m["syllable_length"]
            return info
    info["type"] = "unobstructed"
    return info


def selftest():
    P = T.parse
    assert classify(P("xxxYYYY"), P("xyxYXY"))["type"] == "torus-meridian"
    assert classify(P("XyyxYYY"), P("YxxyXXX"))["type"] == "Alexander-asymmetric"
    # a thickenable (hence unobstructed) presentation must never be obstructed
    for a, b in (("xyxyxY", "xyxYxyyxY"), ("xxyxyxy", "xxyxyxxyy"),
                 ("xxyxxyy", "xxxyyxxyy"), ("x", "y")):
        assert T.thickenable_fast(P(a), P(b))
        assert classify(P(a), P(b))["type"] == "unobstructed", (a, b)
    print("self-test passed")


def main():
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        return
    counts = collections.Counter()
    by_len = collections.Counter()
    examples = {}
    for line in open(sys.argv[1]):
        parts = line.split()
        if len(parts) < 3:
            continue
        L, a, b = int(parts[0]), T.parse(parts[1]), T.parse(parts[2])
        c = classify(a, b)
        counts[c["type"]] += 1
        by_len[(L, c["type"])] += 1
        examples.setdefault(c["type"], []).append(" ".join(parts[:4]))
    print(json.dumps({"counts": counts, "by_length": {f"{k[0]}:{k[1]}": v for k, v in sorted(by_len.items())},
                      "unobstructed_examples": examples.get("unobstructed", [])[:40]}, indent=1))


if __name__ == "__main__":
    main()


def meridian_defect(r1, r2, depth=5):
    """Smallest partner syllable length over the relators that admit a
    torus-knot form (None if neither does).  2 is necessary for
    thickenability (Proposition F3)."""
    best = None
    for (u, v) in ((r1, r2), (r2, r1)):
        m = K.meridian_test(u, v, depth)
        if m and (best is None or m["syllable_length"] < best):
            best = m["syllable_length"]
    return best
