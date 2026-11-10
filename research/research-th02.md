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
| 8 | In Fwd(C4, 28) (216,640 states) 203,706 states carry a T(2,n)-type relator; all have n = 5 and their hidden reflections are exactly four matrices, all in D₆. An exact frozen-relator (unbounded-conjugator) search for further T(2,n)-type partners in a box finds only the D₆-images. **No element of Ŝ(C4) outside D₆ was found** | experiment (§5) |

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
