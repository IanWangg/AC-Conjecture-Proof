# Research round 03

2026-11-19. The five projects ran in overlapping waves from the round-two synthesis. All five target outcomes remain open.

## Track reports

| Target | Result |
| --- | --- |
| [Ordinary AK(3) trivialization](round-03-ak3.md) | Every normally generating rank-two relator pair generates a malnormal subgroup. This removes the malnormality proviso from the finite reverse-barbell search applied to ordinary AK(3) waypoints. The minimum distance to the set of 56 cap-25 escape pairs of energy 17 is 22 cyclic product edges. The 284-move strict witness has cyclic peak 25. |
| [Proof of Stable AC](round-03-stable-proof.md) | Any stable AK(3) trivialization of maximum rank three needs cyclic peak at least 22. At cap 21, all 4,208 first-exit and successor states without the auxiliary singleton retain a one-occurrence pivot. All 56 reentry projections are in the ordinary cap-25 component. The geometric-block test excludes the audited no-singleton sector. |
| [Proof of ordinary AC](round-03-ac-proof.md) | Relative-basis frames give AC-equivalent projections even with no shared slots, by Piggott's characterization of formal AC automorphisms. A fixed-rank path carrying an actual relative basis at every vertex descends. One-row marked-free exchanges also descend when the common block quotient is nonfree. |
| [Disproof of ordinary AC](round-03-ac-disproof.md) | Two-phase primitive exclusion covers arbitrarily long admissible positive and negative bridges and a certified regular language of mixed-sign bridges. The 552 checked three-lobe overgroups cover additional families with repeated readable lobe words. |
| [Disproof of Stable AC](round-03-stable-disproof.md) | In a normalized padded section, an auxiliary cut with two incoming and two outgoing products exchanges at most one marked generator each way. A same-chart, two-incoming cut with rank-two complement admits elimination when the projected one-donor quotient has a single normal-generator conjugacy class up to inversion. |

## Verified extensions and interactions

- The independently verified [cyclic cap-26 component](round-03-cyclic26.md) has 10,340,996 states and no primitive relator among 8,561,906 coordinate classes. It sets the ordinary cyclic peak lower bound to **27**. Eight energy-15 pairs form a single signed-basis orbit and first enter at cap 26. Thirty cyclic product edges reach that set, with a strict 369-move witness of raw peak 29. All rotations of the eight pairs pass the finite two-copy screen for the stated intersecting-axis phase.
- The [two frozen-donor witnesses](round-03-frozen-donors.md) show that neither possible one-sided completion of the existing 533-move braid-kernel lift can produce an ambient primitive. After the lifted endpoint, both relator slots must receive a multiplication before either becomes primitive. In every successive braid-kernel quotient either one-sided completion remains possible, but the corresponding restricted strict distances diverge. This pinpoints where the round-two quotient compiler loses any prospect of a uniform bound.
- In degree seven of the characteristic-two Magnus tower, the ordinary distance is 14 for both the ordered and unordered targets. The round-two stable exclusions and this ordinary path place both stable distances in the interval from 13 to 14. The fixed-padding searches at the new threshold remain a separate calculation. Reproduce the ordinary entries by calling ak3_bounded_test(7,0,14,unordered) in experiments/round01_stable_disproof_search.py for both values of unordered. [Degree-seven results](../results/round03_magnus_degree7.json), [stable lower bound through degree seven](round-02-stable-disproof.md).
- The ordinary proof track both widens the class of allowable rank-reduction frames and identifies a remaining multiplication case involving different donor choices. The stable capped search supplies actual families of rank-three vertices with moving pivots. Together they give an exact test for candidate padded paths and isolate the point at which the current rank-reduction methods cease to apply.
- The graph tracks now share a proof of malnormality for all actual normally generating rank-two sources. The proof puts the bridge map search on a uniform footing. The repeated-lobe overgroups still address only a restricted number of alternating phases, so their use is to exclude concrete next-phase programs and guide which later reachable cores to test.

## Questions for round 04

1. **AK(3) trivialization.** Compare the cap-26 energy-15 escape family and its later-phase successors with the known-trivial archive using the now-uniform bridge map test. Give priority to sources beyond the checked two-copy exclusions.
2. **Stable AC proof.** Extend the exact excursion method past cap 21 and look for a genuinely new geometric/free-quotient block or a vertex where every one-occurrence pivot disappears.
3. **Ordinary AC proof.** Investigate the donor-choice mismatch for relative frames selected only up to conjugacy. Seek a compatible exchange criterion that can be verified along a concrete padded path.
4. **Ordinary AC disproof.** Extend the three-lobe overgroup method to four lobes and look for substantive bridge classes outside both the regular-language test and the overgroup catalogue.
5. **Stable AC disproof.** Test the two-incoming constraint for a changing marked chart and for a quotient with multiple normal-generator conjugacy classes. Compare the theoretical cases with exact fixed-rank quotient searches.
