# Research E: an exact ten-move quotient path in the infinite braid group

Date: 2026-11-02. Status: explicit quotient result, **not a free-group AK(3) trivialization**. No novelty claim is made.

## Previous work and independent direction

I first read the actual Research A, B, and C notes in this repository, then Panteleev–Ushakov's primary discussion of AC and quotient-conjugacy moves ([arXiv:1609.00325](https://arxiv.org/html/1609.00325v1), Sections 1–2). Research A establishes a frozen-braid plateau; Research B distinguishes quotient connectivity from quotient distance divergence; Research C supplies a different family representative in the same unresolved free-group class. The root agent's finite PSL(2,p) experiment suggested distances increasing from 3 to 10 for seven small primes. Research D was separately investigating complete finite free-word peak graphs.

I independently chose to ask whether that apparent finite-quotient distance growth is bounded by a single certificate in the **infinite** braid quotient. The answer is yes, with an exact ten-move path. This removes an entire natural quotient family from consideration as a metric-divergence obstruction for AK(3).

## Statement and metric convention

Let

    B = <x,y | xyx=yxy>,
    p=x^3 y^-4,  b=xyx y^-1 x^-1 y^-1.

In B the pair (p,b) is (p,1). Use the following fixed symmetric alphabet of fourteen instructions: invert either coordinate; right multiply either coordinate by the other coordinate or its inverse; conjugate either coordinate by one of x, x^-1, y, y^-1. Each instruction costs one. Relator permutations and arbitrary-word conjugations are **not** assigned unit cost in this convention.

**Result.** The distance from (p,1) to (x,y) in B under this alphabet is exactly **10**. The image pair has distance at most 10 in **every quotient of B**, with the same named generator images and instruction convention.

The upper bound is the explicit path below. The lower bound follows independently either from the exact PSL(2,Z) search described below, or from the root agent's complete PSL(2,19) breadth-first search, which reports distance 10. See [the finite experiment](finite-quotient-experiment.md) and its script `experiments/finite_quotient_distances.py` for the latter computation. Projection cannot increase distance.

## Explicit certificate

Write X=x^-1 and Y=y^-1. Set C_i(g): r_i -> g r_i g^-1. Starting from (r_0,r_1)=(p,1), perform:

| Step | Instruction |
|---:|---|
| 1 | r_1 <- r_1 r_0^-1 |
| 2 | C_1(Y) |
| 3 | C_1(X) |
| 4 | r_1 <- r_1 r_0^-1 |
| 5 | C_0(X) |
| 6 | r_0 <- r_0 r_1 |
| 7 | C_0(X) |
| 8 | C_0(X) |
| 9 | C_0(y) |
| 10 | r_1 <- r_1 r_0^-1 |

Here is exact matrix replay in PSL(2,Z), using

    x = [[1,1],[0,1]],  y = [[1,0],[-1,1]].

Matrices are written (a,b;c,d); a matrix and its negative represent the same projective element.

| Step | r_0 | r_1 |
|---:|---|---|
| 0 | (13,3;4,1) | (1,0;0,1) |
| 1 | (13,3;4,1) | (1,-3;-4,13) |
| 2 | (13,3;4,1) | (4,-3;-13,10) |
| 3 | (13,3;4,1) | (17,4;-13,-3) |
| 4 | (13,3;4,1) | (1,1;-1,0) |
| 5 | (9,11;4,5) | (1,1;-1,0) |
| 6 | (2,-9;1,-4) | (1,1;-1,0) |
| 7 | (1,-4;1,-3) | (1,1;-1,0) |
| 8 | (0,1;-1,2) | (1,1;-1,0) |
| 9 | (1,1;0,1) | (1,1;-1,0) |
| 10 | (1,1;0,1) | (1,0;-1,1) |

## Why the certificate works in B itself

This does not require assuming that matrix equality implies braid-group equality. Put s=xyx and t=xy. The braid group has presentation

    B = <s,t | s^2=t^3>,

with x=t^-1 s and y=s^-1 t^2. Let z=s^2=t^3. This element commutes with both s and t, hence is central. The quotient by z is

    B/<z> = <S,T | S^2=T^3=1> = C_2 * C_3.

The kernel is precisely the cyclic subgroup <z>, since z is central. The total exponent-sum homomorphism e:B->Z sends x and y to 1, and sends z=(xy)^3 to 6. Consequently the pair of data

    (image in C_2*C_3, total exponent sum)

determines an element of B: two elements with the same first component differ by z^k, and equality of the second component implies 6k=0, hence k=0.

The script independently replays the certificate in free-product syllable normal forms, using

    x -> T^2 S,  X -> S T,
    y -> S T^2,  Y -> T S.

Both endpoint normal forms equal the respective normal forms of x and y. Their total exponent sums are both 1. Thus they equal x and y in B, proving the upper bound without any inference from finite matrix reductions. The integer-matrix table supplies a separate check.

## Exact search and independent controls

The standard-library-only script `experiments/psl2z_search.py` enumerates the exact integer-matrix instruction balls of radius 5 around the initial and target pairs in PSL(2,Z), modulo scalar sign only. There is no modular reduction, matrix-entry cutoff, cyclic-conjugacy identification, or heuristic pruning.

The complete layer sizes are:

| Radius | Initial-pair side | Standard-pair side |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 7 | 10 |
| 2 | 48 | 73 |
| 3 | 337 | 446 |
| 4 | 2,625 | 2,500 |
| 5 | 21,521 | 14,506 |
| Total | 24,539 | 17,536 |

Among all intersections the smallest sum of the two stored shortest depths is 10. Every path of length at most 10 has a midpoint within the two radius-5 balls. Therefore this complete search gives exact distance 10 in PSL(2,Z), independently confirming the finite-quotient lower bound. Since this group is a quotient of B, the B-distance is at least 10; the explicit B path gives equality.

The script checks inverse instruction pairs and the quotient relations, then separately checks the saved path through integer matrices, free-product normal forms, and total exponent sums. The limits are explicit: if a requested state budget interrupts a ball, it marks that search incomplete and does not assert a lower bound from incomplete disjoint balls.

Reproduce from the repository root:

```sh
python3 experiments/psl2z_search.py --depth 5 \
  --output certificates/psl2z_depth5.json \
  --certificate certificates/psl2z_quotient_lift.json
python3 experiments/elementary_verify.py certificates/psl2z_quotient_lift.json
```

The supplied search result records the complete layer counts. The supplied lift certificate uses 16 strict positive-multiplication elementary moves, because each of the three negative multiplications expands into donor inversion, positive multiplication, and donor restoration. This is a counting convention; its ten signed instructions are the path displayed above.

## Explicit failure to lift to an AK(3) solution

If these instructions are instead performed in the free group on the actual AK(3) relator pair (p,b), the endpoint is

    (YYYYxyxYXyyyXXXyxyyyyXY,
     XYxyxYXyyyXXXyxyyyyXXXyxYYYYXYxxxYYYxyXYXyyyy).

Its freely reduced coordinate lengths are (23,45). These words are **not** (x,y). The independent root elementary verifier confirms exactly this endpoint, with 16 strict moves and peak total free-word length 68. The saved certificate's `target` is this actual free-word endpoint, while `quotient_target` is separately labelled (x,y). The distinction prevents the quotient result being mistaken for a free-group trivialization.

Both endpoint errors lie in the normal closure of the braid relator. During the free-group path, however, the braid relator has itself been changed; quotient equality does not grant permission to erase those errors. Removing them requires additional AC reasoning that is not supplied here.

## Consequence for further investigation

All congruence quotients PSL(2,p) used in the root experiment factor through B. Their distances are therefore uniformly at most 10. The observed sequence 3,6,9,9,9,9,10 cannot grow without bound: it has already reached this representation family's exact infinite-quotient ceiling. This does not invalidate Research B's finite-quotient distance principle; it says that a successful divergence argument must use homomorphisms that do not all factor through this braid quotient.

The same upper bound applies to every other quotient of B, finite or infinite, under the stated instruction alphabet. Thus this explicit certificate rules out disconnectedness and distance divergence for the entire fixed-braid-quotient approach to AK(3). It does not settle the ordinary free-group problem, the stable problem, or the full conjecture.
