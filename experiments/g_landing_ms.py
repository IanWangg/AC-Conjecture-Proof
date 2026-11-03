#!/usr/bin/env python3
"""Agent G: land D's 34 certified MS(3,w) members of AK(3)'s class in the
torus graph (research-g.md, Section 4).

For each member (BS(3,4) relator r, short relator t):
  * if t is of torus type: freeze t, move r exactly to torus-type words;
  * otherwise: find torus-type words u exactly conjugate to t in BS(3,4)
    (g_bs; positives are exact), then freeze u and move r to torus-type words.
Every landing node is compared (Whitehead canonical form) with AK(3)'s torus
island.  Also tests the MS(2) holdout #2.

Usage: python3 experiments/g_landing_ms.py [K P L WINDOW]   (default 8 12 100 30)
"""
import glob
import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g_torus as G  # noqa: E402
import g_bs as B  # noqa: E402


def main():
    K, P, L, WIN = (list(map(int, sys.argv[1:5])) + [8, 12, 100, 30][len(sys.argv[1:5]):])
    here = os.path.dirname(os.path.abspath(__file__))
    members = []
    for f in sorted(glob.glob(os.path.join(here, "..", "certificates", "d_ak3_to_ms*.json"))):
        d = json.load(open(f))
        members.append(tuple(d["target"]))
    WH = G._wh()
    mats = G.gl2_matrices(K)

    def key(node):
        R = G.cyc(G.power("x", node[0]) + G.power("y", node[1]))
        return WH.aut_canon((R, node[2]))

    t0 = time.time()
    isl, _, _ = G.bfs(G.start_node("xxxYYYY", "xyxYXY"), K=16, P=24, maxlen=160, depth=6,
                      max_nodes=3000, log=lambda m: None, complete=True)
    island = set(isl)
    print("AK(3) torus island: %d Aut-orbits" % len(island))

    def land(rbs, frozen):
        M, p, q = frozen
        U = G.cyc(G.apply(G.aut_cached(G.mat_inv(M)), rbs))
        prim = G.primitive_complete(U, p, q) if abs(p) != abs(q) else []
        ks = set()
        for (M2, a, b, w) in G.edges(U, p, q, mats, P=P, maxlen=L):
            if abs(a) >= 2 and abs(b) >= 2:
                ks.add(key((p, q, w, M2, a, b)))
        return ks, prim

    outside = 0
    for (rbs, t) in members:
        tf = G.torus_type(t, 12, 20)
        if tf:
            ks, prim = land(rbs, tf)
            how = "direct"
        else:
            assert G.cyc_canon(rbs) == G.cyc_canon("XyyyxYYYY")
            xe, tw = B.xexp(t), B.tlen(t, 3, 4)
            ks, prim, seen, nconj = set(), [], set(), 0
            for M in mats:
                for p2 in range(-P, P + 1):
                    for target in (xe, -xe):
                        num = target - p2 * M[0][0]
                        if p2 == 0 or M[0][1] == 0 or num % M[0][1]:
                            continue
                        q2 = num // M[0][1]
                        if abs(p2) < 2 or abs(q2) < 2 or abs(q2) > P or math.gcd(p2, q2) != 1:
                            continue
                        u = G.torus_word(M, p2, q2)
                        cu = G.cyc_canon(u)
                        if cu in seen or len(u) > L:
                            continue
                        seen.add(cu)
                        if B.tlen(u, 3, 4) != tw or not B.conjugate(u, t, 3, 4, window=WIN):
                            continue
                        nconj += 1
                        k2, pr2 = land(rbs, (M, p2, q2))
                        ks |= k2
                        prim += pr2
            how = "via %d BS(3,4)-conjugate torus words" % nconj
        outside += len(ks - island)
        print("%-12s %-40s landing orbits %d, in island %d, primitive neighbours %d"
              % (t, how, len(ks), len(ks & island), len(prim)), flush=True)
    ks, prim = land("XyyxYYY", G.torus_type("XXXYxxY", 12, 20))
    print("holdout #2 (XyyxYYY, XXXYxxY): landing orbits %d, primitive neighbours %d" % (len(ks), len(prim)))
    print("landing orbits outside the island: %d   (%.0f s)" % (outside, time.time() - t0))


if __name__ == "__main__":
    main()
