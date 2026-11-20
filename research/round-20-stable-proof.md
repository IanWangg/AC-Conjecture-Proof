# Exact peak for chart recovery after the length-six donor release

2026-11-19. After leaving the signed cyclic orbit of `xxyXYY`, the 528 donor-free chartless states from Round 19 first admit a rank-three path to a primitive row at cyclic peak **38** while that donor orbit remains absent. The witness reaches an isolated auxiliary singleton and permits strict destabilization. The complete AK(3) ledger gives the literal energy-22 pair `(XXXXyXyyyXy, XXXXyxyXyXy)` in **952 instructions**, maximum rank **3**, cyclic peak **38**, and raw peak **39**. [Strict stable ledger](../certificates/round20_stable_proof_cap38_release.jsonl), [native and independent receipts](../results/round20_stable_proof_release.json).

## Exact donor-free closure

Take all 528 chartless states of the exact cap-33 Round 19 component that contain no row in the signed cyclic orbit of the length-six donor. Explore all cyclic products of the three rows and discard a successor if it has any row in that donor orbit. Signed ambient generator permutations, cyclic rotations, inversions and relator order are factored out. A primitive detection checks the actual chart for each row. The mode that allows charted states to continue visits none through cap 37. [Root catalogue](../certificates/round20_stable_proof_released_roots.tsv), [root provenance](round-19-stable-proof.md#length-six-donor-release-at-peak-33), [native implementation](../experiments/round20_stable_proof_release.cpp).

| Cyclic cap | Complete retained component | States with a primitive row |
| --- | ---: | ---: |
| 33, 34 and 35 | 528 at each | 0 |
| 36 | 1,584 | 0 |
| 37 | 1,728 | 0 |

Both a complete menu scan in the native graph and an independent literal stack reduction check the cap-37 component. The latter regenerates all 1,728 orbits from the 528 roots, checks that the entire root set comes from Round 19, and verifies all **5,634,816** signed-rotation products. Every stored state has no primitive coordinate. Each permitted successor fits the per-word width 21. Each positive shortest bridge would have total energy above 37. These checks make the cap-37 exclusion exact for paths in this donor-free sector from any of the 528 roots. [Independent replay](../experiments/round20_stable_proof_audit.py).

## Isolated chart at cap 38

From the literal endpoint of the 46-instruction donor-release path, two cyclic products give an isolated auxiliary singleton. The marked compiler keeps the generator names fixed. After the donor-release prefix it uses 26 strict instructions including the two products and the final destabilization. It checks the absence of the length-six donor orbit after each elementary step of the continuation. [Three cyclic states](../certificates/round20_stable_proof_cap38_route.tsv), [fixed-marking compiler](../experiments/round20_stable_proof_replay.py), [Round 19 prefix](../certificates/round19_stable_proof_e17_donor_release.json).

The projected pair is also linked to the first energy-17 marking by a **29-instruction ordinary path** containing one product at cyclic and raw peak **22**. Its exact unbounded single-product primitive test is negative. Therefore the sharp peak 38 concerns the rank-three clearing under the donor-orbit restriction. [Ordinary comparison ledger](../certificates/round20_stable_proof_ordinary_comparison.json), [single-product receipt](../results/round20_stable_proof_release.json).

Allowing the short donor to return in the chartless search from the literal released root, four 50,000-expansion probes at caps 34, 36, 37 and 38 each yield 2,247 signed rank-two projections. The projection sets all lie in the ordinary cap-23 component of the first energy-17 pair, which contains 2,277 orbits. They contain no primitive coordinate and no exact archive match. These probes stop at their budgets. [Projection receipts](../results/round20_stable_proof_release.json).

## Reproduction

Set `reverse` to the verified archive TSV from Round 04, and `prior` to the `exact33-m1` output prefix regenerated in Round 19. [Archive replay](round-04-ak3.md#reproduction), [earlier chartless search](round-19-stable-proof.md#reproduction).

~~~sh
mkdir -p "$work"
roots=certificates/round20_stable_proof_released_roots.tsv
c++ -std=c++17 -O3 experiments/round20_stable_proof_release.cpp -o "$work/release"
for cap in 33 34 35 36 37
do
  "$work/release" "$cap" 350000 "$roots" "$reverse" "$work/all$cap"
done
python3 -B experiments/round20_stable_proof_audit.py "$roots" "$work/all37" "$prior"
"$work/release" 38 220000 "$roots" "$reverse" "$work/first38" --first-chart
cmp "$work/first38.route.tsv" certificates/round20_stable_proof_cap38_route.tsv
python3 -B experiments/round20_stable_proof_replay.py \
  certificates/round18_ak3_c33_minimum_ordinary.json \
  certificates/round19_stable_proof_e17_donor_release.json \
  "$work/first38.route.tsv" "$work/stable38.jsonl"
c++ -std=c++17 -O3 experiments/round06_stable_proof_strict_verify.cpp -o "$work/check"
"$work/check" "$work/stable38.jsonl"
python3 -B experiments/elementary_verify.py certificates/round20_stable_proof_ordinary_comparison.json
~~~
