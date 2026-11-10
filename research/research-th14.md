# Research TH14: what one stabilization buys — Aut-invariance, stable substitution and generator exchange, the composition formula, and one closed exit for AK(3)

Date: 2026-11-09 (Los Angeles). Independent research agent TH14 (round 5, theory round).

**Status: complete for this round.** Everything in this note is about **STABLE** AC equivalence (one extra
generator z with relator z; rank 2n for B2) unless a statement is explicitly marked *ordinary*.
**No ordinary AC result on AK(3) or C4, no AK(3) trivialization (stable or ordinary), no obstruction, no
counterexample; the stable status of AK(3) remains open.** Central claims (all *proved here* with complete
proofs unless labelled otherwise; novelty not established — A and B2 are classical in content):

| # | statement | label |
|---|---|---|
| A | For every balanced presentation U of the trivial group (any rank n), the AC class of the once-stabilized tuple (U, z) in F_{n+1} is invariant under **all of Aut(F_{n+1})**; explicit macro-move counts in terms of the areas of the generators. In particular (U,z) ~AC (φ(U),z) for every φ ∈ Aut(F_n): "chirality" (C4 vs φ(C4)) is invisible after ONE stabilization | proved (stable), §2 |
| A-cert | (C4, z) → (ε_y(C4), z), ε_y: y ↦ y⁻¹ (not known to be realized in rank 2): 695-move rank-3 certificate, own verifier | proved by certificate (stable), §6 |
| B | **Stable substitution theorem.** If (p,q) normally generates F₂ and ⟨p,q,t⟩ = F₂ for some t ("corank ≤ 1"), then (U∘(p,q), z) ~AC (U, z) in rank 3. Case U = (x,y): every corank-≤1 normally generating pair is AC-trivial after one stabilization (B′); rank-n version and rank reduction "corank k ⇒ stably of rank k" (B3) | proved (stable), §3, §7 |
| B2 | **Composition formula.** For balanced presentations U, P of the trivial group of rank n: (U∘P, z₁..z_n) ~AC U ⊔ P in rank 2n. Hence stably U∘P ~ P∘U, and U∘P ~ U whenever P is stably AC-trivial | proved (stable), §4 |
| C | Substitution creates no new primitive-relator exit: w(p,q) primitive in F₂ ⇒ w primitive | proved, §3 |
| E1 | The two stable exits "relators extend to a generating triple" (E1) and "relators lie in a proper rank-2 subgroup" (E2) are finite Stallings-graph tests | proved, §5 |
| E3 | For the standard AK(3) relators (and every ACM replacement of x³y⁻⁴ with the trefoil relator frozen), **no conjugates extend to a generating triple of F₂**: the cheapest stable exit is closed, for all conjugators (Grushko + trace descent in SL₂(ℤ) + a mod-8 obstruction) | proved, §5.1 |
| E-exp | No E1 hit for 47 known members of AK(3)'s class (4,204 subgroups); no E2 factorization for the 18 members of length ≤ 15 (1,150 subgroups, 16 with pruned closure) | experiment, §5.2 |
| F | **Generator exchange ("subgroup-ACM").** Exact conjugacy condition in the one-relator group F/⟨⟨r₂⟩⟩ under which "introduce z = w, eliminate y = v(x,z)" is a one-stabilization equivalence. Consequence: AK(3) ~₁ V_k = (x³zx⁻⁴z⁻¹, xzx^{4k+1}z⁻²) for all k ∈ ℤ (Miller–Schupp type, length 13 + \|4k+1\|) | proved (stable), §9 |
| F-exp | V_k is already in AK(3)'s *ordinary* class for k ∈ {−2,…,2} (engine collisions at barriers 16–21, no certificates) | experiment, §9 |

**What one stabilization buys, in one sentence:** all of Aut (hence all "chirality"), all substitutions by
corank-≤1 pairs, and all generator exchanges satisfying one conjugacy condition — but for AK(3) none of the
exits these open (primitive relator, generating triple, factorization into known-trivial pieces, a
presentation of length ≤ 13 outside its class) was reached; one of them is rigorously closed (E3).

Notation: F = F(x,y), X = x⁻¹, Y = y⁻¹; F₃ = F(x,y,z). "~" is ordinary AC equivalence of tuples **in the
stated free group** (inversion, right multiplication by another relator, conjugation by a letter).
U ~₁ V means (U,z) ~ (V,z) in F₃ (one stabilization); U ~_st V: after finitely many stabilizations.

## 1. Previous work read and choice of direction

Read: README (all), notes A–O (status + coordinator reviews; in full N §1, D Lemmas D1–D6, J §3.7/§7, F §2,
L §3.3; skimmed I §5–6, K §3, G §3.2). Facts used: D2 (letterwise automorphic image of an AC sequence is an AC
sequence — valid verbatim in every rank), D3 (primitive relator ⇒ AC-trivial), N1 (Lemma 1.2 of N sketches the
stable Nielsen move for 3-deformations), L §3.3 (length ≤ 13 classification), G2 (no single ACM move from AK(3)
reaches a primitive relator).

**Direction (the TH14 seed, refined).** J §7 item 6 asked for a labelled stable study; N's Lemma 1.2 used
stabilization only as a sketch for 3-deformations. Nobody in A–O worked out *which rank-2 presentations become
equivalent after one stabilization*. I make (a) fully explicit (Theorem A, stronger than asked: the whole of
Aut(F₃) acts trivially on the class of (U,z)), and replace the vague "substitution move" of (b) by an exact
theorem (Theorem B), a rank-free structural statement (B2: composition = disjoint union stably) and the
exact generator-exchange criterion asked for in the seed (Proposition F, §9). (c) is then a finite, checkable
question: is some member of AK(3)'s class a corank-≤1 pair, or a composite W∘P with W, P both known
AC-trivial, or does a generator exchange lead to a short presentation? §5 and §9 test this; the answer within
the bounds is no, and for the standard relators the first exit is closed by a proof (E3). Not duplicated by
the other round-5 seeds as listed in the brief (TH09/TH18 study killers, TH13/TH15 ordinary families).

## 2. Theorem A: the class of (U, z) is Aut(F_{n+1})-invariant (stable; proved here)

**Macro move.** M(i; j, ε, g): r_i ↦ r_i · g r_j^{ε} g⁻¹ (j ≠ i, ε = ±1, g a word). It is a composite of
2|g|+1 (ε = 1) or 2|g|+3 (ε = −1) elementary moves: conjugate r_j letter by letter, (invert), multiply, undo.
**Fact 0.** If w = ∏_{k=1}^{a} g_k r_{j_k}^{ε_k} g_k⁻¹ with all j_k ≠ i, then r_i ↦ r_i w by a macro moves; also
r_i ↦ w r_i = r_i·(r_i⁻¹ w r_i), again a macro moves (conjugators g_k replaced by r_i⁻¹g_k).
Area_U(w) denotes the least such a for a tuple U and w ∈ ⟨⟨U⟩⟩.

**Theorem A.** Let U = (r₁,…,r_n) ⊂ F_n = F(x₁,…,x_n) with ⟨⟨U⟩⟩ = F_n, and U⁺ = (r₁,…,r_n,z) ⊂ F_{n+1} = F_n * ⟨z⟩.
Then θ(U⁺) ~ U⁺ in F_{n+1} for every θ ∈ Aut(F_{n+1}). Explicitly, with A_i = Area_U(x_i) and |U|_{x_i} the
number of letters x_i^{±1} in U:
(i) transposition σ_i = (x_i z): U⁺ → σ_i(U⁺) by 2A_i + |U|_{x_i} macro moves and one inversion;
(ii) ε_z: z ↦ z⁻¹: one inversion; (iii) ρ_i: z ↦ z x_i: A_i macro moves.

*Proof.* S = {θ : θ(U⁺) ~ U⁺} is a subgroup of Aut(F_{n+1}): if θ₁,θ₂ ∈ S, apply θ₁ letterwise to a sequence
θ₂(U⁺) → U⁺ (D2: inversion and multiplication commute with θ₁, conjugation by a letter g becomes conjugation by
the word θ₁(g)), giving θ₁θ₂(U⁺) ~ θ₁(U⁺) ~ U⁺; and applying θ⁻¹ to θ(U⁺) ~ U⁺ gives U⁺ ~ θ⁻¹(U⁺). By Nielsen,
Aut(F_{n+1}) is generated by the permutations of the basis, one inversion and one transvection; the
transpositions σ_i generate all permutations. So (i)–(iii) suffice.
(ii) is one inversion. (iii): x_i ∈ ⟨⟨U⟩⟩, so (U, z) → (U, z x_i) by Fact 0.
(i): (a) (U, z) → (U, z x_i⁻¹) by Fact 0 (x_i⁻¹ ∈ ⟨⟨U⟩⟩; Area(x_i⁻¹) = A_i).
(b) Replace the letters x_i^{±1} of U one at a time: u x_i v ↦ u z v = (u x_i v)·v⁻¹x_i⁻¹(z x_i⁻¹)x_i v and
u x_i⁻¹ v ↦ u z⁻¹ v = (u x_i⁻¹ v)·v⁻¹ (z x_i⁻¹)⁻¹ v: one macro move each with the last relator. Result:
(σ_i(U), z x_i⁻¹). (c) σ_i(U) normally generates σ_i(F_n) ∋ z with Area_{σ_i U}(z) = A_i, so
z x_i⁻¹ ↦ z⁻¹·z x_i⁻¹ = x_i⁻¹ by Fact 0; invert. Result (σ_i(U), x_i) = σ_i(U⁺). ∎

**Corollary A1 (chirality is invisible after one stabilization; stable).** For every φ ∈ Aut(F_n),
(φ(U), z) ~ (U, z) in F_{n+1}; the rank never exceeds n+1 along the sequence. For n = 2 the Nielsen generators
are, as automorphisms of F₃ fixing z: x↔y = σ_xσ_yσ_x; x ↦ x⁻¹ = σ_x ε_z σ_x; x ↦ xy = σ_x ρ_y σ_x
(check: x ↦ z ↦ zy ↦ xy, z ↦ x ↦ x ↦ z). Counts in §2.1.
Consequently N's question "is C4 ~AC φ(C4)?" is a purely *unstable* question: C4 ~₁ φ(C4) always. A proof of
C4 ≁AC φ(C4) would disprove the ordinary conjecture and simultaneously exhibit two ordinary AC classes that
merge after one stabilization; it would say nothing about the stable conjecture.

### 2.1 Explicit sequences and move counts (proved here)

If θ = θ₁θ₂⋯θ_k with every θ_j one of σ_i, ε_z, ρ_i, the proof gives θ(U⁺) → U⁺ as the concatenation of the
image under θ₁⋯θ_{j−1} of the standard sequence for θ_j, j = k,…,1. Images of macro moves are macro moves
(conjugators become their images), so macro counts add. With A_x = Area_U(x), A_y = Area_U(y), |U|_x, |U|_y the
letter counts, for a rank-2 presentation U of the trivial group:

| φ ∈ Aut(F₂) | as product in Aut(F₃) | macro moves for (U,z) ↔ (φU,z) | inversions |
|---|---|---|---|
| x ↔ y | σ_x σ_y σ_x | 4A_x + 2A_y + 2\|U\|_x + \|U\|_y | 3 |
| x ↦ x⁻¹ | σ_x ε_z σ_x | 4A_x + 2\|U\|_x | 3 |
| x ↦ xy | σ_x ρ_y σ_x | 4A_x + A_y + 2\|U\|_x | 2 |

So realizing a Nielsen generator stably costs O(Area_U(x) + Area_U(y) + |U|) macro moves: the only non-explicit
input is a pair of van Kampen diagrams for x and y over U, i.e. a proof that the group is trivial. No bound on
A_x, A_y in terms of |U| is known (or claimed). A machine-checked instance for C4 is in §6.

**Remark (what is and is not new).** That automorphism moves become redundant after stabilization is classical
(Q**-equivalence = 3-deformation; N's Lemma 1.2 sketches it). The points made explicit here are: one
stabilization always suffices and is never exceeded; the *whole* of Aut(F₃), not only Aut(F₂), fixes the
class; and the cost is governed by the areas of the generators.

## 3. Theorem B: the stable substitution theorem (stable; proved here)

For U = (r₁,r₂) and a pair P = (p,q) of words write U∘P = (r₁(p,q), r₂(p,q)) (substitute x ↦ p, y ↦ q).

**Theorem B.** Let U be a balanced presentation of the trivial group on (x,y). Let p,q ∈ F = F(x,y) satisfy
(N) ⟨⟨p,q⟩⟩ = F and (G) ⟨p,q,t⟩ = F for some t ∈ F. Then U∘(p,q) is a balanced presentation of the trivial
group and (U∘(p,q), z) ~ (U, z) in F₃, i.e. U∘(p,q) ~₁ U.

*Proof.* Let π: F₃ → F, x ↦ p, y ↦ q, z ↦ t; it is onto by (G). By Nielsen's reduction theorem a generating
triple of a free group of rank 2 is carried by Nielsen transformations to (x, y, 1) (Lyndon–Schupp I.2.2 and
the fact that bases of F₂ are Nielsen-equivalent); Nielsen transformations of (π(x),π(y),π(z)) are
precompositions of π with automorphisms of F₃. So there is α ∈ Aut(F₃) with π∘α = π₀, where π₀: x ↦ x,
y ↦ y, z ↦ 1. Put γ = α(z); then ker π = α(ker π₀) = ⟨⟨γ⟩⟩.
*Step 1: (U, z) ~ (U, γ).* F₃/⟨⟨U⟩⟩ = ⟨z⟩ ≅ ℤ; let γ ↦ z^k. Then ℤ/k = F₃/⟨⟨U,γ⟩⟩ ≅ F/⟨⟨π(U)⟩⟩ = F/⟨⟨U∘(p,q)⟩⟩.
Since x, y ∈ ⟨⟨U⟩⟩_F, substituting gives p, q ∈ ⟨⟨U∘(p,q)⟩⟩, so ⟨⟨U∘(p,q)⟩⟩ = ⟨⟨p,q⟩⟩ = F by (N). Hence k = ±1,
γ^{±1}z⁻¹ ∈ ⟨⟨U⟩⟩_{F₃}, and Fact 0 (plus possibly one inversion) gives the claim. This also shows that U∘(p,q)
presents the trivial group.
*Step 2.* Apply α⁻¹ letterwise (D2): α⁻¹(U, γ) ~ α⁻¹(U, z) ~ (U, z), the last by Theorem A.
*Step 3.* α⁻¹(U,γ) = (α⁻¹r₁, α⁻¹r₂, z), and π₀(α⁻¹ r_i) = π(r_i) = r_i(p,q): deleting the letters z^{±1} from
α⁻¹(r_i) leaves r_i(p,q). Each deletion is a macro move with the third relator z. So
α⁻¹(U,γ) ~ (U∘(p,q), z). ∎

**Corollary B′ (U = (x,y)).** If (p,q) satisfies (N) and (G), then (p, q, z) is AC-trivial in F₃.
*Direct proof.* With α as above, (A,B,C) = (α⁻¹x, α⁻¹y, α⁻¹z) is a basis of F₃ with A ≡ p, B ≡ q mod ⟨⟨z⟩⟩
(because π₀∘α⁻¹ = π). Insert z-letters: (p,q,z) ~ (A,B,z). In F₃/⟨⟨A,B⟩⟩ = ⟨C⟩ ≅ ℤ
the image of z is C^{±1} because F₃/⟨⟨A,B,z⟩⟩ = F/⟨⟨p,q⟩⟩ = 1; so (A,B,z) ~ (A,B,C^{±1}), a basis, which is
AC-trivial by Nielsen moves. ∎
Conversely (G) is *equivalent* to: p, q are obtained by deleting z from two elements A, B of a basis (A,B,C) of
F₃ (if (A,B,C) is a basis, then (p, q, C|_{z=1}) generates F). So B′ says exactly: **a rank-3 tuple (p,q,z) into
which z-letters can be inserted so that the first two relators become part of a basis is AC-trivial** — the
rank-3 analogue of D3, and the cheapest way one stabilization can trivialize a rank-2 presentation.

**Worked example (hand-checked).** (p,q) = (x²y, x³y²), t = x: γ = y⁻¹zxz⁻²x, basis (α(x),α(y),α(z)) =
(z, z⁻²x, γ), α⁻¹: x ↦ x²y, y ↦ x³y²z⁻¹, z ↦ x; (A,B,C) = (x²y, x³y²z⁻¹, x) is a basis of F₃ and
(x²y, x³y², z) ~ (A,B,z) ~ (A,B,x) since z ≡ x⁻¹ mod ⟨⟨A,B⟩⟩.

**Lemma C (no new primitive exit).** Let H = ⟨p,q⟩ ≤ F be non-cyclic (so free on p,q). If w(p,q) is primitive
in F, then w is primitive in F(x,y). Hence if U∘(p,q) has a primitive relator, U already has one.
*Proof.* Let g = w(p,q), F = ⟨g⟩ * ⟨g′⟩. By the Kurosh subgroup theorem H is the free product of a free group
and of subgroups H ∩ a⟨g⟩a⁻¹, H ∩ b⟨g′⟩b⁻¹ for double-coset representatives a, b, where the representative
of the trivial double coset may be taken to be 1; so H ∩ ⟨g⟩ = ⟨g⟩ is a free factor of H and g is primitive
in H. The isomorphism F(x,y) → H, x ↦ p, y ↦ q carries w to g. ∎

## 4. Theorem B2: composition is disjoint union, stably (stable; proved here)

**Theorem B2.** Let U = (r₁,…,r_n) ⊂ F(x₁..x_n) be a balanced presentation of the trivial group and
P = (p₁,…,p_n) ⊂ F(z₁..z_n) any n-tuple. Then in F_{2n} = F(x,z):
(U(x), P(z)) ~ (U(P(z)), x₁,…,x_n), by 2ΣA_i + |U| macro moves and n inversions (A_i = Area_U(x_i)).
If P also presents the trivial group, then (U∘P(x), z₁,…,z_n) ~ (U(x), P(z)) = U ⊔ P.

*Proof.* (1) p_i(z) ↦ x_i⁻¹p_i(z) by Fact 0 (x_i⁻¹ ∈ ⟨⟨U⟩⟩). (2) Replace every letter x_i^{±1} of U by p_i(z)^{±1}:
u x_i v ↦ u p_i v = (u x_i v)·v⁻¹(x_i⁻¹p_i)v, and u x_i⁻¹ v ↦ u p_i⁻¹ v = (u x_i⁻¹ v)·v⁻¹x_i (x_i⁻¹p_i)⁻¹ x_i⁻¹ v: one macro
move per letter. Now the tuple is (U(P(z)), x_i⁻¹p_i(z)). (3) If x_i = ∏ g_k r_{j_k}^{ε_k} g_k⁻¹ in F(x), then
p_i(z) = ∏ g_k(P) r_{j_k}(P)^{ε_k} g_k(P)⁻¹, so x_i⁻¹p_i ↦ x_i⁻¹ by A_i macro moves; invert. This proves the
first claim (P arbitrary). If P presents the trivial group, so does U∘P (its normal closure in F(z) contains
all p_i by (3)), and V = (U∘P(z), x₁..x_{n−1}) is a balanced presentation of the trivial group on 2n−1
generators; by Theorem A the class of (V, x_n) is Aut(F_{2n})-invariant, in particular under the permutation
x_i ↔ z_i. ∎

**Corollaries (stable).** Let 𝔖 be the set of stable AC classes of balanced presentations of the trivial
group (all ranks); ⊔ makes it a commutative monoid with unit the class of the standard presentation.
(1) [U∘P] = [U] + [P]: composition of presentations of the same rank realizes the sum.
(2) U∘P ~_st P∘U (n stabilizations; proof: (P∘U(x), z) ~ (P(x), U(z)) = s(U(x), P(z)) ~ s(U∘P(x), z) =
(U∘P(z), x) ~ (U∘P(x), z), s the swap x ↔ z, the last step by Theorem A).
(3) If P is stably AC-trivial then U∘P ~_st U for every U (run the trivialization of (P(z), w) inside
F(x,z,w)); Theorem B is the sharp one-stabilization case P = (p,q) of corank ≤ 1.
(4) The stably trivial presentations of rank n form a submonoid of (normally surjective endomorphisms of F_n,
∘) containing Aut(F_n) and, for n = 2, every corank-≤1 pair. The stable AC conjecture in rank n says that
this submonoid is everything.
Consequence for AK(3): any factorization "member of the stable class of AK(3)" = W∘P gives [AK(3)] = [W] + [P];
if W and P are both AC-trivial, AK(3) is stably AC-trivial. §5 looks for such factorizations.

## 5. Exits for AK(3): what the theorems reduce the question to, one rigorous closure, and a bounded search

Two finite tests on a rank-2 pair (a,b) with K = ⟨g a g⁻¹, b⟩ (g a conjugator; conjugating relators is AC):
**E1** (Corollary B′): ⟨K, t⟩ = F for some t ⇒ (a,b) is AC-trivial after one stabilization.
**E2** (Theorems B, B2): a proper rank-2 subgroup H = ⟨p,q⟩ ⊋ K ⇒ (gag⁻¹, b) = W∘(p,q), so
[(a,b)] = [W] + [(p,q)] in 𝔖 provided W presents the trivial group.

**Lemma E1 (both tests are finite; proved here).** Let Γ be the based Stallings graph of K ≠ F (rank 2,
non-cyclic). (i) ⟨K,t⟩ = F for some t iff identifying some two vertices u ≠ v of Γ and folding gives the rose.
(ii) Every rank-2 subgroup H ⊇ K is represented by a folded quotient of Γ (iterated identification of two
vertices followed by folding).
*Proof.* (i) ⇐: t = αβ⁻¹ with α, β labels of paths from the base to u, v. ⇒: write the reduced word t = α t″ β⁻¹
with α the longest prefix readable in Γ from the base (ending at u) and β⁻¹ the longest remaining suffix
readable backwards from the base (starting at v). If t″ ≠ 1, Γ plus an arc u → v labelled t″ is folded (no
letter of the arc is readable at its ends, by maximality), is the Stallings graph of ⟨K,t⟩ and has rank 3,
so ⟨K,t⟩ ≠ F. Hence t″ = 1 and the graph of ⟨K,t⟩ is fold(Γ/(u~v)); u ≠ v as t ∉ K.
(ii) (Takahasi's argument.) The image Δ of Γ → Γ_H is a folded subgraph, so L = π₁(Δ) is a free factor of H
containing K; rank L ≤ 2 and K ≤ L non-cyclic force rank L = 2, so L = H and Γ → Γ_H is onto; an onto
morphism of folded graphs factors through successive single identifications + foldings. ∎

**Lemma C** (§3) shows that E2 can never produce a new primitive relator; what E2 can produce is a
decomposition into two *other* presentations.

### 5.1 Proposition E3: E1 is closed for the standard AK(3) pair, for all conjugators (proved here)

**Proposition E3.** Let r₂ = xyxy⁻¹x⁻¹y⁻¹ and let s₁ ∈ F be any word conjugate to (x³y⁻⁴)^{±1} modulo ⟨⟨r₂⟩⟩
(for example s₁ = x³y⁻⁴, or any ACM replacement of it with the trefoil relator frozen). Then for no
g, h, t ∈ F is ⟨g s₁ g⁻¹, h r₂ h⁻¹, t⟩ = F. So the cheapest stable exit E1 does not apply to AK(3) in standard
form, whatever conjugates of the relators are used.

*Proof.* Let Φ: F → SL₂(ℤ), x ↦ [[1,1],[0,1]], y ↦ [[1,0],[−1,1]]; Φ(xyx) = Φ(yxy) = [[0,1],[−1,0]], so Φ kills
r₂, and Φ is onto. Put ρ = Φ(x³y⁻⁴) = [[13,3],[4,1]], trace 14. For M = [[a,b],[c,d]] let
f_M(X,Y) = det(v, Mv) = cX² + (d−a)XY − bY² (v = (X,Y)ᵗ). Then f_{hMh⁻¹}(v) = f_M(h⁻¹v) for h ∈ SL₂(ℤ),
f_{−M} = −f_M = f_{M⁻¹}; so the property R(M): "f_M represents 1 or −1 over ℤ" is invariant under
SL₂(ℤ)-conjugation, sign change and inversion.
*(a) R(ρ) fails:* f_ρ = 4X² − 12XY − 3Y² takes only the values 0, 4, 5 mod 8 (Y odd: 4X(X−3Y) ≡ 0 and −3Y² ≡ 5;
Y even: ≡ 4X² + 4(Y/2)²).
*(b) Reduction.* Suppose ⟨g s₁ g⁻¹, h r₂ h⁻¹, t⟩ = F. Passing to PSL₂(ℤ) = ⟨s⟩ * ⟨τ⟩ ≅ C₂ * C₃ (s, τ the images
of S = [[0,−1],[1,0]] and ST = [[0,−1],[1,1]]), the images of g s₁ g⁻¹ and t generate (r₂ ↦ 1). By the
Grushko–Neumann theorem applied to the epimorphism F(a,b) → C₂ * C₃, a ↦ [g s₁ g⁻¹], b ↦ [t], there is a
basis (P,Q) of F(a,b) with P ↦ s, Q ↦ τ^{±1}; writing a as a (primitive) word in P, Q shows that the image of
g s₁ g⁻¹ equals A(s,τ) for a primitive word A ∈ F(u,v). Both A(S,ST) and Φ(g s₁ g⁻¹) lift this element, and
Φ(s₁) is conjugate to ρ^{±1} (ker Φ ∋ r₂). So p := A(S, ST) ∈ SL₂(ℤ) is ± an SL₂(ℤ)-conjugate of ρ^{±1}:
|tr p| = 14 and R(p) fails by (a).
*(c) Every primitive image of trace ±14 satisfies R.* Complete A to a basis (A,A′), q = A′(S,ST). Since
[A,A′] is conjugate to [u,v]^{±1} and tr[S,ST] = 3, Fricke's identity tr[p,q] = ξ² + η² + ζ² − ξηζ − 2 gives
ξ² + η² + ζ² − ξηζ = 5 for (ξ,η,ζ) = (tr p, tr q, tr pq). With |ξ| = 14 this forces ξηζ > 0 (otherwise the left
side is ≥ 196), so |η|² + |ζ|² − 14|η||ζ| + 191 = 0. Apply this to all bases (p, pᵏq), k ∈ ℤ: with
t_k = tr(pᵏq) the identity tr(pw) + tr(p⁻¹w) = tr p·tr w gives t_{k+1} + t_{k−1} = ξ t_k, and ξ t_k t_{k±1} > 0,
so β_k = |t_k| ≥ 1 satisfies β_{k+1} + β_{k−1} = 14β_k and β_k² + β_{k+1}² − 14β_kβ_{k+1} + 191 = 0. Let γ = β_k be a
minimum of the sequence and β its smaller neighbour: γ ≤ β ≤ 7γ, so β = 7γ − √(48γ² − 191) ≥ γ, i.e.
12γ² ≤ 191, γ ≤ 3; and 48γ² − 191 is a nonnegative square only for γ = 2 (then β = 13 and the other
neighbour is 15). So q* = pᵏq satisfies |tr q*| = 2 and {|tr pq*|, |tr p⁻¹q*|} = {13, 15}. As q* ≠ ±I it is
parabolic: q* = ±hTᵐh⁻¹ with h ∈ SL₂(ℤ), T = [[1,1],[0,1]], m ≠ 0. Write h⁻¹ph = [[a,b],[c,d]]; then
tr(pq*) = ±(tr p + mc) and tr(p⁻¹q*) = tr(pq*⁻¹) = ±(tr p − mc), so {|14 + mc|, |14 − mc|} = {13, 15} (replace
mc by −mc if tr p = −14), hence |mc| = 1, c = ±1 = f_{h⁻¹ph}(1,0), and R(p) holds.
(b) and (c) contradict each other. ∎

*Remarks.* (1) The argument works modulo the centre of the trefoil group, so it also covers the exotic
(non-standard) Nielsen classes of generating pairs of that group (Dunwoody–Pietrowski; recalled) — this is
why E3 is not a formal consequence of G's Proposition G2(b). (2) It is the stable analogue of G2(b): G2 says
no single ACM move from AK(3) reaches a primitive relator; E3 says no such move (with the trefoil relator
frozen) reaches a pair whose relators extend to a generating triple. (3) Not done: the mirror statement with
x³y⁻⁴ frozen (quotient C₃ * C₄), other n (a finite Vieta computation for each trace n²+n+2), and other
members of the class (§5.2 is only a bounded search).

### 5.2 Bounded search for E1 and E2 in AK(3)'s class (experiment)

`experiments/th14_exits.py` (tools in `th14_stallings.py`; both self-tested, including a positive control: the
composite AK(2)∘(x², yx⁻³) is detected and refactored). Members: the endpoints of all round-1–4
certificates having AK(3) as one endpoint (48 pairs: AK(3) and its signed-permutation images, P₃, the second
length-13 orbit, the Miller–Schupp members certified by D, G's T(2,7) form), taken in both orders. For each
pair (a,b) the subgroups K = ⟨g a g⁻¹, b⟩ are formed for all g in the ball of radius L **and** for all relative
rotations (g = (prefix of b)(prefix of a)⁻¹). E1: all vertex pairs of the Stallings graph (exact, Lemma E1(i)).
E2: the full closure of folded quotients (exact, Lemma E1(ii)) when it has ≤ 1,500 graphs; otherwise only
quotients reachable through graphs of rank ≤ 3 ("pruned", incomplete for that subgroup).

| run (exact command, repository root) | members | subgroups K | E1 hits | E2 hits | pruned |
|---|---:|---:|---:|---:|---:|
| `th14_exits.py 2 --e1only --maxlen 17` (E1 only; ball radius 2 + rotations) | 47 (all of length ≤ 17) | 4,204 | **0** | — | — |
| `th14_exits.py 1 --maxlen 14` (E1 + E2; ball radius 1 + rotations) | 10 (lengths 13, 14) | 606 | 0 | **0** | 0 |
| `th14_exits.py 1 --maxlen 15 --skip 10` (timeout 290 s: 6 members done) | 6 (length 15) | 396 | 0 | **0** | 4 |
| `th14_exits.py 1 --maxlen 15 --skip 16` (timeout 110 s: 1 member done) | 1 (length 15) | 74 | 0 | **0** | 8 |
| `th14_exits.py 1 --maxlen 15 --skip 17` | 1 (length 15) | 74 | 0 | **0** | 4 |

Totals: E1 — 47 members, 4,204 subgroups, 0 hits. E2 — all 18 members of length ≤ 15, 1,150 subgroups,
0 hits, 16 subgroups with pruned closure (so E2 is exhaustive for 1,134 of them). The 48th member (G's T(2,7) form, length 35) was not tested. An earlier,
unfiltered run of the same script (member list then including three round-5 pairs) covered 15 members and
952 subgroups with the same outcome (0 / 0, 2 pruned).

So within these bounds no member of AK(3)'s class is a corank-≤1 pair, and none factors through a proper
rank-2 subgroup. **This is a bounded search over 47 (E1) resp. 18 (E2) known class members and short conjugators; it is not a
proof that the stable exits are closed for the class** (only Proposition E3 is a proof, and only for the
standard relators).

**Why E2 hits are rare (heuristic, not a theorem).** A proper rank-2 overgroup H of K forces the two relator
cycles to fold onto a rank-2 graph with more than one vertex, i.e. long common or periodic subwords in a
suitable relative position; minimal-length class members have little overlap. Composite presentations are
therefore more likely to be found among *long* members, which this light search does not reach.

## 6. A machine-checked instance of Theorem A for C4 (stable; proved here by certificate)

C4 = (x⁴yx⁻¹y, xy³xy⁻²). N proved Ŝ(C4) ⊇ D₆ = ⟨−I, φ₁, φ₂⟩ and that the matrix of ε_y: y ↦ y⁻¹ is *not* in
D₆ (re-checked here: the group generated by N's three matrices has 12 elements, none equal to diag(1,−1)); whether
C4 ~AC ε_y(C4) in rank 2 is open (if not, C4 is a counterexample to the ordinary conjecture).
`certificates/th14_c4_invy_stable1.json` is an explicit rank-3 sequence

  (xxxxyXy, xyyyxYY, z) → (xxxxYXY, xYYYxyy, z) = (ε_y(C4), z),

695 elementary moves (74 macro moves = 4A_y + 2|U|_y with the derivation of y found by the generator:
area 15), peak total length 33, format `stable1-ac-elementary-rank3-v1`, checked by the independent strict
replayer `experiments/th14_verify3.py` (self-test: two replays, nine negative controls). It is produced by
`experiments/th14_cert.py` exactly as in the proof of Theorem A (ε_y = σ_y ε_z σ_y; the generator's best-first
search supplies the expression of y⁻¹ as a product of 15 conjugates of the relators).
**This certificate is a stable statement (one stabilization). It is not an ordinary AC equivalence between C4
and ε_y(C4) and gives no information on whether one exists.**

## 7. Remark: rank reduction by duality (stable; proved here, short)

**Proposition B3.** Let P = (p₁..p_n) be a balanced presentation of the trivial group on x₁..x_n and suppose
⟨p₁,…,p_n,t₁,…,t_k⟩ = F_n. Then P is stably AC-equivalent to a balanced presentation P^∨ of rank k; precisely
(P, z₁..z_k) ~ (P^∨(z), x₁..x_n) in F_{n+k}. For k = 1 this is Corollary B′ in every rank (rank-1 balanced presentations of the trivial group
are (c^{±1})).
*Proof.* As in Theorem B there is α ∈ Aut(F_{n+k}) with π∘α = π₀ (π: x_i ↦ p_i, z_j ↦ t_j; π₀: x_i ↦ x_i,
z_j ↦ 1). Put A_i = α⁻¹(x_i), C_j = α⁻¹(z_j): a basis with A_i ≡ p_i modulo ⟨⟨z⟩⟩, so (P, z) ~ (A, z) by
inserting z-letters. By Theorem A (applied to the presentation (P, z₁..z_{k−1}) and the generator z_k) the
class of (P,z) is Aut(F_{n+k})-invariant, so (A, z) ~ α(A, z) = (x₁..x_n, α(z₁),…,α(z_k)) ~ (x, P^∨(z)) where
P^∨_j is α(z_j) with the x-letters deleted; (x, P^∨(z)) is the n-fold stabilization of P^∨. ∎
(For n = k = 2, t = (x,y), one finds P^∨ = P: no content. The content is for k < n.)

## 8. Failed attempts and what they show

1. *AK(3) stably trivial via E1.* Closed rigorously for the standard relators and all conjugators
   (Proposition E3); no hit for the 47 known class members of length ≤ 17 within §5.2's bounds.
2. *A shorter rank-2 presentation stably equivalent to AK(3) via factorization (E2).* No factorization found
   (§5.2). Substitution U ↦ U∘(p,q) only lengthens, and by Lemma C it never creates a primitive relator; so
   Theorems B/B2 by themselves produce no presentation of length ≤ 13 stably equivalent to AK(3). The length
   ≤ 13 exit of the seed was not reached.
3. *Derivation of x over C4.* The best-first search found y (area ≤ 15) but not x within 1.2·10⁶ nodes at
   length cap 28; x is then obtained from y (x = x³·x⁻² after deleting y's from the relators: area ≤ 107), so
   certificates for automorphisms that need A_x (x ↔ y, x ↦ xy) were not generated — only ε_y, which needs
   A_y alone. This is a cost issue, not an obstruction: Theorem A covers them.
4. *Two stabilizations.* The same basis-completion trick with two new generators is a tautology
   (Proposition B3 with n = k = 2 returns P itself). I found no argument giving more from a second
   stabilization than B2.

## 9. Proposition F: generator exchange — the "subgroup-ACM" move of the seed (stable; proved here)

**Proposition F.** Let U = (r₁, r₂) be a balanced presentation of the trivial group on (x,y),
G₂ = F(x,y)/⟨⟨r₂⟩⟩, w ∈ F(x,y), v ∈ F(x,z).
(i) In the rank-3 triple (r₁, r₂, z⁻¹w) the first relator can be replaced by y⁻¹v(x,z) by AC moves on the
first relator alone (conjugation, inversion, multiplication by conjugates of the other two) **iff**
y⁻¹·v(x, w(x,y)) is conjugate to r₁^{±1} in the one-relator group G₂.
(ii) In that case U ~₁ V := (r₂(x, v(x,z)), z⁻¹·w(x, v(x,z))), a balanced presentation of the trivial group
on (x,z).

*Proof.* (i) F₃/⟨⟨r₂, z⁻¹w⟩⟩ ≅ G₂ via z ↦ w. The moves in question preserve the conjugacy class of the image
of the first relator up to inversion; conversely a word s′ with image conjugate to r̄₁^{±1} equals
g r₁^{±1} g⁻¹·n with n ∈ ⟨⟨r₂, z⁻¹w⟩⟩ and is reached by conjugation, inversion and Fact 0.
(ii) (r₁, r₂, z) ~ (r₁, r₂, z⁻¹w) (Fact 0, w ∈ ⟨⟨U⟩⟩, one inversion) ~ (y⁻¹v(x,z), r₂, z⁻¹w) by (i). Replace
every y^{±1} in r₂ and in w by v(x,z)^{±1} (one macro move with the first relator per letter, as in the proof
of B2): (y⁻¹v, V) with V ⊂ F(x,z). The triple presents the trivial group and y⁻¹v eliminates y, so V presents
the trivial group; hence v ∈ ⟨⟨V⟩⟩, y⁻¹v ↦ y⁻¹ ↦ y (Fact 0, inversion), giving (y, V(x,z)); by Theorem A the
permutation y ↔ z turns this into (V(x,y), z). ∎

If (x,w) is a basis of F(x,y) with inverse substitution y = v₀(x,z), then V is one ACM move away from an
automorphic image of U (ordinary, given Aut-closure). The genuinely stable instances are those where x and w
generate only *modulo the relators* (with exactly one use of r₁, up to conjugacy in G₂).

**Application to AK(3) (stable; proved).** Take r₁ = xyxy⁻¹x⁻¹y⁻¹, r₂ = x³y⁻⁴; in G₂ = ⟨x,y | x³ = y⁴⟩ the
element x³ = y⁴ is central. For w = x^{3i+1}y^{4j+1} and v = zxz⁻¹: y⁻¹·wxw⁻¹ = y⁻¹(xy)x(xy)⁻¹ in G₂, a cyclic
rotation of r₁. Hence for all i, j ∈ ℤ

  AK(3) ~₁ V_{i,j} = (x³zx⁻⁴z⁻¹, x^{3i+1} z x^{4j+1} z⁻²),

i.e. the Miller–Schupp-type presentations ⟨x,z | z⁻¹x³z = x⁴, z² = x^{3i+1}zx^{4j+1}⟩. Since x^{3i}z ≡ zx^{4i}
modulo the first relator, V_{i,j} ~AC V_{0,i+j} by one *ordinary* ACM move, so this is a one-parameter
family V_k = (x³zx⁻⁴z⁻¹, xzx^{4k+1}z⁻²), k ∈ ℤ, |V_k| ≥ 14. The same computation gives, for every n,
AK(n) ~₁ (xⁿzx^{−(n+1)}z⁻¹, xzx^{(n+1)k+1}z⁻²).

**Test (experiment, D's engine `d_acsearch`, full cyclic-product graph, several sources).** Forward sets of
V_{0,0}, V_{−1,0}, V_{0,−1}, V_{−1,−1}, V_{1,0}, V_{2,0}, V_{−2,0} (y written for z) and of AK(3) share states
at barriers 16–21 (caps 19–22; e.g. `d_acsearch --source xxxyXXXXY,xyxYY --source xxxYYYY,xyxYXY --cap 19`:
"COLLISION 0-1 barrier 19"; no trivializing state in any run). A common forward state is an ordinary AC
equivalence (every cyclic product is an AC composite), so **V_k is already in AK(3)'s ordinary AC class for
k ∈ {−2,…,2}** (engine-level; no certificates were generated in this session). So this natural family gives
no stable shortcut: it leads back into AK(3)'s ordinary class, at lengths ≥ 14. Whether V_k ~AC AK(3) for
all k by a uniform ordinary argument is open here (stably it is Proposition F).

## 10. Honest limits

- Everything proved here is **stable** (rank 3, or rank 2n for B2) except Lemma C, Lemma E1 and the
  SL₂(ℤ) part of Proposition E3, which are statements about subgroups of free groups / matrices. Nothing here
  is an ordinary AC result about AK(3), C4 or the conjecture, and the stable status of AK(3) remains open.
- Theorems A and B2 are classical in content (stable equivalence absorbs automorphisms; sums of
  presentations); I could not consult the literature (Hog-Angeloni–Metzler, Metzler, Myasnikov) in this
  session. Theorem B/B′, Proposition B3, E3 and F may also be known. No novelty is claimed.
- §5.2 is a bounded search over 47 (E1) resp. 18 (E2) known class members with short conjugators; 16
  subgroups had their quotient closure pruned. It does not show that AK(3)'s class has no corank-≤1 member or no composite member.
- The V_k ~AC AK(3) statements of §9 rest on engine collisions (D's engine, J's directedness caveat does not
  matter for a common forward state), not on stored certificates.
- Externally recalled and not re-proved: Nielsen reduction of generating tuples, Grushko–Neumann, Kurosh,
  Fricke's trace identity, PSL₂(ℤ) ≅ C₂ * C₃, the normal form of parabolics in SL₂(ℤ), Takahasi's theorem
  (its two-line proof is included), Dunwoody–Pietrowski (used only in a remark).
- The move counts of Theorem A depend on areas of the generators, for which no a-priori bound exists.

## 11. Advice to the coordinator (ranked)

1. **Record the dichotomy for the chirality programme (N).** By Corollary A1, C4 ~₁ φ(C4) for every φ, with
   an explicit certificate for φ = ε_y. So any invariant separating C4 from φ(C4) must fail to be invariant
   under one stabilization; in particular it cannot be a function of the stabilized tuple's AC class, of
   the Q**-class, or of any rank-3 datum. This sharpens N1 and should be quoted wherever the C4 route is
   described; a successful separation would be a *stable/unstable separation theorem*, not only a
   counterexample.
2. **Stable AK(3): the cheap exits are exhausted.** E1 is closed for the standard form (E3) and for all 47
   short known members within the bounds; substitution creates no primitive exits (Lemma C); the natural
   generator exchanges (Prop. F) return into AK(3)'s ordinary class. A serious stable attack now needs a
   genuine rank-3 search engine (D's engine generalized to three relators with a primitive-in-F₃ exit and
   elimination). Lemma E1 and Prop. F give the two exit tests such an engine should run at every state.
3. **Possible follow-ups (theory, cheap):** (a) E3 for the mirror side (x³y⁻⁴ frozen; C₃ * C₄, traces in
   ℤ[√2]) and for general n; (b) a uniform ordinary proof of V_k ~AC AK(n) (would turn §9 into an ordinary
   one-parameter family, in the style of K1); (c) decide whether corank-≤1 normally generating pairs are
   always *ordinarily* AC-trivial — if not, they are counterexamples that die after one stabilization.
4. **Do not** use any statement of this note as an ordinary AC result; the verifier `th14_verify3.py` is for
   rank-3 certificates only and reports `"stable1": true` exactly when the certificate proves a
   one-stabilization equivalence of two rank-2 presentations.

## 12. Files written and reproduction (all executed in this session; repository root)

- `research/research-th14.md` (this note).
- `experiments/th14_verify3.py` — strict rank-3 replayer. `python3 experiments/th14_verify3.py --selftest` →
  "self-test: two exact replays and nine negative controls passed".
- `experiments/th14_cert.py` — generator for Theorem A certificates (ε_y). `python3 experiments/th14_cert.py
  --selftest` → "th14_cert self-test passed (AK(2): 193 moves)";
  `cd experiments && python3 th14_cert.py invy xxxxyXy xyyyxYY ../certificates/th14_c4_invy_stable1.json`
  (≈ 15 s) → "moves 695 macro 74 area_y 15".
- `certificates/th14_c4_invy_stable1.json` (26 kB). `python3 experiments/th14_verify3.py
  certificates/th14_c4_invy_stable1.json` → `{"endpoint": ["xxxxYXY", "xYYYxyy", "z"], "moves": 695, …,
  "peak_total_length": 33, "stable1": true}`.
- `experiments/th14_stallings.py`, `experiments/th14_exits.py` — Stallings-graph tools and the exit scan
  (`--selftest` for both; scan commands in §5.2, each ≤ 290 s on one core, < 100 MB).
- §9 engine runs (D's binary `d_acsearch`, built from `experiments/d_acsearch.cpp`; each < 5 s):
  `d_acsearch --source xxxyXXXXY,xyxYY --source xxxYYYY,xyxYXY --cap 19` → "COLLISION 0-1 barrier 19";
  `d_acsearch --source xxxyXXXXY,XXyxYY --source xxxyXXXXY,xyXXXYY --source xxxyXXXXY,XXyXXXYY --source
  xxxYYYY,xyxYXY --cap 21 --no-stop` → collisions 0-1 (16), 0-2 (19), 1-3 (17);
  `d_acsearch --source xxxyXXXXY,xxxxyxYY --source xxxyXXXXY,xxxxxxxyxYY --source xxxyXXXXY,XXXXXyxYY
  --source xxxYYYY,xyxYXY --cap 22 --no-stop` → collisions 0-1 (21), 0-3 (20), 2-3 (19);
  "trivializing_states 0" in all three.

## References (all recalled from memory or via earlier notes; none consulted in this session)

- J. Nielsen (1921/1924) and Lyndon–Schupp, *Combinatorial Group Theory*, I.2 (Nielsen reduction), III.3
  (Grushko–Neumann, Kurosh).  M. Takahasi (1951), overgroups of f.g. subgroups of free groups; J. Stallings
  (1983), foldings.
- C. Hog-Angeloni, W. Metzler (eds.), *Two-dimensional homotopy and combinatorial group theory* (Q**-moves,
  stabilization).  M. J. Dunwoody, A. Pietrowski, *Presentations of the trefoil group* (1973).
- R. Fricke / F. Klein (trace identities in SL₂).  Earlier notes of this repository: D (D2, D3, D6), G (G2),
  I (Prop. C), J (§7), L (§3.3), N (N1, Ŝ(C4) ⊇ D₆).

## Coordinator's check (2026-11-09, Los Angeles time)

**This agent stopped at about 04:56–04:57 UTC because the session's model ran out of usage credits, shortly before its deadline and before handing back a final report.** The text above is its last saved version; it already contained a status line, the honest-limits and advice sections, the list of files and the references, so it is published as written. The coordinator did not edit it.

- Mechanical checks re-run by the coordinator: every self-test shipped with this note passes, and every certificate `certificates/<this agent's id>_*.json` in format `ordinary-ac-elementary-v1` replays under `python3 experiments/elementary_verify.py` (certificates in other formats, if any, are not AC trivializations and are labelled by the note itself).
- The proofs were **not** re-derived by the coordinator except where stated below; for independent verdicts on the central claims see the referee notes research-th19.md (TH01–TH09) and research-th20.md (TH10–TH18), which were completed after the same interruption.
- All statements in this note are about **stable** AC equivalence (one or more extra generators) unless explicitly marked *ordinary*; the certificate `certificates/th14_c4_invy_stable1.json` is in the note's own rank-3 format `stable1-ac-elementary-rank3-v1`, replayed by `experiments/th14_verify3.py` (self-test passes), and is not an ordinary AC certificate. Theorem A (after one stabilization every AC class is invariant under all automorphisms) is classical in content, as the note says; it does not bear on the ordinary question for C4.
- **Referee findings (research-th20.md).** Claims A, B, B2, E3, F verified (all stable, labelled so). Minor: the claims table omits the hypothesis "⟨p,q⟩ non-cyclic" of Lemma C (the lemma itself states it). The experimental statement F-exp (the words V_k lie in AK(3)'s *ordinary* class) has no certificate and is unverified.
