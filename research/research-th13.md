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
| T3 | The column p = 2 is the AK series again: AK(k;2) is, up to an automorphism, AC-equivalent to AK(k). So AK(2;2) is AC-trivial (certificate), and AK(3;2) = (xxYYY, xyxyxyxYXYXYXY) is AC-trivial iff AK(3) is. The row p = 1 is AC-trivial (primitive relator; certificates k = 2, 3) | P (from G1, D2, D3) + C |
| T4 | **Plateau of unbounded depth.** For k ≥ 1, p ≥ 3: every ACM path from AK(k;p) with non-increasing total cyclic length stays on (Orb(p_p) ∪ Orb(q_p)) × Orb(W_k), and the first state off this plateau has total cyclic length ≥ 2p+4k+3 + min(4k−2, 2k+2, 2p−4). Hence every AC trivialization of AK(k;p), if one exists, passes through cyclic length ≥ that number; e.g. ≥ initial + 2k+2 for p ≥ k+3 ≥ 6. For k = 1 this is A's theorem with J's bound 2n+9 | P (§4) + X (exact brute force for small k, p) |
| T5 | For p ≥ 2 and (k,p) ≠ (1,2), no pair with a primitive relator is one ACM move from AK(k;p) (arbitrary conjugators, Aut(F₂) free); both meridian defects are > 2, so Prop. M / thickenability exits do not apply either | P modulo the classical Fact C of research-g (§5) + X (exact test k ≤ 6, p ≤ 7) |
| T6 | For k ≥ 2 the partner of the T(2,2k+1) relator in D(k;p) is the Artin word on the generating pair (x, y^k), which is not Nielsen equivalent to (x, y) in ⟨x,y \| x² = y^(2k+1)⟩ by Zieschang's classification (externally reported) — the structural reason the k = 1 "role swap" into a second torus pair does not persist. Experiment: within G's torus-graph bounds, AK(k;p) is an isolated torus node for k ≥ 2, p ≥ 3 (islands of size 1), while AK(k;2) and AK(1;p) have 3-orbit islands | remark + X (§6) |
| X7 | Directed cyclic-product forward sets (D's engine, complete to its maximal cap 31): AK(2;3) 805,962 states, AK(2;4) 10,400, AK(3;3) 65,530 — no primitive relator, no state shorter than the start. Bounded search, **not** evidence of non-triviality | X (§7) |

**Open after this note:** AC-triviality of every AK(k;p) with k ≥ 2, p ≥ 3 (smallest: AK(2;3) = (xxxYYYY, xyxyxYXYXY), length 17) and of AK(k;2) ≅ AK(k), k ≥ 3.

## 1. Previous work read and choice of direction

Read: `README.md` in full; A in full; G §1–3 in full; J §4; I §2–3; K §3; status paragraphs and coordinator reviews of the other notes. Used and re-verified here: G's Lemma 1 (conjugacy in torus groups = syllable necklace + central exponent), Lemma G0 (ACM moves are AC composites, compiled by `g_cert.acm_edge`), G1, G2, Fact C; J's Lemma J0; A's two lemmas; D2 (AC-triviality is Aut(F₂)-invariant), D3 (primitive relator ⇒ AC-trivial).

Direction: the seed family AK(k;p) = (x^p y^-(p+1), W_k). Why it is worth a note: G1 shows that AK(n) hides a second torus knot T(2,2n+1); the family makes both knots T(p,p+1) and T(2,2k+1) free parameters, so one can see which of the AK(n) phenomena (role swap, plateau, absence of exits) are general and which are accidents of k = 1. The answers: the plateau and the absence of one-move exits are general and get *stronger* with k (T4, T5); the role swap persists only as torus ↔ Artin-on-a-non-standard-generating-pair (T2, T6); and the AK series itself sits in the family twice (row k = 1, column p = 2; T3). This is new relative to A–O, which treat only k = 1. Overlap check with the other round-5 seeds: TH04 classifies torus words in the partner classes of AK(n) itself (k = 1), TH07 studies paths beyond A's plateau for AK(n); here both questions are asked for general k, where the answers differ.

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
φ_k(p_p) = (s t^(k+1))^p · t^(2k) s (t^k s)^p t^(k+1) · z^(−p−2(p+1)+p). Using (s t^(k+1))^p t^(2k) = (s t^(k+1))^(p−1) s t^(3k+1) = (s t^(k+1))^(p−1) s t^k z, we get φ_k(p_p) = (s t^(k+1))^(p−1) (s t^k)(s t^k)^p (s t^(k+1)) z^-(2p+1), the first formula. For V: y^k = t^k, X = s z⁻¹, Y^k X = t^(k+1) s z⁻², so V_{k,p} = (t^k s)^p t^k · s z⁻¹ · (t^(k+1) s)^p z^(−2p), the second formula. Conjugating V_{k,p} by s gives (s t^k)^(p+1) (s t^(k+1))^p z^-(2p+1); moving the block (s t^(k+1)) from the end of φ_k(p_p) to the front gives (s t^(k+1))^p (s t^k)^(p+1) z^-(2p+1); these are cyclic rotations of each other, and z is central. So φ_k(p_p) and V_{k,p} are conjugate in H_k, i.e. ψ_k(V_{k,p}) ≡ g p_p g⁻¹ modulo ⟨⟨W_k⟩⟩, and Lemma G0 turns the replacement into ordinary AC moves. Applying φ_k (a letterwise transport of the certificate) gives the second line, with frozen relator φ_k(W_k) = X·x²Y^(2k+1)·x. ∎

**Remarks.** (i) k = 1: V_{1,p} = (yx)^p y X (YX)^p = W_p⁻¹, so D(1;p) is (W_p, x²Y³) — Theorem G1. (ii) |D(k;p)| − |AK(k;p)| = 2pk − k + 1 > 0: the dual is longer; no length is gained. (iii) In the language of §2: F(p,p+1;1,1;k) ≅ F(2,2k+1;1,k;p) up to an automorphism: the Artin length and one torus parameter are exchanged. By Theorem 1(b) one may replace y^k by y^-(k+1) (and x by X).

**Corollary 3 (the AK series occurs twice; small members).**
(a) For every k ≥ 1, AK(k;2) = (x²Y³, W_k) equals D(1;k) up to exchanging the relators and inverting one. Hence φ_1(AK(k)) ~AC AK(k;2), and AK(k;2) is AC-trivial iff AK(k) is (D2).
(b) AK(2;2) = (xxYYY, xyxyxYXYXY) (length 15) is AC-trivial: `certificates/th13_ak_2_2_trivialization.json` (2,351 moves: two torus-frozen ACM moves — the dual of G1, then G's AK(2) move transported — and a primitive finish).
(c) AK(3;2) = (xxYYY, xyxyxyxYXYXYXY) (length 19) is AC-trivial iff AK(3) is; since Aut(F₂) is AC-realized on AK(3)'s class (D6), in fact AK(3;2) ~AC AK(3).
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

(a trivial T-syllable makes two S's adjacent, which cancel).
*J = 0.* The image is alternating with 2L syllables, so L = 2p+1, and the T-necklace is (k+1)^p k^(p+1) or (k+1)^(p+1) k^p. Type TS decodes T^(k+1) ↦ x, T^k ↦ Y, giving rotations of x^pY^(p+1) = p_p or x^(p+1)Y^p = q_p⁻¹; type ST decodes T^(k+1) ↦ y, T^k ↦ X, giving rotations of q_p or p_p⁻¹.
*J ≥ 1.* A *zigzag* is a maximal subword with ≥ 2 letters whose consecutive letters have different types; by the junction rule it is a subword of (xy)^∞ or of (YX)^∞. If all of u is one cyclic zigzag, u is a rotation of (xy)^i or (YX)^i = a^{±i}, whose image has at most one syllable; excluded. Otherwise every junction lies in exactly one zigzag, a zigzag with ℓ letters contains ℓ − 1 junctions, its first and last letters are end letters of runs of length ≥ 2 and its inner letters are runs of length 1. Inside a zigzag all Δ^{±1} cancel except possibly one at each end, so it contributes exactly one a-syllable a^e; from xy = a, yx = Δ⁻¹aΔ, x = a^-kΔ, y = Δ⁻¹a^(k+1):

    ℓ = 2i:    (xy)^i = a^i,  (yx)^i = Δ⁻¹a^iΔ,  (YX)^i = a^-i,  (XY)^i = Δ⁻¹a^-iΔ          e = ±i
    ℓ = 2i+1:  (xy)^i x = a^(i−k)Δ,  (yx)^i y = Δ⁻¹a^(i+k+1),  (YX)^i Y = a^-(i+k+1)Δ,  (XY)^i X = Δ⁻¹a^(k−i)     e ∈ {±(i−k), ±(i+k+1)}.

All other a-syllables come from letters strictly inside runs and are a^{±k}, a^{±(k+1)}, i.e. T^{±k}. Since i+k+1 ≡ i−k (mod 2k+1), the zigzag syllable is T^{±i} (ℓ = 2i) or T^{±(i−k)} (ℓ = 2i+1).
(1) If no T-syllable is trivial, the image is already cyclically reduced, so every zigzag syllable must be T^{±k}: for ℓ = 2i this needs i ≡ ±k, so ℓ ≥ 2k; for ℓ = 2i+1 it needs i ≡ 2k or 0 (mod 2k+1), so ℓ ≥ 4k+1. The number 2J = Σ(ℓ − 1) of junctions is even, so either some zigzag has odd ℓ (2J ≥ 4k) or there are at least two zigzags with even ℓ (2J ≥ 2(2k−1)). By (☆), L ≥ 2p+1+4k−2.
(2) If some T-syllable is trivial, it is a zigzag syllable. If every zigzag had ℓ ≤ 2k−1 (so 1 ≤ i ≤ k−1), every zigzag syllable would be T^{±r} with 1 ≤ r ≤ k−1, hence nontrivial; so some zigzag has ℓ ≥ 2k, 2J ≥ 2k−1, hence 2J ≥ 2k, and by (☆) L ≥ 2p+1+2k+2. ∎

For k = 1 this is A's Lemma 1 with J's Lemma J1a (no partner of length 2p+2). The bound is attained for k = 1 (J: 432 words of length 9 for p = 3) and for (k,p) = (2,2) (264 words of length 11, §7); for k ≥ 3 it is probably not sharp.

**Lemma B (braid side; k ≥ 1, p ≥ 3).** Let u be a cyclically reduced word conjugate to W_k^{±1} in G_p = ⟨x,y | x^p = y^(p+1)⟩ or in G_p′ = ⟨x,y | y^p = x^(p+1)⟩. Then u ∈ Orb(W_k) or |u| ≥ 4k+2 + 2(p−2). The bound is attained.

*Proof.* Let o_x, o_y be the orders of x, y in the quotient C_{o_x} * C_{o_y} by the centre ({o_x,o_y} = {p,p+1}, both ≥ 3) and ab the abelianization x ↦ o_y, y ↦ o_x. The image of W_k^ε (ε = ±1) is alternating with 4k+2 syllables ε_j ∈ {x^{±1}, y^{±1}}, and ab(W_k^ε) = ε(o_y − o_x). Reduce the image of the cyclic word u by repeatedly deleting a trivial syllable and merging its two neighbours. Every syllable arising is the product of a set ("group") of maximal blocks of u in the same letter; a deleted syllable has integer exponent sum o·μ, and the first deleted one is a single block, so μ ≠ 0 for it; the 4k+2 final syllables have exponent sums E_j = ε_j + o·m_j (o = o_x or o_y as appropriate). Comparing exponent sums: e_x(u) = e_x(W_k^ε) + o_x M, e_y(u) = e_y(W_k^ε) + o_y N, where M, N are the sums of all m_j, μ over x-groups resp. y-groups; conjugacy forces ab(u) = ab(W_k^ε), i.e. o_x o_y (M+N) = 0. So the number ν of nonzero m_j, μ is 0 or ≥ 2. If ν = 0 nothing was deleted, every block is a final syllable with E_j = ε_j exactly (orders ≥ 3), and u ∈ Orb(W_k). If ν ≥ 2: |u| ≥ Σ_j |E_j| + Σ|oμ| ≥ (4k+2) + ν·(min(o_x,o_y) − 2) ≥ 4k+2+2(p−2), since |ε_j + o m_j| ≥ o−1 for m_j ≠ 0 and |oμ| ≥ o. Equality: replace in W_k one letter x by X^(p−1) and one letter X by x^(p−1) (in G_p; in G_p′ use y); by Lemma J0 the result is conjugate to W_k. ∎

**Theorem 4 (plateau and depth).** Let k ≥ 1, p ≥ 3 and d(k,p) = min(4k−2, 2k+2, 2p−4) ≥ 2.
(a) Every ACM path starting at AK(k;p) along which the total cyclic length never increases stays, up to order of the relators, in (Orb(p_p) ∪ Orb(q_p)) × Orb(W_k); all its states have length 2p+4k+3.
(b) The first state off this plateau on any ACM path has total cyclic length ≥ 2p+4k+3+d(k,p). In particular every AC trivialization of AK(k;p), if one exists, contains a presentation of total cyclic length ≥ 2p+4k+3+d(k,p).
(c) d is unbounded: d(k,p) = 2k+2 for k ≥ 3, p ≥ k+3; d(2,p) = 6 for p ≥ 5.

*Proof.* On the plateau the frozen relator is a rotation of p_p^{±1}, q_p^{±1} or W_k^{±1}, with quotient G_p, G_p′ or B_k; in B_k, q_p is conjugate to p_p. A move with W_k frozen replaces the power relator by a word conjugate to p_p^{±1} in B_k: by Lemma P it stays in Orb(p_p) ∪ Orb(q_p) or has length ≥ 2p+1+min(4k−2,2k+2). A move with the power relator frozen replaces the other by a word conjugate to W_k^{±1} in G_p or G_p′: by Lemma B it stays in Orb(W_k) or has length ≥ 4k+2+2p−4. Induction on the path gives (a) and (b); the plateau does not contain (x,y). ∎

**What this is and is not.** It is a search-independent statement about the complete ACM graph: AK(k;p) sits in a basin whose rim is at height ≥ d(k,p) above it, and d → ∞ in the family. For k = 1 it reproduces A and J (d = 2; AK(3): 15). After the first exit the frozen relator is no longer of torus type and the method gives nothing; in particular this is **not** evidence that any member is AC-nontrivial (AK(2;2) is AC-trivial although it is not covered: p = 2).
