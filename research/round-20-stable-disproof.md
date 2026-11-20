# One outer active interval after two-padding normalization

2026-11-19. At stable budget 20, the degree-eight erasure of a two-padding AK(3) candidate can be normalized to have exactly one maximal interval away from two nonidentity rows. That interval contains every remaining four-active block. At least one such block has width five or greater. [Exact occupation cuts](../results/round20_stable_disproof_two_outer.json) · [Independent control](../results/round20_stable_disproof_two_outer_control.json)

## Normalizing the degree-eight erasure

Erase both auxiliary letters, keeping four row slots at characteristic-two Magnus degree eight. There are exactly 16 effective middle instructions because the four-slot budget 15 is excluded. At least two rows are nonidentity at every vertex, since the relator linear parts have rank two. Call a vertex idle when exactly two rows are nonidentity. An outer active interval runs from an idle vertex to its first subsequent idle vertex. It can contain four-active blocks, each starting with a crossing from three to four nonidentity rows and ending at its first return to three.

First replace each four-active block of width at most four by its three-slot replacement. Then replace each outer active interval of width at most six. Such an interval can no longer contain a four-active block, which would have width at least five plus two additional outer crossings. Use the rank-two replacement for a three-active interval of width at most six. Its incoming nonidentity rows have independent linear parts, as required by that replacement. All replacements preserve length, since a saving would give a degree-eight path within budget 15. The graph has unordered rows, so adjoining identity slots preserves each replacement edge. [Four-slot budget-15 exclusion](round-09-stable-disproof.md) · [Both local replacement results](round-12-stable-disproof.md)

Some four-active block must remain. The original degree-eight erasure has a three-active vertex at its first outward crossing. If every original four-active block were short, replacing just those blocks would retain a three-active vertex while reducing the path to a one-spare length-16 path. The complete one-spare degree-eight corridor has only idle vertices. Thus some original four-active block has width at least five, and neither normalization step removes it. [Complete length-16 one-spare saturation](round-19-stable-disproof.md#the-long-four-active-interval-in-degree-eight)

After normalization the outer widths are at least seven. Two outer intervals would have widths `(7,7)`, `(7,8)`, `(7,9)` or `(8,8)` up to reversal. Each can contain at most one four-active block, because two such blocks inside the same outer interval require at least 12 instructions. In the two-outer comparison allow the outer interval on either side to stay at three active rows and require a four-active block on at least one side.

## Exact cuts in degree eight

Use the same-degree four-slot group for every transition. In an upward crossing one identity row takes a signed copy of a nonidentity donor. In a downward crossing one row is cancelled by a surviving donor equal to it up to sign. For unchanged occupation enumerate the ordinary inversions, signed right products and single-letter conjugations, rejecting unchanged rows and identities. Sort the four rows after each edge.

For each orientation and placement of idle instructions, expand the two outer intervals from opposite endpoints. A width-$s$ outer interval with a width-$q$ four-active block uses an outer birth and death, $q$ instructions in the block, and $s-q-2$ three-active instructions before or after the block. Explicitly enumerate all these lengths and placements to obtain the idle boundary sets. For the comparison in which just one side has a four-active block, advance its idle boundary through the intervening idle steps and read the other side's outer death backwards. Meet inside that side's three-active interval, always expanding the smaller current layer. When both sides have four-active blocks, carry one idle boundary through the intervening idle steps and intersect the two idle sets.

| Outer widths | Idle placements and orientations | Nonempty cuts |
| --- | ---: | ---: |
| `(7,7)` | 6 | 0 |
| `(7,8)` | 6 | 0 |
| `(7,9)` | 2 | 0 |
| `(8,8)` | 1 | 0 |

The native degree-three `(8,8)` run yields positive controls in all three interval-type combinations. An independent Python enumeration using the general ordinary neighbor generator yields boundary intersection counts 787, 907 and 275, with 921 and 792 four-active return pairs. The native test counts active midpoints for its first two combinations and idle boundaries in its third, so the first two positive counts refer to different vertices. In degree eight every comparison is empty. [Native search](../experiments/round20_stable_disproof_two_outer.cpp) · [Independent occupation enumeration](../experiments/round20_stable_disproof_two_outer_control.py)

The conclusion applies to the normalized degree-eight path because replacements can change the original two-auxiliary lift. The still-possible cases are one outer interval with one or two four-active blocks, and the separate one-padding branch. The ordinary lower bound remains 21 and the stable lower bound remains 20. [Ordinary degree-ten bound](round-17-stable-disproof.md#ordinary-degree-ten-length-20) · [One-padding restriction](round-19-stable-disproof.md#the-remaining-isolated-interval)

## Reproduction

~~~sh
work=/tmp/ac-r20-stable-disproof
mkdir -p "$work"
c++ -std=c++17 -O3 -Wall -Wextra experiments/round20_stable_disproof_two_outer.cpp -o "$work/two-outer"
for degree in 3 8
do
  "$work/two-outer" "$degree" 7 7
  "$work/two-outer" "$degree" 7 8
  "$work/two-outer" "$degree" 7 9
  "$work/two-outer" "$degree" 8 8
done
"$work/two-outer" 3 8 8 | python3 -B experiments/round20_stable_disproof_two_outer_control.py \
  | diff - results/round20_stable_disproof_two_outer_control.json
~~~
