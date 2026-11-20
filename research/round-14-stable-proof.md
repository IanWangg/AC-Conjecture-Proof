# Round 14 stable AC proof track

The same external energy-24 pair now has a strict stable entry from AK(3) in **2,757** instructions with maximum rank three, cyclic peak **40**, and raw peak **57**. The previous entry used 18,477 instructions at cyclic peak 170. The final pair is literally `(XXYxYXXYxxy, XXYXYxxyXyxxy)` in both ledgers. [New strict ledger](../certificates/round14_stable_proof_external_local.jsonl), [replay receipt](../results/round14_stable_proof_local_chart.json), [previous ledger](../certificates/round13_stable_proof_external_projection.jsonl).

## A literal frame for the intrinsic pivot

The rank-three endpoint from Round 13 is `(XYzYZYXYzy, XYxyzyZyxZ, XYxzyZY)`. The first row is primitive and has multiple occurrences of each generator. Apply the three Whitehead changes in order with multiplier and cut `(y,yzZ)`, `(z,zx)`, and `(x,xZ)`. Their composition is the marking $x\mapsto z$, $y\mapsto y$, $z\mapsto yzXY$. These maps use only elementary interactions with the spare generator in the compiled initial frame. The strict construction realizes the marked initial tuple in 188 instructions including stabilization at cyclic peak 28 and raw peak 38. It then transports the recorded rank-three path and normalizes the rows to

~~~text
XXYxZYY  XYXYxZYYZyzyz  XYxZYZyzyyz
~~~

This prefix has 1,914 instructions including stabilization, cyclic peak 40, and raw peak 57. It ends at a literal single-occurrence `z` chart. [Rank-three prefix](../certificates/round14_stable_proof_frame_prefix.json), [construction and replay](../experiments/round14_stable_proof_local_chart.py).

## Strict local deletion

Cyclically rotate and orient the pivot to `zXyxxyy`. Multiplications by conjugates of this pivot replace each occurrence of `z` in the other two rows by the inverse of `Xyxxyy`. The two stabilized donors are then exactly the final energy-24 rows. This takes the existing path to 2,046 instructions with the same cyclic peak.

The bounded word search uses cyclic cuts of the two donor relators and their inverses. A cut $u v^{-1}$ allows replacing $aub$ by $avb$, a right multiplication by a conjugate of the inverse relator. A bidirectional search from the pivot tail and the empty word meets at tail cap 13, expanding 844 and 1,165 words on the two sides. The reconstructed sequence uses 28 explicit normal factors. The checker directly multiplies their conjugates into the free tail and confirms every intermediate length is at most 13. The cap-12 directed rewrite searches do not meet. That negative result is confined to the stated rewrite search. Applying the factors to the pivot uses cyclic energy at most $24+1+13=38$ during the tail clearing, so the full path retains cyclic peak 40. The last move destabilizes the isolated `z`. [Bidirectional factor search](../experiments/round14_stable_proof_tail.cpp), [strict replay receipt](../results/round14_stable_proof_local_chart.json).

The target's signed key `(xxyXXyxyXXY, xxyXyXXYxxYXY)` is absent from the complete cap-32 ordinary catalogue. This gives a stable entry at peak 40 into an ordinary cap-32-absent marking. The ordinary lower bound and the stable upper bound overlap above 32, so these witnesses alone leave a strict stable-versus-ordinary peak gap open. [Target membership check](round-13-stable-proof.md), [independent cap-32 audit](../results/round14_cyclic32_independent.json).

## Reverse cap-32 probe

The reverse search starts from twelve stabilized rank-two keys absent at ordinary cap 32, including the new entry's signed key. The target set is the 4,080,631 reachable marked rank-three orbits from the Round 13 remasked cap-32 run. On the interval 12 through 32 with the native per-row width 21, it expands 120,000 nodes and discovers 1,636,286, with no intersection. It counts 284,670 products omitted for exceeding row width. Expansion also stops at the budget. [Reverse receipt](../results/round14_stable_proof_reverse.json).

## Reproduction

~~~sh
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round14_stable_proof_tail.cpp -o "$work/tail"
python3 -B experiments/round14_stable_proof_local_chart.py \
  certificates/round13_stable_proof_external_prefix.json "$work/tail" \
  "$work/frame-prefix.json" "$work/external-local.jsonl"
c++ -std=c++17 -O3 experiments/round06_stable_proof_strict_verify.cpp -o "$work/check"
"$work/check" "$work/external-local.jsonl"
~~~

To reproduce the reverse probe, generate the Round 13 `min32.nodes.tsv` using the linked prior protocol. Keep columns three through five for `target32.tsv`. Write the receipt's twelve stabilized roots as tab-separated rows to `reverse-roots.tsv`. The receipt records the hashes of both input files and the reached-orbit TSV.

~~~sh
c++ -std=c++17 -O3 experiments/round11_stable_proof_reverse.cpp -o "$work/reverse"
"$work/reverse" 12 32 120000 "$work/reverse-roots.tsv" "$work/target32.tsv" "$work/reverse-short"
~~~
