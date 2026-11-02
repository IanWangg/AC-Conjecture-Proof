#!/usr/bin/env python3
"""Driver and independent cross-checks for e_acdist.cpp (research-e.md).

Standard library only.  Subcommands (run from the repository root):

  python3 experiments/e_nilpotent_tables.py --build
        compile experiments/e_acdist.cpp into the scratch binary (needs g++)
  python3 experiments/e_nilpotent_tables.py --selftest
        independent checks: (1) class-2 distances recomputed by a separate BFS in
        Heisenberg normal form (formulas of research-b.md), (2) every quotient path
        printed by the C++ program is replayed on free words and checked with an
        independent truncated Magnus expansion, (3) free paths are expanded into
        the ordinary-ac-elementary-v1 format and replayed.
  python3 experiments/e_nilpotent_tables.py --run [--quick]
        recompute the tables of research-e.md (state caps as stated there).
  python3 experiments/e_nilpotent_tables.py --certs
        write certificates/e_ak1_trivialization.json (ordinary AC) and
        certificates/e_ak3_quotient_paths.json (quotient-only, NOT ordinary AC).

Words use x, y and X=x^-1, Y=y^-1.  Moves are the 15-instruction alphabet of
research-b.md, numbered as in e_acdist.cpp.
"""
import json
import os
import subprocess
import sys
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.environ.get("E_ACDIST_BIN", os.path.join(
    "/tmp/claude-0/-home-user-AC-Conjecture-Proof/2793adeb-4b51-5217-aae5-371faac65e22",
    "scratchpad/agent-e/e_acdist"))

PRESENTATIONS = {
    "AK1": ("xYY", "xyxYXY"),
    "AK2": ("xxYYY", "xyxYXY"),
    "AK3": ("xxxYYYY", "xyxYXY"),
    "AK4": ("xxxxYYYYY", "xyxYXY"),
    "MS3": ("XyyyxYYYY", "XYxxY"),   # MS(3, y^-1 x^2 y^-1), AC-equivalent to AK(3) (research-c.md)
}


# ---------------------------------------------------------------- free words
def reduce_word(w):
    out = []
    for ch in w:
        if out and out[-1] == ch.swapcase():
            out.pop()
        else:
            out.append(ch)
    return "".join(out)


def inv(w):
    return w[::-1].swapcase()


GENS = "xXyY"


def free_move(a, b, m):
    if m == 0:
        return inv(a), b
    if m == 1:
        return a, inv(b)
    if m == 2:
        return b, a
    if m == 3:
        return reduce_word(a + b), b
    if m == 4:
        return reduce_word(a + inv(b)), b
    if m == 5:
        return a, reduce_word(b + a)
    if m == 6:
        return a, reduce_word(b + inv(a))
    g = GENS[(m - 7) % 4]
    if m < 11:
        return reduce_word(inv(g) + a + g), b
    return a, reduce_word(inv(g) + b + g)


def replay(a, b, path):
    a, b = reduce_word(a), reduce_word(b)
    for m in path:
        a, b = free_move(a, b, m)
    return a, b


# --------------------------------------- independent class-2 (Heisenberg) model
# research-b.md: element x^a y^b c^k, c=[x,y]=XYxy, (a,b,k)(d,e,l)=(a+d,b+e,k+l-bd).
def h_mul(u, v):
    a, b, k = u
    d, e, l = v
    return (a + d, b + e, k + l - b * d)


def h_inv(u):
    a, b, k = u
    return (-a, -b, -k - a * b)


H_GEN = {"x": (1, 0, 0), "X": (-1, 0, 0), "y": (0, 1, 0), "Y": (0, -1, 0)}


def h_word(w):
    r = (0, 0, 0)
    for ch in w:
        r = h_mul(r, H_GEN[ch])
    return r


def h_neighbors(state):
    a, b = state
    ai, bi = h_inv(a), h_inv(b)
    out = [(ai, b), (a, bi), (b, a), (h_mul(a, b), b), (h_mul(a, bi), b),
           (a, h_mul(b, a)), (a, h_mul(b, ai))]
    for g in GENS:
        G, Gi = H_GEN[g], h_inv(H_GEN[g])
        out.append((h_mul(h_mul(Gi, a), G), b))
    for g in GENS:
        G, Gi = H_GEN[g], h_inv(H_GEN[g])
        out.append((a, h_mul(h_mul(Gi, b), G)))
    return out


def heisenberg_distance(r0, r1, limit=10):
    start = (h_word(r0), h_word(r1))
    target = (h_word("x"), h_word("y"))
    dist = {start: 0}
    q = deque([start])
    while q:
        s = q.popleft()
        if s == target:
            return dist[s]
        if dist[s] >= limit:
            continue
        for t in h_neighbors(s):
            if t not in dist:
                dist[t] = dist[s] + 1
                q.append(t)
    return None


# ------------------------------------ independent truncated Magnus expansion
def magnus(word, degree):
    """Dict monomial-string -> integer coefficient, truncated above `degree`."""
    result = {"": 1}
    for letter in word:
        v = letter.lower()
        if letter.islower():
            factor = {"": 1, v: 1}
        else:
            factor = {v * k: (-1) ** k for k in range(degree + 1)}
        prod = defaultdict(int)
        for m1, c1 in result.items():
            for m2, c2 in factor.items():
                if len(m1) + len(m2) <= degree:
                    prod[m1 + m2] += c1 * c2
        result = {m: c for m, c in prod.items() if c}
    return result


def in_gamma(word, c):
    """True iff word lies in gamma_{c+1}(F), i.e. Magnus terms of degree 1..c vanish."""
    return magnus(word, c) == {"": 1}


# ------------------------------------------- conversion to elementary format
def to_elementary(path):
    """15-alphabet move list -> ordinary-ac-elementary-v1 primitive list."""
    out = []
    for m in path:
        if m in (0, 1):
            out.append({"op": "invert", "i": m})
        elif m == 2:  # swap via six primitives (research-e.md)
            out += [{"op": "multiply", "i": 0, "j": 1}, {"op": "invert", "i": 0},
                    {"op": "multiply", "i": 1, "j": 0}, {"op": "invert", "i": 1},
                    {"op": "multiply", "i": 0, "j": 1}, {"op": "invert", "i": 0}]
        elif m == 3:
            out.append({"op": "multiply", "i": 0, "j": 1})
        elif m == 4:
            out += [{"op": "invert", "i": 1}, {"op": "multiply", "i": 0, "j": 1},
                    {"op": "invert", "i": 1}]
        elif m == 5:
            out.append({"op": "multiply", "i": 1, "j": 0})
        elif m == 6:
            out += [{"op": "invert", "i": 0}, {"op": "multiply", "i": 1, "j": 0},
                    {"op": "invert", "i": 0}]
        else:
            g = GENS[(m - 7) % 4]
            # e_acdist: r <- g^-1 r g ; elementary-v1: conjugate(i,h): r <- h r h^-1, h = g^-1
            out.append({"op": "conjugate", "i": 0 if m < 11 else 1, "g": inv(g)})
    return out


# ------------------------------------------------------------- binary runner
def run_bin(args, timeout=2700):
    if not os.path.exists(BIN):
        raise SystemExit(f"binary {BIN} missing; run --build first")
    res = subprocess.run([BIN] + args, capture_output=True, text=True, timeout=timeout)
    if res.returncode != 0:
        raise RuntimeError(res.stderr or res.stdout)
    return json.loads(res.stdout.strip().splitlines()[-1])


def nil(label, c, cap, mod=0):
    r0, r1 = PRESENTATIONS[label] if label in PRESENTATIONS else label
    return run_bin(["--mode", "nil", "--class", str(c), "--mod", str(mod), "--start", r0, r1,
                    "--max-states", str(cap), "--label", str(label)])


def free(label, cap):
    r0, r1 = PRESENTATIONS[label] if label in PRESENTATIONS else label
    return run_bin(["--mode", "free", "--start", r0, r1, "--max-states", str(cap),
                    "--label", str(label)])


def check_quotient_path(r0, r1, path, c):
    """Replay on free words; endpoint must be (x,y) modulo gamma_{c+1}(F)."""
    a, b = replay(r0, r1, path)
    return in_gamma(reduce_word(a + "X"), c) and in_gamma(reduce_word(b + "Y"), c), (a, b)


def selftest():
    failures = 0

    def check(ok, msg):
        nonlocal failures
        print(("ok   " if ok else "FAIL ") + msg)
        failures += 0 if ok else 1

    # Heisenberg model sanity (research-b.md formulas)
    check(h_word("XYxy") == (0, 0, 1), "c = XYxy has coordinates (0,0,1)")
    check(h_word("xyxYXY") == (1, -1, -1), "braid relator class-2 coordinates")
    for w in ["xyXYxxY", "YYxyXyx", "xyxYXY"]:
        check(h_mul(h_word(w), h_word(inv(w))) == (0, 0, 0), f"inverse in Heisenberg model: {w}")
    # Magnus sanity
    check(in_gamma("XYxy", 1) and not in_gamma("XYxy", 2), "[x,y] in gamma_2 \\ gamma_3")
    # (1) independent class-2 distances
    out = run_bin(["--selftest"])
    check(out.get("selftest") == "passed", "C++ internal self-test")
    for label in ["AK1", "AK2", "AK3", "MS3"]:
        r0, r1 = PRESENTATIONS[label]
        d_py = heisenberg_distance(r0, r1, limit=9)
        d_c = nil(label, 2, 2_000_000)
        check(d_c["result"] == "exact" and d_c["distance"] == d_py,
              f"{label}: class-2 distance C++={d_c.get('distance')} independent={d_py}")
    # (2) every class-c quotient path replays and is a genuine class-c certificate
    for label in ["AK1", "AK2", "AK3", "MS3"]:
        r0, r1 = PRESENTATIONS[label]
        for c in (1, 2, 3):
            d = nil(label, c, 2_000_000)
            ok, end = check_quotient_path(r0, r1, d["path"], c)
            check(ok and len(d["path"]) == d["distance"],
                  f"{label}: class-{c} path of length {d['distance']} is (x,y) mod gamma_{c+1}")
    # (3) free path for AK(1) -> elementary certificate replay
    d = free("AK1", 1_000_000)
    check(d["result"] == "exact" and replay(*PRESENTATIONS["AK1"], d["path"]) == ("x", "y"),
          f"AK1 free path length {d.get('distance')} replays to (x,y)")
    sys.path.insert(0, os.path.join(ROOT, "experiments"))
    import elementary_verify  # repository verifier, independent of this file
    cert = {"format": "ordinary-ac-elementary-v1", "start": list(PRESENTATIONS["AK1"]),
            "target": ["x", "y"], "moves": to_elementary(d["path"])}
    check(elementary_verify.replay(cert)["endpoint"] == ["x", "y"],
          "AK1 elementary-v1 expansion accepted by experiments/elementary_verify.py")
    # Negative control: a class-3 path for AK(3) is NOT a free trivialization
    d3 = nil("AK3", 3, 2_000_000)
    check(replay(*PRESENTATIONS["AK3"], d3["path"]) != ("x", "y"),
          "AK3 optimal class-3 path does not trivialize in F (as expected)")
    print(json.dumps({"selftest": "passed" if failures == 0 else "FAILED",
                      "failures": failures}))
    return failures


def run_tables(quick=False):
    caps = {1: 2_000_000, 2: 2_000_000, 3: 6_000_000, 4: 10_000_000, 5: 6_500_000}
    classes = (1, 2, 3) if quick else (1, 2, 3, 4, 5)
    rows = []
    for label in ["AK1", "AK2", "AK3", "MS3", "AK4"]:
        for c in classes:
            if label == "AK1" and c > 5:
                continue
            d = nil(label, c, caps[c])
            rows.append({k: d[k] for k in ("label", "class", "result", "states_stored",
                                            "max_abs_coefficient", "peak_rss_kb")}
                        | {"value": d.get("distance", d.get("distance_at_least"))})
            print(json.dumps(rows[-1]), flush=True)
    return rows


def write_certs():
    d = free("AK1", 1_000_000)
    cert = {"format": "ordinary-ac-elementary-v1", "start": list(PRESENTATIONS["AK1"]),
            "target": ["x", "y"], "moves": to_elementary(d["path"]),
            "description": ("AK(1) = <x,y | x y^-2, xyx y^-1 x^-1 y^-1> to (x,y). "
                            f"Expanded from a shortest {d['distance']}-instruction path in the "
                            "15-instruction alphabet found by exhaustive BFS (e_acdist.cpp).")}
    p1 = os.path.join(ROOT, "certificates", "e_ak1_trivialization.json")
    with open(p1, "w") as f:
        json.dump(cert, f, indent=1)
    paths = []
    for c in (1, 2, 3, 4):
        q = nil("AK3", c, 10_000_000)
        ok, end = check_quotient_path(*PRESENTATIONS["AK3"], q["path"], c)
        assert ok
        paths.append({"class": c, "length": q["distance"], "moves_15_alphabet": q["path"],
                      "free_endpoint": list(end),
                      "endpoint_equals_xy_in_F": list(end) == ["x", "y"]})
    doc = {"format": "e-quotient-path-v1",
           "WARNING": ("Quotient certificates only. Each path maps AK(3) to (x,y) modulo "
                       "gamma_{c+1}(F); none is an ordinary AC trivialization in F."),
           "alphabet": ["inv a", "inv b", "swap", "a<-ab", "a<-aB", "b<-ba", "b<-bA",
                        "a<-X a x", "a<-x a X", "a<-Y a y", "a<-y a Y",
                        "b<-X b x", "b<-x b X", "b<-Y b y", "b<-y b Y"],
           "start": list(PRESENTATIONS["AK3"]), "paths": paths,
           "check": "python3 experiments/e_nilpotent_tables.py --check-quotient-certs"}
    p2 = os.path.join(ROOT, "certificates", "e_ak3_quotient_paths.json")
    with open(p2, "w") as f:
        json.dump(doc, f, indent=1)
    print("wrote", p1, p2)


def check_quotient_certs():
    """Binary-free check of certificates/e_ak3_quotient_paths.json."""
    with open(os.path.join(ROOT, "certificates", "e_ak3_quotient_paths.json")) as f:
        doc = json.load(f)
    for p in doc["paths"]:
        ok, end = check_quotient_path(*doc["start"], p["moves_15_alphabet"], p["class"])
        assert ok and list(end) == p["free_endpoint"] and len(p["moves_15_alphabet"]) == p["length"]
        assert list(end) != ["x", "y"]
        print(f"class {p['class']}: {p['length']} moves; endpoint = (x,y) mod gamma_{p['class']+1}"
              f"; free endpoint word lengths {[len(w) for w in end]} (not (x,y) in F)")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--build" in args:
        subprocess.run(["g++", "-O2", "-std=c++17", "-o", BIN,
                        os.path.join(ROOT, "experiments", "e_acdist.cpp")], check=True)
        print("built", BIN)
    if "--selftest" in args:
        sys.exit(1 if selftest() else 0)
    if "--run" in args:
        run_tables(quick="--quick" in args)
    if "--certs" in args:
        write_certs()
    if "--check-quotient-certs" in args:
        check_quotient_certs()
