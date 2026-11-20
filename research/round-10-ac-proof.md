# Alternating receiving blocks for ordinary chart changes

2026-11-19. The wrong rank-two Wirtinger pair admits no primitive coordinate by changing just one relator identity with the other held fixed up to conjugation and inversion. Both alternatives are excluded for arbitrary donor products and arbitrary conjugators. The marked wrong-to-correct Wirtinger repair and the two actual energy-20 chart changes each require at least three alternating receiving blocks. A common-quotient test excludes two of the four three-block patterns for the product chart change. [Exact finite witnesses and positive control](../results/round10_ac_proof_blocks.json).

## Exact block criteria

A receiving block allows inversions and conjugations of both rows and products into one row. Track the two row identities across any relator permutation. Write $N_v=\langle\!\langle v\rangle\!\rangle_F$. With $v$ held as donor, one can change the receiver from $u$ to $w$ if and only if $u,w$ are conjugate up to inversion in $F/N_v$. Necessity follows by projecting the moves. For sufficiency, first align the signed conjugates in the quotient by lifting a conjugator. The remaining discrepancy is a product of conjugates of $v^{\pm1}$. Apply each factor by conjugating and possibly inverting the donor, making the product, and undoing its temporary changes. This gives a strict ordinary path in the original rank. Interspersed conjugations and inversions of a row never receiving a product can be absorbed into the choice of the temporary donor.

For two blocks between marked pairs $(a,b)$ and $(c,d)$, with the first and second rows receiving in that order, the exact tests are

$$
a \sim c \pmod {N_b},\qquad b\sim d\pmod {N_c}.
$$

Here $\sim$ denotes conjugacy up to inversion. Test both receiving orders and both possible target assignments to cover unlabeled endpoints. The intermediate pair is forced up to individual signed conjugacy. A path with zero or one blocks also satisfies a two-block pattern with an identity block. For the abelian test, the donor exponent vector is primitive because the source and target pairs have unimodular exponent matrices. The absolute determinants against the donor must agree.

There is also an exact three-block lifting condition for the order first row, second row, first row. For some signed conjugates $a'$ and $c'$ of the outer endpoints, the intersection

$$
a'N_b \cap c'N_d
$$

must contain a word $h$ for which $b\sim d\pmod{N_h}$. The two outer conditions have a simultaneous lift if and only if $a\sim c$ in the common quotient $F/(N_bN_d)$. Indeed one may then align the signed conjugates so that $a'^{-1}c'=uv$ with $u\in N_b$ and $v\in N_d$. The word $a'u=c'v^{-1}$ solves both conditions, and all lifts for this alignment form one coset of $N_b\cap N_d$. The middle condition is exactly the frozen-row test with this lift as donor. If the simultaneous lift can be taken primitive and both endpoint pairs normally generate $F_2$, the middle test is automatic. Both $b$ and $d$ then normally generate the infinite cyclic quotient by that primitive, so both are unit generators there.

## Unbounded primitive-family test at the wrong Wirtinger pair

The verified rank-two Wirtinger reduction gives the marked wrong pair $(A,B)$ and the marked corrected pair $(C,A)$. [Verified Wirtinger reduction](round-10-stable-proof.md#the-frozen-repair-and-its-ordinary-endpoints).

~~~text
A = XXYYxyyyxYY
B = XXYxyXyxYY
C = XXYYxyXyyxYY
~~~

Their exponent vectors are $(0,-1),(-1,-1),(-1,-1)$, respectively. After a block fixing $A$, any primitive receiver representative must have $x$-exponent $\pm1$. Up to conjugation and inversion its possible words are $x^{-1}y^k$, $k\in\mathbb Z$, by uniqueness of the primitive class with a given exponent vector. After a block fixing $B$, use the free basis $(x,xy)$. The primitive receiver classes are then represented by $x(xy)^k$, up to conjugation and inversion. [Osborne and Zieschang, Theorem 1.2](https://geodesic.mathdoc.fr/item/IM_1981__63_142788/).

For the $A$-frozen case, take the matrices below in $\mathrm{SL}_2(\mathbb F_7)$.

$$
 x\longmapsto\begin{pmatrix}0&1\\6&3\end{pmatrix},\qquad
 y\longmapsto\begin{pmatrix}0&1\\6&6\end{pmatrix}.
$$

They kill $A$. The image of $B$ has trace 6, and $y$ has order 3. The three residue classes for $k$ yield traces 3, 2 and 2. Trace is invariant under conjugation and inversion in this group, so the whole family is excluded. For the $B$-frozen case, take the following marked permutations in $S_8$, in one-line notation.

~~~text
x = (1,3,2,5,4,7,8,6)
y = (6,1,4,8,3,5,7,2)
~~~

These kill $B$ and give $xy$ order 6. The image of $A$ has cycle type $(1,1,1,5)$. All six residues for $x(xy)^k$ have different cycle types. The congruence tests cover every integer in each primitive family. They apply before any change to the frozen donor beyond signed conjugation, even if the receiver first visits arbitrarily long words.

## Actual chart switches

The checker uses the literal rank-two endpoints of both energy-20 splices. For each of the three comparisons it tests the four two-block templates. The finite witnesses kill the corresponding donor and compare the exact cycle types of the receiver endpoints. The wrong-to-correct comparison places $A$ in the first target slot and checks both assignments. [Replayed energy-20 chart splices](round-09-ac-proof.md#the-first-chart-in-the-energy-20-component).

| Start and target | Rejected by abelianization | Remaining templates rejected by finite quotients | Receiving-block lower bound |
| --- | ---: | ---: | ---: |
| Wrong and corrected Wirtinger pairs | 2 | 2 | 3 |
| Energy-20 same-vertex splice | 1 | 3 | 3 |
| Energy-20 product splice | 3 | 1 | 3 |

For the energy-20 product splice, the pattern receiving row 0 twice and assigning the targets in reverse order has a common quotient whose abelianization has order 5. The projected outer endpoints differ up to sign there. The pattern receiving row 1 twice and retaining the target order has a witness in $S_4$, with $x=(1,3,4,2)$ and $y=(2,3,4,1)$. The first and last donors both vanish, and the projected outer endpoints have cycle types $(4)$ and $(1,1,2)$. These give two exclusions among the four three-block patterns. For the wrong-to-correct repair, the pattern receiving row 1 twice and assigning the common row to its original slot fails the common-quotient test in the original $A$-frozen quotient. The surviving patterns remain unresolved.

For a positive control take the actual left endpoint of the same-vertex splice and perform six strict products, twice into row 0, then twice into row 1, then twice into row 0. The coefficients of the resulting two rows in the original exponent basis are $(5,12)$ and $(2,5)$. A first block reaching either final row requires absolute coefficient one on its own initial row, which neither row has. The control pair therefore has exact minimum three blocks, and the replay exhibits its middle donor.

These bounds apply to the indicated rank-two markings. A higher-rank repair with an active deletion chart and an unrestricted ordinary path with more receiving blocks remain possible.

## Reproduce

~~~sh
python3 -B experiments/round10_ac_proof_blocks.py \
  | diff - results/round10_ac_proof_blocks.json
~~~
