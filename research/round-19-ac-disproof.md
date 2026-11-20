# Eight schedules for four ordinary AK(3) conjugations

2026-11-19. Any ordinary rank-two AC trivialization from literal AK(3) using exactly four single-generator conjugations has one of the following eight signed schedules. Between the first and second, and between the second and third, it needs at least one multiplication each. Between the third and fourth it needs at least two. These are necessary conditions for actual paths. [Exact census and replay](../results/round19_ac_disproof_four_conjugations.json), [four-conjugation lower bound](round-18-ac-disproof.md).

~~~text
xyxy  xyxY  xyXy  xyXY  yxyx  yxyX  yxYx  yxYX
~~~

## Four-letter envelopes and the last two rows

From the literal source subgroup, form the successive containing groups by replacing a current group $K$ with $\langle K,cKc^{-1}\rangle$ at each conjugating letter $c$. Multiplications and inversions between the conjugations preserve the subgroup of the actual tuple. The final containing group must be the ambient free group for the actual path to reach a basis.

| Four-letter check | Schedules |
| --- | ---: |
| Whole final envelope primitive-free | 138 |
| Whole final envelope proper and containing a primitive | 26 |
| Three-letter envelope already the ambient rose | 16 |
| Whole final envelope ambient, forward last-row test fails | 17 |
| Whole final envelope ambient, only reverse last-row test fails | 13 |
| Whole final envelope ambient, both last-row tests pass | 46 |

For a proper three-letter envelope $K$, let $c$ be the last signed letter. After the last conjugation there is a pair $(u,cvc^{-1})$ with $u,v\in K$, up to its order. If the pair generates the ambient group, $\langle K,cvc^{-1}\rangle$ is ambient. Common conjugation by $c^{-1}$ also shows that $\langle K,c^{-1}uc\rangle$ is ambient. The replay checks each necessary condition by the exact Round 11 automaton. It reads a freely reduced word in the conjugated donor core while taking one silent transition across a rose-producing vertex identification in $K$. Both checks retain an explicit completing word in each passing direction. Conjugating the whole pair to obtain the reverse test uses the two-row hypothesis. [Original last-row test](round-11-three-conjugations.md).

The two actual rows immediately after the last conjugation must already be a basis. The Nielsen suffix preserves their subgroup, and a generating pair of the rank-two free group is a free basis. Conjugation preserves a row's primitivity, so both rows immediately before this last conjugation must be primitive. This excludes 38 of the remaining 62 schedules by exact primitive exclusion in their three-letter envelopes. The other 24 have one of eight prefixes. The integer-character argument below excludes four prefixes and 16 schedules, leaving the eight displayed schedules.

## Equal first letters

For $a=x,c=Y$ and for $a=y,c=X$, set
\[
J_a=\langle H^a,H^{a^2}\rangle,\qquad B_{a,c}=\langle J_a,c\rangle,
\]
where $H$ is the literal source subgroup. If the first two conjugations are by $a$, keep the first unchanged coordinate $u\in H$. Just before the third conjugation both coordinates lie in $\langle J_a,u\rangle$. Either sign of the third letter $c$ uses the same containing group $\langle B_{a,c},u\rangle$. The same character normalized on $c$ applies to both orientations.

The Round 18 argument verifies that the normal closure of $\langle J_a,u\rangle$ in $\langle B_{a,c},u\rangle$ is primitive-free for every $u\in H$. The new audit instantiates it for both $(a,c)$ above. Each based fibre component has 12 vertices and 11 edges. The pullback character has exact heights that distinguish the source vertices over each overgroup vertex. Two pairs of fibre vertices with the same source vertex give both nontrivial gapless folds in each case. Every resulting character kills the corresponding representative in addition to the transported generators. The signed double-free gap check covers equal and distinct overgroup endpoints and finds no accepted gap. For a gap folded into a circle on a nonempty stem, any primitive loop must stay in the old core or entirely in the circle. Zero voltage in the circle forces the source endpoints equal, reducing to the primitive-free source. This excludes primitive exposure at the prefixes $xxy,xxY,yyx,yyX$. [Fibre product and stem argument](round-18-ac-disproof.md#the-last-ordinary-schedule-with-three-conjugations).

## Products between conjugations

A mask on the three gaps marks the intervals where a multiplication is permitted. For each of the eight schedules and each mask, partition the four conjugations into blocks separated by permitted multiplications. A product-free block accumulates one exact conjugating word per row. For each of the 16 receiver assignments, track the two row identities, commute inversions past the conjugations and freely reduce each accumulated word. If this cancels two conjugations, the path would have fewer than four and Round 18 already excludes it. Otherwise replace the subgroup before each nonfinal block by the subgroup generated by its two transported copies. Keep the original ambient marking at every boundary. For the final block, one common conjugation permits the two directional last-row tests with the relative transport word. This is a necessary containment check for the chosen receiver assignment even when unrestricted multiplication occurs at every marked gap.

Only mask 111 survives for any of the eight schedules. In addition, the two-phase theorem ensures that immediately before the third conjugation neither row is primitive. The third conjugation preserves this property. The two rows must both be primitive before the fourth conjugation, so two separate multiplications are necessary in the third gap. Thus any trivialization with exactly four conjugations uses at least four multiplications between them, with allocation at least $(1,1,2)$. [Arbitrary two-phase exclusion at literal AK(3)](round-16-ac-disproof.md).

## Compatible relaxed last pairs

There are explicit pairs in the three-letter envelopes for which the one actual final conjugation produces a basis. In the table it acts on the second entry of the input. The replayer directly checks both primitive cyclic classes, both subgroup memberships before the last conjugation, and the ambient rose after it. These witnesses verify compatible primitive exponent vectors and explain why whole-envelope primitivity and determinant tests leave these eight schedules open. The construction gives no path from the literal source to any of these input pairs with the first three prescribed conjugations.

| Schedules | Relaxed input in the three-letter envelope | After last conjugation |
| --- | --- | --- |
| xyxy, xyXy | (yxYXY, X) | (yxYXY, yXY) |
| xyxY, xyXY | (X, yxYXY) | (X, xYX) |
| yxyx, yxYx | (xyXYX, Y) | (xyXYX, xYX) |
| yxyX, yxYX | (Y, xyXYX) | (Y, yXY) |

~~~sh
set -o pipefail
python3 -B experiments/round19_ac_disproof_four_conjugations.py \
  | diff -u results/round19_ac_disproof_four_conjugations.json -
~~~
