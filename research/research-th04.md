# Research TH04: rigidity of the torus island of AK(n) — two of its three sides proved for all n (twist rigidity in torus-knot groups, normal form of bases modulo twists), and the third node constructed for every n

Date: 2026-11-09 (Los Angeles). Independent research agent TH04 (round 5, theory round).

**Status.** Partial results with complete proofs. **No AC trivialization of AK(3), no proof that AK(3) is not AC-trivial, no counterexample.** Headline: of the three kinds of "frozen relator" in G's torus island of AK(n), two are now settled by theorems, uniformly in n. (T8) **For every n ≥ 3, with the relator xⁿY^{n+1} frozen, AK(n) has no torus-type or primitive ACM neighbour other than itself.** (T10) **For every n ≥ 2, with the T(2,2n+1) relator frozen, the island's nodes 2 and 3 have no torus-type or primitive ACM neighbour other than themselves.** (Arbitrary conjugators and automorphisms; G had such statements only for primitive words, and for torus-type words as a bounded search.) The full "island theorem" of the seed (*exactly 3 Aut(F₂)-orbits*) is **not** proved: the same classification is missing on the trefoil side (§6.5), where I prove only that the island is closed under twists (T5) and construct its third orbit for every n (T4). Everything concerns the ordinary (unstabilized) AC relation; no stabilization is used.

## 0. Central claims (labels)

Notation. X = x⁻¹, Y = y⁻¹. For coprime integers p, q with |p|,|q| ≥ 2: R = xᵖyᑫ, T = T_{p,q} = ⟨x,y | R⟩ (a torus-knot group), Q = C_|p| * C_|q| = ⟨s⟩ * ⟨t⟩, π: F₂ → Q (x ↦ s, y ↦ t), ab_T: F₂ → ℤ (x ↦ q, y ↦ −p). A word W is a *partner* of R if ab_T(W) = ±1; this is necessary for ⟨x,y | R, W⟩ to be perfect, hence holds for every word conjugate in T to the other relator of a balanced presentation of the trivial group containing R. Λ = {(a,b) ∈ ℤ² : qa − pb = ±1} is the set of exponent vectors of partners. A cyclic word is of *torus type* if it is cyc θ(x^{p′}y^{q′}) for some θ ∈ Aut(F₂), |p′|,|q′| ≥ 2 coprime (research-g).

*Twists* (of R) are the automorphisms α: y ↦ xᵖy, β: x ↦ yᑫx, σ_x: x ↦ X, σ_y: y ↦ Y (the other generator fixed), their products, and inner automorphisms. They preserve ker π. So **a twist never changes the syllable length ("meridian defect") in Q, and changes the syllable necklace at most by inverting all s-exponents and/or all t-exponents.** This is the mechanism that produces, for any torus-type (or primitive) word, infinitely many others with the same defect; it is why agent G's 3-orbit island could only be a bounded observation.

| # | statement | label |
|---|---|---|
| T1 | **Twist rigidity.** Let {\|p\|,\|q\|} ≠ {2,3}, W a partner of R and θ a twist such that θ(W) is again a partner (e.g. θ(W) conjugate to W^{±1} in T). Then θ is, modulo inner automorphisms, one of id, σ = σ_xσ_y, ι, σι, where ι exists only if 2 ∈ {\|p\|,\|q\|} (T2). These map R to a conjugate of R^{±1}, so (R, θ(W)) lies in the Aut(F₂)-orbit of (R, W). **In every torus-knot group other than the trefoil group, the infinite twist family of a partner contains no other partner** | proved here (§2; ping-pong on ℤ²) |
| T2 | **Hidden involution.** If p = ±2, then ι: x ↦ y^{−2q/p}x⁻¹, y ↦ y induces the identity on T and sends R to a conjugate of R⁻¹. So every conjugacy class of a T(2,m) group that contains a torus-type partner W also contains the different cyclic word ι(W) | proved here (§3) |
| T3 | **The trefoil group is the exception, and exactly how.** For (p,q) = (2,−3): partners with exponent vector outside Λ₀ = {±(1,−1), ±(1,−2)} obey T1. For exponent vector ±(1,−1) the partner-preserving twists are exactly id, ι, κ, ικ (and their σ-composites), with κ: x ↦ x, y ↦ x²Y | proved here (§2.3; the last list uses a finite enumeration) |
| T4 | **Third island node, for every n.** For every n ≥ 1: AK(n) ~AC (cyc ψκ(W_n), xyxYXY), where κ(W_n) = xY(x³Y)^{n−1}xy(X³y)ⁿ (ψ and W_n as in research-g). For n ≥ 3 the three torus pairs AK(n), (x²Y³, W_n), (x²Y³, κW_n) are pairwise not Aut(F₂)-equivalent. For n = 3 the third is G's third island orbit | proved here (§4) + certificate `certificates/th04_ak3_to_kappa_node.json` (6,774 moves) |
| T5 | **The island is closed under twists, for every n ≥ 3.** The twists of the island's torus words that are again partners are: on the T(n,n+1) side b only; on the trefoil side U_n, ιU_n and W_n, ιW_n, κW_n, ικW_n; on the T(2,2n+1) side N_n, ι′N_n. All lie in the 3 orbits. For n = 3, 4, 5 a bounded enumeration finds no torus-type word outside these lists | first sentence proved (§4.3); enumeration is an experiment (§5) |
| T6 | **Generating pairs on the Bass–Serre tree of Q.** If (u,v) is a basis of F₂, then (πu, πv) is: two elliptics conjugate to (sⁱ, tʲ); or an elliptic whose fixed vertex lies on the axis of the hyperbolic element; or two hyperbolics with intersecting axes | proved here (§6.1; classical tools) |
| T7 | **Elliptic roots are impossible on the T(n,n+1) side** (tree proof). If n ≥ 3 and the image of uᵃvᶜ in C_n * C_{n+1} is the necklace of b^{±1} (\|a\|,\|c\| ≥ 2), then πu and πv are both hyperbolic and uᵃ, vᶜ translate in opposite directions along a common segment of their axes | proved here (§6.2) |
| T8 | **Rigidity of AK(n) on the T(n,n+1) side.** Let n ≥ 3. If W = cyc(uᵃvᶜ), (u,v) a basis of F₂ (so: any torus-type or primitive word), is conjugate to b^{±1} in ⟨x,y | xⁿ = y^{n+1}⟩, then W = b^{±1} as cyclic words | proved here (§6.3: normal form of bases modulo twists + finite case analysis + T1); case analysis also checked by brute force for n = 3, 4, 5 |
| T9 | **Stabilizer.** An automorphism of F₂ preserves ⟨⟨xᵖ, yᑫ⟩⟩ iff it is a twist; every basis of F₂ can be brought by a twist to an explicit normal form (L), (Y_k), (X_j) | proved here (§6.3, §6.4) |
| T10 | **Rigidity on the T(2,2n+1) sides.** Let n ≥ 2. With the T(2,2n+1) relator frozen, the only words cyc(uᵃvᶜ) conjugate to the partner P or P⁻¹ are P^{±1} and ι′(P)^{±1}, at node 2 (P = N_n) and at node 3. So nodes 2 and 3 have no torus-type or primitive ACM neighbour other than themselves on that side | proved here (§6.3, Theorem 6.6); case analysis also checked by brute force for n = 2, 3, 4 |

**Not proved:** the analogue of T8/T10 on the trefoil side (trefoil relator frozen: only the six words of T5). This single missing statement (Lemma M, §6.5) is all that separates T4–T10 from the full island theorem; there the result is supported only by bounded enumeration.

## 1. Previous work read and choice of direction

Read: `README.md` in full (closing summary and the index of the fifteen notes A–O); research-g in full, including its coordinator's review (my starting point); research-f §3, research-i §2–3, research-j §4 in full; the status paragraphs of all other notes. For the coordinator's reviews of the other notes I relied on the README's summary of the corrections (D's Lemma D1(c), H's Theorem 2(ii), K's remark); none of them is used here. Re-ran `g_torus.py` functions (exact conjugacy invariant `torus_class`, bounded enumerator `edges`) and used `g_cert.acm_edge` to compile one new certificate.

Facts used from earlier notes (re-checked): Lemma 1 of G = Lemma J0 of J (conjugacy in T is decided by the syllable necklace in Q plus ab_T); Lemma G0 (an ACM replacement with a frozen relator is a composite of ordinary AC moves); Theorem G1 (AK(n) ~AC (ψW_n, b), ψ = (x ↦ xyx, y ↦ yx), φ = ψ⁻¹, φ(b) = x²Y³, U_n = φ(xⁿY^{n+1}) = (xY)ⁿ(xYY)^{n+1}, W_n = (xy)ⁿxY(XY)ⁿ, and W_n is conjugate to U_n⁻¹ in H = ⟨x,y | x² = y³⟩).

**Choice of direction.** I kept the seed (rigidity of the torus island) but changed the plan after the first computation. Listing G's island by words rather than by orbits (§5) shows that the torus-type words in one conjugacy class come in *families related by automorphisms that act trivially on Q* (twists). Any classification must therefore (a) classify factorizations gᵃhᵇ in Q and (b) control twists through the central extension T → Q. Part (b) turned out to have a short complete answer (T1–T3), which also explains two things G observed without explanation: why AK(2) behaves differently, and where the third island orbit comes from. For part (a) the right tool turned out to be a normal form of bases of F₂ modulo twists (Lemma 6.3), which reduces everything to positive (Christoffel-type) words; this settles the T(n,n+1) and T(2,2n+1) sides for all n (T8, T10) and leaves the trefoil side open. This is new relative to notes A–O: G proves statements about primitive words only (G2, Lemma G4) and leaves torus-type neighbours to a bounded search. It does not overlap the other nine seeds of this round (TH07 concerns length lower bounds beyond the plateau; TH09 killers of one-relator groups in general).

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

Let n ≥ 3. (i) T(n,n+1) side: (n−1)n ≥ 6 and no exponent is ±2, so by Corollary 2.3 and the remark after it the only twists of b that are partners are b^{±1}. (ii) T(2,2n+1) side, in the coordinates where W_n = x⁻²y^{2n+1} and the trefoil relator is N_n⁻¹ with N_n = (xYⁿ)²(xY^{n+1})³: by Corollary 2.3 the partner twists are N_n^{±1}, ι′(N_n)^{±1}, where ι′: x ↦ y^{2n+1}X; ι′(N_n) is, up to inversion, the trefoil-type word (xYⁿ)³(xY^{n+1})² and (x⁻²y^{2n+1}, ι′N_n) is node 2 again (Lemma 3.1). The same holds at node 3. (iii) Trefoil side: e(U_n) = (2n+1, −(3n+2)) ∉ Λ₀, so by Proposition 2.4(a) the partner twists of U_n are U_n, ιU_n (ιU_n is, up to inversion, (xY)^{n+1}(xYY)ⁿ, i.e. AK(n) with the roles of x and y exchanged: node 1). e(W_n) = (1,−1), so by Proposition 2.4(b) they are W_n, ιW_n (node 2), κW_n, ικW_n (node 3). All six are conjugate to U_n^{±1} in H (Theorem 4.1 and Lemma 3.1). So **no twist leads out of the three orbits, for every n ≥ 3.** (For sides (i) and (ii) this is superseded by Theorems 6.4 and 6.6, which classify all torus-type words in the class, not only the twists of the known ones.)

## 5. Experiments (exact commands and outputs; one niced core, < 200 MB, each < 1 min)

```
python3 experiments/th04_island.py --selftest
#  th04 self-test passed
#  (3, -4) K 5 matrices 616 kernel-preserving 20 in Gamma^pm 20 equal True
#  (2, -3) K 5 matrices 616 kernel-preserving 44 in Gamma^pm 44 equal True
#  th04 extra checks passed (M2 evidence K=5; T7 consistency n=3: 32 hits, 0 with an elliptic root)
```
The self-test also runs small instances of the checks listed below (`--normal-form 6`, `--check-t8 3 6`, `--check-t8 4 6`, `--check-t2side 2 7`, `--stabilizer 5`, `--check-t7 3 4 5`). Its first part checks: (a) Theorem 2.2 by brute force for (p,q) ∈ {(3,−4), (4,−5), (5,−6), (2,5), (−2,7), (2,−9), (3,5), (3,7), (5,−7), (5,2), (7,−2), (4,3)}: over all reduced words with ≤ 4 syllables and exponents |m| ≤ 3, both D ∈ {I, D_x}, and all v ∈ Λ with |a| ≤ 12, the only solutions are the stated hidden involutions; for the trefoil cases (2,−3), (2,3), (3,−2) extra solutions exist and all have v ∈ Λ₀; (b) Lemma 3.1 on 200 random words for four groups; (c) for n = 1..8 the six words U_n, ιU_n, W_n, ιW_n, κW_n, ικW_n all lie in the class of U_n^{±1} in H (exact invariant `g_torus.torus_class`), κW_n ~ W_n⁻¹, and ι′N_n ~ N_n in T(2,2n+1).

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
No word outside the lists of T5 appears (the script prints UNEXPECTED otherwise). Words are identified up to rotation and inversion (`g_torus.cyc_canon`), so the superscripts −1 in the output carry no information. ικW₃ (matrix entries up to 33) and, for n = 4, 5, ιW_n lie outside K = 16; they are in the class by proof. These runs are bounded searches: they do **not** show that the lists are complete.

**Brute-force checks of the two case analyses (Theorems 6.4, 6.6).** All cyclic words η(W₀) with W₀ = (positive word)(negative word) in A, B, r + t ≤ L, for every admissible k and j, are tested for membership of their necklace in the partner's family.
```
python3 experiments/th04_island.py --check-t8 N 8        (N = 3, 4, 5)
#  n=3: True, [('x',1,'XXYXyXY'), ('x',1,'XYXyxy'), ('y',1,'XYXyxy'), ('y',2,'XYYYXYxY')]
#  n=4: True, [('x',1,'XYXyxy'), ('x',2,'XXXYXyXY'), ('y',1,'XYXyxy'), ('y',3,'XYYYYXYxY')]
#  n=5: True, [('x',1,'XYXyxy'), ('x',3,'XXXXYXyXY'), ('y',1,'XYXyxy'), ('y',4,'XYYYYYXYxY')]
python3 experiments/th04_island.py --check-t2side N 9    (N = 2, 3, 4)
#  True in all three cases: for both partners (N_n and the node-3 partner) the only solutions are the two positive words with k = n
```
So the solutions are exactly b^{±1} (k = 1, j = 1) and the two twist images (k = n−1, j = n−2), resp. the positive words with k = n, as in the proofs.

**Other checks.** `--normal-form 14` (Lemma 6.3): the reduction of the proof, run at matrix level with every claim asserted (both slopes in [k, k+1], strict decrease, termination), ends in (L), (Y_k) with 1 ≤ k ≤ |q|−2 or (X_j) with 1 ≤ j ≤ |p|−2 for all 4,072 matrices with entries ≤ 14 and (p,q) ∈ {(3,−4), (4,−5), (2,−3), (−2,7), (2,5), (5,7)} (for (2,−3): 1,720 of type (L), 2,352 of type (Y₁)). `--stabilizer 12` (Proposition 6.5): for (p,q) ∈ {(3,−4), (2,−3), (2,5), (3,5), (−2,7)}, among the 2,920 matrices with entries ≤ 12 the kernel-preserving ones are exactly those in Γ^± (76, 180, 100, 52, 60 matrices). `--check-t7 3 8 8` and `--check-t7 4 8 8` (Proposition 6.2): 120 resp. 64 words θ_M(xᵃyᶜ) (|M| ≤ 8, 2 ≤ |a|,|c| ≤ 8) have the necklace of b^{±1}; none has an elliptic root. A scratch run (|M| ≤ 6, exponents ≤ 7, n = 3, 4) confirmed that all of them are twists of the two decompositions of b, with exponents {2,3}.

**Experiment for the missing Lemma M (trefoil side).** `--lemma-m n L E LW` enumerates every cyclically reduced W₀ = (positive)(negative) word in A = xy, B = xyy with r + t ≤ L whose image has a necklace in the family of U_n, applies every twist given by a reduced word in A, B with ≤ LW syllables and |m| ≤ E (with or without D_x) for which the exponent vector lands in Λ, keeps the images that are conjugate to U_n^{±1} in H (exact invariant), and determines the type of each by Whitehead's algorithm (minimize, then search the level set for a word xᵃyᶜ).
```
python3 experiments/th04_island.py --lemma-m 3 11 2 3
#  n=3: reduced words 72, twists in the class of U_n^+-1: 62, by Whitehead type: {'other': 56, 'torus(3,4)': ['U', 'iU'], 'torus(2,7)': ['W', 'iW', 'ikW', 'kW']}
#  consistent with Lemma M: True
python3 experiments/th04_island.py --lemma-m 4 13 2 3
#  n=4: reduced words 110, twists in the class of U_n^+-1: 86, by Whitehead type: {'other': 80, 'torus(4,5)': ['U', 'iU'], 'torus(2,9)': ['W', 'iW', 'ikW', 'kW']}
#  consistent with Lemma M: True
python3 experiments/th04_island.py --lemma-m 2 9 2 3
#  n=2: reduced words 42, twists in the class: 38, {'other': 32, 'torus(2,5)': ['W','iW','ikW','kW'], 'torus(2,3)': ['U','iU']}   -> True
python3 experiments/th04_island.py --lemma-m-control 8 2 3      (positive control: AK(2), x²Y³ frozen, partner b)
#  n=2: reduced words 20, twists in the class: 16, {'other': 8, 'torus(2,3)': ['NEW','NEW','NEW','partner'], 'primitive': ['NEW','NEW'], 'torus(2,5)': ['NEW','NEW']}   -> False
```
So, in a search region different from and much larger in matrix size than G's (it reaches ικW₃, whose matrix has entries up to 33), the class of U_n^{±1} contains exactly the six torus-type words and no primitive word, while the control class (where research-g found primitive words) does show extra primitive and torus-type words. This is bounded evidence for Lemma M, not a proof.

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

### 6.3 Normal form of bases modulo twists, and the theorem on the T(n,n+1) side (T8; proved here)

Classical facts used. (F1) Bases of F₂ with the same exponent matrix are simultaneously conjugate (Nielsen). (F2) SL₂(ℕ) is the free monoid on [[1,1],[0,1]] and [[1,0],[1,1]], the matrices of the positive substitutions λ = (x ↦ x, y ↦ xy) and ρ = (x ↦ xy, y ↦ y); so a basis with non-negative exponent matrix is, up to order and simultaneous conjugacy, a pair of positive words. (F3) (x, v) is a basis iff v = xⁱy^{±1}x^{i′}.

**Lemma 6.3 (normal form).** Let |p|,|q| ≥ 2 be coprime and (u,v) a basis of F₂. After applying a twist of R = xᵖyᑫ, a simultaneous conjugation, and possibly inverting u, v, the pair has one of the forms:
- (L) one of u, v is a letter x or y;
- (Y_k) u = w₁(A,B), v = w₂(A,B) with A = xyᵏ, B = xy^{k+1}, 1 ≤ k ≤ |q| − 2, and (w₁,w₂) a basis of F(A,B) consisting of positive words;
- (X_j) the same with A′ = yxʲ, B′ = yx^{j+1}, 1 ≤ j ≤ |p| − 2.

*Proof.* Two primitive vectors with determinant ±1 lie, after sign changes, in one closed quadrant (if a, c > 0, b > 0 > d then |ad − bc| ≥ 2). So after inverting u, v and applying σ_x, σ_y (twists), the exponent matrix [[a,b],[c,d]] (columns e(u), e(v)) is non-negative, and by (F1), (F2) the pair is a pair of positive words; induct on |u| + |v|. If a word has length 1 we are in (L). Otherwise a, b, c, d ≥ 1, the slopes c/a, d/b differ by 1/(ab) and no integer lies strictly between them, so both lie in [k, k+1] for an integer k ≥ 0. If k ≥ 1, the matrix factors as [[1,0],[1,1]]ᵏ[[1,1],[0,1]]M′ with M′ ∈ SL₂(ℕ) up to order of columns, so u, v are positive words w₁, w₂ in ρᵏλ(x) = xyᵏ and ρᵏλ(y) = xy^{k+1}, where (w₁,w₂) is a positive basis. The automorphism x ↦ xy^{qj}, y ↦ y equals β^{j} followed by conjugation by y^{−qj}, so it is a twist; it replaces k by k + qj. Choose j with k₀ = k + qj ∈ [0, |q|−1]. If 1 ≤ k₀ ≤ |q|−2 we are in (Y_{k₀}). If k₀ = 0 the new pair consists of positive words in x and xy and is strictly shorter (here k ≥ |q| ≥ 2). If k₀ = |q|−1, use k₀ − |q| = −1 instead: the new pair consists of positive words in xY and x; after σ_y these are positive words in xy and x, a strictly shorter positive pair (B does occur in a basis). In both cases apply the induction hypothesis. If k = 0, both slopes lie in [1/(j+1), 1/j] for some j ≥ 1 and the same argument with x, y, p, α in place of y, x, q, β applies. ∎

**Theorem 6.4 (T8).** Let n ≥ 3, G_n = ⟨x,y | xⁿ = y^{n+1}⟩, b = xyxYXY. If W = cyc(uᵃvᶜ) for a basis (u,v) of F₂ and integers a, c (in particular: if W is a torus-type or a primitive cyclic word) and W is conjugate to b or b⁻¹ in G_n, then W = b or W = b⁻¹ as cyclic words. Hence **with the T(n,n+1) relator frozen, AK(n) has no torus-type or primitive ACM neighbour other than itself, for every n ≥ 3, with arbitrary conjugators and automorphisms.** (For primitive words this is Proposition G2(a) of research-g, re-proved here.)

*Proof.* Here p = n, q = −(n+1), Q = C_n * C_{n+1}. Record a necklace as the cyclic list of pairs (s-exponent, exponent of the following t-syllable). Then N_b = [(1,1),(1,−1),(−1,−1)], and the set ℱ of images of N_b^{±1} under the factor inversions has four elements: the two with s-exponents (1,−1,−1) are [(1,δ),(−1,−δ),(−1,δ)], δ = ±1 (δ = 1 is N_b⁻¹), and the other two are their inverses. Every member of ℱ satisfies (∗) of §6.2. In terms of pairs (t-exponent, following s-exponent) the members with t-exponents (1,−1,−1) are again [(1,δ),(−1,−δ),(−1,δ)] (δ = 1 is N_b).

Let W = cyc(uᵃvᶜ). By Lemma 6.3 there is a twist γ such that W′ = γ⁻¹(W) = cyc(u′^{a′}v′^{c′}) with (u′,v′) in normal form (a′ = ±a, c′ = ±c). By Lemma 2.1(b) the necklace of W′ lies in ℱ; in particular it has 6 syllables.

*Form (L).* Up to the symmetry x ↔ y and inversion of W′, u′ = x, v′ = x^{i}y^{ε}x^{i′} (F3), and W′ = cyc(x^{a′+e}y^{ε}(x^{e}y^{ε})^{c′−1}) with e = i + i′, c′ ≥ 1 (c′ = 0 gives at most one syllable). If sᵉ = 1 there are ≤ 2 syllables. If sᵉ ≠ 1 ≠ s^{a′+e}, all t-exponents equal ε. If s^{a′+e} = 1 ≠ sᵉ, the necklace is (t^{2ε}, sᵉ, tᵋ, sᵉ, …) with t^{2ε} ≠ 1, and all s-exponents are equal. Each case contradicts (∗) or the length 6. (For u′ = y exchange the roles; s² ≠ 1 and t² ≠ 1 because n ≥ 3.)

*Form (Y_k), 1 ≤ k ≤ n−1.* W′ = cyc η(W₀), where η: A ↦ xyᵏ, B ↦ xy^{k+1} and W₀ = cyc(w₁^{a′}w₂^{c′}) is a cyclically reduced word in A, B. As w₁, w₂ are positive, W₀ is positive, negative, or of the form α₁⋯α_r·β₁⁻¹⋯β_t⁻¹ with α_i, β_i ∈ {A,B}, α_r ≠ β₁, β_t ≠ α₁. Write k_i, l_i ∈ {k, k+1} for the y-exponents of α_i, β_i; all of k, k+1 are nonzero modulo n+1.
- W₀ positive or negative: the letters x^{±1} of W′ are isolated and of one sign, so all s-exponents are equal: not in ℱ.
- t = 1 (so α₁ = α_r ≠ β₁; r = 1 gives a single syllable): W′ = (yᵉ, x, y^{k₂}, x, …, y^{k_{r−1}}, x) with e = k₁ + k_r − l₁ ∈ {k−1, k+2}. If yᵉ ≠ 1 in Q all s-exponents are 1. If yᵉ = 1, two letters x merge and the necklace has 2(r−2) syllables with s-exponents (2,1,…,1); six syllables and ℱ would need r = 5, 2 ≡ −1 (mod n), i.e. n = 3, and three t-exponents in {k, k+1} ⊂ [1,3] that are ≡ ±1 (mod 4) and not all equal, which is impossible. The case r = 1 < t is the inverse situation.
- r, t ≥ 2: W′ = (y^{ε₁}, x, y^{k₂}, …, y^{k_{r−1}}, x, y^{ε₂}, X, Y^{l₂}, X, …, Y^{l_{t−1}}, X) with ε₁ = k₁ − l_t = ±1 and ε₂ = k_r − l₁ = ±1. No run vanishes in Q, so there are 2(r+t−2) syllables and r + t = 5. For (r,t) = (2,3) the necklace is [(1,ε₂), (−1,−l₂), (−1,ε₁)], which lies in ℱ iff ε₁ = ε₂ = δ and l₂ ≡ δ (mod n+1). For δ = 1: l₂ = k = 1 and W₀ = B²A⁻³, W′ = cyc((xyy)²(xy)⁻³) = b⁻¹. For δ = −1: l₂ = k+1 = n and W₀ = A²B⁻³, W′ = cyc((xy^{n−1})²(xyⁿ)⁻³) = τ₀σ_y(b⁻¹), where τ₀ = (x ↦ xy^{n+1}, y ↦ y) is a twist. The case (3,2) gives the inverses.

*Form (X_j), 1 ≤ j ≤ n−2.* The same computation with x and y exchanged (now the isolated letters are y^{±1}, and the x-runs j, j+1 are nonzero modulo n). Positive or negative W₀: all t-exponents equal. t = 1: all t-exponents equal, or after a merge a t-exponent 2 ≢ ±1 (mod n+1). r, t ≥ 2: (r,t) = (2,3) gives [(1,ε₂), (−1,−l₂), (−1,ε₁)] in (t, following s) pairs, in ℱ iff ε₁ = ε₂ = δ, l₂ ≡ δ (mod n): δ = 1 gives j = 1 and W′ = cyc((yxx)²(yx)⁻³) = b; δ = −1 gives j = n−2 and W′ = cyc((yx^{n−2})²(yx^{n−1})⁻³) = τ₁σ_x(b) with the twist τ₁ = (y ↦ yxⁿ).

So in every case W′ is a twist of b^{±1}, hence W = γ(W′) is a twist of b^{±1}. Both W and b^{±1} are partners of xⁿY^{n+1}. As (n−1)n ≥ 3 and neither n nor n+1 is 2, Corollary 2.3 gives W = b^{±1} or W = σ(b^{±1}) = b^{∓1}. ∎

The case analysis was also checked by brute force for n = 3, 4, 5 (all words W₀ with r + t ≤ 7, all admissible k and j): the only cyclic words with necklace in ℱ are b^{±1} (k = 1; j = 1) and the two twist images (k = n−1; j = n−2).

**Theorem 6.6 (T10; the T(2,2n+1) sides).** Let n ≥ 2, T = ⟨x,y | x² = y^{2n+1}⟩ (frozen relator x⁻²y^{2n+1}), Q = C₂ * C_{2n+1}, and let P be a torus-type word whose necklace in Q has L/2 ∈ {5, 7} syllable pairs, all t-exponents in {n, n+1} modulo 2n+1, both values occurring and neither occurring more than L/2 − 2 times. If W = cyc(uᵃvᶜ), (u,v) a basis, is conjugate to P^{±1} in T, then W ∈ {P, P⁻¹, ι′(P), ι′(P)⁻¹}, ι′ = (x ↦ y^{2n+1}X). This applies to the partners of both island nodes with a T(2,2n+1) relator: N_n = (xYⁿ)²(xY^{n+1})³ (t-exponents n+1, n+1, n, n, n) at node 2, and the partner at node 3 (t-exponents n+1, n, n, n+1, n, n, n+1; §4.2). **So with the T(2,2n+1) relator frozen, nodes 2 and 3 have no torus-type or primitive ACM neighbour other than themselves (n ≥ 2).**

*Proof.* Here |p| = 2, so form (X_j) of Lemma 6.3 does not occur, and (Y_k) has 1 ≤ k ≤ 2n−1; k, k+1 ∈ [1, 2n] are nonzero modulo 2n+1 and s = s⁻¹. Let ℱ be the necklace of P^{±1} and its image under t ↦ t⁻¹ (which exchanges the values n and n+1). As in Theorem 6.4, W = γ(W′) with γ a twist, W′ in normal form with necklace in ℱ.
- *Form (L), u′ = x:* W′ = cyc(x^{a′+e}yᵋ(xᵉyᵋ)^{c′−1}). For e even there are ≤ 2 syllables; for e odd the t-exponents are all ε, or (2ε, ε, …, ε); but ±1 ∉ {n, n+1} modulo 2n+1 for n ≥ 2. *u′ = y:* W′ = cyc(y^{a′+e}xᵋ(yᵉxᵋ)^{c′−1}); if tᵉ = 1 there are ≤ 2 syllables; if tᵉ ≠ 1 the t-exponents are (a′+e, e, …, e), or after the cancellation s·s = 1 they are (2e, e, …, e); in both cases one value occurs on all but one syllable, which is excluded.
- *Form (Y_k), W₀ positive:* the necklace is the cyclic sequence (k_i) ∈ {k, k+1}; both n and n+1 must occur, so k = n and W₀ is the unique cyclic word in A, B spelling the necklace. *W₀ negative:* the inverse situation.
- *W₀ = α₁⋯α_rβ₁⁻¹⋯β_t⁻¹ with r, t ≥ 2:* the necklace contains the t-exponents ε₁, ε₂ = ±1 ∉ {n, n+1}.
- *t = 1 < r* (or r = 1 < t, by inversion): W′ = (yᵉ, x, y^{k₂}, …, y^{k_{r−1}}, x), e ∈ {k−1, k+2}. If yᵉ ≠ 1 in Q, the necklace is (e, k₂, …, k_{r−1}); e ∈ {n, n+1} and k_i ∈ {k, k+1} ∩ {n, n+1} force all k_i to be equal (k = n+1 and k_i = n+1, or k = n−1 and k_i = n): one value on all but one syllable. If yᵉ = 1 (k = 1 or k = 2n−1), then s·s cancels and the neighbouring t-syllables merge to an exponent in {2k, 2k+1, 2k+2}, nonzero modulo 2n+1; the remaining exponents k₃, …, k_{r−2} lie in {k, k+1} ∩ {n, n+1}, which is empty unless n = 2, where it has one element: again one value on all but one syllable.

So W′ or its inverse is a positive word S(E) = η_n(W₀) spelling a necklace E ∈ ℱ, and ℱ = {E, −E, rev E, −rev E}. The twist (x ↦ xy^{2n+1})∘σ_y exchanges xyⁿ and xy^{n+1}, hence maps S(E) to S(−E); and σ(S(E)) = S(rev E)⁻¹. So all these words are twists of one another up to inversion. Applying the argument to W = P shows that P is a twist of some S(E)^{±1}; hence every W as above is a twist of P^{±1}, and Corollary 2.3 ({2, 2n+1} ≠ {2,3}) gives W ∈ {P^{±1}, ι′(P)^{±1}} (σ inverts torus-type cyclic words). ∎

### 6.4 The stabilizer of ker π is the twist group (proved here)

**Proposition 6.5.** Let |p|,|q| ≥ 2 be coprime. An automorphism θ of F₂ preserves ker π = ⟨⟨xᵖ, yᑫ⟩⟩ iff it is a twist. Equivalently: two bases whose images in Q are simultaneously conjugate up to factor automorphisms differ by a twist.

*Proof.* Let θ preserve ker π, so π∘θ = φ∘π with φ ∈ Aut(Q); φ(s) has order |p|, hence is conjugate to a power of s. Let (a,c) = e(θx). Replacing a by its absolutely least residue modulo pc (a power of A) or c by its least residue modulo qa (a power of B) strictly decreases |a| + |c| unless 2|a| ≤ |p||c| and 2|c| ≤ |q||a|, or ac = 0. So after composing θ with a twist from ⟨α,β⟩, either ac = 0 or (a,c) lies in Ω = {a, c ≠ 0, 2|a| ≤ |p||c|, 2|c| ≤ |q||a|}. If (a,c) ∈ Ω, the primitive word θx is conjugate to a word in which (say |a| ≤ |c|) the letters x^{±1} are isolated and the y-runs have length ⌊|c|/|a|⌋ or ⌈|c|/|a|⌉ ≤ ⌈|q|/2⌉ < |q| (Fact C of research-g, classical); so its image in Q is cyclically reduced with 2|a| ≥ 2 syllables, not of finite order: contradiction. Hence ac = 0, θx is conjugate to x^{±1} (not to y^{±1}, whose image has order |q|), and after an inner automorphism and σ_x, θx = x. By (F3) θy = xⁱy^{±1}x^{i′}, and its image s^{i}t^{±1}s^{i′} has finite order only if s^{i+i′} = 1. So θ is, up to an inner automorphism, y ↦ x^{pm}y^{±1}, a twist. The converse is Lemma 2.1(b). ∎

Experiment: for (p,q) ∈ {(3,−4), (2,−3), (2,5), (3,5), (−2,7)} and all 2,920 matrices M ∈ GL₂(ℤ) with entries ≤ 12 in absolute value, θ_M preserves ker π iff M ∈ Γ^± (`th04_island.py --stabilizer 12`).

### 6.5 Exactly what is missing for the island theorem

Theorems 6.4 and 6.6 settle the T(n,n+1) side (n ≥ 3) and both T(2,2n+1) sides (n ≥ 2), uniformly in n. One statement is missing:

**Missing Lemma M (trefoil side).** *For n ≥ 3, the only words cyc(uᵃvᶜ), (u,v) a basis, conjugate to U_n^{±1} in H = ⟨x,y | x² = y³⟩ are the six words U_n, ιU_n, W_n, ιW_n, κW_n, ικW_n and their inverses.*

Why it is harder. The necklace length 4n+2 grows with n; the frozen group is the exceptional one (Proposition 2.4 must replace Corollary 2.3); and the trick that killed mixed words in Theorem 6.6 (the junction exponents ±1 are not admissible) fails, because in C₃ every nonzero exponent is ±1. By Lemma 6.3 the reduced words are of form (L) or (Y₁) (words in A = xy, B = xyy; (X_j) is empty), so M is the classification of the cyclic words W₀ = α₁⋯α_r·β₁⁻¹⋯β_t⁻¹ in A, B whose image in C₂ * C₃ has the t-exponent necklace 1ⁿ2^{n+1} or 2ⁿ1^{n+1}, where now cancellations s·s = 1 and y³ = 1 do occur. The expected reduced solutions are the positive words AⁿB^{n+1}, A^{n+1}Bⁿ (from U_n) and the mixed words coming from W_n (up to inversion, W_n = cyc η₁(A^{n+2}B⁻¹A^{−(n−1)}B⁻¹); checked for n ≤ 5) and its twists. A scratch enumeration shows what is different: for n = 3 there are 72 distinct reduced cyclic words (r + t ≤ 11; 42 for n = 2, r + t ≤ 9) whose necklace lies in the family of U_n, with |ab_T| ranging from 1 to 61, and only W₃ has |ab_T| = 1 in that list. So on the trefoil side the necklace does not determine the twist class (single-letter blocks produce cascades of cancellations s·s = 1, y³ = 1), and the abelianization condition must be used inside the classification of reduced words, not only at the end as in Theorems 6.4 and 6.6. One then needs, in addition, that a reduced word whose exponent vector is not Γ^±-equivalent to a point of Λ has no partner among its twists (a uniqueness statement for the ping-pong fundamental domain). I did not solve this.

**Corollary 6.7 (reduction of the island theorem to one conjugacy class; proved).** Let n ≥ 3. All three nodes have the same trefoil-side class (that of U_n^{±1} in H), and by Theorems 6.4 and 6.6 no move with the T(n,n+1) or the T(2,2n+1) relator frozen leads from a node to a different torus-type or primitive state. Hence, if Lemma M holds — i.e. if one conjugacy class of the trefoil group contains no torus-type cyclic word besides the six listed (primitive words are already excluded by G2(b)) — then the torus-type presentations reachable from AK(n) by ACM moves with a torus-type relator frozen are exactly the three Aut(F₂)-orbits of §4.2.

In that case every AC trivialization of AK(n), viewed as an ACM path, would have to leave the island through a state in which the frozen relator's group is not a torus-knot group. Without Lemma M this conclusion rests, on the trefoil side, on the bounded enumerations of research-g and §5.

## 7. Failed attempts (precise reasons)

1. **A syllable-length bound for torus-type words.** My first plan was a finite reduction like G's Lemma G4: "if θ_M(x^{p′}y^{q′}) has L syllables in Q then M and p′, q′ are bounded in terms of L". This is false: twists change M arbitrarily and keep the necklace (§0). The correct replacement is Lemma 6.3 (normal form modulo twists) plus T1 (the central exponent pins the twist).
2. **Tree method for the whole classification.** Lemma 6.1 and Proposition 6.2 handle elliptic roots cleanly, but for two hyperbolic roots whose axes overlap longer than their translation lengths there is no formula for the translation length of gᵃhᶜ, and I could not finish the classification on the tree. Switching to positive (Christoffel-type) words made the T(n,n+1) and T(2,2n+1) sides finite. §6.1–6.2 are kept because they are independent of the classical facts on primitive words used in §6.3.
3. **The trefoil side.** Not solved (Lemma M, §6.5). The method of Theorem 6.6 fails at its key step (junction exponents ±1 are admissible in C₃), and in C₂ * C₃ the cancellations s² = 1, t³ = 1 interact. I only proved closure under twists (T5) and Proposition 2.4.
4. **A "necklace no-hidden-cancellation" lemma** ("for a reduced basis the number of syllables equals the number of runs") is false as first stated: patterns A·B⁻¹·A and B·A⁻¹·B create runs of length k−1 and k+2, which vanish for k = 1 or k = |q|−2. The proofs of Theorems 6.4 and 6.6 treat these patterns explicitly (the cases t = 1 and r = 1).

## 8. Honest limits

- Nothing here decides whether AK(3) is AC-trivial. T8 and T10 are statements about single ACM moves with a torus-type relator frozen and a torus-type or primitive target; a trivialization may pass through states with no torus-type relator (most states of AK(3)'s class), about which this note says nothing.
- The island theorem itself is **not** proved; Lemma M (trefoil side) is open. On that side the claim "exactly six words" is a bounded observation: |M| ≤ 16, exponents ≤ 24, length ≤ 160 for n = 3, 4, 5 (G's enumerator), and the `--lemma-m` experiment for n = 2, 3, 4 (reduced forms with r + t ≤ 2n+5, twists of ≤ 3 syllables).
- Classical inputs, cited and not re-proved: Nielsen (Out(F₂) = GL₂(ℤ); bases with the same matrix are conjugate; commutator criterion), the structure of primitive/positive bases (Christoffel words; Osborne–Zieschang, Cohen–Metzler–Zimmermann), the conjugacy theorem for free products (Lemma J0), and, only for §6.1–6.2, standard facts on isometries of trees (Culler–Morgan). Research-f's Prop. F3 is used for §4.2, and through it Burde–Zieschang/Kurosh as cited there.
- The proofs of Theorems 6.4 and 6.6 are case analyses written under time pressure; each case was cross-checked by brute force for small n (§5), which checks the analysis of the reduced forms, not Lemma 6.3 or Theorem 2.2 themselves (those have their own checks: `--stabilizer`, self-test (a)).
- T4 for n ≠ 3 is proved, not certified; the n = 3 certificate was replayed by `elementary_verify.py`. That AK(n)'s class is closed under Aut(F₂) is known here only for n = 3 (research-d, Lemma D6); it is not used in T1–T10.
- Literature access was limited; no novelty is claimed. Zieschang's 1977 classification of generating pairs of ⟨x,y | xᵖ = yᑫ⟩ is likely to contain Proposition 6.5 in another form.

## 9. Advice to the coordinator (ranked)

1. **Prove Lemma M (trefoil side) — it is the only gap to the island theorem.** Concretely: classify the torus-type cyclic words W₀ = cyc(w₁ᵃw₂ᶜ) in A = xy, B = xyy whose image in C₂ * C₃ is 1ⁿ2^{n+1} or its mirror and whose exponent vector is Γ^±-equivalent to a point of Λ, then apply Proposition 2.4. `lemma_m_experiment` in `th04_island.py` lists the candidates for small n; the torus-type condition on W₀ (not used in Theorems 6.4, 6.6) is essential here, since 56 of the 62 words found for n = 3 are in the class but not of torus type.
2. **Use the method beyond the island.** Lemma 6.3 + Theorem 2.2 give an exact, search-free classification of *all* torus-type and primitive ACM neighbours of any state with a torus-type relator other than a trefoil relator. Apply it to C3, C4 and I's family T(a;p,q) (their torus relators are T(2,7), T(2,5), T(4,7), …): it decides rigorously whether their torus graphs can ever reach defect 2, which G and I could only search.
3. **Do not expect a trivialization of AK(n) inside the torus locus.** Two of the three sides are now closed by theorem for all n; the island is a dead end for constructive work, as G suspected. Constructive effort should freeze non-torus relators (G's BS(3,4) moves, O's Gieseking relator).
4. The trefoil group is exceptional for a structural reason (Proposition 2.4: only for {2,3} do twists preserve partners). Any argument that treats "the trefoil side" like the others will fail at n = 2; this is a useful sanity test for future proofs.

## 10. Files written

- `research/research-th04.md` (this note).
- `experiments/th04_island.py`: `--lemma-m`, `--lemma-m-control` (experiment for Lemma M and its positive control); `--selftest` (Theorem 2.2 by brute force for 12 groups, trefoil exceptions, Lemma 3.1, memberships of the six words for n ≤ 8, case analyses of Theorems 6.4/6.6 for small n, Proposition 6.5 for small matrices, Proposition 6.2 consistency); `--enumerate`, `--check-t8`, `--check-t2side`, `--stabilizer`, `--check-t7`, `--write`.
- `certificates/th04_ak3_to_kappa_node.json` (262 KB): AK(3) → third island node, 6,774 moves, format `ordinary-ac-elementary-v1`.

## References

- Repository notes research-a … research-o; used: research-d (Lemma D6), research-f (Prop. F3), research-g (Lemma 1, Lemma G0, Theorem G1, Prop. G2, Fact C, `g_torus.py`, `g_cert.py`), research-j (Lemma J0).
- J. Nielsen, Math. Ann. 78 (1918) (automorphisms of F₂; commutator criterion).
- R. P. Osborne, H. Zieschang, Invent. Math. 63 (1981); M. Cohen, W. Metzler, A. Zimmermann, Math. Ann. 257 (1981); J. Berstel, A. Lauve, C. Reutenauer, F. Saliola, *Combinatorics on Words: Christoffel Words and Repetitions in Words* (2008) (primitive elements and positive bases of F₂).
- W. Magnus, A. Karrass, D. Solitar, *Combinatorial Group Theory* (free products, conjugacy).
- M. Culler, J. Morgan, *Group actions on ℝ-trees*, Proc. LMS 55 (1987), §1 (translation lengths, ping-pong).
- H. Zieschang, *Generators of the free product with amalgamation of two infinite cyclic groups*, Math. Ann. 227 (1977) (not consulted; cited as the likely source of Proposition 6.5).

## Coordinator's check (2026-11-09, Los Angeles time)

**This agent stopped at about 04:56–04:57 UTC because the session's model ran out of usage credits, shortly before its deadline and before handing back a final report.** The text above is its last saved version; it already contained a status line, the honest-limits and advice sections, the list of files and the references, so it is published as written. The coordinator did not edit it.

- Mechanical checks re-run by the coordinator: every self-test shipped with this note passes, and every certificate `certificates/<this agent's id>_*.json` in format `ordinary-ac-elementary-v1` replays under `python3 experiments/elementary_verify.py` (certificates in other formats, if any, are not AC trivializations and are labelled by the note itself).
- The proofs were **not** re-derived by the coordinator except where stated below; for independent verdicts on the central claims see the referee notes research-th19.md (TH01–TH09) and research-th20.md (TH10–TH18), which were completed after the same interruption.
