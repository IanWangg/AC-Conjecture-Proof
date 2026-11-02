# Research I: exact first-order lifting defects of the braid certificate

Date: 2026-11-02. Status: exact residual-area and subgroup calculations for a particular quotient lift. **No free-group AC trivialization or counterexample is established. No novelty claim is made.**

## Previous work read and independent choice

I read the actual Research A–F notes before choosing this direction. A and F classify the initial cyclic plateau; B exposes nilpotent lifting errors and gives a finite-quotient distance principle; C supplies a uniform MS-to-AK bridge; D exhausts a bounded raw elementary graph; E supplies a ten-instruction path in the infinite braid quotient, with a nontrivial free-group lift. I also read the primary AC/ACM definitions in [Panteleev–Ushakov](https://arxiv.org/html/1609.00325v1), and reviewed relation-module context in [Putman's one-relator notes, Section 6](https://academicweb.nd.edu/~andyp/notes/OneRelator.pdf). After learning that parallel researchers were already studying the complementary torus quotient, I independently concentrated on the missing lifting step in E.

The objective is to quantify that gap and test whether E's endpoint could be completed by ordinary Nielsen operations on the relators. This investigates a possible completion of a concrete candidate path; it does not replace the user's full objective with a quotient statement.

## Results

Write `X=x^-1`, `Y=y^-1`, and let

    b = xyxYXY,    N = <<b>> in F=F(x,y),    B=F/N=B3.

Let `(a,c)` be the exact free-word endpoint of E's certificate. Its errors relative to the basis are

    w0 = aX = YYYYxyxYXyyyXXXyxyyyyXYX,
    w1 = cY = XYxyxYXyyyXXXyxyyyyXXXyxYYYYXYxxxYYYxyXYXyyy.

They have free lengths 24 and 44. The following statements were checked:

1. The minimum numbers of conjugates of `b` or `b^-1` whose products equal `w0` and `w1` in the free group are **exactly 5 and 13**, respectively. These are areas in this particular one-relator presentation, not AC-move distances.
2. Both errors remain nontrivial in `N/[N,N]`. Thus this particular quotient lift fails already in `F/[N,N]`, before asking for exact equality in F.
3. The subgroup `<a,c>` is a **proper infinite-index subgroup of rank 2** in F. Consequently no suffix made only of Nielsen operations on the two relators can take this endpoint to `(x,y)`.

The certificates include exact free-word factorizations attaining the area bounds, sparse group-ring coefficients proving the lower bounds, and the complete folded subgroup graph. The last statement does not exclude individual-relator conjugations, so it is not an AC obstruction.

## Exact arithmetic in B3

As in E, put `s=xyx`, `t=xy`. Then

    B = <s,t | s^2=t^3>,    z=s^2=t^3 is central,
    B/<z> = C2*C3.

Total exponent sum sends x,y to 1 and z to 6. An element of B is therefore determined by its exponent sum and its reduced syllable word in `C2*C3`: elements with the same syllable word differ by `z^k`, and the exponent sum detects k. The implementation uses precisely this pair as a group key. The generator images in the free product are

    x -> T^2 S,   X -> S T,   y -> S T^2,   Y -> T S.

All polynomial equalities below are computed in the integral group ring `Z[B]`, using this exact group equality. No finite matrix reduction or bounded word-length identification is used.

## Fox calculation and a self-contained lower bound

Use left Fox derivatives `D_x`, `D_y`, with

    D_i(uv)=D_i(u)+u D_i(v),
    D_x(x)=1, D_x(y)=0, D_x(X)=-X,

and similarly for y. Evaluate their coefficients in B. Direct differentiation gives

    D_x(b) = 1 + xy - y,
    D_y(b) = x - yx - 1.

If a free word w has an expression

    w = product_j q_j b^(epsilon_j) q_j^-1,

then, since b maps to 1 in B, the product rule gives

    (D_x(w),D_y(w)) = K(w) (D_x(b),D_y(b)),
    K(w) = sum_j epsilon_j * image(q_j) in Z[B].

For these calculations the coefficient K is unique. Here is a short argument that avoids assuming a general one-relator identity theorem. Grade `Z[B]` by total exponent sum. The largest grade of `D_x(b)=1+xy-y` is 2, and its grade-2 part is the single monomial xy. If a nonzero finitely supported polynomial P has largest grade h, the grade-(h+2) part of `P D_x(b)` is exactly `P_h * xy`, which is nonzero: right multiplication by a group element permutes its basis. Thus multiplication on the right by `D_x(b)` is injective. Any two coefficients giving the same derivative must agree.

It follows that every product expression for a particular w has the same K. Each conjugate contributes a signed group-ring basis element, so the number of factors is at least

    ||K(w)||_1 = sum_g |coefficient_g(K(w))|.

This proves an area lower bound without a search over diagrams. It also shows that a nonzero K detects a nonzero class in `N/[N,N]`: derivatives of commutators of elements of N vanish.

For additional context, the general freeness result for a non-power one-relator relation module is Lyndon's identity theorem. The elementary grading argument above supplies the specific uniqueness needed here, rather than importing that theorem as an unchecked hypothesis.

## Explicit coefficients

Put `S_X=1+X+X^2+X^3`, an element of `Z[B]`. Exact sparse Fox calculation gives

    K(w0) = Y^4 - S_X,

    K(w1) = XY - Y^3 + (y-X y^3) S_X - X(1+y+y^2).

The first formula has five distinct group elements, with coefficients `+1,-1,-1,-1,-1`. The second has thirteen distinct group elements, all with coefficient `+1` or `-1`. Exact B-normal forms distinguish all of these terms. Their augmentations are both -3, while their l1 norms are 5 and 13. The program verifies both derivative coordinates, not only `D_x`.

These nonzero coefficients prove that E's endpoint errors cannot be silently discarded even after abelianizing the braid-relator kernel. They are not invariants of arbitrary AC transformations of a presentation: the coordinate images in B can change during a path, and the fixed kernel N is an auxiliary choice.

## Matching upper bounds by exact free-word identities

The saved artifact contains sequences of five and thirteen elementary relation rewrites reducing the errors to the empty word. A rewrite replaces a substring u by `v^-1` when `uv` is a cyclic rotation of `b` or `b^-1`. It also records an exact conjugator q and sign epsilon for that step. If the current word is `P u Q`, the new word is `P v^-1 Q`, and the step satisfies

    current = (q b^epsilon q^-1) * next

as an identity of free words. Multiplying the recorded conjugates in step order therefore reconstructs the original error exactly.

The verifier checks every substring, every relation rotation, every freely reduced next word, and the final product of conjugates. The two products have respectively five and thirteen factors, so they attain the independent lower bounds. This proves the exact areas.

For the first error, the five `(epsilon,q)` pairs are:

    (+1, YYYxyXYX),
    (-1, XXyxYXY),
    (-1, XyxYXY),
    (-1, yxYXY),
    (-1, empty).

All thirteen pairs for the second error are recorded in the JSON certificate. A conjugator in the exact factorization must not be replaced merely by a B-equal shorter word; that would generally alter the identity in the free group.

If the original braid relator were still available as a separate coordinate, these factorizations would specify finite corrections. During E's two-coordinate path that coordinate has itself changed. The certificate does not provide an allowed way to restore it while retaining both current endpoint coordinates. Adding a redundant third relator would change the balanced problem and is not used as an ordinary AC move here.

## A separate obstruction to a Nielsen-only completion

The endpoint words from E are

    a = YYYYxyxYXyyyXXXyxyyyyXY,
    c = XYxyxYXyyyXXXyxyyyyXXXyxYYYYXYxxxYYYxyXYXyyyy.

Their exponent-sum matrix is

    [[-2,3],[-3,4]],    determinant 1.

Nevertheless they do not generate F as a subgroup. Folding the based word-loop graph for these two words gives a deterministic inverse graph with **44 vertices and 45 unoriented edges**, hence rank `45-44+1=2`. Both generator words label based loops, while neither single-letter x nor single-letter y labels a based loop. The graph is therefore not the two-petal rose for F. The JSON stores every oriented labeled arc, and the program reconstructs the folds from the words.

This is the usual subgroup-graph method, described in the primary paper [Kapovich–Myasnikov, Stallings Foldings and Subgroups of Free Groups](https://web.stevens.edu/algebraic/alexeim/Teaching/GroupTheory626/graph5.pdf). Every fold preserves the based subgroup; the final inverse labeled graph recognizes its reduced words. A proper finite-index subgroup of F2 has rank `index+1` by the covering-graph Euler characteristic calculation. A proper rank-2 subgroup therefore has infinite index.

Relator inversion, permutation, and left or right multiplication preserve the subgroup generated by the tuple. Hence no sequence consisting solely of such Nielsen operations can finish this particular endpoint. Individual-relator conjugations are allowed in AC and can change that subgroup, so this is only a restriction on a proposed completion strategy.

## Reproduction and verification

From the repository root:

```sh
python3 experiments/braid_relation_module.py \
  certificates/psl2z_quotient_lift.json --diagrams \
  --output certificates/braid_relation_module.json --summary
python3 experiments/braid_relation_module.py \
  --verify certificates/braid_relation_module.json
```

The program uses only the Python standard library. The second command verifies the stored coefficient and diagram evidence without invoking the diagram search or coefficient-division routine. It also reconstructs the subgroup graph. Executed output reports `PASS`, exact areas `[5,13]`, 44 subgroup vertices, rank 2, and `free_group_goal_solved: false`.

Controls include inverse group operations, kernel conjugates with coefficient one monomial, the full twist `(xy)^3` distinguished from the identity by its exponent sum, a nonempty commutator of kernel elements with zero module coefficient, a generating subgroup example, and a proper subgroup example. The zero-coefficient commutator control emphasizes that first-order vanishing alone cannot prove equality in F.

## Remaining research target

A possible next route is to investigate AC connectivity in the nonsolvable extension `F/[N,N]`, where this particular ten-step quotient lift still fails. Alternatively one could search for a different braid-quotient path whose free endpoint subgroup and module defects are simpler. Neither task is completed here. The calculations give precise lifting data and rule out a Nielsen-only suffix for E's current path; they do not settle any of the user's four breakthrough objectives.
