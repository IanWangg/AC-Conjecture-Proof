# Round 06 · Bounded stable excursions through all marked singleton charts

2026-11-19. A compact search checks the bounded rank-three excursions of AK(3) between singleton charts of any marked generator. A second computation tests primitive projections in a partial cap-23 catalogue. These procedures constrain bounded paths and look for shorter stably reachable pairs.

## All marked singleton charts

Use cyclic words up to individual inversion and cyclic rotation. A singleton is a row of cyclic length one. Its letter, say $z$, can be cleared from every other row using conjugates of that row. To remove one $z^{\pm1}$ from a reduced word $u z^{\pm1} v$, multiply that row on the right by $v^{-1}z^{\mp1}v$. The cyclic length of the recipient cannot increase. Inversions and conjugations of the singleton donor do not change cyclic length. After clearing, conventional isolated destabilization deletes that row and its generator. Thus every bounded singleton state can be projected to a smaller marked tuple without leaving its cyclic cap. [Round-three excursion argument](round-03-stable-proof.md).

Let $C$ be the complete ordinary cyclic cap-22 AK(3) component. All signed ambient basis images of the initial AK(3) pair are in $C$. Since signed basis maps preserve the ordinary cyclic graph, the whole component is invariant under those maps. Every ordinary rank-two phase at peak at most 22 preserves membership in $C$. If a rank-three singleton state projects to $C$, the same is true after an edge retaining that singleton, by projecting the ordinary move. A product that switches directly to a different singleton cannot leave a singleton phase from such a state. If it targets the existing singleton, then the unchanged donor would project to the new singleton after killing the old one. If it uses another recipient and leaves the old singleton, its new singleton also projects to a singleton. Both cases contradict the absence of a primitive coordinate in $C$. This also excludes adding a second singleton of the same letter, since the exponent matrix is unimodular. [Exact cap-22 component and primitive exclusion](research-n-cyclic-search.md).

For a product leaving the singleton phase, let $r,s$ be the rank-two projected donor and other row. The output cyclic energy is at least $2|r|+|s|+1$. Both the donor and the changed singleton project to $r$. Either the donor or the new row contributes at least one extra letter of the singleton generator. Enumerate every compatible lift up to the available slack and every bounded product, as in round three. There are 476 ordered boundary pairs meeting the bound at cap 22, and this weighted boundary is identical in $C_{21}$ and $C_{22}$. The resulting 48,096 seeds coincide with the preceding round's independent seed file. The verifier checks the rank-two hashes and all signed images of AK(3). [First-exit generator](../experiments/round06_stable_proof_singleton_report.py), [prior seed provenance](round-04-stable-proof.md).

For exclusion it suffices to start every seed and prove that the catalogue is closed until a singleton returns. Every seed is also attainable by a bounded stable path when ordinary rank-two phases are allowed. Reach its projected pair in $C$, adjoin $z$, reverse the clearing of $z$ from its enumerated lifted rows, then take the seed's defining product. The original lifted lengths bound that reverse clearing sequence. This allows an exact route to a recorded candidate with a chosen seed, without assuming its precursor is present in the fixed rank-three component of the initial tuple.

## Compact scan and controls

The scanner takes the quotient by all 48 signed permutations of the ambient rank-three basis. It expands every reduced bridge allowed by the Cayley-tree length bound and all signed cyclic rotations. From a product yielding a singleton of any letter, it forms the cleared rank-two projection in the surviving marking. The return set expands all signed rank-two images. The quotient is sufficient for closure because the edge rule commutes with signed basis changes and the eventual rank-two invariant is signed-invariant. Product reduction uses cancellation at the two cyclic seams for the empty bridge. The independent checker instead uses exact stack reduction, Booth rotation, a separate signed relabeling menu and a distinct return-projection routine. It tests every generated orbit for neighbor coverage and verifies that all seed orbits are present. [Cyclic-product completeness proof](research-n-cyclic-search.md), [generator](../experiments/round06_stable_proof_all_singleton.cpp), [independent checker](../experiments/round06_stable_proof_singleton_verify.cpp).

At caps 20 and 21 the new scanner and the verifier recover the previously checked 20 and 56 reentry pairs, all within $C$. The full signed orbit counts are 14 and 264. Cap 22 adds a much larger non-singleton sector. The cap-22 closure and its independent reentry audit are in progress. The completed controls give no stronger rank-three bound by themselves. [Control results](../results/round06_stable_proof_singleton_controls.json).

If the cap-22 excursion set closes into $C$, or a larger verified ordinary component with the same weighted boundary, no stable trivialization at ranks at most three can have peak 22. Every rank-three phase starts in a singleton chart, and each return then preserves the rank-two invariant. A first drop to rank one would require a singleton in rank two, which this invariant excludes. This argument would cover repeated stabilization and destabilization and deletion of old marked generators.

## Chart-free geometry in the cap-23 sample

The previously generated 4,000,000-state literal prefix at cap 23 has 3,270 states with no literal chart of any letter. Whitehead descent leaves 2,275 with no primitive row in any marking. They give 450 inequivalent jointly minimized signed diagrams. The exact paired rotation checker exhausts 165,488 orders without a spherical realization. Each tuple is disk-busting by the rank-three unimodularity argument from round five, so the minimal-diagram criterion applies. [Input provenance](round-04-stable-proof.md), [paired rotation method](round-05-stable-proof.md), [geometry receipt](../results/round06_stable_proof_cap23_geometry.json).

The 2,275 chart-free states supply 4,204 distinct two-row blocks. The cyclic-cover Fox minor excludes an infinite cyclic quotient for 4,180. For 12 more, a single signed product with the recorded relative bridge exposes a literal pivot. The other row projects to a nonprimitive rank-two relator. If its quotient were infinite cyclic, the normal-closure theorem would force that relator to be a primitive conjugacy class. The final 12 blocks are supported in $F(x,y)$ and form two signed orbits in the verified ordinary cap-29 component. Their quotient in rank three really is infinite cyclic. Both rank-two Whitehead minima have checked planar-link parity obstructions. Geometry of such a block in rank three descends to its supporting free factor, so these two nongeometric blocks also fail the joint geometry and free-quotient test. This exhausts the two-row test on the chart-free subset of the prefix. [Fox criterion](round-04-stable-proof.md), [free-factor geometry](round-03-stable-proof.md), [cap-29 verification](round-06-cyclic29.md), [block receipts with explicit exposures](../results/round06_stable_proof_cap23_blocks.json).

## An energy-23 projection outside the ordinary cap-29 component

The same sample contains 15,828 literal triples without a fixed $z$ chart and no $z$-free row of length at most two. Inspecting the 17,112 literal charts and 2,322 intrinsic charts of those triples gives 725 signed rank-two projection classes. The verified cap-29 component contains 151 of those classes, and the known-trivial archive through energy 56 contains none. All 255 distinct rank-two Whitehead minima have independently replayed planar-link parity obstructions. No projected tuple has a primitive row. The exact basis index compares the 744 signed minimized pairs through energy 28 with 23,902 known-trivial archive pairs and excludes a subgroup join after arbitrary independent conjugations on either side. [Projection receipts](../results/round06_stable_proof_cap23_charts.json), [indexed join receipt](../results/round06_stable_proof_cap23_projection_joins.json), [weighted basis index](round-04-ak3.md).

The least cyclic-energy projection in this sample outside the cap-29 component is

~~~text
XXXYxyxyXYY   XYXYYXyXYYXy
~~~

Its cyclic energy is 23. The exact bidirectional prefix search finds an 11-product route at rank two to `(XXXYYxy, XXyxYY)`. After adjoining $z$, insert $z^{-1}$ immediately before the final `xy` in the first row using conjugates of the singleton. The ensuing cap-23 cyclic products reach `(XzyZYYZxy, XXzYZ, XYXzYZxyy)`. The compiled ordinary rank-three ledger from the stabilized AK(3) pair replays in 148 moves with raw peak 28 and cyclic peak 23. Its first loss of the fixed $z$ pivot occurs at move 140. [Strict rank-three ledger](../certificates/round06_stable_proof_cap23_escape.json).

The row `XzyZYYZxy` becomes `Z` through five checked Whitehead automorphisms. The 13 elementary generator replacements making up those automorphisms use the rank-four defining exchange construction. Clear the final singleton from the other two rows and delete it. This proves stable reachability of the displayed pair from AK(3) with maximum rank at most four. The exact compact cap-29 membership test treats all signed ambient versions together and finds the pair absent. Every ordinary connection to this pair therefore requires cyclic peak at least 30. Its joint Whitehead minimum is nongeometric by the parity receipt, so this construction ends at a new waypoint on the stable component. [Transport and membership](../results/round06_stable_proof_cap23_escape.json), [rank-four exchange proof](round-05-stable-chart-transport.md).

The defining exchanges also expand into **21,528,218 strict stable moves**, independently replayed in native code. There are 14 singleton insertions and 14 isolated deletions, including the initial and final rank changes. The full ledger reaches rank four, raw length 1,369, and cyclic length 405. The 23 cyclic peak concerns the 148-move rank-three prefix. No ambient automorphism is treated as a legal move in the full ledger. The compiler starts with explicit normal-closure products for $x,y,z$ and transports them through the prefix and each checked generator replacement. Each exchange first inserts the new literal singleton, uses those identities to produce its defining relation, substitutes the old generator by donor products, then clears and deletes the old singleton. The replay checks each conjugation, multiplication, inversion and isolated rank change. The ledger is regenerated from the compact certificate and the recorded digest. [Full strict report](../results/round06_stable_proof_cap23_strict.json), [independent replay](../results/round06_stable_proof_cap23_strict_verify.json).

## Reproduction

Recover the exact cap-21 and cap-22 TSVs using the [round-four provenance](round-04-stable-proof.md). Run the following commands from the repository root. Cap 22 is the full run. The two smaller controls can be reproduced independently by omitting 22 from the loop and adding `--controls-only` to the summary call.

~~~sh
work=/tmp/ac-r06-stable
prior=/tmp/ac-r04-stable
mkdir -p "$work"
python3 -B experiments/round06_stable_proof_singleton_report.py prepare \
  "$prior/c21.tsv" "$prior/c22.tsv" "$work" > "$work/seeds.json"
c++ -std=c++17 -O3 -pthread experiments/round06_stable_proof_all_singleton.cpp -o "$work/all_singleton"
c++ -std=c++17 -O3 -pthread experiments/round06_stable_proof_singleton_verify.cpp -o "$work/audit"
for cap in 20 21 22; do
  "$work/all_singleton" "$cap" 6 "$work/seeds$cap.tsv" "$prior/c22.tsv" "$work/full$cap" \
    > "$work/full$cap.json"
  "$work/audit" "$cap" 6 "$work/seeds$cap.tsv" "$work/full$cap.states.tsv" "$work/full$cap.returns.tsv" \
    > "$work/audit$cap.json"
done
python3 -B experiments/round06_stable_proof_singleton_report.py summarize \
  "$prior/c21.tsv" "$prior/c22.tsv" "$work"
~~~

Use the literal cap-23 prefix from round four and the compact cap-29 catalogue from its exact computation for the following additional checks.

~~~sh
python3 -B experiments/round05_stable_proof_geometry.py --scan "$prior/exact23.states.tsv" \
  | diff - results/round06_stable_proof_cap23_geometry.json
python3 -B experiments/round06_stable_proof_cap23_blocks.py "$prior/exact23.states.tsv" \
  /tmp/ac-r05-ak3/c29.orbit.tsv | diff - results/round06_stable_proof_cap23_blocks.json
python3 -B experiments/round06_stable_proof_cap23_charts.py "$prior/exact23.states.tsv" \
  /tmp/ac-r05-ak3/c29.orbit.tsv /tmp/ac-r04-archive/reverse.tsv \
  --basis-index-tsv "$work/cap23_minima28.tsv" \
  | diff - results/round06_stable_proof_cap23_charts.json
c++ -std=c++17 -O3 experiments/round04_ak3_basis_index.cpp -o "$work/basis-index"
"$work/basis-index" "$work/cap23_minima28.tsv" /tmp/ac-r04-archive/reverse.tsv "$work/projection_joins.json"
diff "$work/projection_joins.json" results/round06_stable_proof_cap23_projection_joins.json
c++ -std=c++17 -O3 experiments/round05_stable_proof_route.cpp -o "$work/chart-route"
c++ -std=c++17 -O3 experiments/round03_ak3_escape_path.cpp -o "$work/pair-route"
"$work/chart-route" 23 "$prior/seeds23.tsv" "$work/escape23.tsv" 2000000 XXzYZ XYXzYZxyy XzyZYYZxy
printf '%s\t%s\n' XXXYYxy XXyxYY > "$work/escape23_projected.tsv"
"$work/pair-route" 22 "$work/escape23_projected.tsv" "$work/escape23_pair_route.json"
python3 -B experiments/round06_stable_proof_escape23.py "$work/escape23_pair_route.json" \
  "$work/escape23.tsv" /tmp/ac-r05-ak3/c29.orbit.tsv "$work/escape23_ledger.json" \
  | diff - results/round06_stable_proof_cap23_escape.json
diff "$work/escape23_ledger.json" certificates/round06_stable_proof_cap23_escape.json
python3 -B experiments/round06_stable_proof_strict_escape.py --write-ledger "$work/strict_escape23.jsonl" \
  | diff - results/round06_stable_proof_cap23_strict.json
c++ -std=c++17 -O3 experiments/round06_stable_proof_strict_verify.cpp -o "$work/strict_verify"
"$work/strict_verify" "$work/strict_escape23.jsonl" \
  | diff - results/round06_stable_proof_cap23_strict_verify.json
~~~
