# Two width-seven intervals and compact degree-five layers

2026-11-19. A length-20 one-padding AK(3) path cannot have two active intervals of widths six and eight in its degree-nine retraction. The complete cut depends on the previously classified width-six interval and an explicit marked search inside the width-eight interval. The ordinary native corridor also has an opt-in compact representation of its degree-five allowable layers. Eight comparisons reproduce every full and partial tier, with the positive ledgers checked by a monomial-set replay. [Structured interval cut](../results/round16_stable_disproof_six_eight.json) · [Compact layout controls](../results/round16_stable_disproof_compact_controls.json)

## Two width-seven intervals

At stable budget 20, the degree-nine one-padding retraction uses 18 effective instructions. If it has two width-seven intervals, the other four instructions are idle. Both intervals must satisfy the unrestricted width-seven strict-replacement test. Shortening either interval would give a path of at most 17 instructions with the other active interval still present, contrary to the length-17 saturation. [Earlier width-seven comparison](round-13-stable-disproof.md#the-isolated-seven-instruction-interval)

The 5,730 width-seven terminals give 7,047 distinct marked rules after tracking the auxiliary bit. There are 1,278 zero-increment rules and 5,769 nonzero-increment rules. Both possible schedules are retained. Two intervals can both have zero auxiliary increment, or they can have equal nonzero increments on the original parity space, since the initial and final active auxiliary markings are zero. The surviving word's mark is the zero-input mark plus the old marking evaluated on its formal old parity. [Complete width-seven rule generator](../experiments/round16_stable_disproof_two_sevens.py) · [Mark transport](round-15-stable-disproof.md#excluding-widths-six-and-seven-together)

Cut after the second idle instruction and test the three possible distributions of the two intervals across the cut. Both boundaries permit reversals of the true intervals, preserve alignment of the old words with the auxiliary bits, and require the signed terminal equality in the current quotient. With both intervals on one side the auxiliary bits must be restored to zero on that side. A degree-five comparison gives 3 middle states with both intervals on the basis side, 12 with one interval on each side and 6 with both intervals on the AK(3) side. The full degree-six comparison was still active at this checkpoint. [Degree-five control](../results/round16_stable_disproof_two_sevens.json)

## A structured width-six and width-eight cut

For a proposed width-six and width-eight pair, place the known marked width-six transition on one side of the cut and meet inside the width-eight interval. For each of the two orders of the intervals and each integer $i$ from zero through four, the side with the width-six transition has $i$ idle instructions and the opposite side has $4-i$. Expand the idle side with its exact transition table. Enter the active half by importing a signed copy of an active row into the projected identity. The mark of the imported copy is one plus its donor's mark. The reversed active half uses the same birth rule for the reverse of the last cancellation. Keep the three old words aligned with their auxiliary bits. At lower degrees an active vertex can project to an identity row or a wait, so the lower comparison permits such vertices and waits. Degree nine can enforce that the interior vertices remain active and all steps are effective.

The two active depths can depend on $i$. The implementation uses $5-i$ and $3+i$, which place more of the interval on the side with fewer short-prefix states. It streams the last boundary instead of storing both complete active halves. [Shared marked search and structured cut](../experiments/round15_stable_disproof_two_widths.cpp)

| Idle instructions on the width-six side | Degree-six meetings, width-six side from AK(3) | Degree-six meetings, width-six side from the basis |
| ---: | ---: | ---: |
| 0 | 0 | 0 |
| 1 | 0 | 0 |
| 2 | 0 | 0 |
| 3 | 0 | 0 |
| 4 | 0 | 1 |

Degree seven excludes the sole remaining split after 58,577,792 and 222,019,224 streamed moves in its two orientations. Any degree-nine candidate would project to a meeting in at least one of these comparisons. Thus widths six and eight cannot occur together. [Exact degree-six and degree-seven receipts](../results/round16_stable_disproof_six_eight.json)

## Compact allowable layers in degree five

The flag `--compact-degree-five` stores each unpadded degree-five layer as slices. A table indexed by the first, smaller row ID gives the offsets of a sorted list of second row IDs. This represents the exact same unordered pair set. It uses four bytes per stored second row plus the offsets, and needs only a binary search inside the relevant slice. A lower-group value first encountered during the new refinement has no stored slice and fails the membership check. The implementation converts and releases each prior hash layer before refining to the first higher-degree stage. [Native corridor](../experiments/round08_magnus_native_corridor.cpp)

In degree five there are at most 524,288 row IDs. At radii ten and ten, the 22 offset arrays therefore need at most 92,274,864 bytes on a 64-bit platform. The remaining capacity is exactly four bytes per stored pair incidence. The controls cover full degree-six length 11 and 12, ordered degree-six length 12, and degree-seven length 14, each with and without partial degree-six refinement. They agree even on the reconstructed native ledgers. [Verified control generator](../experiments/round16_stable_disproof_compact_controls.py)

A resumable checkpoint would additionally store the degree-five polynomial for every interned row ID, both radii and the prior tier receipts. Saving the compact slices alone would lose the ID-to-polynomial map needed to resume in the same group marking. The current implementation uses compact membership for a live refinement. The authorized older ordinary degree-ten run continues separately in degree six.

## Reproduction

~~~sh
work=/tmp/ac-r16-stable-disproof
mkdir -p "$work"
python3 -B experiments/round16_stable_disproof_two_sevens.py > "$work/two-sevens.txt"
python3 -B experiments/round15_stable_disproof_two_widths.py > "$work/six-seven.txt"
c++ -std=c++17 -O3 experiments/round15_stable_disproof_two_widths.cpp -o "$work/marked-cut"
"$work/marked-cut" 5 --two-sevens < "$work/two-sevens.txt"
"$work/marked-cut" 6 --two-sevens < "$work/two-sevens.txt"
for split in 0 1 2 3 4
do
  "$work/marked-cut" 6 --six-eight "$split" < "$work/six-seven.txt"
done
"$work/marked-cut" 7 --six-eight 4 < "$work/six-seven.txt"
c++ -std=c++17 -O3 experiments/round08_magnus_native_corridor.cpp -o "$work/corridor"
python3 -B experiments/round16_stable_disproof_compact_controls.py "$work/corridor" \
  | diff - results/round16_stable_disproof_compact_controls.json
~~~
