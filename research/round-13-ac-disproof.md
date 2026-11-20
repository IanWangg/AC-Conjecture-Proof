# Proper overgroups of the external rank-three projection

2026-11-19. Let $P=(\texttt{XXYxYXXYxxy},\texttt{XXYXYxxyXyxxy})$ be the marked energy-24 projection reached from AK(3) by the independently replayed 18,477-step stable path. Its signed orbit is absent from the generated ordinary cyclic cap-32 catalogue. The row subgroup $H=\langle P\rangle$ has primitive-free normal closure in every proper overgroup in $F(x,y)$. The exclusion applies until the whole relative conjugators of an ordinary path generate the ambient group together with $H$. [Stable path and catalogue comparison](round-13-stable-proof.md), [replay and case digests](../results/round13_ac_disproof_external.json).

## Exact classification

The two exponent vectors are $(-1,-2)$ and $(0,1)$, with determinant $-1$. The 17-vertex source core has no primitive loop. The independent partial-map replayer verifies closure of all 60 states across the four paired-map tests.

| Rank of principal image | All images | Free quotient excludes |
| --- | ---: | ---: |
| 2 | 2 | 0 |
| 3 | 60 | 60 |
| 4 | 887 | 886 |
| 5 | 3,900 | 3,900 |
| 6 | 4,764 | 4,764 |
| 7 | 1,437 | 1,437 |
| 8 | 76 | 76 |
| **Total** | **11,126** | **11,123** |

The two rank-two images are the source and the ambient rose. The unimodular exponent matrix implies there are no other rank-two overgroups, since the image core carries a free factor whose abelianization already surjects onto $\mathbb{Z}^2$. In each of the 11,123 rank-increasing cases the two rows of $P$ extend to a basis of the image subgroup. The script verifies the inverse Nielsen marking and checks for nonempty identity-labelled loops in the free quotient by those two rows. The signed double-free cyclic languages cover every rank-two ambient primitive, and every case gives zero neutral cycles. [Principal-image reduction and the free-quotient test](round-10-ac-disproof.md), [same-rank reduction](round-09-rank-two-overgroups.md).

The sole remaining proper principal image is a four-vertex rank-four core. The spanning-tree chord basis is $(yx,xxy,xyy,XXy)$, and the two rows read $\texttt{dCbCAb}$ and $\texttt{dCDadb}$. The integer characters $(1,2,0,-3)$ and $(1,1,-1,-3)$ each kill both rows. The first character excludes six of the eight signed double-free languages and the second excludes the remaining two. The independently checked strict-cycle certificates contain 60 inequalities. Therefore each putative cyclic primitive loop has nonzero voltage under at least one character that kills the entire source normal closure.

The proof for general proper overgroups uses the principal image of $H$ in the overgroup core as a free factor. Outside non-tree edges give traversals of zero signed count on the normal closure. A cyclic ambient primitive is sign-pure, so it cannot use those edges. Retraction then places a conjugate of the putative primitive in the excluded normal closure inside the principal image. A finite product of conjugates uses finitely many words, which reduces arbitrary proper overgroups to the same argument. [Proof of the reduction](round-10-ac-disproof.md).

## Single-word enlargements and controls

All 136 single-vertex identifications give rank three under two independent folds. By the one-word gap criterion, for every ambient word $g\notin H$, the subgroup $\langle H,g\rangle$ is thereby proper of rank three, either by one such identification or by adding one cycle. Its marked generators form a basis, so $H$ is malnormal. In an ordinary path from $P$, coalescing conjugations between products and anchoring one row gives one relative word per conjugation block. Any primitive exposure thus needs at least two growth events of the cumulative overgroup and also a product after the ambient group is reached. [One-word gap criterion](round-09-rank-two-overgroups.md#adjoining-a-single-outside-word), [relative-conjugator gauge](round-12-ac-disproof.md#the-first-full-relative-conjugator-subgroup-on-a-strict-route).

The same circuit checks show primitive absence in each of the four shortest absent projection cores from the rank-three experiment, of energy 23. They have 19, 20, 19 and 18 vertices. All 171, 190, 171 and 153 first identifications, respectively, have rank three. Thus each source subgroup is also malnormal. The exhaustive normal-closure classification above concerns the ledger-certified energy-24 marking.

The identical free-quotient solver replays three known positive primitive-kernel witnesses from the AK(2) source. A different marking on a strictly trivializing AK(2) path already satisfies the universal proper-overgroup exclusion. The exact tests constrain a primitive exposure through proper cumulative subgroups. The ordinary AK(3) path problem remains open. [AK(2) comparison](round-11-ac-disproof.md).

## A fixed-donor exclusion at every receiver length

Hold the second row of $P$ fixed while allowing a receiving block on the first row. The determinant condition forces any primitive receiver to have first exponent $\pm1$. Up to inversion and cyclic conjugacy its class is $xy^k$ for some integer $k$. With one-line permutations $x=(1,3,2,5,6,4)$ and $y=(2,4,5,3,1,6)$ in $S_6$, the fixed row vanishes and the receiver has cycle type $(2,2,2)$. The period of $y$ is five. The five candidate types are $(1,2,3)$, $(6)$, $(1,2,3)$, $(1,1,4)$ and $(6)$. None is the receiver type, which rules out this whole block independently of the number of its instructions. [Exact permutation replay](../results/round13_ac_disproof_external.json).

## Reproduction

The compiled census propagates vertex congruences by merging transition tables and queuing forced equalities. It agrees with the Python folding census on the complete sets of 11,126 principal images and 11,124 images reached by rank-increasing chains, including the source. The strict ledger has rank peak 3, raw peak 234 and cyclic peak 170.

~~~sh
set -o pipefail
work=/tmp/ac-r13-external
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round13_ac_disproof_principal.cpp -o "$work/principal"
c++ -std=c++17 -O3 experiments/round06_stable_proof_strict_verify.cpp -o "$work/strict-verify"
python3 -B experiments/round13_ac_disproof_external.py "$work/principal" "$work/strict-verify" \
  | diff -u results/round13_ac_disproof_external.json -
~~~
