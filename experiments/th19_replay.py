"""TH19: second, independent replay of ordinary-ac-elementary-v1 certificates (own 20 lines; same primitive semantics as
experiments/elementary_verify.py: invert(i); multiply(i,j): r_i <- r_i r_j; conjugate(i,g): r_i <- g r_i g^-1, g one letter),
with optional chaining: the target of each file must equal the start of the next."""
import json, sys
def red(w):
    out = []
    for c in w:
        if out and out[-1] == c.swapcase(): out.pop()
        else: out.append(c)
    return out
def replay(path):
    d = json.load(open(path)); assert d["format"] == "ordinary-ac-elementary-v1"
    st = [red(w) for w in d["start"]]; peak = len(st[0]) + len(st[1])
    for mv in d["moves"]:
        i = mv["i"]; assert i in (0, 1)
        if mv["op"] == "invert": st[i] = [c.swapcase() for c in reversed(st[i])]
        elif mv["op"] == "multiply":
            j = mv["j"]; assert j == 1 - i; st[i] = red(st[i] + st[j])
        elif mv["op"] == "conjugate":
            g = mv["g"]; assert len(g) == 1 and g in "xXyY"; st[i] = red([g] + st[i] + [g.swapcase()])
        else: raise ValueError(mv)
        peak = max(peak, len(st[0]) + len(st[1]))
    end = ["".join(w) for w in st]
    assert end == ["".join(red(w)) for w in d["target"]], (end, d["target"])
    return d["start"], end, len(d["moves"]), peak
prev = None
for p in sys.argv[1:]:
    s, e, n, pk = replay(p)
    chain = "" if prev is None else ("  [chains with previous: %s]" % (prev == s))
    print(f"{p}: {s} -> {e}, {n} moves, peak {pk}{chain}")
    prev = e
