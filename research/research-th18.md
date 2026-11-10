# Research TH18: killers of BS(n,n+1) and the t-length filtration of the Miller–Schupp family

Date: 2026-11-09 (Los Angeles). Independent research agent TH18 (round 5, theory round).

**Status.** Partial results with complete proofs and replayed certificates. **No AC trivialization of AK(3), no proof that AK(3) is not AC-trivial, no counterexample.** Everything concerns ordinary (unstable) AC equivalence. An "ACM move" replaces one relator by a word conjugate to it or its inverse modulo the other relator; it is an explicit composite of ordinary AC moves (Lemma G0 of note G), and every ACM move used for a certificate below is compiled to strict elementary moves and replayed.

Notation: X = x⁻¹, Y = y⁻¹; G_n = BS(n,n+1) = ⟨x,y | r_n⟩, r_n = x⁻¹yⁿxy⁻⁽ⁿ⁺¹⁾, an HNN extension of ⟨y⟩ ≅ ℤ with stable letter x; σ(w) = x-exponent sum; MS(n,w) = (r_n, w). ℓ(w) = number of x-letters of a cyclically (Britton-)reduced conjugate of w in G_n (the *t-length*; a conjugacy invariant by Collins' lemma). ι is the automorphism y ↦ y⁻¹ ("mirror"); ι(r_n) is a conjugate of r_n⁻¹.

**Central claims.**

| # | statement | label |
|---|---|---|
| T1 | The killers (normal generators) of G_n are exactly the elements with σ = ±1 | classical (Miller–Schupp 1999); proof included |
| T2 | Complete conjugacy invariant with **unbounded** conjugators: cyclically reduced x^{d₁}y^{a₁}⋯x^{d_ℓ}y^{a_ℓ} and x^{d′₁}y^{a′₁}⋯ are conjugate iff, after a cyclic shift, d = d′ and a − a′ ∈ Λ_d, an explicit lattice of index (n(n+1))^{(ℓ−1)/2} when σ = ±1. So for each ℓ there are finitely many killer classes; their number is Σ_d (n(n+1))^{N−m(d)}(n(n−1))^{m(d)} (ℓ = 2N+1; d runs over sign necklaces, m(d) = number of +-blocks): n(n−1) for ℓ = 3, 2n³(n−1) for ℓ = 5 | proved here (Britton + Collins) |
| T3 | For σ(w) = ±1: the class of w contains a primitive element of F₂ ⇔ w ~ x^{±1} ⇔ ℓ(w) = 1. Hence MS(n,w) is AC-trivial whenever ℓ(w) = 1 (one ACM move + Lemma D3); every MS(1,w) is of this kind | proved here |
| T4 | ℓ = 3 (n ≥ 2): the n(n−1) classes with σ = +1 are C_b = [x²y^bx⁻¹y^{−b}], b ∈ ℤ/n(n+1), n ∤ b, (n+1) ∤ b; x y^a x y^{b′} X y^{c′} ∈ C_b iff b ≡ b′ (mod n+1) and b ≡ −c′ (mod n); ι(C_b) = C_{−b} | proved here |
| T5 | C's bridge word XYx²Y (the AK(n) partner) lies in C_{2n+1}, so ℓ = 3: **for every n ≥ 2, including n = 2, no primitive element is conjugate to it in G_n**, and no single ACM move from M_n = MS(n, XYx²Y) reaches a primitive relator | proved here (uses G2(b)) |
| T6 | Divisor classes: if b | n or b | n+1, every MS(n,w) with w ∈ C_b^{±1} is AC-trivial by two ACM moves and D3, because in ⟨x,y | y^bxy^{−b} = x²⟩ the relator r_n is conjugate to the primitive y⁻¹x^{±(2^m−1)}. Sharp for these representatives: r_n is conjugate to a primitive in ⟨x,y | y^bxy^{−b} = x²⟩ iff b | n or b | n+1 | proved here; certificates |
| T7 | n = 2: the bridge class C_5 = C_{−1} **is** a divisor class (the Johnson class), so every MS(2,w) with ℓ(w) ≤ 3 is AC-trivial. n = 3: the six ℓ = 3 classes are C_{±1}, C_{±2} (AC-trivial) and C_{±5} (bridge, mirror), so **every MS(3,w) with ℓ(w) ≤ 3 is AC-trivial or AC-equivalent to AK(3)**. For n ≥ 3 the bridge class is never a divisor class | proved here (with C's and D's certificates) |
| E1 | D's 34 certified MS(3,w) members of AK(3)'s class lie in exactly **two** BS(3,4)-classes, C_{−5} (17) and its mirror C_5 (17), and these are all benchmark presentations in those classes: all 34 are one r-frozen ACM move from C's bridge presentation or from MS(3, yx²y) | exact computation |
| E2 | Of the 1190 benchmark presentations, 330 have ℓ = 1 and 244 lie in divisor classes: for all 574 a certificate was generated from the proofs and replayed by the strict verifier (67 of them are not in Shehper et al.'s greedy-solved list). All 212 with ℓ = 5 are unsolved there | exact computation + certificates |
| E3 | Holdout P2's class contains the ℓ = 3 classes C_{±3} of BS(4,5) and C_{±14} of BS(5,6) (D's certificates + T2). For n = 4 the ℓ = 3 classes are: C_{±1}, C_{±2} trivial (T6), C_{±6} trivial (L's certificates + T2), C_{±3} ~ P2, C_{±9} ~ AK(4) or its mirror, C_{±7} open | exact computation on certified endpoints |

## 1. Previous work read and choice of direction

Read: `README.md` in full; status paragraphs and coordinator reviews of notes A–O; in full C, G §2–6, D §3 and §4.3–4.5, F §3 (Prop. F2); skimmed L §3.5, K, O; read `experiments/g_bs.py` and `elementary_verify.py`. What I use: Lemma G0 (ACM moves are AC composites), Lemma D2 (AC-triviality is Aut(F₂)-invariant), Lemma D3 (a primitive relator gives AC-triviality), C's theorem M_n ~AC AK(n) (`certificates/ms3_to_ak3_exact.json` for n = 3), D's certificates `d_ak3_to_ms*.json`, `d_ms2[ab]_to_ms*.json`, L's `l_ms*_trivialization.json`, Proposition G2(b).

Direction: the seed. G's `g_bs.py` searched for conjugators yˢ in a window |s| ≤ 30–60, so its negatives were bounded; G asked for "the full theory of BS-frozen moves". The observation that makes this exact is that for x-exponent sum σ ≠ 0 the conjugator is *unique* (it is the solution of a rational fixed-point equation), and the classes are cosets of a lattice. This turns the Miller–Schupp family into finitely many classes per t-length and gives uniform trivialization theorems, which no earlier note has. Two corrections to the seed's expectations: (i) every element with σ = ±1 is a killer (T1), so there is nothing to characterize beyond σ; (ii) the bridge class contains no primitive element **for n = 2 either** (T5) — the difference between n = 2 and n ≥ 3 is instead the arithmetic coincidence of T7. TH09 covers n = 1 and the trefoil; I use n = 1 only through the one-line remark after T3.

## 2. Results with proofs

### 2.0 Classical facts used (externally reported, quoted)

- **Britton's lemma** (Lyndon–Schupp, *Combinatorial Group Theory*, IV.2.1): in an HNN extension ⟨B, t | t⁻¹at = φ(a), a ∈ A⟩, a word g₀t^{ε₁}g₁⋯t^{ε_k}g_k (k ≥ 1) that equals 1 contains a *pinch* t⁻¹gt with g ∈ A or tgt⁻¹ with g ∈ φ(A); and the base B embeds. In G_n (t = x, A = ⟨yⁿ⟩, φ(A) = ⟨yⁿ⁺¹⟩): x⁻¹y^cx is a pinch iff n | c, and xy^cx⁻¹ is a pinch iff (n+1) | c. Write p(+1) = n, q(+1) = n+1, p(−1) = n+1, q(−1) = n; then **y^{p(d)}x^d = x^dy^{q(d)}** in G_n, and x^{−d}y^cx^d is a pinch iff p(d) | c.
- **Collins' lemma** (Lyndon–Schupp IV.2.5): every element is conjugate to a cyclically reduced one (all cyclic permutations of its sequence are pinch-free); if u, v are conjugate, cyclically reduced, and u has k ≥ 1 stable letters, then v has k stable letters and u is obtained from v by a cyclic permutation followed by conjugation by an element of an associated subgroup (so, here, by a power of y).
- **Primitive classes of F₂** (Nielsen; Osborne–Zieschang 1981): two primitive elements with the same image in ℤ² are conjugate in F₂. In particular a primitive element with x-exponent ±1 and y-exponent k is conjugate in F₂ to x^{±1}y^k.
- **Conjugacy in amalgams** (Magnus–Karrass–Solitar, Thm 4.6): in A *_C B, a cyclically reduced element of length ≥ 2 is conjugate only to cyclically reduced elements of the same length.

### 2.1 Theorem T1 (killers; Miller–Schupp)

*For n ≥ 1 and w ∈ F₂: ⟨⟨w⟩⟩ = G_n iff σ(w) = ±1.*

*Proof.* G_n^{ab} ≅ ℤ, generated by x (the relation gives nȳ = (n+1)ȳ), so σ(w) = ±1 is necessary. Conversely let σ(w) = 1 (invert otherwise) and Q = G_n/⟨⟨w⟩⟩. Write w = xv⁻¹ with σ(v) = 0, so x = v in Q, and v is a product of elements y_k^{±1}, y_k = x^{−k}yx^k, a ≤ k ≤ a+m, with m ≥ 1. In G_n, y_{k+1}ⁿ = y_k^{n+1}. Hence u = y_a^{(n+1)^m} equals y_{a+j}^{n^j(n+1)^{m−j}} for 0 ≤ j ≤ m, so u commutes with every y_k in the range, hence with v, hence with x in Q. Then u = x⁻¹ux = y_{a+1}^{(n+1)^m}, while u = y_{a+1}^{n(n+1)^{m−1}}; so y_{a+1}^{(n+1)^{m−1}} = 1 in Q and y has finite order e dividing (n+1)^{m−1}. Since yⁿ and yⁿ⁺¹ are conjugate, they have equal orders: e = e/gcd(e, n+1), so gcd(e, n+1) = 1 and e = 1. Thus y = 1, v = 1, x = 1 in Q. ∎

So the states (r_n, w′) reachable from MS(n,w) by r_n-frozen ACM moves are exactly the words w′ in the G_n-conjugacy class of w^{±1}, and the Miller–Schupp presentations MS(n,·), up to such moves, are the conjugacy classes of G_n in σ⁻¹(±1) modulo inversion.

### 2.2 Theorem T2 (exact conjugacy; the class lattices)

For d ∈ {±1}^ℓ, a ∈ ℤ^ℓ (ℓ ≥ 1) put U_d(a) = x^{d₁}y^{a₁}x^{d₂}y^{a₂}⋯x^{d_ℓ}y^{a_ℓ}, p_i = p(d_i), q_i = q(d_i), and let Λ_d ⊂ ℤ^ℓ be spanned by v_i = q_ie_i − p_ie_{i−1} (indices mod ℓ; v₁ = ±e₁ if ℓ = 1).

**(a)** U_d(a) is cyclically reduced iff for every i (mod ℓ) with d_{i+1} = −d_i: p_{i+1} ∤ a_i. This depends only on a mod Λ_d.
**(b)** Cyclically reduced U_d(a) and U_{d′}(a′) are conjugate in G_n iff ℓ = ℓ′ and for some cyclic shift τ: τd′ = d and τa′ − a ∈ Λ_d.
**(c)** [ℤ^ℓ : Λ_d] = |∏q_i − ∏p_i|; for σ = ±1 this is (n(n+1))^{(ℓ−1)/2}, and the necklace of d has no rotational symmetry.
**(d)** For σ = +1, ℓ = 2N+1, the number of conjugacy classes with sign necklace d is (n(n+1))^{N−m}(n(n−1))^m, m = number of maximal cyclic blocks of + signs. Every element with σ ≠ 0 is conjugate to some cyclically reduced U_d(a).

*Proof.* (a) The only possible pinches are x^{d_i}y^{a_i}x^{d_{i+1}} with d_{i+1} = −d_i, and this is a pinch iff p_{i+1} | a_i. When d_{i+1} = −d_i we have q_i = p_{i+1}, and a_i is changed only by v_i (by q_i) and v_{i+1} (by −p_{i+1}); so a_i mod p_{i+1} is constant on cosets.

(b) (⇐) For 2 ≤ i ≤ ℓ, U_d(a + v_i) = U_d(a) in G_n, since y^{a_{i−1}}x^{d_i}y^{a_i} = y^{a_{i−1}−p_i}x^{d_i}y^{a_i+q_i}; and U_d(a + v₁) = y^{p₁}U_d(a)y^{−p₁}. A cyclic shift of syllables is a conjugation.
(⇒) By Collins' lemma ℓ = ℓ′ and, after a shift (write d″ = τd′, a″ = τa′), U_d(a) = y^{−s}U_{d″}(a″)y^s for some s ∈ ℤ. So

 y^{−a_ℓ}x^{−d_ℓ}⋯y^{−a₁}x^{−d₁} · y^{−s} · x^{d″₁}y^{a″₁}⋯x^{d″_ℓ}y^{a″_ℓ+s} = 1.

Both halves are pinch-free, so by Britton's lemma the junction x^{−d₁}y^{−s}x^{d″₁} is a pinch: d″₁ = d₁ and s = k₁p₁; it equals y^{−k₁q₁}. The new word is again 1 with pinch-free halves, so the new junction x^{−d₂}y^{−(a₁+k₁q₁−a″₁)}x^{d″₂} is a pinch: d″₂ = d₂ and a″₁ − a₁ = k₁q₁ − k₂p₂ for an integer k₂. Inductively d″ = d and a″_i − a_i = k_iq_i − k_{i+1}p_{i+1} for i < ℓ; the last step leaves y^{−a_ℓ−k_ℓq_ℓ+a″_ℓ+s} = 1 in ⟨y⟩ ≅ ℤ, i.e. a″_ℓ − a_ℓ = k_ℓq_ℓ − k₁p₁. Hence a″ − a = Σk_iv_i ∈ Λ_d.

(c) The matrix with rows v_i has diagonal q_i and one further cyclic band −p_i; only the identity and the ℓ-cycle contribute to its determinant, giving ∏q_i − ∏p_i = (n+1)^Pn^N − n^P(n+1)^N for P plus and N minus signs. If a rotation of order k fixed d, k would divide σ.

(d) The last assertion is Collins' lemma (σ ≠ 0 excludes the base) plus a conjugation by a power of y. Let S be the set of sign-change positions i (d_{i+1} = −d_i); |S| = 2m. By (a), φ: ℤ^ℓ/Λ_d → ∏_{i∈S} ℤ/p_{i+1}, a ↦ (a_i mod p_{i+1}), is a well-defined homomorphism; it is onto, its target has order (n(n+1))^m, and the cyclically reduced cosets are the preimage of the n^m(n−1)^m tuples without zero entry. By (b), (c) distinct such cosets are distinct classes. ∎

**Corollary (exact decision, unique conjugator).** For σ ≠ 0 the system a″ − a = Σk_iv_i has a unique rational solution (the recursion k_{i+1} = (k_iq_i − δ_i)/p_{i+1} closes up to the fixed-point equation k₁ = αk₁ + β with α = ∏q_i/∏p_i ≠ 1); the elements are conjugate iff it is integral for some shift. `experiments/th18_bs.py` implements this (`cls`, `solve`, `bs_path`); it replaces the bounded window of `g_bs.conjugate`. Geometrically, k₁p₁ = s is forced because in the affine quotient y ↦ (t ↦ t+1), x ↦ (t ↦ nt/(n+1)) an element with σ ≠ 0 has a unique fixed point.

### 2.3 Theorem T3 (the primitive class)

*Let σ(w) = ±1. Some primitive element of F₂ is conjugate to w in G_n ⇔ w ~ x^{±1} in G_n ⇔ ℓ(w) = 1.*

*Proof.* If ℓ(w) = 1, w ~ x^{±1}y^a, and Λ_{(±)} = ℤ, so w ~ x^{±1} (explicitly xy^a = y^{na}xy^{−na}). If a primitive p is conjugate to w in G_n, then σ(p) = ±1, so p is conjugate in F₂ to x^{±1}y^k (§2.0), which has one stable letter; by Collins' lemma ℓ(w) = 1. ∎

**Corollary T3.1.** If ℓ(w) = 1 then MS(n,w) is AC-trivial: one r_n-frozen ACM move gives (r_n, x^{±1}), then delete the x-letters of r_n (Lemma D3). **Remark (n = 1).** In G₁ every x⁻¹y^cx is a pinch, so a cyclically reduced form has no sign change −+ and therefore none at all: ℓ(w) = |σ(w)|. Thus all killers of BS(1,2) are conjugate to x^{±1} and every MS(1,w) is AC-trivial by one ACM move. (This case belongs to TH09's seed; it is needed in §2.6 only for this one line.)

### 2.4 Theorem T4 (t-length 3)

*Let n ≥ 2. The classes with σ = +1, ℓ = 3 are exactly the n(n−1) classes C_b of w_b = x²y^bx⁻¹y^{−b}, b ∈ ℤ/n(n+1) with n ∤ b and (n+1) ∤ b. The word xy^axy^{b′}x⁻¹y^{c′} has ℓ = 3 iff (n+1) ∤ b′ and n ∤ c′ (otherwise ℓ = 1), and then it lies in C_b for the unique b with b ≡ b′ (mod n+1), b ≡ −c′ (mod n). Moreover ι(C_b) = C_{−b}.*

*Proof.* The only necklace is d = (+,+,−), with v₁ = (n+1)e₁ − ne₃, v₂ = (n+1)e₂ − ne₁, v₃ = ne₃ − (n+1)e₂. The map ℤ³ → ℤ/(n+1) × ℤ/n, a ↦ (a₂, a₃), kills Λ_d and is onto a group of order n(n+1) = [ℤ³ : Λ_d]; so it is the quotient map, a₁ is irrelevant, and by T2(a) the reduced cosets are those with both coordinates non-zero. By the Chinese remainder theorem (β,γ) = (b mod n+1, −b mod n) is a bijection ℤ/n(n+1) → ℤ/(n+1) × ℤ/n, and w_b = U_d(0,b,−b). ι(w_b) = w_{−b}, and ι induces an automorphism of G_n. ∎

*Remark (the automorphisms x ↦ xy^k are inner on G_n).* x ↦ xy^k, y ↦ y fixes r_n up to conjugacy and induces conjugation by y^{nk} on G_n, because y^{nk}xy^{−nk} = xy^k. So w(xy^k, y) ~ w(x,y) in G_n for every word w, and MS(n, w(xy^k,y)) ~AC MS(n,w): on every Miller–Schupp presentation this infinite cyclic subgroup of Aut(F₂) is AC-realized by one ACM move. (This is why a₁ is irrelevant.)

### 2.5 Theorem T5 (the AK(n) partner in BS coordinates)

*For n ≥ 2 the bridge word β_n = x⁻¹y⁻¹x²y⁻¹ of note C (M_n = MS(n,β_n) ~AC AK(n)) lies in C_{2n+1} and has ℓ = 3. Hence no primitive element of F₂ is conjugate to β_n^{±1} in G_n — for every n ≥ 2, including n = 2. Moreover no primitive element is conjugate to r_n^{±1} in ⟨x,y | β_n⟩. So no single ACM move from M_n (with arbitrary conjugators, and up to Aut(F₂)) produces a presentation with a primitive relator.*

*Proof.* β_n is a cyclic conjugate of U_{(+,+,−)}(0,−1,−1); for n ≥ 2, (n+1) ∤ −1 and n ∤ −1, so ℓ = 3 and by T4 b ≡ −1 (mod n+1), b ≡ 1 (mod n), i.e. b = 2n+1. T3 gives the first claim. For the second let ψ = (x ↦ xy, y ↦ y). Then ψ(β_n) = YXYxyx, a rotation of the braid relator xyxYXY, and ψ(r_n) = YXyⁿxYⁿ. In ⟨x,y | xyx = yxy⟩ we have Xyx = yxY (multiply xyx = yxy by X on the left and by Y on the right), so Xyⁿx = (Xyx)ⁿ = yxⁿY and ψ(r_n) = Y·yxⁿY·Yⁿ = xⁿY^{n+1}. A primitive conjugate to r_n^{±1} modulo β_n would be carried by ψ to a primitive conjugate to (xⁿy^{−(n+1)})^{±1} modulo the braid relator, contradicting Proposition G2(b) (n ≥ 2). Neither relator of M_n is primitive (their groups are not ℤ). ∎

(The same computation shows ψ(M_n) is one braid-frozen ACM move from AK(n) — a one-line version of C's theorem up to the automorphism ψ; C's table proves it without ψ.) For n = 2 this corrects the seed's expectation: M₂ is AC-trivial, but not through a primitive in the class of β₂; the mechanism is T6/T7.

### 2.6 Theorem T6 (divisor classes are AC-trivial)

*Let n ≥ 2 and let b ≠ 0 divide n or n+1, with n ∤ b and (n+1) ∤ b (i.e. |b| < n, resp. |b| < n+1). Then in H_b = ⟨x,y | w_b⟩ = ⟨x,y | y^bxy^{−b} = x²⟩ the element r_n is conjugate to a primitive element of F₂. Consequently MS(n,w) is AC-trivial for every w ∈ C_b^{±1}: invert w if σ(w) = −1; one r_n-frozen ACM move w → w_b (T4); one w_b-frozen ACM move r_n → primitive; Lemma D3.*

*Proof.* w_b = 1 says sxs⁻¹ = x² with s = y^b; hence s^mx^e = x^{e2^m}s^m and x^es^{−m} = s^{−m}x^{e2^m} for m ≥ 0. Let b > 0. If n = bm: r_n = x⁻¹s^mx·y^{−(n+1)} = x^{2^m−1}s^my^{−(n+1)} = x^{2^m−1}y⁻¹. If n+1 = bm: xr_nx⁻¹ = yⁿ·xs^{−m}·x⁻¹ = yⁿs^{−m}x^{2^m−1} = y⁻¹x^{2^m−1}. Both are primitive. For b < 0 apply ι: ι(w_b) = w_{−b} and ι(r_n) is conjugate to r_n⁻¹, so r_n is conjugate in H_b to the inverse of the ι-image of the primitive found for −b. ∎

The case b = ∓1 is Johnson's presentation P(n,1) = ⟨x,y | x⁻¹yⁿx = yⁿ⁺¹, y⁻¹xy = x²⟩ and its mirror: w_{−1} = x²y⁻¹x⁻¹y, H_{−1} = BS(1,2) with stable letter y, in agreement with the remark after T3.

**Proposition T6′ (sharpness for the representatives w_b).** *Let n ≥ 2 and b ∈ ℤ with n ∤ b, (n+1) ∤ b. A primitive element of F₂ is conjugate to r_n^{±1} in H_b iff b | n or b | n+1.*

*Proof.* "If" is T6. Let b ∤ n, b ∤ n+1 (so |b| ≥ 2). H_b = K *_{s = y^b} ⟨y⟩ with K = ⟨x,s | sxs⁻¹ = x²⟩ ≅ ℤ[1/2] ⋊ ℤ; the amalgamated subgroup is C = ⟨s⟩ = ⟨y^b⟩, and x^e ∉ C for e ≠ 0 (x^e ≠ 1 dies in K/⟨⟨x⟩⟩ ≅ ℤ, where s survives). The conjugate ρ = yⁿ·x·y^{−(n+1)}·x⁻¹ of r_n is cyclically reduced of length 4, because b ∤ n, b ∤ n+1. H_b^{ab} = ℤ is generated by y (x ↦ 0) and r_n ↦ −1, so a primitive p conjugate to r_n^{±1} has y-exponent ±1 and is conjugate in F₂ to x^my^{±1} (§2.0), which is cyclically reduced of length 2 (m ≠ 0) or lies in a factor (m = 0). By the conjugacy theorem for amalgams it is not conjugate to ρ. ∎

So for the representatives w_{b′}, b′ ≡ b (mod n(n+1)), of a class C_b there is a primitive neighbour iff some b′ divides n or n+1, i.e. iff C_b is a divisor class. Other representatives of C_b (e.g. x²y^{b′}Xy^{c′} with b′ + c′ ≠ 0, or words that are not HNN-reduced) are **not** covered by T6′; see §4.

### 2.7 Theorem T7 (n = 2 and n = 3; the bridge class versus the divisor classes)

**(a)** *For n ≥ 3 the bridge class C_{2n+1} and its mirror C_{−(2n+1)} are not divisor classes; for n = 2 the bridge class is C_5 = C_{−1}, the Johnson class.* Proof: the residues of 2n+1 modulo n(n+1) of least absolute value are 2n+1 and −(n²−n−1); a divisor of n or n+1 has absolute value ≤ n+1; and n²−n−1 ≤ n+1 iff n ≤ 2, where it equals 1. ∎ In the coordinates (b mod n+1, −b mod n) of T4 the bridge class is (−1,−1) and the Johnson class is (−1,+1): **they coincide iff −1 ≡ 1 (mod n)**. This is the BS-coordinate form of "AK(2) is easy, AK(n ≥ 3) is not" (compare G2(a): ā = ā⁻¹ in C₂).

**(b)** *n = 2: every MS(2,w) with ℓ(w) ≤ 3 is AC-trivial.* The ℓ = 3 classes are C_{±1} (ℤ/6 has no other admissible residue), both divisor classes; apply T3.1 and T6. In particular M₂ ~AC AK(2) is trivialized by two ACM moves and D3: `certificates/th18_m2_bridge_trivialization.json` (178 moves).

**(c)** *n = 3: every MS(3,w) with ℓ(w) ≤ 3 is AC-trivial, or w ∈ C_{±5}^{±1} and MS(3,w) ~AC AK(3).* The admissible residues mod 12 are ±1, ±2, ±5; ±1 and ±2 divide 3 or 4 (T6); C_{−5} = C_7 is the bridge class (one ACM move to M₃, then `ms3_to_ak3_exact.json`), and C_5 contains (YXXYx)⁻¹, the short relator of D's certified member `d_ak3_to_ms0939.json`. So AK(3) is AC-trivial iff one (equivalently every) MS(3,w) with w ∈ C_{±5}^{±1} is; the classes of BS(3,4) with ℓ ≤ 3 contribute nothing else. ∎

**(d)** *General n.* w ∈ C_{2n+1}^{±1} ⇒ MS(n,w) ~AC AK(n) (C + one ACM move); w ∈ C_{−(2n+1)}^{±1} ⇒ ι(MS(n,w)) ~AC AK(n), so MS(n,w) is AC-trivial iff AK(n) is (Lemma D2).

## 3. Experiments (exact commands and outputs)

All runs: one niced core, < 100 MB, a few seconds each. `th18_bs.py` and `th18_survey.py` use the standard library and import `elementary_verify.py` and (self-test only) `g_bs.py`.

```
python3 experiments/th18_bs.py --selftest
# th18_bs self-test passed: invariance (3 x 400 trials), 120 compiled paths replayed, 526 conjugate pairs
# cross-checked against g_bs, class counts n(n-1) for n=2,3,4, 36 divisor-class certificates replayed
python3 experiments/th18_survey.py --selftest        # th18_survey self-test passed
```
The self-test checks: invariance of the class invariant under conjugation and insertion of conjugates of r_n^{±1} (n = 2,3,4); agreement with G's bounded search on 3,000 random short pairs (in both directions); T4's count and labels on all words of length ≤ 7; β_n ∈ C_{2n+1}; xy^k ~ x; T6 for all admissible divisors b, 2 ≤ n ≤ 8 (certificate generated and replayed by the strict verifier). A scratch run sampling 6,000 exponent vectors per necklace confirmed T2(d) for ℓ = 5: 12 and 4 classes (n = 2), 72 and 36 (n = 3), and 72 for (++++−−−), n = 2.

**E1. Repository certificates (no third-party data).**
```
python3 experiments/th18_survey.py --certs
d_ak3_to_ms*.json: 34 files    n=3  l=3 C_-5 (bridge) 17 | n=3  l=3 C_5 (bridge) 17
d_ms2a_to_ms*.json: 6 files    n=2  l=5 d=--+++ a=[0,1,0,0,8] 3 | a=[0,1,1,0,1] 3
d_ms2b_to_ms*.json: 34 files   n=2  l=5 d=--+++ a=[0,1,0,0,1] 3 | a=[0,1,1,0,8] 3
                               n=4  l=3 C_-3 9 | C_3 9        n=5  l=3 C_-14 5 | C_14 5
l_ms*_trivialization.json: 8   n=3  C_-1 1, C_1 1 (divisor)   n=4  C_-1 1, C_1 1 (divisor), C_-6 2, C_6 2
```
(Output condensed; classes are of the short relator, normalized to σ = +1.) So: the 34 certified members of AK(3)'s class are **two** conjugacy classes of BS(3,4); P1 (n = 2) is two ℓ = 5 classes; P2's class contains two ℓ = 5 classes of BS(2,3), C_{±3} of BS(4,5) and C_{±14} of BS(5,6); four of L's eight certificates are instances of T6, and the other four show that C_{±6} of BS(4,5) is AC-trivial (hence, by one ACM move, every MS(4,w) with w ∈ C_{±6}^{±1}).

**E2. The 1190-presentation benchmark** (`all_presentations.txt` of shehper/AC-Solver, fetched to scratch, read with `python3 -I`; third-party, not redistributed):
```
python3 -I experiments/th18_survey.py --bench   all_presentations.txt
python3 -I experiments/th18_survey.py --triage  all_presentations.txt greedy_solved_presentations.txt
   T3 (l=1): AC-trivial                     reported solved: True   330
   T6 (divisor class): AC-trivial           reported solved: False   67
   T6 (divisor class): AC-trivial           reported solved: True   177
   bridge class: ~ AK(n) or its mirror      reported solved: False  34 (n=3), 22 (n=4), 16 (n=5), 14 (n=6), 14 (n=7)
   l=3, other class                         reported solved: False  278
   l=3, other class                         reported solved: True    26
   l>=5                                     reported solved: False  212
python3 -I experiments/th18_survey.py --certify all_presentations.txt
# certificates generated and replayed: {'T3': 330, 'T6': 244}; longest has 14198 moves
```
- t-length by n: ℓ = 1: 170/66/34/18/14/14/14 for n = 1..7; ℓ = 5: 32 (n = 2) and 36 each (n = 3..7); the rest ℓ = 3.
- n = 3: 34 (ℓ = 1) + 66 (C_{±1}, C_{±2}) + 34 (C_{±5}) + 36 (ℓ = 5) = 170. The benchmark members of AK(3)'s class found by D's cap-28 search are exactly the 34 presentations with short relator in C_{±5} — E1 explains D's list.
- For n ≥ 4 the 66 presentations in bridge classes are AC-equivalent to AK(n) or its mirror (T7(d)); none is greedy-solved.
- The 26 greedy-solved presentations in non-divisor ℓ = 3 classes lie in C_{±6} (n = 4), C_{±9} (n = 5), C_{±9} and C_{±15} (n = 6): exactly the non-divisor classes with 2b ≡ 0 (mod n) for n even, resp. 2b ≡ 0 (mod n+1) for n odd, that occur for n ≤ 6 ("half classes"; see §4, open).
- n = 2, ℓ = 5: the 32 presentations fall in all 12 classes of the necklace (+++−−); P1 and P2 take two classes each, eight classes (20 presentations) are unresolved here; the 4 classes of (++−+−) do not occur in the benchmark.
- No presentation with ℓ ≥ 5 is in the greedy-solved list: in this benchmark the t-length separates what greedy search solves (ℓ = 1, divisor and half classes) from what it does not.

**Certificates stored** (`python3 experiments/elementary_verify.py certificates/th18_*.json`, all pass):

| file | start | moves | peak |
|---|---|---:|---:|
| th18_m2_bridge_trivialization | M₂ = (XyyxYYY, XYxxY) | 178 | 39 |
| th18_johnson_p31_trivialization | P(3,1) = (XyyyxYYYY, YxyXX) | 166 | 37 |
| th18_ms3_w2_trivialization | (XyyyxYYYY, xxyyXYY) | 80 | 22 |
| th18_ms3_len1_trivialization | (XyyyxYYYY, XyyyxxxyyyyXy), ℓ = 1 | 259 | 98 |
| th18_ms0318 / 0661 / 0707 / 0834 / 0891 / 1038 | benchmark lines (0-based) with n = 3,4,4,5,6,7 in C_{−2}, C_{−1}, C_{−2}, C_{−3}, C_1, C_{−1}; all but 318 absent from the greedy-solved list | 277 / 840 / 650 / 729 / 2138 / 13862 | 65 / 109 / 125 / 143 / 131 / 413 |

All end exactly at ("x","y"). The other 564 certificates are regenerated and replayed by `--certify` (add an output directory and line numbers to store them).
