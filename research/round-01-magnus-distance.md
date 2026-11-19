# Bounded ordinary and stable AC paths in finite Magnus quotients

2026-11-19. This note extends the [ordinary distance principle](research-b.md) to an explicit tower that also handles stable moves. It gives a quantitative equality of bounded reachability and a divergence criterion for counterexamples. The divergence question for AK(3) remains open here.

## Move metric

Write $F_r$ for the free group with basis $x_1,\ldots,x_r$. Use ordered $r$-tuples. Count an inversion, row swap, signed right multiplication by a distinct row, or conjugation by one signed basis letter as one move. For the stable metric, also count insertion or deletion of a singleton generator–relator pair as one move. Generator and row positions can be chosen independently. Surviving positions keep their relative order. Rank zero is allowed on a stable path. These metrics have the same reachability relations as the competition definitions. Arbitrary conjugation splits into generator conjugations, and swaps and signed multiplication can be compiled into the defining moves. [Official definitions](https://github.com/SAIRcompetition/Andrews-Curtis/blob/main/competition/tools/lean/AC.lean).

For $d\ge 1$, take $A_{r,d}=\mathbb F_2\langle X_1,\ldots,X_r\rangle/(\text{monomials of degree}>d)$, and let $J$ be its ideal of positive-degree terms. Define

$$
M_{r,d}:F_r\longrightarrow 1+J,\qquad x_i\longmapsto 1+X_i,
\qquad Q_{r,d}=M_{r,d}(F_r).
$$

The ideal satisfies $J^{d+1}=0$, so $1+J$ is a group with $2^{\dim J}$ elements and $Q_{r,d}$ is a finite 2-group. For $r=0$, use the trivial group. Truncation gives marked surjections from degree $d+1$ to $d$. Insertion at generator slot $g$ gives an injective map on the marked groups by reindexing variables to skip $g$. Its left inverse sets $X_g=0$ and relabels. Write $E_g$ for insertion composed with this deletion map, viewed as an endomorphism of $Q_{r,d}$. An element lies in the insertion image exactly when $E_g$ fixes it. [Background on the Magnus embedding in the pro-2 setting](https://roed314.github.io/gq2/paper/).

Use the same ordinary instructions on $Q_{r,d}^r$. A quotient deletion of row $i$ and generator $g$ requires that row $i$ equal $1+X_g$ and every other row be fixed by $E_g$. After deleting the row, apply the left inverse to the survivors. This is precisely the inverse of the specified quotient insertion. Truncation preserves both deletion tests. A quotient edge can appear before the corresponding free-group edge does at the same evaluated tuple.

## Detecting a surviving generator in a word

For a nonempty reduced word, write its successive maximal runs as

$$
w=x_{i_1}^{e_1}\cdots x_{i_t}^{e_t},\qquad e_j\ne 0,\quad i_j\ne i_{j+1}.
$$

For each $j$, set $a_j=2^{v_2(|e_j|)}$. Over $\mathbb F_2$, $(1+X)^{e_j}=(1+X^{a_j})^{e_j/a_j}$ as formal series. This holds for negative exponents by taking inverses. Its coefficient of $X^{a_j}$ is $1$, since the first-degree coefficient of $(1+T)^h$ is the parity of $h$, for positive or negative $h$. The monomial

$$
X_{i_1}^{a_1}\cdots X_{i_t}^{a_t}
$$

has coefficient $1$ in the full expansion of $w$. It has $t$ runs, which requires a positive-degree contribution from every factor, and the powers in those contributions are then forced. Its degree is at most $\sum_j |e_j|=|w|$. Therefore $M_{r,d}(w)\ne 1$ whenever $d\ge |w|$. Moreover, if $w$ involves $x_g$, the exhibited monomial contains $X_g$, so $E_g$ changes $M_{r,d}(w)$ at the same degree bound. Conversely a word omitting $x_g$ is fixed in every degree. For instance $x_g^{2^s}$ is invisible in degrees below $2^s$, so a single truncation can admit a spurious deletion.

## Bounded path lifting

Let the start be $U$ of rank $n$, the target $V$ of any prescribed rank, and $L\ge 0$ a move bound. Put $M=\max(2,\max_i|U_i|)$ and $H=\max(1,\max_i|V_i|)$, using zero for the inner maximum when a tuple is empty. Set $B=F_{L+2}M$ for Fibonacci numbers $F_1=F_2=1$. For every $d\ge B+H$, the following are equivalent, separately for each of the ordinary and stable instruction sets:

1. There is a free-group path from $U$ to $V$ of at most $L$ moves.
2. There is a path from $M_{n,d}(U)$ to the marked image of $V$ of at most $L$ moves in the degree-$d$ quotient graph.

First bound the lengths in any replay. Adjoin two dummy lengths $2,2$ to the list of current row lengths and let its two largest values be $a\ge b$. Each ordinary move changes at most one length, apart from a swap which preserves the list. A multiplication gives a new length at most $a+b$, a single-letter conjugation at most $a+2\le a+b$, and inversion preserves length. Insertion adds a length $1$, while genuine deletion discards a row and relabels the others. The new second-largest value is at most $a$. Thus after $t$ successful steps the two maxima are at most $F_{t+2}M,F_{t+1}M$. At most $n+L$ generator slots are ever needed.

A free path gives the quotient path by naturality. For the converse, take the instructions from any quotient path of at most $L$ moves and replay them in the free groups starting at $U$. After each step the free tuple projects to the given quotient tuple. At a deletion, the current free row $w$ proposed for removal satisfies $M_{r,d}(wx_g^{-1})=1$. The reduced difference has length at most $B+1$, so $w=x_g$. For every other row $v$, the quotient test $E_g(M_{r,d}(v))=M_{r,d}(v)$ and the generator detection argument force $v$ to omit $x_g$, since $d\ge B\ge |v|$. The free deletion is valid and commutes with projection. The same induction applies over any number of deletions. Finally each free endpoint row $w$ has length at most $B$ and agrees with $V_i$ in the quotient. The difference $wV_i^{-1}$ has length at most $B+H$, so it is trivial. This proves the equivalence, including the empty path.

## Consequences and scope

Let $D_d$ be shortest path length in the degree-$d$ graph, with infinity for disconnected tuples. It is nondecreasing in $d$ by truncation and bounded above by the free-group distance $D$. For each $L<D$, the lifting result implies $D_d>L$ for every $d\ge F_{L+2}M+H$. Consequently

$$
D=\sup_{d\ge 1}D_d
$$

holds for both metrics. For a normally generating tuple and the standard tuple of the same rank, each $D_d$ is finite even in the ordinary quotient graph. The images normally generate, and their abelianized tuples are Nielsen equivalent by the same integral row operations that turn the free abelianized generating tuple into the standard basis. Apply the finite AC theorem for rank at least two. At rank one, the only normally generating free relator is the basis letter or its inverse. Thus a genuine ordinary or stable counterexample would give unbounded distances inside this one fixed tower of finite 2-groups. Bounded distances imply an actual finite free path. [Borovik, Lubotzky and Myasnikov, Theorem 1.1](https://arxiv.org/pdf/1103.1295).

For AK(3), the inputs give $M=7,H=1$. Every degree $d\ge 7F_{L+2}+1$ is therefore exact for deciding the existence of a path of at most $L$ moves under the specified counting convention. This worst-case degree guarantee can be much larger than the degree needed to verify a given instruction list. At a proposed deletion one can split the verification into a singleton equality and a generator-absence test, or replay the free words directly. For a disproof via the quotient tower, the remaining task is to show a lower bound growing with $d$, with stable arguments controlling the rank-changing edges as well as the fixed-rank ones.

## Reproduction

The small-degree search gives exact distances to the ordered target $(x,y)$.

| Degree | Ordinary | Stable |
| ---: | ---: | ---: |
| 1 | 1 | 1 |
| 2 | 3 | 3 |
| 3 | 5 | 5 |
| 4 | 9 | 9 |
| 5 | 11 | 11 |

For degrees one through four, the stable search uses the ordinary distance as its move bound. A path between two rank-two endpoints with at most $L$ moves cannot exceed rank $2+\lfloor L/2\rfloor$, because each insertion must be matched by a deletion. The bidirectional search expands one complete layer at a time. Two disjoint explored balls of radii $a,b$ exclude paths of length at most $a+b$. The separate degree-five stable result uses the peak-rank normalization and the cut bound from the [stable-disproof track](round-01-stable-disproof.md#exact-degree-five-test-for-ak3). These small distances do not give a divergence bound.

Run `python3 -B experiments/round01_magnus_distance.py` to reproduce the [ordinary distances and direct stable searches](../results/round01_magnus_distance.json). The same command independently expands 5,180 nonempty reduced words through length five in ranks one through three, checking 15,036 generator incidences and the first detectable degree of an eighth power.
