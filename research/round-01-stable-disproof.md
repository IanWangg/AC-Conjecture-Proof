# Round 01 · Stable Andrews–Curtis disproof

2026-11-19

Every shortest stable path to an unordered positive basis can be replaced by a path that performs all insertions first, carries out ordinary moves at that peak rank, and then performs all deletions. There is a quantitative restriction on how much the ordinary middle section must mix the added relators with the original ones. Both statements hold in free groups and in the finite characteristic-two Magnus quotients.

## Fixed-rank normalization

Use the instruction metric from the [Magnus distance note](round-01-magnus-distance.md). The ordinary moves are inversion, swap, signed right multiplication, and conjugation by a signed basis letter. Stable insertion and deletion use an isolated singleton relator and its generator. The two positions can be chosen independently, with surviving positions in their previous order. Use the same moves in the Magnus quotients, including the deletion tests in the [quotient definitions](round-01-magnus-distance.md). The free-group insertion convention agrees with the competition definitions. [Official stable definition](https://github.com/SAIRcompetition/Andrews-Curtis/blob/main/competition/tools/lean/AC.lean).

Let $R$ have rank $n$. The unordered positive basis at rank $n$ consists of the $n!$ relator tuples obtained by permuting the standard tuple. Define $A_k$ to be the minimum ordinary distance from $R$ with $k$ appended isolated pairs to the unordered positive basis of rank $n+k$. Here $A_k$ is taken in a single free group or at a single degree of the Magnus tower, with the base tuple projected as appropriate. Write $S_K$ for the stable distance from $R$ to the unordered positive basis of rank $n$ under the rank cap $n+K$. Distances take the value infinity if no path exists.

**Theorem.** For $0\le K\le\infty$,

$$
S_K=\min_{0\le k\le K} (2k+A_k).
$$

**Proof.** To obtain the upper bound, append $k$ isolated pairs and follow an ordinary path to a permutation of the full positive basis. Delete the $k$ added generators and their singleton rows in any order. This uses $2k$ rank-changing moves.

For the lower bound, take any stable path and let $N=n+k$ be its peak rank. Keep $N$ fixed generator slots and $N$ fixed row slots. Start with the ordinary tuple consisting of $R$ and the $k$ appended isolated pairs. At each step, map the current active generators and active rows injectively to these slots with two independent maps. Read the active relators in the mapped basis. The unused generators are paired bijectively with unused rows, each containing the corresponding generator as a singleton. An insertion activates one such pair and changes the two indexing maps. A deletion deactivates the pair whose row is already an isolated singleton. Neither instruction changes any word in the ambient rank-$N$ tuple. An ordinary instruction lifts literally to the assigned slots, with row swaps interpreted as moves in those slots. This maintains the description inductively.

The relevant embeddings in the Magnus tower are literal substitutions of distinct variables. They are injective on the truncated algebras by linear independence of the indexed monomials, and thus also on their marked subgroups. At a deletion, the surviving relators lie in the image of the chart omitting the deleted variable by the required deletion test. Changing the active chart at either type of rank move therefore preserves the same rank-$N$ tuple. This argument also covers relabeling at nonterminal insertion positions.

The final active rows are the active singleton generators in some order. The inactive rows are the remaining singleton generators. Thus the lifted ordinary path ends at a permutation of the rank-$N$ positive basis. The original stable path had at least $k$ insertions to reach $N$ and at least $k$ deletions to finish at $n$. Its length is at least $2k+A_k$, as required. ∎

For an ordered standard target, write $S_K^{\rm ordtarget}$ for the corresponding stable distance. Appending at most $n-1$ row swaps gives

$$
S_K\le S_K^{\rm ordtarget}\le S_K+n-1 .
$$

The theorem concerns a uniform rank cap for the entire path and imposes no bound on the words in a free-group path.

A shortest stable path to the unordered basis already has exactly $k$ insertions and $k$ deletions if its peak rank is $n+k$. Any additional pair of rank changes would make the normalization strictly shorter. Thus along any such shortest path all insertions precede deletions, though ordinary moves can occur at intermediate ranks.

## Necessary relator mixing at the peak rank

Assume that $R$ normally generates the ambient free group, so its exponent-sum matrix is unimodular. The degree-one mod-two row vectors of the appended tuple are a basis, supported on the original variable block and the separate singleton auxiliary variables. Every elementary move preserves the basis property. This also holds in the free-group case using the degree-one mod-two image.

Suppose a finite minimum $S_K=2k+A_k$ is attained with $k\ge1$. Consider a shortest ordinary middle section. A row swap can always be pushed to the end by reindexing the remaining moves, where it is absorbed by the unordered target. Thus a shortest ordinary section needs no explicit row swaps. Fix the row identities throughout that section.

**Lemma.** For each nonempty subset $T$ of the auxiliary rows, at least three right multiplications have one index in $T$ and the other outside $T$.

**Proof.** Initially the row spans of the two blocks in degree one are complementary coordinate subspaces $V_T$ and $V_{T^c}$. Kill the generators originally corresponding to rows of $T$ and erase those rows. If all crossing multiplications point outward, with donor in $T$ and receiver outside, the projected rows of $T$ remain identities. They begin as identities and never receive outside donors. Crossings therefore induce no changes in the retained rows, and this is an ordinary path on the remaining generators. At the endpoint the $T$ rows are singleton generators with degree-one vectors in $V_T$, hence exhaust exactly those generators. The retained rows give the unordered positive basis after projection. If all crossings point inward, the retained rows never use any donors in $T$. Moreover their degree-one span remains $V_{T^c}$, so they again end at exactly the correct singleton generators. The argument without crossings is included in both cases. A conjugation by an erased generator becomes an identity instruction. These projections work in the free groups and the Magnus algebras. Each yields a padded path with $|T|$ fewer auxiliary pairs, with no increase in its ordinary length, contradicting the stable minimum.

It remains to exclude two crossings in opposite directions. Before the first crossing, the row spans are the original two coordinate subspaces. The first receiver block replaces one of its row vectors $v$ by $v+u$ for a nonzero donor $u$ in the other coordinate subspace. Its new span projects bijectively onto the original receiver coordinate subspace, with a nonzero component in the other block. Such a span cannot be a coordinate subspace. Indeed, a coordinate subspace projecting bijectively onto the original receiver span must equal that original span. All later moves within the receiver block preserve its row span, and the second crossing targets the other block. The final span of this block would still be noncoordinate, contradicting the singleton basis endpoint. ∎

Make a multigraph with one vertex for each auxiliary row and one vertex for the whole original block. Add an edge for each right multiplication between different vertices. In particular, repeated uses contribute separate edges. Each cut that separates a nonempty auxiliary subset from the original block has size at least three. This gives degree at least three for every vertex, including the original block, and hence

$$
A_k\ge \left\lceil\frac{3(k+1)}2\right\rceil
\quad\text{and}\quad
S_K\ge 2k+\left\lceil\frac{3(k+1)}2\right\rceil
$$

for any $k\ge1$ realizing the minimum. In particular a shortest path of length $L$ has a normalized representative using only $k\le\lfloor(2L-3)/7\rfloor$ added pairs if $k>0$. The inequality is tied to an optimizing rank in the stable formula. A fixed-rank search performed with unused padding need not satisfy the crossing bound.

## Counterexample criterion in the tower

Let $A_{k,d}$ be the fixed-rank ordinary distance in degree $d$. For fixed $k$ the values are nondecreasing in $d$, since higher-degree quotient paths truncate. The rank-$n+k$ free distance to the unordered basis equals $\sup_d A_{k,d}$. The bounded-path lifting theorem applies uniformly to every target permutation, since all these targets have maximum relator length one. [Bounded path lifting](round-01-magnus-distance.md#bounded-path-lifting).

For a specific normally generating tuple $R$, the following are equivalent.

1. $R$ is a stable counterexample in the ambient free group.
2. The unordered stable quotient distances are unbounded as $d$ increases.
3. For every fixed $k\ge0$, the sequence $A_{k,d}$ diverges as $d$ increases.

A bounded sequence for any single $k$ gives a bounded stable sequence by the formula. Conversely, if all fixed-$k$ sequences diverge, fix a proposed stable bound $L$. Only $k\le\lfloor L/2\rfloor$ can contribute to the minimum. Each term for those finitely many ranks eventually exceeds $L$, hence so does the minimum. The free-path formulation follows from bounded-path lifting and from the ordered-target comparison. Thus ordinary lower bounds can be developed separately for each fixed padded rank. A divergence claim at rank two alone cannot decide stable triviality for AK(3).

## Exact degree-five test for AK(3)

A bit-packed bidirectional breadth-first search gives the following distances and exclusions at degree five. For the unordered searches, sorting the relator rows quotients by relator permutation. The ordinary move operations are equivariant under row permutation, so this preserves the distance to the unordered endpoint. Any path of row orbits lifts by permuting the indices of each successive move to match the current representative.

| Extra isolated pairs | Target convention | Ordinary distance or exclusion |
| ---: | --- | ---: |
| 0 | Unordered | 10 |
| 0 | Ordered | 11 |
| 1 | Unordered | Greater than 8 |
| 2 | Unordered | Greater than 6 |

For a stable path of length at most 10 that minimizes the unordered distance, the cut bound excludes $k\ge3$, since its cost would be at least 12. The two padded searches exclude $k=1,2$ at cost at most 10. Thus the unordered stable distance is exactly 10, attained at $k=0$. Any ordered stable path of length at most 10 would have to attain that same unordered minimum. It would have peak rank $n$ and no rank moves by the equality case of normalization. The ordered rank-two search excludes such a path. The ordered stable distance is therefore exactly 11. This is a finite-quotient lower bound on the free-group stable distance. It does not give divergence.

The negative tests visit 277,751 and 189,669 states in the two complete rank-three balls and 74,434 and 63,539 in the two rank-four balls. Their explored radii sum to the tested bounds. The search takes one full layer from the smaller frontier until the balls meet or the bound is exhausted. The main agent separately reproduced the degree-five unordered searches using an independent polynomial-set representation, as well as the rank-two ordered result.

```sh
python3 -B experiments/round01_stable_disproof_search.py | diff - results/round01_stable_disproof_search.json
```
