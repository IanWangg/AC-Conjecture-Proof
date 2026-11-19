# Exact endpoint test for one-donor chart splices

2026-11-19. The one-donor descent theorem extends to excursions that make nontrivial outgoing changes in the common quotient and later cancel them. For the 148-move rank-three cap-23 ledger, even this stronger criterion cannot compile the route to its selected intrinsic pivot. A different pivot does give a strict ordinary projection of the whole ledger. The obstruction concerns the prescribed projection of this ledger. The intrinsic endpoint also has an independent ordinary connection through the verified cap-29 catalogue and an ambient automorphism. [Round-six construction](round-06-stable-proof.md), [ordinary transport](../results/round07_automorphism_transport.json), [Panteleev–Ushakov, Corollary 3.8](https://arxiv.org/abs/1609.00325).

## Necessary and sufficient endpoint condition

Use the two endpoint free charts of the round-six theorem. The $k+1$ block rows have equal endpoint normal closure $K$, and the markings of $Q=G/K$ are Nielsen equivalent. The common lifted bases identify the two chart groups with one marked $F_n$. Write $d_0,d_1$ for the retained donors and $V_0,V_1$ for the remaining, outside rows in their respective charts. The matched maps to $Q$ imply that $d_0,d_1$ have equal normal closures in $F_n$, hence are conjugate up to inversion by Magnus's theorem. [Round-six theorem](round-06-ac-proof.md#a-path-criterion-with-one-retained-donor), [common lifted bases](round-05-ac-proof.md#common-lifting-and-the-one-donor-splice).

There is an ordinary splice in which the retained donor never receives a multiplication if and only if the images of $V_0,V_1$ in $Q$ are ordinarily AC-equivalent using only the outside rows. For sufficiency, lift such a sequence to the outside rows in $F_n$, align the donor, then correct each lift by a product of conjugates of that donor and its inverse. Every discrepancy belongs to its normal closure. For necessity, project a donor-preserving splice to $Q$. The retained donor vanishes throughout, so delete its updates and every multiplication using it. This leaves an outside-only ordinary sequence in $Q$. Relator permutations can be tracked by row identity. For $n=2$, the test on the outside row is exactly conjugacy up to inversion in $Q$.

The earlier hypothesis imposed vanishing separately on every outgoing donor along a padded interval. The endpoint criterion allows those outgoing changes to cancel after intervening products or conjugations. The exact 110-move control starts at $(z,b,r)$, with $b=xyxYXY$ and $r=xxxYYYY$, and uses block slots 0 and 1. Put $v=(xz)b(xz)^{-1}$, $p=zv$, $u=rp$, and $e=pu$. The outside row first becomes $u$, and the block then imports it to create $e$. Subsequent products change the outside word through

\[
u\longmapsto ue\longmapsto uev\longmapsto ueve^{-1}.
\]

In $Q=F(x,y,z)/\langle\!\langle z,b\rangle\!\rangle$, the images of $e$ and $e^{-1}$ multiply in opposite directions. Both have nontrivial image in the $S_3$ marking taking $x,y$ to adjacent transpositions and $z$ to the identity. At strict steps 6 and 9, respectively, the outside image passes from the transposition to the identity and back. Both steps are inside the interval from 3 to 106 in which every relator is nonprimitive by individual Whitehead minimization.

Writing $w=eve^{-1}$, multiply the block's first row by the inverse of the changed outsider $uw$. Its value becomes $p u w^{-1} u^{-1}$. A product by the conjugate $(ue)v(ue)^{-1}$ restores $p$. Conjugate the outsider by $y$ and restore the block to $(z,b)$. After deleting $z$, the exterior result comes from multiplying $r$ by two explicit conjugates of $b$ and conjugating the product by $y$. The 45-move rank-two splice preserves the frozen donor. The padded replay has raw and cyclic peaks 231 and 157. [Control and both move lists](../results/round07_ac_proof_frozen_endpoint.json).

## Exact obstruction for the cap-23 ledger

The 148-move ledger has 18 products and 19 distinct signed cyclic triples. Every triple has at least one intrinsically primitive row. Immediately before and after product 140 all three rows are primitive. Following selected slot 0, rotate its left relator to the one-occurrence $z$ form and use the first Whitehead map on its right relator. In the latter chart, the marking change is $x\mapsto xz$, $y\mapsto z^{-1}yz$, $z\mapsto z$. Its image of the pivot has exactly one $z^{-1}$. The left and right projections of the retained slot-1 donor have cyclic Whitehead minima 8 and 11. The block normal closures are equal because product 140 is internal to slots 0 and 1. The outside word does not change at that step. The donor obstruction therefore detects precisely the failure of the common lifted marking condition, independent of which basis is used in either free chart.

To test switches involving any pair of pivot slots and any length of interval, use all multiplication boundaries, including step zero. A conjugation or inversion does not change the signed cyclic tuple, the ambient normal closure of either block row, or its role as a potential primitive pivot. For each ordered interval with endpoints $s\le t$, each primitive pivot on either end, and each two-slot block containing them, check the following necessary conditions.

- The abelianizations of the endpoint block normal closures are equal. The full tuple is unimodular. Thus each two-row block is a primitive rank-two lattice, and its cross product up to sign determines the lattice.
- The retained donors in the endpoint free charts lie in the same signed cyclic orbit under automorphisms of $F_2$. This is necessary if the charts share lifted bases and the endpoint block normal closures agree. Compute the minima and use Whitehead peak reduction to exhaust the level orbit of each minimum. The code uses all signed permutations and Whitehead substitutions, with independently checked minimum cuts. [Whitehead's theorem](https://doi.org/10.2307/1968618).

The screen rejects 417 choices by the block lattice and 34 by the donor orbit. It allows the remaining 85 without requiring the common lifted basis or the outside endpoint test, then adds every fixed-pivot edge. This is therefore an overapproximation of every sequence of compatible one-donor splices along the original forward ledger. The reachable pivot slots follow this pattern.

| After strict step | Primitive slots | Reachable slots in the overapproximation |
| ---: | --- | --- |
| 124 | 0, 2 | 0, 2 |
| 128 | 0, 2 | 0 |
| 134 | 0, 1, 2 | 0, 1 |
| 140–148 | 0, 1, 2 | 1 |

The final intrinsic slot 0 cannot be reached even by this overapproximation. In particular switching to slot 2 at the final vertex does not repair the problem. Its corresponding donor shares an orbit with that of slot 0, but the earlier failure at step 128 separates slot 2 from the reachable charts. A shorter set of transvections exposing the same pivot changes only the choice of quotient basis, which cannot affect an orbit obstruction. The result leaves arbitrary ordinary paths and more general splices that change both projected rows open. [Interval classifications and orbit keys](../results/round07_ac_proof_cap23.json).

## A strict projection using the literal $y$ chart

The overapproximation's final slot 1 is attainable by actual compatible switches. Start with the isolated $z$ in slot 2. After step 102, switch to slot 0 using the same surviving $x,y$ marking. After step 134, switch to the literal $y$-pivot in slot 1. For this second switch, the two quotient maps send the ambient pair $(x,zyy)$ to $(x,xyx^{-3})$ and $(x,x^{-4}y)$ in their native bases. Both are free bases. Carry the new marking by mapping its second generator to $x^5 y x^{-3}$.

The checker expresses the difference between the two marked images of $z$ as two conjugates of the retained donor's inverse. It expresses the difference for $y$ as five signed conjugates. Replacing the outside word one letter at a time gives a strict 744-move splice at step 134. Project each intervening operation in its currently selected chart. The full result is a 915-move ordinary path from AK(3), with raw peak 114 and cyclic peak 63. Its endpoint is the carried marking of the final literal $y$ projection. Both the native and carried signed cyclic endpoint classes occur in the independently verified cap-29 catalogue, so the replayed splice does not give a sharp peak. [Strict ordinary replay and verified catalogue membership](../results/round07_ac_proof_cap23.json).

~~~sh
python3 -B experiments/round07_ac_proof_cap23.py /tmp/ac-r05-ak3/c29.orbit.tsv \
  | diff - results/round07_ac_proof_cap23.json
python3 -B experiments/round07_ac_proof_frozen_endpoint.py \
  | diff - results/round07_ac_proof_frozen_endpoint.json
~~~
