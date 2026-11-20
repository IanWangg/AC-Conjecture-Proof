# A strict stable-versus-ordinary cyclic peak gap from AK(3)

Consider the marked pairs

~~~text
E22 = (XXYYYxYXY, XXYYxYXXyxxY)
E24 = (XXYxYXXYxxy, XXYXYxxyXyxxy)
~~~

Each has a strict stable path from AK(3) of cyclic peak **33** and maximum rank **3**. Every ordinary path from AK(3) to either pair must have cyclic peak at least **34**. The inequality compares paths from the same marked source to the same marked endpoint. It gives a finite peak separation. Unbounded ordinary reachability of these endpoints remains open. [E22 stable ledger](../certificates/round16_stable_proof_cap33_e22.jsonl), [E24 stable ledger](../certificates/round16_stable_proof_cap33_external.jsonl).

## Ordinary lower bound

Start the full ordinary cyclic product search at the signed orbit of E22 with total cyclic length at most 33. For two cyclic rows, enumerate all signed rotations and all shortest relative bridges allowed by the cap. Independent conjugation of each relator, inversion and row ordering disappear in the cyclic model. Simultaneous signed generator permutations give an equivariant quotient. Every ordinary path within the cap maps to a path in this quotient, so disjointness already suffices to exclude a marked ordinary path. [Cyclic product and bridge bound](round-12-primitive-step.md), [independent ordinary closure method](round-14-independent-cyclic32.md).

The reverse search closes after expanding all **37,659** signed orbits, with **65,473,912** candidate products and **1,928,110** admitted products. It checks every reached energy-33 state against the complete sorted first-exit index from the AK(3) cap-32 component, which contains **1,258,633,777** keys. There are no matches. The positive index control finds a first-exit record from the ordinary AK(3) starting orbit. [Reverse search](../experiments/round16_ak3_reverse_seed.cpp), [first-exit provenance](round-14-independent-cyclic32.md#exact-first-exit-deduplication-at-cap-33).

The independent stack-reduction verifier recomputes the candidate products, matches both counts, and checks closure and connectedness from E22. It runs directly on the stored reverse catalogue without the first-exit index. The catalogue includes the signed orbit of E24 and excludes the signed orbit of AK(3). Removing the last catalogue row makes the independent checker fail its closure check. The smallest cyclic energy is **20**, with five orbits. A separate Euclidean primitive scan checks the **36,804** distinct cyclic coordinate keys and finds no primitive. A separate exact single-product scan on the full catalogue excludes a primitive immediately after one product with arbitrary conjugating tails and output length. [Compressed catalogue](../certificates/round16_ak3_e22_cap33_component.tsv.gz), [independent verifier](../experiments/round07_ak3_wide_verify.cpp), [matched receipts](../results/round16_ak3_e22_cap33_component.json), [unbounded single-product criterion](round-12-primitive-step.md).

## Stable upper bound

Independent strict replay reaches E22 in **1,306** operations and E24 in **1,346**, with raw peak **41** for both. The E22 ledger deletes an isolated auxiliary generator earlier. The resulting ordinary **40**-instruction suffix joins E22 to E24 and has raw peak **29**. Both endpoints are literal ordered free words. [Ledger construction](round-16-stable-proof.md), [ordinary suffix](../certificates/round16_stable_proof_e22_to_e24.json).

## Reproduction

The stored catalogue and certificates suffice to replay the lower and upper bounds. The optional reverse enumeration requires the Round 14 compacted first-exit directory.

~~~sh
gzip -cd certificates/round16_ak3_e22_cap33_component.tsv.gz > "$work/e22.tsv"
c++ -std=c++17 -O3 -pthread experiments/round07_ak3_wide_verify.cpp -o "$work/wide-verify"
"$work/wide-verify" 33 8 "$work/e22.tsv" "$work/independent.json" XXYYYxYXY XXYYxYXXyxxY
c++ -std=c++17 -O3 experiments/round06_stable_proof_strict_verify.cpp -o "$work/strict"
"$work/strict" certificates/round16_stable_proof_cap33_e22.jsonl
"$work/strict" certificates/round16_stable_proof_cap33_external.jsonl
python3 experiments/elementary_verify.py certificates/round16_stable_proof_e22_to_e24.json
c++ -std=c++17 -O3 -pthread experiments/round16_ak3_reverse_seed.cpp -o "$work/reverse"
"$work/reverse" XXYYYxYXY XXYYxYXXyxxY "$compacted" 2000000 6 "$work/rebuilt.tsv"
cmp "$work/e22.tsv" "$work/rebuilt.tsv"
~~~
