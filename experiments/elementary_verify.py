"""Strict ordinary-AC certificate replay, Python standard library only.

Words: x/y and X/Y (uppercase denotes inverse). Accepted primitives:
invert(i), multiply(i,j) on the RIGHT, conjugate(i,g) = g r_i g^-1
with g one signed generator. All indices are zero-based. No quotient,
rotation, basis-change, stabilization, or endpoint normalization is implicit.
"""
import json
import sys

LETTERS = frozenset("xXyY")


def reduce(word):
    if not isinstance(word, str) or not set(word) <= LETTERS:
        raise ValueError("word must use x,X,y,Y")
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
    if certificate.get("format") != "ordinary-ac-elementary-v1":
        raise ValueError("unsupported certificate format")
    start, target = certificate["start"], certificate["target"]
    if not isinstance(start, list) or len(start) != 2:
        raise ValueError("rank-two start required")
    if not isinstance(target, list) or len(target) != 2:
        raise ValueError("rank-two target required")
    state = [reduce(w) for w in start]
    target = [reduce(w) for w in target]
    peak = sum(map(len, state))
    for step, move in enumerate(certificate["moves"], 1):
        op = move.get("op")
        i = move.get("i")
        if type(i) is not int or i not in (0, 1):
            raise ValueError(f"step {step}: invalid index")
        if op == "invert" and set(move) == {"op", "i"}:
            state[i] = inverse(state[i])
        elif op == "multiply" and set(move) == {"op", "i", "j"}:
            j = move["j"]
            if type(j) is not int or j not in (0, 1) or j == i:
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
    return {"moves": len(certificate["moves"]), "peak_total_length": peak,
            "endpoint": state}


def selftest():
    cert = {"format": "ordinary-ac-elementary-v1", "start": ["xy", "y"],
            "target": ["x", "y"], "moves": [
                {"op": "invert", "i": 1},
                {"op": "multiply", "i": 0, "j": 1},
                {"op": "invert", "i": 1}]}
    assert replay(cert)["endpoint"] == ["x", "y"]
    for moves, target in [
        ([], ["x", "y"]),
        ([{"op": "multiply", "i": 0, "j": 0}], ["xyxy", "y"]),
        ([{"op": "basis_change", "i": 0}], ["xy", "y"]),
        ([{"op": "conjugate", "i": 0, "g": "xy"}], ["xy", "y"]),
        ([{"op": "invert", "i": True}], ["xy", "Y"]),
    ]:
        try:
            replay(dict(cert, moves=moves, target=target))
        except ValueError:
            pass
        else:
            raise AssertionError("invalid certificate accepted")
    print("self-test: exact replay and five negative controls passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        for path in sys.argv[1:]:
            with open(path) as f:
                print(json.dumps({"path": path, **replay(json.load(f))}, sort_keys=True))
