# P: independent full cyclic-cap-21/22 closure and primitive-coordinate review

Date: 2026-11-02. **No AC trivialization or global AC obstruction is
established.** The result is a lower bound on the cyclic peak of any
ordinary, unstabilized AC path from the stated AK(3) tuple.

## Result, prior work, and attribution

N generated full finite-neighbor components with cyclic total length at
most 21 and then 22. I read N's current generator and results, the coordinating
agent's independent cap-20 audit, and the shared Cayley-axis completeness
argument before independently choosing a different closed-set checker.
The new checker is written from scratch: it uses its own stack reduction,
Booth minimum-rotation canonicalizer, state validation, complete bridge
menu, and connectedness traversal. It imports no N search code.

**Checked theorem.** Any ordinary AC path from

    (xxxYYYY, xyxYXY)

to the standard free tuple `(x,y)` has cyclic total peak at least **23**.
The same lower bound holds before the first primitive coordinate occurs.
Cyclic total length means the sum of the two freely cyclically reduced
relator lengths. Conjugating tails may be arbitrarily long. This improves
the earlier analytic cyclic lower bound 15 and is a different assertion
from the previously published raw peak bound 22. The cap-21 audit first
gave cyclic peak 22; the separately audited cap-22 extension below improves
it to 23.

N's component enumeration and the discovery of this stronger finite
bound are credited to N. The axes argument was developed jointly in the
N/coordinating-agent/O discussion. P independently checked its constructive
form and both full certificates. The coordinating agent independently
checked cap 20 in Python. O independently supplied an overlapping
Euclidean primitive-coordinate test; P's second implementation was already
underway when the overlap was discovered. These attributions distinguish
independent reviews from independent discoveries.

## Why a finite menu covers all conjugating tails

Each state is a pair of cyclic conjugacy classes of relators, modulo
individual inversion and permutation. Ambient generators are fixed.
Individual relator conjugations and inversions do not change this state.
Every multiplication of two actual independently conjugated relators,
up to simultaneous conjugation, has the form

    u q v q^-1,

where u,v may independently be inverted. Here q is an arbitrary free
word. Work in the Cayley tree of F(x,y). Every nonempty cyclically reduced
word u has an invariant translation axis through the identity, with
translation length |u|. The axis of `q v q^-1` passes through q.

If the axes intersect, choose a common vertex and conjugate the product
to that vertex. Both translations now read cyclic rotations a,b of u,v
(with the chosen signs). The product's cyclic class is therefore
represented by `a b`: this is the zero-tail menu.

If the axes are disjoint, let p and r be the nearest vertices on them,
and let t label the joining geodesic, of length d>=1. Conjugate to p.
The same product is represented by

    a t b t^-1,

where a,b are signed cyclic rotations of u,v. Since the joining geodesic
leaves each axis, none of its four boundaries with the axis translations
cancels, including the cyclic boundary. Its cyclic length is exactly

    |u|+|v|+2d.

If v is retained as donor, write `S=|u|+|v|`. The new pair's cyclic
total is `S+|v|+2d`. Therefore every disjoint-axis neighbor under cap C
has

    1 <= d <= floor((C-S-|v|)/2).

For every state and recipient choice, enumerate all signed rotations a,b,
the empty tail, and every reduced tail through that finite bound when
positive. Reduce/cyclically reduce each product and retain it if its
new pair sum is at most C. This covers **all** conjugating words q,
regardless of their original length. The enumerated menu can include
redundant tails whose axes actually intersect or are closer; they still
give legal multiplication edges. No completeness claim rests on a bound
on the original arbitrary q.

All menu edges are actual AC operations: put the entries into the chosen
signed conjugate representatives, multiply, and restore the donor.
Conjugating a relator changes no cyclic length. Inversion and permutation
normalization are bookkeeping for the cyclic states; the lower bound
also holds if one treats this as a graph allowing additional free
permutations. Thus a closed set containing the initial cyclic state and
excluding the basis state rules out every ordinary path staying under C.

Empty coordinates would require separate treatment in a generic graph.
The checked component has no empty coordinate (minimum length five),
and every admitted neighbor is checked for actual membership, so no
empty-neighbor omission occurs here. The code can canonicalize an empty
product; it would fail closure if such an unlisted neighbor appeared.

## Independent constructive controls for the axes reduction

The separate `bridge_menu_controls.py` does not import N's generator.
It locates the axis intersections with the path labeled q by matching
periodic prefixes: let l be the longest prefix of q following either
direction of u's periodic axis, and r the longest prefix of q^-1
following either direction of v's periodic axis. The distance between
the axes is `max(0,|q|-l-r)`.

If the prefixes overlap, their common vertex gives two literal cyclic
rotations. Otherwise the intervening substring is the geodesic bridge.
The program constructs the rotations and bridge, checks the original
and reconstructed product as exact free cyclic words, and verifies the
sum-plus-twice-distance length identity in every disjoint case.

Eight control pairs include AK(3), P's length-14 waypoint, N's length-13
waypoint, single generators, proper powers, coincident axes, and a
commutator. With all reduced q through length six and all four sign
choices, **46,624** literal products pass: 1,528 intersecting cases and
45,096 disjoint cases, with distance up to six. These are controls for
the formulas; the unbounded completeness proof is the geometric argument
above.

## Exact cap-21 closed-set audit

The decoded JSON certificate has SHA-256

    0e3e4b99edd9c2f784f9e705826461705ec7e194749d0a93e4bca40ebd5464aa

and 4,100,882 bytes. A format-only Python adapter converts its explicit
state pairs to TSV; the C++ checker validates the actual states and
recomputes every mathematical property independently.

| Verified property | Exact result |
|---|---:|
| Distinct canonical states | 144,292 |
| Signed rotation/bridge candidates checked | 103,553,312 |
| Admitted directed neighbor checks | 5,544,208 |
| Positive-tail candidates checked and admitted | 13,824 |
| Maximum geodesic bridge length needed | 1 |
| Minimum cyclic total length | 13 |
| Minimum individual cyclic length | 5 |
| Minimum possible disjoint-axis neighbor sum | 21 |

The checker validates every source word's alphabet, free cyclic reduction,
inversion/rotation representative, pair order, uniqueness, and cap. It
verifies the initial state is present and the standard basis absent.
Every admitted neighbor must be present. A second traversal of the
checked adjacency graph reaches **every** state from the initial state,
so the catalogue is connected as well as closed.

Booth's independent canonicalizer is compared with exhaustive rotation
enumeration on all freely reduced words through length seven, including
periodic words and cyclic cancellation. This is a convention check; the
closed-set audit then recomputes all 103 million candidate products.

The state histogram by cyclic sum is:

    13:12, 14:40, 15:548, 16:572, 17:3108,
    18:3488, 19:17688, 20:18792, 21:100044.

## Independent primitive-coordinate check

The catalogue has **99,546** distinct cyclic coordinates. P's separate
`scan_cyclic_primitives.py` uses Nielsen's rank-two uniqueness theorem,
not Whitehead descent: for a coprime exponent vector, construct its
positive primitive representative by Euclidean induction, change signs,
then compare cyclic words. A word is primitive exactly when it is a
rotation of that representative or its inverse. Noncoprime vectors are
rejected immediately. The construction is by free-group automorphisms,
so the test is an equivalence, not merely a necessary pattern condition.
See the proof and primary Nielsen source in [P's earlier report](research-p.md).

No coordinate is primitive. The implementation reproduces the exact
counts `4 L phi(L)` of literal cyclically reduced primitive words at
lengths two through nine (and four at length one). Its optional comparison
also agrees with M's separate Whitehead-descent test on **every** catalogue
coordinate. O independently performed the same style of Euclidean
review. Consequently the closed-set bound applies before any primitive
coordinate, not just before the standard basis.

This does not assert that every subgroup represented in the component
contains no hidden primitive element after arbitrary Nielsen operations
outside the cyclic cap. The theorem constrains the stated cap along the
whole ordinary path.

## Subsequent full cap-22 extension

After the cap-21 review passed, N completed the full cap-22 generator.
P reran the same adaptive independent checker on the new explicit set,
without changing its arithmetic or neighbor rules. It again passes
closure and connectedness. The decoded JSON SHA-256 is

    2c8d0ac4c58f590de7151eae3dd09577d2365bf0e858887d801ce24c5c609c8e

| Verified cap-22 property | Exact result |
|---|---:|
| Distinct canonical states | 258,032 |
| Full signed rotation/bridge candidates checked | 193,140,064 |
| Admitted directed neighbor checks | 10,204,280 |
| Positive-tail candidates checked and admitted | 50,688 |
| Maximum geodesic bridge length needed | 1 |
| Minimum cyclic total / coordinate length | 13 / 5 |
| Distinct cyclic coordinates independently scanned | 179,630 |
| Primitive coordinates | 0 |

Every state is reached by the independently checked adjacency traversal
from the original AK(3) class. The cap-22 histogram is

    13:12, 14:40, 15:548, 16:572, 17:3132,
    18:3592, 19:18176, 20:19472, 21:103432, 22:109056.

Thus no ordinary path with cyclic peak at most 22 can reach a primitive
coordinate, in particular the standard basis. This proves the stated
lower bound **23**. The primitive scan uses the same independent Euclidean
algorithm; its cap-22 run did not repeat the optional M Whitehead
comparison, which had already agreed on every cap-21 coordinate.

## Reproduce

Use N's [compressed explicit catalogue](../certificates/cyclic21_component.json.gz.b64).
The adapter and primitive scanner accept decoded JSON, gzip/base64, or
N's split-part manifest directly. Manifest loading verifies every part
hash and both assembled/decoded hashes and byte counts. The adapter prints
both source and TSV hashes. All Python tools use only the standard library.

```sh
python3 experiments/cyclic_catalogue_to_tsv.py \
  certificates/cyclic21_component.json.gz.b64 /tmp/cyclic21.tsv
c++ -std=c++17 -O3 experiments/verify_full_cyclic_component.cpp \
  -o /tmp/verify_full_cyclic_component
/tmp/verify_full_cyclic_component /tmp/cyclic21.tsv 21 /tmp/cyclic21-review.json
python3 experiments/bridge_menu_controls.py --output /tmp/bridge-controls.json
python3 experiments/scan_cyclic_primitives.py \
  certificates/cyclic21_component.json.gz.b64 \
  --crosscheck-directory experiments --output /tmp/cyclic21-primitives.json
```

The checked results are [closure/connectivity](../results/cyclic21_independent_review.json),
[bridge controls](../results/bridge_menu_control_results.json), and
[primitive coordinates](../results/cyclic21_primitive_independent_review.json).
For cap 22, pass N's
[cap-22 manifest](../certificates/cyclic22_component_manifest.json)
directly to the adapter and primitive scanner, pass 22 to the C++ checker,
and compare the
[cap-22 closure result](../results/cyclic22_independent_review.json) and
[primitive scan](../results/cyclic22_primitive_independent_review.json).
Both catalogues are N's output; this report supplies an independent
audit and explains why an infinite choice of conjugating tails is covered.
Higher cyclic peaks remain available, and AK(3)'s unrestricted AC status
is still undecided by these results.
