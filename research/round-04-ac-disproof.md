# Round 04 · Ordinary Andrews–Curtis disproof

2026-11-19. All **7,200** folded four-lobe chains with single-letter links in the catalogue pass the two-copy primitive screen. They certify a bridge of length 17 and an exponential family of longer bridges outside the round-three three-lobe overgroup catalogue and its regular-language criterion.

## Four-lobe overgroups

Use uppercase letters for inverses. Put $p=x^3y^{-4}$ and $b=xyxy^{-1}x^{-1}y^{-1}$. A chain has ordered lobe labels $P,R,S,B$. The outer labels range over the seven rotations of $p$ and six rotations of $b$, respectively. Each middle label ranges over all 26 signed rotations of $p$ or $b$. Three individual letters $c,d,e$ connect consecutive lobes from left to right.

At a lobe labelled $w$, a link leaving its marked vertex must have a label outside $\{w[0],w[-1]^{-1}\}$. At an interior lobe the two outward link labels must also differ. This is exactly the condition that the chain already be folded. Its four circles and three connecting edges give rank four. With the left marked vertex as base the subgroup has basis

$$
P,\quad cRc^{-1},\quad cdS(cd)^{-1},\quad cdeB(cde)^{-1}.
$$

For distinct vertices $i,j$, take the folded join of the two copies rebased at $i,j$. When two independently conjugated elements of the source subgroup have intersecting axes, rebasing at any vertex of intersection puts their elements in the join of the corresponding two copies. If both use the same vertex, the source core suffices. If the axes are disjoint, the generated graph is their barbell. A cyclic primitive cannot cross its separating bridge, which would require both signs of a letter. A primitive confined to a lobe would imply that the corresponding original element is itself primitive up to conjugacy and inversion. Thus primitive absence in the source and in every rebased join certifies the entire two-conjugation-phase test. The argument works with rank-four source cores. [Round 02 two-copy proof](round-02-ac-disproof.md#finite-join-in-place-of-the-infinite-voltage-kernel), [Kapovich and Myasnikov on folding](https://arxiv.org/abs/math/0202285), [Parzanchevski and Puder on rank-two primitive words](https://arxiv.org/abs/1210.6574).

The native test builds every labelled graph and checks all inverse edges and each source-edge projection in every folded join. Its signed transition graphs use one sign of each generator and prohibit consecutive use of one of the two selected letters. The eight graphs for each source or join are acyclic. Every rank-two primitive conjugacy class has the required signed double-free form, so the result is an exact exclusion.

| Check | Count |
| --- | ---: |
| Folded four-lobe sources | 7,200 |
| Distinct-vertex joins | 2,358,360 |
| Rank-six joins | 2,424 |
| Rank-seven joins | 127,448 |
| Rank-eight joins | 2,228,488 |
| Joins requiring exact partial-map fallback | 0 |

The independent checker enumerates the link choices via missing directions, rather than scanning arbitrary link triples. It recovers the source census and the join count from the source sizes. It also folds the four basis words for nine chains and, for each pair of vertices, folds the eight rebased words anew. This rechecks 2,902 joins by topological sorting and replays 513,266 exact closed partial-map pair states. The positive control on the literal AK(2) core finds the three known primitive-containing joins. [Recorded counts and controls](../results/round04_ac_disproof_chains.json).

## A strict extension of the previous bridge language

Take the following chain:

| Item | Word |
| --- | --- |
| $P$ | xxxYYYY |
| $R$ | XXXyyyy |
| $S$ | XXyyyyX |
| $B$ | xyxYXY |
| $c,d,e$ | X,y,y |

Then $q_0=cRdSe=$ **XXXXyyyyyXXyyyyXy** is reduced. It is admissible as a bridge between the two original lobe rotations, since its endpoint directions fit the two outer lobes. It also reads from the left marked vertex to the right marked vertex in the certified chain. Thus $\langle P,q_0Bq_0^{-1}\rangle$ is contained in the chain subgroup. Explicitly, if $h_1,h_2,h_3$ are the three conjugated lobe basis elements displayed above, the second barbell generator is $h_1h_2h_3h_2^{-1}h_1^{-1}$.

This bridge contains $R$ as a contiguous subword, so it fails the round-three interior guard. Direct path evaluation finds zero readings of $q_0$ from all 10,788 starting vertices of the 552 literal three-lobe cores. Thus the four-lobe certificate genuinely extends the earlier three-lobe family. Containment of the barbell subgroup, even up to conjugacy, in one of those cores would induce a label-preserving path for the whole bridge. Every bridge of length below 17 compatible with the displayed four-lobe chain is still readable somewhere in the old catalogue. There is one such bridge at length three and four at length ten. The path enumeration therefore gives 17 as the first escape length in this particular chain. [Three-lobe construction and interior guard](round-03-ac-disproof.md).

For each $m\ge0$ define

$$
q=q_0 B e^{-1}
\left(\prod_{j=1}^m S d^{-1} R^{\epsilon_j} d\right) S e,
\qquad \epsilon_j\in\{-1,1\}.
$$

These labels follow a detour from the right marked vertex back to $S$ and then return to the right marked vertex. The folded incidence conditions and cyclic reduction of the lobe words ensure no cancellation. Each word still has the allowed first and last letters. The two choices of each block are distinct and have equal length. This gives $2^m$ distinct certified bridges of length $32+16m$, all preserving $q_0$ as a prefix. They remain unreadable in the old catalogue and fail the interior guard. The saved checker evaluates all 16 samples with $m=4$ and verifies that $qBq^{-1}$ closes at the left marked vertex in every case.

The conclusion excludes primitive production after the specified two conjugation phases and intervening Nielsen moves for these bridge families. Later unconstrained alternating phases and general signed bridges remain open.

## Reproduce

~~~sh
mkdir -p /tmp/ac-r04-four
c++ -std=c++17 -O3 experiments/round04_ac_disproof_chains.cpp -o /tmp/ac-r04-four/chains
/tmp/ac-r04-four/chains /tmp/ac-r04-four/exceptions.jsonl > /tmp/ac-r04-four/native.json
python3 -B experiments/round04_ac_disproof_chain_audit.py \
  /tmp/ac-r04-four/native.json /tmp/ac-r04-four/exceptions.jsonl \
  | diff - results/round04_ac_disproof_chains.json
~~~
