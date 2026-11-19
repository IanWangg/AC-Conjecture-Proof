# Round 05 · Ordinary Andrews–Curtis disproof

2026-11-19. A third independent-conjugation phase is excluded for 42 intersecting first placements of the AK(3) relators, 42 first one-edge barbells, and two explicit overgroups. The middle conjugation may have an arbitrarily long geodesic bridge provided its unread gap in the indicated source core is bounded. A five-lobe overgroup extends this result to bridges unreadable throughout the round-four catalogue.

## Reducing the middle phase to finitely many overgroups

Put $F=F(x,y)$, $p=x^3y^{-4}$ and $b=xyxy^{-1}x^{-1}y^{-1}$. Use uppercase letters for inverses. Let $\Gamma$ be the folded core of the pair after its first placement by independent conjugations, or any fixed folded overgroup core. Nielsen moves between conjugations preserve the generated subgroup, so both words before the second conjugation belong to the group represented by $\Gamma$.

Place the two resulting axes in the Cayley tree. If they intersect, a common base at a vertex of intersection gives cyclic words $P,Q$ whose loops lift to some vertices $a,b$ of $\Gamma$. Their subgroup is contained in the folded wedge of $\Gamma_a,\Gamma_b$. If the axes are disjoint, use the common marking $(P,qQq^{-1})$, where the reduced word $q$ labels their shortest connecting segment. Start reading $q$ from $a$ and $q^{-1}$ from $b$ in $\Gamma$. If the two readable segments cover $q$, cut at any common position. Otherwise take the full readable segments. In either case write $q=u w v^{-1}$, where $u$ reads from $a$ to $a'$ and $v$ reads from $b$ to $b'$. In the first case $w$ is empty. In the other case neither the first letter of $w$ at $a'$ nor the inverse of the last letter of $w$ at $b'$ reads in $\Gamma$. Call $|w|$ the unread gap for these choices of loop lifts.

Conjugation by $u^{-1}$ now places the pair in the subgroup represented by two copies of $\Gamma$ based at $a',b'$, with a connecting path $w$. For $w$ empty this is the folded wedge. For $w$ nonempty the endpoint directions are absent and the bridge is reduced, so the two copies and the bridge already form a folded graph. This proves containment because the two rows are exactly $u^{-1} P u$ and $w v^{-1}Qv w^{-1}$. Enumerating this menu for a prescribed gap cap covers every placement with some choice of lifts satisfying the cap. [Stallings folding and subgroup inclusions](https://arxiv.org/abs/math/0202285).

Apply the round-two two-copy criterion to each middle overgroup. Every intersecting third pair is contained up to conjugation in a wedge fold of two copies rebased at vertices of that overgroup. For disjoint third axes, any cyclically reduced loop crossing the resulting separating bridge uses both orientations of some generator and therefore cannot be primitive. A primitive loop confined to a lobe would already give a primitive in the middle overgroup. A trivial row leaves only the cyclic case. This excludes a primitive both immediately after the third conjugation and after an arbitrary Nielsen suffix. [Two-copy criterion](round-02-ac-disproof.md#finite-join-in-place-of-the-infinite-voltage-kernel), [rank-two primitive classes](https://arxiv.org/abs/1210.6574).

## Complete finite census

Each row counts literal placements and graph cases with their incidence data. Isomorphic graphs from different cases are included. The middle catalogue at gap zero uses the core itself and its wedges at all unordered pairs of distinct vertices. A nonempty gap has a missing direction at both ends. Its two orientations define the same unbased graph, so the test keeps one of $(a,b,w)$ and $(b,a,w^{-1})$. The last screen includes each middle graph and all its distinct-vertex wedge folds.

| First source core or catalogue | Middle gap cap | Middle overgroups | Final graph checks |
| --- | ---: | ---: | ---: |
| All 42 intersecting first rotation pairs | 4 | 84,874 | 24,161,784 |
| All 42 first one-edge barbells | 4 | 124,278 | 48,578,106 |
| Round-four explicit four-lobe chain | 4 | 11,872 | 18,536,624 |
| Five-lobe chain below | 2 | 2,211 | 4,684,791 |
| Total | | 223,235 | 95,961,305 |

All eight signed double-free transition graphs are acyclic in each of the final cases. For each permissible signing of $x,y$, the transitions prohibit a double of one of the two letters. A cyclically reduced rank-two primitive gives a closed walk in one of these graphs. Independent Python code recomputes the first and middle census through bouquet folds and missing-direction counts. It uses fresh bouquets and topological sorting to recheck 1,140 sampled final joins. Separate exact certificates replay 28,090 closed partial-map states. [Counts and independent replays](../results/round05_ac_disproof_third_phase.json).

For an example with a long middle bridge, start with the one-edge barbell $P=$ **YYYYxxx**, $B=$ **xyxYXY**, and connector $x$. Use the middle bridge

$$
q_m=x(BX P x)^m YYx,\qquad m\ge 0.
$$

The prefix before the final $YYx$ follows the connecting edge and winds around the lobe circles, returning to the right marked vertex. That vertex has no outgoing $Y$. In the reverse direction the final inverse $X$ goes from the right marked vertex to the left, which has no outgoing $y$. The unread gap is exactly $YY$, although $|q_m|=4+15m$. The first and last letters meet both lobe endpoints without folding. Thus the placement is realized by a second conjugation of the braid relator and can be followed by any third conjugation in the exclusion theorem.

## First bridges outside the four-lobe catalogue

Take ordered labels

$$
(P,R,S,T,B)=(\texttt{xxxYYYY},\texttt{XXXyyyy},\texttt{XXyyyyX},
\texttt{xyxYXY},\texttt{YXYxyx})
$$

and connecting edges $c,d,e,f=X,y,y,X$. All outward directions at each attachment are distinct. A reduced path from the first marked vertex to the last reads

$$
q_0=cRdSeTf=\texttt{XXXXyyyyyXXyyyyXyxyxYXYX}.
$$

The independent checker finds no reading of $q_0$ from any of the 187,848 starting vertices of the 7,200 four-lobe cores. Its 23-letter prefix has 16 such readings. Containment even up to conjugacy in an old core would map the folded first barbell into that core, so would give a reading of its bridge. In the new chain the shortest endpoint-compatible bridges outside the old catalogue have length 17, and exactly four such bridges occur at that length. One is **XXXXyyyyyyxyxYXYX**. The saved strict replays give the length-17 and length-24 placements from AK(3) by 20 and 27 single-letter conjugations respectively. The terminal braid label is the rotation obtained by moving its initial **xyx** to the end.

For each $m\ge 0$, let

$$
q=q_0 B f^{-1}\left(\prod_{j=1}^m T^{\epsilon_j} f B f^{-1}\right)T f,
\qquad \epsilon_j\in\{-1,1\}.
$$

The path follows a detour along the two right lobes and returns to the terminal marked vertex. Both choices of each $T^{\epsilon_j}$ attach without cancellation. The choices give distinct words because the two lobe orientations have distinct outgoing labels. There are $2^m$ reduced first bridges of length $38+14m$, all with the unreadable prefix $q_0$. Their barbells lie in the five-lobe core, so the middle-gap-2 third-phase result applies.

## Limits and control

The AK(2) barbell with lobes **xYYYx**, **yxYXYx** and bridge **y** passes the earlier two-copy criterion at all 55 pairs. The new iteration detects 114 primitive-containing graphs at middle gap zero, and 28 at middle gap one. Fresh bouquet folding reproduces a middle core with no primitive and a final wedge containing **xYxYYxYY**. This primitive is the second coordinate of the positive Nielsen program **RLRL** in the basis **(x,Y)**. The example is a limitation of the iterated overgroup criterion. A positive overgroup can contain words outside the actual final two-generated subgroup.

From the literal folded AK(3) core the single and double zero-gap menus have 46 and 6,301 cases, each with an acyclic signed test. This excludes a primitive after an arbitrary Nielsen prelude, a first conjugation with gap zero, and a second arbitrary conjugation. The triple menu has 2,804,905 cases. Among them 2,761,897 pass the signed test, 5,860 pass the exact partial-map test, and 37,148 contain a primitive. No case reaches the fallback budget. The literal source has ten vertices. In the independent numbering by breadth-first $x,X,y,Y$ traversal, use vertex pairs $(0,1),(0,1),(0,19)$ to form successive rebased joins. The transport paths from vertex zero to the second vertex are **x**, **x**, and **XXyx**. Refolding the rebased bouquet words gives intermediate ranks four and six, both primitive-free, and then the entire ambient rose. Thus retaining the rebased overgroups of all elements loses the distinction between the actual rank-two trajectories in this third menu.

For AK(3) the exclusion concerns the specified first placements and the bounded unread middle gap. Arbitrary first placements, unrestricted middle gaps and later alternating phases remain open.

## Reproduce

~~~sh
mkdir -p /tmp/ac-r05-third
c++ -std=c++17 -O3 experiments/round05_ac_disproof_third_phase.cpp -o /tmp/ac-r05-third/scan
for mode in rotation short four; do
  /tmp/ac-r05-third/scan "$mode" 4 "/tmp/ac-r05-third/$mode.exceptions.jsonl" \
    > "/tmp/ac-r05-third/$mode.json"
done
for mode in five ak2_barbell; do
  /tmp/ac-r05-third/scan "$mode" 2 "/tmp/ac-r05-third/$mode.exceptions.jsonl" \
    > "/tmp/ac-r05-third/$mode.json"
done
c++ -std=c++17 -O3 experiments/round05_ac_disproof_literal.cpp -o /tmp/ac-r05-third/literal
/tmp/ac-r05-third/literal /tmp/ac-r05-third/literal.exceptions.jsonl \
  > /tmp/ac-r05-third/literal.json
python3 -B experiments/round05_ac_disproof_third_phase_audit.py /tmp/ac-r05-third \
  | diff - results/round05_ac_disproof_third_phase.json
~~~
