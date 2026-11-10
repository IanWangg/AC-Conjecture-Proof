# Research TH03: the length spectrum of the Gieseking coordinates — a uniform proof that no c-frozen move from P_n reaches a primitive relator (all n ≥ 3)

Date: 2026-11-09 (Los Angeles). Independent research agent TH03 (round 5, theory round).

**Status:** partial, fully proved results about *single generalized (ACM) moves with the relator c frozen*. **No AC trivialization of AK(3), no proof of non-triviality, no counterexample, nothing on the full conjecture.** Every statement is labelled *proved here*, *proved here by exact computation* (script with self-test), *experiment* (exact bounds), *recalled*, or *open*.

| # | statement | label |
|---|---|---|
| T1 | Explicit ρ: F(a,b) → SL(2,ℤ[ω]) and Y ∈ SL(2,ℤ[ω]) with Y·conj(ρ(u))·Y⁻¹ = ρ(φ(u)) for all u; T = Y·conj(Y) gives a representation of the index-2 subgroup H in SL(2,ℤ[ω]) | proved here (hand-checked identities; re-checked by script) |
| T2 | I(u) := tr(ρ(u)Y·conj(ρ(u)Y)) is a **rational integer** depending only on the conjugacy class of (u,1) in G_c (no sign ambiguity, no twist ambiguity) | proved here |
| T3–T5 | σ(s) := I(xˢy) and τ(n) := I(k_n) satisfy u(n+4) = 3u(n+3) − u(n+2) + 3u(n+1) − u(n); σ(s) = σ(1−s); σ(n) < τ(n) < σ(n+1) for all n ≥ 6; **the equation τ(n) = σ(s), n ≥ 1, has exactly the solutions n ∈ {1,2} (s ∈ {−2,3}), n = 4 (s ∈ {−4,5}), n = 5 (s ∈ {−5,6})** | proved here (integer induction; base cases by exact computation) |
| T6 | k_4 ≁ x⁵y, x⁻⁴y and k_5 ≁ x⁶y, x⁻⁵y in G_c, although they have the same invariant I ("isospectral") | proved here by exact rational computation |
| **T7** | **For every n ≥ 3 and every s ∈ ℤ, k_n is not conjugate in G_c to xˢy. Hence for every n ≥ 3 no presentation with a primitive relator is one ACM move (arbitrary conjugators) from P_n = (c, k_n) with c frozen.** Uniform version of O6 (n = 3,…,8), the P_n-coordinate analogue of G2 | proved here (T2 + T5 + T6 + O's Prop. O2) |
| T8 | τ is strictly increasing on n ≥ 2: for n ≠ m (n, m ≥ 2) no c-frozen ACM move joins P_n and P_m (answers K's advice 1(b) negatively); every c-frozen neighbour (c,w) of P_n has I(w^{±1}) = τ(n) | proved here |
| T9 | α: x ↦ x⁻¹, y ↦ yx is an involution of F(x,y) with α(c) conjugate to c⁻¹; it sends xˢy to a conjugate of x^{1−s}y and k_n to a conjugate of x⁻ⁿy⁻¹xyxy, and preserves I and every SL₂-trace invariant; so such invariants can never separate k_n from α(k_n) | proved here |
| T10 | Two-move exits: exact reformulation; G_{k_n} = F(t₀,…,t_{n−1}) ⋊ ℤ and the k_n-frozen primitive exit Q2(n) ⇔ "t₀ʲ is ψ_n-twisted conjugate to t₁⁻¹t₀⁻¹t₁ for some j" | proved here (reformulation only); Q2(n) **open** for all n ≥ 3 |

## 1. Previous work read and choice of direction

Read in full: `README.md`, `research/research-o.md` (with the coordinator's review), `research/research-k.md` (with review); skimmed `research-g.md` (summary table, review); for all other notes A–N the status paragraph and the coordinator's review sections. Re-ran `python3 experiments/o_gc.py --selftest` implicitly through an import cross-check (300 random words: my normal form agrees with `o_gc.nf`). What I use, and have re-derived: O1 (G_c = ⟨x,y | c⟩ ≅ F(a,b) ⋊_φ ℤ, a = x, b = yxY, φ(a) = b, φ(b) = b⁻¹a; elements (u,k), (u,k)(u′,k′) = (uφᵏ(u′), k+k′)); O §2.2 (the conjugacy class of (u,1) meets F(a,b)×{1} exactly in the Reidemeister class R(u) = {v u φ(v)⁻¹}); O2 (a c-frozen ACM move from P_n to a presentation with a primitive relator exists iff k_n = (aⁿb⁻¹a⁻¹, 1) is conjugate in G_c to xˢy = (aˢ,1) for some s); K1 (AK(n) ~AC P_n = (c, k_n), c = xyxYYXy, k_n = xⁿYXyy).

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
