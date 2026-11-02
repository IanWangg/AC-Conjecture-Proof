"""Agent I: uniform certificates for torus-knot-pair presentations.

All certificates are strict `ordinary-ac-elementary-v1` (replayed by
experiments/elementary_verify.py); i_words.Cert expands every compound step.

  T(a;p,q) := (x^p y^q, x^a y x^-1 y),  m := a+1,  c := x^m,  z := x^-1 y.
  As free words  x^a y x^-1 y = c z z,  and  x^p y^q = x^p (x z)^q.

Lemma S (research-i.md): for all integers a, q and k >= 0,
  T(a; 1+mk, q)  ~AC  T(a; mk+m-1, q+2),
by 2k+1 insertions of conjugates of the second relator (lemma_s_cert).

Lemma E (same basis): (x^m y^n, x^p y^q) with mq - np = +-1 is AC-trivial
(euclid_cert, a Euclidean algorithm on the exponent rows).

Usage:
  python3 experiments/i_torus.py --selftest
  python3 experiments/i_torus.py --lemma-s A K Q OUT.json
  python3 experiments/i_torus.py --euclid M N P Q OUT.json
  python3 experiments/i_torus.py --sweep        # replay many parameters
  python3 experiments/i_torus.py --syll W M N    # cyclic syllable length of W in C_M*C_N (x->a, y->b)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from i_words import Cert, red, inv, pw, cyc, orbit  # noqa: E402
import elementary_verify as ev  # noqa: E402


def T(a, p, q):
    return red(pw("x", p) + pw("y", q)), red(pw("x", a) + "yXy")


def lemma_s_cert(a, k, q):
    """Certificate T(a;1+mk,q) -> T(a;mk+m-1,q+2), relator order (B, A)."""
    assert k >= 0
    m = a + 1
    B, A = T(a, 1 + m * k, q)
    c = Cert(B, A)
    C = pw("x", m)
    z, Z = "Xy", "Yx"
    assert red(C + z + z) == A                       # free identity A = c z z
    # 0. rotate B to y^q x^(1+mk)  (= (xz)^q x z^-1 . z c^k as free words)
    c.conj(0, pw("y", q))
    P = red(pw("y", q) + "x" + Z)
    assert c.s[0] == red(P + z + pw(C, k))
    # 1. k commutations  z c -> c z, each = insertion of [c,z] = A (z A^-1 z^-1)
    for j in range(k):
        Q = red(z + pw(C, k - j))                    # suffix after the insertion point
        c.mul_by(0, -1, red(inv(Q) + z))             # insert z A^-1 z^-1
        Q2 = red(z + inv(A) + inv(z) + Q)
        c.mul_by(0, +1, inv(Q2))                     # insert A in front of it
        assert c.s[0] == red(P + pw(C, j + 1) + z + pw(C, k - j - 1)), (a, k, q, j)
    # 2. rotate: conjugate by z
    c.conj(0, z)
    assert c.s[0] == red(z + P + pw(C, k))
    # 3. insert z A z^-1 (= z c z) in front of the suffix z^-1 c^k
    Q = red(Z + pw(C, k))
    c.mul_by(0, +1, red(inv(Q) + z))
    assert c.s[0] == red(z + pw("y", q) + "x" + z + pw(C, k + 1))
    # 4. exact endpoint x^(mk+m-1) y^(q+2)
    B2 = red(pw("x", m * k + m - 1) + pw("y", q + 2))
    c.to_rotation_of(0, B2)
    assert c.s == [B2, A]
    return c


def euclid_cert(m, n, p, q):
    """(x^m y^n, x^p y^q), |mq-np| = 1  ->  (x, y) exactly."""
    assert abs(m * q - n * p) == 1
    c = Cert(red(pw("x", m) + pw("y", n)), red(pw("x", p) + pw("y", q)))
    rows = [[m, n], [p, q]]

    def word(r):
        return red(pw("x", r[0]) + pw("y", r[1]))

    def size(r):
        return abs(r[0]) + abs(r[1])

    guard = 0
    while size(rows[0]) > 1 or size(rows[1]) > 1:
        guard += 1
        assert guard < 10000
        i = 0 if size(rows[0]) >= size(rows[1]) else 1
        j = 1 - i
        best = None
        for s in (1, -1):
            cand = [rows[i][0] - s * rows[j][0], rows[i][1] - s * rows[j][1]]
            if best is None or size(cand) < size(best[1]):
                best = (s, cand)
        s, cand = best
        assert size(cand) < size(rows[i]), (rows, cand)
        # bring r_i to x^e y^f (exact), r_j to the rotation y^g x^h of r_j^(-s)...
        c.to_rotation_of(i, word(rows[i]))
        # r_i * (y^-f2 x^-e2) = x^e y^(f-f2) x^-e2  ~  x^(e-e2) y^(f-f2)   (s=+1)
        # r_i * (y^f2 x^e2)   = x^e y^(f+f2) x^e2  ~  x^(e+e2) y^(f+f2)   (s=-1)
        e2, f2 = rows[j]
        if s == 1:
            donor = red(pw("y", -f2) + pw("x", -e2))
        else:
            donor = red(pw("y", f2) + pw("x", e2))
        c.to_rotation_of(j, donor) if donor else None
        c.mult(i)
        c.cyc_reduce(i)
        rows[i] = cand
        if size(cand) > 0:
            c.to_rotation_of(i, word(cand))
        c.to_rotation_of(j, word(rows[j]))
    # now rows are +-unit vectors; normalize to exact (x, y)
    for i in (0, 1):
        if c.s[i] in ("X", "Y"):
            c.invert(i)
    if c.s == ["y", "x"]:
        c.swap()
    assert c.s == ["x", "y"], c.s
    return c


def syllables(w, mm, nn):
    """Cyclic syllable length of the image of w in C_mm * C_nn (x->a, y->b)."""
    w = cyc(w)
    if not w:
        return 0
    syl = []
    for ch in w:
        g = 0 if ch in "xX" else 1
        e = 1 if ch in "xy" else -1
        if syl and syl[-1][0] == g:
            syl[-1][1] += e
        else:
            syl.append([g, e])
    order = (mm, nn)

    def norm(s):
        out = []
        for g, e in s:
            e %= order[g]
            if e == 0:
                continue
            if out and out[-1][0] == g:
                out[-1][1] = (out[-1][1] + e) % order[g]
                if out[-1][1] == 0:
                    out.pop()
            else:
                out.append([g, e])
        return out

    s = norm(syl)
    changed = True
    while changed and len(s) >= 2:
        changed = False
        if s[0][0] == s[-1][0]:
            g = s[0][0]
            e = (s[0][1] + s[-1][1]) % order[g]
            s = s[1:-1] + ([[g, e]] if e else [])
            s = norm(s)
            changed = True
    return len(s)


def selftest():
    n = 0
    for a in (2, 4, -4, 6, -2, 3):
        for k in range(0, 4):
            for q in (-7, -3, -1, 1, 2, 3, 7, 9):
                c = lemma_s_cert(a, k, q)
                r = ev.replay(c.as_json())
                assert r["endpoint"] == c.s
                n += 1
    m_ok = 0
    for m in range(-6, 7):
        for nn in range(-6, 7):
            for p in range(-6, 7):
                for q in range(-6, 7):
                    if abs(m * q - nn * p) == 1 and (m or nn) and (p or q):
                        c = euclid_cert(m, nn, p, q)
                        assert ev.replay(c.as_json())["endpoint"] == ["x", "y"]
                        m_ok += 1
    assert syllables("xxxxyyyyyyy", 4, 7) == 0
    assert syllables("xxyXy", 4, 7) == 4
    assert syllables("xyxYXY", 3, 4) == 6
    print("i_torus self-test passed: %d Lemma S certificates, %d Euclid certificates replayed" % (n, m_ok))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--selftest"]:
        selftest()
    elif args[:1] == ["--lemma-s"]:
        a, k, q = map(int, args[1:4])
        c = lemma_s_cert(a, k, q)
        note = "Lemma S (research-i.md): T(%d;%d,%d) -> T(%d;%d,%d), generated by experiments/i_torus.py" % (
            a, 1 + (a + 1) * k, q, a, (a + 1) * k + a, q + 2)
        json.dump(c.as_json(note=note), open(args[4], "w"), indent=0)
        print(json.dumps(ev.replay(c.as_json())))
    elif args[:1] == ["--euclid"]:
        m, n, p, q = map(int, args[1:5])
        c = euclid_cert(m, n, p, q)
        json.dump(c.as_json(note="Lemma E: same-basis torus pair, experiments/i_torus.py"), open(args[5], "w"), indent=0)
        print(json.dumps(ev.replay(c.as_json())))
    elif args[:1] == ["--syll"]:
        print(syllables(args[1], int(args[2]), int(args[3])))
    elif args[:1] == ["--sweep"]:
        cnt = 0
        mx = 0
        for a in range(-10, 11):
            for k in range(0, 6):
                for q in range(-11, 12):
                    c = lemma_s_cert(a, k, q)
                    ev.replay(c.as_json())
                    cnt += 1
                    mx = max(mx, len(c.moves))
        print("Lemma S sweep: %d certificates replayed (a in [-10,10], k in [0,5], q in [-11,11]); max moves %d" % (cnt, mx))
