# Unbounded primitive-coordinate search from cyclic cap 32

2026-11-19. None of the **539,705,143** signed orbits in the generated ordinary AK(3) cap-32 component can expose a primitive coordinate in one cyclic product of any output length. The test covers arbitrary conjugating tails, row inversion and either receiving row. Thus an ordinary trivialization must leave the generated cap-32 component before the product that first exposes a primitive. The complete independent cap-32 first-exit audit confirms all 1,073,329,989 anchored records and reproduces the 34,346,559,648-byte boundary ledger byte for byte. The independent outside-closure check is in progress. [Source catalogues](round-11-cyclic32.md), [complete boundary audit](../results/round12_c32_boundary.json), [search and independent control receipts](../results/round12_ak3_primitive_step.json).

## A complete product test at every output length

Let the two cyclically reduced words in a given orientation have lengths $n,m$. The product has abelianization $(s,t)$ equal to the sum of the two input exponent vectors. A cyclic primitive with those exponents has length $L=|s|+|t|$, is sign-pure, and has the Euclidean slope word up to cyclic rotation. If the relator axes are disjoint, a shortest conjugating bridge of positive length $d$ gives cyclic product length $n+m+2d>L$. Only the intersecting-axes case remains, whose cyclic products are products of rotations. Fixing the receiver orientation loses no primitive classes, since reversing both orientations inverts the cyclic product. [Axes and product completeness](research-n-cyclic-search.md), [Euclidean primitive test](../experiments/euclidean_primitive_audit.py).

If a primitive product leaves a nonempty arc from each word, it cancels $r=(n+m-L)/2<\min(n,m)$ letters in each. The suffix and prefix removed from either word are a single contiguous cyclic arc. The two removed arcs read as inverses. Rotating so the entire cancellation occurs at the joining seam therefore produces the same surviving cyclic word. The tester tries each removed arc in one word, matches its inverse arc in the other, and checks both survivor arcs for the required signs and their cyclic product for the Euclidean primitive form. Conversely, every returned pair of rotations multiplies to the displayed cyclic primitive.

If one word is consumed entirely, its full inverse rotation must occur as a contiguous cyclic arc of the longer word. After cutting out that occurrence, the leftover arc can cyclically reduce further. The tester tries every occurrence of every rotation of the shorter word and checks the reduced leftover. This covers the case $r\ge\min(n,m)$ without making an upper-bound assumption about the primitive length.

An independent Python implementation checks the entire exact rotation menu on 769 distinct control pairs. The native test agrees on 674 negative cases and gives replayable primitive products for all 95 positive cases, with complete consumption in 55. The AK(2) reachable control gives the primitive `XyyXyyXy`, and the binary-record mode preserves its parent and rejects a truncated record. [Native scanner](../experiments/round12_ak3_primitive_step.cpp), [independent controls](../experiments/round12_ak3_primitive_step_audit.py).

## First excursion at cyclic energy 33

For the 59,515 new cap-32 states through energy 29, the cap-33 boundary generator agrees with the separate reference menu on every source. It writes 130,884 anchored first-product records after batch deduplication. Testing the second product with no output energy bound gives zero primitive coordinates. This exhausts the two-product pattern with an intermediate of energy exactly 33 for these sources. The boundary cap is a condition on the first product only. The corresponding first-product scans from the full cap-32 catalogue are in progress. [Boundary method](round-10-ak3.md), [complete short-source receipts](../results/round12_ak3_primitive_step.json).

## The second sharp energy-20 waypoint

A separate reverse search from `(xxxxyXXYY, xxyyxYYYxxY)` gives a 36-product route at cyclic cap 32 to a cap-22 orbit. Lifting its signed markings, replaying a cap-22 entry and expanding the products give a strict **1,037-instruction** route with raw peak **41** and cyclic peak **32**. The pair is absent from the independently audited cap-31 component, so its entry peak is exactly 32. This makes both new energy-20 waypoints available as literal ordinary sources for the proper-overgroup and chart tests. [Strict ledger](../certificates/round12_ak3_second_energy20.json), [cap-31 membership check](round-11-cyclic32.md).

## Reproduction

Use the cap-31 orbit file and the cap-32 outside TSV from [Round 11](round-11-cyclic32.md). The cap-22 file below is the signed orbit catalogue.

~~~sh
mkdir -p "$work"
c++ -std=c++17 -O3 -pthread experiments/round12_ak3_primitive_step.cpp -o "$work/primitive-step"
c++ -std=c++17 -O3 -pthread experiments/round10_ak3_frontier.cpp -o "$work/frontier"
python3 -B experiments/round12_ak3_primitive_step_audit.py "$work/primitive-step"
"$work/primitive-step" "$cap31" 6
"$work/primitive-step" "$outside32" 9
awk 'length($0) <= 30 {print} length($0) > 30 {exit}' "$outside32" > "$work/through29.tsv"
"$work/frontier" seed 33 8 "$work/through29.tsv" "$work/c33-short" 0 0 audit
"$work/primitive-step" "$work/c33-short.boundary.bin" 6 --boundary
c++ -std=c++17 -O3 experiments/round07_stable_proof_waypoint_search.cpp -o "$work/backwards"
c++ -std=c++17 -O3 experiments/round03_ak3_escape_path.cpp -o "$work/literal-path"
"$work/backwards" 32 2000000 xxxxyXXYY xxyyxYYYxxY "$work/energy20" "$cap22"
python3 -B experiments/round12_ak3_short_entry.py "$work/energy20.route.tsv" \
  "$work/literal-path" "$work/energy20.strict.json"
python3 -B experiments/elementary_verify.py "$work/energy20.strict.json"
~~~
