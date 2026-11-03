# T's independent review of W's topological filter

Date: 2026-11-02. I found no missing embedding freedom or sign error in
W's orientable sheet-pairing test, its K4/C4/diamond planar charts, or its
three-equation obstruction for the initial AK(n) family. The conclusions
have the restricted scope stated in [W's report](research-w.md).
**No AK(3) ordinary AC solution or unrestricted obstruction is established.**

This review was requested after my basis-coverage investigation had been
published. Before reviewing I read W's full report and the sources
`planar_link_parity.py`, `k4_rotation_parity.py`,
`verify_link_parity.py`, `thickening_rotations.py`, and
`uniform_ak_parity.py`. I specifically tried to invalidate necessity of
the planar constraints or find an omitted planar embedding choice. The
two new control implementations below import none of W's modules.

## Sheet pairing and the exact test

For a corner after a letter `a`, its first dart lies at `a^-1`; the dart
at the end of the preceding corner lies at `a`. Pairing those darts
therefore matches the two cross-sections of the same generator occurrence.
The constructor and separate verifier implement this same occurrence
pairing, including the separate cyclic wrap in each relator.

An orientable generator one-handle is attached to two discs of an oriented
three-ball with opposite boundary orientations. Thus its matched sheet
orders must be opposite. The convention agrees with the P-constraints
defined in [Bläsius–Fink–Rutter, Section 1](https://drops.dagstuhl.de/storage/00lipics/lipics-vol204-esa2021/LIPIcs.ESA.2021.19/LIPIcs.ESA.2021.19.pdf).

Conversely, compatible spherical rotations allow the corner arcs to be
joined across those handles by disjoint strands. The relator strands form
disjoint closed curves on the resulting oriented boundary surface.
Attaching two-handles along them gives a regular thickening with the
required presentation spine. No prescribed framing is part of this
existence question. The ribbon-surface Euler characteristic therefore
gives an exact exhaustive test of these orientable compatible rotations,
not merely a necessary planarity test.

For a balanced trivial presentation, its presentation complex is
contractible: its Euler characteristic is one, its fundamental group and
first homology vanish, and its second cellular homology then vanishes.
A regular thickening has the same fundamental group, hence is orientable.
Consequently failure of the orientable test really does exclude a
thickening of these particular complexes, even if the ambient manifold
was not initially assumed orientable. This inference is not claimed for
arbitrary nontrivial presentation groups.

I also checked the external target theorem's literal statement:
[Lackenby's June 2026 preprint, Theorem 1.3](https://arxiv.org/pdf/2606.06122)
states ordinary AC triviality for thickenable balanced trivial
presentations. I have not independently audited the entire proof of that
external theorem. W's local negative certificates do not depend on its
validity; its role is to justify a potential future positive target.

## Completeness of the planar charts

The useful general fact is the following. Fix a bundle between vertices
`a,b`. If the rest of the graph after deleting `a,b` is connected, all
remaining vertices lie in one complementary sector of the parallel
bundle in a spherical embedding. Every strand from an endpoint to that
remaining graph lies in that same sector. Thus the bundle is one
consecutive cyclic block. Its two endpoint edge orders are opposite.

This applies to every K4 bundle, every C4 bundle, and each of the four
diamond arm bundles. After collapsing the K4 bundles, the simple K4 has
only its two reflected spherical rotation systems; a global reflection
reverses both members of every inverse-vertex sheet pair, leaving the
compatibility equations unchanged. Within each bundle, arbitrary opposite
endpoint permutations give all remaining choices.

For the diamond's direct degree-three-to-degree-three bundle, deleting
its endpoints leaves two disconnected vertices. The argument would fail
there, and forcing that bundle consecutive would be unsound. W explicitly
does not do so. Instead each direct edge is a separate item, alongside
the two long branches. Arbitrary cyclic item orders at one root and the
reverse orders at the other describe the spherical parallel-path
embedding. The arm-bundle permutations are independent. The degree-two
vertices have only two blocks, whose cyclic block order imposes no
further choice. This includes the potentially dangerous interleavings.

I checked these claims independently on 118 labelled multigraphs by
enumerating **every vertex rotation system**, without imposing any sheet
constraints or importing W's chart constructor:

| Underlying graph | Multigraphs | Rotation systems checked | Spherical systems |
| --- | ---: | ---: | ---: |
| K4 | 42 | 488,608 | 466 |
| C4 | 50 | 47,953 | 753 |
| Diamond | 26 | 26,584 | 328 |
| Total | 118 | 563,145 | 1,547 |

Every spherical system satisfies the claimed chart, including reversed
bundle orders and the diamond's arbitrary direct-edge interleaving.
The tests cover K4 multiplicities 1–2 with at most nine edges, C4
multiplicities 1–3 with at most eight edges, and diamond multiplicities
1–2 with at most eight edges. These are controls for the mathematical
chart argument, not a finite proof for arbitrary multiplicities.

## Parity relaxation and the uniform contradiction

The cyclic orientation of three darts changes by the parity of their
restricted permutation. If three darts lie in one permutable block,
that parity is the XOR of their three comparison flips; for two darts
in one block and one outside, only the internal pair flip matters.
Three distinct fixed blocks give no comparison variable. In the
diamond item order, fixing item zero reduces a cyclic order to a linear
list; the constructor correctly omits comparisons involving that fixed
item. These rules include all transitive orders. Dropping transitivity
only enlarges the feasible set, so an XOR contradiction is sound, while
consistency alone is not a positive embedding certificate.

I independently reconstructed W's initial-family triple calculation. Use
its corner indices, `m=2n+1`, and its displayed K4 block orientation.
The paired triples, in the same order as their source triples, are:

| Source vertex/triple | Paired triple | Reference orientations |
| --- | --- | --- |
| `x: (d_(n-2)^+, d_(2n)^+, d_(m+1)^+)` | `(d_(n-1)^-, d_0^-, d_(m+2)^-)` | `(1,0)` |
| `y: (d_n^-, d_(n+1)^-, d_m^+)` | `(d_(n-1)^+, d_n^+, d_(m+1)^-)` | `(1,0)` |
| `y: (d_n^-, d_(n+1)^-, d_(m+3)^-)` | `(d_(n-1)^+, d_n^+, d_(m+2)^+)` | `(1,1)` |

Only the comparisons `A=(e_(n-1),e_(m+2))` and
`B=(e_n,e_(n+1))` occur. The first paired triple contains the A comparison,
the second source triple contains B, and the third row contains both.
Opposite-sheet compatibility therefore gives exactly

```
A = 0,    B = 0,    A+B = 1.
```

All indices and branch memberships remain valid for every `n>=2`,
including `n=2`. This is an all-n labelled-corner argument, not an
extrapolation from computations. An independent implementation controls
the index calculation for `n=2,...,256` and obtains the same masks and
constants throughout.

The same implementation independently exhausts all 2,880 compatible
orders for initial AK(2) and all 86,400 for initial AK(3), obtaining
minimum genus one and two respectively. The full AK(3) genus histogram
agrees exactly with W's separately written enumeration: 724 genus-two,
14,882 genus-three, 55,438 genus-four, and 15,356 genus-five systems.

## Certificate review and scope

W's separate checker reconstructs the corners and sheet bijection,
verifies a spherical reference embedding and the stated chart, rebuilds
the selected triple masks and constants, and checks their XOR. It imports
neither the parity constructor nor its elimination solver. I found no
unsound acceptance path in those operations for the generated
certificates. The completeness of the geometric charts remains a
mathematical input, which is why this review examined it separately.

W reports a complete constructor-plus-separate-checker run on all
258,032 literal canonical C22 tuples: 222,292 K4, 35,692 diamond and 48
C4 cases, all with contradictions. I reviewed the code and this result
but did not independently repeat that entire C22 scan in this review.
The new T computations are precisely the finite chart and initial-family
controls listed above. No stronger independent reproduction is implied.

The initial AK(n) nonthickenability statement and the literal C22
statements survive this review. They do not apply automatically to every
independently conjugated literal representative, do not classify the
whole cap-25 component, do not raise the global AC peak bound, and are
not invariants under later ordinary AC moves. The positive AK(2)
trivializations correctly prevent any such inference. There is no
unresolved criticism requiring W to weaken the current stated claims.

## Reproduce

The review programs use only Python's standard library and import none
of W's code:

```sh
python3 experiments/t_w_review_charts.py --output /tmp/t-w-charts.json
python3 experiments/t_w_review_uniform.py --output /tmp/t-w-uniform.json
```

The saved results are `certificates/t_w_review_charts_results.json` and
`certificates/t_w_review_uniform_results.json`. This is a mathematical
and executable review, not proof-assistant formalization.
