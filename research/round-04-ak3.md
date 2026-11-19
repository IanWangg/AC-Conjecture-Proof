# Round 04 · Ordinary AK(3) trivialization

2026-11-19. A weighted basis index rules out a subgroup join between the complete cyclic cap-26 AK(3) component and 23,902 known-trivial cyclic pairs through energy 56, with arbitrary independent conjugation tails on both sides. A local search beyond cap 26 gives a strict 427-move witness of cyclic peak 27, together with 2,126 other new states. The searches leave ordinary AK(3) triviality open.

## Indexing short bases of a reverse subgroup

Let a forward cyclic pair \(R=(r,s)\) and a known-trivial reverse pair \(T=(u,v)\) each receive one arbitrary independent conjugation of its coordinates. The join condition is that the two generated subgroups become conjugate in \(F(x,y)\). Each pair generates a free group of rank two, since its ambient exponent vectors are a basis of \(\mathbb Z^2\). Accordingly each pair is an intrinsic free basis of its subgroup. A subgroup join suffices for a path, since Nielsen transformations connect any two bases of the same free group. This is the same join condition as the [round-one all-tail test](round-01-ak3.md#exact-subgroup-matching-for-a-single-independent-conjugation-phase-on-each-side).

Rather than expand all independent rotations of every cap-26 forward pair, index the signed, cyclically reduced forward coordinates and pairs. For a fixed reverse core \(K\), search its **intrinsic basis conjugacy classes**. A rank-two primitive conjugacy class is specified by its relatively prime exponent vector in a marked intrinsic basis. Also, two intrinsic primitive classes with vectors forming a matrix of determinant \(\pm1\) have representatives that form an intrinsic basis together. Indeed, lift the matrix to an automorphism of \(F_2\), then apply primitive conjugacy uniqueness to its two images. Thus any such pair of ambient cyclic classes found in the forward catalogue is precisely a subgroup join to \(K\). Independent forward conjugations select the required basis representatives. [Osborne and Zieschang, §3.2](https://geodesic.mathdoc.fr/item/IM_1981__63_142788/), [Kapovich and Myasnikov, Stallings graphs](https://arxiv.org/abs/math/0202285).

Suppress the valence-two vertices of the reverse core and retain the length and label of each resulting path. At an intrinsic slope \((a,b)\), the following bounds hold for the ambient cyclic length. Each term bounds the number of traversals of an edge path by the absolute value of its signed homology coefficient.

| Core | Intrinsic basis and lower bound |
| --- | --- |
| Figure-eight | For its two loop paths \(P,Q\), use \(P,Q\). The bound is \(|a||P|+|b||Q|\). |
| Theta | For three paths \(P,Q,R\) oriented between the two branch vertices, use \(PQ^{-1},PR^{-1}\). The bound is \(|a+b||P|+|a||Q|+|b||R|\). |
| Barbell | With lobes \(P,Q\) and bridge \(t\), use \(P,tQt^{-1}\). The bound is \(|a||P|+|b||Q|\), plus \(2|t|\) when both coefficients are nonzero. A closed loop visiting both lobes crosses the bridge in both directions. |

Take one sign of each relatively prime vector and enumerate all vectors whose bounds fit the forward cap less the minimum coordinate length. Construct the actual primitive cyclic representatives by an elementary Euclidean recursion on the two coefficients. Substitute the two graph basis words, reduce, and canonicalize up to cyclic rotation and inversion. The program then checks determinant, energy, and exact forward pair membership. The table is used only for lower bounds. The code separately checks that every constructed word respects its bound.

If the reverse relator axes meet, the reverse core is obtained by folding an independent rotation pair. The index tests every distinct such unbased core. If they are disjoint, their core is a geodesic barbell, with bridge \(t\) between two cyclic rotations of the relators. Write \(s=|P|+|Q|\) and \(L\) for the forward cap. Both pure slopes can occur together only when the reverse lobe pair is literally present in the forward signed cyclic catalogue, which is tested directly. If at least one coordinate is mixed, the barbell bound gives
\[
 2|t|\le L-s-\ell
 \quad\text{for one mixed and one pure coordinate},\qquad
 4|t|\le L-2s
 \quad\text{for two mixed coordinates},
\]
where \(\ell\) is the least length of an available pure lobe in the forward coordinate index. The first case is impossible when neither lobe is in the index. Enumerating the reduced bridges of these bounded lengths with the admissible outgoing labels is complete. No bound on independent conjugating words is assumed. [Cayley-tree menu proof](research-n-cyclic-search.md).

| Reverse archive energy cap | Known-trivial pairs | Rotation pairs | Distinct rotated cores | Relevant disjoint placements | Basis-pair lookups |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 32 | 9,257 | 1,117,474 | 486,726 | 295,016 | 324,539 |
| 56 | 23,902 | 6,230,442 | 2,675,055 | 295,016 | 324,917 |

Both runs use all 10,340,996 signed cyclic cap-26 forward pairs and 8,561,906 distinct forward coordinate classes. Neither finds a subgroup join. Figure-eight, theta and barbell positive controls all hit. The older rotational core matcher independently recovers the theta control. The barbell control requires a nonempty reverse bridge and independently replays from \((xyxyXY,y)\) to \((x,y)\) in seven strict moves. [Checked search and input hashes](../results/round04_ak3_searches.json), [barbell control certificate](../certificates/round04_ak3_barbell_control.json), [source archive and ordinary reverse ledgers](round-01-ak3.md).

## Broader joins on the 38 fixed forward cores

For the eight energy-15 escapes and the 31 cyclic vertices on the strict escape route, the combined list has 38 distinct pairs. For each displayed forward core we also allow an arbitrary intrinsic Nielsen basis change and then independent conjugations to match the selected basis words on the reverse side. The reverse side can independently conjugate the initial relators before choosing any intrinsic Nielsen basis. The [round-two fiber-product test](round-02-ak3.md) examines 42,464,012 reverse rotation comparisons through energy 32. Its only rank-two rotated target cases have the full ambient group as target, and every forward core has independently tested primitive absence. The finite signed partial-map test then checks 469,970,544 disjoint-bridge placements. No reverse target has two intrinsic lobe cycles, and every tested bridge placement has total fiber rank at most one. All comparisons were resolved. This stronger join test is specific to the 38 displayed forward subgroups. [Partial-map bridge proof](round-03-ak3.md#reverse-joins-and-finite-bridge-maps).

## First disjoint bridges of the energy-15 escapes

The eight pairs lie in one orbit under signed ambient basis permutations, so it suffices to use the two lobes \(P=\mathrm{XXYxYxy}\) and \(Q=\mathrm{XYXyxYYY}\). The complete first-bridge scan with shortest bridge length one through eight checks 183,680 literal legal placements. It checks each resulting source core and 40,551,312 two-copy joins. Every graph passes the signed transition DAG test. In this bounded first-disjoint scope, arbitrary Nielsen moves followed by another independent conjugation phase and a final Nielsen suffix cannot expose an ambient primitive. This complements the [round-three intersecting-axis scan](round-03-cyclic26.md).

There is also an unbounded regular family in the first-disjoint scope. Use the round-three unique-lobe criterion with the 30 signed cyclic rotations of \(P,Q\). Store the first and last eight bridge letters and reject an interior occurrence of any of the 30 words. An endpoint guard tests uniqueness of all signed lobe readings in the graph consisting of that lobe and its eight outward bridge letters. The two guards and interior test together are exact for uniqueness, since no forbidden word of length at most eight can use a lobe edge at both ends of a bridge of length at least eight. The two-copy proof then reduces to primitive absence in all lobe-rotation pair cores. The independent partial-map verifier resolves all 169 such pairs. The language count covers 58,562,158,364 of 65,086,642,154 legal length-20 placements. Some same-sign endpoint guards fail here. The exact language warrants the stated exclusion even for bridges of arbitrarily large length. One hundred twenty independent full folds reproduce the guard decisions, and independent closed-map certificates replay 2,628 two-copy checks on passing controls. [Round-three guard and shared-bridge proof](round-03-ac-disproof.md#allowing-repeated-full-bridge-readings).

## Two products over the cap-26 boundary

From the certified energy-15 pair, take every allowed cyclic product at cap 28 whose resulting energy exceeds 26, then every one-product successor still under cap 28. The complete geometric menu produces 340 first exits of energy 27 and 1,004 of energy 28. The union of these first and second layers adds 2,127 pairs to the cap-26 input, all of energy 27 or 28. It has no new low-energy return within this two-product scope. The extra pairs have no primitive coordinate, and their displayed cores pass the two-copy filter. The intrinsic-basis index then tests the full extra catalogue against all 23,902 reverse pairs with arbitrary tails on both sides and finds no join. One pair of energy 27 has a strict 427-move certificate, with raw peak 35 and cyclic peak 27. [Strict outward certificate](../certificates/round04_ak3_outward27.json), [local search receipts](../results/round04_ak3_searches.json).

## Reproduce

Regenerate the [cap-26 input](round-03-cyclic26.md) and the [round-one archives](round-01-ak3.md#replay-of-the-september-2026-paths). Use archive cap 56 and filter its reverse TSV at energy 32 to make the smaller reverse input. The commands below assume the cap-26 TSV is in `/tmp/ac-r03-cyclic` and the cap-56 reverse TSV is `/tmp/ac-r04-archive/reverse.tsv`.

~~~sh
work=/tmp/ac-r04-ak3
c26=/tmp/ac-r03-cyclic/c26.tsv
reverse56=/tmp/ac-r04-archive/reverse.tsv
python3 -B experiments/round04_ak3_replay.py "$work"
awk 'length($0)-1<=32' "$reverse56" > "$work/reverse32.tsv"
reverse32="$work/reverse32.tsv"
c++ -std=c++17 -O3 experiments/round04_ak3_basis_index.cpp -o "$work/basis-index"
c++ -std=c++17 -O3 experiments/round04_ak3_disjoint.cpp -o "$work/disjoint"
c++ -std=c++17 -O3 experiments/round01_ak3_all_tails.cpp -o "$work/reference"
c++ -std=c++17 -O3 experiments/round02_ak3_fiber_join.cpp -o "$work/fiber"
c++ -std=c++17 -O3 experiments/round03_ak3_bridge_maps.cpp -o "$work/bridge-maps"
c++ -std=c++17 -O3 experiments/round03_ak3_two_copy_frontier.cpp -o "$work/frontier"
"$work/basis-index" "$c26" "$reverse32" "$work/basis-matches.json"
"$work/basis-index" "$c26" "$reverse56" "$work/basis-matches56.json"
"$work/basis-index" "$work/barbell.tsv" "$work/reverse-control.tsv" "$work/barbell.json"
"$work/basis-index" "$work/rose.tsv" "$work/reverse-control.tsv" "$work/rose.json"
"$work/basis-index" "$work/theta-forward.tsv" "$work/theta-reverse.tsv" "$work/theta.json"
"$work/reference" "$work/theta-forward.tsv" "$work/theta-reverse.tsv" "$work/theta-reference.json"
"$work/fiber" "$work/forward.tsv" "$reverse32" rotations "$work/reverse-fiber.json"
"$work/bridge-maps" scan "$work/forward.tsv" "$reverse32" "$work/reverse-bridges.json"
"$work/disjoint" XXYxYxy XYXyxYYY 1 7 "$work/disjoint-hits.jsonl" "$work/disjoint-counts.json"
"$work/disjoint" XXYxYxy XYXyxYYY 8 8 "$work/disjoint8-hits.jsonl" "$work/disjoint8-counts.json"
python3 -B experiments/round04_ak3_bridge_language.py > "$work/language.json"
python3 -B experiments/round04_ak3_outward.py \
  certificates/round03_cyclic26_energy15_escape.json "$c26" "$work/outward"
"$work/basis-index" "$work/outward/novel.tsv" "$reverse56" "$work/outward/basis-matches.json"
"$work/frontier" "$work/outward/novel.tsv" literal \
  "$work/outward/two-copy-hits.jsonl" "$work/outward/two-copy.json"
diff certificates/round04_ak3_outward27.json "$work/outward/outward-witness.json"
diff certificates/round04_ak3_barbell_control.json "$work/outward/barbell-control.json"
python3 -B experiments/round04_ak3_replay.py "$work" --measure "$c26" "$reverse32" "$reverse56" \
  | diff - results/round04_ak3_searches.json
~~~
