# Research TH01: the two-pair abelian lifting problem — a substitution principle, a transfer lattice, and a rigid example where lifting nevertheless holds

Date: 2026-11-09 (Los Angeles). Independent research agent TH01 (round 5, theory round).

**Status (draft being extended; central claims first).** The two-pair abelian lifting problem of N §2.3–2.4 is **not settled in general** (neither proved nor refuted, not even for central N). **No AK(3) trivialization, no obstruction, no counterexample, nothing on the AC conjecture itself.** What is achieved, all *proved here* with complete proofs:

| # | statement | label |
|---|---|---|
| T1 | **Substitution Lemma.** For a pair (u,t) of any group G, any σ ∈ G and any W(X) in the normal closure of X in G∗⟨X⟩: if σ ∈ ⟨⟨u·W(t)⟩⟩ ∩ ⟨⟨u·W(σ)⟩⟩ then (u,t) ~ (u·W(σ), t). So a correction available "from t" can be traded for the same correction "from σ". This is a lifting mechanism that N's correction modules D₀ × D₁ do not see (it changes the base pair and returns). | proved here (§2) |
| T2 | **Transfer lattice.** For z central: (uz,v) ~ (u,v) if z ∈ [⟨⟨v⟩⟩,G]; (uz,v) ~ (u,vz) if z ∈ [⟨⟨uv⟩⟩,G]; (uz,v) ~ (u,vz⁻¹) if z ∈ [⟨⟨uv⁻¹⟩⟩,G]. Hence the central two-pair lifting **holds whenever the two normal closures commute** ([⟨⟨s⟩⟩,⟨⟨t⟩⟩] = 1, e.g. every pair (a,b) ∈ A × B, and all quotients of such), for arbitrary — infinite, non-solvable — A, B. The same transfer for a non-central abelian N (Theorem 3.5) gives the full two-pair abelian lifting when, in addition, one of the two normal closures centralizes N (Corollary 3.6). | proved here (§3) |
| T3 | **A rigid example where lifting still holds.** G = SL(2,3) ∗_{C₂} (C₂ × ℤ) = ⟨SL(2,3), t \| [t,z]⟩, z = −1 central, z ∈ [G,G], Q = G/⟨z⟩ = A₄ ∗ ℤ (infinite, not solvable, not 2-generated), pairs (ω,t) and (zω,t), ω of order 3. (a) N's correction modules vanish (D₀ = D₁ = 0), and for **every** v ∈ G with t-exponent ≠ 0 the element zω is not in (ω^{±1})^G·⟨⟨v⟩⟩ — no path that keeps the normal closure of the second coordinate fixed can remove z (Gerstenhaber–Rothaus degree argument); the transfer lattice of T2 does not contain (z,1) either. (b) Nevertheless **(ω,t) ~ (zω,t)** in G, by an explicit path of four composite moves found with T1 (replayed exactly by `experiments/th01_substitution.py`, 0 failures). So "one-coordinate rigidity" — the natural source of a counterexample — does not obstruct. | proved here (§4); (a) uses an externally reported classical theorem, with the short proof included |
| T4 | Over a quotient G of F with G_ab = ℤ², every central twist of a pair π(U) is its image under a central automorphism θ_n of G; the set of removable twists is a subgroup, and central two-pair lifting is exactly a chirality problem (in N's sense) for the group of central automorphisms (§5). Four candidate invariants that **fail**, with reasons, and one explicit torsion-free test group where neither T1–T2 nor any obstruction I know decides the question (§6). | proved here / failed attempts / open |

Novelty is not established for anything (arXiv blocked; T1 is elementary and may well be folklore).

## 0. Previous work read and choice of direction

Read in full: `README.md`, `research-h.md` (with the coordinator's review: Theorem 2(ii) needs the perturbed pair to normally generate), `research-n.md`; status and reviews of the others; B and E skimmed. Used below, and re-derived where used: H Lemma 2.1/2.2 and Theorem 2(i) (abelian lifting against a *generating* pair), N Theorem N2.3 (correction modules D₀ = N(s−1) + [N,⟨⟨t⟩⟩], D₁ = N(t−1) + [N,⟨⟨s⟩⟩]) and Prop. N2.4 (the residual question is the orbit E(P′) of 0 under the affine AC monodromy).

**Direction: the seed, attacked from the central case.** For N central the linear part of N2.4's monodromy is the exponent-matrix action μ(m) ∈ GL₂(ℤ) (conjugation acts trivially on N), D₀ = D₁ = 0, and the question is purely: *which central twists (s z₀, t z₁) of a normally generating pair (s,t) are AC-equivalent to (s,t)?* I first tried to build a counterexample over a base in which no pair is AC-equivalent to a generating pair, using the most rigid situation I know (free products K ∗ ℤ with K finite in SU(2), where Gerstenhaber–Rothaus forces K to survive in every quotient by an element of nonzero t-exponent). The attempt failed for a structural reason, and the reason is the positive result T1: the second coordinate can be moved by t ↦ tσ⁻¹ and back, and this transports corrections. This is new relative to A–O (N explicitly restricts to corrections "available without changing the base pair") and is disjoint from the other nine seeds.

## 1. Conventions

G is any group; x^g := g⁻¹xg, [a,b] := a⁻¹b⁻¹ab; ⟨⟨u⟩⟩ is the normal closure in G. AC moves on a pair (u,v) of G: invert a coordinate; replace u by uv^{±1} or v by vu^{±1}; conjugate one coordinate by any g ∈ G; swap. "~" is the generated equivalence. Two standard composites are used throughout:

- (M) (u,v) ~ (u·w, v) for every w ∈ ⟨⟨v⟩⟩ (conjugate v, multiply, conjugate back, repeatedly); also (w·u, v), since w·u = u·w^u.
- (C) for central z and any g, h: [gz,h] = [g,h], hence [⟨⟨gz⟩⟩,G] = [⟨⟨g⟩⟩,G] ⊆ ⟨⟨gz⟩⟩ (the group [⟨⟨g⟩⟩,G] is the normal closure of {[g,h] : h ∈ G}).

For G ∗ ⟨X⟩ (free product with an infinite cyclic group) let 𝒦 := ker(G∗⟨X⟩ → G, X ↦ 1) = normal closure of X. For W ∈ 𝒦 and g ∈ G, W(g) ∈ G denotes the image of W under X ↦ g; W(g) ∈ ⟨⟨g⟩⟩. Example: W(X) = [X,c] = X⁻¹·c⁻¹Xc.

## 2. T1: the Substitution Lemma (proved here)

**Lemma 2.1 (substitution).** Let (u,t) be a pair of G, σ ∈ G, W ∈ 𝒦. If
    σ ∈ ⟨⟨u·W(t)⟩⟩ ∩ ⟨⟨u·W(σ)⟩⟩,
then (u,t) ~ (u·W(σ), t).

*Proof.* (1) W(t) ∈ ⟨⟨t⟩⟩, so (u,t) ~ (uW(t), t) by (M). (2) σ⁻¹ ∈ ⟨⟨uW(t)⟩⟩, so (uW(t), t) ~ (uW(t), t′) with t′ := tσ⁻¹, by (M). (3) In G/⟨⟨t′⟩⟩ the images of t and σ coincide, so the two homomorphisms G∗⟨X⟩ → G/⟨⟨t′⟩⟩ given by X ↦ t and X ↦ σ coincide; hence W(t)⁻¹W(σ) ∈ ⟨⟨t′⟩⟩ and (uW(t), t′) ~ (uW(σ), t′) by (M). (4) σ ∈ ⟨⟨uW(σ)⟩⟩, so (uW(σ), t′) ~ (uW(σ), t′σ) = (uW(σ), t). ∎

No hypothesis on normal generation is needed. With W(X) = [X,c]:

**Corollary 2.2 (commutator transfer).** If κ ∈ ⟨⟨u[t,c]⟩⟩ ∩ ⟨⟨u[κ,c]⟩⟩, then (u,t) ~ (u[κ,c], t).

So the trivial rule "u may be multiplied by [t,c]" upgrades to "u may be multiplied by [κ,c]" for every κ that both u[t,c] and u[κ,c] normally generate. The first condition is the nontrivial one; the next lemma is a cheap way to get it.

**Lemma 2.3 (torsion collapse).** Let u, c, t ∈ G and suppose cⁿ = ζ with ζ commuting with t (e.g. cⁿ = 1, or ζ central). Then (cu)ⁿζ⁻¹ ∈ ⟨⟨u[t,c]⟩⟩.

*Proof.* Put p = u[t,c] = u·t⁻¹c⁻¹tc. Then c p c⁻¹ = c u t⁻¹c⁻¹t, so cu = (c p c⁻¹)·(t⁻¹ct). Modulo ⟨⟨p⟩⟩ this reads cu ≡ t⁻¹ct, hence (cu)ⁿ ≡ t⁻¹cⁿt = t⁻¹ζt = ζ. ∎

**Remark 2.4 (what T1 means in N's language).** Let N ⊴ G be abelian, P′ = (s,t), and let E(P′) ⊆ N² be the set of n with P′·n ~ P′ (N2.4). N2.3 gives E ⊇ D₀ × D₁, obtained with the base pair held fixed. Lemma 2.1 gives further elements: (W(σ), 0) ∈ E for every W ∈ 𝒦 and σ with W(σ) ∈ N and σ ∈ ⟨⟨sW(t)⟩⟩ ∩ ⟨⟨sW(σ)⟩⟩ — elements of N ∩ ⟨⟨σ⟩⟩ rather than of N ∩ ⟨⟨t⟩⟩. §4 shows that this can be strictly more than D₀ × D₁ and more than everything obtainable with ⟨⟨second coordinate⟩⟩ held fixed.

## 3. T2: the transfer lattice, and central lifting when the normal closures commute (proved here)

**Proposition 3.1 (three central transfers).** Let (u,v) be a pair of G and z ∈ Z(G).
1. If z ∈ [⟨⟨v⟩⟩,G], then (uz,v) ~ (u,v).
2. If z ∈ [⟨⟨uv⟩⟩,G], then (uz,v) ~ (u,vz).
3. If z ∈ [⟨⟨uv⁻¹⟩⟩,G], then (uz,v) ~ (u,vz⁻¹).

All three hypotheses are unchanged if u, v are multiplied by central elements (by (C)).

*Proof.* 1: z⁻¹ ∈ ⟨⟨v⟩⟩, use (M). 2: (uz,v) → (uz, v·uz). By (C), ⟨⟨vuz⟩⟩ ⊇ [⟨⟨vu⟩⟩,G] = [⟨⟨uv⟩⟩,G] ∋ z (vu is conjugate to uv), so by (M) → (u, vuz); multiply coordinate 1 on the right by u⁻¹: vuz·u⁻¹ = vz. 3: (uz,v) → (uz,v⁻¹) → (uz, v⁻¹uz); as in 2, ⟨⟨v⁻¹uz⟩⟩ ∋ z, so → (u, v⁻¹uz) → (u, v⁻¹z) → (u, vz⁻¹). ∎

**Theorem 3.2 (transfer lattice).** Let (s,t) be a pair of G, Z = Z(G), S = ⟨⟨s⟩⟩, T = ⟨⟨t⟩⟩, R₊ = ⟨⟨st⟩⟩, R₋ = ⟨⟨st⁻¹⟩⟩. Let Λ ≤ Z × Z be the subgroup generated by
    (Z∩[T,G]) × 1,   1 × (Z∩[S,G]),   {(z,z⁻¹) : z ∈ Z∩[R₊,G]},   {(z,z) : z ∈ Z∩[R₋,G]}.
Then (s z₀, t z₁) ~ (s,t) for all (z₀,z₁) ∈ Λ.

*Proof.* Each generator λ = (a,b) gives (s y₀ a, t y₁ b) ~ (s y₀, t y₁) for **all** central y₀, y₁: for the first two kinds this is 3.1(1) applied to (s y₀, t y₁) (and its swap); for the third, 3.1(2) gives (s y₀ z, t y₁ z⁻¹) ~ (s y₀, t y₁ z⁻¹ z); for the fourth, 3.1(3). The generating set is closed under inverses and Z × Z is abelian, so an element of Λ is a product λ₁⋯λ_k of generators, removed one at a time. ∎

(The same argument applied to a Nielsen-transformed pair gives one more family of generators for each primitive class of the free group on (s,t): if q(s,t) is primitive with exponent vector (a,b) and z ∈ Z ∩ [⟨⟨q(s,t)⟩⟩,G], then (z^b, z^{−a}) ∈ Λ. Not needed below.)

**Theorem 3.3 (central lifting for commuting normal closures).** Let (s,t) normally generate G and suppose [S,T] = 1 (for instance G = A × B with s ∈ A, t ∈ B; or any quotient of such a G). Then for all z₀, z₁ ∈ Z(G) ∩ [G,G]: (s z₀, t z₁) ~ (s,t). Consequently, if N ≤ Z(G) ∩ [G,G] and P is any pair of G whose image in G/N is AC-equivalent to the image of (s,t), then P ~ (s,t).

*Proof.* G = ST and [S,T] = 1 give [G,G] = [S,S][T,T], [S,G] = [S,S], [T,G] = [T,T]. Let z ∈ Z ∩ [G,G], z = z_S z_T with z_S ∈ [S,S], z_T ∈ [T,T]. Then z_S is central: it commutes with T because it lies in S, and for g ∈ S, [z_S,g] = [z z_T⁻¹, g] = 1 because z is central and z_T ∈ T commutes with g. Likewise z_T is central. Next, [R₊,G] ⊇ [G,G]: for g ∈ S, [st,g] = [s,g]^t[t,g] = [s,g], and for g ∈ T, [st,g] = [t,g]; the normal closure of {[s,g] : g ∈ S} is [S,S] (modulo it s is central in S, and S is generated by conjugates of s, which are conjugates by elements of S because T centralizes S; so the quotient of S is cyclic), and similarly for T. Now (z_T,1) ∈ Λ, (1,z_S) ∈ Λ, and (z_S,z_S⁻¹) ∈ Λ because z_S ∈ Z ∩ [R₊,G]; hence (z_S,1) = (z_S,z_S⁻¹)(1,z_S) ∈ Λ and (z,1) ∈ Λ. Symmetrically (1,z) ∈ Λ. So Λ ⊇ (Z∩[G,G])², and Theorem 3.2 applies. For the last sentence lift an AC path from the image of P to the image of (s,t): P ~ (s z₀, t z₁) with z_i ∈ N. ∎

This is the two-pair analogue of H's Lemma 2.2 in a situation where neither coordinate normally generates and G/⟨⟨t⟩⟩ ≅ S/(S∩T) is an arbitrary one-normal-generator group (the point where H's argument stops, N §2.3). It also shows that N's fibre-product examples cannot be found among direct products A × B of "weight-one" groups, however wild A and B are.

### 3.1 The same transfer for a non-central abelian N (proved here)

Let N ⊴ G be abelian (written multiplicatively) and [N,L] := ⟨[m,x] : m ∈ N, x ∈ L⟩ for L ⊴ G (a G-normal subgroup of N; N2.3's module [N,L]).

**Lemma 3.4.** For g ∈ G and ν ∈ N: [N,⟨⟨gν⟩⟩] = [N,⟨⟨g⟩⟩] ⊆ ⟨⟨gν⟩⟩.
*Proof.* For m ∈ N, h ∈ G: [m,(gν)^h] = [m, g^hν^h] = [m,ν^h]·[m,g^h]^{ν^h} = [m,g^h], because N is abelian ([a,bc] = [a,c][a,b]^c). Both groups are generated by the G-conjugates of these elements (use [m,xy] = [m,y][m,x]^y and [m,x⁻¹] = ([m,x]⁻¹)^{x⁻¹}), and [m,(gν)^h] ∈ ⟨⟨gν⟩⟩. ∎

**Theorem 3.5 (abelian transfer).** Let N ⊴ G be abelian, (s,t) a pair of G, S, T, R₊ as in 3.2, and ν₀, ν₁ ∈ N arbitrary.
(a) (sν₀·n, tν₁) ~ (sν₀, tν₁) for n ∈ [N,T], and (sν₀, tν₁·n) ~ (sν₀, tν₁) for n ∈ [N,S] (this is part of N2.3).
(b) (sν₀·n, tν₁) ~ (sν₀, tν₁·sns⁻¹) for every n ∈ [N,R₊].
(c) Hence (s n₀, t n₁) ~ (s,t) whenever n₁ ∈ [N,S] and n₀ ∈ [N,T]·([N,R₊] ∩ [N,S]); symmetrically with the roles of s and t exchanged.
(d) If T centralizes N, or S centralizes N, then (s n₀, t n₁) ~ (s,t) for **all** n₀, n₁ ∈ [N,G].

*Proof.* (a) By 3.4, [N,T] ⊆ ⟨⟨tν₁⟩⟩ and [N,S] ⊆ ⟨⟨sν₀⟩⟩; use (M). (b) (sν₀n, tν₁) → (sν₀n, tν₁·sν₀n); the new second coordinate is ts·ν with ν = ν₁^sν₀n ∈ N, so by 3.4 its normal closure contains [N,⟨⟨ts⟩⟩] = [N,R₊] ∋ n; by (M) → (sν₀, tν₁sν₀n); multiply coordinate 1 on the right by (sν₀)⁻¹: tν₁·(sν₀)n(sν₀)⁻¹ = tν₁·sns⁻¹. (c) Write n₀ = ab, a ∈ [N,T], b ∈ [N,R₊]∩[N,S]: remove a by (a), transfer b by (b) to the error n₁·sbs⁻¹ ∈ [N,S] on coordinate 1, remove it by (a). (d) Let T centralize N. Then [m,(st)^h] = [m,s^ht^h] = [m,t^h][m,s^h]^{t^h} = [m,s^h], so [N,R₊] = [N,S], and likewise [N,G] = [N,S]; apply (c). The other case is symmetric (swap the coordinates). ∎

For a generating pair N(s−1)·N(t−1) = [N,G] and (a) alone suffices (H Lemma 2.1); for a normally generating pair (b) is new: it moves an error between the coordinates through the Nielsen-adjacent pair (s, ts).

**Corollary 3.6 (a class in which the two-pair abelian lifting holds).** Let (s,t) normally generate G with [S,T] = 1, and let N ⊴ G be abelian with N ⊆ [G,G] and centralized by S or by T. If the image of a pair P in G/N is AC-equivalent to the image of (s,t), then P ~ (s,t) in G.
*Proof.* P ~ (s n₀, t n₁) with nᵢ ∈ N. In G₁ = G/[N,G] the image of N is central and inside [G₁,G₁], and the normal closures of the images of s and t still commute; Theorem 3.3 gives (s n₀, t n₁) ~ (s,t) in G₁. Lifting this path: (s n₀, t n₁) ~ (s e₀, t e₁) with eᵢ ∈ [N,G], and 3.5(d) finishes. ∎

Example: G = (M ⋊ A) × B with A, B arbitrary groups having one normal generator each (s ∈ A, t ∈ B), M any ℤ[A]-module with M = M·I_A, N = M. For infinite non-solvable A, B this is outside BLM and Guyot, and H's Theorem 2(i) applies only if one of the two pairs is AC-equivalent in G/N to a generating pair.

## 4. T3: a rigid example in which lifting nevertheless holds (proved here)

Let K = SL(2,3), realised as the 24 unit Hurwitz quaternions {±1, ±i, ±j, ±k, (±1±i±j±k)/2} ⊂ SU(2) = S³; z = −1; ω = (−1+i+j+k)/2 (order 3, trace −1). K has exactly the normal subgroups 1, ⟨z⟩, Q₈ = [K,K], K, and K/Q₈ ≅ C₃ is generated by the image of ω. Put

    G := ⟨K, t | [t,z] = 1⟩ = K ∗_{⟨z⟩} (⟨z⟩ × ⟨t⟩),   e: G → ℤ the t-exponent,   Q := G/⟨z⟩ ≅ A₄ ∗ ℤ.

z is central in G and z = [j,i] ∈ [G,G] (ji = −k, so [j,i] = j⁻¹i⁻¹ji = (ji)² = −1). The pairs (ω,t) and (zω,t) normally generate G (⟨⟨ω⟩⟩ ⊇ K and ⟨⟨zω⟩⟩ ⊇ K, see below) and have the same image in Q. G is infinite and not solvable; Q has rank 3 (Grushko), so no pair of Q generates it and H's Lemma 2.2 / Theorem 2(i) cannot be applied; N's correction modules for the central N = ⟨z⟩ are D₀ = D₁ = 0.

**Proposition 4.1 (one-coordinate rigidity; Gerstenhaber–Rothaus).** Let v ∈ G with e(v) ≠ 0.
1. There is a homomorphism ρ: G → SU(2) extending the inclusion K ⊂ SU(2) with ρ(v) = 1.
2. z ∉ ⟨⟨v⟩⟩, and for all u, u′ ∈ G: if u′ ∈ (u^{±1})^G·⟨⟨v⟩⟩ then tr ρ(u′) = tr ρ(u). In particular zω ∉ (ω^{±1})^G·⟨⟨v⟩⟩.
3. Hence: a swap-free AC path in G along which the normal closure of the second coordinate is constant, equal to ⟨⟨v⟩⟩ with e(v) ≠ 0, cannot lead from a pair (ω, ·) to a pair (zω, ·). (Every normally generating pair (u,v) of G has e(u) ≠ 0 or e(v) ≠ 0.) Also (z,1) ∉ Λ for the lattice Λ of Theorem 3.2 at (ω,t) (its first-coordinate generators need z ∈ ⟨⟨q⟩⟩ with e(q) ∈ {1, 1, −1} ≠ 0).

*Proof.* 1 (the classical degree argument of Gerstenhaber–Rothaus 1962, *externally reported*, proof included). For τ ∈ SU(2) let ρ_τ be the identity on K and ρ_τ(t) = τ; this is well defined since −1 is central in SU(2). Write v = k₀t^{n₁}k₁⋯t^{n_r}k_r; the map f_v: S³ → S³, τ ↦ ρ_τ(v) = k₀τ^{n₁}k₁⋯τ^{n_r}k_r is a pointwise product, in the group S³, of constant maps and of copies of id^{±1}. In [S³,S³] = π₃(S³) ≅ ℤ the pointwise product is addition (Eckmann–Hilton), constants are 0 and id^{±1} is ±1; so deg f_v = Σnᵢ = e(v) ≠ 0, f_v is surjective, and some τ₀ has f_v(τ₀) = 1. Take ρ = ρ_{τ₀}. 2: ρ kills ⟨⟨v⟩⟩ and ρ(z) = −1 ≠ 1. If u′ = g⁻¹u^{±1}g·w with w ∈ ⟨⟨v⟩⟩ then ρ(u′) is conjugate to ρ(u)^{±1}, and tr(A⁻¹) = tr(A) in SU(2). Finally tr ρ(zω) = −tr ω = 1 ≠ −1 = tr ρ(ω). 3: along such a path the first coordinate changes only by inversion, conjugation and multiplication by elements of ⟨⟨v⟩⟩, so its class in (·^{±1})^G⟨⟨v⟩⟩ is constant; the statement on Λ follows from 2 with v = t, st, st⁻¹. ∎

**Theorem 4.2.** In G: (ω,t) ~ (zω,t). Explicitly, with p := ω[t,i] = ω·t⁻¹i⁻¹ti,

    (ω,t) → (p,t) → (p, tj⁻¹) → (zω, tj⁻¹) → (zω,t).

*Proof.* Apply Corollary 2.2 with u = ω, c = i, κ = j: [κ,c] = [j,i] = z. It remains to check j ∈ ⟨⟨p⟩⟩ ∩ ⟨⟨zω⟩⟩; we show both normal closures contain K.
(i) By Lemma 2.3 with n = 4, i⁴ = 1: (iω)⁴ ∈ ⟨⟨p⟩⟩. Now iω = (−1−i−j+k)/2 has trace −1, hence order 3, so (iω)⁴ = iω ∈ ⟨⟨p⟩⟩. An element of K outside Q₈ has normal closure K in K. So K ⊆ ⟨⟨p⟩⟩.
(ii) zω ∈ K∖Q₈, so its normal closure in K is K.
The four arrows are the four steps of the proof of Lemma 2.1: the second uses j⁻¹ ∈ ⟨⟨p⟩⟩; for the third, modulo ⟨⟨tj⁻¹⟩⟩ one has t ≡ j and p ≡ ω[j,i] = zω, explicitly p·w = zω with w = (i⁻¹j⁻¹)·(tj⁻¹)⁻¹·(i⁻¹j⁻¹)⁻¹ · (i⁻¹j⁻¹i)·(tj⁻¹)·(i⁻¹j⁻¹i)⁻¹ ∈ ⟨⟨tj⁻¹⟩⟩; the fourth uses j ∈ ⟨⟨zω⟩⟩. ∎

**Corollary 4.3.** In this G the set E((ω,t)) of N2.4 is all of N² = ⟨z⟩² ((1,z) ∈ E because z ∈ K ⊆ ⟨⟨ω⟩⟩), although D₀ × D₁ = 0, the transfer lattice gives only 1 × ⟨z⟩, and no path with constant second normal closure reaches (z,1). The two-pair central lifting holds over this base; the mechanism is the substitution t ↦ tj⁻¹.

The same proof works verbatim for K = SL(2,5) ⊃ SL(2,3) (Q = A₅ ∗ ℤ; every non-central element of the quasisimple group K normally generates it), and — with Lemma 2.3 in its "cⁿ central" form — for torsion-free K such as π₁ of the Brieskorn sphere Σ(2,3,7) one still gets K ⊆ ⟨⟨s[t,a]⟩⟩ (a² = z, s = b: the relation forces (ab)² = z while (ab)⁷ = z^{±1}), but there z is not a single central commutator [κ,c] and I did not complete a chain of commutator transfers; see §6.

## 5. T4: the central case as a chirality problem for central automorphisms (proved here)

**Proposition 5.1.** Let N ≤ Z(G) ∩ [G,G] and φ ∈ Hom(G,N) (so φ kills [G,G] ⊇ N). Then θ_φ: g ↦ g·φ(g) is an automorphism of G (inverse θ_{φ⁻¹}) inducing the identity on G/N and on N, θ_φθ_ψ = θ_{φψ}, and θ_φ(u,v) = (uφ(u), vφ(v)). Consequently:
1. For every pair P of G, E_aut(P) := {φ : θ_φ(P) ~ P} is a **subgroup** of Hom(G,N) (the stabilizer of the AC class of P; automorphisms preserve ~).
2. If G_ab is free abelian on the images of the coordinates of P — e.g. G = F/K with K ⊆ [F,F] and P = π(U) for a normally generating pair U of F — then every central twist P·(n₀,n₁) is θ_φ(P) for the unique φ with φ(u) = n₀, φ(v) = n₁. So E(P) of N2.4 is a subgroup of N², and "P·n ~ P" says that the central automorphism θ_n fixes the class of P.
3. In that situation every θ_n fixes the standard class (H Lemma 2.2). Hence over such G **the two-pair central lifting problem is exactly a chirality problem in the sense of N2.1**, for the abelian group Hom(G,N) ≅ N² of central automorphisms instead of GL₂(ℤ): is the class of π(U) fixed by all θ_n? (These θ_n need not be induced from Aut(F).)

*Proof.* θ_φ(gh) = gh·φ(g)φ(h) = gφ(g)·hφ(h) because φ(g) is central; θ_φ(θ_ψ(g)) = gψ(g)·φ(g)φ(ψ(g)) = g·φ(g)ψ(g) since φ(N) = 1. The rest is immediate. ∎

So a counterexample to central two-pair lifting over a quotient of F with ℤ²-abelianization would be a "central chirality": a class of pairs moved by a central automorphism that fixes the standard class. Theorems 3.2/3.3 and Lemma 2.1 are then lower bounds on the stabilizer E(P), exactly as N's certificates are lower bounds on Ŝ(C4). In §4 the twist (z,1) is *not* automorphic (ω has order 3, zω order 6), which is why a trace argument gives rigidity there.

## 6. Failed attempts, and the sharpest open test case

**(F1) A Gerstenhaber–Rothaus invariant (failed; reason proved).** For G = ⟨K,t | [t,z]⟩ with K ⊂ SU(2) I tried J(p,q) := {tr ρ_τ(p) : ρ_τ(q) = 1} for the "normal form" (e(p), e(q)) = (0, ±1) of a pair. J is nonempty (Prop. 4.1), invariant under all moves on p, and under conjugation/inversion of q, and J(zp,q) = −J(p,q). It is **not** invariant under q ↦ q·w′, w′ ∈ ⟨⟨p⟩⟩: Theorem 4.2 is a counterexample (J(p,t) = {−1}, J(p,tj⁻¹) = {+1} for p = ω[t,i]). So no invariant of the form "conjugacy data of one coordinate modulo the other" survives the substitution t ↦ tσ⁻¹.

**(F2) Homotopy/linking invariants of the word maps (failed; sketch).** The pair of word maps (û,v̂): S³ → S³×S³ avoids the four points (±1,±1); S³×S³ minus points is 2-connected with π₃ = ℤ², so the homotopy class is only (e(u),e(v)). The 5-cycle swept by the conjugacy classes of û(τ) links the punctures (1,1), (−1,1) with numbers (ℓ,−ℓ); u ↦ zu and u ↦ u⁻¹ both change the sign of ℓ, so only |ℓ| could be invariant and it does not see z.

**(F3) The relative homotopy type (failed).** For Q = G/N and X = K(Q,1) ∪ e²_s ∪ e²_t (simply connected), lifts of (s,t) to a central extension correspond to extensions to X of the extension class, and self-equivalences of X rel K(Q,1) act transitively on them (slide a 2-cell over a spherical class of H₂(Q) ⊂ π₂(X)). So nothing of the pair (X, K(Q,1)) up to homotopy can obstruct; AC moves realize only slides over classes supported on the *other* cell, which is the whole difficulty. (This is the two-pair, relative form of N1; sketch, not used elsewhere.)

**(F4) A general proof of the central case (failed).** Writing [G,G] = [S,S]·[T,G], a central z₀ on the first coordinate reduces to its [S,S]-part; Theorem 3.2 removes it when it lies in [R₊,G]∩[S,G] and Lemma 2.1 when a suitable (W,σ) exists. I could not produce (W,σ) in general: the first condition σ ∈ ⟨⟨s·W(t)⟩⟩ is a "collapse" statement about a one-relator quotient, and it genuinely fails in torsion-free situations (next item).

**Test case 6.1 (open; the sharpest instance I know).** Let Ã = Heis(ℤ) ⋊_M ⟨s⟩ with M = [[2,1],[1,1]] acting on Heis(ℤ) = ⟨a,b | z = [a,b] central⟩ through any lift of M; Ã_ab = ℤ (det(M−I) = −1), so Ã = ⟨⟨s⟩⟩, and z ∈ Z(Ã) ∩ [Ã,Ã]. Put G = ⟨Ã, t | [t,z]⟩ = Ã ∗_{⟨z⟩} ℤ², torsion-free, Q = G/⟨z⟩ = (ℤ² ⋊_M ℤ) ∗ ℤ. *Question: is (sz,t) ~ (s,t) in G?* Facts (proved here unless marked): (i) (s,tzʲ) ~ (s,t) for all j, and (sz,t) = θ(s,t) for the central automorphism θ: s ↦ sz, t ↦ t, a ↦ a, b ↦ b; so E = dℤ × ℤ for some d ≥ 0 and the question is whether d = 1. (ii) d = 1 in G/⟨⟨[t,Ã]⟩⟩ = Ã × ℤ (Theorem 3.3), in G/⟨⟨[t,a],[t,b]⟩⟩ = Heis ⋊ F(s,t) (there z = [ta,b] ∈ ⟨⟨ta⟩⟩, so (s,t) → (s,ta) → (sz,ta) → (sz,t)), and in every finite or solvable quotient of G (BLM, Guyot). (iii) sz is not conjugate to s^{±1} in Ã = G/⟨⟨t⟩⟩ ([s,h] is central only if h is). (iv) Commutator transfer with c ∈ Ã fails: for c ∈ Ã with c, cs ∉ ⟨z⟩ the group G/⟨⟨s[t,c]⟩⟩ = ⟨Ã,t | [t,z], t⁻¹ct = cs⟩ is an HNN extension of Ã (⟨c,z⟩ ≅ ⟨cs,z⟩ ≅ ℤ², because Ã is torsion-free and a power of a non-central element is never central), so no nontrivial element of Ã lies in ⟨⟨s[t,c]⟩⟩; for c ∈ ⟨z⟩ or cs ∈ ⟨z⟩ the element s[t,c] is conjugate to s and the transfer is trivial. (v) *Expected, not proved:* z ∉ ⟨⟨v⟩⟩ for every v with e(v) ≠ 0, by the Gerstenhaber–Rothaus argument in U(p) applied to finite quotients of Ã in which z acts as a nontrivial scalar. A proof of d ≠ 1 would be a genuine pair-separating invariant in an infinite group (as hard, I believe, as a disproof of a generalized AC statement: G is residually solvable, so by Guyot it would have to be an unbounded-distance phenomenon along solvable quotients); a proof of d = 1 needs a mechanism beyond Lemma 2.1 with σ ∈ Ã.
