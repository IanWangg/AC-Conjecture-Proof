# Research TH12: the generator area of AK(n) is exactly n+4, and linear lower bounds on the number of moves

Date: 2026-11-09 (Los Angeles). Independent research agent TH12 (round 5, theory round; seed: area and Dehn-function lower bounds on AC complexity).

**Status.** Complexity results only. **No AK(3) trivialization, no proof of non-triviality, no counterexample, nothing on the full conjecture.** Every statement is labelled *proved here*, *recalled*, *experiment*, or *open*. Nothing below is an obstruction: all quantities are finite for every balanced presentation of the trivial group, and by K2 no such quantity can separate AC classes.

## 0. Central claims (all proved here; machine checks in §7)

Notation: F = F(x,y), X = x⁻¹, Y = y⁻¹; AK(n) = (r,s) with r = xⁿY^(n+1), s = xyxYXY, Δ = xyx. An *expression* of a word w over a pair U = (u₀,u₁) is a finite list of factors (gᵢ, jᵢ, εᵢ) with w = ∏ gᵢ u_{jᵢ}^{εᵢ} gᵢ⁻¹ in F. Its *count vector* is (c₀,c₁), c_j = number of factors with jᵢ = j; its *radius* is max |gᵢ|. Area_U(w) = min (c₀+c₁), A(U) = max(Area_U(x), Area_U(y)) ("generator area"). μ, κ denote the numbers of multiplication instructions (E's ids 3–6) and conjugation instructions (ids 7–14) of an instruction path.

- **Theorem 1 (count-matrix calculus).** An instruction path U₀ → … → U_m = (x,y) yields explicit expressions of x and y over U₀ whose 2×2 count matrix is a product of μ elementary matrices (up to permutations), whose signed count matrix is the inverse exponent-sum matrix of U₀, and whose conjugators are sub-products of the κ conjugation letters. Hence A(U₀) ≤ F_(μ+2) (Fibonacci) and radius ≤ κ.
- **Theorem 2 (exact generator area).** For every n ≥ 1: Area_AK(n)(x) = n+4 and Area_AK(n)(y) = n+3. Every expression of x uses ≥ 3 conjugates of r^{±1} and ≥ n+1 of s^{±1}; every expression of y uses ≥ 3 and ≥ n; both minima are attained simultaneously by explicit identities (I_x), (I_y).
- **Corollary (the seed is closed negatively).** The abelianization already forces area ≥ n+2, so the area of AK(n) is within 2 of the trivial bound; area/Dehn-function arguments (in F or in any quotient, with any conjugation-invariant norm) can never give more than μ ≥ log_φ(n) + O(1) for AK(n).
- **Theorem 3.** Every instruction path from AK(n) to (x,y) has **μ ≥ n+2** multiplications (abelianization alone gives exactly n+1; the extra 1 uses Theorem 2).
- **Theorem 4.** For n ≥ 4 every instruction path from AK(n) to (x,y) has **κ ≥ n−3** conjugations.
- **Corollary 5.** d_F(AK(n)) ≥ 2n−1 for n ≥ 4: every AC trivialization of AK(n) by the 15 instructions, and every `ordinary-ac-elementary-v1` certificate, has at least 2n−1 moves. For n = 3 this method gives only ≥ 6 (E's exhaustive bound is 15); it exceeds 15 from n = 9 on. As far as I can see this is the repository's first lower bound on d_F(AK(n)) valid for all n and growing with n; it is a complexity statement, not an obstruction.

## 1. Previous work read and choice of direction

Read: `README.md` in full; B (§1, §4), E (§2–5, §8–9), K (§3, §6–9) in full; status paragraphs of A, C, D, F–J, L–O. Used and re-checked: E's instruction alphabet and Fact 0 (an elementary-v1 primitive is one instruction); B §1 (z = xⁿ central, Δ conjugates x to y); E's tables (d_F(AK(1)) = 8, d_{N₁}(AK(n)) = n+2 for n ≤ 4, d_F(AK(3)) ≥ 15); K2/K3.

Direction: I kept the seed (area as a complexity measure) but its expected outcome reversed. The seed hoped for a growing lower bound A(AK(n)) ≥ g(n) leading to a move bound. I first computed the area exactly (Theorem 2): it is n+4, essentially the abelian bound, so that route provably yields nothing beyond a logarithm. I then replaced "total area" by two finer by-products of the same bookkeeping that *are* forced to be linear: the L/R-word of the count matrix (Theorem 3) and the spread of the conjugators of the s-factors (Theorem 4, via a permutation model in which r acts trivially and s fixes a window — the "stability-type" idea of the seed, used for conjugator length instead of area). New relative to A–O: none of the notes contains area/count matrices, an exact area, or a bound on d_F(AK(n)) for general n (E has n ≤ 4 abelian values by BFS). Not duplicated: TH07 bounds *peak length* by frozen-relator arguments; here only *numbers of moves* are bounded.

## 2. The count-matrix calculus (proved here)

Instructions (E §2): inversion of u_j; swap; u_i ← u_i u_j^ε (ε = ±1, j ≠ i); u_j ← h u_j h⁻¹ for a letter h. To each instruction attach a matrix g ∈ GL₂(ℤ): inversion of u_j ↦ diag with −1 in place j; swap ↦ P = [[0,1],[1,0]]; u₀ ← u₀u₁^ε ↦ [[1,ε],[0,1]]; u₁ ← u₁u₀^ε ↦ [[1,0],[ε,1]]; conjugation ↦ I. |g| is the entrywise absolute value. L = [[1,1],[0,1]], R = [[1,0],[1,1]].

**Lemma 0 (signed counts are forced).** Let E_U be the exponent-sum matrix of U (rows u₀,u₁; columns x,y), assumed unimodular. In every expression of w over U the signed counts σ_j = Σ_{jᵢ=j} εᵢ satisfy (σ₀,σ₁) = ab(w)·E_U⁻¹. In particular c_j ≥ |σ_j| and c_j ≡ σ_j (mod 2). *Proof.* Abelianize the expression. ∎

**Theorem 1.** Let U₀ → U₁ → … → U_m be instructions, g_k the matrix of the k-th one (from U_(k−1) to U_k). Given an expression of w over U_m with count vector c, signed count σ, there is an expression of w over U₀ with

    count vector  c·|g_m|·|g_(m−1)|⋯|g₁|,      signed count  σ·g_m g_(m−1)⋯g₁,

and each of its conjugators has the form g·h_(k₁)h_(k₂)⋯h_(k_q), where g is a conjugator of the given expression, k₁ > k₂ > … > k_q are indices of conjugation instructions, and h_k is the letter with u_j^(k) = h_k u_j^(k−1) h_k⁻¹.

*Proof.* Downward induction on k; replace every factor f·(u_j^(k))^δ·f⁻¹ as follows. Inversion of u_j: by f·(u_j^(k−1))^(−δ)·f⁻¹. Swap: relabel. Conjugation u_j^(k) = h u_j^(k−1) h⁻¹: by (fh)(u_j^(k−1))^δ(fh)⁻¹. Multiplication u₀^(k) = u₀^(k−1)(u₁^(k−1))^ε: for δ = 1 by f u₀^(k−1) f⁻¹ · f (u₁^(k−1))^ε f⁻¹, for δ = −1 by f (u₁^(k−1))^(−ε) f⁻¹ · f (u₀^(k−1))⁻¹ f⁻¹; factors on u₁ are unchanged. So a row vector (a,b) of counts becomes (a, a+b) and signed counts (α,β) become (α, εα+β): right multiplication by |g_k|, resp. g_k. Conjugators change only at conjugation instructions, by one letter on the right. ∎

**Corollary 1.1.** If U_m = (x,y), the trivial expressions of x and y give expressions over U₀ with count matrix C₀ = |g_m|⋯|g₁| (rows x,y), signed count matrix Σ₀ = g_m⋯g₁ = E_{U₀}⁻¹, and radius ≤ κ. C₀ is, up to row/column permutations, a product of μ matrices from {L,R}; hence every entry of C₀ is ≤ F_(μ+1), every row sum ≤ F_(μ+2), the total ≤ F_(μ+3) (F₁ = F₂ = 1). In particular

    A(U₀) ≤ F_(μ+2),   and for every w:  Area_{U₀}(w) ≤ F_(μ+2)·|w|.

*Proof.* Σ₀ = E⁻¹ is Lemma 0. Permutation matrices can be moved to one side (PLP = R). For a product M of μ letters L,R claim: entries ≤ F_(μ+1), row sums and column sums ≤ F_(μ+2), total ≤ F_(μ+3). True for μ = 0. M·L replaces columns (k₀,k₁) by (k₀,k₀+k₁): new entries are old entries or old row sums (≤ F_(μ+2)); a new row sum is an old row sum plus an old entry (≤ F_(μ+3)); new column sums are an old column sum and the old total (≤ F_(μ+3)); the new total is the old total plus an old column sum (≤ F_(μ+4)). M·R is symmetric. ∎

Remarks. (a) The bound is sharp for matrices (alternating words; checked for μ ≤ 14). (b) *1-Lipschitz reformulation:* for one instruction, A(U') ≤ 2A(U) and symmetrically, so log₂A is 1-Lipschitz on the instruction graph, in F and in every quotient Q (define A_Q with conjugates in Q; A_Q ≤ A_F). This is a "new computable-in-principle Lipschitz function" in the sense asked for in K §6; Theorem 2 shows it is useless for AK(n). (c) *ACM analogue.* If s' = g s^δ g⁻¹ · ∏_{i≤k} hᵢ r^{εᵢ} hᵢ⁻¹ (an ACM move with *insertion number* k), then an s'-factor becomes one s-factor and k r-factors: counts (c_r,c_s) ↦ (c_r + k·c_s, c_s), i.e. right multiplication by R^k (or L^k), the signed counts by the product of the k signed transvections; radius grows by max(|g|,|hᵢ|). Thus along an ACM path areas are bounded by the continuant of the insertion numbers, and Theorem 3 below holds with μ replaced by the total insertion number Σk. No bound in terms of the *number* of ACM moves follows (k is unbounded per move).

## 3. The exact generator area of AK(n) (proved here)

**Theorem 2.** Let n ≥ 1, r = xⁿY^(n+1), s = xyxYXY, Δ = xyx.

(i) The following identities hold in F (conjugation written g·u·g⁻¹):

    (I_x)  x = [ ∏_{i=0}^{n} (Δ⁻¹yⁱ) s (Δ⁻¹yⁱ)⁻¹ ] · Δ⁻¹ r⁻¹ Δ · (yx)⁻¹ r (yx) · x⁻¹ r⁻¹ x
    (I_y)  y = r⁻¹ · [ ∏_{i=0}^{n−1} yⁱ s y⁻ⁱ ] · (yⁿxy⁻ⁿ) r⁻¹ (yⁿxy⁻ⁿ)⁻¹ · (yⁿxy^(−n−1)) r (yⁿxy^(−n−1))⁻¹

with count vectors (c_r,c_s) = (3, n+1) and (3, n).

(ii) Every expression of x over AK(n) has c_r ≥ 3, c_r odd, c_s ≥ n+1; every expression of y has c_r ≥ 3, c_r odd, c_s ≥ n.

(iii) Consequently Area(x) = n+4, Area(y) = n+3, A(AK(n)) = n+4, and the minimal count matrix [[3,n+1],[3,n]] is attained. In (I_x) the three r-conjugators have length ≤ 3 for every n.

*Proof.* (i) Three exact free-group facts:
(a) Δ x Δ⁻¹ = s·y, because s·y·Δ = xyxYXY·y·xyx = xyx·x = Δx.
(b) xⁿ = r·y^(n+1), hence xⁿ y x⁻ⁿ y⁻¹ = r y^(n+1)·y·y^(−n−1) r⁻¹ y⁻¹ = r · y r⁻¹ y⁻¹.
(c) (sy)^k = [∏_{i=0}^{k−1} yⁱ s y⁻ⁱ]·y^k.
For (I_x): by (a),(c), Δ x^(n+1) Δ⁻¹ = P·y^(n+1) with P = ∏_{i=0}^{n} yⁱsy⁻ⁱ, so Δ⁻¹·P·r⁻¹·Δ = Δ⁻¹·(Δx^(n+1)Δ⁻¹ y^(−n−1))·r⁻¹Δ = x^(n+1)Δ⁻¹(r y^(n+1))⁻¹Δ = x^(n+1)Δ⁻¹x⁻ⁿΔ. Next Δ⁻¹xⁿΔx⁻ⁿ = XYX·xⁿ·xyx·x⁻ⁿ = X·(Y xⁿ y x⁻ⁿ)·x, and Y xⁿ y x⁻ⁿ = Y(xⁿ y x⁻ⁿ Y)y = (Y r y)·r⁻¹ by (b); so Δ⁻¹xⁿΔx⁻ⁿ = (yx)⁻¹ r (yx)·x⁻¹r⁻¹x. The product of the two displayed elements is x^(n+1)Δ⁻¹x⁻ⁿΔ·Δ⁻¹xⁿΔx⁻ⁿ = x.
For (I_y): by (a),(c), Δ xⁿ Δ⁻¹ = P'·yⁿ with P' = ∏_{i=0}^{n−1} yⁱsy⁻ⁱ. Put C = x⁻ⁿΔxⁿΔ⁻¹, so Δxⁿ Δ⁻¹ = xⁿC = r y^(n+1) C. Hence y^(n+1)·C·y⁻ⁿ = r⁻¹P', i.e. y = r⁻¹·P'·yⁿC⁻¹y⁻ⁿ. Now C = x⁻ⁿ·xyx·xⁿ·XYX = x(x⁻ⁿ y xⁿ Y)X and, using x⁻ⁿ = y^(−n−1)r⁻¹ and xⁿ = r y^(n+1), x⁻ⁿ y xⁿ Y = y^(−n−1) r⁻¹ y r yⁿ = (y^(−n−1) r⁻¹ y^(n+1))·(y⁻ⁿ r yⁿ). Therefore yⁿC⁻¹y⁻ⁿ = (yⁿx y⁻ⁿ) r⁻¹ (·)⁻¹ · (yⁿ x y^(−n−1)) r (·)⁻¹.
(Both identities are also verified by free reduction for n = 1,…,40, §7.)

(ii) E_AK(n) = [[n, −n−1],[1, −1]] has determinant 1 and inverse [[−1, n+1],[−1, n]]. By Lemma 0 the signed counts are (−1, n+1) for x and (−1, n) for y; so c_s ≥ n+1 (resp. n) and c_r is odd. Suppose c_r = 1 in an expression of w ∈ {x,y}. Then modulo ⟨⟨s⟩⟩, i.e. in B₃ = ⟨x,y | xyx = yxy⟩, w is conjugate to r⁻¹. Under the homomorphism B₃ → SL₂(ℤ), x ↦ L = [[1,1],[0,1]], y ↦ [[1,0],[−1,1]] (the braid relation holds: both sides equal [[0,1],[−1,0]]), w has trace 2 while r ↦ [[1,n],[0,1]]·[[1,0],[n+1,1]] has trace n²+n+2 > 2, as has r⁻¹. Contradiction; so c_r ≥ 3.

(iii) follows from (i) and (ii). ∎

**Corollary 2.1 (what area can and cannot give; proved here).**
(a) By Corollary 1.1 and Theorem 2(ii), the count matrix C₀ of any trivialization of AK(n) dominates [[3,n+1],[3,n]] entrywise, so F_(μ+3) ≥ 2n+7: μ ≥ 4 for n = 3 (μ ≥ 5 using det C₀ = ±1, since the only matrix of total 13 is [[3,4],[3,3]]), and in general only μ ≥ log_φ(2n+7) − O(1).
(b) No refinement of the *area* argument can do better: A(AK(n)) = n+4 is linear and within 2 of the abelian bound n+2. In particular for every homomorphism π: F → Q and every conjugation-invariant subadditive norm ν on Q (Hamming norm on permutations, rank(g−1) on matrices, the distance to 1 in a bi-invariant metric on a compact group, …) one has ν(πx) ≤ 3ν(πr) + (n+1)ν(πs) and ν(πy) ≤ 3ν(πr) + n·ν(πs); so no choice of (Q,ν) can certify an area larger than n+4. "Stability-type" inequalities for the pair (r,s) carry no information beyond Theorem 2, and the Lipschitz functions log₂A_Q of Remark (b) are bounded by log₂(n+4) uniformly in Q.
(c) The Dehn function of AK(n), as a presentation of the trivial group, satisfies δ(ℓ) ≤ (n+4)·ℓ. The Bridson/Lishak mechanism (*recalled, not checked here*: balanced presentations of the trivial group whose trivializations are huge because a group with large Dehn function is encoded in the relators) has nothing to grip on in the AK family.

(d) det [[3,n+1],[3,n]] = −3, while C₀ is unimodular: **no trivialization produces minimal expressions of x and y simultaneously.** Since C₀ ≡ Σ₀ (mod 2) entrywise, the total number of factors of the pair of expressions coming from any trivialization is ≥ 2n+9 (minimal possible total: 2n+7).

This is the rigorous negative answer to the seed: **the generator area of AK(n) is as small as it can possibly be**, so lower bounds on the number of moves must come from finer data than area. §4 extracts two such data from the same bookkeeping.

## 4. Linear lower bounds on the number of moves (proved here)

Throughout, a path is an instruction path AK(n) = U₀ → … → U_m = (x,y); Σ := E_AK(n)⁻¹ = [[−1,n+1],[−1,n]]; by Corollary 1.1, Σ = g_m⋯g₁ and C₀ = |g_m|⋯|g₁|, and by Theorem 2(ii) the first column of C₀ is ≥ (3,3).

### 4.1 Theorem 3: at least n+2 multiplications

**Theorem 3.** For every n ≥ 1, every instruction path from AK(n) to (x,y) contains at least n+2 multiplication instructions (at least 4 for n = 1). The abelianization alone gives n+1, and n+1 is attained by paths in ℤ².

*Proof.* *Step 1 (normal form of the product).* The group W of signed permutation matrices normalizes T = {L^{±1},R^{±1}}, and |dt| = |d||t|, |td| = |t||d| for d ∈ W. Moving all W-factors to the left (t·d = d·(d⁻¹td)) gives

    Σ = d·t₁⋯t_μ,   C₀ = |d|·|t₁|⋯|t_μ|,   tᵢ ∈ T, d ∈ W, det d = 1, so d ∈ {±I, ±S}, S = [[0,1],[−1,0]].

*Step 2 (free product length).* *Recalled:* PSL₂(ℤ) = ⟨a⟩ * ⟨b⟩ ≅ ℤ/2 * ℤ/3 with a = ±S, b = ±[[0,−1],[1,1]]. One checks S·[[0,−1],[1,1]] = L and S·[[1,1],[−1,0]] = −R, so in PSL₂(ℤ): L = ab, R = ab⁻¹, L⁻¹ = b⁻¹a, R⁻¹ = ba. Let ℓ be the syllable length of the normal form. Since R·L^(−n−1) = [[1,−n−1],[1,−n]] = −Σ, the class of Σ is ab⁻¹(b⁻¹a)^(n+1) = a·b·a·(b⁻¹a)ⁿ, of length 2n+3, and the class of S⁻¹Σ is b·a·(b⁻¹a)ⁿ, of length 2n+2.

*Step 3 (loss lemma).* For t₁,…,t_μ ∈ T concatenate the 2-syllable forms and reduce by the steps aa → ∅ (loss 2), b^e b^(−e) → ∅ (loss 2), b^e b^e → b^(−e) (loss 1). The loss 2μ − ℓ(t₁⋯t_μ) is the sum of the losses of the steps. Call L,R positive (they begin with a and end with b^{±1}) and L⁻¹,R⁻¹ negative (begin with b^{±1}, end with a). Junctions positive|positive and negative|negative are reduced; positive|negative reads b^e|b^f; negative|positive reads a|a. Hence:
- loss 0 ⇔ all tᵢ positive or all negative;
- loss 1 ⇔ exactly one step, a merge, i.e. t₁,…,t_j positive, t_(j+1),…,t_μ negative and (t_j,t_(j+1)) ∈ {(L,R⁻¹),(R,L⁻¹)};
- loss 2 is impossible: one cancellation aa → ∅ happens inside b^e a·a b^f and leaves b^e b^f adjacent; one cancellation b^e b^(−e) → ∅ happens inside a b^e·b^(−e) a and leaves aa adjacent; two merges need two positive|negative junctions, and between them lies a negative|positive junction whose aa is untouched by merges (a merged syllable is flanked by a's, so merges create no new adjacencies).

*Step 4.* In PSL₂(ℤ), t₁⋯t_μ is the class of d⁻¹Σ, of length 2n+3 (d = ±I) or 2n+2 (d = ±S). By Step 3: if d = ±S then μ = n+1 with loss 0, or μ ≥ n+3; if d = ±I then μ = n+2 with loss 1, or μ ≥ n+3. So μ ≥ n+1, with equality only for loss 0. (This is the abelian bound; it is attained in ℤ²: S·R⁻¹L⁻ⁿ = Σ.)

*Step 5 (loss 0 contradicts Theorem 2).* If all tᵢ ∈ {L,R}, then t₁⋯t_μ = |t₁|⋯|t_μ| and C₀ = |d|·t₁⋯t_μ = |d t₁⋯t_μ| = |Σ|. If all tᵢ ∈ {L⁻¹,R⁻¹}, then with J = diag(1,−1) (JLJ = L⁻¹, JRJ = R⁻¹) t₁⋯t_μ = J|t₁|⋯|t_μ|J and again C₀ = |Σ|. But |Σ| = [[1,n+1],[1,n]] has first column (1,1), contradicting c_r ≥ 3. Hence μ ≥ n+2.

*Addendum (the case μ = n+2).* Matching the loss-1 form with a·b·a·(b⁻¹a)ⁿ shows that the words with μ = n+2 are exactly R·L^(−n−1) and L R^(j−2) L·R⁻¹ L^(−(n+1−j)), 2 ≤ j ≤ n+1 (with d = ±I). Their count matrices are [[1,n+1],[1,n+2]], [[3,3n−1],[1,n]] (j = 2), and [[2j−1,(2j−1)(n−j+1)+j],[2j−3,(2j−3)(n−j+1)+j−1]] (j ≥ 3). Only j ≥ 3 is compatible with Theorem 2(ii). So for n = 1 also μ = 3 is impossible (μ ≥ 4), while for n ≥ 2 the value μ = n+2 is **not** excluded by this argument. (Steps 4–5 and the addendum are confirmed by exhaustive enumeration of all transvection words of length ≤ n+2 for n ≤ 5, §7.) ∎

### 4.2 Theorem 4: at least n−3 conjugations

Let σ: F → ℤ, σ(x) = σ(y) = 1.

**Lemma 4.1 (a permutation model; proved, and machine-checked for 4 ≤ n ≤ 60).** Let n ≥ 4 and let F act on the right on Ω = {0,1,…,n} by x = (1 2 … n)(0), y = (0 1 … n), i.e. i·x = i+1 (1 ≤ i < n), n·x = 1, 0·x = 0; i·y = i+1 (0 ≤ i < n), n·y = 0. Then (a) r acts trivially; (b) s fixes every p ∈ [1,n−3]; (c) if p and p+δ lie in [1,n] (δ = ±1) then p·h = p+δ for both letters h with σ(h) = δ.
*Proof.* (a) xⁿ = 1 = y^(n+1) on Ω. (c) by inspection. (b) for 1 ≤ p ≤ n−3, by (c), p·xyx = p+3 = p·yxy. ∎

**Theorem 4.** Let n ≥ 4. In every instruction path from AK(n) to (x,y), let κ⁺ (resp. κ⁻) be the number of conjugation instructions u_j ← h u_j h⁻¹ with σ(h) = 1 (resp. −1). Then κ = κ⁺ + κ⁻ ≥ n−3.

*Proof.* Take the expression of x over AK(n) given by Corollary 1.1. By Theorem 1 every conjugator is a product h_(k₁)⋯h_(k_q) over *distinct* conjugation instructions, and so is each of its prefixes g'; hence σ(g') ∈ [−κ⁻, κ⁺]. Suppose κ⁺+κ⁻ ≤ n−4 and put v = κ⁻+1 ∈ [1,n−3]. A factor g r^ε g⁻¹ fixes v by Lemma 4.1(a). For a factor g s^ε g⁻¹: every prefix g' satisfies v+σ(g') ∈ [1, κ⁻+κ⁺+1] ⊆ [1,n−3]; by induction on |g'| and Lemma 4.1(c), v·g' = v+σ(g'); so v·g ∈ [1,n−3] is fixed by s (Lemma 4.1(b)), and g s^ε g⁻¹ fixes v. Thus the product x fixes v; but v·x = v+1. Contradiction. ∎

Remarks. (a) The mechanism: the n+1 (at least) s-factors must carry conjugators whose σ-values do not fit into any window of n−3 consecutive integers; in (I_x) they are Δ⁻¹yⁱ, 0 ≤ i ≤ n, so the bound is sharp up to an additive constant *for this invariant*. (b) The r-factors carry no such information: in (I_x) their conjugators have length ≤ 3 for all n. (c) Theorem 4 bounds the radius too: every expression of x over AK(n), whether or not it comes from a path, has an s-conjugator g with a prefix g' of |σ(g')| ≥ ⌊(n−2)/2⌋, so its radius is ≥ ⌊(n−2)/2⌋ (take v = ⌈(n−2)/2⌉ in the proof), in contrast with (b). *Experiment (exact, Stallings folding, §7):* the least radius ρ*(n) of an expression of x over AK(n) (equivalently: the least ρ with x ∈ ⟨g r g⁻¹, g s g⁻¹ : |g| ≤ ρ⟩) is ⌊n/2⌋+1 for every n ≤ 12, and the same for y. So the theorem's radius bound is 2 below the truth in that range; κ ≥ ρ*(n) by Theorem 1. *Open:* prove ρ*(n) = ⌊n/2⌋+1 for all n.

### 4.3 Corollary 5 and comparison with E

**Corollary 5.** For n ≥ 4, d_F(AK(n)) ≥ μ + κ ≥ (n+2) + (n−3) = 2n−1. For 1 ≤ n ≤ 3, d_F(AK(n)) ≥ (n+2) + 1 (and ≥ 5 for n = 1), because κ ≥ 1: a path without conjugations is a chain of Nielsen moves, which would make (r,s) a basis of F and F/⟨⟨s⟩⟩ = B₃ cyclic. The same bounds hold for the number of moves of any `ordinary-ac-elementary-v1` certificate (each primitive is one instruction, E Fact 0).

| n | 1 | 2 | 3 | 4 | 5 | 9 | 10 | 20 | general n ≥ 4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| this note (theorem) | 5 | 5 | 6 | 7 | 9 | 17 | 19 | 39 | 2n−1 |
| theorem + exact radius ρ* (experiment, n ≤ 12) | 5 | 6 | 7 | 9 | 10 | 17 | 19 | — | μ ≥ n+2, κ ≥ max(n−3, ρ*) |
| E (exhaustive BFS) | 8 (exact) | ≥ 15 | ≥ 15 | — | — | — | — | — | — |
| known upper bound | 8 | 19 (E: 19 instructions = 28 elementary-v1 moves) | none | none | none | none | none | none | none (open) |

So for n = 3 the theorem is far weaker than E's exhaustive bound 15, and it overtakes that bound only for n ≥ 9 — where no exhaustive search exists. The calibration cases agree: E's 12-move AK(1) certificate has μ = 5, κ = 3 and count matrix [[7,2],[3,1]]; E's 28-move AK(2) certificate has μ = 10, κ = 10, count matrix [[67,49],[41,30]], radius 6 (§7).

**What the bound is not.** Corollary 5 holds for AK(1) and AK(2), which are AC-trivial. It is a statement about the length of trivializations, not evidence for or against their existence (K2 applies verbatim: μ and κ are not monotone along anything).

### 4.4 General forms (proved here; same proofs)

Nothing in §4.1–4.2 is special to AK(n) except the inputs. For reuse by other families:

**Proposition 6 (abelian word bound).** Let U be a balanced presentation of the trivial group on x,y and Σ = E_U⁻¹. For d ∈ W with det d = det Σ let ℓ_d be the syllable length of the class of d⁻¹Σ in PSL₂(ℤ) = ⟨a⟩ * ⟨b⟩, and ℓ* = min_d ℓ_d. Then every instruction path from U to (x,y) has μ ≥ ⌈ℓ*/2⌉; if μ = ℓ_d/2 for the d of the path (loss 0), its count matrix is exactly |Σ|, i.e. in its expressions of x and y all factors on the same relator carry the same sign; and 2μ − ℓ_d ≠ 2 always.

**Proposition 7 (window lemma).** Let U = (u₀,u₁), let π: F → ℤ be a homomorphism with π(x), π(y) ∈ {−1,0,1}, and let F act on a set Ω containing distinct points p₁,…,p_N such that: (i) u₀ acts trivially on Ω; (ii) u₁ fixes p₁,…,p_N; (iii) p_i·h = p_(i+π(h)) for every letter h and every i with 1 ≤ i, i+π(h) ≤ N; (iv) x or y fixes no p_i. Then every instruction path from U to (x,y) contains at least N conjugation instructions by letters h with π(h) ≠ 0, and every expression of that generator over U has a u₁-conjugator with a prefix g' of |π(g')| ≥ ⌊(N+1)/2⌋.

(Theorem 4 is the case π = σ, N = n−3, p_i = i.) The roles of u₀ and u₁ may be exchanged.

### 4.5 ACM analogue (proved here)

Split every ACM move of insertion number k (Remark (c) of §2) into its k signed transvections. Steps 1–5 of Theorem 3 use only Σ = d·t₁⋯t_μ, C₀ = |d||t₁|⋯|t_μ| and Theorem 2(ii); hence: **every sequence of ACM moves (with arbitrary conjugators) from AK(n) to (x,y) inserts in total at least n+2 conjugates of the frozen relators.** Theorem 4 has no ACM analogue in terms of the number of ACM moves, since one ACM move may conjugate by an arbitrary word; it bounds instead the total σ-variation of the conjugators used.

## 5. K's coordinates P_n = (c, k_n), c = xyxYYXy, k_n = xⁿYXyy

*Proved here.* E_{P_n} = [[1,0],[n−1,1]] (rows c, k_n), so by Lemma 0 the signed counts are (1,0) for x and (−(n−1),1) for y: Area_{P_n}(y) ≥ n, and Area_{P_n}(x) ≥ 3 (c_c is odd, c_k even, and (1,0) is impossible because x is not conjugate in F to the cyclically reduced word c^{±1} of length 7). Σ = R^(−(n−1)) has class (ba)^(n−1) of length 2n−2, and S⁻¹Σ has length 2n−1. By Steps 3–5 of Theorem 3: μ = n−1 would force loss 0 and C₀ = |Σ|, i.e. count vector (1,0) for x, which is impossible; so **every instruction path from P_n to (x,y) has μ ≥ n multiplications.**

*Experiment (verified upper bounds, n = 3).* Composing (I_x), (I_y) with the expressions of r, s over P₃ obtained by reversing K's 68-move certificate gives explicit expressions, checked by free reduction, with count vectors (211, 382) for x and (174, 315) for y; K's 88-move uniform certificate gives (975,1568) and (804,1293). So 3 ≤ Area_{P₃}(x) ≤ 593 and 3 ≤ Area_{P₃}(y) ≤ 489. *Open:* the exact areas over P_n (I expect them to be linear in n; transport along a path is far from optimal because the count matrices multiply), and an analogue of Theorem 4 for P_n (I found no model with a long window: in the obvious metabelian quotient ℤ² ⋊ ℤ of ⟨x,y | c⟩ the affine map induced by k_n has a single fixed point — sketch, not checked).

## 6. Failed attempts and negative results (with precise reasons)

1. **The seed's target "A(AK(n)) ≥ g(n) with g large" is false** (Theorem 2: A = n+4). All routes to a large area fail for the same reason, and each failure is now a corollary: permutation/Hamming, rank and bi-invariant-metric estimates (Corollary 2.1(b)); and quasimorphism or scl estimates for the number c_r of r-conjugates in B₃, which could at best prove c_r ≥ 3 — which is the truth.
2. **Conjugator length of the r-factors:** bounded by 3 for all n ((I_x)); only the s-factors are forced to spread (Theorem 4).
3. **Excluding μ = n+2 for n ≥ 2.** The n−1 words L R^(j−2) L R⁻¹ L^(−(n+1−j)), j ≥ 3, have count matrices compatible with Theorem 2(ii). Excluding them needs to know which non-minimal count vectors are realized by expressions, which I could not determine.
4. **A superlinear bound.** Both mechanisms are saturated at linear size by the identities themselves: (I_x) has n+4 factors and σ-spread n. The actual difficulty of trivializing AK(n) (if any) is invisible to count matrices and conjugator windows; I see no way to push these two invariants beyond c·n.
5. **P_n:** no window model, exact area open (§5).

## 7. Experiments (exact commands and outputs)

    $ PYTHONDONTWRITEBYTECODE=1 python3 experiments/th12_area.py --selftest      # < 5 s, < 50 MB
    identities x,y over AK(n) verified for n = 1..40
    permutation model verified for n = 4..60
    SL2(Z) word classification (n: #words mu=n+1, #words mu=n+2, #admissible): {1: (1, 2, 0), 2: (1, 3, 1), 3: (1, 4, 2), 4: (1, 5, 3), 5: (1, 6, 4)}
    Fibonacci bounds verified for mu <= 14
    e_ak1_trivialization.json {... "moves": 12, "mu": 5, "kappa": 3, "x": {"count": [7, 2], "signed": [-1, 2], "radius": 1}, "y": {"count": [3, 1], "signed": [-1, 1], "radius": 1}}
    e_ak2_peak13_trivialization.json {... "moves": 28, "mu": 10, "kappa": 10, "x": {"count": [67, 49], "signed": [-1, 3], "radius": 6}, "y": {"count": [41, 30], "signed": [-1, 2], "radius": 6}}
    P_3 transport via k_ak3_to_p3.json {... [[21, 38], [37, 67]], "x": [211, 382], "y": [174, 315]}
    P_3 transport via k_ak3_to_p3_uniform.json {... [[171, 275], [97, 156]], "x": [975, 1568], "y": [804, 1293]}
    random reversed paths through bookkeeping (trials, (max mu, its x-area)): (200, (13, 367))
    TH12 selftest OK

    $ PYTHONDONTWRITEBYTECODE=1 python3 experiments/th12_radius.py --selftest 12 8     # about 3 s, < 100 MB
    th12_radius selftest OK
    n=1  rho*(x)=1  rho*(y)=1  theorem: >= 0
    n=2  rho*(x)=2  rho*(y)=2  theorem: >= 0
    n=3  rho*(x)=2  rho*(y)=2  theorem: >= 0
    n=4  rho*(x)=3  rho*(y)=3  theorem: >= 1
    n=5  rho*(x)=3  rho*(y)=3  theorem: >= 1
    n=6  rho*(x)=4  rho*(y)=4  theorem: >= 2
    n=7  rho*(x)=4  rho*(y)=4  theorem: >= 2
    n=8  rho*(x)=5  rho*(y)=5  theorem: >= 3
    n=9  rho*(x)=5  rho*(y)=5  theorem: >= 3
    n=10  rho*(x)=6  rho*(y)=6  theorem: >= 4
    n=11  rho*(x)=6  rho*(y)=6  theorem: >= 4
    n=12  rho*(x)=7  rho*(y)=7  theorem: >= 5

What each line checks: (1) the factor lists of (I_x), (I_y) multiply to x, y by free reduction, with counts (3,n+1), (3,n) and r-conjugators of length ≤ 3; (2) Lemma 4.1 (and Fix(s) = [1,n−3] exactly); (3) for n ≤ 5, exhaustively over all words in L^{±1},R^{±1} of length ≤ n+2 and d ∈ {±I,±S}: the shortest have length n+1 (one word, count matrix |Σ|), those of length n+2 are the n+1 words of the Addendum, of which exactly the n−1 with j ≥ 3 satisfy Theorem 2(ii); (4) sharpness of the Fibonacci bounds; (5) Theorem 1 made executable: the script walks E's certificates backwards, builds the expressions of x and y over AK(1), AK(2), verifies them by free reduction and checks signed counts = E⁻¹, counts ≤ Fibonacci, radius ≤ κ; (6) §5; (7) Theorem 1 again on 200 random instruction paths of length 30 from (x,y), reversed into trivializations (all asserts of (5) pass). The second script decides membership of x, y in H_ρ = ⟨g r g⁻¹, g s g⁻¹ : |g| ≤ ρ⟩ exactly by Stallings folding (ball of radius ρ with a loop r and a loop s at every vertex, folded; x ∈ H_ρ iff x reads a loop at the base vertex); `theorem: >=` is the bound ⌊(n−2)/2⌋ of §4.2(c). `python3 experiments/th12_area.py --cert FILE` runs (5) on any elementary-v1 certificate ending at (x,y). No new AC-equivalence is claimed, so no certificate is written.

## 8. Honest limits

- Everything here is a complexity statement. μ ≥ n+2, κ ≥ n−3 and d_F ≥ 2n−1 hold equally for the AC-trivial AK(1), AK(2) and say nothing about whether AK(n), n ≥ 3, is AC-trivial. For n = 3 the theorem (6 moves) is much weaker than E's exhaustive 15.
- The bounds count instructions of E's alphabet (equivalently elementary-v1 primitives). They do not bound peak length, and they are not invariant under changing the generating set of moves beyond what §4.4 states.
- Theorem 3 relies on the classical free product decomposition PSL₂(ℤ) ≅ ℤ/2 * ℤ/3 (recalled), with the specific generators verified by matrix multiplication; its conclusion is also checked by brute force for n ≤ 5.
- Bridson's and Lishak's results are cited from memory only; I did not have access to the papers. No novelty is claimed for anything here: count matrices are the obvious bookkeeping, and Theorems 2–4 are elementary.
- §5's upper bounds for P₃ are crude; the exact areas over P_n are open.

## 9. Advice to the coordinator (ranked)

1. **Record Theorem 2 as closing the "area / Dehn function / stability" line for the AK family**: A(AK(n)) = n+4 exactly, r-conjugators of length ≤ 3. Nobody should look for large fillings, quasimorphism bounds or approximate-representation bounds on AK(n) again. A Bridson–Lishak-type argument needs relators that encode a group with large Dehn function; AK(n) has none.
2. **Use Corollary 5 as the general-n complement of E's table** (d_F(AK(n)) ≥ 2n−1, with ≥ n+2 multiplications and ≥ n−3 conjugations), clearly labelled as complexity, not obstruction. If a referee wants it stronger, the natural targets are Theorem 3's Addendum (decide μ = n+2 for n ≥ 2).
3. **The executable bookkeeping (`--cert`) is a cheap diagnostic for search agents**: for any found trivialization it returns the count matrix and radius; a search for AK(3) could be pruned or guided by the necessary conditions "count matrix ≥ [[3,4],[3,3]], Σ = [[−1,4],[−1,3]]" — e.g. meet-in-the-middle over abelian words of length μ first, since Theorem 3 lists exactly which abelian words of minimal length can occur.
4. **Open, small, well-posed:** exact generator area of P_n (and whether Theorem 4 has a P_n-analogue); whether μ = n+2 is realizable for AK(2) (its known certificate has μ = 10).
5. Do not invest in superlinear versions of these two invariants (§6.4).

## References

- Repository notes B (§1, §4), E (§2–5), K (§3, §6); certificates `e_ak1_trivialization.json`, `e_ak2_peak13_trivialization.json`, `k_ak3_to_p3*.json`.
- M. R. Bridson, *The complexity of balanced presentations and the Andrews–Curtis conjecture*, arXiv:1504.04187 (recalled from memory; not accessed).
- B. Lishak, *Balanced finite presentations of the trivial group*, arXiv:1504.00418; J. Topol. Anal. 9 (2017) (recalled from memory; not accessed).
- J.-P. Serre, *Trees* (PSL₂(ℤ) ≅ ℤ/2 * ℤ/3; recalled).
- Files written: `research/research-th12.md`, `experiments/th12_area.py`, `experiments/th12_radius.py` (both with `--selftest`).
