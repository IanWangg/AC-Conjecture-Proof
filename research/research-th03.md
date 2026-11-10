# Research TH03: no single generalized move from P_3 reaches a primitive relator — the length spectrum of the Gieseking coordinates (uniform in n) and twisted traces for the killer side

Date: 2026-11-09 (Los Angeles). Independent research agent TH03 (round 5, theory round).

**Status:** partial, fully proved results about *single generalized (ACM) moves* from P_n (for the c-frozen side uniformly in n ≥ 3; for the k_n-frozen side for n = 3, 4, 5). Headline: **no presentation with a primitive relator is one ACM move from P₃ ~AC AK(3), whichever relator is frozen** (T7 + T11) — the complete P₃-analogue of G's Proposition G2; this closes O's open question Q2 for n = 3. Also: the complete answer to O's question Q1 — **k_n is conjugate to xˢy in ⟨x,y | c⟩ iff n ∈ {1,2} and s = −2** (T17) — and a "mirror theorem" (T16). **No AC trivialization of AK(3), no proof of non-triviality, no counterexample, nothing on the full conjecture.** Every statement is labelled *proved here*, *proved here by exact computation* (script with self-test), *experiment* (exact bounds), *recalled*, or *open*.

| # | statement | label |
|---|---|---|
| T1 | Explicit ρ: F(a,b) → SL(2,ℤ[ω]) and Y ∈ SL(2,ℤ[ω]) with Y·conj(ρ(u))·Y⁻¹ = ρ(φ(u)) for all u; T = Y·conj(Y) gives a representation of the index-2 subgroup H in SL(2,ℤ[ω]) | proved here (hand-checked identities; re-checked by script) |
| T2 | I(u) := tr(ρ(u)Y·conj(ρ(u)Y)) is a **rational integer** depending only on the conjugacy class of (u,1) in G_c (no sign ambiguity, no twist ambiguity) | proved here |
| T3–T5 | σ(s) := I(xˢy) and τ(n) := I(k_n) satisfy u(n+4) = 3u(n+3) − u(n+2) + 3u(n+1) − u(n); σ(s) = σ(1−s); σ(n) < τ(n) < σ(n+1) for all n ≥ 6; **the equation τ(n) = σ(s), n ≥ 1, has exactly the solutions n ∈ {1,2} (s ∈ {−2,3}), n = 4 (s ∈ {−4,5}), n = 5 (s ∈ {−5,6})** | proved here (integer induction; base cases by exact computation) |
| T6 | k_4 ≁ x⁵y, x⁻⁴y and k_5 ≁ x⁶y, x⁻⁵y in G_c, although they have the same invariant I ("isospectral") | proved here by exact rational computation |
| **T7** | **For every n ≥ 3 and every s ∈ ℤ, k_n is not conjugate in G_c to xˢy. Hence for every n ≥ 3 no presentation with a primitive relator is one ACM move (arbitrary conjugators) from P_n = (c, k_n) with c frozen.** Uniform version of O6 (n = 3,…,8), the P_n-coordinate analogue of G2 | proved here (T2 + T5 + T6 + O's Prop. O2) |
| T8 | τ is strictly increasing on n ≥ 2: for n ≠ m (n, m ≥ 2) no c-frozen ACM move joins P_n and P_m (answers K's advice 1(b) negatively); every c-frozen neighbour (c,w) of P_n has I(w^{±1}) = τ(n) | proved here |
| T9 | α: x ↦ x⁻¹, y ↦ yx is an involution of F(x,y) with α(c) conjugate to c⁻¹ (a "mirror" symmetry of G_c); it sends xˢy to a conjugate of x^{1−s}y and k_n to a conjugate of x⁻ⁿy⁻¹xyxy, and preserves I and every SL₂-trace invariant; so such invariants can never separate k_n from α(k_n) (T16 does) | proved here |
| **T11** | **k_n-frozen side (O's open question Q2).** G_{k_n} = F(t₀,…,t_{n−1}) ⋊_ψ ℤ, c = (t₁t₂⁻¹t₁⁻¹, 1), and the primitive candidates are xtʲ = (t₁ʲ, 1). An explicit integer *twisted trace* ℓ on the Magnus algebra truncated in degree 3 gives ℓ(c) = −2 but ℓ(xtʲ) = j(j−1)/2 ≥ 0. **Hence c is conjugate to no primitive element in ⟨x,y \| k₃⟩, and — with T7 — no presentation with a primitive relator is one ACM move from P₃ = (xyxYYXy, xxxYXyy), whichever relator is frozen, with arbitrary conjugators (also after any automorphism of F₂).** Same conclusion for n = 4 (𝔽₂-valued twisted traces, degree 4) and n = 5 (rational, degree 3) | proved here (short theory + exact linear algebra, script with self-test); n ≥ 6 **open** |
| T13 | Second, all-integer invariant on G_c: the degree-4 twisted trace L4, with L4(xˢy) = C(s+1,4) ≥ 0 and L4(k_n) = 1, 1, −1, −5, −10, −14, −14, −6, 15 (n = 1..9): an independent proof of O6 (n = 3..8) by a sign, and of T6 | proved here (exact linear algebra) |
| **T16, T17** | **Mirror theorem and complete classification (by hand).** ε(u) = C(p+1,2) + C(q+1,2) + μ_ab(u) mod 2 is a conjugacy invariant of (u,1) and is *flipped* by α; so no degree-1 element of G_c is conjugate to its mirror image. Consequences: xˢy ~ x^{s′}y iff s = s′ or {s,s′} = {−1,0} or {1,2} (O4's bounded observation, now for all s); **k_n ~ xˢy iff n ∈ {1,2} and s = −2**; P_n → α(P_n) is never one c-frozen move | proved here (six mod-2 identities, displayed) |
| T14 | Exact c-frozen neighbourhood of P₃ for second relators of length ≤ 9: exactly 7 cyclic words are neighbours (25 excluded by J, 11 mirror words excluded by ε); **no c-frozen ACM move shortens P₃** (every neighbour (c,w) has \|w\| ≥ 7) | proved here by exact enumeration |
| T10, T15 | Two-move exits P₃ → (c,k′) → (primitive, k′): exact reformulation; **excluded for 6 of the 7 first-move targets k′ of length ≤ 9**, undecided for one (XyyxYxYxy) | proved here (bounded census); the general two-move question is **open** |

## 1. Previous work read and choice of direction

Read in full: `README.md`, `research/research-o.md` (with the coordinator's review), `research/research-k.md` (with review); skimmed `research-g.md` (summary table, review); for all other notes A–N the status paragraph and the coordinator's review sections. Re-ran `python3 experiments/o_gc.py --selftest` (passes) and cross-checked my own normal-form routine against `o_gc.nf` on 300 random words. What I use, and have re-derived: O1 (G_c = ⟨x,y | c⟩ ≅ F(a,b) ⋊_φ ℤ, a = x, b = yxY, φ(a) = b, φ(b) = b⁻¹a; elements (u,k), (u,k)(u′,k′) = (uφᵏ(u′), k+k′)); O §2.2 (the conjugacy class of (u,1) meets F(a,b)×{1} exactly in the Reidemeister class R(u) = {v u φ(v)⁻¹}); O2 (a c-frozen ACM move from P_n to a presentation with a primitive relator exists iff k_n = (aⁿb⁻¹a⁻¹, 1) is conjugate in G_c to xˢy = (aˢ,1) for some s); K1 (AK(n) ~AC P_n = (c, k_n), c = xyxYYXy, k_n = xⁿYXyy).

**Choice of direction.** I kept the seed (make O6 uniform in n), because O's §6.4 explains why finite quotients cannot do it and O's advice 3 names the missing ingredient (the holonomy). Two things turned out differently from the seed's expectation and are the reason this note is not just "O6 with n free":

1. Working with the orientation-reversing element y itself (an *anti-holomorphic* intertwiner Y) instead of the squares in H removes both ambiguities the seed warns about: the invariant I(u) is a canonical **integer**, with no sign and no twist by y (§2).
2. The geometric invariant does **not** separate everything: τ(4) = σ(5) = 74 and τ(5) = σ(6) = 218. So besides the genuine coincidences n = 1, 2 there are two *isospectral but non-conjugate* cases, n = 4, 5, which need a second exact invariant (§4). For n = 3 and all n ≥ 6 the integer I alone suffices.

Notation: capitals are inverses (X = x⁻¹, A = a⁻¹, …); conj(·) is entrywise complex conjugation; ω = e^{2πi/3}, ω² = −1−ω, conj(ω) = ω².

## 2. The representation and the integer invariant (proved here)

### 2.1 Proposition T1

Let

    A = [[1, 1], [ω, 1+ω]],   B = [[1−ω, ω], [1+ω, 0]],   Y = [[ω², 0], [ω², ω]]      (all of determinant 1),

and ρ: F(a,b) → SL(2,ℤ[ω]), a ↦ A, b ↦ B. Then

  (i) Y·conj(A) = B·Y and Y·conj(B) = (B⁻¹A)·Y;
  (ii) ρ(φ(u)) = Y·conj(ρ(u))·Y⁻¹ for every u ∈ F(a,b);
  (iii) T := Y·conj(Y) = [[1,0],[−ω,1]] satisfies T A T⁻¹ = B⁻¹A = ρ(φ²(a)) and T B T⁻¹ = A⁻¹B² = ρ(φ²(b)); so a ↦ A, b ↦ B, t ↦ T is a representation of H = F(a,b) ⋊_{φ²} ⟨t⟩ (t = y²) in SL(2,ℤ[ω]);
  (iv) tr A = 2+ω, tr B = tr AB = 1−ω = conj(tr A), tr(ABA⁻¹B⁻¹) = −2.

*Proof.* (i) Using ω³ = 1, 1+ω+ω² = 0: conj(A) = [[1,1],[ω²,−ω]], so Y·conj(A) = [[ω², ω²],[ω²+1, ω²−ω²]] = [[ω², ω²],[−ω, 0]], and B·Y = [[(1−ω)ω²+ω³, ω²],[(1+ω)ω², 0]] = [[ω², ω²],[−ω, 0]]. Next conj(B) = [[1−ω², ω²],[−ω, 0]], so Y·conj(B) = [[ω²−ω, ω],[ω²−ω−ω², ω]] = [[ω²−ω, ω],[−ω, ω]]; B⁻¹ = [[0, −ω],[ω², 1−ω]], B⁻¹A = [[−ω², 1],[ω, 1]], and (B⁻¹A)·Y = [[−ω⁴+ω², ω],[ω³+ω², ω]] = [[ω²−ω, ω],[−ω, ω]]. (ii) Both sides are homomorphisms F(a,b) → SL(2,ℂ) in u (complex conjugation is a ring automorphism) and agree on a and b by (i), since φ(a) = b, φ(b) = b⁻¹a. (iii) Apply (ii) twice: ρ(φ²(u)) = Y·conj(Y·conj(ρ(u))·Y⁻¹)·Y⁻¹ = T ρ(u) T⁻¹; φ²(a) = b⁻¹a, φ²(b) = a⁻¹b² are free computations; conj(Y) = [[ω,0],[ω,ω²]] gives T. (iv) Direct. ∎

All of (i)–(iv) are also asserted in exact ℤ[ω]-arithmetic by `experiments/th03_uniform.py --selftest`, which checks (ii) on 300 random words as well. The relations of H quoted in my brief (t a t⁻¹ = b⁻¹a, t b t⁻¹ = a⁻¹b²) are confirmed.

*Recalled, not used in any proof:* ρ together with y ↦ (z ↦ Y(z̄)) is the holonomy of the Gieseking manifold, H is the figure-eight knot group and T (trace 2) is a parabolic; A is loxodromic with |λ|² = μ ≈ 2.9656, log μ ≈ 1.0871 (the length of the shortest geodesic of the figure-eight complement). How I found the matrices: a φ-compatible anti-holomorphic structure forces the character (tr a, tr b, tr ab) = (x, x̄, x̄) with |x|² = 2 Re x and trace-of-commutator −2, whence x = 2+ω; A, B were then written down with these traces and Y found by solving the linear system (i).

### 2.2 Proposition T2 (the invariant)

For u ∈ F(a,b) put N(u) := ρ(u)·Y and **I(u) := tr(N(u)·conj(N(u)))**.

  (a) I(u) ∈ ℤ.
  (b) I(v u φ(v)⁻¹) = I(u) for all u, v; in particular I(φ(u)) = I(u). Hence I is constant on R(u), i.e. it is an invariant of the conjugacy class of the degree-1 element (u,1) of G_c: if (u,1) and (u′,1) are conjugate in G_c then I(u) = I(u′).
  (c) I(u) = tr(ρ(u φ(u))·T), the trace of the square (u,1)² = (uφ(u), 2) ∈ H under the representation of T1(iii).

*Proof.* (a) conj(tr(N·conj N)) = tr(conj N·N) = tr(N·conj N), and an element p+qω of ℤ[ω] fixed by complex conjugation has q = 0. (b) By T1(ii), ρ(φ(v))⁻¹·Y = Y·conj(ρ(v))⁻¹, so N(vuφ(v)⁻¹) = ρ(v)·N(u)·conj(ρ(v))⁻¹ and therefore N′·conj(N′) = ρ(v)·N(u)·conj(N(u))·ρ(v)⁻¹, which has the same trace. φ(u) = u⁻¹·u·φ(u⁻¹)⁻¹ ∈ R(u). The last assertion is O §2.2. (c) N·conj(N) = ρ(u)·Y·conj(ρ(u))·conj(Y) = ρ(u)ρ(φ(u))·Y·conj(Y). ∎

Compared with O's sieve: by (c), I is the characteristic-zero version of O's trace of squares, but (a)–(b) show that for degree-1 elements **there is no sign ambiguity and no need to consider the twist y(·)y⁻¹**. (The latter also has a one-line group-theoretic reason: g commutes with g², and g ∉ H, so the G_c-class of g² is a single H-class. This explains why O's two candidate trace lists in §6.3 coincide.)

Define, for s, n ∈ ℤ,

    σ(s) := I(aˢ)        (the class of xˢy = (aˢ,1)),
    τ(n) := I(aⁿb⁻¹a⁻¹)  (the class of k_n = xⁿYXyy = (aⁿBA,1)).

**Necessary condition.** If k_n is conjugate in G_c to xˢy, then τ(n) = σ(s).

## 3. The two integer sequences (proved here)

### 3.1 Lemma T3 (recurrence)

For any C, D ∈ M₂(ℂ) the sequence f(n) := tr(Aⁿ·C·conj(A)ⁿ·D), n ∈ ℤ, satisfies

    f(n+4) = 3 f(n+3) − f(n+2) + 3 f(n+1) − f(n).                       (R)

Both σ and τ are of this form (σ: C = Y, D = conj(Y); τ: C = B⁻¹A⁻¹Y, D = conj(B⁻¹A⁻¹)·conj(Y)), so both satisfy (R) for all n ∈ ℤ.

*Proof.* tr A = 2+ω ≠ ±2, so A has distinct eigenvalues λ, λ⁻¹ and Aⁿ = λⁿE₊ + λ⁻ⁿE₋ with the spectral projections E_±; likewise conj(A)ⁿ = λ̄ⁿ·conj(E₊) + λ̄⁻ⁿ·conj(E₋). Hence f(n) is a linear combination of the four sequences (λ^ε λ̄^δ)ⁿ, ε, δ = ±1. These four numbers are the roots of (z² − pz + 1)(z² − qz + 1) with p = |λ|² + |λ|⁻², q = λ/λ̄ + λ̄/λ, and p + q = (λ+λ⁻¹)(λ̄+λ̄⁻¹) = |2+ω|² = 3, pq = λ²+λ⁻²+λ̄²+λ̄⁻² = 2 Re((2+ω)²) − 4 = 2 Re(3+3ω) − 4 = −1. So the polynomial is z⁴ − 3z³ + z² − 3z + 1, whose recurrence is (R). ∎

(So p = (3+√13)/2 = μ + μ⁻¹, μ ≈ 2.96557, and q = (3−√13)/2 = 2 cos θ: one root outside the unit circle, one inside, two on it.)

**Initial values (exact computation; σ(0) = tr T = 2 and σ(1) = tr(ABT) = 2 also checked by hand):**

    σ(−1), σ(0), σ(1), σ(2) = 2, 2, 2, 2;        τ(0), τ(1), τ(2), τ(3) = 2, 8, 8, 20.

By (R) these determine everything:

| s or n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| σ(s) | 2 | 2 | 8 | 26 | 74 | 218 | 650 | 1928 | 5714 | 16946 |
| τ(n) | 8 | 8 | 20 | 74 | 218 | 632 | 1880 | 5588 | 16562 | 49106 |

(The script computes σ, τ directly from matrix powers for |n| ≤ 206 and asserts (R) on the whole window.)

### 3.2 Lemma T4 (growth, integers only)

Let u: ℤ → ℤ satisfy (R) and suppose that for some m: u(m) > 0 and u(m+i+1) ≥ 2u(m+i) for i = 0, 1, 2. Then u(n+1) ≥ 2u(n) > 0 for all n ≥ m.

*Proof.* Induction: if the inequalities hold at k, k+1, k+2 (and u(k) > 0), then by (R)
u(k+4) − 2u(k+3) = u(k+3) − u(k+2) + 3u(k+1) − u(k) ≥ u(k+2) + 5u(k) > 0. ∎

### 3.3 Theorem T5 (complete solution of τ(n) = σ(s))

  (a) σ(1−s) = σ(s) for all s ∈ ℤ; σ(1) = σ(2) = 2 and σ is strictly increasing on s ≥ 2.
  (b) τ(1) = τ(2) = 8 and τ is strictly increasing on n ≥ 2.
  (c) For every n ≥ 6: σ(n) < τ(n) < σ(n+1); and σ(3) < τ(3) < σ(4).
  (d) The solutions (n, s) of τ(n) = σ(s) with n ≥ 1, s ∈ ℤ are exactly
      (1, −2), (1, 3), (2, −2), (2, 3), (4, −4), (4, 5), (5, −5), (5, 6).

*Proof.* (a, symmetry) The characteristic polynomial of (R) is palindromic, so s ↦ σ(1−s) also satisfies (R); it agrees with σ at s = −1, 0, 1, 2 (all four values are 2), hence everywhere.
(c) e(n) := σ(n+1) − τ(n) and d(n) := τ(n) − σ(n) satisfy (R). From the table, e(6), …, e(9) = 18, 48, 126, 384 and d(3), …, d(6) = 12, 48, 144, 414, so Lemma T4 applies with m = 6, resp. m = 3: e(n) > 0 for n ≥ 6 and d(n) > 0 for n ≥ 3. Also σ(3) = 8 < τ(3) = 20 < σ(4) = 26.
(a, monotonicity) For s ≥ 6, σ(s) < τ(s) < σ(s+1) by (c); for 2 ≤ s ≤ 5 read the table. (b) For n ≥ 6, τ(n) < σ(n+1) < τ(n+1) by (c); for 2 ≤ n ≤ 5 read the table.
(d) By (a) the set of values of σ is {σ(s) : s ≥ 2}, on which σ is injective and increasing, and σ(s′) = σ(s) for s′ = 1−s. For n ≥ 6 and for n = 3, τ(n) lies strictly between two consecutive values by (c), so it is not a value. τ(1) = τ(2) = 8 = σ(3) = σ(−2); τ(4) = 74 = σ(5) = σ(−4); τ(5) = 218 = σ(6) = σ(−5). ∎

*Remarks (not used in proofs).* (1) Closed form, derived by hand from the symmetry and checked numerically (relative error < 10⁻¹⁴ for |s| ≤ 20): σ(s) = (2/√13)·[μ^{s−1/2} + μ^{1/2−s} + 2 cos((s−½)θ)], where μ^{1/2} + μ^{−1/2} = (1+√13)/2 and 2 cos(θ/2) = (√13−1)/2. (2) e(n) = σ(n+1) − τ(n) is antisymmetric about n = 2 (same argument as (a): e(1), …, e(4) = −6, 0, 6, 0), so its zeros are exactly n = −1, 0, 2, 4, 5; and τ(n)/σ(n+1) → 0.97718… (numerical): the leading coefficients of τ and σ differ by a factor that is not a power of μ, which is why the growth argument closes, while the bounded oscillating terms produce the four small-n coincidences. (3) *Recalled:* I(g) = 2 cosh ℓ(g), ℓ the translation length of the glide reflection g; I = 2 exactly for the peripheral classes, in agreement with O4 (s ∈ {−1,0,1,2}). The coordinator independently found the same eight coincidences for n ≤ 14, |s| ≤ 40 with a separate script (holonomy traces in ℚ(ω)).

## 4. The isospectral cases n = 4, 5 (proved here by exact rational computation)

T5 leaves s ∈ {−4, 5} for n = 4 and s ∈ {−5, 6} for n = 5. These are not conjugacies; they need an invariant that is not a function of I.

**The invariant J.** Let A₂ = [[5/3, −1],[1, 0]], B₂ = [[2, 0],[5/6, 1/2]] ∈ SL(2,ℚ) and T₂ = [[12/19, −3/19],[−14/19, 1]] (det T₂ = 186/361). Exact rational arithmetic gives T₂A₂ = (B₂⁻¹A₂)T₂ and T₂B₂ = (A₂⁻¹B₂²)T₂; hence ρ₂: H → GL(2,ℚ), (w, 2m) ↦ ρ₂(w)·T₂ᵐ (a ↦ A₂, b ↦ B₂), is a homomorphism (T₂ρ₂(w)T₂⁻¹ = ρ₂(φ²(w)) holds on generators, hence for all w). For a degree-1 element g = (u,1) put

    J(u) := tr(ρ₂(g²))² / det ρ₂(g²) = tr(ρ₂(uφ(u))·T₂)² / det T₂ ∈ ℚ.

**Lemma.** J(u) depends only on the conjugacy class of (u,1) in G_c. *Proof.* Let g′ = hgh⁻¹. Then g′² = h g² h⁻¹. If h ∈ H, the two squares are conjugate in H. If h ∉ H then h′ := hg⁻¹ ∈ H (even degree) and h g² h⁻¹ = h′ g² h′⁻¹, again conjugate in H. tr²/det is a class function on GL₂. ∎

**Proposition T6.** J(k_1) = J(k_2) = J(x⁻²y) = J(x³y) = 3751/7776 (control: the genuine conjugacies), while

    J(k_4) = 110490491431/362797056  ≠  J(x⁵y) = J(x⁻⁴y) = 15320479/31104,
    J(k_5) = 59111013559/40310784    ≠  J(x⁶y) = J(x⁻⁵y) = 925644326431/362797056.

Hence k_4 is conjugate in G_c neither to x⁵y nor to x⁻⁴y, and k_5 neither to x⁶y nor to x⁻⁵y.

*Proof.* Exact arithmetic with Python `Fraction`s in `th03_uniform.py` (function `J`, self-test item 7; T₂ is obtained by solving the linear intertwiner system exactly and then *verified*). The self-test repeats everything at a second rational point (p = 3 below) with the same conclusion. ∎

*Where the point comes from (heuristic, not needed for the proof).* φ acts on characters (x,y,z) = (tr a, tr b, tr ab) by (x,y,z) ↦ (y, xy−z, x); the fixed locus of φ² is the curve z = y, xy = x + y. The Gieseking point is (2+ω, 1−ω, 1−ω) (it is *swapped with its complex conjugate* by φ, which is what makes Y anti-holomorphic). Rational points with rational matrices: y = p + 1/p, x = y/(y−1), A_p = [[x,−1],[1,0]], B_p = [[p,0],[xp−y,1/p]]; p = 2 gives the matrices above. O's 𝔽₁₃-witness is another point of the same curve (tr = 8, 3 with 8 = 3/(3−1) mod 13). This also re-proves O6 for n = 4, 5 without a sieve over residues, because T5 has already reduced s to two values.

## 5. The uniform theorem (proved here)

**Theorem T7.** For every n ≥ 3 and every s ∈ ℤ, the killer k_n = xⁿy⁻¹x⁻¹y² is not conjugate in G_c = ⟨x,y | xyxy⁻²x⁻¹y⟩ to xˢy. Consequently, **for every n ≥ 3 there is no presentation with a primitive relator one ACM move (arbitrary conjugators, c frozen) away from P_n = (c, k_n)**. For n = 1, 2 such a move exists (O3: k_1 ~ k_2 ~ x⁻²y).

*Proof.* If k_n ~ xˢy then τ(n) = σ(s) (T2). By T5(d) this is impossible for n = 3 and for n ≥ 6, and for n = 4, 5 it leaves exactly the four pairs excluded by T6. The consequence is O's Proposition O2. ∎

This is the uniform analogue, in K's coordinates, of G's Proposition G2 (no primitive relator one ACM move from AK(n), n ≥ 3, with a torus relator frozen); it contains O6 (n = 3,…,8) and is independent of O's sieve. The exceptional solutions of T5(d) at n = 1, 2 are exactly the genuine conjugacies — the control the seed asked for.

**Corollary T8.** (a) For n, m ≥ 2, n ≠ m, there is no ACM move with c frozen from P_n to P_m. (b) More generally, if (c, w) is one c-frozen ACM move from P_n, then w has y-exponent ε = ±1 and I(w^ε) = τ(n), where I(w) := I(u) for the normal form (u,1) of w. (c) The same holds with P_m replaced by its automorphic image α(P_m) of §6.

*Proof.* (b) w ≡ g k_n^{±1} g⁻¹ mod ⟨⟨c⟩⟩ means w^{ε} ~ k_n in G_c; apply T2. (a) k_m^{−1} has degree −1, and τ(n) ≠ τ(m) by T5(b). (c) I(α(k_m)) = τ(m) by T9. ∎

(a) answers K's advice 1(b) ("search for a uniform move P_{n+1} → P_n with c frozen") negatively for all n ≥ 2: the only such coincidence in the whole series is k_1 ~ k_2. (b) is an exact, conjugator-free filter for any proposed c-frozen target: for P₃ the target's invariant must be 20.

## 6. The mirror symmetry α (proved here)

**Proposition T9.** Let α ∈ Aut(F(x,y)), α(x) = x⁻¹, α(y) = yx. Then
  (a) α² = id and α(c) = X·(yXYXYxy)·x, where yXYXYxy is a rotation of c⁻¹ = YxyyXYX; so α preserves ⟨⟨c⟩⟩ and induces an automorphism of G_c, given on normal forms by α(u,k) = (ι(u),0)·(b,1)ᵏ with ι(a) = a⁻¹, ι(b) = b⁻¹;
  (b) α(xˢy) = x⁻ˢyx is conjugate to x^{1−s}y, and α(k_n) = x⁻ⁿ⁻¹y⁻¹xyxyx is conjugate to x⁻ⁿy⁻¹xyxy, with normal form class (a^{−(n−1)}ba, 1);
  (c) I(α(g)) = I(g) for every degree-1 element g. The same holds for J and for every invariant obtained in this way from an SL₂-representation of the fibre.

*Proof.* (a), (b): free reductions (α(y)α(x) = y; α(c) = X·yx·X·XY·XY·x·yx = XyXYXYxyx); α(b) = α(yxY) = yXY = b⁻¹. (c) Let S := AB − BA (det S = 2 − tr[A,B] = 4). For any A, B ∈ SL₂ one has SA = A⁻¹S and SB = B⁻¹S (Cayley–Hamilton), so ρ(ι(u)) = S ρ(u) S⁻¹. With N = ρ(u)Y, the element α(u,1) = (ι(u)b, 1) has N′ = Sρ(u)S⁻¹BY = S·N·Z, Z := Y⁻¹S⁻¹BY. By T1(ii), Y·conj(S)·Y⁻¹ = ρ(φ(a))ρ(φ(b)) − ρ(φ(b))ρ(φ(a)) = A − B⁻¹AB = −B⁻¹S, i.e. Z·conj(S) = −1. Hence N′·conj(N′) = −S·N·conj(N)·conj(Z), whose trace is −tr(N·conj(N)·conj(Z)·S) = −tr(N conj(N))·(−1) = I(u), because conj(Z)·S = conj(Z·conj(S)) = −1. For J the argument is the same with ρ₂ (ρ₂∘ι = S₂ρ₂S₂⁻¹). ∎ (Checked on 300 random words by script; J(xˢy) = J(x^{1−s}y) is asserted in the self-test.)

Consequences. (1) σ(s) = σ(1−s) is explained by α; α swaps the two peripheral classes {x⁻¹y, y} and {xy, x²y} of O4. (2) α(P_n) is, after conjugating and inverting the first relator, P_nᵅ := (c, x⁻ⁿy⁻¹xyxy), of length n+12; for n = 3 it is AC-equivalent to P₃ by D's Lemma D6. T7 holds verbatim for P_nᵅ. (3) Whether k_n ~ α(k_n) in G_c cannot be decided by any SL₂-trace invariant, by (c). It **is** decided, negatively and for all n, by a mod-2 twisted trace: the mirror theorem T16 of §7.5. (4) The rational twisted trace of degree 4 on G_c of §9.4 is also α-invariant on all tested elements.

## 7. The killer side: twisted traces and Q2 (proved here)

O (§3, "Q2") asked for the k₃-frozen analogue of the primitive exit and left it open (finite quotients gave no information). The tool below settles it for n = 3, 4, 5.

### 7.1 Structure of G_{k_n} = ⟨x,y | xⁿy⁻¹x⁻¹y²⟩ (proved here; n ≥ 2)

Put t := yx^{n−1}, so (x,t) is a basis of F(x,y) and y = tx^{1−n}. Then k_n = x^{2n−1}t⁻¹x⁻¹tx^{1−n}tx^{1−n}, which is conjugate to xⁿt⁻¹x⁻¹tx^{1−n}t = t_n⁻¹t_{n−1}t₀, where t_i := xⁱtx⁻ⁱ. Let ψ be the automorphism of F_n = F(t₀,…,t_{n−1}) with ψ(t_i) = t_{i+1} (i < n−1), ψ(t_{n−1}) = t_{n−1}t₀ (inverse: t_i ↦ t_{i−1} for i ≥ 1, t₀ ↦ t_{n−2}⁻¹t_{n−1}). As in O1, x ↦ x, t ↦ t₀ and t_i ↦ xⁱtx⁻ⁱ, x ↦ x are mutually inverse isomorphisms G_{k_n} ≅ F_n ⋊_ψ ⟨x⟩ (the relator maps to ψⁿ(t₀)⁻¹ψ^{n−1}(t₀)t₀ = 1; conversely x t_{n−1} x⁻¹ = t_{n−1}t₀ is the relator). Elements are (u,k) = u·xᵏ, x u x⁻¹ = ψ(u), and degree-1 elements (u,1), (u′,1) are conjugate iff u′ ∈ R_ψ(u) = {v u ψ(v)⁻¹} (same computation as O §2.2).

**Lemma.** (i) For n ≥ 3, c = xyxYYXy has normal form (t₁t₂⁻¹t₁⁻¹, 1). (ii) x·tʲ = (t₁ʲ, 1). (iii) A k_n-frozen ACM move from P_n to a presentation with a primitive relator exists iff c is conjugate in G_{k_n} to x·tʲ for some j ∈ ℤ, i.e. iff t₁ʲ ∈ R_ψ(t₁t₂⁻¹t₁⁻¹) for some j. (Call this Q2(n).)

*Proof.* (i) c = x·tx^{1−n}·x·x^{n−1}t⁻¹·x^{n−1}t⁻¹·x⁻¹·tx^{1−n} = x t x t⁻¹ x^{n−1} t⁻¹ x⁻¹ t x^{1−n} = t₁·t₂⁻¹·t_{n+1}⁻¹·t_n·x, and t_n = t_{n−1}t₀, t_{n+1} = ψ(t_n) = t_{n−1}t₀t₁, so t_{n+1}⁻¹t_n = t₁⁻¹. (ii) x t₀ʲ = t₁ʲ x. (iii) The abelianization λ of G_{k_n} is x ↦ 1, t ↦ 0, and λ(c) = 1. If (p, k_n) is reached with p primitive, then p^{±1} ~ c in G_{k_n}; replacing p by p⁻¹, λ(p) = 1, so p has exponent vector (1, j) in the basis (x,t) and is conjugate in F to x tʲ (Nielsen: a primitive is determined up to conjugacy by its exponent vector). The converse is the definition of an ACM move. ∎ (Script: nf(k_n) = (1, 0) for n = 2,…,7, nf(c) = (t₁t₂⁻¹t₁⁻¹, 1), nf(xtʲ) = (t₁ʲ, 1).)

### 7.2 Twisted traces (proved here)

Let F = F(t₀,…,t_{r−1}), ψ ∈ Aut(F), D ≥ 1, and A_D := ℤ⟨X₀,…,X_{r−1}⟩/(monomials of degree > D). The Magnus map 𝔐: F → A_D^×, t_i ↦ 1+X_i, is a homomorphism, and Ψ(X_i) := 𝔐(ψ(t_i)) − 1 defines a ring endomorphism Ψ of A_D (it maps the augmentation ideal into itself) with 𝔐∘ψ = Ψ∘𝔐. Call an additive map ℓ: A_D → M (M an abelian group) a **twisted trace** if

    ℓ(X_i·m) = ℓ(m·Ψ(X_i))   for all i and all monomials m.                    (TT)

**Lemma T11a.** If ℓ is a twisted trace then ℓ(a·m) = ℓ(m·Ψ(a)) for all a, m ∈ A_D, and ℓ(𝔐(v u ψ(v)⁻¹)) = ℓ(𝔐(u)) for all u, v ∈ F. So u ↦ ℓ(𝔐(u)) is an invariant of the conjugacy class of (u,1) in F ⋊_ψ ℤ.

*Proof.* The set of a with ℓ(am) = ℓ(mΨ(a)) for all m is an additive subgroup containing 1 and the X_i, and it is closed under products: ℓ(ab·m) = ℓ(b·mΨ(a)) = ℓ(mΨ(a)Ψ(b)). So it is A_D. Now take a = 𝔐(v), m = 𝔐(u)·Ψ(a)⁻¹: ℓ(𝔐(v)𝔐(u)𝔐(ψ(v))⁻¹) = ℓ(am) = ℓ(mΨ(a)) = ℓ(𝔐(u)). ∎

(TT) is a finite system of linear equations, and for powers 𝔐(t_iʲ) = Σ_k C(j,k)X_iᵏ, so ℓ(𝔐(t_iʲ)) is an explicit integer-valued polynomial in j. (These invariants live on the polycyclic quotient (F/γ_{D+1}) ⋊ ℤ. Rational twisted traces beyond the constant one exist in degree d only if a product of d eigenvalues of ψ_ab equals 1; for ψ = ψ₃ the eigenvalues are the roots of z³ − z² − 1, whose product is 1 — this is why degree 3 works for n = 3. H's theorem that solvable quotients carry no AC obstruction is not contradicted: this is a statement about one move.)

### 7.3 Theorem T11 (n = 3)

Let n = 3 and D = 3 (A₃ has rank 40). Define ℓ: A₃ → ℤ on monomials X_iX_j… (written ij…) by

    degree 2:  ℓ = 1 on 00, 01, 02, 10, 11, 12, 21, 22;   ℓ(20) = 0;
    degree 3:  ℓ = +1 on 002, 021, 022, 100, 102, 110, 200, 211, 221;
               ℓ = −1 on 010, 012, 101, 120, 121, 202, 212;   ℓ(210) = 2;   ℓ(020) = ℓ(201) = −2;
    ℓ = 0 on all other monomials (in particular in degrees 0 and 1 and on 111, 122, 222).

**Theorem T11.** (a) ℓ is a twisted trace for ψ₃ (t₀ ↦ t₁ ↦ t₂ ↦ t₂t₀; Ψ(X₀) = X₁, Ψ(X₁) = X₂, Ψ(X₂) = X₂ + X₀ + X₂X₀). (b) ℓ(𝔐(t₁ʲ)) = j(j−1)/2 for all j ∈ ℤ. (c) ℓ(𝔐(t₁t₂⁻¹t₁⁻¹)) = −2. (d) Hence c is not conjugate in G_{k₃} to x·tʲ for any j: **Q2(3) has a negative answer**, and no presentation with a primitive relator is one ACM move from P₃ with k₃ frozen.

*Proof.* (a) is the 39 identities (TT) (i ∈ {0,1,2}, m a monomial of degree ≤ 2), each involving at most four values of ℓ; e.g. i = 2, m = 1: ℓ(X₂) = ℓ(X₂ + X₀ + X₂X₀) requires ℓ(X₀) + ℓ(X₂X₀) = 0 ✓; i = 0, m = X₂: ℓ(02) = ℓ(21) ✓; i = 2, m = X₁: ℓ(21) = ℓ(12) + ℓ(10) + ℓ(120) = 1 + 1 − 1 ✓. All 39 are asserted in exact integer arithmetic by `th03_q2.py --selftest` (which also recomputes the full 3-dimensional solution space of (TT) over ℚ and finds ℓ in it). (b) 𝔐(t₁ʲ) = 1 + jX₁ + C(j,2)X₁² + C(j,3)X₁³ and ℓ(1) = ℓ(X₁) = ℓ(111) = 0, ℓ(11) = 1. (c) Expanding (1+X₁)(1−X₂+X₂²−X₂³)(1−X₁+X₁²−X₁³) in A₃ gives 1 − X₂ − X₁X₂ + X₂X₁ + X₂² + X₁X₂X₁ + X₁X₂² − X₂X₁² − X₂²X₁ − X₂³, and ℓ of it is −ℓ(12) + ℓ(21) + ℓ(22) + ℓ(121) + ℓ(122) − ℓ(211) − ℓ(221) − ℓ(222) = −1 + 1 + 1 − 1 + 0 − 1 − 1 − 0 = −2. (d) j(j−1)/2 ≥ 0 > −2 for every integer j; apply T11a and Lemma 7.1(iii). ∎

**Corollary T11′ (the complete one-move statement for P₃).** No presentation with a primitive relator is one ACM move from P₃ = (xyxYYXy, xxxYXyy), whichever of the two relators is frozen and whatever the conjugator; the same holds for every automorphic image θ(P₃), θ ∈ Aut(F₂). *Proof.* T7 (c frozen) and T11 (k₃ frozen); primitivity is Aut(F₂)-invariant and θ transports ACM moves. ∎

**Proposition T12 (n = 4, 5; exact computation).** Q2(4) and Q2(5) also have negative answers. For n = 4: the 𝔽₂-valued twisted traces on A₄ (rank 341) form a 7-dimensional space, and for no residue j mod 8 do all of them agree on 𝔐(t₁ʲ) and 𝔐(t₁t₂⁻¹t₁⁻¹) (for k ≤ 4, C(j,k) mod 2 depends only on j mod 8). For n = 5: over ℚ with D = 3 the solution space of (TT) is 4-dimensional and one twisted trace vanishes on every 𝔐(t₁ʲ) but takes the value −2 on c (here z⁵ − z⁴ − 1 = (z² − z + 1)(z³ − z − 1) has roots of unity as roots, which creates low-degree traces). Together with T7: **for n = 3, 4, 5 no presentation with a primitive relator is one ACM move from P_n, whichever relator is frozen.** For n ≥ 6 the k_n-frozen side is open: there are no non-constant twisted traces mod 2, 3, 5 in degree ≤ 4 (n = 6) or ≤ 3 (n = 7), and only partial congruence conditions for n = 8 (experiment, §9.5); the first rational one is expected in degree n (odd n) or 2n (even n).

### 7.4 The same mechanism on the c-side: the degree-4 twisted trace L4 on G_c (proved here)

Apply §7.2 to F(a,b) with φ (Ψ(X_a) = X_b, Ψ(X_b) = (1+X_b)⁻¹(1+X_a) − 1) and D = 4 (rank 31). The integer functional L4 with

    L4(ba) = 1;  L4 = 1 on aaa, aab, abb, bbb;  L4(aba) = L4(bab) = −1;  L4(baa) = 2;  L4(bba) = 3;
    L4 = 1 on aaaa, aaab, aabb, abbb, bbbb;  L4 = −1 on aaba, abab, baba, babb;  L4 = −2 on abaa, baab;  L4 = 2 on bbaa, bbba;

and 0 elsewhere, satisfies (TT) (30 identities, asserted by `th03_two.py`; the solution space of (TT) over ℚ is 2-dimensional: constants and L4). Hence L4(u) := L4(𝔐(u)) is a second **integer** invariant of the G_c-class of (u,1), of a completely different nature from I (it lives on the polycyclic quotient (F₂/γ₅) ⋊ ℤ).

**Proposition T13.** (a) L4(xˢy) = C(s,3) + C(s,4) = C(s+1,4) = (s+1)s(s−1)(s−2)/24 ≥ 0 for every s ∈ ℤ. (b) L4(k_n) = 1, 1, −1, −5, −10, −14, −14, −6, 15 for n = 1,…,9. (c) Hence k_n ≁ xˢy for n = 3,…,8 by the sign of L4 alone — an independent proof of O6 — and L4(k_4) = −5 ≠ 15 = L4(x⁵y) = L4(x⁻⁴y), L4(k_5) = −10 ≠ 35 = L4(x⁶y) = L4(x⁻⁵y) gives a second, all-integer proof of T6. (Control: L4(k_1) = L4(k_2) = L4(x⁻²y) = L4(x³y) = 1.)

*Proof.* (a) 𝔐(aˢ) = Σ_k C(s,k)X_aᵏ and L4(a) = L4(aa) = 0, L4(aaa) = L4(aaaa) = 1; a product of four consecutive integers is ≥ 0. (b) exact evaluation (script). ∎

So for P₃ **both** one-move primitive exits are excluded by the sign of an explicit integer twisted trace (L4(k₃) = −1 on the c-side, ℓ(c) = −2 on the k₃-side); the hyperbolic invariant I is what makes the c-side uniform in n (L4(k_n) is a quartic polynomial in n and is positive again from n = 9 on).

### 7.5 The mirror theorem and the complete classification (proved here, by hand)

For u ∈ F(a,b) let p, q be the exponent sums of a and b in u, let μ_ab(u) := Σ ε_iε_j over all pairs of positions i < j such that the i-th letter of u is a^{ε_i} and the j-th is b^{ε_j}, and put

    ε(u) := C(p+1, 2) + C(q+1, 2) + μ_ab(u)   (mod 2).

**Theorem T16 (mirror theorem).** (a) ε(v u φ(v)⁻¹) = ε(u) for all u, v: ε is an invariant of the conjugacy class of (u,1) in G_c. (b) ε(α(g)) = ε(g) + 1 for every degree-1 element g of G_c. (c) Hence **no degree-1 element of G_c is conjugate to its mirror image α(g)**; in particular k_n ≁ α(k_n) for every n ≥ 1, and xˢy ≁ x^{1−s}y for every s ∈ ℤ.

*Proof.* (a) In the Magnus algebra truncated in degree 2, 𝔐(u) = 1 + pX_a + qX_b + C(p,2)X_a² + C(q,2)X_b² + μ_ab(u)X_aX_b + μ_ba(u)X_bX_a (an inverse letter contributes 1 − X + X², so mixed terms come only from pairs of distinct positions). Hence ε(u) = ℓ₂(𝔐(u)) mod 2, where ℓ₂ is the sum of the coefficients of X_a, X_b, X_a², X_aX_b, X_b² (note C(p,2) + p = C(p+1,2)). ℓ₂ is a twisted trace mod 2 for φ: with Ψ(X_a) = X_b and Ψ(X_b) = (1+X_b)⁻¹(1+X_a) − 1 ≡ X_a − X_b − X_bX_a + X_b², the six identities (TT) read ℓ₂(a) = ℓ₂(b); ℓ₂(b) = ℓ₂(a) − ℓ₂(b) − ℓ₂(ba) + ℓ₂(bb); ℓ₂(aa) = ℓ₂(ab); ℓ₂(ab) = ℓ₂(bb); ℓ₂(ba) = ℓ₂(aa) − ℓ₂(ab); ℓ₂(bb) = ℓ₂(ba) − ℓ₂(bb), i.e. 1 = 1; 1 ≡ 1 − 1 − 0 + 1; 1 = 1; 1 = 1; 0 = 1 − 1; 1 ≡ 0 − 1 (mod 2). Apply Lemma T11a with M = ℤ/2. (b) α(u,1) = (ι(u)b, 1) (T9). ι(u) has exponent sums (−p, −q) and μ_ab(ι(u)) = μ_ab(u); appending b gives exponent sums (−p, 1−q) and μ_ab = μ_ab(u) − p. So ε(ι(u)b) − ε(u) = [C(1−p,2) − C(p+1,2)] + [C(2−q,2) − C(q+1,2)] − p = −p − (2q−1) − p ≡ 1 (mod 2), using C(1−p,2) = C(p,2) and C(2−q,2) = C(q−1,2). (c) from (a), (b). ∎ (Script: closed form against the Magnus evaluation, invariance and the flip on 500 random words.)

Values: ε(xˢy) = C(s+1,2) mod 2 (0 for s ≡ 0, 3 mod 4; 1 for s ≡ 1, 2), and ε(k_n) = C(n+1,2) mod 2 (u = aⁿBA: p = n−1, q = −1, μ_ab = −n).

**Corollary T17 (complete classification of the primitive classes and of the primitive exits).**
  (a) For s, s′ ∈ ℤ: xˢy ~ x^{s′}y in G_c iff s = s′ or {s,s′} = {−1,0} or {s,s′} = {1,2}. (O4 had this for |s| ≤ 6 within a bounded search.)
  (b) For n ≥ 1 and s ∈ ℤ: k_n ~ xˢy in G_c **iff n ∈ {1, 2} and s = −2**.
  (c) For every n ≥ 1, P_n → P_nᵅ = α(P_n) is not a single c-frozen ACM move.

*Proof.* (a) "If" is O3/O4 (explicit conjugators). "Only if": σ(s) = σ(s′) forces s′ ∈ {s, 1−s} or s, s′ ∈ {−1,0,1,2} (T5(a): σ = 2 exactly on {−1,0,1,2}, σ is injective on s ≥ 2 and symmetric); s′ = 1−s ≠ s is excluded by T16; and ε = 0, 0, 1, 1 on s = −1, 0, 1, 2 separates {−1,0} from {1,2}. (b) T5(d) leaves eight pairs; T6 removes n = 4, 5; ε(k_1) = ε(k_2) = 1 ≠ 0 = ε(x³y) removes s = 3; (1,−2) and (2,−2) are genuine (O3). (c) T16(c). ∎

## 8. Beyond one move (proved reformulation; exact partial census; main question open)

**Lemma T10 (two-move exits).** A path P_n = (c, k_n) → (c, k′) → (p, k′) of two ACM moves (first c frozen, then k′ frozen) with p primitive exists iff there is a word k′ with (1) k′^{±1} ~ k_n in G_c and (2) c conjugate to a primitive element in G_{k′} = ⟨x,y | k′⟩. Symmetrically for P_n → (c′, k_n) → (c′, p): (1′) c′^{±1} ~ c in G_{k_n}, (2′) k_n conjugate to a primitive in G_{c′}. Either path would trivialize P_n (D3). *Proof.* Definition of ACM moves. ∎

Tools now available for each step: (1) is filtered exactly by I, J, L4 (necessary) and certified by explicit twisted conjugators (sufficient; O's compiler turns them into certificates); (2) is a Q2-type question in G_{k′}: if k′ has y-exponent 1 and x-exponent m, put t = yx^m; when the extreme t_i occur once in k′ (Brown's criterion) G_{k′} is free-by-cyclic, the primitive candidates are again x·tʲ = (t₁ʲ,1), and twisted traces apply (`th03_two.second_move`).

**Proposition T14 (exact c-frozen neighbourhood of P₃ up to length 9; exact computation).** Let w be cyclically reduced of y-exponent 1 and length ≤ 9. Then I(w) = 20 for exactly 43 cyclic words, and:
  (a) 7 of them are conjugate to k₃ in G_c (explicit twisted conjugators by BFS): k₃ itself and XYxxyXy (length 7); XyyxYYxy, XYXyxxxy (length 8); XyyxYxyxY, XyyxYxYxy, XYYxyxyXy (length 9) — written as lexicographically least rotations (XyyxxxY is k₃);
  (b) 11 are conjugate to the mirror α(k₃) (1 of length 7, 4 of length 8, 6 of length 9), hence **not** conjugate to k₃ by the mirror theorem T16 (ε = 1 on them, ε(k₃) = 0);
  (c) the remaining 25 (3 of length 6, 6 of length 7, 5 of length 8, 11 of length 9) are **not** conjugate to k₃: their J differs.
Consequently **every presentation (c, w) one c-frozen ACM move from P₃ has |w| ≥ 7**: with arbitrary conjugators, c-frozen moves cannot shorten P₃ (total length ≥ 14 = |P₃|), and the c-frozen neighbours (c, w) with |w| ≤ 9 are **exactly** the seven cyclic words of (a) (up to rotation and inversion of w). (Correction to O §9.1: the word yxyXYXy listed there among the shortest elements of R(a³BA) has y-exponent 2 and is not in the class; the length-7 members are the rotations of k₃ and of XyXYxxy.)

**Proposition T15 (second move through the short neighbours; exact computation).** For k′ ∈ {k₃, XYxxyXy, XyyxYYxy, XYXyxxxy, XyyxYxyxY, XYYxyxyXy} — six of the seven first-move targets of T14 — the element c is conjugate to no primitive element in G_{k′}: **there is no two-move exit P₃ → (c,k′) → (p,k′) through these k′.** Details: ranks 3, 2, 3, 2, 3 for the first five (free-by-cyclic); rational twisted traces of degree 3 for k₃, XYXyxxxy, XyyxYxyxY; 𝔽₂-valued ones of degree 6, resp. 4, for XYxxyXy, XyyxYYxy. For k′ = XYYxyxyXy Brown's criterion fails: with t = y the relator is t₋₁⁻²t₀t₁t₀, so G_{k′} is the mapping torus ⟨F(t₀,t₁), x | x f x⁻¹ = θ(f)⟩ of the *injective, non-surjective* endomorphism θ(t₀) = t₁, θ(t₁) = t₁⁻¹t₀²t₁⁻¹ (its image ⟨t₁, t₀²⟩ is free of rank 2). Every degree-1 element x⁻ᵖfx^{p+1} is conjugate to f·x, and v′(fx)v′⁻¹ = f′x with v′ = x⁻ᵖvx^q gives vθ^q(f)θ(v)⁻¹ = θᵖ(f′), i.e. f′ ∈ R_θ(f) (θ(f) ∈ R_θ(f) always); Lemma T11a does not use invertibility of ψ. The 𝔽₃-valued twisted traces of degree ≤ 8 (13-dimensional space, rank-511 algebra) admit no residue j mod 9 (also none mod 5; and none mod 3 in degree ≤ 10). *Undecided:* k′ = XyyxYxYxy (rank 5): there are no non-constant rational traces in degree ≤ 3, and the traces mod 3 of degree ≤ 5 (rank 3906) leave exactly j ≡ 5 (mod 9); bounded BFS results are in §9.3.

This is a bounded census (|k′| ≤ 9) with exact answers, not a theorem about all two-move exits: the class of k₃ is infinite.

## 9. Experiments and reproduction (exact; one core, < 100 MB, each under one minute)

### 9.1 Commands and outputs (run in this session)

```
python3 experiments/th03_uniform.py --selftest
  th03_uniform self-test passed (cross-checked against o_gc.nf)
  solutions of tau(n) = sigma(s), 1 <= n < 200, s >= 1: (1,3),(2,3),(4,5),(5,6); sigma(s) = sigma(1-s)
  rational point p=2: J(k_4)=110490491431/362797056 != J(x^5y)=15320479/31104 ; J(k_5)=59111013559/40310784 != J(x^6y)=925644326431/362797056
  rational point p=3: J(k_4)=26081288752800144721/350277500542221 != J(x^5y)=4391719583449/200120949 ; ...
python3 experiments/th03_q2.py --selftest
  th03_q2 self-test passed
  n=3: l(c) = -2, l(x t^j) = C(j,2) >= 0  => Q2(3) has no solution j
  n=4: 7 twisted traces mod 2 in degree <= 4, no residue j mod 8 allowed => Q2(4) has no solution
  n=5: Inv(c) = ['1', '0', '-2', '-3']  coefficients: [[1,0,0,0],[0,0,0,0],[0,1,0,0],[0,0,0,1]] => no integer j
python3 experiments/th03_two.py --selftest
  th03_two self-test passed
  L4(x^s y) = C(s+1,4) >= 0;  L4(k_n), n = 1..9: ['1', '1', '-1', '-5', '-10', '-14', '-14', '-6', '15']
  length 7, k3: ['XyyxxxY', 'XYxxyXy'] ... (the lists of T14)
  second move excluded for k' in: XyyxxxY (= k_3), XYxxyXy, XyyxYYxy, XYXyxxxy, XyyxYxyxY; XYYxyxyXy (ascending HNN, 13 traces mod 3, degree 8): (13, []) ; undecided: XyyxYxYxy
python3 experiments/th03_uniform.py --table 12      # the tables of sigma and tau
```

What the self-tests assert. `th03_uniform`: T1 (all matrix identities in ℤ[ω]), T2(b) on 300 random pairs, normal forms against `o_gc.nf`, (R) and σ(1−s) = σ(s) for |n| ≤ 200, the three Lemma-T4 bases, σ(n) < τ(n) < σ(n+1) for 6 ≤ n < 200, the solution list of T5(d) for n < 200, the controls (k_1 ~ k_2 ~ x⁻²y, xy ~ x²y, y ~ x⁻¹y have equal I and equal J), the intertwiner identities for T₂ and invariance of J, and T6 at two rational points. `th03_q2`: the structure of G_{k_n} (n = 2..7), ψψ⁻¹ = id, the 39 identities for ℓ, T11(b),(c) (|j| ≤ 40), invariance on 200 random pairs, equality of the invariant on 60 random F-conjugates of c computed through normal forms, T12. `th03_two`: the 30 identities for L4, T13, T14 (complete enumeration of the cyclically reduced words of length ≤ 9), T15, and T16 (the six identities mod 2, the closed form of ε against the Magnus evaluation, invariance and the α-flip on 500 random words, ε on the 11 mirror words).

### 9.2 Coordinator's independent check (reported to me during the round)

The coordinator computed tr² of k_n² and (xˢy)² with separate code in ℚ(ω) (complex-conjugate trace triple) and found equality exactly for (n,s) ∈ {(1,−2),(1,3),(2,−2),(2,3),(4,−4),(4,5),(5,−5),(5,6)} among n ≤ 14, |s| ≤ 40 — the list of T5(d).

### 9.3 Bounded searches (experiment; not proofs)

O's twisted-conjugacy BFS (`o_cert.twisted_path`, (a,b)-length cap 14, ≤ 4·10⁵ nodes) finds no conjugator between k_n and α(k_n) for n = 1, 2, 3, 4; the BFS classes of k₃ and α(k₃) with cap 13 (1,637 and 1,654 normal forms) are disjoint. (Run before T16 was found; T16 now proves that these classes differ for every n.)

### 9.4 Twisted traces elsewhere (experiment)

On G_c the degree-4 trace L4 takes equal values on g and α(g) for all tested g (k_n and α(k_n), n ≤ 6; xˢy and x^{1−s}y), so, like I and J, it cannot see the mirror; the mod-2 trace ε of T16 does. For G_{k_n}, 𝔽_p-valued traces (p = 2, 3, 5): n = 6, degree ≤ 4 and n = 7, degree ≤ 3: only constants; n = 8, degree 3: p = 2 leaves j ≡ 0, 1 (mod 4), p = 3 leaves j ≡ 8 (mod 9), p = 5 nothing. SL(2,p)-quotients of G_{k₃} (p ≤ 13, all homs with non-abelian image): only j ≢ 2 (mod 3) is excluded, confirming O's remark that such quotients are useless for Q2. (Scratch scripts `q2.py`, `q2mod.py`, `two_mod.py`, `two_asc.py`, `bfs2.py` in my scratch directory; not committed.)

## 10. Failed attempts and dead ends (with reasons)

- **"Traces of squares never agree for n ≥ 3" is false.** τ(4) = σ(5), τ(5) = σ(6). The holonomy alone cannot give the uniform theorem; n = 4, 5 are isospectral and need J or L4 (or O's sieve).
- **A Gaussian-integer point of the character curve.** The point (tr a, tr b, tr ab) = (1−i, 1+i, 1+i) also carries an anti-holomorphic intertwiner, but a search over matrices with entries a+bi, |a|,|b| ≤ 2, found no integral model (the representation need not be conjugate into SL(2,ℤ[i])); I switched to rational points with rational matrices.
- **Separating k_n from its mirror α(k_n)** (and xˢy from x^{1−s}y) with SL₂ data: impossible with I, J (Prop. T9(c)); the rational trace L4 does not do it either on the tested range. What works is a torsion invariant: the mod-2 twisted trace ε of degree 2 (T16), found by computing the action of α on the 𝔽₂-valued twisted traces.
- **Uniform Q2(n).** The twisted-trace method needs degree about n (odd n) or 2n (even n) in an algebra of rank nᵈ; n = 6, 7 are out of reach of the direct linear algebra here, and I found no closed form for the top-degree trace. SL(2,p) quotients carry almost no information.
- **A theorem on all two-move exits.** Only the bounded census T15; the undecided target XyyxYxYxy (rank 5) shows that low-degree traces do not always suffice (mod 3 the residue j ≡ 5 mod 9 survives in degrees 3, 4, 5).

## 11. Honest limits

- Nothing here decides whether AK(3) is AC-trivial. Every result concerns *one* generalized move (T7, T8, T11–T14) or a bounded family of *two*-move paths (T15). No stable or generalized-move result is presented as an ordinary AC result; no AC equivalence is claimed, so no certificate is needed.
- T7 is uniform in n only for the c-frozen side. The k_n-frozen side is proved for n = 3, 4, 5 only.
- T5/T7 use O's Proposition O2 and O §2.2 (re-derived by the coordinator and by me) and Nielsen's classical theorem on primitive elements of F₂ (recalled; O checked it to length 11).
- The base cases of T5, the identities (TT) for ℓ and L4, T6, T12–T15 are exact computer verifications (integers, ℤ[ω], rationals, 𝔽₂); the scripts are short and self-tested, but the 39 + 30 linear identities were not all checked by hand (three samples are displayed in §7.3).
- The geometric interpretations (Gieseking manifold, I = 2cosh of a translation length, Mostow rigidity) are recalled and never used in a proof.
- Novelty is not established for anything here. Twisted (Reidemeister) traces and length-spectrum arguments are classical tools; the application to P_n is what is new relative to notes A–O.

## 12. Advice to the coordinator (ranked)

1. **Record the one-move statement for P₃ in the README:** no presentation with a primitive relator is one ACM move from P₃, whichever relator is frozen (T7 + T11); uniformly in n ≥ 3 for c frozen (T7); for n = 3, 4, 5 for k_n frozen (T12). Have TH08 (audit) re-run the three self-tests and re-check the three displayed (TT) samples and the hand computation of T11(c).
2. **Use twisted traces as the standard exact filter for any frozen-relator conjugacy question in free-by-cyclic one-relator groups.** They are integer linear algebra, give polynomial conditions in the family parameter, and settled Q2(3), which finite linear quotients could not touch. `th03_two.second_move` does this for arbitrary k′ satisfying Brown's criterion. Next targets: the undecided k′ = XyyxYxYxy of T15 (decide whether c ~ x(yx²)⁵ or x(yx²)⁻⁴ in ⟨x,y | k′⟩ — a positive answer would trivialize AK(3) — by 3-adic traces or a longer conjugator search), then the neighbours of length 10–12 (first enumerate them with the I/J/L4 filter as in T14).
3. **Two-move exits are now a finite, exact computation per first-move target.** A proof that *no* k′ in the class of k₃ admits the second move would need a uniform invariant in k′; I see no candidate. The mirror theorem T16 suggests looking for *torsion* twisted traces first: they exist in low degree whenever a product of eigenvalues of the monodromy is −1 or a root of unity, and one of degree 2 decided a question that every SL₂ invariant misses.
4. **Uniform Q2(n):** find the closed form of the top-degree twisted trace for ψ_n (weight (1,…,1), degree n, odd n). For n = 3 its restriction to powers of t₁ is C(j,2); a pattern in n = 5, 7 (degree 5, 7; ranks 3906, 960800 — the latter needs the weight decomposition, not brute force) could give the uniform statement.
5. **Do not expect I to separate everything** (T5(d): n = 4, 5), and do not expect SL₂-type invariants to see the mirror α (T9(c)); for N's chirality question on C4 this is a small worked example in which a symmetry of the frozen relator is invisible to all character-variety data but visible to a mod-2 nilpotent invariant — though here only for single moves.
6. Small erratum for O §9.1: yxyXYXy has y-exponent 2; it is not in the class of k₃ (T14).

## 13. Files written

- `research/research-th03.md` (this note).
- `experiments/th03_uniform.py` — ρ, Y, the integer invariant I, σ, τ, recurrence and growth checks, the rational invariant J; `--selftest`, `--table N`.
- `experiments/th03_q2.py` — G_{k_n} as F_n ⋊ ℤ, truncated Magnus algebra, twisted traces over ℚ and 𝔽₂, Q2(3), Q2(4), Q2(5); `--selftest`.
- `experiments/th03_two.py` — L4 on G_c, the census T14, Magnus rewriting of ⟨x,y | k′⟩ and the second-move test T15, the mirror invariant ε (T16); `--selftest`.
- No certificates (no AC equivalence is claimed).

## References

- Research notes A–O of this repository; especially O (Theorem O1, §2.2, Prop. O2, Theorem O6, question Q2), K (Theorem K1), G (Prop. G2, Lemma G0), D (Lemmas D3, D6).
- W. Magnus, A. Karrass, D. Solitar, *Combinatorial Group Theory* (Magnus expansion, §5.5; Magnus rewriting, §4.4); K. S. Brown, *Trees, valuations and the BNS invariant* (1987) for the criterion used in `structure` — recalled.
- J. Nielsen (1917); R. Osborne, H. Zieschang (1981): primitive elements of F₂ — recalled.
- K. Reidemeister (1936); B. Jiang, *Lectures on Nielsen fixed point theory* (1983): Reidemeister classes and traces — recalled, not consulted.
- H. Gieseking (1912); R. Riley (1975); W. Thurston's notes §4: the Gieseking manifold and the figure-eight representation in PSL(2,ℤ[ω]) — recalled, not consulted; the matrices of T1 were found and verified here.
