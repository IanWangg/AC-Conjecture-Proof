#!/usr/bin/env python3
"""TH20 independent checks for TH16 (own BS conjugacy th20_bs, own torus invariant).
(A) Theorem A, (P,Q) = (3,4),(4,3),(4,5),(5,4): cyclically reduced words of length <= 7 conjugate to w_i^{+-1};
(B) Theorem B, n = 3,4: cyclically reduced words of length <= 2n+3 conjugate to m_n^{+-1} in G_{w_1}, G_{w_2};
(C) T6: the second relators of D's 34 benchmark presentations fall into the two BS(3,4)-classes of w_1, w_2;
(D) Prop. D: m_n ~ p_n in B = F/<<b>>, b ~ w_1 in BS(n,n+1)."""
import sys, glob, json
sys.dont_write_bytecode = True
from th20_lib import red, inv, cyc, aut, torus_inv, conj
import th20_bs as BS
W1, W2 = "XYxxY", "YXXYx"
def orb(w):
    w = cyc(w); return {u[i:] + u[:i] for u in (w, inv(w)) for i in range(len(u))}
def words(L):
    def rec(pre):
        if len(pre) == L:
            if pre[0] != pre[-1].swapcase(): yield pre
            return
        for c in "xXyY":
            if not pre or pre[-1] != c.swapcase(): yield from rec(pre + c)
    yield from rec("")
for (P, Q) in ((3, 4), (4, 3), (4, 5), (5, 4)):
    for name, w in (("w1", W1), ("w2", W2)):
        out = []
        for L in range(1, 8):
            hits = [u for u in words(L) if abs(u.count("x") - u.count("X")) == 1 and BS.conj_pm(u, w, P, Q)]
            out.append("L=%d:%d%s" % (L, len(hits), "" if L != 5 else ("(=Orb)" if set(hits) == orb(w) else "(NOT Orb!)")))
        print("(A) BS(%d,%d) %s:" % (P, Q, name), " ".join(out))
m = lambda n: "X" + "y" * n + "x" + "Y" * (n + 1); mp = lambda n: "X" + "y" * (n + 1) + "x" + "Y" * n
# G_{w1} = <x,t | x^3 = t^2>, t = yx  (y = tX);  G_{w2}: iota-image (y -> Y)
TH1 = {"x": "x", "y": "yX"}                    # word in (x,y) -> word in (x,t), t written y
IOTA = {"x": "x", "y": "Y"}
assert torus_inv(aut(TH1, W1), 3, -2) == torus_inv("", 3, -2)
for n in (3, 4):
    for name, pre in (("w1", lambda u: u), ("w2", lambda u: aut(IOTA, u))):
        cls = lambda u: torus_inv(aut(TH1, pre(u)), 3, -2)
        tgt = {cls(m(n)), cls(inv(m(n)))}; res = []
        for L in range(1, 2 * n + 4):
            hits = [u for u in words(L) if abs(u.count("y") - u.count("Y")) % 2 == 1 and cls(u) in tgt]
            res.append((L, len(hits), set(hits)))
        ok = all(c == 0 for L, c, _ in res[:-1]) and res[-1][2] == orb(m(n)) | orb(mp(n))
        print("(B) n=%d G_%s: words conjugate to m_n^+-1: none of length < %d; at length %d: %d words = Orb(m_n) u Orb(m_n'): %s" % (n, name, 2 * n + 3, 2 * n + 3, res[-1][1], ok))
cnt = {"w1": 0, "w2": 0, "other": 0}; first = set()
for f in sorted(glob.glob("../certificates/d_ak3_to_ms*.json")):
    t = json.load(open(f))["target"]
    r = [w for w in t if conj(w, m(3)) or conj(w, inv(m(3)))]; s = [w for w in t if w not in r]
    assert len(r) == 1 and len(s) == 1, (f, t)
    k = "w1" if BS.conj_pm(s[0], W1, 3, 4) else "w2" if BS.conj_pm(s[0], W2, 3, 4) else "other"; cnt[k] += 1
print("(C) 34 benchmark targets (first relator ~ m_3^+-1 in F):", cnt, "| w1 ~ w2^+-1 in BS(3,4):", BS.conj_pm(W1, W2, 3, 4))
PHI = {"x": "xY", "y": "yyX"}
for n in range(1, 9):
    assert torus_inv(aut(PHI, m(n)), 2, -3) == torus_inv(aut(PHI, "x" * n + "Y" * (n + 1)), 2, -3)
    assert BS.conj_bs("xyxYXY", W1, n, n + 1) or n < 2
print("(D) m_n ~ p_n in B (n <= 8); b ~ w_1 in BS(n,n+1) (2 <= n <= 8)")
