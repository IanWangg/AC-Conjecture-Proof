"""TH19 checks of TH02.
(a) every certificates/th02_*.json whose description names an automorphism '(x -> P, y -> Q)': the target is exactly
    (h(start[0]), h(start[1])), (h(x), h(y)) is a basis of F2 (greedy Nielsen reduction), and the matrix/trace of h.
(b) Theorem 1 identities for the hidden reflection, for random bases (u,v) and n.
(c) bounded check of Prop. 7: automorphisms in a BFS ball fixing the cyclic word x^p y^q up to inversion."""
import sys, json, glob, re, random
sys.path.insert(0, "experiments")
from th19_lib import *
def nielsen_basis(a, b):
    a, b = red(a), red(b)
    while True:
        best = None
        for (na, nb) in [(red(a+b), b), (red(a+inv(b)), b), (red(b+a), b), (red(inv(b)+a), b),
                         (a, red(b+a)), (a, red(b+inv(a))), (a, red(a+b)), (a, red(inv(a)+b))]:
            if len(na) + len(nb) < len(a) + len(b):
                if best is None or len(na) + len(nb) < len(best[0]) + len(best[1]): best = (na, nb)
        if best is None: break
        a, b = best
    return {a.lower(), b.lower()} == {"x", "y"} and len(a) == len(b) == 1
for f in sorted(glob.glob("certificates/th02_*.json")):
    d = json.load(open(f)); m = re.search(r"\(x -> (\w+), y -> (\w+)\)", d.get("description", ""))
    name = f.split("/")[-1]
    if not m:
        print(f"(a) {name}: no automorphism named; start {d['start']} -> target {d['target']}"); continue
    h = {"x": m.group(1), "y": m.group(2)}
    img = [subst(w, h) for w in d["start"]]
    ex, ey = expo(h["x"]), expo(h["y"])
    M = ((ex[0], ey[0]), (ex[1], ey[1]))     # columns = images of x, y
    print(f"(a) {name}: target == h(start): {img == [red(w) for w in d['target']]}; basis: {nielsen_basis(h['x'], h['y'])};"
          f" matrix {M}, det {M[0][0]*M[1][1]-M[0][1]*M[1][0]}, trace {M[0][0]+M[1][1]}; start {d['start']}")
random.seed(3)
gens = [{"x": "xy", "y": "y"}, {"x": "xY", "y": "y"}, {"x": "x", "y": "yx"}, {"x": "x", "y": "yX"}, {"x": "y", "y": "x"}, {"x": "X", "y": "y"}]
for _ in range(300):
    u, v = "x", "y"
    for _ in range(random.randint(0, 5)):
        g = random.choice(gens); u, v = subst(g["x"], {"x": u, "y": v}), subst(g["y"], {"x": u, "y": v})
    n = random.choice([-7, -5, -3, 3, 5, 7, 9]); vn = v*n if n > 0 else inv(v)*(-n)
    rho = red(u + u + vn)
    bu, bv = red(inv(u) + inv(vn)), v            # beta(u), beta(v); as a substitution on words in u,v
    beta = lambda w: red("".join({"x": bu, "X": inv(bu), "y": bv, "Y": inv(bv)}[c] for c in w))   # w is a word in (u,v) coded as x,y
    assert red(bu + inv(u)) == red(u + inv(u)*2 + inv(rho) + u*2 + inv(u))      # beta(u) u^-1 = u (u^-2 rho^-1 u^2) u^-1: a conjugate of rho^-1
    assert beta("xx" + ("y"*n if n > 0 else "Y"*(-n))) == red(inv(u) + inv(rho) + u)   # beta(rho) = u^-1 rho^-1 u
print("(b) Theorem 1 identities (beta(u)u^-1 conjugate of rho^-1; beta(rho) = u^-1 rho^-1 u) hold for 300 random bases")
ball = {("x", "y")}; fr = [("x", "y")]
for depth in range(7):
    nx = []
    for (a, b) in fr:
        for g in gens:
            img = (subst(g["x"], {"x": a, "y": b}), subst(g["y"], {"x": a, "y": b}))
            if img not in ball and len(img[0]) + len(img[1]) <= 30: ball.add(img); nx.append(img)
    fr = nx
for (p, q) in [(3, 4), (3, 5), (4, 5), (3, -4), (2, 3), (2, 5), (2, -5), (2, 7)]:
    R = "x"*p + ("y"*q if q > 0 else "Y"*(-q)); c = canon(R); S = set()
    for (a, b) in ball:
        if canon(subst(R, {"x": a, "y": b})) == c:
            ea, eb = expo(a), expo(b); S.add(((ea[0], eb[0]), (ea[1], eb[1])))
    print(f"(c) x^{p} y^{q}: matrices of automorphisms in the ball ({len(ball)}) fixing the cyclic word up to inversion: {sorted(S)}")
