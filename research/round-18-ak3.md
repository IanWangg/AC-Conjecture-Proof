# Two uncapped ordinary products from the cap-40 menu

None of the **206,077** distinct marked states in the Round 17 cap-40 menu can expose a primitive relator in two ordinary products, even with arbitrary independent conjugations and inversions between products. The intervening cyclic energies and the output lengths are unrestricted. This extends the previous one-product exclusion for the same states. The ordinary AK(3) trivialization remains open. [Round 17 menu](round-17-ak3.md#alternating-product-menus-through-cap-40), [complete scan](../results/round18_ak3_two_products.json).

## Reduction to four boundary words

Let the rows initially be $A,B$, and let $B$ be the first donor. Choose the sign of the final primitive so that its exponent vector is $[A]+j[B]$. After the two products the coefficient $j$ is one of $-2,0,2$. The coefficient on $[A]$ is one after orientation even if the second product changes the other slot. The pair is unimodular, so each vector has a unique primitive cyclic class up to the chosen orientation. The program constructs its Euclidean representative $P$.

A two-product primitive occurs for this slope exactly when there is a spherical equation among the four cyclic words

$$
A,\qquad B^\epsilon,\qquad B^\eta,\qquad P^{-1},
\qquad \epsilon+\eta=j.
$$

Here a spherical equation means that a product of some conjugates of these four words is the identity. Necessity follows by reading the two products and cyclically moving factors, including for a last product into the other slot. Conversely, conjugate the equation to make the first factor literally $A$. Multiply its row by the two indicated conjugates of $B^\epsilon,B^\eta$ in sequence, restoring the donor between products. This leaves a conjugate of $P$. The factors of any solution can be put in the stated order using the elementary product identity $uv=v(v^{-1}uv)$.

## At least one zero bridge

Realize a solution as a map of a sphere with four discs removed to the two-petal rose, with the four positively oriented boundary circuits carrying the given cyclic labels. Take interiors of the labelled edges as regular values. The interval components of their preimages pair inverse boundary letters by disjoint arcs. Cap the four boundary circles to see the resulting ribbon graph with four vertices. If no arc joins distinct boundary components, each vertex with incident letters is a planar bouquet of loops. Such a bouquet has a monogon, by the planar Euler formula. The two consecutive letters in that monogon cancel cyclically, which contradicts cyclic reduction. Every boundary word here is nonempty, so there is an arc connecting two distinct boundary circles.

Join those two circles along a strip containing the arc. Its endpoints have inverse labels, so basing both boundary words at the same side of the common edge midpoint gives a product of cyclic rotations with no conjugating bridge. The other two words then have a product cyclically conjugate to the inverse of this merged word. There are only three pair partitions, and the zero bridge may be on either side.

For each partition the scanner enumerates both zero-bridge menus and compares their inverse cyclic classes. If the inverse of a candidate zero-bridge product is longer than the sum of the remaining two lengths, the other product must use a nonempty shortest bridge. Disjoint axes give the exact cyclic form $R U S U^{-1}$, with $R,S$ rotations and length of $U$ half the length excess. The test reads this pattern directly in the target cyclic word. If there is no length excess, the geometric product theorem permits only the already checked zero-bridge type. These tests also cover an empty merged word by comparing the two zero-bridge menus. [Cyclic product geometry](round-16-cyclic-peak-gap.md#ordinary-lower-bound), [native test](../experiments/round18_ak3_two_products.cpp).

## Independent controls

An independent replayer forms pairings of individual, inverse-labelled boundary letters. It computes the ribbon graph faces and uses the Euler characteristic on each disconnected union to decide whether a planar pairing exists. On **4,000** balanced short four-boundary instances, both implementations agree on **3,960** positives and **40** negatives. The first checker also agrees with stack reduction and literal lexicographic rotation on 20,000 longer examples. [Independent pairing audit](../experiments/round18_ak3_two_products_controls.cpp).

The nonprimitive positive control has no one-product primitive, but the new scanner finds a genuine two-product witness. Its second pair partition uses the nonempty bridge `yyXX`. The compiler aligns the complementary products by free conjugation, reorders the four factors, and emits only elementary AC instructions. The independently replayed control reaches the literal basis in **79** moves at cyclic peak **28**, raw peak **42**. [Strict positive ledger](../certificates/round18_ak3_two_products_control.json), [compiler](../experiments/round18_ak3_two_products_replay.py).

## Reproduction

The decompressed catalogue has the same SHA-256 as the independently generated Round 17 union. It retains literal signed generator markings and ordered slots. The scanner checks both initial donor slots in each record. [Catalogue](../certificates/round18_ak3_two_product_menu40.tsv.gz), [source menu receipt](../results/round17_ak3_minima_menu40.json).

~~~sh
c++ -O3 -std=c++17 -pthread experiments/round18_ak3_two_products.cpp -o "$work/two-products"
c++ -O3 -std=c++17 -pthread experiments/round18_ak3_two_products_controls.cpp -o "$work/controls"
"$work/controls"
gzip -cd certificates/round18_ak3_two_product_menu40.tsv.gz > "$work/menu40.tsv"
"$work/two-products" "$work/menu40.tsv" 10
python3 -B experiments/round18_ak3_two_products_replay.py --write-control "$work/control.tsv"
"$work/two-products" "$work/control.tsv" 1 > "$work/control.json"
python3 -B experiments/round18_ak3_two_products_replay.py "$work/control.json" "$work/control-ledger.json"
python3 -B experiments/elementary_verify.py "$work/control-ledger.json"
~~~
