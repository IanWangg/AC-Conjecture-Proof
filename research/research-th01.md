# Research TH01: the two-pair abelian lifting problem — a substitution principle, a transfer lattice, and a rigid example where lifting nevertheless holds

Date: 2026-11-09 (Los Angeles). Independent research agent TH01 (round 5, theory round).

**Status.** The two-pair abelian lifting problem of N §2.3–2.4 is **not settled in general** (neither proved nor refuted, not even for central N). **No AK(3) trivialization, no obstruction, no counterexample, nothing on the AC conjecture itself.** What is achieved, all *proved here* with complete proofs:

| # | statement | label |
|---|---|---|
| T1 | **Substitution Lemma.** For a pair (u,t) of any group G, any σ ∈ G and any W(X) in the normal closure of X in G∗⟨X⟩: if σ ∈ ⟨⟨u·W(t)⟩⟩ ∩ ⟨⟨u·W(σ)⟩⟩ then (u,t) ~ (u·W(σ), t). So a correction available "from t" can be traded for the same correction "from σ". This is a lifting mechanism that N's correction modules D₀ × D₁ do not see (it changes the base pair and returns). | proved here (§2) |
| T2 | **Transfer lattice.** For z central: (uz,v) ~ (u,v) if z ∈ [⟨⟨v⟩⟩,G]; (uz,v) ~ (u,vz) if z ∈ [⟨⟨uv⟩⟩,G]; (uz,v) ~ (u,vz⁻¹) if z ∈ [⟨⟨uv⁻¹⟩⟩,G]. Hence the central two-pair lifting **holds whenever the two normal closures commute** ([⟨⟨s⟩⟩,⟨⟨t⟩⟩] = 1, e.g. every pair (a,b) ∈ A × B, and all quotients of such), for arbitrary — infinite, non-solvable — A, B. The same transfer for a non-central abelian N (Theorem 3.5) gives the full two-pair abelian lifting when, in addition, one of the two normal closures centralizes N (Corollary 3.6). | proved here (§3) |
| T3 | **A rigid example where lifting still holds.** G = SL(2,3) ∗_{C₂} (C₂ × ℤ) = ⟨SL(2,3), t \| [t,z]⟩, z = −1 central, z ∈ [G,G], Q = G/⟨z⟩ = A₄ ∗ ℤ (infinite, not solvable, not 2-generated), pairs (ω,t) and (zω,t), ω of order 3. (a) N's correction modules vanish (D₀ = D₁ = 0), and for **every** v ∈ G with t-exponent ≠ 0 the element zω is not in (ω^{±1})^G·⟨⟨v⟩⟩ — no path that keeps the normal closure of the second coordinate fixed can remove z (Gerstenhaber–Rothaus degree argument); the transfer lattice of T2 does not contain (z,1) either. (b) Nevertheless **(ω,t) ~ (zω,t)** in G, by an explicit path of four composite moves found with T1 (replayed exactly by `experiments/th01_substitution.py`, 0 failures). So "one-coordinate rigidity" — the natural source of a counterexample — does not obstruct. Likewise for SL(2,5), SL(2,7), A₅, PSL(2,7) in place of SL(2,3): all pairs (u,t) with u non-central are AC-equivalent, although u ranges over 7, 7, 4, 4 conjugacy-and-inversion classes (Prop. 4.4, finite exact computation). | proved here (§4); (a) uses an externally reported classical theorem, with the short proof included |
| T4 | Over a quotient G of F with G_ab = ℤ², every central twist of a pair π(U) is its image under a central automorphism θ_n of G; the set of removable twists is a subgroup, and central two-pair lifting is exactly a chirality problem (in N's sense) for the group of central automorphisms (§5). Four candidate invariants that **fail**, with reasons, and one explicit torsion-free test group where neither T1–T2 nor any obstruction I know decides the question; within the family of paths used in T3 a solution there would need a "collapse" (an element of t-exponent 0 outside the vertex group whose normal closure contains a power of z), for which no source is visible (§6, F5–F6). | proved here / failed attempts / open |

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

**Lemma 2.1 (substitution).** Let (u,t) be a pair of G, σ ∈ G, W ∈ 𝒦.
(i) If σ ∈ ⟨⟨u·W(t)⟩⟩, then (u,t) ~ (u·W(σ), tσ⁻¹).
(ii) If σ ∈ ⟨⟨u·W(t)⟩⟩ ∩ ⟨⟨u·W(σ)⟩⟩, then (u,t) ~ (u·W(σ), t).

*Proof.* (1) W(t) ∈ ⟨⟨t⟩⟩, so (u,t) ~ (uW(t), t) by (M). (2) σ⁻¹ ∈ ⟨⟨uW(t)⟩⟩, so (uW(t), t) ~ (uW(t), t′) with t′ := tσ⁻¹, by (M). (3) In G/⟨⟨t′⟩⟩ the images of t and σ coincide, so the two homomorphisms G∗⟨X⟩ → G/⟨⟨t′⟩⟩ given by X ↦ t and X ↦ σ coincide; hence W(t)⁻¹W(σ) ∈ ⟨⟨t′⟩⟩ and (uW(t), t′) ~ (uW(σ), t′) by (M). This proves (i). (4) If also σ ∈ ⟨⟨uW(σ)⟩⟩, then (uW(σ), t′) ~ (uW(σ), t′σ) = (uW(σ), t). ∎

No hypothesis on normal generation is needed, and the lemma holds verbatim for k-tuples (σ may then be taken in the normal closure of all coordinates other than t). With W(X) = [X,c]:

**Corollary 2.2 (commutator transfer).** If κ ∈ ⟨⟨u[t,c]⟩⟩ ∩ ⟨⟨u[κ,c]⟩⟩, then (u,t) ~ (u[κ,c], t).

So the trivial rule "u may be multiplied by [t,c]" upgrades to "u may be multiplied by [κ,c]" for every κ that both u[t,c] and u[κ,c] normally generate. The first condition is the nontrivial one; the next lemma is a cheap way to get it.

**Lemma 2.3 (torsion collapse).** Let u, c, t ∈ G and suppose cⁿ = ζ with ζ commuting with t (e.g. cⁿ = 1, or ζ central). Then (cu)ⁿζ⁻¹ ∈ ⟨⟨u[t,c]⟩⟩.

*Proof.* Put p = u[t,c] = u·t⁻¹c⁻¹tc. Then c p c⁻¹ = c u t⁻¹c⁻¹t, so cu = (c p c⁻¹)·(t⁻¹ct). Modulo ⟨⟨p⟩⟩ this reads cu ≡ t⁻¹ct, hence (cu)ⁿ ≡ t⁻¹cⁿt = t⁻¹ζt = ζ. ∎

**Corollary 2.3′ (two-sided form).** Let σ, c, d ∈ G with [σ,d] = 1 and put z := [[c,σ],d] (central or not). If σ ∈ ⟨⟨s[t,c]⟩⟩ ∩ ⟨⟨sz[t,cd]⟩⟩, then (s,t) ~ (sz,t).
*Proof.* By 2.1(i) with W = [X,c], resp. W = [X,cd] at the pair (sz,t): (s,t) ~ (s[σ,c], tσ⁻¹) and (sz,t) ~ (sz[σ,cd], tσ⁻¹). With y := [σ,c]: [σ,cd] = [σ,d]·y^d = y^d and z = [y⁻¹,d] = y·d⁻¹y⁻¹d, so z·y^d = y and sz[σ,cd] = s[σ,c]. ∎

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

(If the cyclic groups S/[S,S] and T/[T,T] have coprime orders, st normally generates G and the statement is easy; the content is the case where no element of the class is forced to normally generate, e.g. G_ab ≅ ℤ².) This is the two-pair analogue of H's Lemma 2.2 in a situation where neither coordinate normally generates and G/⟨⟨t⟩⟩ ≅ S/(S∩T) is an arbitrary one-normal-generator group (the point where H's argument stops, N §2.3). It also shows that a counterexample to the central two-pair lifting cannot be found among direct (or central) products of two one-normal-generator groups, however wild the factors are.

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

For a generating pair, [N,G] is generated by the elements [m,s], [m,t] (m ∈ N) and (a) together with conjugation by N suffices (H Lemma 2.1); for a normally generating pair (b) is new: it moves an error between the coordinates through the Nielsen-adjacent pair (s, ts).

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
3. Hence: a swap-free AC path in G along which the normal closure of the second coordinate is constant, equal to ⟨⟨v⟩⟩ with e(v) ≠ 0, cannot lead from a pair (ω, ·) to a pair (zω, ·). (Every normally generating pair (u,v) of G has e(u) ≠ 0 or e(v) ≠ 0.) Also Λ = 1 × ⟨z⟩ for the lattice Λ of Theorem 3.2 at (ω,t), so (z,1) ∉ Λ: here Z(G) = ⟨z⟩, and a generator with nontrivial first coordinate would need z ∈ ⟨⟨q⟩⟩ for q = t, ωt or ωt⁻¹, which have e(q) = 1, 1, −1.

*Proof.* 1 (the classical degree argument of Gerstenhaber–Rothaus 1962, *externally reported*, proof included). For τ ∈ SU(2) let ρ_τ be the identity on K and ρ_τ(t) = τ; this is well defined since −1 is central in SU(2). Write v = k₀t^{n₁}k₁⋯t^{n_r}k_r; the map f_v: S³ → S³, τ ↦ ρ_τ(v) = k₀τ^{n₁}k₁⋯τ^{n_r}k_r is a pointwise product, in the group S³, of constant maps and of copies of id^{±1}. In [S³,S³] = π₃(S³) ≅ ℤ the pointwise product is addition (Eckmann–Hilton), constants are 0 and id^{±1} is ±1; so deg f_v = Σnᵢ = e(v) ≠ 0, f_v is surjective, and some τ₀ has f_v(τ₀) = 1. Take ρ = ρ_{τ₀}. 2: ρ kills ⟨⟨v⟩⟩ and ρ(z) = −1 ≠ 1. If u′ = g⁻¹u^{±1}g·w with w ∈ ⟨⟨v⟩⟩ then ρ(u′) is conjugate to ρ(u)^{±1}, and tr(A⁻¹) = tr(A) in SU(2). Finally tr ρ(zω) = −tr ω = 1 ≠ −1 = tr ρ(ω). 3: along such a path the first coordinate changes only by inversion, conjugation and multiplication by elements of ⟨⟨v⟩⟩, so its class in (·^{±1})^G⟨⟨v⟩⟩ is constant; the statement on Λ follows from 2 with v = t, st, st⁻¹. ∎

**Theorem 4.2.** In G: (ω,t) ~ (zω,t). Explicitly, with p := ω[t,i] = ω·t⁻¹i⁻¹ti,

    (ω,t) → (p,t) → (p, tj⁻¹) → (zω, tj⁻¹) → (zω,t).

*Proof.* Apply Corollary 2.2 with u = ω, c = i, κ = j: [κ,c] = [j,i] = z. It remains to check j ∈ ⟨⟨p⟩⟩ ∩ ⟨⟨zω⟩⟩; we show both normal closures contain K.
(i) By Lemma 2.3 with n = 4, i⁴ = 1: (iω)⁴ ∈ ⟨⟨p⟩⟩. Now iω = (−1−i−j+k)/2 has trace −1, hence order 3, so (iω)⁴ = iω ∈ ⟨⟨p⟩⟩. An element of K outside Q₈ has normal closure K in K. So K ⊆ ⟨⟨p⟩⟩.
(ii) zω ∈ K∖Q₈, so its normal closure in K is K.
The four arrows are the four steps of the proof of Lemma 2.1: the second uses j⁻¹ ∈ ⟨⟨p⟩⟩; for the third, modulo ⟨⟨tj⁻¹⟩⟩ one has t ≡ j and p ≡ ω[j,i] = zω, explicitly p·w = zω with w = (i⁻¹j⁻¹)·(tj⁻¹)⁻¹·(i⁻¹j⁻¹)⁻¹ · (i⁻¹j⁻¹i)·(tj⁻¹)·(i⁻¹j⁻¹i)⁻¹ ∈ ⟨⟨tj⁻¹⟩⟩; the fourth uses j ∈ ⟨⟨zω⟩⟩. ∎

**Corollary 4.3.** In this G the set E((ω,t)) of N2.4 is all of N² = ⟨z⟩² ((1,z) ∈ E because z ∈ K ⊆ ⟨⟨ω⟩⟩), although D₀ × D₁ = 0, the transfer lattice gives only 1 × ⟨z⟩, and no path with constant second normal closure reaches (z,1). The two-pair central lifting holds over this base; the mechanism is the substitution t ↦ tj⁻¹.

**Proposition 4.4 (all slices merge; proved here, with a finite exact computation).** Let K be SL(2,5) or SL(2,7), z = −1 and G_K = ⟨K, t | [t,z]⟩; or let K be A₅ = PSL(2,5) or PSL(2,7) and G_K = K ∗ ⟨t⟩. Then **all pairs (u,t), u ∈ K non-central, are AC-equivalent in G_K**; in particular (u,t) ~ (zu,t) for every such u in the first two cases. Under conjugacy and inversion alone the non-central elements of K form 7, 7, 4, 4 classes respectively, and for K = SL(2,5) ⊂ SU(2) the argument of Proposition 4.1 shows that elements with different traces (all 7 classes have different traces) are never related by a path of the kind described in Proposition 4.1(3).
*Proof.* K is quasisimple, so a non-central element of K has normal closure K in K. For u, κ, c ∈ K with (cu)^{o(c)} and u[κ,c] non-central, Lemma 2.3 gives K ⊆ ⟨⟨u[t,c]⟩⟩ and trivially K ⊆ ⟨⟨u[κ,c]⟩⟩, so (u,t) ~ (u[κ,c],t) by Corollary 2.2. The graph on the non-central elements with these edges, together with conjugation and inversion, is connected in all four cases (`th01_substitution.py --sl25`, `--sl27`: (7,1), (4,1), (7,1), (4,1) = classes before, components after). ∎

The proof of 4.2 also works verbatim for K = SL(2,5) ⊃ SL(2,3) (Q = A₅ ∗ ℤ; every non-central element of the quasisimple group K normally generates it), and — with Lemma 2.3 in its "cⁿ central" form — for torsion-free K such as π₁ of the Brieskorn sphere Σ(2,3,7) = ⟨a,b,z | z central, a², b³, (ab)⁷ ∈ ⟨z⟩, …⟩ one still gets K ⊆ ⟨⟨s[t,a]⟩⟩ for s = b (sketch: modulo ⟨⟨s[t,a]⟩⟩ the element (ab)² becomes a power of z, and (ab)⁷ is one already, so ab becomes central and the perfect group K dies); but there z is not a single commutator [κ,c] of elements commuting modulo z, and I did not complete a chain of commutator transfers; see §6.

## 5. T4: the central case as a chirality problem for central automorphisms (proved here)

**Proposition 5.1.** Let N ≤ Z(G) ∩ [G,G] and φ ∈ Hom(G,N) (so φ kills [G,G] ⊇ N). Then θ_φ: g ↦ g·φ(g) is an automorphism of G (inverse θ_{φ⁻¹}) inducing the identity on G/N and on N, θ_φθ_ψ = θ_{φψ}, and θ_φ(u,v) = (uφ(u), vφ(v)). Consequently:
1. For every pair P of G, E_aut(P) := {φ : θ_φ(P) ~ P} is a **subgroup** of Hom(G,N) (the stabilizer of the AC class of P; automorphisms preserve ~).
2. If G_ab is free abelian on the images of the coordinates of P — e.g. G = F/K with K ⊆ [F,F] and P = π(U) for a normally generating pair U of F — then every central twist P·(n₀,n₁) is θ_φ(P) for the unique φ with φ(u) = n₀, φ(v) = n₁. So E(P) of N2.4 is a subgroup of N², and "P·n ~ P" says that the central automorphism θ_n fixes the class of P.
3. In that situation every θ_n fixes the standard class (H Lemma 2.2). Hence over such G **the two-pair central lifting problem is exactly a chirality problem in the sense of N2.1**, for the abelian group Hom(G,N) ≅ N² of central automorphisms instead of GL₂(ℤ): is the class of π(U) fixed by all θ_n? (These θ_n need not be induced from Aut(F).)

*Proof.* θ_φ(gh) = gh·φ(g)φ(h) = gφ(g)·hφ(h) because φ(g) is central; θ_φ(θ_ψ(g)) = gψ(g)·φ(g)φ(ψ(g)) = g·φ(g)ψ(g) since φ(N) = 1. The rest is immediate. ∎

**Remark 5.2 (logical status; proved here, trivial).** If the AC conjecture holds in rank 2, then any two normally generating pairs U, V of F are AC-equivalent in F, hence π(U) ~ π(V) in every quotient: for pairs *coming from F* the two-pair lifting property (through any normal subgroup) is a consequence of the AC conjecture, and a single failure would disprove it. The lifting problem is independent of the conjecture only for normally generating pairs of G that are not of the form π(U) with π: F(x,y) → G onto and U normally generating F(x,y) — as in §4 and in Test case 6.1 below, where G is normally generated by two elements but needs three generators.

So a counterexample to central two-pair lifting over a quotient of F with ℤ²-abelianization would be a "central chirality": a class of pairs moved by a central automorphism that fixes the standard class. Theorems 3.2/3.3 and Lemma 2.1 are then lower bounds on the stabilizer E(P), exactly as N's certificates are lower bounds on Ŝ(C4). In §4 the twist (z,1) is *not* automorphic (ω has order 3, zω order 6), which is why a trace argument gives rigidity there.

## 6. Failed attempts, and the sharpest open test case

**(F1) A Gerstenhaber–Rothaus invariant (failed; reason proved).** For G = ⟨K,t | [t,z]⟩ with K ⊂ SU(2) I tried J(p,q) := {tr ρ_τ(p) : ρ_τ(q) = 1} for the "normal form" (e(p), e(q)) = (0, ±1) of a pair. J is nonempty (Prop. 4.1), invariant under all moves on p, and under conjugation/inversion of q, and J(zp,q) = −J(p,q). It is **not** invariant under q ↦ q·w′, w′ ∈ ⟨⟨p⟩⟩: Theorem 4.2 is a counterexample (J(p,t) = {−1}, J(p,tj⁻¹) = {+1} for p = ω[t,i]). So no invariant of the form "conjugacy data of one coordinate modulo the other" survives the substitution t ↦ tσ⁻¹.

**(F2) Homotopy/linking invariants of the word maps (failed; sketch).** The pair of word maps (û,v̂): S³ → S³×S³ avoids the four points (±1,±1); S³×S³ minus points is 2-connected with π₃ = ℤ², so the homotopy class is only (e(u),e(v)). The 5-cycle swept by the conjugacy classes of û(τ) links the punctures (1,1), (−1,1) with numbers (ℓ,−ℓ); u ↦ zu and u ↦ u⁻¹ both change the sign of ℓ, so only |ℓ| could be invariant and it does not see z.

**(F3) The relative homotopy type (failed).** For Q = G/N and X = K(Q,1) ∪ e²_s ∪ e²_t (simply connected), lifts of (s,t) to a central extension correspond to extensions to X of the extension class, and self-equivalences of X rel K(Q,1) act transitively on them (slide a 2-cell over a spherical class of H₂(Q) ⊂ π₂(X)). So nothing of the pair (X, K(Q,1)) up to homotopy can obstruct; AC moves realize only slides over classes supported on the *other* cell, which is the whole difficulty. (This is the two-pair, relative form of N1; sketch, not used elsewhere.)

**(F4) A general proof of the central case (failed).** Writing [G,G] = [S,S]·[T,G], a central z₀ on the first coordinate reduces to its [S,S]-part; Theorem 3.2 removes it when it lies in [R₊,G]∩[S,G] and Lemma 2.1 when a suitable (W,σ) exists. I could not produce (W,σ) in general: the first condition σ ∈ ⟨⟨s·W(t)⟩⟩ is a "collapse" statement about a one-relator quotient, and it genuinely fails in torsion-free situations (next item).

**Test case 6.1 (open; the sharpest instance I know).** Let Ã = Heis(ℤ) ⋊_M ⟨s⟩ with M = [[2,1],[1,1]] acting on Heis(ℤ) = ⟨a,b | z = [a,b] central⟩ through any lift of M; Ã_ab = ℤ (det(M−I) = −1), so Ã = ⟨⟨s⟩⟩, and z ∈ Z(Ã) ∩ [Ã,Ã]. Put G = ⟨Ã, t | [t,z]⟩ = Ã ∗_{⟨z⟩} ℤ², torsion-free, Q = G/⟨z⟩ = (ℤ² ⋊_M ℤ) ∗ ℤ. *Question: is (sz,t) ~ (s,t) in G?* Facts (proved here unless marked): (i) (s,tzʲ) ~ (s,t) for all j, and (sz,t) = θ(s,t) for the central automorphism θ: s ↦ sz, t ↦ t, a ↦ a, b ↦ b; so E = dℤ × ℤ for some d ≥ 0 and the question is whether d = 1. (ii) d = 1 in G/⟨⟨[t,Ã]⟩⟩ = Ã × ℤ (Theorem 3.3), in G/⟨⟨[t,a],[t,b]⟩⟩ = Heis ⋊ F(s,t) (there z = [ta,b] ∈ ⟨⟨ta⟩⟩, so (s,t) → (s,ta) → (sz,ta) → (sz,t)), and in every finite or solvable quotient of G (BLM, Guyot). (iii) sz is not conjugate to s^{±1} in Ã = G/⟨⟨t⟩⟩ ([s,h] is central only if h is). (iv) Commutator transfer with c ∈ Ã fails: for c ∈ Ã with c, cs ∉ ⟨z⟩ the group G/⟨⟨s[t,c]⟩⟩ = ⟨Ã,t | [t,z], t⁻¹ct = cs⟩ is an HNN extension of Ã (⟨c,z⟩ ≅ ⟨cs,z⟩ ≅ ℤ², because Ã is torsion-free and a power of a non-central element is never central), so no nontrivial element of Ã lies in ⟨⟨s[t,c]⟩⟩; for c ∈ ⟨z⟩ or cs ∈ ⟨z⟩ the element s[t,c] is conjugate to s and the transfer is trivial. (v) z ∉ ⟨⟨v⟩⟩ for every v with e(v) ≠ 0 (*proved here modulo the externally reported Gerstenhaber–Rothaus degree lemma*): Ã is polycyclic, hence residually finite; take a finite quotient Ā in which z survives and an irreducible unitary representation ψ: Ā → U(n) with ψ(z) = λ·I, λ ≠ 1 (Schur); for τ ∈ U(n) let ρ_τ = ψ on Ã and ρ_τ(t) = τ (well defined, λ·I is central); the map τ ↦ ρ_τ(v) on U(n) is homotopic to τ ↦ τ^{e(v)}, which has degree e(v)ⁿ ≠ 0 (Gerstenhaber–Rothaus; Hopf), so it is onto and some ρ_τ kills v but not z. A proof of d ≠ 1 would be a genuine pair-separating invariant in an infinite group (as hard, I believe, as a disproof of a generalized AC statement: G is residually solvable, so by Guyot it would have to be an unbounded-distance phenomenon along solvable quotients); a proof of d = 1 needs a mechanism beyond Lemma 2.1 with σ ∈ Ã.

**(F5) Why Lemma 2.1 does not settle Test case 6.1 (partial analysis, proved as far as stated).** In Corollary 2.3′ the element σ must commute with d while [[c,σ],d] = z ≠ 1. In G = Ã ∗_{⟨z⟩} ℤ² an element not conjugate into a factor has centralizer mapping to a cyclic subgroup of Q, which forces [[c,σ],d] = 1 (two elements of G whose images lie in a common cyclic subgroup of Q commute); the same happens for σ conjugate into ⟨z,t⟩. So σ must be conjugate into Ã, σ = σ₁^g with σ₁ ∈ Heis(ℤ)∖⟨z⟩, and then c = c₁^g, d = d₁^g with c₁ ∈ Ã, d₁ ∈ Heis(ℤ)∖⟨z⟩ (distinct conjugates of Ã meet in ⟨z⟩). For g ∈ Ã at least one of the two membership conditions fails, by 6.1(iv) applied to s[t,c] and, with sz in place of s, to sz[t,cd] (the exceptional cases c ∈ ⟨z⟩s⁻¹ and cd ∈ ⟨z⟩s⁻¹ cannot hold together because d ∉ ⟨z⟩, and c ∈ ⟨z⟩ or cd ∈ ⟨z⟩ gives [c,σ] = 1). For g involving t they are statements about the one-relator-type quotients G/⟨⟨s[t,c₁^g]⟩⟩, for which I have neither a collapse nor a Freiheitssatz.

**(F6) What any solution of Test case 6.1 must contain, within one natural family of paths (proved here).** Every normal generator of Ã is conjugate in Ã to exactly one (sz^k)^{±1}, k ∈ ℤ (twisted conjugacy: det(M−I) = ±1 removes the non-central part, and the central part cannot be changed); and every nontrivial normal subgroup of Ã contains some z^k, k ≥ 1 (it meets Heis(ℤ), hence its centre). For α ∈ Ã let ρ_α: G → Ã be the retraction t ↦ α; then G/⟨⟨tα⁻¹⟩⟩ = Ã via ρ_α. Consider paths through pairs (p, tα⁻¹), α ∈ Ã, with the two kinds of steps "p ↦ p′ ∈ (p^{±1})^G⟨⟨tα⁻¹⟩⟩" and "α ↦ α′ with αα′⁻¹ ∈ ⟨⟨p⟩⟩" (the steps used in §4). The class κ ∈ ℤ of ρ_α(p) is unchanged by a step of the first kind, by a step of the second kind when ⟨⟨p⟩⟩ ∩ Ã = 1 (then α′ = α), and by a step of the second kind when p is conjugate into Ã (p = h^g with h ∈ Ã; then ρ_α(p) is conjugate in Ã to h for every α). Hence **such a path from (s,t) to (sz,t) must pass through an element p, not conjugate into Ã, whose normal closure contains z^k for some k ≥ 1** (necessarily e(p) = 0, by the argument of 6.1(v) applied to z^k in a finite quotient where z has order > k) — a collapse of the kind Lemma 2.3 produces from torsion, for which no source is visible in the torsion-free group G. General paths (second coordinates not of the form tα⁻¹) are not covered.

## 7. Experiments (exact; light support only)

`experiments/th01_substitution.py` (Python standard library; each mode ≤ 8 s on one core; < 40 MB). It implements G = SL(2,3) ∗_{⟨z⟩} (⟨z⟩ × ℤ) with the amalgam normal form (K = 24 Hurwitz units with doubled integer coordinates), expands the four composite moves of Theorem 4.2 into elementary AC moves (invert; multiply one coordinate by the other; conjugate one coordinate by a generator i, ω, t or an inverse), and checks the endpoint. The membership statements j⁻¹ ∈ ⟨⟨p⟩⟩ and j ∈ ⟨⟨zω⟩⟩ are made explicit: iω = ∏_{m=0..3} γ^m(i p i⁻¹)γ^{−m} with γ = t⁻¹it (Lemma 2.3), and products of conjugates inside K found by breadth-first search.

```
$ PYTHONDONTWRITEBYTECODE=1 python3 experiments/th01_substitution.py --selftest
selftest passed: |K|=24, normal form checks (3000 random triples), Lemma 2.3 identity, replay of 106 moves, S4 identities for Lemma 3.4 / Theorem 3.5(b)
$ PYTHONDONTWRITEBYTECODE=1 python3 experiments/th01_substitution.py --replay
start (omega, t); end == (z*omega, t): True | elementary moves: 106 {'invert': 14, 'multiply': 14, 'conjugate': 78}
$ PYTHONDONTWRITEBYTECODE=1 python3 experiments/th01_substitution.py --sl25        # Proposition 4.4, < 1 s
SL(2,5): slice classes, components after commutator transfer: (7, 1)
PSL(2,5)=A5 (free product A5*Z): (4, 1)
$ PYTHONDONTWRITEBYTECODE=1 python3 experiments/th01_substitution.py --sl27        # Proposition 4.4, about 8 s
SL(2,7): slice classes, components after commutator transfer: (7, 1)
PSL(2,7) (free product PSL(2,7)*Z): (4, 1)
```

The `--sl25`/`--sl27` modes also assert that every non-central element of SL(2,5), SL(2,7) normally generates the group. The self-test also checks: K's normal closures (every element outside Q₈ normally generates K), associativity/inverses/centrality of z on random elements, [j,i] = z, (iω)³ = 1, the identity cu = (cpc⁻¹)(t⁻¹ct) of Lemma 2.3, that the logged elementary moves alone reproduce the endpoint, and the two identities behind Lemma 3.4 and Theorem 3.5(b) on 2000 random instances in S₄ with N = V₄. The replay uses only sound rewriting (merging central letters, moving signs), so the endpoint equality is an identity in G independently of the uniqueness of normal forms. No `ordinary-ac-elementary-v1` certificate is produced: nothing here is an AC equivalence in F(x,y), and the repository verifier does not apply to pairs in G. Controls in the sense of the brief (AK(1), AK(2), the repository certificates) are not applicable: no AC invariant is claimed.

## 8. Honest limits

- The seed problem is **open**. I proved the two-pair lifting only in classes (commuting normal closures, plus the centralizing hypothesis in the non-central case) and in examples; I did not find a counterexample, and I do not have a proof for central N in general.
- The example of §4 lives over Q = A₄ ∗ ℤ, which has rank 3: it is a quotient of F₃, not of F₂. It answers N's question "can E(P′) exceed D₀ × D₁ and the fixed-normal-closure corrections?" (yes), but it is not an instance inside a quotient of F(x,y). I could not build a 2-generated group with the same provable one-coordinate rigidity (imposing a relation that makes ⟨K,t⟩ 2-generated cuts the SU(2)-representation variety down and destroys the degree argument).
- Proposition 4.4 depends on a finite computation (union–find on the non-central elements of K over the edges of Corollary 2.2 with Lemma 2.3); it is exact but was not cross-checked by a second program. I have no computation-free proof that the slices merge for every finite quasisimple K.
- Proposition 4.1 quotes the Gerstenhaber–Rothaus degree argument from memory and reproves it for SU(2); the facts used (pointwise product = sum in π₃(S³); a non-surjective self-map of S³ has degree 0) are standard.
- §6 (F2), (F3) and the Σ(2,3,7) remark at the end of §4 are sketches, labelled as such. The statements about Test case 6.1 use Britton's lemma, the structure of centralizers in amalgams (standard) and, for (v), the degree of the power map on U(n) (externally reported).
- Nothing here bears directly on AK(3): its class is Aut-closed and it is compared with the *generating* standard pair, where H's Theorem 2(i) already gives the lifting.
- Novelty is not established. Lemma 2.1 is a three-line argument and is likely known in some form to people working on Nielsen/AC equivalence in free products; I could not search the literature (arXiv blocked).

## 9. Advice to the coordinator (ranked)

1. **Treat the two-pair central lifting as a chirality problem for central automorphisms (Prop. 5.1), and stop looking for a counterexample through "one coordinate fixed" rigidity.** Theorem 4.2 shows that rigidity of every slice (even with a Kervaire-type theorem behind it) says nothing: the substitution t ↦ tσ⁻¹ couples the slices. Any future candidate obstruction should first be tested against Lemma 2.1/Corollary 2.3′.
2. **One sharp, self-contained problem for a future theory agent: Test case 6.1** (G = (Heis(ℤ) ⋊_M ℤ) ∗_{⟨z⟩} ℤ², is (sz,t) ~ (s,t)?). It is torsion-free, residually solvable, has d = 1 in every finite or solvable quotient (BLM, Guyot) and shows no collapse of the kind used in §4. A positive answer needs a new mechanism (and would suggest the lifting is always true); a negative answer would be the first pair-separating invariant, of unbounded-distance type along the derived series. A cheap first step is computational: enumerate short c₁, g and test whether a ∈ ⟨⟨s[t,c₁^g]⟩⟩ in nilpotent-by-finite quotients (a negative answer in one finite quotient kills a candidate path; a positive answer in all small quotients suggests a collapse to prove).
3. **Use Theorems 3.2/3.5 as cheap lower bounds on E(P′) whenever a quotient-type invariant is proposed** (N §2.4–2.5): the lattice Λ only needs normal closures of the Nielsen-adjacent elements s, t, st, st⁻¹ (and further primitives), which are computable in finite quotients; an invariant must vanish on Λ.
4. **Rank 2.** By Remark 5.2, for pairs coming from F(x,y) any failure of two-pair lifting is an AC counterexample, so the part of the lifting problem that is independent of the conjecture lives on pairs that do not come from F (as in §4, 6.1). To bring §4 into quotients of F(x,y) one needs a 2-generated base in which some class of pairs is provably not the standard one — which is the original difficulty. I do not recommend spending an agent on this before item 2 is understood.
5. H's and N's notes should cross-reference: N §2.3's sentence "the corrections available without changing the base pair are exactly D₀ × D₁" is correct but, by §4 here, the set E(P′) can be strictly larger.

## 10. Files

- `research/research-th01.md` (this note).
- `experiments/th01_substitution.py` — exact replay of Theorem 4.2 in SL(2,3) ∗_{C₂} (C₂ × ℤ) and the finite computations of Proposition 4.4; `--selftest`, `--replay`, `--sl25`, `--sl27`.
- No certificates: no AC equivalence in F(x,y) is claimed.

## References

- Research notes H (Lemma 2.1, Lemma 2.2, Theorem 2, coordinator's review) and N (§2.1–2.5) of this repository.
- M. Gerstenhaber, O. S. Rothaus, *The solution of sets of equations in groups*, Proc. Nat. Acad. Sci. USA 48 (1962) 1531–1533 (externally reported; degree argument reproduced for SU(2)).
- A. V. Borovik, A. Lubotzky, A. G. Myasnikov, *The finitary Andrews–Curtis conjecture*, arXiv:1103.1295; L. Guyot, *On Andrews–Curtis conjectures for soluble groups*, arXiv:1612.06912 (externally reported, via B/E/H/N).
- J. L. Britton (1963), normal form for HNN extensions; normal form theorem for amalgamated free products (classical; Lyndon–Schupp, *Combinatorial Group Theory*, Ch. IV).
- A. A. Klyachko (1993), S. D. Brodskii (1984), J. Howie (1981–82) on equations over torsion-free / locally indicable groups (mentioned only as context in §6; not used in any proof).

## Coordinator's check (2026-11-09, Los Angeles time)

- Re-ran `python3 experiments/th01_substitution.py` with `--selftest`, `--replay`, `--sl25`, `--sl27`: all pass (the explicit path of Theorem 4.2 replays in 106 elementary moves in the finite model).
- Re-derived by hand: the Substitution Lemma 2.1 (four applications of "multiply a coordinate by an element of the normal closure of the other") and Corollary 2.2. Correct.
- Read but not re-derived: Lemma 2.3, the transfer-lattice results of §3 (Proposition 3.1, Theorems 3.2, 3.3, 3.5) and the example of §4, including its use of the externally reported Gerstenhaber–Rothaus theorem; the agent reports that the referee (research-th19.md) marks the main ones verified — see that note.
- Status, stated plainly: the two-pair abelian lifting problem of research-n §2.3 remains **open**, even for central subgroups. All examples in this note live over bases of rank 3 and are not quotients of F(x,y). For a *single* presentation compared with the standard pair, the corresponding lifting statement is now a theorem (research-th05, research-th08); the open problem concerns two arbitrary normally generating pairs.
