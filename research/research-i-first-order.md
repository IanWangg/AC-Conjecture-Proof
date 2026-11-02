# Research I addendum: an actual AC correction in the braid relation-module extension

Date: 2026-11-02. Status: a concrete finite ordinary-AC certificate in an infinite nonsolvable quotient of F2. **This is not an AC trivialization in F2.** No novelty claim is made.

## New previous work and chosen next step

After the original Research I audit, I read Research G's synchronized product construction, its actual free-word lift, and its code. The new prefix supplies one common instruction path whose endpoint maps to `(x,y)` in both the braid quotient and the complementary torus quotient. Its actual free words still have lengths 2,539 and 2,159.

I chose to use that synchronization to construct an actual correction in a larger braid-kernel extension, rather than only measure the new errors. The key extra information is that these endpoint words have exactly the same abelianization in F2 as x and y. This makes their braid relation-module errors augmentation-zero and therefore explicitly correctable by ordinary AC operations modulo the commutator subgroup of the braid-relator kernel.

## Concrete result

Let

    F=F(x,y),  b=xyxYXY,  N=<<b>>,  B=F/N=B3,
    E=F/[N,N].

Here X and Y denote the inverse free generators. There is an explicit ordinary-AC path taking AK(3)'s tuple `(xxxYYYY,xyxYXY)` to `(x,y)` **in E**. It consists of G's 191 strict moves followed by 14 ordinary word-conjugation/multiplication operations. Every conjugating word is stored explicitly, and every word conjugation can be expanded into conjugations by signed free generators.

Checked certificate data:

| Quantity | Value |
|---|---:|
| Total stored word operations | 205 |
| Expansion into strict single-generator moves | 531,377 |
| Final actual free-word lengths | 230,627 and 946,303 |
| Final braid relation-module error supports | 0 and 0 |
| Peak total length at stored operation boundaries | 1,176,950 |
| Proven upper bound for the expanded generator-level raw peak | 1,423,410 |

The generator-level count follows by explicit expansion; the saved verifier replays the 205 stored operations as exact free-word operations and separately checks that expansion rule. It does not naively run 531,377 successive whole-string conjugations. The boundary peak is not asserted to be the exact peak of the expanded sequence.

The quotient E is infinite and nonsolvable because it surjects onto B3, which surjects onto `C2*C3`. Thus this certificate is beyond the fixed nilpotent quotient calculations in B. It also shows that E itself cannot obstruct AK(3)'s AC triviality.

## Why zero Fox error really means equality in E

The earlier report computed Fox derivatives over `Z[B]`. For clarity, the following argument proves the converse needed for the new certificate.

The relation module `N_ab=N/[N,N]` is generated over `Z[B]` by the class of b. There is a well-defined surjection

    Phi: Z[B] -> N_ab,
    Phi(g) = class of q b q^-1, where q maps to g.

Changing the lift q by an element of N only conjugates within N, which acts trivially on its abelianization. Every product of conjugates of b gives a sum of such classes, proving surjectivity.

Fox derivatives evaluated in B define a homomorphism

    delta: N_ab -> Z[B]^2.

Indeed, words in N have quotient image 1, so their derivatives add under multiplication; consequently their commutators differentiate to zero. Conjugation by q acts on their derivatives by left multiplication by its image in B. Therefore

    delta(Phi(P)) = (P D_x(b), P D_y(b)).

Direct differentiation gives

    D_x(b)=1+xy-y,   D_y(b)=x-yx-1.

Right multiplication by `D_x(b)` is injective. Grade `Z[B]` by the homomorphism sending x,y to 1. For nonzero finitely supported P of largest grade h, the grade-(h+2) part of `P D_x(b)` is exactly `P_h xy`, which is nonzero because multiplying by xy permutes group-ring basis elements.

Thus `delta Phi` is injective. Since Phi is surjective, delta is injective as well. For a word w already known to lie in N, this proves

    D_x(w)=D_y(w)=0  iff  w lies in [N,N].

Consequently the saved verifier's exact B-normal-form and Fox-pair checks prove equality in the actual group E, not just in an unspecified linear approximation. This argument is a direct proof for this braid relator; general one-relator relation-module results are discussed in [Putman's notes, Section 6](https://academicweb.nd.edu/~andyp/notes/OneRelator.pdf).

## The correction lemma

Identify a kernel word's class in `N_ab` with its coefficient H in `Z[B]`. Suppose the current relators have the form

    a = (kernel error K) * x,
    c = (kernel error L) * y

in E. Let h be any fixed ambient word in N, with class H. Because `N_ab` is abelian, conjugating the first coordinate by h changes its error by

    C_h(a): K -> K + (1-x)H,

while leaving c unchanged. Here `C_g(r)=g r g^-1`.

There is also a six-operation macro that adds `(1-y)H` to K, still leaving c unchanged:

1. `a <- x a X`.
2. `a <- a c`.
3. `a <- h a h^-1`.
4. `a <- a c^-1`.
5. `a <- h^-1 a h`.
6. `a <- X a x`.

To check the action exactly, step 1 takes K to xK. The conjugation in step 3, applied to a coordinate with quotient image xy, adds `(1-xy)H`; restoring the donor in step 4 leaves that addition on a. Step 5 subtracts `(1-x)H`. Hence before step 6 the error is

    xK + (1-xy)H - (1-x)H = xK + x(1-y)H.

Step 6 multiplies this error on the left by X, giving `K+(1-y)H`. The y-coordinate version exchanges x,y and the coordinate roles. The code separately tests both macros on nontrivial free-word kernel errors by exact free-word replay followed by Fox evaluation.

The action factors and their order matter: replacing `(1-xy)` by a commutative expression would invalidate this macro.

## Every augmentation-zero error is correctable

Let I be the augmentation ideal of `Z[B]`. Every finitely supported K in I has a finite decomposition

    K = (1-x)A + (1-y)B.

This is a right-ideal decomposition. To construct it, write each basis element g as a word `a_1...a_l` in x,X,y,Y and use right telescoping:

    g-1 = sum_i (a_i-1) a_(i+1)...a_l.

For a positive x letter, `x-1=-(1-x)`; for its inverse, `X-1=(1-x)X`. The same formulas hold for y,Y. Since the coefficient sum of K is zero, summing these decompositions gives the displayed A,B exactly.

Any finite coefficient H is represented by an actual kernel word: for each term `n_g g`, choose an ambient word q_g representing g in B and multiply `q_g b q_g^-1` or its inverse `|n_g|` times. The code verifies the resulting word's quotient image and both Fox derivatives exactly.

Use direct conjugation with H=-A, and then the cross macro with H=-B, to kill K while preserving the other coordinate. Correct the second coordinate in the same fashion. This takes two direct conjugations and two six-operation macros: fourteen stored operations in total.

This is a constructive lemma with finitely specified ordinary AC moves. It does not require keeping b as a donor relator: b occurs only inside permitted fixed ambient conjugating words.

## Why G's new prefix supplies the missing augmentation condition

For a kernel word with coefficient K, its F2 exponent vector is

    augmentation(K) * (1,-1),

because b has exponent vector `(1,-1)`. Thus errors with zero F2 abelianization have augmentation zero.

G's synchronized endpoint maps to `(x,y)` in B and in `T=<x,y|x^3=y^4>`. The two abelian quotient homomorphisms send an exponent vector `(u,v)` respectively to

    u+v,    4u+3v.

Their coefficient matrix has determinant -1, so together they determine the original exponent vector. Hence the actual free endpoint from G has exactly the F2 abelianization of `(x,y)`, as also checked directly in the code.

The initial module supports are 54 and 81, their l1 norms are 88 and 116, and both augmentations are zero. The four correction phases have these checked values:

| Phase | Ambient conjugator length | Error support sizes after phase |
|---|---:|---|
| First coordinate, own direction | 57,280 | 1,169 and 81 |
| First coordinate, cross direction | 54,604 | 0 and 81 |
| Second coordinate, own direction | 118,226 | 0 and 1,963 |
| Second coordinate, cross direction | 123,230 | 0 and 0 |

Intermediate error growth is allowed. The important conclusion is exact final vanishing, proved by the quotient-equality criterion above.

These corrections preserve the B3 coordinate images but need not preserve the torus factor. The result is a path in `F/[N,N]`, not an asserted path in a quotient simultaneously refining `B3 times T`. The product prefix is used to obtain the needed abelianization alignment.

## Ordinary-move expansion and actual free-word failure

For a word `h=h_1...h_k`, applying the single-letter conjugations in reverse order `h_k,...,h_1` gives conjugation by h exactly. It uses k strict generator-conjugation moves. A negative right multiplication is replaced by inversion of the donor, positive multiplication, and restoration of the donor, using three strict moves. These rules give the finite count 531,377.

The certificate records the actual long free endpoint, not `(x,y)` as a claimed free target. Its two SHA-256 hashes are

    dafda3343853ec90218d53ffbbf733670d1574a3a393d7d08370749ded0e89ab
    9dc81d1073b8bdd8a356be1def1a47a1d4e4c725530ef1534c66a47ccf19630f

The words are not x,y. A separate optimized C++ subgroup fold finds 1,176,895 vertices and 1,176,896 unoriented edges, rank 2, and accepts neither x nor y as a based loop. Thus the corrected tuple still generates a proper subgroup of F2; a Nielsen-only suffix cannot secretly finish it. This folding code agrees with the earlier independent Python fold on E's original 44-vertex endpoint graph.

These facts do not rule out further ordinary AC moves. In particular, the exact final errors lie in `[N,N]` and need not be the identity. Repeating ever deeper quotient corrections, if possible, would still not produce a finite free-group certificate without a separate finite termination argument.

## Reproduce

The saved 1,723,317-byte JSON certificate is supplied as a 54,800-byte gzip/base64 text file to keep repository transfers compact. Its exact words and operations remain fully present after decoding; no external database or omitted search state is required. The loader detects `.gz.b64` and decodes it with the Python standard library.

From the repository root:

```sh
python3 experiments/first_order_correction.py \
  --verify certificates/first_order_correction.json.gz.b64
```

This replays every stored operation as a free-word operation, checks the recorded exact endpoint and hashes, recomputes its B3 normal forms and both Fox derivatives, and recomputes the expansion count. It does not invoke the augmentation-decomposition or correction-word generator.

To regenerate the certificate from G's synchronized prefix:

```sh
python3 experiments/first_order_correction.py \
  --source certificates/product_quotient_lift.json \
  --output certificates/first_order_correction.json.gz.b64
```

The script imports the earlier `experiments/braid_relation_module.py`; both use only the Python standard library. The saved verification report is `results/first_order_verification.json`.

The independent subgroup check can be reproduced by exporting the verified endpoint:

```sh
python3 experiments/first_order_correction.py \
  --verify certificates/first_order_correction.json.gz.b64 \
  --endpoint-output /tmp/ac_first_order_endpoint.txt
c++ -std=c++17 -O2 experiments/fold_endpoint.cpp -o /tmp/ac_fold_endpoint
/tmp/ac_fold_endpoint /tmp/ac_first_order_endpoint.txt
```

The mathematical completion criterion remains an exact path to the basis in F2, or a global invariant proving none exists. This addendum removes the first braid-kernel module defect by an actual finite AC path, but it does not satisfy that completion criterion.
