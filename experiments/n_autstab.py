#!/usr/bin/env python3
"""Automorphisms realized on an AC class, extracted from Aut(F2)-orbit
coincidences between *different* states of a forward set (agent N, round 4).

Input: a state dump of D's engine (`d_acsearch --dump C file`): lines
"w1 w2 energy barrier src".  Every dumped state is ordinary-AC-equivalent to
the source P0.  If two distinct Sigma-states S, S' of the dump lie in one
Out(F2)-orbit, S' = phi(S) up to Sigma, then phi(P0) ~ phi(S) ~ S' ~ P0, so
the matrix mu(phi) lies in the stabilizer S^(P0) = {M : phi_M(P0) ~ P0}.
The script groups the dump by D's Whitehead canonical form (imported from
experiments/d_whitehead.py), recovers an explicit automorphism for every
coincidence that is not explained by iota = (x->X, y->Y) alone, and reports
the realized matrices modulo +-I together with representative pairs.

Usage:
  python3 experiments/n_autstab.py --self-test
  python3 experiments/n_autstab.py DUMP [--max N] [--out result.json] [--explain]
"""
import json
import os
import random
import sys
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d_whitehead as W  # noqa: E402  (read-only reuse of D's canonical form)

INV = W.INV
# Elementary automorphisms as letter substitutions (image of x and y).
GENS = {
    "x_xy": {"x": "xy", "y": "y"}, "x_xY": {"x": "xY", "y": "y"},
    "y_yx": {"x": "x", "y": "yx"}, "y_yX": {"x": "x", "y": "yX"},
    "swap": {"x": "y", "y": "x"}, "invx": {"x": "X", "y": "y"},
    "invy": {"x": "x", "y": "Y"},
}
INVERSE = {"x_xy": "x_xY", "x_xY": "x_xy", "y_yx": "y_yX", "y_yX": "y_yx",
           "swap": "swap", "invx": "invx", "invy": "invy"}


def subst(w, img):
    out = []
    for c in w:
        base = c.lower()
        s = img[base]
        out.append(s if c == base else W.inverse(s))
    return W.cycred("".join(out))


def compose(names):
    """Substitution of the automorphism g1 o g2 o ... o gk (names[0] outermost)."""
    img = {"x": "x", "y": "y"}
    for g in reversed(names):
        G = GENS[g]
        img = {k: "".join(G[c] if c.islower() else W.inverse(G[c.lower()]) for c in v) for k, v in img.items()}
        img = {k: freered(v) for k, v in img.items()}
    return img


def freered(w):
    out = []
    for c in w:
        if out and out[-1] == INV[c]:
            out.pop()
        else:
            out.append(c)
    return "".join(out)


def apply_img(img, p):
    return tuple(subst(w, img) for w in p)


def matrix(img):
    """Abelianization matrix: columns are exponent vectors of img[x], img[y]."""
    def ev(w):
        return (w.count("x") - w.count("X"), w.count("y") - w.count("Y"))
    a, b = ev(img["x"]), ev(img["y"])
    return ((a[0], b[0]), (a[1], b[1]))


def canon(p):
    return W.canon_pair(p)


def find_aut(s, r, max_states=300000):
    """Return names with compose(names)(s) Sigma-equal to r, or None.
    Greedy Whitehead reduction of both, then BFS through minimal pairs with the
    four type-II maps and the three signed-permutation generators."""
    def reduce_path(p):
        names, cur = [], tuple(W.cycred(w) for w in p)
        while True:
            best = None
            for g in ("x_xy", "x_xY", "y_yx", "y_yX"):
                q = apply_img(GENS[g], cur)
                if all(q) and sum(map(len, q)) < sum(map(len, cur)) and (best is None or sum(map(len, q)) < sum(map(len, best[1]))):
                    best = (g, q)
            if best is None:
                return names, cur
            names, cur = [best[0]] + names, best[1]
    a_names, smin = reduce_path(s)
    b_names, rmin = reduce_path(r)
    L = sum(map(len, smin))
    if L != sum(map(len, rmin)):
        return None
    start, goal = canon(smin), canon(rmin)
    prev = {start: None}
    dq = deque([(start, smin)])
    while dq and len(prev) < max_states:
        key, p = dq.popleft()
        if key == goal:
            break
        for g in GENS:
            q = apply_img(GENS[g], p)
            if sum(map(len, q)) != L or not all(q):
                continue
            k = canon(q)
            if k not in prev:
                prev[k] = (key, g)
                dq.append((k, q))
    if goal not in prev:
        return None
    path, k = [], goal
    while prev[k] is not None:
        k, g = prev[k]
        path.append(g)
    names = [INVERSE[g] for g in reversed(b_names)] + path + a_names
    img = compose(names)
    if canon(apply_img(img, s)) != canon(r):
        raise AssertionError("automorphism check failed")
    return names


def iota(p):
    return tuple(W.cycred(w.swapcase()) for w in p)


def analyse(states, source=None, max_pairs=50, verbose=True, bfs=300000):
    groups = defaultdict(list)
    for i, p in enumerate(states):
        groups[W.aut_canon(p)].append(i)
        if verbose and (i + 1) % 20000 == 0:
            print(f"  canonicalized {i+1}/{len(states)}", file=sys.stderr, flush=True)
    sizes = defaultdict(int)
    for g in groups.values():
        sizes[len(g)] += 1
    keyset = {canon(p): i for i, p in enumerate(states)}
    iota_closed = sum(1 for p in states if canon(iota(p)) in keyset)
    iota_fixed = sum(1 for p in states if canon(iota(p)) == canon(p))
    result = {"states": len(states), "orbits": len(groups), "orbit_size_histogram": dict(sorted(sizes.items())),
              "iota_closed": iota_closed, "iota_fixed": iota_fixed, "matrices": {}, "examples": []}
    # coincidences not explained by iota: orbits containing a state not in {S, iota S} for a chosen S
    n_pairs = 0
    for key, idx in groups.items():
        if len(idx) < 2:
            continue
        base = states[idx[0]]
        ib = canon(iota(base))
        for j in idx[1:]:
            if canon(states[j]) == ib:
                continue
            names = find_aut(base, states[j], max_states=bfs)
            if names is None:
                result.setdefault("unrecovered", 0)
                result["unrecovered"] += 1
                continue
            M = matrix(compose(names))
            Mn = tuple(tuple(-v for v in row) for row in M)
            mk = str(min(M, Mn))
            result["matrices"][mk] = result["matrices"].get(mk, 0) + 1
            if n_pairs < max_pairs:
                result["examples"].append({"from": list(base), "to": list(states[j]), "aut": names, "matrix": M})
                n_pairs += 1
    result["_groups"] = groups
    return result


def matmul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def group_closure(gen_names, limit=200, mod_sign=False):
    """Closure of the matrices of the given automorphisms (exact matrices, i.e.
    elements of Out(F2) = GL2(Z); mod +-I if mod_sign), with a representative
    name-list for each element.  Returns dict mat->names, or None if the
    closure exceeds `limit` elements (infinite group suspected)."""
    def key(M):
        if not mod_sign:
            return M
        Mn = tuple(tuple(-v for v in row) for row in M)
        return min(M, Mn)
    I = ((1, 0), (0, 1))
    reps = {key(I): []}
    frontier = [[]]
    gens = [(list(n), matrix(compose(n))) for n in gen_names]
    while frontier:
        new = []
        for names in frontier:
            M = matrix(compose(names)) if names else I
            for gn, gM in gens:
                P = matmul(gM, M)          # g o (names)
                k = key(P)
                if k not in reps:
                    reps[k] = gn + names
                    new.append(gn + names)
                    if len(reps) > limit:
                        return None
        frontier = new
    return reps


def explain(states, result, extra_gens=(("invx", "invy"),)):
    """Check that every Out-orbit coincidence inside the dump is produced by
    the group generated (mod +-I) by the recovered automorphisms and iota."""
    gen_names = [tuple(ex["aut"]) for ex in result["examples"]]
    seen, gens = set(), []
    for g in list(extra_gens) + gen_names:
        k = str(matrix(compose(list(g))))
        if k not in seen:
            seen.add(k)
            gens.append(list(g))
    reps = group_closure(gens)
    if reps is None:
        return {"group_order": None}
    groups = result.get("_groups") or defaultdict(list)
    if not groups:
        for i, p in enumerate(states):
            groups[W.aut_canon(p)].append(i)
    explained = unexplained = 0
    bad = []
    for key, idx in groups.items():
        if len(idx) < 2:
            continue
        base = states[idx[0]]
        images = {canon(apply_img(compose(names), base)) for names in reps.values()}
        for j in idx:
            if canon(states[j]) in images:
                explained += 1
            else:
                unexplained += 1
                if len(bad) < 10:
                    bad.append([list(base), list(states[j])])
    return {"group_order": len(reps), "group_matrices": sorted(reps),
            "members_of_multi_orbits_explained": explained, "unexplained": unexplained, "unexplained_examples": bad}


def selftest():
    rng = random.Random(11)
    n = 0
    for _ in range(150):
        p = tuple(W.cycred("".join(rng.choice("xXyY") for _ in range(rng.randint(3, 8)))) for _ in range(2))
        if not all(p):
            continue
        names = [rng.choice(list(GENS)) for _ in range(rng.randint(1, 4))]
        q = apply_img(compose(names), p)
        if not all(q):
            continue
        got = find_aut(p, q)
        assert got is not None, (p, q, names)
        img = compose(got)
        assert canon(apply_img(img, p)) == canon(q)
        # the recovered matrix agrees with the planted one modulo the Sigma-stabilizer only
        # up to sign conventions, so we check functional equality instead (done above).
        n += 1
    # matrix of x->xy is [[1,1],[0,1]] (columns = images)
    assert matrix(compose(["x_xy"])) == ((1, 0), (1, 1)) or matrix(compose(["x_xy"])) == ((1, 1), (0, 1))
    # iota pairing on a small synthetic forward set
    states = [("xxxxyXy", "xyyyxYY"), ("XXXXYxY", "XYYYXyy"), ("x", "y")]
    r = analyse(states, verbose=False)
    r.pop("_groups", None)
    assert r["orbits"] == 2 and r["iota_closed"] == 3
    reps = group_closure([["invx", "invy"], ["x_xy", "invx"], ["y_yx", "y_yx", "y_yx", "invx"]])
    assert reps is not None and len(reps) == 12, reps and len(reps)       # D6 of order 12 in GL2(Z)
    assert len(group_closure([["x_xy", "invx"], ["y_yx", "y_yx", "y_yx", "invx"]], mod_sign=True)) == 6
    assert group_closure([["x_xy"]]) is None            # infinite cyclic
    print(f"n_autstab self-test passed: {n} planted automorphisms recovered; D6 closure ok")


def main():
    if sys.argv[1:] == ["--self-test"]:
        selftest()
        return
    fn = sys.argv[1]
    maxn = None
    out = None
    do_explain = False
    bfs = 300000
    args = sys.argv[2:]
    while args:
        a = args.pop(0)
        if a == "--max":
            maxn = int(args.pop(0))
        elif a == "--out":
            out = args.pop(0)
        elif a == "--explain":
            do_explain = True
        elif a == "--bfs":
            bfs = int(args.pop(0))
        else:
            raise SystemExit("unknown option " + a)
    states = []
    with open(fn) as f:
        for line in f:
            parts = line.split()
            if len(parts) < 2:
                continue
            states.append((parts[0], parts[1]))
            if maxn and len(states) >= maxn:
                break
    r = analyse(states, bfs=bfs)
    if do_explain:
        r["explain"] = explain(states, r)
    r.pop("_groups", None)
    if out:
        with open(out, "w") as f:
            json.dump(r, f, indent=1)
    r2 = dict(r)
    r2["examples"] = r["examples"][:5]
    print(json.dumps(r2, indent=1))


if __name__ == "__main__":
    main()
