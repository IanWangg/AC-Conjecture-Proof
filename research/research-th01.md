# Research TH01: the two-pair abelian lifting problem — a substitution principle, a transfer lattice, and a rigid example where lifting nevertheless holds

Date: 2026-11-09 (Los Angeles). Independent research agent TH01 (round 5, theory round).

**Status (draft being extended; central claims first).** The two-pair abelian lifting problem of N §2.3–2.4 is **not settled in general** (neither proved nor refuted, not even for central N). **No AK(3) trivialization, no obstruction, no counterexample, nothing on the AC conjecture itself.** What is achieved, all *proved here* with complete proofs:

| # | statement | label |
|---|---|---|
| T1 | **Substitution Lemma.** For a pair (u,t) of any group G, any σ ∈ G and any W(X) in the normal closure of X in G∗⟨X⟩: if σ ∈ ⟨⟨u·W(t)⟩⟩ ∩ ⟨⟨u·W(σ)⟩⟩ then (u,t) ~ (u·W(σ), t). So a correction available "from t" can be traded for the same correction "from σ". This is a lifting mechanism that N's correction modules D₀ × D₁ do not see (it changes the base pair and returns). | proved here (§2) |
| T2 | **Transfer lattice.** For z central: (uz,v) ~ (u,v) if z ∈ [⟨⟨v⟩⟩,G]; (uz,v) ~ (u,vz) if z ∈ [⟨⟨uv⟩⟩,G]; (uz,v) ~ (u,vz⁻¹) if z ∈ [⟨⟨uv⁻¹⟩⟩,G]. Hence the central two-pair lifting **holds whenever the two normal closures commute** ([⟨⟨s⟩⟩,⟨⟨t⟩⟩] = 1, e.g. every pair (a,b) ∈ A × B, and all quotients of such), for arbitrary — infinite, non-solvable — A, B. | proved here (§3) |
| T3 | **A rigid example where lifting still holds.** G = SL(2,3) ∗_{C₂} (C₂ × ℤ) = ⟨SL(2,3), t \| [t,z]⟩, z = −1 central, z ∈ [G,G], Q = G/⟨z⟩ = A₄ ∗ ℤ (infinite, not solvable, not 2-generated), pairs (ω,t) and (zω,t), ω of order 3. (a) N's correction modules vanish (D₀ = D₁ = 0), and for **every** v ∈ G with t-exponent ≠ 0 the element zω is not in (ω^{±1})^G·⟨⟨v⟩⟩ — no path that keeps the normal closure of the second coordinate fixed can remove z (Gerstenhaber–Rothaus degree argument); the transfer lattice of T2 does not contain (z,1) either. (b) Nevertheless **(ω,t) ~ (zω,t)** in G, by an explicit path of four composite moves found with T1 (replayed exactly by `experiments/th01_substitution.py`, 0 failures). So "one-coordinate rigidity" — the natural source of a counterexample — does not obstruct. | proved here (§4); (a) uses an externally reported classical theorem, with the short proof included |
| T4 | Reformulation of the central case and a list of four invariants that **fail** (with reasons), §5. | proved here / failed attempts |

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

## 4. T3: a rigid example in which lifting nevertheless holds (proved here)

Let K = SL(2,3), realised as the 24 unit Hurwitz quaternions {±1, ±i, ±j, ±k, (±1±i±j±k)/2} ⊂ SU(2) = S³; z = −1; ω = (−1+i+j+k)/2 (order 3, trace −1). K has exactly the normal subgroups 1, ⟨z⟩, Q₈ = [K,K], K, and K/Q₈ ≅ C₃ is generated by the image of ω. Put

    G := ⟨K, t | [t,z] = 1⟩ = K ∗_{⟨z⟩} (⟨z⟩ × ⟨t⟩),   e: G → ℤ the t-exponent,   Q := G/⟨z⟩ ≅ A₄ ∗ ℤ.

z is central in G and z = [j,i] ∈ [G,G] (ji = −k, so [j,i] = j⁻¹i⁻¹ji = (ji)² = −1). The pairs (ω,t) and (zω,t) normally generate G (⟨⟨ω⟩⟩ ⊇ K and ⟨⟨zω⟩⟩ ⊇ K, see below) and have the same image in Q. G is infinite and not solvable; Q has rank 3 (Grushko), so no pair of Q generates it and H's Lemma 2.2 / Theorem 2(i) cannot be applied; N's correction modules for the central N = ⟨z⟩ are D₀ = D₁ = 0.

**Proposition 4.1 (one-coordinate rigidity; Gerstenhaber–Rothaus).** Let v ∈ G with e(v) ≠ 0.
1. There is a homomorphism ρ: G → SU(2) extending the inclusion K ⊂ SU(2) with ρ(v) = 1.
2. z ∉ ⟨⟨v⟩⟩, and for all u, u′ ∈ G: if u′ ∈ (u^{±1})^G·⟨⟨v⟩⟩ then tr ρ(u′) = tr ρ(u). In particular zω ∉ (ω^{±1})^G·⟨⟨v⟩⟩.
3. Hence: an AC path in G along which the normal closure of the second coordinate is constant, and is ⟨⟨v⟩⟩ with e(v) ≠ 0, cannot lead from a pair (ω, ·) to a pair (zω, ·). Also (z,1) ∉ Λ for the lattice Λ of Theorem 3.2 at (ω,t) (its first-coordinate generators need z ∈ ⟨⟨q⟩⟩ with e(q) ∈ {1, 1, −1} ≠ 0).

*Proof.* 1 (the classical degree argument of Gerstenhaber–Rothaus 1962, *externally reported*, proof included). For τ ∈ SU(2) let ρ_τ be the identity on K and ρ_τ(t) = τ; this is well defined since −1 is central in SU(2). Write v = k₀t^{n₁}k₁⋯t^{n_r}k_r; the map f_v: S³ → S³, τ ↦ ρ_τ(v) = k₀τ^{n₁}k₁⋯τ^{n_r}k_r is a pointwise product, in the group S³, of constant maps and of copies of id^{±1}. In [S³,S³] = π₃(S³) ≅ ℤ the pointwise product is addition (Eckmann–Hilton), constants are 0 and id^{±1} is ±1; so deg f_v = Σnᵢ = e(v) ≠ 0, f_v is surjective, and some τ₀ has f_v(τ₀) = 1. Take ρ = ρ_{τ₀}. 2: ρ kills ⟨⟨v⟩⟩ and ρ(z) = −1 ≠ 1. If u′ = g⁻¹u^{±1}g·w with w ∈ ⟨⟨v⟩⟩ then ρ(u′) is conjugate to ρ(u)^{±1}, and tr(A⁻¹) = tr(A) in SU(2). Finally tr ρ(zω) = −tr ω = 1 ≠ −1 = tr ρ(ω). 3: along such a path the first coordinate changes only by inversion, conjugation and multiplication by elements of ⟨⟨v⟩⟩, so its class in (·^{±1})^G⟨⟨v⟩⟩ is constant; the statement on Λ follows from 2 with v = t, st, st⁻¹. ∎

**Theorem 4.2.** In G: (ω,t) ~ (zω,t). Explicitly, with p := ω[t,i] = ω·t⁻¹i⁻¹ti,

    (ω,t) → (p,t) → (p, tj⁻¹) → (zω, tj⁻¹) → (zω,t).

*Proof.* Apply Corollary 2.2 with u = ω, c = i, κ = j: [κ,c] = [j,i] = z. It remains to check j ∈ ⟨⟨p⟩⟩ ∩ ⟨⟨zω⟩⟩; we show both normal closures contain K.
(i) By Lemma 2.3 with n = 4, i⁴ = 1: (iω)⁴ ∈ ⟨⟨p⟩⟩. Now iω = (−1−i−j+k)/2 has trace −1, hence order 3, so (iω)⁴ = iω ∈ ⟨⟨p⟩⟩. An element of K outside Q₈ has normal closure K in K. So K ⊆ ⟨⟨p⟩⟩.
(ii) zω ∈ K∖Q₈, so its normal closure in K is K.
The four arrows are the four steps of the proof of Lemma 2.1: the second uses j⁻¹ ∈ ⟨⟨p⟩⟩; for the third, modulo ⟨⟨tj⁻¹⟩⟩ one has t ≡ j and p ≡ ω[j,i] = zω, explicitly p·w = zω with w = (i⁻¹j⁻¹)·(tj⁻¹)⁻¹·(i⁻¹j⁻¹)⁻¹ · (i⁻¹j⁻¹i)·(tj⁻¹)·(i⁻¹j⁻¹i)⁻¹ ∈ ⟨⟨tj⁻¹⟩⟩; the fourth uses j ∈ ⟨⟨zω⟩⟩. ∎

**Corollary 4.3.** In this G the set E((ω,t)) of N2.4 is all of N² = ⟨z⟩² ((1,z) ∈ E because z ∈ K ⊆ ⟨⟨ω⟩⟩), although D₀ × D₁ = 0, the transfer lattice gives only 1 × ⟨z⟩, and no path with constant second normal closure reaches (z,1). The two-pair central lifting holds over this base; the mechanism is the substitution t ↦ tj⁻¹.

The same proof works verbatim for K = SL(2,5) ⊃ SL(2,3) (Q = A₅ ∗ ℤ; every non-central element of the quasisimple group K normally generates it), and — with Lemma 2.3 in its "cⁿ central" form — for torsion-free K such as π₁ of the Brieskorn sphere Σ(2,3,7) one still gets K ⊆ ⟨⟨s[t,a]⟩⟩ (a² = z, s = b: the relation forces (ab)² = z while (ab)⁷ = z^{±1}), but there z is not a single central commutator [κ,c] and I did not complete a chain of commutator transfers; see §6.
