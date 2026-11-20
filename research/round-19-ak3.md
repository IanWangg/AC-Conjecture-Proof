# Three ordinary products from the new cap-33 minima

None of the **nine** new ordinary energy-17 states can expose a primitive relator in three products. This includes arbitrary conjugating tails, arbitrary inversions, both initial donor choices, and both histories for the second receiver. A separate exact fixed-donor test excludes three-product exposure from all **84** new ordinary states through energy 20. The paths to these states are in the ordinary AK(3) component. The basis remains unresolved. [New states and strict entry](round-18-cyclic33.md#a-sharp-entry-at-cyclic-energy-17), [scan and control receipts](../results/round19_ak3_three_products.json).

## Three products and five boundary words

Write the source as $(A,B)$, with $B$ the first donor. If the first two products change the same row, the final primitive may be oriented to have exponent vector $[A]+j[B]$ for $j\in\{-3,-1,1,3\}$. Even if the third product changes the other row, cyclic conjugation lets its factors be read with the original $A$-coordinate first. For each slope, the exact question is whether some conjugates of the five words

$$
A,\quad B^{\epsilon_1},\quad B^{\epsilon_2},\quad B^{\epsilon_3},\quad P^{-1},
\qquad \epsilon_1+\epsilon_2+\epsilon_3=j,
$$

have product one, where $P$ is the Euclidean primitive of that exponent vector. The implication in either direction follows as in the two-product case, using adjacent exchanges of conjugate factors to put them in order. A successful equation always compiles to three products changing the original receiver, with $B$ held fixed between products. [Two-product reduction](round-18-ak3.md#reduction-to-four-boundary-words).

The cross-boundary preimage-arc argument applies on a sphere with any number of nonempty boundary circuits. Each contraction merges two cyclic coefficients using rotations whose contact letters cancel. The remaining coefficient is freely and cyclically reduced. This yields at most four nonempty boundary words after one contraction. The solver checks the exact four-boundary test from Round 18, or the direct three-boundary product read if the merged coefficient is trivial. Negative results are memoized by the multiset of oriented cyclic classes. For the 84 marked pairs, the solver exhausts **672** primitive slope cases and **52,413** contracting products with zero hits. It also checks **40** fixed-donor cases from the five Round 17 energy-20 minima with zero hits. [Contraction solver](../experiments/round19_ak3_three_products.cpp), [five Round 17 minima](round-17-ak3.md).

## Opposite second receiver

If the second product changes the other row, write $C$ for the first updated row. Its exponent vector is $[A]+s[B]$ for $s\in\{-1,1\}$. An ensuing primitive can be oriented to have class $[B]+j[C]$ for $j\in\{-2,0,2\}$. Any such path gives a spherical relation among $B$, two signed copies of $C$, and $P^{-1}$. Expand each copy of $C$ as a product of a conjugate of $A$ and a conjugate of $B^s$, with signs from that copy. This gives six boundary words. The test permits the two copies to use independent conjugating words for the inner factors. Therefore an empty test excludes the actual alternating path, while a spherical solution by itself would require an additional check that both copies come from the same first update.

For the nine energy-17 states the six-boundary test checks all **108** slope and sign cases. It performs **877,644** contracting products and gives zero hits. The two histories exhaust the second receiver choices. The earlier one- and two-product exclusions for these states therefore extend to a bound of **at least four ordinary products** to first expose a primitive coordinate. [Earlier bounds](round-18-cyclic33.md#a-sharp-entry-at-cyclic-energy-17).

## Controls and strict replay

The independent ribbon graph checker pairs individual inverse letters and computes the genus through the face permutation. It agrees with the contracting solver on 2,000 balanced examples at each of five and six boundaries, including four negative examples in total. The positive ordinary fixture

~~~text
yxyyxxYYXXXXyyyxxYYXXXYxyyyxxYYXXXYX   xxxyyXXYY
~~~

has two nonprimitive rows and fails both the uncapped one-product and two-product primitive tests. The new exact test exposes a conjugate of `y` in its third product. Recovering the literal spherical conjugators, then expanding the operations, gives a strict **379**-instruction route to `(x,y)`. The primitive is exposed after 301 instructions, the full raw peak is 232, and the cyclic peak is 79. [Independent pairing control](../experiments/round19_ak3_three_products_controls.cpp), [strict ledger](../certificates/round19_ak3_three_products_control.json), [witness compiler](../experiments/round19_ak3_three_products_replay.py).

## Reproduction

~~~sh
c++ -O3 -std=c++17 -pthread experiments/round19_ak3_three_products.cpp -o "$work/three-products"
c++ -O3 -std=c++17 -pthread experiments/round19_ak3_three_products_controls.cpp -o "$work/controls"
"$work/controls"
"$work/three-products" fixed certificates/round18_ak3_c33_low20.tsv 8
head -9 certificates/round18_ak3_c33_low20.tsv > "$work/energy17.tsv"
"$work/three-products" alternating "$work/energy17.tsv" 4
python3 -B experiments/round19_ak3_three_products_replay.py --write-control "$work/control.tsv"
"$work/three-products" fixed "$work/control.tsv" 1 > "$work/control.json"
python3 -B experiments/round19_ak3_three_products_replay.py "$work/control.json" "$work/control-ledger.json"
python3 -B experiments/elementary_verify.py "$work/control-ledger.json"
~~~
