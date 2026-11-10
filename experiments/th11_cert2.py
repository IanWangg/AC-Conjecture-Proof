#!/usr/bin/env python3
"""TH11: certificates (c, w) -> AK(3) for two killers w of <x,y|c> outside the classes of k_3 and its
mirror (research-th11, Theorem T10):
   th11_cw14_to_ak3.json : (xyxYYXy, yxxYXyX)  -> AK(3)   [state 146 of d_ak3_aut_invx.json, pulled back]
   th11_cq_to_ak3.json   : (xyxYYXy, YYYxyxyX) -> AK(3)   [D's second length-13 presentation Q, pulled back]
Built with research-i's i_transport.merge (Lemmas D2/D6 made explicit) from D's certificates.
Usage: python3 experiments/th11_cert2.py --selftest     (build + replay, writes nothing)
       python3 experiments/th11_cert2.py --write certificates
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import elementary_verify as ev
import i_transport as T
import th11_kc as K
ROOT = os.path.join(HERE, "..", "certificates")

def prefix(fname, step):
    cert = json.load(open(os.path.join(ROOT, fname)))
    st = list(K.states(cert))[step]
    c = {"format": "ordinary-ac-elementary-v1", "start": cert["start"], "target": list(st), "moves": cert["moves"][:step]}
    ev.replay(c)
    return c

def build():
    real = {g: json.load(open(os.path.join(ROOT, "d_ak3_aut_%s.json" % g))) for g in ("swap", "invx", "x_xy")}
    P0 = tuple(real["swap"]["start"])
    jobs = [("th11_cw14_to_ak3.json", prefix("d_ak3_aut_invx.json", 146), ("xyxYYXy", "yxxYXyX")),
            ("th11_cq_to_ak3.json", json.load(open(os.path.join(ROOT, "d_ak3_to_len13b.json"))), ("xyxYYXy", "YYYxyxyX"))]
    out = {}
    for name, s_cert, R in jobs:
        assert tuple(s_cert["start"]) == P0
        back, names = T.merge(P0, s_cert, real, R)
        back["description"] = ("TH11: (c, w) -> AK(3) for a killer w of <x,y|c> not conjugate to k_3 or its mirror "
                               "(J-hat = -6, N = 32); automorphism %s; experiments/th11_cert2.py" % "o".join(names))
        r = ev.replay(back)
        assert back["start"] == list(R) and r["endpoint"] == list(P0)
        assert K.classify(R[1])[1:] == (-6, 32)
        out[name] = (back, r)
    return out

if __name__ == "__main__":
    res = build()
    for name, (cert, r) in res.items():
        if "--write" in sys.argv:
            json.dump(cert, open(os.path.join(sys.argv[sys.argv.index("--write") + 1], name), "w"), indent=0)
        print(name, json.dumps(r))
    print("th11_cert2 self-test passed")
