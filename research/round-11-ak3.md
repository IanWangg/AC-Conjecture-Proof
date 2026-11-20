# Round 11 · Exact joins and three-block Wirtinger repair

2026-11-19. The entire 777,475-orbit marked cap-32 sample and 20,490 Whitehead-minimized descendants of the strict cap-32 waypoint fail an exact subgroup join to 23,902 verified trivial archive pairs. A constructive search alternating both receivers also misses the reverse states. For the wrong Wirtinger pair, an exact intersection of finite charts produces a new common intermediate. Two explicit finite quotients exclude the middle block for every intermediate exposed by the first two completion stages through cyclic length 24.

## Archive joins from the cap-32 sample

Round 10 checked the 67 external energy-31 signed orbits from the marked energy-17 expansion against the reverse archive. The same all-tail basis test now covers all 777,475 orbits from the expansion, including all 397,801 known external orbits. It allows independent conjugation of each relator on both sides before testing whether the resulting subgroups are conjugate. Equal rank-two subgroup bases can then be joined by ordinary Nielsen moves. The search tests 2,675,055 distinct rotated cores and 297,100 geodesic bridge placements, with no hit among 268 basis-pair lookups. [Round 10 sample ancestry](round-10-ak3.md#a-sharp-cap-32-entry-from-the-marked-energy-17-pair) · [Exact all-tail basis test](round-04-ak3.md) · [Search and input hashes](../results/round11_ak3_archive_joins.json)

A separate search alternates cyclic ordinary products and joint Whitehead minimization from `(XXYxyxY, XXXYXYxxxYYXYxxYxxyxyXXY)`, reached by the strict 875-instruction ledger. With product peak 36, frontier energy 31, beam 144 and seven layers, it generates 20,490 distinct short minimal classes with zero primitive hits. These classes require 2,427,776 reverse bridge placements and 38,314 basis-pair lookups, with zero joins. Joint minimization preserves ordinary AC-triviality by automorphism equivariance and allows a fresh ambient marking at each search edge. The product and frontier bounds apply in these markings. The same program gives two primitive hits in one layer from the known trivial Wirtinger pair. [Strict waypoint](../certificates/round10_ak3_e17_cap32.json) · [Whitehead product method](round-09-ak3.md) · [Search and controls](../results/round11_ak3_archive_joins.json)

## Alternating quotient-conjugacy charts

Let `A = XXYYxyyyxYY`, `B = XXYxyXyxYY` and `C = XXYYxyXyyxYY`. The wrong pair `(A,B)` has a strict 105-instruction path from AK(3). The corrected pair `(C,A)` has a strict 73-instruction path to the basis. The constructive search grows forward beams from the wrong pair and the cap-32 waypoint, plus a reverse beam from `(C,A)`. Each beam alternates the receiver of a finite fixed-donor chart update. A target index uses the retained donor's signed cyclic word and tests the corresponding other row from the archive or the corrected-side beam. It includes all eight signed ambient markings and makes explicit loop-membership tests for every indexed receiver, including those past the heuristic length horizon used to harvest new beam states. Each loop must have determinant of absolute value one with the donor. A found route can be expanded and verified in the free group. [Wirtinger endpoints](round-10-stable-proof.md#the-frozen-repair-and-its-ordinary-endpoints) · [Fixed-donor chart method](round-08-ak3.md) · [Direct checker](../experiments/round11_ak3_targeted_acm.cpp) · [Search and strict compiler](../experiments/round11_ak3_targeted_acm.py)

| Source | Marked pairs | Direct charts | Target-word checks | Joins |
| --- | ---: | ---: | ---: | ---: |
| Wrong Wirtinger | 238 | 93 | 39,156 | 0 |
| Strict cap-32 waypoint | 212 | 138 | 76,176 | 0 |

The reverse beam contributes 186 marked pairs. The quick profile uses four alternating layers and a beam width of 16. Its chart completion requests three stages, with 20 wrong-side direct charts reaching the 90,000-vertex allocation limit before their final requested stage. Only completed stages contribute tests. As a positive control the direct checker detects `X` with donor `A` in the first completion stage from `(C,A)`. Its compiler strictly replays the resulting eight-instruction move to `(X,A)`. [Alternating search receipt](../results/round11_ak3_targeted_acm.json)

## Three-block repair through a common middle relator

Consider the fixed row assignment

~~~text
(A,B) → (h,B) → (h,C) → (A,C).
~~~

The first and third blocks require `h` to appear as a cyclic loop in the charts of `A` with donors `B` and `C`, with `det([h],[B]) = ±1`. The signed exponent vectors of the two donors are equal, so the same weight test works for both graphs. A word labels a loop in each graph precisely when it labels a loop at a vertex of their fibre product. Prune degree-zero and degree-one vertices, then enumerate cyclically reduced paths up to the length bound, taking the least product vertex of each closed path as its base. Record signed cyclic word classes of determinant weight ±1. The test is complete for cyclic words through the stated length in the specified finite completions. [Fibre-product enumeration](../experiments/round11_ak3_wirtinger_middle.cpp) · [Witness and ledger driver](../experiments/round11_ak3_wirtinger_middle.py)

| Completed outer stage | Maximum cyclic length | Product vertices | Common intermediates |
| --- | ---: | ---: | ---: |
| 1 | 24 | 121,303 | 1 |
| 2 | 20 | 95,530,123 | 1 |
| 2 | 24 | 95,530,123 | 2 |

The stage-2 product has 2,075,579 vertices after pruning and visits 141,345,748 reduced prefixes through length 24. The two words are `A` and `XXYxyXYxyxYXYxyXyyxYY`. The new word has independent strict outer routes of 136 instructions from `(A,B)` and 44 from `(A,C)`. Reversing the latter gives the third block. [Complete enumerations and strict outer replays](../results/round11_ak3_wirtinger_middle.json)

In the middle block, fixing `h` means every donor product is trivial in the quotient by `h`. The images of `B` and `C` would have to be conjugate up to inversion. For `h=A`, a marking in \(S_5\) kills `h` and gives cycle types \((5)\) and \((1,1,3)\). For the new `h`, a marking in \(S_7\) kills `h` and gives \((1,6)\) and \((1,1,2,3)\). These finite witnesses exclude middle blocks of any length for both candidates. Hence the three-block pattern above fails whenever both outer conversions are witnessed in the stage-two graphs and the cyclic intermediate has length at most 24. Additional chart stages or additional receiver alternations may admit other possibilities. [Generator images and cycle checks](../results/round11_ak3_wirtinger_middle.json)

## Reproduction

Use the Round 10 marked energy-17 outward sample, the cap-56 reverse archive TSV and its matching `.sources.json`. The reverse archive is obtained by replaying the published ledgers. The TSV hashes are in the search receipts. [Archive generation](round-04-ak3.md#reproduction) · [Round 10 incremental generator](round-10-ak3.md#reproduction)

~~~sh
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round06_ak3_orbit_index.cpp -o "$work/orbit-index"
c++ -std=c++17 -O3 experiments/round09_ak3_whitehead_products.cpp -o "$work/whitehead-products"
c++ -std=c++17 -O3 experiments/round08_ak3_acm.cpp -o "$work/acm"
c++ -std=c++17 -O3 experiments/round11_ak3_targeted_acm.cpp -o "$work/targeted-acm"
c++ -std=c++17 -O3 experiments/round11_ak3_wirtinger_middle.cpp -o "$work/wirtinger-middle"
"$work/orbit-index" "$e17_outward_tsv" "$reverse" "$work/e17.join.json"
printf '%s\t%s\n' XXYxyxY XXXYXYxxxYYXYxxYxxyxyXXY > "$work/waypoint.tsv"
"$work/whitehead-products" 36 31 7 144 "$work/waypoint.tsv" "$work/waypoint.classes.tsv" "$work/waypoint.edges.tsv"
"$work/orbit-index" "$work/waypoint.classes.tsv" "$reverse" "$work/waypoint.join.json"
python3 -B experiments/round11_ak3_targeted_acm.py --quick "$work/acm" "$work/targeted-acm" \
  "$reverse" "$archives" "$work/targeted-trivialization.json"
python3 -B experiments/round11_ak3_wirtinger_middle.py "$work/wirtinger-middle" "$work/targeted-acm" \
  "$work/middle-trivialization.json"
~~~

The marked outward file is the `.outside.tsv` output of the Round 10 expansion, using the single marked energy-17 source for the boundary seed pass, the 135,156 cap-31 orbits of energy up to 23 as the lower set, and 600,000 expansions. Use the exact archive TSV and the matching original archive zip directory at `$archives` to enable direct strict compilation if a target matches.
