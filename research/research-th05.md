# Research TH05: just-obstructing quotients II — the abelian-cokernel criterion, lifting through every solvable normal subgroup, and the just-non-abelian residual

Date: 2026-11-09 (Los Angeles). Independent research agent TH05 (round 5, theory round).

**Status (written incrementally).** Obstruction-side structure theorems with complete proofs. **No AC trivialization of AK(3), no proof of non-triviality, no counterexample, nothing on the full conjecture.** Every statement is labelled *proved here*, *externally reported*, *experiment* or *open*. No novelty claim is made (literature access: none in this session).

| # | statement | label |
|---|---|---|
| T1 | **Abelian-cokernel criterion.** If some pair (s,t) in the Q-class of π(U) has Q/⟨⟨s⟩⟩ or Q/⟨⟨t⟩⟩ abelian, then Q does not obstruct U. (H's Theorem 1 is the case "cokernel trivial".) | proved here (§2) |
| T2 | **Lifting through every solvable or finite normal subgroup.** If N ⊴ Q is central, abelian, solvable or finite (or a directed union / finite Q-invariant series of such), then Q obstructs U iff Q/N does. H's condition "modulo N ∩ [Q,Q]" is removed for pairs coming from F. | proved here (§3) |
| C2 | Fibre products carry nothing over **any** base: H ×_{H_ab} ℤ² obstructs U iff H does (H's Theorem 5 was the case H finite; H §6 and N §2.5(a) listed the infinite case at the standard pair as open). | proved here (§3) |
| C3 | A just-obstructing quotient has **no nontrivial abelian, solvable or finite normal subgroup**, trivial centre, no minimal normal subgroup at all, and is ICC. | proved here (§3) |
| T3 | **Just-non-abelian residual.** g ∈ Q has abelian cokernel iff g survives in every just-non-abelian (JNA) quotient of Q. With Φ_P(Q) the intersection of the kernels of the JNA quotients with perfect monolith: Q obstructs U iff Q/Φ_P(Q) does. A just-obstructing quotient is a subdirect product of infinitely many JNA groups G with perfect monolith [G,G], C_G([G,G]) = 1; a group with only finitely many such quotients obstructs nothing. | proved here (§4) |
| T4 | Classes excluded: just-non-solvable groups; just-infinite and just-non-(virtually solvable) groups unless they are subdirect products of infinitely many **finite** JNA groups with perfect monolith (so residually finite); groups all of whose weight-one quotients are abelian (e.g. all proper quotients nilpotent). | proved here (§5) |
| T5 | SL_n(ℤ), n ≥ 3, and all its quotients obstruct nothing; in SL_n(ℤ) all normally generating pairs are AC-equivalent. | proved here modulo Mennicke's theorem (externally reported) (§6) |
| T6 | SL₂(ℤ[1/p]) and PSL₂(ℤ[1/p]) (the candidate proposed in H §7.2) obstruct nothing. | proved here modulo Serre's congruence subgroup theorem and the normal subgroup property (externally reported) (§6) |
| — | Hyperbolic quotients and residually finite just-obstructing quotients: not excluded; exact reasons in §7. | open, with reasons |

## 0. Previous work read and choice of direction

Read: `README.md` in full; research-h in full (including the coordinator's review); research-n §2 and its review; research-e §2–4; the status paragraphs and coordinator reviews of the other notes A–O; the opening lines of the parallel drafts TH02, TH06–TH09 (to avoid overlap). Facts used below, re-derived where they carry weight: E's Fact 1 (AC paths push forward to quotients); H's Lemma 2.1 and Theorem 2(i) (errors in [N,Q] are removable for abelian N — I rechecked both correction identities, see §3); H's Theorem 2(ii) with the coordinator's corrected hypothesis (only the consequence "Q obstructs U iff Q/N does" is used); H's Theorem 4 (Zorn existence of just-obstructing quotients; chains).

**Direction.** The seed asks which classes of groups can be the home of an obstruction. I looked for the mechanism behind H's Theorem 1 and Lemma 2.2 and found that the right hypothesis is not "a coordinate normally generates Q" but "a coordinate has *abelian cokernel*": then the unimodularity of exponent matrices does the rest (Theorem 1). This single observation (i) removes the restriction N ∩ [Q,Q] in H's abelian lifting, hence disposes of all central extensions and fibre products, the one case H and N left open on the one-pair side; (ii) turns "abelian cokernel" into a residual condition over just-non-abelian quotients, which gives a clean structure theorem for just-obstructing quotients and answers parts (i)–(iii) of the seed; (iii) applies to concrete groups with the normal subgroup property. It is new relative to A–O (H's Theorem 1 needs Q_ab cyclic; H's Theorem 2(i) stops at N ∩ [Q,Q]) and disjoint from the other seeds (TH01 treats the *two-pair* abelian lifting problem, which this note does not solve: see §8).

## 1. Conventions

As in research-h. F = F(x,y); π: F → Q an epimorphism, a = π(x), b = π(y); U a pair normally generating F; e(w) ∈ ℤ² the exponent vector; the exponent matrix of a pair has rows e(u₀), e(u₁). AC moves in Q: inversion of a coordinate, multiplication of a coordinate by the other one or its inverse, conjugation of a coordinate by an arbitrary element of Q, swap. "Multiply a coordinate by an element of the normal closure of the other" is a composite of such moves. Q **obstructs** U if π(U) ≁_Q (a,b). ⟨⟨g⟩⟩ is the normal closure in Q.

**Definition.** The *cokernel* of g ∈ Q is Q/⟨⟨g⟩⟩; g is **co-abelian** if its cokernel is abelian, i.e. [Q,Q] ⊆ ⟨⟨g⟩⟩. Examples: a and b are co-abelian (their cokernels are cyclic); π(p) is co-abelian for every primitive p ∈ F; a normal generator is co-abelian.

**Lemma 0 (proved; E's Fact 1 read backwards).** Every pair (s,t) ~_Q π(U) is π(V) for some V ~ U in F. Hence V has a unimodular exponent matrix M_V, and there is a basis (p,q) of F with e(p) = e(v₀), e(q) = e(v₁); then π(p) ≡ s and π(q) ≡ t modulo [Q,Q].
*Proof.* Apply the moves of a Q-path from π(U) to (s,t) to U in F, lifting each conjugator through π. AC moves preserve |det| of the exponent matrix, and M_U ∈ GL₂(ℤ) because U normally generates F. Aut(F) → GL₂(ℤ) is onto, so M_V is the exponent matrix of a basis (p,q); p v₀⁻¹ and q v₁⁻¹ lie in [F,F]. ∎

## 2. Theorem 1: the abelian-cokernel criterion (proved here)

**Theorem 1.** Let (s,t) ~_Q π(U). If s or t is co-abelian in Q, then π(U) ~_Q (a,b): Q does not obstruct U.

*Proof.* By symmetry (swap) let s be co-abelian, and let V, (p,q) be as in Lemma 0.
1. t⁻¹π(q) ∈ [Q,Q] ⊆ ⟨⟨s⟩⟩, so (s,t) ~ (s, π(q)).
2. Q/⟨⟨π(q)⟩⟩ is a quotient of F/⟨⟨q⟩⟩ ≅ ℤ (q is primitive), hence abelian: [Q,Q] ⊆ ⟨⟨π(q)⟩⟩. As s⁻¹π(p) ∈ [Q,Q], (s, π(q)) ~ (π(p), π(q)).
3. (p,q) is a basis of F, so Nielsen moves (which are AC moves) take (p,q) to (x,y); applying them in Q gives (π(p),π(q)) ~ (a,b). ∎

*Pair-level form (proved the same way).* If (s,t) normally generates Q, its image in Q_ab² is Nielsen-equivalent to that of (a,b), and s or t is co-abelian, then (s,t) ~_Q (a,b). (Take (p,q) = ν(x,y) for the Nielsen transformation ν realizing the equivalence in Q_ab.)

**Corollary 1.1 (proved).** If Q = F/N obstructs U, then for every pair (c,w) ~ U in F the two groups F/N⟨⟨c⟩⟩ and F/N⟨⟨w⟩⟩ are **nonabelian** (H's Corollary 1.1 said: nontrivial). Each is normally generated by one element (the image of the other coordinate). Equivalently: [F,F] ⊄ N⟨⟨c⟩⟩ for every class coordinate c of U.

**Corollary 1.2 (proved).** If every quotient of Q that is normally generated by a single element is abelian — for instance if all proper quotients of Q are nilpotent (a nilpotent group with cyclic abelianization is cyclic) — then Q obstructs nothing. This covers every just-infinite p-group that is a quotient of F (e.g. the 2-generated Gupta–Sidki groups); for such groups the statement is externally reported in a different form (Myropolska, cited in research-h).
*Proof.* For π(U) = (s,t): if t = 1 then s is a normal generator; otherwise Q/⟨⟨t⟩⟩ is a quotient normally generated by the image of s, hence abelian. Apply Theorem 1. ∎

*Remark (the case Q = F).* The co-abelian elements of F are exactly the primitive elements and the conjugates of [x,y]^{±1} (Magnus: ⟨⟨g⟩⟩ = ⟨⟨h⟩⟩ forces g conjugate to h^{±1}; a 2-generator one-relator group with torsion has Euler characteristic −1 + 1/k ≠ 0, so is not abelian). A class coordinate has a primitive exponent vector, so for Q = F Theorem 1 is the classical "a primitive relator trivializes". The content of Theorem 1 is for proper quotients.

## 3. Theorem 2: obstruction lifts through every solvable or finite normal subgroup (proved here)

**Theorem 2.** Let N ⊴ Q. In each of the following cases, Q obstructs U iff Q/N obstructs U.
(a) N is central in Q. (b) N is abelian. (c) N is solvable. (d) N is finite. (e) N has a finite series 1 = N₀ ≤ N₁ ≤ … ≤ N_k = N of Q-normal subgroups with every factor abelian or finite, or N is a directed union of Q-normal subgroups N_i for each of which the equivalence holds.

*Proof.* "Q/N obstructs ⇒ Q obstructs" is E's Fact 1. For the converse assume Q/N does not obstruct U.
(a) Lift a path of Q/N to Q: π(U) ~_Q (a z₀, b z₁) with z₀, z₁ ∈ N central. The cokernel Q/⟨⟨a z₀⟩⟩ is generated by the images ā, b̄, and ā = z̄₀⁻¹ is central in it; a group generated by a central element and one more element is abelian. So a z₀ is co-abelian and Theorem 1 applies.
(b) Put Q₁ = Q/[N,Q]. N₁ = N/[N,Q] is central in Q₁ and Q₁/N₁ = Q/N, so Q₁ does not obstruct U by (a). Lift to Q: π(U) ~_Q (a n₀, b n₁) with n₀, n₁ ∈ [N,Q]. By H's Lemma 2.1, (a n₀, b n₁) ~ (a,b). (I re-derived its two identities with n·g := g⁻¹ng: conjugating coordinate 0 by m ∈ N turns a n₀ into a(n₀ + m(1−a)); "multiply by coordinate 1, conjugate by m, multiply by its inverse" turns it into a(n₀ + m·b⁻¹ − m·a) and leaves coordinate 1 fixed; these span N(a−1) + N(b−1) = [N,Q].)
(c) The derived series of N consists of Q-normal subgroups; apply (b) to N^{(i)}/N^{(i+1)} ⊴ Q/N^{(i+1)} for i = d−1, …, 0.
(d) Induction on |N|. A minimal normal subgroup M of Q inside N exists. If M is abelian use (b); if not, use H's Theorem 2(ii) ("Q obstructs U iff Q/M does"). Then N/M ⊴ Q/M is smaller.
(e) Series: induct using (b), (d). Directed union: a path in Q/N lifts to a path in Q whose two endpoint errors lie in N, hence in one N_i; so Q/N_i does not obstruct, hence neither does Q. ∎

*Remark (transfinite form).* By transfinite induction (successor steps by (b), (d); limit steps by the directed-union argument) the same holds for an ascending normal series of any ordinal length with abelian or finite factors. So hyper-(abelian or finite) quotients obstruct nothing, and in general Q obstructs U iff Q/R(Q) does, where R(Q) is the largest normal subgroup carrying such a series.

*What is new relative to H.* H's Theorem 2(i) reads "Q obstructs U iff Q/(N ∩ [Q,Q]) does" and H's Lemma 2.2 treats central errors only inside [Q,Q]; the remaining piece N/(N ∩ [Q,Q]) is central, and was "the only kernel that survives" (H §7.1). Part (a) removes it. The reason is that H worked at the level of arbitrary pairs of Q, where a central error outside [Q,Q] changes the abelianization; for pairs that come from F (or, at pair level, pairs whose abelianization is Nielsen-equivalent to the standard one) Lemma 0 absorbs it. Pair-level form of (a)–(d): if Q/N has H's property (AC), so has Q.

**Corollary 2.1 (central extensions and fibre products; proved).** For every K ⊴ F: F/[K,F] obstructs U iff F/K does, and F/[K,K] obstructs U iff F/K does. In particular for every quotient H = F/K, the fibre product Q_H = H ×_{H_ab} ℤ² = F/(K ∩ [F,F]) obstructs U iff H does (its kernel onto H is central because [K,F] ⊆ K ∩ [F,F]). Moreover, in H's notation, Λ_H = Γ at the standard pair for **every** H: every matrix M ∈ GL₂(ℤ) fixing (ā,b̄) ∈ H_ab² is the monodromy of an AC loop at (a,b) in H. (Proof: the pair P with H-components (a,b) and ℤ²-components the rows of M lies in Q_H², has the form (a z₀, b z₁) with z_i central, and its abelianization M is unimodular; by the pair-level form of Theorem 1, P ~ (a,b) in Q_H, and the H-component of such a path is a loop at (a,b) with monodromy M⁻¹.) This settles, on the one-pair side, the case listed as open in H §6 ("central kernels outside [Q,Q] over infinite Q/N") and makes H §7.2's proposal (fibre products over SL₂(ℤ), B₃, triangle groups, PSL₂(ℤ[1/2])) equivalent to asking whether the base itself obstructs. It does **not** touch N's two-pair problem, where the base pair only normally generates (§8).

**Corollary 2.2 (just-obstructing quotients; proved).** Let Q be just-obstructing for U (H's Theorem 4). Then:
(a) Q has no nontrivial abelian normal subgroup; in particular Z(Q) = 1.
(b) Q has no nontrivial solvable normal subgroup and no nontrivial finite normal subgroup.
(c) Q has no minimal normal subgroup at all.
(d) Q is ICC (every nontrivial conjugacy class is infinite).
*Proof.* (a), (b): otherwise Theorem 2 gives a proper obstructing quotient. (c): a minimal normal subgroup is abelian, or nonabelian (H's Theorem 2(ii)). (d): if g ≠ 1 has finitely many conjugates g₁,…,g_r, then L = ⟨⟨g⟩⟩ = ⟨g₁,…,g_r⟩ and ⋂C_Q(g_i) has finite index in Q, so Z(L) has finite index in L. Z(L) is characteristic in L, hence an abelian normal subgroup of Q: if Z(L) ≠ 1 this contradicts (a), and if Z(L) = 1 then L is a nontrivial finite normal subgroup, contradicting (b). ∎

This sharpens H's Theorem 4(b)–(d) (there: abelian normal subgroups meet [Q,Q] trivially, hence are central and embed in Q_ab; minimal normal subgroups are central of prime order). TH08's audit remarks that H §7.1's phrase "a group with no minimal normal subgroups" was stronger than what H proved; (c) proves it.

**Corollary 2.3 (closure; proved).** The class of quotients of F that obstruct nothing is closed under extensions with solvable or finite *kernel* (N solvable or finite, Q/N obstructs nothing ⇒ Q obstructs nothing), and under passing to quotients. Whether it is closed under finite-index overgroups or subgroups is not addressed here.

## 4. Theorem 3: the just-non-abelian residual (proved here)

**Definition.** A group G is **just-non-abelian (JNA)** if it is nonabelian and every proper quotient of G is abelian.

**Lemma 4.1 (proved; elementary).**
(i) G is JNA iff G is nonabelian and M := [G,G] is contained in every nontrivial normal subgroup of G (so M is the unique minimal normal subgroup, the monolith).
(ii) Either M is abelian (**solvable type**: G is metabelian), or M is nonabelian; then M is perfect and C_G(M) = 1 (**perfect type**, "JNA-P").
(iii) If Q is generated by two elements a, b and Q/N is nonabelian, there is N' ⊇ N, N' ⊴ Q, with Q/N' JNA. The same holds for every finite Q.
(iv) For Q as in (iii): g ∈ Q is co-abelian iff g ∉ N for every N ⊴ Q with Q/N JNA.
*Proof.* (i) If G is JNA and 1 ≠ K ⊴ G then G/K is abelian, so M ⊆ K; and M ≠ 1. The converse is clear. (ii) If M is nonabelian, [M,M] is a nontrivial normal subgroup of G, so it contains M; and C_G(M) is normal, so if nontrivial it contains M, making M abelian. (iii) Q/N' is abelian iff c := [a,b] ∈ N'. The normal subgroups containing N and not c are closed under unions of chains; a maximal one N' (Zorn) has the property that every normal subgroup properly containing it contains c, i.e. every proper quotient of Q/N' is abelian, while Q/N' is not. For finite Q take N' maximal among normal subgroups containing N with nonabelian quotient. (iv) If the cokernel of g is nonabelian, (iii) gives N' ⊇ ⟨⟨g⟩⟩ with Q/N' JNA. Conversely if g ∈ N with Q/N JNA then Q/⟨⟨g⟩⟩ maps onto the nonabelian group Q/N. ∎

So "co-abelian" is to JNA quotients what "normal generator" is to simple quotients. Define (an empty intersection is Q)

    Φ(Q) := ⋂ {N ⊴ Q : Q/N is JNA},     Φ_P(Q) := ⋂ {N ⊴ Q : Q/N is JNA of perfect type}.

**Theorem 3.** Q obstructs U ⇔ Q/Φ(Q) obstructs U ⇔ Q/Φ_P(Q) obstructs U.
*Proof.* Only "⇐ fails to obstruct" needs proof. (1) Suppose Q/Φ(Q) does not obstruct. Lift: π(U) ~_Q (a k₀, b k₁) with k_i ∈ Φ(Q). The element a is co-abelian, so by Lemma 4.1(iv) a ∉ N for every JNA kernel N; as k₀ ∈ N, also a k₀ ∉ N. Hence a k₀ is co-abelian and Theorem 1 applies. (2) Let Φ_S be the intersection of the JNA kernels of solvable type, so Φ = Φ_S ∩ Φ_P. Then Φ_P/Φ ≅ Φ_PΦ_S/Φ_S embeds in Q/Φ_S, which embeds in a product of metabelian groups. So Φ_P/Φ is a solvable normal subgroup of Q/Φ and Theorem 2(c) gives: Q/Φ obstructs U iff Q/Φ_P does. ∎

**Corollary 3.1 (finitely many perfect-type JNA quotients; proved).** If Q has only finitely many normal subgroups N with Q/N JNA of perfect type, then Q obstructs nothing.
*Proof.* Let 𝒮_r be the class of groups that are subdirect products of an abelian group A and r JNA-P groups G₁,…,G_r. Q/Φ_P(Q) ∈ 𝒮_r for some r; I show by induction on r that a quotient Q̄ ∈ 𝒮_r of F obstructs nothing. r = 0: abelian. Let r ≥ 1, with kernels N₀ (to A), N₁,…,N_r, ⋂N_i = 1. If K := ⋂_{i≠1} N_i = 1, then Q̄ ∈ 𝒮_{r−1}. Otherwise K ∩ N₁ = 1, so K maps isomorphically onto a nontrivial normal subgroup of G₁, which contains the monolith M₁; let M ≤ K be the preimage of M₁. M is nonabelian, and it is a minimal normal subgroup of Q̄ (a nontrivial Q̄-normal subgroup of M maps onto a nontrivial G₁-normal subgroup of M₁, i.e. onto M₁). By H's Theorem 2(ii), Q̄ obstructs U iff Q̄/M does; and Q̄/M embeds subdirectly in (A × G₁/M₁) × G₂ × … × G_r with first factor abelian, so Q̄/M ∈ 𝒮_{r−1}. ∎

**Corollary 3.2 (just-obstructing quotients are residually JNA-P; proved).** Let Q be just-obstructing for U. Then Φ_P(Q) = 1: Q is a subdirect product of JNA groups G_i with perfect monolith M_i = [G_i,G_i], C_{G_i}(M_i) = 1 and G_i/M_i abelian; none of the G_i is Q itself. Moreover every nontrivial normal subgroup K of Q has nontrivial image in **infinitely many** of them.
*Proof.* Φ_P(Q) ≠ 1 would give a proper obstructing quotient (Theorem 3). Q is not JNA (Corollary 2.2(c)). Suppose K ≠ 1 survives only in G₁,…,G_r (r ≥ 1 because Φ_P = 1), with kernels N₁,…,N_r; then K ∩ N₁ ∩ … ∩ N_r lies in every JNA-P kernel, so it is trivial. Take I ⊆ {1,…,r} minimal with K ∩ ⋂_{i∈I} N_i = 1 and j ∈ I; then K_j := K ∩ ⋂_{i∈I∖{j}} N_i ≠ 1 and K_j ∩ N_j = 1, and as in the proof of 3.1 the preimage in K_j of the monolith of G_j is a nonabelian minimal normal subgroup of Q, contradicting Corollary 2.2(c). ∎

*Reading.* The possible "atoms" of an obstruction are exactly the JNA groups of perfect type; no single one, and no finite collection, carries anything — an obstruction can only live in the way infinitely many of them are glued. For finite G of this type, M = Lᵏ with L nonabelian simple and Lᵏ ≤ G ≤ Aut(Lᵏ) with G/Lᵏ abelian. F itself is residually (finite simple), so all of this is consistent with F being the only obstructing quotient, or with none existing.

## 5. Theorem 4: classes of quotients that are excluded (proved here)

**Lemma 5.1.** A virtually solvable JNA group G of perfect type is finite. If G is finite of perfect type, then M = [G,G] ≅ Lᵏ with L nonabelian simple, G permutes the k factors transitively, and Lᵏ ≤ G ≤ Aut(Lᵏ) = Aut(L) ≀ S_k with G/Lᵏ abelian.
*Proof.* Let R ⊴ G be solvable of finite index. R ∩ M is a solvable normal subgroup of G; if nontrivial it contains the monolith M, which is perfect and nontrivial — impossible. So [R,M] ⊆ R ∩ M = 1 and R ⊆ C_G(M) = 1. The second statement is the structure of a minimal normal subgroup of a finite group together with C_G(M) = 1. ∎

**Theorem 4.** Let Q be a quotient of F.
(a) (*just-non-solvable*) If every proper quotient of Q is solvable, Q obstructs nothing.
(b) (*just-infinite; just-non-(virtually solvable)*) Suppose every proper quotient of Q is virtually solvable (e.g. Q just-infinite). If Q obstructs some U, then Q is just-obstructing for U and Q is a subdirect product of **infinitely many finite** JNA groups of perfect type (Lemma 5.1), each nontrivial normal subgroup of Q surviving in infinitely many of them. In particular Q is residually finite, and Q obstructs nothing if it has only finitely many quotients G with Lᵏ ≤ G ≤ Aut(Lᵏ), G/Lᵏ abelian — for instance if all finite quotients of Q are solvable.
(c) (*weight-one quotients abelian*) Corollary 1.2.
(d) (*solvable or finite radical*) Q obstructs U iff Q/R(Q) does (Theorem 2 and the remark after it); so only groups without nontrivial abelian or finite normal subgroups need to be considered at all.
*Proof.* (a) If Q is solvable use Theorem 2(c). Otherwise a JNA quotient of perfect type is non-solvable, so it can only be Q itself: at most one such kernel, and Corollary 3.1 applies. (b) Proper quotients do not obstruct (H's Corollary 3(a)), so Q is just-obstructing. By Corollary 3.2, Q is a subdirect product of proper quotients G_i that are JNA of perfect type; they are virtually solvable, hence finite by Lemma 5.1; infinitely many are needed for each normal subgroup by Corollary 3.2. The last sentence is Corollary 3.1. ∎

This extends H's Theorem 4(e) ("a just-infinite just-obstructing quotient is residually finite"). By the Wilson–Grigorchuk trichotomy (externally reported: a just-infinite group is a branch group, or virtually a power of a hereditarily just-infinite group, or virtually a power of a simple group), what (b) leaves among just-infinite groups is: branch groups and hereditarily-just-infinite-type groups having infinitely many non-solvable finite quotients of the above shape. Virtually-simple-power groups are not residually finite, and branch p-groups have only solvable finite quotients; both are excluded.

**The remaining difficulty, stated exactly (open).** For a just-infinite Q and π(U) = (s,t) with s ≠ 1, S = ⟨⟨s⟩⟩ has finite index and t maps to a normal generator of the finite group Q/S. By Theorem 1 it would suffice to find a co-abelian element in the coset tS:

> **Coset-avoidance problem.** Let Q be just-infinite, S ⊴ Q of finite index, and t ∈ Q with ⟨⟨t⟩⟩S = Q. Does tS contain an element that survives in every finite JNA quotient of Q?

Each JNA kernel N ⊉ S with t ∈ SN removes from tS one coset of S ∩ N, of relative size ≤ 1/|[Q,Q]N/N|; finitely many kernels can never cover tS when these sizes sum to less than 1 (this is how Step B in §6 works), but infinitely many kernels can cover a countable dense set even when the profinite measure of the complement is positive. A positive answer for all just-infinite groups would exclude every group of Theorem 4(b). §6 answers it positively for two arithmetic families by an explicit construction.

## 6. Theorems 5 and 6: SL_n(ℤ), n ≥ 3, and SL₂(ℤ[1/p]) obstruct nothing

Let (n,R) be (n ≥ 3, ℤ) or (2, ℤ[1/p]) with p a prime, and Γ = SL_n(R). "Prime" means a prime number l (l ≠ p in the second case); Γ(m) = ker(Γ → SL_n(R/mR)) for integers m ≥ 1 prime to p, and R/mR = ℤ/m. M_l := {g ∈ Γ : g mod l is a scalar matrix} = ker(Γ → PSL_n(𝔽_l)).

**External inputs (externally reported, not proved here).**
(E1) n ≥ 3: every noncentral normal subgroup of SL_n(ℤ) contains some Γ(m) (Mennicke 1965; Bass–Milnor–Serre 1967).
(E2) Every noncentral normal subgroup of SL₂(ℤ[1/p]) contains some Γ(m), (m,p) = 1 (Serre 1970, congruence subgroup property for SL₂ over rings of S-integers with infinitely many units, together with Margulis' normal subgroup theorem for the irreducible lattice SL₂(ℤ[1/p]) < SL₂(ℝ) × SL₂(ℚ_p); recalled also from Mennicke 1967).
(E3) Classical: SL_k(ℤ) → SL_k(ℤ/m) is onto; SL_n(𝔽_l) is quasisimple except SL₂(𝔽₂) ≅ S₃ and SL₂(𝔽₃) (normal subgroups 1, {±1}, Q₈, everything); SL₂(ℤ)_ab is cyclic; SL_n(ℤ/m) is perfect for n ≥ 3, and SL₂(ℤ/lᵉ) is perfect for l ≥ 5 (elementary matrices are commutators).

**Lemma 6.1 (proved).** The JNA quotients of H = SL_n(ℤ/m) are exactly the maps H → PSL_n(𝔽_l), l | m prime (reduction mod l, then modulo scalars).
*Proof.* PSL_n(𝔽_l) is JNA: simple, or S₃, or A₄. Conversely let G = H/N be JNA, M = [G,G], and H = ∏_{l|m} H_l with H_l = SL_n(ℤ/lᵉ). G is not nilpotent: for n ≥ 3, G is perfect; for n = 2, G_ab is cyclic (H is a quotient of SL₂(ℤ)) and a nilpotent group with cyclic abelianization is cyclic. *One factor.* The images A_l of the H_l are pairwise commuting normal subgroups generating G. If A_l, A_l′ ≠ 1 for l ≠ l′, then M ⊆ A_l ∩ A_l′, which commutes with every A_l″; so M = [G,G] is central and G is nilpotent — impossible. So G is a JNA quotient of one H_l. *Kernel of reduction.* K_l = ker(H_l → SL_n(𝔽_l)) is an l-group; let P be its image in G. If P ≠ 1 then P ⊇ M, so G/P is an abelian quotient of SL_n(𝔽_l), and SL_n(𝔽_l)_ab is an l-group in every case (trivial, or ℤ/2 for (2,2), ℤ/3 for (2,3)); then G is an l-group, hence nilpotent — impossible. So G is a JNA quotient of SL_n(𝔽_l). *Residue field.* In the quasisimple case the normal subgroups are central or everything and only the quotient by the full centre is JNA. S₃ is its own only nonabelian quotient. For SL₂(𝔽₃) the quotients are SL₂(𝔽₃) (not JNA: A₄ is a proper nonabelian quotient), A₄, ℤ/3, 1. ∎

**Lemma 6.2 (proved, given E1/E2).** g ∈ Γ is co-abelian in Γ iff g ∉ M_l for every prime l.
*Proof.* If g ∈ M_l, the cokernel of g maps onto the nonabelian group PSL_n(𝔽_l). Conversely let g ∉ M_l for all l. Then g is noncentral, so ⟨⟨g⟩⟩ ⊇ Γ(m) for some m and Γ/⟨⟨g⟩⟩ is a quotient of SL_n(ℤ/m) (E3). If it were nonabelian it would have a JNA quotient (Lemma 4.1(iii), finite case), which by Lemma 6.1 is reduction to PSL_n(𝔽_l) for some l | m; but g ∉ M_l. ∎

**Lemma 6.3 (row lemma; proved).** Let τ ∈ Γ and m₁ ≥ 1 prime to p. There is τ′ ∈ τΓ(m₁) such that τ′ ∉ M_l for every prime l ∤ m₁p.
*Proof.* Let v = (α₁,…,α_n) be the first row of τ; it is unimodular over the PID R.
*Case n ≥ 3.* Pick α₂′ ∈ α₂ + m₁R, α₂′ ≠ 0, and let P be the finite set of primes l ∤ m₁p dividing α₂′. By the Chinese remainder theorem pick k ∈ ℤ with α₃′ := α₃ + m₁k ≢ 0 (mod l) for all l ∈ P. Put v′ = (α₁, α₂′, α₃′, α₄, …). Then v′ ≡ v (mod m₁) and v′ is unimodular: a prime dividing α₂′ and α₃′ is not in P, so it divides m₁, and then it divides every entry of v. Choose h₀ ∈ Γ with first row v′. The first row of h₀τ⁻¹ is v′τ⁻¹ ≡ vτ⁻¹ = e₁ (mod m₁). Lift the inverse of h₀τ⁻¹ mod m₁, a matrix of SL_n(ℤ/m₁) with first row e₁, to h₁ ∈ Γ with first row exactly e₁ (block form (1,0; c,A) with A ∈ SL_{n−1}(ℤ/m₁) lifted by E3). Then τ′ := h₁h₀ has first row v′ and τ′τ⁻¹ ≡ 1 (mod m₁), so τ′ ∈ Γ(m₁)τ = τΓ(m₁). If τ′ were scalar modulo a prime l ∤ m₁p, l would divide both off-diagonal entries α₂′, α₃′ — impossible.
*Case n = 2.* v = (α,β). Pick β′ ∈ β + m₁R nonzero, P the primes l ∤ m₁p dividing β′, and α′ = α + m₁j ≢ 0 (mod l) for l ∈ P. As before (α′,β′) is unimodular and some τ₁ ∈ τΓ(m₁) has first row (α′,β′); let (γ,δ) be its second row. For k ∈ ℤ the matrix τ′ := e₂₁(m₁k)τ₁ ∈ τΓ(m₁) has first row (α′,β′) and (2,1)-entry γ + m₁kα′; choose k with γ + m₁kα′ ≢ 0 (mod l) for all l ∈ P (m₁α′ is invertible mod l). If τ′ were scalar mod l ∤ m₁p, then l | β′, so l ∈ P, but the (2,1)-entry is nonzero mod l. ∎

**Theorem 5/6 (proved, given E1/E2).** Let Q = Γ/Z₀ with Z₀ central. For every pair (s,t) normally generating Q there is t′ ∈ t⟨⟨s⟩⟩ that is co-abelian in Q. Consequently:
(i) for every epimorphism of F onto a quotient Q′ of Γ, Q′ obstructs nothing (in particular SL_n(ℤ), PSL_n(ℤ), SL₂(ℤ[1/p]), PSL₂(ℤ[1/p]) and, by Theorem 2, every extension of such a group by a solvable or finite kernel, e.g. the fibre products of H §7.2);
(ii) for n ≥ 3, any two normally generating pairs of SL_n(ℤ) are AC-equivalent.
*Proof.* Lift to s̃, t̃ ∈ Γ, so ⟨⟨s̃,t̃⟩⟩Z₀ = Γ, and let S̃ = ⟨⟨s̃⟩⟩. It suffices to find t̃′ ∈ t̃S̃ outside every M_l (Lemma 6.2; images of co-abelian elements are co-abelian). No M_l contains both s̃ and t̃, since M_l ⊇ Z₀ is proper. If s̃ is central take t̃′ = t̃. Otherwise B := {l : s̃ ∈ M_l} is finite (some off-diagonal entry, or a difference of diagonal entries, of s̃ is nonzero), and S̃ ⊇ Γ(m) for some m by E1/E2; enlarge m so that all primes of B ∪ C divide it, where C = ∅ for n ≥ 3 and C = {2,3}∖{p} for n = 2. Write m = m₁m₂ with m₁ the part of m at the primes of B ∪ C.
*Step A: S̃ ⊇ Γ(m₁).* Let S̄ be the image of S̃ in SL_n(ℤ/m) = H₁ × ∏_{l|m₂} H_l. For l | m₂ the group H_l is perfect (l ∉ C) and the projection of S̄ to H_l is all of H_l: otherwise H_l modulo it is a nontrivial perfect group, has a nonabelian simple (hence JNA) quotient, and Lemma 6.1 puts s̃ in M_l, but l ∉ B. Commutators of elements of S̄ with elements of the factor H_l lie in S̄ ∩ H_l and generate [H_l,H_l] = H_l. So S̄ ⊇ 1 × ∏_{l|m₂}H_l, which is the image of Γ(m₁) (E3); as S̃ ⊇ Γ(m), S̃ ⊇ Γ(m₁).
*Step B (n = 2 only): the primes of C′ := C∖B.* The image D of S̃ in ∏_{l∈C′} PSL₂(𝔽_l) is normal with nontrivial projections D_l (s̃ ∉ M_l), so |D₂| ≥ 3 and |D₃| ≥ 4 (nontrivial normal subgroups of S₃, A₄). For each l ∈ C′ the d ∈ D whose l-component equals the inverse of the image of t̃ form at most one coset of ker(D → D_l); together at most |D|(1/3 + 1/4) < |D| elements. Choose ñ ∈ S̃ mapping to none of them and put τ := t̃ñ (for n ≥ 3, τ := t̃). Then τ ∈ t̃S̃ and τ ∉ M_l for every l | m₁: for l ∈ C′ by construction, and for l ∈ B because S̃ ⊆ M_l and t̃ ∉ M_l.
*Step C.* Lemma 6.3 gives τ′ ∈ τΓ(m₁) ⊆ t̃S̃ outside M_l for all l ∤ m₁p; for l | m₁, τ′ ≡ τ (mod l), so τ′ ∉ M_l as well. Take t̃′ = τ′.
(i) (s,t) ~ (s,t′) and Theorem 1 apply when Q′ = Γ/Z₀; any other quotient of Γ is finite (E1/E2) and BLM applies. (ii) SL_n(ℤ) is perfect, so t′ is a normal generator and (s,t) ~ (s,t′) ~ (1,t′) ~ (g,t′) ~ (g,1) for one fixed normal generator g. ∎

*Remarks.* (1) SL_n(ℤ) is classically 2-generated (recalled), so (i) is not vacuous; I did not check whether SL₂(ℤ[1/p]) or PSL₂(ℤ[1/p]) is 2-generated — if not, (i) is vacuous for them but the pair statement stands. (2) PSL₂(ℤ[1/2]) was proposed in H §7.2 as a base in which neither AK(3) relator dies; Theorem 6 removes it together with its fibre products. (3) The proof is a positive solution of the coset-avoidance problem of §5 for these groups; the only non-formal step is Lemma 6.3, which uses two matrix entries as "independent coordinates" to avoid all primes at once. For a general lattice with the congruence subgroup property the same scheme needs a substitute for Lemma 6.3 (one element of a congruence coset that is non-central modulo every prime simultaneously); I did not attempt it.
