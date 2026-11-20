# Round 11 stable AC proof track

The two marked Wirtinger triples have strict rank-three routes on opposite sides of the repair. Stabilized AK(3) reaches the erroneous marking at cyclic peak 23, and the corrected marking reaches a basis at cyclic peak 25. The search compares known-trivial rank-three neighborhoods directly against the cap-22 sector without primitive rows and the exact one-product energy-23 frontier.

## Strict rank-three routes

Apply the shared eleven literal eliminations and eight Whitehead moves from [Round 10](round-10-stable-proof.md) to the wrong and corrected relation 13. Relabel the generators by `x,y,z → z,x,y` and place the resulting singleton pivot last. This marking makes the singleton the same generator as the one introduced by stabilizing AK(3).

| Route | Ordered endpoint on repair side | Strict moves | Raw peak | Cyclic peak |
| --- | --- | ---: | ---: | ---: |
| Stabilized AK(3) to wrong | `(XXYYxyyyxYY, ZYXXYxyXyxY, Z)` | 138 | 43 | 23 |
| Correct to basis | `(XXYYxyyyxYY, ZYXXYYxyXyyxY, Z)` | 110 | 49 | 25 |
| Geometric block control to basis | `(xxYYY, xxxYYYY, zxZXYzxxYYYZyxzX)` | 48 | 38 | 28 |

The common marking identifies the precise missing repair. The wrong route carries the previous exact rank-two AK(3) path into rank three and reverses the literal clearing of the added pivot. The correct route clears that pivot and uses the previous rank-two route to the basis. Both cyclic peaks equal the total cyclic length of the respective repair-side endpoint. The separate control embeds the verified geometric block of [Round 02](round-02-stable-proof.md), clears its conjugate from the third row, then normalizes the first two rows without using the third as a donor. The three ledgers replay with rank fixed at three. [Wrong ledger](../certificates/round11_stable_proof_wrong_prefix.json) · [Correct ledger](../certificates/round11_stable_proof_correct_suffix.json) · [Geometric block ledger](../certificates/round11_stable_proof_geometric_suffix.json)

## Reverse search and join test

The reverse seeds are the states occurring on either verified route to the basis. The two within energy 16–25 are the corrected endpoint and its first shorter cyclic product. Both remain eligible at cap 27. Cap 29 also admits the initial geometric-block control at energy 28. The forward target list comprises 173,389 signed cap-22 triples without primitive rows, 450,874 signed one-product energy-23 triples from the same sector, and the independently reachable wrong endpoint. [Exact cap-22 screen](round-09-stable-proof.md) · [Energy-23 generator](round-10-stable-proof.md)

An edge replaces one row by its product with a conjugate of another row, with either row sign permitted. The search tries every receiver and donor, including the isolated pivot. It enumerates all relative rotations and bridges that fit the energy cap. If the two axes in the free-group Cayley tree intersect, a cyclic rotation product suffices. If they are disjoint, the shortest bridge has length bounded by half the remaining energy after adding the donor length. The vertex key quotients cyclic rotation, row inversion, row permutation and the 48 signed permutations of the ambient basis. A common signed orbit would give a path after transporting one branch by a signed permutation and aligning its rows. The implementation uses a 21-letter per-row encoding and records candidates beyond its width; the expansion budget and chosen energy floor restrict the search. [Scanner](../experiments/round11_stable_proof_reverse.cpp) · [Ledger and seed compiler](../experiments/round11_stable_proof_reverse.py)

The positive control recovers the first cyclic product of the correct suffix in one edge. The start is `(XXYYxyXyyxYZY, XXYYxyyyxYY, Z)` and the shorter destination is `(XXYYxyXyyxYY, XXYYxyyyxYY, Z)` as cyclic representatives. The literal rank-three certificate changes the second marked row at move 14. [Correct ledger](../certificates/round11_stable_proof_correct_suffix.json)

The searches at floor 20 compare each reverse set against 623,738 eligible AK(3)-side target orbits. They also compare an independent search from the wrong repair endpoint against the full reached reverse set at each cap. Both comparisons give zero overlap at every cap.

| Cap | Expansions per side | Reverse orbits | Reverse without a singleton | Forward orbits | Forward without a singleton |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 25 | 12,000 | 223,071 | 1,057 | 103,351 | 0 |
| 27 | 12,000 | 218,380 | 597 | 204,731 | 41 |
| 29 | 9,000 | 845,627 | 36,722 | 117,226 | 42 |

At cap 25 the searches complete distance four on both sides and encounter no admissible product beyond the row-encoding width. Thus no path of at most eight cyclic products connects the wrong endpoint to either eligible reverse seed inside the energy interval 20–25. The cap-27 and cap-29 runs reach shorter complete distances and the reverse side omits some products beyond the encoding width. All three runs stop at the expansion budget. [Search receipts](../results/round11_stable_proof_reverse.json)

At cap 27 the wrong endpoint first reaches a tuple without a singleton in three cyclic products. The first two complete layers reached 136 and 5,399 signed orbits, each with a singleton. The third complete layer contains 14 without one. The explicit route changes rows 1, 2 and 3 in order, with donors 3, 1 and 2. Appended to the wrong prefix, it gives a 154-move strict path from stabilized AK(3) to `(XXYYxyyyxYZY, XYYXyxy, XYYXyxyz)` at raw peak 43 and cyclic peak 27. Two rows still have a literal (z)-chart and both project to the same rank-two pair. [Strict excursion](../certificates/round11_stable_proof_source_excursion.json) · [Orbit route](../results/round11_stable_proof_source_excursion.tsv)

The geometry screen on the entire 450,874-triple one-product frontier is complete. Its 92,361 signed chart projections minimize to 66,951 signed rank-two orbits, each of which has a verified planar-link parity obstruction. The calculation classifies these projected pairs, while the remaining strict rank-three searches can continue changing chart. [Geometry receipt](../results/round11_stable_proof_projected_geometry.json) · [Screen and reproduction](round-10-stable-proof.md)

## Reproduction

Use `chartless22` and `frontier23` for the precise source files from [Round 10](round-10-stable-proof.md). Use `work` for a scratch directory. Each search writes its reached orbit set and a join route, when one is found.

```sh
python3 -B experiments/round11_stable_proof_reverse.py "$work"
c++ -std=c++17 -O3 -pthread experiments/round11_stable_proof_reverse.cpp -o "$work/reverse"
cat "$chartless22" "$frontier23" "$work/wrong.tsv" > "$work/forward-targets.tsv"
"$work/reverse" 16 25 1 "$work/correct.tsv" "$work/control-target.tsv" "$work/control"
for spec in "25 12000" "27 12000" "29 9000"; do
  read -r cap budget <<EOF
$spec
EOF
  "$work/reverse" 20 "$cap" "$budget" "$work/reverse-roots.tsv" \
    "$work/forward-targets.tsv" "$work/reverse$cap"
  "$work/reverse" 20 "$cap" "$budget" "$work/wrong.tsv" \
    "$work/reverse$cap.tsv" "$work/forward$cap"
done
python3 -B experiments/round11_stable_proof_reverse.py "$work" \
  --lift-source-route results/round11_stable_proof_source_excursion.tsv
python3 -B experiments/round10_stable_proof_frontier_geometry.py "$frontier23" \
  --basis-index-tsv "$work/projected-minima28.tsv"
```
