# Research H: a uniform torus-quotient path and the pseudo-meridian distinction

Date: 2026-11-02. Status: proved infinite-family quotient result, with an
explicitly nontrivial free lift. **No AK(3) trivialization, nontriviality
proof, or solution of the full conjecture is claimed.** Novelty is not
established.

## Previous work and independent choice

Before choosing a direction I read the six existing reports A–F, including
A/F's frozen-relator normal-form arguments, B's quotient-distance principle,
C's parameter-uniform MS bridge, D's complete raw cap-18 search, and E's
ten-instruction braid-group certificate and its lifting errors. I also read
the ordinary and ACM definitions in Panteleev–Ushakov's
[primary paper, Sections 1–2](https://arxiv.org/html/1609.00325v1).

I independently chose the complementary infinite quotient obtained by
killing the power relator rather than the braid relator. G independently
chose the same quotient and found an eight-instruction path for n=3. After
coordinating, G focused on the exact n=3 search and H on the symbolic family
and the meaning of its lifting errors. The path pattern and initial
cancellation observation are credited to G; the uniform proof and
independent family checker below were developed in H. This is joint
progress rather than two independent discoveries of the same path.

The interpretation using pseudo-meridians uses Silver–Whitten–Williams,
[*Knot Groups with Many Killers*](https://arxiv.org/html/0909.3275v1),
Definition 1.1 and its discussion of torus-knot automorphisms. It provides a
useful warning about a possible automorphism-based obstruction.

## Uniform result

Let n>=2 and put

    T_n = <x,y | x^n=y^(n+1)>,
    p_n=x^n y^-(n+1),
    b=xyx y^-1 x^-1 y^-1,
    m=xy^-1.

The ordered AK(n) tuple has image `(1,b)` in T_n. We prove

    (1,b) ~AC (x,y) in T_n

by **2n+2 strict elementary moves**. A strict move here is positive right
multiplication of one coordinate by the other, inversion, or conjugation by
one signed named generator. The path needs no inversions or negative
multiplications. Hence the same bound holds in every quotient of T_n with
the corresponding named generator images.

There is also a **2n-move** path from `(1,m)` to `(x,y)`. Consequently the
normally generating element b and the meridian m, despite belonging to
different automorphism orbits, give AC-equivalent pairs `(1,b)` and `(1,m)`.
The displayed move bounds are constructive upper bounds, not minimality
claims for all n. G separately determines the exact n=3 distance under its
fourteen-instruction convention.

## Complete symbolic path

Write X=x^-1, Y=y^-1 and let C_i(g) mean `r_i <- g r_i g^-1`.
Set z=x^n=y^(n+1). Since z commutes with x and y, it is central in T_n.

Start with `(r_0,r_1)=(1,b)` and perform:

1. `r_0 <- r_0 r_1`, giving `(b,b)`.
2. Repeat n-1 times: `C_1(x)`, then `r_1 <- r_1 r_0`.
3. `r_0 <- r_0 r_1`.
4. `C_1(Y)` followed by `C_1(X)`.

The first coordinate remains b during the loop. After k repetitions,
including k=0, the exact freely reduced second word is

    R_k = x^(k+1) y x Y^(k+1) X Y.

This is a free-group identity, proved inductively: the next pair of moves
replaces R_k by `x R_k X b`, whose adjacent inverse letters cancel to the
displayed formula with k increased by one. No quotient relation is used
in this induction.

At k=n-1, use the central power relation:

    R_(n-1) = x^n y x Y^n X Y
            = z y x (y z^-1) X Y
            = y x y X Y
            = b^-1 x.

Thus step 3 changes the first coordinate to `b(b^-1 x)=x`. The last two
conjugations change the second coordinate as follows:

    y x y X Y  --C_1(Y)-->  x y X  --C_1(X)-->  y.

The endpoint is exactly `(x,y)` in T_n. The count is
`1+2(n-1)+1+2=2n+2` strict moves. This proves the entire infinite family.

## A companion meridian path

The standard positive meridian of the `(n,n+1)` torus knot is m=xy^-1,
whose abelianization is `(n+1)-n=1`.

For the tuple `(1,m)`, first copy m into the first coordinate. Repeat n-1
times `C_1(Y)` and positive multiplication of the second coordinate by the
first. After k repetitions the second free word is

    S_k = Y^k x^(k+1) Y.

Indeed `Y S_k y m` freely reduces to S_(k+1). At k=n-1,

    S_(n-1)=Y^(n-1) x^n Y
           =Y^(n-1) z Y
           =y.

Finally multiply the first coordinate by the second to obtain `m y=x`.
The count is `1+2(n-1)+1=2n`. In a symmetric instruction convention, the
two paths concatenate to a path from `(1,b)` to `(1,m)` of length at most
`4n+2`; a strict positive-only expansion of the reversed meridian path is
also finite. No assertion of optimality is needed.

## Why b is a pseudo-meridian, and why this does not obstruct AC moves

For completeness, b normally generates T_n. In the quotient by b, the
braid relation makes Delta=xyx=yxy conjugate x to y. Centrality of z then
gives

    y^n = Delta x^n Delta^-1 = Delta z Delta^-1 = z = y^(n+1).

Hence y=1, and x, being conjugate to y, is also 1. This is a normal
generation argument, not a free-group AC certificate.

In the quotient of T_n by its center, namely `C_n*C_(n+1)`, the image of
b is cyclically reduced of syllable length six. The image of m and of its
inverse has cyclic syllable length two. Conjugacy preserves these cyclic
syllable lengths, so b is not conjugate to m or m^-1 in T_n.

The cited primary paper records that the outer automorphism group of a
nontrivial torus-knot group has order two. Simultaneous inversion
`x -> X, y -> Y` is an automorphism and acts by -1 on the infinite cyclic
abelianization, so it represents the nonidentity outer class. It sends
m to `X y`, a conjugate of m^-1. Thus every automorphic image of m is
conjugate to m or m^-1. Since b normally generates but is not such an
image, b is a pseudo-meridian in the paper's terminology.

Our explicit pair paths show that this difference of one-element
automorphism orbits is **not invariant under two-coordinate AC moves**.
It cannot, by itself, serve as an obstruction for AK(n). This conclusion
uses an explicit path, rather than an assumption that normal generation
implies AC equivalence.

## The free-group lift fails already in abelianization

The path starts at `(1,b)` only after imposing p_n=1. To avoid erasing this
distinction, the saved certificate instead applies exactly the same
strict instructions to the actual free-group tuple `(p_n,b)` and records
its actual endpoint.

The exponent vectors initially are `(n,-n-1)` and `(1,-1)`. After the first
copying operation the fixed donor has exponent vector `(n+1,-n-2)`.
Conjugations do not change exponent sums. After n-1 loop additions and
the final addition, the endpoint exponent vectors are exactly

    r_0: (n^2+n+1, -(n+1)^2),
    r_1: (n^2, 1-n^2-n).

Subtracting the standard basis vectors gives

    abelianization(r_0 x^-1) = (n+1)(n,-n-1),
    abelianization(r_1 y^-1) = n(n,-n-1).

These vectors are nonzero for every n>=2. Thus the free endpoint cannot
possibly be `(x,y)`, even before inspecting noncommutative residuals. The
errors disappear in T_n because they are multiples of the imposed power
relation, not because the AC instructions have removed them in the free
group.

For n=3 the strict eight-move lift has endpoint word lengths **45 and 32**,
peak raw total length **77**, and exponent vectors `(13,-16)` and
`(9,-11)`. The coordinating agent's independent strict free-word verifier
checks this exact recorded endpoint. The tuple remains AC-equivalent to
AK(3); it is not a solution.

## Reproduction

The independently written standard-library checker uses the exact normal
form `z^k` followed by alternating nonzero residues in the two cyclic
factors. It retains the central exponent. In particular its control
checks that `x^n=y^(n+1)=z` is **not** the identity; this prevents a
free-product quotient computation from masquerading as a calculation in
T_n itself.

From the repository root:

```sh
python3 experiments/torus_family.py --n 3 --selftest \
  --output certificates/torus_family_n3_lift.json
python3 experiments/elementary_verify.py certificates/torus_family_n3_lift.json
```

Executed implementation checks: n=2,...,40; both loop formulas; the exact
quotient endpoints of the b and meridian paths; the `2n+2` and `2n` counts;
the closed endpoint exponent vectors; central-element and inverse-word
controls. All passed. The all-n claim rests on the symbolic cancellations
above, not extrapolation from these finite tests.

## Consequence and remaining barrier

E's certificate bounds AK(3)'s image in every quotient annihilating the
braid relator. The uniform certificate here bounds AK(n)'s image in every
quotient annihilating the power relator. For n=3 the latter bound is eight.
Neither family can establish a fixed-quotient disconnection or unbounded
distance obstruction for the corresponding target.

A quotient obstruction must therefore retain enough information that
neither defining relator has simply been set to the identity by the
chosen homomorphism. A positive free-group proof must eliminate the
displayed lifting errors by actual AC moves. Nothing here supplies that
step or satisfies any of the four requested breakthrough objectives.
