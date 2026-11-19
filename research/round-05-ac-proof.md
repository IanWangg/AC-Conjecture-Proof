# Round 05 · Ordinary AC projection in changing free charts

2026-11-19. Two free quotients have a common lifted basis exactly when their generating markings are Nielsen equivalent in the quotient by both kernels. For a one-row chart change this gives an ordinary AC splice. A forced change of eliminated generator can violate the test, even when no projected coordinate is primitive. The full round-four AK(3) witness satisfies the splice requirements and descends to a strict 251-move rank-two ledger.

## Common lifting and the one-donor splice

Let $K,L\lhd G$ with $G/K$ and $G/L$ free of rank $n$. Write $Q=G/(KL)$. Choose bases in $G/K$ and $G/L$ and let $a,b$ be the respective ordered generating tuples induced in $Q$. There are $n$ ambient words forming bases in both quotients if and only if $a,b$ are Nielsen equivalent in $Q$.

For necessity, compare the images of the lifted words with each of the two original markings using the free-group Nielsen generators. For sufficiency, a Nielsen sequence in $Q$ lifts to a basis change in $G/K$, so choose the bases to have matching images in $Q$. For a matched pair $gK,hL$, write $g^{-1}h=kl$ with $k\in K$ and $l\in L$. The word $gk=hl^{-1}$ lifts both prescribed letters. Do this separately for all $n$ matched pairs. This also proves the fiber product identity

$$
\operatorname{im}(G\longrightarrow G/K\times G/L)
=(G/K)\times_Q(G/L).
$$

Now take $G$ free of rank $n+1$. A chart consists of a selected relator whose normal closure gives a free quotient of rank $n$ and a basis for the quotient. A cyclic one-occurrence equation is a chart with the remaining letters as its basis. Both of the following changes have one corresponding donor in their two projected $n$-tuples.

- At a single vertex, switch between distinct pivot rows $p,q$. The projected donor in the first chart is $q$, while in the second it is $p$.
- Across a product $p\mapsto p'=p d^{\pm1}$, keep the changed slot selected. The projected donor is $d$ on both sides.

Let $K$ and $L$ be the normal closures of the selected pivot on each side. In the first case $KL$ kills $p,q$. In the second it kills $p,d$, since the product and its predecessor jointly kill $d$. In both cases the two quotients by the corresponding donor are precisely $Q=G/(KL)$.

When the two generating markings of $Q$ are Nielsen equivalent, use the common lifted bases to put the free quotients in the same coordinates. The two donor words then have equal normal closure, since both maps to $Q$ agree on the basis. By Magnus's normal-closure theorem the donors are conjugate up to inversion. Align the donor slots and normalize one word to the other. Every other row has the same image in $Q$ on both sides, so the discrepancy can be supplied by a finite product of conjugates of the aligned donor and its inverse. Expand each correction into ordinary AC moves, restoring the donor after each use. If the donors are trivial, all remaining projected rows already match. [Magnus's theorem as recalled by Bogopolski and Sviridov](https://msp.org/gtm/2008/14/gtm-2008-14-004s.pdf).

No swap needs a stabilization. For example, the successive pair shapes $(a,b)\to(ab,b)\to(b^{-1}a^{-1},b)\to(b^{-1}a^{-1},a^{-1})\to(ab,a^{-1})\to(aba^{-1},a^{-1})\to(b,a^{-1})\to(b,a)$ use only inversion, right multiplication and conjugation.

If two charts use the **same pivot**, the actual free quotient is the same and a change between its bases can be carried forward as a new marking. If two charts eliminate the **same marked generator**, their common surviving marked letters are already common lifts. A padded path descends when the selected chart exchanges and selected-receiver product steps satisfy the conditions above. A pivot that stays fixed gives the ordinary projected move on retained rows, or no move when the donor is killed. Markings can be transported boundary by boundary, since a free-group isomorphism takes each projected AC move to an AC move with the transported conjugator. If the final projection is a basis, that transported basis is reachable from the start by ordinary moves and then Nielsen-reduces to the original generators. This argument requires no simultaneous choice of a basis for all quotients along the path. The common-lift characterization also applies to the adjacent free quotients in the [two-incoming cut lemma](round-04-stable-disproof.md).

## Two forced chart changes

Use $p=zA^{-1}$ and $q=xB^{-1}$, with $A\in F(x,y)$ and $B\in F(y,z)$. Put $d=p^{-1}q$ and $r=h p^2 q^2$. The strict multiplication $(p,d,r)\to(q,d,r)$ changes which pivot is available in the examples below. Only $z$ occurs once on the left and only $x$ occurs once on the right, both in the receiver row. All four projected relators in each example are nonprimitive, as verified by the signed Euclidean-word test.

**Compatible change.** Take $A=x^2$, $B=z^2y^2$ and $h=yx$. The ambient pair $(x^{-1}z,y)$ projects to $(x,y)$ on the left and $(y^{-2}z^{-1},y)$ on the right, both bases. The common quotient by the donor is $\langle x,y\mid x^3y^2\rangle$. It becomes trivial when $yx=1$ is also imposed. In the carried marking denoted again by $(x,y)$, the left retraction sends $z$ to $x^2$ and the right sends $z$ to $x^{-1}y^{-2}$ and the old $x$ to $x^{-1}y^{-2}x^{-1}$. The exact splice first clears the two donor factors from the other row, turns $yx$ into its right-chart image by one conjugated donor, then sets the donor and its powers to their right-chart values. This takes 15 elementary moves, with raw peak 32.

**Incompatible change.** Take $A=xy^N x^{-1}$, $B=y^2z^2$, $h=y$ with $N=30k+1$ and $k\geq1$. The quotient by the full tuple is trivial. Killing $r$ after $p,q$ gives $y=1$, then $z=1$ and then $x=1$. In each one-pivot projection, first using the donor to remove its powers from $r$ leaves the row $y$. Its conjugates then remove the $y$ letters from the donor, whose remaining exponent in the other generator is $1$ or $-1$. The strict replays for $N=31$ take 192 and 298 moves respectively.

The two projected donor words themselves belong to different cyclic-word orbits under every ambient $F_2$ automorphism, even allowing donor inversion and conjugation. For any word $u$, enumerate all epimorphisms $F_2\to A_5$ killing $u$ and record the cycle types of the commutators of the ordered generator images. A free-group automorphism changes the ordered pair by a Nielsen sequence, which preserves its commutator up to conjugacy and inversion. Conjugating or inverting $u$ preserves the epimorphism condition. The cycle-type count is therefore invariant under all three operations. [Rank-two Nielsen commutator invariant](https://doi.org/10.1017/S0017089512000675).

All 2,280 generating ordered pairs of $A_5$ were tested. On the left exactly 120 kill the donor, all with commutator cycle type $(1,1,3)$. On the right exactly 120 do, all with type $(5)$. The calculation covers every $N=30k+1$, since the projected donor words depend on $N$ only through powers of $y$ and $A_5$ has exponent 30. This excludes a direct splice keeping the designated donor up to inversion and conjugation in a common marking. The two successful rank-two replays use a different donor on part of the path. Thus the common-lift criterion is sufficient for descent, with a concrete limit even for forced one-occurrence charts on an ordinarily trivial rank-three edge. [Exact controls and move lists](../results/round05_ac_proof_charts.json).

## Compiling the rank-three AK(3) witness

The round-four rank-three ledger admits simple chart changes. Keep row 2 in zero-based indices as the $z$ pivot through step 217. At step 218 the multiplication of row 0 by row 2 makes row 0 a pivot for both $z$ and $x$. Switching pivot rows with the same eliminated $z$ projects to one inversion of the retained donor. Then switch the eliminated letter on row 0 and carry the old marking by sending $(y,z)$ to $(y,y^2xy^{-2})$.

The receiver is the selected pivot again at step 235. The carrier marking is unchanged, but the eliminated $x$ changes its image from $x$ to $x E^{-1}$, where $E$ is the new projected donor $y^3x^4$. The old donor becomes $E$ by inversion and a single conjugation. For each occurrence $u$ of $x^{\pm1}$ in the other row, replace its old image by the new image $v$ by multiplying on the right by $S^{-1}u^{-1}vS$, with $S$ the as yet unmodified suffix. Each such factor is a conjugate of $E^{\pm1}$. The step projects to 29 strict moves. All intervening steps are checked in their chosen charts. [Original rank-three path](../certificates/round04_stable_proof_pivotless22.json).

The resulting ordinary rank-two path has 247 moves with raw peak 29. Four further conjugations transport the final projection to the literal surviving-generator marking $y\mapsto y, z\mapsto x$, ending at `(yxxxyyyxY, yxxxYXXXYxxxyyy)`. This is the rank-two projection of the pivotless-for-$z$ endpoint, with the surviving letters named in a different order from the [round-four cyclic screen](round-04-chart-screen.md). The strict path requires neither that screen's catalogue lookup nor a free basis change as an AC operation. The endpoint is not a free basis.

~~~sh
python3 -B experiments/round05_ac_proof_charts.py | diff - results/round05_ac_proof_charts.json
~~~

The projected ordinary orbit is still unresolved for general products without a compatible marking or a constructive second-donor argument. A proof for paths allowing such edges would need a replacement for the one-donor condition. The AK(3) witness checked here provides an exact positive control and ends before that difficulty appears.
