"""TH14: strict replay of rank-3 (one stabilization) AC certificates.  Standard library only.

Format "stable1-ac-elementary-rank3-v1": words over x,y,z with X,Y,Z the inverses; start and target are
lists of exactly three words; primitives (zero-based indices, exactly as in elementary_verify.py):
  invert(i); multiply(i,j) on the RIGHT (j != i); conjugate(i,g) = g r_i g^-1 with g ONE signed generator.
No stabilization/destabilization, rotation, basis change or normalization is implicit.  A certificate proves
that the two triples are ordinary-AC-equivalent IN RANK 3.  If start = [r1,r2,"z"] and target = [s1,s2,"z"]
with r_i, s_i words in x,y only, it proves that (r1,r2) and (s1,s2) are STABLY AC-equivalent with one
stabilization (reported as "stable1": true).  It never proves an ordinary rank-2 AC equivalence.
Usage: python3 experiments/th14_verify3.py CERT.json ...   |   --selftest
"""
import json
import sys

LETTERS = frozenset("xXyYzZ")


def reduce(word):
    if not isinstance(word, str) or not set(word) <= LETTERS:
        raise ValueError("word must use x,X,y,Y,z,Z")
    out = []
    for c in word:
        if out and out[-1] == c.swapcase():
            out.pop()
        else:
            out.append(c)
    return "".join(out)


def inverse(word):
    return word.swapcase()[::-1]


def replay(certificate):
    if certificate.get("format") != "stable1-ac-elementary-rank3-v1":
        raise ValueError("unsupported certificate format")
    start, target = certificate["start"], certificate["target"]
    for t in (start, target):
        if not isinstance(t, list) or len(t) != 3:
            raise ValueError("rank-three start and target required")
    state = [reduce(w) for w in start]
    target = [reduce(w) for w in target]
    if state != start or target != certificate["target"]:
        raise ValueError("start and target must be freely reduced")
    peak = sum(map(len, state))
    for step, move in enumerate(certificate["moves"], 1):
        op, i = move.get("op"), move.get("i")
        if type(i) is not int or i not in (0, 1, 2):
            raise ValueError(f"step {step}: invalid index")
        if op == "invert" and set(move) == {"op", "i"}:
            state[i] = inverse(state[i])
        elif op == "multiply" and set(move) == {"op", "i", "j"}:
            j = move["j"]
            if type(j) is not int or j not in (0, 1, 2) or j == i:
                raise ValueError(f"step {step}: invalid donor index")
            state[i] = reduce(state[i] + state[j])
        elif op == "conjugate" and set(move) == {"op", "i", "g"}:
            g = move["g"]
            if not isinstance(g, str) or len(g) != 1 or g not in LETTERS:
                raise ValueError(f"step {step}: conjugator must be one signed generator")
            state[i] = reduce(g + state[i] + inverse(g))
        else:
            raise ValueError(f"step {step}: unknown or malformed primitive")
        peak = max(peak, sum(map(len, state)))
    if state != target:
        raise ValueError(f"endpoint mismatch: {state!r} != {target!r}")
    xy = frozenset("xXyY")
    stable1 = (start[2] == "z" and target[2] == "z" and all(set(w) <= xy for w in start[:2] + target[:2]))
    return {"moves": len(certificate["moves"]), "peak_total_length": peak, "endpoint": state,
            "stable1": stable1}


def selftest():
    fmt = "stable1-ac-elementary-rank3-v1"
    # (x, y, z x) -> (x, y, z): multiply by x^-1
    cert = {"format": fmt, "start": ["x", "y", "zx"], "target": ["x", "y", "z"], "moves": [
        {"op": "invert", "i": 0}, {"op": "multiply", "i": 2, "j": 0}, {"op": "invert", "i": 0}]}
    r = replay(cert)
    assert r["endpoint"] == ["x", "y", "z"] and r["stable1"] is False
    # the transposition (x z) on the trivial presentation: (x,y,z) -> (z,y,x)
    moves = [{"op": "invert", "i": 0}, {"op": "multiply", "i": 2, "j": 0}, {"op": "invert", "i": 0},   # z -> zX
             {"op": "conjugate", "i": 2, "g": "X"}, {"op": "multiply", "i": 0, "j": 2},                # x -> x.Xz = z
             {"op": "conjugate", "i": 2, "g": "x"},                                                   # back to zX
             {"op": "invert", "i": 0}, {"op": "conjugate", "i": 2, "g": "Z"},                          # Xz ; relator0 = Z
             {"op": "multiply", "i": 2, "j": 0}, {"op": "invert", "i": 0}, {"op": "invert", "i": 2}]   # X -> x
    assert replay({"format": fmt, "start": ["x", "y", "z"], "target": ["z", "y", "x"],
                   "moves": moves})["endpoint"] == ["z", "y", "x"]
    bad = [
        dict(cert, moves=[]),                                                # endpoint mismatch
        dict(cert, moves=[{"op": "multiply", "i": 2, "j": 2}]),              # self-multiplication
        dict(cert, moves=[{"op": "conjugate", "i": 2, "g": "xy"}]),          # word conjugator
        dict(cert, moves=[{"op": "stabilize", "i": 2}]),                     # unknown primitive
        dict(cert, moves=[{"op": "invert", "i": True}]),                     # bool index
        dict(cert, start=["x", "y"], moves=[]),                              # wrong rank
        dict(cert, start=["xX", "y", "zx"]),                                 # unreduced start
        dict(cert, format="ordinary-ac-elementary-v1"),                      # wrong format
        dict(cert, start=["x", "y", "zxw"]),                                 # bad letter
    ]
    for c in bad:
        try:
            replay(c)
        except (ValueError, KeyError):
            pass
        else:
            raise AssertionError("invalid certificate accepted")
    print("self-test: two exact replays and nine negative controls passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        for path in sys.argv[1:]:
            with open(path) as f:
                print(json.dumps({"path": path, **replay(json.load(f))}, sort_keys=True))
