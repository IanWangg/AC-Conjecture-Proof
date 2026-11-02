#!/usr/bin/env python3
"""Independent cross-check of e_peak.cpp (research-e.md, Section 5).

Standard library only.  Recomputes, by a separate string-based BFS, the connected
component of a pair in the graph G_L (pairs of freely reduced words, total length
<= L, edges = the 15 instructions), and compares the component size, the
length histogram, and whether (x,y) is reached with the C++ output.

  python3 experiments/e_peak_check.py            # AK(3) L=13..17, AK(2) L=11..12, control
  E_PEAK_BIN=/path/to/e_peak python3 experiments/e_peak_check.py
  python3 experiments/e_peak_check.py --cert   # writes certificates/e_ak2_peak13_trivialization.json

Build the binary first:  g++ -O2 -std=c++17 -o <bin> experiments/e_peak.cpp
"""
import json
import os
import subprocess
import sys
from collections import Counter, deque

BIN = os.environ.get("E_PEAK_BIN", os.path.join(
    "/tmp/claude-0/-home-user-AC-Conjecture-Proof/2793adeb-4b51-5217-aae5-371faac65e22",
    "scratchpad/agent-e/e_peak"))


def red(w):
    out = []
    for ch in w:
        if out and out[-1] == ch.swapcase():
            out.pop()
        else:
            out.append(ch)
    return "".join(out)


def inv(w):
    return w[::-1].swapcase()


def neighbours(a, b):
    yield inv(a), b
    yield a, inv(b)
    yield b, a
    yield red(a + b), b
    yield red(a + inv(b)), b
    yield a, red(b + a)
    yield a, red(b + inv(a))
    for g in "xXyY":
        yield red(inv(g) + a + g), b
    for g in "xXyY":
        yield a, red(inv(g) + b + g)


def component(a, b, L):
    start = (red(a), red(b))
    seen = {start}
    q = deque([start])
    while q:
        s = q.popleft()
        for t in neighbours(*s):
            if len(t[0]) + len(t[1]) <= L and t not in seen:
                seen.add(t)
                q.append(t)
    hist = Counter(len(s[0]) + len(s[1]) for s in seen)
    return len(seen), ("x", "y") in seen, dict(sorted(hist.items()))


def cxx(a, b, L):
    out = subprocess.run([BIN, "--L", str(L), "--start", a, b], capture_output=True,
                         text=True, timeout=3000, check=True).stdout
    return json.loads(out)


def write_ak2_certificate():
    """Shortest AK(2) path inside G_13 -> ordinary-ac-elementary-v1 certificate."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from e_nilpotent_tables import to_elementary, replay
    import elementary_verify
    a, b = "xxYYY", "xyxYXY"
    out = subprocess.run([BIN, "--L", "13", "--start", a, b, "--path"], capture_output=True,
                         text=True, timeout=3000, check=True).stdout
    d = json.loads(out)
    path = d["path"]
    assert d["contains_xy"] and len(path) == d["bfs_depth_to_xy"]
    assert replay(a, b, path) == ("x", "y")
    # peak of the 15-instruction path itself
    s, peak = (a, b), len(a) + len(b)
    for m in path:
        s = next(t for i, t in enumerate(neighbours(*s)) if i == m)
        peak = max(peak, len(s[0]) + len(s[1]))
    cert = {"format": "ordinary-ac-elementary-v1", "start": [a, b], "target": ["x", "y"],
            "moves": to_elementary(path),
            "description": ("AK(2) = <x,y | x^2 y^-3, xyx y^-1 x^-1 y^-1> to (x,y). Expanded from a "
                            f"shortest {len(path)}-instruction path inside G_13 (all intermediate "
                            "pairs of total length <= 13) found by e_peak.cpp --path; G_12 contains "
                            "no such path. Control for research-e.md; AK(2) triviality is classical.")}
    res = elementary_verify.replay(cert)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "certificates", "e_ak2_peak13_trivialization.json"), "w") as f:
        json.dump(cert, f, indent=1)
    print(json.dumps({"instructions": len(path), "instruction_path_peak": peak,
                      "elementary_moves": res["moves"],
                      "elementary_peak_total_length": res["peak_total_length"]}))


def main():
    cases = [("xxxYYYY", "xyxYXY", L) for L in (13, 14, 15, 16, 17)]
    cases += [("xxYYY", "xyxYXY", L) for L in (11, 12)]
    cases += [("xx", "xyXY", 10)]          # Z/2 x Z: never reaches (x,y)
    cases += [("xYY", "xyxYXY", 9)]        # AK(1): trivial at its own length
    fails = 0
    for a, b, L in cases:
        size, has_xy, hist = component(a, b, L)
        d = cxx(a, b, L)
        ok = (d["component_complete"] and d["component_size"] == size
              and d["contains_xy"] == has_xy
              and {int(k): v for k, v in d["count_by_total_length"].items()} == hist)
        fails += not ok
        print(("ok   " if ok else "FAIL ") +
              f"({a},{b}) L={L}: size {size}, contains (x,y): {has_xy}, histogram {hist}")
    print(json.dumps({"peak_crosscheck": "passed" if not fails else "FAILED", "failures": fails}))
    return fails


if __name__ == "__main__":
    if sys.argv[1:] == ["--cert"]:
        write_ak2_certificate()
    else:
        sys.exit(1 if main() else 0)
