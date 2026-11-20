# All first-chart exits after releasing the length-six donor

Starting from the 528 rank-three states where Round 19 released `xxyXYY`, the donor-free first-chart search at cyclic caps **38 and 39** gives the same **20** signed rank-two projections. These are precisely the nine energy-17 and eleven energy-22 orbits of the first energy-17 marking's ordinary cap-22 component. Each projection has a strict stable path from AK(3) with cyclic peak 38 and maximum rank three. The paths take **950 to 1,022** elementary instructions. [Stable ledgers](../certificates/round21_stable_proof_first_exit_ledgers.json.gz), [route inputs](../certificates/round21_stable_proof_first_exit_routes.json), [verification receipts](../results/round21_stable_proof_first_exits.json).

## Complete first-chart closures

Begin from every chartless node in the Round 19 cap-33 section that has lost the signed cyclic orbit of the length-six donor. Expand only chartless successors retaining that absence. Record every neighboring state with a primitive row as a first exit. The two smallest rows on every expanded state have total length at least 22. The least possible energy of a positive shortest-bridge product on these states is **46**. Thus both searches cover all conjugating tails by the zero-bridge product menu, and every allowable replacement has length at most 16 or 17, respectively. [Seed catalogue](../certificates/round20_stable_proof_released_roots.tsv), [cyclic product theorem](research-n-cyclic-search.md), [Round 20 chart-recovery theorem](round-20-stable-proof.md).

| Cap | Chartless orbits | First chart orbits | Signed rank-two projections | Isolated singleton projections | Literal stack checks |
| --- | ---: | ---: | ---: | ---: | ---: |
| 38 | 15,032 | 2,971 | 20 | 11 | 55,023,296 |
| 39 | 18,272 | 3,115 | 20 | 11 | 67,820,928 |

The native cyclic menu uses cancellation at the two seams of the product. A second verifier independently uses literal signed rotations and a stack to freely and cyclically reduce every product. It uses the existing signed-orbit encoding to verify that each admissible result is in the recorded catalogue and that every listed state is reachable on its side of the first exit. The Python chart check verifies that every exit has exactly one primitive row and that it is a literal singleton. It separately derives the projected rank-two classes by deleting that letter. There are no primitive rank-two coordinates or direct archive matches. An independent stack audit of the ordinary cap-22 reference closes its 374 orbits after 265,192 candidates. Its eleven energy-22 orbits are exactly the isolated singleton projections. The other nine projections have energy 17. [Native search](../experiments/round20_stable_proof_release.cpp), [literal stack closure](../experiments/round21_stable_proof_stack.cpp), [chart and ordinary checks](../experiments/round21_stable_proof_first_exits.py).

## Exact marked stable paths

For each of the 20 projections, follow the stored genealogy back through its released root to the first stabilized energy-17 marking. Lift the cyclic products in the original marking. Every path keeps the length-six donor orbit absent from its release until the first chart. Where the singleton still occurs in either remaining word, remove its occurrences using products with appropriately conjugated singleton relators. The free and cyclic reduction after each removal keeps the cyclic energy within the first-chart cap. Delete the isolated auxiliary generator. The independent strict interpreter verifies the final literal rank-two words, both peak measures and the move count for every ledger. The raw peaks range from 39 to 44. The rank-three cap-37 exclusion from Round 20 gives the matching local lower bound for reaching any first chart under the donor-absence condition. [Independent stable interpreter](../experiments/round06_stable_proof_strict_verify.cpp), [cap-37 exclusion](round-20-stable-proof.md#exact-donor-free-closure).

## Reproduction

Set `prior` to the `exact33-m1` output prefix regenerated in Round 19, and `reverse` to the 23,902 verified archive pairs. [Round 19 catalogue](round-19-stable-proof.md#reproduction), [archive](round-04-ak3.md#reproduction).

~~~sh
mkdir -p "$work"
roots=certificates/round20_stable_proof_released_roots.tsv
c++ -std=c++17 -O3 experiments/round20_stable_proof_release.cpp -o "$work/release"
c++ -std=c++17 -O3 experiments/round21_stable_proof_stack.cpp -o "$work/stack"
c++ -std=c++17 -O3 experiments/round07_stable_proof_waypoint_search.cpp -o "$work/ordinary"
for cap in 38 39
do
  "$work/release" "$cap" 500000 "$roots" "$reverse" "$work/all$cap" > "$work/all$cap.json"
  "$work/stack" "$cap" "$roots" "$work/all$cap.nodes.tsv"
done
"$work/ordinary" 22 1000000 xxyXYY xxxxYxYxYXY "$work/ordinary22"
python3 -B experiments/round21_stable_proof_first_exits.py "$work" "$roots" "$prior" \
  certificates/round18_ak3_c33_minimum_ordinary.json "$work/ordinary22.tsv"
c++ -std=c++17 -O3 experiments/round06_stable_proof_strict_verify.cpp -o "$work/check"
for ledger in "$work"/strict/*.jsonl
do
  "$work/check" "$ledger"
done
~~~

The compressed certificate is a JSON object mapping ledger filenames to their exact JSONL text. Each entry can be extracted and passed directly to the strict interpreter.
