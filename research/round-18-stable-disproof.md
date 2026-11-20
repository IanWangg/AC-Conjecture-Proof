# Narrowing the two active intervals at stable length 20

2026-11-19. A length-20 one-padding path for AK(3) can have two active intervals in its degree-nine retraction only if both have width nine. The completed marked comparisons exclude the six remaining shorter pairs and all three pairs containing an interval of width eight. An isolated interval still needs width at least nine. [Last six shorter pairs](../results/round18_stable_disproof_widths_six_seven.json) · [Width-eight rules and cuts](../results/round18_stable_disproof_wide_cuts.json)

## The last pairs with widths six or seven

Round seventeen leaves at most two idle instructions in the two-interval case. The remaining width pairs with shorter width six are $(6,10)$, $(6,11)$ and $(6,12)$. With shorter width seven they are $(7,9)$, $(7,10)$ and $(7,11)$. For every possible allocation of idle instructions, begin the short side with a residual marked interval rule and meet within the wider interval. Test both sides as the short side, including reversals of its interval. An actual degree-nine path would give a meeting, with the row ordering aligned to its auxiliary coefficients. [Structured cut proof](round-17-stable-disproof.md#structured-cuts-for-the-next-width-pairs)

| Widths | Degree that excludes all splits | Streamed transitions in that degree |
| --- | ---: | ---: |
| (6,10) | 6 | 631,664,404 |
| (6,11) | 6 | 492,645,216 |
| (6,12) | 6 | 275,209,536 |
| (7,9) | 7 | 641,098,416 |
| (7,10) | 7 | 500,921,512 |
| (7,11) | 7 | 280,597,016 |

In degree six, all comparisons are empty when the shorter width is six. The positive lower-quotient controls for the last three rows are on the basis side of the cut. The successive idle splits retain $(6,10,16)$ for $(7,9)$, $(14,2)$ for $(7,10)$ and $2$ for $(7,11)$. All disappear in degree seven. Both zero and nonzero auxiliary increments of the width-seven interval are included.

These six exclusions leave $(8,8)$, $(8,9)$, $(8,10)$ and $(9,9)$ before the wider-interval comparison. The sole-interval branch still needs width at least nine. [Sole-interval lower bound](round-14-stable-disproof.md#completing-the-cut-in-degree-nine)

## Unrestricted width-eight rules

For two intervals, a strict idle shortening of either one would contradict saturation of the degree-nine length-17 corridor, which has an identity row at every tick. Thus a width-eight interval can only use templates that survive the radius-seven comparison. Generate all six internal instructions between birth and death on the formal rows $a,b,a^{\pm1}$. Track the auxiliary coefficient on each physical row and discard a formally trivial row or wait during the active part. At death the equal old parity rows must have different auxiliary coefficients, because the three original rank-three linear rows form a basis.

A literal replacement, or a replacement using the terminal equality, follows from membership in the exact radius-seven ordinary ball. The exponent test excludes equalities with different coefficients modulo 16. The radius-seven ball has 10,514,136 formal pairs. The first five internal widths are 50, 930, 15,842, 262,805 and 4,329,001. Streaming the last internal instruction leaves 3,592,267 distinct marked terminal templates after these tests. The standalone census and its replay give the same sorted table digest. [Native formal rules](../experiments/round18_stable_disproof_width_eight_rules.cpp) · [Generator counts and digest](../results/round18_stable_disproof_wide_cuts.json)

## Cutting between two width-eight intervals

Choose an idle vertex between the two intervals. Each side now contains exactly one interval. This avoids taking two successive wide intervals on the same side of a fixed time cut. The two remaining idle instructions can be distributed as $0+2$, $1+1$ or $2+0$. On each side enumerate every position of the one interval among the idle instructions. Before the first interval the active auxiliary coefficients are zero, so the table's zero-input markings apply on both sides. After that interval the idle instructions transport those marks with the row labels. The erased row's auxiliary bit is one. Thus agreement of the two active words with their aligned bits is a necessary condition for meeting. The reverse interval is covered because any strict replacement of it would give a strict forward replacement.

The three degree-six widths on the AK(3) side are 18,525, 408,540 and 6,098,668. From the basis they are 36,798, 420,135 and 4,328,526. The opposite sets are disjoint in all three allocations. This excludes $(8,8)$, leaving any two-interval candidate with total active width at least 17. [Between-interval search](../experiments/round18_stable_disproof_wide_cuts.cpp) · [Complete cut receipt](../results/round18_stable_disproof_wide_cuts.json)

## A cut inside the wider interval

The same width-eight table gives the short boundary when the other interval has width nine or ten. With $i$ idle moves on the short side, expand $3-i$ active steps from it and supply the remaining active depth from the other side. The projected birth and the reverse of the last cancellation each import a signed copy, with auxiliary coefficient one plus the donor's. Inside the wider interval use actual marked instructions, allowing old waits or identities in lower quotients. The cut preserves all three projected rows and their auxiliary coefficients. Both orientations are tested.

For $(8,10)$ there are zero idle instructions. The two degree-six comparisons check 58,515,744 and 216,693,792 moves and are empty. For $(8,9)$ the one idle instruction can occur on either side. When it is on the wider side both degree-six comparisons are empty. When it is on the short side the degree-six counts are zero with that side based at AK(3) and 12 with it based at the basis. Both degree-seven comparisons for that split are empty after 58,577,792 and 222,019,224 moves. This leaves $(9,9)$ as the only two-interval pair. It would use all 18 instructions inside the two intervals. [Structured results](../results/round18_stable_disproof_wide_cuts.json)

## Reproduction

~~~sh
work=/tmp/ac-r18-stable-disproof
mkdir -p "$work"
python3 -B experiments/round15_stable_disproof_two_widths.py > "$work/six-seven.txt"
python3 -B experiments/round16_stable_disproof_two_sevens.py > "$work/two-sevens.txt"
c++ -std=c++17 -O3 experiments/round15_stable_disproof_two_widths.cpp -o "$work/marked-cut"
for wider in 10 11 12
do
  for (( split=0; split<=12-wider; ++split ))
  do
    "$work/marked-cut" 6 --structured 6 "$wider" "$split" < "$work/six-seven.txt"
  done
done
for wider in 9 10 11
do
  for (( split=0; split<=11-wider; ++split ))
  do
    "$work/marked-cut" 6 --structured 7 "$wider" "$split" < "$work/two-sevens.txt"
    "$work/marked-cut" 7 --structured 7 "$wider" "$split" < "$work/two-sevens.txt"
  done
done
c++ -std=c++17 -O3 experiments/round18_stable_disproof_width_eight_rules.cpp -o "$work/width-eight-rules"
"$work/width-eight-rules" > "$work/width-eight.txt"
LC_ALL=C sort "$work/width-eight.txt" | shasum -a 256
c++ -std=c++17 -O3 experiments/round18_stable_disproof_wide_cuts.cpp -o "$work/wide-cuts"
"$work/wide-cuts" 6 < "$work/width-eight.txt"
"$work/wide-cuts" 6 9 0 < "$work/width-eight.txt"
"$work/wide-cuts" 6 9 1 < "$work/width-eight.txt"
"$work/wide-cuts" 7 9 1 < "$work/width-eight.txt"
"$work/wide-cuts" 6 10 0 < "$work/width-eight.txt"
~~~
