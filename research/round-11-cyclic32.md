# Generated cyclic cap-32 component of AK(3)

2026-11-19. The incremental ordinary search exhausted the cyclic cap-32 component. It added **285,484,620 signed orbits** to the independently checked 254,220,523 at cap 31, for **539,705,143** in all. The generator found no primitive coordinate, and a separate Euclidean scan confirms this for 101,668,360 sign-pure coordinate occurrences among the additions. This gives a generated lower bound of **33** for the cyclic peak of an ordinary AK(3) trivialization. The independent boundary and outside-closure checks are in progress. [Search and replay receipts](../results/round11_cyclic32.json), [independent cap-31 verification](round-10-independent-closures.md).

## Completed expansion

The search read all 1,073,329,989 anchored boundary records generated from the cap-31 catalogue and deduplicated them to 281,402,118 seeds. Expanding every new orbit under the bounded product menu discovered a further 4,082,502. The expansion checked 328,010,482,664 product candidates and admitted 12,567,099,338. The queue closed. Among the new orbits, 1,424,917 have energy at most 31, including two of energy 20. The ancestry ledger has one 32-byte record per outside orbit. The ordinary cyclic product theorem accounts for arbitrary conjugating tails through rotations and shortest bridges. [Boundary coverage and incremental algorithm](round-10-ak3.md), [cyclic product theorem](research-n-cyclic-search.md).

## A sharp entry at energy 20

The new marked pair `(xxxxxyXXy, xxyxxyyXYXY)` reaches energy 20. Its saved cap-32 route has fourteen cyclic products following a cap-31 anchor. A backwards cap-31 search reaches a verified cap-29 orbit in six cyclic products, and another six reach the cap-22 catalogue. Restoring all markings and expanding the cyclic products gives a strict **687-instruction** ordinary route from AK(3), with raw peak **47** and cyclic peak **32**. The energy-20 pair is absent from the complete energy-20 prefix of the independently verified cap-31 catalogue, so its entry peak is sharp. [Strict ledger](../certificates/round11_ak3_cap32_minimum.json), [marking-preserving compiler](../experiments/round11_ak3_cap32_minimum.py).

An all-tail basis lookup against 23,902 known-trivial archive pairs finds no join among all **1,424,917** new orbits through energy 31. The lookup allows independent conjugations of both coordinates on both sides. An alternating cyclic-product and Whitehead-minimization search rooted at both new energy-20 orbits reaches 15,981 short Whitehead classes in six layers at product cap 36, frontier cap 31 and beam width 192. It finds no primitive product or all-tail basis join to the same archive. [Archive method](round-04-ak3.md), [Whitehead search method](round-09-ak3.md), [search receipts](../results/round11_cyclic32.json).

## Reproduction

Use the complete cap-31 catalogue and its cap-32 boundary file from Round 10. For the cap-31 bridge, extract the energy-at-most-24 prefix of the cap-29 catalogue. The second bridge uses the complete cap-22 catalogue. All three lower catalogues are in signed-orbit TSV format. [Catalogue and boundary commands](round-10-ak3.md#reproduction), [independent extension check](round-11-incremental-closure.md).

~~~sh
mkdir -p "$work"
c++ -std=c++17 -O3 -pthread experiments/round10_ak3_frontier.cpp -o "$work/frontier"
c++ -std=c++17 -O3 experiments/round07_stable_proof_waypoint_search.cpp -o "$work/backwards"
c++ -std=c++17 -O3 experiments/round03_ak3_escape_path.cpp -o "$work/literal-path"
"$work/frontier" expand 32 16 "$cap31" "$work/c32" 0 "$boundary32"
awk 'length($0) <= 25 {print} length($0) > 25 {exit}' "$cap29" > "$work/cap29-low24.tsv"
"$work/backwards" 31 3000000 xxyxyXYYXyxYXy xyxyxyXYxyXYYXy "$work/bridge" "$work/cap29-low24.tsv"
"$work/backwards" 29 3000000 xxyxxyXYYXy xxyXYxyXYXYXy "$work/inner" "$cap22"
python3 -B experiments/round11_ak3_cap32_minimum.py "$work/c32.minimum.route.json" \
  "$work/bridge.route.tsv" "$work/inner.route.tsv" "$work/literal-path" "$work/energy20.json"
python3 -B experiments/elementary_verify.py "$work/energy20.json"
c++ -std=c++17 -O3 experiments/round06_ak3_orbit_index.cpp -o "$work/orbit-index"
c++ -std=c++17 -O3 experiments/round09_ak3_whitehead_products.cpp -o "$work/whitehead-products"
awk 'length($0) <= 32 {print} length($0) > 32 {exit}' "$work/c32.outside.tsv" > "$work/through31.tsv"
"$work/orbit-index" "$work/through31.tsv" "$reverse" "$work/through31.join.json"
head -2 "$work/c32.outside.tsv" > "$work/energy20.tsv"
"$work/whitehead-products" 36 31 6 192 "$work/energy20.tsv" "$work/classes.tsv" "$work/whitehead.edges.tsv"
"$work/orbit-index" "$work/classes.tsv" "$reverse" "$work/whitehead.join.json"
~~~

Set `reverse` to the verified cap-56 archive index. [Archive replay and index generation](round-04-ak3.md#reproduction).
