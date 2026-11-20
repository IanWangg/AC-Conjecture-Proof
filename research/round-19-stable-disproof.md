# The one-padding branch has a single active interval

2026-11-19. A length-20 one-padding path for AK(3) would have exactly one active interval in its degree-nine retraction, of width at least nine. The last two-interval schedule, $(9,9)$, is excluded by degree six plus a single degree-seven coefficient. In the two-padding branch, the long four-active interval is already necessary in degree eight. [Two width-nine intervals](../results/round19_stable_disproof_two_nines.json) · [Independent lift](../results/round19_stable_disproof_targeted_nines.json) · [One-coordinate exclusion](../results/round19_stable_disproof_nines_one_coordinate.json) · [Degree-eight saturation](../results/round19_stable_disproof_two_padding_d8.json)

## Moving an instruction across birth or death

Round eighteen leaves $(9,9)$ as the only possible two-interval schedule, with no idle instructions. At birth let $j$ be the spare, $a$ the donor and $b$ the other active row. The first internal instruction can be moved before the birth if it acts on $b$ without taking $j$ as its donor. The two instructions then commute because the birth changes only $j$ and reads only $a$. If the first internal instruction instead inverts $a$, it can move before the birth by reversing the sign of the birth product. In both cases the move before birth stays idle, the boundary after both instructions has the same tuple, and the length of the active interval drops by one. Reverse the same argument to move a last internal instruction past death. Any such move in a genuine $(9,9)$ path would give the already excluded $(8,9)$ schedule. [Prior exclusion](round-18-stable-disproof.md#a-cut-inside-the-wider-interval)

## Closing the two width-nine intervals

Apply the pruning to the labelled first and last internal instructions on both sides. Each side begins at its own marked endpoint, with zero auxiliary coefficients on the original rows and coefficient one on the spare. The projected end of an interval comes from killing one of two equal old words up to sign. Their auxiliary bits must differ, so after the kill the erased row has coefficient one. Compare both surviving old words with their auxiliary bits. All internal moves preserve the joint row alignment. Projected identities and waits inside the lower-degree interval are permitted. The boundary prune uses the labelled operations even when those operations have a trivial lower image.

| Comparison | Marked middle pairs |
| --- | ---: |
| Degree six, direct | 45 |
| Degree six, commutation pruning | 8 |
| Degree seven, commutation pruning | 0 |

After the depth-seven active layers the last internal move is streamed, and the surviving signed duplicates are tested for a permitted return. The degree-seven run checks 1,353,569,743 and 297,290,238 such moves after the parity screen. The complete degree-six cut stores the eight marked pairs as exact polynomials. [Native marked cut](../experiments/round19_stable_disproof_two_nines.cpp)

An independent implementation uses those eight degree-six pairs as the only possible midpoints. For each pair and each side it builds a small degree-six corridor with a four-step prefix and a five-step reversed suffix. It trims to their intersections and evaluates the resulting aligned paths in degree seven using Python polynomial arithmetic. Each of the eight pairs permits one degree-seven return from each side, and the two returns are different in all eight cases. This gives a separate check from the full native degree-seven search after the saved degree-six cut. [Targeted lift and saved coordinates](../experiments/round19_stable_disproof_targeted_nines.py)

Matching the two rows by their degree-six values and marks identifies the same four differing degree-seven coordinates in all eight comparisons. They include lexicographic index 31, the coefficient of $X^2Y^5$. Run the targeted search again in the quotient retaining all degrees through six and just this coordinate at degree seven. All discarded top-degree terms form an ideal because multiplication by a positive-degree term annihilates them. This run tests the terminal equalities directly in the smaller quotient. The two sides still each give one return for each of the eight pairs, and the returns disagree in every case. Thus one extra coefficient over degree six suffices. [Full degree-seven coordinates](../results/round19_stable_disproof_targeted_nines.json) · [One-coordinate quotient](../results/round19_stable_disproof_nines_one_coordinate.json)

## The remaining isolated interval

In a sole-interval candidate of width $s$, the outside $18-s$ effective instructions act only on the original two rows. At the entry and return the erased row is literal $z$ in the full marking, and the two surviving words use only the original generators. Any rank-two degree-ten replacement of the interval by at most $s+2$ instructions would give an ordinary path of length at most 20. Hence the entry and return pairs of a genuine sole interval would themselves need ordinary distance at least $s+3$ in degree ten. This necessary condition also holds for a free-word candidate by projection. [Ordinary length-20 exclusion](round-17-stable-disproof.md#ordinary-degree-ten-length-20)

## The long four-active interval in degree eight

The earlier exact one-spare degree-eight corridor at middle budget 16 has widths

~~~text
1 1 1 1 1 1 2 2 2 1 1 1 2 2 1 1 1
~~~

Replay the unpadded 16-instruction witness, independently verified with monomial sets. Between already witnessed layers enumerate bridges of lengths two, three and four until their penultimate layers stop growing. Appending an identity embeds each witnessed pair in the known one-spare corridor. The ordinary witnesses attain all 22 incidences, so every one-spare corridor vertex is idle. [Exact degree-eight saturation](../experiments/round19_stable_disproof_two_padding_d8.py) · [Earlier complete one-spare counts](round-09-stable-disproof.md)

In the two-padding branch at budget 20 the degree-eight erasure of both variables has 16 effective moves, since the shorter budget 15 is excluded. The first product from an original row into an auxiliary row gives three nonidentity rows. If every four-active interval were of width at most four, replace each by an idle path of no greater length using the short-interval replacement proof. The modified path stays at three or fewer nonidentity rows and retains a three-active vertex. Delete one identity at each vertex to obtain a one-spare path within budget 16 in degree eight. Its three-active vertex contradicts the saturation. Thus the degree-eight retraction itself needs at least one four-active interval of width five or more. This is a necessary condition on the two-padding branch. [Short replacements and identity deletion](round-12-stable-disproof.md#four-active-windows-with-two-added-pairs)

## Reproduction

~~~sh
work=/tmp/ac-r19-stable-disproof
mkdir -p "$work"
c++ -std=c++17 -O3 experiments/round19_stable_disproof_two_nines.cpp -o "$work/two-nines"
"$work/two-nines" 6 --unpruned
"$work/two-nines" 6
"$work/two-nines" 7
python3 -B experiments/round19_stable_disproof_targeted_nines.py results/round19_stable_disproof_two_nines.json \
  | diff - results/round19_stable_disproof_targeted_nines.json
python3 -B experiments/round19_stable_disproof_targeted_nines.py results/round19_stable_disproof_two_nines.json \
  --top-coordinate 31 | diff - results/round19_stable_disproof_nines_one_coordinate.json
python3 -B experiments/round19_stable_disproof_two_padding_d8.py \
  | diff - results/round19_stable_disproof_two_padding_d8.json
~~~
