# Research W: an independent topological route and planar-link parity certificates

Date: 2026-11-02. **No AK(3) ordinary AC trivialization, unrestricted AC
obstruction, or proof/disproof of the AC conjecture is established.** No
novelty or priority claim is made.

The main contributions are a short uniform obstruction to immediately
applying a three-dimensional thickening theorem to the initial AK(n)
presentation, a fast finite parity filter for three planar-link types,
and checked applications to actual reachable tuples. These are local
topological tests. They are not invariants of ordinary AC moves.

## Prior reading and independent choice

Before choosing a direction I fetched the repository README (the
nineteen-researcher version, SHA
`75d1116fb9d548f79d45e651aa27dd2b4616760c`) and read Q/R's all-tail
subgroup results, R's reverse-search follow-up, the cyclic basis-sublevel
proof, and the new T/U/V basis-phase reports. The known cap-22 component
contains no primitive coordinate, and every actual independently
conjugated representative generates a primitive-free subgroup. V's
initial-subgroup basis-phase exclusion now extends its source endpoint
energy to 250. None of these facts excludes a later alternating sequence
of subgroup changes.

While W worked, V and U completed the stronger
[unbounded two-conjugate theorem](research-v-unbounded.md), which W then
read: arbitrary elements of the initial subgroup, independently
conjugated, still generate a primitive-free subgroup. This supersedes
the numerical one-phase restriction. W's topological target remains
distinct and makes no claim to evade that theorem with a Nielsen suffix.

I independently chose a different completion target: a presentation
complex that thickens into a three-manifold. In his June 2026 preprint,
[Lackenby, Theorem 1.3](https://arxiv.org/pdf/2606.06122), proves ordinary
AC triviality for thickenable balanced presentations of the trivial
group. Thus a rigorously thickenable presentation reached by actual
ordinary moves would suffice, even if its displayed relators were both
nonprimitive. This is an application of an external theorem, not a new
proof of that theorem. The preprint also explicitly lists the AK family
among potential counterexamples; it does not assert that these initial
presentations are thickenable.

## 1. The exact local test

Work with nonempty cyclically reduced literal words in `x,X,y,Y`, where
capital letters denote inverses. For every corner `a b` in a cyclic
relator, put an edge from `a^-1` to `b` in its Whitehead link graph.
Keep parallel edges distinct. At an occurrence of a generator, pair the
end of the preceding corner with the start of the following corner.
This gives a fixed bijection between darts incident at `x` and `X`, and
between those incident at `y` and `Y`.

An orientable thickening requires an embedding of this link in an
oriented sphere for which the cyclic orders at each inverse-vertex pair
are **opposite under that sheet bijection**. Cutting an orientable
generator handle leaves two discs on the boundary sphere; gluing them
back is orientation reversing on their boundary circles, which explains
the opposite-order convention. This is the standard synchronized
planarity formulation underlying
[Neuwirth's construction algorithm](https://doi.org/10.1017/S0305004100043279).
The same opposite-order convention is stated explicitly for matched
vertices in [Bläsius--Fink--Rutter, Section 1](https://drops.dagstuhl.de/storage/00lipics/lipics-vol204-esa2021/LIPIcs.ESA.2021.19/LIPIcs.ESA.2021.19.pdf).

Conversely, such a planar compatible diagram can be thickened: blow up
its four vertices to discs on a three-ball, attach the two orientable
generator handles using the prescribed sheet pairings, and attach
two-handles along the disjoint relator curves. Their spine gives the
required presentation complex. For the balanced trivial presentations
considered here it is enough to test orientable thickenings. Any regular
neighbourhood of their contractible presentation complex is simply
connected and hence orientable, even if the larger ambient manifold was
not assumed orientable.

For an explicit exhaustive test, independently enumerate every cyclic
order at `x` and `y`; the opposite orders at `X,Y` are forced. If these
valences are `d_x,d_y`, the count is
`(d_x-1)! (d_y-1)!`, with the usual empty/singleton convention. With
rotation permutation `sigma` and edge-reversal involution `alpha`, the
cycles of `sigma alpha` are the faces of the associated orientable
ribbon surface. If the nonempty link has `c` connected components,
`V` vertices, `E` edges and `F` such faces, its total genus is

```
g = (2c - V + E - F)/2.
```

A compatible planar diagram exists exactly when some enumerated order
has genus zero. Python and native C++ implementations enumerate the
orders separately. A budget stop is `INCOMPLETE`, never a negative
decision. The native search also emits a positive rotation witness,
which the separate Python evaluator checks directly.

## 2. A short uniform initial AK(n) obstruction

Put

```
p_n = x^n Y^(n+1),    b = xyxYXY,    n >= 2,
m = 2n+1.
```

Number the corners after the letters of `p_n` as `e_0,...,e_(m-1)`,
then the six braid corners as `e_m,...,e_(m+5)`. Let `d_i^-` be the dart
at the inverse of the letter before corner `e_i`, and `d_i^+` the dart
at the next letter. The link's six parallel-edge bundles are:

| Endpoints | Corners |
|---|---|
| `x,X` | `e_0,...,e_(n-2)` |
| `X,Y` | `e_(n-1), e_(m+2)` |
| `y,Y` | `e_n,...,e_(2n-1)` |
| `x,y` | `e_(2n), e_(m+5)` |
| `x,Y` | `e_(m+1), e_(m+4)` |
| `X,y` | `e_m, e_(m+3)` |

Every bundle is nonempty, so the simple underlying graph is `K4`.
In a planar embedding, **each parallel-edge bundle is a consecutive
block at both endpoints**. Here is the needed justification: two edges
of a bundle form a Jordan digon. The other two vertices of `K4` are
connected by their own edge and must lie on the same side of that digon.
All their incident strands must therefore lie in a common sector between
consecutive bundle edges. This leaves the whole bundle consecutive in
the cyclic order. Collapsing the bundles gives a planar `K4`; its local
three-neighbour block orders are unique up to global reflection. Choose
the following orientation:

```
at x: X,y,Y      at X: x,Y,y
at y: x,X,Y      at Y: x,y,X.
```

Within a bundle use increasing corner indices at its lower endpoint in
the order `x,X,y,Y`, and the reverse at its upper endpoint, as a reference
embedding. Every planar embedding with the chosen global orientation
differs only by permutations within bundles, with opposite permutations
at their two ends. Global reflection reverses both ends of every sheet
pair and does not change the consistency equations below.

Let `A` be the comparison-flip bit between `e_(n-1),e_(m+2)` in the
`X,Y` bundle, and `B` the bit between `e_n,e_(n+1)` in the `y,Y` bundle.
A flip is zero for the reference order and one for its reversal. The
following three triples of darts, and their paired triples at the
inverse vertices, impose:

| Vertex | Dart triple | Opposite-sheet equation |
|---|---|---|
| `x` | `(d_(n-2)^+, d_(2n)^+, d_(m+1)^+)` | `A=0` |
| `y` | `(d_n^-, d_(n+1)^-, d_m^+)` | `B=0` |
| `y` | `(d_n^-, d_(n+1)^-, d_(m+3)^-)` | `A+B=1` |

For example the first triple meets all three neighbour blocks at `x`,
so its orientation is fixed. Its paired triple at `X` has its first and
third darts in the `X,Y` bundle, making its orientation depend only on
`A`. In the second row the `y,Y` comparison appears only on the `y`
side. In the third it appears on the `y` side and the `X,Y` comparison
appears on the `Y` side. Reading the fixed reference block orders above
gives the displayed constants. Adding the three equations over `F2`
gives `0=1`.

Therefore **the initial literal AK(n) presentation complex has no
orientable thickening for every n>=2**. In particular the initial AK(3)
tuple cannot immediately use Lackenby's theorem. This unbounded initial
family assertion is the labelled-corner proof, not extrapolation from a
finite search. `uniform_ak_parity.py` checks its exact index conventions
for `n=2,...,32` and publishes the three-equation AK(3) certificate.

This is emphatically not an AC obstruction: AK(2) is a positive
countercontrol to any attempted invariance claim. Its initial tuple
fails this test but has many already verified ordinary trivializations.

## 3. A general parity filter for three planar-link types

The filter relaxes comparisons within every permutable linear order to
independent `F2` variables. For any three distinct darts, reversing one
pair comparison changes their cyclic orientation. When all three lie
in a permutable block, the orientation changes by the XOR of its three
pair-comparison flips; when only two lie in the block, only their one
comparison matters. Three fixed distinct blocks give a constant.

For each triple at `x` or `y`, opposite orientation under the sheet
bijection is thus a linear equation. Gaussian elimination may produce
an explicit set of rows whose XOR is `0=1`. Such a contradiction excludes
every actual planar compatible diagram. A consistent relaxed system
alone proves nothing: comparison bits might fail transitivity. It is
reported as `PARITY_CONSISTENT`, not as an embedding or a negative result.

The complete planar-embedding charts used are:

* **K4:** the bundle-block description proved above.
* **C4:** every bundle is consecutive. Removing the endpoints of one
  cycle edge leaves a connected path, so the same digon argument forces
  all remaining attachments into one sector. The two block orders at
  each vertex are fixed; bundle permutations are arbitrary and opposite
  at their endpoints.
* **Diamond (`K4` minus one edge):** let `u,v` be its degree-three simple
  vertices and `w,z` its degree-two vertices. The bundles on the four
  arms `u-w-v` and `u-z-v` are consecutive, again because deleting an
  arm's endpoints leaves the other two vertices connected. Treat each
  long branch as one item, but treat **each direct `u-v` edge as its own
  item**. These items may occur in any cyclic order at `u`, with the
  reverse order at `v`. Each arm's internal bundle orders are independent
  and opposite at the two ends of that bundle. Contracting the two long
  branches reduces this description to arbitrary planar embeddings of
  a parallel-edge graph, so it covers all embeddings. In particular the
  direct `u-v` edges are not incorrectly forced to be consecutive.

For the diamond's permutable cyclic item order fix one long branch as
the first item, then use comparison bits for the remaining linear list.
At a triple spanning three distinct items use those pair comparisons;
at a triple with two darts in one item use only its internal comparison.
This gives the same parity rule, with no enumeration cutoff.

`verify_link_parity.py` is a separate certificate checker. It imports no
constructor, Gaussian solver, or graph-folding routine. It independently
reconstructs corners and sheet pairings, checks the reference diagram's
spherical Euler characteristic and chart orders, reconstructs each
selected triple equation, and checks that their XOR is `0=1`. The
geometric chart-completeness arguments above are still mathematical
inputs, not claims of proof-assistant formalization. T provides a
[separate mathematical and chart review](research-t-w-topology-review.md).
Its code imports no W routine: it exhausts **563,145** unrestricted
rotation systems on **118** small multigraphs; every one of the **1,547**
spherical systems fits the stated chart. T also independently derives
the three uniform equations and checks their indices through n=256.

## 4. Checked finite results

Independent exhaustive Python/native order enumeration agrees on the
initial AK(3) tuple: all **86,400** compatible order choices are
nonplanar, with minimum observed genus **2**. AK(2) has **2,880** choices
and minimum genus **1**. Separate native runs for AK(4) and AK(5)
exhaust **3,628,800** and **203,212,800** choices respectively; each has
minimum genus **2**. These particular minima are finite computations;
no formula for minimum genus at general n is asserted.

All **52** literal canonical states of total cyclic length at most 14
in the published cap-22 catalogue were also exhaustively checked. None
has a planar compatible link: 48 have minimum genus one and four have
minimum genus two. Their raw rotation witnesses and histograms are saved.

The parity filter processes the entire already independently audited
**258,032-state C22 catalogue**. Exactly **222,292** have simple K4 links;
the remaining **35,740** have diamond or C4 links. Every one has a parity
contradiction. Thus none of these **literal canonical cyclic
presentation complexes** is orientably thickenable. The full reproduction
constructs every certificate and passes it to the separate verifier:
**35,692** diamond cases and **48** C4 cases, with **662,591** selected
XOR equations independently checked across all three charts. The full
[audit result](../results/w_cyclic22_topological_parity_audit.json) passes.
The source TSV SHA256 is

```
cd9ba5781a1efcb1bf1b8a72c9a392b79de1cd915da6a520b8f33a4390787fa3.
```

This is not a theorem about all independently conjugated literal
presentation complexes, nor a new global peak lower bound. We do not
silently assume that cyclic normalization preserves the exact local
embedding type of an arbitrary presentation complex. The earlier Q/R
all-tail subgroup theorem has a different invariant and scope.

As a heuristic follow-up, root supplied 300,000 actual sampled subgroup
nodes. Among the **13,587** node tuples with boundary cyclic energy at
most 25, **13,581** have direct parity obstructions and six are outside
the supported charts. The six are retained as unresolved. This is a
sampled set, not the full cap-25 component. A particular actual root
endpoint

```
(XyyyyXXXyxYxxYX, xyXXyXYx)
```

has a two-equation parity contradiction. I separately replayed root's
entry certificate: **2,152 strict ordinary moves**, raw peak **233**, to
those literal words. The obstruction excludes immediate application of
the thickening theorem there; it does not block further ordinary moves.
The larger sample inherits its source-node provenance from root's
heuristic engine; only the selected entry above is independently replayed
here as a full strict ledger. The exact sampled words, source IDs and
selected strict entry are archived in gzip/base64 transports whose hashes
are recorded in `certificates/w_transport_manifest.json`.

An auxiliary ambient-Nielsen descent yields 178,907 distinct shortened
tuples from the C22 input; all also have parity contradictions. Those
ambient substitutions are explicitly search operations, **not ordinary
AC ledgers**. No additional orbit or thickenability-preservation claim is
inferred from that corroborating experiment, and the main C22 conclusion
uses the original literal cyclic tuples directly.

## 5. Positive and independent controls

With seed 20261102, 1,000 independently generated small cyclic word
pairs plus five fixed controls are checked by the independent native
exhaustive rotation enumerator. All **1,005** finish without budget
stops. Among them **640** have explicit planar compatible witnesses,
which the separate Python evaluator verifies. Of the supported-chart
positive cases, 59 are K4, 123 diamond, and 133 C4. **None** receives a
parity obstruction. There are also 297 genuine parity exclusions, 28
consistent but nonplanar relaxed cases, and 365 unsupported cases; the
latter statuses are not promoted to negative conclusions.

The standard tuple `(x,y)`, torus word `xyXY`, projective-plane word
`xx`, Klein-bottle word `xxyy`, and basis `(x,xy)` have planar compatible
orders. These check the sheet orientation convention on familiar
orientable thickenings, including complexes with nontrivial fundamental
groups.

A balanced trivial **nonprimitive-coordinate** positive control is

```
(xxYYY, xxxYYYY).
```

Its native planar witness is independently verified. Neither displayed
word is ambient primitive. Five strict ordinary moves expose the
primitive `xY`; M's existing compiler then finishes at literal `(x,y)`.
The complete replay has **35 strict moves**, raw peak **12**. This shows
that the topological target can recognize a useful tuple before a
primitive is displayed. It is a control, not AK(3).

T's AK(2) positive ledger is also sampled at all distinct cyclic states
of energy at most 14: two are nonplanar and six have planar witnesses.
The first planar state on that particular ledger occurs after a
primitive coordinate is already present; no earlier topological shortcut
is claimed.

## Reproduce and limitations

All Python code uses the standard library; native enumeration requires
C++17. From the repository root:

```sh
c++ -std=c++17 -O3 experiments/thickening_rotations.cpp -o /tmp/w_rotations
python3 experiments/thickening_rotations.py xxxYYYY xyxYXY --output /tmp/w-ak3-python.json
/tmp/w_rotations /tmp/w-ak3-native.json 0 xxxYYYY xyxYXY
python3 experiments/parity_controls.py --binary /tmp/w_rotations --prefix /tmp/w-controls
python3 experiments/verify_link_parity.py certificates/w_ak3_uniform_parity.json certificates/w_root_waypoint_parity.json --output /tmp/w-small-review.json
python3 experiments/cyclic_catalogue_to_tsv.py certificates/cyclic22_component_manifest.json /tmp/w-cyclic22.tsv
python3 experiments/audit_cyclic_link_parity.py /tmp/w-cyclic22.tsv --output /tmp/w-cyclic22-review.json
python3 experiments/elementary_verify.py certificates/w_geometric_nonprimitive_full.json
```

The auxiliary ambient-descent experiment can be regenerated separately:

```sh
python3 experiments/prepare_thickening_candidates.py /tmp/w-cyclic22.tsv --tsv /tmp/w-descended.tsv --provenance /tmp/w-descended-provenance.json
python3 experiments/scan_k4_parity.py /tmp/w-descended.tsv --general --prefix /tmp/w-descended-review
python3 experiments/uniform_ak_parity.py --directory /tmp/w-uniform
```

The small proof certificates, exhaustive initial/low-state results,
random-control summary, full separate-verifier audit, and source are
published alongside this report. The search filter's practical limitation
is mathematical as well as computational: a parity-consistent system
need not come from transitive orders, and supported charts do not cover
every possible Whitehead link.

No thickenable AK(3) waypoint was found. The original four requested
breakthrough outcomes remain unachieved. A useful next experiment is to
screen new coupled-coordinate paths for this topological target while
retaining strict entry ledgers; any positive rotation witness must be
checked before invoking the external thickening theorem.
