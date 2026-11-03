# S: independent review of the rank-two cyclic basis-sublevel argument

Date: 2026-11-02. **No AK(3) trivialization or unrestricted AC invariant
is established.** No novelty claim. I read the coordinating agent's
concrete [cyclic basis-sublevel proof](nielsen-cyclic-sublevels.md) and
its control implementation after independently critiquing the proposed
argument. The repaired statement and its stated conjugation consequence
have no material gap that I can find.

## The quotient and the two necessary cautions

The theorem concerns pairs of **ambient individual conjugacy classes**
of actual free bases of a fixed rank-two subgroup H, with inversion and
coordinate order ignored. It does not assert a low path between two
literal ordered bases using only elementary Nielsen products.

The distinction matters even for H=F(x,y). Both `(x,y)` and `(yxY,y)`
have total cyclic length two. Under elementary inversions, permutations,
and signed products, every first multiplication has cyclic total at
least three. Inversions/permutations alone cannot produce `yxY`.
Thus literal Nielsen-only sublevels need not be connected. Their cyclic
states already coincide, and ordinary ambient conjugation realizes the
literal adjustment at constant cyclic length. The published theorem
explicitly retains this quotient; no raw-peak statement follows.

The barbell translation-length function is also not a norm: the class
(1,1) crosses its bridge twice, making its length greater than the sum
for (1,0) and (0,1). The proof correctly needs only linearity on specified
cones, not convexity or a triangle inequality.

## Independent mathematical checks

For a geometric free basis of H, its primitive conjugacy classes are
determined by their H-abelianization vectors. This is Nielsen uniqueness
inside the abstract rank-two H, with a primary proof in
[Clay--Conant--Ramasubramanian, Corollary 4.4](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf).
It is not a claim that an arbitrary H-word's length is determined by
its abelianization, nor that arbitrary primitive representatives with a
unimodular exponent matrix generate H.

The three geometric formulas in the proof are correct:

    rose:     p|a|+r|b|,
    theta:    p|a+b|+q|a|+r|b|,
    barbell:  p|a|+r|b|+2q min(|a|,|b|).

In the theta case opposite signs remove the common path at precisely
the minority-letter transitions. In the barbell each minority block
corresponds to one pair of bridge traversals. The Euclidean primitive
representative has the needed isolated-minority-letter property;
Nielsen uniqueness then supplies every primitive class. Folded immersion
of the core prevents additional cancellation.

The original informal slope statement needed an axis exception. The
columns (1,0),(0,1) are unimodular and straddle (1,1), so a blanket
non-straddling assertion is false. The concrete proof now handles
vertical columns separately. With both first coordinates positive,
strict straddling of an integer ray forces determinant magnitude at
least the sum of those positive coordinates, hence at least two.
With a vertical column, the other first coordinate is one, so its
slope is an integer; sign choice places the pair in an outer cone
unless it is the axis basis itself. These cases cover every matrix.

Within a unimodular cone, nonnegative unimodular columns are comparable
coordinatewise unless they are the two boundary rays. Subtracting the
dominated column remains inside that same cone. Each geometric length
function is linear there with positive ray values, so the recipient's
length decreases by the donor's positive length. The integer coordinate
sum also decreases, giving termination without assumptions on metric
integrality.

The terminal five ray pairs form two triangles sharing the axis basis.
For rose and barbell, the two mixed classes A+B and A-B are at least as
long as A and B together, so each non-axis core vertex descends directly
to the axis vertex. For theta, the A+B-side also descends there. The
other three core energies equal p+q+r plus respectively p,q,r, and every
pair is connected by a direct signed Nielsen flip. All minimum vertices
are therefore connected under their common energy.

Every reduction operates on an actual basis, maintaining that fact by
Nielsen operations. At the quotient join, primitive conjugacy uniqueness
identifies the required cyclic coordinate classes; no unproved low
realization of an inner automorphism or joint literal-word equality is
needed. This proves the intended quotient sublevel connectivity.

For the conjugation consequence, a constant-H phase may include
subgroup-preserving ambient conjugations as well as Nielsen operations.
Its two-generator tuples are still bases of the same rank-two H, so
the endpoint argument applies to the entire phase. If every
subgroup-changing conjugation before the first primitive were at energy
at most 22, induction would keep all its low phase endpoints in C22.
Q/R's all-tail primitive-free subgroup theorem then excludes the final
unbounded constant-H suffix. I find this use of the lemma sound.

## Independent finite controls

`s_nielsen_length_controls.py` imports none of the coordinating agent's
control routines. It compares symbolic edge counts after actual free
cyclic reduction of graph-path words, rather than merely evaluating the
same weighted formula twice. The saved run passes:

- 3,072 symbolic rose/theta/barbell path checks on 1,024 signed coprime
  vectors with both coordinates of magnitude at most twenty;
- all 2,920 determinant-magnitude-one matrices with entries of magnitude
  at most twelve: 2,880 strict symbolic cone descents, 32 boundary cases,
  and the eight signed/ordered axis exceptions;
- 5,232 finite-core sublevel connectedness checks, using every positive
  integer edge-weight triple with entries at most eight;
- the actual Nielsen-only cyclic-energy-two counterexample above.

These are bounded implementation and convention checks. They do not
replace the all-vector geometric/cone proof, and do not by themselves
establish an unbounded peak-reduction theorem.

## A sharper way to identify the necessary conjugation

In a proposed finite AK(3) path, let T be the first primitive-coordinate
time and let tau be the last preceding visit to C22. Such a visit exists
because the initial tuple belongs to C22. Q/R implies that the subgroup
at tau is primitive-free at every length, so a subgroup-changing
conjugation must occur between tau and T.

Take the **first** such conjugation after tau. Its source is a basis
of the same H as the tuple at tau. If its energy were at most 22,
the basis-sublevel lemma would put its cyclic source state back in C22.
Its conjugated target has the identical cyclic state and occurs later
than tau, before the first primitive; this contradicts the definition
of tau. Therefore this first subgroup-changing conjugation after the
last C22 visit has cyclic total energy at least 23.

This is compatible with the last subgroup-changing conjugation being
low: an earlier high excursion may reach another low component. It
neither increases the known numerical peak bound nor constrains all
unbounded ordinary AC moves. It identifies a particular operation at
which the existing barrier must be crossed.

## Reproduce and scope

```sh
python3 experiments/s_nielsen_length_controls.py \
  --output /tmp/s-nielsen-length-controls.json
```

The saved output is `results/s_nielsen_length_control_results.json`.
The proof concerns cyclic states of bases of a rank-two subgroup; it
does not claim literal Nielsen-only sublevel connectivity, raw peak
reduction, unrestricted AC triviality/nontriviality, or a new primitive
waypoint for AK(3).
