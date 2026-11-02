"""Driver for h_monodromy.cpp (research note H): AC-monodromy of abelian fibre products.

For each finite 2-generated group G (given as permutations), computes |C/Z| (= index of the
AC-monodromy group Lambda_G in GL2(Z)) and |O_ab| (= index of the congruence group Gamma),
and tests the pairs below in Q_G = G x_{G_ab} Z^2.  Lambda_eq_Gamma = 1 means Q_G cannot
obstruct ANY pair.  A test value 0 would mean the pair is NOT AC-equivalent to (x,y) in Q_G,
hence not AC-trivial in F (the controls AK1, AK2 must never give 0).

Usage:
  python3 experiments/h_groups.py --selftest
  python3 experiments/h_groups.py --bin PATH_TO_h_monodromy [--only NAME ...] [--pairs K]
Standard library only.
"""
import argparse
import itertools
import json
import os
import random
import subprocess
import sys

TESTS = [
    ("AK1", "xYY", "xyxYXY"), ("AK2", "xxYYY", "xyxYXY"), ("AK3", "xxxYYYY", "xyxYXY"),
    ("AK4", "xxxxYYYYY", "xyxYXY"), ("AK5", "xxxxxYYYYYY", "xyxYXY"),
    ("MS3", "XyyyxYYYY", "XYxxY"), ("Qlen13", "xxyXYY", "xxxYYXy"),
    ("P1", "XyyxYYY", "YxxyXXX"), ("P2", "XyyxYYY", "XyxxyXX"),
    ("MS2a", "XyyxYYY", "XXXYxxy"), ("MS2b", "XyyxYYY", "XXXYxxY"),
    ("C3", "xxyXy", "xyyyyyxYY"), ("C4", "xxxxyXy", "xyyyxYY"), ("C6", "xxyxxYY", "xyXYYXy"),
]

# ---------------------------------------------------------------- permutations
def compose(p, q):  # first p then q
    return tuple(q[i] for i in p)

def closure(gens, limit=200000):
    n = len(gens[0])
    e = tuple(range(n))
    seen = {e}
    frontier = [e]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                k = compose(g, h)
                if k not in seen:
                    seen.add(k)
                    nxt.append(k)
                    if len(seen) > limit:
                        raise ValueError("group too large")
        frontier = nxt
    return seen

def cyc(n, *cycles):
    p = list(range(n))
    for c in cycles:
        for i, a in enumerate(c):
            p[a] = c[(i + 1) % len(c)]
    return tuple(p)

def direct(*perms):
    """disjoint-union action of a tuple of permutations"""
    out, off = [], 0
    for p in perms:
        out.extend(off + i for i in p)
        off += len(p)
    return tuple(out)

# ---------------------------------------------------------------- matrix groups over F_p
def mat_mul(A, B, p):
    return ((A[0][0]*B[0][0]+A[0][1]*B[1][0]) % p, (A[0][0]*B[0][1]+A[0][1]*B[1][1]) % p), \
           ((A[1][0]*B[0][0]+A[1][1]*B[1][0]) % p, (A[1][0]*B[0][1]+A[1][1]*B[1][1]) % p)

def vec_action(A, p):
    """action on nonzero row vectors v -> v A, points indexed by (a,b) != 0"""
    pts = [(a, b) for a in range(p) for b in range(p) if (a, b) != (0, 0)]
    ix = {v: i for i, v in enumerate(pts)}
    return tuple(ix[((v[0]*A[0][0]+v[1]*A[1][0]) % p, (v[0]*A[0][1]+v[1]*A[1][1]) % p)] for v in pts)

def proj_action(A, p):
    """action on the projective line (row vectors up to scalars)"""
    pts = [(1, b) for b in range(p)] + [(0, 1)]
    def norm(v):
        a, b = v
        if a % p:
            inv = pow(a, p - 2, p)
            return (1, (b * inv) % p)
        return (0, 1)
    ix = {v: i for i, v in enumerate(pts)}
    return tuple(ix[norm(((v[0]*A[0][0]+v[1]*A[1][0]) % p, (v[0]*A[0][1]+v[1]*A[1][1]) % p))] for v in pts)

def gl_gens(p):
    w = next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in prime_factors(p - 1))) if p > 2 else 1
    return [((1, 1), (0, 1)), ((0, p - 1), (1, 0)), ((w, 0), (0, 1))]

def sl_gens(p):
    return [((1, 1), (0, 1)), ((0, p - 1), (1, 0))]

def prime_factors(n):
    f, d = set(), 2
    while d * d <= n:
        while n % d == 0:
            f.add(d)
            n //= d
        d += 1
    if n > 1:
        f.add(n)
    return f

# ---------------------------------------------------------------- affine 2^4 : A5 / S5
def affine_2_4(full_sym):
    pts = [v for v in itertools.product((0, 1), repeat=5) if sum(v) % 2 == 0]
    ix = {v: i for i, v in enumerate(pts)}
    def perm_from(sigma, t):
        out = []
        for v in pts:
            w = [0] * 5
            for i in range(5):
                w[sigma[i]] = v[i]
            w = tuple((w[i] + t[i]) % 2 for i in range(5))
            out.append(ix[w])
        return tuple(out)
    z = (0, 0, 0, 0, 0)
    gens = [perm_from((1, 2, 0, 3, 4), z), perm_from((1, 2, 3, 4, 0), z), perm_from((0, 1, 2, 3, 4), (1, 1, 0, 0, 0))]
    if full_sym:
        gens.append(perm_from((1, 0, 2, 3, 4), z))
    return gens

# ---------------------------------------------------------------- group catalogue
def catalogue():
    S = {}
    A5 = [cyc(5, (0, 1, 2)), cyc(5, (0, 1, 2, 3, 4))]
    S5 = [cyc(5, (0, 1)), cyc(5, (0, 1, 2, 3, 4))]
    S["S4"] = [cyc(4, (0, 1)), cyc(4, (0, 1, 2, 3))]                 # solvable control
    S["SL2_3"] = [vec_action(m, 3) for m in sl_gens(3)]               # solvable control
    S["GL2_3"] = [vec_action(m, 3) for m in gl_gens(3)]               # solvable control
    S["A5"] = A5
    S["S5"] = S5
    S["A6"] = [cyc(6, (0, 1, 2, 3, 4)), cyc(6, (0, 1, 2, 3, 5))]
    S["S6"] = [cyc(6, (0, 1)), cyc(6, (0, 1, 2, 3, 4, 5))]
    S["A7"] = [cyc(7, (0, 1, 2)), cyc(7, (0, 1, 2, 3, 4, 5, 6))]
    for p in (7, 11, 13):
        S[f"PSL2_{p}"] = [proj_action(m, p) for m in sl_gens(p)]
        S[f"PGL2_{p}"] = [proj_action(m, p) for m in gl_gens(p)]
    for p in (5, 7):
        S[f"SL2_{p}"] = [vec_action(m, p) for m in sl_gens(p)]
        S[f"GL2_{p}"] = [vec_action(m, p) for m in gl_gens(p)]
    for m in range(2, 13):
        S[f"A5xC{m}"] = [direct(A5[0], cyc(m, tuple(range(m)))), direct(A5[1], tuple(range(m)))]
    for m, k in ((2, 2), (2, 4), (3, 3), (2, 6), (4, 4), (6, 6), (5, 5)):
        S[f"A5xC{m}xC{k}"] = [direct(A5[0], cyc(m, tuple(range(m))), tuple(range(k))),
                              direct(A5[1], tuple(range(m)), cyc(k, tuple(range(k))))]
    for m in (2, 3, 4, 6):
        c = cyc(m, tuple(range(m)))
        S[f"S5xC{m}"] = [direct(S5[0], c), direct(S5[1], c)]          # full direct product
    for m in (4, 6, 8, 10):
        # fibre product S5 x_{C2} C_m : odd permutations paired with odd powers of an m-cycle
        S[f"S5fibC{m}"] = [direct(S5[0], cyc(m, tuple(range(m)))), direct(S5[1], tuple(range(m)))]
    SL25 = [vec_action(m, 5) for m in sl_gens(5)]
    for m in (2, 3, 4, 5, 6):
        S[f"SL2_5xC{m}"] = [direct(SL25[0], cyc(m, tuple(range(m)))), direct(SL25[1], tuple(range(m)))]
    P7 = [proj_action(m, 7) for m in sl_gens(7)]
    for m in (2, 3, 4):
        S[f"PSL2_7xC{m}"] = [direct(P7[0], cyc(m, tuple(range(m)))), direct(P7[1], tuple(range(m)))]
    S["A5xA5"] = [direct(A5[0], A5[1]), direct(A5[1], A5[0])]
    S["A5xS5"] = [direct(A5[0], S5[0]), direct(A5[1], S5[1])]
    S["A5wrC2"] = [direct(A5[0], tuple(range(5))), direct(A5[1], tuple(range(5))),
                   cyc(10, (0, 5), (1, 6), (2, 7), (3, 8), (4, 9))]   # 3 gens; random 2-gen pairs used
    S["2^4:A5"] = affine_2_4(False)
    S["2^4:S5"] = affine_2_4(True)
    return S

# ---------------------------------------------------------------- driver
def two_generating_pairs(gens, k, seed):
    """the catalogue pair (if 2 gens) plus k-1 random generating pairs of the same group"""
    G = closure(gens)
    order = len(G)
    out = []
    if len(gens) == 2:
        out.append(tuple(gens))
    elems = sorted(G)
    rng = random.Random(seed)
    tries = 0
    while len(out) < k and tries < 2000:
        tries += 1
        a, b = rng.choice(elems), rng.choice(elems)
        try:
            if len(closure([a, b], order + 1)) == order:
                out.append((a, b))
        except ValueError:
            pass
    return order, out

def run_one(binary, a, b, max_order=20000, timeout=1200):
    lines = [str(len(a)), " ".join(map(str, a)), " ".join(map(str, b))]
    lines += [f"{n} {w0} {w1}" for n, w0, w1 in TESTS]
    r = subprocess.run([binary, "--max-order", str(max_order)], input="\n".join(lines) + "\n",
                       capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(r.stdout + r.stderr)
    return json.loads(r.stdout)

def selftest():
    S = catalogue()
    expect = {"S4": 24, "SL2_3": 24, "GL2_3": 48, "A5": 60, "S5": 120, "A6": 360, "S6": 720,
              "PSL2_7": 168, "PGL2_7": 336, "SL2_5": 120, "GL2_5": 480, "A5xC4": 240,
              "S5fibC4": 240, "A5xA5": 3600, "A5wrC2": 7200, "2^4:A5": 960, "2^4:S5": 1920}
    bad = 0
    for name, order in expect.items():
        got = len(closure(S[name]))
        if got != order:
            print("order mismatch", name, got, order)
            bad += 1
    bad += lemma21_check()
    print("selftest passed" if not bad else f"selftest FAILED ({bad})")
    return 0 if not bad else 1

def inv(p):
    q = [0] * len(p)
    for i, j in enumerate(p):
        q[j] = i
    return tuple(q)

def lemma21_check(trials=300):
    """Numerical check of the identities in Lemma 2.1 of research-h.md inside 2^4:A5,
    N = translation subgroup (abelian normal).  Notation m^g := g^-1 m g.
      conj:     m^-1 (a n0) m            == a * n0 * m * (m^a)^-1
      multiply: ((a n0 b n1)^m)(b n1)^-1 == a * n0 * m^(b^-1) * (m^a)^-1
    (products left to right, as in compose).  Returns number of failures."""
    gens = affine_2_4(False)
    G = sorted(closure(gens))
    n = len(gens[0])
    e = tuple(range(n))
    # translations = elements fixing no point or identity whose square is identity and that commute
    # with all translations: take the normal closure of the generator translation gens[2]
    N = closure([gens[2]] + [compose(compose(inv(g), gens[2]), g) for g in G])
    assert len(N) == 16
    rng = random.Random(7)
    mul = lambda *ps: __import__("functools").reduce(compose, ps, e)
    conj = lambda m, g: mul(inv(g), m, g)
    fails = 0
    Nl = sorted(N)
    for _ in range(trials):
        a, b = rng.choice(G), rng.choice(G)
        n0, n1, m = rng.choice(Nl), rng.choice(Nl), rng.choice(Nl)
        u0, u1 = mul(a, n0), mul(b, n1)
        lhs1 = mul(inv(m), u0, m)
        rhs1 = mul(a, n0, m, inv(conj(m, a)))
        lhs2 = mul(mul(inv(m), mul(u0, u1), m), inv(u1))
        rhs2 = mul(a, n0, conj(m, inv(b)), inv(conj(m, a)))
        fails += (lhs1 != rhs1) + (lhs2 != rhs2)
    if fails:
        print("lemma 2.1 identity check FAILED", fails)
    else:
        print(f"lemma 2.1 identities verified in 2^4:A5 ({trials} random instances)")
    return fails

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--bin", default=os.environ.get("H_MONODROMY_BIN", "./h_monodromy"))
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--pairs", type=int, default=2)
    ap.add_argument("--max-order", type=int, default=8000)
    args = ap.parse_args()
    if args.selftest:
        sys.exit(selftest())
    S = catalogue()
    names = args.only or list(S)
    for name in names:
        order, pairs = two_generating_pairs(S[name], args.pairs, seed=sum(map(ord, name)))
        if order > args.max_order:
            print(json.dumps({"group": name, "order": order, "skipped": "order"}))
            continue
        for i, (a, b) in enumerate(pairs):
            res = run_one(args.bin, a, b, max_order=args.max_order + 1)
            res = {"group": name, "pair": i, **res}
            print(json.dumps(res), flush=True)

if __name__ == "__main__":
    main()
