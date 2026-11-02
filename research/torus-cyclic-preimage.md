# Primitive-free cyclic preimages in the torus deletion quotient

Coordinating-agent investigation, 2026-11-02. Developed in parallel with
[N's braid cyclic-preimage argument](research-n.md), whose determinant
idea prompted this complementary representation. No novelty claim is made.
This is an unbounded primitive-exclusion theorem for specified quotient
preimages, **not an AC invariant or an AK(3) solution**.

Let F=F(x,y), p_n=x^n y^(-(n+1)), b=xyxy^-1x^-1y^-1,
and pi_n:F -> T_n=<x,y | p_n>.

## Theorem

For n congruent to 3 or 8 modulo 12, and every c in T_n,

    pi_n^-1(c <pi_n(b)> c^-1)

contains no primitive element of F. In particular this holds for AK(3).
There is no word-length restriction on the primitive or on c.

Consequently, if r has image conjugate to b or b^-1 in T_3, then

    <q p_3 q^-1, h r h^-1>

contains no ambient primitive, for every q,h in F. More generally one
may use any number of elements of ker(pi_3), together with elements
whose images all lie in the same conjugate cyclic subgroup generated
by pi_3(b).

## 1. Integral determinant lemma

For A,B in SL(2,Z), direct expansion gives

    det(AB-BA)=2-tr(ABA^-1B^-1).

If rho:F -> SL(2,Z) satisfies tr(rho([x,y]))=3, then every free basis
(u,v) satisfies tr(rho([u,v]))=3. This follows from the elementary
Nielsen generators: changing a free basis changes its commutator to a
conjugate of [x,y] or its inverse; both have the same matrix trace.
Thus, for every primitive u and a free complement v,

    det(rho(u)rho(v)-rho(v)rho(u))=-1.                 (1)

Suppose rho(u) is conjugate to C^m, with C integral unimodular and
|tr(C)|>2. Set t=tr(C), U_0=0, U_1=1,
U_(j+1)=t U_j-U_(j-1). Cayley--Hamilton gives

    C^m=U_m C-U_(m-1) I   (m>=1).

After conjugating rho(v) by the same integral unimodular conjugator,
the determinant in (1) is divisible by U_m^2. For |m|>=2,
|U_|m||>1; the negative case follows by replacing C with C^-1.
This contradicts (1). The case m=0 also contradicts (1), because the
commutator with I is I. Therefore only m=1 or m=-1 can remain.
This conclusion uses integral divisibility; a general real-matrix
representation would not justify it.

## 2. A representation of T_3

Take

    A = [[0,-1],[1,-1]],       B = [[0,-1],[1,0]].

These satisfy A^3=B^4=I. Hence x->A, y->B kills p_3 and defines a
representation of T_3. Exact multiplication gives

    [A,B] = [[1,1],[1,2]],     tr([A,B])=3,
    rho(b)= [[1,1],[2,3]],     tr(rho(b))=4.

If pi_3(u) is conjugate to pi_3(b)^m and u is primitive, the determinant
lemma excludes m=0 and every |m|>=2. Notice that rho need not be faithful:
it is used only to exclude the images of proper powers.

For n=3 mod12 the same matrices kill p_n. For n=8 mod12 swap A and B;
the commutator trace is again 3 and the braid trace again 4. This proves
the same proper-power exclusion for precisely the stated congruence
classes. No claim for other n follows from these matrices.

## 3. The remaining exponents m=+1 and m=-1

Here one needs information from the exact torus quotient, rather than
only the matrix representation. This is the torus part of
[J's primitive-deletion theorem](research-j.md). A short proof for the
present congruence classes follows.

Use the character chi(x)=n+1, chi(y)=n, so chi(b)=1. If a primitive u
has torus image conjugate to b, its exponent vector is

    (1+n k, -1-(n+1)k)        for an integer k.

Put m0=xY and w=(xY)^nY (capitals denote inverse letters).
The pair (w,m0) is a free basis: y=w^-1 m0^n and
x=m0 w^-1 m0^n. Thus w^k m0 is primitive with the required exponent
vector. Nielsen's rank-two primitive conjugacy theorem says that a
primitive conjugacy class is determined by its exponent vector, so u
is conjugate in F to this word. See Clay--Conant--Ramasubramanian,
[Whitehead graphs and separability in rank two](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf),
Corollary 4.4, and J's explicit implementation of the representatives.

In the free-product quotient C_n*C_(n+1) of T_n, the cyclically reduced
syllable length of b is 6. Direct reduction gives, for w^k m0,

    2(nk+1)       if k>=0,
    2(n(-k)-1)    if k<0.

For n>=3 the first can never be 6. The second equals 6 only when
n=4 and k=-1, which is outside both congruence classes in the theorem.
Conjugate free-product elements of length greater than one have the
same cyclic syllable length. This excludes m=1. Inverting u reduces
m=-1 to the same case. Together with Section 2 this proves the theorem.

## 4. Application and limits

All 32 literal length-eight braid replacements in the first-departure
atlas have exact torus image conjugate to b or b^-1. The theorem covers
each such replacement and arbitrary independent conjugates of both
relators. N's complementary theorem covers all 432 length-nine power
replacements using the braid quotient. Together these remove the
arbitrary-tail limitation from the 5,632-pair primitive-free catalogue.
O and P also obtain an independent folded-graph route; their certificate
additionally covers the two actual later waypoints, which this report
does not infer from the torus matrices.

This rules out reaching a primitive relator by Nielsen moves from any
tuple in the specified families. It does not rule out AC paths that
change the quotient image subgroup by further independent conjugations
and products. In particular it does not prove AK(3) nontrivial under AC.

## Reproduce

    python3 experiments/torus_cyclic_preimage.py --output results/torus_cyclic_preimage_results.json

The standalone standard-library checker verifies the matrix orders,
commutator and braid images, the determinant identity on a finite exact
matrix ball, Cayley--Hamilton divisibility controls, and syllable formulas
for n<=200 in the two congruence classes and -30<=k<=30. These are
arithmetic controls for the unbounded proof above, not finite-search
substitutes for it. No ordinary free-group AC goal has been solved.
