# Stable length 18 and product bounds for AK(3)

2026-11-19. A degree-ten shortest stable path of length 18 can use at most one added pair. The exact signed integral exponent matrix requires seven products at one added pair and nine at two. At six and seven added pairs, the mod-two matrix increases the crossing lower bound by one product.

## Positive padding at degree ten

For a shortest stable path with peak rank $2+k$, the [normalization and cut bound](round-01-stable-disproof.md) put $2k$ instructions into rank changes and require at least $\lceil3(k+1)/2\rceil$ crossing products. The resulting lower bound at $k=5$ is 19 and increases with $k$. An ordinary path at degree ten therefore represents the $k=0$ case, and at stable budget 18 the possible positive values of $k$ are 1 through 4.

Erase the auxiliary letters while retaining the auxiliary rows. Each fixed-rank instruction projects to an allowed instruction or a wait. Truncate further to the lowest degree tested for each value of $k$. The boundary-only bidirectional search retains the two inner balls and checks the last frontier's transitions directly against the opposite ball.

| Added pairs | Middle budget | Retraction degree | Retained tuples from the two ends | Final boundary transitions |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 14 | 8 | 14,451,772 and 63,023,240 | 496,487,707 |
| 3 | 12 | 7 | 870,642 and 4,414,593 | 34,208,217 |
| 4 | 10 | 6 | 54,033 and 297,310 | 2,250,080 |

All three intersection tests are negative. The remaining one-pair case requires testing a degree-nine rank-two erasure at middle budget 16 or finding an additional constraint in degree eight. The degree-eight erasure contains a length-16 path obtained by appending the identity to the [unpadded degree-eight path](round-07-native-distances.md). Any successful length-16 degree-eight projection of a normalized positive-padding path must consist entirely of nonidentity moves, by the [degree-eight retraction exclusion at budget 15](round-08-magnus-distance.md). Its first crossing product must import an original row into the spare row. All three rows are then nonidentity because the two original rows have independent degree-one coefficients before that crossing. This gives a necessary condition on a degree-eight projected geodesic.

## Tight crossing schedules with six and seven added pairs

Contract the two original rows into vertex 0, track auxiliary row labels through swaps, and use an undirected edge for each crossing product. Every nontrivial cut has at least three edges by the [round-one incidence argument](round-01-stable-disproof.md). With six added pairs and exactly eleven products, every product crosses and there are six vertices of degree three and one of degree four. A doubled edge between two cubic vertices would give a cut of size two. Three edges on a pair give a cut of size at most one, and two doubled edges at the unique degree-four vertex would give a cut of size at most two around their three endpoints. Thus the graph is simple or has exactly one doubled edge incident to the degree-four vertex. With seven added pairs and exactly twelve products, all eight vertices are cubic, so the same two-vertex cut argument forces the graph to be simple.

For each marked degree profile, the graph enumerator visits the vertices in order and assigns every incident edge to a later vertex under its remaining degree. It keeps exactly the graphs with at least three edges across every cut, counting repeated edges with multiplicity. Simultaneously relabeling auxiliary vertices and their basis coordinates fixes the matrix test, so only one representative per orbit under relabelings fixing vertex 0 is needed. For six added pairs with vertex 0 cubic, the degree-four vertex is first relabeled to vertex 1. The two round-seven cubic graphs with five added pairs serve as controls.

For a fixed graph, assign a separate index to each edge, including both occurrences of a doubled edge. For each subset of edges, compute all distinct parity matrices realized by using each edge in that subset exactly once. The empty subset has the identity. To obtain the matrices for a larger subset, choose its last edge and apply either directed row addition to each matrix from the smaller subset. An edge incident to vertex 0 permits either actual original row. This recurrence retains all temporal edge orders.

Let $B=I+E_{10}$ be the terminal parity basis in the initial row coordinates. A prefix $P$ and suffix $S$ realize a terminal order if $SP=\Pi B$ for a permutation matrix $\Pi$. Equivalently, the sorted columns of $PB^{-1}$ and $S^{-1}$ agree. Each row addition is its own inverse modulo two, so the same recurrence for the complementary edge subset enumerates $S^{-1}$. The implementation uses nine rows throughout. Unused rows start and finish on isolated unit columns, which forces the column alignment to fix them. [Round-seven column test](round-07-stable-disproof.md).

| Added pairs | Degree of vertex 0 | Labeled graphs | Marked representatives | Prefix matrices | Inverse suffix matrices | Matches |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 3 | 70 | 2 | 35,142 | 177,128 | 0 |
| 6 | 4 | 2,070 | 7 | 1,913,066 | 9,936,534 | 0 |
| 6 | 3 | 2,070 | 25 | 5,184,448 | 26,009,722 | 0 |
| 7 | 3 | 16,800 | 8 | 12,199,560 | 12,199,560 | 0 |

These are exact counts of distinct matrices per graph and edge subset. Six added pairs require at least twelve products and seven added pairs require at least thirteen. In the free group the [three original-letter conjugations](round-06-stable-disproof.md#three-necessary-original-letter-conjugations-in-the-free-group) are additional instructions. Consequently a free stable budget of 26 needs $k\le5$, and a free stable budget of 29 needs $k\le6$.

## Integral exponent matrices with one and two added pairs

Use the integral basis of exponent rows from the initial padded presentation. The terminal matrix in standard order has original block

$$
B=\begin{pmatrix}-1&4\\-1&3\end{pmatrix},
\qquad
B^{-1}=\begin{pmatrix}3&-4\\1&-1\end{pmatrix}.
$$

The other block is the identity. Conjugations leave this matrix alone. Inversions can be commuted to the end of the product sequence by changing the signs of intervening row additions. Tracking row swaps through labels leaves the terminal matrix up to a signed row permutation $Q$. The same equation $SP=QB$ requires agreement of the column multisets of $PB^{-1}$ and $S^{-1}$ up to independent signs. To test this, replace each column by the lexicographically smaller of its two signs and sort. Both matrices are invertible, and no two columns are proportional, so a matching multiset determines a signed alignment.

The search tracks the crossing counts of every nonempty auxiliary subset. Counts can saturate at three because the cut condition only checks the combined threshold for both halves. Both signs of each addition are enumerated. A successful match also reconstructs a signed word in row additions, which is replayed from the identity to the signed terminal matrix.

| Added pairs | Product counts excluded | First signed matrix schedule | Matching state pairs at that size |
| ---: | ---: | ---: | ---: |
| 1 | 3 through 6 | 7 | 65 |
| 2 | 5 through 8 | 9 | 505 |

Smaller counts are excluded by the incidence bound. These are lower bounds on actual free-group product counts. The positive controls realize the required signed exponent matrices only. [Search receipts and signed witnesses](../results/round08_stable_disproof_searches.json).

## Reproduce

~~~sh
work=/tmp/ac-r08-stable-disproof
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round07_magnus_native.cpp -o "$work/native"
"$work/native" 8 2 14 --boundary-only > "$work/d8-k2-L14.json"
"$work/native" 7 3 12 --boundary-only > "$work/d7-k3-L12.json"
"$work/native" 6 4 10 --boundary-only > "$work/d6-k4-L10.json"
python3 -B experiments/round08_stable_disproof_graphs.py "$work/wide"
c++ -std=c++17 -O3 experiments/round08_stable_disproof_tight.cpp -o "$work/tight"
"$work/tight" "$work/wide/graphs.txt" > "$work/wide/parity.jsonl"
python3 -B experiments/round08_stable_disproof_signed.py 1 3 7 > "$work/signed-k1.jsonl"
python3 -B experiments/round08_stable_disproof_signed.py 2 5 9 > "$work/signed-k2.jsonl"
python3 -B experiments/round08_stable_disproof_report.py "$work" \
  | diff - results/round08_stable_disproof_searches.json
~~~
