"""TH10: torus-type and Baumslag-Solitar-type class coordinates (research/research-th10.md,
Theorems A, B, B').

A cyclic word c is of torus type {p,q} if it is conjugate to phi(x^p y^q)^{+-1} for some
phi in Aut(F2).  By Whitehead's theorem (minimal words of an orbit are connected by
length-preserving Whitehead maps) this holds iff the set of minimal-length cyclic words reached
by greedy descent under x->xy^{+-1}, y->yx^{+-1} and then level moves contains a 2-syllable word.
The script (a) checks the three torus coordinates of AK(3) used in the note, including the
explicit bases, (b) scans every state of the repository certificates that start or end at a
named presentation and lists the torus types met, (c) sanity-checks Theorem B's algebraic
core in small permutation groups.  Standard library only; imports the verifier read-only.

Usage: python3 experiments/th10_torus_coords.py --selftest | --scan | --mechanism
"""
import glob, json, os, sys
from math import gcd
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import elementary_verify as ev  # noqa: E402

def inv(w): return w.swapcase()[::-1]

def cyc(w):
    w = ev.reduce(w)
    while len(w) >= 2 and w[0] == w[-1].swapcase():
        w = w[1:-1]
    return w

def subst(w, ix, iy):
    m = {"x": ix, "y": iy, "X": inv(ix), "Y": inv(iy)}
    return ev.reduce("".join(m[c] for c in w))

WH = [("xy", "y"), ("xY", "y"), ("x", "yx"), ("x", "yX")]

def wh_min(w):
    w = cyc(w)
    while True:
        best = min((cyc(subst(w, a, b)) for a, b in WH), key=len)
        if len(best) >= len(w):
            return w
        w = best

def syllables(w):
    """exponents of the cyclic syllables of a cyclically reduced word"""
    if not w or len(set(w.lower())) == 1:
        return [len(w)] if w else []
    k = next(i for i in range(len(w)) if w[i] != w[i - 1])
    w = w[k:] + w[:k]
    out, j = [], 0
    for i in range(1, len(w) + 1):
        if i == len(w) or w[i] != w[j]:
            out.append(i - j); j = i
    return out

def canon(w):
    w = cyc(w)
    return min(u[i:] + u[:i] for u in (w, inv(w)) for i in range(len(u))) if w else ""

def min_set(w, cap=4000):
    """all minimal-length cyclic words (up to rotation/inversion) Whitehead-connected to wh_min(w)"""
    m = canon(wh_min(w)); seen = {m}; todo = [m]
    while todo and len(seen) < cap:
        u = todo.pop()
        for a, b in WH + [("y", "x"), ("X", "y")]:
            v = canon(subst(u, a, b))
            if len(v) == len(m) and v not in seen:
                seen.add(v); todo.append(v)
    return seen

def torus_type(w):
    """sorted (p,q), p,q>=1, if w is an Aut-image of x^p y^q up to conjugacy/inversion; else None"""
    for u in min_set(w):
        s = syllables(u)
        if len(s) == 1:
            return (1, s[0])                      # power of a primitive (s[0]=1: primitive)
        if len(s) == 2:
            return tuple(sorted(s))
    return None

_REP = {}
def rep(w):
    """canonical minimal representative of the Aut(F2)-orbit of the cyclic word w (up to inversion)"""
    c = canon(w)
    if c not in _REP:
        _REP[c] = min(min_set(c))
    return _REP[c]

_BS = {}
def bs_type(w):
    """p >= 1 if w is an Aut-image (up to conjugacy/inversion) of v^-1 u^p v u^-(p+1); else None"""
    if not _BS:
        for p in range(1, 16):
            _BS[rep("X" + "y" * p + "x" + "Y" * (p + 1))] = p
    return _BS.get(rep(w))

def same_cyclic(u, v):
    u, v = cyc(u), cyc(v)
    return len(u) == len(v) and any(c in (u + u) for c in (v, inv(v)))

def states(cert):
    st = [ev.reduce(w) for w in cert["start"]]
    yield tuple(st)
    for mv in cert["moves"]:
        i = mv["i"]
        if mv["op"] == "invert": st[i] = inv(st[i])
        elif mv["op"] == "multiply": st[i] = ev.reduce(st[i] + st[mv["j"]])
        else: st[i] = ev.reduce(mv["g"] + st[i] + inv(mv["g"]))
        yield tuple(st)

# ---- tiny permutation groups for the sanity check of Theorem B --------------------------------
def pmul(a, b): return tuple(b[i] for i in a)          # first a, then b
def pinv(a):
    r = [0] * len(a)
    for i, j in enumerate(a): r[j] = i
    return tuple(r)
def closure(gens, n):
    e = tuple(range(n)); seen = {e}; todo = [e]
    while todo:
        g = todo.pop()
        for s in gens:
            h = pmul(g, s)
            if h not in seen: seen.add(h); todo.append(h)
    return seen
def order(g):
    e = tuple(range(len(g))); k, h = 1, g
    while h != e: h = pmul(h, g); k += 1
    return k
def ppow(g, k):
    e = tuple(range(len(g)))
    if k < 0: g, k = pinv(g), -k
    r = e
    for _ in range(k): r = pmul(r, g)
    return r
def quotient_abelian(G, a, b, c, n):
    """is <a,b>/<<c>> abelian?  i.e. [a,b] in normal closure of c in G=<a,b>"""
    N = closure([pmul(pmul(pinv(g), c), g) for g in G], n)
    comm = pmul(pmul(pinv(a), pinv(b)), pmul(a, b))
    return comm in N

GROUPS = {  # name: (degree, generators)
    "S3": (3, [(1, 0, 2), (1, 2, 0)]), "A4": (4, [(1, 0, 3, 2), (1, 2, 0, 3)]),
    "S4": (4, [(1, 0, 2, 3), (1, 2, 3, 0)]), "A5": (5, [(1, 2, 0, 3, 4), (1, 2, 3, 4, 0)]),
    "D7": (7, [tuple((i + 1) % 7 for i in range(7)), tuple((-i) % 7 for i in range(7))]),
    "7:3": (7, [tuple((i + 1) % 7 for i in range(7)), tuple((2 * i) % 7 for i in range(7))]),
    "7:6": (7, [tuple((i + 1) % 7 for i in range(7)), tuple((3 * i) % 7 for i in range(7))]),
}

# ---- exact Eisenstein arithmetic for the glide-length invariant (note, Proposition 5.2) -------
# a + b*w with w = exp(2 pi i/3), w^2 = -1 - w; an isometry is (A, B, f): z -> A z + B (f = 0)
# or z -> A conj(z) + B (f = 1), A a unit.
def e_mul(p, q): return (p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0] - p[1] * q[1])
def e_add(p, q): return (p[0] + q[0], p[1] + q[1])
def e_conj(p): return (p[0] - p[1], -p[1])
def e_norm(p): return p[0] * p[0] - p[0] * p[1] + p[1] * p[1]
def i_comp(g, h):                      # g o h
    A, B, f = g; C, D, e = h
    if f == 0: return (e_mul(A, C), e_add(e_mul(A, D), B), e)
    return (e_mul(A, e_conj(C)), e_add(e_mul(A, e_conj(D)), B), 1 - e)
def i_inv(g):
    A, B, f = g
    Ai = e_conj(A)                     # units: inverse = conjugate
    if f == 0: return (Ai, e_mul((-1, 0), e_mul(Ai, B)), 0)
    return (A, e_mul((-1, 0), e_mul(A, e_conj(B))), 1)   # z = A conj(y)+B  =>  y = A conj(z) - A conj(B)
SIG = ((-1, -1), (1, 0), 1)            # x -> sigma: z -> conj(w) conj(z) + 1
ETA = ((1, 0), (0, 1), 1)              # y -> eta:   z -> conj(z) + w
def rho(word):
    r = ((1, 0), (0, 0), 0)
    m = {"x": SIG, "y": ETA, "X": i_inv(SIG), "Y": i_inv(ETA)}
    for c in word: r = i_comp(r, m[c])
    return r
def glide2(word):
    """squared glide length of rho(word) (word of odd exponent sum)"""
    g = rho(word); assert g[2] == 1
    g2 = i_comp(g, g); assert g2[0] == (1, 0) and g2[2] == 0
    return e_norm(g2[1])

def selftest():
    assert torus_type("xxxYYYY") == (3, 4) and torus_type("xyxYXY") == (2, 3)
    assert torus_type("xy") == (1, 1) and torus_type("xyXY") is None and torus_type("XyyyxYYYY") is None
    # braid relator = u^2 v^-3 with (u,v)=(xyx,xy), a basis: x = v^-1 u, y = x^-1 v
    assert same_cyclic("xyx" * 2 + inv("xy") * 3, "xyxYXY")
    # G's T(2,7) coordinate: target of g_ak3_to_trefoil_t2_7.json is psi(u0^2 v0^-7), basis (u0,v0)
    root = os.path.dirname(HERE)
    cert = json.load(open(os.path.join(root, "certificates", "g_ak3_to_trefoil_t2_7.json")))
    ev.replay(cert)
    assert [ev.reduce(w) for w in cert["start"]] == ["xxxYYYY", "xyxYXY"]
    u0, v0 = "xyxyxyx", "xy"                          # x = v0^-3 u0, y = x^-1 v0
    assert ev.reduce(inv(v0) * 3 + u0) == "x" and ev.reduce("X" + v0) == "y"
    U, V = subst(u0, "xyx", "yx"), subst(v0, "xyx", "yx")   # psi: x->xyx, y->yx (x = psi(x)psi(y)^-1)
    assert ev.reduce("xyx" + inv("yx")) == "x"
    assert same_cyclic(U * 2 + inv(V) * 7, cert["target"][0]) and cert["target"][1] == "xyxYXY"
    assert torus_type(cert["target"][0]) == (2, 7)
    # C4 ~ T(4;8,5): three torus coordinates of types {5,8},{2,5},{2,5}
    c4 = json.load(open(os.path.join(root, "certificates", "i_c4_to_T4_8_5.json")))
    ev.replay(c4)
    ws = [ev.reduce(w) for w in c4["start"] + c4["target"]]
    assert sorted(torus_type(w) for w in ws) == [(2, 5), (2, 5), (2, 5), (5, 8)], ws
    # Theorem B core: if o(g) is prime to p or o(h) prime to q then <g,h>/<<g^p h^-q>> is abelian
    checked = 0
    for name, (n, gens) in GROUPS.items():
        G = sorted(closure(gens, n))
        for g, h in product(G, G):
            H = closure([g, h], n)
            for p, q in ((2, 3), (3, 4), (2, 7), (5, 2), (8, 5)):
                if gcd(order(g), p) == 1 or gcd(order(h), q) == 1:
                    c = pmul(ppow(g, p), ppow(h, -q))
                    assert quotient_abelian(H, g, h, c, n), (name, g, h, p, q)
                    checked += 1
    # Theorem B' core: with c = V^-1 U^p V U^-(p+1) and N = <<c>> in H = <U,V>:
    #   <U>N is normal in H and contains [U,V]  (so H/N is <u>-by-cyclic and w-bar lies in v^{+-1}<u>)
    assert bs_type("XyyyxYYYY") == 3 and bs_type("xxxYYYY") is None and bs_type("XyxYY") == 1
    ms = json.load(open(os.path.join(root, "certificates", "ms3_to_ak3_exact.json")))
    ev.replay(ms)
    assert any(bs_type(w) == 3 for w in ms["start"] + ms["target"])
    assert sorted(ev.reduce(w) for w in ms["start"] + ms["target"]).count("xxxYYYY") == 1
    bchecked = 0
    for name, (n, gens) in GROUPS.items():
        G = sorted(closure(gens, n))
        for U, V in product(G, G):
            H = closure([U, V], n)
            for p in (1, 2, 3, 4):
                c = pmul(pmul(pinv(V), ppow(U, p)), pmul(V, ppow(U, -p - 1)))
                N = closure([pmul(pmul(pinv(g), c), g) for g in H], n)
                CN = closure(list(N) + [U], n)          # <U>N (N normal in H)
                assert pmul(pmul(pinv(V), U), V) in CN and pmul(pmul(V, U), pinv(V)) in CN, name
                assert pmul(pmul(pinv(U), pinv(V)), pmul(U, V)) in CN, name
                bchecked += 1
    # Theorem A, steps 3-4 (Remark (ii)): in a metabelian group E = <P, Qg> with P in E',
    # every element of Qg*E' is conjugate to some Qg*P^i.  (False in general for derived length 3.)
    achecked = 0
    for name in ("S3", "A4", "D7", "7:3", "7:6"):
        n, gens = GROUPS[name]
        G = sorted(closure(gens, n))
        Gset = set(G)
        comm = lambda g, h: pmul(pmul(pinv(g), pinv(h)), pmul(g, h))
        D1 = closure([comm(g, h) for g in G for h in G], n)
        assert all(comm(g, h) == tuple(range(n)) for g in D1 for h in D1), name   # metabelian
        for Pp, Qg in product(sorted(D1), G):
            if closure([Pp, Qg], n) != Gset:
                continue
            targets = set()
            for i in range(order(Pp)):
                y0 = pmul(Qg, ppow(Pp, i))
                targets |= {pmul(pmul(g, y0), pinv(g)) for g in G}
            assert all(pmul(Qg, m) in targets for m in D1), (name, Pp, Qg)
            achecked += 1
    assert achecked > 0
    # glide-length invariant: rho kills the braid relator and (y x^-1)^3; formula for AK(n) killers
    ident = ((1, 0), (0, 0), 0)
    assert rho("xyxYXY") == ident and rho("yXyXyX") == ident and rho("xX") == ident
    for n in range(0, 60):
        assert glide2("x" * n + "Y" * (n + 1)) == (3 * n // 2 + 1) ** 2
    for al in range(0, 12):            # primitive elements of exponent sum -1: y^-1 (x y^-1)^al, (x^-1 y)^al y^-1 ...
        assert glide2("Y" + "xY" * al) in (1, 4) and glide2("Y" + "yX" * al) in (1, 4)
    import random
    random.seed(5)
    for _ in range(300):               # conjugation invariance on random words
        g = "".join(random.choice("xXyY") for _ in range(random.randint(0, 12)))
        assert glide2(g + "xxxYYYY" + inv(g)) == 25
    # sharpness: exponent 42 does not make the three AK(3) torus quotients abelian
    n, gens = GROUPS["S3"]; t, r = gens
    assert not quotient_abelian(closure(gens, n), t, r, pmul(ppow(t, 2), ppow(r, -3)), n)
    assert not quotient_abelian(closure(gens, n), r, t, pmul(ppow(r, 3), ppow(t, -4)), n)
    n, gens = GROUPS["D7"]; r, t = gens
    assert not quotient_abelian(closure(gens, n), t, r, pmul(ppow(t, 2), ppow(r, -7)), n)
    print(f"selftest passed ({checked} instances of Theorem C's core, {bchecked} of Theorem B(a)'s core, "
          f"{achecked} of Theorem A's step 4)")

def mechanism(samples=400, seed=7):
    """Replay the mechanism of Theorems A/B on the certified pair M_3 = (X yyy x YYYY, X Y xx Y) ~ AK(3):
    for epimorphisms F -> Q (Q finite), N = <<c(a,b)>>, check that Q/N is metacyclic-by-construction
    (<b>N normal with cyclic quotient), and that w(a,b) is conjugate modulo N to the image of the
    primitive element x y^j for some j, whose cokernel is then cyclic."""
    import random
    random.seed(seed)
    groups = dict(GROUPS)
    groups["S5"] = (5, [(1, 0, 2, 3, 4), (1, 2, 3, 4, 0)])
    total = 0
    for name, (n, gens) in groups.items():
        G = sorted(closure(gens, n)); Gset = set(G); e = tuple(range(n))
        pairs = [(a, b) for a in G for b in G]
        if len(pairs) > samples:
            pairs = random.sample(pairs, samples)
        cnt = 0
        for a, b in pairs:
            if closure([a, b], n) != Gset:
                continue
            ev_ = lambda w: _eval(w, a, b, n)
            c, w = ev_("XyyyxYYYY"), ev_("XYxxY")
            N = closure([pmul(pmul(pinv(g), c), g) for g in G], n)
            NW = closure(list(N) + [pmul(pmul(pinv(g), w), g) for g in G], n)
            assert len(NW) == len(G)                                 # (c,w) normally generates Q
            BN = closure(list(N) + [b], n)                           # <b>N
            assert all(pmul(pmul(pinv(g), h), g) in BN for g in (a, b) for h in (b,)), name   # normal
            assert pmul(pmul(pinv(a), pinv(b)), pmul(a, b)) in BN, name                        # Q/<b>N cyclic
            ok = False
            for j in range(order(b)):
                y0 = pmul(a, ppow(b, j))                             # image of the primitive x y^j
                if any(pmul(pinv(pmul(pmul(g, y0), pinv(g))), w) in N for g in G):
                    ok = True; break
            assert ok, (name, a, b)
            cnt += 1
        total += cnt
        print(f"{name}: order {len(G)}, {cnt} generating pairs checked", flush=True)
    print(f"mechanism check passed on {total} epimorphisms")

def _eval(word, a, b, n):
    r = tuple(range(n))
    m = {"x": a, "y": b, "X": pinv(a), "Y": pinv(b)}
    for ch in word: r = pmul(r, m[ch])
    return r

def scan():
    root = os.path.dirname(HERE)
    res, seen_by_key, ncert = {}, {}, [0]
    for f in sorted(glob.glob(os.path.join(root, "certificates", "*.json"))):
        cert = json.load(open(f))
        if cert.get("format") != "ordinary-ac-elementary-v1":
            continue
        key = tuple(ev.reduce(w) for w in cert["start"])
        types = res.setdefault(key, {})
        seen = seen_by_key.setdefault(key, set())      # distinct cyclic words per start pair
        ncert[0] += 1
        for st in states(cert):
            for w in st:
                c = canon(w)
                if c in seen or len(c) > 60: continue
                seen.add(c)
                t = torus_type(c)
                if t and t[0] >= 2:
                    types[t] = types.get(t, 0) + 1
                b = bs_type(c)
                if b:
                    types["BS%d" % b] = types.get("BS%d" % b, 0) + 1
    print(f"{ncert[0]} certificates, {len(res)} start pairs; counts = distinct cyclic words "
          f"(up to rotation and inversion, length <= 60) per start pair")
    for key, types in sorted(res.items(), key=lambda kv: kv[0]):
        print(",".join(key), dict(sorted(types.items(), key=str)))

if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    elif "--scan" in sys.argv: scan()
    elif "--mechanism" in sys.argv: mechanism()
    else: print(__doc__)
