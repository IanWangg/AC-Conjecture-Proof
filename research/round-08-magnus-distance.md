# Degree-ten exclusion and native successive quotient checks

2026-11-19. In the degree-ten characteristic-two Magnus quotient, the ordinary instruction distance of AK(3) is at least **19** for both target orders. The stable distance is at least **18**. A stable path of length 18 could use only one added pair. Every shortest stable path of degree-nine length 17 has rank two throughout.

## Excluding stable length 17 in degree ten

The unordered rank-two degree-ten search exhausts disjoint balls of radii eight and nine, with 93,684,380 and 191,338,037 tuples. This excludes any ordinary length-17 path, with either target order. For a shortest stable path of length at most 17, the peak-rank cutoff leaves at most four added pairs. The rank-two erasures in degrees seven, six and five exclude two, three and four extra pairs at their respective middle budgets 13, 11 and 9. [Degree-ten direct audit](../results/round08_magnus_d10_L17.json), [round-seven padded exclusions](round-07-stable-disproof.md).

For one added pair, the new native search excludes the rank-two degree-eight retraction at middle budget 15. It checks 707,644,692 final boundary transitions against the complete opposite ball. The boundary-only option omits storage of the newly queried states, preserving the full intersection test. This closes the positive-padding cases and carries to degrees nine and ten by projection. In particular every degree-nine shortest stable path to either target order, of length exactly 17, already stays at rank two. [One-padding exclusion](../results/round08_magnus_d8_one_padding_L15.json), [degree-nine exact paths](round-07-native-distances.md).

## Native successive quotient search

The C++ solver uses the [successive corridor principle](round-06-stable-disproof.md) with exact rank-two coefficient arithmetic. It builds two complete degree-four balls, intersects the midpoint sets and restricts each side to states that are reachable by the required tick and can still reach the midpoint. Each next degree lifts just those projected layers, including waits. Intersect and trim each new set before advancing. At the last tier the solver can preserve the marked row order and allow row swaps as explicit instructions.

The low layers use unsigned row-permutation orbits. Every high instruction projects to an instruction or a wait. Therefore every path of length at most the total radius survives the projected tests. Each retained final midpoint instead comes from two actual full-degree paths whose concatenation proves the upper bound. Neither the arithmetic nor the row lookup uses a probabilistic fingerprint. The caches store complete element IDs.

At degree six the native method independently excludes radius 11 and reaches a basis at total radius 12. The complete middle-set counts by tier are $855,22,0$ and $5430,179,1$ respectively. The 12-instruction path reconstructed from the positive midpoint passes separate monomial-set replay. [Native controls](../results/round08_magnus_native_corridor_controls.json), [independent positive replay](../results/round08_magnus_native_corridor_control_witness.json).

At total radius 18 with radii nine and nine, the midpoint counts at degrees four through ten are **5,016,291, 3,666,195, 55,422, 2,715, 166, 6 and 0**. Ordinary paths of length 18 are therefore excluded. The rank-two erasures of paths with two, three or four padded pairs are also excluded at their respective middle budgets. The earlier cut bound excludes five or more. A possible stable path of length 18 therefore needs exactly one padded pair, whose middle budget is 16. [Full tier and layer counts](../results/round08_magnus_d10_L18_corridor.json), [positive-padding cases](round-08-stable-disproof.md).

~~~sh
mkdir -p /tmp/ac-r08-magnus
c++ -std=c++17 -O3 experiments/round07_magnus_native.cpp -o /tmp/ac-r08-magnus/native
/tmp/ac-r08-magnus/native 10 0 17
/tmp/ac-r08-magnus/native 8 1 15 --boundary-only
c++ -std=c++17 -O3 experiments/round08_magnus_native_corridor.cpp -o /tmp/ac-r08-magnus/corridor
/tmp/ac-r08-magnus/corridor 6 5 6
/tmp/ac-r08-magnus/corridor 6 6 6 > /tmp/ac-r08-magnus/control6-L12.json
python3 -B experiments/round07_magnus_witness.py /tmp/ac-r08-magnus/control6-L12.json \
  | diff - results/round08_magnus_native_corridor_control_witness.json
/tmp/ac-r08-magnus/corridor 10 9 9
~~~
