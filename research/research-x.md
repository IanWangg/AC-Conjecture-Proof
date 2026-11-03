# Research X: a restricted two-phase exclusion and exact limits of character extension

Date: 2026-11-02. **AK(3) and the ordinary, unstabilized AC conjecture
remain unresolved.** No novelty or priority claim is made.

The principal new result is an unbounded primitive-free theorem for all
42 initial rotation-successor subgroups. It excludes a specific
two-conjugation-phase route. A separate exact audit shows where extending
V's larger infinite-kernel method succeeds or fails. Actual long-bridge
searches retain ordinary reachability but produce no AK(3) completion.

## Reading, independent choice, and attribution

Before choosing a direction, I fetched the private repository README
(SHA `75d1116fb9d548f79d45e651aa27dd2b4616760c`) and read Q/R's all-tail
theorem, the cyclic basis-sublevel proof, V's new unbounded theorem,
U's independent voltage review, and W's topological draft. I independently
chose to investigate a second conjugation phase: can the 45 infinite
kernels protecting the initial subgroup protect their own independently
conjugated elements? That question led both to exact character-extension
obstructions and to a more useful test on actual rank-two successors.

The graph-identification construction and strict-cycle solver are
**V's algorithms**. The central axes and primitive-class arguments are
Q/R's, and the independent finite voltage auditor is the coordinating
researcher's. X supplies the new finite source families, exact affine
feasibility classification, separate dual/cycle verifier, and recorded
barbell experiments. T independently checks the algebra, real-parameter
coverage, primitive witnesses, and the successor geometry. Shared code
is credited explicitly; these are not presented as independent rewrites
of all prior algorithms.

## 1. All 42 initial rotation successors have an unbounded theorem

Write

```
p = xxxYYYY,    b = xyxYXY,    F=F(x,y).
```

For `0<=i<7` and `0<=j<6`, let `p_i,b_j` be the corresponding cyclic
rotations, and put `H_(i,j)=<p_i,b_j>`. There are 42 **literal source
pairs**; this count is not claimed to count distinct unbased subgroups.

**Theorem.** For every one of these 42 subgroups, every `u,v in H_(i,j)`
and every `a,c in F`, the subgroup

```
<a u a^-1, c v c^-1>
```

contains no ambient primitive element. There is no source-word,
Nielsen-step, conjugating-tail, cyclic-energy, or suffix-length bound.

Here is the finite certificate and the unbounded deduction. Fold each
actual source pair to its finite based core. For every distinct pair of
core vertices, identify them and fold. Across all 42 sources there are
**2,272** such identifications. Every quotient has rank three and an
integer character `chi` that kills the source subgroup and sends the
extra connecting loop to one. These characters and their inverse edge
voltages are saved explicitly.

For each quotient, four signed alphabets and two forbidden doubles give
eight directed edge-state automata. Every cyclic primitive word in rank
two lies in one of them: it uses one sign of each generator and one
generator can be isolated. This is the signed Euclidean primitive
description used in [Q/R](research-r.md), based on
[Clay--Conant--Ramasubramanian, Section 4](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf).
On each cyclic strongly connected component `C`, the saved sign `epsilon`
and integer potential `q` satisfy, for every internal arc of voltage `w`,

```
q(end) <= q(start) + |C| epsilon w - 1.
```

Summing along a nonempty directed closed walk makes its voltage strictly
nonzero. Thus `ker chi` has no ambient primitive element, at any length.
The independent auditor refolds every quotient, checks all source
projections and character values, reconstructs the automata and strongly
connected components, and verifies **42,876 integer inequalities**.
All 42 sources and all 2,272 quotients pass, with no unresolved cases.

To finish, cyclic reductions and rotations of words of `H_(i,j)` label
loops at vertices of its original core. If their two chosen vertices
coincide, the transported subgroup is contained in `H_(i,j)`. If they
differ, identifying those vertices places both loops in a certified
`ker chi`; rebasing preserves their zero voltages. Equivalently, the
pullback voltage on the original graph is an exact coboundary. The
auditor verifies that the character kills the actual source basis, which
implies this coboundary condition on a connected graph.

Q/R's axes argument handles arbitrary conjugators. Intersecting axes
reduce by one common conjugation to cyclic rotations. Disjoint axes give
a folded barbell; a primitive cyclic path cannot traverse its separating
bridge in both directions, and a loop in either circle cannot be a
primitive power of a nonprimitive source. Identity sources cause only
the same cyclic-subgroup case. This is exactly the deduction in
[V's unbounded theorem](research-v-unbounded.md), now with a fully
certified finite dataset for every `H_(i,j)`.

Each source is an actual ordinary AK(3) successor. All 42 entry ledgers
are archived and independently replayed: **231 strict moves in total**,
each with raw peak **13**.

### The precise two-phase consequence

Consider a path starting from `(p,b)` with this prescribed structure:

1. independently conjugate the original two coordinates, with their axes
   intersecting after that phase;
2. perform arbitrary coordinate Nielsen moves;
3. independently conjugate the resulting coordinates;
4. perform arbitrary further coordinate Nielsen moves.

After a common conjugation, the first subgroup is one of the 42 tested
rotation successors. Step 2 stays inside it, the theorem controls step 3,
and step 4 preserves the resulting primitive-free subgroup. This path
cannot expose a primitive coordinate or reach the standard free basis.

This does **not** cover a preceding arbitrary Nielsen prelude in `H0`,
disjoint axes with an arbitrary bridge in step 1, or a third interspersed
conjugation phase. It is not a statement about every two-phase AC path,
not a global invariant, and not a larger numerical cyclic-peak bound.

## 2. A concrete successor and complete finite comparison

One useful source is

```
H1 = <xxxYYYY, XYxyxY>.
```

Conjugating the original braid coordinate by `Y`, then by `X`, reaches
this pair in **two strict moves**. Its immersed theta has branch paths

```
P=y,    Q=XYxyx,    R=xxxYYY,
```

of lengths `(1,5,6)`. The geometric basis
`(P Q^-1,P R^-1)=(yXYXyx,yyyyXXX)` is the inverse/permutation of the
displayed basis. An explicit compiled ordinary bridge reaches this
geometric basis from AK(3) in **23 strict moves**, raw peak **28**.
No relator swap or ambient generator substitution is implicit.

For this 11-vertex graph all 55 identifications pass. A separately saved
independent audit checks 440 automata, 340 cyclic components and 1,178
inequalities. The all-42 theorem already includes this subgroup.

As a finite comparison against known-trivial targets, V's raw-Farey
scanner was adapted to this geometric basis. Its primitive-class length
function is

```
L(a,b)=|a+b|+5|a|+6|b|.
```

On each signed orthant its absolute-coordinate slopes are positive:
`6a+7b` for equal signs, `6a+5b` for opposite signs with `a>=b`, and
`4a+7b` when `b>=a`. Therefore positive Farey additions increase source
energy; the same matrix coverage and raw-word precautions proved by
[T](research-t.md) apply. Raw words are retained throughout every prelude.

At cap 250 the scanner completes **985 source basis families**,
**5,155,565 rotation pairs**, and **2,563,971 distinct unbased cores**.
All pass the sufficient primitive-free filter, and none matches either
of R's two saved known-trivial reverse corpora. The finite primitive
scan is corroboration of the stronger unbounded theorem; the reverse
comparison remains only a finite comparison. The source corpus,
parameterized derivations, and exact result are archived. Code retains
the metadata field `AK_parameter:3` for the original family parameter;
its actual source words are the displayed H1 geometric basis.

## 3. What happens when V's infinite kernels are extended again?

V's initial proof uses 45 rank-three graph groups `K` and specified
characters `chi:pi1(K)->Z`. For each K, X identifies every distinct pair
of its vertices and folds to a graph L. There are **1,015** second
identifications, counted with their parent cases. This is a coarse
overgroup construction; it does not assert that arbitrary elements of
`ker chi` form an actual reachable rank-two successor basis.

Let `z1,z2,z3` be a spanning-tree basis of K. In a spanning-tree basis of
L, let M be their three exponent-coordinate rows, and let h record their
old character values. A character extending the **specified parent
character** must solve

```
M c = h.
```

Rational characters suffice: clearing denominators and a nonzero common
factor preserves their kernels. The final exact classification is:

| Second quotient type | Cases | Exact conclusion |
|---|---:|---|
| Rank two | 551 | No extension of the specified parent character |
| Rank three | 94 | Unique extension; primitive-free kernel certified |
| Rank four | 259 | Some rational extension has a certified primitive-free kernel |
| Rank four | 111 | No real parameter passes the sufficient same-sign-cycle criterion |

For all 551 failures there is a short integer dual row d with
`d M=0` but `d h!=0`. A representative is the first parent case, whose
basis is `(x,YYYY,yxyXY)` and character values are `(-1,3,-1)`.
The second identification gives the ambient rose. Its ambient exponent
rows are `(1,0),(0,-4),(0,1)`. Their relation `(0,1,4)` annihilates the
matrix but has character value `-1`. Thus this character cannot extend
even rationally to the rose. This is an exact limitation of this
extension method, not a primitive witness.

T gives a general algebraic explanation. For any rank-two overgroup
`L>=H0` in F, the two integer maps
`H1(H0)->H1(L)->H1(F)` have product determinant one, because the ambient
exponent determinant of `(p,b)` is one. Each map is therefore unimodular.
Every real character of L killing p and b is consequently zero. A
nonzero parent character killing p,b cannot extend to any such L, even
up to nonzero scaling. The 551 computed rank-two quotients are all
exactly the ambient rose; they explicitly contain primitives x and y.
This explains the failure of the character method without suggesting
that any eligible rank-two successor already contains those primitives.

The 370 rank-four systems have matrix rank three and hence a complete
one-dimensional affine solution space `c=c0+lambda c1`. Every directed
simple cycle has voltage `a lambda+b`. Within an SCC, V's sufficient
criterion requires all cycles to be strictly positive or all strictly
negative. Each alternative is an open real interval; intersecting these
finite unions across components decides feasibility exactly. No bound
on lambda remains. This finds 77 rational successes missed by the
earlier integer menu `[-10,10]`.

Every one of the 353 successful extension kernels has a full integer
potential certificate. The separate checker verifies **15,586** such
inequalities. For the 111 infeasible affine families, it verifies
**2,954 actual directed cycle witnesses** and their affine voltages,
then derives empty real feasibility. It need not trust completeness of
the discovery cycle enumeration: these actual cycles alone impose
necessary constraints already inconsistent for every real parameter.

For 58 of the 111 families, explicit ambient primitive loops have both
affine voltage coefficients zero. The only cyclic words needed are
`xYxYxYY` and `xYxYxYYxYxYY`, of lengths 7 and 12. In signed basis
`(x,Y)`, their primitivity is witnessed by positive basis programs
`RLLR` and `RLLRR`, respectively, taking the first coordinate, where
`L(U,V)=(U,UV)` and `R(U,V)=(UV,V)`. Their actual loops and base paths
are archived and independently checked. Hence these words belong to
**every coarse extension kernel in those affine families**. The remaining
53 cases have no found witness in the specified length-40 positive
menu; no negative conclusion is drawn from that failure.

This does not produce an AK(3) primitive waypoint. A primitive in a
coarse extension kernel need not lie in a subgroup generated by two
eligible source loops, much less an actual reachable free basis pair.
It instead explains why simply repeating the original character argument
cannot establish a global invariant. The 353 certified cases give genuine
unbounded protection for their specified source-kernel vertex pairs;
the other cases retain the distinctions in the table.

## 4. Actual long-bridge search and strict control

The original coupled sampler independently cyclically normalizes its
sampled boundary coordinates. To test a different entry, X retains a
literal first-phase bridge in

```
(p, q b q^-1)
```

**before** the next raw Nielsen prelude. The first letter of each chosen
q is off the p axis and its last inverse letter is off the b axis, so
these entries are genuine barbells. The entry uses exactly `|q|`
ordinary single-letter conjugations. Subsequent phases and the native
primitive detector are the coordinator's/Q's/U's existing algorithms,
with a one-line change allowing a freely reduced noncyclic starting
coordinate. This is a heuristic sampler, not an exhaustive graph search.

| q | Seed | Attempts | Source cap | Reverse-key lookup |
|---|---:|---:|---:|---|
| `Yx` | 20261122 | 2,000,000 | 100 | no |
| `XXyyy` | 20261123 | 2,000,000 | 100 | no |
| `YYYxx` | 20261124 | 2,000,000 | 100 | no |
| `Xy` | 20261125 | 3,000,000 | 120 | both saved corpora |
| `XXXXyyyy` | 20261126 | 3,000,000 | 120 | both saved corpora |
| `YYYYxxxx` | 20261127 | 3,000,000 | 120 | both saved corpora |

These six observed runs make 15,000,000 proposals, store 848,942 nodes
and classify 5,213,582 graphs **summed per run**, without a primitive or
reverse join. These sums are not cross-run union cardinalities. No native
detector budget stop occurs. The failure is not an AC obstruction.

Every selected best path is expanded into allowed elementary moves and
replayed from the literal initial AK(3) tuple: **26,130 strict instructions
in total**. The saved ledgers, not unexpanded macros, establish those
particular reachable endpoints. Full failed-run node journals remain
local scratch; the published archive retains the observed summaries,
source parameters, selected macro paths and complete strict ledgers.
Random-walk regeneration can depend on the C++ random-distribution
implementation; the archived exact words and ledgers do not.

The identical `q=Xy` procedure on AK(2), seed 20261121, finds a hidden
primitive and yields an exact **1,954-move** ordinary completion, raw
peak **149**, ending at literal `(x,y)`. The primitive exposure and full
completion use the already verified R/M/coordinator pipeline. This
calibrates bridge retention and strict compilation; it is not an improved
AK(2) bound or an AK(3) certificate.

## Independent review and reproduction

`verify_second_phase.py` imports no graph constructor, Gaussian solver,
SCC solver, or primitive search. It reconstructs quotient equivalence
relations, checks dual rows, full affine spaces, actual cycles and
potential inequalities, and verifies primitive words by a separate signed
mechanical-word test. T independently reviews the character spaces,
uses parameter roots/open cells rather than interval intersection, and
checks the primitive witnesses with Euclidean words rather than that
mechanical test. See [T's independent review](research-t-x-character-review.md).
Y separately checks all 42 source offsets, ordinary entries and the axes
deduction in [its scope review](research-y-rotation-scope-review.md). Its
shorter entry ledgers use 135 moves in total; X's separately archived
231-move entries remain valid. The intersecting-axes assumption concerns
the **endpoint** of the first pure-conjugation phase; intermediate axes
need not remain intersecting.

Four gzip/base64 transports hold exact data and selected strict ledgers.
The [artifact manifest](../certificates/x_artifact_manifest.json) gives
encoded and decoded lengths and SHA256 hashes. Compression is a transport,
not a mathematical operation. The archive verifier checks every hash and
then replays the finite proof data and actual elementary certificates:

```sh
python3 experiments/verify_x_archives.py --certificates certificates \
  --directory /tmp/x-review --output /tmp/x-review.json
```

Regenerate all 42 unbounded successor certificates, including the existing
independent voltage audit, with:

```sh
python3 experiments/rotation_successor_kernels.py --output /tmp/x-successors.json
```

The second-character constructor, exact interval solver, dual generator,
explicit primitive-witness search, and independent verifier are separately
published. `verify_x_archives.py` unpacks their exact four data inputs as
`x_extensions.json,x_parameters.json,x_duals.json,x_primitives.json` in its
requested directory. The final classification uses the exact parameter
records, superseding the initial bounded integer-menu statuses.

For the direct barbell sampler and saved-path compiler:

```sh
c++ -std=c++17 -O3 experiments/barbell_h_search.cpp -o /tmp/x-barbell
/tmp/x-barbell /tmp/cyclic22.tsv - - 20261122 2000000 150000 100 12 \
  /tmp/x-Yx xxxYYYY YxxyxYXYXy
python3 experiments/compile_barbell_paths.py /tmp/x-Yx --q Yx --n 3
```

The cyclic TSV is reconstructed by the already published
`cyclic_catalogue_to_tsv.py`. The variant source and its exact input words
are authoritative. Neither a heuristic failure, a primitive in a coarse
overgroup, nor the restricted two-phase theorem satisfies any of the four
original breakthrough goals. No such goal is achieved here.
