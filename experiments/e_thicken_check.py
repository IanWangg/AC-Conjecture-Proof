#!/usr/bin/env python3
"""Thickenability survey of the explored AC class of AK(3) (research-e.md, Section 6).

Standard library only.  (1) An independent Python implementation of the
one-vertex link criterion is compared with e_thicken.cpp on controls and random
small presentations.  (2) The connected component of AK(3) in G_L (pairs of total
length <= L, the 15 instructions) is enumerated, its members of total length <= T
are reduced modulo the symmetries that preserve the presentation complex up to
homeomorphism (cyclic rotation and inversion of each relator, relator order, and
the 8 signed permutations of {x,y}), and every class is tested with e_thicken.

  python3 experiments/e_thicken_check.py --selftest
  python3 experiments/e_thicken_check.py --survey 17 14     # L=17, lengths <= 14
  e_peak --L 20 --dump 16 2> dump.txt; python3 experiments/e_thicken_check.py --survey-file dump.txt
"""
import itertools
import json
import os
import random
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e_peak_check import neighbours, red

SCRATCH = ("/tmp/claude-0/-home-user-AC-Conjecture-Proof/2793adeb-4b51-5217-aae5-371faac65e22"
           "/scratchpad/agent-e")
BIN = os.environ.get("E_THICKEN_BIN", os.path.join(SCRATCH, "e_thicken"))


# ------------------------------------------------ independent criterion (Python)
def py_thickenable(rels):
    occ = []  # (generator, sign, relator)
    rel_occ = []
    for i, r in enumerate(rels):
        ids = []
        for ch in r:
            ids.append(len(occ))
            occ.append((0 if ch in "xX" else 1, 1 if ch in "xy" else -1, i))
        rel_occ.append(ids)
    n = len(occ)
    # half-edge naming: ('+',k) / ('-',k)
    pair = {}
    for ids in rel_occ:
        for j, k in enumerate(ids):
            k2 = ids[(j + 1) % len(ids)]
            hf = ("+" if occ[k][1] > 0 else "-", k)
            hs = ("-" if occ[k2][1] > 0 else "+", k2)
            pair[hf] = hs
            pair[hs] = hf
    by_gen = [[k for k in range(n) if occ[k][0] == g] for g in (0, 1)]
    verts = {(occ[k][0], s) for k in range(n) for s in "+-"}
    # connected components of the link graph
    parent = {v: v for v in verts}

    def find(v):
        while parent[v] != v:
            v = parent[v]
        return v
    for (s, k), (s2, k2) in pair.items():
        parent[find((occ[k][0], s))] = find((occ[k2][0], s2))
    comps = len({find(v) for v in verts})
    need = n - len(verts) + 2 * comps

    def cyc_orders(items):
        if len(items) <= 1:
            yield list(items)
            return
        for rest in itertools.permutations(items[1:]):
            yield [items[0]] + list(rest)
    for t0 in (False, True):
        for t1 in (False, True):
            nonor = (t0, t1)
            if any(sum(1 for k in ids if nonor[occ[k][0]]) % 2 for ids in rel_occ):
                continue
            for o0 in cyc_orders(by_gen[0]):
                for o1 in cyc_orders(by_gen[1]):
                    rot = {}
                    for g, order in ((0, o0), (1, o1)):
                        d = len(order)
                        for i, k in enumerate(order):
                            rot[("+", k)] = ("+", order[(i + 1) % d])
                            prev = order[(i - 1) % d]
                            nxt = order[(i + 1) % d]
                            rot[("-", k)] = ("-", nxt if nonor[g] else prev)
                    seen, faces = set(), 0
                    for h in pair:
                        if h in seen:
                            continue
                        faces += 1
                        c = h
                        while c not in seen:
                            seen.add(c)
                            c = rot[pair[c]]
                    if faces == need:
                        return True
    return False


def run_bin(lines):
    res = subprocess.run([BIN], input="\n".join(lines) + "\n", capture_output=True, text=True,
                         timeout=2700, check=True)
    return [json.loads(x) for x in res.stdout.strip().splitlines()]


# ------------------------------------------------------------ canonical forms
SIGNED_PERMS = []
for swap in (False, True):
    for sx in (1, -1):
        for sy in (1, -1):
            SIGNED_PERMS.append((swap, sx, sy))


def apply_aut(w, aut):
    swap, sx, sy = aut
    out = []
    for ch in w:
        g = 0 if ch in "xX" else 1
        s = 1 if ch in "xy" else -1
        s *= sx if g == 0 else sy
        if swap:
            g = 1 - g
        out.append(("x" if g == 0 else "y") if s > 0 else ("X" if g == 0 else "Y"))
    return "".join(out)


def cyc_canon(w):
    """Least cyclic rotation of w or w^-1 (w assumed cyclically reduced or not: we cyclically reduce)."""
    w = red(w)
    while len(w) > 1 and w[0] == w[-1].swapcase():
        w = w[1:-1]
    cands = []
    for v in (w, w[::-1].swapcase()):
        cands += [v[i:] + v[:i] for i in range(len(v))] or [v]
    return min(cands)


def canon(a, b):
    best = None
    for aut in SIGNED_PERMS:
        u, v = cyc_canon(apply_aut(a, aut)), cyc_canon(apply_aut(b, aut))
        key = tuple(sorted((u, v), key=lambda s: (len(s), s)))
        if best is None or key < best:
            best = key
    return best


def survey(L, T, max_cost=5 * 10**7):
    from collections import deque
    start = ("xxxYYYY", "xyxYXY")
    seen = {start}
    q = deque([start])
    while q:
        s = q.popleft()
        for t in neighbours(*s):
            if len(t[0]) + len(t[1]) <= L and t not in seen:
                seen.add(t)
                q.append(t)
    assert ("x", "y") not in seen
    low = [s for s in seen if len(s[0]) + len(s[1]) <= T]
    classes = sorted({canon(*s) for s in low}, key=lambda k: (len(k[0]) + len(k[1]), k))
    tested, skipped = [], []
    for u, v in classes:
        dx = sum(ch in "xX" for ch in u + v)
        dy = len(u) + len(v) - dx
        cost = 4 * __import__("math").factorial(max(dx - 1, 0)) * __import__("math").factorial(max(dy - 1, 0))
        (tested if cost <= max_cost else skipped).append((u, v))
    results = run_bin([f"{u} {v}" for u, v in tested]) if tested else []
    thick = [r for r in results if r["thickenable"]]
    out = {"L": L, "component_size": len(seen), "max_total_length_surveyed": T,
           "pairs_surveyed": len(low), "complex_classes": len(classes),
           "classes_tested": len(tested), "classes_skipped_cost": len(skipped),
           "thickenable_classes": [r["relators"] for r in thick],
           "classes_by_total_length": {}}
    for u, v in classes:
        k = str(len(u) + len(v))
        out["classes_by_total_length"][k] = out["classes_by_total_length"].get(k, 0) + 1
    out["examples"] = [list(c) for c in classes[:12]]
    print(json.dumps(out))
    return out


def survey_file(path, max_cost=2 * 10**8):
    """Classes of the pairs listed in `path` (output of e_peak --dump T), tested with e_thicken."""
    import math
    pairs = [tuple(line.split()) for line in open(path) if line.strip()]
    classes = sorted({canon(a, b) for a, b in pairs}, key=lambda k: (len(k[0]) + len(k[1]), k))
    tested, skipped = [], []
    for u, v in classes:
        dx = sum(ch in "xX" for ch in u + v)
        dy = len(u) + len(v) - dx
        cost = 4 * math.factorial(max(dx - 1, 0)) * math.factorial(max(dy - 1, 0))
        (tested if cost <= max_cost else skipped).append((u, v))
    results = run_bin([f"{u} {v}" for u, v in tested]) if tested else []
    by_len = {}
    for u, v in classes:
        by_len[str(len(u) + len(v))] = by_len.get(str(len(u) + len(v)), 0) + 1
    out = {"dump": os.path.basename(path), "pairs": len(pairs), "complex_classes": len(classes),
           "classes_by_total_length": by_len, "classes_tested": len(tested),
           "classes_skipped_cost": len(skipped), "skipped": [list(c) for c in skipped],
           "thickenable_classes": [r["relators"] for r in results if r["thickenable"]],
           "length_13_classes": [list(c) for c in classes if len(c[0]) + len(c[1]) == 13],
           "length_14_classes": [list(c) for c in classes if len(c[0]) + len(c[1]) == 14]}
    print(json.dumps(out))
    return out


def selftest():
    fails = 0
    controls = [(["x", "y"], True), (["xyXY"], True), (["xyxY"], True), (["xx"], True),
                (["xxx"], True), (["xxX"], True), (["xYY", "xyxYXY"], None),
                (["xxYYY", "xyxYXY"], None), (["xxxYYYY", "xyxYXY"], None)]
    random.seed(7)
    for _ in range(40):
        rels = []
        for _ in range(random.choice((1, 2))):
            w = red("".join(random.choice("xXyY") for _ in range(random.randint(2, 7))))
            if w:
                rels.append(w)
        if rels:
            controls.append((rels, None))
    lines = [" ".join(r) for r, _ in controls]
    cres = run_bin(lines)
    for (rels, want), cr in zip(controls, cres):
        p = py_thickenable(rels)
        ok = (p == cr["thickenable"]) and (want is None or want == p)
        fails += not ok
        if not ok or want is not None or len(rels) == 2 and rels[1] == "xyxYXY":
            print(("ok   " if ok else "FAIL ") + f"{rels}: python={p} c++={cr['thickenable']}")
    print(json.dumps({"thicken_selftest": "passed" if not fails else "FAILED",
                      "cases": len(controls), "failures": fails}))
    return fails


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        sys.exit(1 if selftest() else 0)
    if sys.argv[1:2] == ["--survey-file"]:
        survey_file(sys.argv[2])
    if sys.argv[1:2] == ["--survey"]:
        survey(int(sys.argv[2]), int(sys.argv[3]))
