# Research TH20: referee report on the round-5 theory notes TH10–TH18

Date: 2026-11-09 (Los Angeles) / 2026-11-10 UTC. Agent TH20 (round 5, referee). **Written incrementally; the version of each note that was refereed is identified by its line count and time stamp.**

**Status.** This is a verification report, not a research note: it contains no new AC result. Verdict labels: **VERIFIED** (proof re-derived by me, or claim re-checked by an independent exact computation — which one is stated), **PLAUSIBLE-UNCHECKED**, **GAP**, **ERROR**, **OVERCLAIM**. "Self-test re-run" alone is *not* counted as VERIFIED unless I also read the proof or recomputed independently. My scripts: `experiments/th20_lib.py` (words, automorphisms, pieces, coset-enumeration wrapper around `f_descent.coset_index`, certificate replay with start/target printed) and `experiments/th20_*.py` (one per check; outputs quoted below).

## 0. Pre-check of the coordinator's findings given to TH11 (done 04:11 UTC, before any draft existed)

`python3 experiments/th20_theta_holonomy.py 14 40` (own code, own Q(ω) arithmetic; same Jørgensen normalization as the trace triple (1−ω, 2+ω, 2+ω), which I re-derived as the unique fixed point of the trace map of φ² up to complex conjugation: z = y, x = y/(y−1), y² − 3y + 3 = 0):

```
theta: c -> conj of c^-1; x^s y -> conj of x^(1-s) y; k_n -> X^(n+1) Yxyxyx  [free identities OK]
trace coincidences (n,s), n<=14, |s|<=40: [(1,-2),(1,3),(2,-2),(2,3),(4,-4),(4,5),(5,-5),(5,6)]  (same list for theta(k_n))
```

| claim (coordinator → TH11) | verdict |
|---|---|
| θ = (x ↦ x⁻¹, y ↦ yx) sends c = xyxYYXy to a conjugate of c⁻¹ (θ(c) = XyXYXYxyx, cyclically yXYXYxy, a rotation of c⁻¹) | VERIFIED (by hand and by script) |
| θ(xˢy) = x⁻ˢyx ~ x^{1−s}y | VERIFIED (hand + script, \|s\| ≤ 8) |
| θ(k_n) = x^{−(n+1)}y⁻¹xyxyx, normal form (a⁻ⁿbab, 1) | VERIFIED (hand: reading rule of O1 gives a^{−(n+1)}·ab·a·b; script n ≤ 11) |
| exact invariants of k_n² and (xˢy)² (and of y(xˢy)²y⁻¹) coincide exactly for (n,s) ∈ {(1,−2),(1,3),(2,−2),(2,3),(4,−4),(4,5),(5,−5),(5,6)}, n ≤ 14, \|s\| ≤ 40 | VERIFIED (independent exact computation; relations T A T⁻¹ = B⁻¹A, T B T⁻¹ = A⁻¹B² asserted exactly) |

## 1. TH10 (exotic quotients; abelian-quotient filter, torsion vs torus coordinates)

*Preliminary, from the claims table of the 04:14 UTC draft (proof sections not yet written); each claim below was re-derived by me before reading TH10's proofs.*

| claim | verdict | my derivation |
|---|---|---|
| A (abelian-quotient filter: (s,t) admissible, Q/⟨⟨s⟩⟩ abelian ⇒ standardizable) | VERIFIED (own proof) | pick a basis (w₁,w₂) of F with π(w₁) ≡ s, π(w₂) ≡ t mod [Q,Q] (admissibility); [Q,Q] ⊆ ⟨⟨s⟩⟩ gives (s,t) ~ (s,π(w₂)); Q/⟨⟨π(w₂)⟩⟩ is a quotient of F/⟨⟨w₂⟩⟩ ≅ ℤ, so [Q,Q] ⊆ ⟨⟨π(w₂)⟩⟩ and (s,π(w₂)) ~ (π(w₁),π(w₂)) ~ (a,b) by Nielsen moves. |
| A1 | VERIFIED | ⇐ is A (AC moves preserve admissibility); ⇒ because Q/⟨⟨a⟩⟩ is cyclic. |
| B (class coordinate uᵖv⁻ᑫ, π(u) of finite order prime to p ⇒ no obstruction) | VERIFIED (own proof) | in Q/⟨⟨π(c)⟩⟩ the element ūᵖ = v̄ᑫ is central and ū ∈ ⟨ūᵖ⟩, so the quotient is abelian; apply A. |
| B1 (no periodic p-group, no group of odd exponent or of exponent prime to 3 obstructs AK(n)) | VERIFIED | b = cyc((xyx)²(xy)⁻³) (free reduction checked by hand) and (xyx, xy) is a basis; apply B to u = xyx (p = 2), v = xy (q = 3). |
| B2 (obstruction of AK(3) ⇒ every primitive has image of infinite order or order divisible by 42) | VERIFIED given D6 and G1's certificate | W₃ ~ u²v⁻⁷ with (u,v) = ((xy)³x, xy) (checked by hand for all n: u²v^{−(2n+1)} is conjugate to W_n); Aut-closure (D6) puts g²h⁻³, h²g⁻³, h²g⁻⁷ among the class coordinates for every basis (g,h). Wording: "quotient of a triangle group Δ(l,m,k)" must mean the *marked* quotient x ↦ a, y ↦ b (the triangle generators need not be images of primitives otherwise). |
| D ((aᵏ,bˡ) ~ (a,b) if kl ≡ 1 mod N) | VERIFIED (own proof) | Q/⟨⟨aᵏ⟩⟩ = Q/⟨⟨a⟩⟩ is cyclic and diag(k,l) ∈ SL₂(ℤ/N) lifts to SL₂(ℤ), so the pair is admissible; apply A. The same argument shows more: α(a,b) ~ (a,b) for *every* automorphism α of Q with α(a,b) admissible. |

## 2. TH15 (uniform proof that Aut(F₂) is AC-realized on AK(n), n ≥ 2)

Checked independently before the proof sections of the note existed (words typed from TH15's closed formulas; TH15's code not imported): `python3 experiments/th20_th15_check.py` →
`TH15 closed-form chains: every step is one cyclic product, endpoints = sigma(AK(n)), a(AK(n)) up to rotation/inversion, n = 2..12` (the n = 3 and n = 5 chains are printed in full). I also re-derived every step **symbolically for general n by hand** (free reduction):

- swap, b frozen: XYXyxy·p_n is a rotation of w₁; with r = xy·x^{n−k+1}Y^{n+1}XYX·yᵏ (rotation of w_k), yxyXYX·r = yxy·x^{n−k}Y^{n+1}XYX·yᵏ, a rotation of w_{k+1}; for k = n the same product is yxYⁿXYXyⁿ, a rotation of w′₁ = y^{n+1}xYⁿXYX; with r′ = yxY^{n+1−j}XYX·yⁿX^{j−1}, XyxyXY·r′ = XyxY^{n−j}XYX·yⁿX^{j−1}, a rotation of w′_{j+1}; for j = n it is XX·yⁿX^{n−1} ~ q_n. 2n+1 steps.
- a = (x ↦ xY): (X u_k x)·XyxyXY = u_{k+1} for 0 ≤ k ≤ n−2 and for k = n−1 it gives YⁿxyⁿXY ~ b₁ = XY^{n+1}xyⁿ (phase II, u_{n−1} frozen); (Y^{n+1}xyⁿX)·u_{n−1} = Y^{n+1}xxy^{n−1}XY ~ v₀; (xyⁿXY^{n+1})·(y^{n+1}xY^{n−1}XXy) = xyXXy ~ b₂ = yxyXX = a(b)⁻¹; YxxYX·(x y^{n−1−m}XY^{n+2}x(Yx)ᵐ) = Yxx y^{n−2−m}XY^{n+2}x(Yx)ᵐ ~ v_{m+1}, and for m = n−2 it is ~ (xY)ⁿY^{n+1} = a(p_n). 2n+1 steps.

| claim | verdict |
|---|---|
| Prop. A (swap by 2n+1 cyclic products, b frozen) and Lemma A′ ((w,b) ~ σ(w,b) for every w) | VERIFIED (hand derivation for all n; script n = 2..12; A′: Δ = xyx satisfies Δx = yΔ, Δy = xΔ mod ⟨⟨b⟩⟩ and σ(b) = b⁻¹) |
| Prop. B (a = (x ↦ xy⁻¹) by 2n+1 cyclic products, five phases) | VERIFIED (hand derivation for all n ≥ 2; script n = 2..12) |
| Theorem 1 (every φ ∈ Aut(F₂) is AC-realized on AK(n), n ≥ 2) | VERIFIED given A, B: σ ↦ [[0,1],[1,0]] and a ↦ a unitriangular matrix generate GL₂(ℤ) = Out(F₂), inner automorphisms are conjugations, and the set of realized φ is a subgroup (D6's transport argument). Not new (Panteleev–Ushakov), as the note says. |
| certificates `th15_ak{2,4,8}_aut_*.json` | VERIFIED: all replay; targets are exactly σ(AK(n)) = (yⁿX^{n+1}, yxyXYX), a(AK(n)) = ((xY)ⁿY^{n+1}, xxYXY), and for n = 4 ε_x(AK(4)) = (X⁴Y⁵, XyXYxY), (x ↦ xy)(AK(4)) = ((xy)⁴Y⁵ reduced, xyyxYXY) (targets recomputed by me). |

## 3. TH13 (two-parameter family AK(k;p) = (xᵖY^{p+1}, W_k))

*Preliminary (from `experiments/th13_family.py` and the certificates, before the note existed).* `python3 experiments/th20_th13_check.py`:
```
(1),(2) OK for k,p <= 8: phi_k(p_p) ~ V_{k,p} in <x^2=y^(2k+1)>, necklace (k+1)^p k^(p+1)
(3) coset enumeration: AK(k;p), D(k;p) trivial for k<=4, p<=5; exceptions: []
(4) th13_dual_k{2_p2,2_p3,3_p3}.json: start = AK(k;p), target = (red psi_k(V_{k,p}), W_k); the three trivialization certificates start at AK(2;2), AK(2;1), AK(3;1) and end at (x,y)
```
Hand proofs (mine): (i) ⟨x,y | xᵖ = y^{p+1}, W_k⟩ = 1 for all k, p ≥ 1 (z = xᵖ = y^{p+1} is central; modulo z, x and y are conjugate with xᵖ = 1 = x^{p+1}); (ii) duality: in C₂*C_{2k+1} = ⟨s⟩*⟨t⟩, φ_k(p_p) ↦ (st^{k+1})^{p−1}·st^k·s(t^ks)^p t^{k+1} and V_{k,p} ↦ (t^ks)^p t^k s (t^{k+1}s)^p, both with t-necklace (k+1)^p k^{p+1}; the abelianization x ↦ 2k+1, y ↦ 2 gives −1 for both, so the central exponents agree and φ_k(p_p) ~ V_{k,p} in ⟨x² = y^{2k+1}⟩ (not its inverse).

## 4. TH14 (STABLE theory: one stabilization)

*Preliminary (04:18 UTC draft, claims table + proof of Theorem A).* All statements here are about (U, z) in rank n+1, i.e. **stable**; the note labels them so.

| claim | verdict | reasoning |
|---|---|---|
| A (class of (U,z) is Aut(F_{n+1})-invariant; costs 2A_i+\|U\|_{x_i}, 1, A_i macro moves) | VERIFIED (proof read line by line) | (ii) one inversion; (iii) x_i ∈ ⟨⟨U⟩⟩; (i): the two free identities u x_i v·v⁻¹x_i⁻¹(z x_i⁻¹)x_i v = u z v and u x_i⁻¹ v·v⁻¹(z x_i⁻¹)⁻¹v = u z⁻¹ v are correct, then z ∈ ⟨⟨σ_i U⟩⟩; star transpositions, one inversion, one transvection generate Aut(F_{n+1}) (Nielsen); the realized set is a subgroup (D2 transport, valid in any rank). Classical in content, as the note says. |
| B (stable substitution: ⟨⟨p,q⟩⟩ = F₂ and ⟨p,q,t⟩ = F₂ ⇒ (U∘(p,q), z) ~ (U, z) in rank 3) | VERIFIED (own proof, written before TH14's proof was available) | Nielsen: the generating triple (p,q,t) of F₂ is Nielsen-equivalent to (x,y,1), so there is θ ∈ Aut(F₃) with θ(x) ≡ p, θ(y) ≡ q mod ⟨⟨z⟩⟩. Put k = θ⁻¹(z). ⟨⟨U,k⟩⟩ = θ⁻¹⟨⟨U∘(p,q), z⟩⟩ = F₃ (U∘(p,q) normally generates F₂ because p, q die in F₂/⟨⟨U∘(p,q)⟩⟩), so k has z-exponent sum ±1 and (U,z) ~ (U,k) (delete/insert x,y-letters). Transport by θ: θ(U,z) ~ θ(U,k) = (U(θx,θy), z) ~ (U∘(p,q), z) (delete z-letters), and θ(U,z) ~ (U,z) by A. |
| B2 (composition formula (U∘P, z₁..z_n) ~ U ⊔ P) | PLAUSIBLE, sketch re-derived | z_j ↦ z_j⁻¹p_j(x) (p_j ∈ ⟨⟨U∘P⟩⟩), substitute p_j → z_j inside U∘P, then z_j ∈ ⟨⟨U(z)⟩⟩ turns z_j⁻¹p_j into p_j: (U(z), P(x)); the renaming x ↔ z needs the transvection argument of A. To be compared with TH14's text. |
| C (w(p,q) primitive in F₂ ⇒ w primitive) | VERIFIED **under the hypothesis that (p,q) is a basis of ⟨p,q⟩** (true when (p,q) normally generates F₂) | an element of H ≤ F that is primitive in F is primitive in H (Kurosh). Without the hypothesis the statement is false: p = x, q = 1, w = u·[u,v]. |

## 5. TH12 (generator area of AK(n); linear lower bounds on the number of moves)

Version read: 187 lines (04:30 UTC). `python3 experiments/th20_th12_check.py` (own code):
```
(1) identities OK, n = 1..30
(2) trace(r) = n^2+n+2 in SL2(Z), braid relation holds
(3) n <= 6: mu <= n+1 forces mu = n+1 and count matrix [[1,n+1],[1,n]]  (so mu >= n+2 by c_r >= 3)
(4) permutation model OK, n = 4..40
```

| claim | verdict | what I checked |
|---|---|---|
| Thm 1 (count-matrix calculus; A(U₀) ≤ F_{μ+2}, radius ≤ κ) | VERIFIED (proof read) | downward induction step for each instruction type; Fibonacci bound for products of L, R. |
| Thm 2 (Area_{AK(n)}(x) = n+4, Area(y) = n+3; every expression has c_r ≥ 3 odd, c_s ≥ n+1 resp. n) | VERIFIED | upper bound: identities (I_x), (I_y) re-typed and freely reduced, n ≤ 30; lower bound: E⁻¹ = [[−1,n+1],[−1,n]] gives the signed counts, and c_r = 1 would make x or y conjugate to r⁻¹ in B₃, impossible since tr = 2 ≠ n²+n+2 in SL₂(ℤ) (matrices and braid relation recomputed). |
| Thm 3 (every instruction path AK(n) → (x,y) has μ ≥ n+2 multiplications) | VERIFIED (proof read step by step + exhaustive check n ≤ 6) | Σ = d·t₁⋯t_μ with d ∈ {±I, ±S}; L = ab, R = ab⁻¹ in ℤ/2*ℤ/3; class of Σ has length 2n+3, of S⁻¹Σ 2n+2; the loss analysis (0, 1, never 2) is correct; loss 0 forces C₀ = \|Σ\| with first column (1,1), contradicting c_r ≥ 3. |
| Thm 4 (n ≥ 4: κ ≥ n−3 conjugations) | VERIFIED (proof read; Lemma 4.1 re-checked by script and by hand) | conjugators are products over distinct conjugation instructions, so prefix displacements lie in [−κ⁻, κ⁺]; if κ ≤ n−4 the point v = κ⁻+1 is fixed by every factor but moved by x. |
| Cor. 5 (d_F(AK(n)) ≥ 2n−1 for n ≥ 4, every elementary-v1 certificate has ≥ 2n−1 moves) | VERIFIED given Thm 3, 4 (μ + κ ≤ number of moves). Correctly labelled as a complexity statement, not an obstruction (it holds for the AC-trivial AK(1), AK(2) too). |
| §5 (P_n: μ ≥ n; area bounds 3 ≤ Area_{P₃}(x) ≤ 593) | PLAUSIBLE-UNCHECKED (the μ ≥ n argument is the same loss lemma; the numerical upper bounds were not recomputed). |

## 6. TH11 (relator stabilizers; nilpotent Reidemeister invariants (κ, Ĵ) of G_c; one-move relations between the k_n)

*Preliminary: claims table of the 04:24 UTC draft (sections not yet written) + `experiments/th11_nil.py`.* My checks: `experiments/th20_stab.py` (own Whitehead level-graph / McCool computation of stabilizers in GL₂(ℤ)), `experiments/th20_th11_check.py` (uses TH11's `KJ`, `KJ_ser` for the invariants — not independent for their definition — and my own exact holonomy invariant τ), §0 above.

```
c = xyxYYXy  Stab(w^+-1): [((-1, 1), (0, 1)), ((1, 0), (0, 1))] | Stab(w): [((1, 0), (0, 1))]
b = xyxYXY   Stab(w^+-1): {+-I, +-swap}                          | Stab(w): {I, -swap}
p_2          Stab(w^+-1): [((-1,0),(0,-1)), ((-1,0),(3,1)), ((1,0),(-3,-1)), ((1,0),(0,1))]   <-- order 4
p_3 .. p_7   Stab(w^+-1): {+-I}
(1) closed forms kappa, Jhat = J - kappa agree with th11_nil.KJ for n in [-40,60], s in [-40,40]
(2) 250 random words: (kappa,J) twisted-conjugacy invariant; theta0 flips kappa and preserves Jhat
(3) (n,s) with equal (kappa,Jhat), |n| <= 2000: [(-1,-1), (-1,0), (0,-1), (0,0), (1,-2), (2,-2), (9,5)];  tau(k_9^2) in tau-set of x^5 y: False
(4) pairs n<m<=3000 with Jhat(k_n)=Jhat(k_m): [(1,2,'same kappa'), (6,7,'kappa differs')]; tau-sets of k_6 and theta0(k_7) (and of k_7, theta0(k_6)) are disjoint
```

| claim | verdict | reasoning |
|---|---|---|
| T1: Out(G_c) ≅ ℤ/2 = ⟨[θ₀]⟩; Stab(c^{±1}) = {1,[θ₀]}, Stab(c) = 1; θ₀(u,1) = (ι(u)b, 1) | VERIFIED | own proof of Out: the fibre F(a,b) = [G_c,G_c] is characteristic, so Out(G_c) = N_{GL₂(ℤ)}(⟨A⟩)/⟨A⟩ with A = [[0,1],[1,−1]]; tr A ≠ tr A⁻¹, the centralizer of A is the unit group {±Aᵏ} of ℤ[(1+√5)/2], hence Out = {±I}·⟨A⟩/⟨A⟩ ≅ ℤ/2, and θ₀ acts on the fibre by ι (class −I), y ↦ (b,1) (computed by hand). Stabilizers: independent level-graph computation (rests on Whitehead/McCool, recalled). |
| T2: Stab(b^{±1}) = {±I, ±swap}; Stab(p_n^{±1}) = {±I} "(n ≥ 2)" | VERIFIED for b and for 3 ≤ n ≤ 7; **ERROR for n = 2** | β = (x ↦ xy⁻³, y ↦ y⁻¹) sends p₂ = x²y⁻³ to xy⁻³x ~ p₂, so Stab(p₂^{±1}) = {±I, ±β} has order 4 (TH02's "hidden reflection" of a T(2,q) relator). The stated consequence (only ±I fixes both relators of AK(n)) survives for n = 2, since β ∉ {±swap}. Correct wording: "Stab(p_n^{±1}) = {±I} for n ≥ 3; order 4 for n = 2". |
| T3: (κ, Ĵ) is a complete invariant of φ-twisted conjugacy in F/γ₅F; θ₀ flips κ, fixes Ĵ; θ₀(g) ≁ g for degree-1 g | VERIFIED (own level-by-level argument + TH11's Φ₄) | I−A and I+A are unimodular (levels 1, 3), level 2 gives ℤ/2 (φ acts by det A = −1 on γ₂/γ₃), and coker(I−Φ₄) ≅ ℤ exactly (gcd of the 2×2 minors of I−Φ₄ is 1; eigenvalues 1+λ², 0, 1+μ²); the stabilizer of a normal form z^κ·w₄ is γ₄ mod γ₅, so ℓ·[w₄] is well defined. The θ₀ statements were tested on 250 random words (not re-proved). Note Ĵ = J − κ in the script's normalization. |
| T4 (closed forms) | VERIFIED by computation: agreement on n ∈ [−40,60], s ∈ [−40,40]; on each class mod 4 the invariants are polynomials of degree ≤ 4 (Magnus coefficients), so ≥ 5 points per class suffice. |
| T5 (uniform O6: k_n ≁ xˢy for all n ≥ 3) | VERIFIED given T3, T4 | (s²−s−1)² = (n²−5n−7)² − 48(n+1) checked by expansion; my Runge bounds: no solution for n ≥ 31 or n ≤ −19; brute force \|n\| ≤ 2000 gives exactly TH11's list; (9,5) is excluded by my exact τ. Agrees with O6 (n ≤ 8) and with TH03's independent proof by a different invariant. |
| T6 (k_n ~ k_m iff n = m or {n,m} = {1,2}; k_n ≁ θ₀(k_m)) | VERIFIED given T3, T4 | Ĵ(k_n) is strictly decreasing for n ≥ 9 with Ĵ(k_9) = −15 below all earlier values; the only coincidences are (1,2) (a true conjugacy, O3) and (6,7) with different κ; the remaining case k₆ vs θ₀(k₇) (and k₇ vs θ₀(k₆)) is excluded by τ (both twists). |

**TH13, note version of 04:30 UTC (122 lines, §1–§4 written).** `python3 experiments/th20_th13_plateau.py k p` (own enumeration of *all* cyclically reduced words up to the claimed bounds, own torus invariant):
```
power side k=2 p=2: no word off the plateau for L <= 10;  L=11: 264 words (TH13's count)
power side k=2 p=3: plateau = 28 words at L=7; nothing else for L <= 12;  L=13: 624 words (claimed bound, attained)
braid side k=2 p=3, G_p and G_p': Orb(W_2) = 20 words at L=10; nothing else for L <= 11;  L=12: 144 words (claimed bound, attained)
k=1 p=3: power side first exit L=9 (432 words), braid side L=8 (32 words)   [J's numbers]
```

| claim | verdict | what I checked |
|---|---|---|
| T1 (F(a,b;i,j;m) trivial iff \|bi−aj\| = 1; admissible (i,j) give AC-equivalent presentations) | VERIFIED (proof read; (a) also re-derived for AK(k;p)) | y^{ja} = Δx^{ia}Δ⁻¹ = zⁱ = y^{bi}; (b): shifting (i,j) by l(a,b) multiplies both Artin sides by z^{l(2m+1)}; the free identity for A_m(α⁻¹,β⁻¹) checked by hand. |
| T2 (duality AK(k;p) ~AC (ψ_k(V_{k,p}), W_k), one W_k-frozen ACM move) | VERIFIED (own hand proof + own script k,p ≤ 8 + certificates) | see above; the three certificates start at AK(k;p) and end at (red ψ_k(V_{k,p}), W_k). Wording is correct: D(k;p) is reached only up to the automorphism ψ_k ("AC-trivial iff", by D2). |
| T3 (AK(k;2) ≅ AK(k) up to Aut; AK(2;2), AK(k;1) AC-trivial) | VERIFIED (G1 + D2/D3; certificates replay, starts (xxYYY, W₂), (xYY, W₂), (xYY, W₃), ends (x,y)). Not new information about AK(3). |
| T4 (plateau: first exit from AK(k;p), p ≥ 3, has cyclic length ≥ 2p+4k+3+min(4k−2, 2k+2, 2p−4)) | VERIFIED (Lemma P and Lemma B read line by line; brute force above) | Lemma P: zigzag table (xy)ⁱ = aⁱ, (xy)ⁱx = a^{i−k}Δ, … recomputed; case analysis (1)/(2) and the parity of 2J correct. Lemma B: M+N = 0 forces ν ∈ {0} ∪ [2,∞), and \|ε+om\| ≥ o−1. A statement about ACM paths, correctly labelled as not being evidence of non-triviality. |
| T5, T6, X7 | not yet written at 04:30 UTC — see final re-read below. |

## 7. TH16 (small cancellation; Miller–Schupp nodes as local minima of the ACM graph)

Version read: 04:35 UTC (≈ 25.8 kB). My checks: pieces recomputed with `th20_lib.pieces` and a star-graph triangle test; own Baumslag–Solitar conjugacy code `experiments/th20_bs.py` (Britton reduction + Collins + slide lattice with exact integrality test; self-test: invariance under conjugation and relator insertion, 3000 random cases); `python3 experiments/th20_th16_check.py`:
```
(A) BS(3,4), BS(4,3), BS(4,5), BS(5,4), w1 and w2: no conjugate of w_i^+-1 of length < 5; at L=5 exactly Orb(w_i) (10 words); L=6: 36 resp. 24 words
(B) n=3 (and n=4), G_w1 and G_w2: no conjugate of m_n^+-1 of length < 2n+3; at length 2n+3: 36 (44) words = Orb(m_n) u Orb(m_n')
(C) 34 benchmark targets (first relator ~ m_3^+-1 in F): {'w1': 17, 'w2': 17, 'other': 0} | w1 ~ w2^+-1 in BS(3,4): False
(D) m_n ~ p_n in B (n <= 8); b ~ w_1 in BS(n,n+1) (2 <= n <= 8)
```
Piece table recomputed (max piece, min # pieces, triangle): b (2,4,no), p₃ (3,4,no), c (2,4,yes), k₃ (2,6,yes), q₁ (1,6,yes), q₂ (2,6,yes), m₃ (3,5,yes), w₁,w₂ (1,5,yes); joint maximal pieces AK(3) 3, P₃ 3, Q 2, MS(3,w_i) 3 — **identical to TH16's table**; brute force: no non-power cyclically reduced word of length 3–9 satisfies C′(1/6).

| claim | verdict | what I checked |
|---|---|---|
| T1 (C′(1/6) forces \|r\| ≤ 2 or ≥ 13; C′(1/8): ≤ 2, 17, 18 or ≥ 25; C(6), C(4)–T(4) fail for the listed relators except C(6) for k₃, q₁, q₂) | VERIFIED | pigeonhole re-derived (2ℓ ≤ 4·3^μ); table recomputed. The small-cancellation hypotheses are *not* satisfied by any word the note works with, and the note says so and uses no small-cancellation theorem: the classical statements appear only in Remark 2 as "externally reported", (c) of that remark (thin-annulus theorem) is explicitly not used. |
| T2 (displacement lemma) | VERIFIED (two-line proof read) |
| T3 = Theorem A (shortest conjugates of w_i^{±1} in BS(P,Q), P,Q ≥ 3, P ≠ Q, are Orb(w_i); b ~ w₁ if Q = P+1) | VERIFIED (slide formula recomputed by hand: a′ = (−1+P(k₁−k₂), Qk₂−Pk₃, −1+Q(k₃−k₁)); brute force (A)); rests on Britton/Collins (classical, quoted). |
| T4 = Theorem B (shortest conjugates of m_n^{±1} in G_{w_i} have length 2n+3 and are Orb(m_n) ∪ Orb(m_n′), all n ≥ 3) | VERIFIED (proof read case by case: (n_x,n_y) list, loss table for the eight sign patterns, the equation ε₁ = −ε₂; brute force (B) for n = 3, 4). |
| T5 = Theorem C + Prop. D (MS(n,w_i) are plateaus/local minima of the ACM graph; AK(n) → (m_n,b) → MS(n,w₁) by two ACM moves) | VERIFIED given A, B; (D) recomputed (in B: Xyⁿx = yxⁿY, so m_n = y·p_n·Y). A statement about ACM paths only. |
| T6 (the 34 benchmark members are two ACM nodes) | VERIFIED by independent exact computation (C). |
| T7 (P₃, Q: method gives nothing; "Q local minimum" is necessary for AK(3) to be a counterexample) | PLAUSIBLE-UNCHECKED (the free-by-cyclic structures of G_{q₁}, G_{k₃} were not re-derived; the logical remark uses the externally reported classification of length ≤ 12). |

## 8. TH17 (T(2;p,q) as killers of the trefoil group; level shifts)

Version read: 04:34 UTC (≈ 16 kB; Theorems 1–5 read, Theorem 6 only skimmed). Certificates replayed (`th20_lib.cert_info`): `th17_c3_to_T2_4_7_one_move.json` (274 moves, (xxyXy, xy⁵xY²) → (x⁴y⁷, xxyXy)), `th17_r74member_to_T2_4_9.json` (374, (xxyXy, xy⁷xY²) → (x⁴y⁹, xxyXy)), `th17_T2_4_7_to_third_form.json` (189, (x⁴y⁷, xxyXy) → ((x²y)³(xy)⁻⁸ reduced, xxyXy)), `th17_T2_7_13_to_third_form.json` (574, (x⁷y¹³, xxyXy) → (…, xxyXy)) — all pass.

| claim | verdict | what I checked |
|---|---|---|
| 1 (dictionary: class of xᵖy^q in H = ⟨x,z \| x³z²⟩ is (k;1^q), (k;2·1^{q−1}), (k;2·1^{q−3}) for p = 3k+0,1,2) | VERIFIED (re-derived by hand: xᵖ(xz)^q with x³ = ζ, z² = ζ⁻¹) |
| 2 (Lemma S for a = 2 is the necklace identity) | VERIFIED (immediate from 1) |
| 3 (coincidences: only the Lemma S pairs; AK(n)'s killer class (0;2ⁿ1^{n+1}) is a T(2;·) class only for n = 1; xy^{2i+1}xY² ~ x⁴y^{2i+3}) | VERIFIED ((c) recomputed by hand: ζ(xz)^{2i+2}x²z; (a),(b) are necklace comparisons; "up to automorphisms" uses Out(H) = ℤ/2, classical, quoted) |
| 4 ((x²yXy, xy⁷xY²) ~AC T(2;4,9), a plain AC equivalence) | VERIFIED (certificate replay with endpoints checked + the conjugacy by hand) |
| 5 (family K(a,b,c): trivial iff \|a−b+6c\| = 1 and gcd(a,b) = 1; contains AK(n) and T(2;·)) | VERIFIED (own proof of the triviality criterion: modulo ζ, uᵃ = vᵇ and vᵃ = uᵇ are central, so gcd(a,b) = 1 makes the quotient abelian; d = gcd > 1 gives a (2,3,d) triangle quotient) |
| 6 (third torus form: x^{3k+1}y^q ~ (x²y)^{2k+1}(xy)^{−(q+1)} in H) | VERIFIED (braid computation Δ^{2k+1}u^{−(q+1)} = ζᵏuvu^{−q} ~ ζᵏvu^{−(q−1)} = Δ⁻¹(ζᵏuv^{−(q−1)})Δ re-done; ν(xyXyXy) = x²yXy by free reduction; two certificates replayed) |
| 7 (Theorem 6: rigidity of each level in the restricted graph 𝔖) | PLAUSIBLE-UNCHECKED (Lemmas 6.1–6.3 not verified for lack of time). The note labels it correctly as a statement about a restricted move class, **not** an AC invariant. |
| 8 (Prop. 5: a uniform level shift is equivalent to AC-triviality of all members; inequivalence of two levels would disprove AC) | VERIFIED (formal; level 0 has primitive killers xy, xy³) |

## 9. TH18 (killers of BS(n,n+1); Miller–Schupp classes; generalized AK pairs)

Version read: 04:35 UTC (≈ 26 kB). `python3 experiments/th20_th18_check.py` (own BS conjugacy code):
```
(1) n=2,3,4,5: t-length-3 killer classes with sigma=+1: 2, 6, 12, 20 (claimed n(n-1))
(1) n=2, t-length 5: necklace (+++--): 12 classes, (++-+-): 4 classes (claimed 12 + 4 = 2n^3(n-1) = 16)
(2) T4 class formula verified for n = 2,3,4 (all residues b', c'; a in [-2,2])
(3) bridge word in C_{2n+1} and Q_gamma classes, n = 2..8;   P_beta ~ x^2 y^b X y^-b with b = beta (mod n+1), b = 1 (mod n), n = 2..7
```
All 16 `th18_*.json` certificates replay; endpoints as stated (e.g. `th18_p2_to_ak_4_beta2.json`: (XyyxYYY, XXXYxxY) → (xxxxYYYYY, xYYxyyXY), 914 moves; `th18_p2_to_ak_5_betam2.json`: → (xxxxxYYYYYY, xyyxYYXY), 1547; `th18_ak3_beta1/beta2_trivialization.json`: (xxxYYYY, xYxyXY) resp. (xxxYYYY, xYYxyyXY) → (x,y); `th18_m3_to_ak3_via_t9.json`: (XyyyxYYYY, XYxxY) → (xxxYYYY, xyxYXY)). **None of them starts at AK(3) and ends at (x,y)**: "ak3_beta1/2" are the pairs AK₁(3), AK₂(3) with the torus relator x³y⁻⁴ and a *different* partner.

| claim | verdict | what I checked |
|---|---|---|
| T1 (killers of G_n = elements with σ = ±1; Miller–Schupp) | VERIFIED (classical proof re-derived: a power of y commutes with x = w, giving y^{n^{2k−1}} = 1, and yⁿ ~ y^{n+1} forces y = 1) |
| T2 (complete invariant: sign necklace + exponents mod Λ_d, index (n(n+1))^{(ℓ−1)/2}; class counts) | VERIFIED (lattice and its determinant ∏q_i − ∏p_i re-derived; well-definedness of Britton-reducedness mod Λ_d checked; counts confirmed by (1)); rests on Britton/Collins (classical, quoted) |
| T3 (primitive in the class ⇔ ℓ = 1 ⇔ w ~ x^{±1}) | VERIFIED (own proof: primitives are determined up to conjugacy in F by exponent vector, and xy^a ~ x) |
| T4 (ℓ = 3 classes C_b; membership criterion) | VERIFIED (own derivation: (a,b′,c′) ↦ (b′ mod n+1, c′ mod n) is a bijection ℤ³/Λ → ℤ/(n+1) × ℤ/n; script (2)) |
| T5 (bridge word XYx²Y ∈ C_{2n+1}; no primitive one ACM move from M_n) | VERIFIED (class by hand and script; other direction: a⁻¹(r_n) = p_n in B for a⁻¹ = (x ↦ xy), computed by hand, then G2(b)) |
| T6, T6′ (divisor classes are AC-trivial; sharpness for the representatives w_b) | VERIFIED (T6: both conjugations recomputed, incl. b \| n+1 via u = y^{−(n+1)}xy^{n+1}, u^{2^m} = x; T6′: amalgam length argument read) |
| T7 (MS(2,w), ℓ ≤ 3, AC-trivial; MS(3,w), ℓ ≤ 3, AC-trivial or ~ AK(3)) | VERIFIED (residue arithmetic mod 6, mod 12 redone; uses C's and D's certificates) |
| T8 (half classes are one ACM move from a T(2,m) pair) | VERIFIED for (a) by hand; (b) read only |
| T9 (MS(n,w) ~AC AK_β(n) = (xⁿy^{−(n+1)}, xy^{−β}xy^{β}x⁻¹y⁻¹) for w ∈ C_b^{±1}; AK₁(n) trivial; **holdout P2 ~AC AK₂(4) ~AC AK₋₂(5)**) | VERIFIED (own derivation: modulo P_β, x⁻¹yx = y^{−β}xy^{β}, so r_n = y^{−β}p_n y^{β}; certificates replayed with endpoints). **OVERCLAIM in wording:** AK₂(4) is called "a torus-knot pair" and advice 0 says "P2 is a torus-knot pair". In the project's usage (F §9, G, I) that means two torus-type relators; here only x⁴y⁻⁵ is of torus type — the Whitehead-minimal forms of P₂ = xy⁻²xy²x⁻¹y⁻¹ are x⁻²y⁻²xy and its relatives (4 syllables; `th20_stab` level graph), so P₂ is not a torus word. Correct wording: "P2's class contains a presentation whose first relator is the torus relator x⁴y⁻⁵ (resp. x⁵y⁻⁶)". These are equivalences; P2 remains open, as the note says. |

