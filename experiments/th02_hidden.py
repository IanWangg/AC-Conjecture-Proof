#!/usr/bin/env python3
"""th02_hidden.py (agent TH02) -- symbolic certificates for "hidden reflections".

Theorem TH02.1: if (u,v) is a basis of F(x,y), n any integer and r is conjugate
to (u^2 v^n)^{+-1}, then beta = (u -> u^-1 v^-n, v -> v) is an automorphism with
beta(g) = g mod <<r>> for all g and beta(r) conjugate to r^-1; hence
(beta(r), beta(s)) ~AC (r, s) for EVERY s.  This file builds the ordinary-AC
certificate (r,s) -> (beta(r), beta(s)) exactly, with one inserted conjugate of
r^{+-1} per u-letter of s, and the 2-insertion certificate of Lemma TH02.3:
T(a;2a,q) -> D(a;q) = (x^a y X y, x Y^2 x y^(q-2)).

Usage: python3 experiments/th02_hidden.py --self-test | --write
Words: x,y,X,Y (uppercase = inverse).  Standard library only.
"""
import json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from elementary_verify import reduce as red, inverse as inv, replay


def pw(letter, k):
    return (letter if k >= 0 else letter.swapcase()) * abs(k)


def subst(word, img):
    """letterwise image of word under x -> img['x'], y -> img['y'] (reduced)."""
    return red("".join(img[c] if c in img else inv(img[c.swapcase()]) for c in word))


def compose(f, g):
    """(f o g): apply g first."""
    return {"x": subst(g["x"], f), "y": subst(g["y"], f)}


def cycred(w):
    w = red(w); p = ""
    while len(w) > 1 and w[0] == w[-1].swapcase():
        p += w[0]; w = w[1:-1]
    return p, w          # red(word) = p w p^-1


def conjugator(src, dst):
    """g with g src g^-1 = dst (free group), or None."""
    p, c = cycred(src); q, d = cycred(dst)
    if len(c) != len(d):
        return None
    for k in range(max(1, len(c))):
        if c[k:] + c[:k] == d:
            return red(q + inv(c[:k]) + inv(p))
    return None


class Cert:
    def __init__(self, start):
        self.start = [red(w) for w in start]
        self.state = list(self.start)
        self.moves = []

    def invert(self, i):
        self.moves.append({"op": "invert", "i": i})
        self.state[i] = inv(self.state[i])

    def mult(self, i, j):
        self.moves.append({"op": "multiply", "i": i, "j": j})
        self.state[i] = red(self.state[i] + self.state[j])

    def conj(self, i, g):
        """r_i -> g r_i g^-1 for a word g."""
        for c in reversed(red(g)):
            self.moves.append({"op": "conjugate", "i": i, "g": c})
            self.state[i] = red(c + self.state[i] + c.swapcase())

    def insert(self, i, j, h, eps):
        """r_i -> r_i * h r_j^eps h^-1 (r_j restored afterwards)."""
        self.conj(j, h)
        if eps < 0:
            self.invert(j)
        self.mult(i, j)
        if eps < 0:
            self.invert(j)
        self.conj(j, inv(h))

    def to(self, i, word):
        """conjugate (and invert if necessary) r_i to exactly `word`."""
        g = conjugator(self.state[i], word)
        if g is None:
            self.invert(i)
            g = conjugator(self.state[i], word)
        assert g is not None, (self.state[i], word)
        self.conj(i, g)
        assert self.state[i] == red(word)

    def cert(self, target, description):
        c = {"format": "ordinary-ac-elementary-v1", "start": self.start,
             "target": [red(w) for w in target], "moves": self.moves,
             "description": description}
        assert self.state == c["target"], (self.state, c["target"])
        return c


def hidden_reflection(theta, theta_inv, n):
    """beta = theta o (x -> X Y^n, y -> y) o theta^-1 as a letter map."""
    assert compose(theta, theta_inv) == {"x": "x", "y": "y"}
    assert compose(theta_inv, theta) == {"x": "x", "y": "y"}
    b0 = {"x": red("X" + pw("Y", n)), "y": "y"}
    return compose(theta, compose(b0, theta_inv))


def reflect_cert(pair, i, theta, theta_inv, n, label=""):
    """certificate pair -> (beta(pair[0]), beta(pair[1])), where pair[i] is
    conjugate to (u^2 v^n)^{+-1}, u = theta(x), v = theta(y)."""
    j = 1 - i
    beta = hidden_reflection(theta, theta_inv, n)
    U = theta["x"]
    rho = red(U + U + subst(pw("y", n), theta))
    C = Cert(pair)
    target = [subst(w, beta) for w in C.start]
    C.to(i, rho)                                  # r_i = u^2 v^n exactly
    t = subst(C.state[j], theta_inv)              # s in (u,v)-coordinates
    assert subst(t, theta) == C.state[j]
    ins = 0
    for k, c in enumerate(t):
        tail = inv(t[k + 1:])
        if c == "x":      # x^-1 beta0(x) = X^2 rho^-1 x^2
            C.insert(j, i, subst(tail + "XX", theta), -1); ins += 1
        elif c == "X":    # x beta0(X) = X rho x
            C.insert(j, i, subst(tail + "X", theta), +1); ins += 1
    assert C.state[j] == target[j], (C.state[j], target[j])
    C.to(i, target[i])                            # beta(rho) = u^-1 rho^-1 u
    return C.cert(target, "TH02 hidden reflection %s: %s -> beta(pair), beta = "
                  "(x -> %s, y -> %s); relator %d is conjugate to (u^2 v^%d)^+-1 "
                  "with u = %s, v = %s; %d inserted conjugates."
                  % (label, C.start, beta["x"], beta["y"], i, n, U, theta["y"], ins)), beta


def T(a, p, q):
    return [red(pw("x", p) + pw("y", q)), red(pw("x", a) + "yXy")]


def D(a, q):
    return [red("xYYx" + pw("y", q - 2)), red(pw("x", a) + "yXy")]


def double_form_cert(a, q):
    """T(a;2a,q) -> D(a;q): x^a = A*(Y x Y) freely, A = x^a y X y."""
    C = Cert(T(a, 2 * a, q))
    A = C.state[1]
    t2 = red("YxY" + pw("y", q)); t1 = red("YxY" + A + t2)
    assert red(A + t1) == C.state[0]
    C.insert(0, 1, inv(t1), -1); assert C.state[0] == red(t1)
    C.insert(0, 1, inv(t2), -1); assert C.state[0] == red("YxY" + t2)
    C.conj(0, "y")
    return C.cert(D(a, q), "TH02 Lemma 3: T(%d;%d,%d) -> D(%d;%d), two inserted "
                  "conjugates of A^-1 and one rotation." % (a, 2 * a, q, a, q))


def matrix(aut):
    e = lambda w: (w.count("x") - w.count("X"), w.count("y") - w.count("Y"))
    cx, cy = e(aut["x"]), e(aut["y"])
    return ((cx[0], cy[0]), (cx[1], cy[1]))     # columns = images of x, y


# ---- composition tools: reverse a move list, transport it by an automorphism
def reverse_moves(moves):
    out = []
    for m in reversed(moves):
        if m["op"] == "invert":
            out.append(dict(m))
        elif m["op"] == "conjugate":
            out.append({"op": "conjugate", "i": m["i"], "g": m["g"].swapcase()})
        else:
            out += [{"op": "invert", "i": m["j"]}, dict(m), {"op": "invert", "i": m["j"]}]
    return out


def transport_moves(moves, aut):
    """moves U -> V  become moves aut(U) -> aut(V) (Lemma D2 of research-d)."""
    out = []
    for m in moves:
        if m["op"] == "conjugate":
            for c in reversed(subst(m["g"], aut)):
                out.append({"op": "conjugate", "i": m["i"], "g": c})
        else:
            out.append(dict(m))
    return out


def run(start, moves):
    C = Cert(start)
    for m in moves:
        if m["op"] == "invert":
            C.invert(m["i"])
        elif m["op"] == "multiply":
            C.mult(m["i"], m["j"])
        else:
            C.conj(m["i"], m["g"])
    return C


TH_A = {"x": "Xy", "y": "x"}; TH_A_INV = {"x": "y", "y": "yx"}       # u = z = Xy, v = x
TH_W = {"x": "xYY", "y": "y"}; TH_W_INV = {"x": "xyy", "y": "y"}     # u = w = xYY, v = y


def mmul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def closure(gens, limit=400):
    I = ((1, 0), (0, 1)); seen = {I}; todo = [I]
    while todo and len(seen) <= limit:
        g = todo.pop()
        for h in gens:
            k = mmul(g, h)
            if k not in seen:
                seen.add(k); todo.append(k)
    return seen


def checked(cert):
    out = replay(cert)
    return out


def self_test():
    import random
    rnd = random.Random(2)
    n_cert = 0
    # (1) hidden reflection of A = x^a y X y against random partners s
    for a in range(-7, 9):
        A = red(pw("x", a) + "yXy")
        for _ in range(6):
            s = red("".join(rnd.choice("xyXY") for _ in range(rnd.randint(1, 14)))) or "y"
            c, beta = reflect_cert([s, A], 1, TH_A, TH_A_INV, a + 1)
            replay(c); n_cert += 1
            assert beta == {"x": "x", "y": red("xY" + pw("X", a))}, beta
            assert matrix(beta) == ((1, 1 - a), (0, -1))
    # (2) both reflections of D(a;q), the double form, and the trace formula
    for a in range(-6, 9, 2):
        for q in range(-9, 12, 2):
            replay(double_form_cert(a, q)); n_cert += 1
            c1, b1 = reflect_cert(D(a, q), 1, TH_A, TH_A_INV, a + 1); replay(c1)
            c2, b2 = reflect_cert(D(a, q), 0, TH_W, TH_W_INV, q); replay(c2); n_cert += 2
            assert matrix(b2) == ((-1, 0), (4 - q, 1)), matrix(b2)
            h = mmul(matrix(b1), matrix(b2))
            delta = 4 * a - (a - 1) * q
            assert h[0][0] * h[1][1] - h[0][1] * h[1][0] == 1 and h[0][0] + h[1][1] == 2 - delta
    # (3) C4: the group generated by the two hidden reflections is N's D6
    bA = ((1, -3), (0, -1)); bW = ((-1, 0), (-1, 1))
    N = closure([((-1, 0), (0, -1)), ((-1, 0), (-1, 1)), ((-1, 3), (0, 1))])
    G = closure([bA, bW])
    assert len(G) == 12 and G == N
    assert len(closure([((1, -1), (0, -1)), ((-1, 0), (-3, 1))])) == 12       # C3 ~ D(2;7)
    assert len(closure([((1, -1), (0, -1)), ((-1, 0), (-5, 1))])) > 400       # X  ~ D(2;9)
    # (4) negative controls: the builder must refuse a non-T(2,n) relator
    try:
        reflect_cert(["xxxyyyy", "xyxYXY"], 0, TH_W, TH_W_INV, 5); raise SystemExit("control failed")
    except AssertionError:
        pass
    print("self-test OK: %d certificates built and replayed by elementary_verify.replay" % n_cert)


def loop_cert(a, q):
    """T(a;2a,q) -> h(T(a;2a,q)) exactly, h = beta_A o beta_w (letterwise composition)."""
    X = T(a, 2 * a, q)
    m1 = double_form_cert(a, q)["moves"]                               # X -> D
    c2, bW = reflect_cert(D(a, q), 0, TH_W, TH_W_INV, q)               # D -> bW(D)
    to_bw = m1 + c2["moves"] + transport_moves(reverse_moves(m1), bW)  # X -> bW(X)
    c3, bA = reflect_cert(X, 1, TH_A, TH_A_INV, a + 1)                 # X -> bA(X)
    moves = c3["moves"] + transport_moves(to_bw, bA)                   # -> bA(bW(X))
    h = compose(bA, bW)
    C = run(X, moves)
    M = matrix(h)
    return C.cert([subst(w, h) for w in X],
                  "TH02 Theorem 4: T(%d;%d,%d) -> h(T) exactly, h = beta_A o beta_w = "
                  "(x -> %s, y -> %s), matrix (rows) %s, trace %d; built from Lemma 3 "
                  "and two hidden reflections, no search."
                  % (a, 2 * a, q, h["x"], h["y"], M, M[0][0] + M[1][1])), h


def write_all():
    out = os.path.join(os.path.dirname(HERE), "certificates")
    C4 = ["xxxxyXy", "xyyyxYY"]
    jobs = {
        "th02_c4_reflect_A.json": reflect_cert(C4, 0, TH_A, TH_A_INV, 5, "of x^4yXy = x^5 z^2 on C4")[0],
        "th02_c4_reflect_w.json": reflect_cert(C4, 1, TH_W, TH_W_INV, 5, "of xy^3xY^2 ~ w^2 y^5 on C4")[0],
        "th02_T4_8_5_to_D4_5.json": double_form_cert(4, 5),
        "th02_T2_4_7_to_D2_7.json": double_form_cert(2, 7),
        "th02_x_to_D2_9.json": double_form_cert(2, 9),
        "th02_x_hyperbolic.json": loop_cert(2, 9)[0],
        "th02_T6_12_5_hyperbolic.json": loop_cert(6, 5)[0],
        "th02_c3form_order6.json": loop_cert(2, 7)[0],
    }
    for name, c in jobs.items():
        res = replay(c)
        with open(os.path.join(out, name), "w") as f:
            json.dump(c, f, separators=(",", ":"))
        print(name, json.dumps(res))


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    elif "--write" in sys.argv:
        write_all()
    else:
        print(__doc__)
