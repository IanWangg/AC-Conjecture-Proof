# Rank-two cyclic basis sublevels and the energy of a necessary conjugation

Coordinating-agent investigation, 2026-11-02, with S's independent
mathematical critique and controls. **No AK(3) trivialization or
unrestricted obstruction is claimed.** No novelty claim is made.

The ordinary cyclic peak lower bound 23 was already proved by N/P.
Q/R subsequently excluded ambient primitives from every independently
conjugated subgroup in that component, even after unbounded Nielsen
suffixes. The remaining question here is whether a large Nielsen
excursion could return to another low-energy component before the next
conjugation. For a fixed rank-two subgroup, a geometric argument controls
that possibility at the level of cyclic states.

## 1. The exact statement

Let H be a rank-two subgroup of a finitely generated free group with a
fixed ambient basis. Write l(w) for ambient cyclically reduced length.
A cyclic basis state is the pair of ambient conjugacy classes of a free
basis (u,v) of H, ignoring individual inversion and coordinate order.
Its energy is l(u)+l(v).

**Basis-sublevel lemma.** If two such basis states have energy at most C,
they are joined under that cap by coordinate Nielsen moves in this
cyclic-state quotient. In particular they belong to the same ordinary
cyclic AC component under cap C.

This is **not** a claim about an actual Nielsen-only path between the two
literal ordered pairs. For example `(x,y)` and `(yxY,y)` both have cyclic
sum two, but no Nielsen multiplication can stay at sum two; their cyclic
states already coincide. Independent ambient conjugations realize any
required literal conjugacy adjustment at constant cyclic energy. No raw
length peak-reduction theorem is asserted.

The proof always starts with actual free bases. It never uses the false
criterion that arbitrary primitive words with unimodular exponent
vectors necessarily generate H.

## 2. Geometric translation lengths

The finite unbased core graph of H is immersed in the ambient rose.
After suppressing degree-two vertices, its rank-two topology is a rose,
theta, or barbell. Indeed its vertices have degree at least two and
the sum of degree minus two is two. Each essential path has a positive
integer length. Moving the basepoint globally conjugates H and changes
no cyclic lengths.

Choose a geometric free basis A,B. A primitive element of the abstract
free group H has a coprime exponent vector (a,b) in that basis. Its
ambient cyclic length depends only on this vector: Nielsen's primitive
conjugacy uniqueness holds inside H itself. A primary proof is
[Clay--Conant--Ramasubramanian, Corollary 4.4](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf).

The resulting translation-length functions are:

| Core | Geometric basis | Length of the primitive class (a,b) |
|---|---|---|
| Rose, petal lengths p,r | the two petals | p|a|+r|b| |
| Theta, parallel paths P,Q,R of lengths p,q,r | A=P Q^-1, B=P R^-1 | p|a+b|+q|a|+r|b| |
| Barbell, loops p,r and bridge q | A=left loop, B=bridge/right loop/return | p|a|+r|b|+2q min(|a|,|b|) |

Here these formulas describe **primitive classes**, not arbitrary words
with the same abelianization. Construct a positive primitive representative
by Euclidean induction and change generator signs. The less frequent
letter is isolated in its cyclic word. For the rose no path cancels. In
the theta case, opposite signs cancel the common P path at exactly
min(|a|,|b|) cyclic transitions, giving |a+b| traversals of P. In the
barbell the bridge is crossed exactly twice per minority-letter block,
giving 2 min(|a|,|b|) traversals. No further cancellation occurs in the
immersed core. Nielsen uniqueness transfers these counts to every
primitive representative.

The barbell function is **not a norm**: its value on (1,1) exceeds the
sum of its values on (1,0) and (0,1). Only the stated piecewise linearity
is used below.

## 3. Descent to a finite core of basis matrices

Use the common unimodular fan with successive rays

    (0,-1), (1,-1), (1,0), (1,1), (0,1).

Each formula in Section 2 is linear on every cone of this fan, with
strictly positive values on its nonzero rays.

The exponent columns of an actual H-basis form a unimodular matrix.
Invert either column to make its first coordinate nonnegative. If both
first coordinates are positive, their slopes cannot strictly straddle
an integer k in {-1,0,1}: with columns (a,b),(c,d), the two nonzero
integers b-ka and d-kc would have opposite signs, and

    |ad-bc|=|a(d-kc)-c(b-ka)| >= a+c >= 2.

This contradicts determinant magnitude one. The columns therefore lie
in a common fan cone. If one column is vertical, the other's first
coordinate is one. Its slope is an integer. Orient the vertical column
toward that slope when it is nonzero; the pair lies in an outer cone.
The remaining zero-slope case is exactly the signed/permuted axis basis
{(1,0),(0,1)}. This exception is essential: those two columns straddle
the ray (1,1), despite being unimodular.

Within a common unimodular cone, write both columns in its two-ray
coordinates. They are nonnegative integer unimodular columns. Unless
they are the two rays themselves, one dominates the other coordinatewise.
To see the exceptional case, if (s,t),(u,v) cross with s>u and t<v,
then

    sv-tu = u(v-t)+(s-u)t+(s-u)(v-t).

For this to be one, u=t=0 and s=v=1. Thus it is exactly the ray pair.

Subtract the dominated column from the dominating one. This is a legal
coordinate Nielsen move with an inverted donor. It stays in the cone,
strictly decreases the recipient's translation length by the positive
length of the donor class, and decreases its nonnegative integer
coordinate sum. Repetition terminates at a ray pair. The argument
requires no discretization of metric weights beyond positivity.

All possible boundary pairs form five unoriented vertices, using

    A=(1,0), B=(0,1), C=(1,-1), D=(1,1):
    {A,B}, {A,C}, {B,C}, {A,D}, {B,D}.

Their Nielsen flip graph is two triangles sharing {A,B}.
For rose and barbell, L(C)=L(D)>=L(A)+L(B), so each non-axis pair
strictly descends to {A,B}. For theta put

    alpha=p+q, beta=p+r, gamma=q+r, delta=2p+q+r.

The D-side vertices strictly descend to {A,B}. The other three vertices
have energies p+q+r plus p,q,r respectively, and are directly connected
by Nielsen cycle exchanges. Each descends to a minimum; any tied minima
are joined at the same energy. Consequently the minimum basis energy is

    p+r                         for rose or barbell,
    p+q+r+min(p,q,r)            for theta.

Every basis state descends without increasing energy to this connected
minimum set. Reverse the descent from a second state to join the two
within the maximum of their endpoint energies. The operations act on
actual H-bases throughout. A matrix column gives the correct cyclic
coordinate class by primitive conjugacy uniqueness in H, so no joint
literal-word equality or low inner-automorphism realization is assumed.
This proves the basis-sublevel lemma.

## 4. Consequence for ordinary AK(3) moves

At every ordinary AK(3) tuple the exponent matrix remains unimodular.
The subgroup generated by its two relators therefore has rank two, and
the two generators form a free basis of it. For example this last fact
also follows by folding the initial rank-two two-loop graph: since the
final subgroup still has rank two, there can be no rank-lowering fold.

Call a conjugation subgroup-changing if it changes the subgroup generated
by the two current relators. Inversion and coordinate multiplication
preserve that subgroup. Between two subgroup-changing conjugations, all
tuples are bases of one fixed H, even if lengths grow arbitrarily.

**Conjugation bottleneck.** Before the first primitive coordinate in any
ordinary AK(3) trivialization, at least one subgroup-changing conjugation
must occur at cyclic total energy at least **23**.

Suppose otherwise. Every subgroup-changing conjugation before the first
primitive would have energy at most 22. Its source and target have the
same cyclic state. Start at AK(3), in N/P's complete component C22.
Inductively, between consecutive such conjugations both endpoint bases
have energy at most 22. The lemma joins their cyclic states under that
cap, so the next source is still in C22; its conjugated target is in C22
as well. The initial constant-H phase is handled in the same way.

After the last subgroup-changing conjugation, Q/R's all-tail theorem
makes that subgroup primitive-free at every word length. A remaining
constant-H phase can never expose a primitive, however large its energy.
If there were no subgroup-changing conjugation, the initial primitive-free
subgroup already gives this contradiction. Thus the supposition fails.

This is an existence assertion about **some** necessary conjugation
before the first primitive. It does not say that the last such
conjugation has energy at least 23: an earlier large excursion may enter
another low-energy component. S's separate last-conjugation corollary
is the component-membership statement, not a numerical bound on that
particular move.

The weaker assertion that a full trivialization has some subgroup-changing
conjugation at energy at least 23 also follows from the basis-sublevel
lemma and N/P's cap-22 closure alone: compress every constant-H phase
between low endpoints, including the final standard basis. The stronger
before-first-primitive formulation above uses Q/R's unbounded subgroup
exclusion.

No larger numerical peak bound results. Conjugations at energy 23 or
higher remain possible, so this proves neither non-AC-triviality nor
AC triviality. It identifies which operation must cross the existing
barrier and guides further coupled-coordinate searches.

## 5. Controls and review

`nielsen_tree_peak_controls.py` checks the length formulas by substituting
signed Euclidean primitive words into literal free graph-path words. It
also exhausts unimodular matrices in a finite box and verifies descent
and finite-core minimum connectedness for several positive weight choices.
The saved run has 4,416 formula checks and 16,608 matrix descent controls.

S independently critiques the fan argument, catches the axis exception
and actual-Nielsen-only overstatement, and checks a separate implementation.
Those corrections are incorporated above. The controls support conventions;
the unbounded conclusion is the geometric/cone proof, not extrapolation
from the tested boxes. See S's independent review for its exact scope.

    python3 experiments/nielsen_tree_peak_controls.py --output /tmp/nielsen-tree-controls.json

All four full AC goals remain unachieved.
