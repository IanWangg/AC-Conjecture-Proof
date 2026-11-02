# Research K follow-up: a second finite obstruction on a power-relator departure

Date: 2026-11-02. Status: an unbounded single-coordinate primitive-replacement exclusion at another explicit AK(3)-equivalent tuple. **No global AC obstruction or free-group trivialization is claimed.** No novelty claim is made.

## Previous work and direction

After completing K's rank-two finite certificate, I considered the coordinating agent's next proposed power-relator departure. This is a complementary branch: the original braid relator is retained while the power relator is replaced. I used the same finite-characteristic-quotient idea, but a direct degree-four orbit would be too large. A central-extension filter instead led to a small explicit quotient algebra and a complete conjugacy test. The parent supplied the initial free-by-cyclic presentation; the original-word images and the finite obstruction below were independently derived and checked here.

The primitive-word classification used is again [Clay–Conant–Ramasubramanian, Corollary 4.4](https://msp.org/involve/2014/7-4/involve-v7-n4-p01-p.pdf): two primitive elements in F2 with the same exponent vector are conjugate. The ordinary and ACM definitions are those in [Panteleev–Ushakov](https://arxiv.org/html/1609.00325v1).

## Statement

Write

    p=xxxYYYY,   b=xyxYXY,   r=XXXyxYxxY,
    G=<x,y | r=1>.

The word r has length nine. In the braid quotient B3, it satisfies

    p=(xxY) r (yXX).

This exact conjugacy is checked using the C2*C3 syllable normal form and total exponent sum. Hence replacing p by r while holding b is an allowed ACM move. This statement does not assign a length bound to its ordinary expansion.

**Theorem.** No primitive free word has image conjugate to b or b^-1 in G, regardless of its length.

Therefore, at the tuple (r,b), a single ACM replacement of b with r held fixed cannot create a primitive relator. A primitive replacement of r with b held fixed is already excluded by J, since r is conjugate to p in B3. Thus neither coordinate of this specific first departure admits a primitive one-step shortcut. Further simultaneous changes remain outside the theorem.

## 1. Candidate family and the rank-three model

Introduce

    t=x,  a=y,  d=xyX,  e=xxyXX.

The deletion quotient is the free-by-cyclic group

    F(a,d,e) semidirect_alpha Z,
    alpha(a)=d, alpha(d)=e, alpha(e)=a d^-1.

Indeed r=1 is equivalent to t^3 a t^-3=a(t a t^-1)^-1. The inverse automorphism is alpha^-1(a)=e a, alpha^-1(d)=a, alpha^-1(e)=d. In the resulting normal form,

    b=W t,  W=d e^-1 d^-1.

The natural homomorphism chi sends x to one and y to zero. A primitive word that could be conjugate to b or b^-1 can be inverted to have chi-value one. Its exponent vector is (1,k). Every such primitive is freely conjugate to

    y^k x=a^k t,   k in Z,

by primitive conjugacy uniqueness; these words are primitive because (y,y^k x) is a free basis. We must separate Wt from this entire family.

The code uses the fiber names `a,b,c` for a,d,e, respectively. Thus its W is `bCB` and its automorphism is `a->b, b->c, c->aB`.

## 2. A compact explicit finite quotient

Work over F5 with noncommuting augmentation variables U,V,W. Start with the degree-three truncated algebra. Define a linear functional L on its homogeneous cubic part by the following nonzero coefficients (all values are modulo five):

| Monomial | L | Monomial | L |
|---|---:|---|---:|
| UVU | 4 | UVV | 4 |
| UVW | 1 | UWU | 1 |
| UWV | 4 | VUU | 1 |
| VUV | 1 | VUW | 4 |
| VWV | 4 | VWW | 4 |
| WUU | 4 | WUV | 1 |
| WVV | 1 | WVW | 1 |

All other cubic monomials have value zero. Let A be the quotient of the truncated algebra by ker(L) in degree three. This kernel is a two-sided ideal: multiplying a degree-three element by an augmentation element gives degree at least four and therefore zero. The algebra A has dimension fourteen, with basis the empty monomial, the three degree-one monomials, the nine degree-two monomials, and one cubic symbol Z. We may take Z=UVW because L(UVW)=1.

Its complete multiplication rule is explicit:

- concatenate two ordinary monomials if their total degree is at most two;
- if their total degree is three, replace their concatenation by L of that monomial times Z;
- products of total degree at least four, including Z times a positive-degree element, are zero;
- the empty monomial is the identity.

Let H be generated in A's units by 1+U,1+V,1+W. The free-group automorphism alpha induces

    a->d, d->e, e->a d^-1

on these units. The program checks that this map is genuinely well-defined on A: it verifies associativity on all 2,744 triples of basis elements, multiplicativity of alpha on all 196 basis pairs, and the explicit inverse substitution on every basis element. Thus the calculation does not merely assume the correctness of the supplied L.

Complete finite closure gives

    |H|=78,125,    order(alpha on H)=31.

The finite semidirect product Q=H semidirect_alpha C31 has order **2,421,875**. Define original generator images by x=(1,t), y=(a,1) in the usual fiber/stable notation; equivalently their stable exponents are one and zero. Direct evaluation verifies

    r maps to 1,   b maps to (d e^-1 d^-1)t.

So this is an actual finite quotient of G. The original x,y images generate Q because their stable conjugates recover all three fiber generators.

## 3. Complete conjugacy separation

The finite twisted orbit of W is generated by

    z -> g z alpha(g)^-1,
    g in {a,d,e,a^-1,d^-1,e^-1}.

Its exact completed size is **15,625**. The candidate a has order five in H. None of the five powers 1,a,a^2,a^3,a^4 belongs to the orbit.

This excludes full Q-conjugacy of Wt to every a^k t, not merely conjugacy by a preselected subgroup. If u=Wt and a conjugator g has stable exponent j modulo 31, then q=g u^-j has stable exponent zero and conjugates u exactly as g does. Thus a fiber conjugator always suffices, and the enumerated twisted orbit is the complete relevant conjugacy test.

Every integer k reduces modulo five. Therefore no primitive candidate can be conjugate to b or b^-1 in G. This proves the stated unbounded theorem using an explicit finite group.

The sorted orbit digest, with each fourteen-coefficient vector encoded in base five into eight little-endian bytes, is

    2bcc6e7f66f6f15ece08582b4420f2693207fbdee5dbb7c2729a88276f990b08.

Again this does not contradict finitary AC connectivity: it separates one-coordinate conjugacy replacements, while arbitrary AC paths may change both coordinates.

## 4. Independent discovery check by central lifts

A separate implementation does not use the fourteen-dimensional quotient or enumerate its orbit. It uses literal-string polynomials in the full forty-dimensional degree-three algebra over F5.

First consider its degree-two quotient. Every element of the generated fiber group has a class-two normal form

    a^s d^t e^u [a,d]^v [a,e]^w [d,e]^z,

with all six exponents taken modulo five and commutators defined as inverses-first. Reordering works because commutators are central in degree two, and every generator has order five. This covers every possible lower-degree conjugator.

For target a^k t, the degree-one equation uniquely forces

    (s,t,u)=(2k+1,k,k+1) modulo five.

The independent program checks all 125 central normal forms for each of k=0,...,4: 625 possibilities in total. Exactly one lower-degree conjugator works for each k. Their (v,w,z) values are

| k | (v,w,z) | L of the degree-three defect |
|---:|---|---:|
| 0 | (4,0,0) | 3 |
| 1 | (2,3,0) | 3 |
| 2 | (3,0,4) | 3 |
| 3 | (2,1,2) | 4 |
| 4 | (4,1,4) | 2 |

All possible higher lifts of a lower conjugator differ by a homogeneous cubic kernel element z. Their defects differ by (I-alpha)z. The independent program directly verifies L(I-alpha)=0 on each of the 27 cubic monomials. Every displayed defect has nonzero L, so no choice of higher lift can correct it. This second proof does not rely on the direct finite-orbit enumeration.

The earlier generic central-lift implementation instead enumerates the entire degree-two fiber group (15,625 elements), chooses a lift for each, and tests the same obstruction by linear algebra on all 27 cubic tensor coefficients. It agrees that every parameter is excluded. The image of I-alpha on that full tensor space has rank 21.

There are useful inconclusive controls: the mod-two degree-three test leaves k=0,1 modulo four; its degree-four central lift leaves k=0,1 modulo eight; and the mod-three degree-three filter leaves k=8 modulo nine. These weaker tests are recorded explicitly and were not treated as negative proofs. The decisive exclusion is the mod-five calculation, confirmed by the independent string-polynomial method and the compact direct finite quotient.

## Reproduce

The principal complete test and the independent check are standard-library Python programs:

```sh
python3 experiments/rank3_compact_quotient.py \
  --output results/k-rank3-compact.json
python3 experiments/rank3_mod5_independent.py \
  --output results/k-rank3-mod5-independent.json
```

Supplemental generic filters, including the inconclusive controls, are:

```sh
python3 experiments/twisted_magnus_rank3.py --degree 3
python3 experiments/twisted_magnus_rank3.py --central-lift
python3 experiments/twisted_magnus_odd.py --prime 5
python3 experiments/twisted_magnus_odd.py --prime 3
```

The programs have no external dependencies or heuristic pruning in their recorded completed runs. The compact orbit test and the 625-case independent check both pass. These results block a second proposed primitive waypoint; they do not produce a path to the free basis or an invariant of unrestricted AC moves. The original four breakthrough objectives remain unachieved.
