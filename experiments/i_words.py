"""Agent I: word utilities and an elementary-certificate builder.

Words use x, X=x^-1, y, Y=y^-1.  The builder records ONLY the three strict
primitives of `ordinary-ac-elementary-v1` (see experiments/elementary_verify.py):
  invert(i); multiply(i,j) [right]; conjugate(i,g) = g r_i g^-1, g one letter.
Every compound operation (left multiplication, multiplication by an inverse
or by a conjugate of the other relator, cyclic rotation, cyclic reduction,
swap-free normalization to an exact target) is expanded here into those
primitives, and the state is tracked exactly as the verifier will replay it.

Run `python3 experiments/i_words.py --selftest`.
"""
import json
import sys

LET = "xXyY"


def red(w):
    out = []
    for c in w:
        if out and out[-1] == c.swapcase():
            out.pop()
        else:
            out.append(c)
    return "".join(out)


def inv(w):
    return w.swapcase()[::-1]


def cyc(w):
    w = red(w)
    while len(w) >= 2 and w[0] == w[-1].swapcase():
        w = w[1:-1]
    return w


def pw(w, n):
    """w^n as a freely reduced word (n may be negative)."""
    if n < 0:
        return red(inv(w) * (-n))
    return red(w * n)


def rotations(w):
    return {w[k:] + w[:k] for k in range(max(len(w), 1))}


def orbit(w):
    w = cyc(w)
    return rotations(w) | rotations(inv(w))


def canon(w):
    return min(orbit(w)) if w else ""


def canon_pair(a, b):
    return tuple(sorted((canon(a), canon(b))))


def subst(w, img):
    """Apply the endomorphism x->img['x'], y->img['y'] to w."""
    out = []
    for c in w:
        if c == "x":
            out.append(img["x"])
        elif c == "X":
            out.append(inv(img["x"]))
        elif c == "y":
            out.append(img["y"])
        else:
            out.append(inv(img["y"]))
    return red("".join(out))


class Cert:
    """Exact state + strict elementary move log."""

    def __init__(self, a, b):
        self.start = [red(a), red(b)]
        self.s = list(self.start)
        self.moves = []
        self.peak = len(self.s[0]) + len(self.s[1])

    def _bump(self):
        self.peak = max(self.peak, len(self.s[0]) + len(self.s[1]))

    # --- strict primitives -------------------------------------------------
    def invert(self, i):
        self.s[i] = inv(self.s[i])
        self.moves.append({"op": "invert", "i": i})
        self._bump()

    def mult(self, i):
        j = 1 - i
        self.s[i] = red(self.s[i] + self.s[j])
        self.moves.append({"op": "multiply", "i": i, "j": j})
        self._bump()

    def conj1(self, i, g):
        assert len(g) == 1 and g in LET
        self.s[i] = red(g + self.s[i] + inv(g))
        self.moves.append({"op": "conjugate", "i": i, "g": g})
        self._bump()

    # --- composites --------------------------------------------------------
    def conj(self, i, w):
        """r_i <- w r_i w^-1 (w any word), as single-letter conjugations."""
        for g in reversed(red(w)):
            self.conj1(i, g)

    def mul_by(self, i, sign=1, h=""):
        """r_i <- r_i * (h r_j^sign h^-1), j the other relator; r_j restored."""
        j = 1 - i
        h = red(h)
        if sign < 0:
            self.invert(j)
        self.conj(j, h)
        self.mult(i)
        self.conj(j, inv(h))
        if sign < 0:
            self.invert(j)

    def lmul_by(self, i, sign=1, h=""):
        """r_i <- (h r_j^sign h^-1) * r_i, via conjugation of r_i."""
        # (h r h^-1) r_i = (h r h^-1) [r_i (h r h^-1)] (h r h^-1)^-1
        # so: r_i <- r_i * c ; then conjugate r_i by c where c=h r_j^s h^-1.
        # cheaper: conjugate r_i by g^-1, right-multiply, conjugate back,
        # where g = h r_j^s h^-1 is not a letter; use the identity
        #   c * r_i = c (r_i c) c^-1 .
        j = 1 - i
        c = red(h + (self.s[j] if sign > 0 else inv(self.s[j])) + inv(h))
        self.mul_by(i, sign, h)
        self.conj(i, c)

    def rotate_left(self, i, k):
        """r_i = u v with |u| = k  ->  v u   (conjugation by u^-1)."""
        r = self.s[i]
        if not r:
            return
        k %= len(r)
        if k == 0:
            return
        if k <= len(r) - k:
            self.conj(i, inv(r[:k]))
        else:
            # v u = (v) r (v^-1)... v u = v (u v) v^-1
            self.conj(i, r[k:])
        assert self.s[i] == r[k:] + r[:k], (self.s[i], r, k)

    def cyc_reduce(self, i):
        r = self.s[i]
        while len(r) >= 2 and r[0] == r[-1].swapcase():
            self.conj1(i, r[0].swapcase())
            r = self.s[i]

    def to_rotation_of(self, i, w):
        """Bring cyclically reduced r_i to the exact word w in orbit(r_i)."""
        self.cyc_reduce(i)
        r = self.s[i]
        if w in rotations(r):
            k = (r + r).index(w) if r else 0
            self.rotate_left(i, k)
        elif w in rotations(inv(r)):
            self.invert(i)
            r = self.s[i]
            self.rotate_left(i, (r + r).index(w))
        else:
            raise ValueError("%s not in orbit of %s" % (w, r))
        assert self.s[i] == w

    def swap(self):
        """(a,b)->(b,a) by strict primitives: (a,b)->(ab,b)->(ab,B)->(a,B)...

        Uses: a<-ab ; b<-b^-1 ; b<-b * (a b ... ) -- the standard identity
        (a,b)->(ab,b)->(ab,b^-1 a b)... we use the 9-step identity from
        research-d Lemma D1(a) expressed with conjugations by words.
        """
        a, b = self.s
        self.mult(0)                 # (ab, b)
        self.invert(1)               # (ab, B)
        # b <- B * (ab) conjugated: B^? ; simpler: b <- (ab)^{B}... use
        # (ab, B) -> (ab, B ab) ->conj by B^-1=b... direct approach:
        self.mult(1)                 # (ab, B a b)
        self.conj(1, red(b))         # (ab, a)   since b (B a b) B = a
        self.invert(1)               # (ab, A)
        self.mult(0)                 # (a b A, A)
        self.conj(0, inv(a))         # (b, A)    A (a b A) a = b
        self.invert(1)               # (b, a)
        assert self.s == [b, a], (self.s, a, b)

    def as_json(self, target=None, note=""):
        return {"format": "ordinary-ac-elementary-v1", "note": note,
                "start": self.start, "target": target or list(self.s),
                "moves": self.moves}


def zarco_to_cert(ledger):
    """Convert an integer ledger (1=x,2=y; moves invert/mul/conj/cycle)."""
    m = {1: "x", -1: "X", 2: "y", -2: "Y"}
    a, b = ("".join(m[t] for t in w) for w in ledger["initial"])
    c = Cert(a, b)
    for mv in ledger["moves"]:
        op = mv[0]
        if op == "invert":
            c.invert(mv[1])
        elif op == "mul":
            i, j, s = mv[1], mv[2], mv[3]
            assert j == 1 - i
            c.mul_by(i, s)
        elif op == "conj":
            c.conj1(mv[1], m[mv[2]])
        elif op == "cycle":
            i, k = mv[1], mv[2]
            r = c.s[i]
            if r:
                k %= len(r)
                u = r[:k]
                c.conj(i, inv(u))
                # zarco: r <- reduce(u^-1 r u); same as conj by u^-1
        else:
            raise ValueError(op)
    return c


def selftest():
    sys.path.insert(0, "experiments")
    import elementary_verify as ev
    import random
    rnd = random.Random(7)
    for _ in range(300):
        a = red("".join(rnd.choice(LET) for _ in range(rnd.randint(1, 9))))
        b = red("".join(rnd.choice(LET) for _ in range(rnd.randint(1, 9))))
        if not a or not b:
            continue
        c = Cert(a, b)
        for _ in range(6):
            t = rnd.randrange(6)
            i = rnd.randrange(2)
            if t == 0:
                c.mul_by(i, rnd.choice((1, -1)), red("".join(rnd.choice(LET) for _ in range(rnd.randint(0, 3)))))
            elif t == 1:
                c.lmul_by(i, rnd.choice((1, -1)), red("".join(rnd.choice(LET) for _ in range(rnd.randint(0, 3)))))
            elif t == 2:
                c.conj(i, red("".join(rnd.choice(LET) for _ in range(rnd.randint(0, 3)))))
            elif t == 3 and c.s[i]:
                c.cyc_reduce(i)
                c.rotate_left(i, rnd.randrange(len(c.s[i]) + 1))
            elif t == 4:
                c.swap()
            elif t == 5:
                c.invert(i)
        ev.replay(c.as_json())
        # lmul identity check
    c = Cert("xy", "yy")
    c.lmul_by(0, 1, "x")
    assert c.s[0] == red("x" + "yy" + "X" + "xy"), c.s
    c = Cert("xxyXYY", "xxxYYXy")
    c.to_rotation_of(0, "YYxxyX")
    c.to_rotation_of(1, inv("xxxYYXy")[2:] + inv("xxxYYXy")[:2])
    ev.replay(c.as_json())
    print("i_words self-test passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif sys.argv[1:2] == ["--zarco"]:
        # --zarco LEDGER.json OUT.json : convert, normalize to exact target
        led = json.load(open(sys.argv[2]))
        c = zarco_to_cert(led)
        m = {1: "x", -1: "X", 2: "y", -2: "Y"}
        tgt = ["".join(m[t] for t in w) for w in led["target"]]
        # find matching assignment (maybe swapped)
        s0, s1 = cyc(c.s[0]), cyc(c.s[1])
        if s0 in orbit(tgt[0]) and s1 in orbit(tgt[1]):
            pass
        elif s0 in orbit(tgt[1]) and s1 in orbit(tgt[0]):
            c.swap()
        else:
            raise SystemExit("terminal not in target orbit")
        c.to_rotation_of(0, tgt[0])
        c.to_rotation_of(1, tgt[1])
        json.dump(c.as_json(tgt, note=sys.argv[4] if len(sys.argv) > 4 else ""),
                  open(sys.argv[3], "w"), indent=0)
        print("written", sys.argv[3], len(c.moves), "moves, peak", c.peak)
