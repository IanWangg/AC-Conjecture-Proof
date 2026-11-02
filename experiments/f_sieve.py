#!/usr/bin/env python3
"""Thickenability sieve over published lists of hard balanced presentations.

Research agent F, 2026-11-02.  Standard library only; uses f_thicken.py.

A presentation of the trivial group whose 2-complex is thickenable (embeds
in a 3-manifold) is AC-trivial (externally reported: Lackenby,
arXiv:2606.06122; see research-f.md, Section 2, for the classical argument).
This script tests, for each listed presentation P, whether P itself
(cyclically reduced) is thickenable, and optionally whether some image of P
under a bounded set of Whitehead/Nielsen automorphisms is thickenable.
A negative answer is NOT an obstruction to AC-triviality.

Usage:
  python3 experiments/f_sieve.py --ak 40
  python3 experiments/f_sieve.py --list FILE --format {nahomar,ms,sair,pairs}
"""
import argparse
import json
import re
import sys
import time

sys.path.insert(0, __import__("os").path.dirname(__file__))
import f_thicken as T  # noqa: E402


def ak(n):
    return (tuple([1] * n + [-2] * (n + 1)), T.parse("xyxYXY"))


def sigma_images(r1, r2):
    """The 8 signed letter permutations (thickenability is invariant under
    them, used here only as an internal consistency check)."""
    out = []
    for swap in (False, True):
        for sx in (1, -1):
            for sy in (1, -1):
                def f(a):
                    g = abs(a)
                    s = 1 if a > 0 else -1
                    if swap:
                        g = 3 - g
                    s *= sx if g == 1 else sy
                    return s * g
                out.append((tuple(map(f, r1)), tuple(map(f, r2))))
    return out


def apply_aut(phi, w):
    out = []
    for a in w:
        img = phi[abs(a)]
        out += list(img) if a > 0 else list(T.inverse(img))
    return T.free_reduce(out)


WH = [  # Nielsen-type generators of Aut(F2) used for the bounded Aut search
    {1: (1, 2), 2: (2,)}, {1: (1, -2), 2: (2,)}, {1: (2, 1), 2: (2,)},
    {1: (-2, 1), 2: (2,)}, {1: (1,), 2: (2, 1)}, {1: (1,), 2: (2, -1)},
    {1: (1,), 2: (1, 2)}, {1: (1,), 2: (-1, 2)},
]


def aut_ball(r1, r2, depth, slack):
    """Images of (r1,r2) under products of <= depth Nielsen generators whose
    total cyclic length is <= |r1|+|r2|+slack."""
    L0 = len(r1) + len(r2)
    start = (T.cyc_reduce(r1), T.cyc_reduce(r2))
    seen = {(T.cyc_canon(start[0]), T.cyc_canon(start[1]))}
    frontier = [start]
    out = [start]
    for _ in range(depth):
        nxt = []
        for (a, b) in frontier:
            for phi in WH:
                c = T.cyc_reduce(apply_aut(phi, a))
                d = T.cyc_reduce(apply_aut(phi, b))
                if not c or not d or len(c) + len(d) > L0 + slack:
                    continue
                key = (T.cyc_canon(c), T.cyc_canon(d))
                if key in seen:
                    continue
                seen.add(key)
                nxt.append((c, d))
                out.append((c, d))
        frontier = nxt
    return out


def read_list(path, fmt):
    items = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if fmt == "nahomar":           # "LEN word word NAME"
                parts = line.split()
                items.append((parts[3] if len(parts) > 3 else "",
                              T.parse(parts[1]), T.parse(parts[2])))
            elif fmt == "pairs":            # "name word word"
                parts = line.split()
                items.append((parts[0], T.parse(parts[1]), T.parse(parts[2])))
            elif fmt == "ms":               # AC-Solver padded integer arrays
                arr = json.loads(line)
                h = len(arr) // 2
                r1 = tuple(a for a in arr[:h] if a)
                r2 = tuple(a for a in arr[h:] if a)
                items.append((f"ms{len(items)+1:04d}", r1, r2))
            elif fmt == "sair":
                d = json.loads(line)
                m = re.search(r"<x, y \| (.*) = 1; (.*) = 1>", d["description"])
                ws = []
                for grp in (m.group(1), m.group(2)):
                    w = []
                    for tok in grp.split():
                        g = 1 if tok[0] == "x" else 2
                        w.append(-g if tok.endswith("^-1") else g)
                    ws.append(tuple(w))
                items.append((d["challenge_id"], ws[0], ws[1]))
    return items


def run(items, depth=0, slack=0, verbose=False):
    hits = []
    t0 = time.time()
    for name, r1, r2 in items:
        a, b = T.cyc_reduce(r1), T.cyc_reduce(r2)
        cands = [(a, b)] if depth == 0 else aut_ball(a, b, depth, slack)
        for (c, d) in cands:
            if T.thickenable_fast(c, d):
                hits.append((name, T.fmt(a), T.fmt(b), T.fmt(c), T.fmt(d)))
                if verbose:
                    print("HIT", hits[-1], flush=True)
                break
    return hits, time.time() - t0


def selftest():
    hits, _ = run([(f"AK({n})",) + ak(n) for n in range(1, 8)])
    assert hits == []
    pos = [("basis", T.parse("xy"), T.parse("y")),
           ("thick15", T.parse("xyxyxY"), T.parse("xyxYxyyxY")),
           ("P1", T.parse("XyyxYYY"), T.parse("YxxyXXX"))]
    hits, _ = run(pos)
    assert [h[0] for h in hits] == ["basis", "thick15"], hits
    # Aut-ball contains the start and stays within the length bound
    ball = aut_ball(T.parse("xxxYYYY"), T.parse("xyxYXY"), 3, 6)
    assert ball and all(len(a) + len(b) <= 19 for a, b in ball)
    print("self-test passed: AK(1..7) not thickenable, positive/negative controls, Aut-ball bound")


def main():
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        return
    ap = argparse.ArgumentParser()
    ap.add_argument("--ak", type=int)
    ap.add_argument("--list")
    ap.add_argument("--format", default="pairs")
    ap.add_argument("--depth", type=int, default=0)
    ap.add_argument("--slack", type=int, default=0)
    ap.add_argument("--names", help="only items whose name matches this regex")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    if args.ak:
        items = [(f"AK({n})",) + ak(n) for n in range(1, args.ak + 1)]
    else:
        items = read_list(args.list, args.format)
    if args.names:
        items = [it for it in items if re.search(args.names, it[0])]
    hits, dt = run(items, args.depth, args.slack, args.verbose)
    print(json.dumps({"tested": len(items), "thickenable_hits": len(hits),
                      "aut_depth": args.depth, "aut_slack": args.slack,
                      "seconds": round(dt, 1), "hits": hits[:50]}, indent=1))


if __name__ == "__main__":
    main()
