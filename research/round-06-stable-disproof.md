# Round 06 · Stable lower bounds from synchronized projections

2026-11-19. The ordinary and stable instruction distances of AK(3) in the degree-eight characteristic-two Magnus quotient are at least **16** for either target order. Separately, every successful free-group path has at least three conjugations by the original letters in its normalized ordinary section. This improves the free-group padding cutoff.

## Successive exact corridor lifts

Split a fixed-rank move budget into radii $a,b$. Compute the complete start and goal balls in a cheap quotient, intersect at the midpoint and trim backward to states that can reach the intersection at the assigned layer. Allow waits throughout, so testing exactly $a+b$ clock ticks tests paths of at most $a+b$ instructions. Each higher tier constructs only the lifted prefix and suffix layers permitted by the previous projection. Intersect their terminal layers, then trim those lifted layers backward before moving to the next tier. All moves are reversible within each tier. Therefore a full path of the allowed length survives every trim, and a midpoint intersection in the final graph gives a path there. [Single-tier proof](round-06-magnus-corridor.md).

The intermediate rank-two graphs erase the added variables and retain all rows, including the initially trivial auxiliary rows. The final graph can still be retracted, or can restore the full marked alphabet to test the actual padded quotient. Endpoints and moves in each tier use the same sorting convention. For an ordered final target, the last tier keeps row positions and includes swaps as ordinary instructions, and only the projected layers are sorted. A positive final intersection is reconstructed as an instruction sequence and replayed using explicit monomial sets instead of packed integer arithmetic. The ordered degree-five control gives the known 11 instructions.

The optional instruction filter applies every candidate instruction first to the projected rows in the order inherited from the high tuple. Only the resulting comparison with the low layer sorts those rows. It evaluates a high-degree product or conjugation only if the corresponding low instruction can enter the next allowed layer. Conjugation by an erased variable acts as the identity in this test. The screened and unscreened lifts agree on the ordered degree-five control and on the degree-seven support-restricted exclusion.

## Combining the pair erasures

In rank $r\ge 3$, delete every marked variable outside a chosen pair. Each deletion is an algebra homomorphism, and the intersection of the kernels over all pairs consists exactly of linear combinations of monomials using at least three distinct variables. The monomial span with this support condition is an ideal because multiplying by a monomial cannot decrease support. The quotient retains support at most two and embeds into the product of the pair erasures. Thus it tests those erasures with one common sequence of instructions and one common alignment of the rows. Sorting the separate projections independently would discard that alignment.

The implementation inserts this support-restricted graph between the rank-two retraction and the full padded graph. It uses the same basis letters and ordinary instructions as the full graph. In rank three at degree seven only 742 of the 3,280 monomial positions survive. For the one-padding budget 11 control, the degree-five erased graph admits 24 midpoints. The support-restricted rank-three graph eliminates them all. The unrestricted rank-three run independently gives no intersection, in agreement with the [direct round-five exclusion](round-05-stable-disproof.md). A separate degree-three control follows a nonempty support-restricted corridor through the final full-rank lift and replays five instructions to the ordered basis.

## Positive padding through stable length 15

The [peak-rank normalization and mixing bound](round-01-stable-disproof.md) restrict an optimizing stable path of length at most 15 to $k\le 3$ added pairs. The following rank-two retractions exclude each positive $k$. The ordinary middle radius is $15-2k$. The survivor counts refer to midpoint states in successive degrees, after lifting through the prior corridor.

| Added pairs | Middle radius | Last two tested degrees | Midpoint counts |
| ---: | ---: | ---: | ---: |
| 1 | 13 | 6 and 7 | 13 and 0 |
| 2 | 11 | 5 and 6 | 24 and 0 |
| 3 | 9 | 4 and 5 | 7 and 0 |

All three excluded retractions are consequences of a putative padded degree-eight path. The unpadded split $7+8$ leaves 34,546 midpoints at degree five, 542 at degree six, 13 at degree seven and none at degree eight. This proves the lower bound of 16.

At stable budget 16, $k=1$ needs middle radius 14. Its retracted corridor leaves 8,102 midpoints at degree five, 109 at degree six, one at degree seven and none at degree eight. For $k=2,3,4$, retractions at degrees seven, six and four respectively exclude their middle budgets. Thus any degree-eight stable distance of 16 would be achieved at rank two. [Corridor receipts and replayed controls](../results/round06_stable_disproof_tiers.json).

## Three necessary original-letter conjugations in the free group

Let $p=x^3y^{-4}$, $b=xyxy^{-1}x^{-1}y^{-1}$ and $H=\langle p,b\rangle\le F(x,y)$. Project a normalized fixed-rank path by killing its added generators and retaining the rows. The initial rows all lie in $H$, and the target rows include $x$ and $y$. Products, inversions and swaps preserve containment of all rows in a given subgroup. Conjugations by the erased generators do nothing. When a conjugation by a retained signed letter $c\in\{x,x^{-1},y,y^{-1}\}$ occurs, replace the current containing subgroup $K$ by

$$
J_c(K)=\langle K,cKc^{-1}\rangle.
$$

This contains the new tuple regardless of the chosen recipient and the number of identity rows. The graph certificate checks $H$, all four once-enlarged groups and all sixteen twice-enlarged groups. It refolds each from the literal expanding word lists and separately from spanning-tree bases at every stage. Signed double-free transition graphs exclude ambient primitives in each folded subgroup. The independent partial-map test verifies the same exclusions with 2,772 closed map-pair states. All families of paths with at most two original-letter conjugations therefore fail to reach the basis. At depth three, eight of 64 envelopes admit primitives, including the full rose for $(x,x,y)$. Those envelopes are containment tests and can exceed the actual subgroup of any relator tuple. [Conjugation budget receipt](../results/round06_stable_disproof_conjugations.json).

The ordinary section of a minimum-length stable path using $k>0$ padded pairs requires at least $\lceil 3(k+1)/2\rceil$ crossing multiplications by the round-one incidence bound. These are distinct from the three necessary original-letter conjugations. Including insertion and deletion gives

$$
L\ge 2k+\left\lceil\frac{3(k+1)}2\right\rceil+3
\quad\Longrightarrow\quad
k\le \left\lfloor\frac{2L-9}{7}\right\rfloor .
$$

Thus for free instruction length at most 18 it suffices to check through three padded pairs. A cutoff of 21 needs at most four. This sharpening is specific to the free retraction, where subgroup containment certifies primitive exclusion. It does not use the corresponding finite Magnus graph to infer a stronger padding cutoff.

## Reproduce

~~~sh
python3 -B experiments/round06_stable_disproof_conjugations.py \
  | diff - results/round06_stable_disproof_conjugations.json
python3 -B experiments/round06_stable_disproof_tiers.py 1 6 7 4 5 6 7 --retracted
python3 -B experiments/round06_stable_disproof_tiers.py 2 5 6 4 5 6 7 --retracted
python3 -B experiments/round06_stable_disproof_tiers.py 3 4 5 3 4 5 --retracted
python3 -B experiments/round06_stable_disproof_tiers.py 0 7 8 4 5 6 7 8
python3 -B experiments/round06_stable_disproof_tiers.py 1 7 7 4 5 6 7 8 --retracted
python3 -B experiments/round06_stable_disproof_tiers.py 2 6 6 4 5 6 7 --retracted
python3 -B experiments/round06_stable_disproof_tiers.py 3 5 5 3 4 5 6 --retracted
python3 -B experiments/round06_stable_disproof_tiers.py 4 4 4 3 4 5 --retracted
python3 -B experiments/round06_stable_disproof_tiers.py 1 5 6 4 5 7
python3 -B experiments/round06_stable_disproof_tiers.py 1 5 6 4 5 7 --support-two
python3 -B experiments/round06_stable_disproof_tiers.py 1 2 3 1 2 3 --support-two --screen-instructions
python3 -B experiments/round06_stable_disproof_tiers.py 0 5 6 3 4 5 --ordered
~~~
