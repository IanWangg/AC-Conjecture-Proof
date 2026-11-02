# Research G: exact distance eight in the complementary torus-knot quotient

Date: 2026-11-02. Status: explicit infinite-quotient result and checked free lifting errors. **This does not trivialize AK(3) in the free group.** No novelty claim is made.

## Previous work and independent choice

I read the six existing reports A through F before choosing this direction. A/F prove cyclic plateau constraints, B distinguishes quotient connectivity from metric divergence, C supplies a uniform family equivalence, D exhausts a finite raw elementary graph, and E finds a ten-instruction path in the braid deletion quotient. I also reviewed the ordinary-AC and ACM definitions in Panteleev–Ushakov's [primary paper, Sections 1.2 and 2](https://arxiv.org/html/1609.00325v1). This review led me to choose the complementary deletion quotient: impose the power relator instead of the braid relator, and seek an exact path in that infinite group.

Write X=x^-1, Y=y^-1 and

    p=xxxYYYY,  b=xyxYXY,
    T=<x,y | x^3=y^4>.

The AK(3) relator tuple maps to (1,b) in T.

## Checked result

The distance from (1,b) to (x,y) in T is exactly **eight** under the fixed fourteen-instruction alphabet used in E: invert either coordinate, multiply either coordinate on the right by the other or its inverse, or conjugate either coordinate by x,X,y,Y. The eight-move upper certificate uses only positive multiplication and single-generator conjugation. Consequently its distance is also exactly eight under the smaller strict twelve-instruction alphabet accepted by the repository's elementary verifier.

Every quotient of T has distance at most eight for the corresponding named images. In particular, neither a disconnected-component obstruction nor unbounded instruction distances can come from homomorphisms all factoring through this fixed torus-knot quotient. This complements E's corresponding conclusion for the fixed braid quotient. It does not cover arbitrary homomorphisms from the free group, or synchronized behavior in a product of the two quotients.

## Complete symbolic upper certificate

Use C_i(g): r_i -> g r_i g^-1. Start at (r_0,r_1)=(1,b), and perform:

| Step | Strict elementary operation |
|---:|---|
| 1 | r_0 <- r_0 r_1 |
| 2 | C_1(x) |
| 3 | r_1 <- r_1 r_0 |
| 4 | C_1(x) |
| 5 | r_1 <- r_1 r_0 |
| 6 | r_0 <- r_0 r_1 |
| 7 | C_1(Y) |
| 8 | C_1(X) |

After step 1, r_0=b. Free reduction after the two conjugate/multiply iterations gives, at step 5,

    r_1=f=x^3 y x Y^3 X Y.

In T, z=x^3=y^4 commutes with both generators. Therefore

    f = z y x Y^3 X Y
      = y x z Y^3 X Y
      = y x y X Y
      = b^-1 x.

Step 6 gives r_0=b(b^-1 x)=x. The last two conjugations send f to

    X Y (y x y X Y) y x = y

by free cancellation. This is a complete proof of the upper bound in T, without a finite quotient or a heuristic search assumption.

Agent H independently develops the parameter-uniform version of this cancellation pattern. The present report treats exact distance for n=3 and exposes the actual free-word lifting error.

## Exact lower bound by complete balls in the infinite group

For exact computation, write every T element as

    z^k a_1 ... a_l,

where a_i alternates between a nonidentity x-residue in {x,x^2} and a nonidentity y-residue in {y,y^2,y^3}. Combining same-factor syllables extracts a power of z using division by 3 or 4. Negative exponents use ordinary integer division with remainder. Multiplication and inversion in `experiments/torus_search.py` use precisely this normal form.

The form is unique. Its image modulo the central subgroup <z> is the reduced free-product word in C3*C4, which determines all the a_i. The homomorphism e:T->Z with e(x)=4 and e(y)=3 sends z to 12 and then determines k. Thus equality of stored normal forms is equality in T, not a reduction modulo a finite group.

The complete radius-four balls have these exact sizes:

| Radius | From (1,b) | From (x,y) |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 7 | 10 |
| 2 | 45 | 74 |
| 3 | 302 | 505 |
| 4 | 2,249 | 3,556 |
| Total | 2,604 | 4,146 |

The smallest sum of shortest stored depths at an intersection is eight. Every path of length at most eight has a midpoint in these two radius-four balls. Hence no path of length at most seven exists in the fourteen-instruction graph. Together with the explicit eight-move path, this proves the exact distance, as a computer-assisted lower bound with an independent symbolic upper bound.

All fourteen instruction inverses are checked in the implementation. The balls have no syllable-length cutoff, finite reduction, canonical conjugacy identification, or heuristic pruning. A user-specified state budget explicitly marks a ball incomplete and suppresses a distance conclusion when it is reached.

## Actual free-group lift and a relative filling certificate

Apply the same eight strict operations to the genuine free-group AK(3) tuple (p,b). Its endpoint is

    (xxxYYYYxyxYXYxxxyxYXYxxYYYYxyxYXYxxYYYYxyxYXY,
     XYxxxyxYXYxxYYYYxyxYXYxxYYYYxyxY).

The coordinate lengths are **45 and 32**, and its raw total peak is **77**. The independent repository verifier confirms exactly this endpoint. Neither coordinate equals its target generator as a free word.

There is an additional exact certificate for how these errors lie in the normal closure of p. First consider the formal replay that replaces the initial p by the identity, leaving b as a free word. Its step-5 word is f above. Put f0=b^-1 x and use the commutator convention [p,y]=p y p^-1 Y. Direct free-word multiplication gives

    f f0^-1 = D = [p,y] * (yx)p(yx)^-1.

Thus D is a product of three conjugates of p or p^-1, with conjugators 1,y,yx and signs +,-,+. The formal-zero replay ends at (b f, X Y f y x), so its errors relative to (x,y) are

    b D b^-1,  (XY) D (XY)^-1.

To recover the actual lift, retain a formal marker q for the initial p through the eight moves. For any formal word w(q), scanning left to right gives an exact free identity

    w(p) = (product of prefix-conjugates of p or p^-1) * w(1),

where the prefix at a q occurrence consists of the preceding ambient letters after deleting q markers. This is just telescoping multiplication, not a quotient inference. The first endpoint contains three positive q occurrences; the second contains two. Combining those factors with the three factors of D gives explicit factorizations of the actual endpoint errors into **six and five conjugates**, respectively, of p or p^-1.

`certificates/torus_quotient_lift.json` records the actual free endpoint, all eight strict moves, both nontrivial residual words, and every conjugator/sign in these two factorizations. A saved-factorization checker multiplies the recorded factors as free words and compares exactly against the two residuals, without regenerating a path. These are upper bounds on relative filling area, not minimality claims.

The factorization does not supply an AC correction: by this stage the original p is no longer a stored relator. Deleting its conjugates without restoring a suitable donor would add an unjustified move. This is the remaining lifting issue, rather than a free-group solution hidden in the quotient notation.

## Reproduce

From the repository root:

```sh
python3 experiments/torus_search.py --depth 4 \
  --output certificates/torus_depth4.json \
  --certificate certificates/torus_quotient_lift.json
python3 experiments/elementary_verify.py certificates/torus_quotient_lift.json
python3 experiments/torus_search.py \
  --verify-factorizations certificates/torus_quotient_lift.json
```

All use only the Python standard library. The completed run gives distance eight, the independent elementary replay gives eight moves and peak 77, and the saved factorization replay reports factor counts (6,5) with free endpoint lengths (45,32). None establishes any of the four requested breakthrough objectives.

## Remaining direction

E and G show that the two natural one-relator deletion quotients each admit short paths. This does not produce one common instruction path that works in both, let alone in the free group. Let Np=<<p>> and Nb=<<b>>. Since AK(3) presents the trivial group, Np Nb=F2; hence the diagonal map onto B3 times T is surjective and has kernel Np intersect Nb. Investigating a synchronized product certificate is a stricter test than checking the factors separately and is a natural next lifting experiment. This report does not assert such a certificate.
