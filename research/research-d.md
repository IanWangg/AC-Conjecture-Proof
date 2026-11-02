# Research D: an exact raw elementary peak exclusion for AK(3)

Date: 2026-11-02. Status: computer-assisted finite exclusion with two independently implemented exhaustive searches. **No AC trivialization or counterexample is proved. No novelty claim is made.**

## Previous work read before choosing a direction

I read the target repository's research C note and its exact MS-to-AK certificate, research B's quotient certificates and metric proposition, research A's free-product plateau proof and verifier, and Panteleev–Ushakov's primary [paper](https://arxiv.org/html/1609.00325v1), particularly its definitions of ordinary AC and quotient-conjugacy moves. I also reviewed Carreras's [certificate paper](https://arxiv.org/html/2607.23611v1), which explicitly separates restricted substitution-graph bounds from ordinary elementary peak bounds.

I independently chose to investigate a different, precisely finite question: can AK(3) leave its initial length plateau while *every raw freely reduced elementary state* has small total length? Unlike a cyclically normalized GS search, this graph retains all conjugating prefixes and allows all elementary multiplication moves.

## Checked result

For the starting ordered pair

    (xxxYYYY, xyxYXY),  where X=x^-1 and Y=y^-1,

the entire elementary AC component with **raw freely reduced total length at most 18** has been exhausted. It contains no tuple of length below 13, and in particular no standard tuple `(x,y)`.

Consequently every ordinary AC trivialization of AK(3), if one exists, must have a raw freely reduced state of total length **at least 19**. This is a lower bound for raw word length along a path. It is **not** a lower bound of 19 for cyclically reduced energy, a GS-graph bound, a move-count bound, or an obstruction to arbitrary high-peak paths.

The two independently implemented searches agree on all projected counts. The direct unquotiented implementation exhausts **2,014,992 ordered, oriented raw states**. Its projection under individual relator inversions and relator interchange contains **251,874 states**.

| Raw total length | Projected state count |
|---:|---:|
| 13 | 252 |
| 14 | 588 |
| 15 | 11,984 |
| 16 | 12,810 |
| 17 | 114,440 |
| 18 | 111,800 |
| **Total** | **251,874** |

This is a completed finite graph search, rather than a budget-terminated failure. The distinct cap-19 search mentioned below was incomplete and supplies no further exclusion.

## Exact move set and why it covers ordinary AC paths

The direct C++ search uses precisely these moves, with free reduction after each move:

1. Invert either relator.
2. Right multiply either relator by the other relator, positively.
3. Conjugate either relator by any one of `x,X,y,Y`.

The convention for conjugation is `r -> g r g^-1`. Choosing the opposite convention gives the same move set because inverse generators are present. No stabilization, generator changes, quotient identities, cyclic reduction, or canonical rotations are applied in this search.

These generator conjugations also suffice when the ordinary AC definition permits conjugation by an arbitrary word in one step. More precisely, any conjugation from raw word u to raw word v can be refined into single-generator conjugations without exceeding `max(|u|,|v|)`: first cyclically reduce u by removing its conjugating prefix, rotate the cyclic core into the core of v, and then regrow the conjugating prefix of v. Removing a prefix decreases length by two per letter. Cyclic rotation is a generator conjugation with cancellation and preserves length. Regrowing the target prefix increases length monotonically up to |v|. This is the usual cyclic-word characterization of conjugacy in a free group. Thus an arbitrary-word-conjugation path with raw peak at most 18 would yield a path in the searched graph at the same peak.

Multiplication by an inverse donor is also covered without increasing peak: invert the donor, positively multiply the recipient, and invert the donor back. A left multiplication is the inverse of a suitable right multiplication of inverse relators, with intermediate inversions preserving lengths. Relator order has no bearing on reaching a trivial presentation; the direct search nonetheless retains order and finds neither the exact standard endpoint nor any shorter pair.

## Search completeness and independent implementation

The raw words at bounded total length form a finite set. Every visited state emits **every** permitted primitive successor that stays inside the cap. Breadth-first search terminates only when its pending queue is empty. Therefore the final visited set is exactly the reachable component in the induced finite graph. The minimum energy calculation checks every state in this component.

`experiments/raw_peak_independent.cpp` implements this argument directly with ordered pairs of oriented strings. It uses only positive multiplication and the strict elementary moves listed above. It performs no search-state quotient. Each state is serialized as `first|second`, and the separator is excluded from length calculations. Its completed cap-18 output is:

```json
{"cap":18,"raw_ordered_oriented_states":2014992,"projected_states":251874,"minimum_total_length":13,"target_reached":false,"energy_counts":{"13":252,"14":588,"15":11984,"16":12810,"17":114440,"18":111800}}
```

The separately written Python implementation, `experiments/raw_peak_search.py`, uses a smaller exact quotient under individual relator inversions and relator permutation. Its canonicalization is only

    sort(min(r0,inverse(r0)), min(r1,inverse(r1))).

It does **not** quotient by cyclic rotation, conjugacy, or any ambient free-group automorphism. To avoid losing outgoing moves after choosing an orientation, it emits products `r_i^epsilon r_j^delta` for **both** signs of the recipient and donor. Both recipient orientations matter: using only a positively oriented recipient would omit left-multiplication successors and make the purported exhaustion incomplete. It also emits all four signed generator conjugations for either coordinate. A local self-test independently compares this neighbor formula with primitive successors from all inversion/permutation representatives.

The C++ implementation shares no neighbor-generation or word-reduction code with the Python implementation. After completing its original-state search, it independently projects its final state set and obtains exactly the Python count and energy histogram. This cross-check tests both the quotient treatment and the restricted move generator concern that can invalidate cyclic-normal-form search claims.

## Calibration and bounded runs

The following runs were completed during this investigation. A target-discovery run stops as soon as a standard pair is processed; its discovered count is therefore a partial component size, not an exhaustive count.

| Presentation | Cap | Result | Projected states discovered |
|---|---:|---|---:|
| AK(2) | 12 | complete component; minimum length 11; no target | 335 |
| AK(2) | 13 | target reached | 19,619 before early termination |
| AK(3) | 15 | complete component; minimum length 13 | 1,716 |
| AK(3) | 16 | complete component; minimum length 13 | 2,570 |
| AK(3) | 17 | complete component; minimum length 13 | 107,226 |
| AK(3) | 18 | complete component; minimum length 13 | 251,874 |

AK(2)'s known raw elementary bottleneck 13 is thus recovered as a positive and negative calibration. The first three small-cap AK(3) counts are secondary checks; the independent original-state C++ cross-check was carried out at cap 18, which subsumes their exclusion conclusions.

A separate AK(3), cap-19 run stopped at its **1,000,001-state discovery budget**, after processing 928,497 states. It had not found a target, but the pending queue was nonempty. It proves no cap-19 exclusion. The next length level remains unclassified by these artifacts.

## Reproduce

From the repository root:

```sh
python3 experiments/raw_peak_search.py --selftest --n 3 --cap 18
c++ -std=c++17 -O2 experiments/raw_peak_independent.cpp -o /tmp/ac_raw_peak_check
/tmp/ac_raw_peak_check 18
python3 experiments/raw_peak_search.py --n 2 --cap 12
python3 experiments/raw_peak_search.py --n 2 --cap 13
```

Python requires only its standard library; C++ requires a C++17 compiler and its standard library. `results/raw_peak_results.json` records the six Python calibration and exclusion runs, including run timings. These counts are reproducible checks, not a formal proof-assistant certificate.

## Insight and remaining problem

The initial nonincreasing plateau is surrounded by a small but genuine neighborhood of elementary length excursions that returns only to length 13. Even allowing every raw state through length 18 does not produce a shorter presentation. This provides a rigorously scoped baseline for testing future search tools and purported low-peak trivializations.

It supplies no invariant at unbounded length and does not support a claim that AK(3) is non-AC-trivial. Any successful path can exceed the finite cap. A future computation can classify cap 19 or use its boundary states as certified launch points; a genuine breakthrough still needs a complete trivialization certificate or a global obstruction.
