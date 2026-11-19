# Research round 04

2026-11-19. Five agents continued the five targets using the round-three synthesis. The available researcher slots required overlapping waves. The ordinary AK(3) trivialization and the two conjectures remain open.

## Track reports

| Target | Result |
| --- | --- |
| [Ordinary AK(3) trivialization](round-04-ak3.md) | A weighted intrinsic-basis index compares the entire 10,340,996-state cyclic cap-26 component to 23,902 known-trivial archive pairs through reverse energy 56. It finds no subgroup join after arbitrary independent tails on both sides. The energy-15 orbit has additional finite and regular-language first-bridge exclusions. |
| [Proof of Stable AC](round-04-stable-proof.md) | The exact least cyclic peak for losing all one-occurrence pivots for the fixed auxiliary generator is 22. A strict 247-move rank-three path first loses them at step 235. A separate partial scan checks short-row projections and rules out a free-cyclic two-row block in 5,431 pivotless states. |
| [Proof of ordinary AC](round-04-ac-proof.md) | The remaining donor-choice mismatch is resolved for paths with at most two padded pairs and conjugacy-relative frames at every state. Several shared-block, conjugator and residual-basis conditions cover higher padding. A three-pair example gives a 39-move splice despite failure of both obvious frame transports. |
| [Disproof of ordinary AC](round-04-ac-disproof.md) | All 7,200 four-lobe chains and 2,358,360 two-copy joins pass. One new bridge of length 17 escapes the entire earlier three-lobe read language. Its extension yields exponentially many equal-length bridges with repeated lobe readings that still obey the two-phase exclusion. |
| [Disproof of Stable AC](round-04-stable-disproof.md) | A two-incoming cut can be removed across changing marked charts when the three successive free quotients admit common lifted bases at each incoming edge. An explicit nonfree middle quotient shows where the criterion stops. |

## What the results establish together

- The fixed-$z$ loss occurs at cyclic peak 22. Along its strict witness, allowing any marked generator to be eliminated gives an available one-occurrence chart at every state. All 20 projected pairs return to the cap-26 ordinary AK(3) component and fail the geometricity test. Thus this particular rank-three path explores other charts without a new ordinary component or a geometric completion. The ordinary path theorem covers fixed marked complements, so changing the eliminated generator remains a separate question. [All-chart screen](round-04-chart-screen.md).
- The two-incoming cut theorem permits a change of marked chart under a common lifted basis condition. A separate balanced trivial example has two explicit one-occurrence charts and no common lifted basis, proved by an $A_5$ commutator comparison. Both projected tuples still have strict ordinary trivializations. This gives a concrete test case for a broader moving-chart projection theorem. [Common-lift obstruction](round-04-chart-lifts.md).
- The full cap-26 join audit uses the bounded lengths of intrinsic primitive basis classes in each reverse core. The four-lobe and regular-language proofs instead exclude a prescribed sequence of phases for given lobe and bridge families. These are distinct restrictions on possible completions. Combining them narrows the search to later reachable cyclic states or other alternating paths.
- The [synchronized finite corrections](round-04-finite-corrections.md) yield a 1,793-move free certificate from AK(3). Its endpoint maps to the basis in the braid relation-module quotient and both round-three finite witnesses simultaneously. All eight signed transition tests exclude a primitive in its displayed 157,360-vertex subgroup. The construction also proves connectivity to the basis in every product of the braid-kernel tower with those two finite factors.
- At degree seven in the Magnus tower, the rank-five ordinary search with three padded pairs exhausts radius seven without reaching a basis. Combined with the already checked ordinary distance 14 and the peak-rank lower bound, a stable quotient path of length 13 would have to use one or two padded pairs in its normalized middle section. The stable distance is still between 13 and 14. Reproduce the added search with ak3_bounded_test(7,3,7) in experiments/round01_stable_disproof_search.py. [Rank-five result](../results/round04_magnus_degree7_padding.json).
- The cap-27 generator produced 37,344,580 candidate states. An independent Euclidean-word audit checked its 32,187,372 cyclic coordinate classes and found zero primitive coordinates. Independent closure and connectivity are being checked, so the checked ordinary peak bound remains 27 in this round. [Generation and primitive audit](../results/round04_cyclic27_generation.json).

## Questions for round 05

1. **AK(3) trivialization.** Use the weighted reverse index on later reachable cyclic states and the four-lobe obstruction to prioritize source types. If the cap-27 generation is available, check independent closure before making an exclusion claim.
2. **Stable AC proof.** Search for a first state losing every one-occurrence chart, including old-letter choices, and check genuine geometric/free-quotient targets there.
3. **Ordinary AC proof.** Compare projections when adjacent states eliminate different marked generators. The witnessed change at cap 22 gives a concrete exact control.
4. **Ordinary AC disproof.** Find bridges that escape the four-lobe language, and test what happens when there is one more alternating Nielsen and conjugation phase.
5. **Stable AC disproof.** Relate the marked-cut constraints to exact distance bounds. The degree-seven question can be approached by lifting only the degree-six paths that meet the correct length threshold, or by quotienting the finite fixed-rank searches by permutations of the auxiliary generators.
