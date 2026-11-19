# Round 02 · Stable Andrews–Curtis disproof

2026-11-19. A cut of auxiliary rows that receives a single multiplication can be eliminated in free groups, without prescribing which generators its rows carry at the end. A singleton cut also admits this elimination in the characteristic-two Magnus quotients. The compilation can lengthen the ordinary section. The separate exact search uses the earlier length bound and obtains degree-six stable distances **12 to the unordered basis and 13 to the ordered basis**.

## One-incoming elimination

Use the move metric and peak-rank normalization of the [first round](round-01-stable-disproof.md). Consider the fixed-rank ordinary middle section from a tuple padded with $k$ isolated generator–relator pairs to a permutation of the positive standard basis. Absorb row swaps by changing later row indices. Fix a nonempty subset $T$ of the auxiliary row slots. Write $A$ for the marked generators in those slots at the start, and $B$ for the marked generators in those slots at the end. Thus $|A|=|B|=|T|$.

An incoming multiplication has its receiver in $T$ and its donor outside $T$. Suppose exactly one such move changes $p$ into $p'=p q^\varepsilon$, where $\varepsilon=\pm1$. Until this move the normal closure of the $T$ rows is constant, since inversions, conjugations and multiplications within $T$ preserve it. Outgoing multiplications also leave it unchanged. Thus just before the move their normal closure is $\langle\!\langle A\rangle\!\rangle$. The same argument backward from the end gives normal closure $\langle\!\langle B\rangle\!\rangle$ just after the move. Project the first section by killing $A$ and the last section by killing $B$, discarding the $T$ rows in both cases. Each retained move survives or becomes the identity. In particular an outgoing multiplication is killed by its section's projection.

Write $q_A,q_B$ for the images of the unchanged donor in the two charts. At the critical move, the other $T$ rows vanish in both charts. The image of $p'$ is $q_A^\varepsilon$ in the first chart. The image of $p$ is $q_B^{-\varepsilon}$ in the second chart. Taking images of the two normal-closure equalities gives

$$
\langle\!\langle q_A\rangle\!\rangle
 =\langle\!\langle B\setminus A\rangle\!\rangle,\qquad
\langle\!\langle q_B\rangle\!\rangle
 =\langle\!\langle A\setminus B\rangle\!\rangle .
$$

In free abelianization, the image of a one-element normal closure is cyclic and a subset of the remaining marked generators spans a coordinate sublattice of the same cardinality. Therefore each difference has size at most one. When $A=B$, both projections coincide and concatenate directly. Otherwise write $A\setminus B=\{a\}$ and $B\setminus A=\{b\}$. The free-group Magnus normal-closure theorem makes $q_A$ conjugate to $b^{\pm1}$ and $q_B$ conjugate to $a^{\pm1}$. [Bogopolski and Sviridov, Theorem 1.1](https://msp.org/gtm/2008/14/gtm-2008-14-004s.pdf).

Identify the second chart with the first by renaming its surviving $a$ to $b$ and leaving common generators fixed. The two images of each unchanged retained row agree modulo $\langle\!\langle b\rangle\!\rangle$, because killing $b$ after reindexing makes the two projections identical. Normalize the donor in each chart to $b$ by inversion and conjugation. Keeping that donor, multiply each other row by a product of conjugates of $b^{\pm1}$ to change it to its second chart image. Undo the second donor normalization and follow the projected last section. The resulting ordinary path dispenses with all $|T|$ padded pairs in the cut. One **outgoing** multiplication is handled by reading the path backward, compiling with the two charts in opposite order, and reversing the result. This joins the projected endpoints with the remaining markings identified as above. The initial tuple in the forward direction retains all original marked generators because $A$ consists of auxiliaries.

### Singleton cuts in finite Magnus quotients

The same proof works in the degree-$d$ Magnus quotient when $|T|=1$. Before the update the sole row is literally conjugate to $a^{\pm1}$, because its only earlier changes were conjugations and inversions. After the update it is literally conjugate to $b^{\pm1}$, by running its subsequent changes backward. Thus the donor conjugacies follow directly from the update in the two charts. In a Magnus chart the kernel of a marked generator deletion is the normal closure of that generator. Every element is represented by a word in the marked generators. Modulo their deleted generator, the word equals its evaluation with that letter set to the identity, which is the specified quotient projection. This justifies the same donor corrections. The proof avoids a Magnus normal-closure theorem in the finite quotient.

The finite proof for singletons does not supply the multirow donor conjugacies. For example the rank-one degree-four Magnus group is cyclic of order eight and its generator $x$ and $x^3$ have the same normal closure, while $x^3$ is neither $x$ nor $x^{-1}$.

## Padding rank and length are different optimizations

Suppose the least feasible number of padded pairs is $k>0$. In a free-group path at that padding rank, every nonempty auxiliary cut requires at least two incoming and at least two outgoing multiplications. A zero-direction cut is removable by the direct projection of round one. A one-direction-count cut is removable by the argument above. Consequently all $k+1$ vertices of the contracted incidence multigraph have degree at least four, so its ordinary section uses at least $2k+2$ crossing multiplications and the full normalized witness has length at least $4k+2$. This statement minimizes $k$ for feasibility, allowing the ordinary section to be arbitrarily long.

For an overall **length** minimizer the previous bound of three crossings per cut still applies. The new argument gives a further restriction on equality: an exactly-three-crossing free-group cut must exchange one marked generator between blocks, since otherwise the splice uses the same chart and removes padding with no increase in ordinary length. The same restriction holds for an exactly-three-crossing singleton in the Magnus quotients. The changed-chart proof has no length bound in terms of the crossing count alone.

There is a separate one-move addition to both incidence bounds in the free group when the original tuple generates a proper subgroup as an ordinary group. Every padded start also generates a proper subgroup, as witnessed by the retraction killing the padding. Inversions and multiplications preserve the subgroup generated by all rows, and the final basis generates the whole ambient group. There must therefore be at least one conjugation in addition to all the counted crossing multiplications. At feasible positive minimum padding rank the normalized witness length is at least $4k+3$. At a length-minimizing positive rank, the lower bound is $2k+\lceil 3(k+1)/2\rceil+1$.

After both donor normalizations, the chart switch for each other retained word admits a linear-length implementation. For an ambient word of length $m$, let $u_j,v_j$ be the two images of its $j$th letter. Each pair is equal or differs by insertion or deletion of a signed $b$. Process the positions in order with current expression $u_j\cdots u_m v_1\cdots v_{j-1}$. For a common nonidentity letter, conjugate by its inverse to move it from the front to the end. For an insertion, right multiply by the normalized signed donor. For a deletion, first move the front letter to the end and cancel it by signed multiplication. Identities take no steps. The resulting expression is $v_1\cdots v_m$ after at most $2m$ moves on this row. The identity of expressions holds even if intermediate free reductions cancel letters. The total bound adds the two donor normalization costs to twice the sum of the other retained word lengths at the switch.

To see the cost at a single switch, take an integer $M\ge1$ and use the padded rank-three tuple $(x,x^M y,z)$, with only the last slot in $T$. Its unique incoming move occurs at

$$
(z^{-1}x,z^M y,z)
 \ \longrightarrow\ (z^{-1}x,z^M y,x).
$$

Reach the left tuple by multiplying the first row by $z^{-1}$ and conjugating it to $z^{-1}x$. Then change each $x$ in the second row to $z$, using a signed conjugate of the first row while restoring it after each use. After the displayed move, the first row multiplied by the inverse of the last becomes $z^{-1}$. Invert it and use it to remove all the $z$'s in the second row. This reaches $(z,y,x)$. The path has exactly two outgoing and one incoming multiplications. Projecting on either side of the displayed move and identifying the surviving $z$ with $x$ gives $(x,y)$ and $(x^{-1},x^M y)$. Any strict path between these projected switch states has length at least $\lceil\log_2 M\rceil$, since the maximum absolute exponent coordinate starts at one and can at most double per move. This is a lower bound for joining the switch states. The example leaves open how short a different compilation of the entire path might be. [Replay controls](../results/round02_stable_disproof_search.json).

## Exact finite-quotient distances

Use the bit-packed arithmetic and bidirectional search from [round one](round-01-stable-disproof.md#exact-degree-five-test-for-ak3). A full search on each side expands breadth-first layers. Disjoint explored balls with radii $s,t$ exclude paths of length at most $s+t$. The unordered mode quotients by all relator permutations, which preserve every move type.

| Magnus degree | Padded pairs | Target | Ordinary distance or exclusion |
| ---: | ---: | --- | ---: |
| 6 | 0 | Unordered | 12 |
| 6 | 0 | Ordered | 13 |
| 6 | 1 | Unordered | Greater than 10 |
| 6 | 2 | Unordered | Greater than 8 |
| 6 | 3 | Unordered | Greater than 6 |
| 7 | 0 | Unordered | Greater than 13 |
| 8 | 0 | Unordered | Greater than 13 |

The rank-three, rank-four and rank-five negative degree-six tests exhaust respectively $5{,}856{,}426/3{,}432{,}720$, $2{,}510{,}430/1{,}966{,}076$, and $273{,}806/242{,}446$ visited states on the two sides. If the unordered stable distance were at most 12, take a minimizing normalization. By the round-one bound $2k+\lceil 3(k+1)/2\rceil$, $k\ge4$ already costs at least 16. The computed exclusions rule out $k=1,2,3$ at cost at most 12. Thus the unordered stable distance is exactly 12 and every shortest path to that target has peak rank two. Such a shortest path has no rank changes by the equality case of peak-rank normalization. The ordered ordinary result then implies ordered stable distance exactly 13.

The degree-six padded exclusions persist at every higher degree by truncation. The unpadded degree-seven exclusion, combined with the same length argument, gives a stable distance of at least 13 at degree seven and hence at every higher degree. This is a lower bound in the tower and in the free group. A proof of divergence is still missing.

Run `python3 -B experiments/round02_stable_disproof_search.py --workers 6 | diff - results/round02_stable_disproof_search.json` from the repository root. The searches include the chosen instruction metric and use considerable memory at rank three. The default runs the same tests sequentially. The `--controls-only` flag replays only the chart-switch controls.

[Search implementation](../experiments/round02_stable_disproof_search.py), [recorded results](../results/round02_stable_disproof_search.json).
