# Both relators must receive a product after the braid-kernel lift

2026-11-19. The saved 533-move ordinary path from AK(3) ends at a free tuple $(U,V)$ with exponent vectors $(1,0)$ and $(0,1)$. In the free group, neither row can become primitive along a path that only permits multiplications into that row. In the braid-kernel tower, each of the two corresponding restricted distances to its marked basis generator is finite at every level and diverges with the level. [Saved ordinary prefix](../certificates/optimized_first_order_strict.json), [quotient lifting](round-02-relative-quotients.md).

## Frozen donor criterion

Track the two rows through permutations. A frozen donor may be inverted, conjugated and used as a multiplier. It cannot receive a multiplication by the other row. Let $\phi:F(x,y)\to G$ kill the donor and have noncyclic image. Along any such path the donor remains in $\ker\phi$. It cannot become primitive, because killing a primitive element of $F(x,y)$ would make $\phi(F)$ cyclic. Multiplication by the donor leaves the receiver's image unchanged. Inversions and conjugations of the receiver preserve its image up to conjugacy and inversion.

When $V$ is the donor, the receiver's $x$ exponent remains $\pm1$. A primitive receiver would therefore be conjugate, up to inversion, to $xy^j$ for some integer $j$. When $U$ is the donor, the corresponding candidates are $yx^j$. This uses the rank-two uniqueness of a primitive conjugacy class with specified exponent vector, since these particular words are primitive with the indicated vectors. [Osborne and Zieschang, §3.2](https://geodesic.mathdoc.fr/item/IM_1981__63_142788/).

## Explicit witnesses

Use the following marking in $\mathrm{SL}_2(\mathbb F_{11})$:

$$
x\longmapsto
\begin{pmatrix}0&1\\10&5\end{pmatrix},
\qquad
y\longmapsto
\begin{pmatrix}0&2\\5&1\end{pmatrix}.
$$

The generators do not commute. The 635-letter word $U$ evaluates to the matrix with rows $(8,6)$ and $(4,10)$, and the 1,867-letter word $V$ evaluates to the identity. The trace of $U$ is $7$. The marked $y$ has order six, and the traces of $xy^j$, for $j=0,\ldots,5$, are $5,8,3,6,3,8$. Inversion preserves trace for determinant-one matrices. Thus $V$ cannot serve as a frozen donor until either row becomes primitive.

For the opposite direction, use permutations in one-line notation:

$$
x\longmapsto (1,2,4,5,3),
\qquad y\longmapsto (3,4,2,5,1).
$$

The images in $S_5$ do not commute. The saved word $U$ evaluates to the identity and $V$ to $(3,1,2,4,5)$, a 3-cycle with two fixed points. The three candidates $yx^j$ modulo the order of $x$ have cycle-length partitions $(5)$, $(5)$ and $(1,2,2)$. Inversion preserves cycle type. This excludes $U$ as a frozen donor all the way to a primitive. Consequently both initial rows must receive a product before the first primitive occurs after the saved prefix.

The finite evaluations replay the original 533 elementary moves and check the entire candidate period, including the two noncommutativity controls.

~~~sh
python3 -B experiments/round03_frozen_donors.py | diff - results/round03_frozen_donors.json
~~~

## Divergence in a restricted quotient metric

Let $N$ be the normal closure of the braid relator and let $G_m=F/\gamma_{m+1}(N)$. For the first direction, take the distance in $G_m$ from $(U,V)$ to $(x,V)$ with $V$ permitted only the frozen-donor moves. For the second, take the distance from $(U,V)$ to $(U,y)$ with $U$ frozen. Count inversions, swaps, signed right multiplications and conjugations by single marked letters. Each distance is finite by the quotient lifting proof, which explicitly corrects either first row choice with the other frozen.

Fix a move bound $L$. The permitted instruction lists of length at most $L$ form a finite set. The finite witnesses prove that every one has a free endpoint different from the designated target. The subgroups $\gamma_{m+1}(N)$ are nested with trivial intersection. Thus for sufficiently large $m$ none of the finitely many discrepancies vanish, and the restricted distance exceeds $L$. This proves divergence in both directions. Ordinary AC paths may multiply into both coordinates, so these witnesses give no divergence statement for the unrestricted distances and no AC counterexample.
