"""Class coordinates of AK(3) from the repository's ordinary-AC certificates (research note H, Thm 1).

Every intermediate pair of an ordinary-AC certificate that starts at AK(3) = (xxxYYYY, xyxYXY)
(or at a pair certified equivalent to it) is AC-equivalent to AK(3).  By Theorem 1 of
research-h.md, for every coordinate r of such a pair, NO quotient of the one-relator group
F/<<r>> can obstruct AK(3).  This script replays the certificates with the repository verifier's
primitives (imported read-only), collects the cyclically reduced coordinates up to rotation and
inversion, and prints statistics and the shortest ones.

Usage: python3 experiments/h_class_coordinates.py [--selftest] [--show K]
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import elementary_verify as ev  # noqa: E402  (repository verifier, read-only)

AK3 = ["xxxYYYY", "xyxYXY"]


def cyc_reduce(w):
    w = ev.reduce(w)
    while len(w) >= 2 and w[0] == w[-1].swapcase():
        w = w[1:-1]
    return w


def canon(w):
    """canonical representative of a cyclic word up to rotation and inversion"""
    w = cyc_reduce(w)
    if not w:
        return ""
    cands = []
    for u in (w, ev.inverse(w)):
        cands.extend(u[i:] + u[:i] for i in range(len(u)))
    return min(cands)


def replay_states(cert):
    """yield every state of the certificate, using exactly the verifier's move semantics"""
    state = [ev.reduce(w) for w in cert["start"]]
    yield tuple(state)
    for mv in cert["moves"]:
        i = mv["i"]
        if mv["op"] == "invert":
            state[i] = ev.inverse(state[i])
        elif mv["op"] == "multiply":
            state[i] = ev.reduce(state[i] + state[mv["j"]])
        elif mv["op"] == "conjugate":
            g = mv["g"]
            state[i] = ev.reduce(g + state[i] + ev.inverse(g))
        else:
            raise ValueError("unknown op")
        yield tuple(state)


def collect():
    root = os.path.dirname(HERE)
    files = sorted(glob.glob(os.path.join(root, "certificates", "d_ak3_*.json")))
    files.append(os.path.join(root, "certificates", "ms3_to_ak3_exact.json"))
    coords, used = set(), []
    for f in files:
        with open(f) as fh:
            cert = json.load(fh)
        ev.replay(cert)  # full independent check first (raises on any error)
        ends = [ [ev.reduce(w) for w in cert["start"]], [ev.reduce(w) for w in cert["target"]] ]
        if AK3 not in ends and AK3[::-1] not in ends:
            continue  # only certificates with AK(3) as an exact endpoint
        used.append(os.path.basename(f))
        for st in replay_states(cert):
            for w in st:
                coords.add(canon(w))
    coords.discard("")
    return used, coords


def exps(w):
    return (w.count("x") - w.count("X"), w.count("y") - w.count("Y"))


def main():
    used, coords = collect()
    if "--selftest" in sys.argv:
        assert canon("xxxYYYY") in coords and canon("xyxYXY") in coords
        assert canon("XyyyxYYYY") in coords            # Miller-Schupp relator (BS(3,4) type)
        for w in coords:                                 # Theorem 1 needs primitive exponent vectors
            a, b = exps(w)
            from math import gcd
            assert gcd(abs(a), abs(b)) == 1, w
        print(f"selftest passed: {len(used)} certificates, {len(coords)} class coordinates, "
              f"all with primitive exponent vectors")
        return
    k = 25
    if "--show" in sys.argv:
        k = int(sys.argv[sys.argv.index("--show") + 1])
    by_len = {}
    for w in coords:
        by_len.setdefault(len(w), 0)
        by_len[len(w)] += 1
    print(json.dumps({"certificates": len(used), "distinct_cyclic_coordinates": len(coords),
                      "by_length": dict(sorted(by_len.items())[:20])}))
    for w in sorted(coords, key=lambda u: (len(u), u))[:k]:
        print(len(w), w, exps(w))


if __name__ == "__main__":
    main()
