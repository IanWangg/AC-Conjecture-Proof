# Round 13 · Three alternating ordinary receiving blocks

2026-11-19. Two strictly reachable energy-20 pairs serve as marked sources for a three-block search. The larger run considered 139 first intermediates and tested all 23,902 verified archive pairs in the completed middle and reverse charts. It found no basis path. A separate exact middle-product test covers 872 marked outputs, each followed by an arbitrary-length single-product primitive query. [First energy-20 entry](../certificates/round11_ak3_cap32_minimum.json), [second entry](../certificates/round12_ak3_second_energy20.json), [Round 12 chart results](round-12-ak3.md).

The exact cover calculations in this round exclude both reciprocal two-block orders at each energy-20 seed over the original archive. The tests below allow a third receiving block. [First seed and its ascending cover](round-13-ascending-cover.md), [second seed and its integral cover](round-13-integral-cover.md).

## Genuine three-block archive joins

From a marked AK(3) pair `(r,d)` and a trivial archive pair `(s,e)`, look for

~~~text
(r,d) -> (h,d) -> (h,e) -> (s,e).
~~~

Each arrow changes its named receiver by ordinary moves with the other word kept as a donor. The test imposes the three changes of cyclic class `h != r`, `e != d` and `h != s`. This removes paths with an omitted receiving block. A finite first completion supplies short returns `h` and explicitly checks their earliest completed stage. The exact torus and amalgam first-chart contacts from Round 12 are also included as first-intermediate candidates. For each `h`, check all archive donor words `e` with determinant of absolute value one relative to `h`. Group the resulting `(s,e,h)` queries by the reverse chart `(s,e)`; membership of `h` in that chart supplies the reversed third block. Signed ambient permutations of the archive are included. [Three-block search and strict compiler](../experiments/round13_ak3_three_blocks.py).

The positive control uses five distinct cyclic classes across `r,d,h,e,s` and has all three chart memberships already at stage one. The receiving blocks take 117, 3 and 29 strict instructions. Normalizing the verified reverse endpoint and following its basis suffix gives a fully replayed **224-instruction** strict ordinary path. [Positive controls and short profile](../results/round13_ak3_three_blocks_short.json).

| Archive energy cap | Archive pairs | First intermediates | Middle word checks | Middle word hits | Third word checks | Joins |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 24 | 4,657 | 71 | 205,202 | 5 | 85 | 0 |
| 56 | 23,902 | 139 | 2,588,353 | 55 | 3,670 | 0 |

The larger run has 117 reverse charts, 115 completed at stage three and two at stage two. Its 139 middle charts complete through stage two before their allocation limit. The short run completes the middle charts at stages one and two and all 43 reverse charts at stage two. These are exact membership tests within the completed finite graphs, with intermediate choices and graph limits as recorded in the receipts. The third block remains available outside this family. [Full profile](../results/round13_ak3_three_blocks_full.json).

## Primitive targets in the third block

Harvesting short center words from the 71 first choices gives 85 marked `(h,e)` pairs through cyclic energy 42. In each last chart, the Euclidean slope classification gives two infinite primitive tails and a finite list of interior slopes. A partial-permutation traversal tests each entire tail in the last completed graph. The 170 tail tests and 53 interior class tests give no primitive witness. A separate 110-move control verifies that the primitive completion compiler can turn a nontrivial primitive word and a compatible second row into the basis in the original marking. [Exact slope search and compiler](../experiments/round13_ak3_primitive_third.py), [receipt](../results/round13_ak3_primitive_third.json).

A second center test exhausts a single ordinary product with donor `h` at cyclic energy cap 38 after each of the same 71 first choices. Two choices are excluded by the bound `|h| + ||h|-|d|| > 38`. A separate string implementation agrees on all other rotation and shortest-bridge menus after 53,644 checks. The resulting 872 distinct marked pairs have no primitive coordinate. The unbounded single-product primitive scanner also yields no hit over all 872 pairs, allowing either receiver and arbitrary conjugating tails. The 49 signed keys of energy at most 31 all occur in the new cap-32 catalogue. [Native menu](../experiments/round13_ak3_exact_center.cpp), [independent checker](../experiments/round13_ak3_exact_center.py), [receipt](../results/round13_ak3_exact_center.json).

## Reproduction

Use the verified reverse TSV and its adjacent `.sources.json`, the original archive directory and the ordinary cap-31 and cap-32 catalogues. [Archive provenance and replay](round-04-ak3.md#reproduction), [ordinary catalogues](round-11-cyclic32.md).

~~~sh
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round08_ak3_acm.cpp -o "$work/acm"
c++ -std=c++17 -O3 experiments/round11_ak3_targeted_acm.cpp -o "$work/targeted"
c++ -std=c++17 -O3 experiments/round12_ak3_chart_index.cpp -o "$work/chart-index"
c++ -std=c++17 -O3 experiments/round13_ak3_exact_center.cpp -o "$work/exact-center"
c++ -std=c++17 -O3 -pthread experiments/round12_ak3_primitive_step.cpp -o "$work/primitive-step"
python3 -B experiments/round13_ak3_three_blocks.py "$work/acm" "$work/targeted" "$work/chart-index" \
  "$reverse" "$archives" > "$work/three-block-short.json"
python3 -B experiments/round13_ak3_three_blocks.py "$work/acm" "$work/targeted" "$work/chart-index" \
  "$reverse" "$archives" --first-depth 5 --first-allocation 2500000 --first-horizon 26 \
  --first-bases 512 --center-depth 4 --center-allocation 800000 --reverse-depth 3 \
  --reverse-allocation 500000 --reverse-energy 56 > "$work/three-block-full.json"
python3 -B experiments/round13_ak3_primitive_third.py "$work/acm" "$work/three-block-short.json"
python3 -B experiments/round13_ak3_exact_center.py "$work/exact-center" "$work/primitive-step" \
  "$work/three-block-short.json" --catalogues "$cap31" "$outside32"
~~~
