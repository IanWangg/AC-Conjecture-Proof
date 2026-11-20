# Independent closure at ordinary cap 31 and stable rank-three cap 22

2026-11-19. An ordinary AK(3) trivialization must reach cyclic total length at least **32**. A stable trivialization whose rank never exceeds three must reach cyclic total length at least **23**. The two large independent closure verifiers completed and agree with the generation receipts. [Combined audit](../results/round10_independent_closures.json).

## Ordinary cap 31

The independent verifier reports a closed and connected component from the original AK(3) orbit. It checks 288,686,428,968 candidate products, 16,488,539,344 admitted neighbors and 254,220,523 signed ambient and row orbits. All three totals agree exactly with the generator. The separate Euclidean primitive check finds no primitive coordinate among the 55,347,782 single-sign coordinate occurrences in the same catalogue. The catalogue SHA-256 matches the digest saved by that primitive check. Thus even the first primitive coordinate in an ordinary path requires cyclic peak at least 32. [Generation, primitive receipt and commands](round-09-cyclic31.md), [independent verifier](../experiments/round07_ak3_wide_verify.cpp).

## Rank-three excursions at cap 22

The independent stack-reduction verifier checks that the catalogue contains all 3,008 signed seed orbits from 48,096 literal first exits. It verifies closure of 246,052,265 non-singleton orbits, using 267,125,415,576 candidate products and 10,490,694,648 admitted neighbors. There are 97,463,328 nonempty-bridge candidates. The verifier recovers exactly 432 signed-marked reentries to rank two, and the separate return-only checker reproduces their TSV byte for byte. Each reentry lies in the exact ordinary cap-22 component.

That ordinary component contains no primitive relator and is invariant under signed ambient changes. Within a singleton phase the projected rank-two tuple keeps this invariant, and every departure into the non-singleton phase begins at a checked first exit. Each subsequent return has a checked cleared projection. Rank cannot first fall below two without producing a singleton at rank two, which the invariant excludes. This gives the stable lower bound for all paths at rank at most three, including repeated rank changes and deletion of any isolated marked letter. [Invariant and reproduction commands](round-06-stable-proof.md), [independent non-singleton verifier](../experiments/round06_stable_proof_singleton_verify.cpp), [independent return-only audit](round-10-stable-proof.md).
