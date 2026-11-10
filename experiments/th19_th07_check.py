"""TH19 check of TH07 Theorem A: count the cyclically reduced words of length 2n+3 conjugate in
B = <x,y|xyx=yxy> to p_n^{+-1} (p_n = x^n Y^{n+1}); TH07 claims exactly 4n(n+1)(2n+3) words,
namely the rotations of U^{+-1}, U in {U1(a,c), U2(a,c): 0<=a<=n-1, 0<=c<=n}."""
import sys
sys.path.insert(0, "experiments")
from th19_lib import *

def U1(n, a, c): return "Y" + "x"*a + "Y"*c + "x" + "y" + "X"*(n-c) + "y"*(n-1-a) + "X"
def U2(n, a, c): return "x" + "Y"*c + "x"*a + "Y" + "X" + "y"*(n-1-a) + "X"*(n-c) + "y"

for n in range(1, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 4):
    p = "x"*n + "Y"*(n+1)
    L = 2*n + 3
    found = {w for w in cyc_words(L) if conj_in_B(w, p) or conj_in_B(w, inv(p))}
    claimed = set()
    for a in range(n):
        for c in range(n+1):
            for U in (U1(n, a, c), U2(n, a, c)):
                assert len(U) == L and cyc(U) == U, U
                claimed |= orb(U)
    # also lengths below: 2n+1 gives Orb(p_n) u Orb(q_n), 2n+2 nothing
    low = {L2: sum(1 for w in cyc_words(L2) if conj_in_B(w, p) or conj_in_B(w, inv(p))) for L2 in (2*n+1, 2*n+2)}
    print(f"n={n}: enumerated {len(found)} words of length {L}; formula 4n(n+1)(2n+3) = {4*n*(n+1)*(2*n+3)};"
          f" claimed list has {len(claimed)}; equal sets: {found == claimed}; lengths 2n+1, 2n+2: {low}")
