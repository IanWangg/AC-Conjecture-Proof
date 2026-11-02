#!/usr/bin/env python3
"""Expand a d_acsearch PATH (a list of Sigma-canonical states) into a strict
ordinary-AC certificate (format ordinary-ac-elementary-v1, checked by
experiments/elementary_verify.py).  Standard library only, independent of
the C++ engine: it uses its own canonical forms and re-finds every move.

Elementary moves emitted: invert(i), multiply(i,j) (right), conjugate(i,g)
with g a single signed generator.  A cyclic product step
    r_i <- cyclic_reduction(rot_k(r_i) * rot_l(r_j)^(+-1))
is compiled as: k single-letter conjugations of r_i, l of r_j, an optional
inversion of r_j, multiply(i,j), single-letter conjugations performing the
cyclic reduction of r_i.  The final Sigma-normalization to the exact target
tuple uses rotations, inversions and (if needed) the 8-move swap identity
(a,b)->(ab,b)->(ab,B)->(ab,BAb... see swap_moves).

Usage:
  python3 experiments/d_certify.py PATHFILE START1 START2 TARGET1 TARGET2 OUT.json [description]
PATHFILE holds one canonical state per line: "<word1> <word2>" (the C++
PATH output split on brackets), first line = Sigma-image of START, last
line = Sigma-image of TARGET.
  python3 experiments/d_certify.py --self-test
"""
import json
import sys

INV = {"x": "X", "X": "x", "y": "Y", "Y": "y"}


def reduce(w):
    out = []
    for c in w:
        if out and out[-1] == INV[c]:
            out.pop()
        else:
            out.append(c)
    return "".join(out)


def inverse(w):
    return "".join(INV[c] for c in reversed(w))


def cycred(w):
    w = reduce(w)
    while len(w) >= 2 and w[0] == INV[w[-1]]:
        w = w[1:-1]
    return w


def canon_word(w):
    w = cycred(w)
    cands = [u[k:] + u[:k] for u in (w, inverse(w)) for k in range(len(w))]
    return min(cands) if cands else ""


def canon_pair(a, b):
    return tuple(sorted((canon_word(a), canon_word(b))))


class Builder:
    def __init__(self, start):
        self.state = [reduce(start[0]), reduce(start[1])]
        self.moves = []
        self.peak = sum(map(len, self.state))

    def _apply(self, mv):
        i = mv["i"]
        if mv["op"] == "invert":
            self.state[i] = inverse(self.state[i])
        elif mv["op"] == "multiply":
            self.state[i] = reduce(self.state[i] + self.state[mv["j"]])
        elif mv["op"] == "conjugate":
            g = mv["g"]
            self.state[i] = reduce(g + self.state[i] + INV[g])
        self.moves.append(mv)
        self.peak = max(self.peak, sum(map(len, self.state)))

    def invert(self, i):
        self._apply({"op": "invert", "i": i})

    def multiply(self, i):
        self._apply({"op": "multiply", "i": i, "j": 1 - i})

    def conj(self, i, g):
        self._apply({"op": "conjugate", "i": i, "g": g})

    def conj_word(self, i, word):
        # g r g^-1 for a word g: conjugate by its letters, last letter first
        for g in reversed(word):
            self.conj(i, g)

    def rotate(self, i, k):
        """Left-rotate cyclically reduced relator i by k letters."""
        w = self.state[i]
        n = len(w)
        k %= n
        if k <= n - k:
            for _ in range(k):
                self.conj(i, INV[self.state[i][0]])
        else:
            for _ in range(n - k):
                self.conj(i, self.state[i][-1])
        assert self.state[i] == w[k:] + w[:k]

    def cyclic_reduce(self, i):
        while len(self.state[i]) >= 2 and self.state[i][0] == INV[self.state[i][-1]]:
            self.conj(i, INV[self.state[i][0]])

    def cyclic_product(self, i, k, l, sign):
        j = 1 - i
        self.rotate(i, k)
        if sign < 0:
            self.invert(j)
        self.rotate(j, l)
        self.multiply(i)
        self.cyclic_reduce(i)

    def swap(self):
        a, b = self.state
        self.multiply(0)          # (ab, b)
        self.invert(1)            # (ab, B)
        self.multiply(1)          # (ab, B a b)
        self.conj_word(1, b)      # (ab, a)
        self.invert(1)            # (ab, A)
        self.multiply(0)          # (a b A, A)
        self.conj_word(0, inverse(a))  # (b, A)
        self.invert(1)            # (b, a)
        assert self.state == [a, b][::-1], self.state


def find_step(state, target_canon):
    """Find (i,k,l,sign) with canon(new state) == target_canon."""
    for i in (0, 1):
        j = 1 - i
        u, v = state[i], state[j]
        for sign in (1, -1):
            vv = v if sign > 0 else inverse(v)
            for k in range(len(u)):
                uk = u[k:] + u[:k]
                for l in range(len(vv)):
                    vl = vv[l:] + vv[:l]
                    w = cycred(uk + vl)
                    if w and canon_pair(w, v) == target_canon:
                        return i, k, l, sign
    return None


def orient(builder, i, target):
    """Make relator i literally equal target using inversion + rotation."""
    w = builder.state[i]
    for inv_first in (False, True):
        u = inverse(w) if inv_first else w
        for k in range(len(u)):
            if u[k:] + u[:k] == target:
                if inv_first:
                    builder.invert(i)
                builder.rotate(i, k)
                assert builder.state[i] == target
                return True
    return False


def build(path_states, start, target):
    b = Builder(start)
    if canon_pair(*b.state) != canon_pair(*path_states[0]):
        raise ValueError("path does not start at the start tuple's Sigma-orbit")
    for st in path_states[1:]:
        tc = canon_pair(*st)
        step = find_step(b.state, tc)
        if step is None:
            raise ValueError(f"no cyclic product reaches {st}")
        b.cyclic_product(*step)
        assert canon_pair(*b.state) == tc
    if canon_pair(*b.state) != canon_pair(*target):
        raise ValueError("path end is not in the target's Sigma-orbit")
    if canon_word(b.state[0]) != canon_word(target[0]) or canon_word(b.state[1]) != canon_word(target[1]):
        b.swap()
    assert orient(b, 0, target[0]) and orient(b, 1, target[1])
    return b


def certificate(path_states, start, target, description):
    b = build(path_states, start, target)
    return {"format": "ordinary-ac-elementary-v1", "start": list(start),
            "target": list(target), "moves": b.moves,
            "description": description,
            "cyclic_steps": len(path_states) - 1,
            "peak_total_length_elementary": b.peak}


def read_path(fn):
    states = []
    for line in open(fn):
        p = line.split()
        if len(p) == 2:
            states.append((p[0], p[1]))
    return states


def selftest():
    # AK(3) one cyclic step to some neighbour and back, then swap check
    start = ("xxxYYYY", "xyxYXY")
    b = Builder(start)
    b.cyclic_product(0, 2, 3, -1)
    mid = tuple(b.state)
    path = [start, mid, start]
    c = certificate(path, start, ("xyxYXY", "xxxYYYY"), "self-test")
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    import elementary_verify
    r = elementary_verify.replay(c)
    assert r["endpoint"] == ["xyxYXY", "xxxYYYY"]
    print("self-test passed:", r["moves"], "moves")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        selftest()
        sys.exit(0)
    pathfile, s1, s2, t1, t2, out = sys.argv[1:7]
    desc = sys.argv[7] if len(sys.argv) > 7 else ""
    cert = certificate(read_path(pathfile), (s1, s2), (t1, t2), desc)
    with open(out, "w") as f:
        json.dump(cert, f, indent=1)
    print(f"wrote {out}: {len(cert['moves'])} elementary moves, "
          f"{cert['cyclic_steps']} cyclic steps, peak {cert['peak_total_length_elementary']}")
