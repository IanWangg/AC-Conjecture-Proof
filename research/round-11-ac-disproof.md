# Proper-overgroup exclusion at the wrong Wirtinger waypoint

2026-11-19. The normal closure of the marked wrong Wirtinger subgroup in **every proper overgroup** is primitive-free in the ambient free group. A known-trivial AK(2) marking also satisfies this property, and one ordinary conjugation separates it from a marking with an explicit primitive in a proper-overgroup normal closure. This proves that proper-overgroup primitive exclusion can change along an ordinary AC path and can hold 44 strict moves before reaching a basis. [Exact census, kernel factorization and strict replays](../results/round11_ac_disproof_wirtinger.json).

## Wrong Wirtinger marking

The pair `(XXYYxyyyxYY, XXYxyXyxYY)` is an ordinary AK(3) waypoint reached by 105 strict elementary instructions. Let $H$ be its row subgroup. The [Round 10 reduction](round-10-ac-disproof.md#reducing-arbitrary-proper-overgroups-to-a-finite-fringe) reduces primitive exclusion in $\langle\!\langle H\rangle\!\rangle_G$ for every proper $G<F(x,y)$ containing $H$ to a finite test on folded principal images of the based core. The image is a free factor of the target core. The outside-edge characters and sign purity of a cyclic primitive force any candidate loop into the image with trees attached. Retraction then puts a conjugate of the candidate in the normal closure inside that principal image. The argument applies to an infinitely generated $G$ by restricting to the finitely many conjugators in a proposed normal-closure expression. [Ordinary entry ledger](../certificates/round10_stable_proof_wirtinger_wrong.json).

The 13-vertex source has 701 principal images including the ambient rose. The original core passes the exact partial-map-pair exclusion. All but two other proper images admit rank-increasing chains. The code checks inverse Nielsen markings and runs exact context-free saturation for all eight signed-double-free languages in each resulting free quotient. The 697 cases all exclude nonempty neutral cyclic paths.

| Rank | Wrong Wirtinger principal images | Exclusion method |
| --- | ---: | --- |
| 2 | 2 | Source by map pairs. The ambient rose is omitted. |
| 3 | 35 | Free quotient |
| 4 | 232 | 230 free quotients and two integer voltage checks |
| 5 | 321 | Free quotient |
| 6 | 108 | Free quotient |
| 7 | 3 | Free quotient |

The two exceptions are three-vertex covers of the ambient rose. Use their spanning-tree chord bases in the order below. Each character kills both source rows. For each sign pattern choose the character for the specified forbidden double. A kernel loop has zero voltage for every such character, so the automata can use different characters.

| Chord basis in order | Character when forbidding the signed $x$ double | Character when forbidding the signed $y$ double |
| --- | --- | --- |
| `XX, YY, xyX, yxY` | `(0,3,-2,-1)` | `(1,0,0,-1)` |
| `yX, YX, xxx, Xyx` | `(1,-2,0,2)` | `(1,1,-2,0)` |

For each cyclic strongly connected component of size $N$, the replayer checks integer potentials satisfying $p(v)-p(u)\le N\sigma w(u,v)-1$ on every transition, where $w$ is its voltage and $\sigma\in\{1,-1\}$. Summing around a nonempty closed path forces nonzero voltage. The potential constructor and the independent Warshall reachability verifier agree on the cyclic components and verify 72 inequalities per cover. Every cyclic primitive uses one sign of each generator that occurs and forbids at least one of the two doubles, so the eight automata suffice. The resulting universal exclusion at this waypoint has the same scope as at the original and the energy-17 markings. [Verifier and replay](../experiments/round11_ac_disproof_wirtinger.py).

## Ordinary-trivial controls

For the corrected Wirtinger pair `(XXYYxyXyyxYY, XXYYxyyyxYY)`, the exact positive check finds genuine primitive kernel elements in all 154 proper principal images. The source rows $r_0,r_1$ already give $r_0^{-1}r_1=$ `yyXYYxyyxYY`, a conjugate of `x`. In the rank-three proper overgroup obtained by adjoining `Y`, the checker also factors the primitive `XYYxyyx` as `YY r0^-1 r1 yy`. The corrected pair has a verified 73-instruction ordinary exit to the basis. [Corrected pair ledger](../certificates/round10_stable_proof_wirtinger_correct.json).

For AK(2), write $u=$ `xxYYY`, $v=$ `xyxYXY`, and $c=$ `xYX`. The eight-vertex row subgroup $\langle u,v\rangle$ has no ambient primitive. The five-vertex rank-three subgroup $\langle u,v,c\rangle$ is proper, and

\[
u^{-1}cvu^{-1}c^{-1}=\texttt{yyXyyXyX}
\]

is an ambient primitive. Its cyclic class is the Euclidean word with letter counts $(3,5)$ on `X,y`. The factorization is an actual ordinary path exposing that row. Invert $u$, right-multiply $v$ by $u^{-1}$, conjugate the second row by $c$, and right-multiply the first row by the second. The code checks the six-instruction expansion with three single-letter conjugations. At the level of the word conjugation the path uses $c$. The expansion uses both ambient generators. The initial AK(2) ranked census has a second primitive-positive graph and one rank-four neutral path whose primitive status this test leaves unresolved.

The published AK(2) trivialization starts by inverting $u$ and then conjugating that row by `Y`. Inversion preserves its row subgroup. After the conjugation the pair is `(yyXXy, xyxYXY)`. Its nine-vertex source and all 46 higher-rank proper principal images satisfy primitive exclusion. There are 16 rank-three, 25 rank-four and five rank-five images, all with exact free quotients. Replaying the remaining 44 instructions reaches `(x,y)`. Adjoining `y` to the exclusion-side marking recovers a proper common overgroup of both markings, and adjoining `xYX` after `y` folds to the full rose. This identifies a concrete transition in the primitive-kernel property while respecting the cumulative conjugator restriction from the exclusion side. [AK(2) ledger](../certificates/n_ak2_cyclic13.json).

~~~sh
python3 -B experiments/round11_ac_disproof_wirtinger.py | diff - results/round11_ac_disproof_wirtinger.json
~~~
