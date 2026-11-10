# Research R6-3: extending the exact two-move census of P₃ to intermediate relators of length 10–11

Date: 2026-11-10 (UTC). Agent R6-3, round 6. **Status: final for this time box.** No exit found. Exact results: (i) the c-frozen neighbours (c,k′) of P₃ with |k′| = 10, 11 are exactly 15 + 18 cyclic words (complete, all confirmed by explicit twisted conjugators); (ii) for 14 of 15 (length 10) and 14 of 18 (length 11) of them, no second (k′-frozen) move reaches a primitive **or** a BS(1,2)-type relator; (iii) for the 7 TH03 neighbours with |k′| ≤ 9 the BS(1,2)-type second move is now excluded too. Undecided: 1 target at length 10 (XYxyyxxYXy), 4 at length 11 (§2.2, §2.4). The k₃-frozen side at |c′| = 9 was not attempted. A bounded census is not an obstruction.

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
taken after conjugating all letters to levels ≥ 0 (`structure_asc`, `nf_asc`). If only the bottom level is unique, the
automorphism σ: x ↔ X is applied to k′, c and the families (σ(c)⁻¹ is tested; the union of the three families is
σ-and-inversion stable by th09 Thm 3(a,b), with j ↦ −j). Rational traces: the invariant of each
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
| XyyyxxxxYY | F₇⋊ℤ (m=3) | 𝔽₂, D=4 | 𝔽₂, D=4 | 𝔽₂, D=4 |
| **XYxyyxxYXy** | ascending, rank 2 | **open** | **open** | **open** |

(Entry = coefficient ring and Magnus degree of the twisted traces that leave **no** j, resp. no residue j mod p^e.)
**14 of the 15 length-10 neighbours admit no second-move exit to a primitive or BS(1,2)-type relator.**
(XyyyxxxxYY: only constant traces in degree 3 for ℚ and all 𝔽_p, p ≤ 31; the 18 𝔽₂-valued traces of degree 4,
2,801 monomials, exclude all residues mod 8.) One is undecided: for XYxyyxxYXy the only twisted traces found are constant (ℚ, D ≤ 4; 𝔽₂, D ≤ 9; 𝔽₃, D ≤ 8; 𝔽₅, 𝔽₇, 𝔽₁₁, 𝔽₁₃, D ≤ 8).

### 2.3 BS(1,2)-type second moves through the TH03 neighbours |k′| ≤ 9 (new; proved here)

TH03 T15 excluded only *primitive* second-move targets. The same run (lengths 8, 9; length 7 below) excludes the
BS(1,2)-type targets bs±_j as well: XyyxYYxy (𝔽₂, D=4), XYXyxxxy (ℚ, D=4), XyyxYxyxY (ℚ, D=3), XyyxYxYxy
(𝔽₂, D=5 — this also gives a second, 𝔽₂-valued proof of TH03's ℤ/9 exclusion of its primitive target), and the
ascending XYYxyxyXy (𝔽₃, D=3; for its primitive target TH03's 𝔽₃, D=8 result stands — here D ≤ 4 leaves j ≢ 0, 3, 6 mod 9).
Length 7: k₃ itself (F₃⋊ℤ; ℚ, D=3) and XYxxyXy (F₂⋊ℤ; ℚ, D=4) exclude all three families. **Hence no two-move
exit P₃ → (c,k′) → (BS(1,2)-type or primitive, k′) with |k′| ≤ 9** (primitive part: TH03 T15; BS(1,2) part: here).

### 2.4 First move at length 11 (proved here by exact enumeration) and second move

|k′| = 11: **103** cyclic words with I = 20; 54 have ε = 1, 31 have J ≠ J(k₃); the remaining **18 are all confirmed**
c-frozen neighbours (explicit twisted BFS; no undecided case):

    XXyxxxyyxYY XXyxyxxYYxy XXyXYYxxxyy XXyyxYYYxyy XXYxyxyxyXY XXYxyyxxyXY XXYXyxxYxyy XXYXyxYxxyy XyxyyyxYYxY
    XYxyxxyxYXy XYXyxxyxyxY XYXyxxyxYxy XYXyxxyyxxY XYXyxYxxyxy XYXyxYYxyyy XYYxyyyxYXy XYYxYxyyyXy XYYYxyXyxyy

So the c-frozen neighbours with |k′| ≤ 11 are exactly 7 + 15 + 18 = 40 cyclic words (lengths 7, 8, 9, 10, 11:
2, 2, 3, 15, 18).

**Second move at length 11** (same tests; coefficient ring, degree that leaves no j): excluded for **14 of 18** —
XXyxxxyyxYY, XXyxyxxYYxy, XXYxyxyxyXY, XXYxyyxxyXY, XXYXyxYxxyy, XyxyyyxYYxY, XYxyxxyxYXy, XYXyxxyxyxY,
XYXyxxyyxxY, XYXyxYxxyxy (default schedule: ℚ D ≤ 4, 𝔽₂ D ≤ 7, 𝔽₃/𝔽₅/𝔽₇ D = 3); XXYXyxxYxyy (ascending rank 3;
bs+ needs 𝔽₃, D=5), XYXyxYYxyyy (ascending rank 2; bs± need 𝔽₂, D=8), XYXyxxyxYxy (ascending rank 2; prim 𝔽₃ D=6,
bs− 𝔽₅ D=5, bs+ 𝔽₃ D=8), XYYxyyyxYXy (ascending rank 2; all three 𝔽₃, D=6).
**Not handled (4):** XXyXYYxxxyy, XXyyxYYYxyy, XYYxYxyyyXy, XYYYxyXyxyy — Brown fails and neither extreme t-level is
unique (also after x ↔ X), so G_{k′} is not a mapping torus of a free group endomorphism in either direction and the
twisted-trace machinery does not apply as implemented; these are **undecided**.

### 2.5 The undecided length-10 neighbour (experiment, bounded)

For k′ = XYxyyxxYXy (G_{k′} ascending HNN of rank 2, θ: t₀ ↦ t₁, t₁ ↦ word in t₀, t₁) a BFS of the twisted class of c
(moves u ↦ θ(u), u ↦ g·u·θ(g)⁻¹; length cap 14: 235 normal forms, cap 18: 1,142) meets none of the BFS classes of prim_j, bs±_j for
|j| ≤ 6 (`scratch bfsasc.py`). Not a proof; it remains **undecided**.

## 3. Commands (one core, each < 1 min except where noted; outputs in the scratch directory, not committed)

```
python3 experiments/r63_two.py --selftest 8 9     # family controls; reproduces TH03 T14 (8: 2+9, 9: 3+17) and T15
python3 experiments/r63_two.py 10                 # census L=10 + second moves (Brown and ascending cases;
                                                  #   XyyyxxxxYY via F_2, D=4, ~10 s); about 1 min
python3 experiments/r63_two.py 7 11               # L=7 second moves (BS families); L=11 census
```
**Final check (05:41 UTC):** `python3 experiments/r63_two.py --selftest 10 11` (≈ 1 min, default schedule ℚ D ≤ 4;
𝔽₂ D ≤ 8; 𝔽₃ D ≤ 8; 𝔽₅ D ≤ 5; 𝔽₇ D = 3) reproduces every verdict of §2.1–2.4 in one run (L=10: 14 excluded, XYxyyxxYXy
open; L=11: 14 excluded, 4 not handled); log saved as `certificates/r63_run_10_11.log`.
Earlier, the ascending targets, the deeper 𝔽_p scans and the L = 11 second moves were run through `r63_two.second`,
`structure_asc`, `nf_asc`, `modp_test` from small drivers in the scratch directory (deep.py, deep2.py, asc.py).

## 4. Honest limits

- A bounded census is **not an obstruction**: two-move exits through c-frozen neighbours of length ≥ 12 (and through
  the undecided ones below) are not excluded; the general two-move question stays open.
- Undecided: second move for k′ = XYxyyxxYXy (length 10) — only constant twisted traces found; and for
  the four length-11 targets of §2.4 with no unique extreme t-level (method not applicable).
- The BS(1,2) families rely on research-th09 Thm 3(a,b,d) (read, not re-derived beyond the degree count above) and the
  primitive family on Nielsen (recalled). The ascending-case soundness is TH03's §8 argument (Lemma T11a needs no
  invertibility; the base group embeds by the Freiheitssatz) — checked here only by `NF(k′) = (1, 0)`.
- The k₃-frozen side at |c′| = 9 was **not** attempted (time).
- Exact arithmetic throughout (Fractions, integers mod p via numpy int64 with asserted nullspace checks).

## Coordinator's check (2026-11-09, Los Angeles time)

- Re-ran `PYTHONDONTWRITEBYTECODE=1 python3 experiments/r63_two.py --selftest 10 11` (exit 0, "selftest ok (family controls)"); the per-target lines reproduce the note's counts (second moves excluded vs. undecided; see the commit message). `certificates/r63_run_10_11.log` is a run log, **not** an AC certificate.
- Not re-derived by the coordinator: the correctness of each twisted-trace exclusion; these rest on research-th03's method, whose core the referee research-th19 verified.
- Status, stated plainly: no two-move exit P₃ → (c, k′) → (primitive or BS(1,2)-type relator, k′) exists with |k′| ≤ 9 (all decided), and with |k′| = 10, 11 all but five intermediate relators are decided negatively; the five undecided ones (XYxyyxxYXy at length 10; XXyXYYxxxyy, XXyyxYYYxyy, XYYxYxyyyXy, XYYYxyXyxyy at length 11) are listed in the note. The k₃-frozen side beyond TH03's |c′| ≤ 8 was not attempted. A bounded census is not an obstruction.
