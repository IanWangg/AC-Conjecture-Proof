#!/usr/bin/env python3
"""TH11: c-frozen killer classes visible in the stored certificates of AK(3)'s AC class.
Every intermediate state (r1, r2) of a certificate starting at AK(3) (or at a presentation certified
AC-equivalent to it) is AC-equivalent to AK(3).  If r_i is an automorphic image psi(c)^{+-1} of
c = xyxYYXy (up to conjugacy), then psi^-1 of the state is (c, w) up to trivial moves, and by
research-d Lemma D6 (c, w) ~AC AK(3).  psi is unique up to theta0 and inner automorphisms (T1), so the
conjugacy class of w in G_c is determined up to the mirror.  We list the invariants (kappa, J-hat, N)
of all such w and test them against the primitive classes x^s y.
Usage: python3 experiments/th11_kc.py --selftest         (uses certificates/*.json read-only)
"""
import glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import o_gc
import th11_nil as NIL
import th11_trace as TR
from th11_stab import red, inv, cyc, canon, apply, GENS

C = "xyxYYXy"
def compose(g, f):                       # (g o f)(w) = g(f(w))
    return {"x": red(apply(g, f["x"])), "y": red(apply(g, f["y"]))}
ID = {"x": "x", "y": "y"}
GINV = {}
for g in GENS:
    for h in GENS:
        if compose(g, h) == ID: GINV[id(g)] = h
def minimize_aut(w):
    """(minimal cyclic word u, aut T, aut T^-1) with u = canon(T(w))."""
    u, T, Ti = canon(w), ID, ID
    while True:
        for g in GENS:
            v = canon(apply(g, u))
            if len(v) < len(u):
                u, T, Ti = v, compose(g, T), compose(Ti, GINV[id(g)]); break
        else:
            return u, T, Ti
def orbit_min(u0):
    """all minimal words of the orbit of the minimal word u0, with auts P, P^-1: canon(P(u0)) = word."""
    seen = {u0: (ID, ID)}; todo = [u0]
    while todo:
        u = todo.pop(); P, Pi = seen[u]
        for g in GENS:
            v = canon(apply(g, u))
            if len(v) == len(u) and v not in seen:
                seen[v] = (compose(g, P), compose(Pi, GINV[id(g)])); todo.append(v)
    return seen
CMIN, SC, SCi = minimize_aut(C)
ORB = orbit_min(CMIN)                     # contains the inverse classes as well (theta0)

_MIN = {}
def pull_back(r, s):
    """if r is an automorphic image of c^{+-1}: the word w = psi^-1(s) with psi(c) ~ r^{+-1}; else None."""
    key = canon(r)
    if key not in _MIN: _MIN[key] = minimize_aut(key)
    u, T, Ti = _MIN[key]
    if len(u) != len(CMIN) or u not in ORB: return None
    P, Pi = ORB[u]                        # canon(P(CMIN)) = u = canon(T(r));  psi = T^-1 P SC
    w = red(apply(SCi, red(apply(Pi, red(apply(T, s))))))
    return w
def classify(w):
    u, k = o_gc.nf(w)
    if k == -1: u, k = o_gc.nf(inv(w))
    assert k == 1, "second relator must have degree +-1"
    u = u.replace("x", "a")               # o_gc uses letters a,A,b,B already
    kap, J = NIL.KJ_ser(NIL.mu(u))
    return kap, J - kap, TR.as_int(TR.N(u))
def states(cert):
    st = [red(w) for w in cert["start"]]; yield tuple(st)
    for mv in cert["moves"]:
        i = mv["i"]
        if mv["op"] == "invert": st[i] = inv(st[i])
        elif mv["op"] == "multiply": st[i] = red(st[i] + st[mv["j"]])
        else: st[i] = red(mv["g"] + st[i] + inv(mv["g"]))
        yield tuple(st)

def scan(files, maxlen=40):
    found = {}; seen_w = set()
    for f in files:
        cert = json.load(open(f))
        if cert.get("format") != "ordinary-ac-elementary-v1": continue
        for step, st in enumerate(states(cert)):
            for i in (0, 1):
                r, s = cyc(st[i]), cyc(st[1 - i])
                if len(r) > maxlen or len(s) > maxlen: continue
                w = pull_back(r, s)
                if w is None: continue
                w = cyc(w)
                if w in seen_w: continue
                seen_w.add(w)
                key = classify(w)
                if key not in found or len(cyc(w)) < len(found[key][0]):
                    found[key] = (cyc(w), os.path.basename(f), step, st, i)
    return found

if __name__ == "__main__":
    assert classify("xxxYXyy") == (0, 1, 20) and classify("XXXYxyxy") == (1, 1, 20)
    assert pull_back(C, "xxxYXyy") is not None and pull_back("xxxYYYY", "x") is None
    root = os.path.join(HERE, "..", "certificates")
    pats = ["d_ak3_*.json", "k_ak3_*.json", "i_R212_to_ak3.json", "ms3_to_ak3_exact.json",
            "th11_p3_to_theta0_p3.json"]
    if "--all" in sys.argv: pats.append("g_ak3_*.json")
    files = sorted(f for p in pats for f in glob.glob(os.path.join(root, p)))
    found = scan(files)
    prim = {(NIL.kappa_tri(s), NIL.Jhat_x(s)): s for s in range(-60, 61)}
    print("certificates scanned:", len(files))
    for key in sorted(found):
        w, f, step, st, i = found[key]
        print("  (kappa, J-hat, N) =", key, " shortest w:", w, " from", f, "step", step, "state", st, "c-like relator index", i,
              " primitive (kappa,J-hat) match: s =", prim.get(key[:2]))
    print("th11_kc: %d c-frozen killer classes (up to the level of these invariants) found" % len(found))
