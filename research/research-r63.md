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
