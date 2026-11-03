# T's independent review of X's character and successor-kernel audits

Date: 2026-11-02. **No AK(3) ordinary AC trivialization, unrestricted AC
obstruction, or proof/disproof of the conjecture is established.** I found
no flaw requiring X to weaken the restricted claims reviewed below. No
novelty or priority claim is made.

I read V's unbounded two-conjugate theorem and its graph/character proof,
then X's extension constructor, exact-interval computation, dual-certificate
generator, primitive-witness search, and separate verifier. I chose an
independent audit using a different real-parameter feasibility argument,
explicit completeness checks, and direct kernel-certificate replay. I
also reviewed X's later H1 and 42-rotation successor computations.

## 1. The exact extension problem

Start with one of V's 45 rank-three graphs K and its specified character
`chi: pi_1(K) -> Z`. Identifying another two K vertices and folding gives
an overgroup graph L. Choose a spanning-tree basis for L. Rewriting the
three old K basis loops gives a three-row integer matrix A; evaluating
the old character gives a column c. A character of L extending chi has
coordinate vector h satisfying

```
A h = c.
```

This is an exact linear statement about the specified parent character.
It is not a statement that an actual rank-two AC successor subgroup is
the whole kernel or that every possible useful character must extend
this one.

I independently enumerated the complete expected set of parent-index and
unordered second-vertex-pair triples, checked each occurs once, refolded
each quotient with deterministic union folding, and checked its full
projection and adjacency array. All **1,015** expected cases occur.
I reconstructed the spanning-tree coordinates, old character values,
graph ranks and affine-solution dimensions, importing no V/X constructor
or solver.

The final partition is:

| Cases | Exact conclusion |
| ---: | --- |
| 551 | The specified parent character has no real extension to L |
| 94 | A unique extension exists and its kernel is certified primitive-free |
| 259 | A one-dimensional extension family has an explicitly certified primitive-free member |
| 111 | No member of the one-dimensional family satisfies the sufficient SCC cycle-sign criterion |

For the 551 cases, an integer row u satisfies `u A=0` but `u c!=0`.
This directly disproves the real linear system, without trusting a
Gaussian-elimination failure flag. It also excludes a nonzero scalar
multiple of the specified pullback, since any such extension could be
divided by its nonzero scale.

All 551 quotient graphs have rank two. There is also a short unbounded
explanation of their failure. The ambient exponent columns of
`p=xxxYYYY` and `b=xyxYXY` are `(3,-4)` and `(1,-1)`, with determinant
one. For **any rank-two overgroup L of H0 inside F2**, the two integer
maps

```
H1(H0;Z) -> H1(L;Z) -> H1(F2;Z)
```

are two-by-two matrices whose product has determinant one. Both maps
are therefore unimodular. Any real or integer character of L killing
p and b must be zero. Since each specified parent character kills p,b
but sends its extra loop to one, it cannot extend to such an L. This
explains the rank-two failures beyond the particular 551 examples.
It is a limitation of the character extension strategy, not an AC
obstruction or a claim that every rank-two overgroup is primitive-free.

For every remaining case A has rank three. The graph ranks and vector
shapes show that there are exactly 94 zero-dimensional solution spaces
and 370 full one-dimensional spaces. Each saved particular vector solves
the system; each nonzero direction lies in its nullspace. Thus the
affine lines being tested really parameterize all extensions in those
370 cases, rather than a selected subfamily.

## 2. The 353 successful kernels

For each accepted character I checked inverse-edge antisymmetry and that
its evaluations on the old basis are one nonzero common scalar times the
old character. Therefore the image of the old kernel lies in its kernel.
Clearing rational denominators and dividing a common integer factor do
not change a kernel.

I independently rebuilt all eight signed-double-free automata and found
their strongly connected components with Tarjan's algorithm, separately
from X's mutual-reachability checker. Every saved cyclic component and
potential is checked. In total all **15,586** integer inequalities pass.
For a component C, sign epsilon and integer potential q, these are

```
q(v)-q(u) <= |C| epsilon w(u,v) - 1.
```

Summing around a nonempty closed walk forces nonzero total voltage. Every
ambient cyclic primitive uses one sign of each generator and avoids the
double of at least one of them, so it is covered by one of these eight
automata. Conjugating paths cancel their voltages. Hence the stated
kernel primitive exclusions hold at every word length, by the same
geometric deduction as [V's theorem](research-v-unbounded.md).

A failed potential search alone would prove nothing about primitive
existence. The next part checks a more precise, still method-specific,
negative conclusion.

## 3. All-real-parameter failure in the other 111 lines

Write a family as `h(lambda)=h0+lambda d`. Each actual directed cycle has
an affine voltage `a lambda+b`. V's sufficient criterion requires, within
each cyclic SCC, that all such cycle voltages have one strict sign.
Different SCCs may choose different signs.

X supplies actual cycle witnesses whose necessary constraints already
exclude every real lambda. I verified their state paths, closing arcs,
signed-double restriction, SCC membership, and exact affine coefficients.
There are **2,954** such witnesses in the 111 cases. Completeness of X's
simple-cycle enumeration is unnecessary for this exclusion: a subset of
necessary constraints with empty feasibility already suffices.

Instead of reusing X's interval-intersection argument, my implementation
partitions the real line at every rational root `-b/a` of the supplied
nonconstant voltages. On each open cell all signs are constant. It tests
one rational point per open cell and also every root itself, preserving
the strict inequalities. Across the families there are 476 roots and
**1,063 root/open-cell representatives**. No representative satisfies the
per-SCC same-sign constraints. This independently proves the all-real
failure of that sufficient criterion for every one of the 111 lines.

The conclusion is about the sufficient criterion, not an absence or
existence theorem for ambient primitives. In 58 cases there is a stronger
positive statement: an explicitly supplied ambient primitive loop has
both affine coefficients zero. I checked the graph loop and its base
path, and verified its primitive class using T's earlier signed Euclidean
representative routine, separately from X's mechanical-word test.
Consequently that primitive belongs to every coarse extension kernel on
the line. The other 53 cases receive no primitive-existence conclusion.
Even the 58 explicit primitives do not establish actual AC successor
reachability: the kernels are coarse overgroups.

## 4. H1 and all 42 initial rotation successors

The particular actual successor

```
H1 = <xxxYYYY, XYxyxY>
```

is reached from AK(3) in two strict moves: conjugate the second coordinate
by `Y`, then by `X`. Its displayed geometric basis is just an inversion
and permutation of these two generators:

```
(yXYXyx, yyyyXXX) = (rotated_b^-1, p^-1).
```

The marked theta paths `P=y`, `Q=XYxyx`, `R=xxxYYY` give this basis as
`(P Q^-1,P R^-1)`. Their initial and inverse-final labels are distinct,
so the graph is immersed, with path lengths `(1,5,6)` and eleven vertices.
I independently refolded the literal basis and checked all 55 quotient
graphs, character equations and **1,320 directed pullback equalities**.
All 440 signed automata, 340 cyclic SCCs and **1,178 potential
inequalities** pass. This validates this specific new instance of V's
unbounded arbitrary-two-conjugate theorem. Its bounded primitive-search
metadata is not used in the proof.

X subsequently applied the same construction to all literal rotations

```
<rot_i(xxxYYYY), rot_j(xyxYXY)>,     0<=i<7, 0<=j<6.
```

I independently checked their exact 42-offset coverage and source words,
refolded every source and quotient, and replayed their characters,
pullback coboundaries, SCCs and potentials. The complete audit passes:

| Independently checked object | Count |
| --- | ---: |
| Literal source groups | 42 |
| Quotient vertex identifications | 2,272 |
| Signed-double-free automata | 18,176 |
| Cyclic strongly connected components | 13,756 |
| Integer potential inequalities | 42,876 |
| Directed pullback equalities | 54,252 |

No V/X constructor, SCC implementation, potential solver or bounded
primitive enumeration is imported by these T audit programs. They share
T's explicitly named review helpers and the earlier T Euclidean routine.

For each of the 42 source groups H, the checked finite data and V's
geometric argument imply that every subgroup generated by two independent
conjugates of arbitrary elements of H is ambient primitive-free, without
a word-length bound. This is a restricted subgroup theorem.

The corresponding phase deduction must retain its hypotheses. A first
pure independent-conjugation phase from the literal AK(3) pair is covered
when its two axes intersect **at the end of that phase**. A common
conjugation then produces one of the 42 rotation pairs. Arbitrary Nielsen
mixing stays in that source subgroup; a further independent-conjugation
phase and a subsequent Nielsen suffix cannot expose an ambient primitive.
Intermediate axis intersections are irrelevant. Disjoint endpoint axes
with an arbitrary bridge and a preceding arbitrary H0 Nielsen prelude
are outside this theorem. [Y's separate scope review](research-y-rotation-scope-review.md)
checks this geometric deduction and the actual short rotation entries.
No unrestricted two-phase or global AC invariant is asserted.

## 5. Controls and reproduction

I reran X's own separate checker in addition to the new independent
programs; its 1,015-case counts and all finite certificate totals agree.
I also replayed the supplied AK(2) positive ledger through the repository's
strict verifier: it reaches literal `(x,y)` in 1,954 moves, with raw peak
149. This validates that particular control ledger; it is not AK(3) and
does not improve existing shorter AK(2) certificates. I did not duplicate
X's long heuristic barbell walks, and no completeness conclusion is drawn
from their failed searches.

The scripts accept plain JSON, gzip, or base64-wrapped gzip and record
decoded input SHA256 hashes. The H1 checker extracts offset `(0,4)` from
the public 42-source archive and independently checks its stated
inverse/permutation marking. From the repository root:

```sh
python3 experiments/t_x_review_cells.py certificates/v_vertex_identification_results.json certificates/x_second_phase_data.json.gz.b64 --output /tmp/t-x-cells.json
python3 experiments/t_x_review_h1.py certificates/x_rotation_successors.json.gz.b64 --output /tmp/t-x-h1.json
python3 experiments/t_x_review_all42.py certificates/x_rotation_successors.json.gz.b64 --output /tmp/t-x-all42.json
```

The concrete source artifacts and decoding instructions are published
with [X's report](research-x.md). The T results are
`certificates/t_x_review_cells_results.json`,
`certificates/t_x_review_h1_results.json`, and
`certificates/t_x_review_all42_results.json`. These are checked exact
certificates and mathematical deductions, not proof-assistant
formalizations. All four requested unrestricted breakthrough objectives
remain unachieved.
