"""Agent I: compose Aut(F2)-orbit matches into strict ordinary-AC certificates.

Ingredients (all strict ordinary-ac-elementary-v1):
  * realization certificates P0 -> cyc(g(P0)) for g in GENS (engine + d_certify);
  * an engine certificate P0 -> s (s a state of P0's component);
  * an automorphism phi, found here, with phi(s) = R up to rotation/inversion/swap.
Construction (research-d Lemmas D2/D6, made explicit):
  P0 -> phi(P0)            realize(): transported generator certificates, glued
     -> phi(s)             transport of (P0 -> s) by phi
     -> R (exact)          rotations / inversions / conjugations / swap
and finally the whole sequence is reversed to give R -> P0.

Moves are transported letterwise: invert/multiply unchanged, conjugate(i,g)
becomes conjugation by the word phi(g); since phi is a homomorphism the
transported sequence replays exactly from reduce(phi(start)).

Usage:
  python3 experiments/i_transport.py --selftest
  python3 experiments/i_transport.py merge P0_1 P0_2 S_CERT.json REAL_DIR PREFIX R1 R2 OUT.json
     S_CERT: certificate P0 -> s; REAL_DIR/PREFIX_aut_<g>.json for g in swap,invx,x_xy
"""
import json
import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from i_words import Cert, red, inv, cyc, subst, orbit, canon_pair  # noqa: E402
import elementary_verify as ev  # noqa: E402

MAPS = {
    "swap": {"x": "y", "y": "x"}, "invx": {"x": "X", "y": "y"}, "invy": {"x": "x", "y": "Y"},
    "x_xy": {"x": "xy", "y": "y"}, "x_xY": {"x": "xY", "y": "y"},
    "y_yx": {"x": "x", "y": "yx"}, "y_yX": {"x": "x", "y": "yX"},
}
INVERSE = {"swap": "swap", "invx": "invx", "invy": "invy", "x_xy": "x_xY", "x_xY": "x_xy",
           "y_yx": "y_yX", "y_yX": "y_yx"}
# every map as a composition (left to right = outermost first) of the 3 Nielsen generators
IN_GENS = {"swap": ["swap"], "invx": ["invx"], "x_xy": ["x_xy"],
           "invy": ["swap", "invx", "swap"],
           "x_xY": ["invy", "x_xy", "invy"],
           "y_yx": ["swap", "x_xy", "swap"],
           "y_yX": ["swap", "invy", "x_xy", "invy", "swap"]}


def compose(names):
    """names = [g1,...,gk] -> images of g1 o g2 o ... o gk."""
    img = {"x": "x", "y": "y"}
    for g in reversed(names):            # apply gk first
        img = {v: subst(img[v], MAPS[g]) for v in "xy"} if False else img
    # direct: phi(w) = g1(g2(...gk(w)))
    def phi(w):
        for g in reversed(names):
            w = subst(w, MAPS[g])
        return w
    return {"x": phi("x"), "y": phi("y")}


def expand(names):
    out = []
    for g in names:
        out += IN_GENS[g]
    # expand invy recursively
    res = []
    for g in out:
        res += IN_GENS[g] if g not in ("swap", "invx", "x_xy") else [g]
    return res


def apply_moves(c, moves, img=None):
    """Replay `moves` on Cert c, transported by the automorphism img."""
    for mv in moves:
        if mv["op"] == "invert":
            c.invert(mv["i"])
        elif mv["op"] == "multiply":
            c.mult(mv["i"])
        else:
            g = mv["g"] if img is None else subst(mv["g"], img)
            c.conj(mv["i"], g)


def glue(c, target):
    """Bring c's state to the exact pair `target` (each relator conjugate to the
    corresponding target word or its inverse, possibly after a swap)."""
    t = [red(w) for w in target]
    s0, s1 = cyc(c.s[0]), cyc(c.s[1])
    c0, c1 = cyc(t[0]), cyc(t[1])
    if not (s0 in orbit(c0) and s1 in orbit(c1)):
        if s0 in orbit(c1) and s1 in orbit(c0):
            c.swap()
        else:
            raise ValueError("glue: %r not Sigma-equivalent to %r" % (c.s, t))
    for i in (0, 1):
        w = t[i]
        u = ""
        while len(w) >= 2 and w[0] == w[-1].swapcase():
            u += w[0]
            w = w[1:-1]
        c.to_rotation_of(i, w)
        c.conj(i, u)
        assert c.s[i] == t[i], (c.s[i], t[i])


def reverse_moves(start, moves):
    """Moves of the reversed path (from the end state back to start)."""
    rev = []
    for mv in reversed(moves):
        if mv["op"] == "invert":
            rev.append(dict(mv))
        elif mv["op"] == "multiply":
            j = mv["j"]
            rev += [{"op": "invert", "i": j}, dict(mv), {"op": "invert", "i": j}]
        else:
            rev.append({"op": "conjugate", "i": mv["i"], "g": mv["g"].swapcase()})
    return rev


def realize(P0, gens, real):
    """Cert from exact P0 to (a conjugate pair of) phi(P0), phi = g1 o ... o gk."""
    c = Cert(*P0)
    acc = []                                   # names composed so far
    for g in gens:
        img = compose(acc) if acc else None
        start = [red(subst(w, img)) if img else w for w in P0]
        glue(c, start)
        apply_moves(c, real[g]["moves"], img)
        acc.append(g)
    return c


def find_aut(s, r, max_states=200000):
    """Names [g1..gk] with g1 o..o gk (s) Sigma-equal to r (both cyclic pairs).
    Greedy Whitehead reduction of both ends, then BFS through minimal pairs."""
    def apply(names, p):
        return tuple(cyc(subst(w, compose(names))) for w in p)

    def reduce_path(p):
        names = []
        cur = tuple(cyc(w) for w in p)
        while True:
            best = None
            for g in ("x_xy", "x_xY", "y_yx", "y_yX"):
                q = tuple(cyc(subst(w, MAPS[g])) for w in cur)
                if sum(map(len, q)) < sum(map(len, cur)) and (best is None or sum(map(len, q)) < sum(map(len, best[1]))):
                    best = (g, q)
            if best is None:
                return names, cur
            names = [best[0]] + names           # newest map is outermost
            cur = best[1]

    a_names, smin = reduce_path(s)            # compose(a_names)(s) = smin
    b_names, rmin = reduce_path(r)            # compose(b_names)(r) = rmin
    L = sum(map(len, smin))
    if L != sum(map(len, rmin)):
        raise ValueError("different minimal lengths")
    goal = canon_pair(*rmin)
    start = canon_pair(*smin)
    prev = {start: None}
    dq = deque([(start, smin)])
    found = None
    while dq and len(prev) < max_states:
        key, p = dq.popleft()
        if key == goal:
            found = p
            break
        for g in MAPS:
            q = tuple(cyc(subst(w, MAPS[g])) for w in p)
            if sum(map(len, q)) != L:
                continue
            k = canon_pair(*q)
            if k not in prev:
                prev[k] = (key, g)
                dq.append((k, q))
    if found is None:
        raise ValueError("no automorphism found")
    path = []
    k = goal
    while prev[k] is not None:
        k, g = prev[k]
        path.append(g)
    # path lists maps from goal back to start: applied in order start->goal they are reversed
    mid = path                                  # outermost first: last applied first in list
    # phi = b^-1 o mid o a ;  b^-1 = inverses of b_names in reverse order
    b_inv = [INVERSE[g] for g in reversed(b_names)]
    names = b_inv + mid + a_names
    img = compose(names)
    got = canon_pair(*(cyc(subst(w, img)) for w in s))
    if got != canon_pair(*r):
        raise AssertionError("automorphism check failed")
    return names


def merge(P0, s_cert, real, R):
    s = s_cert["target"]
    names = find_aut(tuple(s), tuple(R))
    gens = expand(names)
    img = compose(gens)
    assert canon_pair(*(cyc(subst(w, img)) for w in s)) == canon_pair(*R)
    c = realize(P0, gens, real)                       # P0 -> ~phi(P0)
    glue(c, [red(subst(w, img)) for w in s_cert["start"]])
    apply_moves(c, s_cert["moves"], img)              # -> phi(s)
    glue(c, R)                                        # -> R exactly
    fwd = c.as_json(list(R))
    ev.replay(fwd)
    back = {"format": "ordinary-ac-elementary-v1", "start": list(R), "target": list(P0),
            "moves": reverse_moves(fwd["start"], fwd["moves"])}
    return back, names


def selftest():
    # AK(3) data from research-d: realization certificates in certificates/
    root = os.path.join(HERE, "..", "certificates")
    real = {g: json.load(open(os.path.join(root, "d_ak3_aut_%s.json" % g))) for g in ("swap", "invx", "x_xy")}
    P0 = tuple(real["swap"]["start"])
    # reversal check
    r = ev.replay(real["x_xy"])
    back = {"format": "ordinary-ac-elementary-v1", "start": r["endpoint"], "target": list(P0),
            "moves": reverse_moves(P0, real["x_xy"]["moves"])}
    assert ev.replay(back)["endpoint"] == list(P0)
    # realization of a composite automorphism, then a synthetic merge:
    gens = ["x_xy", "swap", "invx", "x_xy"]
    c = realize(P0, gens, real)
    img = compose(gens)
    tgt = [cyc(subst(w, img)) for w in P0]
    glue(c, tgt)
    assert ev.replay(c.as_json(tgt))["endpoint"] == tgt
    # find_aut recovers some automorphism between AK(3) and an image of it
    names = find_aut(tuple(tgt), tuple(P0))
    img2 = compose(names)
    assert canon_pair(*(cyc(subst(w, img2)) for w in tgt)) == canon_pair(*P0)
    # full merge: s = P0 itself (empty s-cert), R = image of AK(3) under gens^-1-ish
    s_cert = {"start": list(P0), "target": list(P0), "moves": []}
    R = tuple(cyc(subst(w, compose(["y_yX", "invy"]))) for w in P0)
    back, nm = merge(P0, s_cert, real, R)
    assert ev.replay(back)["endpoint"] == list(P0)
    print("i_transport self-test passed (%d moves in synthetic merge, automorphism %s)" % (len(back["moves"]), nm))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--selftest"]:
        selftest()
    elif a[:1] == ["merge"]:
        P0 = (a[1], a[2])
        s_cert = json.load(open(a[3]))
        assert s_cert["start"] == list(P0)
        real = {g: json.load(open(os.path.join(a[4], "%s_aut_%s.json" % (a[5], g)))) for g in ("swap", "invx", "x_xy")}
        R = (a[6], a[7])
        back, names = merge(P0, s_cert, real, R)
        back["description"] = ("R -> P0 via Aut(F2)-orbit match; automorphism %s; "
                               "experiments/i_transport.py" % "o".join(names))
        r = ev.replay(back)
        json.dump(back, open(a[8], "w"), indent=0)
        print(json.dumps({"path": a[8], **r}))
