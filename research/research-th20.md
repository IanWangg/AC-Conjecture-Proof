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

