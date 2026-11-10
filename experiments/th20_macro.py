#!/usr/bin/env python3
"""TH20: exact replay of *macro* AC sequences on tuples of free words of any rank
(letters x,y,z and inverses X,Y,Z).  Every macro is a composite of ordinary AC moves:
  ("inv", i)            r_i <- r_i^-1
  ("mul", i, j, e, g)   r_i <- r_i * g r_j^e g^-1     (e = +-1, g any word; i != j)
  ("lmul", i, j, e, g)  r_i <- g r_j^e g^-1 * r_i
  ("conj", i, g)        r_i <- g r_i g^-1
  ("rot", i, k)         r_i <- rotate left by k letters (conjugation), after cyclic reduction
  ("swap", i, j)
No automorphism, no stabilization, no quotient rewriting.  Also: strict replay of
ordinary-ac-elementary-v1-style move lists in any rank (replay_strict)."""
import sys
sys.dont_write_bytecode = True
from th20_lib import red, inv, cyc, conj

def run(state, macros, trace=False):
    s = [red(w) for w in state]
    for m in macros:
        op = m[0]
        if op == "inv": s[m[1]] = inv(s[m[1]])
        elif op in ("mul", "lmul"):
            _, i, j, e, g = m
            assert i != j and e in (1, -1)
            d = red(g + (s[j] if e == 1 else inv(s[j])) + inv(g))
            s[i] = red(s[i] + d) if op == "mul" else red(d + s[i])
        elif op == "conj": s[m[1]] = red(m[2] + s[m[1]] + inv(m[2]))
        elif op == "rot":
            w = cyc(s[m[1]]); k = m[2] % max(1, len(w)); s[m[1]] = w[k:] + w[:k]
        elif op == "swap": s[m[1]], s[m[2]] = s[m[2]], s[m[1]]
        else: raise ValueError(m)
        if trace: print(m, s)
    return s

def same_up_to_conj(s, t):
    """coordinatewise conjugate (no inversion, no permutation)"""
    return len(s) == len(t) and all(conj(a, b) for a, b in zip(s, t))

def replay_strict(start, moves, target=None):
    s = [red(w) for w in start]; n = len(s)
    for k, m in enumerate(moves, 1):
        op, i = m["op"], m["i"]
        assert type(i) is int and 0 <= i < n, k
        if op == "invert": s[i] = inv(s[i])
        elif op == "multiply":
            j = m["j"]; assert type(j) is int and 0 <= j < n and j != i, k
            s[i] = red(s[i] + s[j])
        elif op == "conjugate":
            g = m["g"]; assert isinstance(g, str) and len(g) == 1 and g in "xXyYzZ", k
            s[i] = red(g + s[i] + inv(g))
        else: raise ValueError((k, m))
    if target is not None: assert s == [red(w) for w in target], (s, target)
    return s

if __name__ == "__main__":
    # self-test: D's interchange composite (a,b)->(b,a) and AK(3) -> swap by ("swap")
    a, b = "xxxYYYY", "xyxYXY"
    s = run([a, b], [("mul", 0, 1, 1, ""), ("inv", 1), ("mul", 1, 0, 1, ""), ("inv", 1)])
    assert s[1] == inv(red(inv(b) + red(a + b)))
    assert same_up_to_conj(run([a, b], [("rot", 0, 3)]), [a, b])
    assert replay_strict(["xy", "y"], [{"op": "invert", "i": 1}, {"op": "multiply", "i": 0, "j": 1}, {"op": "invert", "i": 1}], ["x", "y"]) == ["x", "y"]
    assert replay_strict(["xz", "y", "z"], [{"op": "invert", "i": 2}, {"op": "multiply", "i": 0, "j": 2}, {"op": "invert", "i": 2}], ["x", "y", "z"])
    print("th20_macro self-test passed")
