# Research T: independent initial-subgroup basis coverage and witness compilation

Date: 2026-11-02. **AK(3) and the ordinary, unstabilized Andrews–Curtis
conjecture remain unresolved.** No novelty claim is made.

The concrete results are an independent finite enumeration of all relevant
initial-subgroup basis classes through cyclic energy 250, an exact audit of
V's actual source words, and a constructive hidden-primitive-to-AC pipeline
calibrated on AK(2). The calibration finishes at the literal pair `(x,y)`;
it is not an AK(3) certificate.

## Prior reading and independent direction

Before choosing a direction I fetched the private repository README and
read the root cyclic-sublevel lemma, Q's arbitrary-tail work, R's exact
primitive detector and reverse-subgroup follow-up, and their supporting
artifacts. The earlier work excludes every arbitrary-tail subgroup of
the complete cap-22 component from containing an ambient primitive.
Longer Nielsen excursions inside one such subgroup cannot help, but a
later independent conjugation can change the subgroup.

I independently chose the following next phase pattern: start from the
original AK subgroup, take an arbitrary Nielsen basis, independently
conjugate its two members, and then seek an ambient primitive in the
resulting subgroup. V independently chose the same direction. We divided
the work: V retained literal raw basis words and scanned all final
rotations; T independently enumerated exponent matrices, checked every
raw source derivation, and built the positive-witness compiler. U supplied
an explicit uniform theta decomposition and independently implemented the
exact primitive detector. The root continued a separate search with
repeated subgroup changes.

## 1. A length formula for the original subgroup

Use capital letters for inverses. Put

```
p_n = x^n Y^(n+1),    b = xyxYXY,    H_n = <p_n,b>,    n >= 2.
```

U observed the following explicit immersed theta graph. Simultaneous
conjugation by `Y` turns the displayed basis into

```
p'_n = Y x^n Y^n = P Q^-1,
b'   = YxyxYX   = P R^-1,
P = Yx,    Q = y^n X^(n-1),    R = xyXY.
```

The three branch paths have lengths `2,2n-1,4`. Their first letters at one
branch vertex are `Y,y,x`; the first letters of their inverses at the
other are `X,x,y`. Their interiors are taken disjoint. The graph is thus
folded and immersed, and its fundamental group has the displayed free
basis. This also verifies that the abstract basis coordinates used below
really are coordinates in `H_n`.

For a primitive conjugacy class in this abstract rank-two free group,
with relatively prime exponent coordinates `(a,b)`, its ambient cyclic
length is

```
F_n(a,b) = 2|a+b| + (2n-1)|a| + 4|b|.                 (1)
```

Here “primitive” refers first to the abstract subgroup basis. It does
not assert ambient primitivity. Formula (1) also does not apply to
arbitrary nonprimitive words with the same exponent vector.

One way to count is to use signed Euclidean primitive representatives.
For equal signs, the positive representative uses `|a|` copies of
`P Q^-1` and `|b|` copies of `P R^-1`, with no path cancellation. For
opposite signs and `a >= -b >= 0`, change basis to
`(A,A B^-1)`, where `A=P Q^-1`, `B=P R^-1`. The new nonnegative
coordinates are `(a+b,-b)`. After conjugating by `P^-1`, the basis
becomes `(Q^-1 P,Q^-1 R)`. Its positive words have path length
`(2n-1)a + 2(a+b) + 4(-b)`. The other opposite cone is symmetric.
These give (1). Every primitive class with the same exponent coordinates
is conjugate to the Euclidean representative, so its ambient cyclic
length is the same. The primitive conjugacy uniqueness and Euclidean
construction are classical; see
[Clay–Conant–Ramasubramanian, Corollary 4.4 and Theorem 4.6](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf).

Writing the absolute coordinates as `(alpha,beta)`, the cone formulas are

| Signs and region | `F_n` |
| --- | --- |
| Same signs | `(2n+1)alpha + 6beta` |
| Opposite signs, `alpha >= beta` | `(2n+1)alpha + 2beta` |
| Opposite signs, `beta >= alpha` | `(2n-3)alpha + 6beta` |

For `n>=2`, every coefficient is positive. In each signed orthant,
increasing either absolute coordinate strictly increases `F_n`.
Consequently each positive Farey update strictly increases total cyclic
basis energy. Pruning at an energy cap is sound for this initial
subgroup. The argument does not justify the same pruning for `n=1`.

## 2. Complete coverage without relying on the Farey program

Modulo independent coordinate inversion and interchange, every basis
cyclic-class pair of `H_n` is represented by a nonnegative unimodular
matrix in one of the four signed orthants. To see this, orient each
column so its first coordinate is nonnegative. If both first coordinates
are positive and the second coordinates have strictly opposite signs,
the absolute determinant is at least the sum of the first coordinates,
hence at least two. This is impossible for a basis. A vertical column
can be flipped to match the other column's second-coordinate sign.
The axis case is immediate.

For nonnegative unimodular columns, either one componentwise dominates
the other or the columns are the two axis vectors. Indeed, strictly
crossing positive columns have absolute determinant at least two;
if one crossed coordinate is zero, determinant one forces the axis
case. Repeatedly subtract the dominated column from the dominating one.
The sum of entries decreases and the determinant remains a unit, so the
process ends at the axes. Reversing it gives positive updates

```
L: (u,v) -> (u,u v),       R: (u,v) -> (u v,v).
```

Every basis maps to a unimodular matrix. Conversely each such matrix
has a free-basis lift by the preceding Euclidean construction. Primitive
conjugacy uniqueness identifies the individual classes of any other
basis with those of this lift. This covers pairs of classes; it does
not claim that arbitrary separately chosen primitive representatives
with unimodular vectors jointly form a literal basis.

T's implementation does not traverse V's L/R tree. It directly lists
projective coprime vectors with

```
a > 0, or a = 0 and b > 0,
F_n(a,b) <= C - s_n,       s_n = min(2n+1,6),
|a| <= floor((C-s_n)/(2n-1)),
|b| <= floor((C-s_n)/4).
```

It then lists unordered determinant-unit vector pairs whose summed
`F_n` is at most `C`. For every vector it separately constructs a signed
Euclidean primitive word, substitutes the literal AK words, and checks
its cyclic length against (1). It canonicalizes each image only for the
final independent-conjugacy class comparison. The generated individual
representatives need not jointly be a basis; this is harmless for this
class enumeration and would not be harmless for further literal
Nielsen moves.

## 3. Independent source audit

The exact AK(3) class counts from T's matrix enumeration are:

| Endpoint cyclic-energy cap | Projective primitive vectors | Unimodular pairs / distinct pair classes |
| ---: | ---: | ---: |
| 22 | 6 | 6 |
| 40 | 23 | 26 |
| 100 | 160 | 176 |
| 120 | 233 | 253 |
| 200 | 666 | 706 |
| 250 | 1,059 | 1,111 |

The equality between the last two counts is observed for these runs;
no additional general injectivity theorem is needed or asserted.

For caps 120, 200 and 250 I also regenerated every source in V's JSONL
from its signs and L/R program. I used only freely reduced literal
words, never independent cyclic reduction between Nielsen steps. The
left multiplication in L is expanded into five permitted inversions
and right multiplications. Every source prefix was replayed through
the repository's strict elementary verifier, and all signed exponent
columns, raw endpoint words, cyclic words, and energies were checked.

| Cap | Actual source bases | Total strict source instructions replayed | Largest raw peak | Largest cyclic peak |
| ---: | ---: | ---: | ---: | ---: |
| 120 | 253 | 4,937 | 124 | 120 |
| 200 | 706 | 18,730 | 204 | 200 |
| 250 | 1,111 | 33,238 | 254 | 250 |

At each cap, the full V source class set equals T's independently
computed set. The cap-250 uncompressed source SHA256 is
`4de92fdc35db0dd2011580bf3994407a59c348bc06806c0a98ca36b2ed6395db`.
T's sorted cap-250 family TSV SHA256 is
`e8372ab7cecace8a3194470723742bc826b77c336b42dc31902d244a7563baff`.
The validator also accepts gzip and base64-wrapped gzip, hashes the
decoded JSONL separately from its transport, and was checked on both
plain and compressed transports of exactly this corpus.

V's terminal cap-250 result scans 5,862,545 rotation pairs and
2,905,457 distinct unbased folded graphs. All have the sufficient signed
DAG absence certificate; there are zero exact-detector exceptions and
zero matches against the two specified known-trivial reverse corpora.
Those are V's downstream computations, not an independent T refolding
of all 2.9 million graphs. See [V's report](research-v.md), its scanner
and terminal result. T independently verifies the finite source
coverage on which that scan relies.

Combined with Q/R's arbitrary-tail reduction, this excludes a precise
phase pattern: an arbitrary initial-H Nielsen basis whose endpoint
cyclic energy is at most 250, followed by arbitrary independent
conjugations, followed by an arbitrary Nielsen suffix exposing a
primitive. The original Nielsen path may itself have larger energy;
its endpoint class is still covered. This is not a global AC invariant.
Higher source endpoint energy and later alternating subgroup changes
are outside the result. It does not classify the whole cyclic cap-250
component or raise the global cyclic peak lower bound beyond 23.

V also tested a distinct reverse route: collapse a bridge in a known-trivial
barbell subgroup. Rebase to one branch vertex and change to its cycle
basis `(u,q v q^-1)`; conjugating the second coordinate by `q^-1` gives
`(u,v)`. Thus a matching initial-H cyclic family would give an AC bridge
after the required strict basis and entry ledgers were compiled. T
independently classified all 56,799 reverse rows by deleting each
undirected graph edge and testing connectivity, rather than using V's
branch-path tracing. Reusing R's batch folding explicitly, this gives
the same 549 barbell rows and the exact same 338 collapsed cycle-family
keys. Their maximum cycle energy is 21, and none occurs in T's complete
cap-40 initial-H matrix list. This finite reverse-corpus exclusion is
recorded in `certificates/t_barbell_reverse_review.json`.

## 4. An actual hidden-primitive-to-completion pipeline

`t_hidden_primitive_completion.py` joins existing constructive routines:
R's exact partial-map-pair detector and spanning-tree basis bridge,
M's primitive-to-generator and completion code, and the strict free-word
verifier. It begins with an actual elementary prefix, not a bare graph
match. A positive detector word is rewritten in a spanning-tree basis;
the corresponding basis change exposes that word as a coordinate, then
M's completion reaches `(x,y)`. Every appended elementary move is
replayed. `INCOMPLETE` or an unexpanded oversized straight-line witness
produces no completion certificate. This glue does not independently
reimplement or establish novelty for R/M's component algorithms.

On V's AK(2) control, the selected raw source is reached by signs
`(-1,+1)` and the L program. T compiles the raw source and its specified
rotations to

```
A = XXyyy,    B = YXyyXyx
```

in 15 strict moves, with raw peak 14. R's detector, independently
confirmed by U, finds the cyclic primitive `xYxYYxYY`, a base path `XX`,
and the based primitive

```
w = XYxYYxYYxx = B^-1 A^-1.
```

The orientation is significant: this B is the inverse of the B used in
an older R/O control. T's compiler uses V's actual pair. The strict
subgroup-basis bridge takes five moves and has raw peak 17. The full
replayed certificate has literal start

```
(xxYYY, xyxYXY)                    [AK(2)]
```

and literal endpoint `(x,y)`, using 232 strict moves and raw peak 33.
It is a calibration of the detection-to-proof pipeline, not an improved
AK(2) bound or an AK(3) result. The initial AK(3) subgroup was also passed
through the glue as a negative control: R's complete exact detector
returns `ABSENT` and the pipeline emits no certificate.

## Artifacts and reproduction

From a checkout with the published repository experiments present, run:

```sh
python3 experiments/nielsen_basis_classes.py --n 3 --cap 250 --families /tmp/t250.tsv --output /tmp/t250.json
python3 experiments/validate_farey_sources.py certificates/v_cap250_sources.jsonl.gz.b64 --n 3 --cap 250 --output /tmp/t250-audit.json
python3 experiments/t_hidden_primitive_completion.py certificates/t_v_ak2_candidate_prefix.json --certificate /tmp/t-ak2-full.json --output /tmp/t-ak2-result.json
python3 experiments/elementary_verify.py certificates/t_v_ak2_hidden_full.json
```

The independently computed matrix result and source audit are in
`certificates/t_basis250_results.json` and
`certificates/t_raw_basis250_review.json`. The two AK(2) prefix and full
ledgers and `certificates/t_v_ak2_hidden_pipeline_results.json` give the
positive calibration. V publishes the source corpus and scanner;
T does not silently depend on unpublished source words. The supplemental
`experiments/t_barbell_reverse_review.py` accepts the two reconstructed
reverse TSV files and `--v-result` pointing to V's anchor JSON; its output
is the independent edge-connectivity review above.

The useful insight is now concrete: full basis-class coverage and exact
primitive detection can be connected to a strict, literal AC proof when
a positive waypoint exists. These particular AK(3) phase searches have
not produced such a waypoint. None of the four requested unrestricted
outcomes has been achieved.
