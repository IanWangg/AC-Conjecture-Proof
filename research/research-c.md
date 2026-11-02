# Research C: a uniform ordinary-AC bridge from an MS branch to AK(n)

Date: 2026-11-02. Status: proved family equivalence with replayable certificates; **no AK(3) trivialization and no counterexample**. Novelty is not established.

## Previous work read before choosing this direction

The target repository was empty at the beginning of this investigation. I subsequently read its initial README and verification standard. I reviewed Carreras's [2026 preprint](https://arxiv.org/html/2607.23611v1), especially Sections 2–4 and its [13-move certificate](https://github.com/joe-carr-data/ac-certificates/blob/main/certs/cert_ms3_yinvx2yinv_equiv_ak3.json), and Panteleev–Ushakov's [paper](https://arxiv.org/html/1609.00325), especially its ACM-move and automorphism discussion. These sources distinguish ordinary AC equivalence from isomorphism of the presented groups. The current repository README also records the [corrected Lisitsa publication](https://doi.org/10.1016/j.jaca.2025.100041); the older stable AK(3) claim is not a usable solved case.

I independently chose to examine whether the isolated n=3 Miller–Schupp certificate admits a parameter-uniform symbolic extension. This is more targeted than another search from AK(3) and supplies a verified family of alternate starting points. The n=3 move pattern is credited to Carreras; the parameterized proof below was obtained during this investigation. I have not established whether this uniform equivalence already appears elsewhere in the literature.

## Result

For every integer n >= 2, the ordered relator tuple

    M_n = (x^-1 y^n x y^-(n+1), x^-1 y^-1 x^2 y^-1)

is ordinary Andrews–Curtis equivalent to

    K_n = (xyx y^-1 x^-1 y^-1, x^n y^-(n+1)).

Thus the presentation commonly denoted MS(n, y^-1 x^2 y^-1) belongs to the AC class of AK(n). For n=3 this recovers the known MS-to-AK equivalence, rather than eliminating AK(3).

No stabilization, quotient inference, or ambient generator change is used. The certificate reaches the inversion/rotation orbit of K_n in 2n+7 packaged moves, where a rotation is counted as one packaged operation. Every rotation is a finite sequence of ordinary single-generator conjugations. Four additional packaged operations reach K_n exactly, with an explicitly expanded certificate provided for n=3.

## Complete symbolic proof

Write X=x^-1 and Y=y^-1. Let A and B denote the current first and second relators. Products are freely reduced after every operation. Define C_i(g) to replace relator i by g r_i g^-1, and L_i(k) to rotate its current word k letters to the left, followed by free reduction. If r=uv and |u|=k, then L_i(k) is conjugation by u^-1 because u^-1(uv)u=vu. This is an ordinary AC operation, expanded into single-generator conjugations in the supplied program.

Starting from (X y^n x Y^(n+1), X Y x^2 Y), perform the following ten operations. The displayed words are exact free-group words, not identities in a quotient.

| Step | Operation | A | B |
|---|---|---|---|
| 0 | start | X y^n x Y^(n+1) | X Y x^2 Y |
| 1 | L_0(n+3) | Y^n X y^n x Y | X Y x^2 Y |
| 2 | B <- B A^-1 | Y^n X y^n x Y | X Y x Y^n x y^n |
| 3 | C_0(Y) | Y^(n+1) X y^n x | X Y x Y^n x y^n |
| 4 | B <- B A | Y^(n+1) X y^n x | X Y x Y^n x Y X y^n x |
| 5 | L_1(2) | Y^(n+1) X y^n x | x Y^n x Y X y^(n-1) |
| 6 | C_0(x) | x Y^(n+1) X y^n | x Y^n x Y X y^(n-1) |
| 7 | A <- A B^-1 | x Y^(n+1) X y x y X y^n X | x Y^n x Y X y^(n-1) |
| 8 | L_0(n+1) | Y X y x y X | x Y^n x Y X y^(n-1) |
| 9 | B <- B^-1 | Y X y x y X | Y^(n-1) x y X y^n X |
| 10 | L_1(n+1) | Y X y x y X | X y^n X Y^(n-1) x y |

For the tail, keep A=c=Y X y x y X fixed. For k=1,...,n-1 do B <- Bc, and if k<n-1 subsequently do C_1(X).

Immediately before multiplication k the second relator is

    X^k y^n X Y^(n-k) x y.

Multiplying by c freely reduces it to

    X^k y^n X Y^(n-k-1) x y X.

When k<n-1, conjugating by X gives the required formula for the next iteration. At k=n-1, the middle Xx cancels and the terminal second relator is

    X^(n-1) y^(n+1) X.

The resulting pair is therefore

    (Y X y x y X, X^(n-1) y^(n+1) X).

The first word is a cyclic rotation of the inverse of xyxYXY. The second is a cyclic rotation of the inverse of x^n Y^(n+1). Inversion and rotation are AC operations, proving the claimed ordinary equivalence. For an exact endpoint, invert the first relator and rotate left 4; then invert the second and rotate left n+2. No relator permutation is needed.

There are ten initial packaged moves, n-1 tail multiplications, and n-2 tail conjugations: 2n+7 in total before endpoint normalization. Inspecting the table and tail shows packaged total relator length never exceeds 4n+11, attained after step 7. This is an upper bound for this particular bridge, not a minimal bottleneck claim.

The compiler chooses the shorter direction for each rotation. Its four rotation costs are n, 2, n+1, n+1. Replacing each of the two negative multiplications by three strict operations gives **5n+11 strict elementary moves** to the displayed orbit member. Explicit endpoint normalization costs a further n+3 moves, giving **6n+14 strict elementary moves** to the exact ordered tuple K_n. These are constructive upper bounds, not optimality claims.

## Reproduction and independent verification

The accompanying independently implemented `experiments/ms_ak_family.py` uses only the Python standard library. It emits freely reduced integer words and compiles every rotation into single-letter conjugations. Negative multiplication is expanded into donor inversion, positive right multiplication, and donor restoration; the resulting elementary certificates use only the strict three ordinary move types.

From the repository root:

```sh
python3 experiments/ms_ak_family.py --self-test --n 3 \
  --output certificates/ms3_to_ak3.json \
  --root-output certificates/ms3_to_ak3_exact.json
python3 experiments/ms_ak_family.py --verify certificates/ms3_to_ak3.json
python3 experiments/elementary_verify.py certificates/ms3_to_ak3_exact.json
```

The family generator and saved-certificate verifier are separate functions. The latter replays the stored elementary moves without invoking the generator or rotation compiler. The root agent's independently written verifier checks the fully expanded certificate against an exact endpoint, without any implicit rotations, inversions, or normal forms.

Executed results in this investigation:

- Parameters n=2,...,100 all replayed successfully and matched the proved terminal formula, the 2n+7 packaged count, and packaged peak 4n+11.
- Four corrupt-certificate controls were rejected: changed terminal operation, invalid conjugator, multiplication by the same relator, and changed target.
- n=3: 13 packaged moves; 26 strict elementary moves to its recorded target orbit; elementary peak total length 23.
- n=3 exact-endpoint certificate: **32 strict elementary moves**, peak total length **23**, endpoint `(xyxYXY, xxxYYYY)`; passed the independent root verifier.
- n=2: 11 packaged moves, 21 strict elementary moves, peak 19. n=10: 27 packaged moves, 61 strict elementary moves, peak 51.

Carreras reports 22 classical moves for n=3 before endpoint normalization. Our count is 26 because our strict elementary convention expands each of the two negative multiplications into three operations, adding four moves. This is a counting convention, not a different endpoint claim.

The finite replay tests support the implementation; the symbolic table and induction prove the entire infinite family. None of these computations asserts global search completeness or a lower bound for ordinary AC paths.

## Insight and remaining barrier

The apparent Baumslag–Solitar-shaped relator in M_n hides a braid relator after a fixed ten-step prefix. The remaining dependence on n is a linear cancellation loop. This supplies a uniform, low-overhead bridge between two descriptions of the same difficult AC class.

It does not lower n, reach a primitive relator, or connect AK(3) to `(x,y)`. In particular, proving M_3 is AC-trivial would now require the same unresolved step as proving AK(3) AC-trivial. A future search can use the family bridge as a certificate-backed change of starting presentation; it must supply a genuinely new outgoing connection to make progress on the user's four breakthrough targets.
