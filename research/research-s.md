# Research S: the three remaining power-nine primitive-replacement exclusions

Date: 2026-11-02. **No AK(3) trivialization, unrestricted AC obstruction,
or proof/disproof of the AC conjecture is established.** No novelty or
priority claim is made. The new conclusions are unbounded exclusions
for three specified frozen-coordinate quotient problems.

## Previous reading and independent direction

Before choosing a direction I fetched the repository README and read
N's cyclic-search report, P's full cap-21/22 independent review, O's
whole-subgroup review, the coordinating agent's first-departure atlas,
and L's branch calculations. The cap-22 search excludes a primitive
coordinate below cyclic peak 23, but it does not exclude a primitive
replacement obtained by an arbitrarily long sequence using one fixed
relator. The atlas still listed three of its six signed-symmetry classes
of length-nine power replacements without such an exclusion.

I independently chose those three deletion quotients, seeking an actual
primitive replacement of the braid relator. Q and R independently chose
the arbitrary-tail hidden-primitive gap, so this investigation did not
duplicate their direction. The attempted positive route instead produced
finite conjugacy obstructions for all three remaining cases.

Put F=F(x,y), with X=x^-1 and Y=y^-1, and write

    p=xxxYYYY,       b=xyxYXY,
    rD=XXXyxYXyy,   rE=XXYxxYYxy,   rF=XXyXYxYxy.

These are classes D/E/F in the six-class ordering of the
[first-departure atlas](first-hump-atlas.md). The other classes were
already covered by K and L. The letters D/E/F here label branches,
not earlier researchers with those names.

## The result

**Theorem.** For each r in {rD,rE,rF}, no primitive word u in F has image
conjugate to b or b^-1 in the one-relator quotient F/<<r>>.

There is no bound on u, the conjugator, or any AC ledger realizing a
replacement. Thus none of these three first-departure pairs (r,b) can
be completed by replacing the braid with a primitive while keeping the
other relator's normal closure fixed.

Together with K's/L's previous three cases, this completes the analogous
exclusion for all six power-nine signed-symmetry classes. In the reverse
coordinate, J's braid-quotient theorem already excludes a primitive
replacement of the power word because every atlas word has braid image
conjugate to p or p^-1. These statements do not classify later updates
of both coordinates and are not invariants under unrestricted AC moves.

The three tuples are actually reachable by short ordinary AC paths.
Using the coordinating agent's existing packed cap-18 checkpoint and its
coordinate-tracking path compiler gives the following exact ledgers:

| Literal endpoint from AK(3) | Strict elementary moves | Raw total peak |
|---|---:|---:|
| (rD,b) | 21 | 17 |
| (rE,b) | 10 | 15 |
| (rF,b) | 13 | 17 |

All pass the separate `elementary_verify.py`. These are newly recorded
small ledgers from an already classified component, not new escapes
from the earlier search region. Their discovery infrastructure and
compiler are credited to the coordinating agent and D/N/P's prior work.

## 1. The primitive families forced by the integer character

The characters below kill the corresponding relator r and send the
chosen oriented braid beta to one:

| Branch | chi(x),chi(y) | beta | A free basis (a0,t0) of the original F |
|---|---|---|---|
| D | 2,3 | b^-1 | a0=x(xY)^2, t0=yX |
| E | 2,1 | b | a0=xY^2, t0=y |
| F | 0,1 | b^-1 | a0=x, t0=y |

For D the inverse basis formulas are x=a0 t0^2 and
y=t0 a0 t0^2. For E they are x=a0 t0^2,y=t0. These are exact free-word
identities, checked in both directions by `s_branch_models.py`.

Suppose a primitive u maps to a conjugate of beta in F/<<r>>. Its
integer character is one. In the displayed free basis its exponent
vector is therefore (k,1) for an integer k. The primitive word a0^k t0
has this vector. Nielsen's rank-two primitive conjugacy uniqueness says
that u is conjugate in F to this representative. A primary proof is
[Clay--Conant--Ramasubramanian, Corollary 4.4](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf).
If a primitive maps to the opposite braid orientation, invert it first.
Consequently it suffices to exclude the displayed infinite family for
each branch, rather than guess a finite list of primitive words.

## 2. Exact models and the finite representations

Use lower-case a,b,c for fiber generators and t for the stable letter.
Their uppercase versions denote group inverses. All representations
below have the rule

    t h t^-1 = alpha(h).

The same letters appearing in an algebra monomial later denote
augmentation variables; a unit generator a is then represented by 1+a.
No ambient generator change is inserted into an AC certificate.

### D: an endomorphism mapping-torus presentation

Take t=yX and a=x(xY)^2, so x=a t^2,y=t a t^2. Put b=t a t^-1.
The defining relation becomes

    alpha(a)=b,      alpha(b)=(A b)^2.

Here alpha is an endomorphism of the free fiber; its abelianization has
determinant two. **Free-group surjectivity is not assumed.** For the
obstruction we only need the finite representations constructed below,
where alpha really is an automorphism.

For an exact Tietze check, in letters a,t set a_i=t^i a t^-i. If
R_D=a_2^-1 A a_1 A a_1 and P_D=t^-2 A t^-4, direct free reduction gives

    rD(a t^2, t a t^2) = P_D R_D P_D^-1.

Hence the relation is precisely a_2=(A a_1)^2, yielding the displayed
presentation after introducing b=a_1. Reading the oriented braid gives

    b_original^-1 = (baBabAbA)t.

The candidate a0^k t0 maps to a^k t.

### E: a rank-three free-by-cyclic presentation

Take t=y,a=xY^2,b=t a t^-1,c=t^2 a t^-2. Then x=a t^2,y=t, and

    alpha(a)=b,     alpha(b)=c,     alpha(c)=B a c^2.

Its inverse is a->a c B^2,b->a,c->b. Both compositions freely reduce
to the identity on every fiber generator.

Let a_i=t^i a t^-i. An exact free-word identity is

    t^5 rE(a t^2,t) t^-5 = a_3^-1 a_1^-1 a_0 a_2^2.

This is exactly a_3=a_1^-1 a_0 a_2^2. The braid and primitive candidates
have forms

    b_original=(aBac)t,      a0^k t0 = a^k t.

### F: transfer to K's already obstructed rank-two model

Put a=Yxy,b=x,t=Xy, so x=b,y=b t. The relation becomes

    alpha(a)=b,       alpha(b)=aB,

the same automorphism as K's second-hump model. Its inverse sends
a->ba,b->a. The first stable-letter relation is an exact free identity
in x,y. If R=t b t^-1 b A in the original words, then

    rF = a^-1 R^-1 a.

Thus the presentation change is exact, not merely an abelian or finite
quotient approximation. The oriented braid has coefficient

    b_original^-1=(baBaBaBAbA)t.

For q=BAbbbABB, exact free-fiber reduction gives

    q (baBaBaBAbA) alpha(q)^-1 = BAbb.

K's [second-hump certificate](research-k-second-hump.md) already excludes
conjugacy of (BAbb)t to every a^j t. The original primitive family is
x^k y=b^(k+1)t, and b^j t is conjugate to a^j t by t. This proves F by
transfer. A fresh direct finite representation check using the original
x,y words is also supplied below; the reused quartic functional is
credited to K.

## 3. Why finite twisted-conjugacy obstructions suffice

In a finite semidirect product H semidirect_alpha C_m, multiply as

    (u,i)(v,j)=(u alpha^i(v), i+j mod m).

If U=(W,1), every conjugation of U by an arbitrary group element g is
also a conjugation by a fiber element: let j be its stable exponent and
put q=g U^-j. Then q has stable exponent zero and
q U q^-1=g U g^-1. Hence conjugacy to (V,1) is equivalent to the
finite twisted equation

    q W alpha(q)^-1=V,       q in H.

For D/E the targets are all powers of a; for F all powers of b. The
integer-character argument in Section 1 is essential: the finite
representation alone would not classify all primitive candidates.

All three representations explicitly kill their original r and map the
oriented original braid to (W,1). Therefore failure of conjugacy in
these finite target groups excludes it in F/<<r>>. No faithfulness of
the representation is required.

## 4. Explicit finite algebras

For a coefficient field F_p and truncation degree d, begin with the
free associative augmentation algebra in the indicated fiber variables,
discard degrees above d, and replace degree d by one scalar coordinate
using a functional L. Its basis is all monomials of degrees less than d,
plus one symbol #. A degree-d product w becomes L(w)#. Products of #
with any positive-degree term vanish. Such a top-degree quotient is
associative; the implementations also check every basis triple.

The units 1+a,1+b,(1+c) generate a finite subgroup H. Word substitution
defines alpha; all basis-product identities and its finite order are
checked explicitly. Thus this really defines a finite semidirect target,
not just a list of numerical invariants.

The selected functionals, with unlisted coefficients zero, are:

    D, p=17, d=4:
      abaa:15, abab:6, abba:6, abbb:16,
      baaa:2, baab:11, baba:11, babb:1.

    E, p=5, d=3:
      aba:4, abb:3, abc:2, acb:4, acc:4,
      baa:1, bab:2, bac:3, bcb:4, bcc:3,
      cab:1, cac:1, cbb:1, cbc:2.

    F, p=5, d=4 (K's functional):
      abaa:1, abab:4, abbb:4, baaa:4, baab:1, babb:1.

### D: seventeen dual linear certificates

The D algebra has dimension 16 over F_17 and alpha has order 16. We
may use its **entire** augmentation-one unit group U, whose order is
17^15. Each 1+n is invertible by its finite geometric series because
the augmentation ideal is nilpotent. The ambient finite target is
U semidirect C_16; the original image need not be all of U.

For each k modulo 17, the candidate a^k has period 17. The twisted
equation is equivalent to

    q W = a^k alpha(q),       q_0=1.

This is an affine **linear** system in the other fifteen coefficients
of q. The saved certificate supplies a dual row lambda_k for every k.
If C_i=e_i W-a^k alpha(e_i) in the stated basis, the verifier checks

    lambda_k C_i=0  for i>=1,     lambda_k C_0=-1  in F_17.

Any q with constant coefficient one would contradict these equalities.
Thus all seventeen candidate powers are excluded in the entire unit
group. The independent verifier imports no Gaussian solver: it rebuilds
the products and checks the displayed dual identities directly.

The ambient target order is 17^15*16=45,798,768,824,157,052,688; there is
no enumeration of that many elements. Only 17 small dual certificates
are needed. The verifier checks all 4,096 associativity triples, all
256 basis-product homomorphism identities, alpha^16 on every basis
element, and the original relation/braid images before using them.

### E and F: closed twisted-orbit certificates

For E the algebra has dimension 14, the generated fiber has 78,125
elements, and alpha has order 60. A closed certificate set containing
W=aBac has 15,625 states and misses all five powers of a. All 93,750
signed-generator twisted edges remain in that set.

For F the algebra has dimension 16, the generated fiber has 15,625
elements, and alpha has order 20. A closed certificate set containing
the actual W=baBaBaBAbA has 3,125 states and misses all five powers of b.
All 12,500 signed-generator edges remain in the set.

The constructor builds these exact orbits. The independent verifier only
needs a closed superset containing W and missing the targets; it does
not trust an assertion of minimality or a stored boolean. Every fiber
conjugator is a word in the signed unit generators, so closure proves
the exclusions at every conjugator length. The group-size computations
are supplementary; the proof does not depend on them being independently
minimal.

Initial lower-degree filters were inconclusive. For example D's degree-
three mod-five filter leaves k=2 mod5, and separate E cubic functionals
leave k=4 or k=0,1. Those are false positives, not actual conjugacies.
The selected E functional is a linear combination of two invariant
functionals; its closed orbit excludes every residue. No survival in
an earlier filter is promoted to a positive group-theoretic claim.

## 5. Independent checks and exact limitations

`s_branch_finite_filters.py` constructs the finite algebras using vectors,
precomputed product tables, and Gaussian elimination for D. The separate
`verify_s_branch_certificates.py` imports none of those routines. It
rebuilds the algebras with dictionaries of literal monomials, checks the
original word maps and finite automorphism orders, verifies D's dual
rows without elimination, and checks every stored E/F orbit edge.
All three pass. The coordinating agent also independently replays the
certificates and reviews the character reduction.
Two invalid-proof controls are correctly rejected: zeroing one D dual
witness, and inserting the candidate identity into E's closed set.

`s_branch_models.py` independently checks the free basis inverses,
Tietze conjugating identities, E/F automorphism inverses, and F's exact
transfer to K. The short original-AK(3) entry certificates pass the
repository's strict elementary verifier. These positive ledgers reach
the stated tuples only; none ends at a free basis.

The signed symmetries used in the atlas preserve ambient primitivity
and send the braid to a rotation of itself or its inverse. Relator
rotation/inversion also preserves the relevant normal closure. Thus the
three results cover their full atlas classes, not just the selected
spellings. Combined with K/L they close the specifically listed missing
first-departure frozen-coordinate cases.

They do **not** give a new cyclic or raw peak bound, prove the whole
length-15 generalized-ACM component closed, or restrict arbitrary later
changes of both relators. In particular they do not settle AK(3).

## Reproduce

All scripts use Python's standard library and reside in `experiments/`.

```sh
python3 experiments/s_branch_models.py
python3 experiments/verify_s_branch_certificates.py \
  certificates/s_branch_D_linear.json --output /tmp/sD-review.json
python3 experiments/verify_s_branch_certificates.py \
  certificates/s_branch_E_orbit.json.gz.b64 --output /tmp/sE-review.json
python3 experiments/verify_s_branch_certificates.py \
  certificates/s_branch_F_orbit.json.gz.b64 --output /tmp/sF-review.json
python3 experiments/elementary_verify.py \
  certificates/s_branch_D_entry.json certificates/s_branch_E_entry.json \
  certificates/s_branch_F_entry.json
```

Regenerate the finite certificates:

```sh
python3 experiments/s_branch_finite_filters.py --model D --selected --linear \
  --output /tmp/sD-linear.json
python3 experiments/s_branch_finite_filters.py --model E --selected --group-order \
  --orbit-certificate /tmp/sE-orbit.json.gz.b64 --output /tmp/sE-result.json
python3 experiments/s_branch_finite_filters.py --model F --selected --group-order \
  --orbit-certificate /tmp/sF-orbit.json.gz.b64 --output /tmp/sF-result.json
```

Certificate compression is deterministic gzip followed by base64; it is
only a transport format. The stored words, linear witnesses and closed
sets are explicit, and their claims are checked afresh.
