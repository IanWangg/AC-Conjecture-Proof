# Research O: finite reduction of arbitrary relative conjugating tails

Date: 2026-11-02. Status: an unbounded theorem for a restricted subgroup
family, supported by explicit finite graph certificates. **No AK(3)
trivialization, nontriviality proof, or global AC invariant is claimed.**
No novelty or priority claim is made.

## Previous work read and independent choice

Before choosing a direction I read the repository's current README, the
coordinating agent's first-hump atlas, M's initial subgroup theorem and
first-hump follow-up, and J's initial primitive-replacement theorem. The
existing 5,632-pair catalogue expressly excluded arbitrary independent
conjugating tails. I independently chose to address that gap using the
geometry of folded subgroup graphs.

P independently chose the same geometric idea. After we compared our
initial observations, I developed the finite-tail reduction and a
self-contained initial-AK(3) certificate, while P independently reviewed
the reduction and extended the finite checks to the first-departure
catalogue and later waypoints. N independently developed a different
analytic argument for the uniform initial family using braid matrices.
These complementary investigations are credited separately; the finite
AK(3) graph check here does not depend on N's matrix argument.

The primary graph background used is
[Kapovich–Myasnikov, *Stallings Foldings and Subgroups of Free Groups*](https://web.stevens.edu/algebraic/alexeim/Teaching/GroupTheory626/graph5.pdf).
The primitive conjugacy fact is Nielsen's rank-two theorem, with the
modern proof in
[Clay–Conant–Ramasubramanian, Corollary 4.4](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf).

## 1. A rank-two finite-tail reduction lemma

Let F=F(x,y), let u,v be nonempty cyclically reduced words which are not
primitive in F, and write

    H(q)=<u, q v q^-1>,       L=floor(|u|/2)+floor(|v|/2).

**Lemma.** If H(q) contains no ambient primitive for every reduced q of
length at most L, then H(q) contains no ambient primitive for **every** q
in F, with no length bound.

Here primitive means a member of a free basis of the ambient group F. The
lemma is a finite reduction of this specific subgroup question, rather
than an AC invariant or an assertion that arbitrary finite searches prove
an unbounded result.

### Double-coset normalization preserves the subgroup exactly

Choose q0 of minimum reduced length in the double coset

    <u> q <v>.

Such a representative exists because word length is a nonnegative integer.
For any integers a,b, replacing q by u^a q v^b changes the second
generator to

    u^a (q v q^-1) u^-a.

Together with u this generates exactly the same subgroup. Thus
H(q0)=H(q), not just an isomorphic or quotient subgroup.

### Long minimal representatives leave a genuine bridge

Represent H(q0) by a circle labeled u and a disjoint circle labeled v,
joined by a path labeled q0, with the basepoint on the u-circle. Include
inverse arcs. The circles are individually folded because their words
are cyclically reduced; the joining path is reduced. Before its endpoints
meet, the only possible folds consume the joining path from its two ends.

Suppose c letters are consumed at the u end. They follow one direction
around the u-circle, since a reduced path on a circle cannot reverse
direction. If c exceeds |u|/2, left multiplication of q0 by the opposing
power u or u^-1 shortens it. If c is at least |u|, a whole copy cancels;
otherwise the reduced product has length at most

    |q0|+|u|-2c < |q0|.

Both alternatives contradict minimality. Hence at most floor(|u|/2)
joining edges can be consumed there. The same argument at the v end,
using right multiplication by v or v^-1, gives floor(|v|/2).

Consequently, if |q0|>L, the folds stop before their endpoints meet. The
resulting graph consists of the two original circles, possibly with their
joining attachment points moved around the circles, and a nonempty
intervening path. It is folded: a possible additional fold at either
attachment would mean the corresponding endpoint-consumption had not
stopped. Every intervening edge is a bridge.

### A rank-two primitive cyclic loop cannot cross that bridge

Every cyclically reduced primitive of F2 uses at most one sign of x and
at most one sign of y. One way to derive this fact is to construct a
positive primitive for each coprime nonnegative exponent vector by
Euclidean induction, invert either ambient generator for other signs,
and apply Nielsen's uniqueness of primitive conjugacy classes with a
given exponent vector. Cyclically reduced conjugate words differ only
by cyclic rotation.

Any closed path that crosses a bridge must cross it in both directions,
and hence uses both signs of its edge label. Therefore a cyclic loop
whose label is a rank-two primitive cannot cross any intervening bridge.
It must lie in one of the two circles. Its label is then a cyclic
rotation of a nonzero power of u or v, which is not primitive: exponent
vectors exclude proper powers, and u,v themselves were assumed
nonprimitive.

Finally, if an element of H(q0) is primitive but is not cyclically reduced
as a based word, remove its conjugating prefix and suffix. Folded inverse
paths are unique, so the cyclic middle word reads a closed path at the
endpoint of that prefix. The bridge argument applies to that closed
path as well; it does not require it to be based at the distinguished
vertex.

This excludes a primitive when |q0|>L. When |q0|<=L, the finite hypothesis
excludes it. The lemma follows.

The rank-two condition matters: the sign restriction used for primitive
cyclic words is special to F2. The argument is not asserted in higher
rank.

## 2. Application to all independently conjugated initial AK(3) relators

Put

    p=xxxYYYY,    b=xyxYXY,    X=x^-1, Y=y^-1.

The finite cutoff in the lemma is

    floor(7/2)+floor(6/2)=6.

There are exactly 1+4(1+3+...+3^5)=1,457 reduced words q with |q|<=6.
The script computes the folded graph of every literal pair

    (p, q b q^-1).

They give 1,378 distinct based graphs. Each graph has an explicit
certificate that it contains no cyclic loop labeled by a primitive word
of **any** length. Combining the finite certificates with the lemma gives:

**Theorem.** For all a,c in F(x,y), the subgroup

    <a p a^-1, c b c^-1>

contains no ambient primitive element.

Indeed simultaneous conjugation by a^-1 gives H(a^-1 c), and ambient
conjugation preserves primitivity. Inverting either displayed generator
also preserves its cyclic subgroup. Independent rotations are already
included because they are conjugations.

This statement extends M's initial fixed-subgroup result to arbitrary
independent conjugating tails. N independently obtains a uniform AK(n)
version by a different analytic route. The proof here establishes the
specific n=3 statement without that analytic input.

## 3. What the finite graph certificate proves

For each signed alphabet {s,t} among xy,xY,Xy,XY, form the directed edge
graph of the folded subgroup graph. An edge-state can be followed by a
second edge-state when their endpoints match. Delete all transitions
whose two labels are ss, and separately delete all transitions whose two
labels are tt. The certificate supplies a topological order for each
resulting graph.

Both graphs are acyclic in every case. Hence any nonempty signed cyclic
loop contains both doubled-letter patterns ss and tt. This is impossible
for a primitive cyclic word of rank two. To justify the last claim,
Euclidean induction supplies a positive primitive representative for its
exponent vector. If one positive count is larger, the outer substitution
isolates the less numerous letter; if both coprime counts equal one, xy
has neither double. Nielsen uniqueness transfers this isolation property
to every primitive cyclic representative. A one-generator primitive loop
also avoids at least one of the doubles and is excluded by the same
acyclicity test.

The certificate therefore proves all-length primitive absence within
each of the 1,378 finite subgroup graphs. There are 11,024 explicitly
checked topological orders. The verifier:

- enumerates all 1,457 q afresh;
- folds every pair using a local batch union-find implementation;
- matches the exact based graph to the stored graph;
- checks inverse arcs and every topological-order inequality;
- checks both isolated cyclic factors p,b for the long-tail case;
- confirms that the free-basis graph (x,y) fails the exclusion test.

During review I independently compared every graph to M's earlier
one-fold-at-a-time implementation; all 1,457 encodings agree. The
published verifier has no dependency on M's implementation.

## 4. Scope and implications

Arbitrarily conjugating and inverting the **two original individual
relators**, followed by arbitrary Nielsen operations, cannot produce a
primitive coordinate: the final Nielsen operations preserve the subgroup
in the theorem. This rules out that restricted completion strategy at
unbounded word length.

The statement does **not** cover arbitrary initial Nielsen mixing before
the individual conjugations, or later interspersed conjugations and
Nielsen operations. Those can change which two elements are being
conjugated, and can leave this subgroup family. Thus the result gives
neither non-AC-triviality nor a new global cyclic/raw peak bound. It is
not a proof that additional conjugations of arbitrary later tuple bases
are harmless.

P uses the same independently reviewed finite-tail lemma with a separate
implementation to extend the first-departure catalogue and the two new
waypoints. Those larger finite checks and their precise scope belong to
P's report; they are not silently included in this smaller certificate.

## Reproduce

All files use only Python's standard library. Put the script in
`experiments/` and the certificate in `certificates/`:

```sh
python3 experiments/arbitrary_tail_certificate.py \
  --verify certificates/arbitrary_tail_graphs.json.gz.b64 \
  --output results/arbitrary_tail_results.json
```

To regenerate and immediately verify the certificate:

```sh
python3 experiments/arbitrary_tail_certificate.py \
  --certificate /tmp/arbitrary_tail_graphs.json.gz.b64
```

The compressed certificate has 68,181 ASCII bytes. Its decoding and all
checks are handled by the script. The finite verification returns PASS;
the passage to all conjugating tails is the proved reduction lemma, not
an extrapolation of those finite data. The original four breakthrough
objectives remain unachieved.
