# Chartless releases from the nine energy-17 ordinary states

2026-11-19. A stabilized energy-17 minimum first admits a one-product transition to three nonprimitive rows at cyclic peak **28**. At that peak, strict rank-three excursions from the first minimum reach all nine signed energy-17 minimum orbits after deletion. The complete ordinary AK(3) prefix to the first minimum gives verified stable paths to those nine literal endpoints at maximum rank three and cyclic peak **33**. [Ordinary prefix](../certificates/round18_ak3_c33_minimum_ordinary.json), [marked route inputs](../certificates/round19_stable_proof_e17_routes.json), [strict receipts](../results/round19_stable_proof_e17.json).

## Exact entrance and first-exit calculation

All nine energy-17 representatives have the short row `xxyXYY` and a nonprimitive length-eleven companion. Stabilize by `z`. A first chartless state in one product has to change the unique primitive row, which is the added singleton. The output row has width at most the cyclic cap minus 17. Thus the width-21 native scanner retains the entire chartless entrance menu through cap 33. The signed rotation product search gives no entrance at cap 27 from any of the nine sources. At cap 28 the first source has **48** entrances. An independent stack reducer recomputes the entrance products in the only possible receiving slot and verifies the whole cap-28 chartless closure, checking **874,368** product candidates after entrance. [Independent audit](../experiments/round19_stable_proof_e17_audit.py).

From those one-product entrances, expand only states in which no row is primitive and harvest every adjacent first exit with a primitive row. In the completed components through cap 33, the two shortest rows have combined width at least 17. The smallest possible positive-bridge departure energy across the chartless sources is 36, computed as their total energy plus the smallest donor width plus two. Every capped exit from these stored states therefore fits width 21 and uses a zero bridge. These checks concern the chartless sector from the one-product entrances.

| Rank-three cap | Chartless orbits | Charted first exits | Native signed rank-two projections | Identical ordinary cap from the first minimum |
| --- | ---: | ---: | ---: | ---: |
| 28 and 29 | 432 at each | 441 at each | 9 | 17 |
| 30 and 31 | 5,568 at each | 5,630 at each | 62 | 19 |
| 32 | 61,200 | 50,817 | 363 | 21 |
| 33 | 73,768 | 63,001 | 363 | 21 |

The table uses the first source. At cap **28**, all nine sources give the same chartless orbit set of 432 states and the same nine projected keys. Separately, at cap **32**, all nine give the same chartless orbit set of 61,200 states and the same 363 projected keys. The projection equalities compare exact signed sets after the native primitive-chart normalization. The projected pairs give zero primitive coordinates. The cap-28 marked transfers use two to seven cyclic products and 39 to 99 strict instructions including stabilization and deletion. The independent stable replay verifies the full ledgers from AK(3). [Census and path receipts](../results/round19_stable_proof_e17.json), [fixed-marking compiler](../experiments/round19_stable_proof_e17.py).

## Length-six donor release at peak 33

Every chartless state in the cap-32 calculation retains precisely one row in the signed cyclic orbit of `xxyXYY`. At cap 33, **528** chartless states lack that orbit. A **46-instruction** strict path from the first stabilized minimum enters the chartless sector in one product and removes the short donor's orbit with the next product. The exact endpoint is `(XXXXyXyyyXy, XXXXyxyXyXy, XXyyZXZxzxY)`. Both its cyclic and raw peaks are 33. Under the specified one-product entrance and subsequent chartless condition, the minimum peak for releasing that donor is exactly 33. [Strict donor-release ledger](../certificates/round19_stable_proof_e17_donor_release.json).

The broader cap-32 reverse probe of the Round 18 chart allows up to three auxiliary occurrences, bridge length at most three and per-row width 21. From the 7,229 earlier singleton roots it expands **225,000** states and discovers **8,652,144**, with zero intersections with the earlier one-occurrence component. This remains a bounded negative. No strict path to the basis or full stable release at cap 32 was found. [Reverse probe receipt](../results/round19_stable_proof_e17.json).

## Reproduction

~~~sh
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round12_stable_proof_corridor.cpp -o "$work/corridor"
c++ -std=c++17 -O3 experiments/round07_stable_proof_waypoint_search.cpp -o "$work/ordinary"
for cap in 17 19 21
do
  "$work/ordinary" "$cap" 1000000 xxyXYY xxxxYxYxYXY "$work/ordinary$cap" \
    > "$work/ordinary$cap.json"
done
i=0
while read -r a b
do
  [ "$((${#a} + ${#b}))" -eq 17 ] || continue
  i=$((i+1))
  for cap in 27 28 29 30 31 32 33
  do
    if [ "$i" -eq 1 ] || [ "$cap" -eq 27 ] || [ "$cap" -eq 28 ] || [ "$cap" -eq 32 ]
    then
      "$work/corridor" 3 "$cap" 220000 "$a" "$b" Z "$work/exact$cap-m$i" \
        > "$work/exact$cap-m$i.json"
    fi
  done
done < certificates/round18_ak3_c33_low20.tsv
python3 -B experiments/round19_stable_proof_e17_audit.py "$work"

python3 -B experiments/round19_stable_proof_e17.py \
  certificates/round18_ak3_c33_minimum_ordinary.json \
  certificates/round19_stable_proof_e17_routes.json \
  certificates/round18_ak3_c33_low20.tsv "$work/strict"
c++ -std=c++17 -O3 experiments/round06_stable_proof_strict_verify.cpp -o "$work/check"
for ledger in "$work"/strict/stable-*.jsonl
do
  "$work/check" "$ledger"
done
python3 -B experiments/round04_stable_proof_paths.py verify \
  certificates/round19_stable_proof_e17_donor_release.json
~~~
