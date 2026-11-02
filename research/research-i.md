# Research I: shared-vertex torus-knot pairs and the length-14 frontier

Date: 2026-11-02. Independent research agent I (round 3).

**Status:** IN PROGRESS (checkpoint). No AK(3) trivialization, no counterexample.

## Previous work read and choice of direction

Read README and notes A–F in full; skimmed experiments/ and certificates/.

Direction (draft): the "torus-knot-pair" classes (AK(n), C3, C4, C6) consist of two
relators each of which is a torus-knot relator u^p v^q in some basis of F2. Bases of F2
up to simultaneous conjugation correspond to oriented Farey edges (Nielsen: the kernel
of Aut(F2) -> GL2(Z) is Inn(F2)). I study pairs by the Farey position of the two bases:
same edge (proved AC-trivial, Euclid), adjacent edges sharing a primitive (family
T(a;p,q) = (x^p y^q, x^a y x^-1 y), contains C3/C4 states), and AK(n) (no shared vertex).

## Checkpoint results

1. P1 ~AC C6: external ledger (alejandrozarco/andrews-curtis-ms14, commit a6c67b9,
   certs/P1_equiv_C6.json, 1066 moves) converted by `experiments/i_words.py --zarco` to
   `certificates/i_p1_to_c6.json`; `python3 experiments/elementary_verify.py
   certificates/i_p1_to_c6.json` -> moves 1091, peak 41, endpoint (xxyxxYY, xyXYYXy).
2. Engine runs (D's d_acsearch, full cyclic-product graph): C3 ~ T(2;4,7) (barrier 16),
   T(2;4,7) ~ T(2;5,9) (19), T(2;4,9) ~ T(2;5,11) (21); T(4;4,3) has a primitive relator
   after one product, and T(-4;7,-3), T(-4;8,-3) connect to it (AC-trivial).
   T(4;7,5) not connected to C4 at cap 24. (T(a;p,q) = (x^p y^q, x^a y x^-1 y).)
3. Observed: x^2yx^-1y is the braid relator in basis (u,v)=(xy,y^-1); so
   T(2;p,q) = (braid(u,v), (uv)^p v^-q). B3-conjugacy is decided by (PSL2(Z) image, abelianization).
