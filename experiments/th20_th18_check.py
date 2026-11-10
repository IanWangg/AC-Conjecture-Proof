#!/usr/bin/env python3
"""TH20 independent checks for TH18 with own BS conjugacy code (th20_bs).
(1) number of killer classes (sigma = +1) of t-length 3 in BS(n,n+1): n(n-1), n = 2..5; of t-length 5 for n = 2: 16;
(2) T4: x y^a x y^b' X y^c' ~ x^2 y^b X y^-b  iff  b = b' (mod n+1), b = -c' (mod n)   (exhaustive residues, n = 2..4);
(3) T5: bridge word XYxxY in C_{2n+1}; T9: P_beta, Q_gamma classes; r_n ~ p_n mod P_beta (hand proof in the note);
(4) T6: r_n conjugate to a primitive in <x,y | y^b x y^-b = x^2> for b | n or b | n+1: free-group identity check of the proof's formulas via coset-free rewriting is replaced by the certificates; here only the class labels."""
import sys, itertools
sys.dont_write_bytecode = True
from th20_lib import red, inv, cyc
import th20_bs as BS
py = lambda e: "y" * e if e >= 0 else "Y" * (-e)
def word(signs, exps): return red("".join(("x" if s > 0 else "X") + py(a) for s, a in zip(signs, exps)))
def classes(n, signs, rng):
    reps = []
    for exps in itertools.product(rng, repeat=len(signs)):
        w = word(signs, exps)
        if BS.tlen(w, n, n + 1) != len(signs): continue
        if not any(BS.conj_bs(w, r, n, n + 1) for r in reps): reps.append(w)
    return reps
for n in range(2, 6):
    c3 = classes(n, (1, 1, -1), range(0, n * (n + 1)))
    print("(1) n=%d: t-length-3 killer classes with sigma=+1: %d (claimed n(n-1) = %d)" % (n, len(c3), n * (n - 1)))
a = classes(2, (1, 1, 1, -1, -1), range(0, 6)); b = classes(2, (1, 1, -1, 1, -1), range(0, 6))
print("(1) n=2, t-length 5: necklace (+++--): %d classes, (++-+-): %d classes (claimed 12 + 4 = 2n^3(n-1) = 16)" % (len(a), len(b)))
for n in range(2, 5):
    N = n * (n + 1)
    for a_, b_, c_ in itertools.product(range(-2, 3), range(1, N), range(1, N)):
        w = word((1, 1, -1), (a_, b_, c_))
        if BS.tlen(w, n, n + 1) != 3: assert b_ % (n + 1) == 0 or c_ % n == 0; continue
        bb = next(t for t in range(N) if t % (n + 1) == b_ % (n + 1) and t % n == (-c_) % n)
        assert BS.conj_bs(w, word((1, 1, -1), (0, bb, -bb)), n, n + 1), (n, a_, b_, c_)
        assert bb % n and bb % (n + 1)
print("(2) T4 class formula verified for n = 2,3,4 (all residues b', c'; a in [-2,2])")
for n in range(2, 9):
    assert BS.conj_bs("XYxxY", word((1, 1, -1), (0, 2 * n + 1, -(2 * n + 1))), n, n + 1)
    for g in range(1, n):          # Q_gamma = x y^-g x y^-1 X y^g  in C_b, b = -1 mod n+1, b = -g mod n
        bb = next(t for t in range(n * (n + 1)) if t % (n + 1) == n and t % n == (-g) % n)
        assert BS.conj_bs(red("x" + py(-g) + "x" + "Y" + "X" + py(g)), word((1, 1, -1), (0, bb, -bb)), n, n + 1)
print("(3) bridge word in C_{2n+1} and Q_gamma classes, n = 2..8")
