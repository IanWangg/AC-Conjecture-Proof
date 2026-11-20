# Round 15 stable AC proof track

The strict stable entry from AK(3) to the ordered energy-24 pair `(XXYxYXXYxxy, XXYXYxxyXyxxy)` now takes **1,832** elementary moves, with rank peak **3**, cyclic peak **35**, and raw peak **45**. Round 14 took 2,757 moves, with cyclic peak 40 and raw peak 57. The fixed-marking rank-three prefix to the literal deletion chart also improves from cyclic peak 40 to **32**. [Full strict ledger](../certificates/round15_stable_proof_cap35_external.jsonl) · [Full replay receipt](../results/round15_stable_proof_cap35.json) · [Literal-chart receipt](../results/round15_stable_proof_cap32.json)

## Replacing high-energy products

Record the ordered triple of individual cyclic classes after each original elementary move. Each class is represented by its least cyclic rotation over both signs. Scan for runs of product edges above the target cap. At each run, search in both directions from its bounding cyclic triples, keeping the generator marking and row order fixed. The search used row width 21, cyclic energy at least 14, and relative bridges of length at most one. Positive paths are checked independently of that search by expanding every edge into elementary conjugations, inversions and right multiplications.

The cap-35 ledger replaces sixteen runs, nine before the literal deletion chart and seven during tail clearing. The first replacement, spanning original rank-three steps 600 through 703, has identical bounding cyclic triples. Conjugations and inversions suffice to match the exact free words. The compiler expands all other detours and checks their ordered free-word boundary states against the original ledger. It then erases loops in the ordered cyclic trace and recompiles the surviving **136 product edges**, keeping the ambient generators fixed. The final rank-three state is literally the target pair with an isolated `z` in its original deletion slot. [Detour input](../certificates/round15_stable_proof_cap35_detours.json) · [Compiler](../experiments/round15_stable_proof_splice.py) · [Independent stack-reduction checker](../experiments/round06_stable_proof_strict_verify.cpp)

The rank-three detours allow the projected ordinary donor pair to vary temporarily. For example, some tail detours exchange the 13-letter donor `XXYXYxxyXyxxy` for the 12-letter `XXYXYXYxxyxy`. Other tail states contain `z` in more than one relator. Both exact energy-24 donors return before the final deletion. Holding the two donors fixed in Round 14 required a known tail of length 13, corresponding to total energy 38. [Round 14 local clearing](round-14-stable-proof.md) · [Round 15 tail detours](../certificates/round15_stable_proof_cap35_detours.json)

## Cap-32 literal chart

Thirteen detours lead from stabilized AK(3) to the exact ordered chart

~~~text
XXYxZYY  XYXYxZYYZyzyz  XYxZYZyzyyz
~~~

The compact chart prefix uses **898** rank-three elementary moves after stabilization, **71** product edges, cyclic peak **32**, and raw peak **37**. This gives a directly replayable forward seed in the literal marking. The chart can be locally cleared to the same external pair, but the cap-32 prefix alone stops before that clearing. [Literal-chart ledger](../certificates/round15_stable_proof_cap32_literal.json) · [Cap-32 detours](../certificates/round15_stable_proof_cap32_detours.json)

At cap 34, the ordered bidirectional probe found detours for seventeen of the eighteen over-cap runs in the Round 14 full trace. It did not join the last tail segment, between original rank-three steps 2403 and 2743, within 22,000 expansions under the stated bridge and width restrictions. The source there is `(XXYYxxyyZ, XXYxYXXYxxy, XXYXYxxyXyxxy)`; the target is `(Z, XXYxYXXYxxy, XXYXYxxyXyxxy)`. This is a bounded search result. Changing the earlier clearing route can change the forward seeds for this last join.

The energy-24 pair is absent from the certified ordinary cap-32 component. The new stable upper bound is 35, so a strict stable-versus-ordinary peak gap for the exact endpoint remains open. [Ordinary cap-32 audit](../results/round14_cyclic32_independent.json) · [Exact endpoint membership](round-13-stable-proof.md)

## Reproduction

~~~sh
mkdir -p "$work"
python3 -B experiments/round15_stable_proof_splice.py \
  certificates/round14_stable_proof_external_local.jsonl \
  certificates/round15_stable_proof_cap35_detours.json "$work/external.jsonl"
c++ -std=c++17 -O3 experiments/round06_stable_proof_strict_verify.cpp -o "$work/check"
"$work/check" "$work/external.jsonl"

python3 -B experiments/round15_stable_proof_splice.py --prefix \
  certificates/round14_stable_proof_frame_prefix.json \
  certificates/round15_stable_proof_cap32_detours.json "$work/literal.json"
python3 -B experiments/round04_stable_proof_paths.py verify "$work/literal.json"
~~~
