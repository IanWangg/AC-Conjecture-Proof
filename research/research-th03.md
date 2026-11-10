# Research TH03: no single generalized move from P_3 reaches a primitive relator — the length spectrum of the Gieseking coordinates (uniform in n) and twisted traces for the killer side

Date: 2026-11-09 (Los Angeles). Independent research agent TH03 (round 5, theory round).

**Status:** partial, fully proved results about *single generalized (ACM) moves* from P_n (for the c-frozen side uniformly in n ≥ 3; for the k_n-frozen side for n = 3, 4, 5). Headline: **no presentation with a primitive relator is one ACM move from P₃ ~AC AK(3), whichever relator is frozen** (T7 + T11) — the complete P₃-analogue of G's Proposition G2; this closes O's open question Q2 for n = 3. **No AC trivialization of AK(3), no proof of non-triviality, no counterexample, nothing on the full conjecture.** Every statement is labelled *proved here*, *proved here by exact computation* (script with self-test), *experiment* (exact bounds), *recalled*, or *open*.

| # | statement | label |
|---|---|---|
| T1 | Explicit ρ: F(a,b) → SL(2,ℤ[ω]) and Y ∈ SL(2,ℤ[ω]) with Y·conj(ρ(u))·Y⁻¹ = ρ(φ(u)) for all u; T = Y·conj(Y) gives a representation of the index-2 subgroup H in SL(2,ℤ[ω]) | proved here (hand-checked identities; re-checked by script) |
| T2 | I(u) := tr(ρ(u)Y·conj(ρ(u)Y)) is a **rational integer** depending only on the conjugacy class of (u,1) in G_c (no sign ambiguity, no twist ambiguity) | proved here |
| T3–T5 | σ(s) := I(xˢy) and τ(n) := I(k_n) satisfy u(n+4) = 3u(n+3) − u(n+2) + 3u(n+1) − u(n); σ(s) = σ(1−s); σ(n) < τ(n) < σ(n+1) for all n ≥ 6; **the equation τ(n) = σ(s), n ≥ 1, has exactly the solutions n ∈ {1,2} (s ∈ {−2,3}), n = 4 (s ∈ {−4,5}), n = 5 (s ∈ {−5,6})** | proved here (integer induction; base cases by exact computation) |
| T6 | k_4 ≁ x⁵y, x⁻⁴y and k_5 ≁ x⁶y, x⁻⁵y in G_c, although they have the same invariant I ("isospectral") | proved here by exact rational computation |
| **T7** | **For every n ≥ 3 and every s ∈ ℤ, k_n is not conjugate in G_c to xˢy. Hence for every n ≥ 3 no presentation with a primitive relator is one ACM move (arbitrary conjugators) from P_n = (c, k_n) with c frozen.** Uniform version of O6 (n = 3,…,8), the P_n-coordinate analogue of G2 | proved here (T2 + T5 + T6 + O's Prop. O2) |
| T8 | τ is strictly increasing on n ≥ 2: for n ≠ m (n, m ≥ 2) no c-frozen ACM move joins P_n and P_m (answers K's advice 1(b) negatively); every c-frozen neighbour (c,w) of P_n has I(w^{±1}) = τ(n) | proved here |
| T9 | α: x ↦ x⁻¹, y ↦ yx is an involution of F(x,y) with α(c) conjugate to c⁻¹; it sends xˢy to a conjugate of x^{1−s}y and k_n to a conjugate of x⁻ⁿy⁻¹xyxy, and preserves I and every SL₂-trace invariant; so such invariants can never separate k_n from α(k_n) | proved here |
| **T11** | **k_n-frozen side (O's open question Q2).** G_{k_n} = F(t₀,…,t_{n−1}) ⋊_ψ ℤ, c = (t₁t₂⁻¹t₁⁻¹, 1), and the primitive candidates are xtʲ = (t₁ʲ, 1). An explicit integer *twisted trace* ℓ on the Magnus algebra truncated in degree 3 gives ℓ(c) = −2 but ℓ(xtʲ) = j(j−1)/2 ≥ 0. **Hence c is conjugate to no primitive element in ⟨x,y \| k₃⟩, and — with T7 — no presentation with a primitive relator is one ACM move from P₃ = (xyxYYXy, xxxYXyy), whichever relator is frozen, with arbitrary conjugators (also after any automorphism of F₂).** Same conclusion for n = 4 (𝔽₂-valued twisted traces, degree 4) and n = 5 (rational, degree 3) | proved here (short theory + exact linear algebra, script with self-test); n ≥ 6 **open** |
| T10 | Two-move exits: exact reformulation and which tools decide each step | proved here (reformulation only); existence of a two-move exit from P₃ is **open** |

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
