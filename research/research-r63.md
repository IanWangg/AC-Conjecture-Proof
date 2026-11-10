# Research R6-3: extending the exact two-move census of P₃ to intermediate relators of length 10–11

Date: 2026-11-10 (UTC). Agent R6-3, round 6. **Status: in progress** (time-boxed, ~25 minutes).

Scope: P₃ = (c, k₃), c = xyxYYXy, k₃ = xxxYXyy (research-k). TH03 (T14, T15, T18) excluded two-move exits
P₃ → (c,k′) → (exit, k′) with |k′| ≤ 9 (exit = primitive). Here: |k′| = 10 (then 11), and the second move is
tested both for a primitive target and for a BS(1,2)-type target (research-th09, T1/T3).

## 1. Method (all exact; script `experiments/r63_two.py`, built on TH03's `th03_uniform`, `th03_q2`, `th03_two`)

**First move (c frozen).** By TH03 T8(b)/T10, (c,k′) is one c-frozen ACM move from P₃ iff k′^{±1} ~ k₃ in G_c; up to
rotation and inversion k′ is a cyclically reduced word of y-exponent 1 (lexicographically least rotation). Filters, in
order: I(k′) = 20 (T2), ε(k′) = ε(k₃) = 0 (mirror invariant, T16), J(k′) = J(k₃) at the rational points p = 2, 3 (T6).
Every survivor is then **confirmed** conjugate to k₃ by explicit twisted-conjugacy BFS (moves u ↦ φ(u),
u ↦ v·u·φ(v)⁻¹; class of k₃ with normal-form length cap 15 = 4,733 normal forms, intersected with a BFS from the
candidate). Re-run of lengths 8, 9 reproduces TH03 T14 exactly (8: 2 neighbours + 9 excluded; 9: 3 + 17).

**Second move (k′ frozen).** c must become a primitive or a BS(1,2)-type relator (research-th09 Thm 1: a BS(1,2)-type
relator anywhere in the AC class trivializes it). In G_{k′} (t = yx^m, m = x-exponent of k′; abelianization x ↦ 1,
t ↦ 0) the candidates of the right degree are, by Nielsen and research-th09 Thm 3(d) (one-parameter families):
  prim_j = x·tʲ;   bs+_j = Q Q P⁻¹ Q⁻¹ P;   bs−_j = Q Q P Q⁻¹ P⁻¹,   Q = x·tʲ, P = t,   j ∈ ℤ
(bs±_j are the inverses of v(t^{±1}, x tʲ) = P^{∓1}QP^{±1}Q⁻²; c has degree +1, v has degree −1, so c ~ v^{−1} is the
only possibility; by Thm 3(a,b) this covers all BS(1,2)-type killers up to conjugacy and inversion).
Test: twisted traces on the Magnus algebra (TH03 Lemma T11a) of the free-by-cyclic structure (Brown's criterion,
`th03_two.structure`) or — new here — of the **ascending** structure when only the top t-level is unique
(G_{k′} is then the mapping torus of the injective endomorphism θ of F(t₀..t_{r−1}); Freiheitssatz), with normal forms
taken after conjugating all letters to levels ≥ 0 (`structure_asc`, `nf_asc`). Rational traces: the invariant of each
family is a polynomial of degree ≤ D in j (Newton interpolation at j = 0..D, exact), and its integer roots are
computed exactly; 𝔽_p traces: all residues j mod p^e > D. Positive controls (self-test): a member of each family,
used as the moved relator, is found by the corresponding test.

## 2. Results (exact computation; labels as in TH03)

### 2.1 First move: the c-frozen neighbours (c,k′) of P₃ with |k′| = 10 (proved here by exact enumeration)

Cyclically reduced k′ of length 10, y-exponent 1, up to rotation: **52** have I(k′) = 20; **26** of them have ε = 1
(mirror side, not conjugate to k₃ by T16); **11** have J ≠ J(k₃); the remaining **15 are all confirmed** conjugate
to k₃ in G_c by explicit twisted BFS (no undecided case):

    XXyxyxxxxY  XXyXYxYxyy  XXyXYYxxyy  XXYxxyyyXY  XyyxxyxYxY  XyyxYxxyxY  XyyyxxxxYY  XYxxYXyxyy
    XYxyxyxYXy  XYxyxYxyXy  XYxyXyyxxY  XYxyyxxYXy  XYXyxYxyxy  XYYxxyxyXy  XYYYxyyyXy

So (with TH03 T14) the c-frozen neighbours with |k′| ≤ 10 are exactly 7 + 15 = 22 cyclic words.

### 2.2 Second move (k′ frozen): primitive or BS(1,2)-type target (proved here by exact linear algebra, except as stated)

| k′ (len 10) | structure of G_{k′} | prim | bs+ | bs− |
|---|---|---|---|---|
| XXyxyxxxxY | F₄⋊ℤ (m=3) | ℚ, D=4 | ℚ, D=4 | ℚ, D=4 |
| XXyXYYxxyy | F₃⋊ℤ | ℚ, D=3 | ℚ, D=3 | ℚ, D=3 |
| XXYxxyyyXY | F₄⋊ℤ | ℚ, D=4 | ℚ, D=4 | ℚ, D=4 |
| XyyxxyxYxY | F₅⋊ℤ | ℚ, D=3 | ℚ, D=3 | ℚ, D=3 |
| XyyxYxxyxY | F₄⋊ℤ | 𝔽₂, D=4 | 𝔽₂, D=4 | 𝔽₂, D=4 |
| XYxxYXyxyy | F₃⋊ℤ | 𝔽₂, D=5 | 𝔽₂, D=4 | 𝔽₂, D=4 |
| XYxyxyxYXy | F₂⋊ℤ | ℚ, D=3 | ℚ, D=3 | ℚ, D=3 |
| XYxyxYxyXy | F₃⋊ℤ | ℚ, D=3 | ℚ, D=3 | ℚ, D=3 |
| XYxyXyyxxY | F₃⋊ℤ | 𝔽₂, D=4 | 𝔽₂, D=4 | 𝔽₂, D=5 |
| XXyXYxYxyy | ascending, rank 2 | 𝔽₃, D=3 | 𝔽₃, D=6 | 𝔽₃, D=6 |
| XYXyxYxyxy | ascending (via x↔X), rank 2 | 𝔽₃, D=6 | 𝔽₃, D=8 | 𝔽₅, D=5 |
| XYYxxyxyXy | ascending (via x↔X), rank 3 | 𝔽₃, D=3 | 𝔽₇, D=3 | 𝔽₇, D=3 |
| XYYYxyyyXy | ascending (via x↔X), rank 3 | 𝔽₇, D=3 | 𝔽₇, D=3 | 𝔽₇, D=3 |
| **XyyyxxxxYY** | F₇⋊ℤ (m=3) | **open** | **open** | **open** |
| **XYxyyxxYXy** | ascending, rank 2 | **open** | **open** | **open** |

(Entry = coefficient ring and Magnus degree of the twisted traces that leave **no** j, resp. no residue j mod p^e.)
**13 of the 15 length-10 neighbours admit no second-move exit to a primitive or BS(1,2)-type relator.**
Two are undecided: for XyyyxxxxYY the only twisted traces found are constant (ℚ, D ≤ 3; 𝔽_p, D = 3, all p ≤ 31;
𝔽₂, D ≤ 3); for XYxyyxxYXy only constant ones too (ℚ, D ≤ 4; 𝔽₂, D ≤ 9; 𝔽₃, D ≤ 8; 𝔽₅, 𝔽₇, 𝔽₁₁, 𝔽₁₃, D ≤ 8).

### 2.3 BS(1,2)-type second moves through the TH03 neighbours |k′| ≤ 9 (new; proved here)

TH03 T15 excluded only *primitive* second-move targets. The same run (lengths 8, 9; length 7 below) excludes the
BS(1,2)-type targets bs±_j as well: XyyxYYxy (𝔽₂, D=4), XYXyxxxy (ℚ, D=4), XyyxYxyxY (ℚ, D=3), XyyxYxYxy
(𝔽₂, D=5 — this also gives a second, 𝔽₂-valued proof of TH03's ℤ/9 exclusion of its primitive target), and the
ascending XYYxyxyXy (𝔽₃, D=3; for its primitive target TH03's 𝔽₃, D=8 result stands — here D ≤ 4 leaves j ≢ 0, 3, 6 mod 9).
Length 7: k₃ itself (F₃⋊ℤ; ℚ, D=3) and XYxxyXy (F₂⋊ℤ; ℚ, D=4) exclude all three families. **Hence no two-move
exit P₃ → (c,k′) → (BS(1,2)-type or primitive, k′) with |k′| ≤ 9** (primitive part: TH03 T15; BS(1,2) part: here).

### 2.4 First move at length 11 (proved here by exact enumeration); second move only partly run

|k′| = 11: **103** cyclic words with I = 20; 54 have ε = 1, 31 have J ≠ J(k₃); the remaining **18 are all confirmed**
c-frozen neighbours (explicit twisted BFS; no undecided case):

    XXyxxxyyxYY XXyxyxxYYxy XXyXYYxxxyy XXyyxYYYxyy XXYxyxyxyXY XXYxyyxxyXY XXYXyxxYxyy XXYXyxYxxyy XyxyyyxYYxY
    XYxyxxyxYXy XYXyxxyxyxY XYXyxxyxYxy XYXyxxyyxxY XYXyxYxxyxy XYXyxYYxyyy XYYxyyyxYXy XYYxYxyyyXy XYYYxyXyxyy

So the c-frozen neighbours with |k′| ≤ 11 are exactly 7 + 15 + 18 = 40 cyclic words (lengths 7, 8, 9, 10, 11:
2, 2, 3, 15, 18). Second move at length 11: see §3 (time-boxed; only partly run).
