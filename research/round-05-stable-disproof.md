# Round 05 · Exact degree-seven stable distance by marked retraction

2026-11-19. The degree-seven characteristic-two Magnus stable distance of AK(3) is **14** to both the unordered and the ordered basis. Every path attaining that distance stays at rank two. All three relevant positive-padding cases can be excluded by searches whose ambient alphabet has only the two original variables. The finite calculation gives a lower bound of 14 in the free group.

## Retract the alphabet and keep all rows

Let $A_{k,d}$ be the ordinary distance in the degree-$d$ rank-$(n+k)$ Magnus group from the original $n$ relators padded with $k$ isolated pairs to an unordered basis. For $e\le d$, truncate to degree $e$ and set every added variable to zero. This is a homomorphism to the degree-$e$ rank-$n$ Magnus group. Apply it to each of the $n+k$ relators, keeping every row. An inversion, row swap or signed right product remains the same instruction or has no effect. A conjugation by a retained letter remains legal, and a conjugation by an erased letter has no effect.

The new endpoint problem has $n+k$ rows in a group marked by only $n$ letters. It starts with the original relators and $k$ identity rows and ends at the unordered original basis and $k$ identity rows. The identities are allowed to become nontrivial during the path. A final permutation of the full basis can assign the surviving generators to any row slots, which the unordered projected endpoint allows. Thus its distance $I_{k,e}$ satisfies

$$
A_{k,d}\ \ge\ I_{k,e}\qquad(e\le d).
$$

Keeping the rows avoids imposing any conjectural eliminability of the padding. The recourse to a lower Magnus degree retains the same inequality. The corresponding retraction also works in the free groups, by sending the added generators to the identity.

For AK(3) only $x,y$ survive, so the coefficient vectors at degrees four, five, and six have respectively $31$, $63$, and $127$ bits. In comparison, a direct degree-seven search at rank four uses $21,845$ bits per row. The projected search may admit paths that fail to lift to the original padded graph. It certifies exclusions when its two searched balls are disjoint.

For $k\ge n$ the projected distances have a uniform upper bound over all degrees. This is already true in the free group. Fill $n$ spare identity rows with the basis elements by multiplying conjugates of the original normally generating relators and their inverses. Restore each donor after using it. Use the resulting basis rows to clear the original ones. The resulting free-group sequence projects to every degree. Thus the all-padding retraction gives finite-length exclusions, while a divergence proof for multiple added pairs needs to retain information that this retraction erases.

## Complete searches at the needed thresholds

The generator expands one complete breadth-first layer at a time, choosing the smaller frontier. It sorts the rows to take the quotient by row permutations, which preserve the instructions on both the marked and the retracted graphs. In each negative case the final ball radii sum to the tested threshold.

| Padded pairs $k$ | Projection degree $e$ | Ordinary threshold | Visited from both ends | Result |
| ---: | ---: | ---: | --- | --- |
| 1 | 6 | 11 | 590,239 / 2,241,421 | $I_{1,6}>11$ |
| 2 | 5 | 9 | 45,581 / 272,526 | $I_{2,5}>9$ |
| 3 | 4 | 7 | 2,622 / 20,971 | $I_{3,4}>7$ |

At degree five, the one-identity control has distance 10. The degree-six information is essential for using the stated retraction to exclude a length-11 one-padding middle section. The rank-three degree-seven direct search independently excludes it as well, with 5,865,816 and 62,814,006 visited states. [Exact retraction results](../results/round05_stable_disproof_retractions.json), [direct one-padding check](../results/round05_magnus_degree7_one_padding.json).

The [peak-rank formula and incidence bound](round-01-stable-disproof.md) imply that, if the degree-seven stable distance were at most 13, a minimizing path would use at most three padded pairs. Indeed four or more would already cost at least 16 elementary moves. For each $k=1,2,3$, a stable length at most 13 gives a normalized ordinary middle section of length at most $13-2k$. The first three searches exclude those sections. The [round-three rank-two searches](../results/round03_magnus_degree7.json) showed that the ordinary distance is 14 to both targets. They exclude $k=0$ at length 13 and supply an ordered endpoint at length 14. This proves the exact stable distances.

## All shortest degree-seven paths stay at rank two

Increase the three positive-padding thresholds by one.

| Padded pairs $k$ | Projection degree $e$ | Ordinary threshold | Visited from both ends | Result |
| ---: | ---: | ---: | --- | --- |
| 1 | 7 | 12 | 8,656,959 / 2,247,723 | $I_{1,7}>12$ |
| 2 | 6 | 10 | 823,413 / 277,049 | $I_{2,6}>10$ |
| 3 | 4 | 8 | 33,824 / 20,971 | $I_{3,4}>8$ |

A path attaining the stable distance 14 would have a normalized ordinary middle section within these thresholds if it used one, two, or three padded pairs. Four or more are again excluded by the incidence bound for a minimizer. Thus every shortest stable path at degree seven, for either target convention, uses peak rank two. The equality case in the peak-rank normalization then forces zero rank changes. The same positive-padding exclusions carry to every higher degree at stable length 14, for a path minimizing distance to the unordered basis. Distance divergence with the Magnus degree remains open. [Extended exclusion results](../results/round05_stable_disproof_extended_retractions.json).

The independent replay represents each polynomial as a set of monomials, computes multiplication by explicit concatenation with parity cancellation, and computes inverses by powering to the uniform exponent minus one. It checks the essential three cases against the bit-packed search. Run from the repository root.

~~~sh
python3 -B experiments/round05_stable_disproof_retractions.py --independent \
  | diff - results/round05_stable_disproof_retractions.json
python3 -B experiments/round05_stable_disproof_retractions.py --extended \
  | diff - results/round05_stable_disproof_extended_retractions.json
~~~
