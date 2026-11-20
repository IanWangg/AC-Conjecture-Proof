# Round 10 stable AC proof track

The exact cap-22 singleton return set now has an independent byte-for-byte verification. At cap 23, all one-product departures from the cap-22 triples without a primitive row yield no primitive projection, sphere or singleton return. The older Wirtinger approach to AK(3) now has a strict rank-three source certificate and an explicit finite obstruction to correcting its erroneous relator with the other rows held fixed. Its reduced repair problem yields one rank-two pair on the AK(3) component and one with a short ordinary trivialization.

## Independent singleton returns through cap 22

The [Round 08 generator](round-08-stable-proof.md) recorded 432 singleton return projections from 246,052,265 signed rank-three excursion orbits. A separate scanner computes only the returns from the raw catalogue. If an ordinary cyclic product turns one row into a singleton, a signed sum of the two input exponent vectors equals a signed coordinate vector. Also, both input lengths are at least two. A positive shortest bridge would make the product length the sum of those lengths plus twice the bridge length, so only products of signed cyclic rotations are needed. The scanner tests every compatible unordered pair using ordinary stack reduction. The cyclic products \(uv\) and \(vu\) are conjugate, so for each detected singleton it clears its letter with each possible retained donor and expands the signed rank-two markings.

| Cyclic cap | Source orbits | Exponent-compatible pair occurrences | Rotation tests | Signed cyclic reentry pairs |
| --- | ---: | ---: | ---: | ---: |
| 20 | 14 | 20 | 58 | 20 |
| 21 | 264 | 339 | 2,823 | 56 |
| 22 | 246,052,265 | 132,882,153 | 2,970,917,363 | 432 |

All three reentry files match the original generator byte for byte. The cap-22 file has SHA-256 `785ee4da9044feb892ea90d4b3090faac441e843f03cbfecd1d9482aae829567`. All returns are within the exact ordinary cap-22 invariant. The separate verifier has now checked all 246,052,265 non-singleton state orbits for closure and the presence of all seed orbits. The complete cap-22 enclosure independently gives cyclic peak at least 23 for any stable trivialization of AK(3) at rank at most three. [Independent return checker](../experiments/round10_stable_proof_return_audit.cpp) · [Audit and controls](../results/round10_stable_proof_cap22_return_audit.json) · [Completed closure](round-10-independent-closures.md) · [Literal return file](../results/round08_stable_proof_cap22_returns.tsv)

## One cap-23 product beyond the cap-22 chartless sector

Start with the 173,389 exact cap-22 signed excursion triples with no primitive row. Enumerate every ordinary cyclic product of peak at most 23 and retain the destinations of energy exactly 23. The resulting layer contains 450,874 signed triples. Its 213,075,576 candidates all have empty geodesic bridge. The generator admits 8,034,108 product occurrences across energies through 23. Every retained destination records a predecessor orbit. [Generator](../experiments/round10_stable_proof_chartless_frontier.cpp) · [Frontier and all screening receipts](../results/round10_stable_proof_frontier23.json)

- The native scanner finds 153,614 primitive rows across the layer and zero primitive projected coordinates. It also exports the 297,260 triples without any primitive row.
- Abstract nonplanarity excludes 183,700 of the jointly Whitehead-minimized chartless triples. The other 113,560 give 86,280 signed minima, with no sphere in 9,192,946 exact paired rotation tests.
- The independent singleton scan finds no literal return in a further product from this layer. It checks 1,836,408 rotation products after the exponent-vector gate.
- All literal and intrinsic charts give 92,361 signed rank-two pairs. The exact cap-30 ordinary component contains 24,739. The reverse archive comprises 22,426 signed classes of known trivial pairs, and contains none of the projections.
- Joint Whitehead descent yields 129,792 distinct signed marked pairs of cyclic length at most 28 from the projected pairs. The exact all-tail basis index compares these against 23,902 verified reverse archive entries. All 494,634 basis-pair lookups give no join. This comparison allows independent conjugations of both coordinates on each side. [Exact join receipt](../results/round10_stable_proof_frontier_reverse_join.json), [basis-index completeness](round-04-ak3.md).

These are exact tests of the one-product layer attached to the specified cap-22 chartless sector. The overall cap-23 rank-three component can contain additional states.

## The published Wirtinger connection

The 2002 Wirtinger construction drops relation 12 from a 14-generator presentation, with an erroneous conjugator \(x_5\) in relation 13 where the unknot diagram requires \(x_4\). The incorrect diagram leaves a rank-three family after eleven eliminations. Shehper et al. corrected the provenance and retained an explicit ordinary AC path connecting one member's rank-two projection to AK(3). Lisitsa's final journal article likewise leaves stable AK(3) open. [Original construction, §3](https://web.stevens.edu/algebraic/alexeim/Publications/AC%20Conjecture/ac1.pdf) · [Corrected derivation, Appendices B and F](https://arxiv.org/pdf/2408.15332) · [Lisitsa's final article](https://doi.org/10.1016/j.jaca.2025.100041)

The published 53 products and conjugations, expanded into 67 strict moves by restoring inverted donors, take `(XYxYXyxYYxyXy, YXyyXYxyxYYx)` to the exact AK(3) marking with raw peak 25. The source is the literal \(z\)-projection of the marked rank-three tuple `(XzYXyxzXYxyZ, YxYXyxZXYxyxzX, Xyz)`, up to a based conjugation of the second row. The once-stabilized marking compiler from Round 09 gives an actual 295-move ordinary rank-three path from stabilized AK(3) to that exact tuple with raw peak 54 and cyclic peak 30. A separate symbolic reconstruction of the original elimination order checks the link to the erroneous Wirtinger presentation with \(x=x_5\), \(y=x_7\), \(z=x_{12}\) and added relator \(x^{-1}yz\). [Published path replay](../certificates/round10_stable_proof_wirtinger_rank2.json) · [Strict rank-three path](../certificates/round10_stable_proof_wirtinger_rank3.json) · [Eliminations and replay](../results/round10_stable_proof_wirtinger.json)

## The frozen repair and its ordinary endpoints

Hold the 13 common relators fixed at rank 14, including \(x_5^{-1}x_7x_{12}\), and ask whether the erroneous and corrected versions of relation 13 are conjugate up to inversion in their quotient. Eleven checked literal eliminations of the common rows leave two fixed relators on \(x=x_1\), \(y=x_{10}\), \(z=x_{12}\). An explicit permutation marking of their quotient sends the erroneous relation 13 to a 5-cycle and the corrected one to a 3-cycle. The two images cannot be conjugate even after inversion. This excludes correcting just relation 13 by arbitrary conjugations, inversions, and products with the fixed donors. [Elimination and \(S_5\) witness](../results/round10_stable_proof_wirtinger.json) · [Witness generator](../experiments/round10_stable_proof_wirtinger.py)

An eight-step joint Whitehead descent isolates one of the two fixed rows. Taking its rank-two quotient gives the two marked pairs below.

| Source | Projected pair | Independently replayed ordinary route |
| --- | --- | --- |
| Erroneous relator | `(XXYYxyyyxYY, XXYxyXyxYY)` | 105 moves from AK(3), cyclic peak 21 |
| Corrected relator | `(XXYYxyXyyxYY, XXYYxyyyxYY)` | 73 moves to `(x,y)`, cyclic peak 23 |

For the corrected pair, one marked row differs from the other by one insertion of \(x^{-1}\). Multiplying by the inverse of the shorter row gives a conjugate of \(x^{-1}\), after which ordinary donor products clear \(x\) from the second row. The wrong pair's ordinary connection goes through nine cyclic product edges. Four local ordinary searches from the wrong pair missed the corrected pair and a primitive coordinate. Each stopped at the 400,000-expansion limit, at caps 25, 29, 33 and 37. [Wrong pair ordinary certificate](../certificates/round10_stable_proof_wirtinger_wrong.json) · [Correct pair basis certificate](../certificates/round10_stable_proof_wirtinger_correct.json) · [Bounded join receipts](../results/round10_stable_proof_wirtinger_join_checks.json)

The two historical AK(3) pairs and AK(3) itself also have zero one-product primitive hits after applying the 80 length-five substitutions with three occurrences and self-exponent \(\pm1\) on one generator, restricted to nonprimitive image words. These substitutions have stable ancestry by Round 09. A rank-two primitive's cyclic length is the \(\ell^1\)-norm of its exponent vector, so a primitive result in one product cannot require a positive shortest bridge. The scan checks every signed cyclic rotation product of the resulting 48 distinct ordered image pairs per source. [Substitution product scanner](../experiments/round10_stable_proof_wirtinger_substitutions.py) · [Results](../results/round10_stable_proof_wirtinger_substitutions.json)

A second repair test freezes the first two relators of the marked rank-three source and changes only the added relator \(x^{-1}yz\). Their abelian quotient sends each generator to the same integer generator, so a replacement must have absolute total exponent one. An \(S_5\) marking of the frozen quotient sends the added relator to a 5-cycle and each generator to a 3-cycle. Among 1,317 distinct cyclic words of length at most seven with unit total exponent and a literal chart, 605 pass this cycle-type test. Four have a rank-two quotient with a primitive coordinate. One \(S_6\) marking sends the added relator to two disjoint 2-cycles and sends each of the four alternatives to a 5-cycle. A five-step Whitehead descent sends the second frozen relator to \(y^{-1}\), presenting the frozen quotient as an explicit rank-two one-relator group. Homomorphisms to \(\mathrm{SL}_2(\mathbb F_5)\) and \(\mathrm{SL}_2(\mathbb F_{11})\) separate the trace of the added relator from each of these four targets. The traces are invariant under conjugation and inversion. Thus none of the four gives the required frozen change. [Full short-word census and matrix witnesses](../results/round10_stable_proof_wirtinger.json)

## Reproduction

Use the chartless cap-22 export from [Round 09](round-09-stable-proof.md), the verified ordinary cap-30 catalogue and the reverse archive from [Round 04](round-04-ak3.md). The return checker also accepts the corresponding complete cap-20 and cap-21 catalogues.

~~~sh
c++ -std=c++17 -O3 experiments/round10_stable_proof_return_audit.cpp -o "$work/return-audit"
"$work/return-audit" "$states22" "$work/c22.returns.tsv"
cmp "$work/c22.returns.tsv" results/round08_stable_proof_cap22_returns.tsv
c++ -std=c++17 -O3 -pthread experiments/round10_stable_proof_chartless_frontier.cpp -o "$work/frontier"
"$work/frontier" "$chartless22" "$work/frontier23" 6
"$work/primitive-catalogue" "$work/frontier23.triples.tsv" 23
"$work/primitive-catalogue" "$work/frontier23.triples.tsv" 23 "$work/chartless23.tsv"
"$work/return-audit" "$work/frontier23.triples.tsv" "$work/frontier23.returns.tsv"
python3 -B experiments/round09_stable_proof_chartless_geometry.py "$work/chartless23.tsv"
python3 -B experiments/round10_stable_proof_frontier_projections.py \
  "$work/frontier23.triples.tsv" "$work/frontier23.parents.tsv" "$c30" "$reverse"
python3 -B experiments/round10_stable_proof_frontier_geometry.py "$work/frontier23.triples.tsv" \
  --basis-index-tsv "$work/frontier23.minima28.tsv"
c++ -std=c++17 -O3 experiments/round04_ak3_basis_index.cpp -o "$work/basis-index"
"$work/basis-index" "$work/frontier23.minima28.tsv" "$reverse" "$work/frontier23.reverse-join.json"
python3 -B experiments/round10_stable_proof_wirtinger.py \
  "$work/published.json" "$work/rank3.json" results/round10_stable_proof_wirtinger_wrong_route.json \
  "$work/wrong.json" "$work/correct.json"
python3 -B experiments/round10_stable_proof_wirtinger_substitutions.py
~~~
