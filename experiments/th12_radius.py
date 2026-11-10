"""TH12 experiment: exact minimal radius of an expression of x (and y) over AK(n).

rho*(w) = least rho such that w lies in H_rho = < g u g^-1 : u in {r,s}, |g| <= rho >
(a subgroup of the free group F(x,y); membership decided by Stallings folding).
By Theorem 1 of research-th12.md every instruction trivialization has kappa >= rho*(x), rho*(y).
Usage: python3 experiments/th12_radius.py [--selftest] [--pn] [nmax] [rhomax]
"""
import sys

class Fold:
    def __init__(self):
        self.par = [0]; self.nb = [dict()]          # nb[v][letter] -> vertex
    def new(self):
        self.par.append(len(self.par)); self.nb.append(dict()); return len(self.par) - 1
    def find(self, v):
        while self.par[v] != v:
            self.par[v] = self.par[self.par[v]]; v = self.par[v]
        return v
    def edge(self, u, a, v):                         # add edge u --a--> v, folding as needed
        todo = [(u, a, v)]
        while todo:
            u, a, v = todo.pop(); u = self.find(u); v = self.find(v)
            for p, c, q in ((u, a, v), (v, a.swapcase(), u)):
                p = self.find(p); q = self.find(q)
                w = self.nb[p].get(c)
                if w is None: self.nb[p][c] = q
                else:
                    w = self.find(w)
                    if w != q: self.merge(w, q, todo)
    def merge(self, p, q, todo):
        p = self.find(p); q = self.find(q)
        if p == q: return
        if len(self.nb[p]) < len(self.nb[q]): p, q = q, p
        self.par[q] = p
        for c, w in self.nb[q].items(): todo.append((p, c, w))
        self.nb[q] = dict()
    def loop(self, v, word):
        cur = v
        for k, c in enumerate(word):
            nxt = v if k == len(word) - 1 else self.new()
            self.edge(cur, c, nxt); cur = nxt
    def reads_loop(self, word):
        v = self.find(0)
        for c in word:
            w = self.nb[self.find(v)].get(c)
            if w is None: return False
            v = self.find(w)
        return v == self.find(0)

def H(rels, rho):
    f = Fold(); layer = [(0, "")]; verts = [0]
    for _ in range(rho):
        nxt = []
        for v, last in layer:
            for c in "xXyY":
                if last and c == last.swapcase(): continue
                w = f.new(); f.edge(v, c, w); nxt.append((w, c)); verts.append(w)
        layer = nxt
    for v in verts:
        for u in rels: f.loop(v, u)
    return f

def radius(rels, word, rhomax):
    for rho in range(rhomax + 1):
        if H(rels, rho).reads_loop(word): return rho
    return None

def ak(n): return ["x"*n + "Y"*(n+1), "xyxYXY"]

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--selftest" in sys.argv:
        assert radius(["x", "y"], "x", 2) == 0
        assert radius(["yxY", "y"], "x", 3) == 0          # x = Y (yxY) y is a word in the generators
        assert radius(["yxY", "xyX"], "x", 3) == 1        # needs the conjugator Y
        assert radius(["yxY", "xyX"], "y", 3) == 1
        assert radius(["xy", "y"], "x", 2) == 0           # x = (xy) y^-1
        assert radius(["xxyXXY", "y"], "x", 3) is None    # <<[x^2,y], y>> does not contain x
        print("th12_radius selftest OK")
    nmax = int(args[0]) if args else 6; rhomax = int(args[1]) if len(args) > 1 else 7
    if "--pn" in sys.argv:                               # K's coordinates P_n = (xyxYYXy, x^n YXyy)
        for n in range(2, nmax + 1):
            rels = ["xyxYYXy", "x"*n + "YXyy"]
            print("P_%d  rho*(x)=%s  rho*(y)=%s" % (n, radius(rels, "x", rhomax), radius(rels, "y", rhomax)), flush=True)
        sys.exit(0)
    for n in range(1, nmax + 1):
        print("n=%d  rho*(x)=%s  rho*(y)=%s  theorem: >= %d" % (n, radius(ak(n), "x", rhomax), radius(ak(n), "y", rhomax), max(0, (n-2)//2)), flush=True)
