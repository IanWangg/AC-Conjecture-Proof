#!/usr/bin/env python3
"""Explore an AC class by GS-type moves and test every state for thickenability.

Research agent F, 2026-11-02.  Standard library only.

States: unordered pairs of cyclically reduced words modulo rotation, inversion,
relator swap and the 8 signed letter permutations (AC-triviality is invariant
under all of these).  Moves: u <- CR(rot_i(u) * c * rot_j(v^e) * c^-1) for
conjugators c with |c| <= K, keeping total length <= cap.  Every move is a
composite of ordinary AC moves, so every visited state is AC-equivalent (up to
a signed letter permutation) to the start.  A thickenable visited state of a
trivial-group class would prove the start AC-trivial (Theorem 2.1 of
research-f.md) and its descent would give an explicit certificate.

This is a bounded experiment, NOT an exhaustive elementary-graph search.
Usage: python3 experiments/f_component_sieve.py w1 w2 --cap 18 --K 0
"""
import argparse
import collections
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
import f_thicken as T  # noqa: E402
import f_knotlike as KL  # noqa: E402

SIGNED = []
for swap in (False, True):
    for sx in (1, -1):
        for sy in (1, -1):
            SIGNED.append((swap, sx, sy))


def relabel(w, s):
    swap, sx, sy = s
    out = []
    for a in w:
        g = abs(a)
        sg = 1 if a > 0 else -1
        if swap:
            g = 3 - g
        sg *= sx if g == 1 else sy
        out.append(sg * g)
    return tuple(out)


def key(u, v):
    best = None
    for s in SIGNED:
        a, b = T.cyc_canon(relabel(u, s)), T.cyc_canon(relabel(v, s))
        k = (a, b) if a <= b else (b, a)
        if best is None or k < best:
            best = k
    return best


def conjugators(K):
    out = [()]
    fr = [()]
    for _ in range(K):
        nf = []
        for w in fr:
            for g in (1, -1, 2, -2):
                if not w or w[-1] != -g:
                    nf.append(w + (g,))
        out += nf
        fr = nf
    return out


def neighbours(u, v, cap, conj):
    for (a, b) in ((u, v), (v, u)):
        for i in range(len(a)):
            ar = a[i:] + a[:i]
            for e in (1, -1):
                be = b if e == 1 else T.inverse(b)
                for j in range(len(be)):
                    br = be[j:] + be[:j]
                    for c in conj:
                        w = T.cyc_reduce(ar + c + br + T.inverse(c))
                        if w and len(w) + len(b) <= cap:
                            yield w, b


def run(r1, r2, cap, K, limit, dump=None):
    conj = conjugators(K)
    start = (T.cyc_reduce(r1), T.cyc_reduce(r2))
    seen = {key(*start): start}
    queue = collections.deque([start])
    hits = []
    knotlike = 0
    by_len = collections.Counter()
    t0 = time.time()
    while queue and len(seen) < limit:
        u, v = queue.popleft()
        by_len[len(u) + len(v)] += 1
        if T.thickenable_fast(u, v):
            hits.append((T.fmt(u), T.fmt(v)))
        if not KL.knotlike_obstructed(u, v):
            knotlike += 1
            if dump is not None:
                dump.write(f"{len(u)+len(v)} {T.fmt(u)} {T.fmt(v)}\n")
        for w, b in neighbours(u, v, cap, conj):
            k = key(w, b)
            if k not in seen:
                seen[k] = (w, b)
                queue.append((w, b))
    return {"start": [T.fmt(start[0]), T.fmt(start[1])], "cap": cap, "K": K,
            "states_visited": sum(by_len.values()), "states_seen": len(seen),
            "complete": not queue, "by_total_length": dict(sorted(by_len.items())),
            "alexander_symmetric_states": knotlike,
            "thickenable_hits": hits[:20], "n_hits": len(hits),
            "seconds": round(time.time() - t0, 1)}


def selftest():
    triv = run(T.parse("xy"), T.parse("y"), 9, 0, 10**5)
    assert triv["complete"] and triv["n_hits"] > 0
    ak3 = run(T.parse("xxxYYYY"), T.parse("xyxYXY"), 18, 0, 10**5)
    assert ak3["complete"] and ak3["states_seen"] == 542 and ak3["n_hits"] == 0
    print("self-test passed: trivial class has thickenable states; AK(3) cap-18 class "
          "has 542 states, none thickenable")


def main():
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        return
    ap = argparse.ArgumentParser()
    ap.add_argument("w1")
    ap.add_argument("w2")
    ap.add_argument("--cap", type=int, default=17)
    ap.add_argument("--K", type=int, default=0)
    ap.add_argument("--limit", type=int, default=400000)
    ap.add_argument("--dump", help="write Alexander-symmetric states to this file")
    a = ap.parse_args()
    dump = open(a.dump, "w") if a.dump else None
    print(json.dumps(run(T.parse(a.w1), T.parse(a.w2), a.cap, a.K, a.limit, dump), indent=1))


if __name__ == "__main__":
    main()
