# The external projection at cyclic peak 33

2026-11-19. A strict stable path from AK(3) to the exact ordered energy-24 pair `(XXYxYXXYxxy, XXYXYxxyXyxxy)` uses **1,346 elementary instructions**, maximum rank **3**, cyclic peak **33**, and raw peak **41**. The independent stack-reduction verifier confirms the entire ledger, including stabilization and destabilization. Round 15 reached the same pair at cyclic peak 35. [Strict ledger](../certificates/round16_stable_proof_cap33_external.jsonl), [replay receipt](../results/round16_stable_proof_pivot.json), [Round 15 path](round-15-stable-proof.md).

## Direct clearing of the cap-32 chart

Replay the Round 15 literal chart prefix, including the stabilization. Rotate and orient its first row to `zXyxxyy`. Use it as a donor to substitute for each occurrence of `z` and `Z` in the other rows. The free-word move compiler restores the pivot after each multiplication. In **1,031** strict instructions from AK(3) the result is

~~~text
zXyxxyy  XXYxYXXYxxy  XXYXYxxyXyxxy
~~~

This reaches both exact donors together at cyclic peak **32** and raw peak **41**. The pivot still carries a six-letter tail. [Round 15 chart prefix](../certificates/round15_stable_proof_cap32_literal.json), [strict compiler](../experiments/round16_stable_proof_pivot.py).

## Search with one auxiliary occurrence

Start from the cleared chart and search toward the exact donors with an isolated `z` in the first slot. Keep the generator marking and row order. Canonicalize each word under inversion and cyclic rotation. Allow either ordinary donor to change by multiplication with the other one. Also allow a product changing the pivot using either ordinary donor. Thus the cyclic tuple keeps exactly one auxiliary occurrence throughout. The search admits row widths up to 21, energies at least 12 and relative bridges of length at most three subject to the energy cap. It expands the smaller current frontier at each layer.

At cap 33 the run joins after **43,559** expansions and gives a **26-product** tail. Both ordinary donors temporarily change. For example, the second row becomes `XXYYYxYXY` and the third becomes `XXYYXYxYY`. The pivot first reaches `Z` with different donors, then two ordinary products restore their original cyclic classes. The compiler expands each product and normalizes the final literal words before deleting `z`. At cap 32 this traversal ends with an empty frontier after **47,249** expansions and gives no join. That run concerns the stated search restrictions. [Marked tail](../certificates/round16_stable_proof_cap33_tail.tsv), [search implementation](../experiments/round16_stable_proof_pivot.cpp).

A separate search also fills the last missing cap-34 cut in the original Round 14 path. The marked tail from original rank-three steps 2,403 to 2,743 uses 16 products. The full splice gives **1,773** strict moves with maximum rank three, cyclic peak 34 and raw peak 45. [Full detour input](../certificates/round16_stable_proof_cap34_detours.json), [independent strict replay input](../certificates/round16_stable_proof_cap34_external.jsonl).

## A shorter external projection

Destabilizing at the first isolated pivot gives the energy-21 pair `(XXYYYxYXY, XXYYxYXXyxxY)` in **1,306** strict moves with maximum rank three, cyclic peak 33 and raw peak 41. The historical label E22 counts the isolated auxiliary letter in the preceding rank-three triple. A 40-move strict ordinary path from this pair to the energy-24 pair has raw peak 29, so the shorter pair is also absent from ordinary cap 32. The arbitrary-tail single-product test finds no primitive exposure from it. [Stable ledger](../certificates/round16_stable_proof_cap33_e22.jsonl), [ordinary comparison path](../certificates/round16_stable_proof_e22_to_e24.json), [primitive-product check](../results/round16_stable_proof_pivot.json).

An independent reverse closure at ordinary cap 33 contains both E22 and E24 and excludes AK(3). Together with the stable ledgers, this establishes a strict cyclic peak gap at both exact markings. [Ordinary reverse closure and comparison](round-16-cyclic-peak-gap.md).

## Reproduction

~~~sh
mkdir -p "$work"
printf 'zXyxxyy\tXXYxYXXYxxy\tXXYXYxxyXyxxy\n' > "$work/start.tsv"
printf 'Z\tXXYxYXXYxxy\tXXYXYxxyXyxxy\n' > "$work/target.tsv"
c++ -std=c++17 -O3 experiments/round16_stable_proof_pivot.cpp -o "$work/pivot"
"$work/pivot" 12 32 700000 "$work/start.tsv" "$work/target.tsv" "$work/cap32" 1
"$work/pivot" 12 33 700000 "$work/start.tsv" "$work/target.tsv" "$work/cap33" 1
cmp "$work/cap33.route.tsv" certificates/round16_stable_proof_cap33_tail.tsv

python3 -B experiments/round16_stable_proof_pivot.py \
  certificates/round15_stable_proof_cap32_literal.json "$work/external33.jsonl" \
  --route "$work/cap33.route.tsv"
python3 -B experiments/round16_stable_proof_pivot.py \
  certificates/round15_stable_proof_cap32_literal.json "$work/external-e22.jsonl" \
  --route "$work/cap33.route.tsv" --stop-after 24
python3 -B experiments/round15_stable_proof_splice.py \
  certificates/round14_stable_proof_external_local.jsonl \
  certificates/round16_stable_proof_cap34_detours.json "$work/external34.jsonl"
c++ -std=c++17 -O3 experiments/round06_stable_proof_strict_verify.cpp -o "$work/check"
"$work/check" "$work/external33.jsonl"
"$work/check" "$work/external-e22.jsonl"
"$work/check" "$work/external34.jsonl"
python3 -B experiments/elementary_verify.py certificates/round16_stable_proof_e22_to_e24.json
printf 'XXYYYxYXY\tXXYYxYXXyxxY\n' > "$work/e22.tsv"
c++ -std=c++17 -O3 -pthread experiments/round12_ak3_primitive_step.cpp -o "$work/primitive-step"
"$work/primitive-step" "$work/e22.tsv" 1
~~~
