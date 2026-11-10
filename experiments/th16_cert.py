#!/usr/bin/env python3
"""TH16: search a short cyclic-product path (second relator frozen) and compile it to a strict
ordinary-ac-elementary-v1 certificate.  Usage:
  python3 experiments/th16_cert.py R S TARGET_R OUT.json [cap]   # (R,S) -> (TARGET_R, S), S frozen, exact words
Standard library only; the output is checked by experiments/elementary_verify.py."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from th16_rigidity import red, cyc, inv, rots, orb

def find_path(r, s, target_orb, cap=16, maxdepth=8):
    """BFS over r -> cyc(a + b), a in rots(r^{+-1}), b in rots(s^{+-1}); returns list of (a, b, result)"""
    canon = lambda w: min(orb(w))
    start = cyc(r); seen = {canon(start): None}; frontier = [start]
    bs = rots(s) + rots(inv(s))
    for _ in range(maxdepth):
        nxt = []
        for w in frontier:
            for a in rots(w) + rots(inv(w)):
                for b in bs:
                    v = cyc(a + b)
                    if not v or len(v) > cap: continue
                    c = canon(v)
                    if c in seen: continue
                    seen[c] = (canon(w), a, b, v); nxt.append(v)
                    if v in target_orb:
                        path = []; k = c
                        while seen[k] is not None:
                            pk, a_, b_, v_ = seen[k]; path.append((a_, b_, v_)); k = pk
                        return path[::-1]
        frontier = nxt
    return None

class Cert:
    def __init__(self, r, s):
        self.st = [red(r), red(s)]; self.start = list(self.st); self.moves = []
    def conj(self, i, g):
        self.st[i] = red(g + self.st[i] + g.swapcase()); self.moves.append({"op": "conjugate", "i": i, "g": g})
    def invert(self, i):
        self.st[i] = inv(self.st[i]); self.moves.append({"op": "invert", "i": i})
    def mult(self, i, j):
        self.st[i] = red(self.st[i] + self.st[j]); self.moves.append({"op": "multiply", "i": i, "j": j})
    def cycred(self, i):
        while len(self.st[i]) > 1 and self.st[i][0] == self.st[i][-1].swapcase(): self.conj(i, self.st[i][-1])
    def bring(self, i, w):
        """make relator i exactly equal to w, where w is a rotation of the current (cyclically reduced) word or of its inverse"""
        self.cycred(i)
        if w not in rots(self.st[i]): self.invert(i)
        assert w in rots(self.st[i]), (w, self.st[i])
        while self.st[i] != w: self.conj(i, self.st[i][-1])      # move the last letter to the front

def compile_path(r, s, path, target_r):
    C = Cert(r, s)
    for a, b, v in path:
        C.bring(0, a); C.bring(1, b); C.mult(0, 1); C.cycred(0)
        assert C.st[0] in rots(v), (C.st[0], v)
    C.bring(0, target_r); C.bring(1, red(s))
    assert C.st == [target_r, red(s)]
    return {"format": "ordinary-ac-elementary-v1", "start": C.start, "target": C.st, "moves": C.moves}

if __name__ == "__main__":
    r, s, tgt, out = sys.argv[1:5]; cap = int(sys.argv[5]) if len(sys.argv) > 5 else 16
    path = find_path(r, s, orb(tgt), cap)
    assert path is not None, "no path within the bounds"
    cert = compile_path(r, s, path, tgt)
    json.dump(cert, open(out, "w"))
    print("cyclic products:", [(a, b, v) for a, b, v in path])
    print("elementary moves:", len(cert["moves"]), "written to", out)
