# Research TH02: hidden reflections — the mechanism behind the realized automorphisms

Date: 2026-11-09 (Los Angeles). Independent research agent TH02 (round 5, theory round).

**Status.** **No AK(3) trivialization, no proof of non-triviality, no counterexample, nothing on the full conjecture.** What is achieved: the automorphisms that earlier notes found *by search* in the stabilizers Ŝ(U) = {M ∈ GL₂(ℤ) : φ_M(U) ~AC U} are explained by one symbolic mechanism, proved here and compiled to replayable certificates with no search. Every statement is labelled *proved here*, *experiment* (exact bounds), *externally reported*, or *open*.

**Central claims (all for ordinary AC moves; F = F(x,y), X = x⁻¹, Y = y⁻¹).**

| # | statement | label |
|---|---|---|
| 1 | **Hidden reflection.** If (u,v) is a basis of F, n ∈ ℤ, and r is conjugate to (u²vⁿ)^{±1}, then β = (u ↦ u⁻¹v⁻ⁿ, v ↦ v) satisfies β(r,s) ~AC (r,s) for **every** word s. β acts as the identity on F/⟨⟨r⟩⟩; its matrix is the reflection with (−1)-eigenvector ab(r) and (+1)-eigenvector [v] | proved here (Thm 1); 360 generated certificates replayed |
| 2 | N's group D₆ ⊆ Ŝ(C4) is exactly ⟨β_A, β_w⟩, the hidden reflections of the two relators of C4 = (x⁵z², w²y⁵), z = x⁻¹y, w = xy⁻²; D's swap on AK(3) is the hidden reflection of the braid relator, and it is realized on (xyxYXY, s) for every s, in particular on AK(n) for all n | proved here (Cor. 2, Thm 5); certificates |
| 3 | **Double form.** T(a;2a,q) ~AC D(a;q) := (xY²xy^{q−2}, xᵃyXy) for all a, q (one ACM move, two insertions) | proved here (Lemma 3) |
| 4 | **Trace formula.** For a pair of T(2,·)-type relators with exponent determinant ±1, tr(R₁R₂) = 2 − D, D = det(v₁,v₂)·det(ρ₁,ρ₂) odd; ⟨R₁,R₂⟩ is finite iff D ∈ {1,3}. For D(a;q): D = δ := 4a − (a−1)q. So C4 ~ D(4;5) and the C3-form D(2;7) (δ = +1) give D₆, while X = T(2;4,9) ~ D(2;9), T(6;12,5), T(−4;−8,3) (δ = −1) give an infinite dihedral group with a hyperbolic element of trace 3. **The difference between C3/C4 and X is the sign of δ, not the value of a** | proved here (Thm 4); certificates |
| 5 | For every n ≥ 1, Ŝ(AK(n)) ⊇ ⟨−I, swap, [[−1,3],[0,1]]⟩, an infinite group containing a hyperbolic element of trace 3 (uses research-g Theorem G1) | proved here (Thm 5) |
| 6 | **Ŝ(Y) is infinite for Y = T(4;7,5)** (N reported no result for Y): Y ~AC Y′ = (x⁴yXy, xyXY³Xy), a pair of types T(2,5), T(2,3) with D = −3, trace 5 | proved here by certificate (Thm 6) |
| 7 | **Limits of the mechanism.** For a torus relator xᵖy^q (coprime, \|p\|,\|q\| ≥ 2) the stabilizer of the cyclic word up to inversion in Out(F₂) is {±I} if \|p\|,\|q\| ≥ 3 and the Klein four-group {±I, ±β} if min = 2. All hidden reflections lie in the index-2 subgroup Γ_τ = ker(det · sgn(M mod 2)) of GL₂(ℤ); hence they can **never** realize x ↦ x⁻¹, y ↦ y⁻¹, x ↦ xy^{±1} or y ↦ yx^{±1} on any class | proved here (Prop. 7; uses Whitehead's peak-reduction theorem, classical) |
| 8 | In Fwd(C4, 30) (1,246,365 states) 1,195,158 states carry a T(2,n)-type relator; all have n = 5 and their hidden reflections are exactly five matrices, all in D₆. An exact frozen-relator (unbounded-conjugator) search for further T(2,n)-type partners in a box finds only the D₆-images. **No element of Ŝ(C4) outside D₆ was found** | experiment (§5) |
| 9 | Other symmetric relators occur in Fwd(C4, 28): for those fixed by transvections, by ±swap, and for one fixed by x ↦ x⁻¹ (an HNN extension of the trefoil group, Collins' lemma) the required conjugacy is **disproved**; for the relator xxxyXYYXXyyXY (fixed by x ↦ x⁻¹ up to inversion, state of total length 20) it is **open**, and if it holds then Ŝ(C4) ⊇ {M : M₁₂ ≡ 0 mod 3}, of index 4 | proved (Props 9, 10) / open (§4) |

So the best outcome named in the brief (a matrix outside D₆ in Ŝ(C4)) was **not** reached; what is reached is a symbolic proof of everything previously known about Ŝ(C4), Ŝ(X), a new infinite stabilizer (Y), a uniform statement for AK(n), and a precise description of what this mechanism can and cannot produce (§4, §6).

## 0. Previous work read and choice of direction

Read in full: `README.md`, `research-i.md`, `research-n.md`; status paragraphs and coordinator's reviews of A–O; `research-g.md` §2–3 (Lemma 1, Lemma G0, Theorem G1), `research-d.md` (Lemmas D2, D3, D6). Facts used, as verified there: AC equivalence is Aut(F₂)-equivariant (D2); an ACM move (replace r_i by a word conjugate to r_i^{±1} modulo ⟨⟨r_j⟩⟩) is a composite of ordinary AC moves (G0); Ŝ(U) is a subgroup of GL₂(ℤ) = Out(F₂) and Ŝ(φU) = M_φ Ŝ(U) M_φ⁻¹ (N §1–3); conjugacy in ⟨x,y | xᵖy^q⟩ is decided by the syllable necklace in C_p * C_q and the central exponent (G Lemma 1); AK(n) ~AC (ψ(W_n), xyxYXY) (G Theorem G1).

**Direction** (the seed, kept): all known elements of the stabilizers were found by search (N: orbit coincidences in forward sets; D, I: images of generators). I looked for automorphisms φ that fix a relator r as a cyclic word up to inversion and act on F/⟨⟨r⟩⟩ by an inner automorphism: then φ(s) is conjugate to s modulo r for *every* partner s, so φ(r,s) ~AC (r,s) by one ACM move. The surprise is that such φ exist outside {inner, ±I} exactly for relators with an exponent 2 (type T(2,n)), and that both relators of C4 are of this type in two different bases. This is new relative to A–O (N lists the matrices; I and G work with frozen torus relators but never use automorphisms acting trivially on the one-relator quotient) and disjoint from the other nine seeds.

**Notation.** ab(w) ∈ ℤ² is the exponent vector. Matrices are written by rows, columns are the images of x and y (N's convention); automorphisms are composed as maps. A cyclic word is of **type T(2,n)** if it is conjugate to θ(x²yⁿ)^{±1} for some θ ∈ Aut(F₂); we always take n odd, |n| ≥ 3 (|n| = 1 is the primitive case). T(a;p,q) = (xᵖy^q, xᵃyXy), A = xᵃyXy, m = a+1, z = Xy (I's notation).

## 1. The mechanism (proved here)

**Lemma 0 (stabilizer principle).** Let U = (r, s) and φ ∈ Aut(F₂). Suppose (a) φ(r) is conjugate in F to r^{±1}, and (b) φ(s) is conjugate to s^{±1} in G_r := F/⟨⟨r⟩⟩. Then φ(U) ~AC U. In particular, if φ satisfies (a) and induces an *inner* automorphism of G_r, then φ(r,s) ~AC (r,s) for every s.

*Proof.* (φ(r), φ(s)) → (r, φ(s)) by conjugating and possibly inverting the first relator; (r, φ(s)) → (r, s) is one ACM move, a composite of ordinary AC moves by research-g Lemma G0. If φ induces conjugation by ḡ on G_r, then φ(s) ≡ g s g⁻¹ modulo ⟨⟨r⟩⟩, so (b) holds for every s. ∎

The automorphisms satisfying (a) form the stabilizer Stab[r] of the cyclic word r up to inversion; it contains Inn(F₂), and Lemma 0 only depends on the class of φ in Out(F₂) = GL₂(ℤ). The *hidden* part is K_r := ker(Stab[r]/Inn → Out(G_r)): these classes are realized on (r, s) for all s simultaneously.

**Theorem 1 (hidden reflection).** Let (u, v) be a basis of F, n ∈ ℤ, ρ = u²vⁿ, and β = (u ↦ u⁻¹v⁻ⁿ, v ↦ v). Then:

1. β ∈ Aut(F₂) and β² is conjugation by vⁿ;
2. β(u) = u · (u⁻²ρ⁻¹u²) and β(u⁻¹) = u⁻¹ · (u⁻¹ρu) as free words, so β(g) ≡ g modulo ⟨⟨ρ⟩⟩ for every g ∈ F;
3. β(ρ) = u⁻¹ρ⁻¹u;
4. for every r conjugate to ρ^{±1} and every word s: **β(r, s) ~AC (r, s)**, by an explicit sequence that inserts one conjugate of r^{±1} into s for each letter u^{±1} of s written in the basis (u, v);
5. on ℤ² the matrix of β is the reflection R with R·ab(ρ) = −ab(ρ) and R[v] = [v]; det([v], ab(ρ)) = ±2. In the basis ([u],[v]) it is [[−1,0],[−n,1]].

*Proof.* (1) (u⁻¹v⁻ⁿ, v) is a Nielsen transform of the basis (u, v). β²(u) = (u⁻¹v⁻ⁿ)⁻¹v⁻ⁿ = vⁿuv⁻ⁿ and β²(v) = v. (2) u·u⁻²·(v⁻ⁿu⁻²)·u² = u⁻¹v⁻ⁿ and u⁻¹·u⁻¹·(u²vⁿ)·u = vⁿu = β(u)⁻¹; both inserted factors are conjugates of ρ^{∓1}. (3) β(ρ) = u⁻¹v⁻ⁿu⁻¹v⁻ⁿvⁿ = u⁻¹(v⁻ⁿu⁻²)u. (4) Write s = t₁⋯t_k in the letters u^{±1}, v^{±1} and put W_j = β(t₁⋯t_j)t_{j+1}⋯t_k, so W₀ = s and W_k = β(s). By (2), W_j = W_{j−1}·h_jρ^{ε_j}h_j⁻¹ with h_j = (t_{j+1}⋯t_k)⁻¹u⁻², ε_j = −1 if t_j = u; h_j = (t_{j+1}⋯t_k)⁻¹u⁻¹, ε_j = +1 if t_j = u⁻¹; and W_j = W_{j−1} if t_j = v^{±1}. Each step is "conjugate the first relator to h_jρ^{ε_j}h_j⁻¹, multiply, conjugate back". Finally ρ → β(ρ) = u⁻¹ρ⁻¹u by (3), and conjugation carries ρ^{±1} to r and β(ρ)^{±1} to β(r). (5) β[u] = −[u] − n[v], β[v] = [v], and 2[u] + n[v] ↦ −(2[u] + n[v]); det([v], 2[u]+n[v]) = 2 det([v],[u]) = ±2. ∎

So K_ρ ∋ β for every relator of type T(2,n). By (5), β is conjugate in GL₂(ℤ) to the swap, not to diag(−1,1). `experiments/th02_hidden.py` implements (4) verbatim (`reflect_cert`); its self-test builds and replays 360 certificates (random partners s, a ∈ [−7,8]; all D(a;q), a ∈ {−6,…,8}, q ∈ {−9,…,11}), each accepted by `elementary_verify.replay`.

**Examples.**
- *Braid relator.* xyxYXY is conjugate to (u²v³)⁻¹ with u = (xyx)⁻¹, v = xy, and the hidden reflection has the matrix of the swap x ↔ y (in B₃ the swap is conjugation by the Garside element xyx). Hence **swap(xyxYXY, s) ~AC (xyxYXY, s) for every s**; D's searched certificate `d_ak3_aut_swap.json` is the case s = x³Y⁴.
- *A = xᵃyXy = zz·x^m up to rotation* (u = z = Xy, v = x, n = m = a+1): β_A = (x ↦ x, y ↦ xYX^a), i.e. y ↦ y·A⁻¹; matrix [[1, 1−a],[0, −1]].
- *xY²xy^{q−2} = w²y^q*, w = xY² (u = w, v = y, n = q): β_w = (x ↦ y²Xy^{2−q}, y ↦ y); matrix [[−1, 0],[4−q, 1]].

## 2. Applications (proved here)

**Corollary 2 (C4, X: N's Propositions N3 and N4 without search).** C4 = (x⁴yXy, xy³xY²) = (z²x⁵, w²y⁵) up to rotation, with z = Xy, w = xY². Both relators are of type T(2,5), so Ŝ(C4) ∋ β_A = [[1,−3],[0,−1]] and β_w = [[−1,0],[−1,1]]. Their product [[2,−3],[1,−1]] has trace 1 and determinant 1, hence order 6 with cube −I, so ⟨β_A, β_w⟩ is dihedral of order 12 and **equals N's group D = ⟨−I, M₁, M₂⟩** (β_w = M₁, β_A = −M₂; checked in the self-test). For every T(a;p,q), Ŝ ⊇ {±I, ±β_A} (−I because ι(T(a;p,q)) is Σ-equivalent to T(a;p,q)); for X = T(2;4,9) this is N's reflection ρ = −β_A.

**Lemma 3 (double form).** For all integers a, q: T(a;2a,q) = (x^{2a}y^q, A) ~AC D(a;q) := (xY²xy^{q−2}, A).

*Proof.* As free words xᵃ = A·YxY. So x^{2a}y^q = A·(YxY)·A·(YxY)·y^q ≡ YxY²xy^{q−1} modulo ⟨⟨A⟩⟩, which is conjugate (by y) to xY²xy^{q−2}. Two insertions of conjugates of A⁻¹ and one rotation (`double_form_cert`). ∎

**Theorem 4 (trace formula; why C3/C4 and X differ).** Let r₁, r₂ be of types T(2,n₁), T(2,n₂) with ρ_i = ab(r_i), det(ρ₁,ρ₂) = ±1, and let v_i be the (+1)-eigenvectors of their hidden reflections R_i, with signs chosen so that det(v_i, ρ_i) = 2. Then

    tr(R₁R₂) = 2 − D,   D := det(v₁,v₂)·det(ρ₁,ρ₂),   D odd.

Consequently ⟨R₁,R₂⟩ ⊆ Ŝ(r₁,r₂) is finite iff D ∈ {1, 3} (dihedral of order 12 containing −I, resp. of order 6); for every other D the element R₁R₂ is hyperbolic (|tr| ≥ 3) and Ŝ(r₁,r₂) is infinite. For D(a;q): D = δ := 4a − (a−1)q, the determinant of the exponent matrix.

*Proof.* R_i = I − ρ_iℓ_iᵀ with ℓ_i(w) = det(v_i, w): indeed R_iρ_i = ρ_i − 2ρ_i and R_iv_i = v_i. So tr(R₁R₂) = 2 − ℓ₁(ρ₁) − ℓ₂(ρ₂) + ℓ₁(ρ₂)ℓ₂(ρ₁) = −2 + det(v₁,ρ₂)det(v₂,ρ₁). The Plücker relation det(v₁,ρ₁)det(v₂,ρ₂) − det(v₁,v₂)det(ρ₁,ρ₂) − det(v₁,ρ₂)det(v₂,ρ₁) = 0 gives det(v₁,ρ₂)det(v₂,ρ₁) = 4 − D. Since ρ_i = 2[u_i] + n_i[v_i] with n_i odd, v_i ≡ ρ_i mod 2, so det(v₁,v₂) ≡ det(ρ₁,ρ₂) ≡ 1 mod 2 and D is odd. A matrix of determinant 1 and odd trace t has finite order iff t = ±1 (order 6 or 3). For D(a;q): ρ₁ = (2, q−4), v₁ = (0,−1), ρ₂ = (a−1, 2), v₂ = (1,0), so D = det(ρ₁,ρ₂) = 4 − (q−4)(a−1) = δ. ∎

The members of the double family presenting the trivial group are those with δ = ±1 (a is then even, so gcd(2a, a+1) = 1 and I's Prop. G applies): δ = +1: (a,q) ∈ {(2,7), (4,5)} and the degenerate (0,1), (−2,3); δ = −1: (2,9), (6,5), (−4,3) and the degenerate (0,−1). Hence:

| class | double form | δ | ⟨β_A, β_w⟩ | previously |
|---|---|---|---|---|
| C3 ~ T(2;4,7) | D(2;7) | +1 | D₆ (order 12) | Aut-closed by 3 searched certificates (I) |
| C4 ~ T(4;8,5) | D(4;5) = C4 | +1 | D₆ (order 12) | D₆ by 2 searched certificates (N) |
| X = T(2;4,9) | D(2;9) | −1 | infinite, rotation [[4,−1],[5,−1]] of trace 3 | infinite by a searched certificate (N) |
| T(6;12,5) | D(6;5) | −1 | infinite, trace 3 | new |
| T(−4;−8,3) | D(−4;3) | −1 | infinite, trace 3 | new |

This answers the question left by N (§5 item 6) and by the brief: **a = 2 versus a = 4 is not the relevant distinction; C3 (a = 2) and C4 (a = 4) carry the same hexagonal D₆, and X differs from both because δ = −1.** The extra symmetry of C3 (its class is Aut-closed) and N's element ψ = [[−2,1],[1,0]] of Ŝ(X) are *not* in ⟨−I, β_A, β_w⟩ (ψ and −ψ have determinant −1 and trace ∓2, so they are not reflections, and ⟨β_A,β_w⟩ ≅ D_∞ contains no other elements of determinant −1); they come from further states (§5) or from other mechanisms.

**Theorem 5 (AK(n), uniform in n).** For every n ≥ 1: (i) swap(AK(n)) ~AC AK(n); (ii) Ŝ(AK(n)) ⊇ ⟨−I, τ, R⟩ with τ the swap and R = [[−1,3],[0,1]]; τR = [[0,1],[−1,3]] is hyperbolic of trace 3, so Ŝ(AK(n)) is infinite.

*Proof.* (i) Theorem 1 for the braid relator. −I: ι(AK(n)) is Σ-equivalent to AK(n). (ii) By research-g Theorem G1, AK(n) ~AC (w_n, xyxYXY), w_n = cyc ψ(W_n), ψ = (x ↦ xyx, y ↦ yx), W_n = (xy)ⁿxY(XY)ⁿ. With V = xy and U = xVⁿ one has W_n ~ U²V^{−(2n+1)}, of type T(2,2n+1), with ab(W_n) = (1,−1) and [V] = (1,1): its hidden reflection has the matrix of the swap, so that of w_n is ΨτΨ⁻¹ = [[−1,3],[0,1]], Ψ = [[2,1],[1,1]]. ∎

For n = 3, D's Lemma D6 gives all of GL₂(ℤ) (by search); (ii) is uniform in n and needs only G1. Self-test: for n = 1,…,6 the reflection of w_n is recomputed, G1 is re-verified by an independent exact normal-form computation in B₃, and the certificate (w_n, b) → β(w_n, b) is built and replayed.

**Theorem 6 (Y = T(4;7,5)).** Y = (x⁷y⁵, x⁴yXy) ~AC Y′ = (xyXY³Xy, x⁴yXy), a pair of types T(2,3) and T(2,5) of total length 15. The hidden reflections are β_A = [[1,−3],[0,−1]] and β_t = [[−2,1],[−3,2]], with D = −3: β_Aβ_t = [[7,−5],[3,−2]] has trace 5, so **Ŝ(Y) is infinite**.

*Proof.* Certificate `th02_y_to_double_form.json` (two A-frozen cyclic products; symbolically, t = xyXY³Xy ≡ x¹⁸(X²y)⁵ modulo A, whose inverse has the necklace [1,1,1,1,−2] of x⁷y⁵ in C₅ * C₂ and the same abelianization modulo ab(A)); Theorem 1 at Y′ and at Y; `th02_y_hyperbolic.json` is the single certificate Y → h(Y), h = β_A∘β_t, replayed by the strict verifier. ∎

## 3. What the mechanism can and cannot produce (proved here)

**Proposition 7 (stabilizers of torus words).** Let r = xᵖy^q with gcd(p,q) = 1, |p|,|q| ≥ 2, and let Stab[r] ≤ Out(F₂) = GL₂(ℤ) be the stabilizer of the cyclic word r up to inversion.
1. If |p|,|q| ≥ 3 then Stab[r] = {±I}, and K_r = 1.
2. If |p| = 2 (so q is odd, |q| ≥ 3) then Stab[r] = {±I, ±β}, β = (x ↦ x⁻¹y^{−q}, y ↦ y), and K_r = {1, β}.

In both cases −I (the class of ι = (x ↦ X, y ↦ Y)) acts on G_r^{ab} ≅ ℤ by −1, so it is not hidden: by Lemma 0 it is realized on (r, s) iff ι(s) is conjugate to s⁻¹ in G_r.

*Proof.* Applying x ↦ X and/or y ↦ Y (which conjugates stabilizers) we may take p, q > 0. *Whitehead's theorem* (externally reported, classical: Lyndon–Schupp, *Combinatorial Group Theory*, Prop. I.4.20–4.23): if w, w′ are cyclic words of minimal length in their Aut(F)-orbit and w′ = α(w), then α is a product of Whitehead automorphisms through cyclic words of that same length; and a cyclic word is minimal iff no Whitehead automorphism shortens it. In rank 2 the Whitehead automorphisms are, up to inner automorphisms, the eight signed letter permutations and the four maps x ↦ xy^{±1}, y ↦ yx^{±1}. Direct computation of cyclic lengths: |(x ↦ xy)(r)| = 2p+q, |(x ↦ xY)(r)| = 2p+q−2, |(y ↦ yx)(r)| = p+2q, |(y ↦ yX)(r)| = p+2q−2. So r is minimal, and a non-permutation Whitehead map preserves its length only if p = 2 (x ↦ xY) or q = 2 (y ↦ yX).

(1) For p, q ≥ 3 every factorization as above consists of signed permutations (the same computation applies to each permuted word), and the signed permutations π with π(r) = r^{±1} as cyclic words are 1 and ι only (the swap would need p = q). ι acts by −1 on G_r^{ab}, hence K_r = 1.

(2) For p = 2 put w_j = xY^jxy^{q−j}, 0 ≤ j ≤ q, so w₀ = r and w_q is a rotation of x²Y^q. With σ = (x ↦ xY): σ(w_j) = w_{j+1}; the maps y ↦ yx^{±1} send every w_j to a word of length 2q > q+2, and x ↦ xy, resp. σ, lengthens w₀, resp. w_q. By induction on the length of a level factorization (a level move at π(w_j) is πσ^{±1}π⁻¹), every α with α(r) = r^{±1} is πσ^k with π a signed permutation, 0 ≤ k ≤ q and π(w_k) = r^{±1}. Comparing y-exponents forces k ∈ {0, q}: k = 0 gives π ∈ {1, ι}; k = q gives π ∈ {x ↦ X, y ↦ Y}, and (x ↦ X)∘σ^q = (x ↦ XY^q, y ↦ y) = β, (y ↦ Y)∘σ^q = ιβ. β is hidden by Theorem 1; ι and ιβ act by −1 on G_r^{ab}. ∎

Machine check (`th02_scan.py --self-test` → `stab_order`): a breadth-first search through the level set, tracking matrices, returns |Stab| = 2 for (p,q) ∈ {(3,4),(3,5),(4,5),(3,7),(5,7),(5,8)} and 4 for (2,3),(2,5),(2,7),(2,9).

**Corollary 8 (the mechanism is confined to an index-2 subgroup).** Let χ: GL₂(ℤ) → {±1}, χ(M) = det(M)·sgn(M mod 2), where sgn is the sign character of GL₂(𝔽₂) ≅ S₃, and Γ_τ = ker χ. Every hidden reflection of a T(2,n)-type relator (n odd) lies in Γ_τ, and so does −I. Therefore the subgroup of Ŝ(U) generated by −I and the hidden reflections of all T(2,n)-type relators of all states AC-equivalent to U is contained in Γ_τ, which has index 2 in GL₂(ℤ) and contains the swap but **none** of x ↦ x⁻¹, y ↦ y⁻¹, x ↦ xy^{±1}, y ↦ yx^{±1}.

*Proof.* By Theorem 1(5) a hidden reflection is conjugate to [[−1,0],[−n,1]], n odd: determinant −1, and modulo 2 the transposition [[1,0],[1,1]], so χ = (−1)(−1) = 1. χ(−I) = 1. χ(diag(−1,1)) = χ(diag(1,−1)) = (−1)(+1) = −1; the four transvections have determinant 1 and are transpositions modulo 2, so χ = −1; χ(swap) = (−1)(−1) = 1. ∎

Consequences. (a) For torus-type relators with both exponents ≥ 3 (xⁿY^{n+1} in AK(n), n ≥ 3; x⁸y⁵ in T(4;8,5)) there is no hidden symmetry at all. (b) The realizations of x ↦ x⁻¹ and x ↦ xy on the classes of AK(3), C3, P1, P2 (D, I) are **not** explained by hidden reflections; they need relators whose stabilizer contains a diag(−1,1)-type or transvection-type element acting compatibly (for a primitive relator x both occur: x ↦ x⁻¹ and y ↦ yx^k are hidden), or genuine loops. (c) For C4 the open chirality question splits into two questions of different nature: *inside Γ_τ* (e.g. the swap): equivalent to finding one more suitable T(2,n)-type relator somewhere in the class, see §5; *outside Γ_τ* (x ↦ x⁻¹, x ↦ xy): no torus-type hidden reflection can ever decide it. A proof that Ŝ(C4) ⊆ Γ_τ would already disprove the AC conjecture (Prop. C of research-i), and it is a weaker statement than Ŝ(C4) = D₆.

**Remark (orbifold form; proved here, not used elsewhere).** For ρ = u²vⁿ, n odd, F embeds with index 2 in E = ⟨g⟩ * ⟨c | c²⟩ ≅ ℤ * ℤ/2 by v = g², u = g⁻ⁿc: indeed E′ := ⟨u, v, b | bub⁻¹ = u⁻¹v⁻ⁿ, bvb⁻¹ = v, b² = vⁿ⟩ (the extension of F by β, legitimate since β² is conjugation by vⁿ and β(vⁿ) = vⁿ) has (bu)² = 1, and ⟨b, v | [b,v], b² = vⁿ⟩ = ⟨g⟩ with b = gⁿ, v = g². In E the relator is ρ ~ [c, gⁿ] and β is conjugation by gⁿ. So a T(2,n)-relator is a commutator of the cone-point generator with the n-th power of the core of the annulus orbifold double-covered by the pair of pants with fundamental group F, and "hidden reflection" means "conjugation by an element of E outside F".

## 4. Beyond hidden reflections: symmetric relators in the class of C4 (experiment + proved reductions)

Lemma 0 also applies to stabilizer elements that are *not* hidden; then condition (b) must be checked for the actual partner. `experiments/th02_survey.py` computes Stab[r] for every relator r of a state dump by breadth-first search through Whitehead level sets (the method of Prop. 7).

**Experiment (Fwd(C4, 28), relators of length ≤ 15: 1,713 distinct words).** Besides ±I, the hidden reflections and elements of D₆, exactly 19 relators have further stabilizer elements, of three kinds:

1. relators lying, up to automorphism, in a subgroup ⟨x, yxY⟩, e.g. **r₂ = xxyxYXyXYXyxY** = a²bAB·Ab with a = x, b = yxY: fixed by all transvections y ↦ yxᵏ and by ε_x = (x ↦ X); state (xyXYYXyXY, r₂), total length 22;
2. ε_x-symmetric relators (ε_x(r) ~ r⁻¹), e.g. **r₁ = xxxyXYYXXyyXY** = x³P with ε_x(P) = P⁻¹; state (s_w, r₁), s_w = xyyyxYY the second relator of C4, total length 20;
3. relators with −swap in the stabilizer, e.g. xxxYXyyyXYYXXY; state (xyxYXyyxY, xxxYXyyyXYYXXY).

Condition (b) was tested in finite quotients (`th02_candidates.py`). A quotient in which φ(s) and s have different cycle types or traces **proves** that Lemma 0 does not apply at that state; non-separation proves nothing.

| relator, partner, φ | result | verdict |
|---|---|---|
| r₂, xyXYYXyXY, transvections y ↦ yxᵏ (k = 1, −3, ±4) | 40 of 770 homomorphisms to S₆ separate | not realized by Lemma 0 at this state (proved) |
| xxYxxYXyyXyyXY, both partners, ±swap | 82 of 223 (S₆) separate | not realized (proved) |
| xxxYXyyyXYYXXY, xyxYXyyxY, −swap | 50 of 229 (S₇) and 24 of 111 (SL₂(11)) separate | not realized (proved) |
| r₂, xyXYYXyXY, ε_x | no finite quotient tried separates (S₆, S₇, SL₂(11)), but **Prop. 10 below: not conjugate** | not realized by Lemma 0 at this state (proved) |
| r₁, s_w, ε_x | no separation in S₅–S₇, SL₂(7), SL₂(11), SL₂(13), but the tests are vacuous or nearly so (see below) | **open**, no evidence either way |

Two remarks proved here. (a) ε_x is **not** an inner automorphism of F/⟨⟨r₂⟩⟩ (a homomorphism h to S₅ with h∘ε_x not conjugate to h), nor of F/⟨⟨r₁⟩⟩: with x_i = yⁱxy⁻ⁱ the relator r₁ reads x₀³ = x₁x₋₁²x₁, so the Alexander module is ℤ[t^{±1}]/(2t² − 3t + 2); ε_x acts on it by −1, an inner automorphism by ±tᵏ, and t is not a root of unity in ℚ(√−7). So neither is a "hidden reflection of diag(−1,1)-type"; the candidates concern the specific partners only. (b) Since Δ(1) = 1, all elements of y-exponent 1 are conjugate in the metabelian quotient of F/⟨⟨r₁⟩⟩, and every homomorphism of this group to S₅, S₆, S₇, SL₂(11), SL₂(13) found by the tests is metabelian (x of order 3 and y² inverting x, resp. no representation with non-commuting x₀, x₁, x₂); only 12 representations into SL₂(7) are not. Hence those tests carry essentially no information for r₁. For r₂ the Alexander module is trivial.

Bounded searches for an explicit chain (all negative): r₁-frozen cyclic products from s_w to ε_x(s_w)^{±1}: partner length ≤ 24 exhaustive (260 + 260 words), ≤ 36 not exhaustive (177k + 177k words); r₂-frozen: ≤ 22 exhaustive (263 + 263), ≤ 32 not exhaustive; and no state S of Fwd(C4, 30) (1,246,365 states) has ε_x(S) or swap(S) in Fwd(C4, 30).

**Proposition 9 (what an ε_x-candidate would give; proved here).** If condition (b) holds for ε_x at one state AC-equivalent to C4 (for instance if ε_x(s_w) is conjugate to s_w^{±1} in F/⟨⟨r₁⟩⟩), then ε_x ∈ Ŝ(C4) and

    Ŝ(C4) ⊇ ⟨D₆, ε_x⟩ = Γ⁰(3)^± := {M ∈ GL₂(ℤ) : M₁₂ ≡ 0 mod 3},

a maximal subgroup of index 4. So Ŝ(C4) would be infinite, the Aut(F₂)-orbit of the class of C4 would have at most 4 elements, and one further element (e.g. the swap) would make the class Aut(F₂)-closed.

*Proof.* The states above lie in Fwd(C4, 28), so they are AC-equivalent to C4 without automorphism, and Lemma 0 gives ε_x ∈ Ŝ(C4). ε_xβ_w = [[1,0],[−1,1]] and β_A·(−ε_x) = [[1,3],[0,1]]; these two transvections and −I generate Γ⁰(3) (the transpose of the classical generators of Γ₀(3)), of index 4 in SL₂(ℤ), and β_A, β_w, ε_x all have M₁₂ ≡ 0 mod 3. Γ⁰(3)^± is the stabilizer of a point for the action of PGL₂(𝔽₃) ≅ S₄ on the 4 points of P¹(𝔽₃), which is primitive; hence it is maximal. ∎

**Proposition 10 (the r₂-candidate is false; proved here).** In G = F/⟨⟨r₂⟩⟩, r₂ = xxyxYXyXYXyxY, the element ε_x(p) is not conjugate to p^{±1} for p = xyXYYXyXY (nor for the other partner xxYxyXYXyy of r₂ in Fwd(C4, 28), which is conjugate to p⁻¹ in G). So Lemma 0 does not give ε_x at the states containing r₂ or its mirror image xxYxyXYXyXYxy.

*Proof.* Put a = x, b = yxY, t = y, d = ab. Then r₂ = a²bABAb, and r₂ = 1 ⟺ ada = dad; so G = ⟨a, d, t | ada = dad, tat⁻¹ = a⁻¹d⟩ is an HNN extension of the trefoil group B₃ with associated subgroups ⟨a⟩, ⟨b⟩, b = a⁻¹d (both infinite cyclic). As free words p = (aB)·T·(AB) and ε_x(p) = (Ab)·T·(ab), so p ~ t⁻¹h and ε_x(p) ~ t⁻¹h′ with h = ABaB = a⁻¹d⁻¹a²d⁻¹a and h′ = abAb = da⁻²d. Both have t-exponent −1, so only p ~ ε_x(p) is possible, and by Collins' lemma (Lyndon–Schupp IV.2.5; externally reported, classical) two cyclically reduced elements t⁻¹h, t⁻¹h′ of t-length 1 are conjugate iff h′ = bᵏha⁻ᵏ in B₃ for some k ∈ ℤ. Under B₃ → ℤ (a, d ↦ 1) we have b ↦ 0, h ↦ 0, h′ ↦ 0, so k = 0, and h ≠ h′: under a ↦ [[1,1],[0,1]], d ↦ [[1,0],[−1,1]] (a homomorphism B₃ → SL₂(ℤ)) h ↦ [[−1,−2],[4,7]] and h′ ↦ [[3,−2],[−4,3]]. For the second partner: p″ = xxYxyXYXyy ~ t·b²aBA, and b²aBA = h⁻¹ in B₃ by the braid relation. The mirror relator is ι(r₂)⁻¹ up to rotation and Fwd(C4, 28) is ι-closed. ∎

(`th02_candidates.collins_r2_check` re-verifies the free identities and the two matrices.) This also shows how weak the quotient tests are: h′ = ah⁻¹a⁻¹, every SL₂-representation of G restricts to a rigid representation of B₃ (tr(a) is a root of s² − s ∓ 1), and none of the 400 homomorphisms tried separates p from ε_x(p).

**Proposition 11 (Collins form of the open candidate; proved here, with a bounded exclusion).** Let r₁ = xxxyXYYXXyyXY and x_i = yⁱxy⁻ⁱ. Then r₁ = 1 ⟺ x₀³ = x₁x₋₁²x₁, and F/⟨⟨r₁⟩⟩ is the HNN extension of

    H = ⟨x₀, x₁, x₂ | x₁³ = x₂x₀²x₂⟩ = ⟨x₁⟩ *_{x₁³ = x₂x₀²x₂} F(x₀, x₂)

with stable letter t = y, tx₀t⁻¹ = x₁, tx₁t⁻¹ = x₂ (Magnus–Moldavanskii; the associated subgroups are free of rank 2 by the Freiheitssatz). As free words s_w = xy³xY² = x₀x₃y and ε_x(s_w) = x₀⁻¹x₃⁻¹y, so s_w ~ t·x₂x₀ and ε_x(s_w) ~ t·x₂⁻¹x₀⁻¹. By Collins' lemma, **ε_x(s_w) is conjugate to s_w in F/⟨⟨r₁⟩⟩ iff there is a word Z(p, q) with**

    Z(x₀, x₁) · x₂⁻¹x₀⁻¹ · Z(x₁, x₂)⁻¹ = x₂x₀   in H.

Abelianizing H forces the exponent sums of Z to be (−6, +6); in particular |Z| ≥ 12. **No reduced word Z of length ≤ 18 is a solution**: each of the 924 + 11,088 + 126,984 + 1,311,024 words of lengths 12, 14, 16, 18 with these exponent sums violates the equation in one of five random finite quotients of H (`th02_candidates.py r1 L`), which excludes it rigorously. Whether a longer Z exists is **open**; a solution would give ε_x ∈ Ŝ(C4) and Prop. 9, and a proof that none exists (a twisted-conjugacy problem in the amalgam H) would exclude this state too.

*Proof of the reduction.* yXY = x₁⁻¹ and YX²y = x₋₁⁻², so r₁ = x₀³x₁⁻¹x₋₁⁻²x₁⁻¹; shifting by y gives the relator of H. In the HNN extension x₃ = tx₂t⁻¹, so x₀x₃t = x₀tx₂ ~ t·x₂x₀, and likewise for ε_x(s_w); both are cyclically reduced of t-length 1 and t-exponent +1. Collins' lemma: t·g ~ t·g′ iff g = z⁻¹g′φ(z) for some z in ⟨x₀,x₁⟩, φ the shift; put Z = z⁻¹. In H^{ab} = ℤ³/⟨(−2,3,−2)⟩ the equation reads (α−2, β−α, −β−2) = λ(−2,3,−2), whence λ = 4, (α,β) = (−6,6). ∎

**What remains open in §4.** The ε_x-symmetric relators of kind 2: r₁ with partners s_w and xxxyXYYXyy (Prop. 11 is the exact form of the question for s_w), its mirror xxxYXyyXXYYXy, and six relators of length 15. **Neither these candidates nor their negations are claimed.**

## 5. Experiments (exact commands; all run in this session, single core, niced)

S = `scratchpad/agent-th02`; N's dumps are in `scratchpad/agent-n`; the engine is D's `d_acsearch` (shared binary).

```
python3 experiments/th02_hidden.py --self-test
  self-test OK: 360 certificates built and replayed by elementary_verify.replay
python3 experiments/th02_scan.py --self-test
  th02_scan self-test OK (400 planted T(2,n) words, 7 negative controls, braid relator = swap)
python3 experiments/th02_acm.py --self-test        -> th02_acm self-test OK
python3 experiments/th02_auto.py --self-test       -> th02_auto self-test OK
python3 experiments/th02_survey.py --self-test     -> th02_survey self-test OK
python3 experiments/th02_candidates.py --self-test -> th02_candidates self-test OK
```

**5.1 Hidden reflections present in forward sets** (`th02_scan.py DUMP [--d6]`; a relator is recognized as T(2,n)-type by Whitehead reduction to a word with two equal-sign occurrences of one generator; self-test: 400 planted words).

| forward set | states | states with a T(2,n)-type relator | distinct reflections | group generated |
|---|---:|---:|---:|---|
| Fwd(C4, 28) (N's dump) | 216,640 | 203,706 | 4, all n = 5, all in D₆ | D₆ (order 12) |
| Fwd(C4, 30) (`d_acsearch --cap 30 --source xxxxyXy,xyyyxYY --dump 30 …`) | 1,246,365 | 1,195,158 | 5, all n = 5, all in D₆ | D₆ (order 12) |
| Fwd(Y, 28), Y = T(4;7,5) | 136,468 | 125,676 | 4 (n = 5 and n = 3) | infinite (Thm 6) |
| Fwd(X, 26), X = T(2;4,9) | 421,898 | 369,383 | 14 (n = 3 and n = 9) | infinite; N's ψ not found in ⟨−I, these⟩ by a bounded search (entries ≤ 60) |
| Fwd(AK3, 22) | 257,488 | 101,688 | 90, all n = 3 | infinite; contains swap, [[−1,1],[0,1]], [[−1,−1],[0,1]], which with −I generate Γ_τ; contains neither x ↦ X nor x ↦ xy (Cor. 8) |
| Fwd(C6, 26) | 37,648 | 26,415 | 1 (n = 3) | order 2 |

So for AK(3) the hidden reflections of trefoil-type relators at different states of the class account for the whole index-2 subgroup Γ_τ of Ŝ(AK3) = GL₂(ℤ) (experiment: the states are engine states, certificates for the connecting paths were not built), and D's two searched certificates for x ↦ X and x ↦ xy are exactly the part that this mechanism cannot give. For C4 the mechanism gives D₆ and nothing else up to cap 30.

**5.2 Exact frozen-relator search for further T(2,n)-type partners of C4** (`th02_acm.py --explore 6 6 6 2`, 97 s). T(2,n)-type cyclic words are parametrized as W(M,t) = θ_M(xYᵗxy^{t+1}), n = 2t+1. With one relator of a double-T(2,·) state frozen (a torus-knot group, conjugacy decided exactly by necklace and central exponent, conjugators unbounded), all W(M,t) with ab(W) = ±ab(s) + k·ab(r), |k| ≤ 6, (+1)-eigenvector v₀ + 2jρ, |j| ≤ 6, and t ≤ 6 (n ≤ 13) were tested for conjugacy with the partner; breadth-first to depth 2 from C4. Output: 5 states, 6 distinct hidden reflections, generated group of order 12 — exactly the D₆-images of C4, no new partner. The box is finite and not exhaustive: there are infinitely many bases, and no a priori bound on (M, t) is proved.

**5.3 Stabilizer survey and candidates** (§4): `python3 experiments/th02_survey.py scratchpad/agent-n/c4_dump28.txt 14` prints
```
distinct relator words of length <= 14: 616; minimal forms 608; infinite stabilizers 4
stabilizer orders (count of words): {1: 574, 2: 33, 4: 5}
((-1, 0, -1), False) count 2   e.g. ('xxxyXYYXXyyXY', ((-1, 0), (0, 1)))
((-1, 0, 1), False) count 4    e.g. ('xxYxxYXyyXyyXY', ((0, 1), (1, 0)))
((-1, 0, 1), True) count 12
```
and the quotient tests of §4 are `python3 experiments/th02_candidates.py sn|sl2|inner|bfs …` (exact invocations in the table of §4; e.g. `sn xxyxYXyXYXyxY xyXYYXyXY XyxYYxyxY 7` → "S_7: homs 5190, separating 0", `inner xxyxYXyXYXyxY 6` → "nontrivial homs 50, with h.eps_x conjugate to h: 10", `sn xxxYXyyyXYYXXY xyxYXyyxY YXYxyXXYx 7` → "homs 229, separating 50").

**5.4 All-pairs signed-permutation test at cap 30** (scratch script `allpairs.py`: canonicalize every state of the dump, apply φ letterwise, look the result up): for φ = ε_x and φ = swap, 0 of the 1,246,365 states of Fwd(C4, 30) have their image in the set. N did the all-pairs test (for all automorphisms) at cap 28; M tested only the images of C4 itself at cap 34.

**5.5 D(6;5) = (xyyyxYY, x⁶yXy)**, the length-16 double form of T(6;12,5): its forward set to cap 24 has 889 states and no primitive relator (`d_acsearch --cap 24 --source xYYxyyy,xxxxxxyXy`). Its stabilizer is infinite by Theorem 4 (certificate `th02_T6_12_5_hyperbolic.json`). Whether it is AC-trivial or one of the published residual classes was not checked. T(−4;−8,3) is Σ-equivalent to T(−4;8,−3), which research-i certifies AC-trivial, so that row of the table of §2 carries no new information.

**5.6 AK(n): where the reflections come from (experiment).** Fwd(AK(4), 23) (57,024 states, `d_acsearch --cap 23 --source xxxxYYYYY,xyxYXY --dump 23 …`) contains 17 distinct hidden reflections, all of trefoil type (n = 3), among them the swap, R_a = [[1,1],[0,−1]] (state (x²YXY, x²y³XY⁶)) and ρ₃ = [[−1,1],[0,1]] (state (xyXYYXy, xyxY³xy²XY)); the same three occur in Fwd(AK(3), 22) at the states (x²YXY, x²y²XY⁵) and (xyXYYXy, xyxY²xyXY). Since ⟨swap, R_a⟩ is dihedral of order 12 and contains −I and −R_a = [[−1,−1],[0,1]], these three reflections generate Γ_τ (checked: all 372 matrices with χ = +1 and entries ≤ 6 are products, none with χ = −1). The patterns suggest

    AK(n) ~AC (x²YXY, x²y^{n−1}XY^{n+2})   and   AK(n) ~AC (xyXY²Xy, xyxY^{n−1}xy^{n−2}XY)   for all n ≥ 3   (conjecture; engine paths for n = 3, 4),

which together with Theorem 1 would give **Γ_τ ⊆ Ŝ(AK(n)) for every n ≥ 3** (index ≤ 2), by a uniform symbolic argument. Only the cases n = 3, 4 are supported (engine paths of 5 and 12 cyclic products for n = 3; for n = 4 both states lie in Fwd(AK(4), 23)); no uniform derivation was found in the time available.

## 6. Failed attempts and honest limits

- **The best outcome was not reached.** I found no element of Ŝ(C4) outside D₆. Three independent attempts failed: (i) scanning Fwd(C4, 30) for T(2,n)-type relators (only the D₆ reflections); (ii) the exact frozen-relator search of §5.2 (only the D₆-images; finite box, not exhaustive); (iii) non-hidden stabilizer elements of other relators (§4): transvections, ±swap and the ε_x-candidate at r₂ are *disproved* at the states where they occur (Prop. 10), and the ε_x-candidates of type r₁ are undecided. None of this is evidence that Ŝ(C4) = D₆: Y, which looked just as rigid in N's and I's searches, has an infinite stabilizer through a non-obvious trefoil-type relator at total length 15 (Thm 6), and the forward sets are a thin part of the class.
- **No structural proof that the mechanism cannot produce more for C4.** What is proved is Cor. 8 (confinement to Γ_τ) and Prop. 7 (no hidden symmetry for torus words with both exponents ≥ 3). A classification of the T(2,n)-type words in a given conjugacy class of a T(2,5) torus-knot group would decide whether ⟨hidden reflections of A-frozen and s_w-frozen states⟩ = D₆; I do not have it (infinitely many bases must be controlled).
- Proposition 7 relies on Whitehead's peak-reduction theorem (classical, quoted from memory, arXiv blocked) and on hand length computations, cross-checked by `stab_order` for ten (p,q). Lemma 0, Theorem 1, Lemma 3, Theorem 4 are elementary and self-contained; Theorem 5(ii) uses research-g Theorem G1 (proved there; re-verified here for n ≤ 6 by an independent normal-form computation); Theorem 6 rests on the certificate.
- The finite-quotient tests of §4 are necessary conditions only. For r₁ they are vacuous (all homomorphisms found are metabelian); I first misread them as evidence and corrected this after computing the Alexander module. For r₂ they did not separate two elements that Prop. 10 proves non-conjugate, so non-separation must not be read as evidence.
- "Γ_τ ⊆ Ŝ(AK(3)) through hidden reflections" (§5.1, §5.6) is an experiment: the connecting paths exist as engine paths but were not compiled to certificates (for AK(3) the full statement Ŝ = GL₂(ℤ) is already certified by D).
- Everything here concerns stabilizers of classes under Aut(F₂); nothing bears on whether AK(3), C3, C4, X or Y is AC-trivial. An infinite stabilizer is compatible with both answers; only Ŝ ≠ GL₂(ℤ) would be decisive (a counterexample), and that is not shown for any class.
- Novelty is not established. That the swap of the braid generators is inner in B₃ is classical; whether the general "exponent-2" reflection and its use for AC stabilizers appear in the literature (e.g. in Panteleev–Ushakov's work on automorphic moves, externally reported in research-g) could not be checked.
- Resources: all jobs single-core, niced, ≤ 100 s each, < 400 MB.

## 7. Advice to the coordinator (ranked)

1. **Decide the equation of Proposition 11** (one agent; a twisted-conjugacy problem in the amalgam H = ⟨x₁⟩ *_{x₁³ = x₂x₀²x₂} F(x₀,x₂)): is there a word Z with Z(x₀,x₁)·x₂⁻¹x₀⁻¹·Z(x₁,x₂)⁻¹ = x₂x₀? *Yes* ⇒ ε_x ∈ Ŝ(C4), Ŝ(C4) ⊇ Γ⁰(3)^± of index 4 (Prop. 9), and the D₆-rigidity of C4 is gone; *no* ⇒ this state is excluded like r₂ (Prop. 10). No solution has length ≤ 18. Amalgam normal forms should decide it; the same routine then applies to the other symmetric relators that `th02_survey.py` lists at higher caps. Either answer is a theorem.
2. **Run `th02_scan.py` and `th02_survey.py` on every existing large dump** (M's cap-34 set of C4 if it can be exported as words; P1, P2, C3). Each new T(2,n)-type relator outside the known group is an immediate, search-free certificate (`th02_auto.auto_reflect` plus the engine path); each symmetric relator is a new instance of item 1. For C4 the decisive event is any reflection outside D₆.
3. **Uniform AK(n) theorem within reach:** prove the two conjectured forms of §5.6 symbolically (Lemma-S-style identities). With Theorem 1 this gives Γ_τ ⊆ Ŝ(AK(n)) for all n ≥ 3 without search; only one coset (x ↦ x⁻¹) would then separate the AK series from full Aut(F₂)-closure.
4. **Classify T(2,n)-type words in a conjugacy class of a T(2,5) torus-knot group** (necklace [1,1,1,1,−1] in C₅ * C₂ for C4). If only the D₆-images occur, the hidden-reflection part of Ŝ(C4) from double-T(2,·) states is exactly D₆ — the "precise structural statement" asked for in the brief, which I could support only experimentally (§5.2).
5. **Use χ as the organizing invariant of the chirality question.** By Cor. 8 the torus-type mechanism never leaves Γ_τ. For each frontier class record separately (a) Ŝ ∩ Γ_τ and (b) whether some element with χ = −1 is realized. A proof that Ŝ(C4) ⊆ Γ_τ would be a counterexample to the AC conjecture and needs an invariant that changes sign under x ↦ x⁻¹; N's Theorem N1 says where it cannot live.
6. Low priority: D(6;5) = (xy³xY², x⁶yXy) (length 16, infinite stabilizer, 889 states at cap 24) should be matched against the published residual list.

## 8. Files written and reproduction

- `research/research-th02.md` (this note).
- `experiments/th02_hidden.py` — Theorem 1, Lemma 3, Theorem 4 as certificate builders (`--self-test`, `--write`).
- `experiments/th02_scan.py` — recognition of T(2,n)-type relators, hidden reflections of a dump, `stab_order` (`--self-test`, `DUMP [--d6]`).
- `experiments/th02_acm.py` — exact conjugacy in torus-knot groups, frozen-relator search for T(2,n)-type partners (`--self-test`, `--explore K J T DEPTH`).
- `experiments/th02_auto.py` — automatic θ for a T(2,n)-type relator, certificates for Y and AK(n) (`--self-test`, `--write`).
- `experiments/th02_survey.py` — stabilizers of all relators of a dump (`--self-test`, `DUMP maxlen`).
- `experiments/th02_candidates.py` — quotient tests and bounded frozen search for non-hidden candidates (`--self-test`, `sn|sl2|inner|bfs`).
- Certificates (all `ordinary-ac-elementary-v1`):

```
python3 experiments/elementary_verify.py certificates/th02_*.json     (moves / peak)
th02_c4_reflect_A.json          C4 -> beta_A(C4)                         89 / 33
th02_c4_reflect_w.json          C4 -> beta_w(C4)                         95 / 31
th02_T4_8_5_to_D4_5.json        T(4;8,5) -> D(4;5) (= C4 up to Sigma)    43 / 38
th02_T2_4_7_to_D2_7.json        T(2;4,7) -> D(2;7)                       47 / 35
th02_x_to_D2_9.json             X = T(2;4,9) -> D(2;9)                   55 / 41
th02_x_hyperbolic.json          X -> h(X), h = [[4,-1],[5,-1]], trace 3  954 / 115
th02_T6_12_5_hyperbolic.json    T(6;12,5) -> h(T), trace 3               1698 / 199
th02_c3form_order6.json         T(2;4,7) -> h(T), h of order 6           766 / 75
th02_y_to_double_form.json      Y = T(4;7,5) -> (x^4yXy, xyXY^3Xy)       17 / 24
th02_y_reflect_t.json           Y' -> beta_t(Y')                         285 / 47
th02_y_hyperbolic.json          Y -> h(Y), h = [[7,-5],[3,-2]], trace 5  2064 / 175
th02_ak3_swap_hidden.json       AK(3) -> beta(AK(3)), matrix = swap      131 / 27
```
All twelve replay (output recorded in the final report). In the Y-certificates the relators are ordered (x⁴yXy, x⁷y⁵), as in the engine.

## References

- Earlier notes of this repository: research-d (Lemmas D2, D3, D6), research-g (Lemma 1, Lemma G0, Theorem G1), research-i (family T(a;p,q), Prop. C, Prop. G, Lemma S), research-n (Ŝ, Propositions N3, N4, Theorem N1), research-m (cap-34 forward set of C4).
- R. C. Lyndon, P. E. Schupp, *Combinatorial Group Theory*, Springer 1977: Whitehead's theorem and peak reduction (Ch. I §4), conjugacy in free products and HNN extensions (Ch. IV; Collins' lemma), Magnus' theorems on one-relator groups (Ch. II §5). Externally reported, quoted from memory.
- J. H. C. Whitehead, On equivalent sets of elements in a free group, Ann. of Math. 37 (1936). Externally reported.
- D. Panteleev, A. Ushakov, Conjugacy search problem and the Andrews–Curtis conjecture (externally reported through research-g; not consulted).
- arXiv and journal hosts were not reachable in this session; no novelty claim is made.

## Coordinator's check (2026-11-09, Los Angeles time)

**This agent stopped at about 04:56–04:57 UTC because the session's model ran out of usage credits, shortly before its deadline and before handing back a final report.** The text above is its last saved version; it already contained a status line, the honest-limits and advice sections, the list of files and the references, so it is published as written. The coordinator did not edit it.

- Mechanical checks re-run by the coordinator: every self-test shipped with this note passes, and every certificate `certificates/<this agent's id>_*.json` in format `ordinary-ac-elementary-v1` replays under `python3 experiments/elementary_verify.py` (certificates in other formats, if any, are not AC trivializations and are labelled by the note itself).
- The proofs were **not** re-derived by the coordinator except where stated below; for independent verdicts on the central claims see the referee notes research-th19.md (TH01–TH09) and research-th20.md (TH10–TH18), which were completed after the same interruption.
- Re-ran all six self-tests (`th02_acm.py`, `th02_auto.py`, `th02_candidates.py`, `th02_hidden.py`, `th02_scan.py`, `th02_survey.py`, each with `--self-test`): pass; `th02_hidden.py` builds and replays 360 certificates. All files `certificates/th02_*.json` replay under `python3 experiments/elementary_verify.py`.
- Re-derived by hand: **Theorem 1 (hidden reflection)**. For a basis (u,v) and r conjugate to (u²vⁿ)^{±1}, the map β = (u ↦ u⁻¹v⁻ⁿ, v ↦ v) is an automorphism, β(u²vⁿ) = u⁻¹v⁻ⁿu⁻¹ is a cyclic conjugate of (u²vⁿ)⁻¹, and modulo ⟨⟨r⟩⟩ one has u = u⁻¹v⁻ⁿ, so β induces the identity on F/⟨⟨r⟩⟩; the frozen-relator principle (one generalized move, then conjugating/inverting r) gives β(r,s) ~AC (r,s) for every s. For the braid relator (u,v) = (xyx, yx), n = −3, and the resulting matrix has (−1)-eigenvector (1,−1) and (+1)-eigenvector (1,1): it is the swap, in agreement with research-th15's Lemma S.
- Read but not re-derived: the identification D₆ = ⟨β_A, β_w⟩ for C4 (Corollary 2), the trace formula (item 4), Theorem 6 (the stabilizer of Y = T(4;7,5) is infinite; by certificate) and Proposition 7 (hidden reflections lie in an index-2 subgroup and never realize a Nielsen generator; uses Whitehead's theorem). See research-th19.md for the referee's verdicts.
- Scope: item 8 ("no element of Ŝ(C4) outside D₆ was found") is a bounded experiment plus a statement about this one mechanism. Whether Ŝ(C4) equals D₆ — which would make C4 a counterexample — or is infinite remains open.
