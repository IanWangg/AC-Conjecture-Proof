# A stronger product bound at small positive padding

2026-11-19. For AK(3), a shortest normalized stable path whose peak uses $k$ added pairs with $1\le k\le5$ must make at least $\lceil3(k+1)/2\rceil+1$ right products. This refinement applies in the free group and in all the characteristic-two Magnus quotients. It rules out four added pairs through free stable length 19, and five through length 22. Three of the four positive padding ranks are also excluded at degree nine and stable budget 17.

## Crossing schedules in the initial basis

Track the row identities after absorbing swaps into their indices, and use the mod-two exponent vectors of the starting padded rows as a coordinate basis. Write $p=x^3y^{-4}$ and $b=xyxy^{-1}x^{-1}y^{-1}$. The terminal labels $x,y$ have signed coefficient rows $(-1,4),(-1,3)$ in the $(p,b)$ block, so mod two they give $p,p+b$. Each auxiliary terminal label has its original unit coefficient vector. Right products are additions of one row to another in these coordinates. The sign of a product, inversion of a row, and conjugation have no effect on this calculation.

For a stable length minimizer each cut separating a nonempty set of auxiliary rows from the original block has at least three crossings. Contract the two original rows to one vertex. The [round-one incidence bound](round-01-stable-disproof.md) requires at least $m=\lceil3(k+1)/2\rceil$ crossing products. If there are only $m$ total products, every one must cross two contracted vertices. In particular there can be no direct product between the original rows. We test this exact budget using only the condition of three crossings per cut. The exclusion permits both actual original row choices at every incident product.

For $k\le4$, the first search enumerates every ordered sequence of half the products forward from the identity matrix and the other half backward from each target basis permutation. It keeps one terminal permutation from each orbit under simultaneous permutations of auxiliary rows and auxiliary coordinate labels. Such a permutation fixes the start, the move menu, and the cut requirement. Each modulo-two product is its own inverse. At a matching midpoint the two exact crossing vectors add, so every cut can be checked.

An independent search avoids representatives of target permutations altogether. Let $B=I+E_{10}$ be the target with labels in their standard order, using zero-based indices. A product prefix $P$ and suffix $S$ reach a target order exactly when $SP=\Pi B$ for a permutation matrix $\Pi$. Equivalently $PB^{-1}=S^{-1}\Pi$. Thus the column multisets of $PB^{-1}$ and $S^{-1}$ must be equal. The matrices are invertible, giving a unique column alignment for any match. The second implementation compares the sorted columns of its two half-enumerations and adds their cut counts. It agrees with the orbit-weighted parity counts from the first program.

| Added pairs | Products tested | Parity matches across all target orders | Matches with every cut at least three |
| ---: | ---: | ---: | ---: |
| 1 | 3 | 0 | 0 |
| 2 | 5 | 24 | 0 |
| 3 | 6 | 4,368 | 0 |
| 4 | 8 | 2,728,488 | 0 |

## The tight five-padding graph

For $k=5$ the contracted multigraph has six vertices and nine edges. Every vertex has degree at least three, so all six have degree three. A pair of parallel edges would leave a cut of size at most two around its endpoints. Every cut of the contracted graph, up to taking the complement, is among those tested in the incidence theorem. The graph must therefore be simple cubic. Its complement is a simple two-regular graph on six vertices, so is either a six-cycle or two disjoint triangles. The corresponding cubic graphs are the triangular prism and $K_{3,3}$. Both are vertex-transitive, so one placement of the original block suffices per graph.

For each graph the column-multiset check now requires the prefixes and inverse suffixes to use complementary edge sets. Each edge is used exactly once, with either direction and (at the original block) either original row. Each graph gives 139,392 prefixes and 1,751,040 inverse suffixes, without a parity match. This completes the extra-product lower bound at all five stated ranks.

In the free group the [three original-letter conjugations](round-06-stable-disproof.md#three-necessary-original-letter-conjugations-in-the-free-group) add to the product bound. Inserting and deleting the padding adds $2k$. Thus for $1\le k\le5$ a globally shortest stable path using $k$ padded pairs in its normalization has length at least $2k+\lceil3(k+1)/2\rceil+4$. The earlier incidence and conjugation bounds exclude $k\ge6$ through length 22. Consequently free budget 19 requires $k\le3$, and free budget 22 requires $k\le4$. [Exact search and independent checks](../results/round07_stable_disproof_searches.json).

## Rank-two erasures at degree nine

At stable length 17, peak-rank normalization and the incidence bound restrict the added pairs to $k\le4$. Erase the auxiliary letters but retain the auxiliary rows. A path in the full padded degree-nine graph projects to such a rank-two retraction, with every instruction preserved or becoming the identity. Truncating further preserves this implication.

| Added pairs | Ordinary budget after rank changes | Tested retraction degree | Visited from the two ends |
| ---: | ---: | ---: | --- |
| 2 | 13 | 7 | 14,169,404 and 61,977,462 |
| 3 | 11 | 6 | 859,102 and 4,407,633 |
| 4 | 9 | 5 | 46,539 and 292,787 |

These exact balls are disjoint. The remaining one-padding exclusion at budget 15 in the middle graph is pending. The exact degree-nine stable distance 17 follows from the independently replayed rank-two path and the earlier length-16 exclusions. [Native distance results](round-07-native-distances.md), [erasure receipts](../results/round07_stable_disproof_searches.json).

## Reproduce

~~~sh
work=/tmp/ac-r07-stable-disproof
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round07_stable_disproof_incidence.cpp -o "$work/incidence"
for k in 1 2 3 4; do
  "$work/incidence" "$k" > "$work/incidence-$k.json"
done
python3 -B experiments/round07_stable_disproof_incidence_audit.py > "$work/incidence-independent.json"
python3 -B experiments/round07_stable_disproof_cubic.py > "$work/incidence-cubic.json"
c++ -std=c++17 -O3 experiments/round07_magnus_native.cpp -o "$work/native"
"$work/native" 5 4 9 > "$work/d5-k4-L9.json"
"$work/native" 6 3 11 > "$work/d6-k3-L11.json"
"$work/native" 7 2 13 > "$work/d7-k2-L13.json"
python3 -B experiments/round07_stable_disproof_report.py "$work" \
  | diff - results/round07_stable_disproof_searches.json
~~~
