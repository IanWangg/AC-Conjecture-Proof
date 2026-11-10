# Research TH10: the metabelian-quotient filter — why torsion, Burnside and just-infinite quotients cannot obstruct AK(n), and which characteristic quotients survive

Date: 2026-11-09 (Los Angeles). Independent research agent TH10 (round 5, theory round; seed: counterexample side, "exotic homes" such as free Burnside groups and other characteristic quotients of F).

**Status.** Obstruction-side theorems with complete proofs (no-go results) and a filter-by-filter analysis of candidate homes. **AK(3) is neither trivialized nor obstructed; no counterexample; the AC conjecture is neither proved nor disproved.** The lead example of the seed is eliminated: no free Burnside group B(2,N), of any exponent N, can obstruct any AK(n) or any Miller–Schupp presentation, and none of odd exponent can separate C4 or any T(a;p,q) from anything. Novelty is not established for any item (Theorem A for Q = F contains the known AC-triviality of MS(1,w)).

## Central claims (P = proved here, X = externally reported/recalled, E = experiment, O = open)

| # | statement | label |
|---|---|---|
| A | **Metabelian-quotient filter.** If some coordinate c of some pair AC-equivalent to U has Q/⟨⟨π(c)⟩⟩ *metabelian*, then Q does not obstruct U. Pair level: an admissible pair (s,t) of Q with Q/⟨⟨s⟩⟩ metabelian is standardizable. (The case Q/⟨⟨π(c)⟩⟩ = 1 is H's Theorem 1 / E's Prop. 5; already the *abelian* case applies where H's Theorem 1 "never applies", i.e. when Q_ab is not cyclic.) | P (§2) |
| A1 | Q has (AC) iff every admissible pair is AC-equivalent to one with a coordinate s such that Q/⟨⟨s⟩⟩ is abelian (equivalently: metabelian). | P (§2) |
| B | **Baumslag–Solitar coordinates.** Let c = v⁻¹u^p v u^{-(p±1)} be a class coordinate of U, (u,v) a basis of F, and Q̄ = Q/⟨⟨π(c)⟩⟩. If the image of u has finite order in Q̄ (e.g. π(u) has finite order in Q, or some power π(u)^N, N ≥ 1, is central in Q), or Q̄ is finite or residually finite, then Q does not obstruct U. | P (§3) |
| B1 | **AK(n), n ≥ 2, and every Miller–Schupp presentation MS(n,w):** if Q obstructs it, then π(y) has infinite order in Q. Hence no periodic group — no B(2,N), N even or odd, no Golod–Shafarevich/Grigorchuk/Gupta–Sidki torsion group — and no just-infinite group obstructs any AK(n) or MS(n,w). | P (§3), using C's theorem M_n ~ AK(n) |
| B2 | **AK(3):** if Q obstructs AK(3), then *every primitive element of F has image of infinite order in Q*, and for every basis (u,v) the group Q/⟨⟨π(v⁻¹u³vu⁻⁴)⟩⟩ is a non-metabelian, non-residually-finite quotient of BS(3,4), and Q/⟨⟨π(u²v⁻³)⟩⟩, Q/⟨⟨π(u³v⁻⁴)⟩⟩, Q/⟨⟨π(u²v⁻⁷)⟩⟩ are non-metabelian. So no quotient of a triangle group, of a free product of two finite cyclic groups, or of PB(m) = F/⟨⟨g^m : g primitive⟩⟩ obstructs AK(3). Same conclusion ("primitives have infinite order") for P1 = C6 and P2. | P (§3), using D Lemma D6, I §5 and certificates |
| C | **Torus coordinates.** If u^p v^{-q} is a class coordinate and π(u) has finite order prime to p, or π(v) finite order prime to q, then Q does not obstruct U. For the chirality targets (no BS coordinate known): a quotient with characteristic kernel separates C4 from an automorphic image only if its primitive order is infinite or divisible by 10; for C3 = T(2;4,7), infinite or divisible by 210. So B(2,N), N odd, is useless for C4, C3 and all T(a;p,q) as well. | P (§3) + E (list of types) |
| D | Q = F: a pair with a class coordinate of type v⁻¹uvu⁻² (BS(1,2)) is AC-trivial. (Recalled as known for MS(1,w): Myasnikov–Myasnikov–Shpilrain.) | P (§2); X for attribution |
| E | Fuchsian characteristic quotients Q_n = ⟨x,y | [x,y]^n⟩: Q₂ obstructs no AK(n) (its braid quotient is V₄-by-ℤ, metabelian); for n divisible by 3 or 4 the braid quotient is not metabelian (for all n ≥ 3 it is D(n,n,n) ⋊ ℤ, X), and Q_n passes every filter of H, N and this note that I could test; U is AC-trivial iff sup_n d_{Q_n}(U) < ∞. | P (§5) |
| F | B(2,N), N odd ≥ 665: passes H's Theorems 1, 2(i), fails filter A. Its finite residual is perfect; the standard AC class is invariant under the non-tame "power" automorphisms of determinant ±1. | P from X (§4) |
| G | Extending A from metabelian to solvable (or finite) one-relator quotients; whether B(2,N) has (AC); whether Q_n (n ≥ 3) or F/(F')^N obstructs AK(3); whether B(2,10k) separates C4 from τ(C4). | O (§6) |

## 0. Previous work read and choice of direction

Read in full: `README.md`, notes H, N, E §2–4; status paragraphs and coordinator's reviews of A–O; skimmed B §1, C (statement and proof table), D (Lemma D6), I (Prop. C, §5), K, O. Facts used, as verified in those notes: the conventions of E/H; H Theorem 1, Theorem 2(i),(ii) with the corrected hypothesis, Corollary 3, Theorem 4; N2.1; C's theorem M_n = (x⁻¹yⁿxy^{-(n+1)}, x⁻¹y⁻¹x²y⁻¹) ~AC AK(n) for all n ≥ 2 (certificate `ms3_to_ak3_exact.json` for n = 3); D Lemma D6 (Aut(F₂) is AC-realized on AK(3)); I §5 (the same for C3, P1); G1 (`g_ak3_to_trefoil_t2_7.json`); `i_c4_to_T4_8_5.json`; E Theorem 1 (residual chains).

**Why this direction.** The seed asks which infinite characteristic quotients pass all filters of H and N, with B(2,N), N odd, as lead example. H's Theorem 1 "never applies" to B(2,N) because Q_ab is not cyclic — but the proof of H's Lemma 2.2 only needs a one-relator quotient to be *abelian*, and a module computation extends this to *metabelian*. The resulting filter (Theorem A) is new relative to A–O and decides the seed's lead example and most of its other candidates at once, through the Baumslag–Solitar coordinate x⁻¹yⁿxy^{-(n+1)} that C put into the class of AK(n): in a quotient where y has finite order this relation makes the one-relator quotient metacyclic. The rest of the note records what survives (§4–6). Overlap warning: TH05 (just-infinite, NSP, hyperbolic quotients) and TH09 (killers of one-relator groups) may reach related statements by other routes; Corollary B1's just-infinite clause and Proposition A3 are the points of contact.

## 1. Conventions

F = F(x,y), X = x⁻¹, Y = y⁻¹; π: F → Q an epimorphism, a = π(x), b = π(y); e(w) ∈ ℤ² the exponent vector. AC moves in Q: inversion, multiplication of one coordinate by the other or its inverse, conjugation of a coordinate by any element of Q, swap. "Multiply coordinate i by an element of the normal closure of the other coordinate" is a composite of AC moves (conjugate the donor, multiply, conjugate back). A pair (s,t) of Q is **admissible** if it normally generates Q and its image in Q_ab is Nielsen-equivalent to (ā, b̄); it is **standardizable** if (s,t) ~_Q (a,b). Q **has (AC)** if every admissible pair is standardizable; Q **obstructs** U if π(U) is not standardizable. If U normally generates F then π(U) is admissible (its exponent matrix is unimodular), and admissibility is AC-invariant. A **class coordinate** of U is a coordinate of some pair AC-equivalent to U in F; conjugates and inverses of class coordinates are class coordinates, and their exponent vectors are primitive. G_c := F/⟨⟨c⟩⟩. Primitive elements of F with the same exponent vector are conjugate (Nielsen; classical).

## 2. Theorem A: the metabelian-quotient filter (proved here)

**Lemma 0.** If (s,t) is admissible, there is a basis (p,q) of F with π(p) ≡ s and π(q) ≡ t modulo [Q,Q].
*Proof.* Some sequence of Nielsen moves takes (ā,b̄) to (s̄,t̄) in Q_ab. Apply the same sequence to (x,y) in F; the result is a basis (p,q) whose image in Q_ab is (s̄,t̄). ∎

**Theorem A.** Let (s,t) be an admissible pair of Q such that Q̄ := Q/⟨⟨s⟩⟩ is metabelian. Then (s,t) ~_Q (a,b). Consequently, if some pair (c,w) ~_AC U in F has Q/⟨⟨π(c)⟩⟩ metabelian, then Q does not obstruct U.

*Proof.* Take (p,q) as in Lemma 0, write bars for images in Q̄, and let M := [Q̄,Q̄], an abelian normal subgroup.
1. p̄ ∈ M, because s̄ = 1 and π(p) ≡ s mod [Q,Q].
2. Q̄ = ⟨p̄,q̄⟩, so Q̄/⟨⟨p̄⟩⟩ is cyclic and M ⊆ ⟨⟨p̄⟩⟩ ⊆ M. Thus M = ⟨⟨p̄⟩⟩ and Q̄ = M⟨q̄⟩.
3. M acts trivially on itself by conjugation, so M is a module over ℤ[τ,τ⁻¹] with τ·m := q̄mq̄⁻¹ (written additively). By step 2, M = ℤ[τ^{±1}]·p̄. Since f(τ) − f(1) ∈ (τ⁻¹ − 1)ℤ[τ^{±1}] for every Laurent polynomial f, we get M = ℤ·p̄ + (τ⁻¹ − 1)M.
4. t ≡ π(q) mod [Q,Q], so t̄ = q̄·m₀ with m₀ ∈ M. Write m₀ = i·p̄ + (τ⁻¹ − 1)m with i ∈ ℤ, m ∈ M. Then, in Q̄,
   m·(q̄p̄ⁱ)·m⁻¹ = q̄·(q̄⁻¹mq̄)·p̄ⁱ·m⁻¹ = q̄·(τ⁻¹m + i p̄ − m) = q̄·m₀ = t̄.
5. Let m̃ ∈ F map to m and put g₀ := m̃·qpⁱ·m̃⁻¹, p' := m̃pm̃⁻¹. Then (p', g₀) is a basis of F, π(p') ≡ s mod [Q,Q], and by step 4, t⁻¹π(g₀) ∈ ⟨⟨s⟩⟩. Multiplying coordinate 1 by this element: (s,t) ~ (s, π(g₀)).
6. Q/⟨⟨π(g₀)⟩⟩ is a quotient of F/⟨⟨g₀⟩⟩ ≅ ℤ, hence abelian, so [Q,Q] ⊆ ⟨⟨π(g₀)⟩⟩ ∋ s⁻¹π(p'). Multiplying coordinate 0: (s, π(g₀)) ~ (π(p'), π(g₀)).
7. (p', g₀) is carried to (x,y) by Nielsen moves, which are AC moves and commute with π: (π(p'),π(g₀)) ~ (a,b).
For the last sentence, (π(c),π(w)) ~_Q π(U) is admissible. ∎

**Remarks.** (i) If Q̄ is abelian, M = 1 and steps 3–4 are empty: this is the argument of H's Lemma 2.2, and the case Q̄ = 1 is H's Theorem 1. (ii) Steps 3–4 say: *in a metabelian group generated by p̄ ∈ M and q̄, every element of q̄M is conjugate to some q̄p̄ⁱ*, the image of a primitive element. (iii) For Q = F: a class coordinate c with G_c metabelian makes U AC-trivial. G_c ≅ ℤ for c primitive; G_c ≅ BS(1,2) = ℤ[1/2] ⋊ ℤ for c = v⁻¹uvu⁻² with (u,v) a basis. So **every pair with a class coordinate of type v⁻¹uvu⁻² is AC-trivial**; for the Miller–Schupp presentations MS(1,w) this is, as far as I recall, a theorem of Myasnikov–Myasnikov–Shpilrain (X; not checked), and step 4 is the reason behind it. This is the positive control of the theorem. (iv) The filter sees only the image of ker π in G_c: it asks whether G_c/π-kernel is metabelian.

**Corollary A1 (criterion for (AC)).** Let 𝒢_Q := {g ∈ Q : Q/⟨⟨g⟩⟩ is metabelian}; it contains the image of every primitive element of F. Then Q has (AC) iff every admissible pair of Q is AC-equivalent to a pair with a coordinate in 𝒢_Q, and **Q obstructs U iff no coordinate of any pair in the Q-class of π(U) lies in 𝒢_Q.** The same holds with "abelian" in place of "metabelian".
*Proof.* (⇒) Q/⟨⟨a⟩⟩ is cyclic. (⇐) Theorem A, after a swap if necessary. ∎

**Corollary A2 (two pairs).** If U and V each have a class coordinate whose one-relator quotient of Q is metabelian, Q does not separate U from V. If ker π is φ-invariant (φ ∈ Aut(F)) and U has such a coordinate, Q does not separate U from φ(U).
*Proof.* Both pairs are standardizable; φ(c) is a class coordinate of φ(U) and Q/⟨⟨πφ(c)⟩⟩ ≅ Q/⟨⟨π(c)⟩⟩ via the induced automorphism. ∎

**Proposition A3 (good cosets).** If (s,t) is admissible and t ∈ g·⟨⟨s⟩⟩ for some g ∈ 𝒢_Q, then (s,t) is standardizable.
*Proof.* (s,t) ~ (s,g), admissible, and Q/⟨⟨g⟩⟩ is metabelian. ∎

## 3. Consequences: Baumslag–Solitar and torus coordinates (proved here)

**Theorem B (Baumslag–Solitar coordinates).** Let (u,v) be a basis of F and c = v⁻¹u^p v u^{-q} a class coordinate of U (then |p − q| = 1, because e(c) = (p − q)e(u) is primitive; so gcd(p,q) = 1). Let Q̄ = Q/⟨⟨π(c)⟩⟩.
(a) If the image ū of u has finite order in Q̄, then ⟨ū⟩ is normal in Q̄ with cyclic quotient.
(a′) If ū^N is central in Q̄ for some N ≥ 1 (e.g. π(u)^N is central in Q), then ū^N = 1.
(b) Every finite quotient of Q̄ is metacyclic; hence Q̄ is metabelian if it is residually finite.
In each case Q does not obstruct U.
*Proof.* (a) v̄⁻¹ū^p v̄ = ū^q. If ū has order m, the conjugate elements ū^p and ū^q have the same order, so gcd(m,p) = gcd(m,q); this number divides gcd(p,q) = 1. Hence ⟨ū^p⟩ = ⟨ū^q⟩ = ⟨ū⟩, v̄ normalizes ⟨ū⟩, and Q̄/⟨ū⟩ is generated by v̄. (a′) ū^{pN} = v̄⁻¹ū^{pN}v̄ = ū^{qN}, so ū^{(q−p)N} = ū^{±N} = 1. (b) Apply (a) in the finite quotient; Q̄'' lies in the kernel of every map to a metabelian group, hence in the finite residual. In each case Q̄ is metabelian; apply Theorem A. ∎

*Remark.* The same argument gives ū of finite order whenever Q̄ carries a conjugation-invariant function ℓ with ℓ(g^k) = |k|·ℓ(g) that is positive on elements of infinite order — e.g. stable translation length when Q̄ is a hyperbolic group (X) — since ℓ(ū^p) = ℓ(ū^q) forces ℓ(ū) = 0. So a hyperbolic one-relator quotient at a Baumslag–Solitar coordinate never obstructs.

**Corollary B1 (AK(n) and Miller–Schupp presentations).** Let n ≥ 2 and let U be AK(n), or any presentation MS(n,w) = (x⁻¹yⁿxy^{-(n+1)}, x⁻¹w) of the trivial group. If Q obstructs U, then:
(i) the image of y in Q/⟨⟨π(x⁻¹yⁿxy^{-(n+1)})⟩⟩ has infinite order; in particular π(y) has infinite order in Q;
(ii) Q/⟨⟨π(x⁻¹yⁿxy^{-(n+1)})⟩⟩ is not residually finite (and not metabelian);
(iii) Q is not periodic, not just-infinite, and no nontrivial power of π(y) is central in Q. In particular **no free Burnside group B(2,N), no group of finite exponent, no finitely generated torsion group of any kind, and no central extension of such a group (e.g. Adian's torsion-free groups A(2,N), X) obstructs any AK(n) or MS(n,w).**
*Proof.* By C's theorem, x⁻¹yⁿxy^{-(n+1)} = v⁻¹uⁿvu^{-(n+1)} with (u,v) = (y,x) is a coordinate of M_n ~ AK(n); for MS(n,w) it is a coordinate of the presentation itself. (i), (ii) are Theorem B(a), (b); the statements on central powers are (a′) (in a central extension of a periodic group some power of π(y) is central). (iii): if Q is just-infinite and π(c) = 1, the other coordinate normally generates Q and Theorem A applies to it; if π(c) ≠ 1, ⟨⟨π(c)⟩⟩ has finite index and (b) applies. ∎

**Corollary B2 (AK(3), P1 = C6, P2: every primitive element).** If Q obstructs AK(3), then:
(i) for **every primitive element g of F**, π(g) has infinite order and no nontrivial power of π(g) is central in Q;
(ii) for every basis (u,v) of F, Q/⟨⟨π(v⁻¹u³vu⁻⁴)⟩⟩ is a non-metabelian, non-residually-finite quotient of BS(3,4) in which u has infinite order, and the torus quotients Q/⟨⟨π(u²v⁻³)⟩⟩, Q/⟨⟨π(u³v⁻⁴)⟩⟩, Q/⟨⟨π(u²v⁻⁷)⟩⟩ are non-metabelian.
Consequently no quotient of a triangle group ⟨x,y | x^l, y^m, (xy)^k⟩, of a free product of two finite cyclic groups, of PB(m) := F/⟨⟨g^m : g primitive⟩⟩, or of any group in which one primitive element is torsion or has a nontrivial central power (torus-knot groups, B₃), obstructs AK(3). Statement (i) also holds for P1 = C6 and P2.
*Proof.* The AC class of AK(3) is closed under Aut(F₂) (D, Lemma D6), so every automorphic image of a class coordinate is a class coordinate. The class contains x⁻¹y³xy⁻⁴ (C; `ms3_to_ak3_exact.json`), x³y⁻⁴, the braid relator ~ (xyx)²(xy)⁻³, and G's relator ~ U²V⁻⁷ for a basis (U,V) (`g_ak3_to_trefoil_t2_7.json`; identities checked by the self-test of §7). Hence for every basis (u,v) the four words of (ii) are class coordinates; apply Theorems B and A. Every primitive g is the first member of a basis. P1 = (x⁻¹y²xy⁻³, x⁻³y⁻¹x²y) and P2 = (x⁻¹y²xy⁻³, x⁻³y⁻¹x²y⁻¹) (start pairs of `i_p1_aut_swap.json`, `i_p2_aut_swap.json`) have the BS(2,3) relator as a coordinate, and Aut(F₂) is AC-realized on their classes (I §5). (Cross-check for the representative C6 = (xxyxxYY, xyXYYXy) of P1's class: `m_c6_aut_x_xy.json` passes through xyXyXYxYxY, an automorphic image of x⁻¹y²xy⁻³ up to conjugacy and inversion; §7.) ∎

**Theorem C (torus coordinates versus torsion).** Let (u,v) be a basis of F, p, q nonzero integers, and c = u^p v^{-q} (or a conjugate or inverse) a class coordinate of U. If the image of u in Q̄ = Q/⟨⟨π(c)⟩⟩ has finite order prime to p, or the image of v has finite order prime to q, then Q̄ is abelian and Q does not obstruct U.
*Proof.* z := ū^p = v̄^q is central in Q̄ = ⟨ū,v̄⟩. If ū has order m prime to p and kp ≡ 1 (mod m), then ū = z^k is central and Q̄ is abelian. Symmetrically for v̄. ∎

**Corollary C1 (chirality targets; no BS coordinate is known for them).** Let ker π be characteristic and m(Q) ∈ ℕ ∪ {∞} the common order of the images of the primitive elements. If Q separates C4 from the standard pair or from any φ(C4), then m(Q) is infinite or divisible by 10; for C3 = T(2;4,7), infinite or divisible by 210. For arbitrary kernel: Q does not obstruct T(a;p,q) = (x^p y^q, x^a y x⁻¹ y) if π(x) has finite order prime to p or to a+1, or π(y) finite order prime to q, or π(x⁻¹y) finite odd order. In particular **groups of odd exponent — the Novikov–Adian range of B(2,N) — separate none of C4, C3, T(a;p,q) from anything.**
*Proof.* Corollary A2 and Theorem C. x^a y x⁻¹ y = x^{a+1}(x⁻¹y)² with basis (x, x⁻¹y). C4 = (x⁴yx⁻¹y, xy³xy⁻²) ~ T(4;8,5) (`i_c4_to_T4_8_5.json`) has the coordinates x⁸y⁵, x⁵(x⁻¹y)², and xy³xy⁻² = w·y⁵·w with w = xy⁻² (basis (w,y)): types (8,5), (5,2), (2,5), so a finite m(Q) must be divisible by 2 and 5. The certificates starting at C3 contain coordinates of torus types (2,3), (4,7), (5,9) (§7), forcing 2, 3, 5, 7 ∣ m(Q). ∎

For AK(n) the torus coordinates add: if Q obstructs AK(n), then π(xyx) has infinite or even order and π(xy) infinite order or order divisible by 3 (braid relator ~ (xyx)²(xy)⁻³; for n = 3 this is superseded by B2(i)).

## 4. Free Burnside groups B = B(2,N) = F/F^N

**External facts used (recalled, not verified here).** (X1) Novikov–Adian, Adian: for odd N ≥ 665, B(2,N) is infinite and the centralizer of every nontrivial element is cyclic. (X2) Kostrikin, Zelmanov, with the Hall–Higman reduction: B(2,N) has a largest finite quotient R(2,N). (X3) Ivanov, Lysenok: B(2,N) is infinite for large N divisible by a high power of 2.

**4.1 Filter by filter (N odd ≥ 665).**
- H Theorem 1 never applies: B_ab = (ℤ/N)² is not cyclic.
- H Theorem 2(i): B has no nontrivial abelian normal subgroup (proved from X1): such an A lies in the centralizer of one of its nontrivial elements, so A is finite cyclic; B/C_B(A) embeds in Aut(A) and C_B(A) is cyclic, so B would be finite.
- H Corollary 3: B is not virtually solvable (a finitely generated virtually solvable torsion group is finite).
- H Theorem 2(ii): whether B has a minimal normal subgroup is not decided here; Proposition 4.1 shows that the top chief factors of the finite residual are invisible.
- N2.1: F^N is verbal, so B is a legitimate (basis-sensitive) home for a chirality invariant.
- **Filter A: B fails it.** For AK(n), MS(n,w), P1, P2: all N (Corollary B1, B2). For C4: unless 10 ∣ N; for C3: unless 210 ∣ N (Corollary C1). The groups B(2,10k) (X3 range, even exponent) are the only Burnside groups not excluded as separators of C4 from τ(C4) by this note.

**Proposition 4.1 (finite residual; proved here from X2).** Let B = B(2,N) be infinite and K = ker(B → R(2,N)). Then: (a) K is the finite residual of B, K ⊆ [B,B], and K is finitely generated, infinite, perfect, without proper subgroups of finite index; (b) K has maximal proper B-normal subgroups M; for each, K/M is a nonabelian minimal normal subgroup of B/M and B/M has (AC); the same holds for B/(M₁ ∩ … ∩ M_r).
*Proof.* (a) Every finite quotient of B factors through R(2,N), which maps onto (ℤ/N)². K/[K,K] is a finitely generated abelian group of exponent dividing N, hence finite; [K,K] is characteristic in K, so normal of finite index in B, so it contains K. A finite-index subgroup of K contains a finite-index normal subgroup of B, hence K. (b) A union of a chain of proper B-normal subgroups of K is proper because K is finitely generated; Zorn gives M. K/M is minimal normal in B/M, perfect and nontrivial, hence nonabelian. (B/M)/(K/M) = R(2,N) is finite and has (AC) (H Cor. 3(b)); H Theorem 2(ii) lifts (AC) to B/M. For I = M₁ ∩ … ∩ M_{r−1} ⊄ M_r: I·M_r = K, so I/(I ∩ M_r) ≅ K/M_r as B-groups is a nonabelian minimal normal subgroup of B/(I ∩ M_r) with quotient B/I; induct. ∎

**Lemma 4.2 (Euclid for torus pairs; classical, proof included).** If ad − bc = ±1, then (x^a y^b, x^c y^d) is AC-trivial in F.
*Proof.* u₀u₁⁻¹ = x^a y^{b−d} x^{−c} is conjugate to x^{a−c}y^{b−d}: "row₀ − row₁" is realized inside the family. Replacing u₁ first by x^{−c}y^{−d} (a conjugate of u₁⁻¹) and restoring it afterwards realizes "row₀ + row₁"; symmetrically for row₁. These operations reduce a unimodular matrix to a signed permutation matrix, i.e. the pair to (x^{±1}, y^{±1}) or (y^{±1}, x^{±1}). ∎

**Proposition 4.3 (power twists; proved here).** Let a = π(x), b = π(y) have orders dividing N in Q and kl ≡ 1 (mod N). Then (a^k, b^l) ~_Q (a,b). If Q is relatively free of exponent N, let P ≤ Aut(Q) be generated by the tame automorphisms T (induced from Aut(F)) and the power automorphisms θ_k: a ↦ a^k, b ↦ b (gcd(k,N) = 1). Then every α ∈ P whose determinant on Q_ab = (ℤ/N)² is ±1 satisfies (α(a), α(b)) ~_Q (a,b).
*Proof.* Let k' be an inverse of k modulo N²; then k' ≡ l (mod N) and kk' = 1 + N²β. The pair (x^k y^N, x^{Nβ} y^{k'}) has determinant 1, so it is AC-trivial in F (Lemma 4.2), and its image in Q is (a^k, b^l). For the second statement let S = {α ∈ Aut(Q): α(a,b) ~ (a,b)}, a subgroup containing T (automorphisms preserve ~_Q). The subgroup generated by the conjugates θ_kTθ_k⁻¹ contains T and is normalized by the θ's, so it is the normal closure of T in P; P modulo it is generated by the θ_k, and det identifies this quotient with (ℤ/N)^×/{±1} (θ₋₁ is tame). So {α ∈ P: det α = ±1} is generated by the θ_kτθ_k⁻¹, τ a Nielsen generator, and θ_kτθ_k⁻¹ ∈ S iff (τ(a)^l, τ(b)) ~ (a^l, b), l = k⁻¹. For an inversion this is an inversion move; for τ: a ↦ ab it holds since (ab)^l ≡ a^l mod ⟨⟨b⟩⟩; for τ: b ↦ ba since ba ≡ b mod ⟨⟨a⟩⟩ = ⟨⟨a^l⟩⟩; for the swap, (b^l, a) ~ (a, b^l), and applying the automorphism b ↦ b^l to (a^l, b^k) ~ (a,b) gives (a^l, b) ~ (a, b^l). ∎

**4.4 The Burnside AC problem (open).** *Does B(2,N) have (AC)?* By Corollary A1 it fails iff some admissible AC class of B consists of pairs (s,t) with both B/⟨⟨s⟩⟩ and B/⟨⟨t⟩⟩ non-metabelian. For N = p prime the one-relator Burnside quotients E = B/⟨⟨s⟩⟩ of admissible pairs are of two kinds only (proved here): E ≅ ℤ/p, or E is infinite with E' perfect of index p. (E_ab ≅ ℤ/p since s̄ is part of a basis of (ℤ/p)²; E/E'' is a finitely generated metabelian torsion group, hence a finite p-group with cyclic abelianization, hence cyclic, so E' = E''; a finite E is nilpotent, so E' = 1.) Proposition 4.3 shows that the obvious non-tame bases are standardizable. A failure of (AC) in B would not by itself be a counterexample to the AC conjecture: the offending pair would have to be the image of a pair normally generating F, and by B1, B2, C1 it is not one of the pairs of this project.

## 5. Characteristic quotients: reductions and what survives

Let Q = F/V with V characteristic, and suppose Q obstructs U (or separates U from φ(U)).

**5.1 Reductions (proved here, from H and §2–3).**
- (R1) Solvable layers are invisible: if V ⊆ W ⊴ F with W/V solvable and W ⊆ [F,F]·V, then F/W already obstructs U. (The derived series of W/V is normal in Q and inside [Q,Q]; apply H's Theorem 2(i) to its last nontrivial term and induct.) So a product variety 𝔘𝔙 with 𝔘 solvable and V(F) ⊆ [F,F] is no better than 𝔙.
- (R2) For every class coordinate c, the image of G_c in the variety — G_c/V(G_c) when V is verbal — is not metabelian (Theorem A).
- (R3) For AK(3), P1, P2: V contains no nontrivial power of a primitive element, and no primitive element has a nontrivial central power in Q (Corollary B2). So the exponent-type characteristic quotients B(2,N), PB(m), and all their quotients are excluded; a surviving Q has "primitive order" m(Q) = ∞.
- (R4) For C4: m(Q) is infinite or divisible by 10 (Corollary C1); B(2,10k) and PB(10k) are not excluded.

**5.2 The Fuchsian family Q_n = ⟨x,y | [x,y]^n⟩ (n ≥ 2).** ⟨⟨[x,y]^n⟩⟩ is characteristic: the Nielsen generators send [x,y] to a conjugate of [x,y]^{±1} ([y,x] = [x,y]⁻¹; [x⁻¹,y] = x[x,y]⁻¹x⁻¹; [xy,y] = y⁻¹[x,y]y). Recalled (X, standard): Q_n is the orbifold group of a torus with one cone point of order n, a cocompact Fuchsian group — non-elementary hyperbolic, linear, residually finite, with no nontrivial finite or abelian normal subgroup. Hence (proved from this): H's Theorem 1 never applies (Q_ab = ℤ²); there is no abelian normal subgroup (Theorem 2(i)); there is no minimal normal subgroup (a minimal normal N is infinite, and N ∩ L ∈ {1, N} for every finite-index normal L, with N ∩ L = 1 impossible, so N lies in the finite residual, which is trivial); Q_n is not virtually solvable; primitives have infinite order (R3 passes).

*Braid coordinate (proved here).* In B₃ = ⟨x,y | xyx = yxy⟩ one has [x,y] = yx⁻¹ (indeed x⁻¹y⁻¹xy·x = x⁻¹y⁻¹·yxy = y). Put d = yx⁻¹ and d_k = x^k d x^{-k}; the braid relation reads x d x² = d x² d x, i.e. d₁ = d₀d₂. So in E_n := Q_n/⟨⟨π(xyxy⁻¹x⁻¹y⁻¹)⟩⟩ = ⟨x,y | xyx = yxy, (yx⁻¹)^n⟩ the normal closure D of d is generated by d₀, d₁ (d_{k+2} = d_k⁻¹d_{k+1}, d_{k−1} = d_k d_{k+1}⁻¹) and E_n/D is cyclic.
- n = 2: d₀² = d₁² = (d₀⁻¹d₁)² = 1 force D abelian, so E₂ is metabelian and, by Theorem A, **Q₂ = ⟨x,y | [x,y]²⟩ obstructs no AK(n)** (the braid relator is a coordinate of AK(n) itself). The same holds for every quotient of Q₂, e.g. the relatively free group of the law [x,y]² = 1.
- n divisible by 3 or 4: E_n is not metabelian, because it maps onto S₄ (a quotient of PSL(2,ℤ) in which d, an element of S₄' = A₄ normally generating A₄, has order 3), respectively onto SL(2,3) (where d ∈ Q₈ has order 4). For every n ≥ 3, E_n ≅ D(n,n,n) ⋊ ℤ with D(n,n,n) = ⟨d₀,d₁ | d₀ⁿ, d₁ⁿ, (d₀⁻¹d₁)ⁿ⟩ the von Dyck group, given the classical fact (X) that B₃' is free on d₀, d₁. E₃ is virtually abelian of derived length 3: the first case beyond the reach of Theorem A.
- BS coordinate x⁻¹y³xy⁻⁴: the quotient ⟨x,y | x⁻¹y³x = y⁴, [x,y]^n⟩ contains t = x⁻¹yx and y with t³ = y⁴, (t⁻¹y)^n = 1, a quotient of a central extension of the triangle group Δ(3,4,n); whether it is non-metabelian with y of infinite order was **not verified** (expected for n ≥ 3).

*Residual chain (proved here).* For 1 ≠ w ∈ F take a finite quotient φ of F with φ(w) ≠ 1 and n = ord φ([x,y]); then w ∉ ⟨⟨[x,y]^{nk}⟩⟩ for all k. So K_j = ⟨⟨[x,y]^{j!}⟩⟩ is a nested chain with trivial intersection, and E's Theorem 1 gives d_F(U) = sup_j d_{Q_{j!}}(U): **U is AC-trivial iff sup_n d_{Q_n}(U) < ∞.** Unlike E's chains of finite 2-groups, here a single term may be infinite: Q_n obstructs U iff d_{Q_n}(U) = ∞. For n ≥ 3 I know no reason for or against.

**5.3 Other candidates, briefly.**
- F/(F')^N (verbal; Burnside-by-abelian; metabelian for N = 2, so take N ≥ 3): primitives have infinite order; its braid quotient is B₃/(B₃')^N, an extension of a 2-generator group of exponent N by ℤ. Not decided.
- B(2,10k), PB(10k): the only exponent-type quotients not excluded for C4 versus τ(C4).
- Adian's torsion-free central extensions A(2,N) of B(2,N) (X): primitives have infinite order, but y^N is central, so they are excluded for AK(n), MS(n,w) by Theorem B(a′).

## 6. What would have to be proved for a counterexample

By Corollary A1 the task has an exact form. Fix U (AK(3) against the standard pair, or C4 against τ(C4)) and a quotient Q.
1. **Exact criterion.** Q obstructs U iff there is a set 𝒞 of admissible pairs of Q, closed under the AC moves of Q, containing π(U), such that for every (s,t) ∈ 𝒞 both Q/⟨⟨s⟩⟩ and Q/⟨⟨t⟩⟩ are non-metabelian (equivalently: nonabelian). An "invariant" is any property that certifies membership in such a 𝒞.
2. **Necessary conditions on Q for AK(3)** (all proved): infinite, not virtually solvable (H); no class coordinate normally generates (H); abelian normal subgroups inside [Q,Q] and nonabelian minimal normal subgroups may be factored out (H); every primitive element has infinite order; not periodic; not just-infinite; for every basis (u,v) the quotient Q/⟨⟨π(v⁻¹u³vu⁻⁴)⟩⟩ is a non-residually-finite quotient of BS(3,4) with u of infinite order, and the three torus quotients are non-metabelian (this note). Every certified class coordinate of BS(3,4) or torus type found in §7 (@@COUNT@@), and each of its automorphic images, gives such a condition.
3. **Smallest untested homes.** (a) Q₃ = ⟨x,y | [x,y]³⟩, more generally Q_n, n ≥ 3: decide whether x⁻¹y³xy⁻⁴ has a metabelian quotient there (a finite computation in a Fuchsian group quotient), then whether the image of x³y⁻⁴ in E₃ = D(3,3,3) ⋊ ℤ is conjugate to a primitive image (decidable: E₃ is virtually ℤ³). If yes, Q₃ is dead by Proposition A3. (b) F/(F')³. (c) For C4: B(2,10k).
4. **The theorem that would close the solvable gap:** *if Q/⟨⟨s⟩⟩ is solvable (or finite) and (s,t) is admissible, then (s,t) is standardizable.* True for finite and solvable Q (BLM, Guyot). If true in general, every one-relator quotient at every class coordinate of a counterexample must be non-solvable; with Theorem B this would say that an obstructing Q for AK(3) has, for every basis, a non-solvable quotient of BS(3,4) as a quotient — a very rigid requirement.
5. **Controls for any proposed invariant:** it must vanish on every pair with a coordinate in 𝒢_Q, in particular on AK(1), AK(2), on every MS(1,w), and be constant along every certificate in `certificates/`.

## 7. Experiment (light; exact)

`experiments/th10_torus_coords.py` (standard library; imports the repository verifier read-only):
```sh
python3 experiments/th10_torus_coords.py --selftest
#  selftest passed (30821 instances of Theorem B's core, 27028 of Theorem B''s core)
python3 experiments/th10_torus_coords.py --scan      # about 3 CPU-minutes
```
The self-test (a) checks the word identities quoted in §3: the braid relator is conjugate to (xyx)²(xy)⁻³; the target of `g_ak3_to_trefoil_t2_7.json` (replayed) is (U²V⁻⁷ up to conjugacy, braid) for the explicit basis (U,V); `ms3_to_ak3_exact.json` (replayed) joins AK(3) to a pair containing a BS(3,4)-type relator; C4 and T(4;8,5) have torus types (2,5),(2,5),(2,5),(5,8); (b) checks the algebraic core of Theorem C (30,821 instances: generating pairs of S₃, A₄, S₄, A₅, D₇, 7:3, 7:6 and five types (p,q)) and of Theorem B(a) (27,028 instances: ⟨u⟩·⟨⟨c⟩⟩ is normal and contains [u,v] for c = v⁻¹u^p v u^{-(p+1)}, p ≤ 4); (c) checks that S₃, S₃, D₇ are nonabelian images of the three torus quotients of AK(3). Type detection: Whitehead descent on cyclic words followed by a breadth-first search over the minimal level set; a positive answer exhibits an automorphism, so positives are sound.

The scan lists, for the states of all 148 strict certificates grouped by start pair, the distinct cyclic coordinates of torus type (p,q) and of BS(p,p+1) type ("BSp"). Selected rows (start pair: types with multiplicities):
- AK(3) (xxxYYYY, xyxYXY): BS3: 415, (2,3): 508, (3,4): 169, (2,7): 2;
- AK(4), AK(5), AK(6), AK(7), AK(8), AK(10) (K's certificates): BS4, BS5, BS6, BS7, BS8, BS10 respectively, plus (2,3) and (n,n+1);
- C6 = (xxyxxYY, xyXYYXy): BS2: 31, (2,3): 5 (witness xyXyXYxYxY in `m_c6_aut_x_xy.json`);
- C4 = (xxxxyXy, xyyyxYY): (2,5): 72, (5,8): 7, no BS type; C3 = (x⁴y⁷, x²yx⁻¹y): (2,3), (2,7), (3,8), (4,7), (5,9), no BS type; X = T(2;4,9): (2,3), (2,9), (3,10), (4,9), (5,11), no BS type.
So within the certified part of their classes, the two "chiral" candidates C4 and X (and C3) have only torus coordinates, while every class known to be Aut-closed except C3 has a Baumslag–Solitar coordinate. This is an observation about the certificates, not a theorem about the classes.

## 8. Failed attempts (with reasons)

1. **From metabelian to solvable or finite one-relator quotients.** Step 4 of Theorem A needs every element of q̄M that normally generates Q̄ to be congruent to an element of 𝒢_Q. For metabelian Q̄ the conjugates of q̄p̄ⁱ suffice. They do not in general: in Q̄ = 7^{1+2} ⋊ ℤ/3 (order 1029; t acts by diag(2,4) on the Frattini quotient and trivially on the centre; p̄ = (1,1,0)), which is generated by p̄ ∈ Q̄' and q̄ = t, the coset tQ̄' consists of 7 conjugacy classes of normal generators, and the elements tp̄ⁱ meet only 4 of them (checked by machine). Whether other elements of 𝒢_Q meet the remaining classes depends on Q, not only on Q̄; I could not decide it. For non-solvable finite Q̄ the method fails more drastically: in A₅¹⁹ (2-generated by P. Hall; X) the normal generator (g,…,g) belongs to no generating pair, so it is not a primitive image.
2. **Lifting with memory.** If Q̄ = Q/⟨⟨s⟩⟩ has (AC), lifting a standardizing path of (1,t̄) gives (s,t) ~ (an₀, bn₁) with n_i ∈ ⟨⟨s⟩⟩, but after the first move ⟨⟨s⟩⟩ is no longer the normal closure of a coordinate, and H's module corrections need an abelian kernel. No gain over H's Theorem 2.
3. **Torus coordinates with non-coprime torsion.** If gcd(ord ū, p) > 1 and gcd(ord v̄, q) > 1 the quotient is a central extension of a quotient of ℤ/p' * ℤ/q', and nothing forces it to be metabelian (S₄ for (2,3)); so Theorem C cannot be sharpened to "any torsion" — the BS coordinate is what makes Corollary B1 work.
4. **Minimal normal subgroups of B(2,N), and (AC) for B(2,N).** Not decided; both need the internal theory of Burnside groups, which I cannot verify here. After Corollary B1 they are irrelevant for AK(n), but 4.4 remains a clean open problem.
5. **Q_n for n ≥ 3.** The braid quotient E₃ = D(3,3,3) ⋊ ℤ is virtually abelian but not metabelian, so attempt 1 is exactly what blocks a decision.

## 9. Honest limits

- Everything here is a necessary condition on a hypothetical obstructing quotient; nothing shows that AK(3), C4 or anything else is or is not AC-trivial. F itself satisfies every condition (G_c is not metabelian for the known coordinates of AK(3)).
- Corollary B2 uses D's Lemma D6, I §5, C's theorem and G1 through their certificates; I replayed `ms3_to_ak3_exact.json`, `g_ak3_to_trefoil_t2_7.json`, `i_c4_to_T4_8_5.json` and all certificates in the scan, but not D's seven automorphism certificates separately (they are covered by the repository's verification standard).
- Facts about Burnside groups, Fuchsian groups, P. Hall's 19, the freeness of B₃' on d₀, d₁ and the Myasnikov–Myasnikov–Shpilrain attribution are recalled from memory (arXiv and journals are blocked here) and are labelled X wherever used; no theorem of §2–3 depends on them.
- Theorem A for Q = F with a BS(1,2)-type coordinate is a known phenomenon; Theorems A–C are elementary, and I could not check the literature (BLM, Guyot, Myropolska, Gilman–Myasnikov) for equivalent statements. Novelty is not established.
- The statements about E_n for n not divisible by 3 or 4, and about the BS quotient of Q_n, are not proved here.

## 10. Advice to the coordinator (ranked)

1. **Record Theorem A and Corollaries B1–B2 in the README's list of constraints**: an obstructing quotient for AK(3) has no primitive torsion, is not periodic, not just-infinite, and all its one-relator quotients at class coordinates are non-metabelian; for all AK(n), MS(n,w): π(y) has infinite order. This removes the whole Burnside/torsion side of the counterexample search for the AK and MS families. A second reader should check steps 3–4 of Theorem A (the module identity) and Theorem B(a).
2. **Give one agent the solvable gap** (§6.4, §8.1): prove or refute "Q/⟨⟨s⟩⟩ solvable (or finite) ⇒ (s,t) standardizable". The order-1029 group of §8.1 is the first test case; a refutation would be the first genuinely new pair-level obstruction mechanism since N's affine monodromy problem.
3. **Decide Q₃** (§6.3(a)): a finite, exact computation in a virtually abelian group. If the image of x³y⁻⁴ (or of another killer) in E₃ is conjugate to a primitive image, Q₃ is dead; iterate over n and over the 164 coordinates.
4. **Chirality:** look for a Baumslag–Solitar-type coordinate in C4's class (the scan found none among 79 torus-type coordinates). Finding one would, with Theorem B, remove all torsion quotients for C4 as well; its absence in larger forward sets would be a structural difference between C4 and the Aut-closed classes worth stating.
5. **Use 𝒢_Q as a search target on the constructive side:** by Remark (iii) a single class coordinate of type v⁻¹uvu⁻² (or any c with G_c metabelian) trivializes; `th10_torus_coords.py` detects the type in milliseconds per word.

## Files written

- `research/research-th10.md` (this note).
- `experiments/th10_torus_coords.py` (`--selftest`, `--scan`).

## References

- Notes B, C, D, E, G, H, I, N of this repository and the certificates named above.
- A. V. Borovik, A. Lubotzky, A. G. Myasnikov, *The finitary Andrews–Curtis conjecture*; L. Guyot, *On Andrews–Curtis conjectures for soluble groups* (externally reported via B, E, H).
- A. D. Myasnikov, A. G. Myasnikov, V. Shpilrain, *On the Andrews–Curtis equivalence* (2002) — recalled for MS(1,w); not consulted.
- S. I. Adian, *The Burnside problem and identities in groups*; A. Yu. Ol'shanskii, *Geometry of defining relations in groups*; E. Zelmanov (restricted Burnside problem); S. Ivanov, I. Lysenok (even exponents) — recalled, not consulted.
- J. Nielsen (primitive elements and [x,y] under Aut(F₂)); J. H. C. Whitehead (minimal words); P. Hall, *The Eulerian functions of a group* (A₅¹⁹) — classical, recalled.
