"""Agent O: the one-relator group G_c = <x,y | c>, c = xyxYYXy, as F(a,b) x| Z.

K (research-k) proved AK(n) ~AC P_n = (c, k_n), k_n = x^n YXyy, for all n >= 2.
Here c has y-exponent sum 0, so Magnus rewriting with stable letter y gives

    G_c = F(a,b) x|_phi Z,   a = x,  b = yxY,   y a Y = b,  y b Y = B a,

i.e. phi(a) = b, phi(b) = B a (phi^-1: a -> ab, b -> a).  Every element has a
unique normal form (u, k) with u a reduced word over {a,A,b,B} and k in Z,
multiplication (u,k)(u',k') = (u phi^k(u'), k+k').

Two elements (u,k), (u',k) are conjugate in G_c iff u' = v phi^m(u) phi^k(v)^-1
for some m in Z and v in F(a,b) (twisted conjugacy); for k = 1 the class of u
is its Reidemeister class R(u) = {v u phi(v)^-1}, which is phi-invariant.

Functions here: normal forms, the inverse map back to F(x,y) words with an
explicit factorisation of the relator insertions (used by o_cert.py), and
finite permutation quotients used for exact non-conjugacy proofs.

    python3 experiments/o_gc.py --selftest
"""
import itertools
import random
import sys

LET = "xXyY"


def red(w):
    out = []
    for ch in w:
        if out and out[-1] == ch.swapcase():
            out.pop()
        else:
            out.append(ch)
    return "".join(out)


def inv(w):
    return w.swapcase()[::-1]


def cyc(w):
    w = red(w)
    while len(w) >= 2 and w[0] == w[-1].swapcase():
        w = w[1:-1]
    return w


C_WORD = "xyxYYXy"            # the frozen relator c of P_n


def killer(n):
    return "x" * n + "YXyy"   # k_n


# ---------------------------------------------------------------- phi on F(a,b)
PHI = {"a": "b", "b": "Ba"}
PHI_INV = {"a": "ab", "b": "a"}


def apply_endo(img, u):
    out = []
    for ch in u:
        if ch.islower():
            out.append(img[ch])
        else:
            out.append(inv(img[ch.lower()]))
    return red("".join(out))


_phi_cache = {}


def phi_pow(k, u):
    """phi^k(u) for a reduced word u over a,A,b,B."""
    key = (k, u)
    if key in _phi_cache:
        return _phi_cache[key]
    v = u
    if k >= 0:
        for _ in range(k):
            v = apply_endo(PHI, v)
    else:
        for _ in range(-k):
            v = apply_endo(PHI_INV, v)
    if len(_phi_cache) < 200000:
        _phi_cache[key] = v
    return v


def nf(w):
    """Normal form (u, k) of the F(x,y)-word w in G_c = F(a,b) x| Z."""
    u, k = "", 0
    for ch in w:
        if ch == "x":
            u = red(u + phi_pow(k, "a"))
        elif ch == "X":
            u = red(u + phi_pow(k, "A"))
        elif ch == "y":
            k += 1
        elif ch == "Y":
            k -= 1
        else:
            raise ValueError(w)
    return u, k


def nf_mul(p, q):
    (u, k), (u2, k2) = p, q
    return red(u + phi_pow(k, u2)), k + k2


def nf_inv(p):
    u, k = p
    return phi_pow(-k, inv(u)), -k


def to_word(p):
    """The canonical F(x,y)-word of a normal form: u(x, yxY) y^k, reduced."""
    u, k = p
    out = []
    for ch in u:
        out.append({"a": "x", "A": "X", "b": "yxY", "B": "yXY"}[ch])
    out.append("y" * k if k >= 0 else "Y" * (-k))
    return red("".join(out))


def twisted_conj(v, u):
    """v u phi(v)^-1 : the twisted-conjugation action for k = 1."""
    return red(v + u + inv(apply_endo(PHI, v)))


# ---------------------------------------------------------------- permutations
def pmul(p, q):           # (p*q)(i) = q(p(i)) : apply p then q (left action on words)
    return tuple(q[i] for i in p)


def pinv(p):
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def cycle_type(p):
    n = len(p)
    seen = [False] * n
    ct = []
    for i in range(n):
        if not seen[i]:
            l, j = 0, i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                l += 1
            ct.append(l)
    return tuple(sorted(ct))


def evalword(w, sx, sy):
    n = len(sx)
    e = tuple(range(n))
    img = {"x": sx, "X": pinv(sx), "y": sy, "Y": pinv(sy)}
    r = e
    for ch in w:
        r = pmul(r, img[ch])
    return r


def perm_order(p):
    from math import lcm
    o = 1
    for l in cycle_type(p):
        o = lcm(o, l)
    return o


def all_perms(n):
    return [tuple(p) for p in itertools.permutations(range(n))]


def class_reps(n):
    """One permutation per cycle type of S_n."""
    reps = {}
    for p in itertools.permutations(range(n)):
        ct = cycle_type(p)
        if ct not in reps:
            reps[ct] = tuple(p)
    return list(reps.values())


def perm_quotients(relator, n, transitive_only=True, limit=None):
    """All pairs (sx, sy) with sx a class representative, relator(sx,sy)=1."""
    out = []
    perms = all_perms(n)
    for sx in class_reps(n):
        for sy in perms:
            if evalword(relator, sx, sy) == tuple(range(n)):
                if transitive_only and not _transitive(sx, sy, n):
                    continue
                out.append((sx, sy))
                if limit and len(out) >= limit:
                    return out
    return out


def _transitive(sx, sy, n):
    seen = {0}
    stack = [0]
    while stack:
        i = stack.pop()
        for j in (sx[i], sy[i], pinv(sx)[i], pinv(sy)[i]):
            if j not in seen:
                seen.add(j)
                stack.append(j)
    return len(seen) == n


def group_closure(gens, limit=2000000):
    """Elements of the permutation group generated by gens (BFS)."""
    n = len(gens[0])
    e = tuple(range(n))
    seen = {e}
    frontier = [e]
    while frontier:
        nxt = []
        for g in frontier:
            for s in gens:
                h = pmul(g, s)
                if h not in seen:
                    seen.add(h)
                    nxt.append(h)
                    if len(seen) > limit:
                        raise RuntimeError("group too large")
        frontier = nxt
    return seen


def conj_class(g, group):
    return {pmul(pmul(pinv(h), g), h) for h in group}


# ---------------------------------------------------------------- self-test
def selftest():
    rnd = random.Random(11)
    # 1. c dies, and the normal form is a homomorphism killing <<c>>.
    assert nf(C_WORD) == ("", 0), nf(C_WORD)
    assert nf("yxY") == ("b", 0) and nf("x") == ("a", 0) and nf("y") == ("", 1)
    for _ in range(500):
        w = red("".join(rnd.choice(LET) for _ in range(rnd.randint(0, 14))))
        g = red("".join(rnd.choice(LET) for _ in range(rnd.randint(0, 6))))
        cc = C_WORD if rnd.random() < 0.5 else inv(C_WORD)
        w2 = red(w + g + cc + inv(g))
        assert nf(w) == nf(w2)
        # homomorphism property and inverse
        v = red("".join(rnd.choice(LET) for _ in range(rnd.randint(0, 10))))
        assert nf(red(w + v)) == nf_mul(nf(w), nf(v))
        assert nf(inv(w)) == nf_inv(nf(w))
        # the canonical word represents the same element
        assert nf(to_word(nf(w))) == nf(w)
    # 2. phi and phi^-1 are mutually inverse automorphisms
    for u in ("a", "b", "ab", "aB", "bbA"):
        assert apply_endo(PHI_INV, apply_endo(PHI, u)) == u
        assert apply_endo(PHI, apply_endo(PHI_INV, u)) == u
    # 3. the relation y b Y = B a holds in G_c
    assert nf("yyxYY") == nf("yXYx")
    # 4. killers: k_n = a^n B A y in normal form; conjugation formula
    for n in range(1, 8):
        assert nf(killer(n)) == ("a" * n + "BA", 1), (n, nf(killer(n)))
    # 5. twisted conjugation is conjugation in G_c
    for _ in range(300):
        u = red("".join(rnd.choice("aAbB") for _ in range(rnd.randint(0, 8))))
        v = red("".join(rnd.choice("aAbB") for _ in range(rnd.randint(0, 6))))
        lhs = nf_mul(nf_mul((v, 0), (u, 1)), nf_inv((v, 0)))
        assert lhs == (twisted_conj(v, u), 1)
        # phi(u) is in R(u)
        assert twisted_conj(inv(u), u) == apply_endo(PHI, u)
    # 6. permutation machinery: S_3 quotient of G_c exists? check evaluation
    sx, sy = (1, 0, 2), (0, 2, 1)
    assert cycle_type(pmul(sx, sy)) == (3,)
    print("o_gc self-test passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        for w in sys.argv[1:]:
            print(w, nf(w), to_word(nf(w)))
