# Research TH17: the family T(2;p,q) as killers of the trefoil group — necklace dictionary, coincidences with AK(n), a third torus form of every level, and a rigidity theorem for level shifts

Date: 2026-11-09 (Los Angeles). Independent research agent TH17 (round 5, theory round).

**Status.** Partial results, all proved here or certified. **No AC trivialization of AK(3), no proof that AK(3) is not AC-trivial, no counterexample, nothing on the full conjecture.** Everything concerns the ordinary (unstabilized) AC relation. Novelty is not established for any item (literature access is blocked).

**Central claims (labels).**

| # | statement | label |
|---|---|---|
| 1 | **Dictionary (Thm 1).** In H = F/⟨⟨x²yx⁻¹y⟩⟩ = ⟨x,z \| x³z²⟩ (z = x⁻¹y, ζ = x³ central) the killer x^p y^q of T(2;p,q), p = 3k+ρ, q ≥ 3, has class (central exponent; necklace) = (k; 1^q), (k; 2·1^{q−1}), (k; 2·1^{q−3}) for ρ = 0, 1, 2. In braid generators u = xy, v = y⁻¹ (x²yx⁻¹y = uvuv⁻¹u⁻¹v⁻¹): x^{3k+1}y^q = Δ^{2k}·u·v^{−(q−1)}, so **the level k is the exponent of the full twist Δ² = ζ** | proved |
| 2 | **Lemma S of note I (a = 2) is exactly the necklace identity** (k; 2·1^{q−1}) = (k; 2·1^{(q+2)−3}), i.e. one A-frozen ACM move; two-line braid proof. The same holds for every a | proved (Cor. 1.1) |
| 3 | **Coincidences (Thm 2).** Up to inversion and all automorphisms: (a) inside T(2;·) the Lemma S pairs are the only coincidences; the classes C_k^∓ = (k; 2·1^{6k+1∓1}) are pairwise distinct; (b) the killer of AK(n) has class (0; 2ⁿ1^{n+1}), which is a T(2;·) class only for n = 1 — **no AK(n), n ≥ 2, is related to a member of T(2;·) by automorphisms and trefoil-frozen moves**; (c) xy^{2i+1}xy⁻² ~ x⁴y^{2i+3} in H for all i: the family of G5 is the row p = 4 of T(2;·) | proved |
| 4 | **(x²yx⁻¹y, xy⁷xy⁻²) ~AC T(2;4,9) = X** by one move — a plain AC equivalence (notes G, I had it only up to an automorphism / as "same status") | proved + certificate (374 moves) |
| 5 | **A two-parameter family containing both AK(n) and T(2;·) (Thm 3):** K(a,b,c) = (x²yx⁻¹y, (xy)^a y^b x^{3c}), killer u^a v^{−b} Δ^{2c}, class (c; 2^a 1^b); trivial group iff \|a−b+6c\| = 1 and gcd(a,b) = 1; AK(n) = K(n,n+1,0) (after the automorphism μ), T(2;3k+1,q) = K(1,q−1,k); members are pairwise inequivalent under trefoil-frozen moves and automorphisms except K(a,b,c) ↔ K(b,a,−c) | proved |
| 6 | **Third torus form of every level (Thm 4):** x^{3k+1}y^q ~ (x²y)^{2k+1}(xy)^{−(q+1)} in H, so T(2;3k+1,6k+2∓1) ~AC ν(T*(2k+1, −(6k+3∓1))), T*(P,Q) := (x^P y^Q, xyx⁻¹yx⁻¹y), ν = (x ↦ x²y, y ↦ xy). Note I's two "sporadic" T(8,3)/T(10,3) members of C3 and X are the case k = 1 of a uniform family of {T(2,3), T(2k+1, 6k+3∓1)} pairs | proved + certificates (k = 1, 2) |
| 7 | **Rigidity (Thm 6):** in the graph 𝔖 of all pairs of "x-shared torus-shaped" words (x^p(x^e y)^q, x^M(x^f y)^N) with frozen-relator conjugacy moves, the component of a level-k member (k ≥ 1) consists of the shear/flip orbits of T(2;3k+1,q) and T(2;3k+2,q+2) glued by Lemma S; it contains no primitive relator and no member of another level | proved (restricted move class; **not** an AC invariant) |
| 8 | A uniform level shift k → k+1 for all k ≥ 0 is equivalent to AC-triviality of all members (level 0 is trivial; the shift 0 → 1 is a trivialization of C3 or X); AC-inequivalence of any two levels would disprove the AC conjecture | proved (Prop. 5; elementary) |

Certificates (format `ordinary-ac-elementary-v1`, all replayed by `experiments/elementary_verify.py`, outputs in §8): `certificates/th17_r74member_to_T2_4_9.json`, `certificates/th17_c3_to_T2_4_7_one_move.json`, `certificates/th17_T2_4_7_to_third_form.json`, `certificates/th17_T2_7_13_to_third_form.json`.

## 0. Previous work read and choice of direction

I read `README.md` in full; notes I (§0–§5, §9–§10 and its review), G (§2–§3.4), A and J §4 in full; F §3 and the status/review parts of the other notes; and the drafts of TH02 and TH09 of this round to avoid overlap. Facts used and re-checked: G Lemma 1 / J Lemma J0 (conjugacy in ⟨a,b | a^m = b^n⟩ = necklace in C_m * C_n plus abelianization), G Lemma G0 (an ACM move is a composite of ordinary AC moves), A Lemma 1 (AK(n)'s partner has necklace 2ⁿ1^{n+1}), I Prop. G and Lemma S, D Lemmas D2/D3.

**Direction.** I kept the seed: treat every member of T(2;·) as "the trefoil group with a killer", compute the killer classes uniformly, compare with AK(n), and then attack the level shift. The new elements relative to A–O are: the exact dictionary and its braid form (level = full-twist exponent); the complete coincidence classification (note I's remark after Lemma S was a sketch for fixed A and q ≥ 3 only); the family K(a,b,c) that puts AK(n) and T(2;·) on two edges of one two-parameter family; the third torus form of each level; and a complete description of the component of each level in a precisely defined restricted graph. TH09 (census of killers of the trefoil group), TH04 (torus island of AK(n)) and TH02 (realized automorphisms) are adjacent; I do not classify killers in general, do not treat AK(n)'s island, and mention the one automorphism that falls out (Remark 6.4) only in passing.

**Notation.** X = x⁻¹, Y = y⁻¹. A = x²yXy; z = Xy, so A = x³z² as free words. H = F/⟨⟨A⟩⟩ = ⟨x,z | x³z²⟩, ζ = x³ = z⁻² central, H/⟨ζ⟩ = C₃ * C₂. Braid generators u = xy, v = Y: A is a cyclic rotation of uvuVUV, t := uv = x, Δ := uvu = x²y = vuv, Δ² = t³ = ζ, ΔuΔ⁻¹ = v. Abelianization ab: H → ℤ, x ↦ 2, z ↦ −3, y ↦ −1, u, v ↦ 1, ζ ↦ 6.
Every non-elliptic element of H is conjugate to a unique-up-to-rotation normal form ζ^c x^{e₁}z x^{e₂}z ⋯ x^{e_r}z with e_i ∈ {1,2}; its **class** (c; [e₁…e_r]) (necklace up to rotation) is a complete conjugacy invariant (G Lemma 1). Using z⁻¹ = zζ and x^{−e} = x^{3−e}ζ⁻¹: inversion sends (c; [e₁…e_r]) to (−c; [3−e_r, …, 3−e₁]), and the automorphism τ: x ↦ X, z ↦ z⁻¹ of H sends it to (−c; [3−e₁, …, 3−e_r]). Out(H) = ⟨τ⟩ ≅ ℤ/2 (Schreier; equivalently Aut(C₃*C₂) = Inn ⋊ ℤ/2, as used in F Prop. F3). The **symmetrized class** is the orbit {(c;N), (c;N^rev), (−c;N^comp), (−c;N^{comp,rev})}. ab(c; [e_i]) = 6c + Σ(2e_i − 3).

## 1. The dictionary

**Theorem 1 (proved here).** Let p = 3k + ρ with ρ ∈ {0,1,2}.
1. For q ≥ 3 the class of x^p y^q in H is (k; 1^q) if ρ = 0, (k; 2·1^{q−1}) if ρ = 1 (this also holds for q = 1, 2), and (k; 2·1^{q−3}) if ρ = 2.
2. As free words x y^q = u v^{−(q−1)}, hence in H: x^{3k+1}y^q = Δ^{2k} u v^{−(q−1)}.
3. With μ = (x ↦ xy, y ↦ Y) ∈ Aut(F): μ(xyxYXY) is a cyclic rotation of A and μ(AK(n)) = ((xy)ⁿy^{n+1}, A), whose killer uⁿv^{−(n+1)} has class (0; 2ⁿ1^{n+1}).

*Proof.* y = xz, so x^p y^q = x^{p+1} z (xz)^{q−1}. For ρ = 0 this is ζ^k (xz)^q; for ρ = 1 it is ζ^k x²z(xz)^{q−1}; for ρ = 2 it is ζ^{k+1} z(xz)^{q−1}, which is conjugate (by z) to ζ^{k+1}(xz)^{q−2}x z² = ζ^k (xz)^{q−2}x, a rotation of ζ^k x²z(xz)^{q−3}. (2): uv = xyY = x. (3): u = x·xz = x²z and v⁻¹ = y = xz, so uⁿv^{−(n+1)} = (x²z)ⁿ(xz)^{n+1} is already a normal form; this is A Lemma 1 in the present coordinates. ∎

**Corollary 1.1 (Lemma S is a necklace identity).** For all k and q ≥ 1, x^{3k+1}y^q and x^{3k+2}y^{q+2} have the same class (k; 2·1^{q−1}), so T(2;3k+1,q) → T(2;3k+2,q+2) is a single A-frozen ACM move. Braid proof: (uv)² = uvuv = Δv, so x^{3k+2}y^{q+2} = ζ^k Δ v^{−(q+1)} = ζ^k vuv·v^{−(q+1)} = ζ^k v u v^{−q}, a rotation of ζ^k u v^{−(q−1)} = x^{3k+1}y^q. For general a (m = a+1, group ⟨x,z | x^m z²⟩, ζ = x^m) the same two lines give x^{mk+m−1}(xz)^{q+2} = ζ^{k+1}z(xz)^{q+1} ~ ζ^k(xz)^q x ~ ζ^k x²z(xz)^{q−1} = x^{1+mk}(xz)^q, which is Lemma S of note I for every a. ∎

So the trivial-group members with q ≥ 1 (I Prop. G: p ≥ 1, p ≢ 0 mod 3, q = 2p ∓ 1) fall into the classes

    C_k^− = (k; 2·1^{6k})   ∋ T(2;3k+1,6k+1), T(2;3k+2,6k+3),
    C_k^+ = (k; 2·1^{6k+2}) ∋ T(2;3k+1,6k+3), T(2;3k+2,6k+5),      k ≥ 0,

with ab = +1 on C_k^− and −1 on C_k^+. C_0^∓ are AC-trivial (primitive killer), C_1^− is C3's class and C_1^+ is X's.

## 2. Coincidences

**Theorem 2 (proved here).**
(a) For p, p′ ∈ ℤ and q, q′ ≥ 3: x^p y^q is conjugate to x^{p′}y^{q′} in H iff (p′,q′) = (p,q) or {(p,q),(p′,q′)} = {(3k+1,q), (3k+2,q+2)} for some k. The symmetrized classes of the C_k^∓ (k ≥ 0, both signs) are pairwise distinct.
(b) The symmetrized class of AK(n)'s killer, {(0; 2ⁿ1^{n+1}), (0; 2^{n+1}1ⁿ)}, equals that of a member of T(2;·) iff n = 1 (then it is C_0^+). Consequently, for n ≥ 2 there are no φ ∈ Aut(F) and no (p,q) such that φ(AK(n)) arises from T(2;p,q) (or from any pair (w, A) with w in the class of x^p y^q) by A-frozen moves, relator inversions and conjugations.
(c) For every i ≥ 1, x y^{2i+1} x Y² has class (1; 2·1^{2i+2}), the class of x⁴y^{2i+3}. Hence (A, xy^{2i+1}xY²) ~AC T(2;4,2i+3) by one A-frozen move, for every i (the group is trivial only for i = 2, 3).

*Proof.* (a) By Theorem 1 the classes are (k;1^q), (k;2·1^{q−1}), (k;2·1^{q−3}); a necklace 1^q contains no 2, and 2·1^j determines j. So two classes agree iff the residues agree and (k,q) = (k′,q′), or the residues are 1 and 2 with k = k′ and q − 1 = q′ − 3. The symmetrized class of (k; 2·1^j) is {(k; 2·1^j), (−k; 1·2^j)} (a two-block necklace is its own reversal), and 1·2^j = 2·1^{j′} forces j = j′ = 1, which is excluded for the even values j = 6k, 6k+2.
(b) 2ⁿ1^{n+1} or 2^{n+1}1ⁿ equals 2·1^j or 1·2^j only for n = 1, j = 2 (or n = 0). If φ(AK(n)) arose as stated, φμ⁻¹ would carry A to a conjugate of A^{±1}, hence induce an automorphism of H carrying the class of uⁿv^{−(n+1)} to that of (x^p y^q)^{±1}; automorphisms of H and inversion preserve symmetrized classes.
(c) Conjugating by X, the word becomes (xz)^{2i+1} x z⁻¹x⁻¹z⁻¹ = (xz)^{2i+1} x·zζ·x²ζ⁻¹·zζ = ζ (xz)^{2i+2} x² z. Compare Theorem 1 with k = 1, q = 2i+3. ∎

**Corollary 2.3 (certified).** (x²yXy, xy⁷xY²) ~AC (x⁴y⁹, x²yXy) = T(2;4,9) = X by one A-frozen move: `certificates/th17_r74member_to_T2_4_9.json` (374 moves, peak 45). Notes G (Prop. G5(b)) and I (§7, group {R62, R74, X}) had this member of the published residual class R74 linked to X only up to automorphisms ("same AC-triviality status"); it is a plain AC equivalence. The case i = 2 re-derives C3 ~AC T(2;4,7) as one move (`certificates/th17_c3_to_T2_4_7_one_move.json`, 274 moves; note I has a 36-move search certificate).

**Answer to the seed's question.** No T(2;·) member has a killer conjugate to AK(n)'s for n ≥ 2, even up to inversion and automorphisms. AK(3) (class (0; 2³1⁴), SL₂(ℤ)-trace 14 under u ↦ [[1,1],[0,1]], v ↦ [[1,0],[−1,1]], ζ ↦ −I) and C3 (class (1; 2·1⁶), trace −8) are both {T(2,3), T(2,7)} pairs with 14-syllable killers, but different ones.

## 3. A two-parameter family containing AK(n) and T(2;·)

For integers a, b ≥ 1 and c put k(a,b,c) := (xy)^a y^b x^{3c} (= u^a v^{−b} Δ^{2c} in H) and K(a,b,c) := (A, k(a,b,c)).

**Theorem 3 (proved here).**
1. k(a,b,c) has class (c; 2^a 1^b) and ab = a − b + 6c.
2. K(a,b,c) presents the trivial group iff |a − b + 6c| = 1 and gcd(a,b) = 1.
3. K(n,n+1,0) = μ(AK(n)), and k(1,q−1,k) is a cyclic rotation of x^{3k+1}y^q, so K(1,q−1,k) = T(2;3k+1,q) up to rotation.
4. Two trivial-group members K(a,b,c), K(a′,b′,c′) have equal symmetrized classes iff (a′,b′,c′) ∈ {(a,b,c), (b,a,−c)}. So apart from this mirror symmetry no two members are related by automorphisms of F and A-frozen moves.

*Proof.* (1) (x²z)^a(xz)^b ζ^c is a normal form. (2) Necessity of |ab| = 1 is clear. Let G be the group of K(a,b,c). In G, w := v^b = u^a ζ^c commutes with v and with u, so it is central. In G/⟨w⟩ we have v^b = 1, hence u^b = 1 (u and v are conjugate in H), and u^a = ζ^{−c} is central; if gcd(a,b) = 1 then u is central, so v = u and G/⟨w⟩ is cyclic, hence trivial because G is perfect; then G = ⟨w⟩ is abelian, hence trivial. If d = gcd(a,b) > 1 then d | a − b = ±1 − 6c, so gcd(d,6) = 1 and d ≥ 5; killing ζ and u^d (hence v^d) kills k(a,b,c), so G maps onto ⟨x̄,z̄ | x̄³, z̄², (x̄²z̄)^d⟩, the (2,3,d) triangle group, which is not trivial. (3) is Theorem 1(2),(3). (4) The symmetrized class is {(c; 2^a1^b), (−c; 1^a2^b)} and a two-block necklace determines its block lengths. ∎

Remarks. (i) The two "edges" c = 0 and a = 1 of the family are AK(n) (b = a ± 1) and T(2;·); interior members such as K(2,7,1), K(2,9,1), K(3,8,1), K(4,9,1) are further balanced presentations of the trivial group of the same kind, pairwise inequivalent under automorphisms and trefoil-frozen moves. Whether any of them is AC-equivalent to AK(n) or to a T(2;·) class is not examined here. (ii) Under u ↦ [[1,1],[0,1]], v ↦ [[1,0],[−1,1]] (so ζ ↦ −I) the killer has trace (−1)^c(ab+2): for T(2;·) the trace is (−1)^k(6k+2) or (−1)^k(6k+4).

## 4. A third torus form of every level

**Theorem 4 (proved here).** For all k ∈ ℤ and q ≥ 1, (x²y)^{2k+1}(xy)^{−(q+1)} = Δ^{2k+1}u^{−(q+1)} is conjugate in H to x^{3k+1}y^q. Hence, with W(k,q) := (x²y)^{2k+1}(xy)^{−(q+1)},

    T(2;3k+1,q) ~AC (W(k,q), A) = ν(T*(2k+1, −(q+1))),   T*(P,Q) := (x^P y^Q, xyXyXy),  ν = (x ↦ x²y, y ↦ xy),

by one A-frozen move; W(k,q) is a torus word of type T(2k+1, q+1) in the basis (x²y, xy), and ν(xyXyXy) = A exactly.

*Proof.* Δ^{2k+1}u^{−(q+1)} = ζ^k·uvu·u^{−(q+1)} = ζ^k u v u^{−q}, a rotation of ζ^k v u^{−(q−1)} = Δ⁻¹(ζ^k u v^{−(q−1)})Δ, and ζ^k u v^{−(q−1)} = x^{3k+1}y^q by Theorem 1(2). The free reduction of ν(xyXyXy) = x²y·xy·YX²·xy·YX²·xy is x²yXy. ∎

So each class C_k^∓ contains three torus pairs "in standard position": T(2;3k+1,q) (type {T(2,3), T(3k+1,q)}), T(2;3k+2,q+2), and ν(T*(2k+1,−(q+1))) (type {T(2,3), T(2k+1,q+1)}), q = 6k+2∓1. In T* the trefoil relator is x²w³ (w = Xy) and shares the order-2 generator x with the killer, whereas in T(2;·) it is x³z² and shares the order-3 generator. For k = 1 this gives the types T(3,8) in C3's class and T(3,10) in X's class; note I found a T(8,3) and a T(10,3) member by search (T(6;8,3) and σT(8;10,3), with a 4-syllable partner, so those are different nodes) and regarded them as sporadic. Since Aut(F₂) is AC-realized on C3's class (note I), C3 ~AC T*(3,−8) = (x³Y⁸, xyXyXy) (length 17).
Certificates: `certificates/th17_T2_4_7_to_third_form.json` (k = 1) and `certificates/th17_T2_7_13_to_third_form.json` (k = 2, the level-2 class of T(2;7,13)).

## 5. What a level shift would mean

**Proposition 5 (proved here; elementary).** (i) If C_k^− ~AC C_{k+1}^− and C_k^+ ~AC C_{k+1}^+ for all k ≥ 0 (or C_k^− ~ C_k^+ ~ C_{k+1}^− for all k), then every member of T(2;·) is AC-trivial; conversely, if the AC conjecture holds, all these equivalences hold. (ii) The shift 0 → 1 alone is a trivialization of C3 (resp. X). (iii) A proof that two of the classes C_k^∓ are AC-inequivalent would disprove the AC conjecture.
*Proof.* C_0^∓ contain T(2;1,1) and T(2;1,3), whose killers xy and xy³ are primitive (D Lemma D3). The rest is formal. ∎

So the level-shift question is not easier than the frontier problem "is C3 AC-trivial"; only shifts between levels ≥ 1 (e.g. C3 ~ T(2;7,13)) are a genuinely weaker target, and only restricted-move separation statements can be proved without settling the conjecture. Theorem 2 already gives the seed's example: no sequence of trefoil-frozen moves, Lemma S moves and automorphisms changes the level. Theorem 6 goes one step further and lets both relators move.
