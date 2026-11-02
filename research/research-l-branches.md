# Research L follow-up: two further power-departure primitive exclusions

Date: 2026-11-02. Status: analytic single-coordinate exclusions at two
explicit deletion quotients. **No unrestricted AC obstruction or AK(3)
trivialization is claimed.** Novelty is not established.

## Previous work and scope

After the main L investigation, the coordinating agent supplied a
classification of the first length-15 departures: there are six
power-length-nine classes under the stated signed symmetries. K had
already excluded primitive replacements of the braid relator after the
departure `XXXyxYxxY`. I independently checked the two additional
analytic reductions proposed by the coordinating agent.

Use X=x^-1, Y=y^-1, with

    p=xxxYYYY,  b=xyxYXY,
    r_A=XXXXYxxxy,  r_C=XXXyXYxxy.

Both r_A and r_C have image conjugate to p in B3. The checker confirms
their equal total exponent sums and equal cyclic necklaces in C2*C3;
the central-kernel argument from A/E upgrades these two data to exact
B3 conjugacy. Thus replacing p by either word while retaining b is an
allowed ACM replacement. Any strict elementary entry certificate is
separate evidence; no quotient identity is silently counted as an
elementary move here.

The primitive classification used in both arguments is Nielsen's
rank-two uniqueness theorem: primitive elements with the same
abelianization vector are conjugate in F2. A primary modern proof is
[Clay–Conant–Ramasubramanian, Corollary 4.4](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf).

## 1. The Baumslag–Solitar branch

The quotient by r_A is

    G_A=<x,y | y^-1 x^3 y=x^4> = BS(3,4).

More generally put `G_n=<x,y | y^-1 x^n y=x^(n+1)>` for n>=2.
Its character chi sends x to zero and y to one. The braid word b has
chi-value -1. After inverting a proposed primitive replacement if
necessary, it would be conjugate to b^-1 and have exponent vector
`(k,1)` for some integer k. All such primitive words are freely
conjugate to

    v_k=x^k y.

These are primitive because `(x,x^k y)` is a free basis, and Nielsen
uniqueness covers every other primitive with that vector.

View G_n as an HNN extension with base group `<x>` and stable letter y.
Its Britton pinches are

    Y x^(n q) y -> x^((n+1)q),
    y x^((n+1)q) Y -> x^(n q).

In cyclic order, the stable letters of b are `y,Y,Y` and the intervening
x-exponents are `1,-1,1`. The two opposite-sign junctions would require
n or n+1 to divide 1. Neither can occur for n>=2. Thus b, and also its
inverse, is cyclically Britton-reduced with stable-letter length three.

Each v_k is cyclically Britton-reduced with stable-letter length one.
Collins' HNN conjugacy theorem preserves the stable-letter length of
positive-length cyclically reduced representatives. See
[Diekert–Duncan–Myasnikov, Theorem 5.2](https://arxiv.org/html/1206.4431v2#S5.SS2).
Therefore no v_k can be conjugate to b or b^-1 in G_n. This proves the
uniform statement for all n>=2 and in particular the r_A branch.

The restriction is real: in BS(1,2), the identity `Y x y=x^2` reduces

    (XY) b (yx) = x^2 Y.

The right-hand word is primitive. This exact positive control is checked
by Britton reductions in the program.

## 2. The transported rank-two free-by-cyclic branch

For G_C=F/<<r_C>>, set

    t=x,  a=y X^2,  d=x y X^3.

Since d=t a t^-1, these definitions reconstruct x=t and y=a t^2.
Write a_j=t^j a t^-j. The defining word rewrites to

    r_C = a_-3 a_-4^-1 a_-2.

Applying stable conjugation by t^4 gives the equivalent relation

    a_2=a_0 a_1^-1.

Consequently

    G_C = F(a,d) semidirect_alpha Z,
    alpha(a)=d,  alpha(d)=a d^-1.

The substitution is an automorphism, with inverse
`alpha^-1(a)=d a`, `alpha^-1(d)=a`. This is an exact presentation
change, not merely a homomorphism to a free-by-cyclic quotient.

Use chi(x)=1, chi(y)=2. The inverse braid word has normal form

    b^-1 = W t,  W=a d^2 a^-1 d a^-1.

In the checker the second fiber generator is written `b` instead of d,
so this coefficient is `abbAbA`. This is **exactly** the W and the
automorphism in K's original rank-two finite obstruction.

Every free primitive of chi-value one has exponent vector
`(1-2k,k)`. The free basis `(x,c)` with `c=X^2 y` reconstructs
`y=x^2 c`, so Nielsen uniqueness supplies the complete candidate family

    c^k x,   k in Z.

In the fiber,

    c=alpha^-2(a)=a d a
      =alpha^-4((d a^-1)^-1).

These are freely reduced identities in F(a,d), checked without using a
finite quotient. Thus each candidate is conjugate by a power of the
stable letter to one of K's already excluded candidates:

    c^k t = t^-4 [ (d a^-1)^(-k) t ] t^4.

K's theorem excludes full group conjugacy of Wt to `(d a^-1)^j t` for
every integer j, using a completed finite characteristic-quotient test.
Conjugacy is transitive, so it also excludes conjugacy to every c^k t.
After normalizing signs by inversion this proves that no free primitive
can represent a conjugate of b or b^-1 in G_C.

This argument transfers K's finite separation through an independently
verified exact model; it does not rerun or claim to replace K's finite
enumeration.

## 3. Consequence and symmetry scope

At either tuple `(r_A,b)` or `(r_C,b)`, replacing the braid coordinate
while retaining its new power coordinate cannot produce a primitive
free relator at any word length. Replacing the power coordinate with b
retained is already excluded by J, since each r has image conjugate to p
in B3. Thus neither coordinate of these two waypoints has a one-step
primitive shortcut.

The simultaneous inversion of x,y sends b to a cyclic rotation of b^-1,
and swapping x,y sends b exactly to b^-1. Therefore the conclusions
transport to the four signed-symmetry representatives in each of the two
listed power-departure classes. Together with K's earlier power-departure
branch, this addresses three of the six first length-nine power classes.
It does not classify subsequent moves, the other three classes, or the
entire cyclic-length-15 component.

## Reproduction and checks

Run:

```sh
python3 experiments/remaining_branch_obstructions.py \
  --output results/remaining_branch_results.json
```

The script is standalone and uses only the Python standard library. It
checks the exact B3 conjugacy invariants for r_A and r_C, Britton
reduction formulas for n=2,...,50 and primitive parameters -20,...,20,
the BS(1,2) positive control, both inverse automorphism substitutions,
the original r_C word, the braid's exact normal form, and the
stable-conjugacy transfer formulas for parameters -12,...,12. The finite
checks support the formulas; the unbounded conclusions follow from the
two analytic arguments above.

These are limitations on particular frozen-coordinate strategies. They
are not invariants under unrestricted Andrews–Curtis moves and satisfy
none of the user's four full breakthrough objectives.
