"""TH19 independent replay of TH06's quotient-only 8-move records (certificates/th06_*_8move_class*.json) in N_c.
Own truncated Magnus algebra Z<X,Y>/(deg > c) and own standard factorization of Lyndon words; nothing is imported from
th06_proconj.py.  Conventions read from the note: g^h = h^-1 g h, [g,h] = g^-1 h^-1 g h, C(w) = [C(u), C(v)] for the standard
factorization w = uv (v the longest proper Lyndon suffix), g_i = product of C(w)^e in list order; Nielsen codes of E:
3,4: u0 <- u0 u1^(+-1); 5,6: u1 <- u1 u0^(+-1).  The 8 instructions must carry (x,y) to the normalized pair V mod gamma_{c+1},
where V is obtained from the presentation by the Nielsen instructions.  QUOTIENT-ONLY: this is not an AC statement in F."""
import json, sys, ast
sys.path.insert(0, "experiments")
from th19_lib import red, inv
def run(path):
    d = json.load(open(path)); c = d["class"]
    def mul(A, B):
        out = {}
        for m1, a in A.items():
            r = c - len(m1)
            for m2, b in B.items():
                if len(m2) <= r: out[m1+m2] = out.get(m1+m2, 0) + a*b
        return {m: v for m, v in out.items() if v}
    ONE = {(): 1}
    def ainv(A):                      # A = 1 + n, n nilpotent: sum (-n)^k
        n = dict(A); n[()] = n.get((), 0) - 1; n = {m: -v for m, v in n.items() if v}
        R = dict(ONE); P = dict(ONE)
        for _ in range(c):
            P = mul(P, n)
            if not P: break
            for m, v in P.items(): R[m] = R.get(m, 0) + v
        return {m: v for m, v in R.items() if v}
    LET = {"x": {(): 1, (0,): 1}, "y": {(): 1, (1,): 1}}; LET["X"] = ainv(LET["x"]); LET["Y"] = ainv(LET["y"])
    def word(w):
        R = dict(ONE)
        for ch in w: R = mul(R, LET[ch])
        return R
    def pw(A, e):
        if e < 0: A, e = ainv(A), -e
        R = dict(ONE)
        while e:
            if e & 1: R = mul(R, A)
            A = mul(A, A); e >>= 1
        return R
    def lyndon(w): return all(w < w[i:] for i in range(1, len(w)))
    def C(w):                         # image of the commutator of the standard bracketing
        if len(w) == 1: return LET[w]
        i = next(i for i in range(1, len(w)) if lyndon(w[i:]))     # longest proper Lyndon suffix
        a, b = C(w[:i]), C(w[i:])
        return mul(mul(ainv(a), ainv(b)), mul(a, b))
    conj = lambda A, G: mul(mul(ainv(G), A), G)
    U = list(d["presentation"])
    for i in d["nielsen"]:
        a, b = U
        U = [(inv(a), b), (a, inv(b)), (b, a), (red(a+b), b), (red(a+inv(b)), b), (a, red(b+a)), (a, red(b+inv(a)))][i]
        U = list(U)
    assert U == list(d["normalized"]), "Nielsen part"
    conjs = d["conjugators"]
    if isinstance(conjs, str): conjs = ast.literal_eval(conjs)
    gs = []
    for rec in conjs:
        g = dict(ONE)
        for w, e in rec:
            assert lyndon(w)
            g = mul(g, pw(C(w), e))
        gs.append(g)
    u0, u1 = LET["x"], LET["y"]
    u0 = mul(conj(u0, gs[0]), u1); u0 = mul(conj(u0, gs[1]), ainv(u1))
    u1 = mul(conj(u1, gs[2]), u0); u1 = mul(conj(u1, gs[3]), ainv(u0))
    ok = (u0 == word(U[0]) and u1 == word(U[1]))
    print(f"{path}: class {c}, presentation {d['presentation']}, Nielsen part reproduced, 8-move scheme reaches the normalized pair mod gamma_{c+1}: {ok}")
for p in sys.argv[1:]: run(p)
