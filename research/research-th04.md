# Research TH04: rigidity of the torus island of AK(n) — twist rigidity in torus-knot groups, the hidden involution, and the third island node for every n

Date: 2026-11-09 (Los Angeles). Independent research agent TH04 (round 5, theory round).

**Status.** Partial results with complete proofs. **No AC trivialization of AK(3), no proof that AK(3) is not AC-trivial, no counterexample.** The full "island theorem" of the seed (*the torus-type presentations reachable from AK(n) by ACM moves with a torus-type relator frozen are exactly 3 Aut(F₂)-orbits*) is **not** proved. What is proved: the mechanism that makes the question infinite (twists) is completely controlled (T1–T3), the island's third orbit is identified and constructed for every n (T4), and the T(n,n+1) side is reduced to one configuration (T7). §6.3 states exactly the two missing lemmas. Everything concerns the ordinary (unstabilized) AC relation; no stabilization is used.

## 0. Central claims (labels)

Notation. X = x⁻¹, Y = y⁻¹. For coprime integers p, q with |p|,|q| ≥ 2: R = xᵖyᑫ, T = T_{p,q} = ⟨x,y | R⟩ (a torus-knot group), Q = C_|p| * C_|q| = ⟨s⟩ * ⟨t⟩, π: F₂ → Q (x ↦ s, y ↦ t), ab_T: F₂ → ℤ (x ↦ q, y ↦ −p). A word W is a *partner* of R if ab_T(W) = ±1; this is necessary for ⟨x,y | R, W⟩ to be perfect, hence holds for every word conjugate in T to the other relator of a balanced presentation of the trivial group containing R. Λ = {(a,b) ∈ ℤ² : qa − pb = ±1} is the set of exponent vectors of partners. A cyclic word is of *torus type* if it is cyc θ(x^{p′}y^{q′}) for some θ ∈ Aut(F₂), |p′|,|q′| ≥ 2 coprime (research-g).

*Twists* (of R) are the automorphisms α: y ↦ xᵖy, β: x ↦ yᑫx, σ_x: x ↦ X, σ_y: y ↦ Y (the other generator fixed), their products, and inner automorphisms. They preserve ker π. So **a twist never changes the syllable length ("meridian defect") in Q, and changes the syllable necklace at most by inverting all s-exponents and/or all t-exponents.** This is the mechanism that produces, for any torus-type (or primitive) word, infinitely many others with the same defect; it is why agent G's 3-orbit island could only be a bounded observation.

| # | statement | label |
|---|---|---|
| T1 | **Twist rigidity.** Let {|p|,|q|} ≠ {2,3}, W a partner of R and θ a twist such that θ(W) is again a partner (e.g. θ(W) conjugate to W^{±1} in T). Then θ is, modulo inner automorphisms, one of id, σ = σ_xσ_y, ι, σι, where ι exists only if 2 ∈ {|p|,|q|} (T2). These map R to a conjugate of R^{±1}, so (R, θ(W)) lies in the Aut(F₂)-orbit of (R, W). **In every torus-knot group other than the trefoil group, the infinite twist family of a partner contains no other partner** | proved here (§2; ping-pong on ℤ²) |
| T2 | **Hidden involution.** If p = ±2, then ι: x ↦ y^{−2q/p}x⁻¹, y ↦ y induces the identity on T and sends R to a conjugate of R⁻¹. So every conjugacy class of a T(2,m) group that contains a torus-type partner W also contains the different cyclic word ι(W) | proved here (§3) |
| T3 | **The trefoil group is the exception, and exactly how.** For (p,q) = (2,−3): partners with exponent vector outside Λ₀ = {±(1,−1), ±(1,−2)} obey T1. For exponent vector ±(1,−1) the partner-preserving twists are exactly id, ι, κ, ικ (and their σ-composites), with κ: x ↦ x, y ↦ x²Y | proved here (§2.3; the last list uses a finite enumeration) |
| T4 | **Third island node, for every n.** For every n ≥ 1: AK(n) ~AC (cyc ψκ(W_n), xyxYXY), where κ(W_n) = xY(x³Y)^{n−1}xy(X³y)ⁿ (ψ and W_n as in research-g). For n ≥ 3 the three torus pairs AK(n), (x²Y³, W_n), (x²Y³, κW_n) are pairwise not Aut(F₂)-equivalent. For n = 3 the third is G's third island orbit | proved here (§4) + certificate `certificates/th04_ak3_to_kappa_node.json` (6,774 moves) |
| T5 | **The island is closed under twists, for every n ≥ 3.** The twists of the island's torus words that are again partners are: on the T(n,n+1) side b only; on the trefoil side U_n, ιU_n and W_n, ιW_n, κW_n, ικW_n; on the T(2,2n+1) side N_n, ι′N_n. All lie in the 3 orbits. For n = 3, 4, 5 a bounded enumeration finds no torus-type word outside these lists | first sentence proved (§4.3); enumeration is an experiment (§5) |
| T6 | **Generating pairs on the Bass–Serre tree of Q.** If (u,v) is a basis of F₂, then (πu, πv) is: two elliptics conjugate to (sⁱ, tʲ); or an elliptic whose fixed vertex lies on the axis of the hyperbolic element; or two hyperbolics with intersecting axes | proved here (§6.1; classical tools) |
| T7 | **T(n,n+1) side.** Let n ≥ 3 and W = cyc(uᵃvᵇ) be a torus-type word conjugate to b^{±1} in ⟨x,y | xⁿ = y^{n+1}⟩ (b = xyxYXY). Then πu and πv are both hyperbolic in C_n * C_{n+1}, and uᵃ, vᵇ translate in opposite directions along a common segment of their axes | proved here (§6.2) |

**Not proved:** that every torus-type word in the relevant conjugacy classes is one of the listed words. Two lemmas are missing (§6.3): the hyperbolic–hyperbolic case of the factorization problem in Q, and "the stabilizer of ⟨⟨xᵖ, yᑫ⟩⟩ in Aut(F₂) consists of twists".

## 1. Previous work read and choice of direction

Read: `README.md` in full; research-g in full (my starting point); research-f §3, research-i §2–3, research-j §4 in full; status paragraphs and coordinator reviews of the other notes. Re-ran `g_torus.py` functions (exact conjugacy invariant `torus_class`, bounded enumerator `edges`) and used `g_cert.acm_edge` to compile one new certificate.

Facts used from earlier notes (re-checked): Lemma 1 of G = Lemma J0 of J (conjugacy in T is decided by the syllable necklace in Q plus ab_T); Lemma G0 (an ACM replacement with a frozen relator is a composite of ordinary AC moves); Theorem G1 (AK(n) ~AC (ψW_n, b), ψ = (x ↦ xyx, y ↦ yx), φ = ψ⁻¹, φ(b) = x²Y³, U_n = φ(xⁿY^{n+1}) = (xY)ⁿ(xYY)^{n+1}, W_n = (xy)ⁿxY(XY)ⁿ, and W_n is conjugate to U_n⁻¹ in H = ⟨x,y | x² = y³⟩).

**Choice of direction.** I kept the seed (rigidity of the torus island) but changed the plan after the first computation. Listing G's island by words rather than by orbits (§5) shows that the torus-type words in one conjugacy class come in *families related by automorphisms that act trivially on Q* (twists). Any classification must therefore (a) classify factorizations gᵃhᵇ in Q and (b) control twists through the central extension T → Q. Part (b) turned out to have a short complete answer (T1–T3), which also explains two things G observed without explanation: why AK(2) behaves differently, and where the third island orbit comes from. This is new relative to notes A–O: G proves statements about primitive words only (G2, Lemma G4) and leaves torus-type neighbours to a bounded search. It does not overlap the other nine seeds of this round (TH07 concerns length lower bounds beyond the plateau; TH09 killers of one-relator groups in general).

## 2. Twist rigidity (proved here)

### 2.1 Twists

Exponent vectors e(W) = (e_x, e_y) are column vectors; an automorphism θ acts on them by its matrix M_θ ∈ GL₂(ℤ), and M_θ = I iff θ is inner (Nielsen). Put ξ(a,b) = qa − pb, so ab_T(W) = ξ(e(W)), and

    A = [[1,p],[0,1]],  B = [[1,0],[q,1]],  D_x = diag(−1,1),  D_y = diag(1,−1) = −D_x,   Γ^± = ⟨A, B, D_x, D_y⟩.

**Lemma 2.1.** (a) M_α = A, M_β = B, M_{σ_x} = D_x, M_{σ_y} = D_y, so twists modulo inner automorphisms correspond bijectively to Γ^±. (b) For every twist θ there is φ ∈ Aut(Q), a composite of an inner automorphism and the factor inversions s ↦ s⁻¹, t ↦ t⁻¹, with π∘θ = φ∘π. (c) Since D_xAD_x = A⁻¹ and D_xBD_x = B⁻¹, every element of Γ^± is ±M₀ or ±M₀D_x with M₀ ∈ ⟨A,B⟩, and conjugation by D_x preserves the syllable length of reduced words in A, B.

*Proof.* (a) α maps a word with exponents (a,b) to one with exponents (a+pb, b); similarly for the others. (b) πα(y) = sᵖt = t, πβ(x) = tᑫs = s, πσ_x(x) = s⁻¹; inner automorphisms of F₂ induce inner automorphisms of Q. (c) Direct. ∎

By (b), W and θ(W) have the same syllable length in Q for every twist θ, and by Lemma J0 the class of θ(W) in T is determined by φ(necklace of W) together with the single integer ξ(M_θ e(W)). So the only thing that distinguishes the members of a twist family inside T is the central exponent, i.e. the abelianization. The next theorem says that this integer is never ±1 again.

### 2.2 Theorem T1

**Theorem 2.2.** Let |p|,|q| ≥ 2 be coprime with {|p|,|q|} ≠ {2,3}. If v ∈ Λ, M ∈ Γ^± and Mv ∈ Λ, then M = ±I, or |p| = 2 and M = ±B^{2/p}D_x, or |q| = 2 and M = ±A^{2/q}D_x.

*Proof.* The statement is symmetric under exchanging the coordinates (p ↔ q, A ↔ B, D_x ↔ −D_x, ξ ↔ −ξ), so assume |p| < |q|; then (|p|−1)(|q|−1) ≥ 3 and c := |p||q| − |p| − |q| ≥ 2.

(0) *Points of Λ.* Let v = (a,b), qa − pb = ε = ±1. If a = 0 then |pb| = 1, impossible; likewise b ≠ 0. As |qa|,|pb| ≥ 2 differ by 1, ||q||a| − |p||b|| = 1. Hence |p||b| ≥ |q||a| − 1 ≥ (|p|+1)|a| − 1 ≥ |p||a|, i.e. |a| ≤ |b|.

(1) *One syllable.* For m ≠ 0: ξ(Aᵐv) = ε + mpq·b and ξ(Bᵐv) = ε − mpq·a, and |mpqb|,|mpqa| ≥ 6. So Aᵐv, Bᵐv ∉ Λ.

(2) *Ping-pong regions.* Let X_A = {b ≠ 0, |a| ≥ (|p|−1)|b|}, X_B = {a ≠ 0, |b| ≥ (|q|−1)|a|}, Y = {a ≠ 0, |b| ≥ |a|} ⊇ X_B. For m ≠ 0:
- (i) Aᵐ(Y) ⊆ X_A: |a + mpb| ≥ |p||b| − |a| ≥ (|p|−1)|b|, and b ≠ 0.
- (ii) Bᵐ(X_A) ⊆ X_B: here |a| ≥ |b| ≥ 1 and |b + mqa| ≥ |q||a| − |b| ≥ (|q|−1)|a|.
- (iii) if w = (±a, b) with (a,b) ∈ Λ, then w ∈ Y by (0), and Bᵐw ∈ Y: its second coordinate has absolute value ≥ |q||a| − |b| ≥ |q||a| − (|q||a|+1)/|p| ≥ |a|, because c·|a| ≥ 1.

Consequently, if M₀ = S_k⋯S₁ is a reduced word (the S_i alternately nonzero powers of A and B) with k ≥ 2 and w = (±a,b) with (a,b) ∈ Λ, then M₀w ∈ X_A ∪ X_B: S₂S₁w ∈ X_A ∪ X_B by (i)–(iii), and (i), (ii) alternate afterwards.

(3) *The regions miss Λ.* If (a,b) ∈ X_A ∩ Λ then |q|(|p|−1)|b| ≤ |q||a| ≤ |p||b| + 1, so c·|b| ≤ 1, contradicting c ≥ 2. If (a,b) ∈ X_B ∩ Λ then |p|(|q|−1)|a| ≤ |p||b| ≤ |q||a| + 1, so c·|a| ≤ 1, again impossible.

(4) *Conclusion.* Write M = ±M₀D with M₀ = S_k⋯S₁ reduced and D ∈ {I, D_x} (Lemma 2.1(c)), and w = Dv = (±a, b). If k ≥ 2, Mv ∉ Λ by (2), (3). If D = I: k = 1 is excluded by (1), and k = 0 gives M = ±I. If D = D_x:
- k = 0: ξ(D_xv) = −qa − pb = ε − 2qa ∉ {±1} since |2qa| ≥ 4.
- S₁ = Aᵐ: ξ(AᵐD_xv) = −ε + pb(mq − 2). This is ±1 iff pb(mq−2) ∈ {0, 2ε}. Zero needs mq = 2, impossible for |q| ≥ 3. The value 2ε needs |p| = 2, |b| = 1, |mq − 2| = 1, so |q| = 3: the excluded trefoil case.
- S₁ = Bᵐ: ξ(BᵐD_xv) = ε + qa(mp − 2). This is ±1 iff qa(mp−2) ∈ {0, −2ε}. Zero means mp = 2: the stated exception. The value −2ε needs |q| = 2, impossible. ∎

**Corollary 2.3 (T1).** Let {|p|,|q|} ≠ {2,3}, W a partner of R, θ a twist with θ(W) a partner. Then θ ∈ Inn(F₂)·{id, σ, ι, σι} (ι only if 2 ∈ {|p|,|q|}; its matrix is the exceptional one, §3). In particular this holds if θ(W) is conjugate to W^{±1} in T, or if ⟨x,y | R, θ(W)⟩ is perfect. Each of these θ maps R to a conjugate of R^{±1}, so (R, θ(W)) = θ(θ⁻¹(R), W) is in the Aut(F₂)-orbit of (R, W).

*Remark (σ is invisible on torus-type words).* If W = cyc(uᵃvᵇ) with (u,v) a basis, then σ(W) = W⁻¹ as cyclic words: σ(w) = (rev w)⁻¹ for every word, so σ(uᵃvᵇ) = (rev u)⁻ᵃ(rev v)⁻ᵇ, and (rev u, rev v) is a basis with the same exponent matrix as (u,v), hence simultaneously conjugate to it. So on unoriented torus-type cyclic words the only nontrivial partner-preserving twist is ι.

### 2.3 The trefoil group (T3)

Take (p,q) = (2,−3), R = x²Y³ (the normalization φ(b) of research-g), Λ = {3a + 2b = ±1}. Steps (0), (1), (2), (4) of the proof hold verbatim (c = 1 suffices in (iii)); only (3) fails, and (X_A ∪ X_B) ∩ Λ = Λ₀ := {±(1,−1), ±(1,−2)} (X_A ∩ Λ forces |a| = |b| = 1, X_B ∩ Λ forces |a| = 1, |b| = 2).

**Proposition 2.4.** (a) If v ∈ Λ ∖ Λ₀, M ∈ Γ^± and Mv ∈ Λ, then M = ±I or M = ±M_ι = ±BD_x. (b) If v = (1,−1), the M ∈ Γ^± with Mv ∈ Λ are exactly ±I, ±M_ι, ±M_κ, ±M_ιM_κ, where M_κ = [[1,2],[0,−1]] = −A⁻¹D_x is the matrix of κ: x ↦ x, y ↦ x²Y.

*Proof.* (a) If the reduced word of M has k ≥ 2 syllables, then Mv ∈ X_A ∪ X_B by (2); the same applied to M⁻¹ (also k syllables, Lemma 2.1(c)) and the point Mv ∈ Λ gives v ∈ X_A ∪ X_B, so v ∈ Λ₀. For k ≤ 1 the case analysis (4) leaves mp = 2 (M = ±BD_x) and the case |b| = 1, which again means v = ±(1,−1) ∈ Λ₀. (b) For k ≥ 2 a solution must end in Λ₀, whose points have (|a|,|b|) ∈ S = {(1,1), (1,2)}. Starting from (|a|,|b|) = (1,1): a syllable keeps the vector in S only for one value of m with |m| = 1 (A: (1,1) → (1,1); B: (1,1) → (1,2); B: (1,2) → (1,1); A never keeps (1,2) in S). At the first exit from S one has |a| ≥ 3 ≥ (3/2)|b| (exit by an A-syllable) or |b| ≥ 4 > 2|a| (exit by a B-syllable). Afterwards the two conditions alternate: from |b| > 2|a| an A-syllable gives |a′| ≥ 2|b| − |a| > (3/2)|b|, and from |a| ≥ (3/2)|b| a B-syllable gives |b′| ≥ 3|a| − |b| > 2|a|. Neither condition holds on S, so the vector never returns to S. Hence solutions are among the words (), A^{±1}, B^{±1}, B^{±1}A^{±1}, with D ∈ {I, D_x}; the enumeration in `th04_island.py` (all reduced words with ≤ 5 syllables, |m| ≤ 4) returns exactly the four matrices I, A⁻¹D_x, BD_x, BA up to sign. ∎

So in the trefoil group twists of partners *can* be partners, but only for the two "small" exponent classes, and only finitely many. This is the precise reason for two observations of research-g: AK(2) (whose torus relator x²Y³ is itself a trefoil relator) has exits that AK(n ≥ 3) lacks, and the trefoil side of AK(n) carries more torus-type words than the other side. Example of a trefoil twist on a primitive word: in ⟨x,y | x²y³⟩ one has XYY = xy.

## 3. The hidden involution (T2; proved here)

**Lemma 3.1.** Let p = ±2, m = 2/p, and ι: x ↦ y^{−mq}x⁻¹, y ↦ y. Then (a) ι induces the identity on T; (b) ι(R) is conjugate to R⁻¹; (c) ι² is inner; (d) M_ι = B^{m}D_x, and for a partner W the cyclic word ι(W) is different from W and from W⁻¹, although ι(W) = W in T.

*Proof.* (a) In T, x² = (xᵖ)ᵐ = y^{−mq}, so y^{−mq}x⁻¹ = x. (b) For p = 2: ι(R) = y^{−q}Xy^{−q}X·yᑫ, conjugate to Xy^{−q}X, conjugate to (yᑫx²)⁻¹. For p = −2: ι(R) = (xy^{−q})²yᑫ = xy^{−q}x, conjugate to (yᑫx⁻²)⁻¹. (c) ι²(x) = y^{−mq}xy^{mq}, ι²(y) = y. (d) ι sends the exponent vector (a,b) to (−a, b − mqa). This equals (a,b) only if a = 0, and −(a,b) only if 2b = mqa, i.e. ξ(a,b) = 0; neither holds for a partner. ∎

So whenever the frozen relator is of type T(2,m) (the trefoil and T(2,2n+1) relators of the island), torus-type words in a conjugacy class come in pairs {W, ι(W)}, and (R, ιW) = ι(ι⁻¹R, W) is the same Aut(F₂)-orbit as (R, W). A bounded enumeration by matrix size sees the two members at very different sizes (for the trefoil side of AK(3): |M| ≤ 4 for W₃ and 15 for ιW₃), which is why orbit counts and word counts differ.

## 4. The third island node (T4, T5)

### 4.1 Theorem

Coordinates as in research-g: b = xyxYXY, φ = (x ↦ xY, y ↦ yyX), ψ = φ⁻¹ = (x ↦ xyx, y ↦ yx), φ(b) = x²Y³, H = ⟨x,y | x² = y³⟩, U_n = (xY)ⁿ(xYY)^{n+1}, W_n = (xy)ⁿxY(XY)ⁿ.

**Theorem 4.1.** For every n ≥ 1, κ(W_n) = xY(x³Y)^{n−1}xy(X³y)ⁿ (cyclically; length 8n) is conjugate to W_n⁻¹, hence to U_n, in H. Consequently

    AK(n) = (xⁿY^{n+1}, b)  ~AC  (cyc ψκ(W_n), b)      (cyclic length of the first relator: 14n − 3),

by a single replacement of the first relator with b frozen.

*Proof.* κ(xy) = x³Y and κ(XY) = XyX², so κ(W_n) = (x³Y)ⁿ·x·yX²·(XyX²)ⁿ = (x³Y)ⁿxy(X³y)ⁿX², whose cyclic reduction is the stated word. In Q = C₂ * C₃ the image of W_n is (st)ⁿ(st²)^{n+1}, with cyclic sequence of t-exponents 1ⁿ2^{n+1}. Since πκ(y) = s²t⁻¹ = t⁻¹, the image of κ(W_n) has t-exponents 2ⁿ1^{n+1}. The image of W_n⁻¹ has the reversed and negated sequence, 1^{n+1}2ⁿ, the same necklace. Further e(W_n) = (1,−1) and e(κW_n) = M_κ(1,−1) = (−1,1), so ab_T(κW_n) = −ab_T(W_n). By Lemma J0, κ(W_n) is conjugate to W_n⁻¹ in H, and W_n is conjugate to U_n⁻¹ (Theorem G1). Applying ψ, which maps ⟨⟨x²Y³⟩⟩ onto ⟨⟨b⟩⟩ and U_n to xⁿY^{n+1}: ψκ(W_n) is conjugate to xⁿY^{n+1} modulo ⟨⟨b⟩⟩. Lemma G0 turns this replacement into ordinary AC moves. ∎

**Certificate (n = 3).** `certificates/th04_ak3_to_kappa_node.json`: from exactly (xxxYYYY, xyxYXY) to (xxyxxyxxxyxxyxxxyXYXXYXXXYXXYXXXYXXYXyx, xyxYXY), 6,774 strict moves, peak 189; the endpoint's first relator is a rotation of cyc ψκ(W₃) (checked). In trefoil coordinates κ(W₃) = xYxxxYxxxYxyXXXyXXXyXXXy, which is, up to rotation and inversion, the word YxxxYxxxYxxxYXyXXXyXXXyX of G's third island orbit.

### 4.2 The three nodes are different orbits

W_n = cyc(u²v^{−(2n+1)}) with the basis u = (xy)ⁿx, v = xy (then x = v⁻ⁿu, y = u⁻¹v^{n+1}). In C₂ * C_{2n+1} = ⟨s′⟩ * ⟨t′⟩ (u ↦ s′, v ↦ t′) the trefoil relator x²Y³ becomes (t′⁻ⁿs′)²(t′^{−(n+1)}s′)³: 10 syllables. For the third node the roots are (κu, κv), and κ⁻¹(x²Y³) is conjugate to κ(x²Y³) (κ² is conjugation by x²), which is cyclically yX²yX²y; its image is s′t′^{n+1}(s′t′ⁿ)²s′t′^{n+1}(s′t′ⁿ)²s′t′^{n+1}: 14 syllables. By research-f, Prop. F3, the syllable length of the partner modulo the centre of a torus-knot relator group is an invariant of the Aut(F₂)-orbit. So for n ≥ 2 the pairs (x²Y³, W_n) and (x²Y³, κW_n) are not Aut(F₂)-equivalent (defects 10 and 14 on the T(2,2n+1) side), and for n ≥ 3 neither is equivalent to AK(n), whose relator groups are T(n,n+1) and T(2,3). Summary of the island for n ≥ 3 (relator types; defects):

| node | relators | defects |
|---|---|---|
| 1 = AK(n) | T(n,n+1), T(2,3) | 6 and 4n+2 |
| 2 (Theorem G1) | T(2,3), T(2,2n+1) | 4n+2 and 10 |
| 3 (Theorem 4.1) | T(2,3), T(2,2n+1) | 4n+2 and 14 |

Nodes 2 and 3 are joined to node 1 by moves with the trefoil relator frozen, and node 3 = κ-twist of node 2. No node has defect 2 or a primitive relator.

### 4.3 Closure of the island under twists (T5, first sentence)

Let n ≥ 3. (i) T(n,n+1) side: (n−1)n ≥ 6 and no exponent is ±2, so by Corollary 2.3 and the remark after it the only twists of b that are partners are b^{±1}. (ii) T(2,2n+1) side, in the coordinates where W_n = x⁻²y^{2n+1} and the trefoil relator is N_n⁻¹ with N_n = (xYⁿ)²(xY^{n+1})³: by Corollary 2.3 the partner twists are N_n^{±1}, ι′(N_n)^{±1}, where ι′: x ↦ y^{2n+1}X; ι′(N_n) is, up to inversion, the trefoil-type word (xYⁿ)³(xY^{n+1})² and (x⁻²y^{2n+1}, ι′N_n) is node 2 again (Lemma 3.1). The same holds at node 3. (iii) Trefoil side: e(U_n) = (2n+1, −(3n+2)) ∉ Λ₀, so by Proposition 2.4(a) the partner twists of U_n are U_n, ιU_n (ιU_n is, up to inversion, (xY)^{n+1}(xYY)ⁿ, i.e. AK(n) with the roles of x and y exchanged: node 1). e(W_n) = (1,−1), so by Proposition 2.4(b) they are W_n, ιW_n (node 2), κW_n, ικW_n (node 3). All six are conjugate to U_n^{±1} in H (Theorem 4.1 and Lemma 3.1). So **no twist leads out of the three orbits, for every n ≥ 3.**

## 5. Experiments (exact commands and outputs; one niced core, < 200 MB, each < 1 min)

```
python3 experiments/th04_island.py --selftest
#  th04 self-test passed
```
The self-test checks: (a) Theorem 2.2 by brute force for (p,q) ∈ {(3,−4), (4,−5), (5,−6), (2,5), (−2,7), (2,−9), (3,5), (3,7), (5,−7), (5,2), (7,−2), (4,3)}: over all reduced words with ≤ 4 syllables and exponents |m| ≤ 3, both D ∈ {I, D_x}, and all v ∈ Λ with |a| ≤ 12, the only solutions are the stated hidden involutions; for the trefoil cases (2,−3), (2,3), (3,−2) extra solutions exist and all have v ∈ Λ₀; (b) Lemma 3.1 on 200 random words for four groups; (c) for n = 1..8 the six words U_n, ιU_n, W_n, ιW_n, κW_n, ικW_n all lie in the class of U_n^{±1} in H (exact invariant `g_torus.torus_class`), κW_n ~ W_n⁻¹, and ι′N_n ~ N_n in T(2,2n+1).

```
python3 experiments/th04_island.py --write certificates
#  {'moves': 6774, 'peak_total_length': 189, 'endpoint': ['xxyxxyxxxyxxyxxxyXYXXYXXXYXXYXXXYXXYXyx', 'xyxYXY']}
python3 experiments/elementary_verify.py certificates/th04_ak3_to_kappa_node.json
#  {"endpoint": ["xxyxxyxxxyxxyxxxyXYXXYXXXYXXYXXXYXXYXyx", "xyxYXY"], "moves": 6774, "path": "certificates/th04_ak3_to_kappa_node.json", "peak_total_length": 189}
```

**Bounded listing of the island by words (T5, second sentence).** `--enumerate n K P L` lists, with G's enumerator `g_torus.edges`, every torus-type or primitive word θ_M(x^{p′}y^{q′}) with |entries of M| ≤ K, |p′|,|q′| ≤ P, length ≤ L that is conjugate to the partner or its inverse, for the three frozen relators, and names it.

```
python3 experiments/th04_island.py --enumerate 3 16 24 160
#  T(n,n+1) frozen, class of b: 1 word: b
#  trefoil frozen, class of U_n: 5 words: kW^-1 (len 24), W^-1 (14), iW^-1 (29), iU^-1 (17), U^-1 (18)
#  T(2,2n+1) frozen, class of N_n: 2 words: i'N^-1, N^-1
python3 experiments/th04_island.py --enumerate 4 16 24 160      (same for n = 5)
#  T(n,n+1): b only;  trefoil: kW^-1, W^-1, iU^-1, U^-1;  T(2,2n+1): i'N^-1, N^-1
```
No word outside the lists of T5 appears (the script prints UNEXPECTED otherwise). ικW₃ (matrix entries up to 33) and, for n = 4, 5, ιW_n lie outside K = 16; they are in the class by proof. These runs are bounded searches: they do **not** show that the lists are complete.

**Trefoil twists (Proposition 2.4), scratch run.** For (p,q) = (2,−3), all reduced words with ≤ 5 syllables, |m| ≤ 4: v = (1,−1) has exactly the four solutions I, A⁻¹D_x, BD_x, BA (up to sign); v = (3,−4), (3,−5), (5,−8), (7,−11) have only I and BD_x.

## 6. Towards the island theorem

### 6.1 Generating pairs on the tree (T6; proved here with classical tools)

Q acts on its Bass–Serre tree 𝒯: vertices are the cosets w⟨s⟩ and w⟨t⟩, edges the elements w (joining w⟨s⟩ and w⟨t⟩); edge stabilizers are trivial; P_s = ⟨s⟩ and P_t = ⟨t⟩ span the base edge. A nontrivial element is elliptic (conjugate into ⟨s⟩ or ⟨t⟩, exactly one fixed vertex) or hyperbolic, with translation length τ equal to its cyclic syllable length.

**Lemma 6.1.** Let g, h generate Q. Then exactly one of the following holds. (EE) Both are elliptic and (g,h) is conjugate to (sⁱ, tʲ) or (tʲ, sⁱ). (EH) One is elliptic and its fixed vertex lies on the axis of the other, which is hyperbolic. (HH) Both are hyperbolic and their axes intersect.

*Proof.* (EE) Both are nontrivial. They are not both conjugate into ⟨s⟩ (else ⟨g,h⟩ ⊆ ⟨⟨s⟩⟩ ≠ Q), nor both into ⟨t⟩. So after conjugation g = sⁱ and h = wtʲw⁻¹ with w reduced, w = 1 or w ending in an s-syllable; conjugating by a power of s, w = 1 or w also begins with a t-syllable. If w ≠ 1, every alternating product of nontrivial powers of s and nontrivial elements wtˡw⁻¹ is reduced as written, so the only elements of ⟨g,h⟩ of syllable length ≤ 1 are powers of s, and t ∉ ⟨g,h⟩. Hence w = 1. (EH) Let e be elliptic with fixed vertex P, h hyperbolic with axis A, and suppose P ∉ A. Let P₀ be the point of A nearest to P and X the set of points x ≠ P₀ for which the geodesic [P₀,x] starts with the first edge of [P₀,P]. A nontrivial power of e fixes only P and acts freely on the edges at P, so it maps 𝒯 ∖ X into X; a nontrivial power of h maps X ∪ {P₀} into 𝒯 ∖ (X ∪ {P₀}). By ping-pong (orbit of P₀), ⟨e,h⟩ = ⟨e⟩ * ⟨h⟩, whose abelianization is infinite, whereas Q^{ab} is finite. (HH) Two hyperbolic isometries of a tree with disjoint axes generate a free group (classical ping-pong; Culler–Morgan §1), but Q has torsion. ∎

In case (EE), gᵃhᵇ has at most 2 syllables. So a torus-type word of defect ≥ 4 has at least one hyperbolic root.

### 6.2 The T(n,n+1) side (T7; proved here)

Let n ≥ 3, Q = C_n * C_{n+1}. The image of b = xyxYXY is the cyclic word N_b = (s, t, s, t⁻¹, s⁻¹, t⁻¹). Because 1 ≢ −1 modulo n and modulo n+1, in N_b and in N_b⁻¹ *the s-exponents are not all equal and the t-exponents are not all equal* (∗).

**Proposition 6.2.** Let (u,v) be a basis of F₂ and a, b′ integers with |a|,|b′| ≥ 2 such that the image of uᵃv^{b′} in Q is conjugate to N_b^{±1}. Then πu and πv are hyperbolic, their axes share a segment of positive length, and (πu)ᵃ, (πv)^{b′} translate in opposite directions along it.

*Proof.* Let g = πu, h = πv; they generate Q. Case (EE) of Lemma 6.1 gives ≤ 2 syllables. Case (HH): if the axes met in one point, or g^a and h^{b′} translated in the same direction along the common segment, the translation lengths would add (Culler–Morgan 1.5–1.8), giving τ ≥ 2|a| + 2|b′| ≥ 8 > 6. It remains to exclude (EH). Since gᵃh^{b′} is conjugate to h^{b′}gᵃ, we have an elliptic e, a hyperbolic k and |c|,|d| ≥ 2 with ⟨e,k⟩ = Q and e^c k^d conjugate to N_b^{±1}. Assume e is conjugate into ⟨s⟩; the other case is identical with s and t exchanged, since (∗) and "n, n+1 are not both even" are symmetric.

*Normalization.* Conjugating, e = sᵐ ≠ 1; by Lemma 6.1 the axis of k contains P_s; conjugating by a power of s it contains the base edge, i.e. k is cyclically reduced; conjugating once more by a power of s, and replacing (k,d) by (k⁻¹,−d) if necessary, k = s^{i₁}t^{j₁}⋯s^{i_r}t^{j_r} (reduced, r ≥ 1) and d ≥ 2. Then e^c k^d = s^{mc+i₁}t^{j₁}⋯t^{j_r}·k^{d−1}.

*Case A: s^{mc+i₁} ≠ 1.* The word is cyclically reduced of length 2rd = 6, so r = 1, d = 3, and all three t-exponents equal j₁, contradicting (∗).

*Case B: s^{mc+i₁} = 1.* Then s^{i₁} ∈ ⟨e⟩, so V := s^{−i₁}k = t^{j₁}s^{i₂}⋯t^{j_r} satisfies ⟨e,V⟩ = Q. Claim: r = 1. Suppose r ≥ 2 and write V = CV₀C⁻¹ (reduced, C of maximal length; C = 1 or C begins with a t-syllable). If V₀ is one syllable ε, then |C| ≥ 1 and, exactly as in the proof of (EE), alternating products of powers of s and of the elements CεˡC⁻¹ are reduced as written, so t ∉ ⟨e,V⟩: contradiction. Otherwise V₀ = ε₁Mε₂ with ε₁, ε₂ nontrivial in the same factor, ε₂ε₁ ≠ 1, and V is hyperbolic with axis Cε₁·A_c, where A_c is the axis of the cyclically reduced element Mε₂ε₁. Let Y be the base vertex fixed by ε₁ and Y′ the other one; the neighbours of Y on A_c are Y′ and (ε₂ε₁)⁻¹Y′. P_s lies on the axis of V iff Z := ε₁⁻¹C⁻¹P_s lies on A_c. The reduced word ε₁⁻¹C⁻¹ ends with a t-syllable (or is ε₁⁻¹ itself, a t-syllable, if C = 1), so the geodesic from Y to Z has positive length and first vertex ε₁⁻¹Y′, which is neither Y′ nor ε₁⁻¹ε₂⁻¹Y′. A geodesic that starts on A_c and leaves it at once ends outside A_c. So P_s is not on the axis of V, contradicting Lemma 6.1 (EH) for the generating pair (e,V). Hence r = 1.

With r = 1, e^c k^d is conjugate to t^{j₁}(s^{i₁}t^{j₁})^{d−1}, a cyclic word with d−1 syllables s^{i₁}, one syllable t^{2j₁} and d−2 syllables t^{j₁}. If t^{2j₁} ≠ 1 it is reduced, so d = 4 and all s-exponents are equal: contradiction with (∗). If t^{2j₁} = 1, then d ≥ 3 (for d = 2 the element is elliptic) and two syllables s^{i₁} merge to s^{2i₁}; if s^{2i₁} ≠ 1 the word is reduced with d−2 = 3 equal t-exponents, contradicting (∗); and s^{2i₁} = 1 = t^{2j₁} would make n and n+1 both even. ∎

The same argument fails for n = 2 exactly at (∗) (in C₂, s = s⁻¹), in agreement with G's primitive exits of AK(2). The known solution is of type (HH): b = cyc((xy)³(xyy)⁻²) = cyc((xxy)²(xy)⁻³), with roots mapping to (st, st²) and (s²t, st), which translate in the same direction along a common segment of length 2, the exponents having opposite signs.

### 6.3 Exactly what is missing

Fix a frozen relator R = xᵖyᑫ and the necklace class 𝒩 of the partner. The torus-type words in the partner's class are the uᵃvᵇ, (u,v) a basis. The classification splits into three steps:

1. **Factorizations in Q** (open in the (HH) case). Determine all generating pairs (g,h) of Q that are images of bases, up to conjugacy and factor inversions, and exponents with gᵃhᵇ ∈ 𝒩^{±1}. For the T(n,n+1) side Proposition 6.2 leaves only (HH) pairs with opposite translation directions. **Missing Lemma M1:** *for n ≥ 3 the only such factorizations of N_b^{±1} are those of b itself.* What blocks a quick proof: when the common segment is longer than the translation lengths (deep cancellation), the translation length of gᵃhᵇ is not given by a formula, and one needs the Nielsen-reduced normal form of generating pairs of C_n * C_{n+1} (Zieschang's method) rather than the three-case Lemma 6.1.
2. **From pairs in Q to bases of F₂** (open). **Missing Lemma M2:** *if θ ∈ Aut(F₂) preserves ⟨⟨xᵖ, yᑫ⟩⟩, then θ is a twist.* Equivalently: two bases whose images in Q are simultaneously conjugate up to factor inversions differ by a twist. Half of it is easy: if θ preserves ker π then (πθx, πθy) is an (EE) pair, conjugate to (sⁱ, tʲ), and Nielsen's commutator criterion ([θx, θy] is conjugate to [x,y]^{±1}) forces [sⁱ,tʲ] ~ [s,t]^{±1}, i.e. i, j = ±1; so after composing with σ_x, σ_y and an inner automorphism, π∘θ = π. What remains is that π∘θ = π implies θ ∈ ⟨α, β⟩·Inn. I expect this to follow from Zieschang's classification of Nielsen classes of generating pairs of torus-knot groups, but did not prove it.
3. **Twists** (done). By T1–T3, each twist family contributes exactly the listed words.

So: **M1 + M2 for the three frozen relators ⟹ the island of AK(n) is exactly three Aut(F₂)-orbits.** T(n,n+1) side: M1 as stated. T(2,2n+1) side: 10 or 14 syllables, expected factorizations N_n only. Trefoil side: 4n+2 syllables, expected factorizations: those of U_n and of W_n.
