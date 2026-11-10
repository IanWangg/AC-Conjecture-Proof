#!/usr/bin/env python3
"""TH11: certificate P_3 = (c, k_3) -> theta0(P_3) = (c, XXXYxyxy), theta0 = (x->X, y->yx).

Construction (research-d Lemmas D2/D6, tools of research-i):
   P_3 -> AK(3)                 reverse of K's certificate k_ak3_to_p3.json
       -> theta0(AK(3))         D's realization certificates (invx, x_xy, swap), transported
       -> theta0(P_3)           K's certificate transported letterwise by theta0
       -> (c, cyc theta0(k_3))  rotations / inversion (theta0(c) is a conjugate of c^-1)
Usage: python3 experiments/th11_cert.py --selftest        (builds and replays, writes nothing)
       python3 experiments/th11_cert.py --write certificates
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import elementary_verify as ev
import i_transport as T
from i_words import red, cyc, subst

ROOT = os.path.join(HERE, "..", "certificates")
C, K3 = "xyxYYXy", "xxxYXyy"
THETA = ["invx", "y_yX"]                      # compose: invx(y_yX(w)):  x -> X, y -> yx

def build():
    real = {g: json.load(open(os.path.join(ROOT, "d_ak3_aut_%s.json" % g))) for g in ("swap", "invx", "x_xy")}
    kcert = json.load(open(os.path.join(ROOT, "k_ak3_to_p3.json")))
    P0 = tuple(real["swap"]["start"])
    assert tuple(kcert["start"]) == P0 and kcert["target"] == [C, K3]
    img = T.compose(THETA)
    assert img == {"x": "X", "y": "yx"}, img
    gens = T.expand(THETA)
    assert T.compose(gens) == img
    R = [C, cyc(subst(K3, img))]
    assert R[1] == "XXXYxyxy", R
    assert cyc(subst(C, img)) in [(C.swapcase()[::-1])[i:] + (C.swapcase()[::-1])[:i] for i in range(7)]
    c = T.realize(P0, gens, real)                               # AK(3) -> ~theta0(AK(3))
    T.glue(c, [red(subst(w, img)) for w in kcert["start"]])
    T.apply_moves(c, kcert["moves"], img)                       # -> theta0(P_3)
    T.glue(c, R)                                                # -> R exactly
    fwd = c.as_json(list(R)); ev.replay(fwd)
    first = {"format": "ordinary-ac-elementary-v1", "start": [C, K3], "target": list(P0),
             "moves": T.reverse_moves(kcert["start"], kcert["moves"])}
    assert ev.replay(first)["endpoint"] == list(P0)
    cert = T.concat(first, fwd)
    cert["description"] = ("TH11: P_3 = (c,k_3) -> (c, cyc theta0(k_3)), theta0 = (x->X, y->yx); the two killers are "
                           "not conjugate in <x,y|c> (kappa invariant); built by experiments/th11_cert.py from "
                           "k_ak3_to_p3.json and d_ak3_aut_{swap,invx,x_xy}.json")
    return cert

if __name__ == "__main__":
    cert = build()
    r = ev.replay(cert)
    assert r["endpoint"] == [C, "XXXYxyxy"] and cert["start"] == [C, K3]
    if "--write" in sys.argv:
        out = os.path.join(sys.argv[sys.argv.index("--write") + 1], "th11_p3_to_theta0_p3.json")
        json.dump(cert, open(out, "w"), indent=0)
        print("wrote", out)
    print("th11_cert self-test passed:", json.dumps(r))
