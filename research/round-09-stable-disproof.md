# Padded exact corridors and exclusions at stable length 19

2026-11-19. The stable instruction distance of AK(3) in the degree-ten characteristic-two Magnus quotient is at least 19 for either target order. The crossing graph of a shortest stable path from any normally generating balanced tuple to the unordered positive basis contains two edge-disjoint spanning trees. With $k$ added pairs this gives at least $2k$ crossing products.

## Retractions and cut counts

As before, erase the added variables and retain the auxiliary rows at both ends. Test the resulting ordinary budget $19-2k$. The adaptive bidirectional search stores both inner balls, then tests each last-boundary transition directly against the opposite ball.

| Added pairs | Middle budget | Retraction degree | Radii | Retained tuples | Final boundary transitions |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 15 | 8 | $7+8$ | 265,103,602 and 63,023,240 | 2,206,422,978 |
| 3 | 13 | 7 | $6+7$ | 15,337,233 and 4,414,593 | 183,178,338 |
| 4 | 11 | 7 | $5+6$ | 872,891 and 297,500 | 13,305,834 |

All three intersection tests are negative. At degree ten the [product cutoffs](round-07-stable-disproof.md) exclude five or more added pairs for a shortest stable path of length at most 19. The exact retractions leave only zero or one added pair at this budget. The [free-group conjugation bound](round-06-stable-disproof.md#three-necessary-original-letter-conjugations-in-the-free-group) excludes four or more added pairs at free stable budget 19, so the same conclusion applies there. [Exact results](../results/round09_stable_disproof_searches.json).

At stable budget 18, the one-pair case is now excluded by the degree-nine retraction at middle budget 16. The successive degree-three through degree-nine midpoint counts are 232,448, 4,060,216, 250,833, 3,930, 132, 2 and 0. This handles the last padding rank left open by the [round-eight erasures](round-08-stable-disproof.md). The [round-eight degree-ten ordinary corridor](round-08-magnus-distance.md) excludes the unpadded case at budget 18. Together these prove the degree-ten stable lower bound of 19 for the unordered basis and hence for either target order. The one-pair free retraction at middle budget 17 is still open. [One-pair corridor receipt](../results/round09_stable_disproof_searches.json).

In the integral abelianization search, every auxiliary cut must receive at least three products as in [round eight](round-08-stable-disproof.md). For three auxiliary rows, all seven nonempty auxiliary subsets are tested simultaneously. The signed column-multiset search gives zero admissible matches at six, seven and eight products. At eight products each half contains 564,336 distinct pairs of a matrix and saturated cut counts. Thus a shortest free stable path peaking at rank five requires at least nine products, besides at least three original-letter conjugations and six rank changes.

## Two edge-disjoint spanning trees

Let the original tuple be balanced and normally generating, of arbitrary rank. Normalize a shortest stable path at its peak rank and absorb swaps into row labels. Write $O$ for the vertex contracting all original rows and keep one vertex for each of the $k$ auxiliary rows. Every crossing product gives one undirected edge, with separate edges for repeated products. The [round-one cut theorem](round-01-stable-disproof.md#necessary-relator-mixing-at-the-peak-rank) gives at least three edges across each nontrivial cut.

Use the initial rows as a coefficient basis modulo two. Each auxiliary column starts and ends with a single nonzero entry. For a fixed column, a product is active if its donor has entry one, so it toggles its recipient. Let $T$ contain its initial source and all actual rows touched by active products. For every row in $T$ except the initial source, select the product that first toggled it from zero to one. The donor already carried a one, so following these selected products back in time leads to the initial source. The selected products form a spanning tree on $T$.

Run the path backward and select the corresponding first toggles from zero to one. The backward initial source is the forward terminal singleton row. Reversal preserves the set of active products because a row addition is its own inverse modulo two and leaves the donor unchanged. The second tree therefore spans the same set $T$. Its edges are forward toggles from one to zero, so its product occurrences are disjoint from those of the first tree. On contracting the original rows, each tree has a connected image. Discard loops and choose a spanning tree in each image to get two edge-disjoint trees on the contracted image of $T$.

The maximal vertex sets admitting two such trees partition the crossing graph. Each singleton admits two empty trees. If two sets with tree pairs overlap, keep the trees on the first set and contract that set in both trees of the second. Each image remains connected and yields a tree on the new vertices and the contracted vertex. Attach the two resulting trees separately to the two trees of the first set. This gives two edge-disjoint trees on the union and proves that distinct maximal sets are disjoint.

In a maximal set $U$ without $O$, all rows are auxiliary. Each of their own columns stays supported in $U$ throughout the path, since its touched set lies in the maximal set containing its initial source. The submatrix on these rows and columns starts as the identity. Internal products act on it by row additions, and an incoming donor from outside $U$ has zero in all its columns. The submatrix stays invertible, so each row of $U$ always carries an auxiliary bit of $U$. A row of $U$ cannot donate to a row outside $U$, because that active product would take a column's touched set outside its maximal set.

Every edge between distinct maximal sets must therefore meet the set containing $O$. Any other maximal set would have at least three edges into that set by the cut theorem. Two of those edges suffice to join the two pairs of trees, using one joining edge per tree, contradicting maximality. The full crossing graph thus admits two edge-disjoint spanning trees, and every partition into $r$ nonempty parts has at least $2(r-1)$ edges between the parts. This includes the bound of $2k$ total crossing edges. The proof applies to free groups and characteristic-two Magnus quotients. In particular a shortest stable path of length $L$ has $k\le\lfloor L/4\rfloor$. For free AK(3), the [three necessary original-letter conjugations](round-06-stable-disproof.md#three-necessary-original-letter-conjugations-in-the-free-group) further give $k\le\lfloor(L-3)/4\rfloor$ when $k>0$.

## The extra product at small positive padding

At $k\ge5$ the new crossing bound already exceeds $\lceil3(k+1)/2\rceil$. At $k=3,4$, suppose a shortest path uses exactly $m=\lceil3(k+1)/2\rceil=2k$ total products. The cut theorem forces all products to cross. The $k+1$ contracted vertices all have degree three, except possibly one of degree four. A doubled edge must meet that exceptional vertex, since two cubic endpoints would give a cut of size two. Triple edges and two doubled pairs both violate the cut bound. There is at most one doubled pair.

For a fixed auxiliary column with touched row set $T$, the two trees on actual rows above show there are at least $2(n-1)$ active products, where $n=|T|$.

If the contracted image of $T$ is a proper vertex set, it has at most $n$ vertices of total degree at most $3n+1$, and its cut has at least three edges. Its internal edges therefore number at most $(3n-2)/2$. They include every active product, so

$$
2(n-1)\le (3n-2)/2,
$$

which gives $n\le2$. With two touched rows we need two edges between them, so a column with a proper touched image can be active only along the doubled pair, if it exists.

A column whose touched image is the whole graph must be active at every product, since it needs at least $2k$ active products. There can be at most one such auxiliary column because the first donor initially carries just one bit. Write $v$ for its initial row if this column exists. Every edge outside the doubled pair must then have a donor in $O$, in $v$, or at a doubled endpoint. Every other row retains its own bit from a column with proper touched image.

When the graph is simple, all edges must meet $O$ or $v$. For $k=4$ their combined degree is at most seven, below the eight required edges. For $k=3$ the simple cubic graph is $K_4$. The edge between $O$ and $v$, if $v$ exists, consumes one incidence at each, so the two vertices can meet at most five different edges.

It remains to consider $k=4$ with a doubled pair. There are six other edges. If the possible donor set occupies at most three vertices, its total degree is at most ten with four incidences already consumed. To meet all six other edges it must have exactly three vertices, use all six residual incidences, and have no other internal edge. One vertex of this set is outside the doubled pair and must have three distinct neighbors, with just two vertices available outside the set.

If the possible donor set has four vertices, the two doubled endpoints are auxiliary rows distinct from $v$. Each of their own columns is active only along the doubled pair. On those two rows and those two columns the matrix starts as the identity and changes only by invertible two-row additions. Each of these rows therefore always carries an auxiliary bit from a column other than $v$. Neither can donate outside the doubled pair. The six other edges must all meet $O$ or $v$, both cubic. To do so they must connect each of $O,v$ to each of the other three vertices. This gives each doubled endpoint two simple edges in addition to the two doubled edges, contradicting the existence of only one degree-four vertex.

This proves at least $\lceil3(k+1)/2\rceil+1$ products for arbitrary normally generating balanced tuples with $k\ge3$, in the free group and the characteristic-two Magnus quotients. For AK(3), combine this with the [small-padding checks](round-07-stable-disproof.md) at $k=1,2$. A free shortest stable path of length $L$ with positive padding must then satisfy $k\le\lfloor(2L-11)/7\rfloor$, after charging the three original-letter conjugations. The corresponding characteristic-two bound is $k\le\lfloor(2L-5)/7\rfloor$.

## Native lifts with spare rows and exact free endpoints

The native corridor works with two original rows and up to three spare rows in the rank-two retraction. Padded searches begin at degree three and keep all the spare rows at each stage. At every lift, project each high row separately while preserving its position. Apply a candidate instruction in that projected order, then sort the result when looking up the allowed lower corridor. This screens the instruction before evaluating its high-degree image. A move can fix the projected tuple and still change the high tuple. At the selected last stage the same lift can evaluate actual reduced free words, with projection given by the truncated Magnus expansion of each word. The selected last stage can keep row order and treat swaps as instructions. [Generalized native implementation](../experiments/round08_magnus_native_corridor.cpp).

The optional first-arrival search assigns each high state just its earliest discovered tick. To see completeness, take any midpoint of a successful high path and replace each of its half paths by a high shortest path to that midpoint. Wait at the midpoint to fill any saved ticks. The projection is still a complete low path, so at every tick the projected state of the shortened half lies in the existing low corridor. Each prefix of a shortest half is shortest as well, so the screened breadth-first search finds its states at those same earliest ticks. Thus the intersection of the two screened high balls contains every successful midpoint. Conversely, an intersection supplies two actual high paths. Backward trimming recovers all bounded paths through the midpoint set using each state's recorded start distance as its earliest tick.

The legacy degree-six controls preserve the complete midpoint counts at budgets 11 and 12. At augmented budget 12 the unordered degree-six search leaves one midpoint and gives an explicit 12-move path. The ordered version has no midpoint. Lifting the unordered result to the free-word tier eliminates its remaining midpoint. The first-arrival mode agrees with the layered mode on widths, midpoint counts and the answers to the selected controls. The independent monomial-set replayer checks the positive ledgers. [Controls and replay receipts](../results/round09_stable_disproof_searches.json).

## Reproduce

~~~sh
work=/tmp/ac-r09-stable-disproof
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round07_magnus_native.cpp -o "$work/native"
"$work/native" 8 2 15 --boundary-only > "$work/d8-k2-L15-native.json"
"$work/native" 7 3 13 --boundary-only > "$work/d7-k3-L13-native.json"
"$work/native" 7 4 11 --boundary-only > "$work/d7-k4-L11-native.json"
python3 -B experiments/round08_stable_disproof_signed.py 3 6 8 > "$work/signed-k3.jsonl"
c++ -std=c++17 -O3 experiments/round08_magnus_native_corridor.cpp -o "$work/corridor"
"$work/corridor" 6 6 6 --screen --ledger > "$work/screen-control6-L12.json"
"$work/corridor" 6 6 6 --spare-rows 1 --ordered --ledger > "$work/padded-control6-L12-ordered.json"
"$work/corridor" 6 6 6 --spare-rows 1 --ledger > "$work/padded-control6-L12.json"
"$work/corridor" 6 6 6 --spare-rows 1 --ledger --first-arrivals > "$work/first-padded-control6-L12.json"
"$work/corridor" 6 6 6 --spare-rows 1 --free --ledger > "$work/padded-free-control6-L12.json"
"$work/corridor" 6 6 6 --spare-rows 1 --free --ledger --first-arrivals > "$work/first-padded-free-control6-L12.json"
"$work/corridor" 7 7 7 --spare-rows 1 --ledger > "$work/padded-control7-L14.json"
"$work/corridor" 7 7 7 --spare-rows 1 --ledger --first-arrivals > "$work/first-padded-control7-L14.json"
"$work/corridor" 9 8 8 --spare-rows 1 > "$work/d9-k1-L16-corridor.json"
python3 -B experiments/round09_stable_disproof_report.py "$work" \
  | diff - results/round09_stable_disproof_searches.json
~~~
