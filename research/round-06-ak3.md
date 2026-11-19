# Round 06 · Ordinary AK(3) trivialization

2026-11-19. The low-length rank-two waypoint first found by stable transport is ordinarily reachable from AK(3). A strict 267-move path reaches the exact marked pair at cyclic peak 29, the least possible peak. The cap-29 component and a two-product continuation to cap 32 have no displayed primitive. The ordinary trivialization remains open.

## Ordinary transport to the marked waypoint

Take the marked endpoint $W=(\texttt{XXyxYxyXYxyXYxY},\texttt{XXyyxYY})$ of the earlier primitive deletion. The independent membership query misses its signed orbit at cap 28 and finds it at cap 29. Two complete disjoint balls of radii four and twelve and a joining edge give exact cyclic-product distance 17 to its signed orbit at cap 29, checking 1,034,682,848 products. Strictly lifting the orbit route initially gives 151 ordinary moves to a signed image of $W$ with raw and cyclic peak 29. [Stable source](round-05-stable-chart-transport.md), [checked cap-29 component](round-06-cyclic29.md).

To reach the actual marked pair, take the ambient relabeling $x\mapsto y^{-1},\,y\mapsto x^{-1}$. An independently enumerated seven-product route reaches the relabelled seed's literal signed cyclic class at cyclic peak 19. Normalize the two rows to the exact relabelled seed by allowed elementary moves. Now transport the instructions of the 151-move route into this marking and append row normalization. Only conjugator letters change in the transported instructions. The compiler replays all 267 moves in the original free group, using signed-letter conjugations, inversions, and right products. The final exact tuple is $W$, in the order displayed above, with raw and cyclic peak 29. [Exact marked certificate](../certificates/round06_ak3_marked_waypoint29.json).

An independent literal graph search gives exact cap-29 product distance **18** to the signed cyclic pair of $W$ in its original ambient marking. It checks 2,162,581,956 products and exhibits an edge between two disjoint balls of radii four and thirteen. Its shorter elementary replay uses 263 moves with raw peak 33 and cyclic peak 29. Thus the orbit distance 17 and the fixed-marking distance 18 are distinct. Neither figure is asserted to minimize the number of elementary moves. [Literal-route certificate](../certificates/round06_ak3_literal_waypoint29.json).

## Arbitrary-tail joins from cap 29

The reverse-basis lookup now accepts signed ambient orbits on the forward side. It first checks membership of a candidate coordinate up to signed ambient permutation, inversion and rotation. Its pair query applies the **same** ambient permutation to both coordinates, then sorts and minimizes over the eight permutations. This asks exactly the same question as a literal lookup in the full ambient expansion. Every signed image of the forward seed is already reachable at cap 22, so every orbit image in cap 29 is an ordinary waypoint. The old and compact implementations agree on the cap-28 rotation, core, bridge, slope, candidate-coordinate, basis-pair and topology counts.

The cap-29 scan checks all 35,968,003 forward orbits against 23,902 known-trivial reverse archive pairs. It considers 6,230,442 reverse rotation pairs, 2,675,055 distinct rotated cores, 2,747,792 relevant nonempty bridges, and 2,460,314 short intrinsic basis-pair lookups. It finds no subgroup join. The weighted basis lengths and the determinant condition cover arbitrary independent tails on both sides in this single matching-subgroup model. An agreement would produce an ordinary path by a common conjugation followed by a Nielsen basis change. [Join completeness](round-04-ak3.md#indexing-short-bases-of-a-reverse-subgroup), [scan and replay receipts](../results/round06_ak3_searches.json).

## Low-energy cap-29 entries and cap-32 continuation

Comparing the complete cap-28 and cap-29 components contributes 1,995 new signed orbits through energy 22. They consist of one at energy 17, 35 at 19, 112 at 20, 464 at 21 and 1,383 at 22. The unique first-energy orbit has representative $(\texttt{xxyxYXXy},\texttt{xyxyxyyXY})$. Its exact cap-29 orbit distance is 34 products. A 477-move ordinary certificate reaches the same orbit at raw peak 39 and cyclic peak 29. Its least cyclic entry peak is 29 by exclusion from cap 28. [Energy-17 certificate](../certificates/round06_ak3_energy17_escape29.json).

For all 1,995 seed representatives, a second-phase primitive test considers every intersecting-axis first placement and every two-copy join of its folded core. The 172,161 rotation placements contribute 82,683 distinct cores and 15,221,075 joins. The signed transition test verifies 15,293,966 graphs. The exact map test verifies the remaining 9,792. For the energy-17 representative, the disjoint first-bridge test exhausts lengths one through eight, with 236,160 placements, 62,528,992 joins and no primitive. These restrictions allow arbitrary Nielsen basis changes between the two independent conjugation phases and after them. [Two-copy argument](round-02-ac-disproof.md), [census receipts](../results/round06_ak3_searches.json).

From all 1,995 orbits, exhaust up to two cyclic products at cap 32 that leave the cap-29 component on the first step and stay outside it. After removing duplicates, the first layer adds 1,608,559 orbits and the second adds 5,572,027. The two layers enumerate 1,740,349,600 candidate products. The independent Euclidean scan finds no displayed primitive among all 7,180,586 orbits. There are also zero arbitrary-tail subgroup joins with the 23,902 known-trivial archive pairs, after 71,836 basis-pair lookups. The lowest new energy is 23. An independently replayed 300-move strict path reaches one of these energy-23 orbits at cyclic peak 31 and raw peak 43. The negative statement concerns this particular continuation. Paths that return through other cap-29 states or take more products lie outside the search. [Outward certificate](../certificates/round06_ak3_outward_energy23.json).

## Reproduce

Use the checked compact cap-28 and cap-29 TSVs and the reverse archive at energy 56 from the previous reports. The following builds the new programs and uses the two independent earlier route programs to recover the marked certificate.

~~~sh
work=/tmp/ac-r06-ak3
prior=/tmp/ac-r05-ak3
reverse=/tmp/round02-ak3/reverse56.tsv
mkdir -p "$work"
c++ -std=c++17 -O3 -pthread experiments/round05_ak3_orbit_path.cpp -o "$work/orbit-path"
c++ -std=c++17 -O3 experiments/round03_ak3_escape_path.cpp -o "$work/literal-path"
c++ -std=c++17 -O3 experiments/round06_ak3_orbit_index.cpp -o "$work/orbit-index"
c++ -std=c++17 -O3 -pthread experiments/round06_ak3_outward.cpp -o "$work/outward"
c++ -std=c++17 -O3 experiments/round03_ak3_two_copy_frontier.cpp -o "$work/two-copy"
c++ -std=c++17 -O3 experiments/round04_ak3_disjoint.cpp -o "$work/disjoint"
"$work/orbit-path" 29 XXyxYxyXYxyXYxY XXyyxYY "$work/stable-projection29.route.json"
printf 'XXyxYxyXYxyXYxY\tXXyyxYY\n' > "$work/waypoint.literal.tsv"
"$work/literal-path" 29 "$work/waypoint.literal.tsv" "$work/waypoint.literal.route.json"
python3 -B experiments/round03_ak3_escape_replay.py "$work/waypoint.literal.route.json" \
  "$work/waypoint.literal.cert.json" "$work/waypoint.literal.replay.json"
cmp "$work/waypoint.literal.cert.json" certificates/round06_ak3_literal_waypoint29.json
printf 'XXXXyyy\tXYXyxy\n' > "$work/seed-gamma.tsv"
"$work/literal-path" 22 "$work/seed-gamma.tsv" "$work/seed-gamma.route.json"
python3 -B experiments/round06_ak3_waypoint.py "$work/stable-projection29.route.json" \
  "$work/seed-gamma.route.json" "$work/waypoint.marked.json" > "$work/marked-replay.json"
cmp "$work/waypoint.marked.json" certificates/round06_ak3_marked_waypoint29.json
"$work/orbit-path" 29 xxyxYXXy xyxyxyyXY "$work/energy17.orbit-route.json"
python3 -B experiments/round05_ak3_lift_orbit_path.py "$work/energy17.orbit-route.json" \
  "$work/energy17.json" "$work/energy17.replay.json"
cmp "$work/energy17.json" certificates/round06_ak3_energy17_escape29.json
python3 -B experiments/round06_ak3_low_escapes.py "$prior/c28.orbit.tsv" "$prior/c29.orbit.tsv" \
  "$work/escape-short.tsv" 22 > "$work/low-escapes.json"
"$work/two-copy" "$work/escape-short.tsv" rotations \
  "$work/escape-short.two-copy-hits.jsonl" "$work/escape-short.two-copy.json"
"$work/disjoint" xxyxYXXy xyxyxyyXY 1 8 \
  "$work/energy17.disjoint-hits.jsonl" "$work/energy17.disjoint.json"
"$work/orbit-index" "$prior/c29.orbit.tsv" "$reverse" "$work/c29.reverse56.json"
"$work/orbit-index" "$prior/c28.orbit.tsv" "$reverse" "$work/c28.reverse56-control.json"
"$work/outward" 32 2 6 "$work/escape-short.tsv" "$prior/c29.orbit.tsv" \
  "$work/outward32.tsv" "$work/outward32.json"
python3 -B experiments/round05_ak3_orbit_audit.py primitive "$work/outward32.tsv" \
  > "$work/outward32.primitive.json"
"$work/orbit-index" "$work/outward32.tsv" "$reverse" "$work/outward32.reverse56.json"
"$work/orbit-path" 29 xxyXXYY xyxyXYxyXYxyXY "$work/outward32.entry.json"
python3 -B experiments/round06_ak3_outward_replay.py "$work/outward32.entry.json" \
  "$work/outward32.json" "$work/outward32.cert.json" > "$work/outward32.replay.json"
cmp "$work/outward32.cert.json" certificates/round06_ak3_outward_energy23.json
python3 -B experiments/round06_ak3_receipts.py "$work" results/round05_ak3_searches.json \
  | diff - results/round06_ak3_searches.json
~~~
