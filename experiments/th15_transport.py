#!/usr/bin/env python3
"""TH15: constructive Lemma D2 / D6 -- transport, reversal and composition of strict
ordinary-AC certificates, giving certificates AK(n) -> phi(AK(n)) for phi any word in
s = swap, a = (x -> xY), A = a^-1 = (x -> xy).

  transport(moves, phi): letterwise image of an elementary certificate under phi in Aut(F2)
      (invert -> invert, multiply -> multiply, conjugate by g -> conjugate by the letters of
      phi(g)); it runs from red(phi(start)) to red(phi(target)).
  reverse(moves): the inverse certificate (multiply(i,j) -> invert j, multiply(i,j), invert j).
  chain(n, word): AK(n) -> red(g_1 g_2 ... g_k (AK(n))) as the concatenation of the base
      certificates for g_1, then g_1-transported g_2, ... (the induction in Lemma D6).

Named maps (verified on generators by this script; composition (fg)(w) = f(g(w))):
  swap = s;  x_xY = a;  x_xy = A;  y_yx = s A s;  y_yX = s a s;
  invy = a s A s a s  (= Inn_y o (y -> Y));   invx = s a s A s a  (= Inn_x o (x -> X)).

    python3 experiments/th15_transport.py --selftest
    python3 experiments/th15_transport.py --nielsen N [OUTDIR]     # all seven maps for AK(N)
    python3 experiments/th15_transport.py --named N NAME OUT.json  # one named map
    python3 experiments/th15_transport.py --batch 2 8
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import elementary_verify  # noqa: E402
import th15_aut_family as fam  # noqa: E402

red, inv, cyc, rots, INV = fam.red, fam.inv, fam.cyc, fam.rots, fam.INV

AUT = {"s": {"x": "y", "y": "x"}, "a": {"x": "xY", "y": "y"}, "A": {"x": "xy", "y": "y"}}
NAMED = {"swap": "s", "x_xY": "a", "x_xy": "A", "y_yx": "sAs", "y_yX": "sas",
         "invy": "asAsas", "invx": "sasAsa"}
DIRECT = {"swap": {"x": "y", "y": "x"}, "x_xY": {"x": "xY", "y": "y"}, "x_xy": {"x": "xy", "y": "y"},
          "y_yx": {"x": "x", "y": "yx"}, "y_yX": {"x": "x", "y": "yX"},
          "invy": {"x": "x", "y": "Y"}, "invx": {"x": "X", "y": "y"}}


def ap(phi, w):
    return red("".join(phi[c] if c in phi else inv(phi[INV[c]]) for c in w))


def word_aut(word):
    """The automorphism g_1 g_2 ... g_k as a dict (g_1 outermost)."""
    phi = {"x": "x", "y": "y"}
    for g in reversed(word):
        phi = {c: ap(AUT[g], phi[c]) for c in "xy"}
    return phi


def transport(moves, phi):
    out = []
    for m in moves:
        if m["op"] == "conjugate":
            for h in reversed(ap(phi, m["g"])):      # g r g^-1, g = h_1..h_k: h_k first
                out.append({"op": "conjugate", "i": m["i"], "g": h})
        else:
            out.append(dict(m))
    return out


def reverse(moves):
    out = []
    for m in reversed(moves):
        if m["op"] == "invert":
            out.append(dict(m))
        elif m["op"] == "conjugate":
            out.append({"op": "conjugate", "i": m["i"], "g": INV[m["g"]]})
        else:
            j = m["j"]
            out += [{"op": "invert", "i": j}, dict(m), {"op": "invert", "i": j}]
    return out


def run(state, moves):
    state = list(state)
    for m in moves:
        i = m["i"]
        if m["op"] == "invert":
            state[i] = inv(state[i])
        elif m["op"] == "multiply":
            state[i] = red(state[i] + state[m["j"]])
        else:
            state[i] = red(m["g"] + state[i] + INV[m["g"]])
    return state


_base = {}


def base(n, g):
    """Elementary moves AK(n) -> red(g(AK(n))) for g in 's', 'a', 'A'."""
    if (n, g) not in _base:
        if g == "A":
            mv = reverse(transport(base(n, "a"), AUT["A"]))
        else:
            mv = fam.certificate("swap" if g == "s" else "a", n)[0]["moves"]
        ak = [fam.p(n), fam.B]
        assert run(ak, mv) == [ap(AUT[g], w) for w in ak], (n, g)
        _base[(n, g)] = mv
    return _base[(n, g)]


def chain(n, word):
    moves, ak = [], [fam.p(n), fam.B]
    for i, g in enumerate(word):
        moves += transport(base(n, g), word_aut(word[:i]))
    assert run(ak, moves) == [ap(word_aut(word), w) for w in ak]
    return moves


def normalize(state, target):
    """Letter conjugations (and inversions if needed) taking state to the exact target tuple."""
    moves, state = [], list(state)
    for i in (0, 1):
        while len(state[i]) >= 2 and state[i][0] == INV[state[i][-1]]:
            g = INV[state[i][0]]
            moves.append({"op": "conjugate", "i": i, "g": g})
            state[i] = red(g + state[i] + INV[g])
        if target[i] not in rots(state[i]):
            assert target[i] in rots(inv(state[i])), (state, target)
            moves.append({"op": "invert", "i": i})
            state[i] = inv(state[i])
        while state[i] != target[i]:
            g = INV[state[i][0]]
            moves.append({"op": "conjugate", "i": i, "g": g})
            state[i] = red(g + state[i] + INV[g])
    return moves


def named_certificate(n, name):
    ak = [fam.p(n), fam.B]
    target = [cyc(ap(DIRECT[name], w)) for w in ak]
    moves = chain(n, NAMED[name])
    moves += normalize(run(ak, moves), target)
    cert = {"format": "ordinary-ac-elementary-v1", "start": ak, "target": target, "moves": moves,
            "description": f"AK({n}) -> phi(AK({n})) exactly (cyclically reduced), phi = {name} = word "
                           f"'{NAMED[name]}' in s = swap, a = (x->xY), A = a^-1; composed by letterwise "
                           f"transport (Lemma D2) from the closed-form paths of research-th15.md."}
    r = elementary_verify.replay(cert)
    assert r["endpoint"] == target
    return cert, r


def check_identities():
    for name, word in NAMED.items():
        phi, psi = word_aut(word), DIRECT[name]
        # equal up to an inner automorphism: phi(c) = h psi(c) h^-1 for a common h
        hs = [h for h in ("", "x", "X", "y", "Y") if all(red(h + psi[c] + inv(h)) == phi[c] for c in "xy")]
        assert hs, (name, phi, psi)
    return True


def main():
    args = sys.argv[1:]
    if args[:1] == ["--selftest"]:
        check_identities()
        for n in (2, 3):
            for name in NAMED:
                named_certificate(n, name)
        print("selftest passed: 7 named maps = words in s, a, A up to inner automorphisms; "
              "composed certificates for n = 2, 3 replay to the exact targets")
    elif args[:1] == ["--nielsen"]:
        n = int(args[1])
        for name in NAMED:
            cert, r = named_certificate(n, name)
            if len(args) > 2:
                with open(os.path.join(args[2], f"th15_ak{n}_aut_{name}.json"), "w") as f:
                    json.dump(cert, f)
            print(f"n={n} {name}: {r['moves']} moves, peak {r['peak_total_length']}, endpoint {tuple(r['endpoint'])}")
    elif args[:1] == ["--named"]:
        n, name, out = int(args[1]), args[2], args[3]
        cert, r = named_certificate(n, name)
        with open(out, "w") as f:
            json.dump(cert, f)
        print(f"n={n} {name}: {r['moves']} moves, peak {r['peak_total_length']}, wrote {out}")
    elif args[:1] == ["--batch"]:
        for n in range(int(args[1]), int(args[2]) + 1):
            res = [named_certificate(n, name)[1] for name in NAMED]
            print(f"n={n}: all 7 maps verified; moves {[r['moves'] for r in res]}, "
                  f"peaks {[r['peak_total_length'] for r in res]}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
