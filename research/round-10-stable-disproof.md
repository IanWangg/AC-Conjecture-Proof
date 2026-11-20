# Excluding stable length 19 in degree ten

2026-11-19. AK(3) needs at least **20 instructions** to reach either order of the standard basis in the degree-ten characteristic-two Magnus quotient, both ordinarily and stably. The same lower bounds apply in the free group. The remaining one-padding case is excluded by identifying every vertex in the complete degree-nine retraction corridor at middle budget 17. [Native corridors](../results/round10_stable_disproof_corridors.json) · [Independent degree-nine saturation](../results/round10_stable_disproof_saturation.json)

## Ordinary and free exclusions

The complete unpadded degree-ten search uses radii 9 and 10. Successive degrees four through ten retain 5,786,782, 19,799,763, 234,604, 11,965, 798, 76 and zero midpoint states. It excludes the unordered basis, hence either marked order as well. Projection sends every free ordinary path to a quotient path of no greater length.

For stable budget 19 the round-nine retractions already exclude $k=2,3,4$ added pairs. The $2k$ crossing products and $2k$ rank changes exclude $k\ge5$. Exact free-word lifting of the one-spare retraction at radii 8 and 9 also gives zero midpoints. This independently closes the free case. [Earlier positive-padding exclusions and two-tree bound](round-09-stable-disproof.md)

## One added pair in the Magnus quotient

Erase the added variable and retain its row. The complete one-spare, degree-nine corridor at middle budget 17 goes from the unordered triple $(p,b,1)$ to $(x,y,1)$. Its widths with the same global clock on both sides are

~~~text
1 3 3 3 2 2 2 2 2  2 4 5 6 5 4 3 3 1
~~~

Take the two existing unpadded 17-step degree-nine paths, one for each explicit target order, and replay them independently using monomial sets. For witnessed states at layers $t$ and $t+m$, enumerate every ordinary bridge of $m=2,3$ steps and add the penultimate state at layer $t+m-1$. Each new state is on a full path by concatenating an existing prefix, the bridge and an existing suffix. Iterate at each bridge length until no layer grows. These unpadded witnesses reach all the widths listed above. Adding an identity row embeds their unordered states injectively in the padded corridor. Equality of finite cardinalities at every layer therefore proves that every padded degree-nine corridor vertex has an identity row. A separate native unpadded search reproduces the same widths. [Original degree-nine ledgers](round-07-native-distances.md) · [Witness and corridor comparison](../results/round10_stable_disproof_saturation.json)

Suppose a shortest stable path of at most 19 instructions in degree ten uses one added pair. Normalize and absorb row swaps into row labels. Its ordinary part has at most 17 instructions. Both directions of crossing between the original rows and spare occur. If all crossings pointed one way, the rank-reduction argument for the cut bound would remove the spare and shorten the stable path. In the degree-nine retraction, up to the first crossing whose recipient is the spare, that row stays the identity. Earlier products with the spare as donor act trivially in the retraction. The two original rows continue to have independent original mod-two exponent vectors, since original products are invertible row additions and every conjugation or inversion preserves their mod-two vectors. The first product importing an original row makes the spare nonidentity, and leaves both original rows nonidentity. Its projected state would thus have three nonidentity rows inside the complete 17-tick corridor, a contradiction. This argument applies unchanged to the free group. [Directional cut argument](round-01-stable-disproof.md#necessary-relator-mixing-at-the-peak-rank)

The saturation test is useful whenever witnesses using a smaller set of active rows match all widths of a larger complete erasure corridor. At the next budget, a one-padding path would require at least 18 effective instructions in the degree-nine retraction. In particular a degree-ten candidate of total stable length 20 with one padding pair cannot conjugate by the erased generator, since that instruction would leave at most 17 effective steps.

## Initial exclusions at budget 20

The two-tree bound excludes all $k\ge6$ at stable budget 20. Exact boundary searches also exclude $k=4$ through a degree-seven retraction of middle budget 12 and $k=5$ through a degree-six retraction of middle budget 10. They check 39,672,547 and 2,550,224 final boundary candidates respectively. The five-pair case is already excluded in the free group by the original-letter conjugation bound. The three-pair degree-seven retraction at middle budget 14 has a midpoint with all three spare rows equal to the identity. Such idle paths are consistent with the earlier exact unpadded degree-seven distance of 14. The three-pair case remains open at this budget. [Budget-20 receipts](../results/round10_stable_disproof_budget20.json) · [Unpadded degree-seven result](../results/round03_magnus_degree7.json)

The saturated degree-nine corridor consists of 53 distinct unpadded vertices. A separate search takes their closed neighborhood of radius four in the degree-nine instruction graph, containing 487,205 vertices. The induced subgraph has 101 low midpoints at radii 10 and 10. Lifting the two halves through their trimmed lower corridors gives zero degree-ten common states. Thus every degree-ten ordinary path of length at most 20 would project to at least one vertex farther than four instructions from every degree-nine geodesic. This conclusion only excludes the specified neighborhood. [Neighborhood generator and exact lift](../experiments/round10_stable_disproof_neighborhood.py)

## Reproduction

The two large searches reproduce the saved exact corridor widths. The saturation check takes the saved profiles as upper bounds and separately certifies that unpadded paths attain every width.

~~~sh
work=/tmp/ac-r10-distance
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round08_magnus_native_corridor.cpp -o "$work/corridor"
"$work/corridor" 10 9 10 --free --ledger > "$work/ordinary-L19-corridor.json"
"$work/corridor" 9 8 9 --spare-rows 1 --free --ledger --first-arrivals > "$work/one-padding-L17-corridor.json"
"$work/corridor" 9 8 9 --first-arrivals --ledger > "$work/unpadded-d9-L17.json"
python3 -B experiments/round10_stable_disproof_saturate.py \
  | diff - results/round10_stable_disproof_saturation.json
c++ -std=c++17 -O3 experiments/round07_magnus_native.cpp -o "$work/native"
"$work/native" 7 4 12 --boundary-only
"$work/native" 7 3 14 --boundary-only
c++ -std=c++17 -O3 experiments/round10_stable_disproof_padding5.cpp -o "$work/padding5"
"$work/padding5"
python3 -B experiments/round10_stable_disproof_neighborhood.py 4 20
~~~
