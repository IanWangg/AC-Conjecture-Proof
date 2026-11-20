# One four-active block in the normalized two-padding erasure

2026-11-19. At stable budget 20, a two-padding AK(3) path has a degree-eight erasure that can be normalized to one outer active interval with exactly one four-active block. That block has width at least five. Round 20 leaves one or two blocks inside the sole outer interval. All **210** exact occupation sequences with two blocks are now excluded. [Normalization](round-20-stable-disproof.md), [occupation census](../results/round21_stable_disproof_nested_language.json), [exact cuts](../results/round21_stable_disproof_nested_blocks.json).

## Covering the midpoint

Both blocks have width at least five. Two outer crossings leave at most 14 instructions for the two blocks. For ordered widths $s,t\geq 5$ with $s+t\leq 14$, distribute the remaining $14-s-t$ steps among the two idle sections, the two three-active sections next to the ends, and the three-active gap between the blocks. Each distribution gives a different occupation sequence. The 210 sequences include 100 with three active rows at tick eight and 110 with four.

Expand from both ends to depth seven. On each side, track whether the path is idle, approaching the first block, in its first block, between the blocks, or in its second block. Four substages in each block enforce its three mandatory internal edges before it can return to three active rows. Prune a state if it cannot finish its required crossings and steps in the remaining time. At depth eight, the midpoint is either between the blocks on both sides, or inside the first block of one side and the second block of the other. In the latter case, reverse one edge from the second-block side's midpoint into the first-block side's smaller-depth states. The match uses the required internal steps in that block counted from both ends. An independent Python enumeration concatenates all the accepted half-occupations and verifies exact set equality with the direct census. [Native checker](../experiments/round21_stable_disproof_nested_blocks.cpp), [independent occupation check](../experiments/round21_stable_disproof_nested_language.py).

Each state is a sorted four-row tuple over the specified truncated characteristic-two Magnus group. A birth imports a signed copy into an identity row. A death cancels one member of a signed duplicate pair. A same-occupation instruction enumerates row inversion, single-letter conjugation, and signed right product with a different active row. It retains changed rows that stay nonidentity. These transitions are reversible. Discarding waits is valid because a wait would shorten the complete degree-eight path to budget 15, which is excluded. [Ordinary instruction engine](../experiments/round07_magnus_native.cpp), [budget-15 exclusion](round-09-stable-disproof.md).

| Degree | Midpoint between blocks | Midpoint in the first block from AK(3) | Midpoint in the first block from the basis |
| --- | ---: | ---: | ---: |
| 3 | 133,498 | 308,682 | 363,797 |
| 8 | 0 | 0 | 0 |

The counts are distinct matching midpoint tuples within each of the three cases. The degree-eight run makes **143,892,603** state expansion calls across required occupation transitions and interns **925,841** individual rows. Its measured peak resident memory is 13,318,094,848 bytes. This leaves a single four-active block of width $5\leq s\leq 14$ inside one outer interval. The restriction concerns the normalized degree-eight erasure. The replacements used to normalize it can change the two-auxiliary lift. The separate one-padding length-20 branch still has the Round 19 single-active-interval condition. [One-padding restriction](round-19-stable-disproof.md#the-remaining-isolated-interval).

## Reproduction

~~~sh
work=/tmp/ac-r21-stable-disproof
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round21_stable_disproof_nested_blocks.cpp -o "$work/nested"
"$work/nested" 3
"$work/nested" 8
python3 -B experiments/round21_stable_disproof_nested_language.py \
  | diff -u results/round21_stable_disproof_nested_language.json -
~~~
