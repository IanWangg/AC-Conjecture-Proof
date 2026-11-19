# Round 07 · Ordinary AK(3) connection to the energy-23 waypoint

2026-11-19. The exact marked pair $W_{23}=(\texttt{XXXYxyxyXYY},\texttt{XYXYYXyXYYXy})$ is ordinarily reachable from AK(3) at cyclic peak **30**. This is the least possible cyclic peak, since the independently verified cap-29 ordinary component excludes every signed image of the pair. The target is a waypoint on the ordinary component. [Strict marked certificate](../certificates/round07_ak3_marked_waypoint30.json), [earlier stable path and cap-29 exclusion](round-06-stable-proof.md).

## Exact entry across the cap-29 component boundary

The reverse search starts at the orbit of $W_{23}$ and visits the full bounded cyclic-product graph at cap 30 until an orbit in the checked cap-29 component appears. Its complete ball of radius 16 is disjoint from cap 29. The first intersection at radius **17** occurs at the orbit represented below.

~~~text
xxyXYxyXYxyXY   xyxyXyxYXyxYXY
~~~

The search checks 11,008,776 candidate products and discovers 7,509 orbits before stopping. An exact bidirectional cap-29 search gives a 26-product path from AK(3) to the intersection orbit. Lift each edge of the concatenation in the marked basis, with the 17-product suffix reversed from the search direction. The resulting ordinary certificate to the exact $W_{23}$ uses 956 elementary moves and has raw peak 40. Its initial 170 moves reach the needed signed image of the AK(3) seed by ordinary moves. Every later elementary instruction is interpreted in that marking. The two macro segments have separately verified distances. The sum is the length of this constructed route. [Search and replay receipts](../results/round07_ak3_searches.json).

## The smaller component around the waypoint

At cap 29 the signed-orbit component of $W_{23}$ has **3,745** orbits and is disjoint from the AK(3) component. An independent wide-key verifier checks all 5,281,776 candidate products and 170,640 admissible products for closure and connectivity. The minimum cyclic total length is 18, attained by the orbit of $(\texttt{xxxyxyXXy},\texttt{xxyXyXYxy})$. The exact Euclidean scan of this component finds zero primitive coordinates. A separate weighted intrinsic-basis comparison with the 23,902 known-trivial archive pairs finds zero joins after arbitrary independent tails on both sides. This supplements the previous comparison of the single $W_{23}$ waypoint.

Continue the cap-30 entry by the five-product cap-29 route from $W_{23}$ to the energy-18 orbit. The 846-move strict ordinary certificate reaches one marked image with raw peak 40 and cyclic peak 30. The orbit is absent from the checked cap-29 AK(3) catalogue, so its minimum cyclic entry peak is also 30. It is the unique new energy-18 orbit in the cap-30 generator output. [Energy-18 certificate](../certificates/round07_ak3_waypoint_chamber18.json), [ordinary cap-29 catalogue](round-06-cyclic29.md).

Whitehead minimization and separately verified planar-link parity checks exclude geometry throughout the 3,745-orbit waypoint component. In a different test at cap 36, keep one donor of the energy-18 pair fixed up to conjugation and inversion. Three cyclic products through the other row reach 66,340 or 67,931 distinct recipient classes, depending on which donor is fixed. Neither sphere contains a primitive. This last test controls three products at the specified cyclic peak. [Weights and geometry convention](round-01-stable-proof.md), [bounded checks](../results/round07_ak3_searches.json).

## Full cap-30 search

The previous compact pair key was limited to total length 29. The new generator retains the two individual word codes separately and minimizes the pair under the same eight signed ambient basis permutations. It keeps one predecessor per discovered orbit to reconstruct routes immediately. The full cap-22 control reproduces the previous packed TSV and independent checker receipt byte-for-byte.

The cap-30 generator closes its queue at 73,876,424 orbits, with 78,886,780,816 candidate products and 4,543,003,748 admissible product checks. The independent Euclidean scan agrees that there is no primitive coordinate, and the full weighted basis index gives zero joins with the 23,902 known-trivial archive pairs after 3,462,820 basis-pair lookups. At the round handoff the independent cap-30 closure audit is still running. The independently checked universal lower bound on the cyclic peak to a primitive remains 30.

The new catalogue contains 95 orbits through energy 22, with counts 1, 2, 10, 37 and 45 from energies 18 through 22. Their 93 distinct Whitehead-minimal keys all give planar-link parity obstructions. The two-copy calculation at these sources covers 10,554 intersecting first-axis placements and 906,253 distinct-vertex joins. It excludes primitives in every case. The scope allows arbitrary Nielsen changes between the two independent conjugation phases and at the end. The first placement has intersecting axes. [Two-copy criterion](round-02-ac-disproof.md#finite-join-in-place-of-the-infinite-voltage-kernel), [generation and verification status](../results/round07_ak3_searches.json).

## Reproduce

Use the exact prior cap-22 and cap-29 compact TSVs and the energy-56 archive from the preceding rounds. The commands build the wide generator and checker, recover the two strict certificates, independently verify the disjoint cap-29 component, and run the full cap-30 audits.

~~~sh
work=/tmp/ac-r07-ak3
prior=/tmp/ac-r05-ak3
reverse=/tmp/round02-ak3/reverse56.tsv
mkdir -p "$work"
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_wide_orbits.cpp -o "$work/wide"
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_wide_verify.cpp -o "$work/verify"
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_waypoint_bridge.cpp -o "$work/bridge"
c++ -std=c++17 -O3 -pthread experiments/round05_ak3_orbit_path.cpp -o "$work/orbit-path"
c++ -std=c++17 -O3 experiments/round03_ak3_escape_path.cpp -o "$work/literal-path"
c++ -std=c++17 -O3 experiments/round06_ak3_orbit_index.cpp -o "$work/orbit-index"
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_frozen_sphere.cpp -o "$work/frozen-sphere"
c++ -std=c++17 -O3 experiments/round03_ak3_two_copy_frontier.cpp -o "$work/two-copy"

"$work/wide" 22 1 "$work/c22"
cmp "$work/c22.orbit.tsv" "$prior/c22.orbit.tsv"
"$work/verify" 22 1 "$work/c22.orbit.tsv" "$work/c22.verify.json"
cmp "$work/c22.verify.json" "$prior/c22.verify.json"

for cap in 29 30; do
  "$work/bridge" "$cap" 1000000 "$prior/c29.orbit.tsv" "$work/waypoint$cap"
done
"$work/orbit-path" 29 xxyXYxyXYxyXY xyxyXyxYXyxYXY "$work/waypoint30.prefix.route.json"
python3 -B experiments/round07_ak3_waypoint_replay.py "$work/waypoint30.prefix.route.json" \
  "$work/waypoint30.bridge.route.json" "$work/literal-path" "$work/waypoint30.marked.json" \
  > "$work/waypoint30.marked.replay.json"
cmp "$work/waypoint30.marked.json" certificates/round07_ak3_marked_waypoint30.json
python3 -B experiments/round07_ak3_waypoint_replay.py "$work/waypoint30.prefix.route.json" \
  "$work/waypoint30.bridge.route.json" "$work/literal-path" "$work/waypoint29.chamber18.json" \
  --continue-route "$work/waypoint29.lowest.route.json" > "$work/waypoint29.chamber18.replay.json"
cmp "$work/waypoint29.chamber18.json" certificates/round07_ak3_waypoint_chamber18.json
"$work/verify" 29 1 "$work/waypoint29.orbit.tsv" "$work/waypoint29.verify.json" \
  XXXYxyxyXYY XYXYYXyXYYXy
python3 -B experiments/round05_ak3_orbit_audit.py primitive "$work/waypoint29.orbit.tsv" \
  > "$work/waypoint29.primitive.json"
"$work/orbit-index" "$work/waypoint29.orbit.tsv" "$reverse" "$work/waypoint29.reverse56.json"
python3 -B experiments/round01_geometric_archive.py "$work/waypoint29.orbit.tsv" \
  > "$work/waypoint29.geometry.json"
"$work/frozen-sphere" 36 3 > "$work/chamber18.frozen36.json"

"$work/wide" 30 8 "$work/c30"
python3 -B experiments/round05_ak3_orbit_audit.py primitive "$work/c30.orbit.tsv" \
  > "$work/c30.primitive.json"
"$work/orbit-index" "$work/c30.orbit.tsv" "$reverse" "$work/c30.reverse56.json"
python3 -B experiments/round06_ak3_low_escapes.py "$prior/c29.orbit.tsv" "$work/c30.orbit.tsv" \
  "$work/c30.low22.tsv" 22 > "$work/c30.low22.json"
python3 -B experiments/round01_geometric_archive.py "$work/c30.low22.tsv" \
  > "$work/c30.low22.geometry.json"
"$work/two-copy" "$work/c30.low22.tsv" rotations "$work/c30.low22.two-copy-hits.jsonl" \
  "$work/c30.low22.two-copy.json"
python3 -B experiments/round07_ak3_receipts.py "$work" | diff - results/round07_ak3_searches.json
~~~

To finish the pending independent audit, run:

~~~sh
"$work/verify" 30 8 "$work/c30.orbit.tsv" "$work/c30.verify.json"
~~~
