# Research TH13: the two-parameter Akbulut–Kirby family AK(k;p) — duality, plateau depth, exits

Date: 2026-11-09 (Los Angeles). Independent research agent TH13 (round 5, theory round).

**Status.** Partial results, all with complete proofs or replayed certificates. **No AC trivialization of AK(3), no proof that AK(3) is not AC-trivial, no proof or disproof of the AC conjecture.** Everything concerns ordinary (unstabilized) AC equivalence. No novelty is claimed (literature access was not available).

Notation: X = x⁻¹, Y = y⁻¹, and for k, p ≥ 1

    W_k = (xy)^k x · Y(XY)^k        (the relation (xy)^k x = y(xy)^k; length 4k+2; W_1 = b = xyxYXY)
    p_p = x^p Y^(p+1),  q_p = y^p X^(p+1)
    AK(k;p) = (p_p, W_k)            (total length 2p+4k+3;  AK(1;p) = AK(p))
    V_{k,p} = (y^k x)^p y^k · ((x y^k)^p x)⁻¹     (the relation (x y^k)^p x = y^k (x y^k)^p; length (2p+1)(k+1))
    D(k;p) = (V_{k,p}, x² Y^(2k+1))  =  ⟨x,y | x² = y^(2k+1), (x y^k)^p x = y^k (x y^k)^p⟩.

**Central claims (labels: P = proved here, C = certificate replayed, X = experiment).**

| # | statement | label |
|---|---|---|
| T1 | AK(k;p) presents the trivial group for all k, p ≥ 1. More generally F(a,b;i,j;m) = ⟨x,y \| x^a = y^b, (x^i y^j)^m x^i = y^j (x^i y^j)^m⟩ is trivial iff \|bi − aj\| = 1, and for fixed (a,b,m) all admissible (i,j) give AC-equivalent presentations | P (§2) |
| T2 | **Duality.** For all k, p ≥ 1: AK(k;p) ~AC (ψ_k(V_{k,p}), W_k) by one W_k-frozen ACM move, where ψ_k = (x ↦ x(xy)^k, y ↦ xy); hence ψ_k⁻¹(AK(k;p)) ~AC D(k;p). For k = 1 this is G's Theorem G1. So "torus T(p,p+1) relation + Artin relation of length 2k+1 in (x,y)" = "torus T(2,2k+1) relation + Artin relation of length 2p+1 in (x, y^k)" | P (§3) + C for (k,p) = (2,2), (2,3), (3,3) |
| T3 | The column p = 2 is the AK series again: AK(k;2) is, up to an automorphism, AC-equivalent to AK(k). So AK(2;2) is AC-trivial (certificate), and **AK(3) ~AC AK(3;2) = (xxYYY, xyxyxyxYXYXYXY)**, i.e. AK(3) ~AC ⟨x,y \| x² = y³, (xy)³x = y(xy)³⟩ by plain AC moves (certificate, 2,522 moves, using D6). The row p = 1 is AC-trivial (primitive relator; certificates k = 2, 3) | P (from G1, D2, D3, D6) + C |
| T4 | **Plateau of unbounded depth.** For k ≥ 1, p ≥ 3: every ACM path from AK(k;p) with non-increasing total cyclic length stays on (Orb(p_p) ∪ Orb(q_p)) × Orb(W_k), and the first state off this plateau has total cyclic length ≥ 2p+4k+3 + min(4k−2, 2k+2, 2p−4). Hence every AC trivialization of AK(k;p), if one exists, passes through cyclic length ≥ that number; e.g. ≥ initial + 2k+2 for p ≥ k+3 ≥ 6. For k = 1 this is A's theorem with J's bound 2n+9 | P (§4) + X (exact brute force for small k, p) |
| T5 | For p ≥ 2 and (k,p) ≠ (1,2), no pair with a primitive relator is one ACM move from AK(k;p) (arbitrary conjugators, Aut(F₂) free); both meridian defects are > 2, so Prop. M / thickenability exits do not apply either | P modulo the classical Fact C of research-g (§5) + X (exact test k ≤ 6, p ≤ 7) |
| T6 | **Aut(F₂) is AC-realized on AK(2;3) and on AK(2;4)**: θ(AK(2;p)) ~AC AK(2;p) for every θ ∈ Aut(F₂), p = 3, 4 (certificates for the transvection x ↦ xy and the swap; these generate Out(F₂)); an explicit certificate AK(2;3) → mirror image (XXXYYYY, XyXyXYxYxY) has 2,349 moves and cyclic peak 44. Yet the mirror image of AK(2;3) is *not* found by complete forward searches to cap 31 (two-sided) / 34 (one-sided): a calibration for bounded "automorphic image not found" observations (cf. the C4 question in I, M, N): an individual stabilizer element can be invisible at start + 17 in a class whose stabilizer is everything | P by C (§6) + X |
| T7 | For k ≥ 2 the partner V_{k,p} in D(k;p) is the T(2,2p+1) Wirtinger word on the generating pair (x, y^k), which is not the image of any basis of F₂ (commutator-necklace argument) — the structural reason the k = 1 role swap into a second torus pair does not persist. Experiment: within G's torus-graph bounds AK(k;p) is an isolated torus node for k ≥ 2, p ≥ 3, while AK(k;2) and AK(1;p) have 3-orbit islands | P (Lemma 7) + X (§7) |
| X8 | Directed cyclic-product forward sets (D's engine, complete to its maximal cap 31): AK(2;3) 805,962 states, AK(2;4) 10,400, AK(3;3) 65,530 — no primitive relator, no state shorter than the start. Bounded search, **not** evidence of non-triviality | X (§8) |

**Open after this note:** AC-triviality of every AK(k;p) with k ≥ 2, p ≥ 3 (smallest: AK(2;3) = (xxxYYYY, xyxyxYXYXY), length 17) and of AK(k;2) ≅ AK(k), k ≥ 3.

## 1. Previous work read and choice of direction

Read: `README.md` in full; A in full; G §1–3 in full; J §4; I §2–3; K §3; status paragraphs and coordinator reviews of the other notes. Used and re-verified here: G's Lemma 1 (conjugacy in torus groups = syllable necklace + central exponent), Lemma G0 (ACM moves are AC composites, compiled by `g_cert.acm_edge`), G1, G2, Fact C; J's Lemma J0; A's two lemmas; D2 (AC-triviality is Aut(F₂)-invariant), D3 (primitive relator ⇒ AC-trivial).

Direction: the seed family AK(k;p) = (x^p y^-(p+1), W_k). Why it is worth a note: G1 shows that AK(n) hides a second torus knot T(2,2n+1); the family makes both knots T(p,p+1) and T(2,2k+1) free parameters, so one can see which of the AK(n) phenomena (role swap, plateau, absence of exits) are general and which are accidents of k = 1. The answers: the plateau and the absence of one-move exits are general and get *stronger* with k (T4, T5); the role swap persists only as torus ↔ Artin-on-a-non-standard-generating-pair (T2, T7); the AK series itself sits in the family twice (row k = 1, column p = 2; T3); and the first genuinely new members AK(2;3), AK(2;4) already have all of Aut(F₂) AC-realized although bounded searches do not see their mirror images (T6). This is new relative to A–O, which treat only k = 1. Overlap check with the other round-5 seeds: TH04 classifies torus words in the partner classes of AK(n) itself (k = 1), TH07 studies paths beyond A's plateau for AK(n); here both questions are asked for general k, where the answers differ.

## 2. Triviality, and the three-parameter family behind AK(k;p) (proved)

For integers a, b, i, j and m ≥ 0 let A_m(α,β) = (αβ)^m α · ((βα)^m β)⁻¹ and F(a,b;i,j;m) = (x^a y^-b, A_m(x^i, y^j)). So AK(k;p) = F(p,p+1;1,1;k) and D(k;p) = F(2,2k+1;1,k;p) up to inverting and rotating relators.

**Theorem 1.** (a) F(a,b;i,j;m) presents the trivial group iff |bi − aj| = 1. In particular AK(k;p) and D(k;p) do.
(b) Let |a|,|b| ≥ 2 and bi − aj = ±1, bi′ − aj′ = ±1. Then A_m(x^i′, y^j′) is conjugate to A_m(x^i, y^j)^{±1} in ⟨x,y | x^a = y^b⟩; hence F(a,b;i,j;m) ~AC F(a,b;i′,j′;m) by one ACM move.

*Proof.* (a) The exponent-sum matrix has rows (a, −b) and (i, −j), determinant bi − aj, so the condition is necessary. Conversely let z = x^a = y^b (central), α = x^i, β = y^j, Δ = (αβ)^m α. The second relation says Δ = β(αβ)^m, so βΔ = β(αβ)^m α = Δα, i.e. y^j = Δ x^i Δ⁻¹. Then y^(ja) = Δ x^(ia) Δ⁻¹ = Δ z^i Δ⁻¹ = z^i = y^(bi), so y^(bi−aj) = 1 and y = 1. Now x^a = 1 and x^i = Δ⁻¹ y^j Δ = 1 with gcd(a,i) = 1, so x = 1.
(b) The solutions of bi − aj = 1 are (i,j) + l(a,b). In T = ⟨x,y | x^a = y^b⟩, x^(i+la) = x^i z^l and y^(j+lb) = y^j z^l with z central; replacing (α,β) by (αz^l, βz^l) multiplies both (αβ)^m α and (βα)^m β by z^(l(2m+1)), so A_m is unchanged as an element of T. The solutions of bi − aj = −1 are the negatives, and A_m(α⁻¹,β⁻¹) = (α⁻¹β⁻¹)^m α⁻¹ · β(αβ)^m is a cyclic rotation of ((βα)^m β)·((αβ)^m α)⁻¹ = A_m(α,β)⁻¹ (free identity). ∎

Direct check for AK(k;p): the exponent matrix is (p, −(p+1); 1, −1), determinant 1; Δ_k = (xy)^k x conjugates x to y, x^p = y^(p+1) is central, so y^p = x^p = y^(p+1) and y = 1 = x. Coset enumeration (`f_descent.is_trivial_group`) confirms k ≤ 4, p ≤ 5 and several F(a,b;i,j;m) (self-test).

## 3. Duality (proved; certificates)

**Lemma 2 (coordinates in which W_k is a torus relator).** ψ_k = (x ↦ x(xy)^k, y ↦ xy) is an automorphism of F = F(x,y) with inverse φ_k = (x ↦ xY^k, y ↦ y^k X y), and ψ_k(x² Y^(2k+1)) = x·W_k·X as free words. Hence φ_k induces an isomorphism B_k := F/⟨⟨W_k⟩⟩ → H_k := ⟨x,y | x² = y^(2k+1)⟩.

*Proof.* φ_k(x)φ_k(y) = xY^k·y^kXy = y, so φ_k(xy) = y and φ_k(x(xy)^k) = xY^k y^k = x; conversely ψ_k(x)ψ_k(y)^-k = x and ψ_k(y)^k ψ_k(x)⁻¹ψ_k(y) = (xy)^k (xy)^-k X·xy = y. Finally ψ_k(x²Y^(2k+1)) = x(xy)^k·x(xy)^k·(xy)^-(2k+1) = x·(xy)^k x (xy)^-(k+1) = x·(xy)^k x·Y(XY)^k·X, because (xy)^-(k+1) = Y(XY)^k X. ∎

In H_k write s = x, t = y, z = s² = t^(2k+1) (central), so H_k/⟨z⟩ = C₂ * C_(2k+1). By G's Lemma 1 (= J's Lemma J0), conjugacy classes in H_k are classified by the cyclic syllable necklace in C₂ * C_(2k+1) together with the exponent of z.

**Theorem 2 (duality).** For all k, p ≥ 1, in H_k:

    φ_k(p_p) = (s t^(k+1))^(p−1) (s t^k)^(p+1) (s t^(k+1)) · z^-(2p+1),
    V_{k,p}  = (t^k s)^(p+1) (t^(k+1) s)^p · z^-(2p+1),

and these two elements are conjugate (by cyclic rotations of syllables). The class has syllable length 4p+2, t-exponent necklace (k+1)^p k^(p+1), and central exponent −(2p+1). Consequently

    AK(k;p) = (p_p, W_k)  ~AC  (ψ_k(V_{k,p}), W_k)      (one ACM move, W_k frozen),
    φ_k(AK(k;p))  ~AC  D(k;p) = (V_{k,p}, x²Y^(2k+1)),

and AK(k;p) is AC-trivial iff D(k;p) is (Lemma D2).

*Proof.* In H_k: X = s z⁻¹, Y^k = t^(k+1) z⁻¹, Y = t^(2k) z⁻¹, t^(3k+1) = t^k z. So φ_k(x) = xY^k = s t^(k+1) z⁻¹ and φ_k(Y) = YxY^k = t^(2k) s t^(k+1) z⁻². Then
(t^(2k) s t^(k+1))^(p+1) = t^(2k) s (t^(3k+1) s)^p t^(k+1) = t^(2k) s (t^k s)^p t^(k+1) z^p, so
φ_k(p_p) = (s t^(k+1))^p · t^(2k) s (t^k s)^p t^(k+1) · z^(−p−2(p+1)+p). Using (s t^(k+1))^p t^(2k) = (s t^(k+1))^(p−1) s t^(3k+1) = (s t^(k+1))^(p−1) s t^k z, we get φ_k(p_p) = (s t^(k+1))^(p−1) (s t^k)(s t^k)^p (s t^(k+1)) z^-(2p+1), the first formula. For V: y^k = t^k, X = s z⁻¹, Y^k X = t^(k+1) s z⁻², so V_{k,p} = (t^k s)^p t^k · s z⁻¹ · (t^(k+1) s)^p z^(−2p), the second formula. Conjugating V_{k,p} by s gives (s t^k)^(p+1) (s t^(k+1))^p z^-(2p+1); moving the block (s t^(k+1)) from the end of φ_k(p_p) to the front gives (s t^(k+1))^p (s t^k)^(p+1) z^-(2p+1); these are cyclic rotations of each other, and z is central. So φ_k(p_p) and V_{k,p} are conjugate in H_k, i.e. ψ_k(V_{k,p}) ≡ g p_p g⁻¹ modulo ⟨⟨W_k⟩⟩, and Lemma G0 turns the replacement into ordinary AC moves. Applying φ_k (a letterwise transport of the certificate) gives the second line, with frozen relator φ_k(W_k) = φ_k(x)⁻¹·x²Y^(2k+1)·φ_k(x), a conjugate of x²Y^(2k+1). ∎

**Remarks.** (i) k = 1: V_{1,p} = (yx)^p y X (YX)^p = W_p⁻¹, so D(1;p) is (W_p, x²Y³) — Theorem G1. (ii) |D(k;p)| − |AK(k;p)| = 2pk − k + 1 > 0: the dual is longer; no length is gained. (iii) In the language of §2: F(p,p+1;1,1;k) ≅ F(2,2k+1;1,k;p) up to an automorphism: the Artin length and one torus parameter are exchanged. By Theorem 1(b) one may replace y^k by y^-(k+1) (and x by X).

**Corollary 3 (the AK series occurs twice; small members).**
(a) For every k ≥ 1, AK(k;2) = (x²Y³, W_k) equals D(1;k) up to exchanging the relators and inverting one. Hence φ_1(AK(k)) ~AC AK(k;2), and AK(k;2) is AC-trivial iff AK(k) is (D2).
(b) AK(2;2) = (xxYYY, xyxyxYXYXY) (length 15) is AC-trivial: `certificates/th13_ak_2_2_trivialization.json` (2,351 moves: two torus-frozen ACM moves — the dual of G1, then G's AK(2) move transported — and a primitive finish).
(c) AK(3;2) = (xxYYY, xyxyxyxYXYXYXY) (length 19) is AC-trivial iff AK(3) is; since Aut(F₂) is AC-realized on AK(3)'s class (D6), in fact AK(3) ~AC AK(3;2) by plain AC moves: `certificates/th13_ak3_to_ak_3_2.json` (2,522 moves, peak 74) composes D's certificates for x ↦ xY and y ↦ yX (G's φ = (x ↦ xY, y ↦ yyX) is their product), the second transported by the first, with one x²Y³-frozen ACM move φ(p_3) → W_3 and a swap.
(d) AK(k;1) = (xYY, W_k) is AC-trivial for every k (primitive relator, D3); certificates for k = 2, 3.

**Certificates of the duality move** (`th13_family.py --write certificates`; start exactly AK(k;p), end exactly (red ψ_k(V_{k,p}), W_k)): (k,p) = (2,2): 2,686 moves; (2,3): 6,718 moves; (3,3): 9,192 moves. They are long because G's compiler goes through normal forms; minimality is not claimed.

## 4. The plateau and its depth (proved)

Moves are A's quotient-conjugacy (ACM) replacements; lengths are cyclic lengths; Orb(w) = rotations of w and of w⁻¹. Every ordinary AC path projects to an ACM path, so lower bounds here hold for AC paths with arbitrary conjugators.

**Coordinates on B_k.** Δ = (xy)^k x and a = xy form a basis of F with x = a^-k Δ, y = Δ⁻¹a^(k+1), and Δ²a^-(2k+1) is conjugate to x W_k X (as in Lemma 2). So B_k = ⟨Δ,a | Δ² = a^(2k+1)⟩, with centre ⟨Δ²⟩ and B_k/centre = C₂ * C_(2k+1) = ⟨S⟩ * ⟨T⟩ (Δ ↦ S, a ↦ T):

    x = a^-k Δ ↦ T^(k+1) S,   Y = a^-(k+1) Δ ↦ T^k S      (type TS)
    X = Δ⁻¹ a^k ↦ S T^k,      y = Δ⁻¹ a^(k+1) ↦ S T^(k+1)  (type ST).

Also yΔ = Δx and Δy = xΔ in B_k (from W_k), so conjugation by Δ exchanges x and y, and q_p = Δ p_p Δ⁻¹.

**Lemma P (power side; all k, p ≥ 1).** Let u be a cyclically reduced word conjugate to p_p^{±1} in B_k. Then either u ∈ Orb(p_p) ∪ Orb(q_p) (length 2p+1), or |u| ≥ 2p+1 + min(4k−2, 2k+2).

*Proof.* The image of p_p is (T^(k+1)S)^p (T^kS)^(p+1): cyclically reduced, 2p+1 syllables S, all T-syllables in {T^k, T^-k} (T^(k+1) = T^-k). The same holds for p_p⁻¹. Let L = |u|. A *run* is a maximal subword of u (cyclically) of letters of one type; if both types occur there are 2J ≥ 2 junctions between runs. As u is reduced, a junction TS|ST is xy or YX and a junction ST|TS is yx or XY. Rewrite u in F(Δ,a): at each of the J junctions TS|ST a pair ΔΔ⁻¹ cancels, so u becomes a cyclic word with L − 2J letters Δ^{±1} separated by powers of a. Its image has at most L − 2J syllables S, and cyclic reduction never creates S-syllables, so

    (☆)  2p+1 ≤ L − 2J,  and  2p+1 ≤ L − 2J − 2 if some T-syllable of this word is trivial in C_(2k+1)

(a trivial T-syllable makes two S's adjacent, which cancel; if the word has only one S, its image has at most one syllable, which is excluded).
*J = 0.* The image is alternating with 2L syllables, so L = 2p+1, and the T-necklace is (k+1)^p k^(p+1) or (k+1)^(p+1) k^p. Type TS decodes T^(k+1) ↦ x, T^k ↦ Y, giving rotations of x^pY^(p+1) = p_p or x^(p+1)Y^p = q_p⁻¹; type ST decodes T^(k+1) ↦ y, T^k ↦ X, giving rotations of q_p or p_p⁻¹.
*J ≥ 1.* A *zigzag* is a maximal subword with ≥ 2 letters whose consecutive letters have different types; by the junction rule it is a subword of (xy)^∞ or of (YX)^∞. If all of u is one cyclic zigzag, u is a rotation of (xy)^i or (YX)^i = a^{±i}, whose image has at most one syllable; excluded. Otherwise every junction lies in exactly one zigzag, a zigzag with ℓ letters contains ℓ − 1 junctions, its first and last letters are end letters of runs of length ≥ 2 and its inner letters are runs of length 1. Inside a zigzag all Δ^{±1} cancel except possibly one at each end, so it contributes exactly one a-syllable a^e; from xy = a, yx = Δ⁻¹aΔ, x = a^-kΔ, y = Δ⁻¹a^(k+1):

    ℓ = 2i:    (xy)^i = a^i,  (yx)^i = Δ⁻¹a^iΔ,  (YX)^i = a^-i,  (XY)^i = Δ⁻¹a^-iΔ          e = ±i
    ℓ = 2i+1:  (xy)^i x = a^(i−k)Δ,  (yx)^i y = Δ⁻¹a^(i+k+1),  (YX)^i Y = a^-(i+k+1)Δ,  (XY)^i X = Δ⁻¹a^(k−i)     e ∈ {±(i−k), ±(i+k+1)}.

All other a-syllables come from letters strictly inside runs and are a^{±k}, a^{±(k+1)}, i.e. T^{±k}. Since i+k+1 ≡ i−k (mod 2k+1), the zigzag syllable is T^{±i} (ℓ = 2i) or T^{±(i−k)} (ℓ = 2i+1).
(1) If no T-syllable is trivial, the image is already cyclically reduced, so every zigzag syllable must be T^{±k}: for ℓ = 2i this needs i ≡ ±k, so ℓ ≥ 2k; for ℓ = 2i+1 it needs i ≡ 2k or 0 (mod 2k+1), so ℓ ≥ 4k+1. The number 2J = Σ(ℓ − 1) of junctions is even, so either some zigzag has odd ℓ (2J ≥ 4k) or there are at least two zigzags with even ℓ (2J ≥ 2(2k−1)). By (☆), L ≥ 2p+1+4k−2.
(2) If some T-syllable is trivial, it is a zigzag syllable. If every zigzag had ℓ ≤ 2k−1 (so 1 ≤ i ≤ k−1), every zigzag syllable would be T^{±r} with 1 ≤ r ≤ k−1, hence nontrivial; so some zigzag has ℓ ≥ 2k, 2J ≥ 2k−1, hence 2J ≥ 2k, and by (☆) L ≥ 2p+1+2k+2. ∎

For k = 1 this is A's Lemma 1 with J's Lemma J1a (no partner of length 2p+2). The bound is attained for k = 1 (J: 432 words of length 9 for p = 3) and for (k,p) = (2,2) (264 words of length 11, §8); for k ≥ 3 it is probably not sharp.

**Lemma B (braid side; k ≥ 1, p ≥ 3).** Let u be a cyclically reduced word conjugate to W_k^{±1} in G_p = ⟨x,y | x^p = y^(p+1)⟩ or in G_p′ = ⟨x,y | y^p = x^(p+1)⟩. Then u ∈ Orb(W_k) or |u| ≥ 4k+2 + 2(p−2). The bound is attained.

*Proof.* Let o_x, o_y be the orders of x, y in the quotient C_{o_x} * C_{o_y} by the centre ({o_x,o_y} = {p,p+1}, both ≥ 3) and ab the abelianization x ↦ o_y, y ↦ o_x. The image of W_k^ε (ε = ±1) is alternating with 4k+2 syllables ε_j ∈ {x^{±1}, y^{±1}}, and ab(W_k^ε) = ε(o_y − o_x). Reduce the image of the cyclic word u by repeatedly deleting a trivial syllable and merging its two neighbours. Every syllable arising is the product of a set ("group") of maximal blocks of u in the same letter; a deleted syllable has integer exponent sum o·μ, and the first deleted one is a single block, so μ ≠ 0 for it; the 4k+2 final syllables have exponent sums E_j = ε_j + o·m_j (o = o_x or o_y as appropriate). Comparing exponent sums: e_x(u) = e_x(W_k^ε) + o_x M, e_y(u) = e_y(W_k^ε) + o_y N, where M, N are the sums of all m_j, μ over x-groups resp. y-groups; conjugacy forces ab(u) = ab(W_k^ε), i.e. o_x o_y (M+N) = 0. So the number ν of nonzero m_j, μ is 0 or ≥ 2. If ν = 0 nothing was deleted, every block is a final syllable with E_j = ε_j exactly (orders ≥ 3), and u ∈ Orb(W_k). If ν ≥ 2: |u| ≥ Σ_j |E_j| + Σ|oμ| ≥ (4k+2) + ν·(min(o_x,o_y) − 2) ≥ 4k+2+2(p−2), since |ε_j + o m_j| ≥ o−1 for m_j ≠ 0 and |oμ| ≥ o. Equality: replace in W_k one letter x by X^(p−1) and one letter X by x^(p−1) (in G_p; in G_p′ use y); by Lemma J0 the result is conjugate to W_k. ∎

**Theorem 4 (plateau and depth).** Let k ≥ 1, p ≥ 3 and d(k,p) = min(4k−2, 2k+2, 2p−4) ≥ 2.
(a) Every ACM path starting at AK(k;p) along which the total cyclic length never increases stays, up to order of the relators, in (Orb(p_p) ∪ Orb(q_p)) × Orb(W_k); all its states have length 2p+4k+3.
(b) The first state off this plateau on any ACM path has total cyclic length ≥ 2p+4k+3+d(k,p). In particular every AC trivialization of AK(k;p), if one exists, contains a presentation of total cyclic length ≥ 2p+4k+3+d(k,p).
(c) d is unbounded: d(k,p) = 2k+2 for k ≥ 3, p ≥ k+3; d(2,p) = 6 for p ≥ 5.

*Proof.* On the plateau the frozen relator is a rotation of p_p^{±1}, q_p^{±1} or W_k^{±1}, with quotient G_p, G_p′ or B_k; in B_k, q_p is conjugate to p_p. A move with W_k frozen replaces the power relator by a word conjugate to p_p^{±1} in B_k: by Lemma P it stays in Orb(p_p) ∪ Orb(q_p) or has length ≥ 2p+1+min(4k−2,2k+2). A move with the power relator frozen replaces the other by a word conjugate to W_k^{±1} in G_p or G_p′: by Lemma B it stays in Orb(W_k) or has length ≥ 4k+2+2p−4. Induction on the path gives (a) and (b); the plateau does not contain (x,y). ∎

**What this is and is not.** It is a search-independent statement about the complete ACM graph: AK(k;p) sits in a basin whose rim is at height ≥ d(k,p) above it, and d → ∞ in the family. For k = 1 it reproduces A and J (d = 2; AK(3): 15). After the first exit the frozen relator is no longer of torus type and the method gives nothing; in particular this is **not** evidence that any member is AC-nontrivial (AK(2;2) is AC-trivial although it is not covered: p = 2).

## 5. The known exits do not apply (proved, modulo the classical Fact C of research-g)

**Proposition 5.** Let k ≥ 1, p ≥ 2, (k,p) ≠ (1,2). Then no pair with a primitive relator is one ACM move away from AK(k;p) — with arbitrary conjugators, and the same for every automorphic image of AK(k;p). Moreover both meridian defects (cyclic syllable lengths of each relator in the other relator's torus group) are 4p+2 and 4k+2, never 2, so Prop. M of research-i and F's thickenability criterion do not apply at AK(k;p) or at any state one ACM move away.

*Proof.* The frozen relators p_p and W_k are not primitive. Two cases, exactly as in G's Proposition G2.
(a) *A primitive π conjugate to W_k^{±1} in G_p = ⟨x^p = y^(p+1)⟩.* The abelianization x ↦ p+1, y ↦ p sends W_k to 1, so the exponent vector (m,l) of π satisfies (p+1)m + pl = ±1; m, l ≠ 0 have opposite signs. If |m| = 1 then |l| = 1 (for p ≥ 3; l = (p+2)/p is not an integer) and the image of π has 2 syllables < 4k+2. If |m| ≥ 2 then 1 < |l|/|m| < 2, so by Fact C the letters x^σ of π are isolated and the y-runs have length 1 or 2; all are nontrivial in C_p * C_(p+1) (p+1 ≥ 4), so the image of π is cyclically reduced with all x-syllables equal to x^σ. The image of W_k^{±1} has x-syllables x and x⁻¹ (k+1 and k of them), distinct for p ≥ 3. So for p ≥ 3 there is no such π. For p = 2 (so k ≥ 2): in ⟨x² = y³⟩ the image of W_k has t-exponent necklace 1^k 2^(k+1) (Theorem G1's computation), which contains both factors 11 and 22; a primitive with |m| ≥ 2 has, by Fact C, a balanced necklace in {1,2} (run lengths 1, 2, with the bijection 1 ↔ 2 if the y-letters are negative), and one with |m| = 1 has 2 syllables. No such π.
(b) *A primitive π conjugate to p_p^{±1} in B_k.* Transport by φ_k to H_k; π′ = φ_k(π) is primitive with exponent vector (m,l), and the abelianization x ↦ 2k+1, y ↦ 2 of H_k sends φ_k(p_p) to −1, so (2k+1)m + 2l = ±1. If |m| = 1, π′ is conjugate to x^{±1}y^l and its image has ≤ 2 syllables < 4p+2. If |m| ≥ 3, then k < |l|/|m| < k+1, so by Fact C the x-letters of π′ are isolated, the y-runs have lengths k and k+1 (nontrivial in C_(2k+1)), and the cyclic sequence of run lengths is balanced. The t-exponent necklace of the image is this sequence, up to the bijection k ↔ k+1 when the y-letters are negative (−k ≡ k+1), hence balanced. But the necklace of φ_k(p_p)^{±1} is (k+1)^p k^(p+1) or k^p (k+1)^(p+1) (Theorem 2), which for p ≥ 2 contains both squares (k+1)(k+1) and kk. No such π.
Automorphisms carry primitives to primitives and transport ACM moves. The defects are read off from Theorem 2 (4p+2) and from the alternating image of W_k in C_p * C_(p+1) (4k+2). ∎

Exact machine check (G's complete finite test `primitive_complete`, Lemma G4): for 1 ≤ k ≤ 6, 2 ≤ p ≤ 7 a primitive neighbour exists only for (k,p) = (1,2) (self-test, item 6).

**Summary of the family by known exits.** Row p = 1: AC-trivial. AK(1;2) = AK(2) and AK(2;2): AC-trivial. Column p = 2, k ≥ 3: equivalent to AK(k). All other members (k ≥ 2, p ≥ 3): no exit at ACM distance one, plateau depth ≥ d(k,p) ≥ 2; status open.

## 6. Aut(F₂) is AC-realized on AK(2;3) and AK(2;4) — and a caution about mirror images (proved by certificates)

**Lemma 6.1 (D6 in general form).** For a pair P, S(P) = {θ ∈ Aut(F₂) : θ(P) ~AC P} is a subgroup of Aut(F₂) containing the inner automorphisms.
*Proof.* If θ₂(P) ~AC P then θ₁θ₂(P) ~AC θ₁(P) by transporting the moves letterwise by θ₁ (D2), so θ₁, θ₂ ∈ S(P) gives θ₁θ₂ ∈ S(P); and θ(P) ~AC P gives P ~AC θ⁻¹(P) by transport with θ⁻¹. Conjugating both relators by a word is a composite of AC moves. ∎

**Theorem 6 (certificates).** For every θ ∈ Aut(F₂): θ(AK(2;3)) ~AC AK(2;3) and θ(AK(2;4)) ~AC AK(2;4), where AK(2;3) = (xxxYYYY, xyxyxYXYXY) (length 17) and AK(2;4) = (xxxxYYYYY, xyxyxYXYXY) (length 19).
*Proof.* `certificates/th13_ak_2_3_aut_x_xy.json`: AK(2;3) → (xyxyxYYY, xyyxyyxYXYYXY) = τ(AK(2;3)) exactly, τ = (x ↦ xy, y ↦ y); 212 elementary moves (21 cyclic products found by M's engine at barrier 29, compiled by `d_certify.py`). `certificates/th13_ak_2_3_aut_swap.json`: AK(2;3) → (yyyXXXX, yxyxyXYXYX) = σ(AK(2;3)) exactly, σ = (x ↔ y); one W_2-frozen ACM move p_3 → q_3 (Lemma P: q_p = Δ p_p Δ⁻¹), 6,309 moves. The images of τ and σ in Out(F₂) = GL₂(ℤ) are (1 0; 1 1) and (0 1; 1 0), which generate GL₂(ℤ); the kernel of Aut(F₂) → GL₂(ℤ) is Inn(F₂) (Nielsen). By Lemma 6.1, S(AK(2;3)) = Aut(F₂). For AK(2;4) the same argument with `certificates/th13_ak_2_4_aut_x_xy.json` (AK(2;4) → (xyxyxyxYYYY, xyyxyyxYXYYXY) = τ(AK(2;4)) exactly; 306 moves, 25 cyclic products, barrier 37) and `certificates/th13_ak_2_4_aut_swap.json` (→ (yyyyXXXXX, yxyxyXYXYX); 12,899 moves). ∎

**Corollary 6.2 (explicit mirror certificate).** `certificates/th13_ak_2_3_mirror.json`: AK(2;3) → ι_x(AK(2;3)) = (XXXYYYY, XyXyXYxYxY) exactly, ι_x = (x ↦ X, y ↦ y); 2,349 elementary moves, peak free length 68, peak cyclic length 44. It is assembled by the rules of Lemma 6.1 (R(αβ) = R(α) followed by the α-transport of R(β); R(α⁻¹) = α⁻¹-transport of the reversed R(α)) from the τ-certificate and a short swap certificate `certificates/th13_ak_2_3_aut_swap_short.json` (63 moves; 7 cyclic products at barrier 23), along ι_x = Inn(X)∘μ∘σ, μ = τ₂⁻¹τ τ₂⁻¹ = (x ↦ xyX, y ↦ X), τ₂ = στσ = (y ↦ yx) (`th13_family.py --mirror`).

So, as for AK(3) (D6), automorphic images of AK(2;3) may be used freely, and the class of AK(2;3) is *not* a chirality candidate in N's sense. The swap σ is realized on every AK(k;p) by the same single ACM move (certificate also for (2,4)), and ι = (x ↦ X, y ↦ Y) fixes AK(k;p) up to rotation and inversion; what is open for general (k,p) is the realization of one transvection τ. The two engine paths for p = 3, 4 have the same shape (22 and 26 states), so a uniform symbolic realization on AK(2;p) in the style of K1 looks likely; it was not attempted. For AK(3;3) no automorphic image was found (M's engine, budget 1.5·10⁷ states, complete to barrier 34 = start + 13).

**Caution for bounded "chirality" searches (experiment + the theorem above).** The mirror image ι_x(AK(2;3)) = (XXXYYYY, XyXyXYxYxY), ι_x = (x ↦ X), is AC-equivalent to AK(2;3) by Theorem 6. Nevertheless: (i) D's engine with the two sources AK(2;3) and ι_x(AK(2;3)), complete to cap 31: 1,611,924 = 2 × 805,962 states, **no collision**; (ii) M's engine from AK(2;3), complete to cap 34 (17 above the start; 12,677,954 states): the mirror states and the images under x ↦ xY, y ↦ yX are **not** in the forward set, although τ(AK(2;3)) is reached at barrier 29. (For comparison AK(3) meets its mirror image at barrier 19. Likewise for AK(2;4): M's engine complete to cap 39, 5,808,576 states, reaches τ(AK(2;4)) and the image under y ↦ yx at barrier 37 but none of the mirror-type images.) So every directed cyclic-product path from AK(2;3) to its mirror image has peak cyclic length ≥ 35, far above the barriers 29 (transvection) and 23 (swap) of the generators; the explicit certificate of Corollary 6.2 (elementary moves, with conjugations that are not all cyclic products) has peak cyclic length 44. Since the graph is ι_x-equivariant, (i) also says that no state S of Fwd(AK(2;3), 31) has its mirror image ι_x(S) in that set. Hence the absence of a *particular* automorphic image from complete forward sets — even to start + 17 — does not show inequivalence; here the full stabilizer is obtained only as the group generated by the visible elements τ, σ (N's closure method would find it too). For C4 the visible elements generate only D₆ (N: nothing beyond D₆ by orbit collapse within cap 28; M: no automorphic image of C4 itself to cap 34 = start + 20, as reported in those notes), which is a stronger negative observation than the one made here; but the present example shows that individual stabilizer elements can have barriers beyond start + 17 in a class whose stabilizer is everything, so a non-D₆ element of Ŝ(C4), if it exists, may sit beyond the affordable caps.

## 7. Why the k = 1 role swap does not persist: a non-standard generating pair (proved remark + experiment)

For k = 1, V_{1,p} = W_p⁻¹ is itself a torus-type word, so AK(p) acquires a second torus pair (G1). For k ≥ 2, V_{k,p} is the T(2,2p+1) Wirtinger word evaluated on the pair (x, y^k), which generates H_k but:

**Lemma 7.** For k ≥ 2, no basis (α,β) of F maps, in H_k/centre = C₂ * C_(2k+1), to a simultaneous conjugate of (s, t^k); and no basis maps, in B_k/centre, to a simultaneous conjugate of (x, Δ_k y^i x^j) for any i, j (Δ_k = (xy)^k x).
*Proof.* For a basis (α,β) of F₂ the commutator [α,β] is conjugate to [x,y]^{±1} (Nielsen; MKS Thm 3.9). In C₂ * C_(2k+1) the image of [x,y] is s t s t⁻¹ (H_k coordinates), resp. the image of [Δ,a]^{±1} = S T S T⁻¹ up to conjugacy and inversion (B_k coordinates; (Δ,a) is a basis): T-exponent necklace {1, −1}. But [s, t^k] = s t^k s t^-k has necklace {k, −k}, and in B_k, [x, Δy^i x^j] = x^(i+1) y⁻¹ x^-i (use Δy = xΔ, Δx⁻¹ = y⁻¹Δ) is conjugate to xY ↦ T^(k+1)S·T^kS, necklace {k+1, k} = {−k, k}. {k,−k} = {1,−1} modulo 2k+1 only for k = 1. ∎

Consequences (remarks, no claim about AC classes): (i) there is no automorphism θ with θ(x) ≡ x, θ(y) ≡ y^k modulo ⟨⟨x²Y^(2k+1)⟩⟩ and the centre, so V_{k,p} is not "θ(W_p^{±1})" in the way it is for k = 1. (ii) The coordinate change behind the Miller–Schupp form of AK(n) (C, K: the pair (x, c) with c ≡ Δ_1 x^j is a basis and p_n ≡ x^n c x^-(n+1) c⁻¹) has no analogue of this shape for k ≥ 2. I did not prove that no Miller–Schupp-type form exists at all.

**Experiment (bounded; G's torus graph, exact primitive-neighbour test; `th13_family.py --islands`).** Aut-orbits of torus pairs reachable by torus-word ACM edges, bounds |M| ≤ 12, exponents ≤ 20, length ≤ 120:

| member | Aut-orbits | torus types met | winners |
|---|---:|---|---:|
| AK(2;2) | 3 | (2,3)&(2,3), (2,3)&(2,5) twice | 1 (it is AC-trivial) |
| AK(3;2) ≅ AK(3) | 3 | (2,3)&(3,4), (2,3)&(2,7) twice | 0 |
| AK(2;3), AK(2;4), AK(2;5) | 1 each | (p,p+1)&(2,5) only | 0 |
| AK(3;3), AK(3;4), AK(4;3) | 1 each | (p,p+1)&(2,2k+1) only | 0 |

(AK(2;3), AK(3;3), AK(2;4) also at bounds 16, 24, 160: still 1 orbit.) So within these bounds every member with k ≥ 2, p ≥ 3 is an **isolated torus node**: no other torus-type word in either partner class. This is consistent with Lemma 7 but is a bounded experiment, not a classification.

## 8. Experiments (exact commands; outputs from this session; one niced core, < 0.6 GB)

**Self-test and certificates.**
```
python3 experiments/th13_family.py --selftest          # th13_family self-test passed   (about 20 s CPU)
python3 experiments/th13_family.py --write certificates
python3 experiments/d_certify.py experiments/th13_path_ak_2_3_x_xy.txt xxxYYYY xyxyxYXYXY xyxyxYYY xyyxyyxYXYYXY certificates/th13_ak_2_3_aut_x_xy.json
python3 experiments/d_certify.py experiments/th13_path_ak_2_4_x_xy.txt xxxxYYYYY xyxyxYXYXY xyxyxyxYYYY xyyxyyxYXYYXY certificates/th13_ak_2_4_aut_x_xy.json
python3 experiments/d_certify.py experiments/th13_path_ak_2_3_swap.txt xxxYYYY xyxyxYXYXY yyyXXXX yxyxyXYXYX certificates/th13_ak_2_3_aut_swap_short.json
python3 experiments/th13_family.py --mirror certificates   # th13_ak_2_3_mirror.json moves 2349
for f in certificates/th13_*.json; do python3 experiments/elementary_verify.py $f; done
```
The self-test checks: ψ_kφ_k = id and ψ_k(x²Y^(2k+1)) ∈ Orb(W_k) (k ≤ 8); Theorem 2 by G's exact `torus_class` (k, p ≤ 8: equal classes, central exponent −(2p+1), 4p+2 syllables, t-exponents k^(p+1)(k+1)^p); triviality of AK(k;p), D(k;p) (k ≤ 4, p ≤ 5) and of sample F(a,b;i,j;m) by coset enumeration; Theorem 1(b) on samples; Lemmas P and B by brute force over all cyclically reduced words (below); Proposition 5 by G's complete primitive test (k ≤ 6, 2 ≤ p ≤ 7: only (1,2)); Lemma 7's necklaces (k ≤ 8).

Verifier output (all thirteen pass):

| certificate | from → to | moves | peak |
|---|---|---:|---:|
| `th13_dual_k2_p2.json` | AK(2;2) → (ψ_2(V_{2,2}), W_2) | 2,686 | 183 |
| `th13_dual_k2_p3.json` | AK(2;3) → (ψ_2(V_{2,3}), W_2) | 6,718 | 263 |
| `th13_dual_k3_p3.json` | AK(3;3) → (ψ_3(V_{3,3}), W_3) | 9,192 | 367 |
| `th13_ak_2_2_trivialization.json` | AK(2;2) → (x, y) | 2,351 | 139 |
| `th13_ak_2_1_trivialization.json` | AK(2;1) → (x, y) | 574 | 69 |
| `th13_ak_3_1_trivialization.json` | AK(3;1) → (x, y) | 1,054 | 99 |
| `th13_ak3_to_ak_3_2.json` | AK(3) = (xxxYYYY, xyxYXY) → AK(3;2) = (xxYYY, xyxyxyxYXYXYXY) | 2,522 | 74 |
| `th13_ak_2_3_aut_x_xy.json` | AK(2;3) → (xyxyxYYY, xyyxyyxYXYYXY) | 212 | 43 |
| `th13_ak_2_3_aut_swap.json` | AK(2;3) → (yyyXXXX, yxyxyXYXYX) | 6,309 | 263 |
| `th13_ak_2_4_aut_x_xy.json` | AK(2;4) → (xyxyxyxYYYY, xyyxyyxYXYYXY) | 306 | 55 |
| `th13_ak_2_4_aut_swap.json` | AK(2;4) → (yyyyXXXXX, yxyxyXYXYX) | 12,899 | 343 |
| `th13_ak_2_3_aut_swap_short.json` | AK(2;3) → (yyyXXXX, yxyxyXYXYX) | 63 | 33 |
| `th13_ak_2_3_mirror.json` | AK(2;3) → (XXXYYYY, XyXyXYxYxY) | 2,349 | 68 |

**First exits, exact (`th13_family.py --exits`, about 2.5 min).** Number of cyclically reduced words of length L conjugate to the partner (exact test via `torus_class`), for all L between the plateau length and the listed maximum:

- power side (words ~ p_p^{±1} in B_k, off the plateau): (k,p) = (1,3): none at 8, 432 at 9 [Lemma P bound 9]; (2,2): none at 6–10, 264 at 11 [bound 11]; (2,3): none at 8–12 [bound 13]; (3,2): none at 6–11 [bound 13]; (3,3): none at 8–12 [bound 15].
- braid side (words ~ W_k^{±1} in G_p and in G_p′, same counts): (1,3): none at 7, 32 at 8 [Lemma B bound 8]; (1,4): none at 7–9, 40 at 10 [10]; (1,5): none at 7–11, 48 at 12 [12]; (2,3): none at 11, 144 at 12 [12]; (2,4): none at 11–12 [14].
So Lemma B is sharp in every case tested and Lemma P is sharp for k = 1, 2.

**Torus islands (`th13_family.py --islands`, 47 s):** the table of §7.

**Forward sets (D's engine, `g++ -O2 -std=c++17 -o d_acsearch experiments/d_acsearch.cpp`; directed cyclic-product graph, Σ-classes, complete to cap 31 = the engine's maximum).**
```
./d_acsearch --cap 31 --maxstates 12000000 --source xxxYYYY,xyxyxYXYXY       # AK(2;3): budget_hit 0, total_states 805962, trivializing_states 0
./d_acsearch --cap 31 --maxstates 12000000 --source xxxxYYYYY,xyxyxYXYXY     # AK(2;4): total_states 10400, trivializing_states 0
./d_acsearch --cap 31 --maxstates 12000000 --source xxxYYYY,xyxyxyxYXYXYXY   # AK(3;3): total_states 65530, trivializing_states 0
./d_acsearch --cap 31 ... --source xxxYYYY,xyxyxYXYXY --source XXXYYYY,XyXyXYxYxY   # AK(2;3) + mirror: total_states 1611924, no COLLISION
./d_acsearch --cap 24 ... --source xxxYYYY,xyxYXY --source XXXYYYY,XyXYxY           # AK(3) + mirror: COLLISION 0-1 barrier 19
```
Energy spectra: AK(2;3): 17 (2 states), then 19, 20, …; AK(2;4): 19 (2 states), then 23, 24, …; AK(3;3): 21 (2 states), then 23, … — no state below the start, and the first exits 19 = 17+2, 23 = 19+4, 23 = 21+2 equal 2p+4k+3+d(k,p) of Theorem 4 (so Theorem 4(b) is sharp for these three members, already in the cyclic-product subgraph).

**Automorphic images (M's engine, `g++ -O2 -std=c++17 -pthread -o m_acsearch experiments/m_acsearch.cpp`).**
```
./m_acsearch --source xxxYYYY,xyxyxYXYXY --cap 33 --width 2 --threads 1 --maxstates 20000000 --exact-targets experiments/th13_targets_ak_2_3.txt --no-stop
#   budget_hit 0, last_complete_barrier 33, total_states 5858556, trivializing_states 0; target_hits 1: HIT x_xy barrier 29, PATH len 22 verified  (mirror, x_xY, y_yX: not hit)
./m_acsearch --source xxxxYYYYY,xyxyxYXYXY --cap 39 --width 2 --threads 1 --maxstates 15000000 --exact-targets experiments/th13_targets_ak_2_4.txt --no-stop
#   budget_hit 0, total_states 5808576, trivializing_states 0; hits: x_xy, x_yx, y_yx (and their q-forms) at barrier 37; mirror, x_xY, y_yX, x_Yx: not hit
./m_acsearch --source xxxYYYY,xyxyxyxYXYXYXY --cap 37 --width 2 --threads 1 --maxstates 15000000 --exact-targets experiments/th13_targets_ak_3_3.txt --no-stop
#   budget_hit 1, last_complete_barrier 34, trivializing_states 0, no target hit
```
The first of these commands (AK(2;3)) with `--cap 34 --maxstates 17000000`: budget_hit 0, last_complete_barrier 34, total_states 12677954, trivializing_states 0, same single hit.

**Aut-minimal lengths (D's `d_whitehead.aut_canon`).** AK(2;2): 14; AK(2;3): 17; AK(2;4): 19; AK(2;5): 21; AK(3;2): 16; AK(3;3): 19; AK(4;3): 21. In these cases the minimum is min(2p+4k+3, 3p+2k+4), the second value being the length of the image under (x ↦ xY): ⟨x,y | x^(k+1) = y x^k y, (xY)^p = y^(p+1)⟩ (free identity: W_k ↦ x^(k+1) Y X^k Y). So AK(2;3) is Aut-minimal at length 17, outside the published length ≤ 16 lists.

All searches are directed, engine-relative and bounded; "no trivializing state" is **not** evidence of non-triviality.

## 9. Failed attempts (precise reasons)

1. **A second torus pair for k ≥ 2 (a literal generalization of G1).** The partner class of the T(2,2k+1) relator contains V_{k,p}, which for k ≥ 2 is not of torus type: ⟨x,y | V_{k,p}⟩ is the amalgam of the T(2,2p+1) group ⟨x,c⟩ with ⟨y⟩ along c = y^k, and its centre is trivial because the centre of ⟨x,c⟩ is generated by (xc)^(2p+1) ∉ ⟨c⟩. Whether some *other* torus-type word lies in the class is not decided: Lemma 7 excludes the natural candidate, the bounded experiment of §7 finds none, but there is no classification.
2. **A Miller–Schupp / K-type normal form for k ≥ 2.** For k = 1, C and K pass through p_n ≡ x^n c x^-(n+1) c⁻¹ with (x,c) a basis. In B_k, p_p = x^p Δ_k x^-(p+1) Δ_k⁻¹, but by Lemma 7 no basis of F maps to a conjugate of (x, Δ_k y^i x^j). This kills the direct analogue only; other normal forms were not explored.
3. **Depth beyond the first exit.** After the first exit the frozen relator is not of torus type, Lemma J0 is unavailable, and Lemmas P/B say nothing. Theorem 4 is a statement about the rim of the first basin only.
4. **Direct trivialization of the smallest open member AK(2;3).** Complete forward sets to cap 31 (D) and cap 34 (M; 12,677,954 states) contain no primitive relator; no trivialization was found. No conclusion.
5. **An explicit mirror certificate from the ACM swap certificate.** Composing along ι_x ≡ τ₂⁻¹τ τ₂⁻¹σ with the 6,309-move compiled swap certificate would have exceeded the 2 MB limit; this was resolved by taking the swap from a 7-step engine path instead (63 moves), giving Corollary 6.2.
6. **Transvection on AK(3;3); uniform transvection on AK(2;p).** Not found within the budget for AK(3;3) (complete to start + 13); for AK(2;p) only p = 3, 4 are certified.

## 10. Honest limits

- Nothing here trivializes or obstructs AK(3), and no member with k ≥ 2, p ≥ 3 is shown AC-trivial or non-trivial. Theorem 4's unbounded depth is a statement about local minima of the ACM graph; AK(2;2) and the row p = 1 show that members of the family can be AC-trivial.
- Theorems 1, 2, 4, Lemmas P, B, 6.1, 7 are proved in full here (given G's Lemma 1 = J's Lemma J0, the conjugacy theorem for free products, and Nielsen's commutator theorem). Proposition 5 uses Fact C of research-g (classical structure of primitive words; G checked it by machine for |m|+|k| < 60); the exact machine test covers k ≤ 6, p ≤ 7 independently of the argument.
- Theorem 6 and Corollary 3(b),(c) rest on replayed certificates plus Lemma 6.1; Corollary 3(c)'s certificate uses D's two generator certificates for AK(3).
- §7's islands, §8's forward sets and the "mirror not found" statements are bounded, directed, engine-relative experiments.
- T3 and the k = 1 cases of T2, T4, T5 are restatements of G1, A, J, G2; what is new relative to A–O is the dependence on k, Theorem 6, and Lemma 7. No novelty claim against the literature (Panteleev–Ushakov and Myasnikov–Myasnikov–Shpilrain treat AK(n); I could not check whether the two-parameter family appears elsewhere).

## 11. Advice to the coordinator (ranked)

1. **Record the calibration of §6 next to the C4 question (N).** In AK(2;3)'s class the images under x ↦ xy, y ↦ yx and the swap are visible in complete forward sets (barriers start + 12, + 12, + 6), but the mirror image and the images under x ↦ xY, y ↦ yX are not visible up to start + 17, and no state of the cap-31 forward set has its mirror image in the set; the composed certificate reaches the mirror image with cyclic peak start + 27. The stabilizer is nevertheless all of Aut(F₂), by closure. So the barrier of an individual stabilizer element can exceed start + 17 even when the stabilizer is the whole group; for C4, where the visible elements generate only D₆, a non-D₆ element may likewise sit beyond the affordable caps. The C4 chirality question should not be read from caps; it needs a structural source of one new stabilizer element (or an invariant).
2. **Use AK(2;3) (length 17) as a laboratory twin of AK(3).** Same qualitative features (rigid plateau, no one-move exit, Aut-realized) but an isolated torus node and forward sets about 50 times smaller at equal height (5.9·10⁶ states at start + 16 against AK(3)'s 2.9·10⁸ at start + 16; growth ×2.2–2.7 per unit of cap; 1.27·10⁷ at start + 17), so caps of start + 19 to + 20 are affordable on this machine; a meet-in-the-middle against T(22) there is the cheapest new experiment in the project. A trivialization of AK(2;3) would not settle AK(3), but its peak would calibrate what to expect.
3. **Uniform transvection on AK(2;p).** The two engine paths (`experiments/th13_path_ak_2_{3,4}_x_xy.txt`) have the same shape; turning them into a closed-form chain in the style of K1 would give "Aut(F₂) is AC-realized on AK(2;p) for all p ≥ 3", and probably shows how to treat general k (TH15's k = 1 method may transfer).
4. **Sharpen Lemma P for k ≥ 3 and classify torus-type words in the two partner classes for k ≥ 2** (an "isolation theorem" explaining §7's islands); with TH04's k = 1 classification this would settle the torus graph of the whole family.
5. Low priority: the dual presentations D(k;p) are longer than AK(k;p) and give no shortening; the wider family F(a,b;i,j;m) reduces to (a,b,m) by Theorem 1(b) and was not explored further.

## References

- research-a (plateau lemmas), research-g (Lemma 1, G0, G1, G2, Fact C, `g_torus.py`, `g_cert.py`), research-j (Lemma J0, Theorem J1), research-i (Prop. M, Lemma E), research-k (Theorem K1), research-d (D2, D3, D6, `d_acsearch.cpp`, `d_certify.py`), research-m (`m_acsearch.cpp`), research-n (chirality of C4).
- W. Magnus, A. Karrass, D. Solitar, *Combinatorial Group Theory*: conjugacy theorem for free products (Thm 4.2); Nielsen's theorem that [α,β] is conjugate to [x,y]^{±1} for every basis (α,β) of F₂ (Thm 3.9); Out(F₂) = GL₂(ℤ).
- D. Panteleev, A. Ushakov, *Conjugacy search problem and the Andrews–Curtis conjecture*, arXiv:1609.00325 (ACM moves; externally reported, not re-read in this session).
- H. Zieschang, *Generators of the free product with amalgamation of two infinite cyclic groups*, Math. Ann. 227 (1977): classification of generating pairs of ⟨s,t | s^p = t^q⟩ (context for Lemma 7, which is proved here directly and does not rely on it; citation from memory).
