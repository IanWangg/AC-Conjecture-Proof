# Completed ordinary cap-33 generation and independent checks

The native ordinary cap-33 search closes after expanding **1,318,624,663** outside orbits, starting from **1,258,633,777** compacted first-exit seeds. Together with the verified cap-32 component, there are **1,858,329,806** signed orbits. The search checks **1,636,187,542,080** candidate products and admits **66,651,281,822**. It gives a generated ordinary cyclic peak lower bound of **34** for trivializing AK(3). The independent primitive audit is complete and the independent full closure audit is running. [Generation and audit receipts](../results/round18_ak3_cyclic33.json), [cap-32 verification and cap-33 seed provenance](round-14-independent-cyclic32.md).

The separate packed audit checks all **1,318,624,663** outside rows and finds zero primitive occurrences among **311,133,869** sign-pure coordinates. The unbounded primitive-product test also finds zero hits in the **59,990,886** further orbits discovered beyond the first-exit seeds. Round 12 covered every lower orbit, and Round 13 covered every first-exit seed. Thus every orbit in the generated cap-33 component fails the one-product primitive test with arbitrary conjugating tails and output length. [Complete receipt](../results/round18_ak3_cyclic33.json), [lower-component product test](round-12-primitive-step.md), [first-exit product test](round-13-cap33-two-products.md).

## A sharp entry at cyclic energy 17

One of the nine minimum-energy additions has literal marking `(xxyXYY, xxxxYxYxYXY)` and cyclic energy **17**. The recorded route uses twelve cyclic products after its cap-32 anchor. Applying the marking-preserving compiler with the two saved lower routes gives a strict ordinary path from AK(3) in **879** instructions at cyclic peak **33** and raw peak **39**. The signed target orbit is absent from all 616 cap-31 catalogue rows through energy 17 and the cap-32 addition catalogue has no rows in that range. Its exact ordinary entry peak is therefore 33. [Strict ordinary ledger](../certificates/round18_ak3_c33_minimum_ordinary.json), [anchored orbit path](../certificates/round18_ak3_c33_minimum_orbit.json), [checked receipt](../results/round18_ak3_c33_minimum.json).

The new arbitrary two-product test gives no primitive from this exact marking. Its $K_4$ planar link has a one-equation parity contradiction. Separate symmetric-group tests leave two slope residues modulo four in each fixed-donor direction. Every surviving slope parameter of absolute value at most 24 also fails the three-stage graph completions. The fixed-donor replacement question outside these checks remains open. [Two-product test](round-18-ak3.md), [all checks on this marking](../results/round18_ak3_c33_minimum.json).

The cap-33 additions through energy 20 comprise **nine** energy-17, **59** energy-19 and **16** energy-20 orbits. All **84** fail the arbitrary two-product primitive test and give literal $K_4$ planar-link parity contradictions. The simultaneous ambient-equivalence and the arbitrary-tail subgroup comparisons both give zero joins to the verified 23,902-pair archive. [Complete short catalogue](../certificates/round18_ak3_c33_low20.tsv), [tests](../results/round18_ak3_cyclic33.json).

## Independent closure and attachment

The verifier stores each pair once in an indexed catalogue. The flat membership slots store 32-bit indices and compare both full coordinate keys on every lookup, including after hash collisions. The cap-33 command allocates an 8 GiB slot table. All reductions, candidate products and new-orbit attachments use the independent stack implementation. The lower catalogue can be read from multiple disjoint files.

In complete-extension mode, scan all old sources for products of exactly the new cap and all new sources for products of at most the cap. Products of smaller energy from old sources are covered by the already verified lower closure. An optional seed-manifest pass also checks that each compacted first-exit child and its recorded old anchor occur in the appropriate catalogues. This explicitly covers a first-exit child attached only to old nodes. Such a child would escape an outside-only closure audit if omitted from both its catalogue and the scan sources. The ready-to-use audit is an independent check on the generated cap-33 result. [Verifier](../experiments/round07_ak3_wide_verify.cpp).

The cap-22 control compares map, flat and split-manifest outputs byte for byte on **32,363** orbits. The complete mode independently checks **13,164** compacted seeds, **13,004,928** old-source candidates and **11,215,112** new-source candidates. A duplicated source, an undersized table and an omitted boundary state each trigger separate failure checks. [Control receipts](../results/round18_ak3_cyclic_verify_controls.json).

## Independent primitive enumeration

The packed primitive verifier precomputes every cyclic rotation of each signed Christoffel primitive word through width 31. The primitive classification in rank two gives one cyclic primitive class for every relatively prime pair of signed exponent sums. For positive counts $a,b$, place the $b$ letters of the second generator at the increments of $\lfloor ib/(a+b)\rfloor$. Include the four length-one words. The verifier checks both coordinates of each exact 32-byte ledger row under this classification. [Rank-two primitive language](research-q.md), [packed audit](../experiments/round18_ak3_cyclic_primitives.cpp).

An independent Euclidean fixture supplies **26,128** signed and rotated positive occurrences and an equal number of negatives. They all classify as expected. The full cap-32 addition control exactly reproduces the prior **101,668,360** sign-pure coordinate occurrences across **285,484,620** rows, with zero primitive hits. [Controls](../results/round18_ak3_cyclic_verify_controls.json).

## Literal planar-link screen through the cap-37 bridge contact

All **1,141,922** states discovered through the first cap-37 bridge contact give literal cyclic presentation complexes with a planar-link parity obstruction. They contain 1,073,610 $K_4$ links, 68,304 diamond links and eight $C_4$ links. The independent parity checker verifies **1,947,409** equations in the contradiction witnesses. These are the particular canonical complexes through the first contact, with the scope of the original planar-link method. [Exact cap-37 bridge](round-17-cyclic-peak-gap.md), [screen driver](../experiments/round17_ak3_link_screen.py), [receipt](../results/round18_ak3_cap37_link_screen.json).

## Reproduction

Set `native` to the output prefix from the Round 14 native expansion, `lower` to the manifest of independently verified cap-32 catalogue files, and `compacted` to the compacted boundary shard directory. The strict waypoint ledger is also directly replayable. [Native expansion command](round-14-independent-cyclic32.md#reproduction).

~~~sh
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_wide_verify.cpp -o "$work/independent"
printf '%s\n' "$compacted"/unique.*.bin > "$work/seed-manifest.txt"
"$work/independent" --flat-complete 33 14 "@$lower" "$native.outside.tsv" \
  "$work/c33-independent.json" 31 "$work/seed-manifest.txt"
c++ -std=c++17 -O3 -pthread experiments/round18_ak3_cyclic_primitives.cpp -o "$work/primitive-coordinates"
"$work/primitive-coordinates" "$native.outside.parents.bin" 10
c++ -std=c++17 -O3 experiments/round03_ak3_escape_path.cpp -o "$work/literal"
python3 -B experiments/round17_ak3_e22_ordinary.py \
  certificates/round18_ak3_c33_minimum_orbit.json \
  certificates/round18_ak3_c33_anchor_cap32.tsv certificates/round18_ak3_c33_anchor_cap29.tsv \
  "$work/literal" "$work/c33-minimum.json"
python3 -B experiments/elementary_verify.py "$work/c33-minimum.json"
~~~
