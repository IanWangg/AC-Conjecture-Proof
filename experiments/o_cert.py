"""Agent O: compiler from exact ACM moves with the relator c = xyxYYXy frozen to strict
`ordinary-ac-elementary-v1` certificates, via the normal form of G_c = F(a,b) x| Z (o_gc.py).

An ACM move (c, W) -> (c, W') is legal when W' represents a conjugate of W^{+-1} in G_c.
Given a conjugator g (an F-word, usually assembled from a twisted-conjugation path) with
nf(g W^{+-1} g^-1) == nf(W'), the compiler
  1. inverts/conjugates W by ordinary AC moves,
  2. rewrites the result to the canonical word of its normal form by explicit insertions of
     conjugates of c (each insertion = conjugate c, multiply, restore c),
  3. rewrites the canonical word to W' by the reverse procedure.
Every relator insertion comes from one of four local commutation rules (y or Y moved past a
fibre letter a, A, b, B); the factorisation W = C * prod h_i c^{e_i} h_i^-1 is asserted as a
free-group identity before any move is emitted, and the final state is asserted to equal W'.

Also: a twisted-conjugacy BFS with parent pointers (`twisted_path`), the primitive finish
(research-g `finish_primitive`), and `--selftest`, which builds and replays the certificates
P_2 -> (x,y), P_1 -> (x,y), (c,xy) -> (c,xxy), (c,k_1) -> (c,k_2).

    python3 experiments/o_cert.py --selftest
    python3 experiments/o_cert.py --write certificates
"""
import json
import os
import sys
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import o_gc as G            # noqa: E402
import g_cert as GC         # noqa: E402
import elementary_verify as EV  # noqa: E402

red, inv = G.red, G.inv
C = G.C_WORD

FW = {"a": "x", "A": "X", "b": "yxY", "B": "yXY"}


def fw(u):
    return red("".join(FW[ch] for ch in u))


# local rules: y * Fw(L) = Fw(phi(L)) * y * E,  E = h c^eps h^-1  (None: free identity)
E_PLUS = {"a": None, "A": None, "b": ("yXYX", 1), "B": ("yxYYXy", -1)}
# Y * Fw(L) = Fw(phi^-1(L)) * Y * E
E_MINUS = {"a": ("Xy", -1), "A": ("xyyXYX", 1), "b": None, "B": None}


def factor_word(factors):
    return red("".join(h + (C if e > 0 else inv(C)) + inv(h) for h, e in factors))


def _check_rules():
    for L, E in E_PLUS.items():
        lhs = red("y" + fw(L))
        rhs = red(fw(G.apply_endo(G.PHI, L)) + "y" + (factor_word([E]) if E else ""))
        assert lhs == rhs, (L, lhs, rhs)
    for L, E in E_MINUS.items():
        lhs = red("Y" + fw(L))
        rhs = red(fw(G.apply_endo(G.PHI_INV, L)) + "Y" + (factor_word([E]) if E else ""))
        assert lhs == rhs, (L, lhs, rhs)


def conj_factors(g, factors):
    """g (prod h c^e h^-1) g^-1 = prod (g h) c^e (g h)^-1."""
    return [(red(g + h), e) for h, e in factors]


def comm1(u, sign):
    """Factors F with  y^sign Fw(u) = Fw(phi^sign(u)) y^sign prod F  (free identity)."""
    table = E_PLUS if sign > 0 else E_MINUS
    factors = []
    suffix = ""
    for L in reversed(u):
        E = table[L]
        if E is not None:
            factors.append((red(inv(suffix) + E[0]), E[1]))
        suffix = red(fw(L) + suffix)
    return factors


def comm(k, u):
    """Factors F with  y^k Fw(u) = Fw(phi^k(u)) y^k prod F."""
    if k == 0:
        return []
    sign = 1 if k > 0 else -1
    letter = "y" if k > 0 else "Y"
    endo = G.PHI if k > 0 else G.PHI_INV
    rest = comm(k - sign, G.apply_endo(endo, u))
    return conj_factors(inv(letter), rest) + comm1(u, sign)


def factorize(W):
    """Return (u, k, factors) with W = red(Fw(u) y^k) * prod h c^e h^-1 as free words."""
    u, k, factors = "", 0, []
    for g in W:
        factors = conj_factors(inv(g), factors)
        if g in "yY":
            k += 1 if g == "y" else -1
        else:
            letter = "a" if g == "x" else "A"
            new = comm(k, letter)
            u = red(u + G.phi_pow(k, letter))
            factors = new + factors
    assert (u, k) == G.nf(W)
    Cw = G.to_word((u, k))
    assert red(Cw + factor_word(factors)) == W, "factorisation failed"
    return u, k, factors


# ------------------------------------------------------------- compiler
def mult_by_conj(cert, i, h, eps):
    """r_i <- r_i * h r_j^eps h^-1 with r_j restored (j = 1-i)."""
    j = 1 - i
    cert.conj_word(j, h)
    if eps < 0:
        cert.invert(j)
    cert.multiply(i)
    if eps < 0:
        cert.invert(j)
    cert.conj_word(j, inv(h))


def canonicalize(cert, i):
    """Rewrite relator i (with relator j = c, up to conjugacy irrelevant: j must BE c) to the
    canonical word of its normal form."""
    j = 1 - i
    assert cert.s[j] == C, "frozen relator must be exactly c"
    W = cert.s[i]
    u, k, factors = factorize(W)
    for h, e in reversed(factors):
        mult_by_conj(cert, i, h, -e)
    assert cert.s[i] == G.to_word((u, k)), (cert.s[i], G.to_word((u, k)))
    return u, k


def uncanonicalize(cert, i, target):
    """Relator i is the canonical word of nf(target); rewrite it to target."""
    u, k, factors = factorize(target)
    assert cert.s[i] == G.to_word((u, k))
    for h, e in factors:
        mult_by_conj(cert, i, h, e)
    assert cert.s[i] == target, (cert.s[i], target)


def acm_move(cert, i, g, eps, target):
    """(c, W) -> (c, target) with target == g W^eps g^-1 in G_c (g an F-word)."""
    if eps < 0:
        cert.invert(i)
    cert.conj_word(i, g)
    assert G.nf(cert.s[i]) == G.nf(target), "not the same element of G_c"
    canonicalize(cert, i)
    uncanonicalize(cert, i, target)


# ------------------------------------------------------- twisted conjugacy BFS
STEP = {"a": "x", "A": "X", "b": "yxY", "B": "yXY", "y": "y", "Y": "Y"}


def twisted_neighbours(u):
    out = [(v, G.twisted_conj(v, u)) for v in "aAbB"]
    out.append(("y", G.apply_endo(G.PHI, u)))
    out.append(("Y", G.apply_endo(G.PHI_INV, u)))
    return out


def twisted_path(u0, goal, L, maxnodes=3000000):
    """BFS in the twisted-conjugation graph of (., 1) from u0; `goal(u)` is a predicate.
    Returns (u_found, conjugator g) with (g . u0 . g^-1) having normal form (u_found, 1),
    or None.  Nodes are limited to length <= L."""
    parent = {u0: None}
    dq = deque([u0])
    while dq:
        u = dq.popleft()
        if goal(u):
            steps = []
            while parent[u] is not None:
                v, u = parent[u]
                steps.append(v)
            steps.reverse()
            g = ""
            for v in steps:
                g = red(STEP[v] + g)
            return u0 if not steps else _apply_steps(u0, steps), g
        for v, w in twisted_neighbours(u):
            if len(w) <= L and w not in parent:
                parent[w] = (v, u)
                dq.append(w)
                if len(parent) > maxnodes:
                    return None
    return None


def _apply_steps(u, steps):
    for v in steps:
        u = dict(twisted_neighbours(u))[v]
    return u


# ------------------------------------------------------------- certificates
def cert_to_json(cert, note):
    return {"format": "ordinary-ac-elementary-v1", "note": note, "start": cert.start,
            "target": list(cert.s), "moves": cert.moves}


def trivialize_pn(n, L=14):
    """(c, k_n) -> (c, primitive) by one ACM move with c frozen, then the primitive finish."""
    k = G.killer(n)
    u0, _ = G.nf(k)
    res = twisted_path(u0, lambda u: set(u) <= set("aA"), L)
    if res is None:
        return None
    u_found, g = res
    target = G.to_word((u_found, 1))          # x^s y
    cert = GC.Cert(C, k)
    acm_move(cert, 1, g, 1, target)
    assert cert.s == [C, target]
    GC.finish_primitive(cert, 1, ("x", "y"))
    assert cert.s == ["x", "y"], cert.s
    return cert, target


def move_between(W, Wp, L=14):
    """(c, W) -> (c, Wp) with c frozen, if the BFS finds the conjugator."""
    u0, k0 = G.nf(W)
    u1, k1 = G.nf(Wp)
    assert k0 == k1 == 1
    res = twisted_path(u0, lambda u: u == u1, L)
    if res is None:
        return None
    _, g = res
    cert = GC.Cert(C, W)
    acm_move(cert, 1, g, 1, Wp)
    assert cert.s == [C, Wp]
    return cert


def selftest():
    _check_rules()
    import random
    rnd = random.Random(5)
    # factorisation on random words
    for _ in range(300):
        W = red("".join(rnd.choice("xXyY") for _ in range(rnd.randint(0, 12))))
        factorize(W)
    # comm identities directly
    for k in range(-3, 4):
        for u in ("a", "A", "b", "B", "ab", "Ba", "aab", "BAb"):
            F = comm(k, u)
            lhs = red(("y" * k if k >= 0 else "Y" * (-k)) + fw(u))
            rhs = red(fw(G.phi_pow(k, u)) + ("y" * k if k >= 0 else "Y" * (-k)) + factor_word(F))
            assert lhs == rhs, (k, u)
    out = {}
    for n in (1, 2):
        cert, target = trivialize_pn(n)
        rep = EV.replay(cert_to_json(cert, ""))
        assert rep["endpoint"] == ["x", "y"]
        out[f"P{n}"] = (len(cert.moves), rep["peak_total_length"], target)
    c1 = move_between("xy", "xxy")
    rep = EV.replay(cert_to_json(c1, ""))
    out["xy->xxy"] = (len(c1.moves), rep["peak_total_length"])
    c2 = move_between(G.killer(1), G.killer(2))
    rep = EV.replay(cert_to_json(c2, ""))
    out["k1->k2"] = (len(c2.moves), rep["peak_total_length"])
    print("o_cert self-test passed:", out)
    return out


def write_all(outdir):
    for n in (1, 2):
        cert, target = trivialize_pn(n)
        path = os.path.join(outdir, f"o_p{n}_one_acm_move_trivialization.json")
        with open(path, "w") as f:
            json.dump(cert_to_json(cert, f"P_{n} = (c, k_{n}) -> (c, {target}) by one ACM move with c = xyxYYXy frozen "
                                   f"(k_{n} is conjugate in G_c to the primitive word {target}), then primitive finish; "
                                   "compiled by o_cert.py"), f)
        print(path, json.dumps(EV.replay(json.load(open(path)))))
    c1 = move_between("xy", "xxy")
    path = os.path.join(outdir, "o_c_xy_to_c_xxy.json")
    with open(path, "w") as f:
        json.dump(cert_to_json(c1, "(c, xy) -> (c, xxy): the primitive words xy and x^2 y are conjugate in G_c "
                               "(both pairs are AC-trivial; recorded as evidence for the G_c class structure)"), f)
    print(path, json.dumps(EV.replay(json.load(open(path)))))
    c2 = move_between(G.killer(1), G.killer(2))
    path = os.path.join(outdir, "o_p1_to_p2.json")
    with open(path, "w") as f:
        json.dump(cert_to_json(c2, "(c, k_1) -> (c, k_2): k_1 and k_2 are conjugate in G_c; one ACM move with c frozen"), f)
    print(path, json.dumps(EV.replay(json.load(open(path)))))


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif sys.argv[1:2] == ["--write"]:
        write_all(sys.argv[2] if len(sys.argv) > 2 else "certificates")
    else:
        print(__doc__)
