"""TH19 check of TH07 Theorem B: cyclically reduced words conjugate to b^+-1 (b = xyxYXY) in
G_n = <x,y | x^n = y^(n+1)>: Orb(b) (12 words, length 6), nothing of length 7..2n+1, and exactly
Orb(b_1) u Orb(b_2) (8n+8 words) at length 2n+2."""
import sys
sys.path.insert(0, "experiments")
from th19_lib import *
b = "xyxYXY"
for n in (3, 4, 5):
    b1 = "X"*(n-1) + "y" + "x" + "Y" + "x"*(n-1) + "Y"
    b2 = "x" + "y" + "X"*(n-1) + "Y" + "x"*(n-1) + "Y"
    kb, kbi = (conj_key := lambda w: ((n+1)*expo(w)[0] + n*expo(w)[1], neck_pq(w, n, n+1)))(b), None
    keys = {conj_key(b), conj_key(inv(b))}
    counts = {}
    top = set()
    for L in range(6, 2*n + 3):
        found = [w for w in cyc_words(L) if abs((n+1)*expo(w)[0] + n*expo(w)[1]) == 1 and conj_key(w) in keys]
        counts[L] = len(found)
        if L == 6: assert set(found) == orb(b)
        if L == 2*n + 2: top = set(found)
    print(f"n={n}: counts by length {counts}; length {2*n+2}: equals Orb(b_1) u Orb(b_2): {top == (orb(b1) | orb(b2))} (8n+8 = {8*n+8})")
