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
| 6 | **Third torus form of every level (Thm 4):** x^{3k+1}y^q ~ (x²y)^{2k+1}(xy)^{−(q+1)} in H, so T(2;3k+1,6k+2∓1) ~AC ν(T*(2k+1, −(6k+3∓1))), T*(P,Q) := (x^P y^Q, xyx⁻¹yx⁻¹y), ν = (x ↦ x²y, y ↦ xy). So every class contains a {T(2,3), T(2k+1, 6k+3∓1)} pair; for k = 1 the new relator types are T(3,8) (C3) and T(3,10) (X). (Note I's T(6;8,3) and σT(8;10,3) are different nodes, of types {T(7,2), T(8,3)} and {T(9,2), T(10,3)}) | proved + certificates (k = 1, 2) |
| 7 | **Rigidity (Thms 6, 6\*):** in the graph 𝔖 of all pairs of "x-shared torus-shaped" words (x^p(x^e y)^q, x^M(x^f y)^N) with frozen-relator conjugacy moves, the component of a level-k member (k ≥ 1) consists of the shear/flip orbits of T(2;3k+1,q) and T(2;3k+2,q+2) glued by Lemma S; the component of the third form (shared primitive x²y) is a single shear orbit. Neither contains a primitive relator or a member of another level | proved (restricted move classes; **not** AC invariants) |
| 8 | A uniform level shift k → k+1 for all k ≥ 0 is equivalent to AC-triviality of all members (level 0 is trivial; the shift 0 → 1 is a trivialization of C3 or X); AC-inequivalence of any two levels would disprove the AC conjecture | proved (Prop. 5; elementary) |

Certificates (format `ordinary-ac-elementary-v1`, all replayed by `experiments/elementary_verify.py`, outputs in §8): `certificates/th17_r74member_to_T2_4_9.json`, `certificates/th17_c3_to_T2_4_7_one_move.json`, `certificates/th17_T2_4_7_to_third_form.json`, `certificates/th17_T2_7_13_to_third_form.json`.

## 0. Previous work read and choice of direction

I read `README.md` in full; notes I (§0–§5, §9–§10 and its review), G (§2–§3.4), A and J §4 in full; F §3, N §3.3, and the status paragraphs and coordinator's reviews of all other notes B–O; and the drafts of TH02 and TH09 of this round to avoid overlap. Facts used and re-checked: G Lemma 1 / J Lemma J0 (conjugacy in ⟨a,b | a^m = b^n⟩ = necklace in C_m * C_n plus abelianization), G Lemma G0 (an ACM move is a composite of ordinary AC moves), A Lemma 1 (AK(n)'s partner has necklace 2ⁿ1^{n+1}), I Prop. G and Lemma S, D Lemmas D2/D3.

**Direction.** I kept the seed: treat every member of T(2;·) as "the trefoil group with a killer", compute the killer classes uniformly, compare with AK(n), and then attack the level shift. The new elements relative to A–O are: the exact dictionary and its braid form (level = full-twist exponent); the complete coincidence classification (note I's remark after Lemma S was a sketch for fixed A and q ≥ 3 only); the family K(a,b,c) that puts AK(n) and T(2;·) on two edges of one two-parameter family; the third torus form of each level; and a complete description of the component of each level in a precisely defined restricted graph. TH09 (census of killers of the trefoil group), TH04 (torus island of AK(n)) and TH02 (realized automorphisms) are adjacent; I do not classify killers in general, do not treat AK(n)'s island, and mention the one automorphism that falls out (Remark 6.4) only in passing.

**Notation.** X = x⁻¹, Y = y⁻¹. A = x²yXy; z = Xy, so A = x³z² as free words. H = F/⟨⟨A⟩⟩ = ⟨x,z | x³z²⟩, ζ = x³ = z⁻² central, H/⟨ζ⟩ = C₃ * C₂. Braid generators u = xy, v = Y: A is a cyclic rotation of uvuVUV, t := uv = x, Δ := uvu = x²y = vuv, Δ² = t³ = ζ, ΔuΔ⁻¹ = v. Abelianization ab: H → ℤ, x ↦ 2, z ↦ −3, y ↦ −1, u, v ↦ 1, ζ ↦ 6.
Every non-elliptic element of H is conjugate to a unique-up-to-rotation normal form ζ^c x^{e₁}z x^{e₂}z ⋯ x^{e_r}z with e_i ∈ {1,2}; its **class** (c; [e₁…e_r]) (necklace up to rotation) is a complete conjugacy invariant (G Lemma 1). Using z⁻¹ = zζ and x^{−e} = x^{3−e}ζ⁻¹: inversion sends (c; [e₁…e_r]) to (−c; [3−e_r, …, 3−e₁]), and the automorphism τ: x ↦ X, z ↦ z⁻¹ of H sends it to (−c; [3−e₁, …, 3−e_r]). Aut(H) = Inn(H)·⟨τ⟩ (Schreier). Short argument from Aut(C₃*C₂) = Inn ⋊ ℤ/2 (the fact quoted in F Prop. F3): an automorphism α preserves the centre, so up to an inner automorphism α(x) = x^{±1}ζ^i, α(z) = zζ^j; the relator forces (i,j) = (2m, −3m), resp. (2m, 1−3m), and then α(H) lies in the preimage of |1−6m|·ℤ under ab, so m = 0 and α is the identity, resp. τ. Both formulas were also checked on 300 random normal forms. The **symmetrized class** is the orbit {(c;N), (c;N^rev), (−c;N^comp), (−c;N^{comp,rev})}. ab(c; [e_i]) = 6c + Σ(2e_i − 3).

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
3. K(n,n+1,0) = μ(AK(n)) up to the order of the relators (μ(xyxYXY) reduces to A exactly), and k(1,q−1,k) is a cyclic rotation of x^{3k+1}y^q, so K(1,q−1,k) = T(2;3k+1,q) up to rotation.
4. Two trivial-group members K(a,b,c), K(a′,b′,c′) have equal symmetrized classes iff (a′,b′,c′) ∈ {(a,b,c), (b,a,−c)}. So apart from this mirror symmetry no two members are related by automorphisms of F and A-frozen moves.

*Proof.* (1) (x²z)^a(xz)^b ζ^c is a normal form. (2) Necessity of |ab| = 1 is clear. Let G be the group of K(a,b,c). In G, w := v^b = u^a ζ^c commutes with v and with u, so it is central. In G/⟨w⟩ we have v^b = 1, hence u^b = 1 (u and v are conjugate in H), and u^a = ζ^{−c} is central; if gcd(a,b) = 1 then u is central, so v = u and G/⟨w⟩ is cyclic, hence trivial because G is perfect; then G = ⟨w⟩ is abelian, hence trivial. If d = gcd(a,b) > 1 then d | a − b = ±1 − 6c, so gcd(d,6) = 1 and d ≥ 5; killing ζ and u^d (hence v^d) kills k(a,b,c), so G maps onto ⟨x̄,z̄ | x̄³, z̄², (x̄²z̄)^d⟩, the (2,3,d) triangle group, which is not trivial. (3) is Theorem 1(2),(3). (4) The symmetrized class is {(c; 2^a1^b), (−c; 1^a2^b)} and a two-block necklace determines its block lengths. ∎

Remarks. (i) The two "edges" c = 0 and a = 1 of the family are AK(n) (b = a ± 1) and T(2;·); interior members such as K(2,7,1), K(2,9,1), K(3,8,1), K(4,9,1) are further balanced presentations of the trivial group of the same kind, pairwise inequivalent under automorphisms and trefoil-frozen moves. Whether any of them is AC-equivalent to AK(n) or to a T(2;·) class is not examined here. (ii) Under u ↦ [[1,1],[0,1]], v ↦ [[1,0],[−1,1]] (so ζ ↦ −I) the killer has trace (−1)^c(ab+2): for T(2;·) the trace is (−1)^k(6k+2) or (−1)^k(6k+4).

## 4. A third torus form of every level

**Theorem 4 (proved here).** For all k ∈ ℤ and q ≥ 1, (x²y)^{2k+1}(xy)^{−(q+1)} = Δ^{2k+1}u^{−(q+1)} is conjugate in H to x^{3k+1}y^q. Hence, with W(k,q) := (x²y)^{2k+1}(xy)^{−(q+1)},

    T(2;3k+1,q) ~AC (W(k,q), A) = ν(T*(2k+1, −(q+1))),   T*(P,Q) := (x^P y^Q, xyXyXy),  ν = (x ↦ x²y, y ↦ xy),

by one A-frozen move; W(k,q) is a torus word of type T(2k+1, q+1) in the basis (x²y, xy), and ν(xyXyXy) = A exactly.

*Proof.* Δ^{2k+1}u^{−(q+1)} = ζ^k·uvu·u^{−(q+1)} = ζ^k u v u^{−q}, a rotation of ζ^k v u^{−(q−1)} = Δ⁻¹(ζ^k u v^{−(q−1)})Δ, and ζ^k u v^{−(q−1)} = x^{3k+1}y^q by Theorem 1(2). The free reduction of ν(xyXyXy) = x²y·xy·YX²·xy·YX²·xy is x²yXy. ∎

So each class C_k^∓ contains three torus pairs "in standard position": T(2;3k+1,q) (type {T(2,3), T(3k+1,q)}), T(2;3k+2,q+2), and ν(T*(2k+1,−(q+1))) (type {T(2,3), T(2k+1,q+1)}), q = 6k+2∓1. In T* the trefoil relator is x²w³ (w = Xy) and shares the order-2 generator x with the killer, whereas in T(2;·) it is x³z² and shares the order-3 generator. For k = 1 this gives the types T(3,8) in C3's class and T(3,10) in X's class. Note I found a T(8,3) and a T(10,3) relator in these classes by search (T(6;8,3) and σT(8;10,3)); those are different nodes — their second relator is of type T(7,2), resp. T(9,2), with a 4-syllable image in the torus quotient, whereas here it is the trefoil relator with 6 syllables — and note I showed that that "duality" is not a family. The third form is uniform in k. Since Aut(F₂) is AC-realized on C3's class (note I), C3 ~AC T*(3,−8) = (x³Y⁸, xyXyXy) (length 17).
Certificates: `certificates/th17_T2_4_7_to_third_form.json` (k = 1) and `certificates/th17_T2_7_13_to_third_form.json` (k = 2, the level-2 class of T(2;7,13)).

## 5. What a level shift would mean

**Proposition 5 (proved here; elementary).** (i) If C_k^− ~AC C_{k+1}^− and C_k^+ ~AC C_{k+1}^+ for all k ≥ 0 (or C_k^− ~ C_k^+ ~ C_{k+1}^− for all k), then every member of T(2;·) is AC-trivial; conversely, if the AC conjecture holds, all these equivalences hold. (ii) The shift 0 → 1 alone is a trivialization of C3 (resp. X). (iii) A proof that two of the classes C_k^∓ are AC-inequivalent would disprove the AC conjecture.
*Proof.* C_0^∓ contain T(2;1,1) and T(2;1,3), whose killers xy and xy³ are primitive (D Lemma D3). The rest is formal. ∎

So the level-shift question is not easier than the frontier problem "is C3 AC-trivial"; only shifts between levels ≥ 1 (e.g. C3 ~ T(2;7,13)) are a genuinely weaker target, and only restricted-move separation statements can be proved without settling the conjecture. Theorem 2 already gives the seed's example: no sequence of trefoil-frozen moves, Lemma S moves and automorphisms changes the level. Theorem 6 goes one step further and lets both relators move.

## 6. Rigidity of every level among x-shared torus-shaped pairs

**The restricted move class.** A *shape* is a word S(a,b,n) := x^a(x^b y)^n (a, b ∈ ℤ, n ≠ 0), considered up to cyclic rotation and inversion; S(a,b,n)⁻¹ is a rotation of S(−a,b,−n). Shapes are the torus-type words in the bases (x, x^b y) — all bases that contain the fixed primitive x. Let 𝔖 be the graph whose vertices are the unordered pairs {W, W′} of shapes and in which {W, W′} is joined to {W, W″} iff W″ is conjugate to W′^{±1} in F/⟨⟨W⟩⟩. Every edge is an ACM move, hence an ordinary AC equivalence (G Lemma G0). T(2;p,q) = {S(p,0,q), S(3,−1,2)} is a vertex; Lemma S, the moves of Theorem 2 between shapes, and note I's "shared-vertex" moves are edges. Moves through words that are not shapes (e.g. Theorem 4, which shares x²y instead of x) are outside 𝔖.

**Parameters.** Write P(c,p,M | q; f) := {S(p, c+f, q), S(M, f, 2)}. With y₁ := x^{c+f}y and z := x^f y the two words are x^p y₁^q = x^p(x^c z)^q and x^M z² = x^{M−c} y₁ x^{−c} y₁. T(2;p,q) = P(1,p,3 | q; −1). The quantity D = 2p − q(M − 2c) is the exponent-sum determinant. On triples (c,p,M) define

    U(c,p,M) = (c+p, p, M+2p),   V(c,p,M) = (c+M, p−qM, M),   Φ(c,p,M) = (M−c, −p, M),   ε(c,p,M) = (c−M, p, −M).

Φ and ε are involutions and conjugate U, V to U⁻¹, V⁻¹ (direct check); D is preserved up to sign.

**Lemma 6.1 (second word frozen).** Let M be odd, |M| ≥ 3, H_M = ⟨x,z | x^M z²⟩, q ≥ 3, and K = x^p(x^c z)^q with c ≢ 0, p ≢ 0, p + c ≢ 0 (mod M). The shapes S_z(a,b,n) := x^a(x^b z)^n conjugate to K in H_M are exactly
(α) (a,b,n) = (p − μqM, c + μM, q), μ ∈ ℤ (these are equal to K in H_M);
(β) (a,b,n) = (p − (μ+1)qM, −c − μM, −q), μ ∈ ℤ;
(γ) only if p ≡ c (mod M): (a,b,n) = (p + M − 2c − μ(q+2)M, c + μM, q+2) and (a − (q+2)M, −b, −(q+2)) for these (a,b).
The shapes conjugate to K⁻¹ are the S_z(−a,b,−n) for (a,b,n) in this list.
*Proof.* Put ζ = x^M, so z⁻¹ = zζ. First, S_z(a,b,−n) = x^a(z⁻¹x^{−b})ⁿ = ζⁿx^a(zx^{−b})ⁿ, which is conjugate (by x^{−b}) to S_z(a+nM, −b, n); so it suffices to treat n ≥ 1, and (β), the second half of (γ) are the images of (α), (γ) under this flip. The image of K in C_|M| * C₂ is x^{p+c}z(x^c z)^{q−1}, cyclically reduced with 2q syllables and x-exponent necklace [p+c, c^{q−1}], not constant. Let W = S_z(a,b,n), n ≥ 1, with image x^{a+b}z(x^b z)^{n−1}. If b ≡ 0 the image has ≤ 2 syllables. If b ≢ 0 and a+b ≢ 0 it has 2n syllables and necklace [a+b, b^{n−1}]; comparing multisets (q ≥ 3; the repeated entry is b resp. c) gives n = q, b ≡ c, a ≡ p; writing a = p + λM, b = c + μM we get W = Kζ^{λ+μq}, and Kζ^j ~ K only for j = 0 (Lemma J0), i.e. (α). If b ≢ 0 and a+b ≡ 0, write a = −b + λM: W = ζ^λ z(x^b z)^{n−1} ~ ζ^{λ−1}(x^b z)^{n−2}x^b, which has at most one syllable for n ≤ 2 and necklace [2b, b^{n−3}] with 2(n−2) syllables for n ≥ 3 (2b ≢ 0 as M is odd); so n = q+2, b ≡ c, 2b ≡ p + c, i.e. p ≡ c, and with b = c + μM, p = c + λ₀M one computes W ~ ζ^{λ−1+μ(q+1)}x^c(x^c z)^q while K = ζ^{λ₀}x^c(x^c z)^q, so λ = λ₀ + 1 − μ(q+1), which is (γ). ∎

**Lemma 6.2 (first word frozen).** Let |p| ≥ 2, q ≥ 4, gcd(p,q) = 1, G = ⟨x,y₁ | x^p y₁^q⟩ and R = x^{M−c}y₁x^{−c}y₁ with c ≢ 0 and c ≢ M (mod p). A shape S₁(a,b,n) := x^a(x^{−b}y₁)ⁿ is conjugate to R^{±1} in G iff, up to rotation and inversion, it is one of the words x^{M−c+κp} y₁ x^{−c−κp} y₁ = S₁(M+2κp, c+κp, 2), κ ∈ ℤ (all equal to R in G).
*Proof.* By inversion we may take n ≥ 1; then the y₁-syllables of the image in C_|p| * C_q are positive powers. The image of R has 4 syllables x^{M−c}, y₁, x^{−c}, y₁. For W = x^{a−b}y₁(x^{−b}y₁)^{n−1}: if b ≡ 0 there are ≤ 2 syllables; if b ≢ 0 and a ≡ b the image is a single syllable for n = 1 and y₁²(x^{−b}y₁)^{n−2}x^{−b} cyclically for n ≥ 2, with 2(n−1) syllables and a syllable y₁², which is neither y₁ nor y₁⁻¹ because q ≥ 4; otherwise there are 2n syllables, so n = 2 and (a−b, −b) ≡ (M−c, −c) or (−c, M−c) (mod p), and it is conjugate to R, not R⁻¹, because y₁ ≢ y₁⁻¹. In the first case a − b = M − c + λp, b = c + κp and W = R·x^{(λ−κ)p}, so λ = κ by Lemma J0. The second case gives the same cyclic words (rotate by half). ∎

**Lemma 6.3 (the orbit).** Let p₀ ≥ 4, q = 2p₀ ∓ 1 and let Ω be the orbit of (1,p₀,3) under ⟨U,V,Φ,ε⟩. For every (c,p,M) ∈ Ω: (i) M is odd, |M| ≥ 3, |p| ≥ 4 and gcd(p,q) = 1; (ii) c ≢ 0 and c ≢ M (mod p); (iii) if |M| ≠ 3 then |M| ≥ 5 and c ≢ 0, p ≢ 0, p ≢ ±c (mod M); (iv) |M| = 3 iff (c,p,M) ∈ ⟨V,Φ,ε⟩(1,p₀,3).
*Proof.* Φ, ε preserve |p|, |M| and all the conditions and normalize ⟨U⟩, ⟨V⟩, so it suffices to follow reduced words in U, V. Let M̃ = M − 2c (odd, U-invariant, M̃ = (2p − D)/q, so |M̃| ≤ (2|p|+1)/q < |p|) and P̃ = p + qc (V-invariant, P̃ = (D + qM)/2).
*Start.* V^μ(1,p₀,3) = (1+3μ, p₀−3μq, 3) has |p| ≥ 3|μ|q − p₀ > max(|1+3μ|, |3μ−2|, 3) for μ ≠ 0 (as q ≥ 2p₀−1 ≥ 7), and c = 1+3μ ∉ {0, 3}; for μ = 0, c = 1 and p₀ ≥ 4 does not divide 1 or 2; so (i), (ii) hold and |p| > |M|. (gcd(p,q) divides D = ±1 everywhere.)
*U-step.* Let (c₀,p,M₀) satisfy (i), (ii) and |p| > |M₀|, and (c,p,M) = U^κ(c₀,p,M₀), κ ≠ 0. Then |M| ≥ 2|p| − |M₀| > |p| ≥ 4, and residues mod p are unchanged, so (i), (ii) persist. Since 2c ≡ −M̃ (mod M) and M is odd: c ≡ 0 iff M | M̃, impossible as 0 < |M̃| < |M|; M | p is impossible; p ≡ ±c iff M | 2p ± M̃. The number 2p ± M̃ is odd and |2p ± M̃| < 3|p| < 3|M|, so it would be ±M; for |κ| ≥ 2, |M| > 3|p| excludes this; for κ = ±1, 2p + σM̃ = τ(M₀ + 2κp) gives either 4p = τM₀ − σM̃ (impossible, |M₀| + |M̃| < 2|p|) or M̃ = ±M₀, i.e. c₀ = 0 or c₀ = M₀, contradicting (ii) for (c₀,p,M₀). So (iii) holds.
*V-step.* Let (c₁,p₁,M) satisfy (i), (iii) and |M| > |p₁|, and (c,p,M) = V^μ(c₁,p₁,M), μ ≠ 0. Then |p| ≥ q|M| − |p₁| > (q−1)|M|, residues mod M are unchanged, and gcd(p,q) | D. As qc ≡ P̃ (mod p): c ≡ 0 iff p | P̃ and c ≡ M iff p | qM − P̃ = (qM − D)/2; both numbers are nonzero and of absolute value ≤ (q|M|+1)/2 < |p|. So (i)–(iii) hold and |p| > |M|.
Alternating the two steps from the start vertices proves (i)–(iii) on Ω, and |M| ≥ 5 after the first U-step, which is (iv). ∎

**Theorem 6 (proved here).** Let k ≥ 1, p₀ = 3k+1, q₀ ∈ {6k+1, 6k+3}, and let 𝒞 be the connected component of T(2;p₀,q₀) in 𝔖. Then 𝒞 is exactly the set of vertices P(c,p,M | q; f) with either q = q₀ and (c,p,M) in the ⟨U,V,Φ,ε⟩-orbit of (1,p₀,3), or q = q₀+2 and (c,p,M) in the orbit of (1,p₀+1,3); in both cases f = (1−M)/2. In particular:
1. no vertex of 𝒞 contains a primitive word (always |p| ≥ 4, q ≥ 7, |M| ≥ 3, N = 2);
2. the 2-word of a vertex is of trefoil type iff |M| = 3 iff the vertex is {W, A} with W conjugate in H to (x^{p₀}y^{q₀})^{±1}; all other vertices are {T(p,q), T(M,2)} pairs with |M| ≥ 5;
3. 𝒞 contains no member of T(2;·) other than T(2;p₀,q₀) and T(2;p₀+1,q₀+2), and no image of another member under an automorphism of F. So within 𝔖 there is no level shift, no passage between C_k^− and C_k^+, and no trivialization.

*Proof.* Induction along paths. The moves below change (M,f) by (2κp, −κp) (first word frozen) or not at all, and ε replaces (M,f) by (−M, f+M); so 2f + M = 1 throughout, and for |M| = 3 the 2-word x^M(x^f y)² is A up to rotation. Let P = P(c,p,M | q; f) be a vertex as described. (a) First word frozen: by Lemma 6.3 (i), (ii), Lemma 6.2 applies (a shape in (x,y) is a shape in (x,y₁)), and the new vertex is P(c+κp, p, M+2κp | q; f−κp), with triple U^κ(c,p,M). (b) Second word frozen, |M| ≥ 5: by Lemma 6.3 (iii), Lemma 6.1 applies without case (γ); (α) gives the triple V^μ(c,p,M); (β), after inverting the word, gives (−c−μM, −p+(μ+1)qM, M) = V^{−(μ+1)}Φ(c,p,M); inverses give the same vertices. (c) Second word frozen, |M| = 3: by Lemma 6.3 (iv) the 2-word is A and the other word is conjugate in H to K₀^{±1}, K₀ = x^{p₀}y^{q₀}; Lemma 6.1 applied to K₀ (c = 1, p₀ ≡ 1 mod 3, so (γ) occurs) gives the triples V^μ(1,p₀,3), their Φ-images, and V^μ(1,p₀+1,3) with exponent q₀+2 and their Φ-images. The same orbit analysis applies to the start (1,p₀+1,3) with q₀+2 = 2(p₀+1) ∓ 1 (at its |M| = 3 vertices the killer is degenerate, and (c) covers them). Conversely every such vertex is reached, since U, V, Φ and Lemma S are edges; ε only re-describes the same word (x^M z² = x^{−M}(x^M z)² cyclically). Items 1, 2 are Lemma 6.3 (i), (iv). For 3: if a vertex of 𝒞 is φ(T(2;p′,q′)) for some φ ∈ Aut(F), its trefoil-type word is A by item 2, so φ induces an automorphism of H and the symmetrized classes of x^{p′}y^{q′} and K₀ agree; apply Theorem 2(a). ∎

**Theorem 6\* (the third form; proved here by the same method).** For k ≥ 1 let P₀ = 2k+1 and Q ∈ {6k+2, 6k+4}, so that T*(P₀,−Q) = {x^{P₀}y^{−Q}, x²(Xy)³} is the pair of Theorem 4 before applying ν. Put P*(c,p,M | Q; f) := {S(p, c+f, Q), S(M, f, 3)}, U*(c,p,M) = (c+p, p, M+3p), V*(c,p,M) = (c+M, p−QM, M). The component 𝒞* of T*(P₀,−Q) = P*(1,−P₀,2 | Q; −1) in 𝔖 is exactly the set of P*(c,p,M | Q; f) with (c,p,M) in the ⟨U*,V*⟩-orbit of (1,−P₀,2) and f = −(1+M)/3. Every vertex has |p| ≥ 3 and M ≡ 2 (mod 3); the 3-word is of trefoil type iff M = 2 iff the vertex is {W, xyXyXy} with W equal, in ⟨x,w | x²w³⟩ (w = Xy), to the killer up to inversion; all other vertices have |M| ≥ 7. There is no primitive word, no analogue of Lemma S and no flip. Consequently the component of ν(T*(P₀,−Q)) in the graph ν(𝔖) of (x²y)-shared torus-shaped pairs contains no trivialization and no automorphic image of a member of T(2;·) of another level.

*Proof.* Notation: y₁ = x^{c+f}y, w = x^f y; the words are x^p y₁^Q = x^p(x^c w)^Q and x^M w³ = x^{M−c}y₁x^{−c}y₁x^{−c}y₁; D* = 3p − Q(M−3c) = ±1; 3f + M = −1 is invariant.
(1*) *3-word frozen.* Let M ≡ 2 (mod 3), |M| ≥ 2, ζ = x^M = w⁻³ in ⟨x,w | x^M w³⟩, K = x^p(x^c w)^Q, Q ≥ 4, and assume (N) c ≢ 0, p ≢ 0, p+c ≢ 0 (mod M), or (D) M = 2 and c, p odd. Then x^a(x^b w)ⁿ is conjugate to K iff (a,b,n) = (p−μQM, c+μM, Q), and to K⁻¹ iff (−a,b,−n) is of this form. Indeed, for n ≥ 1 the image in C_|M| * C₃ of x^a(x^b w)ⁿ has ≤ 2 syllables if b ≡ 0; w-exponent necklace 1ⁿ and x-necklace [a+b, b^{n−1}] if b ≢ 0 ≢ a+b; and w-necklace [2, 1^{n−2}] (one syllable if n = 1) if b ≢ 0 ≡ a+b. In case (N) K has necklaces 1^Q and [p+c, c^{Q−1}] (not constant), so n = Q, b ≡ c, a ≡ p, and x^{p+λM}(x^{c+μM}w)^Q = Kζ^{λ+μQ} forces λ = −μQ (Lemma J0). In case (D) K has w-necklace [2, 1^{Q−2}], so a, b are odd and n = Q, with the same computation. For n ≤ −1 pass to the inverse word: K⁻¹ has w-necklace 2^Q resp. [2^{Q−2}, 1], which is not of the forms above for Q ≥ 4.
(2*) *Q-word frozen.* Let |p| ≥ 2, Q ≥ 4, gcd(p,Q) = 1 and c ≢ 0, M ≢ 0, M ≢ c (mod p). Exactly as in Lemma 6.2 (6 syllables, x-necklace [M−c, −c, −c] not constant, a syllable y₁² is impossible), x^a(x^{−b}y₁)ⁿ is conjugate to (x^M w³)^{±1} in ⟨x,y₁ | x^p y₁^Q⟩ iff, up to inversion, (a,b,n) = (M+3κp, c+κp, 3).
(3*) *Orbit.* M̃ := M − 3c = (3p − D*)/Q is U*-invariant with |M̃| < |p|, and P̃ := p + Qc = (D* + QM)/3 is V*-invariant. The vertices V*^μ(1,−P₀,2) = (1+2μ, −P₀−2μQ, 2) have c, p odd, |p| > max(|c|, |c−2|, 2) and c ∉ {0,2}, so (D) and the hypotheses of (2*) hold and |p| > |M|. A U*-step from a vertex (c₀,p,M₀) with |p| > |M₀| satisfying the hypotheses of (2*) gives |M| ≥ 3|p| − |M₀| > 2|p|, hence |M| ≥ 7; residues mod p are unchanged; 3c ≡ −M̃ (mod M), so c ≡ 0 would force M | M̃, impossible as 0 < |M̃| < |M|; M ∤ p; and p + c ≡ 0 would force M | 3p − M̃, a nonzero number of absolute value < 4|p| < 2|M|, hence 3p − M̃ = τ(M₀ + 3κp), i.e. either 3|p| ≤ |M₀| + |M̃| < 2|p| or M̃ = −τM₀, which means c₀ = 0 or 3c₀ = 2M₀ — impossible since c₀ ≢ 0 (mod p) and 3 ∤ M₀. So (N) holds. A V*-step from a vertex with |M| > |p₁| satisfying (N) gives |p| > (Q−1)|M|; residues mod M are unchanged; and c ≡ 0, c ≡ M (mod p) would force p | P̃ resp. p | (2QM − D*)/3, nonzero numbers of absolute value < |p|; M ≢ 0 as 0 < |M| < |p|.
By (1*)–(3*) every neighbour of a vertex of the stated form is again of this form, and M = 2 occurs only at the vertices V*^μ(1,−P₀,2), whose Q-word equals the killer in ⟨x,w | x²w³⟩. The last sentence follows from Theorem 2(a) as in Theorem 6. ∎

**Remark 6.4 (the flip is a realized automorphism).** Case (β) with μ = −1 says x^p(xy)^{−q} ~ x^p y^q in H (indeed (xy)⁻¹ = u⁻¹ and y = v⁻¹ are conjugate by t). Since φ₀ = (x ↦ X, y ↦ xy) fixes A up to rotation and sends x^p y^q to the inverse of a rotation of x^p(xy)^{−q}, φ₀(T(2;p,q)) ~AC T(2;p,q) by one A-frozen move, for all (p,q). Up to an inner automorphism φ₀ is the reflection ρ = (x ↦ x⁻¹, y ↦ yx) that note N found on X by search (`n_x_r1_aut.json`); here it is uniform in (p,q) and comes with a reason. More generally an automorphism of F that preserves A up to conjugacy and inversion is AC-realized on (w, A) whenever the necklace of w is symmetric under the induced symmetry (all two-block necklaces are). This is a special case of what TH02 studies; I do not pursue it.

**What Theorems 6 and 6\* are not.** 𝔖 and ν(𝔖) are small, explicitly restricted move classes (one fixed shared primitive — the order-3 generator x resp. the order-2 generator x²y — and torus-shaped words only). The theorems are not AC invariants and gives no evidence that the levels are AC-distinct; by Proposition 5(iii) no such invariant statement can be proved without disproving the conjecture.

## 7. Failed attempts and what remains open (precise reasons)

- **AK(n) inside T(2;·)?** No: Theorem 2(b) is a proof that this fails for n ≥ 2, even up to automorphisms. AK(n) and T(2;·) meet only as two edges of the family K(a,b,c) of Theorem 3.
- **Level shift through the killer's torus group, x-shared words.** Fails by Theorem 6. Record of an error caught on the way: my first hand classification of the shapes conjugate to the killer (Lemma 6.1) omitted the branch (β) (negative exponent q, c ↦ −c); the two-sided brute-force test in `experiments/th17_shear.py` exposed it, and (β) turned out to be the realized automorphism of Remark 6.4. The final statements are the ones proved above and they agree with the brute force.
- **Level shift through the third form, (x²y)-shared words.** Fails by Theorem 6*: the component is a single shear orbit.
- **All torus-type words, arbitrary bases.** A two-move level shift T(2;p,q) → (K, A′) → (K′, A′) with A′ of trefoil type exists iff some class C_{k′}^± contains a word of torus type T(p,q) with the right partner. Theorem 6 excludes this when the basis contains x. For arbitrary bases I tried (i) Christoffel-word run structure of α³β² (as in G Lemma G4) and (ii) the Fricke trace identity tr(AᴾBᑫ) = U_{P−1}(a)U_{Q−1}(b)c − U_{P−1}(a)U_{Q−2}(b)a − U_{P−2}(a)U_{Q−1}(b)b + 2U_{P−2}(a)U_{Q−2}(b) on SL₂(ℤ) (U Chebyshev, (a,b,c) = traces of α, β, αβ, which satisfy a²+b²+c²−abc = 5 for every basis of F(u,v)); neither was completed. What (ii) shows quickly: if α is elliptic and β parabolic the trace is linear in Q (|tr| = Q or Q ± 1), which is exactly the pattern of the three known forms (types T(3k+1, τ−1), T(3k+2, τ+1), T(2k+1, τ) in the class of |trace| τ); if both are parabolic |tr| = PQ ± 2 (the AK-type words). The hyperbolic cases and the central exponents are **open**. Known torus types in C_k^∓ (j = 6k or 6k+2): T(3k+1, j+1), T(3k+2, j+3), T(2k+1, j+2), their central twists, and for k = 1 also T(2, j+1) (Theorem 2(c): the T(2, j+1)-word xy^{j−1}xY² lies in (1; 2·1^j) for every even j, so it is a killer only at level 1).
- **A symbolic level shift.** None found. By Proposition 5 a uniform one would trivialize C3.

## 8. Experiments (exact commands, outputs from this session; each < 2 min, one core, < 0.3 GB)

```sh
python3 experiments/th17_levels.py --selftest
#  th17_levels self-test passed: 1517 dictionary cases, 74 members, 24 coincidence groups, 320 K-cases
python3 experiments/th17_shear.py --selftest
#  th17_shear self-test passed: 21832 orbit vertices checked, 6 vertices brute-forced
#  th17_shear third-form self-test passed: 13645 orbit vertices checked, 5 vertices brute-forced
python3 experiments/th17_levels.py --cert certificates     # the two one-move certificates of Cor. 2.3
python3 experiments/th17_shear.py --cert certificates      # the two third-form certificates of Thm 4
for f in certificates/th17_*.json; do python3 experiments/elementary_verify.py $f; done    # exit 0 each
#  {"endpoint": ["xxyxxyxYXYXYXYXYXYXYX", "xxyXy"], "moves": 189, "path": "certificates/th17_T2_4_7_to_third_form.json", "peak_total_length": 48}
#  {"endpoint": ["xxyxxyxxyxxyxYXYXYXYXYXYXYXYXYXYXYXYXYX", "xxyXy"], "moves": 574, "path": "certificates/th17_T2_7_13_to_third_form.json", "peak_total_length": 90}
#  {"endpoint": ["xxxxyyyyyyy", "xxyXy"], "moves": 274, "path": "certificates/th17_c3_to_T2_4_7_one_move.json", "peak_total_length": 39}
#  {"endpoint": ["xxxxyyyyyyyyy", "xxyXy"], "moves": 374, "path": "certificates/th17_r74member_to_T2_4_9.json", "peak_total_length": 45}
```

What the self-tests check (all exact, via `g_torus.torus_class`, a complete conjugacy invariant):
- `th17_levels`: Theorem 1 for −20 ≤ p ≤ 20, 3 ≤ q < 40; Lemma S as an equality of classes for −6 ≤ k ≤ 6; the braid form; Theorem 2 on the 48 trivial-group members of levels 0–11, AK(1..24) and the two G5 presentations (exactly 24 coincidence groups: the Lemma S pairs, with AK(1) in C_0^+, (A, xy⁵xY²) in C_1^− and (A, xy⁷xY²) in C_1^+); Theorem 3(1) for a, b ≤ 8, |c| ≤ 2; and Theorem 3(2) against coset enumeration (`f_descent.is_trivial_group`) on the 24 triples with |a−b+6c| = 1, a ≤ 6, b ≤ 12, −1 ≤ c ≤ 2 (the only one with gcd(a,b) > 1 is (5,10,1), and it is the only non-trivial one).
- `th17_shear`: Theorem 4 for k ≤ 7; Theorem 2(c) for i ≤ 11; Lemma 6.3 on all 21,832 triples reached by reduced shear words of length ≤ 5 (exponents ≤ 2) from eight start vertices; and Lemmas 6.1/6.2 by **two-sided** brute force (every shape in a parameter box is tested for conjugacy, and the set found must equal the predicted set) at six vertices: T(2;4,7), two of its U-images (M = 11, −5), one V-image, T(2;5,9) (degenerate killer) and T(2;4,9). The third-form part does the same for Theorem 6*: the orbit conditions (3*) on 13,645 triples from five start vertices, and two-sided brute force at T*(3,−8), one U*-image (M = 11), one V*-image, T*(3,−10) and T*(5,−14).

Certificates (start → target, strict `ordinary-ac-elementary-v1`):

| file | start → target | moves | peak |
|---|---|---:|---:|
| `th17_r74member_to_T2_4_9.json` | (xxyXy, xyyyyyyyxYY) → (x⁴y⁹, xxyXy) | 374 | 45 |
| `th17_c3_to_T2_4_7_one_move.json` | C3 = (xxyXy, xyyyyyxYY) → (x⁴y⁷, xxyXy) | 274 | 39 |
| `th17_T2_4_7_to_third_form.json` | (x⁴y⁷, xxyXy) → ((x²y)³(xy)⁻⁸ reduced, xxyXy) | 189 | 48 |
| `th17_T2_7_13_to_third_form.json` | (x⁷y¹³, xxyXy) → ((x²y)⁵(xy)⁻¹⁴ reduced, xxyXy) | 574 | 90 |

The compiler is note G's `g_cert.acm_edge` (frozen relator θ(x³y²) with θ = (x ↦ x, y ↦ Xy)); nothing is trusted beyond the replay.

## 9. Honest limits

- No result here bears on whether AK(3), C3, X or any level is AC-trivial. Theorems 2, 3(4) and 6 are statements about restricted move classes (trefoil-frozen moves and automorphisms; the graph 𝔖). They are **not** AC invariants.
- Theorems 6 and 6* fix the shared primitive (x, resp. x²y) and allow only torus-shaped words; the passage between the two graphs (Theorem 4) is itself a move outside both. The classification of all torus-type words in a class of a torus-knot group is open (§7).
- Theorems 2(b), 3(4), 6(3) and 6* use Aut(H) = Inn(H)·⟨τ⟩; the short argument in §0 reduces it to the classical description of Aut(C₃*C₂), which is quoted, not re-proved.
- That (x²yXy, xy⁷xY²) belongs to the published component R74 is note G's reading of third-party data; the certificate itself only concerns the two displayed presentations.
- Novelty is not established. The family K(a,b,c) and the braid form are elementary and may well be known.

## 10. Advice to the coordinator (ranked)

1. **Treat "level shift" as equivalent to the C3 problem** (Prop. 5): a uniform shift would trivialize C3 and X. The only genuinely weaker target is a shift between levels ≥ 1, e.g. C3 ~ T(2;7,13); the shortest known handles for it are now the third forms T*(3,−8) (length 17) and T*(5,−14) (length 25).
2. **Record the certified merge** (x²yXy, xy⁷xY²) ~AC X: the presentation that note G reports as a member of R74 is in X's class by plain AC moves (notes G and I linked {R62, R74, X} only through automorphisms).
3. **Classify torus-type words in the classes C_k^∓ for arbitrary bases** (§7). This decides whether any two-move level shift exists and is the same problem as the rigidity of AK(n)'s torus island (TH04); the trace identity on SL₂(ℤ) reduces it to the hyperbolic bases, where exponential growth of the Chebyshev terms should give a finite check per class.
4. **The family K(a,b,c)** gives a two-parameter list of trefoil-killer presentations with AK(n) and T(2;·) on its edges. Cheap experiments: Aut-minimal lengths and cap-limited components of K(2,7,1), K(2,9,1), K(3,8,1), and a test whether any interior member falls into AK(3)'s, C3's or X's class.
5. For any pair with a trefoil-type relator the symmetrized class (c; necklace) is an exact, instantly computable invariant of the pair under automorphisms and trefoil-frozen moves; it should be stored with every such state in future searches (it separates AK(3), C3, X and all levels at once).

## 11. Files written

- `research/research-th17.md` (this note).
- `experiments/th17_levels.py` (dictionary, coincidences, family K; `--selftest`, `--cert`), `experiments/th17_shear.py` (third form, shear orbit, two-sided brute force; `--selftest`, `--cert`).
- `certificates/th17_r74member_to_T2_4_9.json`, `certificates/th17_c3_to_T2_4_7_one_move.json`, `certificates/th17_T2_4_7_to_third_form.json`, `certificates/th17_T2_7_13_to_third_form.json` (54 KB in total).

## References

- Notes A, D, F, G, I, J of this repository (A Lemma 1; D Lemmas D2, D3; F Prop. F3; G Lemmas 1, G0, G4, Thm G1, Prop. G5; I Prop. G, Lemma S, §5, §7; J Lemma J0).
- W. Magnus, A. Karrass, D. Solitar, *Combinatorial Group Theory* (conjugacy in free products; Fricke trace identities).
- O. Schreier, *Über die Gruppen AᵃBᵇ = 1*, Abh. Math. Sem. Hamburg 3 (1924) (automorphisms of torus-knot groups) — quoted, not consulted in this session.
- D. Panteleev, A. Ushakov, *Conjugacy search problem and the Andrews–Curtis conjecture* (ACM moves), as reported in notes A and G.

## Coordinator's check (2026-11-09, Los Angeles time)

- Re-ran `python3 experiments/th17_levels.py --selftest` and `python3 experiments/th17_shear.py --selftest`: pass. All four `certificates/th17_*.json` replay under `python3 experiments/elementary_verify.py`; the coordinator checked their start and target tuples: C3 → T(2;4,7) (274 moves), the R74 member (x²yXy, xy⁷xY²) → X = T(2;4,9) (374 moves; a plain AC equivalence, where research-g and research-i had it only up to an automorphism), and the two "third torus form" certificates.
- Read: the claims table and Theorem 1's braid form x^{3k+1}y^q = Δ^{2k}·u·v^{−(q−1)}; consistent with research-i's Lemma S (re-derived by the coordinator in round 3) and with research-a's necklace 2ⁿ1^{n+1} for AK(n). Not re-derived line by line: Theorems 2–4 and the rigidity Theorems 6, 6*; see the referee note research-th20.md for an independent verdict.
- Scope reminder (as the note says): Theorems 6, 6* concern restricted move classes and are not AC invariants; Proposition 5 shows that a uniform level shift would itself trivialize C3 and X, so that question is as hard as the frontier classes.
