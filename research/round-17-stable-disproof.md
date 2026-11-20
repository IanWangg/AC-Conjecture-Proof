# Ordinary length 20 excluded and three stable width pairs closed

2026-11-19. AK(3) needs at least **21 ordinary instructions**, both in the degree-ten characteristic-two Magnus quotient and in the free group. Its stable lower bound is **20**. Complete quotient comparisons exclude the width pairs $(7,7)$, $(6,9)$ and $(7,8)$ in a length-20 one-padding path. Its degree-nine retraction would have a single interval of width at least nine, or two intervals whose total width is at least 16. [Ordinary degree-ten receipt](../results/round17_stable_disproof_ordinary_d10_l20.json) · [Repeated widths](../results/round17_stable_disproof_two_sevens.json) · [Widths six and nine](../results/round17_stable_disproof_six_nine.json) · [Widths seven and eight](../results/round17_stable_disproof_seven_eight.json)

## Ordinary degree-ten length 20

The full unpadded first-arrival corridor ran at radii 10 and 10 to the unordered positive basis. It finished at 22:22 Pacific time after approximately 2 hours and 38 minutes. The native JSON has all eleven layers on each side of every tier. Its midpoint counts agree with the live progress log.

| Magnus degree | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Retained midpoints | 6,254,117 | 100,546,410 | 967,687 | 44,934 | 3,431 | 263 | 0 |

An ordinary path of at most 20 instructions would project to a path in this rank-two degree-ten graph and supply a midpoint. The graph already includes either target order. The empty last tier therefore excludes ordinary length at most 20 for both orders and, by projection, for free words. At stable budget 20, one or two added pairs remain possible under the current exclusions. [Successive corridor method and lower-degree controls](round-08-magnus-distance.md) · [Stable length-19 exclusion](round-10-stable-disproof.md) · [Remaining stable branches](round-11-stable-disproof.md)

The degree-six tiers retain 3,979,918 and 2,760,335 pair incidences summed over their layers. The saved JSON records their counts. A targeted replay of degrees seven through ten would need the actual degree-six tuple layers and their row polynomials, which this run did not serialize.

## Completed two-width-seven comparison

Both intervals must use the residual width-seven templates. The four instructions outside the intervals are idle, and each side of the cut has two of them. All 7,047 marked rules are included, so the test covers two zero increments as well as two equal nonzero increments. The three positions of the two intervals across the cut give the following exact meetings. [Setup and complete table](round-16-stable-disproof.md#two-width-seven-intervals)

| Quotient degree | Both on the basis side | One on each side | Both on the AK(3) side |
| ---: | ---: | ---: | ---: |
| 5 | 3 | 12 | 6 |
| 6 | 0 | 0 | 0 |

The final degree-six boundaries check 355,349,810 and 189,533,785 transitions. Every actual D9 retraction with these widths would give a matching state with its auxiliary markings aligned in D6. Both directions use the full marked rules because reversing a true interval preserves its length and the absence of a shorter idle replacement. Thus the degree-six comparison eliminates the $(7,7)$ case in both the free and degree-ten branches.

## Structured cuts for the next width pairs

The marked comparison can meet within the wider interval, using the residual terminal transitions only for the shorter one. This permits a uniform treatment of widths $(6,9)$ and $(7,8)$. They leave three idle instructions. With $i$ idle instructions on the side of the shorter interval, that side expands $5-i$ active instructions for $(6,9)$ or $4-i$ for $(7,8)$. The opposite half supplies the remaining active depth. For the width-seven shorter interval all 7,047 marked rules remain available. The auxiliary bits are propagated through the wider interval along with the three projected words, and lower quotients permit projected waits and identities. All four splits and both orientations are part of the comparison. [Native structured search](../experiments/round15_stable_disproof_two_widths.cpp)

For $(6,9)$, all eight degree-six comparisons are empty after 714,320,796 streamed moves. Each actual D9 path would meet in the appropriate split and orientation, so the degree-six exclusions rule out the whole pair. [All eight comparisons](../results/round17_stable_disproof_six_nine.json)

For $(7,8)$, the four degree-six comparisons with the shorter interval on the AK(3) side are empty. With that interval on the basis side, the four idle splits give 6, 6, 28 and 8 candidate meetings. Degree seven eliminates all eight comparisons after 724,294,452 streamed moves. This rules out the other remaining pair of total width 15. Earlier rounds excluded total widths 12 through 14. Thus two active intervals consume at least 16 of the 18 effective middle instructions, leaving at most two idle moves. [Degree-six controls and degree-seven exclusions](../results/round17_stable_disproof_seven_eight.json) · [Earlier width pairs](round-16-stable-disproof.md)

## Reproduction

~~~sh
work=/tmp/ac-r17-stable-disproof
mkdir -p "$work"
python3 -B experiments/round16_stable_disproof_two_sevens.py > "$work/two-sevens.txt"
python3 -B experiments/round15_stable_disproof_two_widths.py > "$work/six-seven.txt"
c++ -std=c++17 -O3 experiments/round15_stable_disproof_two_widths.cpp -o "$work/marked-cut"
"$work/marked-cut" 5 --two-sevens < "$work/two-sevens.txt"
"$work/marked-cut" 6 --two-sevens < "$work/two-sevens.txt"
for split in 0 1 2 3
do
  "$work/marked-cut" 6 --structured 6 9 "$split" < "$work/six-seven.txt"
  "$work/marked-cut" 6 --structured 7 8 "$split" < "$work/two-sevens.txt"
  "$work/marked-cut" 7 --structured 7 8 "$split" < "$work/two-sevens.txt"
done
c++ -std=c++17 -O3 experiments/round08_magnus_native_corridor.cpp -o "$work/ordinary-corridor"
"$work/ordinary-corridor" 10 10 10 --first-arrivals --ledger \
  | diff - results/round17_stable_disproof_ordinary_d10_l20.json
~~~
