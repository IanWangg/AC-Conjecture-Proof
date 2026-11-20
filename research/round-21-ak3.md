# Four ordinary products with changing receivers

Every one of the nine cap-33 energy-17 marked pairs needs at least **five** ordinary products to expose a primitive row. The test allows arbitrary free conjugations and inversions between products and imposes no cyclic energy bound. Round 19 excludes three or fewer products. Round 20 excludes four when the first three receivers are the same. The remaining four-product histories give **450** distinct spherical equations across the nine pairs, all negative. [Strict ordinary entries](round-20-c33-minima.md), [three-product bound](round-19-ak3.md), [fixed-donor four-product bound](round-20-ak3.md#four-fixed-donor-products), [complete decisions](../results/round21_ak3_four_products.json).

## Receiver histories and shared factors

Call the initial receiving row $A$ and the initial donor $B$. Orient each result to preserve its old receiver as the first factor. Each signed operation can then be written as the receiver followed by a conjugate of the donor or its inverse. The two choices of fourth receiver give the same menu of possible oriented cyclic output classes. A cyclic rotation interchanges the two factors, and if needed an overall inversion changes the relative sign. Thus the first three receiver choices suffice to specify a test.

In the display below, each factor can carry its own conjugation. Repeated occurrences of a capital letter denote the same cyclic class in an actual path. The exponents $s,t,u,v$ are independent signs.

| First three receivers | Earlier updated rows | Final exposure | Boundaries including $P^{-1}$ |
| --- | --- | --- | ---: |
| $A,A,B$ | $C=A B^s B^t$ | $B C^u C^v$ | 8 |
| $A,B,A$ | $C=A B^s$, $D=B C^t$ | $C D^u D^v$ | 9 |
| $A,B,B$ | $C=A B^s$ | $B C^t C^u C^v$ | 8 |

Expanding every $C$ and $D$ in one row of this table expresses the final word as a product of conjugates of $A^{\pm1}$ and $B^{\pm1}$. Its abelianization is primitive since the source exponent matrix has determinant of absolute value one and the updates are elementary shears. Let $P$ be the Euclidean primitive of that exponent vector. The necessary condition is that the expanded factors together with $P^{-1}$ give a spherical equation. Tests use both initial receiver choices and all 16 sign histories. The spherical decision depends only on the oriented boundary multiset under exchanges of consecutive conjugate factors. This gives 14 distinct tests per source pair for $A,A,B$, 20 for $A,B,A$, and 16 for $A,B,B$.

A negative spherical decision excludes the corresponding history with all free conjugators. A positive requires the same updated cyclic class at each repeated occurrence to give an ordinary continuation. [Native expansion and search](../experiments/round21_ak3_four_products.cpp).

| History | Equations across nine sources | Contracting products | Witnesses |
| --- | ---: | ---: | ---: |
| $A,A,B$ | 126 | 10,395,723 | 0 |
| $A,B,A$ | 180 | 98,641,403 | 0 |
| $A,B,B$ | 144 | 7,353,412 | 0 |

## Complete contraction with a forced endpoint

An equality of conjugates gives a planar pairing of inversely labelled boundary letters. Pick any nonempty cyclically reduced coefficient. If all of its pairings return to that same coefficient, fill the other holes with disks and retain only its own arcs. This gives a noncrossing matching of its letters on a disk. Such a matching pairs at least two cyclically adjacent letters, which cannot be inverse in a cyclically reduced coefficient. Consequently the search can always choose one boundary in advance and contract across that boundary.

A particular letter occurrence must pair across if it has no inverse occurrence on that boundary. More generally, if an arc from it returns to an inverse occurrence on the same boundary, cutting along the arc gives a genus-zero surface on one side. Its oriented boundary consists of the intervening cyclic segment and some subset of the other coefficients. The two halves of the endpoint letters cancel in abelianization. The segment's abelianization therefore has to be the negative of a subset sum of the other coefficient vectors. If none of the possible inverse occurrences balances this way, the selected endpoint must pair across. Searching the partners of this endpoint gives every needed contraction. When no endpoint is forced, the search uses all endpoints of the shortest coefficient.

Contracting across a paired arc merges two rotated coefficients with those inverse letters at the seam. The usual spherical test applies to the shorter list after free and cyclic reduction. If the new word is trivial, remove both original coefficients. Recursing down to the two-boundary conjugacy test is exact for any retained boundary width. Capping the cache of previously rejected equations merely causes some exact recomputation. [Shared implementation](../experiments/round19_ak3_three_products.cpp).

## Independent controls

The independent literal ribbon-graph genus checker agrees with the new contraction rules on **9,000** balanced short equations, 3,000 at each boundary width seven, eight and nine. A separate negative at each width consists of repeated positive copies of the same commutator, whose central coordinate in the free class-two quotient rules out a spherical equality. Three independently replayed ordinary controls have nonprimitive source rows and reach the literal basis in four products with the prescribed receiver history. Their full elementary ledgers use **16, 18 and 20** instructions, respectively. The spherical witnesses of all control equations also replay as free equalities. [Pairing checks](../experiments/round21_ak3_four_products_controls.cpp), [strict control ledgers](../certificates/round21_ak3_four_products_controls.json), [independent census and replayer](../experiments/round21_ak3_four_products_verify.py).

## Reproduction

~~~sh
mkdir -p "$work"
c++ -O3 -std=c++17 -pthread experiments/round21_ak3_four_products.cpp -o "$work/four-products"
c++ -O3 -std=c++17 -pthread experiments/round21_ak3_four_products_controls.cpp -o "$work/pairings"
"$work/pairings"
head -9 certificates/round18_ak3_c33_low20.tsv > "$work/energy17.tsv"
python3 -B experiments/round21_ak3_four_products_verify.py --write-controls "$work"
for mode in AAB ABA ABB; do
  "$work/four-products" "$mode" "$work/$mode.tsv" 1 > "$work/$mode-control.json"
done
"$work/four-products" AAB "$work/energy17.tsv" 2 700000 > "$work/AAB.json"
"$work/four-products" ABA "$work/energy17.tsv" 12 1200000 > "$work/ABA.json"
"$work/four-products" ABB "$work/energy17.tsv" 2 700000 > "$work/ABB.json"
python3 -B experiments/round21_ak3_four_products_verify.py --check-controls "$work" \
  --source "$work/energy17.tsv" --receipt "$work/AAB.json" \
  --receipt "$work/ABA.json" --receipt "$work/ABB.json"
~~~
