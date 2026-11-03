#!/usr/bin/env python3
"""Agent G: compile exact torus-group ACM moves into strict elementary
ordinary-AC certificates (format ordinary-ac-elementary-v1).

An ACM move  u -> u'  with frozen v = cyc(theta(x^p y^q)) is legal when u' is
conjugate to u^{+-1} in <x,y | v> (decided by g_torus.torus_class).  It is
realised by elementary moves as follows.

  * Work in theta-coordinates: the pair (U, V) = (theta^-1 u, theta^-1 v).
    An elementary move there maps to elementary moves in the original
    coordinates: invert -> invert, multiply -> multiply, conjugation by a
    letter g -> conjugation by the word theta(g), expanded letterwise.  Since
    theta is a homomorphism and free reduction is canonical, the original
    state is always red(theta(state)).  (`View`.)
  * Conjugate V to exactly R = x^p y^q.
  * Rewrite U to a canonical cyclic word by "chunk" replacements
    A S B -> A S' B where S^-1 S' = h R^{+-1} h^-1 is checked explicitly;
    such a replacement is U <- U * (k R^{+-1} k^-1), k = B^-1 h: conjugate the
    frozen relator by k, (invert), multiply, (invert), conjugate back.
  * Rewrite u' the same way and append the reversed step list.

Nothing here is trusted: every certificate is replayed by
experiments/elementary_verify.py.

Run `python3 experiments/g_cert.py --selftest`.
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g_torus as T  # noqa: E402

red, inv, cyc, power, apply = T.red, T.inv, T.cyc, T.power, T.apply


# ------------------------------------------------------------ recorder

class Cert:
    def __init__(self, r0, r1):
        self.start = [red(r0), red(r1)]
        self.s = list(self.start)
        self.moves = []

    def invert(self, i):
        self.s[i] = inv(self.s[i])
        self.moves.append({"op": "invert", "i": i})

    def multiply(self, i):
        j = 1 - i
        self.s[i] = red(self.s[i] + self.s[j])
        self.moves.append({"op": "multiply", "i": i, "j": j})

    def conj_letter(self, i, g):
        self.s[i] = red(g + self.s[i] + inv(g))
        self.moves.append({"op": "conjugate", "i": i, "g": g})

    def conj_word(self, i, w):
        """s_i -> w s_i w^-1."""
        for g in reversed(w):
            self.conj_letter(i, g)

    def cyclically_reduce(self, i):
        w = self.s[i]
        c = cyc(w)
        k = (len(w) - len(c)) // 2
        self.conj_word(i, inv(w[:k]))
        assert self.s[i] == c

    def rotate_to(self, i, target):
        """Conjugate the cyclically reduced s_i to the rotation `target`."""
        w = self.s[i]
        assert len(w) == len(target)
        for r in range(len(w)):
            if w[r:] + w[:r] == target:
                self.conj_word(i, inv(w[:r]))
                assert self.s[i] == target
                return
        raise ValueError("not a rotation")

    def to_json(self, target=None):
        return {"format": "ordinary-ac-elementary-v1", "start": self.start,
                "target": target if target is not None else list(self.s),
                "moves": self.moves}


class View:
    """theta-coordinates on top of a Cert.  theta = (wx, wy) and its exact inverse."""

    def __init__(self, cert, theta, theta_inv):
        for c in "xy":
            assert apply(theta, apply(theta_inv, c)) == c, "theta_inv is not the exact inverse"
        self.c, self.th, self.thi = cert, theta, theta_inv
        self.U = [apply(theta_inv, cert.s[0]), apply(theta_inv, cert.s[1])]
        self.check()

    def check(self):
        for i in (0, 1):
            assert apply(self.th, self.U[i]) == self.c.s[i]

    def invert(self, i):
        self.c.invert(i)
        self.U[i] = inv(self.U[i])

    def multiply(self, i):
        self.c.multiply(i)
        self.U[i] = red(self.U[i] + self.U[1 - i])

    def conj_word(self, i, w):
        self.c.conj_word(i, apply(self.th, w))
        self.U[i] = red(w + self.U[i] + inv(w))

    def mult_by_conj(self, i, k, eps):
        """U_i <- U_i * k U_j^eps k^-1 (j the other index)."""
        j = 1 - i
        self.conj_word(j, k)
        if eps < 0:
            self.invert(j)
        self.multiply(i)
        if eps < 0:
            self.invert(j)
        self.conj_word(j, inv(k))


# --------------------------------------------------------- automorphisms

def nielsen_reduce_basis(a, b, limit=100000):
    """Length-reducing Nielsen moves taking the basis (a, b) to letters.
    Returns the list of moves (kind, i, sign) applied in order:
    ('R', i, s): w_i <- w_i w_j^s ; ('L', i, s): w_i <- w_j^s w_i."""
    w = [red(a), red(b)]
    moves = []
    for _ in range(limit):
        if len(w[0]) == 1 and len(w[1]) == 1:
            return w, moves
        best = None
        for i in (0, 1):
            j = 1 - i
            for s in (1, -1):
                wj = w[j] if s > 0 else inv(w[j])
                for kind, cand in (("R", red(w[i] + wj)), ("L", red(wj + w[i]))):
                    if len(cand) < len(w[i]) and (best is None or len(cand) - len(w[i]) < best[0]):
                        best = (len(cand) - len(w[i]), kind, i, s, cand)
        if best is None:
            raise ValueError("not a basis (Nielsen reduction stuck): %r" % (w,))
        _, kind, i, s, cand = best
        w[i] = cand
        moves.append((kind, i, s))
    raise ValueError("limit")


def exact_inverse(theta):
    """Exact inverse automorphism, via Nielsen reduction of the basis theta."""
    w, moves = nielsen_reduce_basis(*theta)
    # theta o nu_1 o ... o nu_k = sigma (letters); apply the same moves to (x, y)
    v = ["x", "y"]
    for kind, i, s in moves:
        j = 1 - i
        vj = v[j] if s > 0 else inv(v[j])
        v[i] = red(v[i] + vj) if kind == "R" else red(vj + v[i])
    # now theta(v) = w (letters, possibly permuted/inverted); fix up
    img = {}
    for k in (0, 1):
        img[w[k]] = v[k]
        img[inv(w[k])] = inv(v[k])
    th_inv = (img["x"], img["y"])
    for c in "xy":
        assert apply(theta, apply(th_inv, c)) == c
        assert apply(th_inv, apply(theta, c)) == c
    return th_inv


def compose(a, b):
    """(a o b)(g) = a(b(g))."""
    return (apply(a, b[0]), apply(a, b[1]))


# ------------------------------------------------------ rewriting in G(R)

def conj_rep(E, R):
    """Write E = h R^eps h^-1 exactly (free group); return (h, eps)."""
    E = red(E)
    C = cyc(E)
    k = (len(E) - len(C)) // 2
    h0 = E[:k]
    for eps, Rr in ((1, R), (-1, inv(R))):
        for r in range(len(Rr)):
            if Rr[r:] + Rr[:r] == C:
                h = red(h0 + inv(Rr[:r]))
                assert red(h + Rr + inv(h)) == E
                return h, eps
    raise ValueError("not a conjugate of R^{+-1}: %s" % E)


def runs(w):
    out = []
    for c in w:
        g = c.lower()
        e = 1 if c == g else -1
        if out and out[-1][0] == g:
            out[-1][1] += e
        else:
            out.append([g, e])
    return out


def word_of_runs(rs):
    return "".join((g if e > 0 else g.upper()) * abs(e) for g, e in rs)


class Rewriter:
    """Rewrites a cyclic word W into canonical form in G = <x,y | x^p y^q>,
    recording steps ('ins', k, eps) [W <- W k R^eps k^-1] and ('conj', g)
    [W <- g W g^-1].  `self.W` is always the exact current reduced word."""

    def __init__(self, W, p, q):
        self.p, self.q = p, q
        self.R = red(power("x", p) + power("y", q))
        self.W = red(W)
        self.steps = []
        P, Q = abs(p), abs(q)
        self.P, self.Q = P, Q
        # x^P = z^{sp}, y^Q = x^{cy} with cy = -p*sign(q) ... derive: y^q = x^-p
        self.yQ_as_x = -p if q > 0 else p      # y^{|q|} = x^{yQ_as_x}
        self.xP_as_y = -q if p > 0 else q      # x^{|p|} = y^{xP_as_y}

    def conj(self, g):
        self.W = red(g + self.W + inv(g))
        self.steps.append(("conj", g))

    def replace(self, pos, length, new):
        """W = A S B with S = W[pos:pos+length] (no wrap) -> A new B."""
        A, S, B = self.W[:pos], self.W[pos:pos + length], self.W[pos + length:]
        h, eps = conj_rep(inv(S) + new, self.R)
        k = red(inv(B) + h)
        newW = red(self.W + k + (self.R if eps > 0 else inv(self.R)) + inv(k))
        assert newW == red(A + new + B)
        self.W = newW
        self.steps.append(("ins", k, eps))

    def make_cyclically_reduced(self):
        c = cyc(self.W)
        k = (len(self.W) - len(c)) // 2
        if k:
            self.conj(inv(self.W[:k]))  # W = h c h^-1 -> h^-1 W h
        assert self.W == c

    def rotate_runs(self):
        """Rotate so that the cyclic word does not have a run wrapping around."""
        w = self.W
        if len(w) >= 2 and w[0].lower() == w[-1].lower():
            # find first position where generator changes
            for r in range(1, len(w)):
                if w[r].lower() != w[r - 1].lower():
                    self.conj(inv(w[:r]))
                    return
            # single run: nothing to do

    def _run_positions(self):
        rs = runs(self.W)
        pos, out = 0, []
        for g, e in rs:
            out.append((g, e, pos))
            pos += abs(e)
        return out

    def step_once(self):
        """Apply one normalising chunk replacement; return False if all
        y-runs are in [1,Q-1] and all x-runs have nonzero residue mod P
        (a single zero-residue x-run opposite a single y-run is allowed:
        that is the degenerate class y^j z^k)."""
        self.make_cyclically_reduced()
        self.rotate_runs()
        rs = self._run_positions()
        P, Q = self.P, self.Q
        for idx, (g, e, pos) in enumerate(rs):
            if g == "y" and not (1 <= e <= Q - 1):
                if e >= Q:  # last Q letters y^Q -> x^c (merges into the next x-run)
                    self.replace(pos + e - Q, Q, power("x", self.yQ_as_x))
                else:       # e <= -1 : Y^{|e|} -> y^{e+Q} x^{-c}
                    self.replace(pos, -e, power("y", e + Q) + power("x", -self.yQ_as_x))
                return True
        nx = sum(1 for r in rs if r[0] == "x")
        if nx >= 2:
            for idx, (g, e, pos) in enumerate(rs):
                if g == "x" and e % P == 0:
                    # convert the LAST chunk x^{+-P} to a y-power merging FORWARD
                    # (central mass always flows forward, so no oscillation)
                    self.replace(pos + abs(e) - P, P, power("y", self.xP_as_y if e > 0 else -self.xP_as_y))
                    return True
        return False

    def normalise_residues(self, limit=100000):
        for _ in range(limit):
            if not self.step_once():
                return
        raise RuntimeError("normalisation did not terminate")

    def _push_x(self, idx):
        """Move one central chunk out of x-run idx into the following y-run."""
        g, e, pos = self._run_positions()[idx]
        P = self.P
        res = e % P
        if e > res:      # positive excess: last P letters x^P -> y^d
            self.replace(pos + e - P, P, power("y", self.xP_as_y))
        else:            # e < res (e may be negative): whole run -> x^{e+P} y^{-d}
            self.replace(pos, abs(e), power("x", e + P) + power("y", -self.xP_as_y))

    def _push_y(self, idx):
        """Move one central chunk out of y-run idx into the following x-run
        (or onto the end of the word)."""
        g, e, pos = self._run_positions()[idx]
        Q = self.Q
        if e >= Q:
            self.replace(pos + e - Q, Q, power("x", self.yQ_as_x))
        else:
            self.replace(pos, -e, power("y", e + Q) + power("x", -self.yQ_as_x))

    def collect_centre(self):
        """Linear canonical word: residues from the minimal necklace rotation,
        all central excess as one trailing x-power."""
        P, Q = self.P, self.Q
        self.normalise_residues()
        rs = self._run_positions()
        if len(rs) <= 1:
            return
        if len(rs) == 2 and any(g == "x" and e % P == 0 for g, e, _ in rs):
            yi = [i for i, r in enumerate(rs) if r[0] == "y"][0]
            pos = rs[yi][2]
            if pos:
                self.conj(inv(self.W[:pos]))
            return
        syl = tuple((g, e % (P if g == "x" else Q)) for g, e, _ in rs)
        n = len(syl)
        rots = [syl[i:] + syl[:i] for i in range(n)]
        s0 = min(range(n), key=lambda i: rots[i])
        assert rs[s0][0] == "x"
        pos0 = rs[s0][2]
        if pos0:
            self.conj(inv(self.W[:pos0]))
        m = n // 2
        for t in range(m):
            while True:
                g, e, _ = self._run_positions()[2 * t]
                assert g == "x"
                if 1 <= e <= P - 1:
                    break
                self._push_x(2 * t)
                while True:
                    g2, e2, _ = self._run_positions()[2 * t + 1]
                    assert g2 == "y"
                    if 1 <= e2 <= Q - 1:
                        break
                    self._push_y(2 * t + 1)
        rs = self._run_positions()
        assert len(rs) in (n, n + 1)
        for k, (g, e, _) in enumerate(rs[:n]):
            assert (g, e) == syl[(s0 + k) % n] or (g, e % (P if g == "x" else Q)) == syl[(s0 + k) % n]


def canonical(W, p, q):
    rw = Rewriter(W, p, q)
    rw.make_cyclically_reduced()
    rw.collect_centre()
    return rw


def reverse_steps(steps, R):
    """Steps taking W0 to W1, reversed (taking W1 to W0)."""
    out = []
    for st in reversed(steps):
        if st[0] == "conj":
            out.append(("conj", inv(st[1])))
        else:
            _, k, eps = st
            out.append(("ins", k, -eps))
    return out


def apply_steps_to_view(view, i, steps):
    for st in steps:
        if st[0] == "conj":
            view.conj_word(i, st[1])
        else:
            _, k, eps = st
            view.mult_by_conj(i, k, eps)


def acm_edge(cert, i, theta, p, q, target_theta_word):
    """In `cert`, relator j = 1-i equals (up to conjugacy) theta(x^p y^q).
    Replace relator i by the word theta(target) (exactly, freely reduced),
    where target is conjugate to U_i^{+-1} in <x,y | x^p y^q>."""
    th_inv = exact_inverse(theta)
    view = View(cert, theta, th_inv)
    j = 1 - i
    R = red(power("x", p) + power("y", q))
    # frozen relator to exactly R
    V = view.U[j]
    hV, epsV = conj_rep(V, R)
    if epsV < 0:
        view.invert(j)
        hV, epsV = conj_rep(view.U[j], R)
    view.conj_word(j, inv(hV))
    assert view.U[j] == R
    U = view.U[i]
    tgt = red(target_theta_word)
    cT = T.torus_class(tgt, p, q)
    if T.torus_class(U, p, q) != cT:
        assert T.torus_class(inv(U), p, q) == cT, "target not conjugate to U^{+-1}"
        view.invert(i)
        U = view.U[i]
    rw1 = canonical(U, p, q)
    rw2 = canonical(tgt, p, q)
    assert rw1.W == rw2.W, (rw1.W, rw2.W)
    apply_steps_to_view(view, i, rw1.steps)
    apply_steps_to_view(view, i, reverse_steps(rw2.steps, R))
    assert view.U[i] == tgt, (view.U[i], tgt)
    view.check()
    return view


def finish_primitive(cert, i, theta):
    """Relator i is (in theta-coordinates) a primitive word.  Trivialise:
    returns with cert.s == ['x', 'y']."""
    th_inv = exact_inverse(theta)
    view = View(cert, theta, th_inv)
    P = cyc(view.U[i])
    m, n = T.expvec(P)
    # automorphism alpha with alpha(x) a rotation of P
    M = None
    for b in range(-abs(m) - abs(n) - 2, abs(m) + abs(n) + 3):
        for d in range(-abs(m) - abs(n) - 2, abs(m) + abs(n) + 3):
            if m * d - b * n in (1, -1):
                M = ((m, b), (n, d))
                break
        if M:
            break
    alpha = T.aut_from_matrix(M)
    assert T.min_rot(cyc(alpha[0])) == T.min_rot(P)
    th2 = compose(theta, alpha)
    th2i = exact_inverse(th2)
    view = View(cert, th2, th2i)
    # relator i is now a conjugate of x
    hx, ex = conj_rep(view.U[i], "x")
    if ex < 0:
        view.invert(i)
        hx, ex = conj_rep(view.U[i], "x")
    view.conj_word(i, inv(hx))
    assert view.U[i] == "x"
    j = 1 - i
    # delete x-letters from relator j: W = A x^e B -> A B
    while True:
        W = view.U[j]
        k = next((t for t, c in enumerate(W) if c in "xX"), None)
        if k is None:
            break
        c = W[k]
        B = W[k + 1:]
        eps = -1 if c == "x" else 1
        view.mult_by_conj(j, inv(B), eps)
    assert view.U[j] in ("y", "Y"), view.U[j]
    if view.U[j] == "Y":
        view.invert(j)
    # now original state is (theta2(x), theta2(y)) in positions (i, j): Nielsen-reduce
    nielsen_finish(cert)
    return cert


def nielsen_finish(cert):
    """cert.s is a basis of F_2; reduce to exactly ('x','y') by AC moves."""
    for _ in range(100000):
        a, b = cert.s
        if {a, b} <= {"x", "X", "y", "Y"} and {a.lower(), b.lower()} == {"x", "y"}:
            break
        best = None
        for i in (0, 1):
            j = 1 - i
            for s in (1, -1):
                wj = cert.s[j] if s > 0 else inv(cert.s[j])
                for kind, cand in (("R", red(cert.s[i] + wj)), ("L", red(wj + cert.s[i]))):
                    if len(cand) < len(cert.s[i]) and (best is None or len(cand) - len(cert.s[i]) < best[0]):
                        best = (len(cand) - len(cert.s[i]), kind, i, s)
        if best is None:
            raise ValueError("not a basis: %r" % (cert.s,))
        _, kind, i, s = best
        j = 1 - i
        if s < 0:
            cert.invert(j)
        if kind == "R":
            cert.multiply(i)
        else:  # w_j w_i = w_j (w_i w_j) w_j^-1
            cert.multiply(i)
            cert.conj_word(i, cert.s[j])
        if s < 0:
            cert.invert(j)
    # signs
    for i in (0, 1):
        if cert.s[i] in ("X", "Y"):
            cert.invert(i)
    if cert.s == ["y", "x"]:
        swap(cert)
    assert cert.s == ["x", "y"], cert.s


def swap(cert):
    """(a,b) -> (b,a) by D1(a): (a,b)->(ab,b)->(ab,b^-1)->(ab,b^-1ab)->(ab,a)
    ->(ab,a^-1)->(aba^-1... ) realised with right multiplications, inversions
    and word conjugations."""
    a, b = cert.s
    cert.multiply(0)                 # (ab, b)
    cert.invert(1)                   # (ab, B)
    cert.multiply(1)                 # (ab, B ab) = (ab, B a b)
    cert.conj_word(1, b)             # (ab, a b ... ) : b(B a b)B = a
    assert cert.s[1] == red(a), cert.s
    cert.invert(1)                   # (ab, A)
    cert.multiply(0)                 # (ab A, A)
    cert.conj_word(0, inv(a))        # A(abA)a = b
    assert cert.s[0] == red(b)
    cert.invert(1)                   # (b, a)
    assert cert.s == [red(b), red(a)]


# ------------------------------------------------------------------ main

def replay(cert_json):
    import importlib.util
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("ev", os.path.join(here, "elementary_verify.py"))
    ev = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ev)
    return ev.replay(cert_json)


PHI = ("xY", "yyX")    # phi(xyxYXY) = xxYYY
PSI = ("xyx", "yx")    # psi = phi^-1


def wirtinger_t2(n):
    """T(2,2n+1) relator (xy)^n x ((yx)^n y)^-1."""
    return red("xy" * n + "x" + inv("yx" * n + "y"))


def ak_to_trefoil_t2(n):
    """Certificate AK(n) = (x^n y^-(n+1), xyxYXY) -> (w_n, xyxYXY) where
    w_n = cyc(psi(W_n)) and W_n the T(2,2n+1) relator."""
    b = "xyxYXY"
    cert = Cert("x" * n + "Y" * (n + 1), b)
    # theta = psi: psi(x^2 y^-3) = b (cyclically)
    acm_edge(cert, 0, PSI, 2, -3, wirtinger_t2(n))
    cert.cyclically_reduce(0)
    cert.cyclically_reduce(1)
    target = [cert.s[0], b]
    assert cert.s[1] == b
    return cert, target


def ak2_trivial():
    """AK(2) -> (x,y): one ACM move of the braid relator (frozen x^2 y^-3)
    to the primitive word yXyXyXy, then primitive-relator finish."""
    cert = Cert("xxYYY", "xyxYXY")
    ident = ("x", "y")
    acm_edge(cert, 1, ident, 2, -3, "yXyXyXy")
    finish_primitive(cert, 1, ident)
    return cert


def selftest():
    # exact inverse and swap
    th = T.aut_from_matrix(((3, 2), (4, 3)))
    thi = exact_inverse(th)
    c = Cert("xxy", "yX")
    swap(c)
    assert c.s == ["yX", "xxy"]
    r = replay(c.to_json())
    # canonical forms agree exactly when torus_class agrees (random test)
    import random
    rng = random.Random(5)
    for _ in range(300):
        p = rng.choice([2, 3, -2, -3, 4])
        q = rng.choice([3, -3, 5, -4, 7])
        if math.gcd(p, q) != 1:
            continue
        w = cyc("".join(rng.choice("xXyY") for _ in range(rng.randint(1, 16))))
        if not w:
            continue
        R = red(power("x", p) + power("y", q))
        g = "".join(rng.choice("xXyY") for _ in range(rng.randint(0, 5)))
        kpos = rng.randrange(len(w) + 1)
        rot = rng.randrange(len(R))
        w2 = cyc(w[:kpos] + g + R[rot:] + R[:rot] + inv(g) + w[kpos:])
        if not w2:
            continue
        a, b2 = canonical(w, p, q), canonical(w2, p, q)
        assert a.W == b2.W, (w, w2, p, q, a.W, b2.W)
        # the recorded steps reproduce the canonical word
        W = red(w)
        for st in a.steps:
            if st[0] == "conj":
                W = red(st[1] + W + inv(st[1]))
            else:
                W = red(W + st[1] + (R if st[2] > 0 else inv(R)) + inv(st[1]))
        assert W == a.W
    cert = ak2_trivial()
    out = replay(cert.to_json(["x", "y"]))
    print("g_cert self-test passed; AK(2) one-ACM-move certificate:", out["moves"], "moves, peak", out["peak_total_length"])


# ------------------------------------------------- certificate algebra

def reverse_certificate(cj):
    """Exact reversal of an ordinary-ac-elementary-v1 certificate.
    invert is an involution; conjugate(i,g) is undone by conjugate(i,g^-1);
    multiply(i,j) is undone by invert(j), multiply(i,j), invert(j)
    (red(red(s t) t^-1) = red(s))."""
    moves = []
    for mv in reversed(cj["moves"]):
        if mv["op"] == "invert":
            moves.append(dict(mv))
        elif mv["op"] == "conjugate":
            moves.append({"op": "conjugate", "i": mv["i"], "g": mv["g"].swapcase()})
        else:
            j = mv["j"]
            moves += [{"op": "invert", "i": j}, {"op": "multiply", "i": mv["i"], "j": j},
                      {"op": "invert", "i": j}]
    return {"format": "ordinary-ac-elementary-v1", "start": list(cj["target"]),
            "target": list(cj["start"]), "moves": moves}


def concat_certificates(a, b):
    assert [red(w) for w in a["target"]] == [red(w) for w in b["start"]]
    return {"format": "ordinary-ac-elementary-v1", "start": list(a["start"]),
            "target": list(b["target"]), "moves": a["moves"] + b["moves"]}


def transport_certificate(cj, phi):
    """Apply the automorphism phi letterwise to a certificate (Lemma D2):
    invert/multiply unchanged, conjugate(i,g) -> conjugation by the word phi(g)."""
    start = [apply(phi, w) for w in cj["start"]]
    c = Cert(*start)
    for mv in cj["moves"]:
        if mv["op"] == "invert":
            c.invert(mv["i"])
        elif mv["op"] == "multiply":
            c.multiply(mv["i"])
        else:
            c.conj_word(mv["i"], apply(phi, mv["g"]))
    return c.to_json([apply(phi, w) for w in cj["target"]])


def landing_certificate(r1, r2, moved, M, p, q, target):
    """Certificate (r1, r2) -> (theta(target), theta(x^p y^q)) exactly, where
    theta = aut_from_matrix(M) and the frozen relator is cyc theta(x^p y^q)."""
    theta = T.aut_from_matrix(M)
    cert = Cert(r1, r2)
    acm_edge(cert, moved, theta, p, q, target)
    return cert.to_json(list(cert.s)), theta


def aut_equivalence_certificate(A, landA, B, landB):
    """A, B rank-2 presentations; landX = (moved, M, p, q, target) with the
    SAME (p, q, target).  Returns (phi, certificate phi(A) -> B)."""
    cA, thA = landing_certificate(A[0], A[1], *landA)
    cB, thB = landing_certificate(B[0], B[1], *landB)
    phi = compose(thB, exact_inverse(thA))
    tA = transport_certificate(cA, phi)
    endA = [red(w) for w in tA["target"]]
    endB = [red(w) for w in cB["target"]]
    if endA != endB:
        assert endA == endB[::-1], (endA, endB)
        sw = Cert(*endA)
        swap(sw)
        tA = concat_certificates(tA, sw.to_json(list(sw.s)))
    return phi, concat_certificates(tA, reverse_certificate(cB))


# ------------------------------------- Whitehead with tracked automorphisms

_WH_MAPS = [("xy", "y"), ("xY", "y"), ("x", "yx"), ("x", "yX")]   # x->xy, x->xY, y->yx, y->yX


def _signed_perm_auts():
    out = []
    for swap_ in (False, True):
        for sx in (1, -1):
            for sy in (1, -1):
                a = ("x" if sx > 0 else "X", "y" if sy > 0 else "Y")
                out.append((a[1], a[0]) if swap_ else a)
    return out


def _canon_word(w):
    return min(u[k:] + u[:k] for u in (w, inv(w)) for k in range(len(w)))


def _canon_pair(p):
    return tuple(sorted(_canon_word(w) for w in p))


def aut_canon_tracked(p):
    """Like d_whitehead.aut_canon, but also returns an automorphism alpha with
    _canon_pair(cyc alpha(p)) == canonical form.  Positives are sound."""
    alpha = ("x", "y")
    p = tuple(cyc(w) for w in p)
    improved = True
    while improved:
        improved = False
        for m in _WH_MAPS:
            q = tuple(cyc(apply(m, w)) for w in p)
            if all(q) and sum(map(len, q)) < sum(map(len, p)):
                p, alpha, improved = q, compose(m, alpha), True
                break
    L = sum(map(len, p))
    seen = {_canon_pair(p): (p, alpha)}
    stack = [(p, alpha)]
    while stack:
        cur, al = stack.pop()
        for m in _WH_MAPS:
            q = tuple(cyc(apply(m, w)) for w in cur)
            if all(q) and sum(map(len, q)) == L:
                c = _canon_pair(q)
                if c not in seen:
                    seen[c] = (q, compose(m, al))
                    stack.append(seen[c])
    best = None
    for c, (q, al) in seen.items():
        for s in _signed_perm_auts():
            r = tuple(cyc(apply(s, w)) for w in q)
            cr = _canon_pair(r)
            if best is None or cr < best[0]:
                best = (cr, compose(s, al))
    return best


def sigma_match(cert, target):
    """Transform cert's current state into the exact pair `target`, assuming
    the two pairs agree up to cyclic rotation, inversion and order."""
    for i in (0, 1):
        cert.cyclically_reduce(i)
    tc = [cyc(w) for w in target]
    if _canon_word(cert.s[0]) != _canon_word(tc[0]):
        swap(cert)
    for i in (0, 1):
        if T.min_rot(cert.s[i]) != T.min_rot(tc[i]):
            cert.invert(i)
        cert.rotate_to(i, tc[i])
    # undo cyclic reduction of the target (target may not be cyclically reduced)
    for i in (0, 1):
        if target[i] != tc[i]:
            w = red(target[i])
            k = (len(w) - len(tc[i])) // 2
            cert.conj_word(i, w[:k])
            assert cert.s[i] == w
    assert cert.s == [red(w) for w in target], (cert.s, target)


def aut_equivalence_certificate_general(A, landA, B, landB):
    """Like aut_equivalence_certificate, but the two normalised landing pairs
    need only lie in the same Aut(F_2)-orbit (found by tracked Whitehead)."""
    cA, thA = landing_certificate(A[0], A[1], *landA)
    cB, thB = landing_certificate(B[0], B[1], *landB)
    RA = red(power("x", landA[2]) + power("y", landA[3]))
    RB = red(power("x", landB[2]) + power("y", landB[3]))
    canA, alA = aut_canon_tracked((RA, landA[4]))
    canB, alB = aut_canon_tracked((RB, landB[4]))
    assert canA == canB, (canA, canB)
    phi = compose(thB, compose(exact_inverse(alB), compose(alA, exact_inverse(thA))))
    tA = transport_certificate(cA, phi)
    c = Cert(*tA["target"])
    sigma_match(c, cB["target"])
    tA = concat_certificates(tA, c.to_json(list(c.s)))
    return phi, concat_certificates(tA, reverse_certificate(cB))


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif sys.argv[1:2] == ["--write-g5"]:
        outdir = sys.argv[2]
        jobs = [
            ("g_r327_to_c3_via_aut.json", aut_equivalence_certificate,
             ("xxyXYXy", "xyXyyyyXy"), (0, ((-1, -1), (3, 4)), -2, 3, "YxYxYxYxYxYXyX"),
             ("xxyXy", "xyyyyyxYY"), (1, ((-2, -1), (-1, 0)), -2, 3, "YxYxYxYxYxYXyX")),
            ("g_r74_to_r62_via_aut.json", aut_equivalence_certificate_general,
             ("xxyXy", "xyyyyyyyxYY"), (0, ((-1, 0), (-7, -1)), -2, 9, "YxYYxYX"),
             ("xxyxyXy", "xyXYYYYXy"), (0, ((-2, -1), (-7, -4)), 2, -3, "YxYxYxYxYxYxYxYXyX")),
        ]
        for name, fn, A, la, B, lb in jobs:
            phi, cj = fn(A, la, B, lb)
            r = replay(cj)
            out = {"format": cj["format"], "start": cj["start"], "target": cj["target"], "moves": cj["moves"],
                   "note": "agent G: phi(A) -> B with phi = %s, A = %s, B = %s" % (list(phi), list(A), list(B))}
            with open(os.path.join(outdir, name), "w") as f:
                json.dump(out, f, separators=(",", ":"))
            print(name, "phi =", phi, r["moves"], "moves, peak", r["peak_total_length"])
    elif sys.argv[1:2] == ["--write"]:
        outdir = sys.argv[2]
        c2 = ak2_trivial()
        j2 = c2.to_json(["x", "y"])
        print("ak2:", replay(j2))
        with open(os.path.join(outdir, "g_ak2_torus_acm_trivialization.json"), "w") as f:
            json.dump(j2, f)
        for n in (3,):
            c, tgt = ak_to_trefoil_t2(n)
            j = c.to_json(tgt)
            print("ak%d -> trefoil+T(2,%d):" % (n, 2 * n + 1), replay(j), "target", tgt)
            with open(os.path.join(outdir, "g_ak%d_to_trefoil_t2_%d.json" % (n, 2 * n + 1)), "w") as f:
                json.dump(j, f)
