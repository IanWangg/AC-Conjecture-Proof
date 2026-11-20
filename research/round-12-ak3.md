# Round 12 · Exact and reciprocal charts at the energy-20 waypoints

The two new energy-20 ordinary waypoints have four frozen-donor directions. Three are excluded by the tests below, and a companion calculation excludes the fourth. An exact torus-quotient calculation tests one of those directions against the entire verified reverse archive. Eleven of the twelve reciprocal contacts fail by finite witnesses, and a Fox obstruction excludes the twelfth. A separate two-sided finite-chart search generates no ordinary AK(3) trivialization.

## Reciprocal chart join

Write the forward pair as `(r,d)` and a verified ordinary-trivial reverse pair as `(s,e)`. Seek a replacement of `r` by `e` with `d` fixed and a replacement of `s` by `d` with `e` fixed. A join has the common intermediate `(e,d)` up to row order. The two changes can be compiled using the finite completion procedure, followed by the reverse pair's verified path to the basis. This test also covers pairs whose original coordinate classes are all distinct, so it extends the direct common-donor queries of Round 11. [Round 11 direct joins](round-11-ak3.md), [chart compiler](round-08-ak3.md).

For each forward chart, test every archive word with determinant weight of absolute value one. Then group contacts by reverse chart and test only their prescribed forward donors in that chart. The archive contains 23,902 pairs with cyclic total length at most 56. All eight signed ambient permutations yield 147,060 distinct possible retained donors in their marked form. Each completed finite chart is scanned exactly for the requested target words. The indexed lookup stores all reduced paths of length at most five, rotates a candidate to start at its least frequent five-letter factor, then checks the rest of the loop directly. A missing factor excludes the whole cyclic word. A control built around the corrected Wirtinger pair has four distinct starting coordinate classes across the two ends, matches the independent direct scanner, and produces two strict routes to `(x,y)` in 213 and 245 moves. [Indexed scanner](../experiments/round12_ak3_chart_index.cpp), [two-sided query and strict compiler](../experiments/round12_ak3_reciprocal_charts.py).

| Forward cap-32 additions | Requested stages | Test words in forward charts | Forward hits | Test words in reverse charts | Reciprocal joins |
| --- | ---: | ---: | ---: | ---: | ---: |
| Two energy-20 seeds | 4 | 68,583 | 11 | 130 | 0 |
| All 28 through energy 22 | 3 | 1,311,147 | 1,756 | 3,229 | 0 |

The allocation limits are 2,200,000 and 350,000 vertices, respectively. The forward scans expand four and 56 oriented charts. The reverse scans use 130 and 2,525 charts. Their last completed stage histograms, allocation stops, and control replays are recorded in the receipt. A failed reciprocal join here only covers the last completed graphs. The 248 new cap-32 orbits through energy 24 also give 243 Whitehead-minimized keys, all with verified planar-link parity obstructions. [Reciprocal search receipt](../results/round12_ak3_reciprocal_charts.json), [geometry receipt](../results/round12_ak3_low_geometry.json).

## The first energy-20 waypoint

Let `A=xxxxxyXXy` and `B=xxyxxyyXYXY`. This marking has a 687-move ordinary path from AK(3). [Strict entry](../certificates/round11_ak3_cap32_minimum.json).

With $z=x^{-2}y$, the relation $A=1$ is $x^7z^2=1$. The element $c=x^7=z^{-2}$ is central. The quotient by its cyclic subgroup is $C_7*C_2$. Two elements of the original one-relator group are conjugate exactly when their free-product images are conjugate and their integer values under $\chi(x)=2$ and $\chi(y)=-3$ agree. Indeed, lift a free-product conjugator. Its discrepancy is a power of $c$, and $\chi(c)=14$ detects that power. Cyclic syllable normal forms decide the free-product condition.

The receiver has $\chi(B)=1$ and cyclic syllable length ten. The primitive classes with the corresponding signed homology weight have representatives `xxy (xxyxy)^j` and inverses of `xy (xxyxy)^j`, with $j\ge0$. Their exponent vectors exhaust $(2,1)+k(3,2)$ over all integers $k$. The initial words and the indicated period form free bases, and the representatives are primitive by Nielsen multiplication. Rank-two primitive conjugacy uniqueness gives completeness. In the free product they have length $2+4j$ and $x$-syllable powers only three or four, even after inversion. The reduced free-product image of $B$ has an $x^6$ syllable, excluding all such replacements. [Exact form and primitive checks](../results/round12_ak3_frozen_primitives.json), [Osborne and Zieschang, §3.2](https://geodesic.mathdoc.fr/item/IM_1981__63_142788/).

With $B$ instead frozen, primitive slopes for $A$ have representatives `xxyxy (xxy)^j`, the exceptional `xy`, and inverses of `x (xxy)^j`. They exhaust the slopes $(3,2)+k(2,1)$. In the permutation marking with one-line images `x=(1,3,4,5,6,7,8,2)` and `y=(2,1,4,6,8,7,5,3)`, $B$ vanishes and $A$ has cycle type $(1,1,1,1,2,2)$. Each tail has period seven in this marking. Neither tail nor the exception yields the required type. [Permutations and the fourteen residue replays](../results/round12_ak3_frozen_primitives.json).

The exact torus condition gives seven donor keys from 12,179 compatible archive words. Every key already appears by stage two of the corresponding forward finite chart. These keys occur with twelve distinct marked archive receivers. For eleven contacts a finite permutation marking kills the selected reverse donor and distinguishes the archive receiver from $A$ even up to inversion. The sole remaining contact holds `XXYYxyXXyyxYY` fixed and asks whether `XXXXXYxxY` and `XXYYxyy` are conjugate up to inversion in its one-relator quotient. This narrows one direction of the first waypoint's reciprocal search to a single unrestricted conjugacy problem. [Complete torus lookup](../results/round12_ak3_torus_chart.json), [eleven verified separating markings](../results/round12_ak3_torus_separators.json), [Fox obstruction for the remaining contact](round-12-torus-contact-fox.md).

## The second energy-20 waypoint

Let `A'=xxxxyXXYY` and `B'=xxyyxYYYxxY`. The literal pair has a strict 1,037-instruction ordinary entry. The quotient by $A'$ is $H*_{a=x^2}\langle x\rangle$, where $H=\langle a,b\mid a^2 b=b^2 a\rangle$ and $b=y$. In $H$ put $u=ab^{-1}$ and $u_i=b^i u b^{-i}$. The relation is $u_2=u_0 u_1$. Introducing $u_1$ gives the explicit semidirect product $F(u_0,u_1)\rtimes\langle b\rangle$, with $u_0\mapsto u_1$, $u_1\mapsto u_0u_1$. The inverse sends $u_0\mapsto u_1u_0^{-1}$ and $u_1\mapsto u_0$. In particular $a$ has infinite order since it has height one in this semidirect product, so the cyclic amalgam is defined by injective maps. [Strict entry](../certificates/round12_ak3_second_energy20.json).

Conjugating $B'$ gives $x b^{-3}u^2b^3=xu_{-3}^2$. Its primitivity candidates have transverse character $\chi(x)=1$, $\chi(y)=2$, with $\chi=1$ after orientation. Their abelian slopes are $(5,-2)+k(2,-1)$. They are `x (xxY)^j` and inverses of `xY (xxY)^j` for $j\ge0$. In the amalgam the first family has representatives $x u_0^j$. The second is conjugate to $x u_{-1}^{-(j+1)}$, using $x^{-1}=x a^{-1}$ and $a=ub$. For $j=0$ the first representative has just one syllable and cannot be conjugate to $B'$. All remaining representatives have two syllables because their nonidentity $H$ coefficient has height zero and lies outside $\langle a\rangle$.

The conjugacy theorem for amalgams reduces a two-syllable comparison to cyclic permutation and conjugation by an element of $\langle a\rangle$. Keeping the $x$ factor first, conjugating by $a^k$ commutes with $x$, so equality reduces to conjugating the $H$ coefficients by $a^k$ in $H$. Conjugation by $a$ acts on the free kernel's abelianization by the Fibonacci matrix $M=\begin{pmatrix}0&1\\1&1\end{pmatrix}$. The vector for $u_i$ is $M^i(1,0)^T$. These vectors are primitive. Equality for the positive family forces $j=2$ and $k=-3$, because $M$ has no nonzero vector fixed by a nonzero power. Equality for the negative family forces $j+1=2$ and a power of $M$ taking $(1,0)^T$ to its negative. Squaring that power rules it out. In the remaining case, $a^{-3}u^2a^3=b^{-3}u^2b^3$ would force $b^3a^{-3}=(u_0u_1)^{-2}$ to centralize $u_0^2$ in $F(u_0,u_1)$. Free reduction distinguishes the two words. This rules out all primitive replacements with $A'$ held fixed. The other frozen direction is excluded by the companion permutation and matrix checks. [Fourth frozen direction](round-12-ac-proof.md). [Amalgam conjugacy criterion, §4.2](https://eprints.maths.manchester.ac.uk/113/1/amalgam_Ie.pdf), [free-word checks](../results/round12_ak3_frozen_primitives.json).

## Reproduction

Use the completed cap-32 additions TSV as `forward` and the verified cap-56 reverse archive TSV as `reverse`, with its adjacent `.sources.json`. [Cap-32 generation](round-11-cyclic32.md#reproduction), [archive replay](round-04-ak3.md#reproduction).

~~~sh
c++ -std=c++17 -O3 experiments/round12_ak3_chart_index.cpp -o "$work/chart-index"
c++ -std=c++17 -O3 experiments/round11_ak3_targeted_acm.cpp -o "$work/reference"
python3 -B experiments/round12_ak3_reciprocal_charts.py "$work/chart-index" "$work/reference" "$forward" "$reverse" \
  --forward-energy 20 --depth 4 --allocation 2200000 > "$work/reciprocal20.json"
python3 -B experiments/round12_ak3_reciprocal_charts.py "$work/chart-index" "$work/reference" "$forward" "$reverse" \
  --forward-energy 22 --depth 3 --allocation 350000 > "$work/reciprocal22.json"
python3 -B experiments/round12_ak3_torus_chart.py "$reverse" --separators results/round12_ak3_torus_separators.json \
  | diff - results/round12_ak3_torus_chart.json
python3 -B experiments/round12_ak3_frozen_primitives.py | diff - results/round12_ak3_frozen_primitives.json
awk 'length($0) <= 25 {print} length($0) > 25 {exit}' "$forward" > "$work/outside24.tsv"
python3 -B experiments/round01_geometric_archive.py "$work/outside24.tsv" | diff - results/round12_ak3_low_geometry.json
~~~
