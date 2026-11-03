# U independent review: an unbounded one-phase primitive exclusion

Date: 2026-11-02. **This is a restriction on one phase, not a resolution
of AK(3) or the ordinary Andrews–Curtis conjecture.** The construction and
new [phase theorem](research-v-unbounded.md) are V's work. U independently checked its geometry,
algebra and finite certificates using a separate implementation.

Put `H0=<xxxYYYY,xyxYXY>` in the ambient free group `F(x,y)`. The conclusion
under review is the following unrestricted-length statement:

> For any `u,v` in `H0` and any `a,b` in `F(x,y)`, the subgroup
> `<a u a^-1,b v b^-1>` contains no ambient primitive element.

No joint basis assumption on `u,v` is required. In particular, there is
no bound on an initial Nielsen prelude inside `H0`, the lengths of its
two endpoint words, either independent conjugator, or a later Nielsen
suffix inside the resulting subgroup.

This statement does not claim invariance after a second arbitrary
subgroup-changing phase. A general AC path may alternate Nielsen moves
and independent conjugations repeatedly; the theorem does not cover all
such paths.

## Geometry and character containment

Use the ten-vertex folded inverse graph `Gamma` representing `H0`.
Every freely reduced word of `H0` labels a based closed loop in `Gamma`.
Cyclic reduction removes inverse prefix/suffix paths and leaves a closed
loop at some graph vertex. Every cyclic rotation of the remaining word
is another closed loop at a vertex of `Gamma`.

Q/R's axes argument reduces arbitrary independent conjugators of two
nontrivial words to cyclic rotations of their cyclic reductions when
their conjugated axes intersect. If the axes are disjoint, the folded
subgroup graph is a barbell. A cyclic path crossing its bridge reads
both signs of some ambient letter, whereas a cyclic primitive in rank
two uses one sign of each generator. A primitive therefore would have
to lie in a single circle. A primitive cannot be a proper power, so this
would imply a primitive was already in `H0`, contrary to its exact
initial negative certificate. If either `u` or `v` is trivial, the same
cyclic-subgroup argument suffices.

It remains to consider two cyclic loops at vertices `alpha,beta` of
`Gamma`. If `alpha=beta`, simultaneously transport their common base
to the original basepoint. The resulting subgroup lies inside `H0`
and is primitive-free.

For `alpha != beta`, identify those vertices and fold, obtaining an
immersed inverse graph `K`. Every such graph has rank three in V's
certificate. Its integer edge weights `w(e)` are antisymmetric under
edge reversal and define a homomorphism `chi:pi1(K)->Z` by adding edge
weights along a loop. The pullback of these weights to `Gamma` is a
coboundary: there is an integer vertex potential `d` satisfying

```
w(image of e) = d(terminal e) - d(initial e)
```

on every original directed edge. Consequently **every original closed
loop at every original vertex** has zero voltage. The two selected loops
become based at the same quotient vertex, and each has zero voltage.
Their generated subgroup also has zero voltage. Transporting its base
to the base of `K` does not change loop voltage.

This direct coboundary check establishes the required containment without
assuming that the transported loops jointly form a basis. In V's
equivalent normalization, if `s_alpha,s_beta` are original spanning paths,
`t=s_alpha s_beta^-1` has `chi(t)=1`, and the common conjugate of the pair
has the form `(A,t B t^-1)` with `A,B in H0`. U checked this normalization
as well. Nonzero character and rank-three statements are useful audit
conditions; the loop containment itself follows directly from the
pullback coboundary.

## Why the finite potentials exclude primitives of every length

Every cyclic primitive word in rank two uses a signed alphabet among
`xy,xY,Xy,XY` and avoids at least one of the two signed double letters.
This is the standard signed Christoffel/Euclidean description of primitive
classes, also used in Q's direct criterion. If the absolute first count
is at least the second, its cyclic representative has no double of the
second letter; the opposite count inequality reverses the roles. The
single-letter cases are included by forbidding the other letter's double.
Primitive conjugacy uniqueness makes the same condition hold for all
cyclic rotations. See
[Clay–Conant–Ramasubramanian, Section 4](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf)
and [Q/R's prior proofs](research-r.md).

For each signed alphabet and choice of forbidden double, V constructs a
finite edge-state automaton. A state is an available signed outgoing
edge. An automaton transition follows that edge and then chooses the
next signed edge, omitting the forbidden double. Its integer weight is
the voltage of the edge just traversed. Thus a compatible cyclic word
corresponds to a directed closed walk with exactly the same total voltage.
Every directed closed walk is wholly inside one strongly connected
component (SCC).

For each cyclic SCC of size `N`, the certificate gives a sign
`epsilon in {-1,+1}` and integer potential `h` such that every internal
automaton arc `e:r->s` satisfies

```
h(s)-h(r) <= N*epsilon*w(e)-1.
```

Summing this inequality around any nonempty closed walk of length `L`
gives

```
N*epsilon*total_voltage >= L > 0.
```

Therefore that walk cannot have zero voltage. Different SCCs may use
different signs; a closed walk cannot combine them. Singleton SCCs with
self-loops are checked too. A graph with no cyclic SCC is vacuous in
that alphabet, as it admits no compatible cyclic loop.

If a zero-voltage based primitive loop initially has a conjugating
prefix, cyclic reduction removes that prefix and its inverse. Their
voltages cancel. The remaining cyclic primitive still has zero voltage,
which the finite SCC potentials exclude. Thus the certificate rules out
primitive elements in the relevant kernel at **all word lengths**, not
merely the bounded words examined in an earlier exploratory scan.

## Independent finite check

`u_verify_voltage_phase.py` imports no V/R folding, character, SCC or
Bellman–Ford implementation. It uses its own equivalence-relation
folding and independently folds the literal original AK(3) words.
For each identification it checks the complete quotient graph and vertex
projection, inverse arcs, rank, integer character and pullback coboundary.
Its SCCs are computed from transitive reachability, rather than V's
two-pass DFS. It then checks the supplied potentials by exact integer
inequalities rather than trusting a Bellman–Ford result or status flag.

| Independent check | Count |
| --- | ---: |
| Original native negative-map states | 72 |
| All unordered distinct vertex identifications | 45 |
| Rank-three quotient graphs and projections | 45 |
| Directed original-edge coboundary equalities | 990 |
| Extra-generator voltage normalizations | 45 |
| Signed forbidden-double automata | 360 |
| Cyclic SCCs | 302 |
| Integer potential inequalities | 822 |

All checks pass. The independent initial negative certificate is important
for coincident cut vertices and the disjoint-axis case.

The AK(2) positive calibration checks that this sufficient exclusion
does not incorrectly pass a known successful one-phase route. U
independently folds the eight-vertex AK(2) original graph and locates the
actual successful rotated pair `(XXyyy,YXyyXyx)` at cut vertices `(3,7)`.
Their quotient still has rank three. U independently constructs its
normalized character, with extra generator `xYX`, and finds the primitive
`xYxYYxYY` as a zero-voltage loop at vertex zero. A strict cycle-sign
potential cannot exist on the SCC containing that loop. Thus rank three
alone is not an obstruction; the AK(3) weighted-cycle certificates do
essential additional work.

The exact input hashes and results are in
`results/u_voltage_phase_review.json`. From the published checkout:

```sh
python3 experiments/u_verify_voltage_phase.py certificates/v_vertex_identification_results.json certificates/v_voltage_cycle_results.json --initial-absence certificates/u_native_initial_absence.json --output /tmp/u-voltage-review.json
```

V publishes the finite construction and full proof. U's independent
review supports the stated single-phase theorem. It supplies neither a
global invariant under AC moves nor an AK(3) trivialization.
