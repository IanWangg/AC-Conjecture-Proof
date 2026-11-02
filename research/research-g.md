# Research G: the torus-knot-pair ACM graph of AK(3) (exact long-conjugator moves toward the 3-manifold locus)

Date: 2026-11-02. Independent research agent G (round 3).

**Status:** IN PROGRESS (checkpoint). No claim yet.

## 1. Previous work read and choice of direction

Read in full: README.md, research-a … research-f; skimmed experiments/ and certificates/.
Re-ran `elementary_verify.py --selftest` (passes) and `certificates/ms3_to_ak3_exact.json` (32 moves, peak 23).

Direction (draft): AK(3) is a *torus-knot pair*: x^3y^-4 presents the T(3,4) group and the braid
relator presents the trefoil group. Quotient-conjugacy (ACM) moves with a frozen torus-type relator can be
decided *exactly*, with arbitrarily long conjugators, by normal forms in <x,y | x^p y^q>. Torus-type cyclic
words are exactly the images theta_M(x^p' y^q'), M in GL(2,Z) = Out(F_2). The "torus graph" has these
pairs as vertices. A vertex whose partner relator has syllable length 2 in C_p * C_q (a meridian) is
AC-trivial by an explicit Euclidean algorithm. Plan: build the graph, calibrate on AK(2), search from AK(3).
