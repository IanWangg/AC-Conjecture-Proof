# Research G follow-up: synchronizing the two infinite deletion quotients

Date: 2026-11-02. Status: explicit ordinary-AC certificate in a stronger infinite quotient, with an exact finite-ball lower bound. **This is not an AK(3) free-group trivialization.** No novelty claim is made.

This follow-up uses the six previous reports and G's complementary torus-quotient certificate. It addresses a genuine gap between the earlier results: a path valid in each factor separately does not automatically give one common instruction path valid in their product.

## Result

Let F=F(x,y), p=x^3 y^-4, b=xyx y^-1 x^-1 y^-1, and

    B=F/<<b>> = B3,
    T=F/<<p>> = <x,y | x^3=y^4>.

Use the diagonal generator images in B times T. There is an explicit sequence of **191 strict elementary AC moves** taking the image of (p,b) to the diagonal pair (x,y) simultaneously in B times T. Every move is a relator inversion, positive right multiplication, or conjugation by one of x,X,y,Y. Thus every homomorphism factoring through this product has a uniform instruction-distance upper bound of 191 in this alphabet.

An exact radius-six bidirectional search in the larger fourteen-instruction alphabet finds no path of length at most twelve. Consequently

    13 <= d_14((p,b),(x,y)) <= 191

in this product. The upper bound is constructive and not claimed optimal. In particular the exact factor distances 10 and 8 do not themselves give a synchronized path of length ten.

The free-group lift of the 191 moves has nontrivial endpoint coordinate lengths **2,539 and 2,159**, with raw peak **4,698**. It passes the independent repository verifier against those actual words. Both errors disappear in B and T, but the verifier does not claim that they disappear in F.

## Why this is a stronger quotient test

Put Np=<<p>> and Nb=<<b>> in F. Since the AK(3) presentation defines the trivial group, Np Nb=F. The usual normal-subgroup Chinese-remainder argument gives

    F/(Np intersect Nb) = B times T.

For completeness, given classes represented by u modulo Nb and v modulo Np, write u^-1 v=n_b n_p with n_b in Nb and n_p in Np. Then w=u n_b=v n_p^-1 has the required two images. The diagonal map is therefore onto the full product, not merely an unspecified subdirect subgroup.

The explicit pure-factor generator words below also verify surjectivity constructively. This product retains more information than either deletion quotient, while still imposing the nontrivial kernel Np intersect Nb. A certificate here cannot be silently lifted across that remaining kernel.

## A synchronization lemma

Consider two groups B,T with designated ambient generators, and two AC programs P_B and P_T. Delete every conjugation from a program, retaining its relator inversions and multiplications, and call the resulting operation on an abstract free pair (a,b) its **bare Nielsen operation**.

Suppose:

1. P_B takes the B component of the starting tuple to the desired B component;
2. P_T takes the T component to the desired T component;
3. their bare Nielsen operations agree exactly, with common operation N;
4. ambient representatives of the needed pure B and pure T conjugators are available in the product.

Then the following is a synchronized product program:

    P_B with pure B conjugators;
    N^-1;
    P_T with pure T conjugators.

Indeed, after the first phase the B pair is its target and the T pair has undergone only N. The middle phase undoes N on the T pair. The final phase gives its T target, while its bare N cancels the middle N^-1 on B. This proof concerns exact free Nielsen operations; equality only of exponent matrices would not suffice without an additional argument.

All phases are ordinary AC operations. No arbitrary quotient simplification is used as a move.

## Aligning the two known programs

Research E gives a ten-instruction program E in B, taking (p,1) to (x,y). Research G gives an eight-instruction program G in T, taking (1,b) to (x,y). Both use C_i(g): r_i -> g r_i g^-1.

Construct aligned versions:

- P_B: first apply r_0 <- r_0 r_1^-1 three times, then apply E. The prefix does nothing in B because r_1=1.
- P_T: first apply r_1 <- r_1 r_0^-1 once, then apply G. This prefix does nothing in T because r_0=1.

Deleting all conjugations, **both programs give exactly**

    (a,b) -> (a b a^-1 b^3 a^-1, b^3 a^-1).

This is checked both by symbolic free cancellation and by the program. Its exponent matrix is [[-1,4],[-1,3]], of determinant one, but the certificate uses the stronger exact word equality.

The bare multiplication ledger of P_B has seven instructions. In the notation M_i^epsilon for right multiplication of coordinate i by the other coordinate to exponent epsilon, it is

    M_0^-, M_0^-, M_0^-, M_1^-, M_1^-, M_0^+, M_1^-.

Its inverse is the reversed ledger with signs reversed. The aligned programs have lengths 13 and 9 when each arbitrary-word conjugation is temporarily treated as one packaged operation, so the synchronized construction has 13+7+9=29 packaged operations. The strict expansion count is given below.

## Explicit pure-factor conjugators

Replay E formally from (p,1), keeping free words instead of imposing the braid relation. Its endpoint words are

    u_B = XXXyxyyyyXY,
    v_B = XyyyXXXyxyyyyXXXyxYYYYXYxxx.

Their images are (x_B,1_T) and (y_B,1_T), respectively. In T they are the identity because every source word in this replay is in the normal closure of p. In B, E's proved endpoint gives x and y. They have lengths 11 and 27.

Similarly, replay G formally from (1,b). Its endpoint words are

    u_T = xyxYXYxxxyxYYYXY,
    v_T = XYxxxyxYYY.

Their images are (1_B,x_T) and (1_B,y_T). They have lengths 16 and 10. Their B images vanish because the words are in the normal closure of b; their T images follow from G's symbolic proof. The script independently checks all four exact product images.

In phase one, replace conjugation by x or y in P_B by conjugation by u_B or v_B, and replace inverse letters by inverse words. In phase three, use u_T and v_T instead. Thus all conjugating elements are explicitly represented by ambient words on the original x,y.

The six phase-one conjugations expand to 98 single-generator conjugations, and the four phase-three conjugations expand to 58. There are nineteen signed multiplications, eight with a negative donor. Expand each negative multiplication into donor inversion, positive multiplication, and donor restoration. The strict move count is

    98+58+19+2*8 = 191.

The saved certificate contains every one of these primitive operations. Conjugation by a word c1...ck is expanded by applying the single-letter conjugations in reverse order, ensuring the stated convention g r g^-1.

## Exact product normal forms and the finite lower bound

For B, use the C2*C3 reduced syllable word together with the exponent-sum homomorphism e_B(x)=e_B(y)=1. As explained in E, the quotient kernel is central with generator (xy)^3 and exponent sum six, so this data determines an element of B exactly. For T, use G's central-extension normal form z^k times a reduced C3*C4 syllable word. Thus a product element is represented without finite reductions or heuristic identifications.

In these exact normal forms, radius-six instruction balls have sizes:

| Radius | From the AK pair | From the diagonal standard pair |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 14 | 10 |
| 2 | 138 | 77 |
| 3 | 1,226 | 574 |
| 4 | 10,609 | 4,445 |
| 5 | 91,840 | 35,390 |
| 6 | 800,777 | 291,197 |
| Total | 904,605 | 331,694 |

The complete balls are disjoint. Every instruction path of length at most twelve has a midpoint in these two balls, proving the lower bound thirteen in the fourteen-instruction graph. The implementation stores no extra length or matrix-entry cap. Its state budget was 1,200,000 per ball and was not reached. The run completed in approximately 22 seconds on the investigation host; time is not part of the mathematical claim.

The upper certificate is independent of this search: its proof is the explicit synchronization construction. The strict free replay and the exact product normal-form replay agree after every phase. The implementation also checks inverse instructions and distinguishes the nontrivial central elements from the identity.

## Reproduce

The two standard-library scripts must be placed together in `experiments/`:

```sh
python3 experiments/product_search.py --certificate-only \
  --certificate certificates/product_quotient_lift.json
python3 experiments/elementary_verify.py certificates/product_quotient_lift.json
python3 experiments/product_search.py \
  --verify-certificate certificates/product_quotient_lift.json
python3 experiments/product_search.py --depth 6 --budget 1200000 \
  --output certificates/product_depth6.json
```

The independent elementary verifier prints the actual free endpoint, which is lengthy. A successful replay does not identify it with (x,y); only the exact product evaluator does so. The certificate explicitly labels its scope, quotient target, actual free target, phase endpoints, and pure-factor words.

The `--verify-certificate` command reads the saved primitive ledger without invoking its constructor. It replays both actual free words and exact product elements, compares the recorded actual target exactly, and independently verifies that the product endpoint is the diagonal basis. Its output explicitly reports the ordinary free-group goal as unsolved.

## Remaining obstruction to the original goal

All quotient metrics from homomorphisms factoring through B times T are now bounded by this one 191-move program. The two deletion quotients and their combined product therefore cannot furnish an unbounded-distance obstruction for this AK(3) tuple.

The remaining errors lie in Np intersect Nb. Removing them by ordinary AC operations in F remains an unsolved lifting problem. The construction does not make those errors available as separate relators, does not use stabilization, and supplies no invariant at unbounded free-word length. None of the user's four breakthrough objectives has been achieved.
