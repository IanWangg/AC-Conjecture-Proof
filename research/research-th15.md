# Research TH15: a self-contained uniform proof that Aut(F₂) is AC-realized on AK(n) — a hidden reflection and a hidden transvection

Date: 2026-11-09 (Los Angeles). Independent research agent TH15 (round 5, theory round).

**Status.** *Proved here (complete symbolic proofs + replayed certificates):* for every n ≥ 1 and every
φ ∈ Aut(F₂), AK(n) is ordinary-AC-equivalent to φ(AK(n)) (Theorem 1). Two independent proofs:
(i) a half-page conceptual one — AK(n) ~AC (β_n, b) with β_n = x⁻¹y⁻⁽ⁿ⁺¹⁾xyⁿ a Baumslag–Solitar
relator; the swap acts on F/⟨⟨b⟩⟩ as an inner automorphism and the transvection x ↦ xy acts on
F/⟨⟨β_n⟩⟩ as an inner automorphism, and these two generate Out(F₂); (ii) closed-form paths of
2n+1 cyclic products for each of the two generators, compiled to strict certificates.
Consequences: the AC class of AK(n) is a union of Aut(F₂)-orbits for all n, so the places where
the repository quoted Panteleev–Ushakov for n ≠ 3 (G1's Aut-form, K1.3, Corollary D7) are now
unconditional; AK(n) ~AC (x⁻¹y⁻⁽ⁿ⁺¹⁾xyⁿ, x²y⁻¹x⁻¹y⁻¹) of length 2n+8 (the length of C's M_n);
every Miller–Schupp presentation has an infinite stabilizer; C's MS-bridge is two generalized
moves (n+3 cyclic products); the generalized-move distance from AK(n) to a(AK(n)) is exactly 3.
*Not achieved:* no AC trivialization of AK(3), no obstruction, no counterexample. Theorem 1 itself
is not new (Panteleev–Ushakov, arXiv:1609.00325, externally reported); contributed here are the
explicit uniform proof, the mechanism and the certificates. No novelty claim.

**Central claims (for the referee).** F = F(x,y), X = x⁻¹, Y = y⁻¹, b = xyxYXY, p_n = xⁿY^{n+1},
q_n = yⁿX^{n+1}, AK(n) = (p_n, b), β_n = XY^{n+1}xyⁿ, σ = (x ↔ y), T = (x ↦ xy, y ↦ y), a = T⁻¹.

| # | statement | label |
|---|---|---|
| 1 | **Theorem 1.** AK(n) ~AC φ(AK(n)) for all n ≥ 1, φ ∈ Aut(F₂) (ordinary AC moves; relators up to conjugation/inversion) | proved here (§2–3); theorem due to Panteleev–Ushakov |
| 2 | **Lemma S.** σ(b) = b⁻¹ and σ(w) ≡ ΔwΔ⁻¹ mod ⟨⟨b⟩⟩ for all w (Δ = xyx): the swap is inner on F/⟨⟨b⟩⟩ | proved here (A's observation; also TH02's "hidden reflection") |
| 3 | **Lemma T (hidden transvection).** For β = x⁻¹y^m x y^{−n'} and k = (n'−m)i: T_k = (x ↦ xy^k) satisfies T_k(β) = y^{−k}βy^k and T_k(w) ≡ y^{mi} w y^{−mi} mod ⟨⟨β⟩⟩. So T_k(β, s) ~AC (β, s) for **every** s; for \|n'−m\| = 1 this holds for all k | proved here |
| 4 | **Lemma H (hub).** β_n ≡ conjugate of p_n mod ⟨⟨b⟩⟩, so AK(n) ~AC (β_n, b); explicitly n cyclic products = 2n+4 elementary moves | proved here; certificate n = 3: 10 moves |
| 5 | **Prop. A / B (closed forms).** (p_n, b) → σ(AK(n)) and (p_n, b) → a(AK(n)) by 2n+1 cyclic products each (peaks 2n+13 and 4n+7) | proved here (tables §4); certificates n = 2..8 |
| 6 | **Cor. 5.** AK(n) ~AC (β_n, xy^{k+1}xYXY) for every k ∈ ℤ; k = −1 gives H_n = (XY^{n+1}xyⁿ, xxYXY), length 2n+8 | proved here; certificates |
| 7 | **Cor. 6.** MS(n,w) ~AC MS(n,w') whenever x⁻¹w' = T_k(x⁻¹w) up to conjugacy; the stabilizer Ŝ(MS(n,w)) ⊆ GL₂(ℤ) is infinite for every w | proved here; 247 generated certificates replayed |
| 8 | **Prop. D.** C's bridge AK(n) ~AC M_n = MS(n, y⁻¹x²y⁻¹) in n+3 cyclic products; M_n = a(β′_n, b) up to rotation | proved here; certificates n = 2..8 |
| 9 | **Prop. E.** In generalized (frozen-relator) moves, σ(AK(n)) is at distance exactly 1 and a(AK(n)) at distance exactly 3 from AK(n), n ≥ 2 | proved here |

A **cyclic product** replaces one relator r by cyc(g·r′) or cyc(r′·g), r′ a rotation of r^{±1},
g a rotation of the other relator or of its inverse; it is a composite of ordinary AC moves
(research-d Lemma D1(a),(b)). cyc = cyclic reduction; rotation = cyclic rotation.

## 1. Previous work read and choice of direction

Read: `README.md` in full; notes A, C in full; D §1–3, §4.5; K §2–3; G §2–3; J §4 (Lemma J0,
Theorem J1); status paragraphs of the others. Tools re-used read-only: `experiments/d_certify.py`
(cyclic-product path → strict certificate) and `experiments/elementary_verify.py` (replayer).
Facts used (re-verified where used): Lemma D1(a),(b); Lemma D2 (letterwise transport of an AC
sequence by φ ∈ Aut(F₂)); the subgroup argument inside Lemma D6; Lemma G0 (a quotient-conjugacy
move is an AC composite).

**Choice of direction.** I kept the seed: Lemma D6 (n = 3) rests on seven search-found
certificates and for n ≠ 3 the repository quotes Panteleev–Ushakov. Decoding D's n = 3 certificate
for x ↦ xY (7 cyclic steps: relator sequence p₃, x²Y³xyXY, xY³xy²XY | XY⁴xy³ | x²y²XY⁵ | yxyXX |
…) showed a pattern linear in n, exactly as C found for the MS bridge; this gave Prop. B. Asking
*why* a Baumslag–Solitar relator appears in the middle gave the mechanism (Lemma T) and the short
proof. New relative to A–O: the uniform paths, Lemma T, Lemma H and Corollaries 5–6 (D has n = 3
by search; G, K, I quote the external theorem for n ≠ 3).

**Overlap found during the round (honest note).** TH02's draft (read at 04:24 UTC, after my Props
A, B were done) contains the same "stabilizer principle" (its Lemma 0 = my Lemma M) and the swap
on (b, s) as a "hidden reflection"; it proves that hidden reflections lie in an index-2 subgroup
of GL₂(ℤ) and *never* realize x ↦ xy^{±1}. Lemma T is the complementary mechanism (a BS relator
instead of a T(2,n)-type relator) and is what makes the full group appear for AK(n). TH18's draft
contains the conjugacy classification in BS(n,n+1) (its T2, T4), which agrees with the lattice
computation in Remark 4.3 below; as far as that draft shows, TH18 does not state Lemma T or Theorem 1.

## 2. The mechanism (proved here)

For a pair R = (r, s) put S(R) = {φ ∈ Aut(F₂) : φ(R) ~AC R}, where φ(R) = (φ(r), φ(s)).

**Lemma 0 (S is a class invariant and a group; from D2/D6, N).** (a) If R ~AC R′ then S(R) = S(R′).
(b) S(R) is a subgroup of Aut(F₂) containing Inn(F₂).
*Proof.* Applying φ letterwise to an AC sequence R → R′ gives an AC sequence φ(R) → φ(R′) (Lemma
D2: inversion and multiplication commute with φ; conjugation by a letter g becomes conjugation by
the letters of φ(g)). So φ(R) ~ R iff φ(R′) ~ R′: (a). If α, β ∈ S(R) then αβ(R) ~ α(R) ~ R
(transport R ~ β(R) by α) and α⁻¹(R) ~ α⁻¹(α(R)) = R; conjugating both relators by a word is an
AC composite: (b). ∎

**Lemma M (one frozen relator; = G0 plus the stabilizer principle, cf. TH02 Lemma 0).** Let r, s
be words, φ ∈ Aut(F₂), and suppose (i) φ(s) = h s^ε h⁻¹ in F and (ii) φ(r) ≡ g r^δ g⁻¹ modulo
⟨⟨s⟩⟩ (ε, δ = ±1). Then (r, s) ~AC (φ(r), φ(s)). In particular this holds for every r if φ
satisfies (i) and induces an inner automorphism of F/⟨⟨s⟩⟩. With φ = id: (r, s) ~AC (r′, s)
whenever r′ is conjugate to r^{±1} modulo ⟨⟨s⟩⟩.
*Proof.* By (ii), φ(r) = g r^δ g⁻¹ · Π_j h_j s^{ε_j} h_j⁻¹ in F. Conjugate r by g, invert if δ = −1;
for each j conjugate s by h_j, invert if ε_j = −1, multiply the first relator by it on the right,
and undo the change of s. Finally conjugate s by h and invert if ε = −1. ∎

**Lemma S (the swap is inner modulo b).** σ(b) = b⁻¹, and with Δ = xyx: ΔxΔ⁻¹ = b·y and
ΔyΔ⁻¹ = x·b⁻¹ in F. Hence σ(w) ≡ ΔwΔ⁻¹ mod ⟨⟨b⟩⟩ for every w, and σ ∈ S((r, b)) for every r.
*Proof.* σ(b) = yxyXYX = b⁻¹. ΔxΔ⁻¹ = xyx·x·XYX = xyxYX = (xyxYXY)y. ΔyΔ⁻¹ = xyx·y·XYX =
x(yxyXYX). Apply Lemma M with s = b. ∎

**Lemma T (hidden transvection of a Baumslag–Solitar relator).** Let m, n′ ∈ ℤ,
β = x⁻¹y^m x y^{−n′}, T_k = (x ↦ xy^k, y ↦ y). Then (i) T_k(β) = y^{−k}βy^k for all k; (ii) if
k = (n′−m)i, then T_k(w) ≡ y^{mi} w y^{−mi} mod ⟨⟨β⟩⟩ for every w. Hence T_{(n′−m)i} ∈ S((r, s))
whenever s is conjugate to β^{±1}, for every r. For β_n = x⁻¹y^{−(n+1)}xyⁿ (m = −(n+1), n′ = −n,
n′−m = 1): T = T₁ acts on Γ_n := F/⟨⟨β_n⟩⟩ as conjugation by y^{−(n+1)}; explicitly
Y^{n+1}·x·y^{n+1} = (xβ_nX)·xy in F.
*Proof.* (i) T_k(β) = y^{−k}x⁻¹·y^m·xy^k·y^{−n′} = y^{−k}(x⁻¹y^m x y^{−n′})y^k. (ii) Modulo β,
y^m x = x y^{n′}, so y^{mi}x = xy^{n′i} and y^{mi}·x·y^{−mi} = xy^{(n′−m)i} = T_k(x); y is fixed by
both maps. The displayed identity: x·XY^{n+1}xyⁿ·X·xy = Y^{n+1}xy^{n+1}. Apply Lemma M. ∎

**Lemma H (the Baumslag–Solitar hub).** Modulo ⟨⟨b⟩⟩, xyX ≡ Yxy (because xyX·(Yxy)⁻¹ = xyXYXy is a
rotation of b⁻¹). Hence the rotation Yⁿ·xyⁿX·Y of β_n is ≡ Yⁿ·Yxⁿy·Y = Y^{n+1}xⁿ, a rotation of
p_n. So β_n is conjugate to p_n modulo ⟨⟨b⟩⟩ and **AK(n) ~AC (β_n, b)** for every n ≥ 1 (Lemma M,
φ = id). Likewise for the Miller–Schupp orientation β′_n = x⁻¹yⁿxy^{−(n+1)}: its rotation
yⁿ·xY^{n+1}X ≡ yⁿ·YX^{n+1}y, a rotation of q_n ≡ Δp_nΔ⁻¹; so AK(n) ~AC (β′_n, b) as well. ∎

## 3. Theorem 1 and its short proof (proved here)

**Lemma N (generation).** Aut(F₂) is generated by σ, T and Inn(F₂).
*Proof.* By Nielsen (classical) Aut(F₂) is generated by σ, ε_x = (x ↦ X) and T. With a = T⁻¹ and
c = σTσ = (y ↦ yx) one computes on generators (aca)(x) = a(c(xY)) = a(Y) = Y and
(aca)(y) = a(yx) = yxY; hence (acaσ)(x) = yxY and (acaσ)(y) = Y, i.e. acaσ = Inn_y∘ε_y with
ε_y = (y ↦ Y), and ε_x = σε_yσ. (Checked mechanically in `th15_transport.py --selftest`.) ∎

**Theorem 1.** For every n ≥ 1 and every φ ∈ Aut(F₂): AK(n) ~AC φ(AK(n)).
*Proof.* By Lemma H and Lemma 0(a), S(AK(n)) = S((β_n, b)). By Lemma S (frozen relator b, moved
relator β_n) σ ∈ S((β_n, b)); by Lemma T (frozen relator β_n, moved relator b) T ∈ S((β_n, b)).
By Lemma 0(b) and Lemma N, S((β_n, b)) = Aut(F₂). ∎

So the whole of Out(F₂) = GL₂(ℤ) is produced by two "hidden" symmetries sitting on the two
relators of one presentation of the class: σ on b (one b-frozen generalized move) and T on β_n
(one β_n-frozen generalized move). In ACM terms: σ costs 1 move from AK(n); T costs 3
(AK(n) → (β_n, b) → (β_n, T(b)) → T(AK(n))).

## 4. Closed-form paths (proved here; second, certificate-level proof of Theorem 1 for n ≥ 2)

Every line below is an identity of freely reduced words valid for all n in the stated range;
"~" means equal as cyclic words. `experiments/th15_aut_family.py --check 2 200` re-verifies each
identity, and that every multiplier is a rotation of the frozen relator or its inverse.

**Proposition A (swap; n ≥ 1).** With b frozen, 2n+1 cyclic products take p_n to q_n; all
multipliers are rotations of b⁻¹ (μ₁ = XYXyxy, μ₂ = yxyXYX, μ₃ = XyxyXY). Since σ(b) = b⁻¹,
this realizes σ on AK(n). Packaged peak total length 2n+13. Intermediate words:

    w_k  = y^k · xy · x^(n−k+1) Y^(n+1) · XYX      (1 ≤ k ≤ n; = y^k Δ x^(n−k) Y^(n+1) Δ⁻¹; length 2n+7)
    w′_j = yⁿ X^(j−1) · yx · Y^(n+1−j) · XYX       (1 ≤ j ≤ n; = yⁿ X^j Δ Y^(n+1−j) Δ⁻¹; length 2n+5)

| step | product | result |
|---|---|---|
| A1 | μ₁·p_n = XYXyxy·xⁿY^{n+1} | ~ w_1 |
| A2 (1 ≤ k ≤ n−1) | μ₂·(xy·x^{n−k+1}Y^{n+1}XYX·y^k) = yxy·x^{n−k}Y^{n+1}XYX·y^k (XYX·xyx cancels) | ~ w_{k+1} |
| A3 | μ₂·(xyx·Y^{n+1}XYX·yⁿ) = yxYⁿXYX·yⁿ | ~ w′_1 |
| A4 (1 ≤ j ≤ n−1) | μ₃·(yx·Y^{n+1−j}XYX·yⁿX^{j−1}) = XyxY^{n−j}XYX·yⁿX^{j−1} (XyxyXY·yx = Xyxy) | ~ w′_{j+1} |
| A5 | μ₃·(yxYXYX·yⁿX^{n−1}) = XX·yⁿX^{n−1} (XyxyXY·yxYXYX = XX) | ~ q_n |

In each row the second factor is a rotation of the current word (w_k, w_n, w′_j, w′_n). This is
Lemma S spelled out: Δ is pushed through p_n one letter at a time (Δx = yΔ, ΔY = XΔ mod b). ∎

**Proposition B (a = (x ↦ xY); n ≥ 2).** 2n+1 cyclic products take (p_n, b) to
((xY)ⁿY^{n+1}, yxyXX); a(p_n) = (xY)ⁿY^{n+1} and a(b) = xxYXY = (yxyXX)⁻¹, so this realizes a.
Packaged peak 4n+7. Words:

    u_k = x^(n−k) Yⁿ x y^k X Y   (0 ≤ k ≤ n−1; u_0 = p_n; length 2n+3 for k ≥ 1)
    b₁  = X Y^(n+1) x yⁿ = β_n ,   b₂ = y x y X X
    v_m = x x y^(n−1−m) X Y^(n+2) (xY)^m   (0 ≤ m ≤ n−2; length 2n+4+m),   v_(n−1) = (xY)ⁿ Y^(n+1)

| phase (frozen) | product | result |
|---|---|---|
| I (b), 0 ≤ k ≤ n−2 | (X u_k x)·μ₃ = x^{n−k−1}Yⁿxy^k·XYx·XyxyXY = x^{n−k−1}Yⁿxy^k·yXY (for k = 0: x^{n−1}Y^{n+1}x·XyxyXY = x^{n−1}YⁿxyXY) | = u_{k+1} |
| II (u_{n−1}) | (X u_{n−1} x)·μ₃ = Yⁿxy^{n−1}XYx·XyxyXY = YⁿxyⁿXY; the *second* relator (μ₃, a rotation of b⁻¹) is replaced | ~ b₁ |
| III (b₁) | (Y^{n+1}xyⁿX)·u_{n−1} = Y^{n+1}xyⁿX·xYⁿxy^{n−1}XY = Y^{n+1}·xx·y^{n−1}XY | ~ v_0 |
| IV (v_0) | (xyⁿXY^{n+1})·(y^{n+1}xY^{n−1}XXy) = xyⁿ·Y^{n−1}XXy = xyXXy; first factor a rotation of b₁, second of v_0⁻¹ | ~ b₂ |
| V (b₂), 0 ≤ m ≤ n−2 | (YxxYX)·(x y^{n−1−m}XY^{n+2}x(Yx)^m) = Yxx·y^{n−2−m}XY^{n+2}x(Yx)^m; YxxYX is a rotation of b₂⁻¹, the second factor the rotation of v_m by one letter | ~ v_{m+1} (for m = n−2: YxY^{n+2}x(Yx)^{n−2} ~ (xY)ⁿY^{n+1}) |

Count: (n−1)+1+1+1+(n−1) = 2n+1. Lengths: phase I 2n+9; (u_{n−1}, b₁) 4n+6; (v_0, b₁) 4n+7;
(v_0, b₂) 2n+9; phase V ≤ 3n+7. ∎

**Reading Prop. B through §2.** Phase I continued one more step would give (b₁, b) = the hub of
Lemma H; phases III–IV are Lemma T (v_0 is a conjugate of b modulo b₁, and b₂⁻¹ = a(b) is one
further b₁-multiplication away from v_0); phase V is the a-image of phase I. The search-found
n = 3 path of D takes the two shortcuts II and IV (it replaces the frozen relator instead).

**Proposition C (hub path; n ≥ 2).** (p_n, b) → (β_n, b) by the n products of phase I with
k = 0, …, n−1 (the last one is the product of phase II, assigned to the first relator); then,
with β_n frozen, three products take b to a(b):

    (Y^(n+1) x yⁿ X)·b              = Y^(n+1) x y^(n+1) x Y X Y        ~ c₁ = x y^(n+1) x Y X Y^(n+2)
    (x yⁿ X Y^(n+1))·(y^(n+1) x YX Y^(n+2) x) = x y^(n−1) X Y^(n+2) x  ~ v_0
    (Y X y^(n+1) x Y^(n−1))·(y^(n−1) X Y^(n+2) xx) = Y X Y x x          ~ xxYXY = a(b).

The multipliers are rotations of β_n, β_n, β_n⁻¹. So **AK(n) ~AC H_n := (XY^{n+1}xyⁿ, xxYXY)** by
n+3 cyclic products (peak 4n+10); |H_n| = 2n+8. ∎

**Proposition D (C's bridge by n+3 cyclic products; n ≥ 2).** Put f_k = x^k·YX·y^{n−k}·x·Yⁿ
(0 ≤ k ≤ n; f_n = p_n after free reduction, f_0 ~ β′_n = XyⁿxY^{n+1}). With b frozen and the
multiplier YXyxyX (a rotation of b⁻¹): YXyxyX·(xYX·y^{n−k}xYⁿ·x^{k−1}) = YX·y^{n−k+1}xYⁿ·x^{k−1}
~ f_{k−1} for k = n, …, 1 (for k = n the rotation of p_n is x·Y^{n+1}·x^{n−1}). Then, with β′_n
frozen:

    (yⁿ x Y^(n+1) X)·b                              = yⁿ x Yⁿ x Y X Y        ~ c₁′ = x Yⁿ x Y X y^(n−1)
    (x Y^(n+1) X yⁿ)·(Yⁿ x YX y^(n−1) x)            = x Y^(n+2) X y^(n−1) x  ~ v₀′ = x x Y^(n+2) X y^(n−1)
    (X Yⁿ x y^(n+1))·(Y^(n+1) X y^(n−1) xxY)        = X Y x x Y              (a rotation of a(b)).

So AK(n) → (β′_n, b) → M_n = (x⁻¹yⁿxy^{−(n+1)}, x⁻¹y⁻¹x²y⁻¹) by n+3 cyclic products (peak 4n+7):
C's theorem, with M_n = a(β′_n, b) up to rotation. (C's own certificate is shorter in
elementary moves — 32 against 57 for n = 3; the gain here is the two-move structure.) ∎

**Proposition E (generalized-move distances; n ≥ 2).** Call a *generalized move* the replacement
of one relator by a word conjugate to it or its inverse modulo the other (Lemma M with φ = id),
and compare pairs up to conjugation, inversion and interchange of relators. Then σ(AK(n)) is at
distance exactly 1 from AK(n), and a(AK(n)) at distance exactly 3.
*Proof.* Upper bounds: Lemma S; and AK(n) → (β_n, b) → (β_n, a(b)) → (a(p_n), a(b)) (Lemma H,
Lemma T, and the a-image of Lemma H, using a(β_n) = yβ_nY). Lower bound for a: exponent vectors
are ab(p_n) = (n, −n−1), ab(b) = (1, −1), ab(a(p_n)) = (n, −2n−1), ab(a(b)) = (1, −2), so no
relator of a(AK(n)) is conjugate in F to a relator of AK(n)^{±1}: both relators must change, and
two moves on the same relator compose to one. Shape (p_n, b) → (p_n, b′) → (p″, b′): b′ must be
conjugate in F to a(b)^{±1} or a(p_n)^{±1} and in G_n = ⟨x,y | xⁿ = y^{n+1}⟩ to b^{±1}. But the
image of a(b) = xxYXY in C_n * C_{n+1} has cyclic syllable length 4 (n ≥ 3) or 2 (n = 2), not 6;
and under G_n → ℤ (x ↦ n+1, y ↦ n) a(p_n) ↦ −n² ≠ ±1 = image of b^{±1}. Shape
(p_n, b) → (p′, b) → (p′, b″): p′ must be conjugate to p_n^{±1} in B. Under B → ℤ, a(p_n) ↦ −(n+1)
≠ ±1; and under A's map B → C₂ * C₃ = ⟨s⟩ * ⟨t⟩ (x ↦ t²s, Y ↦ ts, X ↦ st) one gets
xxYXY ↦ t²st²s·ts·st·ts = t²st², of cyclic syllable length 2 ≠ 4n+2 = that of p_n (A, Lemma 1).
Finally σ(AK(n)) ≠ AK(n) up to conjugation, inversion and interchange (ab(q_n) = (−n−1, n)), so
its distance is exactly 1. ∎

**Remark 4.3 (the class of b in Γ_n; consistent with TH18's T4, which has the full
classification).** In Γ_n, y^{n+1}x = xyⁿ gives three slide rules on words xy^{a}xy^{b′}Xy^{c′}:
(a, b′) → (a+(n+1), b′−n), (b′, c′) → (b′+n, c′−(n+1)), (c′, a) → (c′+(n+1), a−n) (the last after
a cyclic rotation). Applying all three once changes (a, b′, c′) to (a+1, b′, c′): this is Lemma T
again, since T(xy^{a}xy^{b′}Xy^{c′}) = xy^{a+1}xy^{b′}Xy^{c′}. The three displayed products of
Prop. C are these three slides with k = −1 applied to b = (1, −1, −1).

## 5. Corollaries (proved here unless marked)

**Corollary 2 (the class is Aut(F₂)-invariant; Corollary D7 for all n).** Let n ≥ 1. If
R ~AC AK(n) then φ(R) ~AC AK(n) for every φ ∈ Aut(F₂). Hence if U has in its AC class a state
whose Aut(F₂)-orbit meets the AC class of AK(n), then U ~AC AK(n): automorphism-orbit matching
(Whitehead canonical forms) is a valid equivalence test against AK(n) for every n.
*Proof.* φ(R) ~ φ(AK(n)) by Lemma D2 and φ(AK(n)) ~ AK(n) by Theorem 1. ∎

**Corollary 3 (G1's Aut-form, now unconditional).** For every n ≥ 1,
AK(n) ~AC (W_n, x²y⁻³), W_n = (xy)ⁿx((yx)ⁿy)⁻¹, i.e. AK(n) ≅_AC ⟨x,y | (xy)ⁿx = y(xy)ⁿ, x² = y³⟩.
*Proof.* G1: AK(n) ~AC (ψ(W_n), b), and b is a rotation of ψ(xxYYY); apply Corollary 2 with ψ⁻¹. ∎

**Corollary 4 (K1.3, I, G).** Every Aut(F₂)-image of P_n = (xyxYYXy, xⁿYXyy) (K1), of
M_n = MS(n, y⁻¹x²y⁻¹) (C) and of every other certified member of AK(n)'s class is AC-equivalent
to AK(n), for all n ≥ 2, without the external theorem. (K's "Whitehead-canonical form"
(XⁿYYxy, XYXYxyy) is P_n itself up to rotation and inversion — checked for n = 3..7 — so that
particular sentence of K1.3 never needed an automorphism.)

**Corollary 5 (a ℤ-family through the hub).** For all n ≥ 1 and k ∈ ℤ:

    AK(n) ~AC (β_n, T^k(b)) = (x⁻¹y⁻⁽ⁿ⁺¹⁾xyⁿ, x y^(k+1) x y⁻¹ x⁻¹ y⁻¹)   (cyclically reduced: |k+1|+5 letters),

i.e. AK(n) ≅_AC ⟨x,y | x⁻¹y^{n+1}x = yⁿ, xy^{k+1}x = yxy⟩. For k = −1 this is H_n (length 2n+8;
for n = 3: (XYYYYxyyy, xxYXY), length 14); for k = 0 the hub (length 2n+9).
*Proof.* AK(n) ~ (β_n, b) (Lemma H) ~ T^k(β_n, b) (Lemma T) = (Y^kβ_ny^k, T^k(b)), and
T^k(b) = xy^k·y·xy^k·Y·Y^kX·Y = xy^{k+1}xYXY. ∎

**Corollary 6 (Miller–Schupp presentations have a hidden transvection).** Write
MS(n, w) = (x⁻¹yⁿxy^{−(n+1)}, x⁻¹w) for an arbitrary word w (C's convention). For every n ≥ 1,
every w and every k ∈ ℤ: MS(n, w) ~AC MS(n, w_k), where x⁻¹w_k := y^k·T_k(x⁻¹w)·y^{−k}, i.e.
w_k = w(xy^k, y)·y^{−k}. Consequently T ∈ S(MS(n, w)): the stabilizer Ŝ(MS(n,w)) ⊆ GL₂(ℤ)
contains the infinite cyclic group generated by the transvection [T], for every w.
*Proof.* Lemma T with β = β′_n (m = n, n′ = n+1): T_k(β′_n) = y^{−k}β′_ny^k and T_k is inner on
F/⟨⟨β′_n⟩⟩ (conjugation by y^{nk}). ∎

**Corollary 7 (C's bridge is two generalized moves).** T(x⁻¹y⁻¹x²y⁻¹) = YXYxyx is a rotation of
b. Hence M_n = (β′_n, XYxxY) ~AC (β′_n, b) by one β′_n-frozen move (Corollary 6, k = 1) and
(β′_n, b) ~AC (q_n, b) ~AC AK(n) by b-frozen moves (Lemmas H, S). C's ten-step prefix and
linear tail is an elementary expansion of this.

**Remark 5.1 (what this says about stabilizers in general).** TH02's draft states (its Prop. 7,
not re-checked by me) that "hidden reflections" (relators of type T(2,n)) generate only subgroups
of an index-2 subgroup of GL₂(ℤ) and never give a Nielsen transvection. Lemma T supplies the missing kind of hidden symmetry: any
class containing a pair one of whose relators is θ(x⁻¹y^m x y^{−n′}) with m ≠ n′, θ ∈ Aut(F₂),
has an **infinite** stabilizer (it contains θT_{n′−m}θ⁻¹). For N's chirality question this gives
a concrete test: if the AC class of C4 contains a relator of Baumslag–Solitar type (m ≠ n′) in
any basis, then Ŝ(C4) is infinite, which would decide N's dichotomy "exactly D₆ or infinite"
(it would not by itself decide whether Ŝ(C4) is all of GL₂(ℤ)). Not tested here.

**Remark 5.2 (H_n versus M_n; no length record).** M_n = (β′_n, XYxxY) is a(β′_n, b) up to
rotation, and H_n = (β_n, xxYXY) is a(β_n, b) up to rotation; β_n is a rotation of ε_x(β′_n).
Both have length 2n+8, one more than AK(n); for n = 3 they are further length-14 members of
AK(3)'s class (besides P₃). Nothing here shortens AK(n).

## 6. Failed attempts and what they showed

1. **Two generalized moves with torus-type frozen relators (the seed's first suggestion).** I
   first tried (p_n, b) → (p_n, φ(b)) → (φ(p_n), φ(b)) and the mirror shape, deciding conjugacy
   by Lemma J0. This is impossible for φ = a (Proposition E proves it for every n ≥ 2): the
   syllable length of a(b) in C_n * C_{n+1} is 4, not 6. So a(AK(n)) is not reachable by two
   generalized moves; an intermediate relator other than the two torus-knot relators is needed,
   and the Baumslag–Solitar relator β_n is the one D's search had found implicitly.
2. **Inversions as generators.** ε = (x ↦ X, y ↦ Y) is free: ε(p_n) = Xⁿy^{n+1} and
   ε(b) = XYXyxy are rotations of p_n⁻¹ and b⁻¹. But a single inversion ε_x changes b into a
   different trefoil-type relator and I found no direct symbolic path (D's n = 3 certificate has
   24 cyclic steps without an obvious pattern). It is obtained indirectly: ε_x = Inn∘(σaσTσa)
   (Lemma N), realized by transport (396 elementary moves for n = 3 against D's 170). A short
   uniform path for ε_x is *not* given here.
3. **A peak-optimal swap.** Prop. A has packaged peak 2n+13. D's n = 3 swap has peak 15 = 2n+9,
   which is optimal by Theorem J1. I did not extract the uniform peak-(2n+9) swap (pushing the
   conjugator xy instead of xyx through p_n seems to give words of length ≤ 2n+5, peak 2n+11:
   a hand computation, not checked by script and not claimed).
4. **Nothing towards trivialization.** The hub (β_n, b) and H_n do not shorten AK(n)
   (Remark 5.2). By Remark 4.3 the b-partners modulo β_n of the shape xy^{a}xy^{b′}Xy^{c′}
   include all a ∈ ℤ, b′ ≡ −1 (mod n), c′ ≡ −1 (mod n+1); that there are no others of this
   shape, and that no partner is primitive, is TH18's T4/T3/T5 (for the orientation β′_n) —
   not re-proved here.

## 7. Experiments (exact commands; outputs from this session; < 5 s each, one core, < 100 MB)

    $ python3 experiments/th15_aut_family.py --check 2 120
    closed-form paths verified for n = 2..120: swap 2n+1 cyclic products (peak 2n+13); a = (x->xY)
    2n+1 cyclic products (peak 4n+7); hub (p_n,b)->(beta_n,b)->(beta_n,xxYXY) n+3 products (peak
    4n+10); (p_n,b)->(beta'_n,b)->M_n n+3 products (peak 4n+7); every multiplier is a rotation of
    the frozen relator or its inverse; Lemma S / Lemma T free-group identities hold
    $ python3 experiments/th15_aut_family.py --selftest
    selftest passed (identities n = 2..40; n = 3 certificates replay; corrupted ones rejected)
    $ python3 experiments/th15_aut_family.py --batch 2 8      (35 lines, condensed: elementary moves / peak; all replayed to the exact targets)
    n      2      3      4      5      6      7      8
    swap   22/19  26/21  30/23  34/25  38/27  42/29  46/31
    a      30/21  48/27  63/33  78/39  93/45  108/51 122/57
    hub    8/15   10/17  12/19  14/21  16/23  18/25  20/27
    hubT   35/25  42/31  49/37  56/43  63/49  70/55  77/61
    ms     41/22  57/28  72/34  86/40  100/46 114/52 128/58
    $ python3 experiments/th15_transport.py --selftest
    selftest passed: 7 named maps = words in s, a, A up to inner automorphisms; composed
    certificates for n = 2, 3 replay to the exact targets
    $ python3 experiments/th15_transport.py --batch 2 8
    n=2: all 7 maps verified; moves [22, 30, 51, 104, 83, 279, 272], peaks [19, 21, 21, 23, 21, 33, 33]
    n=3: all 7 maps verified; moves [26, 48, 81, 143, 110, 403, 396], peaks [21, 27, 27, 27, 27, 45, 45]
    n=4: all 7 maps verified; moves [30, 63, 105, 176, 134, 509, 502], peaks [23, 33, 32, 32, 33, 57, 57]
    ...
    n=8: all 7 maps verified; moves [46, 122, 194, 301, 229, 927, 920], peaks [31, 57, 56, 56, 57, 105, 105]
    (order: swap, x_xY, x_xy, y_yx, y_yX, invy, invx; targets = cyclically reduced φ(AK(n)), exact)
    $ python3 experiments/th15_hidden.py --selftest
    selftest passed: 247 hidden-transvection certificates built and replayed (8 BS relators
    x^-1 y^m x y^-n', random partners; M_n -> (b-rotation, beta'_n), n = 2..8; random MS(n,w))

Stored certificates (all pass `python3 experiments/elementary_verify.py certificates/th15_*.json`):

| file | statement | moves / peak |
|---|---|---|
| `th15_ak{2,4,8}_aut_swap.json` | AK(n) → σ(AK(n)) = (yⁿX^{n+1}, yxyXYX) | 22/19, 30/23, 46/31 |
| `th15_ak{2,4,8}_aut_x_xY.json` | AK(n) → a(AK(n)) = ((xY)ⁿY^{n+1}, xxYXY) | 30/21, 63/33, 122/57 |
| `th15_ak4_aut_invx.json`, `th15_ak4_aut_x_xy.json` | AK(4) → (X⁴Y⁵, XyXYxY), → ((xy)³xY⁴, xyyxYXY) (composed) | 502/57, 105/32 |
| `th15_ak3_hub.json` | AK(3) → (XYYYYxyyy, xyxYXY) = (β₃, b) | 10/17 |
| `th15_ak3_hubT.json` | AK(3) → H₃ = (XYYYYxyyy, xxYXY) | 42/31 |
| `th15_ak3_to_ms3.json` | AK(3) → M₃ = (XyyyxYYYY, XYxxY) (Prop. D) | 57/28 |
| `th15_ms3_hiddenT.json` | (XYxxY, β′₃) → (XYxyxY, β′₃): hidden transvection on M₃ | 49/32 |

The n = 3 swap and a certificates are regenerated by `--cert swap 3 OUT.json`, `--cert a 3 OUT.json`
(26 and 48 moves; D's stored ones have 45 and 48). TH20 re-derived Props A, B by hand and with an
independent script (its §2) before this note's proof sections existed.

## 8. Honest limits

- Theorem 1 is Panteleev–Ushakov's theorem; I could not read their proof (the brief describes it
  only as externally reported), so I cannot say how different the argument is. No novelty claim
  for the theorem, for Lemma S (A, TH02) or for Lemma M (G0, TH02's Lemma 0). Lemma T is an
  elementary fact about BS(m,n′) (the map t ↦ ta^{n′−m} is conjugation by a^m); I do not know
  whether its use for AC-equivalences of Miller–Schupp presentations is in the literature.
- Nothing here bears on whether AK(3) is AC-trivial. Theorem 1 only says the invariant "S(R)"
  (N's Ŝ) does not distinguish AK(n) from the trivial presentation, for any n.
- Certificates were generated for n = 2..8 (closed forms checked symbolically to n = 120); the
  statements for all n rest on the displayed identities, each a finite cancellation uniform in n.
- Proposition E counts generalized moves with arbitrary conjugators; it is not a bound on
  ordinary AC length or peak. Remark 4.3 is a consistency remark, not a classification.
- The elementary-move counts are those of `d_certify.py`'s compilation; no minimality claim.

## 9. Advice to the coordinator (ranked)

1. **Replace the external dependency.** Wherever the README / G / K / I say "by Panteleev–Ushakov
   (externally reported)" for n ≠ 3, cite Theorem 1 here (two generators, 2n+1 cyclic products
   each, certificates). D's Lemma D6 for n = 3 is also covered (independent second proof).
2. **Merge with TH02 and TH18.** The three notes fit together: TH02's hidden reflections
   (relators of type T(2,n)), Lemma T's hidden transvections (relators of Baumslag–Solitar type,
   m ≠ n′) and TH18's conjugacy classification in BS(n,n+1). A joint statement: "S(R) contains
   the hidden symmetries of every relator occurring in any pair of the class". For AK(n) these
   already generate everything; for C4 only reflections are known (D₆).
3. **A concrete test for the chirality question (N).** Scan C4's stored forward set for relators
   of Baumslag–Solitar type θ(x⁻¹y^m x y^{−n′}), m ≠ n′ (candidate recognizer: Whitehead-reduce
   the cyclic word and look for a minimal form with exactly one x and one X; not implemented or
   proved complete here). One hit makes Ŝ(C4) infinite (Remark 5.1).
   Likewise for C3, P1, P2 this would explain I's search-found transvections symbolically.
4. **Do not expect more for AK(3) from symmetry.** All of GL₂(ℤ) is realized and costs nothing
   conceptually; the hub adds no shorter presentation. The remaining value of the hub is as a
   third exact arena (after B and G_n) for frozen-relator searches: with β_n frozen, conjugacy
   is decidable with unbounded conjugators (TH18's T2), exactly as G did for torus relators.

## References

- D. Panteleev, A. Ushakov, *Conjugacy search problem and the Andrews–Curtis conjecture*,
  arXiv:1609.00325 (Groups Complexity Cryptology 2019) — externally reported: Aut(F₂) is
  AC-realized on AK(n); ACM moves.
- J. Nielsen, *Die Isomorphismengruppe der freien Gruppen*, Math. Ann. 91 (1924) — generators of
  Aut(F₂) (classical).
- C. F. Miller III, P. E. Schupp, *Some presentations of the trivial group*, Contemp. Math. 250
  (1999) — the family MS(n,w) (externally reported).
- Repository notes: A (Δ conjugates x to y in B), C (MS bridge), D (Lemmas D1, D2, D6; n = 3
  certificates), G (Lemma G0, Theorem G1), J (Lemma J0, Theorem J1), K (Theorem K1), N (Ŝ);
  round-5 drafts TH02 (Lemma 0, hidden reflections), TH18 (conjugacy in BS(n,n+1)), TH20 (referee).
