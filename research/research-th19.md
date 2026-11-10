# Research TH19: referee report on the round-5 theory notes TH01–TH09

Date: 2026-11-10 (UTC). Referee agent TH19 (round 5). **Status: referee report; nothing here is a new result.**

**Scope and method.** Independent check of the central claims of `research/research-th01.md` … `research-th09.md`.
Verdicts: **VERIFIED** (I re-derived the proof, or re-checked the claim by an independent exact computation — the last
column says which), **PLAUSIBLE-UNCHECKED**, **GAP**, **ERROR**, **OVERCLAIM**. My scripts are `experiments/th19_*.py`
(standard library only, each well under one minute, none imports code of the refereed notes; `th19_th09_census.py`
uses the repository's Todd–Coxeter from research-f). All `certificates/th0N_*.json` in format
`ordinary-ac-elementary-v1` were replayed with `python3 experiments/elementary_verify.py` and their start/target
compared with the notes. Every self-test shipped by the nine notes passed when I ran it (04:34 UTC, 17 scripts).
The version of each note I refereed is given by its line count at my last reading.

**Bottom line.** I found **no error and no overclaim of substance** in the nine notes. None of them claims an AK(3)
trivialization, an obstruction, or a counterexample, and none presents a generalized-move (ACM) or quotient statement
as an ordinary-AC result. The one coordinator warning that applied (holonomy traces alone do not separate k_n from
xˢy for n = 4, 5) is handled correctly by TH03.

## TH01 — two-pair abelian lifting (N §2.3)

| claim | verdict | how checked |
|---|---|---|
| T1 Substitution Lemma 2.1, Cor. 2.2 (commutator transfer), Lemma 2.3 (torsion collapse) | VERIFIED | re-derived line by line (four (M)-steps; c·p·c⁻¹·t⁻¹ct = cu) |
| T2 Prop. 3.1, Thm 3.2 (transfer lattice), Thm 3.3 (central lifting when [⟨⟨s⟩⟩,⟨⟨t⟩⟩] = 1) | VERIFIED | re-derived, including [R₊,G] ⊇ [G,G] and "z_S, z_T are central" |
| T3(b) (ω,t) ~ (zω,t) in G = ⟨SL(2,3), t \| [t,z]⟩ although D₀ = D₁ = 0 | VERIFIED | by hand in the Hurwitz quaternions: [j,i] = (ji)² = −1; iω = (−1−i−j+k)/2 has order 3, so iω = (iω)⁴ ∈ ⟨⟨ω[t,i]⟩⟩, hence K ⊆ ⟨⟨p⟩⟩; Cor. 2.2 applies with κ = j, c = i |
| T3(a) one-coordinate rigidity (Gerstenhaber–Rothaus), Λ = 1 × ⟨z⟩ | VERIFIED modulo the classical degree fact deg(τ ↦ k₀τ^{n₁}k₁⋯) = Σnᵢ | re-derived; Z(G) = ⟨z⟩ |
| status line "the two-pair problem is not settled in general" | accurate | — |

No certificate (no statement about F). T4 (failed invariants, §5–6) not refereed.

## TH02 — hidden reflections; the stabilizers Ŝ

| claim | verdict | how checked |
|---|---|---|
| 1 (Lemma 0, Thm 1): for r ~ (u²vⁿ)^{±1}, β = (u ↦ u⁻¹v⁻ⁿ, v ↦ v) has β(r,s) ~AC (r,s) for **every** s | VERIFIED | re-derived (β(u)u⁻¹ and β(ρ)ρ are conjugates of ρ^{∓1}); `th19_th02_check.py` (b): the two identities for 300 random bases |
| 2: N's D₆ ⊆ Ŝ(C4) is ⟨β_A, β_w⟩; the swap is the hidden reflection of the braid relator, so swap(b,s) ~AC (b,s) for all s, in particular swap(AK(n)) ~AC AK(n) for all n | VERIFIED | by hand: b ~ (u²v³)⁻¹ with u = (xyx)⁻¹, v = xy; β = (x ↦ xyxyXYX, y ↦ xyxYX), matrix = swap. Certificates `th02_c4_reflect_A/w.json`, `th02_ak3_swap_hidden.json`: start exact, target = β(start) exactly, (β(x),β(y)) a basis, matrices [[1,−3],[0,−1]], [[−1,0],[−1,1]], swap (script part (a)) |
| 3 (Lemma 3) T(a;2a,q) ~AC D(a;q) | VERIFIED | free identity xᵃ = A·YxY; three certificates replay with the stated endpoints |
| 4 (Thm 4) tr(R₁R₂) = 2 − D; D₆ for δ = +1 (C3-form, C4), hyperbolic element of trace 3 for δ = −1 (X, T(6;12,5)) | VERIFIED for the listed cases | certificates `th02_c3form_order6.json` (trace 1), `th02_x_hyperbolic.json`, `th02_T6_12_5_hyperbolic.json` (trace 3): target = h(start) exactly, h a basis |
| 5 (Thm 5) Ŝ(AK(n)) ⊇ ⟨−I, swap, [[−1,3],[0,1]]⟩, infinite, for all n ≥ 1 | VERIFIED given G's Theorem G1 | W_n = x⁻¹U²V^{−(2n+1)}x with V = xy, U = xVⁿ recomputed; ΨτΨ⁻¹ = [[−1,3],[0,1]]; τR has trace 3 |
| 6 (Thm 6) Ŝ(Y) is infinite for Y = T(4;7,5) (new) | VERIFIED by certificate | `th02_y_to_double_form.json`, `th02_y_hyperbolic.json`: Y → h(Y) exactly, matrix [[7,−5],[3,−2]], trace 5 |
| 7 (Prop. 7, Cor. 8) stabilizer of the cyclic word xᵖy^q; hidden reflections lie in the index-2 subgroup ker(det·sgn(M mod 2)), which contains none of the Nielsen generators x ↦ x⁻¹, x ↦ xy^{±1}, … | Cor. 8 VERIFIED (re-derived); Prop. 7 PLAUSIBLE-UNCHECKED (Whitehead's theorem; only a bounded ball check, script part (c)) | — |
| 8 experiment in Fwd(C4,28); "no element of Ŝ(C4) outside D₆ found" | not re-run; labelled experiment; **the C4 question stays open**, as the note says | — |

## TH03 — uniform O6 and the killer side Q2 (Gieseking coordinates P_n = (c, k_n))

| claim | verdict | how checked |
|---|---|---|
| T1: A, B, Y ∈ SL(2,ℤ[ω]) with Y·conj(A) = BY, Y·conj(B) = B⁻¹AY; T = Y·conj(Y) represents H | VERIFIED | `th19_th03_check.py` (own ℤ[ω] arithmetic): T1(i),(iii),(iv) asserted exactly |
| T2: I(u) = tr(ρ(u)Y·conj(ρ(u)Y)) ∈ ℤ is a conjugacy invariant of (u,1) in G_c | VERIFIED | re-derived: (u,k) ↦ ρ(u)(Y∘conj)^k is a homomorphism to SL₂(ℂ)⋊⟨conj⟩; the square of a degree-1 element is linear, its trace changes at most by complex conjugation and is real |
| T3–T5: recurrence u(n+4) = 3u(n+3) − u(n+2) + 3u(n+1) − u(n); σ(s) = σ(1−s); σ(n) < τ(n) < σ(n+1) for n ≥ 6; τ(n) = σ(s) exactly for n ∈ {1,2,4,5} | VERIFIED | same script, |n|, |s| ≤ 120: solutions (1,−2),(1,3),(2,−2),(2,3),(4,−4),(4,5),(5,−5),(5,6) only (agrees with the coordinator's `fig8_check.py`); Lemma T4 re-derived (if d(k+1) ≥ 2d(k) > 0 for three consecutive k then d(k+4) ≥ 2.5 d(k+3)); doubling bases found at k = 2 (τ−σ, Δσ, Δτ) and k = 6 (σ(n+1)−τ(n)) |
| T6: n = 4, 5 are isospectral (same I) but not conjugate | VERIFIED twice | `th19_th03_J.py` reproduces every value of J in Prop. T6 exactly; `th19_th03_n45.py` (third independent PSL(2,7)/PSL(2,13) computation, 176 + 416 homs of H): (4,−4),(4,5),(5,−5),(5,6) each separated, the true conjugacies (1,−2),(2,−2) never |
| **T7: for every n ≥ 3 and s ∈ ℤ, k_n ≁ xˢy in G_c — no c-frozen one-move primitive exit from P_n** (uniform O6) | **VERIFIED** (scope: one ACM move, c frozen) | T2 + T5 + T6 + O's Prop. O2. Holonomy traces alone do not suffice for n = 4, 5, and the note says so |
| T8: τ strictly increasing on n ≥ 2, so no c-frozen move joins P_n and P_m (n ≠ m ≥ 2) | VERIFIED | Δτ doubling base from n = 2 |
| T9: mirror automorphism α (x ↦ x⁻¹, y ↦ yx), α(c) ~ c⁻¹, I∘α = I | VERIFIED for α(c), α(xˢy), α(k_n) (free reductions by hand) and the identity SA = A⁻¹S; the trace computation was read, not re-derived | — |
| **T11: Q2(3) is negative — c is not conjugate in G_{k₃} to x·tʲ; with T7: no primitive relator is one ACM move from P₃, whichever relator is frozen (Cor. T11′)** — this closes O's open question Q2 for n = 3 | **VERIFIED** | `th19_th03_q2.py` (own truncated Magnus algebra): normal forms k₃ ↦ (1,0), c ↦ (t₁t₂⁻¹t₁⁻¹,1), xtʲ ↦ (t₁ʲ,1); all 39 identities (TT) hold for the printed functional ℓ; invariance under u ↦ v u ψ(v)⁻¹ on 400 random pairs; ℓ(t₁ʲ) = j(j−1)/2 ≥ 0; ℓ(c) = −2. Lemma T11a and Lemma 7.1 re-derived |
| T12: Q2(4), Q2(5) negative | VERIFIED | `th19_th03_tt.py` (own solver of (TT)): n = 4 over 𝔽₂, D = 4: solution space of dimension 7, no residue j mod 8 survives; n = 5 over ℚ, D = 3: dimension 4, one trace vanishes on all t₁ʲ and is −2 on c |
| T13: integer twisted trace L4 on G_c; L4(xˢy) = C(s+1,4) ≥ 0, L4(k_n) = 1, 1, −1, −5, −10, −14, −14, −6, 15 (n = 1..9): second proof of O6 for n = 3..8 | VERIFIED | same script: L4 satisfies the 30 identities; solution space of dimension 2; values reproduced exactly |
| T14: exactly 43 cyclic words of y-degree 1 and length ≤ 9 have I = 20; 25 have J ≠ J(k₃); 7 are conjugate to k₃; so every c-frozen neighbour (c,w) of P₃ has |w| ≥ 7 | VERIFIED (counts and the 7 positives; the status of the 11 mirror words as in the note) | `th19_th03_t14.py`: 43 = 25 (by length 6:3, 7:6, 8:5, 9:11) + 18 (7:3, 8:6, 9:9); `th19_th03_t14a.py`: own twisted-conjugacy BFS (cap 15, 4,733 class elements) reaches exactly the 7 listed words |
| T15 (second moves through five short neighbours), §9 experiments | PLAUSIBLE-UNCHECKED (not re-run; correctly labelled a bounded census) | — |

Outputs: σ(0..9) = 2, 2, 2, 8, 26, 74, 218, 650, 1928, 5714; τ(1..9) = 8, 8, 20, 74, 218, 632, 1880, 5588, 16562.
Remark for the README: TH08's finding F2 (the closing summary overstated O6 because the k_n-frozen half was open)
was correct when written; TH03's T11/T12 now prove that half for n = 3, 4, 5 (for n = 6, 7, 8 it remains open).

## TH04 — rigidity of the torus island

| claim | verdict | how checked |
|---|---|---|
| T1 (Thm 2.2, Cor. 2.3) twist rigidity: outside the trefoil group a twist of a partner is a partner only for ±I and (if 2 ∈ {|p|,|q|}) the hidden involution | VERIFIED | ping-pong proof re-derived step by step ((0)–(4)); `th19_th04_check.py` (c): among 7,772 twist matrices and all partner vectors in a box, exactly {±I} for (3,−4), (3,5), (4,5), exactly {±I, ±M_ι} for (2,±5), (2,7), and 12 matrices for the trefoil |
| T2 (Lemma 3.1) hidden involution ι for p = ±2 (the same automorphism as TH02's β) | VERIFIED | by hand and script part (b) |
| T3 (Prop. 2.4) the trefoil exception κ: x ↦ x, y ↦ x²Y | PLAUSIBLE (proof read; consistent with the brute force) | — |
| T4 (Thm 4.1) AK(n) ~AC (cyc ψκ(W_n), b) for all n ≥ 1 — G's third island node, uniformly | VERIFIED | script part (a): κ(W_n) ~ W_n⁻¹ in ⟨x,y \| x² = y³⟩ for n ≤ 12 (own necklace test); certificate `th04_ak3_to_kappa_node.json` (6,774 moves): start exactly AK(3), target[0] a rotation of cyc ψκ(W₃), κ(W₃) = G's third-node word up to rotation/inversion |
| T5 structure of the island (experiment), T6 (Lemma 6.1, Bass–Serre tree) | T5 not re-run (labelled experiment); T6 read (case EE checked), not fully re-derived | — |
| "the island theorem is not proved; two lemmas are missing" | accurate | — |

## TH05 — homes for an obstruction

| claim | verdict | how checked |
|---|---|---|
| T1 cokernel criterion: a class pair with a coordinate of abelian (Thm 1) or metabelian (Thm 1⁺) cokernel ⇒ Q does not obstruct; Example 1.3 (no quotient in which x commutes with yxy⁻¹, or yx⁻¹ with xyx⁻², obstructs AK(n)) | VERIFIED | re-derived: Lemma 0, Lemma 2.1 (α ↦ [α,σ] is onto A, so σA is one conjugacy class), the B₃ computation xvx⁻¹ = u⁻¹v ⇔ xyx = yxy |
| T2 lifting through central / abelian / solvable / finite normal subgroups; C2 fibre products over any base; C3 just-obstructing ⇒ no abelian, solvable or finite normal subgroup, no minimal normal subgroup, ICC | VERIFIED | re-derived: the cokernel of a·z₀ (z₀ central) is generated by a central element and b, hence abelian; (b)–(e) from H's Lemma 2.1 and corrected 2(ii); ICC argument checked |
| T3 just-non-abelian residual (Thm 3, Cor. 3.1, 3.2) | VERIFIED | re-derived (Zorn with the single element [a,b]; subdirect induction) |
| T4 excluded classes | PLAUSIBLE (formal consequence of T2, T3; read) | — |
| T5/T6 SL_n(ℤ) (n ≥ 3) and SL₂(ℤ[1/p]) obstruct nothing | VERIFIED modulo the cited external theorems (Mennicke / Bass–Milnor–Serre; Serre + Margulis), which I also only recall | Lemmas 6.1–6.3 and Steps A–C re-derived |
| "hyperbolic and residually finite just-obstructing quotients are not excluded" | accurate | — |

## TH06 — nilpotent, metabelian and pro-p quotients with arbitrary conjugators

| claim | verdict | how checked |
|---|---|---|
| Lemma 1.1 / Thm 1: in every nilpotent ⟨a,b⟩, (a,b) → (a e₀, b e₁) for all e_i ∈ γ₂ by 4 conjugations + 4 multiplications; d*_Q(U) ≤ ℓ(U) + 8 | VERIFIED | induction on the lower central series re-derived (it is the classical lemma of the brief in two-conjugation form); `th19_th06_check.py`: brute force in two 2-generated 2-groups (orders 256, 512): 0 failures for (a,b) and (b, a e₀); control S₄ fails, as it may; ℓ(AK(n)) = 3, 4, 5, 6 recomputed by BFS in GL₂(ℤ) |
| Lemma 1.2 (abelian-by-nilpotent), Lemma 1.3, Lemma 1.4, Thm 1′ (C = 8 / 24 / 32 for metabelian / Q″ central / derived length ≤ 3) | VERIFIED | re-derived (the 8-instruction word for [c,μ]; [a,K][ba,K] = [K,Q]) |
| Lemma 1.5 (series with coinvariant-free layers; SL₂(ℤ/pⁿ) towers) | PLAUSIBLE (same computation as 1.1; read) | — |
| Thm 2 pro-p version; "the pro-p completion with arbitrary conjugators sees exactly the exponent matrix" | VERIFIED | inverse limit of non-empty finite solution sets |
| Thm 4: with syllable instructions (a) or power instructions (b, Hilbert basis theorem) the chain N_c stays faithful; Cor. 5 | VERIFIED | re-derived; (a) is E's Lemma 2(a) with syllable length |
| Prop. 7 (bounded d* on finite simple quotients) | PLAUSIBLE modulo Liebeck–Shalev (external); counting argument read | — |
| files `certificates/th06_*.json` | **not** AC certificates (format `th06-8move-nilpotent-v1`, quotient-only, labelled so in the files); the strict verifier rightly rejects them | their own `--verify`/self-test pass |

Consistency with the brief: Theorem 1 is exactly the "about ten moves plus Nielsen moves" bound; nothing contradicts it.

## TH07 — beyond the plateau of AK(n)

| claim | verdict | how checked |
|---|---|---|
| Thm A: the words of length 2n+3 conjugate to p_n^{±1} in B are exactly the 4n(n+1)(2n+3) rotations of U1(a,c)^{±1}, U2(a,c)^{±1} | VERIFIED for n = 1,…,4 by exhaustive enumeration; general proof read, no gap found | `th19_th07_check.py`: 40, 168, 432, 880 words, equal to the claimed sets; 0 words of length 2n+2 |
| Thm B: braid side — besides Orb(b) nothing shorter than 2n+2; exactly Orb(b₁) ∪ Orb(b₂) (8n+8 words) at 2n+2; hence a braid-side exit costs ≥ 4n+3 | VERIFIED for n = 3, 4, 5 by exhaustive enumeration; proof read | `th19_th07_B.py`: counts 12, 0, …, 0, 8n+8 |
| Thm C: the class of b modulo w_n = xⁿyX^{n+1}Y | VERIFIED in part | `th19_th07_C.py` (own Britton reduction): v_j = x^{n(j−1)}βx^{−n(j−1)} (|j| ≤ 6) and e_n = x^{n²−1}βx^{−(n²−1)} for n = 3, 4, 5; for n = 3, 4 the words of length ≤ n+3 conjugate to β^{±1} are exactly the claimed 46 and 76 (exhaustive in words, conjugator search bounded) |
| Cor. C1/C2: 2n+9 (J1) is sharp; ACM path AK(n) → (w_n,b) → (w_n,e_n) → (d_n,e_n) → P_n of peak 3n+6; S_n = (xⁿYXyy, x^{n−1}yyXY) ~AC AK(n); the ACM barrier between AK(3) and Q, P₃ is exactly 15 | VERIFIED for n = 3,…,8 (free-word triangles) together with Thm C for n = 3, 4, 5 | `th19_th07_paths.py`: w_n ∈ C_n, triangles (w,d,e), (w,a,d), (d,a,c), lengths 2n+7, 2n+9, 3n+6, 2n+7, n+11; S₃ = D/E's second length-13 pair up to x ↦ X |
| Cor. C3 balanced chain (peak 2n+8+⌊(2n+1)/3⌋) | VERIFIED for 3 ≤ n ≤ 10 (triangles and lengths) | same script |
| scope statement: all numbers are ACM peaks in cyclic length, not elementary peaks, and no evidence about triviality | accurate | — |

## TH08 — audit of G–O

Every error or wording problem TH08 reports that I re-derived is **real**:

| finding | my check |
|---|---|
| F1 README: "no quotient with an abelian normal subgroup inside its derived subgroup or a nonabelian minimal normal subgroup" overstates H (H proves descent to Q/N) | CONFIRMED |
| F2 README: "no single ACM move from … P₃,…,P₈ reaches a primitive relator" — O6 is c-frozen only, Q2 was open | CONFIRMED (now proved for n = 3, 4, 5 by TH03 T11/T12) |
| F3 README (I, M), M §3.5: "no automorphic image of itself" is false as stated (N3: φ₁(C4), φ₂(C4) ∈ Fwd(C4,28)); correct: none of the seven Nielsen-generator images | CONFIRMED (quotes located in README lines 35, 41 and research-m line 99) |
| F4 N §2.3: the central example does not show D₀ ⊊ [N,Q]; D₀, D₁ need not be submodules; example ℤ⁵ ⋊ A₅ | CONFIRMED (example recomputed: D₀ of rank 2, [N,Q] of rank 4) |
| F5 I Prop. M: the congruence hypothesis is superfluous for AC-triviality (Lemma E + G0 = G §2.4(b)) | CONFIRMED |
| F6 N §1 "kernel not characteristic" points the wrong way | CONFIRMED |
| F9 O §2.3 typo ∂ = aBAB for abAB; F10 N §3.2 R and R⁻¹ interchanged | CONFIRMED (both recomputed: φ(abAB) = b⁻¹(abAB)⁻¹b; φ₁∘φ₂ has matrix M₁M₂) |
| F7, F8, F11 | read; consistent; not re-derived |

New results of TH08 §3: Lemma TH08-L, **Thm TH08-P1** (F/(V₀∩V₁) ≅ G₀ × G₁ and F/[V₀,V₁] never obstruct — "AK(3) is
AC-trivial modulo [⟨⟨x³y⁻⁴⟩⟩, ⟨⟨b⟩⟩]"), Cor. P2, Lemma TH08-S: **VERIFIED** by re-derivation (Steps 1–3 of P1; the
five-term sequence in S). They are consistent with, and partly implied by, TH05's Theorems 1 and 2. I did not re-audit
the long list "verified correct" (H, N, O, K, G, I, L, M); where my own reading of H, N, O overlapped it, I agree.

## TH09 — killers; the BS(1,2) exit; census of trefoil killers

| claim | verdict | how checked |
|---|---|---|
| T1 (Thm 1): G_r ≅ BS(1,2) ⇒ every balanced (r,s) of the trivial group is AC-trivial (one generalized move to a primitive, then D3) | VERIFIED | re-derived exactly as in the brief (every element of degree ±1 of ℤ[1/2]⋊ℤ is conjugate to t^{±1}; a primitive of degree 1 exists for any marking); `th19_th09_check.py` (1); certificates `th09_ms1_1..6.json` replay from (XyxYY, s) to (x,y) |
| T2 (Thm 2): BS(1,m) occurs only for m = 2 (m = 0 primitive) | VERIFIED | abelianization ℤ × ℤ/|m−1| |
| T3 (Thm 3): BS(1,2)-type killer classes of G_r form the one-parameter family v_j^± | VERIFIED | re-derived (IA(F₂) = Inn); bounded cross-check: all 26 BS(1,2)-type partners of b in a ball of 8,865 automorphisms lie in the family |
| T4 (Thm 4): a BS(1,2)-type word is conjugate in B to (xⁿY^{n+1})^{±1} iff n ≤ 2 | VERIFIED | run-count argument re-read; own necklace computation, n ≤ 12, |j| ≤ 40: hits only for n = 1, 2 |
| T5 (Thm 5): T(n,n+1) side, none for n ≥ 3 | VERIFIED (proof read; bounded machine check n = 3..7: 0 hits, n = 2: 4 hits) | script part (4) |
| T6 (Thm 6): Gieseking side, n = 3, 4 | VERIFIED | `th19_th09_gieseking.py` (own normal form of G_c): |tr| of (v_j^+)² = 5,3,5,5,2,0,3, of (v_j^-)² = 3,5,3,0,2,5,5, k₃: 4, k₄: 1 — the note's numbers |
| T8 (Thm 8) killer criterion for torus-knot groups | VERIFIED | re-derived |
| T9 census k ≤ 9: 1, 1, 2, 5, 15 killer classes; at k = 7 the classes without a known exit are exactly AK(3) = 1111222 and C3 = 1111112 | VERIFIED | `th19_th09_census.py` (own class enumeration + repository Todd–Coxeter): same lists; `th19_th09_necklace.py`: necklaces of AK(2), AK(3), AK(4), C3 and of both certificate presentations recomputed |
| T10 exchange exit; two trivializations | VERIFIED by replay | `th09_x7_trivialization.json`: (XXXYXXYxxy, XYYXy) → (x,y), 6,998 moves, necklace 1121122; `th09_k9_112121122_trivialization.json`: (XyXyXYXyXYxyxyxYxY, xxYYY) → (x,y), 7,147 moves |
| exchange-graph data and depth-2 exits (§7.4) | not re-run (labelled bounded experiment) | — |

"Undecided" in T9 means "no exit known", as the note says; it is not a hardness claim.
