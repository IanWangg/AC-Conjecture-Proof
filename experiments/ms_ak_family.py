#!/usr/bin/env python3
"""Parameterized ordinary AC certificate MS(n,YxxY) ~ AK(n), n >= 2.

Word alphabet: x=1, y=2, X=-1, Y=-2.  No dependencies.
The n=3 packaged ledger is from Carreras, arXiv:2607.23611,
cert_ms3_yinvx2yinv_equiv_ak3.json.  The uniform extension and
this implementation were independently developed in this investigation.
"""
import argparse
import copy
import json
from pathlib import Path


def reduce_word(word):
    out = []
    for letter in word:
        if type(letter) is not int or letter not in (-2, -1, 1, 2):
            raise ValueError("Invalid letter")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse(word):
    return [-letter for letter in reversed(word)]


def check_state(state):
    if not isinstance(state, list) or len(state) != 2:
        raise ValueError("Expected two relators")
    if any(not isinstance(w, list) or reduce_word(w) != w for w in state):
        raise ValueError("Relators must be freely reduced")


def elementary_step(state, move):
    """Accept only inversion, multiplication, single-letter conjugation."""
    state = copy.deepcopy(state)
    if not isinstance(move, list) or len(move) < 2:
        raise ValueError("Malformed move")
    op, i, *args = move
    if type(i) is not int or i not in (0, 1):
        raise ValueError("Bad relator index")
    if op == "invert" and not args:
        state[i] = inverse(state[i])
    elif op == "mul" and len(args) == 2:
        j, sign = args
        if type(j) is not int or j not in (0, 1) or i == j:
            raise ValueError("Bad multiplier index")
        if type(sign) is not int or sign not in (-1, 1):
            raise ValueError("Bad multiplier sign")
        multiplier = state[j] if sign == 1 else inverse(state[j])
        state[i] = reduce_word(state[i] + multiplier)
    elif op == "conj" and len(args) == 1:
        g = args[0]
        if type(g) is not int or g not in (-2, -1, 1, 2):
            raise ValueError("Bad conjugating letter")
        state[i] = reduce_word([g] + state[i] + [-g])
    else:
        raise ValueError("Unknown/malformed elementary move")
    return state


def compile_moves(initial, packaged):
    """Expand rotations and negative multiplications to strict AC1--AC3."""
    state = copy.deepcopy(initial)
    expanded = []
    packaged_peak = sum(map(len, state))
    for move in packaged:
        op, i, *args = move
        if op == "cycle":
            if len(args) != 1 or not state[i]:
                raise ValueError("Invalid rotation")
            k = args[0] % len(state[i])
            word = state[i][:]
            wanted = reduce_word(word[k:] + word[:k])
            # u^-1 (uv) u = vu; alternatively v (uv) v^-1 = vu.
            letters = [-g for g in word[:k]]
            alternative = list(reversed(word[k:]))
            if len(alternative) < len(letters):
                letters = alternative
            replacements = [["conj", i, g] for g in letters]
        elif op == "mul" and args[-1] == -1:
            j = args[0]
            wanted = elementary_step(state, move)[i]
            replacements = [["invert", j], ["mul", i, j, 1],
                            ["invert", j]]
        else:
            wanted = elementary_step(state, move)[i]
            replacements = [move]
        for elementary in replacements:
            state = elementary_step(state, elementary)
            expanded.append(elementary)
        if state[i] != wanted:
            raise AssertionError("Compilation mismatch")
        packaged_peak = max(packaged_peak, sum(map(len, state)))
    return expanded, state, packaged_peak


def cyclic_normal_form(word):
    word = word[:]
    while len(word) >= 2 and word[0] == -word[-1]:
        word = word[1:-1]
    if not word:
        return ()
    return min(tuple(w[k:] + w[:k])
               for w in (word, inverse(word)) for k in range(len(w)))


def orbit_normal_form(state):
    return sorted(cyclic_normal_form(word) for word in state)


def make_certificate(n):
    if type(n) is not int or n < 2:
        raise ValueError("The stated certificate requires n >= 2")
    initial = [[-1] + [2]*n + [1] + [-2]*(n+1),
               [-1, -2, 1, 1, -2]]
    target = [[1, 2, 1, -2, -1, -2], [1]*n + [-2]*(n+1)]
    packaged = [
        ["cycle", 0, n+3], ["mul", 1, 0, -1],
        ["conj", 0, -2], ["mul", 1, 0, 1],
        ["cycle", 1, 2], ["conj", 0, 1],
        ["mul", 0, 1, -1], ["cycle", 0, n+1],
        ["invert", 1], ["cycle", 1, n+1],
    ]
    for k in range(n-1):
        packaged.append(["mul", 1, 0, 1])
        if k < n-2:
            packaged.append(["conj", 1, -1])
    expanded, reached, packaged_peak = compile_moves(initial, packaged)
    return {"claim": "AC_equivalence", "parameter": n,
            "initial": initial, "target": target, "reached": reached,
            "packaged_moves": packaged, "moves": expanded,
            "packaged_peak": packaged_peak}


def verify(certificate):
    """Replay saved elementary moves; do not invoke the generator/compiler."""
    if certificate.get("claim") != "AC_equivalence":
        raise ValueError("Wrong claim")
    initial = certificate["initial"]
    target = certificate["target"]
    reached = certificate["reached"]
    for state in (initial, target, reached):
        check_state(state)
    state = copy.deepcopy(initial)
    peak = sum(map(len, state))
    for move in certificate["moves"]:
        # Generator emits only positive multiplication, inversion and conj.
        if move[0] == "mul" and move[-1] != 1:
            raise ValueError("Strict certificate requires positive product")
        state = elementary_step(state, move)
        peak = max(peak, sum(map(len, state)))
    if state != reached:
        raise ValueError("Recorded terminal tuple does not match")
    if orbit_normal_form(state) != orbit_normal_form(target):
        raise ValueError("Terminal tuple is outside target AC symmetry orbit")
    n = certificate["parameter"]
    expected_initial = [[-1] + [2]*n + [1] + [-2]*(n+1),
                        [-1, -2, 1, 1, -2]]
    expected_target = [[1, 2, 1, -2, -1, -2], [1]*n + [-2]*(n+1)]
    if n < 2 or initial != expected_initial or target != expected_target:
        raise ValueError("Certificate does not encode the stated family")
    return {"n": n, "packaged_moves": len(certificate["packaged_moves"]),
            "strict_elementary_moves": len(certificate["moves"]),
            "elementary_peak_total_length": peak,
            "packaged_peak_total_length": certificate["packaged_peak"]}


def self_test():
    for n in range(2, 101):
        cert = make_certificate(n)
        result = verify(json.loads(json.dumps(cert)))
        assert result["packaged_moves"] == 2*n + 7
        assert cert["reached"] == [[-2, -1, 2, 1, 2, -1],
                                   [-1]*(n-1) + [2]*(n+1) + [-1]]
        assert result["packaged_peak_total_length"] == 4*n + 11
    cert = make_certificate(3)
    for mutate in (
        lambda c: c["moves"].append(["conj", 0, 1]),
        lambda c: c["moves"].append(["conj", 0, 3]),
        lambda c: c["moves"].append(["mul", 0, 0, 1]),
        lambda c: c["target"][1].append(1),
    ):
        bad = copy.deepcopy(cert)
        mutate(bad)
        try:
            verify(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("Corrupt certificate was accepted")
    print("PASS: n=2..100; fixed terminal formula; linear packaged peak; "
          "four corrupted-certificate rejection checks")


def exact_root_certificate(certificate):
    """Root's independent format, with endpoint rotations explicitly compiled."""
    n = certificate["parameter"]
    tail = [["invert", 0], ["cycle", 0, 4],
            ["invert", 1], ["cycle", 1, n+2]]
    extra, reached, _ = compile_moves(certificate["reached"], tail)
    if reached != certificate["target"]:
        raise AssertionError("Exact target normalization failed")
    symbols = {1: "x", -1: "X", 2: "y", -2: "Y"}
    def word_string(word):
        return "".join(symbols[g] for g in word)
    moves = []
    for op, i, *args in certificate["moves"] + extra:
        if op == "invert":
            moves.append({"op": "invert", "i": i})
        elif op == "mul":
            assert args[1] == 1
            moves.append({"op": "multiply", "i": i, "j": args[0]})
        elif op == "conj":
            moves.append({"op": "conjugate", "i": i,
                          "g": symbols[args[0]]})
        else:
            raise AssertionError("Uncompiled operation")
    return {"format": "ordinary-ac-elementary-v1",
            "start": list(map(word_string, certificate["initial"])),
            "target": list(map(word_string, certificate["target"])),
            "moves": moves,
            "description": f"MS({n},y^-1 x^2 y^-1) to AK({n}), exact tuple"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--root-output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    cert = (json.loads(args.verify.read_text()) if args.verify
            else make_certificate(args.n))
    result = verify(cert)
    if args.output:
        args.output.write_text(json.dumps(cert, indent=2) + "\n")
    if args.root_output:
        args.root_output.write_text(
            json.dumps(exact_root_certificate(cert), indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
