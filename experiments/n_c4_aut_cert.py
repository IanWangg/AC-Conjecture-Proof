#!/usr/bin/env python3
"""Certificates C4 -> phi(C4) for automorphisms phi realized on the AC class of
C4 = (x^4 y x^-1 y, x y^3 x y^-2) (agent N, round 4).

A d_acsearch PATH from C4 to a state S' with S' Sigma-equal to phi(C4) is
expanded to strict elementary moves with D's d_certify (read-only), then the
state is brought to the exact freely reduced words of phi(C4) with I's Cert
builder (rotations, inversions, swap, conjugation).  Output format:
ordinary-ac-elementary-v1, replayed by experiments/elementary_verify.py.

Usage: python3 experiments/n_c4_aut_cert.py --self-test
       python3 experiments/n_c4_aut_cert.py --write certificates
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import d_certify  # noqa: E402
import elementary_verify as ev  # noqa: E402
from i_words import Cert, red, subst  # noqa: E402
from i_transport import glue  # noqa: E402
from n_autstab import compose, matrix  # noqa: E402

C4 = ("xxxxyXy", "xyyyxYY")

# Engine output (d_acsearch --cap 24 --source xxxxyXy,xyyyxYY --exact-targets ...), see research-n.md section 3.
PATHS = {
    "m1": {"aut": ["x_xy", "invx"],
           "path": "[xxxxyXy xyyyxYY] [xyyyxYY xxxxyyyyxY] [xyyyxYY xxxyyXyxY] [xyyyxYY xxyyXYXyxY] [xyyyxYY xyxyxYYXyXY] [xyyyxYY xyxyxyxYXY]"},
    "m2": {"aut": ["y_yx", "y_yx", "y_yx", "invx"],
           "path": "[xxxxyXy xyyyxYY] [xxxxyXy xxxyyXYYXy] [xxxxyXy xyXYYXyXY] [xxxxyXy xxxyxYxyyy] [xxxxyXy xxxyxYXXXYxyy] [xxxxyXy xxxyxxxyXYXXXYXy]"},
}


def parse_path(text):
    return [tuple(seg.strip("[] ").split()) for seg in text.split("]") if seg.strip()]


def build(name):
    info = PATHS[name]
    states = parse_path(info["path"])
    img = compose(info["aut"])
    target = [red(subst(w, img)) for w in C4]          # exact phi(C4)
    last = states[-1]
    c1 = d_certify.certificate(states, C4, last, "engine path")
    c = Cert(*C4)
    for mv in c1["moves"]:
        if mv["op"] == "invert":
            c.invert(mv["i"])
        elif mv["op"] == "multiply":
            c.mult(mv["i"])
        else:
            c.conj1(mv["i"], mv["g"])
    assert c.s == [red(w) for w in last], (c.s, last)
    glue(c, target)
    cert = {"format": "ordinary-ac-elementary-v1", "start": list(C4), "target": target, "moves": c.moves,
            "description": "C4 -> phi(C4) exactly, phi = %s (outermost first), matrix (columns = images of x,y) %s; "
                           "engine path (%d cyclic products) expanded by d_certify, then glued to the exact image words. "
                           "Proves phi(C4) ~AC C4 (agent N)." % (" o ".join(info["aut"]), matrix(img), len(states) - 1)}
    r = ev.replay(cert)
    assert r["endpoint"] == target
    return cert, r


def selftest():
    for name in PATHS:
        cert, r = build(name)
        assert r["endpoint"] == cert["target"]
    # the two matrices generate, with -I, a group of order 12 (D6)
    from n_autstab import group_closure
    reps = group_closure([["invx", "invy"]] + [PATHS[n]["aut"] for n in PATHS])
    assert reps is not None and len(reps) == 6
    print("n_c4_aut_cert self-test passed:", {n: (len(build(n)[0]["moves"]), build(n)[1]["peak_total_length"]) for n in PATHS})


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        selftest()
    elif len(sys.argv) == 3 and sys.argv[1] == "--write":
        for name in PATHS:
            cert, r = build(name)
            fn = os.path.join(sys.argv[2], "n_c4_aut_%s.json" % name)
            with open(fn, "w") as f:
                json.dump(cert, f)
            print(fn, r)
    else:
        print(__doc__)
